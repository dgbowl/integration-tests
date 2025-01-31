import importlib
import subprocess

def test_import_yadg():
    assert importlib.import_module("yadg")

def test_import_dgpost():
    assert importlib.import_module("dgpost")

def test_versions():
    assert subprocess.run(["yadg", "--version"], check=True)
    assert subprocess.run(["dgpost", "--version"], check=True)