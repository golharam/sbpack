from typing import Union
from copy import deepcopy
import urllib.parse
import urllib.request
import pathlib

from ruamel.yaml import YAML
fast_yaml = YAML(typ="safe")


class MissingTypeName(BaseException):
    pass


class MissingCWLType(BaseException):
    pass


class RecordMissingFields(BaseException):
    pass


class ArrayMissingItems(BaseException):
    pass


class MissingKeyField(BaseException):
    pass


built_in_types = ["null", "boolean", "int", "long", "float", "double", "string",  "File", "Directory"]
magic_string = "##sbpack_rename_user_type##"


def normalize_to_map(obj: Union[list, dict], key_field: str):
    if isinstance(obj, dict):
        return deepcopy(obj)
    elif isinstance(obj, list):
        map_obj = {}
        for v in obj:
            if not isinstance(v, dict):
                raise RuntimeError("Expecting a dict here")
            k = v.get(key_field)
            if k is None:
                raise MissingKeyField(key_field)
            v.pop(key_field, None)
            map_obj[k] = v
        return map_obj
    else:
        raise RuntimeError("Expecting a dictionary or a list here")


def normalized_path(link: str, base_url: urllib.parse.ParseResult):
    link_url = urllib.parse.urlparse(link)
    if link_url.scheme in ["file://", ""]:
        new_url = base_url._replace(
            path=str((pathlib.Path(base_url.path) / pathlib.Path(link)).resolve())
        )
    else:
        new_url = link_url

    return new_url


def load_linked_file(base_url: urllib.parse.ParseResult, link: str, is_import=False):

    link_url = urllib.parse.urlparse(link)
    if link_url.scheme in ["file://", ""]:
        new_url = base_url._replace(
            path=str((pathlib.Path(base_url.path) / pathlib.Path(link)).resolve())
        )

    else:
        new_url = link_url

    contents = urllib.request.urlopen(new_url.geturl()).read().decode("utf-8")
    new_base_url = new_url._replace(path=str(pathlib.Path(new_url.path).parent))

    if is_import:
        _node = fast_yaml.load(contents)

    else:
        _node = contents

    return _node, new_base_url, new_url