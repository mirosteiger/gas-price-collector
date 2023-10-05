"""
Usage:
    python3 setup.py py2app
"""

from setuptools import setup

APP = ["benzin_tracker.py"]
DATA_FILES = [("images", ["images/icon.svg"])]
OPTIONS = {
    "argv_emulation": True, 
    "packages": ["rumps", "requests", "bs4"]}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
