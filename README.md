# Coursera Dump

This project export in Excel Coursera courses.

# How to Install

Python 3 should be already installed. Then use pip (or pip3 if there is a conflict with old Python 2 setup) to install dependencies:

```bash
$ pip install -r requirements.txt # alternatively try pip3
```

Remember, it is recommended to use [virtualenv/venv](https://devman.org/encyclopedia/pip/pip_virtualenv/) for better isolation.

# How to launch

Example of script launch on Linux, Python 3.5:

```#!bash
python coursera.py
```

# Usage

usage: coursera.py [-h] [-c COUNT] [-o OUTPUT]

export Cousera courses to excel

optional arguments:

  -h, --help            show this help message and exit

  -c COUNT, --count COUNT
                        count courses to export in excel

  -o OUTPUT, --output OUTPUT
                        output filename


# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
