# Android UI 自动化测试框架

这是一个基于 Python、pytest、Appium 2、UiAutomator2 和 Allure 的 Android UI 自动化测试框架，用于对已有 APK 在一台或多台 Android 设备上执行自动化测试。

框架支持：

- 从 `config/appium.yaml` 读取设备矩阵。
- 每台设备独立启动和关闭 Appium 服务。
- 多设备并行执行，单设备内保持用例顺序。
- 每台设备生成独立 Allure 报告。
- 统一保存日志、截图、页面源码和运行元数据。
- 使用 PO 分层组织页面对象和业务用例。

## 环境准备

安装 Python 依赖：

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

安装 Appium 2 和 Android 驱动：

```bash
npm install -g appium@2
bash scripts/install_uiautomator2.sh
```

检查本机 Android/Appium 工具：

```bash
python --version
node --version
java -version
adb version
appium -v
adb devices
```

Allure 原始结果由 `allure-pytest` 生成，HTML 报告由全局安装的 Allure CLI 生成。

## 配置说明

APK 放在 `apps/` 目录下，并在 `config/appium.yaml` 中配置 `android.app`。

多设备配置位于 `config/appium.yaml` 的 `android.devices` 下。每台设备必须配置唯一的：

- `name`
- `udid`
- `appium_port`
- `system_port`
- `chromedriver_port`
- `mjpeg_server_port`

如果 Appium 无法从 APK 自动识别启动信息，需要手动配置：

- `app_package`
- `app_activity`
- `app_wait_activity`

如果命令行、pytest 和 Appium 解析到不同的 Android SDK，可以在 `.env` 中固定：

```bash
ANDROID_ADB_PATH=
ANDROID_SDK_ROOT=
ANDROID_HOME=
```

这些环境变量会被 runner、pytest fixture 和 Appium 子进程共同使用。

## Appium 服务管理

默认情况下，框架会托管 Appium 服务：

```yaml
appium:
  manage_servers: true
```

当一台设备开始执行本轮测试时，框架会为它启动一个独立 Appium 服务，并等待 `http://host:port/status` 健康检查通过。该设备的所有测试执行完成后，框架再关闭对应服务。

多设备执行时，每台设备使用自己的 `appium_port`，避免多个设备争用同一个 Appium 服务。

如果端口上存在旧的本地 Appium 进程，框架会按配置自动清理残留服务。只有在明确需要复用外部 Appium 服务时，才建议关闭托管模式：

```bash
set APPIUM_MANAGE_SERVERS=false
python run_tests.py --device emulator_5554
```

## 执行方式

默认执行 `config/appium.yaml` 中配置的所有设备：

```bash
python run_tests.py
```

执行指定设备：

```bash
python run_tests.py --device emulator_5554
```

执行多台指定设备：

```bash
python run_tests.py --device emulator_5554 --device emulator_5556
```

显式执行全部配置设备：

```bash
python run_tests.py --all-devices
```

列出配置设备：

```bash
python run_tests.py --list-devices
```

只执行运行前检查：

```bash
python run_tests.py --preflight --all-devices
```

当选择多台设备时，runner 会自动追加：

```bash
-n <device_count> --dist=loadgroup
```

这样可以保证不同设备并行执行，同时同一台设备上的有序用例不会被拆散到多个 worker。

如果模拟器启动较慢或偶发 `adb` 发现失败，可以在 `.env` 中适当调大：

```bash
ANDROID_ADB_EXEC_TIMEOUT=
```

并保留默认的 session 重试配置，让短暂的设备发现失败有机会自动恢复。

## 报告和产物

默认每次运行都会写入 `reports/latest`：

```text
reports/latest/
  logs/
    YYYY-MM-DD/
      HHMMSS/
        master.log
        gw0.log
        appium/
          emulator_5554.log
          emulator_5556.log
  screenshots/
  page_sources/
  metadata/
  allure-results/
  allure-results-<device>/
  allure-report/              # 单设备运行时生成
  allure-report-<device>/     # 多设备运行时按设备生成
```

失败截图、页面源码、session 元数据会在可用时自动附加到 Allure。

多设备运行时，框架只生成每台设备各自独立的 Allure HTML 报告，不保留混合 HTML 报告，避免不同设备结果混在一起。

如需单独保留某次执行结果，可以指定报告目录：

```bash
python run_tests.py --report-dir reports/<name>
```

## 日志说明

控制台日志按级别输出不同颜色，方便快速区分普通信息、警告和错误。

文件日志按日期和运行时间保存：

```text
reports/latest/logs/YYYY-MM-DD/HHMMSS/
```

Appium 子进程日志保存在同一轮日志目录下的 `appium/` 子目录中。旧日期日志会根据 `ANDROID_AUTOMATION_LOG_RETENTION_DAYS` 自动清理。

如果 Windows 控制台中文显示异常，可以先执行：

```bash
chcp 65001
```

## 项目结构

当前项目采用 PO 分层设计，同时保留多设备执行、日志、报告和诊断能力：

```text
config/
  appium.yaml                             # 全局 Appium 和设备配置
src/android_automation/base/
  base_page.py                            # 页面对象基类
src/android_automation/pages/
  login_page.py                           # 登录页面对象示例
  home_page.py                            # 首页页面对象示例
  app_page.py                             # 通用应用状态页面对象
src/android_automation/utils/
  logger.py                               # 日志工具导出
  adb_utils.py                            # ADB 工具导出
src/android_automation/
  runner.py                               # CLI 编排、preflight、pytest 执行和 Allure 报告生成
  config.py                               # YAML/.env 加载、设备矩阵校验
  appium_service.py                       # Appium 服务启动、关闭和健康检查
  driver_factory.py                       # Appium capability 构建
  runtime.py                              # runner 和 pytest 共享的运行上下文
  session.py                              # Appium driver session 创建和重试
  artifacts.py                            # 截图、页面源码、元数据和 Allure 附件
test_cases/
  conftest.py                             # pytest 全局入口，兼容转发到当前 fixture 实现
  test_app_lifecycle.py                   # 应用安装/卸载生命周期用例入口
  test_smoke.py                           # 启动冒烟用例入口
tests/
  ...                                     # 保留现有测试实现，兼容旧入口
```

## 默认用例顺序

默认有序流程为：

1. 安装应用
2. 启动应用
3. 可选元素检查
4. 卸载应用

多设备执行时，`--dist=loadgroup` 会让同一台设备的有序流程保持在同一个 worker 上执行，不同设备之间并行运行。

