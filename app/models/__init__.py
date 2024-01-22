#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# 导入所有模型，并将 Base 放在最前面， 以便 Base 拥有它们
# imported by Alembic
"""
from .base import MappedBase
from .sys_api import Api
from .sys_casbin_rule import CasbinRule
from .sys_dept import Dept
from .sys_dict_data import DictData
from .sys_dict_type import DictType
from .sys_login_log import LoginLog
from .sys_menu import Menu
from .sys_opera_log import OperaLog
from .sys_role import Role
from .sys_user import User
from .fuzz_test_case import FuzzTestCase
from .fuzz_test_field import FuzzTestField
from .fuzz_test_suite import FuzzTestSuite