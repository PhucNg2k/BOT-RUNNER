import importlib.util
import os
from typing import Type
from base_bot import BaseBot
from base_platform import BasePlatform

class Loader:
    @staticmethod
    def load_class_from_file(file_path: str, base_class: Type) -> object:
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type) and issubclass(attr, base_class) and attr is not base_class:
                return attr # return class definition only

        raise ImportError(f"No subclass of {base_class.__name__} found in {file_path}")

    @staticmethod
    def load_bot(file_path: str) -> BaseBot:
        return Loader.load_class_from_file(file_path, BaseBot)

    @staticmethod
    def load_platform(file_path: str) -> BasePlatform:
        return Loader.load_class_from_file(file_path, BasePlatform)
