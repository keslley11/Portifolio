import pyautogui

#mostra posição e cor de on está o mouse

print("Pressione Ctrl-C para Sair:")
try:
    while True:
        x, y = pyautogui.position()
        positionStr = "X: " + str(x).rjust(4) + "Y: " + str(y).rjust(4)
        pixelColor = pyautogui.screenshot().getpixel((x,y))
        positionStr += ' RGB: (' + str(pixelColor[0]).rjust(3)
        positionStr += ',' + str(pixelColor[1]).rjust(3)
        positionStr += ',' + str(pixelColor[2]).rjust(3) + ")"
        print(positionStr, end="")
        print("\b"*len(positionStr), end="", flush=True)

except KeyboardInterrupt:
    print("\nEncerrado!")

    