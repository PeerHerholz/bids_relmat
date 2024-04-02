import argparse
import os
from pathlib import Path
from shutil import copytree
from bids import BIDSLayout
from bids_relmat.utils import (check_path, validate_input_dir,
                               generate_json_sidecar_file, check_output_path_relmat_templates)
from bids_relmat.conversion import add_relmat_metadata_subject_json


# define parser to collect required inputs
def get_parser():

    __version__ = open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                    '_version.py')).read()

    class MaxListAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            if len(values) > 2:
                raise argparse.ArgumentError(self, "maximum length of list is 2")
            setattr(namespace, self.dest, values)

    parser = argparse.ArgumentParser(description='a CLI for easing up the conversion from BIDS to BIDS-NBS datasets')
    parser.add_argument('bids_dir', action='store', type=Path, help='The directory where the to-be-updated BIDS-compliant dataset is stored.')
    parser.add_argument('analysis_level', help='Level of the analysis that will be performed. '
                        'Multiple participant level analyses can be run independently '
                        '(in parallel) using the same output_dir.',
                        choices=['participant', 'group'], nargs='?')
    parser.add_argument('--participant_label',
                        help='The label(s) of the participant(s) that should be analyzed. '
                        'The label corresponds to sub-<participant_label> from the BIDS spec '
                        '(so it does not include "sub-"). If this parameter is not '
                        'provided all subjects should be analyzed. Multiple '
                        'participants can be specified with a space separated list.',
                        nargs="+")
    parser.add_argument('--get_relmat_files',
                        help='Indicating if relmat metadata template files should be stored under sourcedata in the specified BIDS dataset'
                        'for subsequent metadata information denotation and usage during the conversion.', default=False, action="store_true")
    parser.add_argument('--new_bids_dir', action='store', type=Path, help='The directory where the new BIDS relmat compliant dataset should be stored, in case metadata should not be changed in-place.')
    parser.add_argument('--skip_bids_validation', default=False,
                        help='Assume the input dataset is BIDS compliant and skip the validation \
                             (default: False).',
                        action="store_true")
    parser.add_argument('-v', '--version', action='version',
                        version='BIDS-NBS version {}'.format(__version__))
    return parser


# define the CLI
def run_bids_relmat():

    # get arguments from parser
    args = get_parser().parse_args()

    # special variable set in the container
    if os.getenv('IS_DOCKER'):
        exec_env = 'singularity'
        cgroup = Path('/proc/1/cgroup')
        if cgroup.exists() and 'docker' in cgroup.read_text():
            exec_env = 'docker'
    else:
        exec_env = 'local'

    # check if BIDS validation should be run
    if args.skip_bids_validation:
        print("Input data will not be checked for BIDS compliance.")
    else:
        print("Making sure the input data is BIDS compliant "
              "(warnings can be ignored in most cases).")
        validate_input_dir(exec_env, args.bids_dir)

    # check if BIDS relmat compliant data should be saved in a newly created directory
    # get_relmat_file and new_bids_dir should be used together
    if not args.get_relmat_files and args.new_bids_dir:

        print('--new_bids_dir can only be used in combination with --get_relmat_files and not during the actual conversion')
        print('to prevent a missing link between the added/adapted metadata in the BIDS relmat dataset and their source in the')
        print('BIDS relmat template files. If you created a new BIDS directory in step 1, please use this as input.')

    # check if nbs_files should be saved in new BIDS directory
    elif args.new_bids_dir:

        # print some helpful/informative messages
        print("BIDS relmat files will be saved in a new BIDS directory: %s" % args.new_bids_dir)
        print("Thus, files in the original dataset will not be adapted in-place.")

        # check if new BIDS directory path already exists
        # if not create it
        check_path(args.new_bids_dir)

        # copy all files from existing BIDS directory to new one
        copytree(args.bids_dir, args.new_bids_dir, dirs_exist_ok=True)

        # assign BIDS directory
        bids_dir_run = args.new_bids_dir

    # no new BIDS directory will be created
    else:

        # print some helpful/informative messages
        print("Files in the original dataset will be adapted in-place.")

        # assign BIDS directory
        bids_dir_run = args.bids_dir

    # check if Step 1 should be run, ie relmat template files
    if args.get_nbs_files:

        # check if new relmat template files directory path already exists
        # if not create it
        relmat_template_path = check_output_path_relmat_templates(bids_dir_run)

        # get relmat template files and save them in indicated BIDS directory
        generate_json_sidecar_file(relmat_template_path)

    # if not, the conversion should be run
    elif not args.get_nbs_files and not args.new_bids_dir:

        # initialize BIDS dataset layout
        layout = BIDSLayout(bids_dir_run, derivatives=True)

        # initialize empty subject list
        subjects_to_analyze = []

        # check analysis level and gather subject list
        if args.analysis_level == "participant":
            if args.participant_label:
                subjects_to_analyze = args.participant_label
            else:
                print("No participant label indicated. Please do so.")
        else:
            subjects_to_analyze = layout.get(return_type='id', target='subject')

        print('The following subjects will be processed: %s' % subjects_to_analyze)

        # check if indicated participants are missing and if so, provide a list of them
        list_part_prob = []
        for part in subjects_to_analyze:
            if part not in layout.get_subjects():
                list_part_prob.append(part)
        if len(list_part_prob) >= 1:
            raise Exception("The participant(s) you indicated are not present in the BIDS dataset, please check again."
                            "This refers to: %s" % list_part_prob)

        # gather sessions that should be analyzed and provide a respective update
        sessions_to_analyze = layout.get(return_type='id', target='session')

        if not sessions_to_analyze:
            print('Processing data from one session.')
        else:
            print('Processing data from %s sessions:' % str(len(sessions_to_analyze)))
            print(sessions_to_analyze)

        # check if relmat files exist and if not, raise an Exception
        relmat_metadata_tpl = str(bids_dir_run) + '/sourcedata/BIDS_relmat_templates/relmat_template.json'

        # error if event files do not exist at indicated path
        if not os.path.exists(relmat_metadata_tpl):
            print('No relmat metadata template found at: %s' % relmat_metadata_tpl)
            print('Please check again and make sure to run step 1, ie --get_relmat_files first.')
            raise OSError

        # loop over subjects and run output conversion
        for subject_label in subjects_to_analyze:
            # get needed files and check if data from multiple sessions should be gathered
            if not sessions_to_analyze:
                list_relmat = layout.get(subject=subject_label, extension='tsv',
                                         suffix='relmat', return_type='filename')
            else:
                list_relmat = layout.get(subject=subject_label, extension='tsv',
                                         suffix='relmat', return_type='filename',
                                         session=sessions_to_analyze)

            # loop over found event.json files, applying conversion
            for relmat_file in list_relmat:

                # apply relmat conversion
                print('Creating the following _relmat.json: %s' % relmat_file)

                add_relmat_metadata_subject_json(relmat_file, relmat_metadata_tpl,
                                                 bids_dir_run, subject_label)


# run the CLI
if __name__ == "__main__":

    run_bids_relmat()
