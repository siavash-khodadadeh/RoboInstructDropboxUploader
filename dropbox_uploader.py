from os import listdir
from os.path import join, isfile
from datetime import datetime

import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError

import settings


dbx = dropbox.Dropbox(settings.DROPBOX_ACCESS_TOKEN)


def _backup_file(local_file, backup_path):
    with open(local_file, 'rb') as f:
        print("Uploading " + local_file + " to Dropbox as " + backup_path + "...")
        try:
            dbx.files_upload(f.read(), backup_path, mode=WriteMode('overwrite'))
        except ApiError as err:
            if (err.error.is_path() and
                    err.error.get_path().error.is_insufficient_space()):
                print('Not enough space in dropbox')
            elif err.user_message_text:
                print(err.user_message_text)
            else:
                print(err)


def backup(directory):
    for file_name in (f for f in listdir(directory) if isfile(join(directory, f))):
        today = datetime.now()
        destination_folder = str(today.year) + "_" + str(today.month) + "_" + str(today.day) + '/'
        destination_address = join(settings.DROPBOX_DIRECTORY, destination_folder, file_name)
        _backup_file(join(directory, file_name), destination_address)


backup(settings.LOCAL_DIRECTORY)
