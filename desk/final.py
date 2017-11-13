import wx, wx.html
from makeindex import *
import os
from searchquery import *

class HtmlWindow(wx.html.HtmlWindow):
    def __init__(self, parent, id, size=(400,600)):
        wx.html.HtmlWindow.__init__(self, parent, id, size=size)
    def OnLinkClicked(self, link):
        wx.LaunchDefaultBrowser(link.GetHref())

class SearchBox(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "search answer")
        hwin = HtmlWindow(self, -1)
        global answer
        hwin.SetPage(answer)
        irep = hwin.GetInternalRepresentation()
        hwin.SetSize((irep.GetWidth()+25, irep.GetHeight()+10))
        self.SetClientSize(hwin.GetSize())
        self.CentreOnParent(wx.BOTH)
        self.SetFocus()

class myframe(wx.Frame):

    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, "Desktop Search Engine",size=(400,300))
        self.panel = wx.Panel(self)
        self.text = wx.TextCtrl(self.panel, -1, pos = (10,10), size=(300,-1))
        self.buttonsearch = wx.Button(self.panel, label = 'Search', pos=(310, 10), size=(60, -1))
        self.text_dir = wx.TextCtrl(self.panel, -1, pos= (10, 130), size = (300,-1))
        self.buttonindex = wx.Button(self.panel, label = "Index", pos=(165,200), size = (60,-1))
        self.buttonopen = wx.Button(self.panel, label = "Open", pos=(310,130), size = (60,-1))
        self.static_box = wx.StaticText(self.panel, -1, "Create file index, please enter your dir name:", pos = (10, 100))
        self.Bind(wx.EVT_BUTTON, self.index, self.buttonindex)
        dirname = os.environ['HOME']
        self.text_dir.SetValue(dirname + '/Desktop')
        self.Bind(wx.EVT_BUTTON,self.fopen,self.buttonopen)
        self.Bind(wx.EVT_BUTTON,self.fsearch,self.buttonsearch)

    def fopen(self,event):
		style=wx.OPEN
		fdialog=wx.DirDialog(self,'Open',style=style)
		if fdialog.ShowModal()==wx.ID_OK:
			self.path=fdialog.GetPath()
			self.text_dir.SetValue(self.path)

    def index(self, event):
        l = self.text_dir.GetValue()
        analyser = 'Stemming'
        xxx = make_index(l, analyser)
        if xxx:
            box1 = wx.MessageDialog(None, 'Finish making index!', 'finish', wx.OK)
            if box1.ShowModal() == wx.ID_OK:
                box1.Destroy()
        if not xxx:
            box2 = wx.MessageDialog(None, 'The dir does not exist!', 'wrong', wx.OK)
            if box2.ShowModal() == wx.ID_OK:
                box2.Destroy()
    def fsearch(self,event):
        l=self.text.GetValue()
        filetypelist = []
        global answer
        answer=''
        if not check_all_stop_words(l):
            box = wx.MessageDialog(None, 'STOP WORDS! NO information! please re-type!', 'stop words', wx.OK)
            if box.ShowModal() == wx.ID_OK:
                box.Destroy()
            self.text.Clear()
        else:
            a, b = searchfile(l, 'TF-IDF', 'OR', filetypelist, 'majorclust')
            print a,b
            answer += a
            dlg = SearchBox()
            dlg.Show()

if __name__=='__main__':
    app = wx.PySimpleApp()
    frame = myframe(None, -1)
    frame.Show()
    app.MainLoop()
