import win32gui

# screenWidth, screenHeight = pyautogui.size()
# #
handler = win32gui.FindWindow(None, 'Genshin Impact')
# win32gui.SetForegroundWindow(handler)
# win32gui.SetActiveWindow(handler)
# pyautogui.press('c')
#
left, top, right, bottom = win32gui.GetWindowRect(handler)


# print(f'w:${offsetX}, h${offsetY}')
# time.sleep(3)
# pyautogui.press('esc')


def mouse_move(x, y):
    """
    鼠标移动事件
    :param x: 横坐标
    :param y: 纵坐标
    :return:
    """
    pass
    # print(f'鼠标移动X,Y:{x},{y}')


def mouse_click(x, y, button, pressed):
    """
    鼠标点击事件
    :param x: 横坐标
    :param y: 纵坐标
    :param button: 按钮枚举对象 Button.left 鼠标左键 Button.right 鼠标右键 Button.middle 鼠标中键
    :param pressed: 按下或者是释放,按下是True释放是False
    :return:
    """
    pass
    if pressed:
        print('按下鼠标')
        print(x - left)
        print(y - top)
    else:
        pass
    print(''.center(20, '*'))


def mouse_scroll(x, y, dx, dy):
    """
    鼠标滚动事件
    :param x: 横坐标
    :param y: 纵坐标
    :param dx:滚轮的横坐标方向的移动量,0未移动,1向前面滚动和-1向后面滚动
    :param dy:滚轮的纵坐标方向的移动量,0未移动,1向前面滚动和-1向后面滚动
    :return:
    """
    pass


from pynput import mouse

# with mouse.Listener(
#         on_move=mouse_move,  # 鼠标移动事件
#         on_click=mouse_click,  # 鼠标点击事件
#         on_scroll=mouse_scroll  # 鼠标滚动事件
# ) as listener:
#     listener.join()


# import time
# import execute
# time.sleep(1)
# execute.screenshot(handler, 1450, 142, 1837, 493, "./tmp/ttt.jpg")
#
# import easyocr
# reader = easyocr.Reader(['en'])
# result = reader.readtext("./tmp/ttt.jpg")
# print(result)


# import gi_scanner as scanner
#
# lisa = scanner.BaseScanner()
# lisa.shit()

import execute

execute.test()
