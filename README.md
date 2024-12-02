# CardMaster - 卡牌大师辅助工具

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-windows-lightgrey.svg)
![Status](https://img.shields.io/badge/status-stable-green.svg)
[![Stars](https://img.shields.io/github/stars/achord/cardmaster?style=social)](https://github.com/achordchan/cardmaster)



<p align="center">
  <strong>🎮 一个基于Python开发的游戏辅助工具，提供卡牌选择和技能释放的自动化功能</strong>
</p>

<p align="center">
  <a href="#功能特点">功能特点</a> •
  
  <a href="#使用说明">使用说明</a> •
  <a href="#注意事项">注意事项</a>
</p>

</div>

## ✨ 功能特点
- 🎯 快捷键控制开启/关闭（F1）
- ⚙️ 自定义技能位置设置
- 🎴 支持黄、蓝、红牌快速选择
- 🌟 大招黄牌功能
- 🖥️ 用户友好的图形界面
- ⌨️ 按键自定义设置

## 🛠️ 技术栈
- 🐍 Python 3.x
- 🎨 tkinter (GUI框架)
- 🤖 pyautogui (自动化控制)
- ⌨️ keyboard (按键监听)
- 📦 pipenv (依赖管理)

## 📁 项目结构
```
project-root/
├── card-master-gui.py    # 主GUI程序
├── build.py             # 构建脚本
├── check_deps.py        # 依赖检查
├── config/              # 配置文件目录
├── dist/                # 打包发布目录
├── build/               # 构建临时文件
├── venv/                # 虚拟环境
├── Pipfile              # 依赖管理文件
└── Pipfile.lock         # 依赖版本锁定文件
```

### 📖 使用说明
1. 运行程序后，使用F1键开启/关闭功能
2. 使用P键设置技能位置
3. 默认按键设置：
   - W：选择黄牌 🟡
   - E：选择蓝牌 🔵
   - T：选择红牌 🔴
   - R：大招黄牌 ⭐

## ⚠️ 注意事项
- 请以管理员身份运行程序以确保按键监听功能正常工作
- 禁止实战使用！仅允许训练场使用！
- 本工具仅供学习参考使用

## 👨‍💻 作者
- 作者：Achord
- 联系方式：
  - 📧 邮箱：achordchan@gmail.com

## 📄 开源协议
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ⚖️ 免责声明
本项目仅供学习和研究使用，请遵守相关法律法规和游戏规则。作者不对使用本工具造成的任何后果负责。

---

<div align="center">
  <sub>Built with ❤️ by Achord</sub>
</div>
