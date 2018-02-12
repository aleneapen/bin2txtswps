from wx.html import HtmlWindow as wxHTMLWindow
import wx
import sys
import os
import file_loop
from threading import Thread
import time
import webbrowser
from traceback import print_exc

# Simple browser elements for about and help
class wxHTML(wxHTMLWindow):
    def __init__(self, *args, **kwargs):
        super(wxHTML,self).__init__(*args,**kwargs)
        self.Bind(wx.html.EVT_HTML_LINK_CLICKED,self.OnNavigate)
    def OnNavigate(self,e):
        webbrowser.open(e.GetLinkInfo().GetHref())
        

# Set standardised paramaters here:
DEFAULT_DICT = {
    "border_size" : 5,
    "min_window_width" : 650,
    "min_window_height" : 700,
    "instruction_box_width": 160,
    "about_text": [
                                "<p><h3><b>bin2txtswps</b></h3> depends on the following opensource projects:<br>",
                                "<ol><li><b>Neo</b>: <a href=\"https://github.com/NeuralEnsemble/python-neo\">https://github.com/NeuralEnsemble/python-neo</a></li>",
                                "<li><b>Numpy</b>: <a href=\"http://www.numpy.org/\">http://www.numpy.org/</a></li>",
                                "<li><b>wxPython</b>: <a href=\"https://www.wxpython.org/\">https://www.wxpython.org/</a></li>",
                                "<li><b>Python</b>: <a href=\"http://www.python.org/\">http://www.python.org/</a></li></ol></p>",
                                "",
                                "<p>bin2txtswps source is available at:<br>",
                                "<ul><li><a href=\"https://github.com/aleneapen/bin2txtswps\">https://github.com/aleneapen/bin2txtswps</a></li></ul><br>",
                                "<br>For further inquires, contact:<br>",
                                "<ul><li><a href=\"mailto:alen.eapen@bristol.ac.uk\">alen.eapen@bristol.ac.uk</a></li></ul></p>",
                    ],
    "help_page": """<html>
    <body>
    <h2>Using bin2txtswps</h2>
    <p>
    Bin2txtswps can be used to convert some common neuroscience binary files to ascii (Axon text format, ATF) files.
    <br>
    <br>
    Currently, the following binary formats are supported: 
    <ul><li>Axon binary format (ABF)</li>
    <li>WinWCP files (WCP)</li>
    <li>Igor pro files (IBW)</li>
    </ul>      
    </p> 

    </body><html>
    """,
    "instruction_text": ["> Choose the folder that contains binary data files to convert",
                        "> Then, start conversion",
                        "> Converted files will be written to a subfolder named \"bin2txtswps\" in the folder you chose",
                        "> Check help page for more information"]
}

# To redirect stdout and stderr to textbox in the program
class RedirectText(object):
    def __init__(self,aWxTextCtrl):
        self.out=aWxTextCtrl
 
    def write(self,string):
        wx.CallAfter(self.out.AppendText, string)



# Methods and classes to take care of threading
EVT_RESULT_ID = wx.NewId()

def EVT_RESULT(win, func):
    win.Connect(-1, -1, EVT_RESULT_ID, func)

class ResultEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data


class WorkerThread(Thread):
    def __init__(self, notify_window,user_func,variable_dict):
        Thread.__init__(self)
        self._notify_window = notify_window
        self._want_abort = 0
        self.user_func = user_func
        self.variable_dict = variable_dict
        self.start()

    def run(self):
        print("****************************")
        print("Starting conversion process:")
        start_time = time.time()
        file_i = 0
        try:
            for i in self.user_func(**self.variable_dict):
                file_i += i
                if self._want_abort:
                    print('Trying to stop conversion')
                    self.show_conversion_info(file_i,start_time)
                    wx.PostEvent(self._notify_window, ResultEvent(None))
                    return
        except Exception as e:
            print('*********************************************\nError in converting file. Stopping process \n*********************************************')
            print_exc()
            wx.PostEvent(self._notify_window, ResultEvent(None))
            return
        self.show_conversion_info(file_i,start_time)

        wx.PostEvent(self._notify_window, ResultEvent(1))
    def show_conversion_info(self,number_of_files,start_time):
        elapsed_time = time.time() - start_time
        # Summary info:
        print("Created " + str(number_of_files) + " new txt files.")
        print("Time elapsed: " + str('{:.3f}'.format(elapsed_time)) + " seconds")
        print("****************************")
    def abort(self):
        self._want_abort = 1


# Main frame which will hold program GUI

ID_FOLDER_BUTTON = wx.NewId()
ID_RUN_BUTTON = wx.NewId()
ID_CANCEL_BUTTON = wx.NewId()

class Main_Frame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(Main_Frame,self).__init__(*args,**kwargs)
        self.SetTitle("bin2txtswps")
        
        self.SetBackgroundColour("white")
        
        
        self.user_folderName = ""
        
        # Threading variables
        self.worker = None

        # Initialisation methods
        self.InitMenuBar()
        self.InitFrameContents()
        self.Show(True)


        # Generic binds
        self.Bind(wx.EVT_CLOSE,self.OnQuit)

        # Thread binds
        EVT_RESULT(self,self.OnProcessCompletion)

    def InitMenuBar(self):
        menubar = wx.MenuBar()
        controls_menu = wx.Menu()
        quitItem = controls_menu.Append(wx.ID_EXIT, 'Exit', 'Exit bin2txtswps')
        menubar.Append(controls_menu,'&Controls')
        help_menu = wx.Menu()
        helpItem = help_menu.Append(wx.ID_ANY, 'Help', 'Help')
        aboutItem = help_menu.Append(wx.ID_ABOUT, 'About', 'About bin2txtswps')
        
        menubar.Append(help_menu,'&Help')
        self.SetMenuBar(menubar)

        # Binds for Menu items
        self.Bind(wx.EVT_MENU,self.OnHelpMenu,helpItem)
        self.Bind(wx.EVT_MENU,self.OnAboutMenu,aboutItem)
        self.Bind(wx.EVT_MENU,self.OnQuit,quitItem)
        
        
    

    def InitFrameContents(self):
        panel = wx.Panel(self)
        self.main_sizer = wx.GridBagSizer(5,5)
        
        # HEADER
        header_title = wx.StaticText(panel,label="bin2txtswps")
        header_font = wx.Font(20, wx.DEFAULT,wx.NORMAL,wx.NORMAL)
        header_title.SetFont(header_font)
        self.main_sizer.Add(header_title,pos=(0,0),flag=wx.TOP|wx.LEFT|wx.BOTTOM, border = 10)
        self.main_sizer.Add(wx.StaticLine(panel), pos=(1, 0), span=(1, 5), flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=5)

        instructions_box = wx.StaticBox(panel, label="Instructions")
        self.instructions_box_sizer = wx.StaticBoxSizer(instructions_box,wx.VERTICAL)
        instructions_text_str = "\n".join(DEFAULT_DICT["instruction_text"])
        instructions_text = wx.StaticText(panel, label =instructions_text_str)
        self.instructions_box_sizer.Add(instructions_text,flag=wx.ALL, border=5)


        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.folder_button = wx.Button(panel, label="Choose Folder",id=ID_FOLDER_BUTTON)
        self.run_button = wx.Button(panel, label="Start Conversion",id=ID_RUN_BUTTON)
        self.cancel_button = wx.Button(panel, label="Cancel Conversion",id=ID_CANCEL_BUTTON)
        self.button_sizer.Add(self.folder_button,flag=wx.RIGHT|wx.LEFT|wx.BOTTOM, border=5)
        self.button_sizer.Add(self.run_button,flag=wx.RIGHT|wx.LEFT|wx.BOTTOM, border=5)
        self.button_sizer.Add(self.cancel_button,flag=wx.RIGHT|wx.LEFT|wx.BOTTOM, border=5)
        self.cancel_button.Enable(False)

        
        self.instructions_box_sizer.Add(self.button_sizer)
        

        output_box = wx.StaticBox(panel, label="Output")
        output_box_sizer = wx.StaticBoxSizer(output_box,orient=wx.VERTICAL)
        output_text = wx.TextCtrl(output_box,style=wx.TE_MULTILINE|wx.TE_READONLY)
        output_text.SetBackgroundColour(wx.Colour(0,0,0))
        output_text.SetForegroundColour(wx.Colour(255,255,255))
        
        output_text.SetFont(wx.Font(-1, wx.DEFAULT,wx.NORMAL,wx.NORMAL))

        
        output_box_sizer.Add(output_text,flag=wx.EXPAND|wx.ALL,proportion=1,border=5)
        output_box_sizer.SetMinSize(-1,300)
        redir=RedirectText(output_text)
        sys.stdout = redir
        sys.stderr = redir
        self.output_text_box = output_text
        
        bottom_space = wx.StaticText(panel)
        
        
        self.main_sizer.Add(self.instructions_box_sizer,pos=(2,0),span=(1,5),flag=wx.EXPAND|wx.ALL, border=5)
        self.main_sizer.Add(output_box_sizer,pos=(3,0),span=(1,5),flag=wx.ALL|wx.EXPAND, border=5)
        self.main_sizer.Add(bottom_space,pos=(4,0), border=1)
        self.main_sizer.AddGrowableCol(0)
        self.main_sizer.AddGrowableRow(3)
        
        

        panel.SetSizer(self.main_sizer)
        


        self.main_sizer.Fit(self)
        self.Center()
  
        # Binds for buttons
        self.Bind(wx.EVT_BUTTON,  self.OnButtonClick,id=ID_FOLDER_BUTTON)
        self.Bind(wx.EVT_BUTTON,  self.OnButtonClick,id=ID_RUN_BUTTON)
        self.Bind(wx.EVT_BUTTON,  self.OnButtonClick,id=ID_CANCEL_BUTTON)

    def OnAboutMenu(self,e):
        dialog = wx.Dialog(self)
        dialog.SetTitle("About bin2Txtswps")
        dialog.SetSize(DEFAULT_DICT["min_window_width"],400)
        html_contents = wxHTML(dialog)
        html_contents.SetPage("\n".join(DEFAULT_DICT["about_text"]))
        return dialog.ShowModal()
    
    def OnHelpMenu(self,e):
        help_frame = wx.Dialog(self)
        help_frame.SetTitle("Help")
        help_frame.SetSize(DEFAULT_DICT["min_window_width"],400)
        html_contents = wxHTML(help_frame)
        html_contents.SetPage(DEFAULT_DICT["help_page"])
        return help_frame.ShowModal()        
        

    def OnQuit(self,e):
        
        if self.worker:
            print('Trying to stop conversion')
            self.worker.abort()
            self.worker = None
        else:
            self.Close()
            self.Destroy()

    def OnButtonClick(self,e):
        id = e.GetId()
        
        if id == ID_FOLDER_BUTTON:
            dlg = wx.DirDialog(None, "Folder Selection",style=wx.DD_DIR_MUST_EXIST)
            if dlg.ShowModal() == wx.ID_OK:
                self.user_folderName = dlg.GetPath()
                print("Chosen folder is: {}".format(self.user_folderName))
                print("ATF files will be written to: {}".format(os.path.join(self.user_folderName,"bin2txtswps")))
                
            else:
                print("Folder selection cancelled")
            dlg.Destroy()
        if id == ID_RUN_BUTTON:
            if self.user_folderName == "":
                print("Choose a folder first")
                return
            
            if not self.worker:
                
                self.worker = WorkerThread(self,file_loop.folder_converter,{"folderName":self.user_folderName})
                self.folder_button.Enable(False)
                self.run_button.Enable(False)
                self.cancel_button.Enable(True)
                self.Fit()
            
            self.user_folderName = str()

        if id == ID_CANCEL_BUTTON:
            if self.worker:
                self.worker.abort()
            
    def OnProcessCompletion(self, event):
        """Show Result status."""
        if event.data is None:
            print("Process terminated")
        else:
            print("Process completed")

        self.folder_button.Enable(True)
        self.run_button.Enable(True)
        self.cancel_button.Enable(False)
        self.worker = None



if __name__ == "__main__":
    app = wx.App()
    Main_Frame(None)
    app.MainLoop()
