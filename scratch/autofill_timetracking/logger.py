from __future__ import annotations

import contextlib
import io
import logging
import os
import sys
import traceback
from pathlib import Path
from types import FrameType
from typing import TYPE_CHECKING, Any, cast

import hamcrest
import hamcrest.core.base_matcher
import screenpy.actions
import screenpy.narration.narrator
import screenpy.narration.stdout_adapter
import screenpy.resolutions
import screenpy_selenium.actions.chain

import scratch.autofill_timetracking.actions

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping, Sequence
    from types import FunctionType, TracebackType

    type T_exc = (
        tuple[type[BaseException], BaseException, TracebackType | None]
        | tuple[None, None, None]
        | None
    )

__logger: type[logging.Logger] = logging.getLoggerClass()
_logRecordFactory = logging.getLogRecordFactory()


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


if hasattr(sys, "_getframe"):

    def currentframe() -> FrameType:
        return sys._getframe(3)

else:  # pragma: no cover

    def currentframe() -> FrameType:
        """Return the frame object for the caller's stack frame."""
        try:
            raise Exception  # noqa:TRY301,TRY002
        except Exception:  # noqa: BLE001
            rt = sys.exc_info()
            return rt[2].tb_frame.f_back  # type: ignore[union-attr,return-value]


def mod_path(function: FunctionType | Callable) -> Path:
    return Path(function.__code__.co_filename)


# when adding functions to this list, you must avoid those which have decorators.
ignore_srcfiles: list[Path] = [
    mod_path(mod_path),
    mod_path(contextlib.contextmanager),
    mod_path(screenpy.narration.stdout_adapter.StdOutAdapter.aside),
    mod_path(screenpy.pacing.act),
    mod_path(screenpy.narration.narrator._chainify),
    mod_path(screenpy.actor.Actor.named),
    mod_path(screenpy.actions.eventually.Eventually.describe),
    mod_path(screenpy.actions.see.See.describe),
    mod_path(screenpy.actions.either.Either.describe),
    mod_path(screenpy.actions.silently.Silently),
    mod_path(screenpy.actions.see_all_of.SeeAllOf.describe),
    mod_path(screenpy.actions.see_any_of.SeeAnyOf.describe),
    mod_path(scratch.autofill_timetracking.actions.see.See.describe),
    mod_path(scratch.autofill_timetracking.actions.see_all_of.SeeAllOf.describe),
    mod_path(scratch.autofill_timetracking.actions.see_any_of.SeeAnyOf.describe),
    mod_path(hamcrest.core.base_matcher.BaseMatcher.matches),
    mod_path(hamcrest.assert_that),
    mod_path(hamcrest.core.core.isnot.is_not),
    mod_path(screenpy_selenium.actions.chain.Chain.describe),
]

# ignore_srcfiles is used when walking the stack to check when we've got the first
# caller stack frame, by skipping frames whose filename is listed.
#
# Ordinarily we would use __file__ for this, but frozen modules don't always
# have __file__ set, for some reason (see Issue #21736). Thus, we get the
# filename from a handy code object from a function defined each module.

# _srcfile is only used in conjunction with sys._getframe().
# To provide compatibility with older versions of Python, set _srcfile
# to None if _getframe() is not available; this value will prevent
# findCaller() from being called. You can also do this if you want to avoid
# the overhead of fetching caller information, even when _getframe() is
# available.
# if not hasattr(sys, '_getframe'):
#    _srcfile = None


def find_file_dir(file: str, parents: Sequence[Path] | None = None) -> Path:
    parents = parents or Path(__file__).parent.parents
    for p in parents:
        for pl in p.glob(file):
            return pl.parent
    # return next(pl for p in parents for pl in p.glob(file)).parent
    raise Warning(f"cannot find folder containing {file}")


def project_name_root(project_name: str, parents: Sequence[Path] | None = None) -> Path:
    parents = parents or Path(__file__).parent.parents
    for p in parents:
        if p.name == project_name:
            return p
    # return next(p for p in parents if p.name == project_name)
    raise Warning("cannot find project root")


def find_root(project_name: str | None = None) -> Path:
    parents = Path(__file__).parent.parents
    if project_name:
        return project_name_root(project_name, parents)
    # assume root based on finding these files :
    root_files = ["pyproject.toml", "setup.py"]
    for file in root_files:
        if rt := find_file_dir(file, parents):
            return rt

    raise Warning("cannot find project root")


PROJECT_ROOT = find_root()


class ScreenpyLogger(__logger):  # type: ignore[valid-type,misc]
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
    L4 = L4
    L3 = L3
    L2 = L2
    L1 = L1
    NOTSET = NOTSET
    timestamp_format = "%Y-%m-%dT%H-%M-%S"
    pycharm_filelink = False

    def __init__(self, name: str, level: int = NOTSET) -> None:
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
    def __add_level_name(name: str, level: int) -> None:
        logging.addLevelName(level, name)
        setattr(logging, name, level)

    def __log(self, level: int, msg: object, *args: Any, **kwargs: Any) -> None:
        """
        using f"{fn.relative_to(PROJECT_ROOT)}:{lno}"

        tests/fixtures/users.py:43
        tests/journeys/login.py:50
        tests/task/goto_login_page.py:20
        tests/task/scheduling/goto_schedule.py:29
        tests/task/scheduling/goto_find_schedule.py:19

        using f"{fn.relative_to(Path.cwd(), walk_up=True)}:{lno}"

        ../fixtures/users.py:43
        ../journeys/login.py:50
        ../task/goto_login_page.py:20
        ../task/scheduling/goto_schedule.py:29
        ../task/scheduling/goto_find_schedule.py:19


        """
        if not self.isEnabledFor(level):
            return

        fn, lno, func, sinfo = self.findCaller()

        file_line = f"{fn.name}:{lno}"
        if self.pycharm_filelink:
            with contextlib.suppress(ValueError):
                file_line = f"{fn.relative_to(PROJECT_ROOT)}:{lno}"
                with contextlib.suppress(ValueError):
                    file_line = f"{fn.relative_to(Path.cwd(), walk_up=True)}:{lno}"

        extra = {"fileline": file_line} | kwargs.pop("extra", {})
        self._log(level, msg, args, **kwargs, extra=extra)

    def makeRecord(
        self,
        name: str,
        level: int,
        fn: str,
        lno: int,
        msg: object,
        args: tuple[object, ...] | Mapping[str, object] | None,
        exc_info: T_exc,
        func: str | None = None,
        extra: dict | None = None,
        sinfo: str | None = None,
    ) -> logging.LogRecord:
        """
        bypassing restrictions to override created timestamp
        """
        rv = _logRecordFactory(name, level, fn, lno, msg, args, exc_info, func, sinfo)
        if extra is not None:
            for key in extra:
                rv.__dict__[key] = extra[key]
        return rv

    def log(self, level: int, msg: object, *args: Any, **kwargs: Any) -> None:
        self.__log(level, msg, *args, **kwargs)

    def trace(self, msg: object, *args: Any, **kwargs: Any) -> None:
        self.__log(TRACE, msg, *args, **kwargs)

    def notice(self, msg: object, *args: Any, **kwargs: Any) -> None:
        self.__log(NOTICE, msg, *args, **kwargs)

    def diag(self, msg: object, *args: Any, **kwargs: Any) -> None:
        self.__log(DIAG, msg, *args, **kwargs)

    def verbose(self, msg: object, *args: Any, **kwargs: Any) -> None:
        self.__log(VERBOSE, msg, *args, **kwargs)

    def debug(self, msg: object, *args: Any, **kwargs: Any) -> None:
        self.__log(DEBUG, msg, *args, **kwargs)

    def info(self, msg: object, *args: Any, **kwargs: Any) -> None:
        self.__log(INFO, msg, *args, **kwargs)

    def print_stack_trace(self) -> None:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        str_list = traceback.format_exception(exc_type, exc_value, exc_traceback)
        self.critical("".join(str_list))

    def findCaller(
        self, stack_info: bool = False, stacklevel: int = 1
    ) -> tuple[Path, int, str, str | None]:
        """
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        """
        f = currentframe()
        # On some versions of IronPython, currentframe() returns None if
        # IronPython isn't run with -X:Frames.
        if f is not None:
            f = cast(FrameType, f.f_back)

        orig_f: FrameType = f
        while f and stacklevel > 1:
            f = f.f_back  # type: ignore[assignment]
            stacklevel -= 1
        if not f:
            f = orig_f
        rv: tuple[Path, int, str, str | None]
        rv = Path(os.path.devnull), 0, "(unknown function)", None
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = Path(co.co_filename)
            if filename in ignore_srcfiles:
                f = cast(FrameType, f.f_back)
                continue
            sinfo = None
            if stack_info:
                sio = io.StringIO()
                sio.write("Stack (most recent call last):\n")
                traceback.print_stack(f, file=sio)
                sinfo = sio.getvalue()
                if sinfo[-1] == "\n":
                    sinfo = sinfo[:-1]
                sio.close()
            rv = (Path(co.co_filename), f.f_lineno, co.co_name, sinfo)
            break
        return rv


def create_logger(name: str, enable_filepath: bool = False) -> ScreenpyLogger:
    logging.setLoggerClass(ScreenpyLogger)
    # pycharm gets confused about getLogger returning ScreenpyLogger
    # mypy also doesn't understand this since it is a dynamic call.
    # noinspection PyTypeChecker
    logger: ScreenpyLogger = logging.getLogger(name)  # type: ignore[assignment]
    logger.pycharm_filelink = enable_filepath
    logging.setLoggerClass(__logger)
    logger.setLevel(DEBUG)
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
