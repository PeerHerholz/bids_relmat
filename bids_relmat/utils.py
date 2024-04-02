import os
from shutil import copyfile
import importlib_resources
import json
import sys


# define function to check path
def check_path(path):
    """
    Check if paths exist, if not create them.

    Parameters
    ----------
    path : str
        Path to that should be created.

    Examples
    --------
    Check if the indicated sourcedata directory exists in the current directory.

    >>> check_output_path(os.curdir + '/bids_dataset/sourcedata')

    Check if the indicated sourcedata directory exists at a given path, for
    example, the user's Desktop.

    >>> check_output_path('/home/user/Desktop/BIDS_dataset/sourcedata')
    """

    if os.path.isdir(path) is False:
        os.makedirs(path)


# define function to check output path for relmat template files
def check_output_path_relmat_templates(path):
    """
    Check if the desired sourcedata path to save the relmat templates exists and if not,
    create it.

    Parameters
    ----------
    path : string
        Path to sourcedata directory where the relmat template files will be saved.

    Returns
    -------
    path : PosixPath
        A PosixPath indicating the path to the relmat files.

    Examples
    --------
    Check if the directory exists at a given path, for
    example, the user's Desktop.

    >>> check_output_path('/home/user/Desktop/BIDS_dataset')
    """

    # generate full path to relmat files based on indicated directory name
    relmat_path = os.path.abspath(path) + '/sourcedata/BIDS_relmat_templates'

    # check if the path exists and if not create it
    if os.path.isdir(relmat_path) is False:

        # create the path if it doesn't exist
        os.makedirs(relmat_path)

        # print an informative message where the atlas will be provided
        print('relmat files will be saved to %s' % relmat_path)

    return relmat_path


def generate_json_sidecar_file(relmat_path):
    """
    Create relmat .json metadata template files at specified
    sourcedata directory.

    Parameters
    ----------
    relmat_path : str or PosixPath
        A string or PosixPath indicating the path to the sourcedata directory the relmat files
        should be saved in.

    Returns
    -------
    Generated relmat .json metadata template files in the specified directory.

    Examples
    --------
    Create relmat .json metadata template files.

    >>> generate_json_sidecar_file('/home/user/BIDS_dataset/sourcedata/BIDS_relmat_templates')
    """

    # get metadata
    json_metadata_relmat = importlib_resources.files(__name__).joinpath('data/relmat_template.json')

    relmat_path_json = relmat_path + '/relmat_template.json'

    # copy the files to the required directory
    copyfile(json_metadata_relmat, relmat_path_json)

    return relmat_path_json


def validate_input_dir(exec_env, bids_dir, participant_label=None):
    """
    Validate BIDS directory and structure via the BIDS-validator.
    Functionality copied from fmriprep.

    Parameters
    ----------
    exec_env : str
        Environment BIDSonym is run in.
    bids_dir : str
        Path to BIDS root directory.
    participant_label: str
        Label(s) of subject to be checked (without 'sub-').
    """

    import tempfile
    import subprocess
    validator_config_dict = {
        "ignore": [
            "EVENTS_COLUMN_ONSET",
            "EVENTS_COLUMN_DURATION",
            "TSV_EQUAL_ROWS",
            "TSV_EMPTY_CELL",
            "TSV_IMPROPER_NA",
            "VOLUME_COUNT_MISMATCH",
            "BVAL_MULTIPLE_ROWS",
            "BVEC_NUMBER_ROWS",
            "DWI_MISSING_BVAL",
            "INCONSISTENT_SUBJECTS",
            "INCONSISTENT_PARAMETERS",
            "BVEC_ROW_LENGTH",
            "B_FILE",
            "PARTICIPANT_ID_COLUMN",
            "PARTICIPANT_ID_MISMATCH",
            "TASK_NAME_MUST_DEFINE",
            "PHENOTYPE_SUBJECTS_MISSING",
            "STIMULUS_FILE_MISSING",
            "DWI_MISSING_BVEC",
            "EVENTS_TSV_MISSING",
            "TSV_IMPROPER_NA",
            "ACQTIME_FMT",
            "Participants age 89 or higher",
            "DATASET_DESCRIPTION_JSON_MISSING",
            "FILENAME_COLUMN",
            "WRONG_NEW_LINE",
            "MISSING_TSV_COLUMN_CHANNELS",
            "MISSING_TSV_COLUMN_IEEG_CHANNELS",
            "MISSING_TSV_COLUMN_IEEG_ELECTRODES",
            "UNUSED_STIMULUS",
            "CHANNELS_COLUMN_SFREQ",
            "CHANNELS_COLUMN_LOWCUT",
            "CHANNELS_COLUMN_HIGHCUT",
            "CHANNELS_COLUMN_NOTCH",
            "CUSTOM_COLUMN_WITHOUT_DESCRIPTION",
            "ACQTIME_FMT",
            "SUSPICIOUSLY_LONG_EVENT_DESIGN",
            "SUSPICIOUSLY_SHORT_EVENT_DESIGN",
            "MALFORMED_BVEC",
            "MALFORMED_BVAL",
            "MISSING_TSV_COLUMN_EEG_ELECTRODES",
            "MISSING_SESSION"
        ],
        "error": ["NO_T1W"],
        "ignoredFiles": ['/dataset_description.json', '/participants.tsv']
    }
    # Limit validation only to data from requested participants
    if participant_label:
        all_subs = set([s.name[4:] for s in bids_dir.glob('sub-*')])
        selected_subs = set([s[4:] if s.startswith('sub-') else s
                             for s in participant_label])
        bad_labels = selected_subs.difference(all_subs)
        if bad_labels:
            error_msg = 'Data for requested participant(s) label(s) not found. Could ' \
                        'not find data for participant(s): %s. Please verify the requested ' \
                        'participant labels.'
            if exec_env == 'docker':
                error_msg += ' This error can be caused by the input data not being ' \
                             'accessible inside the docker container. Please make sure all ' \
                             'volumes are mounted properly (see https://docs.docker.com/' \
                             'engine/reference/commandline/run/#mount-volume--v---read-only)'
            if exec_env == 'singularity':
                error_msg += ' This error can be caused by the input data not being ' \
                             'accessible inside the singularity container. Please make sure ' \
                             'all paths are mapped properly (see https://www.sylabs.io/' \
                             'guides/3.0/user-guide/bind_paths_and_mounts.html)'
            raise RuntimeError(error_msg % ','.join(bad_labels))

        ignored_subs = all_subs.difference(selected_subs)
        if ignored_subs:
            for sub in ignored_subs:
                validator_config_dict["ignoredFiles"].append("/sub-%s/**" % sub)
    with tempfile.NamedTemporaryFile('w+') as temp:
        temp.write(json.dumps(validator_config_dict))
        temp.flush()
        try:
            subprocess.check_call(['bids-validator', bids_dir, '-c', temp.name])
        except FileNotFoundError:
            print("bids-validator does not appear to be installed", file=sys.stderr)
