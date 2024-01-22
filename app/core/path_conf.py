"""路径配置文件"""
import os
from pathlib import Path
from app.core.conf import settings

# 项目根文件夹路径（app）
ROOTPATH = Path(__file__).resolve().parent.parent.parent
# alembic 迁移文件夹路径
ALEMBICPATH = os.path.join(ROOTPATH, 'alembic', 'versions')
# 日志文件夹路径
BASE_LOG_PATH = os.path.join(ROOTPATH, 'log')
# RBAC model.conf 文件路径
RBAC_MODEL_CONF = os.path.join(ROOTPATH, 'core', settings.CASBIN_RBAC_MODEL_NAME)
# 离线 IP 数据库路径
IP2REGION_XDB = os.path.join(ROOTPATH, 'static', 'ip2region.xdb')