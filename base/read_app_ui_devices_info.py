from pojo.app_ui_devices_info import APP_UI_Devices_Info
import configparser


class Read_APP_UI_Devices_Info(object):
    __instance = None
    __inited = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self, filepath):
        if self.__inited is None:
            self.devices_info = self._read_devices_info(filepath)
            self.__inited = True

    def _read_devices_info(self, filepath):
        try:
            config = configparser.ConfigParser()
            with open(filepath, 'r', encoding='utf-8') as file:
                config.read_file(file)

            devices_info = APP_UI_Devices_Info()

            def get_list(info, delimiter):
                return list(filter(None, info.split(delimiter))) if info else []

            devices_info.devices_desc = get_list(config.get('devices_info', 'devices_desc', fallback=''), '||')
            devices_info.app_ui_configs = get_list(config.get('devices_info', 'app_ui_configs', fallback=''), '||')

            api_configs = []
            for tmp_api_config in get_list(config.get('devices_info', 'api_configs', fallback=''), '||'):
                api_configs.append(get_list(tmp_api_config, '&&'))
            devices_info.api_configs = api_configs

            devices_info.server_ports = get_list(config.get('devices_info', 'server_ports', fallback=''), '||')
            devices_info.server_ips = get_list(config.get('devices_info', 'server_ips', fallback=''), '||')

            system_auth_alert_labels = []
            for tmp_system_auth_alert_label in get_list(
                    config.get('devices_info', 'system_auth_alert_labels', fallback=''), '||'):
                system_auth_alert_labels.append(get_list(tmp_system_auth_alert_label, '&&'))
            devices_info.system_auth_alert_labels = system_auth_alert_labels

            devices_info.is_enable_system_auth_check = get_list(
                config.get('devices_info', 'is_enable_system_auth_check', fallback=''), '||')
            # devices_info.udids = get_list(config.get('devices_info', 'udids', fallback=''), '||')
            devices_info.platformNames = get_list(config.get('devices_info', 'platformNames', fallback=''), '||')
            devices_info.automationNames = get_list(config.get('devices_info', 'automationNames', fallback=''), '||')
            devices_info.platformVersions = get_list(config.get('devices_info', 'platformVersions', fallback=''), '||')
            devices_info.deviceNames = get_list(config.get('devices_info', 'deviceNames', fallback=''), '||')
            devices_info.systemports = get_list(config.get('devices_info', 'systemports', fallback=''), '||')
            devices_info.appActivitys = get_list(config.get('devices_info', 'appActivitys', fallback=''), '||')
            devices_info.appPackages = get_list(config.get('devices_info', 'appPackages', fallback=''), '||')
            devices_info.bundleIds = get_list(config.get('devices_info', 'bundleIds', fallback=''), '||')
            devices_info.apps_dirs = get_list(config.get('devices_info', 'apps_dirs', fallback=''), '||')
            devices_info.apps_urls = get_list(config.get('devices_info', 'apps_urls', fallback=''), '||')
            devices_info.noSigns = get_list(config.get('devices_info', 'noSigns', fallback=''), '||')
            devices_info.fullResets = get_list(config.get('devices_info', 'fullResets', fallback=''), '||')
            devices_info.noResets = get_list(config.get('devices_info', 'noResets', fallback=''), '||')

            return devices_info.get_devices_info()

        except Exception as e:
            print(f"Error reading configuration file: {e}")
            return None

