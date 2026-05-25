#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  
 @time        :    16:32
"""
import os
import platform
import subprocess
import argparse
from base.read_report_config import Read_Report_Config
from common.custom_multiprocessing import Custom_Pool
from common.dateTimeTool import DateTimeTool
from common.logger.logTool import logger
from common.network import Network
from common.strTool import StrTool


class AllureReportGenerator:

    def __init__(self, start_port=None):
        if start_port:
            self.start_port = start_port
        else:
            report_config = Read_Report_Config().report_config
            self.start_port = report_config.app_ui_start_port

        self.test_time = DateTimeTool.getNowTime('%Y_%m_%d_%H_%M_%S_%f')
        self.report_dirs = self._get_report_dirs()

    @staticmethod
    def _get_report_dirs():
        report_dirs = []
        devices_dirs = os.listdir('output/')
        for device_dir in devices_dirs:
            for report_dir in os.listdir(f'output/{device_dir}'):
                report_dirs.append(f'output/{device_dir}/{report_dir}')
        return report_dirs

    def generate_windows_report(self, report_dir, port):
        generate_report_command = f'allure generate {report_dir}/report_data -o {report_dir}/report/app_ui_report_{self.test_time}'
        subprocess.check_output(generate_report_command, shell=True)
        open_report_command = f'start cmd.exe @cmd /c "allure open -p {port} {report_dir}/report/app_ui_report_{self.test_time}"'
        subprocess.check_output(open_report_command, shell=True)

    def run(self):
        if platform.system() == 'Windows':
            self._generate_windows_reports()
        else:
            self._generate_linux_reports()

    def _generate_windows_reports(self):
        p_pool = Custom_Pool(20)
        for i, report_dir in enumerate(self.report_dirs):
            port = str(int(self.start_port) + i)
            self._kill_existing_process_windows(port)
            logger.info(f'生成报告 {report_dir}/report/app_ui_report_{self.test_time}, 使用端口 {port}')
            logger.info(f'报告地址: http://{Network.get_local_ip()}:{port}/')
            p = p_pool.apply_async(self.generate_windows_report, (report_dir, port))
        p_pool.close()
        p_pool.join()

    @staticmethod
    def _kill_existing_process_windows(port):
        get_allure_process_id_command = f'netstat -ano|findstr "0.0.0.0:{port}"'
        try:
            get_allure_process_id = subprocess.check_output(get_allure_process_id_command, shell=True)
            get_allure_process_id = get_allure_process_id.decode('utf-8')
            process_id = StrTool.getStringWithLBRB(get_allure_process_id, 'LISTENING', '\r\n').strip()
            kill_command = f'taskkill /F /pid {process_id}'
            subprocess.check_call(kill_command, shell=True)
            logger.info(f'关闭已监听端口 {port} 的进程，进程ID: {process_id}')
        except subprocess.CalledProcessError:
            logger.info(f'未找到监听端口 {port} 的服务')

    def _generate_linux_reports(self):
        get_allure_process_ids_command = "ps -ef|grep -i allure\\.CommandLine|grep -v grep|awk '{print $2}'"
        allure_process_ids = subprocess.check_output(get_allure_process_ids_command, shell=True).decode(
            'utf-8').splitlines()

        for i, report_dir in enumerate(self.report_dirs):
            port = str(int(self.start_port) + i)
            self._kill_existing_process_linux(port, allure_process_ids)
            print(
                f'{DateTimeTool.getNowTime()} 生成报告 {report_dir}/report/app_ui_report_{self.test_time}, 使用端口 {port}')
            print(f'{DateTimeTool.getNowTime()} 报告地址: http://{Network.get_local_ip()}:{port}/')
            self._generate_linux_report(report_dir, port)

    @staticmethod
    def _kill_existing_process_linux(port, allure_process_ids):
        get_port_process_ids_command = f"netstat -anp|grep -i {port}|grep -v grep|awk '{{print $7}}'|awk -F '/' '{{print $1}}'"
        port_process_ids = subprocess.check_output(get_port_process_ids_command, shell=True).decode(
            'utf-8').splitlines()

        for port_process_id in port_process_ids:
            if port_process_id in allure_process_ids:
                print(f'{DateTimeTool.getNowTime()} 关闭进程ID: {port_process_id}, 监听端口: {port}')
                subprocess.check_output(f"kill -9 {port_process_id}", shell=True)

    def _generate_linux_report(self, report_dir, port):
        generate_report_command = f'allure generate {report_dir}/report_data -o {report_dir}/report/app_ui_report_{self.test_time}'
        subprocess.check_output(generate_report_command, shell=True)
        open_report_command = f'nohup allure open -p {port} {report_dir}/report/app_ui_report_{self.test_time} >logs/generate_app_ui_test_report_{self.test_time}.log 2>&1 &'
        subprocess.check_output(open_report_command, shell=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-sp', '--start_port', help='生成报告使用的开始端口，多份报告每次加1', type=str)
    args = parser.parse_args()

    generator = AllureReportGenerator(start_port=args.start_port)
    generator.run()

    # 调用方法
    # generator = AllureReportGenerator(start_port="8080")
    # generator.run()