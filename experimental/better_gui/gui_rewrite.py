import wx

class Example(wx.Frame):
    def __init__(self,*args,**kwargs):
        super(Example,self).__init__(*args,**kwargs)
        self.InitUI()
        self.SetTitle('Bin2txtswps')
        self.Centre()
        self.Show(True)

    def InitUI(self):
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        quitItem = fileMenu.Append(wx.ID_EXIT, 'Exit', 'Exit bin2txtswps')
        menubar.Append(fileMenu,'&Controls')
        

        aboutMenu = wx.Menu()
        menubar.Append(aboutMenu,"&About")
        
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.OnQuit,quitItem)
        self.Bind(wx.EVT_MENU, self.about_menu)
        wx.TextCtrl(self)


        



    def OnQuit(self,e):
        self.Close()
    def about_menu(self,event):
        pass

app = wx.App()
Example(None)
app.MainLoop()