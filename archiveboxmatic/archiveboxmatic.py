import logging
import time

logger = logging.getLogger(__name__)


class ArchiveboxmaticArchive:
    def __init__(self, config, archive):
        timestamp = int(time.time())
        self.name = archive["name"]
        self.is_schedule = True if "schedule" in archive else False
        self.schedule = archive["schedule"] if "schedule" in archive else "none"
        self.environment = f"{' '.join(config['archivebox']['environment'])} bash -c '"
        self.path = config["archivebox"]["path"]
        self.sources = archive["sources"]
        self.path = config["archivebox"]["path"]
        self.archivebox_command = self.construct_archivebox_command(config, archive)
        self.identifier = (
            f"{timestamp}"
            if "schedule" not in archive
            else f"{archive['schedule']}-{timestamp}"
        )

    def construct_archivebox_command(self, config, archive):
        default_command = f"archivebox add --depth={archive['depth']}"
        if config["archivebox"]["method"] == "docker-compose":
            return f"docker-compose run {default_command}"
        elif config["archivebox"]["method"] == "python":
            return f"{default_command}"
        else:
            raise ("Problem in construct_archivebox_command.")

    def construct_commands(self):
        if "text_files" in self.sources:
            for i in self.sources["text_files"]:
                yield f"{self.environment} cd {self.path} && cat {i} | while read line; do echo ${{line}}#{self.identifier}; done | {self.archivebox_command}'"
        if "shaarli" in self.sources:
            # for i in self.sources["shaarli"]:
            logger.info("Shaarli not implemented yet.")
        if "reddit_saved" in self.sources:
            # for i in self.sources["reddit_saved"]:
            logger.info("Saved reddit posts not implemented yet.")
        if "firefox_bookmarks" in self.sources:
            # for i in self.sources["firefox_bookmarks"]:
            logger.info("Firefox Bookmarks not implemented yet.")
        if "firefox_history" in self.sources:
            # for i in self.sources["firefox_history"]:
            logger.info("Firefox History not implemented yet.")
