import PyInstaller.__main__
import os
import sys

# 确保config目录存在
if not os.path.exists('config'):
    os.makedirs('config')

# 创建默认的settings.json
if not os.path.exists('config/settings.json'):
    with open('config/settings.json', 'w') as f:
        f.write('{"x": 0, "y": 0}')

# 定义打包选项
options = [
    'card-master-gui.py',
    '--onefile',
    '--noconsole',
    '--name=CardMaster',
    '--clean',  # 清理临时文件
    '--add-data=config;config',  # 添加配置目录
    '--hidden-import=keyboard',  # 显式导入keyboard模块
    '--hidden-import=pyautogui',  # 显式导入pyautogui模块
    '--hidden-import=tkinter',    # 显式导入tkinter模块
    '--hidden-import=json',       # 显式导入json模块
    '--uac-admin',  # 请求管理员权限
    # 添加运行时DLL
    '--add-binary={}\\DLLs\\tcl86t.dll;.'.format(sys.base_prefix),
    '--add-binary={}\\DLLs\\tk86t.dll;.'.format(sys.base_prefix),
]

# 如果有图标文件，添加图标
if os.path.exists('icon.ico'):
    options.append('--icon=icon.ico')

# 运行打包命令
PyInstaller.__main__.run(options) 