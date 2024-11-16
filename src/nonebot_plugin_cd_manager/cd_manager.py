"""
Description: 用于管理命令的cd
"""
import time
from .data_manager import DataManager


def check_if_in_cd(
    plugin_data: DataManager, group_id: str | int, command: str
) -> tuple[bool, float]:
    """检查是否在cd中
    Args:
        plugin_data (DataManager): 插件数据管理器
        group_id (str | int): 群组id
        command (str): 命令

    Return:
        tuple[bool, float]: 是否在cd中, 剩余时间"""
    in_cd = False
    remaining_time = 0

    # 先检查全局cd
    try:
        data_command = plugin_data.data["all"].get(command)
    except AttributeError:
        data_command = None

    if data_command:
        cd = data_command[0]
        last_time = data_command[1]
        # 判断是否在cd中
        if time.time() - last_time < cd:
            in_cd = True
            remaining_time = cd - (time.time() - last_time)
        else:
            data_command[1] = time.time()

    # 再检查群组cd
    if not in_cd:
        try:
            data_command = plugin_data.data["group"].get(group_id).get(command)
        except AttributeError:
            data_command = None

        if data_command:
            cd = data_command[0]
            last_time = data_command[1]
            # 判断是否在cd中
            if time.time() - last_time < cd:
                in_cd = True
                remaining_time = cd - (time.time() - last_time)
            else:
                data_command[1] = time.time()

    return in_cd, remaining_time
