"""
Description: 用于管理命令的cd
"""

import time
import random
from nonebot.matcher import Matcher
from nonebot.log import logger  # noqa
from .data_manager import plugin_data
from .config import config


match_rule = config.match_rule


def check_if_in_cd(group_id: str | int, event_message: str) -> tuple[bool, float]:
    """检查是否在cd中
    Args:
        group_id (str | int): 群组id
        event_message (str): 事件消息

    Return:
        tuple[bool, float]: 是否在cd中, 剩余时间"""

    def _match_rule(cmd: str, message: str) -> bool:
        """匹配规则
        Args:
            cmd (str): 命令
        Return:
            bool: 是否匹配"""
        if match_rule == "all":
            return cmd == message
        elif match_rule == "start":
            return message.startswith(cmd)
        elif match_rule == "in":
            return cmd in message

    data = (
        plugin_data.data["group"].get(group_id, {})
        if group_id != "all"
        else plugin_data.data["all"]
    )
    if not data:
        data = plugin_data.data["all"]

    for cmd in data:
        totle_cmd_list = [cmd] + data[cmd][2]
        for _cmd in totle_cmd_list:
            match_rule_result = _match_rule(_cmd, event_message)
            if match_rule_result:
                remain_time = data[cmd][0] - (time.time() - data[cmd][1])
                if remain_time > 0:
                    return True, remain_time
                data[cmd][1] = time.time()
                return False, 0
    return False, 0


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
