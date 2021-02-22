import mouse, keyboard, tkinter, time
from threading import Thread

root = tkinter.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()

class BBBot:
    ativo = False

def main(event):
    if event.name == 'f2':
        BBBot.ativo = not BBBot.ativo
        if(BBBot.ativo):
            print("Bot Ativo!")
        else:
            print("Bot Desativado!")
        thread = Thread(target=work, args=())
        thread.start()

# 1920x1080 tested on
def work():
    keyboard.send('f5')
    time.sleep(2)
    mouse.wheel(-100);
    time.sleep(.5)
    mouse.move(width / 2, height - (height * .25))
    mouse.click()
    time.sleep(.5)
    mouse.move(width / 2, height - (height * .12))
    mouse.click()
    # if not captcha
    mouse.move(width / 2, height - (height * .62))
    time.sleep(2)
    mouse.click()
    if(BBBot.ativo):
        work()

keyboard.on_release(main)

x = 0

while True:
    x += 1