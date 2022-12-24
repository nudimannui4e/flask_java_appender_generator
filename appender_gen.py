#!/usr/bin/env python

import sys


def usage():
    usage_string = """Скрипт использует 3 аргумента, для вывода logback.xml по шаблону
Пример: 
  1.LOGGER - имя класса, пример: com.panbet.web.managers.account.AccountManager
  2.LOGNAME - просто имя файла лога, указывается без расширения(!)
  3.LEVEL - уровень логирования. info | debug"""
    print(usage_string)


def generate_appender():
    if len(sys.argv) < 4:
        # Сюда добавить вывод имени аргумента, а не значения
        print('Not enough param\n') 
        usage()
    elif len(sys.argv) == 4:
        for param in sys.argv:
            if not isinstance(param, str):
                print(f'{param} shoud be a string')
        LOGGER = str(sys.argv[1])
        LOGNAME = str(sys.argv[2])
        LEVEL = str(sys.argv[3])  # create list of level in future
        # от этого желательно избавиться
        GMT_PATTERN = str('{"yyyy-MM-dd-HH" GMT}')
        LOG_PREFIX = str('${logPrefix}')
        appender = f'''
    <!-- START {LOGNAME}.log -->
    <appender name="{LOGNAME.upper()}_FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>{LOG_PREFIX}/{LOGNAME}.log</file>
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <fileNamePattern>$logPrefix/old/{LOGNAME}.%d{GMT_PATTERN}.log</fileNamePattern>
            <maxHistory>7</maxHistory>
        </rollingPolicy>
        <encoder>
            <pattern>%d{GMT_PATTERN} [%t] [%c] %-6p%m%n</pattern>
        </encoder>
    </appender>
    <appender name="{LOGNAME.upper()}_ROLL" class="ch.qos.logback.classic.AsyncAppender">
       <appender-ref ref="{LOGNAME.upper()}_FILE"/>
    </appender>
    <logger name="{LOGGER}" additivity="false" level="{LEVEL.upper()}">
        <appender-ref ref="{LOGNAME.upper()}_FILE"/>
        <appender-ref ref="ERROR_ROLL"/>
    </logger>
    <!-- END {LOGNAME}.log -->
        '''
        print(appender)

if __name__ == "__main__":
  generate_appender()
