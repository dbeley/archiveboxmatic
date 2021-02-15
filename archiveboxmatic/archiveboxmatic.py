import logging
import time

logger = logging.getLogger(__name__)


class ArchiveboxmaticArchive:
    def __init__(self, config, archive):
        self.name = archive["name"]
        self.is_schedule = True if "schedule" in archive else False
        self.schedule = archive["schedule"] if "schedule" in archive else "none"
        self.environment = f"{' '.join(config['environment'])} bash -c '"
        self.sources = archive["sources"]
        self.path = config["path"]
        self.archivebox_command = self.build_archivebox_command(
            config["method"], archive
        )

    def build_archivebox_command(self, method, archive):
        default_command = f"archivebox add --depth={archive['depth']}"
        if method == "docker-compose":
            return f"docker-compose run {default_command}"
        elif method == "python":
            return f"{default_command}"
        else:
            raise ("Problem in build_archivebox_command.")

    def build_commands(self):
        timestamp = int(time.time())
        self.identifier = (
            f"{timestamp}" if self.is_schedule else f"{self.schedule}-{timestamp}"
        )
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
