# bin2txtswps
Convert from common neuroscience binary formats (ABF, WCP) to text formats (ATF). This is useful for analysis programs that require text formats. bin2txtswps uses [neo](http://neo.readthedocs.io/en/0.5.1/install.html), [numpy](http://www.numpy.org/), [wx](https://wxpython.org/) and [quantities](https://github.com/python-quantities/python-quantities). It has a windowed (bin2txtswps_win.py) and a command line (bin2txtswps_cmd.py) entry point.

# Before running
Required python modules are listed in requirements.txt (this file was auto-generated with pip)
* Tested with python 2.7 and python 3.6
* The program has been tested and is functional on the following operating systems:
  * Windows 7 
  * Windows 10
  * Ubuntu 16.04

## Usage
The entry point for this program is bin2txtswps_win.py: run this file to start the program

## To-do
* Extended testing - particularly with multiple channels
* Add more input and output formats

## Changelogs

### 24/Sept/2017
* Changed code to work with Python 3.6.2
* Changed write_ATF function in ATF_functions to use numpy.stack instead of vstack
* Changed build_full_header in ATF_functions to improve code readability

### 25/Nov/2017
* Bug in neo 0.5.1 (reading WinWCP data) addressed by updating neo to 0.5.2 in requirements.txt
* Numpy requirement downgraded to 1.11.1 due to a bug in compatibility with py2exe
* Added additional headers in ATF_functions.py
* Updated bin2txtswps_win.py for python3
* Updated setup.py for py2exe
* Using read_header() function of axonIO to get additional information for headers