from __future__ import annotations

import inspect
import logging
import os
import sys
import traceback

__logger: type[logging.Logger] = logging.getLoggerClass()


ALL = logging.CRITICAL * 10  # 500 #IO  # Trace.always
STDERR = logging.CRITICAL * 2  # 100
STDOUT = STDERR - 10  # 90
CRITICAL = logging.CRITICAL  # 50
FATAL = logging.FATAL  # 50
ERROR = logging.ERROR  # 40
WARNING = logging.WARNING  # 30
WARN = logging.WARNING  # 30
DIAG = WARN - 5  # 25
INFO = logging.INFO  # 20
NOTICE = INFO - 5  # 15
DEBUG = logging.DEBUG  # 10
VERBOSE = DEBUG - 3  # 7
TRACE = DEBUG - 5  # 5
L4 = 4
L3 = 3
L2 = 2
L1 = 1
NOTSET = logging.NOTSET  # 0


class ScreenpyLogger(__logger):  # type: ignore
    TRACE = TRACE
    ALL = ALL
    STDERR = STDERR
    STDOUT = STDOUT
    CRITICAL = CRITICAL
    FATAL = FATAL
    ERROR = ERROR
    WARNING = WARNING
    WARN = WARN
    DIAG = DIAG
    INFO = INFO
    NOTICE = NOTICE
    DEBUG = DEBUG
    VERBOSE = VERBOSE
    TRACE = TRACE
    L4 = L4
    L3 = L3
    L2 = L2
    L1 = L1
    NOTSET = NOTSET
    timestamp_format = "%Y-%m-%dT%H-%M-%S"

    def __init__(self, name, level=NOTSET):
        super().__init__(name, level)
        self.__add_level_name("TRACE", TRACE)
        self.__add_level_name("NOTICE", NOTICE)
        self.__add_level_name("DIAG", DIAG)
        self.__add_level_name("VERBOSE", VERBOSE)
        self.__add_level_name("L4", L4)
        self.__add_level_name("L3", L3)
        self.__add_level_name("L2", L2)
        self.__add_level_name("L1", L1)

    @staticmethod
    def __add_level_name(name: str, level: int):
        logging.addLevelName(level, name)
        setattr(logging, name, level)

    def __log(self, level: int, msg: str, *args, **kwargs):
        if self.isEnabledFor(level):
            # TODO: might need to look at overriding findCaller
            # this currently doesn't do that because we only need fileline in the format
            # handler. But perhaps the default logging handler could deal with it now.
            info = self._find_first_non_library_stack_frame_info()
            file_line = f"{info[0]}:{info[1]}"
            extra = {"fileline": file_line}
            self._log(level, msg, args, **kwargs, extra=extra)

    def trace(self, msg: str, *args, **kwargs):
        self.__log(TRACE, msg, *args, **kwargs)

    def notice(self, msg: str, *args, **kwargs):
        self.__log(NOTICE, msg, *args, **kwargs)

    def diag(self, msg: str, *args, **kwargs):
        self.__log(DIAG, msg, *args, **kwargs)

    def verbose(self, msg: str, *args, **kwargs):
        self.__log(VERBOSE, msg, *args, **kwargs)

    def debug(self, msg: str, *args, **kwargs):
        self.__log(DEBUG, msg, *args, **kwargs)

    def info(self, msg: str, *args, **kwargs):
        self.__log(INFO, msg, *args, **kwargs)

    def print_stack_trace(self):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        str_list = traceback.format_exception(exc_type, exc_value, exc_traceback)
        self.critical("".join(str_list))

    @staticmethod
    def _find_first_non_library_stack_frame_info(
        hint: int = 0,
    ) -> tuple[str | None, int | None]:
        libs = [
            # 'trace.py',
            # '__init__.py',
            # 'tracelogger.py',
            "contextlib.py",
            "conftest.py",
            # screenpy
            "stdout_adapter.py",
            "pacing.py",
            "narrator.py",
            "actor.py",
            "eventually.py",
            "see.py",
            # hamcrest
            "base_matcher.py",
            "assert_that.py",
        ]
        rt: tuple[str | None, int | None] = (None, None)
        stack = inspect.stack()
        for i in range(hint, len(stack)):
            info = inspect.getframeinfo(stack[i][0])
            filename = info.filename.replace(os.sep, "/").split("/")[-1]
            rt = (filename, info.lineno)
            if filename not in libs:
                break
        return rt


def create_logger(name: str) -> ScreenpyLogger:
    logging.setLoggerClass(ScreenpyLogger)
    # pycharm gets confused about getLogger returning ScreenpyLogger
    # mypy also doesn't understand this since it is a dynamic call.
    # noinspection PyTypeChecker
    logger: ScreenpyLogger = logging.getLogger(name)  # type: ignore
    logging.setLoggerClass(__logger)
    logger.setLevel(DEBUG)
    # logger.propagate = False
    return logger


def enable_logger(
    logger: ScreenpyLogger,
    level: int = ScreenpyLogger.DEBUG,
    fmt: logging.Formatter | None = None,
):
    """DO NOT USE THIS FUNCTION WHEN USING automation.trace."""
    if fmt is None:
        # fmtstr = '{asctime} {filename}:{lineno} {levelname:>8} [{name}] {msg} '
        # fmtstr = '{asctime} {filename}:{lineno:<4} {levelname:>8} {msg} '
        # fmtstr = '{asctime} {levelname:>8} {msg} '
        fmtstr = "{asctime} {msg} "
        fmt = logging.Formatter(fmtstr, datefmt="%H:%M:%S", style="{")

    logger.setLevel(level)
    ch = logging.StreamHandler(sys.__stdout__)
    ch.setLevel(level)
    ch.setFormatter(fmt)
    logger.addHandler(ch)
