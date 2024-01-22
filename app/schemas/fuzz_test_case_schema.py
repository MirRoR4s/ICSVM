"""模糊测试用例请求体原型"""
from .base import SchemaBase

class CaseSchema(SchemaBase):
    """TODO"""
    name: str
    suite_name: str

class CreateCaseSchema(CaseSchema):
    """TODO"""
    desc: str
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "test_case",
                    "suite_name": "test_suite",
                    "desc": "test_case_desc"
                }
            ]
        
    }
    }

class ReadCaseResponseSchema(CaseSchema):
    """
    - suite_name
    - name
    - desc
    - fields
    """
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "test_case",
                    "suite_name": "test_suite",
                    "desc": "test_case_desc",
                    "fields": 
                        [
                            "test_field1",
                            "test_field2"
                        ]
                        
                    
                }
            ]
        }
    }

class UpdateCaseSchema(CaseSchema):
    """
    - suite_name
    - name
    - new_name
    - new_desc
    """
    new_name: str
    new_desc: str
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "suite_name": "test_suite",
                    "name": "test_case",
                    "new_name": "new_name",
                    "new_desc": "new_desc"
                        
                    
                }
            ]
        }
    }

class DeleteCaseSchema(CaseSchema):
    """
    - suite_name
    - name
    """
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "suite_name": "test_suite",
                    "name": "test_case"
                }
            ]
        }
    }