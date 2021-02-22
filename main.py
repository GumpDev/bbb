import sys
from tkinter import simpledialog
from tkinter.constants import DISABLED
import mouse, keyboard, tkinter, tkinter.commondialog, time, os, datetime, pyscreenshot, tkinter.messagebox
from threading import Thread
from sys import platform
import clipboard
from PIL import Image 

root = tkinter.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
monitores = 1

class BBBot:
    ativo = False
    internetSpeed = 2
    tries = 0
    sucess = 0
    thread = Thread()
    iniciado = False
    needConfig = True
    pos = []
    step = 0
    def updateTries():
        if(not BBBot.iniciado):
            BBBot.TT = tkinter.Text(root,background='black', fg='white')
            BBBot.TT.insert(1.0, "Tentativas: {}\nAcertos: {}".format(BBBot.tries,BBBot.sucess))
            BBBot.TT.pack()
            BBBot.iniciado = True
        else: 
            BBBot.TT.delete(1.0, "end")
            BBBot.TT.insert(1.0, "Tentativas: {}\nAcertos: {}".format(BBBot.tries,BBBot.sucess))

BBBot.updateTries()

T = tkinter.Text(root,background='black', fg='white')
T.pack()
T.insert(tkinter.END, "=============================\nBem-vindo ao bot de\nvotação da Karol Conká no BBB\n=============================\nAbra a página de votação do bbb, deixe em tela cheia no seu monitor principal e utilize 'f2' para ativar/desativar o bot")

def mouseClickLinux(mouseBtn):
    os.system("xdotool click {}".format(mouseBtn))

def config():
    if BBBot.step == 0:
        tkinter.messagebox.showinfo(title="Calibrando", message="Precisamos calibrar antes de começar!\n abra o site de votação do bbb e aperte 'f4'")
    elif BBBot.step == 1:
        scroll()
        tkinter.messagebox.showinfo(title="Calibrando", message="Coloque seu mouse encima do nome da karol conká e aperte 'f4'")
    elif BBBot.step == 2:
        BBBot.pos.append(mouse.get_position())
        tkinter.messagebox.showinfo(title="Calibrando", message="Coloque seu mouse encima do captcha e aperte 'f4'\nImportante que você não de scroll na página!")
    elif BBBot.step == 3:
        BBBot.pos.append(mouse.get_position())
        tkinter.messagebox.showinfo(title="Calibrando", message="Coloque seu mouse encima da imagem de OK quando você vota na Karol Conká e aperte 'f4'\nse necessario resolva o captcha para ir para página de voto realizado!")
    elif BBBot.step == 4:
        BBBot.pos.append(mouse.get_position())
        tkinter.messagebox.showinfo(title="Calibrado!", message="Calibrado, agora só apertar 'f2' para começar a usar")
        BBBot.needConfig = False

def main(event):
    if event.name == 'f4' and BBBot.needConfig:
        BBBot.step += 1
        config()
    if not BBBot.needConfig and event.name == 'f2':
        BBBot.ativo = not BBBot.ativo
        current_time = datetime.datetime.now() 
        if(BBBot.ativo):
            T.insert(tkinter.END, "\n[{}:{}:{}] Bot Ativo!".format(current_time.hour,current_time.minute,current_time.second))
            BBBot.thread = Thread(target=work, args=())
            BBBot.thread.start()
        else:
            T.insert(tkinter.END, "\n[{}:{}:{}] Bot Desativado!".format(current_time.hour,current_time.minute,current_time.second))

def takeScreenshot():
    image = pyscreenshot.grab() 
    image.save("output.png") 

def scroll():
    if platform == "linux" or platform == "linux2":
        keyboard.send('ctrl+shift+j')
        time.sleep(1)
        clipboard.copy("window.scrollTo(0,1000)")
        keyboard.send('ctrl+v, enter')
        keyboard.send('ctrl+shift+j')      
        time.sleep(.5)
    else:
        mouse.wheel(-100)

# 1920x1080 tested on
def work():
    BBBot.tries += 1
    BBBot.updateTries()
    keyboard.send('f5')
    time.sleep(BBBot.internetSpeed)
    if platform == "linux" or platform == "linux2":
        keyboard.send('ctrl+shift+j')
        scroll()
        mouse.move(BBBot.pos[0][0],BBBot.pos[0][1])
        mouseClickLinux(1)
        time.sleep(.5)
        mouse.move(BBBot.pos[1][0],BBBot.pos[1][1])
        mouseClickLinux(1)
        # if not captcha
        mouse.move(BBBot.pos[2][0],BBBot.pos[2][1])
        time.sleep(BBBot.internetSpeed)
        # mouseClickLinux(1)                     
    else:
        scroll()
        time.sleep(.5)
        mouse.move(BBBot.pos[0][0],BBBot.pos[0][1])
        mouse.click()
        time.sleep(.5)
        mouse.move(BBBot.pos[1][0],BBBot.pos[1][1])
        mouse.click()
        # if not captcha
        mouse.move(BBBot.pos[2][0],BBBot.pos[2][1])
        time.sleep(BBBot.internetSpeed)
        # mouse.click()    
    time.sleep(BBBot.internetSpeed)
    takeScreenshot()
    im = Image.open("output.png")
    cordinate = x, y = mouse.get_position()[0], mouse.get_position()[1]
    if im.getpixel(cordinate) == (0, 0, 0):
        BBBot.sucess += 1
    if(BBBot.ativo):
        work()

keyboard.on_release(main)

def on_closing():
    root.destroy()
    sys.exit()

BBBot.internetSpeed = simpledialog.askfloat("Calibrando", "Qual é o tempo médio para carregar sua página?",
                            parent=root,
                            minvalue=1.0, maxvalue=100000.0)
config()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()