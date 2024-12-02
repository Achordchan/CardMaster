import threading
import time
import pyautogui
import keyboard
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import sys
import traceback

class CardMasterGUI:
    def __init__(self):
        try:
            self.root = tk.Tk()
            self.root.title("徐州第一卡牌大师大扣老师")
            self.root.geometry("400x600")
            self.root.resizable(False, False)
            
            # 变量初始化
            self.x = 0
            self.y = 0
            self.open = False
            self.running = False
            self.lock = threading.Lock()
            
            # 颜色常量
            self.w_blue = 'blue'
            self.w_red = 'red'
            self.w_yellow = 'yellow'
            self.w_limit = 'limit'
            
            # 默认按键设置
            self.key_settings = {
                'yellow': 'w',    # 黄牌
                'blue': 'e',      # 蓝牌
                'red': 't',       # 红牌
                'ultimate': 'r'   # 大招黄牌
            }
            
            self.keyColorMap = {
                self.key_settings['blue']: self.w_blue,
                self.key_settings['red']: self.w_red,
                self.key_settings['yellow']: self.w_yellow,
            }
            
            # 确保配置目录存在
            self.setup_config_dir()
            
            # 添加大招黄牌开关状态
            self.ultimate_enabled = True  # 默认开启
            
            self.setup_ui()
            self.load_settings()
            
            # 启动监控线程
            self.monitor_thread = threading.Thread(target=self.monitor_keys, daemon=True)
            self.monitor_thread.start()
            
            # 设置快捷键
            try:
                keyboard.add_hotkey('f1', self.toggle)
            except Exception as e:
                self.log(f"快捷键设置失败: {str(e)}")
                messagebox.showerror("错误", "快捷键设置失败，请以管理员身份运行")
        
        except Exception as e:
            messagebox.showerror("初始化错误", f"程序启动失败: {str(e)}")
            sys.exit(1)

    def setup_config_dir(self):
        # 获取程序运行路径
        if getattr(sys, 'frozen', False):
            self.app_path = os.path.dirname(sys.executable)
        else:
            self.app_path = os.path.dirname(os.path.abspath(__file__))
        
        # 确保配置文件目录存在
        self.config_path = os.path.join(self.app_path, 'config')
        os.makedirs(self.config_path, exist_ok=True)
        
        # 设置配置文件路径
        self.settings_file = os.path.join(self.config_path, 'settings.json')

    def setup_ui(self):
        try:
            # 设置主题色和样式
            self.root.configure(bg='#f0f0f0')
            style = ttk.Style()
            style.theme_use('clam')
            
            # 定义颜色
            PRIMARY_COLOR = '#2196F3'
            BG_COLOR = '#f5f5f5'
            TEXT_COLOR = '#333333'
            
            # 配置样式
            style.configure('TLabelframe', background=BG_COLOR)
            style.configure('TLabelframe.Label', 
                           background=BG_COLOR,
                           foreground=TEXT_COLOR,
                           font=('Microsoft YaHei UI', 9, 'bold'))
            style.configure('TButton', 
                           padding=8,
                           background=PRIMARY_COLOR,
                           font=('Microsoft YaHei UI', 9))
            style.configure('TLabel', 
                           background=BG_COLOR,
                           foreground=TEXT_COLOR,
                           font=('Microsoft YaHei UI', 9))
            style.configure('TCheckbutton', 
                           background=BG_COLOR,
                           font=('Microsoft YaHei UI', 9))
            style.configure('TEntry', 
                           padding=5,
                           font=('Microsoft YaHei UI', 9))
            
            # 主容器
            main_container = ttk.Frame(self.root, padding="10 5")
            main_container.pack(fill='both', expand=True)
            
            # 左侧面板 - 控制区域
            left_panel = ttk.Frame(main_container)
            left_panel.pack(side='left', fill='y', padx=(0, 5))
            
            # 状态和控制组合框
            status_control_frame = ttk.LabelFrame(left_panel, text="状态和控制", padding="10 5")
            status_control_frame.pack(fill='x', pady=(0, 5))
            
            self.status_label = ttk.Label(status_control_frame, 
                                        text="已停止",
                                        font=('Microsoft YaHei UI', 9, 'bold'))
            self.status_label.pack(pady=2)
            
            ttk.Button(status_control_frame, 
                      text="开启/关闭 (F1)",
                      command=self.toggle).pack(fill='x', pady=2)
            
            # 位置设置框
            position_frame = ttk.LabelFrame(left_panel, text="技能位置", padding="10 5")
            position_frame.pack(fill='x', pady=(0, 5))
            
            self.coord_label = ttk.Label(position_frame, text="未设置")
            self.coord_label.pack(pady=2)
            
            ttk.Button(position_frame, 
                      text="设置位置 (P)",
                      command=self.set_position).pack(fill='x', pady=2)
            
            # 教程框
            tutorial_frame = ttk.LabelFrame(left_panel, text="使用教程", padding="10 5")
            tutorial_frame.pack(fill='x', pady=(0, 5))
            
            # 设置教程文本样式
            style.configure('Tutorial.TLabel',
                           font=('Microsoft YaHei UI', 8),
                           foreground='#333333',
                           background=BG_COLOR,
                           padding=2,
                           wraplength=150)  # 文本自动换行
            
            # 添加教程内容
            tutorial_text = [
                "*按F1开启功能",
                "*进入游戏后对准技能按P键设置技能位置（不要在训练场频繁使用）",
                
                "*默认按键设置：",
                "   • W - 选择黄牌",
                "   • E - 选择蓝牌",
                "   • T - 选择红牌",
                "   • R - 黄牌落地",
                "*  本工具仅供学习参考",
                
            ]
            
            for line in tutorial_text:
                ttk.Label(tutorial_frame, 
                         text=line,
                         style='Tutorial.TLabel').pack(anchor='w')
            
            # 在左侧面板底部添加作者信息框
            author_frame = ttk.LabelFrame(left_panel, text="关于作者", padding="10 5")
            author_frame.pack(fill='x', pady=(5, 0), side='bottom')
            
            # 设置作者信息样式
            style.configure('Author.TLabel',
                           font=('Microsoft YaHei UI', 8),
                           foreground='#666666',
                           background=BG_COLOR,
                           padding=2)
            
            # 添加作者信息
            ttk.Label(author_frame, 
                     text="作者: Achord",
                     style='Author.TLabel').pack(anchor='w')
            
            ttk.Label(author_frame,
                     text="Tel: 13160235855",
                     style='Author.TLabel').pack(anchor='w')
            
            ttk.Label(author_frame,
                     text="Email: achordchan@gmail.com",
                     style='Author.TLabel').pack(anchor='w')
            
            # 右侧面板 - 按键设置和日志
            right_panel = ttk.Frame(main_container)
            right_panel.pack(side='left', fill='both', expand=True)
            
            # 按键设置框
            key_frame = ttk.LabelFrame(right_panel, text="按键设置", padding="10 5")
            key_frame.pack(fill='x', pady=(0, 5))
            
            # 按键设置网格
            key_settings = [
                ("黄牌按键", "yellow_key_var", 'yellow'),
                ("蓝牌按键", "blue_key_var", 'blue'),
                ("红牌按键", "red_key_var", 'red'),
                ("大招黄牌", "ultimate_key_var", 'ultimate')
            ]
            
            # 设置标签样式
            style.configure('Key.TLabel', 
                           font=('Microsoft YaHei UI', 12, 'bold'),  # 更大更粗的字体
                           foreground='#2196F3',  # 使用主题蓝色
                           background='#ffffff',   # 白色背景
                           padding=5)              # 增加内边距
            
            for i, (key_name, key_var_name, default_key) in enumerate(key_settings):
                # 左侧说明标签
                ttk.Label(key_frame, text=f"{key_name}:").grid(
                    row=i, column=0, padx=5, pady=2, sticky='e'
                )
                
                # 创建一个Frame来包装按键显示
                key_display_frame = ttk.Frame(key_frame)
                key_display_frame.grid(row=i, column=1, padx=5, pady=2, sticky='w')
                
                # 显示按键的标签（使用大写字母）
                key_label = ttk.Label(
                    key_display_frame, 
                    text=self.key_settings[default_key].upper(),
                    style='Key.TLabel'
                )
                key_label.pack(padx=5)
                
                # 保存标签的引用，以便后续更新
                setattr(self, f"{default_key}_key_label", key_label)
            
            # 大招开关
            self.ultimate_var = tk.BooleanVar(value=self.ultimate_enabled)
            ultimate_check = ttk.Checkbutton(
                key_frame, 
                text="启用大招黄牌",
                variable=self.ultimate_var,
                command=self.toggle_ultimate
            )
            ultimate_check.grid(row=4, column=0, columnspan=2, pady=2)
            
          
            
            # 日志框
            log_frame = ttk.LabelFrame(right_panel, text="运行日志", padding="10 5")
            log_frame.pack(fill='both', expand=True)
            
            # 创建带滚动条的日志文本框
            log_container = ttk.Frame(log_frame)
            log_container.pack(fill='both', expand=True)
            
            scrollbar = ttk.Scrollbar(log_container)
            scrollbar.pack(side='right', fill='y')
            
            self.log_text = tk.Text(log_container, 
                                   height=10,
                                   wrap=tk.WORD,
                                   font=('Microsoft YaHei UI', 9),
                                   bg='#ffffff',
                                   relief='flat',
                                   yscrollcommand=scrollbar.set)
            self.log_text.pack(side='left', fill='both', expand=True)
            scrollbar.config(command=self.log_text.yview)

        except Exception as e:
            messagebox.showerror("UI错误", f"界面创建失败: {str(e)}")
            sys.exit(1)

    def log(self, message):
        try:
            self.log_text.insert('end', f"{message}\n")
            self.log_text.see('end')
        except:
            print(message)  # 作为备用输出
        
    def set_position(self):
        try:
            self.log("请将鼠标移动到W技能位置，然后按P键...")
            self.root.withdraw()  # 暂时隐藏窗口
            keyboard.wait('p')
            self.x, self.y = pyautogui.position()
            self.coord_label.config(text=f"X: {self.x}, Y: {self.y}")
            self.log(f"位置已设置: X={self.x}, Y={self.y}")
            self.save_settings()
            self.root.deiconify()  # 显示窗口
        except Exception as e:
            self.log(f"设置位置失败: {str(e)}")
            messagebox.showerror("错误", "设置位置失败")
            self.root.deiconify()
        
    def toggle(self):
        try:
            self.open = not self.open
            status = "运行中" if self.open else "已停止"
            self.status_label.config(text=status)
            self.log(f"状态: {status}")
        except Exception as e:
            self.log(f"切换状态失败: {str(e)}")
            
    def save_settings(self):
        try:
            settings = {
                'x': self.x,
                'y': self.y,
                'key_settings': self.key_settings,
                'ultimate_enabled': self.ultimate_enabled  # 保存开关状态
            }
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f)
        except Exception as e:
            self.log(f"保存设置失败: {str(e)}")
            
    def load_settings(self):
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    self.x = settings.get('x', 0)
                    self.y = settings.get('y', 0)
                    if self.x and self.y:
                        self.coord_label.config(text=f"X: {self.x}, Y: {self.y}")
                    
                    # 加载按键设置
                    if 'key_settings' in settings:
                        loaded_settings = settings['key_settings']
                        if 'ultimate' not in loaded_settings:
                            loaded_settings['ultimate'] = 'r'
                        self.key_settings = loaded_settings
                        self.keyColorMap = {
                            self.key_settings['blue']: self.w_blue,
                            self.key_settings['red']: self.w_red,
                            self.key_settings['yellow']: self.w_yellow,
                        }
                        
                        # 更新显示的按键标签
                        if hasattr(self, 'yellow_key_label'):
                            self.yellow_key_label.config(text=loaded_settings['yellow'].upper())
                            self.blue_key_label.config(text=loaded_settings['blue'].upper())
                            self.red_key_label.config(text=loaded_settings['red'].upper())
                            self.ultimate_key_label.config(text=loaded_settings['ultimate'].upper())
                    
                    # 加载大招开关状态
                    self.ultimate_enabled = settings.get('ultimate_enabled', True)
                    self.ultimate_var.set(self.ultimate_enabled)
        except Exception as e:
            self.log(f"加载设置失败: {str(e)}")

    def parseRgb(self, r, g, b):
        # 先判断蓝量限制
        if (r <= 74 and g >= 130 and g <= 196 and b >= 161 and b <= 237):
            return self.w_limit
        
        # 红色判断 (调整判断条件，使其更精确)
        if (r >= 79 and r <= 255 and g <= 54 and b <= 59):
            return self.w_red
        
        # 黄色判断
        if (r >= 66 and g >= 57 and b <= 68):
            return self.w_yellow
        
        # 蓝色判断 (最后判断蓝色，并调整条件使其更精确)
        if (r <= 60 and g <= 208 and b >= 200):
            return self.w_blue
        
        # 如果都不匹配，返回 None
        return None
            
    def selectCard(self, key):
        with self.lock:
            if self.running:
                return
            self.running = True
        
        try:
            expectColor = self.keyColorMap[key]
            self.log(f"选择: {key} -> {expectColor}")
            
            if key != self.key_settings['yellow']:
                keyboard.send('w')
            
            time.sleep(0.3)
            start = time.perf_counter()
            
            while True:
                if not self.open:
                    self.log("中断选牌")
                    break
                passTime = time.perf_counter() - start
                if passTime > 3:
                    self.log("选牌超时")
                    break  # 超时时直接退出，不做任何操作
                try:
                    r, g, b = pyautogui.pixel(self.x, self.y)
                    color = self.parseRgb(r, g, b)
                    if color is None:  # 如果识别到None，不输出日志
                        continue
                    self.log(f"识别: {color}")
                    if color == self.w_limit:
                        self.log("蓝不够")
                        break  # 蓝不够时直接退出，不做任何操作
                    if color == expectColor:
                        self.log("锁定")
                        keyboard.send('w')
                        break
                except Exception as e:
                    self.log(f"获取颜色失败: {str(e)}")
                    break  # 出错时直接退出，不做任何操作
                time.sleep(0.2)
        
        finally:  # 确保无论如何都会释放锁
            with self.lock:
                self.running = False
            
    def monitor_keys(self):
        while True:
            if self.open and not self.running:
                current_settings = self.key_settings  # 获取当前的按键设置
                if keyboard.is_pressed(current_settings['blue']):
                    self.handle_hotkey(current_settings['blue'])
                elif keyboard.is_pressed(current_settings['red']):
                    self.handle_hotkey(current_settings['red'])
                elif keyboard.is_pressed(current_settings['yellow']):
                    self.handle_hotkey(current_settings['yellow'])
                elif keyboard.is_pressed(current_settings['ultimate']):
                    self.handle_ultimate()
            time.sleep(0.1)
            
    def handle_hotkey(self, key):
        threading.Thread(target=self.selectCard, args=(key,)).start()
        
    def run(self):
        try:
            self.root.mainloop()
        except Exception as e:
            messagebox.showerror("运行错误", f"程序运行失败: {str(e)}")
            sys.exit(1)

    def save_key_settings(self):
        try:
            # 获取新的按键设置
            new_settings = {
                'yellow': self.yellow_key_var.get().lower(),
                'blue': self.blue_key_var.get().lower(),
                'red': self.red_key_var.get().lower(),
                'ultimate': self.ultimate_key_var.get().lower()
            }
            
            # 验证输入
            if len(set(new_settings.values())) != 4:
                messagebox.showerror("错误", "按键设置不能重复")
                return
            
            if not all(len(key) == 1 for key in new_settings.values()):
                messagebox.showerror("错误", "请输入单个字符作为按键")
                return
            
            # 更新设置
            self.key_settings = new_settings
            
            # 更新按键映射
            self.keyColorMap = {
                new_settings['blue']: self.w_blue,
                new_settings['red']: self.w_red,
                new_settings['yellow']: self.w_yellow,
            }
            
            # 更新显示的按键标签
            self.yellow_key_label.config(text=new_settings['yellow'].upper())
            self.blue_key_label.config(text=new_settings['blue'].upper())
            self.red_key_label.config(text=new_settings['red'].upper())
            self.ultimate_key_label.config(text=new_settings['ultimate'].upper())
            
            # 保存到配置文件
            self.save_settings()
            
            # 提示成功
            self.log("按键设置已更新：")
            self.log(f"黄牌: {new_settings['yellow'].upper()}")
            self.log(f"蓝牌: {new_settings['blue'].upper()}")
            self.log(f"红牌: {new_settings['red'].upper()}")
            self.log(f"大招: {new_settings['ultimate'].upper()}")
            messagebox.showinfo("成功", "按键设置已保存")
            
        except Exception as e:
            self.log(f"保存按键设置失败: {str(e)}")
            messagebox.showerror("错误", "保存按键设置失败")

    # 添加大招开关控制方法
    def toggle_ultimate(self):
        self.ultimate_enabled = self.ultimate_var.get()
        status = "启用" if self.ultimate_enabled else "禁用"
        self.log(f"大招黄牌功能已{status}")
        self.save_settings()

    # 修改 handle_ultimate 方法
    def handle_ultimate(self):
        try:
            if not self.ultimate_enabled:
                return
            
            # 先模拟按W
            keyboard.send('w')
            time.sleep(0.1)  # 短暂延迟
            
            # 然后选择黄牌
            self.handle_hotkey(self.key_settings['yellow'])
        except Exception as e:
            self.log(f"大招黄牌执行失败: {str(e)}")

if __name__ == "__main__":
    try:
        # 设置异常钩子
        def show_error(exc_type, exc_value, exc_traceback):
            error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
            messagebox.showerror('错误', f'程序发生错误:\n{error_msg}')
            sys.exit(1)

        sys.excepthook = show_error
        
        # 初始化程序
        pyautogui.FAILSAFE = True
        app = CardMasterGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("错误", f"程序启动失败: {str(e)}\n{traceback.format_exc()}")
        sys.exit(1) 