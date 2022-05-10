import wx
import wx.xrc
import os
import pickle
import sys
import logging

path=r"测试数据.txt"
path2=r"heartpack.txt"

def read_or_new_pickle(path, default):
    try:
        with open(path,"rb") as f:
            foo = pickle.load(f)
    except Exception:
        foo = default
        with open(path,"wb") as f:
            pickle.dump(foo, f)
    return foo
def save_variable(v,filename):
  f=open(filename,'wb')
  pickle.dump(v,f)
  f.close()
  return filename

def load_variavle(filename):
  f=open(filename,'rb')
  r=pickle.load(f)
  f.close()
  return r

init_data=["0","0","0","0"]
heartpack=" "
init_data=read_or_new_pickle(path,init_data)
rehost=init_data[0]
report=init_data[1]
host=init_data[2]
port=init_data[3]
heart_data=read_or_new_pickle(path2,heartpack)


class MyFrame1(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"发包工具", pos=wx.DefaultPosition, size=wx.Size(750, 700),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        gbSizer2 = wx.GridBagSizer(0, 0)
        gbSizer2.SetFlexibleDirection(wx.BOTH)
        gbSizer2.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, u"local", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        gbSizer2.Add(self.m_staticText2, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_textCtrl1 = wx.TextCtrl(self, wx.ID_ANY, host, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer2.Add(self.m_textCtrl1, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_textCtrl2 = wx.TextCtrl(self, wx.ID_ANY, port, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer2.Add(self.m_textCtrl2, wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_staticText3 = wx.StaticText(self, wx.ID_ANY, u"server", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText3.Wrap(-1)
        gbSizer2.Add(self.m_staticText3, wx.GBPosition(0, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_textCtrl3 = wx.TextCtrl(self, wx.ID_ANY, rehost, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer2.Add(self.m_textCtrl3, wx.GBPosition(0, 4), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_textCtrl4 = wx.TextCtrl(self, wx.ID_ANY, report, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer2.Add(self.m_textCtrl4, wx.GBPosition(0, 5), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_button1 = wx.Button(self, wx.ID_ANY, u"启动", wx.DefaultPosition, wx.Size(60, -1), 0)
        gbSizer2.Add(self.m_button1, wx.GBPosition(0, 6), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_button_stop = wx.Button(self, wx.ID_ANY, u"停止", wx.DefaultPosition, wx.Size(60, -1), 0)
        gbSizer2.Add(self.m_button_stop, wx.GBPosition(0, 7), wx.GBSpan(1, 1), wx.ALL, 5)

        bSizer1.Add(gbSizer2, 1, wx.EXPAND, 5)

        gbSizer8 = wx.GridBagSizer(0, 0)
        gbSizer8.SetFlexibleDirection(wx.BOTH)
        gbSizer8.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        gbSizer8.SetMinSize(wx.Size(-1, 22))
        self.m_staticText5 = wx.StaticText(self, wx.ID_ANY, u"发包内容", wx.DefaultPosition, wx.Size(520, 20), 0)
        self.m_staticText5.Wrap(-1)
        gbSizer8.Add(self.m_staticText5, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_staticText6 = wx.StaticText(self, wx.ID_ANY, u"次数", wx.DefaultPosition, wx.Size(30, 20), 0)
        self.m_staticText6.Wrap(-1)
        gbSizer8.Add(self.m_staticText6, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_staticText7 = wx.StaticText(self, wx.ID_ANY, u"客户端序号", wx.DefaultPosition, wx.Size(60, 20), 0)
        self.m_staticText7.Wrap(-1)
        gbSizer8.Add(self.m_staticText7, wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        bSizer1.Add(gbSizer8, 1, wx.EXPAND, 5)

        gbSizer4 = wx.GridBagSizer(0, 0)
        gbSizer4.SetFlexibleDirection(wx.BOTH)
        gbSizer4.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_textCtrl5 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(520, -1), 0)
        gbSizer4.Add(self.m_textCtrl5, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_textCtrl6 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(30, -1), 0)
        gbSizer4.Add(self.m_textCtrl6, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_textCtrl8 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(60, -1), 0)
        gbSizer4.Add(self.m_textCtrl8, wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_button2 = wx.Button(self, wx.ID_ANY, u"发送", wx.DefaultPosition, wx.Size(45, -1), 0)
        gbSizer4.Add(self.m_button2, wx.GBPosition(0, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        bSizer1.Add(gbSizer4, 1, wx.EXPAND, 5)

        gbSizer6 = wx.GridBagSizer(0, 0)
        gbSizer6.SetFlexibleDirection(wx.BOTH)
        gbSizer6.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_textCtrl9 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(520, -1), 0)
        gbSizer6.Add(self.m_textCtrl9, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_textCtrl10 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(30, -1), 0)
        gbSizer6.Add(self.m_textCtrl10, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_textCtrl11 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(60, -1), 0)
        gbSizer6.Add(self.m_textCtrl11, wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_button5 = wx.Button(self, wx.ID_ANY, u"发送", wx.DefaultPosition, wx.Size(45, -1), 0)
        gbSizer6.Add(self.m_button5, wx.GBPosition(0, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        bSizer1.Add(gbSizer6, 1, wx.EXPAND, 5)

        gbSizer7 = wx.GridBagSizer(0, 0)
        gbSizer7.SetFlexibleDirection(wx.BOTH)
        gbSizer7.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_textCtrl12 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(520, -1), 0)
        gbSizer7.Add(self.m_textCtrl12, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_textCtrl13 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(30, -1), 0)
        gbSizer7.Add(self.m_textCtrl13, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_textCtrl14 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(60, -1), 0)
        gbSizer7.Add(self.m_textCtrl14, wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_button6 = wx.Button(self, wx.ID_ANY, u"发送", wx.DefaultPosition, wx.Size(45, -1), 0)
        gbSizer7.Add(self.m_button6, wx.GBPosition(0, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        bSizer1.Add(gbSizer7, 1, wx.EXPAND, 5)

        gbSizer5 = wx.GridBagSizer(0, 0)
        gbSizer5.SetFlexibleDirection(wx.BOTH)
        gbSizer5.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText4 = wx.StaticText(self, wx.ID_ANY, u"心跳包", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText4.Wrap(-1)
        gbSizer5.Add(self.m_staticText4, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_textCtrl7 = wx.TextCtrl(self, wx.ID_ANY, heart_data, wx.DefaultPosition, wx.Size(300, -1), 0)
        gbSizer5.Add(self.m_textCtrl7, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_button3 = wx.Button(self, wx.ID_ANY, u"过滤", wx.DefaultPosition, wx.Size(80, -1), 0)
        gbSizer5.Add(self.m_button3, wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_button4 = wx.Button(self, wx.ID_ANY, u"过滤回包", wx.DefaultPosition, wx.Size(80, -1), 0)
        gbSizer5.Add(self.m_button4, wx.GBPosition(0, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_button54 = wx.Button(self, wx.ID_ANY, u"清除记录", wx.DefaultPosition, wx.Size(80, -1), 0)
        gbSizer5.Add(self.m_button54, wx.GBPosition(0, 4), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_button56 = wx.Button(self, wx.ID_ANY, u"一键发包", wx.DefaultPosition, wx.Size(80, -1), 0)
        gbSizer5.Add(self.m_button56, wx.GBPosition(0, 5), wx.GBSpan(1, 1), wx.ALL, 5)

        bSizer1.Add(gbSizer5, 1, wx.EXPAND, 5)

        gbSizer9 = wx.GridBagSizer(0, 0)
        gbSizer9.SetFlexibleDirection(wx.BOTH)
        gbSizer9.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText8 = wx.StaticText(self, wx.ID_ANY, u"协议格式", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText8.Wrap(-1)
        gbSizer9.Add(self.m_staticText8, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_textFomat = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer9.Add(self.m_textFomat, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_button57 = wx.Button(self, wx.ID_ANY, u"解包", wx.DefaultPosition, wx.Size(80, -1), 0)
        gbSizer9.Add(self.m_button57, wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_textCtrl32 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(347, -1), 0)
        gbSizer9.Add(self.m_textCtrl32, wx.GBPosition(0, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_button58 = wx.Button(self, wx.ID_ANY, u"封包", wx.DefaultPosition, wx.Size(80, -1), 0)
        gbSizer9.Add(self.m_button58, wx.GBPosition(0, 4), wx.GBSpan(1, 1), wx.ALL, 5)

        bSizer1.Add(gbSizer9, 1, wx.EXPAND, 5)

        gbSizer10 = wx.GridBagSizer(0, 0)
        gbSizer10.SetFlexibleDirection(wx.BOTH)
        gbSizer10.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_textCtrl33 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(150, -1), 0)
        gbSizer10.Add(self.m_textCtrl33, wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_button59 = wx.Button(self, wx.ID_ANY, u"拦截该协议号包", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer10.Add(self.m_button59, wx.GBPosition(0, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_button60 = wx.Button(self, wx.ID_ANY, u"显示协议号", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer10.Add(self.m_button60, wx.GBPosition(0, 4), wx.GBSpan(1, 1), wx.ALL, 5)

        bSizer1.Add(gbSizer10, 1, wx.EXPAND, 5)

        self.m_textCtrl15 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(740, 350),
                                        wx.TE_MULTILINE | wx.TE_READONLY)
        bSizer1.Add(self.m_textCtrl15, 0, wx.ALL, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_textCtrl1.Bind(wx.EVT_TEXT, self.local_ip)
        self.m_textCtrl2.Bind(wx.EVT_TEXT, self.local_port)
        self.m_textCtrl3.Bind(wx.EVT_TEXT, self.server_ip)
        self.m_textCtrl4.Bind(wx.EVT_TEXT, self.server_port)
        self.m_button1.Bind(wx.EVT_BUTTON, self.start_all)
        self.m_button_stop.Bind(wx.EVT_BUTTON, self.stop_server)
        self.m_textCtrl5.Bind(wx.EVT_TEXT, self.send_pack)
        self.m_textCtrl6.Bind(wx.EVT_TEXT, self.send_time)
        self.m_textCtrl8.Bind(wx.EVT_TEXT, self.client_id)
        self.m_button2.Bind(wx.EVT_BUTTON, self.handle_send)
        self.m_textCtrl9.Bind(wx.EVT_TEXT, self.send_pack2)
        self.m_textCtrl10.Bind(wx.EVT_TEXT, self.send_time2)
        self.m_textCtrl11.Bind(wx.EVT_TEXT, self.client_id2)
        self.m_button5.Bind(wx.EVT_BUTTON, self.hendle_send2)
        self.m_textCtrl12.Bind(wx.EVT_TEXT, self.send_pack3)
        self.m_textCtrl13.Bind(wx.EVT_TEXT, self.send_time3)
        self.m_textCtrl14.Bind(wx.EVT_TEXT, self.client_id3)
        self.m_button6.Bind(wx.EVT_BUTTON, self.hendle_send3)
        self.m_textCtrl7.Bind(wx.EVT_TEXT, self.heart_data)
        self.m_button3.Bind(wx.EVT_BUTTON, self.start_filter)
        self.m_button4.Bind(wx.EVT_BUTTON, self.filter_reback)
        self.m_button54.Bind(wx.EVT_BUTTON, self.clear_print)
        self.m_button56.Bind(wx.EVT_BUTTON, self.send_all_pack)
        self.m_textFomat.Bind(wx.EVT_TEXT, self.fomat)
        self.m_button57.Bind(wx.EVT_BUTTON, self.unpack)
        self.m_textCtrl32.Bind(wx.EVT_TEXT, self.Pro_value)
        self.m_button58.Bind(wx.EVT_BUTTON, self.pack)
        self.m_textCtrl33.Bind(wx.EVT_TEXT, self.pro_number)
        self.m_button59.Bind(wx.EVT_BUTTON, self.hook)
        self.m_button60.Bind(wx.EVT_BUTTON, self.show_Pronumber)
        self.m_textCtrl15.Bind(wx.EVT_TEXT, self.log_show)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def local_ip(self, event):
        event.Skip()

    def local_port(self, event):
        event.Skip()

    def server_ip(self, event):
        event.Skip()

    def server_port(self, event):
        event.Skip()

    def start_all(self, event):
        event.Skip()

    def stop_server(self, event):
        event.Skip()

    def send_pack(self, event):
        event.Skip()

    def send_time(self, event):
        event.Skip()

    def client_id(self, event):
        event.Skip()

    def handle_send(self, event):
        event.Skip()

    def send_pack2(self, event):
        event.Skip()

    def send_time2(self, event):
        event.Skip()

    def client_id2(self, event):
        event.Skip()

    def hendle_send2(self, event):
        event.Skip()

    def send_pack3(self, event):
        event.Skip()

    def send_time3(self, event):
        event.Skip()

    def client_id3(self, event):
        event.Skip()

    def hendle_send3(self, event):
        event.Skip()

    def heart_data(self, event):
        event.Skip()

    def start_filter(self, event):
        event.Skip()

    def filter_reback(self, event):
        event.Skip()

    def clear_print(self, event):
        event.Skip()

    def send_all_pack(self, event):
        event.Skip()

    def fomat(self, event):
        event.Skip()

    def unpack(self, event):
        event.Skip()

    def Pro_value(self, event):
        event.Skip()

    def pack(self, event):
        event.Skip()

    def pro_number(self, event):
        event.Skip()

    def hook(self, event):
        event.Skip()

    def show_Pronumber(self, event):
        event.Skip()

    def log_show(self, event):
        event.Skip()