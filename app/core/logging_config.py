from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOGGING_CONFIG = {
    "version": 1,
    # 不要禁用已存在的日志记录器
    "disable_existing_loggers": False,
    "formatters": {
        # 标准日志格式器 : 用于控制台和文件日志
        "standard": {
            # 日志格式  时间 | 日志级别 | 日志文件名-函数名-行号 | 日志消息
            "format": "%(asctime)s | %(levelname)s | %(filename)s-%(funcName)s:%(lineno)d | %(message)s"
        },
        # 访问日志格式器 : 用于访问日志文件
        "access": {
            # 日志格式 时间 | 日志级别 | 日志消息
            "format": "%(asctime)s | %(levelname)s | %(message)s"
        },
    },
    "handlers": {
        # 控制台日志处理器 : 打印 DEBUG 及以上级别的日志到终端
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "DEBUG",
        },
        # 应用日志文件处理器 : 打印 INFO 及以上级别的日志到文件
        # 日志文件按天分割，保留 14 天的日志文件
        # 日志文件编码为 utf-8
        # 日志文件路径 : logs/app.log
        "app_log": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": f"{LOG_DIR}/app.log",
            "when": "midnight",
            "backupCount": 14,
            "formatter": "standard",
            "level": "INFO",
            "encoding": "utf-8",
        },
        # 错误日志文件处理器 : 打印 ERROR 及以上级别的日志到文件
        # 日志文件按天分割，保留 30 天的日志文件
        # 日志文件编码为 utf-8
        # 日志文件路径 : logs/error.log
        "error_log": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": f"{LOG_DIR}/error.log",
            "when": "midnight",
            "backupCount": 30,
            "formatter": "standard",
            "level": "ERROR",
            "encoding": "utf-8",
        },
        # 请求日志文件处理器 : 打印 INFO 及以上级别的日志到文件
        # 日志文件按天分割，保留 14 天的日志文件
        # 日志文件编码为 utf-8
        # 日志文件路径 : logs/access.log
        "access_log": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": f"{LOG_DIR}/access.log",
            "when": "midnight",
            "backupCount": 14,
            "formatter": "access",
            "level": "INFO",
            "encoding": "utf-8",
        },
    },
    # 根日志记录器,未指定logger的日志会被记录到这里
    # 这里配置了 app_log 和 console 处理器, 所以所有未指定 logger 的日志都会被记录到文件和终端
    "root": {
        "handlers": ["app_log", "console", "error_log"],
        "level": "INFO",
    },
    "loggers": {
        # uvicorn 访问日志, 交给 access_log 处理器
        "uvicorn.access": {
            "handlers": ["access_log", "console"],
            "level": "INFO",
            "propagate": False,
        },
        # uvicorn 错误日志, 交给 app_log 处理器
        # uvicorn.error 会记录 uvicorn 内部的启动日志
        "uvicorn.error": {
            "handlers": ["console", "error_log"],
            "level": "INFO",
            "propagate": False,
        },
        # 数据库日志, 打印到文件和终端
        "sqlalchemy.engine": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
