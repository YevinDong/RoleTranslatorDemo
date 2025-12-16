import os
import sys
from loguru import logger

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_dir = os.path.join(root_dir, "logs")

if not os.path.exists(log_dir):
    os.makedirs(log_dir)


class LoggerManager:
    def __init__(self):
        self.logger = logger
        self.logger.remove()
        self.logger.add(
            sys.stdout,
            level="DEBUG",
            format="<green>{time:YYYY/MM/DD HH:mm:ss}</green> | "
            "{process.name} | "
            "{thread.name} | "
            "<cyan>{module}</cyan>.<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{level}</level> | "
            "<level>{message}</level>",
        )

    def get_logger(self):
        return self.logger


log = LoggerManager().get_logger()

if __name__ == "__main__":
    log.debug("debug")
    log.info("info")
    log.warning("warning")
    log.error("error")
    log.critical("critical")

    print('str.pdf'['str.pdf'.rindex('.'):])

    def test():
        try:
            1/0
        except Exception as e:
            log.error(e)
    test()
