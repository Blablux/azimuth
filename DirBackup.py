#!/usr/bin/env python
"""This script is used to rsync a source directory to a target directory, with
    the option to exclude some files based on extension. Require modules
    `shutil`, `sh`, `logging`, `argparse` and `os`.

"""

import os
from shutil import rmtree
import argparse
import logging
from sh import rsync

# Parse arguments
parser = argparse.ArgumentParser(
    description=__doc__)

parser.add_argument("backupdir", help="Specify the directory to backup.")
parser.add_argument("destinationdir",
                    help="Specify the directory where the backup is stored.")
parser.add_argument("-t", "--trash",
                    help="Delete unnecessary files and empty the trash.",
                    action="store_true")
parser.add_argument("-e", "--exclude",
                    help="Exlude the following directories from backup.",
                    action="append")
parser.add_argument("-l", "--logfile",
                    help="Specify the logfile to monitor.")
parser.add_argument("-q", "--quiet",
                    help="Do not print to stdout.", action="store_true")

args = parser.parse_args()

# Redefine variables
sourcedir = args.backupdir
targetdir = args.destinationdir
logfile = args.logfile

# Logging
rootLogger = logging.getLogger()
logFormatter = logging.Formatter("%(asctime)s - %(message)s")
rootLogger.setLevel(logging.INFO)
if logfile:
    fileHandler = logging.FileHandler(logfile)
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

if not args.quiet:
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)


def check_dir_exist(os_dir):
    # Directory exist-check
    if not os.path.exists(os_dir):
        logging.error("{} does not exist.".format(os_dir))
        exit(1)

check_dir_exist(sourcedir)


def delete_files(ending, indirectory):
    # Delete function
    for r, d, f in os.walk(indirectory):
        for files in f:
            if files.endswith("." + ending):
                try:
                    os.remove(os.path.join(r, files))
                    logging.info("Deleting {}/{}".format(r, files))
                except OSError:
                    logging.warning("Could not delete {}/{}".format(r, files))
                    pass

# Delete actual files first
if args.trash:
    file_types = ["tmp", "bak", "dmp"]
    for file_type in file_types:
        delete_files(file_type, sourcedir)
    # Empty trash can
    try:
        rmtree(os.path.expanduser("~/.local/share/Trash/files"))
    except OSError:
        logging.warning("Could not empty the trash or trash already empty.")
        pass

# Handle exclusions
exclusions = []
if args.exclude:
    for argument in args.exclude:
        exclusions.append("--exclude={}".format(argument))

# Rsync files
logging.info("Starting rsync.")
if logfile and exclusions and args.quiet:
    rsync("-auhv", exclusions, "--log-file={}".format(logfile), sourcedir,
          targetdir)
elif logfile and exclusions:
    print(rsync("-auhv", exclusions, "--log-file={}".format(logfile),
          sourcedir, targetdir))
elif args.quiet and exclusions:
    rsync("-av", exclusions, sourcedir, targetdir)
elif logfile and args.quiet:
    rsync("-av", "--log-file={}".format(logfile), sourcedir, targetdir)
else:
    rsync("-av", sourcedir, targetdir)

logging.info("done.")
