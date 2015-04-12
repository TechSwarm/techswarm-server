import os
import sys
import tsserver
from tsserver import configutils


def msg(s, end=''):
    if end == '':
        s += ' '
    print(s, file=sys.stderr, end=end)


def msg_line(s):
    msg(s, os.linesep)


#
# Uploads
#
def save_test():
    with open(os.path.join(upload_folder, test_filename), 'w') as f:
        f.write('test')


msg("Checking if files can be saved in upload directory...")
upload_folder = configutils.get_upload_dir()
test_filename = 'install-script-test-file.txt'

try:
    save_test()
except FileNotFoundError:
    msg("Directory does not exist, creating it...")
    os.makedirs(upload_folder, 0o744)
    save_test()
except PermissionError:
    msg("Directory is non-writable, trying to chmod it...")
    os.chmod(upload_folder, 0o744)
    save_test()
os.remove(os.path.join(upload_folder, test_filename))
msg_line("ok")

#
# Database
#
msg("Creating database...")
msg_line("Database URL: %s" % tsserver.db.engine.url)
tsserver.db.create_all()

#
# Finish
#
msg_line("Everything is done!")
