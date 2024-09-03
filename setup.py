import sys
import os
from cx_Freeze import setup, Executable

files = ['icon.ico']
target = Executable(
    script= 'app.py',
    base= 'Win32GUI',
    icon= 'icon.ico'
)
setup(
    name= 'Crimson Simple Image Converter',
    version= '1.0.0',
    description= 'Image converter and PDF Image Extractor',
    author= 'Alex S. Alves Rocha Filho',
    options= {'build_exe': {'include_files': files}},
    executables= [target]
)