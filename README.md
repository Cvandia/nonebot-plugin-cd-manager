<div align="center">

# nonebot-plugin-cd-manager

<a href="https://v2.nonebot.dev/store"><img src="https://count.getloli.com/get/@nonebot-plugin-cd-manager?theme=asoul"></a>

_⭐基于Nonebot2的通用cd管理插件⭐_

<a href="https://www.python.org/downloads/release/python-310/"><img src="https://img.shields.io/badge/python-3.10+-blue"></a> <a href=""><img src="https://img.shields.io/badge/QQ-1141538825-yellow"></a> <a href="https://github.com/Cvandia/nonebot-plugin-cd-manager/blob/main/LICENCE"><img src="https://img.shields.io/badge/license-MIT-blue"></a> <a href="https://v2.nonebot.dev/"><img src="https://img.shields.io/badge/Nonebot2-2.2.0+-red"></a>[![Pylint](https://github.com/Cvandia/nonebot-plugin-cd-manager/actions/workflows/pylint.yml/badge.svg)](https://github.com/Cvandia/nonebot-plugin-cd-manager/actions/workflows/pylint.yml)

**中文简体**

</div>

---

## ⭐ 介绍

**通用cd管理插件**，可以设置和查看命令的冷却时间。

## 📜 免责声明

> [!note]
> 本插件仅供**学习**和**研究**使用，使用者需自行承担使用插件的风险。作者不对插件的使用造成的任何损失或问题负责。请合理使用插件，**遵守相关法律法规。**
使用**本插件即表示您已阅读并同意遵守以上免责声明**。如果您不同意或无法遵守以上声明，请不要使用本插件。

## 💿 安装

<details>
<summary>安装</summary>

`pipx` 安装

```bash
pipx install nonebot-plugin-cd-manager -U
```
> [!note] 在nonebot的pyproject.toml中的plugins = ["xxx"]添加此插件

`nb-cli`安装
```bash
nb plugin install nonebot-plugin-cd-manager -U
```

`git clone`安装(不推荐)

- 命令窗口

cmd

下运行
```bash
git clone https://github.com/Cvandia/nonebot-plugin-cd-manager
```
- 在窗口运行处
将文件夹

nonebot-plugin-cd-manager

复制到bot根目录下的`src/plugins`(或创建bot时的其他名称`xxx/plugins`)

</details>

<details>
<summary>注意</summary>

推荐镜像站下载

清华源```https://pypi.tuna.tsinghua.edu.cn/simple```

阿里源```https://mirrors.aliyun.com/pypi/simple/```

</details>

## ⚙️ 配置

**在.env中添加以下配置**

|     基础配置     | 类型  | 必填项 |      默认值       |                 说明                  |
| :--------------: | :---: | :----: | :---------------: | :-----------------------------------: |
| data_parent_path |  str  |   否   | "./data/cdrecall" | 数据存储路径，默认为"./data/cdrecall" |

## ⭐ 使用

> [!note]
> 请注意你的 `COMMAND_START` 以及上述配置项。

### 指令：

|  指令  | 需要@ | 范围  |        说明        | 权限  |
| :----: | :---: | :---: | :----------------: | :---: |
| 设置cd |  是   |  all  | 设置命令的冷却时间 |  all  |
| 查看cd |  是   |  all  | 查看命令的冷却时间 |  all  |

## 🌙 TODO
 - [x] 添加设置cd 指令
 - [ ] 添加查看cd 指令
 - [ ] 添加删除cd 指令

<center>喜欢记得点个star⭐</center>

## 💝 特别鸣谢

- [x] [nonebot2](https://github.com/nonebot/nonebot2): 本项目的基础，非常好用的聊天机器人框架。更多参考[官方文档](https://v2.nonebot.dev/)
