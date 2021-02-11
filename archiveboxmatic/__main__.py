"""
ArchiveBoxMatic: Configure ArchiveBox with the simplicity of a yaml file.
"""
import logging
import argparse
import schedule
import datetime
import time
from yaml import load, Loader
from archiveboxmatic import ArchiveboxmaticArchive
from job import job, job_monthly, job_yearly

logger = logging.getLogger()


# TODO Add config file validation.
def validate_config(config, args):
    return True


def read_config(config_file):
    try:
        with open(config_file, "r") as f:
            config = load(f, Loader=Loader)
    except Exception as e:
        logger.error(e)
    return config


def main():
    logger.info("Archiveboxmatic is running.")
    args = parse_args()
    config = read_config(args.config_file)
    # Check if config is valid with the selected arguments.
    if not validate_config(config, args):
        raise Exception("Config is not valid.")

    allowed_schedules = (
        [args.schedule]
        if args.schedule != "all"
        else ["daily", "weekly", "monthly", "yearly", "none"]
    )

    for i in config["archives"]:
        archive = ArchiveboxmaticArchive(config, i)

        if archive.schedule in allowed_schedules:
            if archive.schedule == "daily":
                schedule.every().day.at("12:00").do(job, args=args, archive=archive)
            if archive.schedule == "weekly":
                schedule.every().monday.at("10:00").do(job, args=args, archive=archive)
            if archive.schedule == "monthly":
                schedule.every().day.at("05:00").do(
                    job_monthly, args=args, archive=archive
                )
            if archive.schedule == "yearly":
                schedule.every().day.at("01:00").do(
                    job_yearly, args=args, archive=archive
                )
            if archive.schedule == "none":
                job(args, archive)

    while True:
        schedule.run_pending()
        time.sleep(60)
        logger.debug(f"Next job in {schedule.next_run() - datetime.datetime.now()}.")


def parse_args():
    format = "%(levelname)s :: %(message)s"
    parser = argparse.ArgumentParser(
        description="ArchiveBoxMatic: configure ArchiveBox with the simplicity of a yaml file."
    )
    parser.add_argument(
        "--debug",
        help="Display debugging information.",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.INFO,
    )
    parser.add_argument(
        "-c",
        "--config_file",
        help="Config file (default: ./config.yaml).",
        type=str,
        default="config.yaml",
    )
    parser.add_argument(
        "-s",
        "--schedule",
        help="Only run scheduled tasks for a specific timeframe (Choices: daily, weekly, monthly, yearly, all. Default: all).",
        type=str,
        default="all",
    )
    parser.add_argument(
        "--dry-run",
        help="Run the script without starting the archive process. Can be used to validate the config file.",
        dest="dry_run",
        action="store_true",
    )
    parser.set_defaults(dry_run=False)
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel, format=format)
    return args


if __name__ == "__main__":
    main()
