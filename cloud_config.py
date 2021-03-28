import yaml


def get_config(module: str = None, config_file="config.yaml"):
    with open(config_file) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    result = data.get(module)
    if result is None:
        raise ValueError(f"Module: {module} not found in config file")
    else:
        return result
