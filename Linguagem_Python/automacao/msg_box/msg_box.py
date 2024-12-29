#import pymsgbox
import pyautogui
'''
https://pyautogui.readthedocs.io/en/latest/msgbox.html
'''

'''
pymsgbox.alert(text='text', title='title', button='OK')
pymsgbox.confirm(text='text', title='title', buttons=['OK', 'Cancel'])
pymsgbox.prompt(text='text', title='title' , default='')
pymsgbox.password(text='text', title='title', default='', mask='*')
'''
alert = pyautogui.alert(text='text', title='title', button='OK')
confirm = pyautogui.confirm(text='text', title='title', buttons=['OK', 'Cancel'])
prompt = pyautogui.prompt(text='text', title='title' , default='')
password = pyautogui.password(text='text', title='title', default='', mask='*')