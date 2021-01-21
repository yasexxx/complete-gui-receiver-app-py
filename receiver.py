import os
import sys
import time
import tkinter as tk
import threading
import socket
import pyaudio
from tkinter import Button, PhotoImage, ttk
import selectors
from threading import Thread
import struct
from PIL import ImageTk, Image

LARGE_FONT= ("Verdana", 12)
logo_png = os.path.dirname(os.path.realpath(__file__))+'\\assets\\logo-select.ico'

class MainWindow(object):
    def __init__(self, master):
        super(MainWindow, self).__init__()
        self.master = master
        self.master.geometry('477x253')
        self.master.iconbitmap(r'{}'.format(logo_png))
        container = tk.Frame(self.master)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StandbyPage, SettingPage, ConnectPage, HomePage):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.configure(background='gold')
        self.frame = tk.Frame(self,  width=477 , height=253)
        self.frame.configure(background='gold')
        self.frame.place(x=0, y=0)
        label = tk.Label(self.frame, text="Go to Setting to \ninitialize connection.", fg='maroon',
                         bg='gold', font=('broadway', 15, 'bold'))

        label_2 = tk.Label(self.frame, text="Status: Disconnected", fg='maroon',
                         bg='gold', font=('broadway', 12, 'bold'))

        label_3 = tk.Label(self.frame, text="WiFi Receiver Interface", fg='maroon',
                         bg='gold', font=('broadway', 15, 'bold'))
        b1 = tk.Button(self, text="Settings", command=lambda: self.controller.show_frame(SettingPage), fg='black', bg="white",
                       relief='solid',
                       font=('arial', 10, 'bold'), width='6',
                       height='1')
        b2 = tk.Button(self.frame, text="Exit", command=self.exit_, fg='black', bg="white",
                       relief='solid',
                       font=('arial', 10, 'bold'), width='6',
                       height='1')

        label.place(relx=0.25, rely=0.60, anchor='w')
        
        label_2.place(relx=0.28, rely=0.40, anchor='w')
        label_3.place(relx=0.5, rely=0.05, anchor='n')          
        b1.place(x=0, y=0)
        b2.place(relx=0.94, rely=0 , anchor='n')
        path1 = os.path.dirname(os.path.realpath(__file__))+'\\assets\\wifi_.gif'
        path2 = os.path.dirname(os.path.realpath(__file__))+'\\assets\\logo-final.png'
        load_img = Image.open(path1)
        load_img2 = Image.open(path2)
        wd = 70
        ht = 70
        wd1 = 70
        ht1 = 70
        img_res2 = load_img2.resize((wd,ht), Image.ANTIALIAS)
        img_res1 = load_img.resize((wd1, ht1), Image.ANTIALIAS)
        get_img = ImageTk.PhotoImage(img_res1)
        img_logo = tk.Label(self.frame, image=get_img, bg="gold")
        get_img2 = ImageTk.PhotoImage(img_res2)
        img_logo2 = tk.Label(self.frame, image=get_img2, bg="gold")


        img_logo.image = get_img
        img_logo.place(relx=0.75, rely=0.3, anchor="w")
        img_logo2.image = get_img2
        img_logo2.place(relx=0.06, rely=0.3, anchor="w")

    def exit_(self):
        self.destroy()
        sys.exit()
                    
        


class StandbyPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.parent = parent
        self.configure(background='gold')
        self.frame = tk.Frame(self, width=477 , height=253)
        self.frame.place(x=0,y=0)
        self.frame.configure(background='gold')
    
        label = tk.Label(self.frame, text="", textvariable=change_text, fg='maroon',
                         bg='gold', width=20, font=('broadway', 25, 'bold'))
        
        label_2 = tk.Label(self.frame, text="Status: Connected", fg='maroon',
                         bg='gold',textvariable=change_text_1, font=('broadway', 12, 'bold')) 

        b1 = tk.Button(self.frame, text="Exit", command=self.exit_, fg='black', bg="white",
                       relief='solid',
                       font=('arial', 10, 'bold'), width='6',
                       height='1')

        self.b2 = tk.Button(self.frame, text="Off", command=self.toggle_button, fg='black', bg="white",
                       relief='raised',
                       font=('arial', 10, 'bold'), width='12',
                       height='2')
        
        label.pack(side="top", fill="both", expand=True)
        label.place(x=5, y=95)
        label_2.place(relx=0.33, rely=0.3, anchor='w')
        b1.place(relx=0.94, rely=0 , anchor='n')
        self.b2.place(relx=0.5, rely=0.75 , anchor='n')
        
        text = "Connection is \nEstablished!"
        change_text.set(text)
        change_text_1.set('Status: Server Offline')
        

    def initialize_onn(self):
        self.ip =  ip_addr.get()
        self.port = port_addr.get()
        self.port = self.port+1
        self.server = Server_Operation( self.ip, self.port)
        self.server._is_on1()
        self.server.create_server()

    def initialize_off(self):
        self.server._is_of1()
        self.server.create_server()

    def toggle_button(self):
        if self.b2.config('relief')[-1] == 'sunken':
            self.b2.config(relief="raised")
            self.b2['text'] ='Off'
            self.initialize_off()
            change_text_1.set('Status: Disconnected')
        else:
            self.b2.config(relief="sunken")
            self.b2['text'] ='On'
            self.initialize_onn()
            #change_text_1.set('Status: Connecting...')

    def exit_(self):
        self.destroy()
        self.parent.destroy()
        sys.exit()
        
    def change_live(self):
        change_text.set("Live Announcement")

    def change_emergency(self):
        change_text.set("Emergency Alarm")

    def change_hourlybell(self):
        change_text.set("Hourly Bell")

    def change_standby(self):
        change_text.set("Standby Mode")


class SettingPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller= controller
        self.configure(background='gold')
        self.frame = tk.Frame(self, width=477 , height=253)
        self.frame.place(x=0,y=0)
        self.frame.configure(background='gold')
        label = tk.Label(self.frame, text="Settings", fg='maroon',
                         bg='gold', width=10, font=('broadway', 15, 'bold'))
        l1 = tk.Label(self.frame, text='IP Address:', bg='gold',
                        font=('arial', 15, 'bold'))
        l2 = tk.Label(self.frame, text='Port:', bg='gold',
                        font=('arial', 15, 'bold'))
        l3 = tk.Label(self.frame, text='', bg='gold',
                        font=('arial', 10, 'bold'), textvariable=bind_0)
        l4 = tk.Label(self.frame, text='', bg='gold',
                        font=('arial', 8, 'bold'), textvariable=ip_0)
        l5 = tk.Label(self.frame, text='', bg='gold',
                        font=('arial', 8, 'bold'), textvariable=port_0)
        e1 = tk.Entry(self.frame, textvariable=ip_addr,width=20,relief= 'solid') #state=read
        b1 = tk.Button(self, text="Back", command=lambda: controller.show_frame(HomePage), fg='black', bg="white",
                       relief='solid',
                       font=('arial', 10, 'bold'), width='6',
                       height='1')

        b2 = tk.Button(self, text="Confirm", command=self.confirm_on, fg='black', bg="white",
                       relief='solid',
                       font=('arial', 10, 'bold'), width='6',
                       height='1')
                    
        
        num_list = []
        for i in range (56000, 59999):
            num_list.append(str(i))
        if len(num_list)>0 :
            self.combo = ttk.Combobox(self.frame, width=15,values=num_list, height=7)
            self.combo.place(relx=0.5, rely=0.5, anchor='w')
            self.combo.current(0)
            self.combo.bind("<<ComboboxSelected>>", self.on_select)
        label.place(relx=0.5, rely=0.05, anchor='c')
        l1.place(relx=0.25, rely=0.3, anchor='w')
        l2.place(relx=0.25, rely=0.5, anchor='w')
        l3.place(relx=0.25, rely=0.75, anchor='w')
        l4.place(relx=0.28, rely=0.83, anchor='w')
        l5.place(relx=0.28, rely=0.90, anchor='w')
        e1.place(relx=0.5, rely=0.3, anchor='w')
        b1.place(x=0, y=0)
        b2.place(relx=0.5, rely=0.65, anchor='w')
        
    
        name = socket.gethostname()
        address = socket.gethostbyname(name)
        #ip_addr.set(address)


    def confirm_on(self):
        text1 = ip_addr.get()
        int1 = port_addr.get()
        text1 = 'IP: '+text1
        text2 = 'Port: '+str(int1)
        bind_0.set("Binding at:")
        ip_0.set(text1)
        port_0.set(text2)
        self._job_2 = self.frame.after(5000, self.go_to_connect)
    
    def go_to_connect(self):
        if self._job_2 is not None:
            self.frame.after_cancel(self._job_2)
            self._job_2 = None
            self.controller.show_frame(ConnectPage)
        
    def on_select(self, event=None):
        x = event.widget.get()
        number = int(x)
        port_addr.set(number)



class ConnectPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background = 'gold')
        self.frame = tk.Frame(self, width=447, height=253)
        self.frame.place(x=0,y=0)
        self.frame.configure(background = 'gold')
        photo = PhotoImage(file = "button_.gif") 
        self.b1 = Button(self.frame, text = 'Tap to connect', image = photo, bg='gold', 
                    command=self.connect_btn,border=0,activebackground='gold',compound='top')             
        self.b1.image = photo
        self.b1.place(relx=0.5, rely=0.5, anchor='c')
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.not_yet_connect = True

    def connect_btn(self):
        #w =self.controller.show_frame(StandbyPage)
        self.b1['state'] ='disabled'
        self.b1['image'] = None
        self.text_connect_('.')
        t1 = threading.Thread(target=self.binding_, daemon=True)
        t1.start()

    def binding_(self):
        #ip = 'localhost' 
        #port = int(12345)  

        ip = ip_addr.get()
        port = port_addr.get()
        addr = (ip, port)
        self.socket.bind(addr)
        print("Listening to: ",addr)
        self.socket.listen(5)
        conn, addr = self.socket.accept()
        if conn:
            print("Connected!", addr)
            self.not_yet_connect = False
            self.socket.close()

    def text_connect_(self, s):
        txt = "Connecting"+s
        print(txt)
        if len(txt)<20: 
            self.b1['text'] = txt
            self._job_1 = self.frame.after(1000, self.text_connect_, s+' .')
        else:
            if self._job_1 is not None:
                self.frame.after_cancel(self._job_1)
                self._job_1 = None
                if self.not_yet_connect:
                    self.text_connect_('.')
                else:
                    self.controller.show_frame(StandbyPage)



sel = selectors.DefaultSelector()


class Server_Operation(object):
    def __init__(self, host, port):
        super(Server_Operation, self).__init__()
        self.host = host
        self.port = port
        self.on_data = False
        self.is_on = False

    def create_server(self):
        if self.is_on:
            self.lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.lsock.setblocking(False)
            self.lsock.bind((self.host, self.port))
            self.lsock.listen(5)
            print('listening on', (self.host, self.port))
            change_text_1.set('Status: Server Connecting...')
            
            sel.register(self.lsock, selectors.EVENT_READ, data=self.accept_connection)
            thread_run = Thread(target=self.run_program, daemon=True)
            thread_run.start()
            #thread_run.join()
        else:
            return
    
    def _is_on1(self):
        self.is_on = True
        
    def _is_of1(self):
        self.is_on = False
        if self.lsock:
            sel.unregister(self.lsock)

    def accept_connection(self,sock, mask):
        conn, self.addr = sock.accept()  # Should be ready to read
        print(f"Connection established from:  {self.addr}")
        change_text_1.set('Status: Server Connected')
        change_text.set("Standby Mode")
        conn.setblocking(False)
        select_events = selectors.EVENT_READ | selectors.EVENT_WRITE
        sel.register(conn, select_events, data=self.service_connection)

    def service_connection(self, key, mask):
        sock = key
        if mask & selectors.EVENT_READ:
            self.read_handler(sock)
        #if mask & selectors.EVENT_WRITE:
            #self.write_handler(sock)

    def run_program(self):
        while True:
            if not self.is_on:
                break
            try:
                events = sel.select(timeout=None)
                for key, mask in events:
                    callback = key.data
                    callback(key.fileobj,mask)
            except WindowsError as e:
                break
                

    def read_handler(self, sock):
        try:
            recv_data = sock.recv(1024)
            if len(recv_data) > 0:
                self.on_data =True
        except Exception as e:
            sel.unregister(sock)
            sock.close()
            self.on_data =False
        if self.on_data:
            data_len = len(recv_data)
            if data_len == 27:
                try:
                    un_pack = struct.unpack(">i19si" ,recv_data)
                    data_1 = un_pack[0]
                    data_1 = int(data_1)
                    data_2 = un_pack[2]
                    data_2 = int(data_2)
                    data_3 = un_pack[1].decode()
                    if data_1 == 4020 and data_2 == 202304 and data_3[9:17] == "020opera":
                        print("Connected at 2")
                        change_text.set("Emergency Bell")
                        w2 = Server_wave(self.host, self.port)
                        sel.unregister(sock)
                        sock.close()
                except Exception as e:
                    print(f"the message is wrong 2: {e}")
                    sel.unregister(sock)
                    sock.close()
            elif data_len == 19:
                try:
                    un_pack = struct.unpack(">ii11s" ,recv_data)
                    data_1 = un_pack[0]
                    data_1 = int(data_1)
                    data_2 = un_pack[1]
                    data_2 = int(data_2)
                    data_3 = un_pack[2].decode()
                    if data_1 == 32 and data_2 == 2319 and data_3[4:9]=="rithm":
                        print('Connected at 1')
                        #print(ip_port)
                        #ip_add = ip_port[0]
                        #port_add = ip_port[1]
                        change_text.set("Live Announcement")
                        w1 = Speaker_Live(self.host, self.port)
                        sel.unregister(sock)
                        sock.close()
                except Exception as e:
                    print(f"the message is wrong: {e}")
                    sel.unregister(sock)
                    sock.close()

            elif data_len == 37:
                try:
                    un_pack = struct.unpack(">29sii" ,recv_data)
                    data_1 = un_pack[0].decode()
                    data_2 = un_pack[1]
                    data_2 = int(data_2)
                    data_3 = un_pack[2]
                    data_3 = int(data_3)
                    if data_1[5:22] == '20apBjok0q3k2oCo3' and data_2 == 10390 and data_3 == 209340:
                        print('Connected at 3')
                        #print(ip_port)
                        #ip_add = ip_port[0]
                        #port_add = ip_port[1]
                        change_text.set("Hourly Bell")
                        s3 = Server_hourbell(self.host, self.port)
                        sel.unregister(sock)
                        sock.close()
                except Exception as e:
                    print(f"the message is wrong: {e}")
                    sel.unregister(sock)
                    sock.close()

class Speaker_Live(object):
    def __init__(self,ip , port):
        super(Speaker_Live, self).__init__()
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        chunks =1024
        self.format = FORMAT
        self.rate = RATE
        self.channels = CHANNELS
        self.chunks = chunks
        self.frames = []
        self.stopp = False
        print("Speaker is ready to live!")
        self.ip = ip
        if port is not None:
            self.port = int(port)+1
        self.address = (self.ip, self.port)
        print("Live at : {}".format(self.address))
        self.initialize_speaker()


    def initialize_speaker(self):
        self.Audio = pyaudio.PyAudio()

        stream = self.Audio.open(format=self.format,
                            channels=self.channels,
                            rate=self.rate,
                            output=True,
                            frames_per_buffer=self.chunks,
                            )

        self.udpThread = threading.Thread(target=self.udpStream, daemon=True)
        self.AudioThread = threading.Thread(target=self.play, args=(stream,), daemon=True)
        self.udpThread.start()
        self.AudioThread.start()
        self.udpThread.join()
        self.AudioThread.join()


    def udpStream(self):
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            udp.bind(self.address)
        except Exception as e:
            print("error: {}".format(e))
        udp.settimeout(7)
        while True:
            try:
                soundData ,addr = udp.recvfrom(self.chunks*self.channels*2)
                self.frames.append(soundData)
                if soundData !=b'':
                    #print("data")
                    pass
                else:
                    print('no data')
            except Exception as e:
                print("error9: {}".format(e))
                self.stopp = True
                break
        print("closing connection")
        udp.close()


    def play(self,stream):
        BUFFER = 10
        print('Streaming now!')
        while True:
            if self.stopp:
                break
            if len(self.frames) == BUFFER:
                while True:
                    try:
                        stream.write(self.frames.pop(0), self.chunks)
                    except:
                        break

        print("stop streaming")
        stream.stop_stream()
        stream.close()
        self.Audio.terminate()
        change_text.set("Standby Mode")


class Server_wave(object):
    def __init__(self, ip, port):
        super(Server_wave, self).__init__()
        self.frames = []
        self.chunks = 1024
        self.ip = ip
        # if port is not None:
        #     self.port = int(port)
        self.port = port+1
        self.port_1 = port+2
        self.address = (self.ip, self.port)
        self.address_1 = (self.ip, self.port_1)
        self.done = False
        self.next_ = False
        self.Audio = pyaudio.PyAudio()
        self.start_wave()
        

    def start_wave(self):
        self.sock = socket.socket()
        print("binding")
        self.sock.bind(self.address)
        self.recv_msg()

    def recv_msg(self):
        self.sock.settimeout(3)
        print("Listening at {}".format(self.address))
        try:
            self.sock.listen(5)
        except:
            self.next_ = False
        else: self.next_ = True
    
        if self.next_:
            try:
                conn1, addr = self.sock.accept()
                data = conn1.recv(12)
                print("receiving ")
                if data:
                    addr1 = conn1.getpeername()
                    print(f"Connected to : {addr1}")
                    print("closing socket1")
                    conn1.close()
                    self.sock.close()
                    self.running_data(data)
            except Exception as e:
                print(e)

    def running_data(self, data):
        if data:
            data = struct.unpack(">iii", data)
            print(f"Pyaudio format: {data[0]}")
            print(f"Pyaudio sample rate: {data[1]}")
            print(f"Pyaudio channel: {data[2]}")
            data_1 = data[0]
            data_2 = data[1]
            data_3 = data[2]
            self.chn = data_3
            if data_1 and data_2 and data_3:

                self.stream = self.Audio.open(format=data_1,
                                              channels=data_3,
                                              rate=data_2,
                                              output=True)
                udpThread = Thread(target=self.udpStream, daemon=True)
                AudioThread = Thread(target=self.play, daemon=True)
                print("starting all")
                udpThread.start()
                AudioThread.start()
                udpThread.join()
                AudioThread.join()
            else:
                print("Invalid Data! ")

    def udpStream(self):
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp.bind(self.address_1)
        print("done binding udp")
        print("binding @: ", self.address_1)
        while True:
            try:
                udp.settimeout(5)
                soundData, addr = udp.recvfrom(self.chunks * self.chn * 2)
                if soundData is not b"":
                    self.frames.append(soundData)
                else:
                    print("not the data")
            except Exception as e:
                print("error: " + str(e))
                self.done = True
                break
        print("closing socket2")
        udp.close()

    def play(self):
        while True:
            if len(self.frames) == 0 and self.done:
                time.sleep(5)
                self.stream.stop_stream()
                if self.stream.is_stopped():
                    break
            if len(self.frames) > 0:
                while True:
                    try:
                        self.stream.write(self.frames.pop(0))
                    except:
                        break
        print("closing streaming")
        self.stream.close()
        self.Audio.terminate()
        change_text.set("Standby Mode")



class Server_hourbell(object):
    def __init__(self, ip, port):
        super(Server_hourbell, self).__init__()
        self.frames = []
        self.chunks = 1024
        self.ip = ip
        # if port is not None:
        #     self.port = int(port)
        self.port = port+1
        self.port_1 = port+2
        self.address = (self.ip, self.port)
        self.address_1 = (self.ip, self.port_1)
        self.done = False
        self.Audio = pyaudio.PyAudio()
        self.start_wave()
        self.next_ = False

    def start_wave(self):
        self.sock = socket.socket()
        print("binding")
        self.sock.bind(self.address)
        self.recv_msg()

    def recv_msg(self):
        self.sock.settimeout(3)
        print("Listening at {}".format(self.address))
        try:
            self.sock.listen(5)
        except:
            self.next_ = False
        else: self.next_ = True
    
        if self.next_:
            try:
                conn1, addr = self.sock.accept()
                data = conn1.recv(12)
                print("receiving ")
                if data:
                    addr1 = conn1.getpeername()
                    print(f"Connected to : {addr1}")
                    print("closing socket1")
                    conn1.close()
                    self.sock.close()
                    self.running_data(data)
            except Exception as e:
                print(e)

    def running_data(self, data):
        if data:
            data = struct.unpack(">iii", data)
            print(f"Pyaudio format: {data[0]}")
            print(f"Pyaudio sample rate: {data[1]}")
            print(f"Pyaudio channel: {data[2]}")
            data_1 = data[0]
            data_2 = data[1]
            data_3 = data[2]
            self.chn = data_3
            if data_1 and data_2 and data_3:

                self.stream = self.Audio.open(format=data_1,
                                              channels=data_3,
                                              rate=data_2,
                                              output=True)
                udpThread = Thread(target=self.udpStream, daemon=True)
                AudioThread = Thread(target=self.play, daemon=True)
                print("starting all")
                udpThread.start()
                AudioThread.start()
                udpThread.join()
                AudioThread.join()
            else:
                print("Invalid Data! ")

    def udpStream(self):
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp.bind(self.address_1)
        print("done binding udp")
        print("binding @: ", self.address_1)
        while True:
            try:
                udp.settimeout(5)
                soundData, addr = udp.recvfrom(self.chunks * self.chn * 2)
                if soundData is not b"":
                    self.frames.append(soundData)
                else:
                    print("not the data")
            except Exception as e:
                print("error: " + str(e))
                self.done = True
                break
        print("closing socket2")
        udp.close()

    def play(self):
        while True:
            if len(self.frames) == 0 and self.done:
                time.sleep(5)
                self.stream.stop_stream()
                if self.stream.is_stopped():
                    break
            if len(self.frames) > 0:
                while True:
                    try:
                        self.stream.write(self.frames.pop(0))
                    except:
                        break
        print("closing streaming")
        self.stream.close()
        self.Audio.terminate()
        change_text.set("Standby Mode")


if __name__ == "__main__":
    root = tk.Tk()
    ip_addr = tk.StringVar(root)
    port_addr = tk.IntVar(root)
    bind_0 = tk.StringVar(root)
    ip_0 = tk.StringVar(root)
    port_0 = tk.StringVar(root)
    change_text = tk.StringVar(root)
    change_text_1 = tk.StringVar(root)
    root.title('Wi-Fi Receiver')
    app = MainWindow(root)
    root.mainloop()
