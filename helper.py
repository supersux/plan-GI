import pyautogui
import win32con
import win32gui
import win32ui


# 指定区域截图
def screenshot(hwnd, left=0, top=0, right=0, bottom=0, file="test"):
    if hwnd == 0 or right <= left or bottom <= top:
        pass
    # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    width = right - left
    height = bottom - top
    hWndDC = win32gui.GetWindowDC(hwnd)
    # 创建设备描述表
    mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    # 创建内存设备描述表
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建位图对象准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 为bitmap开辟存储空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    # 将截图保存到saveBitMap中
    saveDC.SelectObject(saveBitMap)
    # 保存bitmap到内存设备描述表
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (left, top), win32con.SRCCOPY)
    # 输出到文件
    saveBitMap.SaveBitmapFile(saveDC, file)
    # 释放内存
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hWndDC)


def screenshot_rect(hwnd, rect=(0, 0, 0, 0), file="test"):
    screenshot(hwnd, rect[0], rect[1], rect[2], rect[3], file)


# 模拟点击
def click(pos_x, pos_y):
    pyautogui.click(pos_x, pos_y)


# 模拟坐标点击
def click_pos(pos):
    pyautogui.click(pos[0], pos[1])


# 模拟按键
def press(key):
    pyautogui.press(key)
