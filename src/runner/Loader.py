import importlib.util
import os
from typing import Type
from ..bots.BaseBot import BaseBot
from ..client_platform.BasePlatform import BasePlatform

class Loader:
    @staticmethod
    def load_class_from_module(module_name: str, base_class: type):
        """
        Dynamically load a class that is a subclass of base_class from a module name.
        """
        module = importlib.import_module(module_name)
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type) and issubclass(attr, base_class) and attr is not base_class:
                return attr
        raise ImportError(f"No subclass of {base_class.__name__} found in {module_name}")

    @staticmethod
    def load_bot(module_name: str):
        """
        Load a bot class from a module name.
        """
        return Loader.load_class_from_module(module_name, BaseBot)

    @staticmethod
    def load_platform(file_path: str) -> BasePlatform:
        return Loader.load_class_from_file(file_path, BasePlatform)
