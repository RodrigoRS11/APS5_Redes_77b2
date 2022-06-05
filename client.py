import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
import time

HOST = '127.0.0.1'
PORT = 59000

class Client:
    def enviarLogin(self):

        self.login = str(self.vlogin.get())
        self.senha = str(self.vsenha.get())

        time.sleep(2)

        self.tela1.destroy()

        self.gui()

        rcv = threading.Thread(target=self.receive)
        rcv.start()

    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        self.win = Tk()
        self.win.withdraw()

        self.tela1 = Toplevel()

        self.tela1.title("Login e Cadastro")
        self.tela1.geometry("500x220")
        self.tela1.configure(background="#008")

        self.txt1=Label(self.tela1,
           text="O cadastro será feito automáticamente caso você não o tenha feito antes!",
           background="#ff0",
           foreground="#000")
        self.txt1.place(x=50,
           y=10,
           width=400,
           height=30)

        self.txt2=Label(self.tela1,
           text="Login",
           background="#fffafa",
           foreground="#000000")
        self.txt2.place(x=110,
           y=50,
           width=60,
           height=30)

        self.txt3=Label(self.tela1,
           text="Senha",
           background="#fffafa",
           foreground="#000000")
        self.txt3.place(x=110,
           y=90,
           width=60,
           height=30)

        self.txt4=Label(self.tela1,
           text="------------------------------------------------------------------------",
           background="#ff0",
           foreground="#000")
        self.txt4.place(x=50,
           y=180,
           width=400,
           height=30)

        self.vlogin=Entry(self.tela1)
        self.vlogin.place(x=190,
             y=50,
             width=195,
             height=30)

        self.vsenha=Entry(self.tela1)
        self.vsenha.place(x=190,
             y=90,
             width=195,
             height=30)

        self.btnLogin=Button(self.tela1,
               text="Logar",
                command= self.enviarLogin )
        self.btnLogin.place(x=110,
               y=130,
               width=275,
               height=30)

        self.win.mainloop()


    def gui(self):
        self.win.deiconify()
        self.win.title("CHAT  e  JOGO-DA-VELHA")
        self.win.configure(bg="#008")

        self.chat_label = tkinter.Label(self.win, text="Chat: ", bg="lightgray")
        self.chat_label.config(font=("Arial",12))
        self.chat_label.pack(padx=20, pady=5)

        self.textCons = Text(self.win)
        self.textCons.pack(padx=20,pady=5)

        self.msg_label = tkinter.Label(self.win, text="Message: ", bg="lightgray")
        self.msg_label.config(font=("Arial",12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tkinter.Entry(self.win)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.win, text="Send", command=lambda: self.writeBtn(self.input_area.get()))
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)

        self.textCons.config(state=DISABLED)

    def writeBtn(self, msg):
        self.textCons.config(state=DISABLED)
        self.mssg = msg
        self.input_area.delete(0, END)
        snd = threading.Thread(target=self.sendMessage)
        snd.start()
        
    def receive(self):
        while True:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == 'login?':
                    self.sock.send(self.login.encode('utf-8'))
                if message == 'senha?':
                    self.sock.send(self.senha.encode('utf-8'))
                if message == 'linha?':
                    msg = tkinter.Tk()
                    msg.withdraw()
                    self.linha = simpledialog.askstring("Linha", "Digite a linha ", parent=msg)
                    self.sock.send(self.linha.encode('utf-8'))
                if message == 'coluna?':
                    msg = tkinter.Tk()
                    msg.withdraw()
                    self.coluna = simpledialog.askstring("Coluna", "Digite a coluna ", parent=msg)
                    self.sock.send(self.coluna.encode('utf-8'))
                else:
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END, message)
                    self.textCons.see(END)
            except:
                print("Error")
                self.sock.close()
                break

    def sendMessage(self):
        loop = 0
        self.textCons.config(state=DISABLED)
        while loop == 0:
            if self.mssg == '!jogo':
                message = '!jogo'
                self.sock.send(message.encode('utf-8'))
                loop = 1
                break
            if self.mssg == '0':
                message = '0'
                self.sock.send(message.encode('utf-8'))
                break
            if self.mssg == '1':
                message = '1'
                self.sock.send(message.encode('utf-8'))
                break
            if self.mssg == '2':
                message = '2'
                self.sock.send(message.encode('utf-8'))
                break
            else:
                message = (f'{self.login}: {self.mssg}\n')
                self.sock.send(message.encode('utf-8'))
                break
        
client = Client(HOST, PORT)
        
