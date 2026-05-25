#app ui 测试
#cd AutomationTest/
#usage: run_app_ui_test.py [-h] [-k KEYWORD] [-d DIR] [-m MARKEXPR] [-s CAPTURE] [-r RERUNS] [-lf LF] [-tt TEST_TYPE] [-dif DEVICES_INFO_FILE] [-clr CLR]
#
#options:
#  -h,   --help                                                       show this help message and exit
#  -k    KEYWORD,     --keyword KEYWORD                               只执行匹配关键字的用例，会匹配文件名、类名、方法名
#  -d    DIR,         --dir DIR                                       指定要测试的目录
#  -m    MARKEXPR,    --markexpr MARKEXPR                             只运行符合给定的mark表达式的测试
#  -s    CAPTURE,     --capture CAPTURE                               是否在标准输出流中输出日志,1:是、0:否,默认为0
#  -r    RERUNS,      --reruns RERUNS                                 失败重跑次数,默认为0
#  -lf   LF,          --lf LF                                         是否运行上一次失败的用例,1:是、0:否,默认为0
#  -tt   TEST_TYPE,   --test_type TEST_TYPE                          【必填】测试类型,phone、windows
#  -dif  DEVICES_INFO_FILE, --devices_info_file DEVICES_INFO_FILE    【必填】多设备并行信息文件，当--test_type为phone时，此选项需提供
#  -clr  CLR,         --clr CLR                                       是否清空已有测试结果,1:是、0:否,默认为0

python -u run_app_ui_test.py -d cases/doozy_tv -s 1 -lf 0 -tt phone -dif config/doozy_tv/devices_conf_info_tv.conf -clr 1

python -u run_app_ui_test.py -d cases/tests -s 1 -lf 0 -tt phone -dif config/doozy_tv/devices_conf_info_tv.conf -clr 1




#app ui 测试报告生成
#cd AutomationTest/
python -u generateReport_app_ui_test_report.py -sp 9084