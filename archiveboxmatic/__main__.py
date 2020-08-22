"""
ArchiveBoxMatic: Configure ArchiveBox with the simplicity of a yaml file.
"""
import logging
import time
import argparse
from yaml import load, Loader
import subprocess


logger = logging.getLogger()
start_time = time.time()


class ArchiveboxmaticArchive:
    def __init__(self, config, archive):
        self.name = archive["name"]
        self.is_schedule = True if "schedule" in archive else False
        self.schedule = archive['schedule'] if "schedule" in archive else "none"
        self.environment = f"{' '.join(config['archivebox']['environment'])} bash -c '"
        self.path = config["archivebox"]["path"]
        self.sources = archive["sources"]
        self.path = config["archivebox"]["path"]
        self.archivebox_command = self.construct_archivebox_command(config, archive)

    def construct_archivebox_command(self, config, archive):
        default_command = f"archivebox add --depth={archive['depth']}"
        if config["archivebox"]["method"] == "docker-compose":
            return (
                f"docker-compose run {default_command}"
            )
        elif config["archivebox"]["method"] == "python":
            return (
                f"{default_command}"
            )
        else:
            raise ("Problem in construct_archivebox_command.")

    def construct_commands(self):
        # text_files
        if "text_files" in self.sources:
            for i in self.sources["text_files"]:
                yield f"{self.environment} cd {self.path} && cat {i} | {self.archivebox_command}'"
        # shaarli
        if "shaarli" in self.sources:
            for i in self.sources["shaarli"]:
                yield f"{self.environment} cd {self.path} && cat {i} | {self.archivebox_command}'"
        # reddit_saved
        if "reddit_saved" in self.sources:
            for i in self.sources["reddit_saved"]:
                yield f"{self.environment} cd {self.path} && cat {i} | {self.archivebox_command}'"
        # firefox_bookmarks
        if "firefox_bookmarks" in self.sources:
            for i in self.sources["firefox_bookmarks"]:
                yield f"{self.environment} cd {self.path} && cat {i} | {self.archivebox_command}'"
        # firefox_history
        if "firefox_history" in self.sources:
            for i in self.sources["firefox_history"]:
                yield f"{self.environment} cd {self.path} && cat {i} | {self.archivebox_command}'"


def run_command(command):
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        shell=True,
        text=True,
        # executable="/bin/bash",
    )
    output, error = process.communicate()


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
    args = parse_args()
    config = read_config(args.config_file)
    # Check if config is valid with the selected arguments.
    if not validate_config(config, args):
        raise Exception("Config is not valid.")

    # with open("ArchiveboxMatic.sh", "w") as f:
    #     f.write("#!/usr/bin/env bash\n")
    #     for i in config["archives"]:
    #         archive = ArchiveboxmaticArchive(config, i)
    #         logger.debug(f"###### Processing archive {archive.name}")

    #         for j in archive.construct_commands():
    #             # logger.debug(j)
    #             # run_command(j)
    #             f.write(f"{j}\n")
    allowed_schedules = [args.schedule] if args.schedule != "all" else ["daily","weekly","monthly","yearly","none"]

    for i in config["archives"]:
        archive = ArchiveboxmaticArchive(config, i)
        logger.info(f"###### Processing archive {archive.name}")

        if archive.schedule in allowed_schedules:
            for j in archive.construct_commands():
                logger.info(f"Raw command : {j}")
                run_command(j)

    logger.info("Runtime : %.2f seconds." % (time.time() - start_time))


def parse_args():
    format = "%(levelname)s :: %(message)s"
    parser = argparse.ArgumentParser(description="ArchiveBoxMatic: configure ArchiveBox with the simplicity of a yaml file.")
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
        default="all"
    )
    parser.set_defaults(boolean_flag=False)
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel, format=format)
    return args


if __name__ == "__main__":
    main()
