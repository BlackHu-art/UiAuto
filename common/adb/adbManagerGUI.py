#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @author      :  Frankie
 @time        :    11:19
"""

import os
import queue
import shutil
import subprocess
import threading
import time
import zipfile
from datetime import datetime
from common.mail.tempEmailService import EmailService

import pyperclip  # 导入用于复制文本到剪贴板的库
import wx
import wx.stc as stc
import yaml


def sanitize_device_name(device_name):
    return "".join([c if c.isalnum() else "_" for c in device_name])


def find_adb_path():
    adb_path = shutil.which('adb')
    if adb_path is None:
        raise FileNotFoundError(
            "ADB executable not found in PATH. Please ensure ADB is installed and added to your system's PATH.")
    return adb_path


ADB_PATH = find_adb_path()


class ADBManager(wx.Frame):
    def __init__(self, parent, title):
        super(ADBManager, self).__init__(parent, title=title, size=(1300, 800))

        # Use a default icon provided by wx.ArtProvider
        icon = wx.ArtProvider.GetIcon(wx.ART_GO_HOME, wx.ART_FRAME_ICON, (16, 16))
        self.SetIcon(icon)

        self.lock = threading.Lock()
        self.ip_entry = None  # 初始化 ip_entry
        self.devices = []
        self.connected_devices_file = 'connected_devices.yaml'
        self.load_connected_devices()  # Load devices before initializing the UI
        self.apps = []
        self.log_queue = queue.Queue()
        self.init_ui()
        self.get_devices()
        self.thread_running = False  # 标志变量，控制线程运行


    def init_ui(self):
        panel = wx.Panel(self)

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)  # Main horizontal sizer

        # Left vertical sizer for main controls, with fixed width
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        left_panel = wx.Panel(panel, size=(500, 800))
        left_panel.SetSizer(left_sizer)

        # Connect Device and Select Device and App Section
        device_box = wx.StaticBox(left_panel)
        device_sizer = wx.StaticBoxSizer(device_box, wx.VERTICAL)

        ip_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.ip_entry = wx.ComboBox(left_panel, choices=self.devices, style=wx.CB_DROPDOWN)
        ip_sizer.Add(self.ip_entry, 1, wx.EXPAND | wx.ALL, 5)

        self.btn_connect = wx.Button(left_panel, label="Connect To Devices")
        self.btn_connect.Bind(wx.EVT_BUTTON, self.on_connect_device)
        ip_sizer.Add(self.btn_connect, 0, wx.ALL, 5)

        device_sizer.Add(ip_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # 初始化设备列表和按钮的BoxSizer
        device_list_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.listbox_devices = wx.ListBox(left_panel, style=wx.LB_MULTIPLE)
        device_list_sizer.Add(self.listbox_devices, 1, wx.EXPAND | wx.ALL, 5)

        button_sizer = wx.BoxSizer(wx.VERTICAL)  # Button BoxSizer for Refresh and Disconnect Buttons

        self.btn_refresh_devices = wx.Button(left_panel, label="Refresh Devices")
        self.btn_refresh_devices.Bind(wx.EVT_BUTTON, self.on_refresh_devices)
        button_sizer.Add(self.btn_refresh_devices, 1, wx.EXPAND | wx.ALL, 5)  # Set proportion to 1

        self.btn_get_device_info = wx.Button(left_panel, label="Get Device Info")
        self.btn_get_device_info.Bind(wx.EVT_BUTTON, self.on_get_device_info)
        button_sizer.Add(self.btn_get_device_info, 1, wx.EXPAND | wx.ALL, 5)  # Set proportion to 1

        self.btn_disconnect_device = wx.Button(left_panel, label="Disconnect Devices")
        self.btn_disconnect_device.Bind(wx.EVT_BUTTON, self.on_disconnect_device)
        button_sizer.Add(self.btn_disconnect_device, 1, wx.EXPAND | wx.ALL, 5)  # Set proportion to 1

        # New Restart Devices Button
        self.btn_restart_devices = wx.Button(left_panel, label="Restart Devices")
        self.btn_restart_devices.Bind(wx.EVT_BUTTON, self.on_restart_devices)
        button_sizer.Add(self.btn_restart_devices, 1, wx.EXPAND | wx.ALL, 5)  # Set proportion to 1

        self.btn_disconnect_device = wx.Button(left_panel, label="Kill adb server")
        self.btn_disconnect_device.Bind(wx.EVT_BUTTON, self.on_kill_adb)
        button_sizer.Add(self.btn_disconnect_device, 1, wx.EXPAND | wx.ALL, 5)  # Set proportion to 1

        device_list_sizer.Add(button_sizer, 0, wx.ALL, 0)
        device_sizer.Add(device_list_sizer, 0, wx.EXPAND | wx.ALL, 0)

        # Add text entry and button for input text
        text_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # 添加静态文本标签
        text_sizer.Add(wx.StaticText(left_panel, label="Input Text"), 0, wx.ALL | wx.CENTER, 5)
        # 创建文本输入框并绑定 Enter 键事件
        self.text_entry = wx.TextCtrl(left_panel, style=wx.TE_PROCESS_ENTER)
        self.text_entry.Bind(wx.EVT_TEXT_ENTER, self.on_input_text)
        text_sizer.Add(self.text_entry, 1, wx.EXPAND | wx.ALL, 5)

        device_sizer.Add(text_sizer, 0, wx.EXPAND)

        # Actions Section within the combined section
        email_sizer = wx.BoxSizer(wx.HORIZONTAL)  # First row of buttons and input fields

        # 按钮
        self.btn_get_random_email = wx.Button(left_panel, label="Get Email")
        self.btn_get_random_email.Bind(wx.EVT_BUTTON, self.on_get_random_email)
        email_sizer.Add(self.btn_get_random_email, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 1)  # 按钮固定宽度且居中

        # 第一个输入框，提示文案为 "email"
        email_label = wx.StaticText(left_panel)
        email_sizer.Add(email_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 1)  # 标签对齐输入框
        self.email_input = wx.TextCtrl(left_panel, style=wx.TE_PROCESS_ENTER)
        self.email_input.SetHint("email")  # 设置提示文案
        self.email_input.Bind(wx.EVT_TEXT_ENTER, self.on_input_text)  # 绑定 Enter 键事件
        email_sizer.Add(self.email_input, 1, wx.ALL | wx.EXPAND, 1)

        # 第二个输入框，提示文案为 "vercode"
        vercode_label = wx.StaticText(left_panel)
        email_sizer.Add(vercode_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 1)  # 标签对齐输入框
        self.vercode_input = wx.TextCtrl(left_panel, style=wx.TE_PROCESS_ENTER)
        self.vercode_input.SetHint("vercode")  # 设置提示文案
        self.vercode_input.Bind(wx.EVT_TEXT_ENTER, self.on_input_text)  # 绑定 Enter 键事件
        email_sizer.Add(self.vercode_input, 1, wx.ALL | wx.EXPAND, 1)

        # 添加到主布局
        device_sizer.Add(email_sizer, 0, wx.EXPAND | wx.ALL, 1)  # 调整整体间距

        left_sizer.Add(device_sizer, 0, wx.EXPAND | wx.ALL, 1)

        # Select App and Actions Section
        app_action_box = wx.StaticBox(left_panel, label='Actions')
        app_action_sizer = wx.StaticBoxSizer(app_action_box, wx.VERTICAL)

        # Select App Section within the combined section
        app_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.combo_apps = wx.ComboBox(left_panel)  # 移除 style=wx.CB_READONLY
        app_sizer.Add(wx.StaticText(left_panel, label="Select App"), 0, wx.ALL | wx.CENTER, 5)
        app_sizer.Add(self.combo_apps, 1, wx.EXPAND | wx.ALL, 5)

        app_action_sizer.Add(app_sizer, 0, wx.EXPAND)

        row0_sizer = wx.BoxSizer(wx.HORIZONTAL)  # First row of buttons

        self.btn_restart_app = wx.Button(left_panel, label="Restart App")  # 在初始化时添加按钮和绑定事件处理器
        self.btn_restart_app.Bind(wx.EVT_BUTTON, self.on_restart_app)
        row0_sizer.Add(self.btn_restart_app, 1, wx.ALL, 5)

        self.btn_clear_app_data = wx.Button(left_panel, label="Clear App Data")
        self.btn_clear_app_data.Bind(wx.EVT_BUTTON, self.on_clear_app_data)
        row0_sizer.Add(self.btn_clear_app_data, 1, wx.ALL | wx.EXPAND, 5)

        self.btn_screenshot = wx.Button(left_panel, label="Take Screenshot")
        self.btn_screenshot.Bind(wx.EVT_BUTTON, self.on_take_screenshot)
        row0_sizer.Add(self.btn_screenshot, 1, wx.ALL | wx.EXPAND, 5)

        app_action_sizer.Add(row0_sizer, 0, wx.EXPAND)

        # Actions Section within the combined section
        row1_sizer = wx.BoxSizer(wx.HORIZONTAL)  # First row of buttons
        self.btn_install_app = wx.Button(left_panel, label="Install App")
        self.btn_install_app.Bind(wx.EVT_BUTTON, self.on_install_app)
        row1_sizer.Add(self.btn_install_app, 1, wx.ALL | wx.EXPAND, 5)

        self.btn_uninstall_app = wx.Button(left_panel, label="Uninstall App")
        self.btn_uninstall_app.Bind(wx.EVT_BUTTON, self.on_uninstall_app)
        row1_sizer.Add(self.btn_uninstall_app, 1, wx.ALL | wx.EXPAND, 5)

        self.btn_get_current_app = wx.Button(left_panel, label="Get Current App")
        self.btn_get_current_app.Bind(wx.EVT_BUTTON, self.on_get_current_app)
        row1_sizer.Add(self.btn_get_current_app, 1, wx.ALL | wx.EXPAND, 5)

        app_action_sizer.Add(row1_sizer, 0, wx.EXPAND)

        row2_sizer = wx.BoxSizer(wx.HORIZONTAL)  # Second row of buttons
        self.btn_clear_logs = wx.Button(left_panel, label="Clear Devices Logs")
        self.btn_clear_logs.Bind(wx.EVT_BUTTON, self.on_clear_logs)
        row2_sizer.Add(self.btn_clear_logs, 1, wx.ALL | wx.EXPAND, 5)

        self.btn_activity = wx.Button(left_panel, label="Get Current activity")  # 在初始化时添加按钮和绑定事件处理器
        self.btn_activity.Bind(wx.EVT_BUTTON, self.on_current_activity)
        row2_sizer.Add(self.btn_activity, 1, wx.ALL, 5)

        # 选择APK文件按钮
        self.btn_select_apk = wx.Button(left_panel, label="Select APK and Parse")
        self.btn_select_apk.Bind(wx.EVT_BUTTON, self.on_select_apk)
        row2_sizer.Add(self.btn_select_apk, 1, wx.ALL, 5)

        app_action_sizer.Add(row2_sizer, 0, wx.EXPAND)

        left_sizer.Add(app_action_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # performance testing
        monkey_box = wx.StaticBox(left_panel, label='performance testing')
        monkey_sizer = wx.StaticBoxSizer(monkey_box, wx.VERTICAL)

        row0_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # 初始化 self.apps_activity
        self.apps_activity = wx.ComboBox(left_panel)
        row0_sizer.Add(wx.StaticText(left_panel, label="Select Activity"), 0, wx.ALL | wx.CENTER, 5)
        row0_sizer.Add(self.apps_activity, 1, wx.EXPAND | wx.ALL, 5)
        monkey_sizer.Add(row0_sizer, 0, wx.EXPAND)

        row1_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_startup_activity = wx.Button(left_panel, label="Get Start Activity")
        self.btn_startup_activity.Bind(wx.EVT_BUTTON, self.on_get_apps_activity)
        row1_sizer.Add(self.btn_startup_activity, 1, wx.ALL, 5)

        # 启动时间统计按钮
        self.btn_startup_time = wx.Button(left_panel, label="Measure App Startup Time")
        self.btn_startup_time.Bind(wx.EVT_BUTTON, self.on_measure_startup_time)
        row1_sizer.Add(self.btn_startup_time, 1, wx.EXPAND | wx.ALL, 5)
        monkey_sizer.Add(row1_sizer, 0, wx.EXPAND)

        mon_sizer = wx.BoxSizer(wx.HORIZONTAL)
        mon_sizer.Add(wx.StaticText(left_panel, label="Input times"), 0, wx.ALL | wx.CENTER, 5)
        self.times_entry = wx.TextCtrl(left_panel)
        mon_sizer.Add(self.times_entry, 1, wx.EXPAND | wx.ALL, 5)

        self.btn_run_monkey = wx.Button(left_panel, label="Run Monkey Test")
        self.btn_run_monkey.Bind(wx.EVT_BUTTON, self.on_run_monkey_test)
        mon_sizer.Add(self.btn_run_monkey, 0, wx.ALL, 5)

        monkey_sizer.Add(mon_sizer, 0, wx.EXPAND)

        action_sizer1 = wx.BoxSizer(
            wx.HORIZONTAL)  # Adding Get ANR Files and Kill Monkey Test buttons in the same style as Actions section buttons
        self.btn_get_anr_files = wx.Button(left_panel, label="Get ANR Files")
        self.btn_get_anr_files.Bind(wx.EVT_BUTTON, self.on_get_anr_files)
        action_sizer1.Add(self.btn_get_anr_files, 1, wx.EXPAND | wx.ALL, 5)

        self.btn_kill_monkey = wx.Button(left_panel, label="Kill Monkey Test")
        self.btn_kill_monkey.Bind(wx.EVT_BUTTON, self.on_kill_monkey_test)
        action_sizer1.Add(self.btn_kill_monkey, 1, wx.EXPAND | wx.ALL, 5)

        self.btn_capture_bugreport = wx.Button(left_panel, label="Get bugreport")
        self.btn_capture_bugreport.Bind(wx.EVT_BUTTON, self.on_capture_bugreport)
        action_sizer1.Add(self.btn_capture_bugreport, 1, wx.ALL | wx.EXPAND, 5)

        monkey_sizer.Add(action_sizer1, 0, wx.EXPAND)

        action_sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        # 添加 Save Logs 按钮
        self.btn_save_logs = wx.Button(left_panel, label="Get Devices Logs")
        self.btn_save_logs.Bind(wx.EVT_BUTTON, self.on_save_logs)
        action_sizer2.Add(self.btn_save_logs, 1, wx.EXPAND | wx.ALL, 5)

        self.btn_kill_all_apps = wx.Button(left_panel, label="Kill All BG Apps")
        self.btn_kill_all_apps.Bind(wx.EVT_BUTTON, self.on_kill_all_apps)
        action_sizer2.Add(self.btn_kill_all_apps, 1, wx.EXPAND | wx.ALL, 5)

        self.btn_get_packages = wx.Button(left_panel, label="Packages List")
        self.btn_get_packages.Bind(wx.EVT_BUTTON, self.on_get_installed_packages)
        action_sizer2.Add(self.btn_get_packages, 1, wx.EXPAND | wx.ALL, 5)

        monkey_sizer.Add(action_sizer2, 0, wx.EXPAND)

        left_sizer.Add(monkey_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # Add left_panel to the main_sizer with fixed width
        main_sizer.Add(left_panel, 0, wx.EXPAND | wx.ALL, 5)

        # Output Section, with fixed width
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        right_panel = wx.Panel(panel)
        right_panel.SetSizer(right_sizer)

        output_box = wx.StaticBox(right_panel)
        output_sizer = wx.StaticBoxSizer(output_box, wx.VERTICAL)

        self.text_output = stc.StyledTextCtrl(right_panel,
                                              style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL | wx.VSCROLL)
        self.text_output.SetWrapMode(stc.STC_WRAP_WORD)  # Enable word wrap

        # 设置默认样式
        self.text_output.StyleSetSpec(stc.STC_STYLE_DEFAULT, "size:10,face:Courier New,fore:#FFFFFF,back:#000000")
        self.text_output.StyleClearAll()

        # 设置日志信息样式
        self.text_output.StyleSetSpec(1, "fore:#00FF00")  # INFO: Green
        self.text_output.StyleSetSpec(2, "fore:#FFFF00")  # WARNING: Yellow
        self.text_output.StyleSetSpec(3, "fore:#FF0000")  # ERROR: Red

        output_sizer.Add(self.text_output, 1, wx.EXPAND | wx.ALL, 0)

        clear_button = wx.Button(right_panel, label='Clear Log')
        clear_button.Bind(wx.EVT_BUTTON, self.on_clear_log)
        output_sizer.Add(clear_button, 0, wx.EXPAND | wx.ALL, 0)

        right_sizer.Add(output_sizer, 1, wx.EXPAND | wx.ALL, 0)

        # Add right_panel to the main_sizer with fixed width
        main_sizer.Add(right_panel, 1, wx.EXPAND | wx.ALL, 5)

        panel.SetSizer(main_sizer)
        self.root = panel
        self.Bind(wx.EVT_CLOSE, self.on_close)

        self.Centre()
        self.Show(True)

        self.root.GetParent().Bind(wx.EVT_IDLE, self.on_idle)

    def execute_adb_command(self, command):
        try:
            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore',
                creationflags=subprocess.CREATE_NO_WINDOW
            ).stdout
            return result
        except subprocess.CalledProcessError as e:
            self.log_message("ERROR", f"Failed to execute command: {command}, output: {e.output}")
            raise
        except Exception as e:
            self.log_message("ERROR", f"Unexpected error occurred: {e}")
            raise

    def on_get_random_email(self, event):
        """处理 Get Random Email 按钮点击事件"""
        if self.thread_running:
            self.log_message("WARNING", "Previous process is still running. Aborting...")
            return

        self.thread_running = True

        def task():
            try:
                email_service = EmailService()
                random_email_data = email_service.get_random_email()

                if random_email_data and random_email_data.get("data", {}).get("account"):
                    email_account = random_email_data["data"]["account"]
                    self.log_message("INFO", f"Random Email Account Retrieved: {email_account}")

                    wx.CallAfter(self.email_input.SetValue, email_account)

                    # 循环调用 get_email_list
                    for attempt in range(10):
                        email_list_data = email_service.get_email_list()
                        if email_list_data and email_list_data.get("data", {}).get("total") == 1:
                            self.log_message("INFO", "Email list retrieved successfully.")
                            # email_id = email_list_data["data"]["list"][0].get("id")
                            email_id = email_list_data.get("data", {}).get("rows", [])
                            if email_id:
                                email_service.emailId= email_id[0].get("id")
                                self.log_message("INFO", f"Found email with ID")
                                break
                        else:
                            self.log_message("WARNING", f"No email found. Attempt {attempt + 1}/10. Retrying in 10 seconds...")
                            time.sleep(10)
                    else:
                        self.log_message("ERROR", "Failed to retrieve email after 10 attempts.")
                        return

                    # 获取邮件详情并提取验证码
                    verification_code = email_service.get_email_detail()
                    if verification_code:
                        wx.CallAfter(self.vercode_input.SetValue, verification_code)
                        self.log_message("INFO", f"Verification Code Retrieved: {verification_code}")
                    else:
                        self.log_message("ERROR", "Failed to retrieve verification code.")
                else:
                    self.log_message("ERROR", "Failed to retrieve random email account.")
            finally:
                self.thread_running = False  # 任务结束，释放标志

        threading.Thread(target=task, daemon=True).start()

    def on_get_installed_packages(self, event):
        # 获取选中的设备
        selected_devices = self.listbox_devices.GetSelections()
        if not selected_devices:
            self.log_message('WARNING', "Please select at least one device")
            return

        installed_packages = []

        for device_index in selected_devices:
            selected_device = self.listbox_devices.GetString(device_index)

            try:
                # 执行 adb 命令获取设备上的安装包列表
                command = f"adb -s {selected_device} shell pm list packages"
                result = self.execute_adb_command(command).splitlines()

                # 处理结果并记录到日志
                device_packages = []
                for package in result:
                    if package.startswith('package:'):
                        package_name = package[len('package:'):].strip()
                        self.log_message('WARNING', f" {package_name}")
                        device_packages.append(package_name)

                installed_packages.append(device_packages)

            except Exception as e:
                self.log_message('WARNING', f"获取设备 {selected_device} 的安装包列表失败: {e}")

        return installed_packages

    def on_kill_all_apps(self, event):
        # 获取选中的设备
        selected_devices = self.listbox_devices.GetSelections()
        if not selected_devices:
            wx.MessageBox("Please select at least one device", "Error", wx.OK | wx.ICON_ERROR)
            return

    def on_connect_device(self, event):
        ip_address = self.ip_entry.GetValue()
        if not ip_address:
            self.log_message("WARNING", "No IP Address entered")
            return
        if ip_address in self.devices:
            self.log_message("WARNING", f"IP Address {ip_address} already connected")
            return
        thread = threading.Thread(target=self.execute_connect_command, args=(ip_address,))
        thread.start()

    def execute_connect_command(self, ip_address):
        try:
            result = self.execute_adb_command(f"adb connect {ip_address}")
            if f"connected" in result:
                wx.CallAfter(self.log_message, "WARNING", f"execute_adb_command result : \n{result}\n")
                wx.CallAfter(self.get_devices)
                wx.CallAfter(self.save_connected_device, ip_address)
            else:
                wx.CallAfter(self.log_message, "ERROR", f"Unable to connect to {ip_address}: {result}")
        except subprocess.TimeoutExpired:
            wx.CallAfter(self.log_message, "ERROR", "Connection attempt timed out. Please try again.")
        except Exception as e:
            wx.CallAfter(self.log_message, "ERROR", f"Error: Unable to connect to {ip_address}: {str(e)}")

    def save_connected_device(self, ip_address):
        with self.lock:
            sanitized_ip = sanitize_device_name(ip_address)
            if ip_address not in self.devices:
                self.devices.append(ip_address)
            else:
                return  # 早期返回以避免进一步处理

            # 更新 connected_devices.yaml 文件
            self.update_connected_devices_yaml(sanitized_ip, ip_address)

    def load_connected_devices(self):
        with self.lock:
            if os.path.exists(self.connected_devices_file):
                with open(self.connected_devices_file, 'r') as file:
                    device_list = yaml.safe_load(file)
                    if device_list:
                        self.devices.extend([list(device.values())[0] for device in device_list])

    def update_connected_devices_yaml(self, sanitized_ip, ip_address):
        # 检查设备是否已存在，若不存在则添加
        existing_devices = self.load_devices_from_yaml()
        if ip_address in existing_devices:
            self.log_message("INFO", f"IP Address {ip_address} already saved in file")
            return

        with open(self.connected_devices_file, 'a') as file:
            yaml.dump([{sanitized_ip: ip_address}], file)
            self.log_message("INFO", f"IP Address {ip_address} saved to file")

    def load_devices_from_yaml(self):
        if not os.path.exists(self.connected_devices_file):
            return []

        with open(self.connected_devices_file, 'r') as file:
            device_list = yaml.safe_load(file)
            if device_list:
                return [list(device.values())[0] for device in device_list]
            else:
                return []

    def on_get_device_info(self, event):
        """获取选中设备的信息并打印到日志页面"""
        selected_devices = self.listbox_devices.GetSelections()
        if not selected_devices:
            self.log_message("WARNING", "Please select a device first!")
            return

        for index in selected_devices:
            device_name = self.listbox_devices.GetString(index)
            self.get_device_basic_info(device_name)

    def get_device_basic_info(self, device_name):
        """通过adb命令获取设备的基本信息并打印到日志页面"""
        # 定义获取设备信息的 adb 命令
        basic_info_commands = {
            "Model": ["adb", "-s", device_name, "shell", "getprop", "ro.product.model"],
            "Brand": ["adb", "-s", device_name, "shell", "getprop", "ro.product.brand"],
            "Android Version": ["adb", "-s", device_name, "shell", "getprop", "ro.build.version.release"],
            "Serial Number": ["adb", "-s", device_name, "shell", "getprop", "ro.serialno"],
            "SDK Version": ["adb", "-s", device_name, "shell", "getprop", "ro.build.version.sdk"],
            "CPU Architecture": ["adb", "-s", device_name, "shell", "getprop", "ro.product.cpu.abi"],
            "Hardware": ["adb", "-s", device_name, "shell", "getprop", "ro.hardware"],
            "Storage": ["adb", "-s", device_name, "shell", "df", "-h", "/data"],
            "Total Memory": ["adb", "-s", device_name, "shell", "cat", "/proc/meminfo", "|", "grep", "MemTotal"],
            "Available Memory": ["adb", "-s", device_name, "shell", "cat", "/proc/meminfo", "|", "grep",
                                 "MemAvailable"],
            "Resolution": ["adb", "-s", device_name, "shell", "wm", "size"],
            "Density": ["adb", "-s", device_name, "shell", "wm", "density"],
            "Timezone": ["adb", "-s", device_name, "shell", "getprop", "persist.sys.timezone"],
            "Mac": ["adb", "-s", device_name, "shell", "ip", "addr", "show", "wlan0"],
        }

        device_info = {}
        try:
            for key, command in basic_info_commands.items():
                result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        encoding='utf-8', creationflags=subprocess.CREATE_NO_WINDOW)

                if result.returncode == 0:
                    # 成功获取结果，将结果存入device_info字典
                    device_info[key] = result.stdout.strip()
                else:
                    # 如果失败，记录错误信息
                    device_info[key] = f"Error: {result.stderr.strip()}"

            # 将设备信息打印到日志页面
            self.log_message("WARNING", f"Device Info for {device_name}")
            for key, value in device_info.items():
                self.log_message("INFO", f"{key}: {value}")

        except subprocess.CalledProcessError as cpe:
            # 处理子进程执行错误
            self.log_message("ERROR", f"CalledProcessError while getting info for {device_name}: {str(cpe)}")

        except FileNotFoundError:
            # 处理找不到adb命令的情况
            self.log_message("ERROR", f"FileNotFoundError while getting info for {device_name}: adb not found")

        except Exception as e:
            # 捕获其他异常
            self.log_message("ERROR", f"An error occurred while getting info for {device_name}: {str(e)}")

    def on_refresh_devices(self, event):
        self.get_devices()

    # Define the on_restart_devices method
    def on_restart_devices(self, event):
        selected_devices = self.listbox_devices.GetSelections()
        if not selected_devices:
            self.log_message("WARNING", "No device selected")
            return
        for device in selected_devices:
            selected_device = self.listbox_devices.GetString(device)
            thread = threading.Thread(target=self.execute_reboot_device, args=(selected_device,))
            thread.start()

    def on_kill_adb(self, event):
        try:
            result = subprocess.check_output(
                ["adb", "kill-server"],
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            wx.CallAfter(self.log_message, "INFO", f"ADB server killed\n{result.strip()}")
        except subprocess.CalledProcessError as e:
            wx.CallAfter(self.log_message, "ERROR", f"Failed to kill ADB server\n{e.output}")

    def execute_reboot_device(self, selected_device):
        try:
            result = subprocess.check_output(
                ["adb", "-s", selected_device, "reboot"],
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            wx.CallAfter(self.log_message, "INFO", f"Rebooted {selected_device}\n{result.strip()}")
        except subprocess.CalledProcessError as e:
            wx.CallAfter(self.log_message, "ERROR", f"Failed to reboot {selected_device}\n{e.output}")

    def on_get_apps_activity(self, event):
        # 获取选中的设备
        selected_devices = self.listbox_devices.GetSelections()
        if not selected_devices:
            self.log_message("WARNING", "Please select a device first!")
            return

        # 获取选中的应用
        selected_app = self.combo_apps.GetValue()
        if not selected_app:
            self.log_message("WARNING", "Please select an app first!")
            return

        # 对于每个选中的设备，获取启动活动
        for device_index in selected_devices:
            selected_device = self.listbox_devices.GetString(device_index)
            self.get_startup_activity(selected_device, selected_app)

    def get_startup_activity(self, device, app_package):
        try:
            # 启动应用
            start_command = f"adb -s {device} shell am start -n {app_package}/.MainActivity"
            start_result = self.execute_adb_command(start_command)
            self.log_message("INFO", f"Started {app_package} on {device}: {start_result}")

            # 获取启动事件
            dumpsys_command = f"adb -s {device} shell dumpsys activity activities"
            dumpsys_result = self.execute_adb_command(dumpsys_command)

            # 解析输出以获取启动活动的详细信息
            lines = dumpsys_result.splitlines()
            found_activity = False
            for line in lines:
                if "Hist #0:" in line:
                    found_activity = True
                    continue
                if found_activity:
                    activity_info = line.strip()
                    if activity_info:
                        self.log_message("INFO", f"Startup activity for {app_package} on {device}: {activity_info}")
                        break

            if not found_activity:
                self.log_message("WARNING", f"No startup activity found for {app_package} on {device}")

        except subprocess.CalledProcessError as e:
            self.log_message("ERROR", f"Failed to get startup activity for {app_package} on {device}: {e.output}")
        except Exception as e:
            self.log_message("ERROR",
                             f"An error occurred while getting startup activity for {app_package} on {device}: {str(e)}")

    def on_measure_startup_time(self, event):
        selected_devices = self.listbox_devices.GetSelections()
        if not selected_devices:
            self.log_message("WARNING", "Please select a device first!")
            return

        app_package = self.combo_apps.GetValue()
        if not app_package:
            self.log_message("WARNING", "Please get a valid app package name!")
            return

        # for index in selected_devices:
        #     device_name = self.listbox_devices.GetString(index)
        #     main_activity = self.get_main_activity(device_name, app_package)
        #     if main_activity:
        #         threading.Thread(target=self.measure_startup_time, args=(device_name, app_package, main_activity),
        #                          daemon=True).start()
        #     else:
        #         self.log_message("WARNING", f"Unable to determine main activity for {app_package}")

    def measure_startup_time(self, device_name, app_package, main_activity):
        with self.lock:
            self.log_message("INFO", f"Measuring startup time for {app_package} on {device_name}.")

        try:
            start_time = time.time()
            start_command = ["adb", "-s", device_name, "shell", "am", "start", "-W", "-n", f"{app_package}/{main_activity}"]
            start_result = self.run_adb_command(device_name, start_command)
            end_time = time.time()

            if "Error" in start_result:
                with self.lock:
                    self.log_message("ERROR", f"Failed to start {app_package} on {device_name}: {start_result}")
                return

            startup_time = end_time - start_time
            with self.lock:
                self.log_message("INFO", f"Startup time for {app_package} on {device_name} is {startup_time:.2f} seconds.")

        except Exception as e:
            with self.lock:
                self.log_message("ERROR",
                                 f"An error occurred while measuring startup time for {app_package} on {device_name}: {str(e)}")

    def run_adb_command(self, device_name, command):
        try:
            output = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            ).stdout.strip()
            return output
        except subprocess.CalledProcessError as e:
            with self.lock:
                self.log_message("ERROR", f"ADB Command Failed on {device_name}: {e.stderr}")
            return None
        except UnicodeDecodeError:
            with self.lock:
                self.log_message("ERROR", f"ADB Command produced non-UTF-8 output on {device_name}.")
            return None

    def on_clear_logs(self, event):
        selected_devices = self.listbox_devices.GetSelections()
        if not selected_devices:
            self.log_message("WARNING", "No device selected")
            return
        for device in selected_devices:
            selected_device = self.listbox_devices.GetString(device)
            thread = threading.Thread(target=self.execute_clear_logs, args=(selected_device,))
            thread.start()

    def on_current_activity(self, event):
        """获取选中设备的当前应用的 Activity 并输出到日志"""
        selected_device_indices = self.listbox_devices.GetSelections()
        if not selected_device_indices:
            self.log_message("WARNING", "Please select at least one device first!")
            return

        no_active_activity_devices = []
        error_devices = []
        no_resumed_activity_devices = []

        # 依次获取每个选中设备的当前 Activity 信息
        for index in selected_device_indices:
            device_name = self.listbox_devices.GetString(index)
            adb_command = ["adb", "-s", device_name, "shell", "dumpsys", "window", "|", "grep", "mCurrentFocus"]
            resumed_activity_command = ["adb", "-s", device_name, "shell", "dumpsys", "activity", "activities", "|",
                                        "grep", "mResumedActivity"]

            try:
                # 执行 adb 命令获取当前 Activity
                result = subprocess.run(adb_command, shell=False, capture_output=True, encoding="utf-8",
                                        creationflags=subprocess.CREATE_NO_WINDOW)

                if result.returncode == 0:
                    # 获取并格式化输出的 Activity 信息
                    activity_info = result.stdout.strip()
                    if activity_info:
                        self.log_message("INFO", f"Current Activity: \n{activity_info}\n")
                    else:
                        no_active_activity_devices.append(device_name)
                else:
                    # 记录错误信息
                    error_devices.append((device_name, result.stderr.strip()))

                # 执行 adb 命令获取启动 Activity
                resumed_result = subprocess.run(resumed_activity_command, shell=False, capture_output=True,
                                                encoding="utf-8",
                                                creationflags=subprocess.CREATE_NO_WINDOW)

                if resumed_result.returncode == 0:
                    # 获取并格式化输出的启动 Activity 信息
                    resumed_activity_info = resumed_result.stdout.strip()
                    if resumed_activity_info:
                        self.log_message("INFO", f"Resumed Activity: \n{resumed_activity_info}\n")
                    else:
                        no_resumed_activity_devices.append(device_name)
                else:
                    # 记录错误信息
                    error_devices.append((device_name, resumed_result.stderr.strip()))

            except subprocess.CalledProcessError as e:
                error_devices.append((device_name, str(e)))
            except OSError as e:
                error_devices.append((device_name, str(e)))
            except Exception as e:
                error_devices.append((device_name, str(e)))

        if no_active_activity_devices:
            self.log_message("WARNING", f"No active Activity found on devices: {', '.join(no_active_activity_devices)}")

        if no_resumed_activity_devices:
            self.log_message("WARNING",
                             f"No resumed Activity found on devices: {', '.join(no_resumed_activity_devices)}")

        for device_name, error_msg in error_devices:
            self.log_message("ERROR",
                             f"Device: {device_name} - Failed to retrieve current or resumed Activity: {error_msg}")

    def on_select_apk(self, event):
        # 弹出文件选择框
        with wx.FileDialog(self, "Select APK File", wildcard="APK files (*.apk)|*.apk",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            # 获取选中的APK文件路径
            apk_path = fileDialog.GetPath()

            # 验证文件路径是否为有效的APK文件
            if not apk_path.endswith('.apk'):
                self.log_message("ERROR", f"Invalid APK file: {apk_path}\n")
                return

            self.log_message("INFO", f"Selected APK: {apk_path}\n")

            # 调用 aapt 命令解析APK信息
            self.parse_apk_info(apk_path)

    def parse_apk_info(self, apk_path):
        aapt_command = ["aapt", "dump", "badging", apk_path]

        try:
            # 执行 aapt 命令
            output = subprocess.run(aapt_command, capture_output=True, text=True, check=True).stdout

            # 输出解析结果到日志
            self.log_message("INFO", "APK Info:\n")
            self.log_message("INFO", output + "\n")

        except subprocess.CalledProcessError as e:
            self.log_message("ERROR", "Failed to parse APK info.\n")
            self.log_message("ERROR", f"Command: {' '.join(aapt_command)}\n")
            self.log_message("ERROR", f"Return code: {e.returncode}\n")
            self.log_message("ERROR", f"Output: {e.output}\n")
            self.log_message("ERROR", f"Error: {e.stderr}\n")

        except Exception as e:
            self.log_message("ERROR", "An unexpected error occurred while parsing APK info.\n")
            self.log_message("ERROR", str(e) + "\n")

    def execute_clear_logs(self, selected_device):
        try:
            result = subprocess.check_output(
                ["adb", "-s", selected_device, "shell", "logcat", "-c"],
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            wx.CallAfter(self.log_message, "WARNING", f"Cleared logs for {selected_device}")
        except subprocess.CalledProcessError as e:
            wx.CallAfter(self.log_message, "ERROR", f"Failed to clear logs for {selected_device}\n{e.output}")

    def on_run_monkey_test(self, event):
        selected_devices = self.listbox_devices.GetSelections()
        selected_app = self.combo_apps.GetValue()
        times_entry = self.times_entry.GetValue()
        if not selected_devices:
            wx.CallAfter(self.log_message, "WARNING", "No device selected")
            return
        if not selected_app:
            wx.CallAfter(self.log_message, "WARNING", "No app selected")
            return
        if not times_entry:
            wx.CallAfter(self.log_message, "WARNING", "No times entry")
            return
        log_file_dir = wx.DirSelector("Select log file directory")
        if not log_file_dir:
            wx.CallAfter(self.log_message, "WARNING", "No log file directory selected")
            return
        for device in selected_devices:
            selected_device = self.listbox_devices.GetString(device)
            sanitized_device_name = sanitize_device_name(selected_device)

            log_file_path = os.path.join(log_file_dir, f"{sanitized_device_name}_log.txt")
            sys_log_file_path = os.path.join(log_file_dir, f"{sanitized_device_name}_Syslog.txt")

            # bugreport_file_path = os.path.join(log_file_dir, f"{sanitized_device_name}_bugreport")
            # if not os.path.exists(bugreport_file_path):  # 判断不存在则创建bugreport文件夹
            #     os.makedirs(bugreport_file_path)

            thread = threading.Thread(target=self.execute_monkey_and_logcat, args=(
                selected_device, selected_app, times_entry, log_file_path, sys_log_file_path))
            thread.start()

    def execute_monkey_and_logcat(self, selected_device, selected_app, times_entry, log_file_path, sys_log_file_path):
        try:
            # Clear logs before starting the monkey test
            self.execute_clear_logs(selected_device)

            logcat_process = subprocess.Popen(
                ["adb", "-s", selected_device, "logcat", "-v", "time"],
                stdout=open(sys_log_file_path, "w"),
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            wx.CallAfter(self.log_message, "INFO", f"System logs saved to {sys_log_file_path}")

            start_time = datetime.now()  # Record start time

            # 设定执行事件的百分比
            # （1）pct-touch --触摸事件，点击时间百分比
            # （2）pct-motion--动作事件，设定动作时间百分比
            # （3）pct-trackball --轨迹球事件，设定轨迹球事件百分比
            # （4）pct-nav--基本导航事件，设定基本导航事件百分比，输入设备上、下、左、右键
            # （5）pct-majornav-主要导航事件，设定主要导航事件百分比，兼容中间建、返回键、菜单键
            # （6）pct-syskeys--系统导航事件，设定系统导航事件百分比，HOME、BACK建、拨号键及音量键等
            # （7）pct-appswitch--Activity事件，设定启动Activity事件百分比
            # （8）pct-anyevent--不常用事件，设定不常用事件百分比
            # ["adb", "-s", selected_device, "shell", "monkey", "-p", selected_app, "--throttle", "500",
            #  "--ignore-crashes --ignore-timeouts --ignore-security-exceptions ",
            #  "--ignore-timeouts", "-v", times_entry],

            monkey_process = subprocess.Popen(
                ["adb", "-s", selected_device, "shell", "monkey", "-p", selected_app, "-v", "-v", "-v", "-s", "1000000",
                 "--ignore-crashes", "--ignore-timeouts", "--ignore-security-exceptions", "--kill-process-after-error",
                 "--pct-appswitch", "0", "--pct-touch", "15", "--pct-syskeys", "5", "--pct-motion", "5",
                 "--pct-trackball", "0",
                 "--pct-majornav", "30", "--pct-nav", "40", "--pct-anyevent", "5", "--pct-flip", "0", "--pct-pinchzoom",
                 "0",
                 "--throttle", "500", times_entry],
                stdout=open(log_file_path, "w"),
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            wx.CallAfter(self.log_message, "INFO",
                         f"Monkey test started on {selected_device}, logs saved to {log_file_path}")

            stdout, stderr = monkey_process.communicate()
            if stderr:
                wx.CallAfter(self.log_message, "ERROR", f"Monkey test encountered errors: {stderr.decode()}")

            end_time = datetime.now()  # Record end time

            run_time = end_time - start_time
            hours, remainder = divmod(run_time.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            wx.CallAfter(self.log_message, "WARNING",
                         f"Monkey test on {selected_device} completed successfully in {int(hours)}h {int(minutes)}m {int(seconds)}s")

            logcat_process.terminate()
            logcat_process.wait()
            wx.CallAfter(self.log_message, "INFO", f"System logs capture completed on {selected_device}")

            # Capture bugreport and convert to HTML
            # self.capture_bugreport(selected_device, bugreport_file_path)
            # self.convert_bugreport_to_html(bugreport_file_path, bugreport_html_path)
        except subprocess.CalledProcessError as e:
            wx.CallAfter(self.log_message, "ERROR", f"Failed to start Monkey test on {selected_device}\n{e}")

    def on_capture_bugreport(self, event):
        selected_devices = self.listbox_devices.GetSelections()
        if not selected_devices:
            self.log_message("WARNING", "No device selected")
            return
        save_dir = wx.DirSelector("Select directory to save bugreport")
        if not save_dir:
            self.log_message("WARNING", "No directory selected")
            return
        for device in selected_devices:
            selected_device = self.listbox_devices.GetString(device)
            sanitized_device_name = sanitize_device_name(selected_device)
            bugreport_file_path = os.path.join(save_dir, f"{sanitized_device_name}_bugreport")
            os.makedirs(bugreport_file_path, exist_ok=True)  # 创建路径
            thread = threading.Thread(target=self.capture_bugreport, args=(selected_device, bugreport_file_path))
            thread.start()

    def capture_bugreport(self, selected_device, bugreport_file_path):
        try:
            wx.CallAfter(self.log_message, "INFO",
                         f"Start to capture bugreport on {selected_device} to {bugreport_file_path}")

            # 确保文件目录存在
            os.makedirs(bugreport_file_path, exist_ok=True)

            # 获取设备的Android版本
            version_result = subprocess.run(
                ["adb", "-s", selected_device, "shell", "getprop", "ro.build.version.release"],
                text=True,
                encoding='utf-8',
                errors='replace',
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            android_version_str = version_result.stdout.strip()
            wx.CallAfter(self.log_message, "INFO",
                         f"bugreport is running on {selected_device} Android version {android_version_str}")

            # 验证版本号是否有效，并将其转换为元组
            try:
                android_version = tuple(map(int, android_version_str.split('.')))
            except ValueError:
                wx.CallAfter(self.log_message, "ERROR", "Invalid Android version format")
                return

            if android_version >= (8, 0):
                # 对于Android 8至11版本，使用bugreport命令并将输出保存到文件
                result = subprocess.run(
                    ["adb", "-s", selected_device, "bugreport", bugreport_file_path],
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                wx.CallAfter(self.log_message, "INFO", f"Command result: {result.stdout}")
            else:
                # 对于Android 7及以下版本，使用bugreport命令并将输出保存到文件
                output_file = os.path.join(bugreport_file_path, f"bugreport_{selected_device}.txt")
                result = subprocess.run(
                    ["adb", "-s", selected_device, "bugreport", output_file],
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                wx.CallAfter(self.log_message, "INFO", f"Command result: {result.stdout}")

            # 检查是否存在.zip格式的bugreport文件，并进行相应处理
            self.process_zip_files(bugreport_file_path)

            # 输出错误信息
            if result.stderr:
                wx.CallAfter(self.log_message, "WARNING", f"Subprocess stderr: {result.stderr}")

        except subprocess.CalledProcessError as e:
            wx.CallAfter(self.log_message, "ERROR", str(e))
        except FileNotFoundError as e:
            wx.CallAfter(self.log_message, "ERROR", f"File not found error: {str(e)}")
        except PermissionError as e:
            wx.CallAfter(self.log_message, "ERROR", f"Permission error: {str(e)}")
        except Exception as e:
            wx.CallAfter(self.log_message, "ERROR", f"An unexpected error occurred: {str(e)}")

    def process_zip_files(self, bugreport_file_path):
        # 检查是否存在.zip格式的bugreport文件，并进行相应处理
        zip_files = [f for f in os.listdir(bugreport_file_path) if f.endswith('.zip')]
        if zip_files:
            # 遍历所有.zip文件进行处理
            for zip_file in zip_files:
                zip_path = os.path.join(bugreport_file_path, zip_file)
                # 解压并处理bugreport文件
                self.extract_bugreport_file(zip_path, bugreport_file_path)
        else:
            # 如果没有找到.zip文件，记录错误信息
            wx.CallAfter(self.log_message, "ERROR", "Failed to find the generated bugreport file.")

    def extract_bugreport_file(self, zip_path, bugreport_file_path):
        """ 解压指定的ZIP文件到其所在目录，并处理所有找到的bugreport.txt文件。 """
        try:
            # 使用zipfile模块解压ZIP文件
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(os.path.dirname(zip_path))
            # 解压成功后记录日志
            wx.CallAfter(self.log_message, "WARNING", f"Successfully extracted ZIP file {zip_path}")

            # 遍历解压后的文件夹，寻找所有 bugreport.txt 文件
            found_valid_files = False  # 添加标志位，用于检查是否找到了有效文件
            for root, dirs, files in os.walk(bugreport_file_path):
                for file_name in files:
                    if file_name.startswith("bugreport") and file_name.endswith(".txt"):
                        txt_file_path = os.path.join(root, file_name)
                        # 找到bugreport文件后记录日志
                        wx.CallAfter(self.log_message, "INFO", f"Found bugreport file: {file_name}")
                        # 调用convert_bugreport_to_html方法处理每个文件
                        self.convert_bugreport_to_html(txt_file_path)
                        found_valid_files = True

            # 检查是否找到有效文件
            if not found_valid_files:
                wx.CallAfter(self.log_message, "ERROR", "No valid bugreport.txt files found")
        except Exception as e:
            # 异常处理，记录错误日志
            wx.CallAfter(self.log_message, "ERROR", f"An unexpected error occurred during extraction: {e}")
            return None

    def convert_bugreport_to_html(self, bugreport_file_path):
        try:
            # 设置jar文件路径
            jar_path = os.path.join(os.path.dirname(__file__), "chkbugreport-0.5-215.jar")
            # 使用subprocess模块执行Java命令，将bugreport转换为HTML
            result = subprocess.run(
                ["java", "-jar", jar_path, bugreport_file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            if result.returncode == 0:
                # 转换成功后记录日志
                wx.CallAfter(self.log_message, "WARNING", f"Bugreport HTML generated Successfully")
            else:
                # 转换失败时抛出异常
                raise subprocess.CalledProcessError(result.returncode, result.args, output=result.stdout,
                                                    stderr=result.stderr)

        except subprocess.CalledProcessError as e:
            # 异常处理，记录错误日志
            wx.CallAfter(self.log_message, "ERROR", f"Failed to convert bugreport to HTML\n{e.stderr}")

    def on_get_anr_files(self, event):
        selected_devices = self.listbox_devices.GetSelections()
        if not selected_devices:
            self.log_message("WARNING", "No device selected")
            return
        anr_dir = wx.DirSelector("Select directory to save ANR files")
        if not anr_dir:
            self.log_message("WARNING", "No directory selected")
            return
        for device in selected_devices:
            selected_device = self.listbox_devices.GetString(device)
            sanitized_device_name = sanitize_device_name(selected_device)
            thread = threading.Thread(target=self.pull_anr_files,
                                      args=(selected_device, sanitized_device_name, anr_dir))
            thread.start()

    def pull_anr_files(self, selected_device, sanitized_device_name, anr_dir):
        try:
            # 创建以设备名称命名的文件夹
            device_anr_dir = os.path.join(anr_dir, f"{sanitized_device_name}_anr")
            os.makedirs(device_anr_dir, exist_ok=True)

            pull_command = ["adb", "-s", selected_device, "pull", "/data/anr", device_anr_dir]
            subprocess.check_output(pull_command,
                                    stderr=subprocess.STDOUT,
                                    text=True,
                                    encoding='utf-8',
                                    errors='ignore',
                                    creationflags=subprocess.CREATE_NO_WINDOW)
            wx.CallAfter(self.log_message, "INFO", f"ANR files from {selected_device} saved to {device_anr_dir}")
        except subprocess.CalledProcessError as e:
            # 获取错误输出和返回码
            error_output = e.output.strip()
            return_code = e.returncode

            # 构建详细的错误信息
            detailed_error_msg = (
                f"Failed to get ANR files from {selected_device}.\n"
                f"Command: {' '.join(e.cmd)}\n"
                f"Return code: {return_code}\n"
                f"Error output:\n{error_output}"
            )

            wx.CallAfter(self.log_message, "ERROR", detailed_error_msg)

    def on_kill_monkey_test(self, event):
        selected_devices = self.listbox_devices.GetSelections()
        if not selected_devices:
            self.log_message("WARNING", "No device selected")
            return
        for device in selected_devices:
            selected_device = self.listbox_devices.GetString(device)
            thread = threading.Thread(target=self.kill_monkey_process, args=(selected_device,))
            thread.start()

    def kill_monkey_process(self, selected_device):
        try:
            # 获取并杀掉 monkey 测试进程
            pid_command = ["adb", "-s", selected_device, "shell", "ps | grep monkey"]
            result = subprocess.check_output(pid_command, stderr=subprocess.STDOUT, text=True, encoding='utf-8',
                                             errors='ignore', creationflags=subprocess.CREATE_NO_WINDOW)
            if result:
                pid = result.split()[1]  # 获取 monkey 进程的 PID
                kill_command = ["adb", "-s", selected_device, "shell", "kill", pid]
                subprocess.check_output(kill_command, stderr=subprocess.STDOUT, text=True, encoding='utf-8',
                                        errors='ignore', creationflags=subprocess.CREATE_NO_WINDOW)
                wx.CallAfter(self.log_message, "INFO", f"Monkey test process on {selected_device} killed")
            else:
                wx.CallAfter(self.log_message, "INFO", f"No monkey test process found on {selected_device}")
        except subprocess.CalledProcessError as e:
            wx.CallAfter(self.log_message, "ERROR",
                         f"Failed to kill monkey test process on {selected_device}\n{e.output}")

    def on_get_current_app(self, event):
        selected_devices = self.listbox_devices.GetSelections()
        if not selected_devices:
            self.log_message("WARNING", "No device selected")
            return

        for device in selected_devices:
            selected_device = self.listbox_devices.GetString(device)
            thread = threading.Thread(target=self.get_current_app, args=(selected_device,))
            thread.start()

    def get_current_app(self, selected_device):
        try:
            result = subprocess.check_output(
                ["adb", "-s", selected_device, "shell", "dumpsys", "window", "|", "grep", "mCurrentFocus"],
                stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='ignore',
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            current_app = result.strip().split()[-1].split('/')[0]
            wx.CallAfter(self.update_current_app, selected_device, current_app)
        except subprocess.CalledProcessError as e:
            wx.CallAfter(self.log_message, "ERROR", f"Failed to get current app on {selected_device}\n{e.output}")

    def update_current_app(self, selected_device, current_app):
        if current_app and current_app not in self.apps:
            self.apps.append(current_app)
            self.combo_apps.SetItems(self.apps)
            if selected_device == self.listbox_devices.GetString(self.listbox_devices.GetSelections()[0]):
                self.combo_apps.SetValue(current_app)
        self.log_message("INFO", f"Current app running on {selected_device}: {current_app}")

    def on_restart_app(self, event):
        selected_devices = self.listbox_devices.GetSelections()
        if not selected_devices:
            self.log_message("WARNING", "No device selected")
            return
        selected_app = self.combo_apps.GetValue()
        if not selected_app:
            self.log_message("WARNING", "No app selected")
            return

        for device in selected_devices:
            selected_device = self.listbox_devices.GetString(device)
            thread = threading.Thread(target=self.execute_restart_command, args=(selected_device, selected_app))
            thread.start()

    def execute_restart_command(self, selected_device, selected_app):
        try:
            # 停止应用程序
            stop_command = ["adb", "-s", selected_device, "shell", "am", "force-stop", selected_app]
            wx.CallAfter(self.log_message, "INFO", f"Stopping app ... ...")
            subprocess.run(stop_command, check=True, stderr=subprocess.STDOUT, text=True, encoding='utf-8',
                           errors='ignore', creationflags=subprocess.CREATE_NO_WINDOW)

            # 启动应用程序
            start_command = ["adb", "-s", selected_device, "shell", "monkey", "-p", selected_app, "-c",
                             "android.intent.category.LAUNCHER", "1"]
            wx.CallAfter(self.log_message, "INFO", f"Starting app ... ...")
            subprocess.run(start_command, check=True, stderr=subprocess.STDOUT, text=True, encoding='utf-8',
                           errors='ignore', creationflags=subprocess.CREATE_NO_WINDOW)

            wx.CallAfter(self.log_message, "WARNING", f"Restarted {selected_app} on {selected_device} successfully \n")
        except subprocess.CalledProcessError as e:
            wx.CallAfter(self.log_message, "ERROR",
                         f"Failed to restart {selected_app} on {selected_device}\n{e.output}")
        except Exception as e:
            wx.CallAfter(self.log_message, "ERROR",
                         f"An unexpected error occurred while restarting {selected_app} on {selected_device}: {str(e)}")

    def on_install_app(self, event):
        selected_devices = self.listbox_devices.GetSelections()
        if not selected_devices:
            self.log_message("WARNING", "No device selected")
            return
        apk_path = wx.FileSelector("Select APK file", wildcard="APK files (*.apk)|*.apk")
        if not apk_path:
            self.log_message("WARNING", "No APK file selected")
            return
        for device in selected_devices:
            selected_device = self.listbox_devices.GetString(device)
            thread = threading.Thread(target=self.execute_install_command, args=(selected_device, apk_path))
            thread.start()

    def execute_install_command(self, selected_device, apk_path):
        try:
            install_command = ["adb", "-s", selected_device, "install", "-r", apk_path]
            self.log_message("INFO", f"Executing: {' '.join(install_command)}")
            result = subprocess.check_output(
                install_command, stderr=subprocess.STDOUT, text=True, encoding='utf-8',
                errors='ignore', creationflags=subprocess.CREATE_NO_WINDOW
            )
            wx.CallAfter(self.log_message, "INFO", f"Installed {apk_path} on {selected_device}\n{result.strip()}")
        except subprocess.CalledProcessError as e:
            wx.CallAfter(self.log_message, "ERROR", f"Failed to install {apk_path} on {selected_device}\n{e.output}")

    def on_uninstall_app(self, event):
        selected_devices = self.listbox_devices.GetSelections()
        if not selected_devices:
            self.log_message("WARNING", "No device selected")
            return
        selected_app = self.combo_apps.GetValue()
        if not selected_app:
            self.log_message("WARNING", "No app selected")
            return
        for device in selected_devices:
            selected_device = self.listbox_devices.GetString(device)
            thread = threading.Thread(target=self.execute_uninstall_command, args=(selected_device, selected_app))
            thread.start()

    def execute_uninstall_command(self, selected_device, selected_app):
        try:
            uninstall_command = ["adb", "-s", selected_device, "uninstall", selected_app]
            self.log_message("INFO", f"Running command: {' '.join(uninstall_command)}")
            result = subprocess.check_output(
                uninstall_command, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='ignore',
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            wx.CallAfter(self.log_message, "INFO", f"Uninstalled {selected_app} on {selected_device}\n{result.strip()}")

            # 从选项列表中移除已卸载的应用
            if selected_app in self.apps:
                self.apps.remove(selected_app)
                wx.CallAfter(self.combo_apps.SetItems, self.apps)
                wx.CallAfter(self.combo_apps.SetValue, "")  # 清除选择的值
        except subprocess.CalledProcessError as e:
            wx.CallAfter(self.log_message, "ERROR",
                         f"Failed to uninstall {selected_app} on {selected_device}\n{e.output}")

    def on_input_text(self, event):
        # 获取触发事件的输入框对象
        source = event.GetEventObject()
        input_text = source.GetValue()

        selected_devices = self.listbox_devices.GetSelections()
        if not selected_devices:
            self.log_message("WARNING", "No device selected")
            return

        if not input_text:
            self.log_message("WARNING", "No input text provided")
            return

        for device in selected_devices:
            selected_device = self.listbox_devices.GetString(device)
            thread = threading.Thread(target=self.execute_input_text_command, args=(selected_device, input_text))
            thread.start()

    def execute_input_text_command(self, selected_device, input_text):
        try:
            input_command = ["adb", "-s", selected_device, "shell", "input", "text", input_text]
            subprocess.check_output(input_command, stderr=subprocess.STDOUT, text=True, encoding='utf-8',
                                    errors='ignore',
                                    creationflags=subprocess.CREATE_NO_WINDOW)
            wx.CallAfter(self.log_message, "INFO", f"Text '{input_text}' input on {selected_device}")
        except subprocess.CalledProcessError as e:
            wx.CallAfter(self.log_message, "ERROR", f"Failed to input text on {selected_device}\n{e.output}")

    def on_clear_app_data(self, event):
        selected_devices = self.listbox_devices.GetSelections()
        selected_app = self.combo_apps.GetValue()
        if not selected_devices:
            self.log_message("WARNING", "No device selected")
            return
        if not selected_app:
            self.log_message("WARNING", "No app selected")
            return
        for device in selected_devices:
            selected_device = self.listbox_devices.GetString(device)
            thread = threading.Thread(target=self.execute_clear_app_data, args=(selected_device, selected_app))
            thread.start()

    def execute_clear_app_data(self, selected_device, selected_app):
        try:
            clear_data_command = ["adb", "-s", selected_device, "shell", "pm", "clear", selected_app]
            result = subprocess.check_output(clear_data_command, stderr=subprocess.STDOUT, text=True, encoding='utf-8',
                                             errors='ignore', creationflags=subprocess.CREATE_NO_WINDOW)
            wx.CallAfter(self.log_message, "INFO",
                         f"Cleared data for {selected_app} on {selected_device}\n{result.strip()}")
        except subprocess.CalledProcessError as e:
            wx.CallAfter(self.log_message, "ERROR",
                         f"Failed to clear data for {selected_app} on {selected_device}\n{e.output}")

    def on_save_logs(self, event):
        selected_devices = self.listbox_devices.GetSelections()
        if not selected_devices:
            self.log_message("WARNING", "Please select a device first!")
            return

        # 选择保存日志的文件夹
        dlg = wx.DirDialog(self, "Choose a directory to save logs", "", wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            save_directory = dlg.GetPath()

            for index in selected_devices:
                device_name = self.listbox_devices.GetString(index)
                sanitized_device_name = sanitize_device_name(device_name)
                log_file_path = os.path.join(save_directory, f"{sanitized_device_name}_log.txt")

                # 获取并保存设备日志
                self.save_device_log(device_name, log_file_path)
            wx.CallAfter(self.log_message, "WARNING", "Log saving completed.")
        dlg.Destroy()

    def save_device_log(self, device_name, log_file):
        try:
            # adb logcat -d: 获取当前日志，并在执行后退出
            adb_command = f"adb -s {device_name} logcat -d"
            result = subprocess.run(adb_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    creationflags=subprocess.CREATE_NO_WINDOW, encoding='utf-8')

            # 如果命令执行成功，保存日志
            if result.returncode == 0:
                if result.stdout:
                    with open(log_file, 'w', encoding='utf-8') as log_output:
                        log_output.write(result.stdout)
                    self.log_message("INFO", f"Successfully saved log for {device_name} to {log_file}")
                else:
                    self.log_message("WARNING", f"No log output for {device_name}")
            else:
                # 如果命令执行失败，记录错误信息
                self.log_message("WARNING", f"Failed to save log for {device_name}: {result.stderr}")
        except Exception as e:
            # 捕获异常，防止卡住
            self.log_message("ERROR", f"An error occurred while saving log for {device_name}: {str(e)}")

    def on_take_screenshot(self, event):
        selected_devices = self.listbox_devices.GetSelections()
        if not selected_devices:
            self.log_message("WARNING", "No device selected")
            return
        screenshot_dir = wx.DirSelector("Select screenshot directory")
        if not screenshot_dir:
            self.log_message("WARNING", "No screenshot directory selected")
            return
        for device in selected_devices:
            selected_device = self.listbox_devices.GetString(device)
            sanitized_device_name = sanitize_device_name(selected_device)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = os.path.join(screenshot_dir, f"screenshot_{timestamp}_{sanitized_device_name}.png")
            thread = threading.Thread(target=self.execute_screenshot_command, args=(selected_device, screenshot_path))
            thread.start()

    def execute_screenshot_command(self, selected_device, screenshot_path):
        try:
            screenshot_command = ["adb", "-s", selected_device, "shell", "screencap", "-p", "/sdcard/screenshot.png"]
            subprocess.check_output(screenshot_command, stderr=subprocess.STDOUT, text=True, encoding='utf-8',
                                    errors='ignore', creationflags=subprocess.CREATE_NO_WINDOW)
            pull_command = ["adb", "-s", selected_device, "pull", "/sdcard/screenshot.png", screenshot_path]
            subprocess.check_output(pull_command, stderr=subprocess.STDOUT, text=True, encoding='utf-8',
                                    errors='ignore', creationflags=subprocess.CREATE_NO_WINDOW)
            wx.CallAfter(self.log_message, "INFO", f"Screenshot saved to {screenshot_path}")
            wx.CallAfter(self.display_screenshot, screenshot_path)  # 在主线程中显示截图
        except subprocess.CalledProcessError as e:
            wx.CallAfter(self.log_message, "ERROR", f"Failed to take screenshot on {selected_device}\n{e.output}")

    def display_screenshot(self, screenshot_path):
        dlg = ScreenshotDialog(self, screenshot_path)
        dlg.ShowModal()
        dlg.Destroy()

    def copy_screenshot_to_clipboard(self, screenshot_path):
        with open(screenshot_path, 'rb') as file:
            image_data = file.read()
            pyperclip.copy(image_data)  # 复制截图内容到剪贴板

    def on_disconnect_device(self, event):
        selected_devices = self.listbox_devices.GetSelections()
        if not selected_devices:
            self.log_message("WARNING", "No device selected")
            return

        for device in selected_devices:
            selected_device = self.listbox_devices.GetString(device)
            thread = threading.Thread(target=self.execute_disconnect_command, args=(selected_device,))
            thread.start()

    def execute_disconnect_command(self, selected_device):
        try:
            result = subprocess.run(
                ['adb', 'disconnect', selected_device],
                capture_output=True,
                text=True,
                timeout=10,
                encoding='utf-8',
                errors='ignore',
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            if "disconnected" in result.stdout:
                wx.CallAfter(self.log_message, "INFO", f"Disconnected from {selected_device}")
            else:
                wx.CallAfter(self.log_message, "ERROR", f"Unable to disconnect from {selected_device}: {result.stderr}")
        except subprocess.TimeoutExpired:
            wx.CallAfter(self.log_message, "ERROR", "Disconnection attempt timed out. Please try again.")
        except Exception as e:
            wx.CallAfter(self.log_message, "ERROR", f"Error: Unable to disconnect from {selected_device}: {str(e)}")

        wx.CallAfter(self.get_devices)  # 确保在主线程中刷新设备列表

    # 更新设备列表的方法
    def get_devices(self):
        try:
            command = ["adb", "devices"]
            result = self.execute_adb_command(command)
            # 简化字符串处理
            devices = [
                line.split()[0].strip()
                for line in result.splitlines()
                if line.strip().endswith("device")
            ]
            wx.CallAfter(self.update_device_list, devices)

        except subprocess.CalledProcessError as e:
            wx.CallAfter(self.log_message, "ERROR", f"Failed to get devices: {e.output}")
        except Exception as e:
            wx.CallAfter(self.log_message, "ERROR", f"Unexpected error occurred: {e}")

    def update_device_list(self, devices):
        self.devices = devices
        if self.devices:
            self.listbox_devices.SetItems(self.devices)
            self.log_message("INFO", f"Refreshing Devices List: {', '.join(self.devices)}\n")
        else:
            self.listbox_devices.SetItems([])  # Clear the listbox if no devices are connected
            self.log_message("WARNING", "No devices connected")

        # 适应设备列表大小，取消滑动框
        self.listbox_devices.FitInside()
        self.listbox_devices.Layout()

    # Method to log messages
    def log_message(self, level, message):
        wx.CallAfter(self._log_message, level, message)

    def _log_message(self, level, message):
        if level == "INFO":
            style = 1
        elif level == "WARNING":
            style = 2
        elif level == "ERROR":
            style = 3
        else:
            style = 0

        start_pos = self.text_output.GetTextLength()
        self.text_output.AppendText(f"{level}: {message}\n")
        end_pos = self.text_output.GetTextLength()

        # Apply styling
        self.text_output.StartStyling(start_pos)
        self.text_output.SetStyling(end_pos - start_pos, style)

        # Move cursor to the end to show the latest log
        self.text_output.GotoPos(end_pos)

        # Force scroll to bottom
        self.text_output.EnsureCaretVisible()  # This ensures the caret is visible and scrolls to it if necessary

    # Method to clear the log
    def on_clear_log(self, event):
        wx.CallAfter(self.text_output.ClearAll)

    def on_kill_server(self, event):
        thread = threading.Thread(target=self._kill_server)
        thread.start()

    def _kill_server(self):
        try:
            subprocess.check_output(
                ["adb", "kill-server"],
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                errors='ignore',
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            self.log_message("INFO", "ADB server killed successfully")
        except subprocess.CalledProcessError as e:
            self.log_message("ERROR", f"Failed to kill ADB server: {e.output}")

    def on_close(self, event):
        self.Destroy()

    def on_idle(self, event):
        while not self.log_queue.empty():
            log_level, message = self.log_queue.get()
            self.log_message(log_level, message)
        event.RequestMore()


class ScreenshotDialog(wx.Dialog):
    def __init__(self, parent, screenshot_path):
        super().__init__(parent, title="Screenshot", size=(900, 600))

        self.screenshot_path = screenshot_path
        self.screenshot_bitmap = wx.StaticBitmap(self)
        self.update_screenshot_bitmap_threadsafe()

        copy_button = wx.Button(self, label="Copy to Clipboard")
        copy_button.Bind(wx.EVT_BUTTON, self.on_copy_to_clipboard)

        self.info_bar = wx.InfoBar(self)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.screenshot_bitmap, 1, wx.EXPAND | wx.ALL, 10)
        vbox.Add(copy_button, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        vbox.Add(self.info_bar, 0, wx.EXPAND)

        self.SetSizer(vbox)
        self.Layout()

        self.call_later_timer = None
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def update_screenshot_bitmap_threadsafe(self, screenshot_path=None):
        if screenshot_path is None:
            screenshot_path = self.screenshot_path  # 如果没有提供新的路径，使用类变量
        thread = threading.Thread(target=self._update_screenshot_bitmap, args=(screenshot_path,))
        thread.start()

    def _update_screenshot_bitmap(self, screenshot_path):
        try:
            img = wx.Image(screenshot_path, wx.BITMAP_TYPE_PNG)
            scaled_img = self.scale_image(img)
            wx.CallAfter(self.screenshot_bitmap.SetBitmap, wx.Bitmap(scaled_img))
            wx.CallAfter(self.Layout)
        except Exception as e:
            wx.CallAfter(self.show_info_bar, f"Failed to load screenshot: {str(e)}", wx.ICON_ERROR)
            # 考虑添加日志记录此处的异常，以便于问题诊断

    def scale_image(self, img):
        dialog_width, dialog_height = self.GetClientSize()
        padding_width = 20  # 窗口边距和控件间距
        padding_height = 60  # 窗口边距和控件间距及按钮的高度

        scale_width = dialog_width - padding_width
        scale_height = dialog_height - padding_height

        aspect_ratio = min(scale_width / img.GetWidth(), scale_height / img.GetHeight())
        new_width = int(img.GetWidth() * aspect_ratio)
        new_height = int(img.GetHeight() * aspect_ratio)

        return img.Scale(new_width, new_height, wx.IMAGE_QUALITY_HIGH)

    def on_copy_to_clipboard(self, event):
        if wx.TheClipboard.Open():
            try:
                image = wx.Image(self.screenshot_path, wx.BITMAP_TYPE_PNG)
                bitmap = wx.Bitmap(image)
                data_object = wx.BitmapDataObject(bitmap)
                wx.TheClipboard.SetData(data_object)
                wx.TheClipboard.Close()
                wx.CallAfter(self.show_info_bar, "Screenshot copied to clipboard", wx.ICON_INFORMATION)
            except Exception as e:
                wx.CallAfter(self.show_info_bar, f"Failed to copy screenshot to clipboard: {str(e)}", wx.ICON_ERROR)
        else:
            wx.CallAfter(self.show_info_bar, "Unable to open clipboard", wx.ICON_ERROR)

    def show_info_bar(self, message, icon):
        self.info_bar.ShowMessage(message, icon)
        if self.call_later_timer:
            self.call_later_timer.Stop()
        self.call_later_timer = wx.CallLater(1000, self.info_bar.Dismiss)  # 使InfoBar在2秒后自动关闭

    def on_close(self, event):
        if self.call_later_timer:
            self.call_later_timer.Stop()
        self.Destroy()


if __name__ == '__main__':
    app = wx.App(False)
    frame = ADBManager(None, "ADB Manager")
    app.MainLoop()
