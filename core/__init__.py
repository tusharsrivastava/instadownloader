import os
import subprocess

FILE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_version_from_git():
    try:
        return subprocess.check_output(['git', 'describe', '--tags'],
                                       cwd=FILE_DIR).decode('utf-8').strip()
    except Exception:
        return '?'


VERSION = get_version_from_git()

default_app_config = 'core.apps.CoreConfig'
