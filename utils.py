from yaml import safe_load
import os


def get_config(filename='config.yml'):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    instance_dir_path = '/'.join([dir_path, 'instance'])
    file_path = '/'.join([dir_path, 'instance', filename])

    if os.path.isdir(instance_dir_path):
        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                return safe_load(f)
        else:
            return FileNotFoundError('The filename was not found in the '
                                     'instance directory.')
    else:
        return NotADirectoryError('The instance directory does not exist.')
