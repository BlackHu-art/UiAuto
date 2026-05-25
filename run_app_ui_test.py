# -*- coding: utf-8 -*-

from base.read_app_ui_config import Read_APP_UI_Config
from base.read_app_ui_devices_info import Read_APP_UI_Devices_Info
from common.httpclient.doRequest import DoRequest
from multiprocessing import Process
from common.fileTool import FileTool
from common.custom_multiprocessing import Custom_Pool
from common.pytest import deal_pytest_ini_file
from init.java.java_maven_init import java_maven_init
from init.httpserver.http_server_init import http_server_init
from init.mitmproxy.mitmproxy_init import mitmproxy_init
from common.logger.logTool import logger
import argparse
import os
import pytest
import sys
import ujson


def pytest_main(pytest_execute_params):
    """
    执行 pytest 测试，不返回退出码，仅记录执行状态。

    :param pytest_execute_params: pytest 的命令行参数列表
    :type pytest_execute_params: list
    """
    try:
        # 调用 pytest.main()
        pytest.main(pytest_execute_params)

        # 记录执行结果，确保将 int 转换为 str 输出
        # logger.info(f"pytest 主函数执行完成，退出码{exit_code}")

    except Exception as e:
        logger.error(f"pytest 主函数执行失败： {str(e)}", exc_info=True)
        raise


def start_app_device_test(index, device_info, keyword, dir, markexpr, capture, reruns, lf, clr):
    # 文件重命名逻辑增强
    for path, dirs, files in os.walk('config/app_ui_tmp'):
        for file in files:
            if file.isdigit() and int(file) == index:
                old_path = os.path.join(path, file)
                new_path = os.path.join(path, str(os.getpid()))
                try:
                    os.rename(old_path, new_path)
                    # 成功重命名文件
                except Exception as e:
                    logger.error(f"重命名文件 {old_path} 失败: {e}")
                    continue

    logger.info('开始检测appium server是否可用......')
    try:
        server_url = f"http://{device_info['server_ip']}:{device_info['server_port'].strip()}/wd/hub"
        do_request = DoRequest(server_url)
        http_response_result = do_request.get('/status')
        result = ujson.loads(http_response_result.body)
        if result['status'] == 0:
            logger.info('appium server状态为可用......')
        else:
            logger.error('appium server状态为不可用......')
            sys.exit(1)
    except Exception as e:
        logger.error(f'appium server状态为不可用: {e}')
        raise

    a_devices_desired_capabilities = device_info['capabilities']
    logger.info(f'开始设备{device_info["device_desc"]}测试......')

    for desired_capabilities in a_devices_desired_capabilities:
        # 将当前 Desired Capabilities 写入文件
        FileTool.writeObjectIntoFile(desired_capabilities,
                                     f'config/app_ui_tmp/{os.getpid()}_current_desired_capabilities')

        desired_capabilities_desc = None
        if 'appPackage' in desired_capabilities:
            desired_capabilities_desc = desired_capabilities['appPackage']
        elif 'app' in desired_capabilities:
            desired_capabilities_desc = desired_capabilities['app'].split('/')[-1]
        elif 'bundleId' in desired_capabilities:
            desired_capabilities_desc = desired_capabilities['bundleId']

        logger.info(f'当前设备开始测试的desired_capabilities为: {desired_capabilities}')

        # 构建 Pytest 的命令行参数
        pytest_execute_params = ['-c', 'config/pytest.ini', '-v', '--alluredir',
                                 f'output/{device_info["device_desc"]}/{desired_capabilities_desc}/report_data/']

        # 判断关键字参数
        if keyword:
            pytest_execute_params.append('-k')
            pytest_execute_params.append(keyword)
            logger.info(f'当前设备开始测试的关键字keyword为: {keyword}')
        # 判断markexpr参数
        if markexpr:
            pytest_execute_params.append('-m')
            pytest_execute_params.append(markexpr)
            logger.info(f'当前设备开始测试的markexpr为: {markexpr}')
        # 判断是否输出日志
        if capture:
            if int(capture):
                pytest_execute_params.append('-s')
        # 判断是否失败重跑
        if reruns:
            if int(reruns):
                pytest_execute_params.append('--reruns')
                pytest_execute_params.append(reruns)
                logger.info(f'当前设备失败重跑次数为: {reruns}')
        # 判断是否只运行上一次失败的用例
        if lf:
            if int(lf):
                pytest_execute_params.append('--lf')
                logger.info('只运行上一次失败的用例')
        # 判断是否清空已有测试结果
        if clr:
            if int(clr):
                pytest_execute_params.append('--clean-alluredir')
                logger.info(f'执行清空已有测试结果：{clr}')
        pytest_execute_params.append(dir)
        # 启动子进程
        process = Process(target=pytest_main, args=(pytest_execute_params,))
        process.start()
        process.join()
        # 子进程异常处理
        if process.exitcode != 0:
            logger.error(f'子进程执行失败，exitcode: {process.exitcode}')
            # 进行必要的清理工作
            process.close()
        logger.info(f'当前设备结束测试的desired_capabilities为: {desired_capabilities}')
    logger.info(f'结束设备{device_info["device_desc"]}测试......')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--keyword', help='只执行匹配关键字的用例，会匹配文件名、类名、方法名', type=str)
    parser.add_argument('-d', '--dir', help='指定要测试的目录', type=str)
    parser.add_argument('-m', '--markexpr', help='只运行符合给定的mark表达式的测试', type=str)
    parser.add_argument('-s', '--capture', help='是否在标准输出流中输出日志,1:是、0:否,默认为0', type=str)
    parser.add_argument('-r', '--reruns', help='失败重跑次数,默认为0', type=str)
    parser.add_argument('-lf', '--lf', help='是否运行上一次失败的用例,1:是、0:否,默认为0', type=str)
    parser.add_argument('-tt', '--test_type', help='【必填】测试类型,phone、windows', type=str)
    parser.add_argument('-dif', '--devices_info_file',
                        help='【必填】多设备并行信息文件，当--test_type为phone时，此选项需提供', type=str)
    parser.add_argument('-clr', '--clr', help='是否清空已有测试结果,1:是、0:否,默认为0', type=str)
    args = parser.parse_args()

    try:
        if not args.test_type:
            raise ValueError('请指定测试类型,查看帮助:python run_app_ui_test.py --help')

        # 处理pytest文件
        deal_pytest_ini_file()

        # 初始化java依赖的libs
        # java_maven_init()

        # 初始化httpserver
        http_server_init()

        # 初始化mitmproxy
        mitmproxy_init()

        keyword = args.keyword
        dir = args.dir
        markexpr = args.markexpr
        capture = args.capture
        reruns = args.reruns
        lf = args.lf
        clr = args.clr
        test_type = args.test_type.lower()
        devices_info_file = args.devices_info_file
        if test_type == 'phone':
            if not devices_info_file:
                raise ValueError('请指定多设备并行信息文件,查看帮助:python run_app_ui_test.py --help')
            logger.info('开始初始化进程......')
            p_pool = Custom_Pool(int(Read_APP_UI_Config().app_ui_config.max_device_pool))
            devices_info = Read_APP_UI_Devices_Info(devices_info_file).devices_info
            logger.info('当前使用的配置文件路径:' + devices_info_file)
            if os.path.exists('config/app_ui_tmp'):
                FileTool.truncateDir('config/app_ui_tmp/')
            else:
                os.makedirs('config/app_ui_tmp')
            for i in range(len(devices_info)):
                device_info = devices_info[i]
                FileTool.writeObjectIntoFile(device_info, f'config/app_ui_tmp/{i}')
                p = p_pool.apply_async(start_app_device_test,
                                       (i, device_info, keyword, dir, markexpr, capture, reruns, lf, clr))
            p_pool.close()
            p_pool.join()
        else:
            sys.exit()
    except Exception as e:
        logger.error(f'发生错误: {e}')
        sys.exit(1)
