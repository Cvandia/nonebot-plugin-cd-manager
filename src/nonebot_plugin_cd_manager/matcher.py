"""
插件：cd_manager
Description: 用于管理命令的cd
"""

from nonebot.adapters import Bot, Event
from nonebot.message import event_preprocessor
from nonebot.log import logger
from nonebot.exception import IgnoredException
from nonebot_plugin_alconna import on_alconna, Alconna, Args, Option, Match, MultiVar

from .data_manager import plugin_data
from .cd_manager import check_if_in_cd


set_cd = on_alconna(
    Alconna(
        "设置cd",
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
            "-g|--group", Args["group_id", int | str, "all"]
        ),  # 用于查看cd的类型，后面跟群号或者all，all为全局cd，默认为all
    ),
)

del_cd = on_alconna(
    Alconna(
        "删除cd",
        Args["command", MultiVar(str, "*")],  # 用于删除cd的命令
        Option(
            "-g|--group", Args["group_id", int | str, "all"]
        ),  # 用于删除cd的类型，后面跟群号或者all，all为全局cd，默认为all
    ),
)


@view_cd.handle()
async def _(group_id: Match[str | int]):
    group_id = str(group_id.result)
    if group_id == "all":
        result = plugin_data.data["all"]
    else:
        result = plugin_data.data["group"].get(group_id, {})
    for key, value in result.items():
        await view_cd.send(f"{key}的cd为{value[0]}秒")


@del_cd.handle()
async def _(command: Match[str], group_id: Match[str | int]):
    command_result: list[str] = list(command.result)
    group_id = str(group_id.result)
    for cmd in command_result:
        if group_id == "all":
            plugin_data.data["all"].pop(cmd, None)
        else:
            if group_id not in plugin_data.data["group"]:
                plugin_data.data["group"][group_id] = {}
            plugin_data.data["group"][group_id].pop(cmd, None)
        logger.warning(f"删除{group_id}的{cmd}的cd")

    await del_cd.finish(f"已成功删除{group_id}的{command_result}的cd")


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


@event_preprocessor
async def _(bot: Bot, event: Event):
    event_type = event.get_type()
    if event_type != "message":
        return
    result, remain_time = check_if_in_cd(
        plugin_data, event.get_session_id, event.get_plaintext()
    )
    if result:
        logger.warning("在cd中")
        await bot.send(event, f"cd中, 请等待{remain_time:.2f}秒后再试")
        raise IgnoredException("在cd中")
    return
