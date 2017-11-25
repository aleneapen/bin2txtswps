# This program converts various neuroscience files to ASCII text files.
__author__ = "Alen Eapen"

# import stfio

from os import path
import file_loop
import wx

print("Select the format that you want to convert from")
print("Choose the folder where the files are located")
print(".atf files will be written to bin2txtswps sub-folder \n")

print("Disclaimer: ")
print("This program uses Neo: http://pythonhosted.org/neo/,")
print("NumPy: http://www.numpy.org/,")
print("Quantities: https://pythonhosted.org/quantities/,")
print("wxPython: http://www.wxpython.org/,")
print("Python: https://www.python.org/ \n")


# Supported format list
bin_format_l = ["abf","wcp"]
out_format_l = ["atf","txt"]
dialogApp = wx.App()



dlg = wx.SingleChoiceDialog(None, "Choose one of the following input formats:",\
    "Input File format: ", bin_format_l, wx.CHOICEDLG_STYLE)

if dlg.ShowModal() == wx.ID_OK:
    bin_format = dlg.GetStringSelection()
else:
    print("Format selection cancelled")
    raw_input()
    exit()

dlg.Destroy()
	

dlg = wx.DirDialog(None, "Folder Selection",style=wx.DD_DIR_MUST_EXIST)

if dlg.ShowModal() == wx.ID_OK:
	folderName = dlg.GetPath()
else:
    print("Folder selection cancelled")
    raw_input()
    exit()
dlg.Destroy()

file_loop.folder_converter(folderName,bin_format)


    

