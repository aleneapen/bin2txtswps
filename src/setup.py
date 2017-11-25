from distutils.core import setup
import py2exe
import wx
import appdirs
 
# includes = []

# setup(
    # options = {"py2exe": {"compressed": 1, 
                          # "optimize": 1,
                          # "includes": includes,
                          # "bundle_files": 1,
                          # "dist_dir" "dist",
                          # "xref": False,
                          # "skip_archive": False,
                          # "ascii": False,
                          # "custom_boot_script": '',
                         # }
              # },
    # zipfile = None,
    # console = [
		# {
		# "script": "abf2txt_browser_v2.py",
		# }
	# ],
# )

py2exe_options = dict(
                      ascii=False,
                      includes=['appdirs','packaging'],
                      packages=['packaging'],
                      excludes=['matplotlib','_ssl','doctest','pdb','pydoc','pyreadline', 'doctest', 'encoding'
                                'optparse','_gtkagg', '_tkagg', 'bsddb', 'curses', 'pywin.debugger',	'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl','Tkconstants','setuptools','pip','_hashlib'],  # Exclude standard library
                      dll_excludes=['libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll', 'tcl84.dll','tk84.dll','numpy-atlas.dll'],  # Exclude msvcr71
					  compressed=1,
					  optimize=2,
					  bundle_files=1,
					 )

setup(name='<Name>',
      version='1.0',
      author='Alen Eapen',
      console=[{"script":'src\\bin2txtswps_win.py'}],
      options={'py2exe': py2exe_options},
	  zipfile=None,
	  
      )