import os
import json
from shutil import copy
from bids_relmat.utils import check_path


def add_relmat_metadata_subject_json(sub_relmat_json, template_relmat_json,
                                     bids_dir, sub_id):
    """
    Add relmat metadata from templates to existing relmat.json files.

    Parameters
    ----------
    sub_relmat_json : str or PosixPath
        A string or PosixPath indicating the path to the existing relmat.json file.
    template_relmat_json : str or PosixPath
        A string or PosixPath indicating the path to the Relmat template metadata file.

    Returns
    -------
    Updated relmat metadata.

    Examples
    --------
    Add relmat metadata from templates to existing relmat.json files.

    >>> add_relmat_metadata_subject_json('/home/user/BIDS_dataset/derivatives/sub-01/func/sub-01_tasl-rest_relmat.json',
                                         '/home/user/BIDS_dataset/sourcedata/BIDS_relmat_templates/relmat_template.json')
    """

    # check if subject relmat.json already exists
    # if so, add template data to it
    if os.path.exists(sub_relmat_json):

        # open both files
        with open(sub_relmat_json, 'r') as sub_relmat_json:
            sub_relmat_data = json.load(sub_relmat_json)

        with open(template_relmat_json, 'r') as template_relmat_json_tpl:
            template_relmat_json_tpl_data = json.load(template_relmat_json_tpl)

        # copy existing relmat.json to sourcedata as a backup
        if 'ses-' in sub_relmat_json:
            ses_s = sub_relmat_json.find('ses-')+4
            ses_e = sub_relmat_json.find('/', ses_s)
            ses_id = sub_relmat_json[ses_s: ses_e]
            sub_bu_path = str(bids_dir) + '/sourcedata/BIDS_pre_relmat_backup/sub-%s/ses-%s/' % (sub_id, ses_id)
        else:
            sub_bu_path = str(bids_dir) + '/sourcedata/BIDS_pre_relmat_backup/sub-%s/' % sub_id

        check_path(sub_bu_path)
        copy(sub_relmat_json, sub_bu_path + sub_relmat_json.split('/')[-1])
        os.remove(sub_relmat_json)

        # add template metadata to existing relmat.json
        sub_relmat_data.update(template_relmat_json_tpl_data)

        # overwrite existing relmat.json file with updated data
        with open(sub_relmat_json, 'w') as output_file:
            json.dump(sub_relmat_data, output_file, indent=4)

    # if not, a subject relmat.json file will created from the template data
    else:

        # use template data to create subject relmat.json
        with open(template_relmat_json, 'r') as sub_relmat_json:
            sub_relmat_data = json.load(sub_relmat_json)

        # save subject relmat.json file
        with open(sub_relmat_json, 'w') as output_file:
            json.dump(sub_relmat_data, output_file, indent=4)

    return sub_relmat_data
