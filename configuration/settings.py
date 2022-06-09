import yaml
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
config_path = BASE_DIR / "config.yaml"


def get_config(path):
    with open(path) as f:
        configuration = yaml.safe_load(f)
    return configuration


config = get_config(config_path)
