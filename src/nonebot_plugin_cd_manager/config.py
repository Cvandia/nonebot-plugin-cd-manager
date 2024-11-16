from pydantic import BaseModel
from nonebot.plugin import get_plugin_config

class Config(BaseModel):
    data_parent_path: str = "./data/cdrecall"

config = get_plugin_config(Config)