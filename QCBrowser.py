#!/usr/bin/python
#!encoding:utf-8
#!filename:QCBrowser.py
#----------------------------------------------------------------------------
# Name:         QCBrowser.py
# Purpose:      用于访问HP Quality Center服务器的浏览器客户端
# Author:       Sam Huang
# Email:        sam.hxq@gmail.com
# Blog:         www.hiadmin.org
# Copyright:    (c) 2013 by Sam.huang
# Licence:      wxWindows license
#----------------------------------------------------------------------
import wx
import wx.html2 as webview
import sys, os
import ConfigParser

#----------------------------------------------------------------------
name = "Quality Center Browser"
version = " 0.8"
Build = "20130913"

#----------------------------------------------------------------------
class QualityCenterBrowser(wx.Panel):
    """创建主函数
    创建button、StaticText并绑定函数事件

    """
    def __init__(self, parent,HomePage, frame=None):
        wx.Panel.__init__(self, parent, -1)
        self.HomePage = HomePage
        self.frame = frame      
        sizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.wv = webview.WebView.New(self)
        #显示地址栏URL地址
        self.Bind(webview.EVT_WEBVIEW_LOADED, self.OnWebViewLoaded, self.wv)
        
        #创建回退按钮
        btn = wx.BitmapButton(self, -1, wx.Bitmap("src/left.png"),
                                style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnPrevPageButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)
        self.Bind(wx.EVT_UPDATE_UI, self.OnCheckCanGoBack, btn)

        #创建前进按钮
        btn = wx.BitmapButton(self, -1, wx.Bitmap("src/right.png"),
                                style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnNextPageButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)
        self.Bind(wx.EVT_UPDATE_UI, self.OnCheckCanGoForward, btn)

        #创建刷新按钮
        btn = wx.BitmapButton(self, -1,wx.Bitmap("src/reload.png"),
                                style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnRefreshPageButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)

        #创建txt描述
        txt = wx.StaticText(self, -1, "Address:")
        btnSizer.Add(txt, 0, wx.CENTER|wx.ALL, 2)

        #创建地址栏下来菜单中的URL地址列表
        self.location = wx.ComboBox(self, -1, "", 
                            style=wx.CB_DROPDOWN|wx.TE_PROCESS_ENTER)
        self.location.AppendItems(['http://qc.hiadmin.org/',
                                    'http://www.whatbrowser.org/intl/zh-CN/'])
        self.Bind(wx.EVT_COMBOBOX, self.OnLocationSelect, self.location)
        self.location.Bind(wx.EVT_TEXT_ENTER, self.OnLocationEnter)
        btnSizer.Add(self.location, 1, wx.EXPAND|wx.ALL, 2)

        sizer.Add(btnSizer, 0, wx.EXPAND)
        sizer.Add(self.wv, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.wv.LoadURL(self.HomePage)


    # WebView events
    def OnWebViewLoaded(self, evt):
        # 地址栏显示完整的URL地址
        self.HomePage = evt.GetURL()
        self.location.SetValue(self.HomePage)
        
    # Control bar events
    def OnLocationSelect(self, evt):
        url = self.location.GetStringSelection()
        self.wv.LoadURL(url)

    def OnLocationEnter(self, evt):
        url = self.location.GetValue()
        self.location.Append(url)
        self.wv.LoadURL(url)

    def OnPrevPageButton(self, event):
        self.wv.GoBack()

    def OnNextPageButton(self, event):
        self.wv.GoForward()

    def OnCheckCanGoBack(self, event):
        event.Enable(self.wv.CanGoBack())
        
    def OnCheckCanGoForward(self, event):
        event.Enable(self.wv.CanGoForward())

    def OnRefreshPageButton(self, evt):
        self.wv.Reload()
              
#----------------------------------------------------------------------
def QCBrowserRun(frame, nb):
    """
    如果配置文件存在就从配置文件里面读取配置信息、否则就默认配置
    """
    if os.path.exists("config.ini") == True: 
        cf = ConfigParser.ConfigParser()
        cf.read("config.ini")
        HomePage = cf.get("info","url") #默认主页
        if "192.168" not in HomePage:
            HomePage = "http://qc.hiadmin.org"
    else:
        HomePage = "http://qc.hiadmin.org"

    win = QualityCenterBrowser(nb,HomePage)
    return win

#----------------------------------------------------------------------
class QualityCenterBrowserApp(wx.App):
    """创建窗口控件
    """
    def __init__(self, module):
        self.name = name
        self.demoModule = module
        wx.App.__init__(self)

    def OnInit(self):
        #设置浏览器窗口大小，名称等信息
        frame = wx.Frame(None, -1, self.name + version, size=(950,650))
        frame.SetIcon(wx.Icon("src\QCBrowser_32.ico",wx.BITMAP_TYPE_ICO))
        frame.CreateStatusBar() #创建状态栏
        menuBar = wx.MenuBar() #创建菜单
        menu = wx.Menu()
        menuBar.Append(menu, "&about")

        ns = {}
        ns['wx'] = wx
        ns['app'] = self
        ns['module'] = self.demoModule
        ns['frame'] = frame
        
        frame.SetMenuBar(menuBar) #设置菜单
        frame.Show(True)
        win = self.demoModule.QCBrowserRun(frame, frame)                
        return True

#----------------------------------------------------------------------------
def QCBrowserApp(argv):
    import QCBrowser as module #动态加载模块
    app = QualityCenterBrowserApp(module)
    app.MainLoop()

#----------------------------------------------------------------------
if __name__ == '__main__':
    QCBrowserApp(['QCBrowser.py'])

