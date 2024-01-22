"""模糊测试套件请求体原型"""
from .base import SchemaBase


class SuiteSchema(SchemaBase):
    """
    - name
    """
    name: str = "test_suite"

class ReadSuiteSchema(SuiteSchema):
    """
    - name
    - desc
    - cases_name
    """
    cases_name: list[str] | None = None
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "test",
                    "desc": "test",
                    "cases_name": ["test_case_1", "test_case_2"]
                }
            ]
        }
    }

class CreateSuiteSchema(SuiteSchema):
    """
    - name
    - desc
    """
    desc: str = "description"
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "test_suite",
                    "desc": "test_suite_desc",
                }
            ]
        }
    }

class UpdateSuiteSchema(SuiteSchema):
    """TODO"""
    new_name: str
    new_desc: str
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "旧名称",
                    "new_name": "新名称", 
                    "new_desc": "新描述",
                }
            ]
        }
    }

class SuiteTemplateSchema(SuiteSchema):
    """
    - name
    - desc
    - cases_name
    """
    cases_name: list[str]

class DeleteSuiteSchema(SuiteSchema):
    pass