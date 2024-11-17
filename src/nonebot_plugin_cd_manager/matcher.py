"""
插件：cd_manager
Description: 用于管理命令的cd
"""

from nonebot.adapters import Bot, Event
from nonebot.matcher import Matcher
from nonebot.message import run_preprocessor
from nonebot.exception import IgnoredException
from nonebot.log import logger
from nonebot_plugin_alconna import on_alconna, Alconna, Args, Option, Match, MultiVar

from .data_manager import plugin_data
from .cd_manager import check_if_in_cd, send_random_cd_message


set_cd = on_alconna(
    Alconna(
        ["设置cd", "添加cd"],
        Args["cd", int]["command", MultiVar(str, "*")],  # 用于设置cd的时间和响应命令
        Option(
            "-g|--group", Args["group_id", int | str, "all"]
        ),  # 用于设置cd的类型，后面跟群号或者all，all为全局cd，默认为all
    ),
)

view_cd = on_alconna(
    Alconna(
        "查看cd",
        Option(
            "-g|--group", Args["group_id", int | str, ""]
        ),  # 用于查看cd的类型，后面跟群号或者all，all为全局cd，默认为all
    ),
)

del_cd = on_alconna(
    Alconna(
        ["删除cd", "移除cd"],
        Args["command", MultiVar(str, "*")],  # 用于删除cd的命令
        Option(
            "-g|--group", Args["group_id", int | str, "all"]
        ),  # 用于删除cd的类型，后面跟群号或者all，all为全局cd，默认为all
    ),
)


@view_cd.handle()
async def _(group_id: Match[str | int]):
    group_id = str(group_id.result)
    all_cd = plugin_data.data["all"]
    group_cd = plugin_data.data["group"]

    def format_cd(cd_data):
        return "\n".join([f"{k}: {v[0]}s" for k, v in cd_data.items()]) or "无"

    if not group_id:
        all_cmd_data = format_cd(all_cd)
        group_cmd_data = (
            "\n".join(
                [f"群组{gid}的cd：\n{format_cd(gcd)}" for gid, gcd in group_cd.items()]
            )
            or "无"
        )
        await view_cd.finish(f"全局cd：\n{all_cmd_data}\n\n群组cd：\n{group_cmd_data}")
    elif group_id == "all":
        all_cmd_data = format_cd(all_cd)
        await view_cd.finish(f"全局cd：\n{all_cmd_data}")
    else:
        group_cmd_data = format_cd(group_cd.get(group_id, {}))
        await view_cd.finish(f"群组{group_id}的cd：\n{group_cmd_data}")


@del_cd.handle()
async def _(command: Match[str], group_id: Match[str | int]):
    command: list[str] = list(command.result)
    group_id = str(group_id.result)
    # 检查是否有这个命令
    for cmd in command:
        if group_id == "all":
            if cmd in plugin_data.data["all"]:
                plugin_data.data["all"].pop(cmd)
            else:
                await del_cd.finish(f"全局cd中没有{cmd}")
                return
        else:
            if group_id not in plugin_data.data["group"]:
                await del_cd.finish(f"群组{group_id}中没有{cmd}")
                return
            if cmd in plugin_data.data["group"][group_id]:
                plugin_data.data["group"][group_id].pop(cmd)
            else:
                await del_cd.finish(f"群组{group_id}中没有{cmd}")
                return
        logger.warning(f"删除{group_id}的{cmd}的cd")
    await del_cd.finish(f"已成功删除{group_id}的{command}的cd记录")


@set_cd.handle()
async def _(
    cd: Match[int],
    command: Match[str],
    group_id: Match[str | int],
):
    command_result: list[str] = list(command.result)
    group_id = str(group_id.result)
    cd = cd.result
    for cmd in command_result:
        if group_id == "all":
            plugin_data.data["all"][cmd] = [cd, 0]
        else:
            if group_id not in plugin_data.data["group"]:
                plugin_data.data["group"][group_id] = {}
            plugin_data.data["group"][group_id][cmd] = [cd, 0]
        logger.warning(f"设置{group_id}的{cmd}的cd为{cd}")

    await set_cd.finish(f"已成功设置{group_id}的{command_result}的cd为{cd}")


@run_preprocessor
async def _(bot: Bot, event: Event, matcher: Matcher):
    if event.get_type() != "message":
        return
    group_id = str(event.group_id) if hasattr(event, "group_id") else "all"
    event_messgae = event.get_message().extract_plain_text()
    if not event_messgae:
        return
    if matcher.plugin_name == "nonebot_plugin_cd_manager":
        return
    is_in_cd, remain_time = check_if_in_cd(plugin_data, group_id, event_messgae)
    if is_in_cd:
        await send_random_cd_message(matcher, remain_time)
        raise IgnoredException("在cd中")
