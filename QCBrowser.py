#!/usr/bin/python
#!encoding:utf-8
#!filename:QCBrowser.py
#Python3.6
#-------------------------------------------------------------------

# Name:         QCBrowser.py
# Purpose:      用于访问HP Quality Center服务器的浏览器客户端
# Author:       Sam Huang
# Email:        sam.hxq@gmail.com
# Blog:         www.hiadmin.org
# Copyright:    (c) 2018 by Sam.huang
# Licence:      wxWindows license
#---------------------------------------------------------------------

name = "Quality Center Browser"
version = " 1.5"
Build = "20180321"
#---------------------------------------------------------------------

import wx
import wx.html2 as webview
import sys, os
import requests
import webbrowser
import configparser
#----------------------------------------------------------------------


class QualityCenterBrowser(wx.Panel):
    """创建主函数
    创建button、StaticText并绑定函数事件
    """
    def __init__(self, parent, log, frame=None):
        #self.log = log
        wx.Panel.__init__(self, parent, -1)

        #self.HomePage = "http://qc.hiadmin.org"
        self.HomePage = HomePage
        self.frame = frame
        if frame:
            self.titleBase = frame.GetTitle()

        sizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.wv = webview.WebView.New(self)

        #显示地址栏URL地址
        self.Bind(webview.EVT_WEBVIEW_LOADED, self.OnWebViewLoaded, self.wv)


        #创建返回按钮
        btn = wx.BitmapButton(self, -1, wx.Bitmap('src/Left.png'))
        self.Bind(wx.EVT_BUTTON, self.OnPrevPageButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)

        #创建前进按钮
        btn = wx.BitmapButton(self, -1, wx.Bitmap('src/Right.png'))
        self.Bind(wx.EVT_BUTTON, self.OnNextPageButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)

        #创建刷新按钮
        btn = wx.BitmapButton(self, -1, wx.Bitmap('src/Reload.png'))
        self.Bind(wx.EVT_BUTTON, self.OnStopButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)

        #创建一个主页按钮
        btn = wx.BitmapButton(self, -1,wx.Bitmap('src/Home.png'))
        self.Bind(wx.EVT_BUTTON, self.OnHomePage, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)

        txt = wx.StaticText(self, -1, "Address:")
        btnSizer.Add(txt, 0, wx.CENTER|wx.ALL, 2)

        self.location = wx.ComboBox(
            self, -1, "", style=wx.CB_DROPDOWN|wx.TE_PROCESS_ENTER)
        self.location.AppendItems(['http://qc.hiadmin.org',
                                  'http://qc.hiadmin.org/ua.html'])
        self.Bind(wx.EVT_COMBOBOX, self.OnLocationSelect, self.location)
        self.location.Bind(wx.EVT_TEXT_ENTER, self.OnLocationEnter)
        btnSizer.Add(self.location, 1, wx.EXPAND|wx.ALL, 2)

        #创建帮助按钮
        btn = wx.BitmapButton(self, -1,wx.Bitmap("src/Help.png"))
        #btn = wx.Button(self, -1, "Help", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnHelpUrl, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)

        #创建升级按钮
        btn = wx.BitmapButton(self, -1,wx.Bitmap("src/Download.png"))
        self.Bind(wx.EVT_BUTTON, self.OnUpdate, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)

        sizer.Add(btnSizer, 0, wx.EXPAND)
        sizer.Add(self.wv, 1, wx.EXPAND)
        self.SetSizer(sizer)

        self.wv.LoadURL(self.HomePage)


    def ShutdownDemo(self):
        # put the frame title back
        if self.frame:
            self.frame.SetTitle(self.titleBase)

    def OnWebViewLoaded(self, evt):
        # The full document has loaded
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

    def OnStopButton(self, evt):
        self.wv.Stop()

    def OnRefreshPageButton(self, evt):
        self.wv.Reload()


    #按钮主页事件
    def OnHomePage(self, event):
        url = HomePage
        self.wv.LoadURL(url)

    def OnHelpUrl(self, evt):
        webbrowser.open_new_tab("http://qc.hiadmin.org/qa/")

    def OnUpdate(self,evt):
        webbrowser.open_new_tab("http://qc.hiadmin.org/download/")
#----------------------------------------------------------------------

def QCBrowserRun(frame, nb):
    """
    如果配置文件存在就从配置文件里面读取配置信息、否则就默认配置
    """
    if os.path.exists("config.ini") == True:
        cf = configparser.ConfigParser()
        cf.read("config.ini")
        global HomePage
        HomePage = cf.get("info","url") #默认主页
        if "192.168" not in HomePage:
            HomePage = "http://qc.hiadmin.org/direction/"
    else:
        HomePage = "http://qc.hiadmin.org/direction/"

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
        # 设置浏览器窗口大小，名称等信息
        frame = wx.Frame(None, -1, self.name + version, size=(1080, 800))
        frame.SetIcon(wx.Icon("src\QCBrowser_32.ico", wx.BITMAP_TYPE_ICO))
        frame.CreateStatusBar()  # 创建状态栏

        ns = {}
        ns['wx'] = wx
        ns['app'] = self
        ns['module'] = self.demoModule
        ns['frame'] = frame

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
