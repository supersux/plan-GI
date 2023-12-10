import json

import win32gui

import scanner

# 路由字典
character_router_dict = {}
weapon_router_dict = {}

# 固定值字典
character_outer_dict = {}

# 用户信息字典
character_user_dict = {}


# 读json文件
def read_from_json(file):
    with open(file, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


def gen_code_dict():
    character = read_from_json('./src/character.json')
    for key, value in character.items():
        character_router_dict[value['route']] = key

    weapon = read_from_json('./src/weapon.json')
    for key, value in weapon.items():
        weapon_router_dict[value['route']] = key
    print(weapon_router_dict)

    pass


def test():
    gen_code_dict()
    pass


def execute():
    # 获取窗口句柄
    hwnd = win32gui.FindWindow(None, 'Genshin Impact')
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    # 激活窗口
    win32gui.SetForegroundWindow(hwnd)
    win32gui.SetActiveWindow(hwnd)
    # 进入角色信息界面
    # pyautogui.press('c')
    # 角色信息扫描
    # sc = scanner.AttrScanner(hwnd, left, top, callback)
    # sc.scan()
    # 武器信息扫描
    # sc = scanner.WeaponScanner(hwnd, left, top, callback)
    # sc.scan()

    # 天赋信息扫描
    sc = scanner.TalentsScanner(hwnd, left, top, callback)
    sc.scan()

    # print("executes")

    # 兼容性处理
    # 将扫描结果导出json文件


def callback(result, packager: scanner.BasePackager):
    print("call back")
    print(result)
    packager.do(result, character_user_dict)
