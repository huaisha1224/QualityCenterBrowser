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
#----------------------------------------------------------------------------
import wx
import wx.html2 as webview
import wx.lib.inspection
import wx.lib.mixins.inspection
import sys, os
assertMode = wx.PYAPP_ASSERT_DIALOG
name = "Quality Center Browser"
version = " 0.5"

#----------------------------------------------------------------------
class QualityCenterBrowser(wx.Panel):
    """创建主函数
    创建button、StaticText并绑定函数事件

    """
    def __init__(self, parent, frame=None):
        wx.Panel.__init__(self, parent, -1)
        self.current = "http://qcbrowser.duapp.com/"
        self.frame = frame      
        sizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.wv = webview.WebView.New(self)
        #self.Bind(webview.EVT_WEBVIEW_NAVIGATING, self.OnWebViewNavigating, self.wv)
        self.Bind(webview.EVT_WEBVIEW_LOADED, self.OnWebViewLoaded, self.wv)
        
        #创建回退按钮
        btn = wx.Button(self, -1, "<-", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnPrevPageButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)
        self.Bind(wx.EVT_UPDATE_UI, self.OnCheckCanGoBack, btn)

        #创建前进按钮
        btn = wx.Button(self, -1, "->", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnNextPageButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)
        self.Bind(wx.EVT_UPDATE_UI, self.OnCheckCanGoForward, btn)

        #创建刷新按钮
        btn = wx.Button(self, -1, "Refresh", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnRefreshPageButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)

        #创建地址栏
        txt = wx.StaticText(self, -1, "Address:")
        btnSizer.Add(txt, 0, wx.CENTER|wx.ALL, 2)

        #创建地址栏下来菜单中的URL地址列表
        self.location = wx.ComboBox(
            self, -1, "", style=wx.CB_DROPDOWN|wx.TE_PROCESS_ENTER)
        self.location.AppendItems(['http://60.190.244.146:8090/qcbin',
                                   'http://qcbrowser.duapp.com/',
                                   'http://www.whatbrowser.org/intl/zh-CN/'])
        self.Bind(wx.EVT_COMBOBOX, self.OnLocationSelect, self.location)
        self.location.Bind(wx.EVT_TEXT_ENTER, self.OnLocationEnter)
        btnSizer.Add(self.location, 1, wx.EXPAND|wx.ALL, 2)


        sizer.Add(btnSizer, 0, wx.EXPAND)
        sizer.Add(self.wv, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.wv.LoadURL(self.current)


    # WebView events
    def OnWebViewLoaded(self, evt):
        # 地址栏显示完整的URL地址
        self.current = evt.GetURL()
        self.location.SetValue(self.current)
        

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
    win = QualityCenterBrowser(nb)
    return win

#----------------------------------------------------------------------
class QualityCenterBrowserApp(wx.App, wx.lib.mixins.inspection.InspectionMixin):
    def __init__(self, name, module):
        self.name = name
        self.demoModule = module
        wx.App.__init__(self, redirect=False)

    def OnInit(self):
        self.SetAssertMode(assertMode)
        self.InitInspection()  # for the InspectionMixin base class
        #设置浏览器窗口大小，名称等信息
        frame = wx.Frame(None, -1, self.name + version, pos=(50,50), size=(950,650),
                        style=wx.DEFAULT_FRAME_STYLE)
        frame.CreateStatusBar() #创建状态窗口

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
        self.frame = frame                    
        return True

#----------------------------------------------------------------------------
def QCBrowserApp(argv):
    import QCBrowser as module #动态加载模块
    app = QualityCenterBrowserApp(name, module)
    app.MainLoop()

#----------------------------
if __name__ == '__main__':
    QCBrowserApp(['','QCBrowser.py'])

