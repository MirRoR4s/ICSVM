"""全局日志类"""
import os
from loguru import logger
from app.core.path_conf import BASE_LOG_PATH
from app.core.conf import settings

if not os.path.exists(BASE_LOG_PATH):
    os.mkdir(BASE_LOG_PATH)

log_stdout_file = os.path.join(BASE_LOG_PATH, settings.LOG_STDOUT_FILENAME)
log_stderr_file = os.path.join(BASE_LOG_PATH, settings.LOG_STDERR_FILENAME)
log_config = {
    "rotation": "10 MB",
    "retention": "15 days",
    "compression": "tar.gz",
    "enqueue": True,
}
logger.add(
    log_stdout_file,
    level='INFO',
    filter=lambda record: record['level'].name == 'INFO' or record['level'].no <= 25,
    **log_config,
    backtrace=False,
    diagnose=False,
)

logger.add(
    log_stderr_file,
    level='ERROR',
    filter=lambda record: record['level'].name == 'ERROR' or record['level'].no >= 30,
    **log_config,
    backtrace=True,
    diagnose=True,
)