class LevelFilter:
    def __init__(self, levelname: str):
        self.levelname = levelname

    def filter(self, record):
        return self.levelname == record.levelname


def configure(*args, **kwargs):
    import logging.config
    import json
    import logging
    import pkg_resources
    import warnings

    jsonConfig = pkg_resources.resource_string(__name__, "logging.json")

    def default_logging(default_level):
        logging.basicConfig(
            format="[%(levelname)s][%(name)s][%(asctime)s][%(relativeCreated)07dms][%(processName)s:%(threadName)s][%(pathname)s:%(lineno)s][%(funcName)s]\n%(message)s\n",
            level=default_level,
        )
        warnings.warn("fallback logging setup used!")

    if jsonConfig:
        try:
            config = json.loads(jsonConfig)
            logging.config.dictConfig(config)
        except Exception as e:
            default_logging(default_level=logging.INFO)
            logging.error(f"{e}")
    else:
        default_logging(default_level=logging.INFO)
