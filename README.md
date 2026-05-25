# [自动化测试]()

# [概况]()
* 本项目支持接口自动化测试、app ui自动化测试、web ui自动化测试、性能测试
* 本项目由以下工具组成
    * pytest：python的一个单元测试框架,https://docs.pytest.org/en/latest/
    * pytest-xdist：pytest的一个插件,可多进程同时执行测试用例,https://github.com/pytest-dev/pytest-xdist
    * allure-pytest：用于生成测试报告,http://allure.qatools.ru/
    * PyHamcrest：一个匹配器对象的框架，用于断言，https://github.com/hamcrest/PyHamcrest
    * requests：http请求框架,http://docs.python-requests.org/en/master/
    * Appium：移动端的自动化测试框架,https://github.com/appium/appium/tree/v1.15.1
    * JPype1：用于执行java代码,https://github.com/jpype-project/jpype
    * paramiko：ssh客户端,https://docs.paramiko.org/en/stable/
    * Pillow：用于图片处理,https://pillow.readthedocs.io/en/latest/
    * PyMySQL：用于操作MySQL数据库,https://github.com/PyMySQL/PyMySQL
    * allpairspy: 用于将参数列表进行正交分析，实现正交分析法用例覆盖，https://pypi.org/project/allpairspy/
    * websockets：用于websocket请求，https://github.com/aaugustin/websockets
    * sqlacodegen：用于根据数据库表结构生成python对象，https://github.com/agronholm/sqlacodegen
    * SQLAlchemy：SQL工具包及对象关系映射（ORM）工具，https://github.com/sqlalchemy/sqlalchemy
* 当前仅支持Python>=3.6
* 项目如需执行java代码(即使用jpype1)，则项目目录所在的路径不可包含中文
    
# [使用]()
## 一、环境准备
### 1、脚本运行环境准备
#### 1.1、安装系统依赖
* Windows:
    * 安装Microsoft Visual C++ 2019 Redistributable，下载地址：https://visualstudio.microsoft.com/zh-hans/downloads/ 【jpype1、图像识别字库所需依赖】

#### 1.2、安装python依赖模块
* pip3 install -r requirements.txt
* 安装pgmagick
    * Linux:
        * pip3 install pgmagick==0.7.6
    * Windows:
        * 下载安装对应版本：https://www.lfd.uci.edu/~gohlke/pythonlibs/#pgmagick

#### 1.3、安装allure
* 源安装
    * sudo apt-add-repository ppa:qameta/allure
    * sudo apt-get update 
    * sudo apt-get install allure
    * 其他安装方式：https://github.com/allure-framework/allure2
* 手动安装
    * 下载2.7.0版本:https://github.com/allure-framework/allure2/releases
    * 解压allure-2.7.0.zip
    * 加入系统环境变量:export PATH=/home/john/allure-2.7.0/bin:$PATH

#### 1.4、安装openjdk8或jdk8
* sudo add-apt-repository ppa:openjdk-r/ppa
* sudo apt-get update
* sudo apt-get install openjdk-8-jdk

#### 1.5、安装maven
* 完成maven的安装配置

#### 1.6、安装Oracle Instant Client
* Windows
    * 下载地址:http://www.oracle.com/technetwork/topics/winx64soft-089540.html
    * 下载安装包instantclient-basic-windows.x64-11.2.0.4.0.zip
    * 解压zip包,并配置环境变量
        * 系统环境变量加入D:\instantclient-basic-windows.x64-11.2.0.4.0\instantclient_11_2
        * 配置中文编码,环境变量创建NLS_LANG=SIMPLIFIED CHINESE_CHINA.UTF8  
    * 注意:如果使用64位,python和instantclient都需要使用64位

#### 1.7、图像识别字库准备
* 下载对应字库:https://github.com/tesseract-ocr/tessdata
* 将下载的字库放到common/java/lib/tess4j/tessdata/
* Windows
    * 安装Microsoft Visual C++ 2019 Redistributable，下载地址：https://visualstudio.microsoft.com/zh-hans/downloads/



### 3、appium server运行环境准备
#### 3.1、安装jdk1.8,并配置环境变量
* export JAVA_HOME=/usr/lib/jvm/jdk8
* export JRE_HOME=${JAVA_HOME}/jre 
* export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
* export PATH=${JAVA_HOME}/bin:$PATH

#### 3.2、安装配置appium server
* 安装appium desktop server
    * 下载Appium-windows-1.15.1.exe
    * 下载地址:https://github.com/appium/appium-desktop/releases
    * 以管理员身份启动服务

* Android环境准备
    * 安装java(JDK),并配置JAVA_HOME=/usr/lib/jvm/jdk8
    * 安装Android SDK,并配置ANDROID_HOME="/usr/local/adt/sdk"
    * 使用SDK manager安装需要进行自动化的Android API版本

* Windows环境准备
    * 支持Windows10及以上版本
    * 设置Windows处于开发者模式
    * 下载WinAppDriver并安装(V1.1版本),https://github.com/Microsoft/WinAppDriver/releases
    * \[可选\]下载安装WindowsSDK,在Windows Kits\10\bin\10.0.17763.0\x64内包含有inspect.exe用于定位Windows程序的元素信息


* 修改性能测试负载机的系统最大打开文件数,避免并发用户数大于最大打开文件数

## 三、运行测试
* cd AutomationTest/
* python3 -u run_app_ui_test.py --help
* python3 -u run_app_ui_test.py 运行cases/app_ui/目录所有的用例
* python3 -u run_app_ui_test.py -tt phone -k keyword 运行匹配关键字的用例，会匹配文件名、类名、方法名
* python3 -u run_app_ui_test.py -tt phone -d dir     运行指定目录的用例，默认运行cases/app_ui/目录
* python3 -u run_app_ui_test.py -m mark              运行指定标记的用例



## 四、生成测试报告
* cd AutomationTest/
* python3 -u generateReport_app_ui_test_report.py -sp 9084
* 访问地址http://ip:9084

## 五、项目说明
* 元素的显式等待时间默认为30s
* 封装的显式等待类型支持:page_objects/app_ui/wait_type.py
* 封装的定位类型支持:page_objects/app_ui/locator_type.py
* 项目
    * android 
        * demoProject 例子项目

# [项目结构]()
* base 基础请求类
* cases 测试用例目录
* common 公共模块
* common_projects 每个项目的公共模块
* config　配置文件
* init 初始化
* logs 日志目录
* output 测试结果输出目录 
* packages app ui测试的安装包
* page_objects 页面映射对象
* pojo 存放自定义类对象
* test_data 测试所需的测试数据目录

# [编码规范]()
* 统一使用python >= 3.6.8
* 编码使用-\*- coding:utf8 -\*-,且不指定解释器
* 类/方法的注释均写在class/def下一行，并且用三个双引号形式注释
* 局部代码注释使用#号
* 所有中文都直接使用字符串，不转换成Unicode，即不是用【u'中文'】编写
* 所有的测试模块文件都以test_projectName_moduleName.py命名
* 所有的测试类都以Test开头，类中方法(用例)都以test_开头
* 每个测试项目都在cases目录里创建一个目录，且目录都包含有api、scenrarios两个目录
* case对应setup/teardown的fixture统一命名成fixture_[test_case_method_name]
* 每一个模块中测试用例如果有顺序要求【主要针对ui自动化测试】，则自上而下排序，pytest在单个模块里会自上而下按顺序执行

# [pytest常用]()
* @pytest.mark.skip(reason='该功能已废弃')
* @pytest.mark.parametrize('key1,key2',[(key1_value1,key2_value2),(key1_value2,key2_value2)])
* @pytest.mark.usefixtures('func_name')

# [注意点]()
* 运行pytest时指定的目录内应当有conftest.py，方能在其他模块中使用。@allure.step会影响fixture，故在脚本中不使用@allure.step
* 由于web ui配置的驱动是直接设置在系统环境变量，app ui指定了混合应用的浏览器驱动，在运行app ui时appium有可能会读取到系统的环境变量的配置，故运行时请排查此情况
* 数据库操作，所有表操作均进行单表操作，如需多表查询，使用代码进行聚合

* app ui测试
    * 能用id、name、link(不常变化的链接)定位的，不使用css定位，能使用css定位，不使用xpath定位
    * 如需要上传文件到手机或者从手机下载文件，请确保有手机对应目录的读写权限
    * 视频录制统一对单个单个case进行，保证录制时间不超过3分钟，且录制文件不要过大，否则会引起手机内存无法存储视频
            * 确认手机是否能进行视频录制执行命令adb shell screenrecord /sdcard/test.mp4，能正常执行即可
    * 设备屏幕坐标系原点都在最左上角，往右x轴递增，往下y轴递增