
# 因为最后上传dict的时候只需要一次性的上传，并且gist里面抽象出来的都是专门针对于github交互的api不涉及其他

# 后续最好是针对输入类型返回特定的输出类型

from typing import Union

from entry import Entry


def add_entry(current_dict:Union[dict,str],entry:Union[str,Entry],tags:list=[])->str:
    """
    提供一个单纯的词或者一个对象，以及可能想一起添加的标签，来一次性添加到字典中
    """
    modified_dict=""
    pass
    return modified_dict

def add_attribute(current_dict:Union[dict,str],entry_id:str,tags:list)->str:
    """
    必须单独指定一个特定的entry才能对着它加
    """
    modified_dict=""
    pass
    return modified_dict