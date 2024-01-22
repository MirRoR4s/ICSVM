"""模糊测试字段请求体原型"""
from .base import SchemaBase

class FieldSchema(SchemaBase):
    """TODO"""
    suite_name: str
    case_name: str
    name: str

class CreateFieldSchema(FieldSchema):
    """TODO"""
    type: str
    attribute: dict | None
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "suite_name": "test",
                    "case_name": "test",
                    "name": "test", 
                    "type": "static",
                    "attribute": {"default_value": 0}
                }
            ]
        }
    }

class ReadFieldResponseSchema(CreateFieldSchema):
    """TODO"""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "suite_name": "test",
                    "case_name": "test",
                    "name": "test", 
                    "type": "static",
                    "attribute": {"default_value": 0}
                }
            ]
        }
    }

class UpdateFieldSchema(FieldSchema):
    """
    - suite_name
    - case_name
    - name
    - new_name
    - new_type
    - new_attribute
    """
    new_name: str
    new_type: str
    new_attribute: dict
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "suite_name": "test_suite",
                    "case_name": "test_case",
                    "name": "test_field", 
                    "new_name": "test",
                    "new_type": "simple",
                    "new_attribute": {"default_value": 0}
                }
            ]
        }
    }

class DeleteFieldSchema(FieldSchema):
    """
    - suite_name
    - case_name
    - name
    
    """
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "suite_name": "test_suite",
                    "case_name": "test_case",
                    "name": "test_field", 
                }
            ]
        }
    }

# class Fuzzable(FieldBaseSchema):
#     """
#     所有 primitives 和 blocks 的父类。
#     """
#     name: str
#     default_value: int | str | bytes | None = 0
#     fuzzable: bool = False
#     fuzz_values: list | None = None

# class FuzzableBlock(Fuzzable):
#     """TODO"""
#     request_name: str | None = None
#     children: Fuzzable | None | list[Fuzzable] = None

# class Static(Fuzzable):
#     """TODO"""
#     default_value: int = 0
#     model_config = {
#         "json_schema_extra": {
#             "examples": [
#                 {   
#                     "suite_name": "test",
#                     "case_name": "test",
#                     "name": "test",
#                     "default_value": 0
#                 }
#             ]
#         }
#     }

# class Simple(FieldBaseSchema):
#     """TODO"""
#     fuzzable: bool = True

# class Delim(FieldBaseSchema):
#     """TODO"""
#     name: str
#     default_value: str
#     fuzzable: bool

# class Group(FieldBaseSchema):
#     name: str
#     values: list[bytes] | list[str]
#     default_value: str
#     encoding: str = 'ascii'
#     fuzzable: bool = True

# class RandomData(FieldBaseSchema):
#     name: str
#     default_value: str | bytes | None = None
#     min_length: int = 0
#     max_length: int = 1
#     max_mutations: int
#     step: int | None = None
#     fuzzable: bool = True

# class String(FieldBaseSchema):
#     name: str
#     default_value: str
#     size: int | None = None
#     padding: bytes = b'\x00'
#     encoding: str = 'ascii'
#     max_len: int | None = None
#     fuzzable: bool = True

# class FromFile(FieldBaseSchema):
#     name: str
#     default_value: bytes
#     filename: str
#     max_len: int = 0
#     fuzzable: bool = True

# class Mirror(FieldBaseSchema):
#     name: str
#     primitive_name: str
#     request_name: str
#     fuzzable: bool = True

# class BitField(FieldBaseSchema):
#     name: str
#     default_value: int
#     width: int = 8
#     max_num: int | None = None
#     endian: str = '>'
#     output_format: str = "binary"
#     signed: bool = False
#     full_range: bool = False
#     fuzz_values: list | None = None
#     fuzzable: bool = True

# class Byte(FieldBaseSchema):
#     name: str
#     default_value: int
#     max_num: int
#     endian: str
#     output_format: str
#     signed: bool
#     full_range: bool
#     full_values: list[int]
#     fuzzable: bool
    
# class Bytes(FieldBaseSchema):
#     name: str
#     default_value: bytes = b''
#     size: int | None = None
#     padding: bytes = b"\x00"
#     max_len: int | None = None
#     fuzz_values: list = None

# class Word(FieldBaseSchema):
#     name: str
#     default_value: int = 0
#     max_num: int | None = None
#     endian: str = LITTLE_ENDIAN
#     output_format: str = 'binary'
#     signed: bool = False
#     full_range: bool = False
#     fuzz_values: list | None = None
#     fuzzable: bool = True
    
# class DWord(Word):
#     pass

# class QWord(Word):
#     pass

# class Block(SchemaBase):
#     """
#     fot the detailed information, see this: http://boofuzz.readthedocs.io/
#     """
#     name: str
#     default_value: int | None = None
#     children_name: str | None = None
#     group: str | None = None
#     encoder: str | None = None
#     dep: str | None = None
#     dep_value: bytes | None = None
#     dep_values: list[bytes] | None = None
#     dep_compare: str | None = None

# class FieldSchema(SchemaBase):
#     """TODO"""
#     name: str
#     attribute: dict | None = None