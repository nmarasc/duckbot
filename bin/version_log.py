'''Keep a log of new and modified files.

Scrape the output of git status for new and modified files and append
those results to a log for latter recall.

'''
import os
import subprocess
from pathlib import Path

git_top = ['git', 'rev-parse', '--show-toplevel']
# git status is used over git ls-files because the latter will
# only show files before staging. Using status to see staged files
# allows this to be run in a pre-commit hook.
git_status = ['git', 'status', '--short']

# Change context to root of project
root_dir = subprocess.check_output(git_top)
os.chdir(root_dir.strip())

log_dir = os.path.join(os.getcwd(), '.log')
log_new = os.path.join(log_dir, 'new.log')
log_mod = os.path.join(log_dir, 'mod.log')

# Create log dir if it does not already exist, make sure log files exist
try:
    os.mkdir(log_dir)
    Path(log_new).touch()
    Path(log_mod).touch()
except FileExistsError:
    pass

# Read in previous values
with open(log_new) as f:
    old_new = set(f.read().splitlines())
with open(log_mod) as f:
    old_mod = set(f.read().splitlines())

# Capture new and modified files
status = subprocess.check_output(git_status).splitlines()
new = set([item.split()[1] for item in status if item.split()[0] == b'A'])
mod = set([item.split()[1] for item in status if item.split()[0] == b'M'])

# Combine with previous values
new |= old_new
# Since it's possible that multiple commits will happen before any push,
# the modified set needs to be checked for anything marked as new. This
# prevents trying to update a non existent 'Last Updated' line
mod = (mod | old_mod) - new

# Write out values to the logs files
with open(log_new, 'w') as f:
    for item in new:
        f.write(f'{item}\n')
with open(log_mod, 'w') as f:
    for item in mod:
        f.write(f'{item}\n')

print('new:')
for item in new: print(item)
print('mod:')
for item in mod: print(item)
