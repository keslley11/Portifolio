import pyautogui
'''
 Windows:
>> pip install pyautogui

IOS:
>> sudo pip3 install pyobjc-framework-Quartz
>> sudo pip3 install pyobjccore
>> sudo pip3 install pyobjc

Linux:
>> sudo pip3 install python3-xlib
>> sudo apt-get install scrot
>> sudo apt-get install python3-tk
>> sudo apt-get install python3-dev
'''



'''
import time
time.sleep(3) #delay para começar o código
'''
#safety
pyautogui.FAILSAFE=True # interrompe programa se o mouse estiver em [0,0] (canto superior esquerdo)
pyautogui.PAUSE=1 # pausa antes de cada comando

#comandos
print(pyautogui.size()) # monitor.

print(pyautogui.position())
'''
mouseNow.py
'''

pyautogui.moveTo(300,780, duration=0.5) 
'''
for i in range(4):
    pyautogui.moveTo(100,100, duration=0)
    pyautogui.moveTo(200,100, duration=0)
    pyautogui.moveTo(200,200, duration=0)
    pyautogui.moveTo(100,200, duration=0)
'''
'''
for i in range(4):
    pyautogui.moveRel(100,0, duration=0)
    pyautogui.moveRel(0,100, duration=0)
    pyautogui.moveRel(-100,0, duration=0)
    pyautogui.moveRel(0,-100, duration=0)
'''

pyautogui.click(1776,18) 
pyautogui.click(1776,18, button="right")#pyautogui.rightClick(1776,18)
pyautogui.click(1776,18, button="center")

pyautogui.dragTo(0, 0, duration=3)  # drag mouse to XY
pyautogui.dragRel(200, 200, duration=3)

pyautogui.mouseDown(1776,18) #segura o click
pyautogui.mouseUp() #solta o click

pyautogui.doubleClick(1776,18)

pyautogui.screenshot('screen.png')
position = list(pyautogui.locateAllOnScreen('locate.png')) #encontrar clicaveis
for item in position:
    print(item)

pyautogui.scroll(-200)

img = pyautogui.screenshot() #print da tela
print(img.getpixel((100,100))) # cor do pixel indicado em RGB
print(pyautogui.pixelMatchesColor(100,100,(0,0,0))) #verifica cor do pixel


pyautogui.click(300,300)
pyautogui.typewrite("      ;;;;;") #digita
pyautogui.typewrite(['a','c','left','b'],0.25) #digita
#print(pyautogui.KEYBOARD_KEYS) #outras opções
'''
>>> pyautogui.KEYBOARD_KEYS
['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', 
'_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', 'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace', 'browserback', 'browserfavorites', 'browserforward', 'browserhome', 'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear', 'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete', 'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20', 'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja', 'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail', 'launchmediaselect', 
'left', 'modechange', 'multiply', 'nexttrack', 'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn', 'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn', 'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator', 'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 
'tab', 'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen', 'command', 'option', 'optionleft', 'optionright']
'''

pyautogui.keyDown('shift') #segura
pyautogui.press('4')
pyautogui.keyUp('shift')
#pyautogui.hotkey('shift','4')

with pyautogui.hold('shift'):
    pyautogui.press(['left', 'left', 'left', 'left'])


