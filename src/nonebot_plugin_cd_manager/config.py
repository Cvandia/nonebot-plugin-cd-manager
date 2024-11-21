"""
Description: 配置文件
"""

from typing import Literal
from pydantic import BaseModel
from nonebot.plugin import get_plugin_config


class Config(BaseModel):
    """
    插件配置
    """

    data_parent_path: str = "./data/cd_manager"
    match_rule: Literal["full", "start", "in"] = "in"


config = get_plugin_config(Config)
