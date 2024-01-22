

def sqlalchemy_list2dict(sqlalchemy_list: list) -> dict:
    """
    将SQLAlchemy查询结果集转换为字典形式

    :param sqlalchemy_list: sqlalchemy查询结果集,要求每个对象都有name属性,并且name属性的值是以空格分隔的字符串
    :return: 
    """
    result_dict = {}
    for obj in sqlalchemy_list:
        result_dict['name'] = obj.name
        result_dict['desc'] = obj.description 
    return result_dict
