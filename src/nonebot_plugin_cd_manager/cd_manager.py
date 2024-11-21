"""
Description: 用于管理命令的cd
"""

import time
import random
from nonebot.matcher import Matcher
from .data_manager import DataManager
from .config import config


match_rule = config.match_rule


def check_if_in_cd(
    plugin_data: DataManager, group_id: str | int, event_message: str
) -> tuple[bool, float]:
    """检查是否在cd中
    Args:
        plugin_data (DataManager): 插件数据管理器
        group_id (str | int): 群组id
        command (str): 命令

    Return:
        tuple[bool, float]: 是否在cd中, 剩余时间"""

    def check_cd(data_command):
        for command, (cd, last_time) in data_command.items():
            if (
                (match_rule == "in" and command in event_message)
                or (match_rule == "full" and command == event_message)
                or (match_rule == "start" and event_message.startswith(command))
            ):
                if time.time() - last_time < cd:
                    return True, cd - (time.time() - last_time)
                else:
                    data_command[command][1] = time.time()
                    return False, 0
        return False, 0

    # 先检查全局cd
    global_cd = plugin_data.data.get("all", {})
    in_cd, remain_time = check_cd(global_cd)
    if in_cd:
        return in_cd, remain_time

    # 再检查群组cd
    group_cd = plugin_data.data.get("group", {}).get(group_id, {})
    return check_cd(group_cd)


async def send_random_cd_message(matcher: Matcher, remain_time: float):
    """发送随机cd消息
    Args:
        matcher (Matcher): 匹配器
        remain_time (float): 剩余时间
    """
    random_message = random.choice(
        [
            "baka!, 恁cd还有{:.2f}秒嘞",
            "哼哼，臭杂鱼，你的cd还有{:.2f}秒！！",
            "哼，你的cd还有{:.2f}秒，不许再说话",
            "呜呜，还有{:.2f}秒，你就不能慢一点吗，主人~",
            "有笨蛋想要连续触发咱？但是你的cd还有{:.2f}秒哦~",
        ]
    )
    await matcher.send(random_message.format(remain_time))
