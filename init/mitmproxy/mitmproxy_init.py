from base.read_mitmproxy_config import Read_Mitmproxy_Config
from common.strTool import StrTool
from common.logger.logTool import logger
import multiprocessing
import platform
import subprocess


def start_mitmproxy(port, ssl_insecure):
    if 'Windows' == platform.system():
        if ssl_insecure:
            subprocess.check_output(
                "start cmd.exe @cmd /c mitmdump -k -p %s -s %s " % (port, 'init/mitmproxy/addons.py'), shell=True)
        else:
            subprocess.check_output("start cmd.exe @cmd /c mitmdump -p %s -s %s " % (port, 'init/mitmproxy/addons.py'),
                                    shell=True)
    else:
        if ssl_insecure:
            subprocess.check_output(
                'nohup mitmdump -k -p %s -s %s' % (port, 'init/mitmproxy/addons.py >>logs/mitmproxy.log 2>&1 &'),
                shell=True)
        else:
            subprocess.check_output(
                'nohup mitmdump -p %s -s %s' % (port, 'init/mitmproxy/addons.py >>logs/mitmproxy.log 2>&1 &'),
                shell=True)


def get_mitmproxy_process_id_windows(port):
    command = ['netstat', '-ano']
    findstr_command = ['findstr', f"0.0.0.0:{port}"]
    try:
        netstat_output = subprocess.check_output(command)
        findstr_output = subprocess.check_output(findstr_command, input=netstat_output)
        process_info = findstr_output.decode('utf-8')
        process_id = StrTool.getStringWithLBRB(process_info, 'LISTENING', '\r\n').strip()
        return process_id
    except Exception as e:
        logger.error(f'mitmproxy未查找到监听端口{port}的服务: {e}')
        return None


def kill_mitmproxy_process_windows(process_id):
    command = ['taskkill', '/F', '/PID', process_id]
    try:
        logger.info(f'关闭mitmproxy进程, 进程ID: {process_id}')
        subprocess.check_call(command)
    except Exception as e:
        logger.error(f'关闭mitmproxy进程失败, 进程ID: {process_id}, {e}')


def get_mitmproxy_process_ids_linux():
    command = ["ps", "-ef"]
    grep_commands = ["grep", "'mitmdump'", "|", "grep", "-v", "grep", "|", "awk", "'{print $2}'"]
    try:
        ps_output = subprocess.check_output(command)
        grep_output = subprocess.check_output(grep_commands, input=ps_output)
        process_ids = grep_output.decode('utf-8').split('\n')
        return [pid.strip() for pid in process_ids if pid.strip()]
    except Exception as e:
        logger.error(f'mitmproxy未查找到监听端口的服务: {e}')
        return []


def kill_mitmproxy_process_linux(process_id):
    command = ["kill", "-9", process_id]
    try:
        logger.info(f'关闭mitmproxy进程, 进程ID: {process_id}')
        subprocess.check_call(command)
    except Exception as e:
        logger.error(f'关闭mitmproxy进程失败, 进程ID: {process_id}, {e}')


def mitmproxy_init():
    mitmproxy_config = Read_Mitmproxy_Config().mitmproxy_config
    port = mitmproxy_config.proxy_port
    ssl_insecure = mitmproxy_config.ssl_insecure

    system = platform.system().lower()

    if system == "windows":
        process_id = get_mitmproxy_process_id_windows(port)
        if process_id:
            kill_mitmproxy_process_windows(process_id)

    elif system == "linux":
        process_ids = get_mitmproxy_process_ids_linux()
        for process_id in process_ids:
            kill_mitmproxy_process_linux(process_id)

    elif system == "darwin":
        pass

    logger.info(f'启动mitmproxy, 使用端口{port}')
    p = multiprocessing.Process(target=start_mitmproxy, args=(port, ssl_insecure,))
    p.daemon = True
    p.start()


