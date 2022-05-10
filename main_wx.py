'''
发包工具：基于python的socket开发
UI界面使用的是wxFormBuilder绘制，底层是wxpython库
多线程处理收发数据和等待手动发送数据
重定向print到UI界面显示打印
基本上涉及的技术就是上面这些东西
制作人——谢耿锋

'''
import wx
import myFarm
import sys
import socket
import io
import threading
import time
import pickle
import logging
from multiprocessing import Queue
import gc
import struct
import xlsxwriter
import xlrd2
from xlutils.copy import copy
import xlwt

path=r"测试数据.txt"
path2=r"heartpack.txt"
#path3=r"协议文档.xlsx"
path4=r"协议文档.xls"
protocal_dict={}  #协议号字典
Fomat=""          #协议格式

try:
    workbook = xlrd2.open_workbook(path4)
    new_book=copy(workbook)
    table=workbook.sheet_by_index(0)
    nrows=table.nrows
    if nrows > 1:
        List_protocal=[int(i) for i in table.col_values(0,start_rowx=1,end_rowx=None)]
        List1_fomat=table.col_values(1,start_rowx=1,end_rowx=None)
        if len(List_protocal)==len(List1_fomat):
            fomat_dict=dict(zip(List_protocal,List1_fomat))
            protocal_dict=fomat_dict
        else:
            print("协议格式文档的协议号与协议格式列长度不一致")
except Exception:
    workbook = xlsxwriter.Workbook(path4)
    worksheet = workbook.add_worksheet('sheet1')
    headings = ['协议号', '协议格式', '备注']
    worksheet.write_row('A1', headings)
    workfomat = workbook.add_format({'bold': True,'border': 2,'align': 'center','valign': 'vcenter','fg_color': '#F4B084'})
    workbook.close()


rehost=myFarm.load_variavle(path)[0]
try:
    report=int(myFarm.load_variavle(path)[1])
except Exception:
    logging.warning("端口号必须是整数")

host=myFarm.load_variavle(path)[2]
try:
    port=int(myFarm.load_variavle(path)[3])
except Exception:
    logging.warning("端口号必须是整数")
server_start,will_send,heart_pack,num,filter,will_send2,num2,will_send3,num3,client_id,client_id2,client_id3,filterback,fil_prnumber,pro_fit,show_pro=1,"",[],0,-1,"",0,"",0,[],[],[],1,0,-1,-1
temp=sys.stdout
q=Queue(1000)
hex_di={0:'0',1:"1",2:"2",3:"3",4:"4",5:"5",6:"6",7:"7",8:"8",9:"9",10:"a",11:"b",12:"c",13:"d",14:"e",15:"f"}

def int_to_hex(L:list):
    global hex_di
    new_l=[]
    for i in L:
        di=i%16
        dd=i//16
        new_l.append(hex_di[dd]+hex_di[di])
    return new_l

def hex_to_int(L:list):
    global hex_di
    new_dict = {v: k for k, v in hex_di.items()}
    new_l=[]
    for i in L:
        data=new_dict[i[0]]*16+new_dict[i[1]]
        new_l.append(hex(data))
    return new_l

def byte_to_list(byte_data):
    mid_data = [int(i) for i in byte_data]
    string_data = int_to_hex(mid_data)
    result_data=" ".join(string_data)
    return result_data

def list_to_byte(s:str):
    datapack = hex_to_int(s.split(" "))
    pack_data = [int(i, 16) for i in datapack]
    pack = bytes(pack_data)
    return pack

def change_string(s:list):
    try:
        a=int(s)
        return a

    except:
        a=s.encode('utf-8')
        return a



class RedirectText(object):
    def __init__(self, aWxTextCtrl):
        self.out = aWxTextCtrl

    def write(self, string):
        self.out.AppendText(string)

def input_send(client,sendpack,number,q:Queue):
    try:
        datapack = hex_to_int(sendpack.split(" "))
        data = [int(i, 16) for i in datapack]
        pack = bytes(data)
        q.put(pack)
        n=number
        while n>0:
            try:
                client.send(pack)
                time.sleep(0.05)
                n-=1
                q.put(["发送成功"])
            except:
                q.put(['链接已中断'])
                break
    except Exception:
        logging.warning("序列化失败，请检查输入的发包内容是否有误")



def client_to_server(cnn, client,i,q:Queue):
    global server_start
    while server_start==1:
        try:
            recv_data = cnn.recv(4096)
            pro_num=struct.unpack("<H",recv_data[2:4])[0]
            if pro_fit==1 and pro_num==fil_prnumber:
                pass
            else:
                client.sendall(recv_data)
            if recv_data:
                string_recv=byte_to_list(recv_data)
                head=f" 端{i}>>>:"
                if show_pro==1:
                    show_recv=str(pro_num)+head+string_recv
                else:
                    show_recv = head+string_recv
                if filter==-1:
                    q.put(show_recv)
                elif string_recv!=heart_pack:
                    q.put(show_recv)
        except Exception:
            q.put(["服务器链接已经中断"])
            client.close()
            break



def server_to_client(client:socket, cnn,i,q:Queue):
    global server_start
    while server_start==1:
        try:
            read_data = client.recv(4096)
            pro_num = struct.unpack("<H", read_data[2:4])[0]
            if cnn:
                cnn.sendall(read_data)
                logging.info(read_data)
                if read_data and filterback == -1:
                    string_read = byte_to_list(read_data)
                    head = f" 端{i}<<<:"
                    if show_pro==1:
                        show_read = str(pro_num)+head+string_read
                    else:
                        show_read = head + string_read
                    if filter == -1:
                        q.put(show_read)
                    elif show_read != heart_pack:
                        q.put(show_read)
            else:
                client.close()
        except Exception:
            q.put(["客户端链接已经中断"])
            client.close()
            break





class handlesend_thread(threading.Thread):
    def __init__(self, client,sendpack,number,q):
        threading.Thread.__init__(self)  # 线程初始化，一定不能少
        self.client = client
        self.sendpack=sendpack
        self.num=number
        self.q=q

    def run(self) -> None:
        input_send(self.client,self.sendpack,self.num,self.q)


class server_thread(threading.Thread):
    def __init__(self, cnn, client,i,q):
        threading.Thread.__init__(self)
        self.cnn = cnn
        self.client = client
        self.i=i
        self.q = q

    def run(self) -> None:
        client_to_server(self.cnn, self.client,self.i,self.q)


class client_thread(threading.Thread):
    def __init__(self, client, cnn,i,q):
        threading.Thread.__init__(self)
        self.cnn = cnn
        self.client = client
        self.i=i
        self.q = q

    def run(self) -> None:
        server_to_client(self.client, self.cnn,self.i,self.q)

class Showlog(threading.Thread):
    def __init__(self,q:Queue,text_ctrl:wx.TextCtrl):
        threading.Thread.__init__(self)
        self.q=q
        self.text=text_ctrl
        sys.stdout = RedirectText(self.text)

    def run(self) -> None:
        i=0
        while 1:
            if not q.empty():
                data=q.get_nowait()
                print(data)
            else:
                time.sleep(0.05)



class Report(threading.Thread):
    def __init__(self, rehost, report, host, port,q,text1,text2,text3):
        threading.Thread.__init__(self)
        self.rehost = rehost
        self.report = report
        self.host = host
        self.port = port
        self.cnn={}
        self.client={}
        self.i=0
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((host, port))
        self.s.listen(1000)
        self.q=q
        self.text1=text1
        self.text2=text2
        self.text3=text3
        q.put((host, port))

    def run(self) -> None:
        global server_start
        while self.i<=1000 and server_start==1:
            try:
                self.i += 1
                q.put("ready")
                self.cnn[self.i], self.addr = self.s.accept()
                self.text1.SetValue(str(self.i))
                self.text2.SetValue(str(self.i))
                self.text3.SetValue(str(self.i))
                q.put(self.addr)
                self.client[self.i] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client[self.i].setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.client[self.i].connect((self.rehost,self.report))
                q.put("链接成功")
                self.thread1 = server_thread(self.cnn[self.i], self.client[self.i],self.i,self.q)
                self.thread2 = client_thread(self.client[self.i], self.cnn[self.i],self.i,self.q)
                self.thread1.start()
                self.thread2.start()
            except Exception:
                q.put("远程链接服务器失败或者代理服务器已关闭")
                break
        self.s.close()



    # def start(self):
    #     self.thread1.start()
    #     self.thread2.start()

    def handlesend(self,will_send,num,i):
        thread3 = handlesend_thread(self.client[i], will_send,num,self.q)
        thread3.start()




class Mainwindow(myFarm.MyFrame1):
    def __init__(self,parent):
        myFarm.MyFrame1.__init__(self,parent)


    def local_ip( self, event ):
        global host
        host=self.m_textCtrl1.GetValue()
        logging.info(host)
        addr_data=myFarm.load_variavle(path)
        addr_data[2]=host
        myFarm.save_variable(addr_data,path)


    def local_port(self, event):
        global port
        port=int(self.m_textCtrl2.GetValue())
        logging.info(port)
        addr_data = myFarm.load_variavle(path)
        addr_data[3] = str(port)
        myFarm.save_variable(addr_data, path)


    def server_ip(self, event):
        global rehost
        rehost=self.m_textCtrl3.GetValue()
        logging.info(rehost)
        addr_data = myFarm.load_variavle(path)
        addr_data[0] = rehost
        myFarm.save_variable(addr_data, path)



    def server_port(self, event):
        global report
        report=int(self.m_textCtrl4.GetValue())
        logging.info(report)
        addr_data = myFarm.load_variavle(path)
        addr_data[1] = str(report)
        myFarm.save_variable(addr_data, path)


    def start_all(self, event):
        global r,rehost, report, host, port,q,server_start
        server_start=1
        r= Report(rehost, report, host, port,q,self.m_textCtrl8,self.m_textCtrl11,self.m_textCtrl14)
        show=Showlog(q,self.m_textCtrl15)
        show.start()
        r.start()


    def stop_server(self, event):
        global server_start
        server_start=-server_start

    def send_pack(self, event):
        global will_send,protocal_dict
        will_send=self.m_textCtrl5.GetValue()
        try:
            btye_data=list_to_byte(will_send)
            pro_num = struct.unpack("<H", btye_data[2:4])[0]
            if pro_num in protocal_dict:
                self.m_textFomat.SetValue(protocal_dict[pro_num])
            q.put(will_send)
        except Exception:
            pass

    def send_time(self, event):
        global num
        try:
            num=int(self.m_textCtrl6.GetValue())
        except Exception:
            q.put("输入数据有误,只能输入数字")
        q.put(num)

    def client_id(self, event):
        global client_id
        try:
            client_id=self.m_textCtrl8.GetValue().split(",")
            q.put(client_id)
        except Exception:
            q.put("请输入客户端序号，如果有多个用,号隔开")

    def handle_send(self, event):
        if len(will_send) > 2:
            for i in client_id:
                r.handlesend(will_send,num,int(i))
        else:
            q.put("发送内容为空")

    def send_pack2(self, event):
        global will_send2
        will_send2 = self.m_textCtrl9.GetValue()
        q.put(will_send2)

    def send_time2(self, event):
        global num2
        try:
            num2 = int(self.m_textCtrl10.GetValue())
        except Exception:
            logging.warning("输入数据有误,只能输入数字")
        q.put(num2)

    def client_id2(self, event):
        global client_id2
        try:
            client_id2 = self.m_textCtrl11.GetValue().split(",")
            q.put(client_id2)
        except Exception:
            logging.warning("请输入客户端序号，如果有多个用,号隔开")

    def hendle_send2(self, event):
        if len(will_send2) > 2:
            for i in client_id2:
                r.handlesend(will_send2,num2,int(i))
        else:
            q.put("发送内容为空")

    def send_pack3(self, event):
        global will_send3
        will_send3 = self.m_textCtrl12.GetValue()
        print(will_send3)

    def send_time3(self, event):
        global num3
        try:
            num3 = int(self.m_textCtrl13.GetValue())
        except Exception:
            q.put("输入数据有误,只能输入数字")
        q.put(num3)

    def client_id3(self, event):
        global client_id3
        try:
            client_id3 = self.m_textCtrl14.GetValue().split(",")
            q.put(client_id3)
        except Exception:
            q.put("请输入客户端序号，如果有多个用,号隔开")

    def hendle_send3(self, event):
        if len(will_send3) > 2:
            for i in client_id3:
                r.handlesend(will_send3,num3,int(i))
        else:
            q.put("发送内容为空")

    def heart_data(self, event):
        global heart_pack
        heart_pack=self.m_textCtrl7.GetValue()
        myFarm.save_variable(heart_pack,path2)
        q.put(heart_pack)

    def start_filter(self, event):
        global filter,heart_pack
        filter=-filter
        heart_pack = self.m_textCtrl7.GetValue()
        q.put(f"1是开启心跳过滤，-1是关闭心跳过滤：{filter}")

    def close_sokect(self, event):
        r.s.close()
        r.client.close()

    def filter_reback(self, event):
        global filterback
        filterback=-filterback
        q.put(f"过滤服务器回包1是开启过滤，-1是不过滤：{filterback}")

    def clear_print(self, event):
        self.m_textCtrl15.Clear()

    def send_all_pack(self, event):
        for i in client_id:
            r.handlesend(will_send, num, int(i))
            r.handlesend(will_send2, num, int(i))
            r.handlesend(will_send3, num, int(i))

    def fomat(self, event):
        global Fomat
        Fomat=self.m_textFomat.GetValue()

    def unpack(self, event):
        datapack = hex_to_int(will_send.split(" "))
        data = [int(i, 16) for i in datapack]
        pack = bytes(data)
        try:
            pack_value=list(struct.unpack(Fomat,pack))
            pack_str=[i.decode('utf-8') if isinstance(i,bytes) else i for i in pack_value]
            value = " ".join([str(i) for i in pack_str])
            self.m_textCtrl32.SetValue(value)
        except Exception as e:
            logging.debug(e)
            q.put("解包失败，协议格式的总长度和封包是否一致")


    def pack(self, event):
        global Fomat,nrows,path3,path4,new_book
        packdata=self.m_textCtrl32.GetValue().split(" ")
        pro_num = packdata[1]
        if pro_num not in protocal_dict:
            sheet=new_book.get_sheet(0)
            sheet.write(nrows,0,pro_num)
            sheet.write(nrows,1,Fomat)
            new_book.save(path4)
        pack = [change_string(i) for i in packdata]
        try:
            data=struct.pack(Fomat,*pack)
            self.m_textCtrl5.SetValue(byte_to_list(data))
        except Exception as e:
            logging.debug(e)
            q.put("封包失败")

    # def Pro_value(self, event):
    #     global Fomat
    #     value = self.m_textCtrl32.GetValue().split(" ")
    #     q.put(value)
    #     if len(value)>2:
    #         pro_num=int(value[1])
    #         q.put(pro_num)
    #         if int(pro_num) in protocal_dict and len(Fomat)<1:
    #             Fomat=protocal_dict[pro_num]
    #             self.m_textFomat.SetValue(Fomat)
    #             q.put(Fomat)





    def pro_number(self, event):
        global fil_prnumber
        try:
            fil_prnumber=int(self.m_textCtrl33.GetValue())
        except Exception:
            q.put("协议号必须是整数")

    def hook(self, event):
        global pro_fit
        pro_fit=-pro_fit
        q.put(f"拦截协议号{fil_prnumber}的包，1是拦截，-1是不拦截：{pro_fit}")

    def show_Pronumber(self, event):
        global show_pro
        show_pro=-show_pro
        q.put(f"1显示协议号，-1不显示：{show_pro}")

if __name__ == '__main__':
    logging.basicConfig(filename='example.log',format='%(levelname)s:%(message)s',level=logging.NOTSET)
    app = wx.App()
    main_win = Mainwindow(None)
    main_win.Show()
    app.MainLoop()

