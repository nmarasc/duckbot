#!/bin/bash
rc=0
usage="usage: $0 [-h] [-f | -u <version-number>]
       \t-f, --freeze\t- Freeze changed or added files for updating later
       \t-u, --update\t- Apply updated version number to frozen files
       \t-h, --help\t- Display usage information"
VERSION_RE='^[0-9]+.[0-9]+(.[0-9]+)?$'
POSITIONAL=()
FREEZE=0
UPDATE=0
UPDATE_VAL=
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'
PROJECT_DIR=`git rev-parse --show-toplevel`
LOG_DIR=".version_log"
NEW="$LOG_DIR/new.txt"
MOD="$LOG_DIR/modified.txt"

# Set command line options
function parseOps {
  while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
      -f|--freeze) # Save changed/new files for updating
        FREEZE=1
        shift
      ;;
      -u|--update) # Make the change
        UPDATE=1
        UPDATE_VAL="$2"
        shift
        shift
      ;;
     -h|--help) # Display usage
        echo -e "$usage"
        popd ; exit 0
      ;;
      *) # Unknown argument
        POSITIONAL+=("$1")
        shift
      ;;
    esac
  done
  set -- "${POSITIONAL[@]}"
}

# Save new and modified files to update later
function freeze {
  # Do the saves
  git ls-files -m >> "$MOD"
  git ls-files -o --exclude-standard >> "$NEW"
  # Remove any duplicates
  sort -u "$MOD" -o "$MOD"
  sort -u "$NEW" -o "$NEW"
}

# Change the last updated on each file modified or add one for new files
function update {
  # Change modified
  cat "$MOD" | xargs sed -ri "s/^.*Last Updated: [0-9]+\.[0-9]+(\.[0-9]+)?$/$1/"
  # Add new
  cat "$NEW" | xargs sed -i "1s/^/$1\n/"
  # Modify README
  "${VISUAL:-${EDITOR:-vi}}" README.md
}

pushd "$PROJECT_DIR" > /dev/null || exit 1
if ! [ -d "$LOG_DIR" ]; then
  mkdir "$LOG_DIR"
fi
if [ $# -eq 0 ]; then
  echo -e "warn: No arguments supplied, showing saved change list\n"
  if [ -f "$MOD" ]; then
    echo -e "Modified:${YELLOW}"
    cat "$MOD" | xargs -L1 echo -e "\t"
    echo -e "${NC}"
  else
    echo "No modified files"
  fi
  if [ -f "$NEW" ]; then
    echo -e "New:${RED}"
    cat "$NEW" | xargs -L1 echo -e "\t"
    echo -e "${NC}"
  else
    echo "No new files"
  fi
else
  parseOps $@
  checksum=$(($FREEZE + $UPDATE))
  # Used mutual exclusive arguments
  if [ $checksum -gt 1 ]; then
    echo "error: update and freeze are mutually exclusive"
    rc=2
  # No version number provided
  elif [[ ($UPDATE -eq 1 ) && (-z $UPDATE_VAL) ]]; then
    echo "error: no version number provided for update"
    rc=3
  # Freeze selected
  elif [ $FREEZE -eq 1 ]; then
    echo "Freezing new and modified files for version update"
    freeze
  # Update selected
  elif [ $UPDATE -eq 1 ]; then
    if ! [[ $UPDATE_VAL =~ $VERSION_RE ]]; then
      echo "error: version was not of a valid format"
      echo -e "           major.minor[.hotfix] e.g. 1.0, 2.1.2"
      rc=4
    else
      echo "Updating frozen files to new version"
      text="# Last Updated: $UPDATE_VAL"
      update "$text"
    fi
  # Something bad happened, should never reach this
  else
    echo "error: nothing selected, exiting"
    rc=5
  fi
fi
popd > /dev/null || exit 6
exit $rc
