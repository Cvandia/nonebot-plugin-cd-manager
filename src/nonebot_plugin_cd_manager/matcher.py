"""
插件：cd_manager
Description: 用于管理命令的cd
"""

from nonebot.adapters import Bot, Event
from nonebot.matcher import Matcher
from nonebot.message import run_preprocessor
from nonebot.exception import IgnoredException
from nonebot_plugin_alconna import (
    on_alconna,
    Alconna,
    Args,
    Option,
    Match,
    MultiVar,
    Query,
)

from .cd_manager import check_if_in_cd, send_random_cd_message
from .matcher_utils import view_cd_list, del_cd_command, add_cd_command


set_cd = on_alconna(
    Alconna(
        ["设置cd", "添加cd"],
        Args["cd?", int]["command?", MultiVar(str, "+")],  # 用于设置cd的时间和响应命令
        Option(
            "-g|--group", Args["group_id", int | str, "all"]
        ),  # 用于设置cd的类型，后面跟群号或者all，all为全局cd，默认为all
    ),
    use_cmd_start=True,
)

view_cd = on_alconna(
    Alconna(
        "查看cd",
        Option(
            "-g|--group", Args["group_id", int | str, ""]
        ),  # 用于查看cd的类型，后面跟群号或者all，all为全局cd，默认为all
    ),
    use_cmd_start=True,
)

del_cd = on_alconna(
    Alconna(
        ["删除cd", "移除cd"],
        Args["command?", MultiVar(str, "+")],  # 用于删除cd的命令
        Option(
            "-g|--group", Args["group_id", int | str, "all"]
        ),  # 用于删除cd的类型，后面跟群号或者all，all为全局cd，默认为all
    ),
    use_cmd_start=True,
)


@view_cd.handle()
async def _(group_id: Match[str | int]):
    group_id = str(group_id.result)
    await view_cd.finish(view_cd_list(group_id))


@del_cd.handle()
async def _(
    command: Match[tuple[str, ...]], group_id: Query[str | int] = Query("group", "all")
):
    command: list[str] = list(command.result)
    group_id = str(group_id.result) if group_id.result != "all" else "all"
    try:
        del_cd_command(command, group_id)
    except ValueError as e:
        await del_cd.finish(str(e))
    await del_cd.finish(f"已成功删除{group_id}的{command}")


@set_cd.handle()
async def _(
    cd: Match[int],
    command: Match[tuple[str, ...]],
    group_id: Query[str | int] = Query("group", "all"),
):
    command: list[str] = list(command.result)
    group_id = str(group_id.result) if group_id.result != "all" else "all"
    cd = cd.result
    try:
        add_cd_command(command, group_id, cd)
    except ValueError as e:
        await set_cd.finish(str(e))
    await set_cd.finish(f"已成功设置{group_id}的{command}的cd为{cd}")


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
    is_in_cd, remain_time = check_if_in_cd(group_id, event_messgae)
    if is_in_cd:
        await send_random_cd_message(matcher, remain_time)
        raise IgnoredException("在cd中")
