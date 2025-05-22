from dataclasses import dataclass, field
from typing import List, Dict, Optional, Union


@dataclass
class DescriptionTable:
    non_table_before: Optional[str] = field(default_factory=str)
    non_table_after: Optional[str] = field(default_factory=str)
    headers: Optional[str] = field(default_factory=str)
    description_table_processed: Optional[Dict[str, any]] = field(default_factory=dict)
    # table_headers: Optional[Dict[str, str]] = field(default_factory=dict)
    data_rows: Optional[List[List[str]]] = field(default_factory=list)

    def dictification(self):
        return {**self.__dict__}


@dataclass
class UrlInfo:
    raw: str
    url_hash: Optional[str] = None
    protocol: Optional[str] = None
    host: Optional[List[str]] = field(default_factory=list)
    port: Optional[List[str]] = field(default_factory=list)
    path: Optional[List[str]] = field(default_factory=list)
    query: Optional[Dict[str, str]] = field(default_factory=dict)
    variable: Optional[Dict[str, str]] = field(default_factory=dict)
    description: Optional[str] = field(default_factory=str)
    description_table: DescriptionTable = field(default_factory=DescriptionTable)
    query_dict: Optional[Dict[str, any]] = field(default_factory=dict)

    def dictification(self):
        return {**self.__dict__} | {'description_table': self.description_table.dictification()}

# @dataclass
# class Header:
#     key: str
#     value: str
#     description: Optional[str] = None
#
# @dataclass
# class Body:
#     mode: str
#     raw: Optional[str] = None
#     json: Optional[Dict[str, Union[str, int, float, bool, None]]] = None
#     formdata: Optional[List[Dict[str, str]]] = None
#     urlencoded: Optional[List[Dict[str, str]]] = None

@dataclass
class WebRequest:
    name: str
    method: str
    url: UrlInfo
    # headers: List[Header] = field(default_factory=list)
    # body: Optional[Body] = None
    description: Optional[str] = None

    def dictification(self):
        result = {**self.__dict__}
        result.update({'url': self.url.dictification()})
        return result

@dataclass
class EndPoint:
    name: str
    path: str
    methods: Dict[str, WebRequest] = field(default_factory=dict)
    children: List['EndPoint'] = field(default_factory=list)

    def dictification(self):
        result = {'class_name': self.name,
                  'methods': {k: v.dictification() if hasattr(v, 'dictification') else v for k,v in self.methods.items()},
                  'children': [child.dictification() for child in self.children],
                  'parent_field_name': f'{self.name.split("_")[-1]}',
                  }
        return result