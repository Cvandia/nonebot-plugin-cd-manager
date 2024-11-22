"""
Description: 用于mathcer.py的工具函数
"""

from .data_manager import plugin_data
from nonebot.log import logger


def view_cd_list(group_id: str | int) -> str:
    """
    查看cd列表
    Args:
        group_id (str | int): 群组id
    Return:
        str: format后的cd列表格式
    """
    all_cd_data = plugin_data.data["all"]
    group_cd_data = plugin_data.data["group"]

    def format_cd(cd_data: dict):
        return (
            "\n".join(
                [
                    f"{k}: {v[0]}s,别名:{'|'.join(a for a in v[2])}"
                    for k, v in cd_data.items()
                ]
            )
            or "无"
        )

    if not group_id:
        all_cmd_data = format_cd(all_cd_data)
        group_cmd_data = (
            "\n".join(
                [
                    f"群组{gid}的cd：\n{format_cd(gcd)}"
                    for gid, gcd in group_cd_data.items()
                ]
            )
            or "无"
        )
        return f"全局cd：\n{all_cmd_data}\n\n群组cd：\n{group_cmd_data}"
    elif group_id == "all":
        return f"全局cd：\n{format_cd(all_cd_data)}"
    else:
        return f"群组{group_id}的cd：\n{format_cd(group_cd_data.get(group_id, {}))}"


def del_cd_command(command_list: list[str], group_id: str | int) -> None:
    """
    删除cd命令
    Args:
        command (list[str]): 命令列表
        group_id (str | int): 群组ID
    Raises:
        ValueError: 如果未找到指定的命令
    """
    data = (
        plugin_data.data["all"]
        if group_id == "all"
        else plugin_data.data["group"].get(group_id, {})
    )
    for cmd in list(data.keys()):
        totle_cmd_list = [cmd] + data[cmd][2]
        if all(c in totle_cmd_list for c in command_list):
            if group_id == "all":
                plugin_data.data["all"].pop(cmd)
            else:
                plugin_data.data["group"][group_id].pop(cmd)
            plugin_data.save_data()


def add_cd_command(command: list[str], group_id: str | int, cd: int) -> None:
    """
    添加cd命令
    Args:
        command (list[str]): 命令
        group_id (str | int): 群组id
        cd (int): cd时间
    Return:
        None
    """
    data = (
        plugin_data.data["all"]
        if group_id == "all"
        else plugin_data.data["group"].get(group_id, {})
    )
    for cmd in data:
        totle_cmd_list = [cmd] + data[cmd][2]
        logger.warning(totle_cmd_list)
        if all(c in totle_cmd_list for c in command):
            raise ValueError("命令已存在,请勿重复添加")
    if group_id == "all":
        plugin_data.data["all"][command[0]] = [cd, 0, command[1:]]
    else:
        if group_id not in plugin_data.data["group"]:
            plugin_data.data["group"][group_id] = {}
        plugin_data.data["group"][group_id][command[0]] = [cd, 0, command[1:]]
    plugin_data.save_data()
