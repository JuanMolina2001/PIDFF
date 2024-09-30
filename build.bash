#!/bin/bash

if ! command -v pyinstaller &> /dev/null
then
    echo "PyInstaller not installed. Please install it before running this script."
    exit 1
fi

pyinstaller --onefile --add-data "assets;assets" main.py
