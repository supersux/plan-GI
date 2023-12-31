# 内容执行器，执行的内容在这里编写
import win32gui

import helper
import packager
import parser
import router
import scanner

# 翻页坐标
POS_TURN_PAGE = (87, 568)
FILE_CHARACTER = './output/character_user.json'
# 用户信息字典
character_user_dict = {}


# 初始化需要执行的内容
def init():
    router.init()


# 实际需要执行的内容
def execute():
    # 获取原神窗口句柄
    hwnd = win32gui.FindWindow(None, 'Genshin Impact')
    if hwnd == 0:
        print("原神没有启动或者没有将原神调整为英文")
    else:
        # 获取窗口位置
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        # 激活窗口
        win32gui.SetForegroundWindow(hwnd)
        win32gui.SetActiveWindow(hwnd)
        # 回到主界面
        home(((left + right) / 2, (top + bottom) / 2))
        # 打开角色信息界面
        open_character_page()
        # 创建OCR扫描工具
        operator = parser.EasyOCRParser()
        # 执行扫描
        character_scan(hwnd, left, top, operator)
        # 输出到文件
        out_to_file(FILE_CHARACTER, character_user_dict)


def callback(result, pkg: packager.BasePackager):
    pkg.package(result, character_user_dict)


# 进入角色页面，当前方案是多次ESC之后点击屏幕中心进入主界面，之后再键入C进入角色界面
def home(pos):
    for i in range(0, 2):
        helper.press('esc')
        helper.sleep(0.8)
    helper.click_pos(pos)
    helper.sleep(0.8)


def open_character_page():
    helper.press('c')
    helper.sleep(0.5)


def open_wish_page():
    helper.press('f3')
    helper.sleep(0.5)


def next_character(left, top):
    helper.click(POS_TURN_PAGE[0] + left, POS_TURN_PAGE[1] + top)
    helper.sleep(0.5)


def character_scan(hwnd, left, top, operator):
    loop_list = []
    while True:
        character = do_character_scan(hwnd, left, top, operator)
        print('%s 读取完成...' % router.character_reverse_router_dict[character])
        if character in loop_list:
            break
        loop_list.append(character)
        # 切换到下一个角色
        next_character(left, top)
    loop_list.clear()


def do_character_scan(hwnd, left, top, operator):
    # 角色信息扫描
    sc = scanner.AttrScanner(hwnd, left, top, callback)
    character = sc.scan(operator, 'root')
    # 武器信息扫描
    sc = scanner.WeaponScanner(hwnd, left, top, callback)
    sc.scan(operator, character)
    # 天赋信息扫描
    sc = scanner.TalentsScanner(hwnd, left, top, callback)
    sc.scan(operator, character)
    return character


def out_to_file(path, src_dict):
    helper.out_to_json(path, src_dict)
