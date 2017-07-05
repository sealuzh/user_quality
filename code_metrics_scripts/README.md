# Android Quality Metrics Extractor

In order to run the script the user needs to install Python and the PyCharm Community Edition environment.

## Environment Configuration
Select from the File menu the Create Project option, in the Location field select the folder containing the sources extracted and in the Interpreter field select the folder related to your Python environment.

## Script Configuration
In order to run the script, the config.ini file in the src folder needs to be edited, in particular:

* base = folder containing the scripts
* input = folder containing the apks
* output = folder containing the dissassembled apks

In the package it is provided an example of the results in the output.txt file related to the apk placed in the \toDisass\apks folder.
Place the apktool.jar file in the \src folder.

### SOFTWARE REQUIREMENTS

#### Requirements:
* Androguard (APK Python module)
* Apkil (SMALI Python module)
* Apktool (A tool for reverse engineering Android apk files)
* Java (baksmali.jar executable)

#### Download:

* http://www.python.org/download/releases/2.7/
* https://www.jetbrains.com/pycharm/download/

Tested with Python 2.7.6 using Linux Mint 17.3 and Microsoft Windows 7 64 bit.

The software is released by authors under Open Source license.




