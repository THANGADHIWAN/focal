"""
Configuration module for the LIMS application.
"""
from .settings import Settings
from .logging import setup_logging

__all__ = ['Settings', 'setup_logging']
