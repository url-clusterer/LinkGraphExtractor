import yaml


class ConfigLoader:
    def __init__(self):
        with open('config.yml') as stream:
            self.configs = yaml.safe_load(stream)

    configs = None


def get_configs():
    if ConfigLoader.configs is None:
        ConfigLoader.configs = ConfigLoader().configs
    return ConfigLoader.configs
