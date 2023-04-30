@echo off
python setup.py bdist_wheel
rmdir /S /Q build playsoundsimple.py.egg-info