from abc import ABC, abstractmethod
from collections.abc import Collection
import json
from typing import Any, Generic, Optional, TypeVar
import typing
import xor_encrypt
from decimal import Decimal

SAVE_FILENAME = "save.json"

ENCRYPT_KEY = "2023.12.15 Don't touch blocks. You can't cheat!"

TProperty = TypeVar("TProperty")
TPropertyAllowSet = TypeVar("TPropertyAllowSet")

class PropertyInfo(ABC, Generic[TProperty, TPropertyAllowSet]):

    @abstractmethod
    def get_name(self) -> str:
        pass
    
    @abstractmethod
    def on_load(self, src: dict[str, Any], dst: dict[str, Any]):
        pass

    @abstractmethod
    def on_save(self, src: dict[str, Any], dst: dict[str, Any]):
        pass

    @abstractmethod
    def get(self, save: dict[str, Any]) -> TProperty:
        pass

    @abstractmethod
    def set(self, save: dict[str, Any], val: TPropertyAllowSet) -> bool:
        pass

class SimplePropertyInfo(
    PropertyInfo[TProperty, TProperty], Generic[TProperty]):
    
    __name: str
    __data_type: type[TProperty]
    __default_value: TProperty

    def __init__(self, name: str, data_type: type[TProperty], default_value: TProperty):
        self.__name = name
        self.__data_type = data_type
        self.__default_value = default_value

    def get_name(self) -> str:
        return self.__name
    
    @property
    def data_type(self) -> type[TProperty]:
        return self.__data_type
    
    @property
    def default_value(self) -> TProperty:
        return self.__default_value
    
    def on_load_value(self, src: dict[str, Any], val: Any) -> Any:
        return val

    def on_load(self, src: dict[str, Any], dst: dict[str, Any]):
        name = self.__name
        found = False
        if name in src:
            val = self.on_load_value(src, src[name])
            if isinstance(val, self.__data_type):
                dst[name] = val
                found = True
        if not found:
            dst[name] = self.__default_value

    def on_save(self, src: dict[str, Any], dst: dict[str, Any]):
        name = self.__name
        dst[name] = src[name]

    def get(self, save: dict[str, Any]) -> TProperty:
        return save[self.__name]

    def set(self, save: dict[str, Any], val: TProperty) -> bool:
        if not isinstance(val, self.__data_type):
            return False
        name = self.__name
        old_val = save[name]
        if val == old_val:
            return False
        save[name] = val
        return True

_property_dict: dict[str, PropertyInfo] = {}

_save: dict[str, Any] = {}

def define(prop: PropertyInfo):
    global _property_dict
    _property_dict[prop.get_name()] = prop

def define_simple(name: str, data_type: type[TProperty], default_value: TProperty):
    define(SimplePropertyInfo(name, data_type, default_value))

def get_property(name: str) -> PropertyInfo:
    global _property_dict
    return _property_dict[name]

def get_all_properties() -> Collection[PropertyInfo]:
    global _property_dict
    return _property_dict.values()

def load():
    global _save

    json_obj = None
    with open(SAVE_FILENAME, "r", encoding = "utf-8") as file:
        try:
            json_obj = json.load(file)
            if not isinstance(json_obj, dict):
                json_obj = None
        except:
            pass
    if json_obj == None:
        json_obj = {}
    for prop in get_all_properties():
        prop.on_load(json_obj, _save)
    save()

def save():
    global _save

    json_obj = {}
    for prop in get_all_properties():
        prop.on_save(_save, json_obj)
    with open(SAVE_FILENAME, "w", encoding = "utf-8") as file:
        json.dump(json_obj, file)

def get(name: str, as_type: type[TProperty]) -> TProperty:
    global _save

    val = get_property(name).get(_save)
    if not isinstance(val, as_type):
        raise TypeError(f"Invalid type {as_type} for property {name} in gamesave.")
    return typing.cast(TProperty, val)

def set(name: str, val: Any):
    global _save

    need_save = get_property(name).set(_save, val)
    if need_save:
        save()

class EncryptedPropertyInfo(SimplePropertyInfo[TProperty], Generic[TProperty]):
    
    def on_load_value(self, src: dict[str, Any], val: Any) -> Any:
        if not isinstance(val, str):
            return None
        name = self.get_name()
        md5_name = name + "_md5"
        if md5_name not in src:
            return None
        md5_val = src[md5_name]
        if not isinstance(md5_val, str):
            return None
        result = xor_encrypt.decrypt(val, ENCRYPT_KEY, md5_val)
        if result != None:
            result = self.convert_str_to_value(result)
        return result
    
    def on_save(self, src: dict[str, Any], dst: dict[str, Any]):
        name = self.get_name()
        val = src[name]
        str_val = self.convert_value_to_str(val)
        str_val, md5_val = xor_encrypt.encrypt(str_val, ENCRYPT_KEY)
        md5_name = name + "_md5"
        dst[name] = str_val
        dst[md5_name] = md5_val
        
    def convert_str_to_value(self, str_val: str) -> Optional[TProperty]:
        return self.data_type(str_val)

    def convert_value_to_str(self, val: TProperty) -> str:
        return str(val)

define_simple("is_fullscreen", bool, False)
define_simple("is_mute", bool, False)
define(EncryptedPropertyInfo("best_score", Decimal, Decimal(0)))