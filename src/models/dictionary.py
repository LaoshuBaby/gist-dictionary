# 文件说明: 字典数据模型 / File Description: Pydantic models for dictionary entries and wordbank
from pydantic import BaseModel
from typing import List, Optional


class EntryBase(BaseModel):
    word: str
    tags: Optional[List[str]] = []


class EntryCreate(EntryBase):
    pass


class Entry(EntryBase):
    id: str


class Dictionary(BaseModel):
    wordbank: List[Entry]


class TagUpdate(BaseModel):
    tags: List[str]
