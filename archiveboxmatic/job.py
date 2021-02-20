import logging
import subprocess
import datetime
from archiveboxmatic import ArchiveboxmaticArchive

logger = logging.getLogger(__name__)


def job(args, global_config, archive_config):
    archive = ArchiveboxmaticArchive(global_config, archive_config)
    logger.debug(f"###### Processing archive {archive.name}")
    for i in archive.build_commands():
        logger.debug(f"Raw command : {i}")
        if not args.dry_run:
            run_command(i)


def job_monthly(args, global_config, archive_config):
    if datetime.datetime.now().day == 1:
        archive = ArchiveboxmaticArchive(global_config, archive_config)
        logger.debug(f"###### Processing archive {archive.name}")
        for i in archive.build_commands():
            logger.debug(f"Raw command : {i}")
            if not args.dry_run:
                run_command(i)


def job_yearly(args, global_config, archive_config):
    if datetime.datetime.now().day == 1 and datetime.datetime.now().month == 1:
        archive = ArchiveboxmaticArchive(global_config, archive_config)
        logger.debug(f"###### Processing archive {archive.name}")
        for i in archive.build_commands():
            logger.debug(f"Raw command : {i}")
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
