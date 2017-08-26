# bin2txtswps
Convert from common neuroscience binary formats (ABF, WCP) to text formats (ATF). This is useful for analysis programs that require text formats. bin2txtswps uses [neo](http://neo.readthedocs.io/en/0.5.1/install.html), [numpy](http://www.numpy.org/), [wx](https://wxpython.org/) and [quantities](https://github.com/python-quantities/python-quantities). It has a windowed (bin2txtswps_win.py) and a command line (bin2txtswps_cmd.py) entry point.

# Before running
Required python modules are listed in requirements.txt (this file was auto-generated with pip)
* Python 2.7 is required
* The program has been tested and is functional on the following operating systems:
  * Windows 7 
  * Windows 10

## Usage
The entry point for this program is bin2txtswps_win.py: run this file to start the program

## To-do
* Extended testing - particularly with multiple channels
* Add more input and output formats
