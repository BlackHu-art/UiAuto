# -*- coding: utf-8 -*-

import calendar
import datetime
import time
import pytz  # 用于处理时区


class DateTimeTool:
    @classmethod
    def getNowTime(cls, format='%Y-%m-%d %H:%M:%S', timezone=None):
        """
        获取当前时间字符串。

        :param format: 时间格式，默认为 '%Y-%m-%d %H:%M:%S'
        :param timezone: 时区，默认为本地时区
        :return: 当前时间的字符串表示
        """
        if timezone:
            tz = pytz.timezone(timezone)
            now = datetime.datetime.now(tz)
        else:
            now = datetime.datetime.now()
        return now.strftime(format)

    @classmethod
    def getNowDate(cls, format='%Y-%m-%d', timezone=None):
        """
        获取当前日期字符串。

        :param format: 日期格式，默认为 '%Y-%m-%d'
        :param timezone: 时区，默认为本地时区
        :return: 当前日期的字符串表示
        """
        if timezone:
            tz = pytz.timezone(timezone)
            now = datetime.datetime.now(tz).date()
        else:
            now = datetime.date.today()
        return now.strftime(format)

    @classmethod
    def getNowTimeStampWithSecond(cls, timezone=None):
        """
        获取当前时间戳（秒）。

        :param timezone: 时区，默认为本地时区
        :return: 当前时间戳（秒）
        """
        if timezone:
            tz = pytz.timezone(timezone)
            now = datetime.datetime.now(tz)
        else:
            now = datetime.datetime.now()
        return int(now.timestamp())

    @classmethod
    def getNowTimeStampWithMillisecond(cls, timezone=None):
        """
        获取当前时间戳（毫秒）。

        :param timezone: 时区，默认为本地时区
        :return: 当前时间戳（毫秒）
        """
        if timezone:
            tz = pytz.timezone(timezone)
            now = datetime.datetime.now(tz)
        else:
            now = datetime.datetime.now()
        return int(round(now.timestamp() * 1000))

    @classmethod
    def timeStampToDateTime(cls, timeStamp: int, is_with_millisecond=False):
        """
        将时间戳转换为 datetime 对象。

        :param timeStamp: 时间戳
        :param is_with_millisecond: 是否为毫秒时间戳，默认为 False
        :return: 转换后的 datetime 对象
        """
        try:
            if is_with_millisecond:
                timeStamp = timeStamp / 1000
            resultDateTime = datetime.datetime.fromtimestamp(timeStamp)
            return resultDateTime
        except Exception as e:
            print(f"Error converting timestamp to datetime: {e}")
            return None

    @classmethod
    def strToTimeStamp(cls, str, str_format: str = '%Y-%m-%d %H:%M:%S', is_with_millisecond=False):
        """
        将日期字符串转换为时间戳。

        :param str: 日期字符串
        :param str_format: 日期字符串格式，默认为 '%Y-%m-%d %H:%M:%S'
        :param is_with_millisecond: 是否返回毫秒时间戳，默认为 False
        :return: 转换后的时间戳
        """
        try:
            dst_dateTime = datetime.datetime.strptime(str, str_format)
            if is_with_millisecond:
                timestamp = int(time.mktime(dst_dateTime.timetuple()) * 1000)
            else:
                timestamp = int(time.mktime(dst_dateTime.timetuple()))
            return timestamp
        except Exception as e:
            print(f"Error converting string to timestamp: {e}")
            return None

    @classmethod
    def getWeekDay(cls, start_on_monday=True):
        """
        获取今天的星期几，从1开始。

        :param start_on_monday: 如果为 True，则从周一（1）开始计数；否则从周日（1）开始计数
        :return: 星期几，从1开始
        """
        if start_on_monday:
            return datetime.datetime.now().weekday() + 1
        else:
            return datetime.datetime.now().isoweekday()

    @classmethod
    def getHowDaysAgo(cls, targetDateTime, targetDateTime_format='%Y-%m-%d %H:%M:%S', howDaysAgo=0):
        """
        获取目标日期多少天之前或之后的日期。

        :param targetDateTime: 目标日期字符串
        :param targetDateTime_format: 目标日期字符串格式，默认为 '%Y-%m-%d %H:%M:%S'
        :param howDaysAgo: 天数，默认为 0
        :return: 目标日期多少天之前的日期
        """
        targetDateTime = datetime.datetime.strptime(targetDateTime, targetDateTime_format)
        resultDateTime = targetDateTime - datetime.timedelta(days=howDaysAgo)
        return resultDateTime

    @classmethod
    def dateTimeToStr(cls, theDateTime, format='%Y-%m-%d'):
        """
        将 datetime 对象转换为字符串。

        :param theDateTime: datetime 对象
        :param format: 日期格式，默认为 '%Y-%m-%d'
        :return: 日期字符串
        """
        return theDateTime.strftime(format)

    @classmethod
    def strToDateTime(cls, str, str_format: str = '%Y-%m-%d %H:%M:%S'):
        """
        将日期字符串转换为 datetime 对象。

        :param str: 日期字符串
        :param str_format: 日期字符串格式，默认为 '%Y-%m-%d %H:%M:%S'
        :return: datetime 对象
        """
        dst_dateTime = datetime.datetime.strptime(str, str_format)
        return dst_dateTime

    @classmethod
    def getHowYearsAgo(cls, nowDate, howYearsAgo=0, nowDate_format='%Y-%m-%d'):
        """
        获取目标日期多少年之前或之后的日期。

        :param nowDate: 目标日期字符串
        :param howYearsAgo: 年数，默认为 0
        :param nowDate_format: 目标日期字符串格式，默认为 '%Y-%m-%d'
        :return: 目标日期多少年之前的日期
        """
        nowDate = datetime.datetime.strptime(nowDate, nowDate_format)
        resultDate = nowDate - datetime.timedelta(days=howYearsAgo * 365)
        return resultDate

    @classmethod
    def getCurrentMonthFirstDayOrLastDay(cls, day_type=1):
        """
        获取当前月的第一天或最后一天日期。

        :param day_type: 类型，默认为 1 表示第一天，-1 表示最后一天
        :return: 当前月的第一天或最后一天日期
        """
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        last_day = calendar.monthrange(year, month)[1]
        if day_type == 1:
            start = datetime.date(year, month, 1)
            return start
        elif day_type == -1:
            end = datetime.date(year, month, last_day)
            return end
