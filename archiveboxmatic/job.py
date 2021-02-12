import logging
import subprocess
import datetime

logger = logging.getLogger(__name__)


def job(args, archive):
    logger.info(f"###### Processing archive {archive.name}")
    for i in archive.construct_commands():
        logger.info(f"Raw command : {i}")
        if not args.dry_run:
            run_command(i)


def job_monthly(args, archive):
    if datetime.datetime.now().day == 1:
        logger.info(f"###### Processing archive {archive.name}")
        for i in archive.construct_commands():
            logger.info(f"Raw command : {i}")
            if not args.dry_run:
                run_command(i)


def job_yearly(args, archive):
    if datetime.datetime.now().day == 1 and datetime.datetime.now().month == 1:
        logger.info(f"###### Processing archive {archive.name}")
        for i in archive.construct_commands():
            logger.info(f"Raw command : {i}")
            if not args.dry_run:
                run_command(i)


def run_command(command):
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        shell=True,
        text=True,
    )
    output, error = process.communicate()
