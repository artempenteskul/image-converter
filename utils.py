import os
import uuid

from enum import Enum

UPLOAD_FOLDER = 'media'


# check int enum in order to make enum with keys 100, 75, 50, 25
class QualityEnum(Enum):
    HUNDRED = '100'
    SEVENTY_FIVE = '75'
    FIFTY = '50'
    TWENTY_FIVE = '25'


def generate_id_for_file() -> str:
    # here we need to add check whether we already use this uuid or not
    # we can implement it using listdir all folders in original folder and compare existing ids with our
    return str(uuid.uuid4())


def get_filename_from_file_id(file_id: str) -> str:
    if os.path.exists(os.path.join(UPLOAD_FOLDER, '100', file_id)):
        files_in_folder = os.listdir(os.path.join(UPLOAD_FOLDER, '100', file_id))
        if len(files_in_folder) > 1:
            # probably we need to add better explanation for exception here
            raise Exception('Multiple files for one id.')
        filename = files_in_folder[0]
        return filename
    else:
        # here we need to add better explanation for exception
        raise Exception('Unknown files route.')
