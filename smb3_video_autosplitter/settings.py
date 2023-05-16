import logging

import yaml

LOGGER = logging.getLogger(__name__)
with open("config.yml", "r") as file:
    _config: dict = yaml.safe_load(file)

NES_FRAMERATE = 1008307711 / 256 / 65536
NES_MS_PER_FRAME = 1000.0 / NES_FRAMERATE


def get(name, default=None):
    return _config.get(name, default)
