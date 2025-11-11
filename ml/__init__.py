"""
Core machine-learning utilities shared by the LieDetect backend.
"""

from importlib import import_module

__all__ = ["common"]

common = import_module("ml.common")



