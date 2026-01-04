# app/models.py
from logging import getLogger

from app import rbac_core
rbac_core.__all__

logger = getLogger(__name__)
logger.info("确保所有模型在此处加载")

