#!/bin/bash

if ! command -v pyinstaller &> /dev/null
then
    echo "PyInstaller not installed. Please install it before running this script."
    exit 1
fi

if [ $1 = "main" ]
then
    pyinstaller --noconsole --onefile --add-data "assets;assets" $1.py

fi
if [ $1 = "updater" ]
then
    pyinstaller --noconsole --onefile $1.py
fi
