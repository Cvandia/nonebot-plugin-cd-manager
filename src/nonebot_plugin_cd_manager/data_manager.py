from nonebot import get_driver
from nonebot.log import logger
from .config import config
from pathlib import Path

import json

driver = get_driver()


class DataManager:
    '''插件数据管理器'''
    def __init__(self):
        self.data_path = Path(config.data_parent_path)
        self.data_path.mkdir(parents=True, exist_ok=True)
        self.data_path = self.data_path / "data.json"
        if not self.data_path.exists():
            with open(self.data_path, "w") as f:
                f.write("{}")
        # self.data = {
        #     "all": {
        #         "command": [cd(int), time(float)],
        #     },
        #     "group": {
        #         "group_id": {
        #             "command": [cd(int), time(float)],
        #         }
        #     },
        # }
        self.data: dict[
            str, dict[str, dict[str, list[int, float]] | list[int, float]]
        ] = {
            "all": {},
            "group": {},
        }

    def load_data(self):
        '''加载数据'''
        with open(self.data_path, "r") as f:
            self.data = json.load(f)
            logger.success("Loaded data")

    def save_data(self):
        '''保存数据'''
        with open(self.data_path, "w") as f:
            json.dump(self.data, f)
            logger.success("Saved data")


plugin_data = DataManager()


@driver.on_bot_connect
async def startup():
    plugin_data.load_data()


@driver.on_bot_disconnect
async def shutdown():
    plugin_data.save_data()
