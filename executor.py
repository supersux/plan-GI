import json

import win32gui

import parser
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


def gen_code_dict(src, des):
    content = read_from_json(src)
    for key, value in content.items():
        des[value['route']] = key


# 创建名称和武器路由字典
def init():
    gen_code_dict('./src/character.json', character_router_dict)
    gen_code_dict('./src/weapon.json', weapon_router_dict)


def execute():
    # 获取窗口句柄
    hwnd = win32gui.FindWindow(None, 'Genshin Impact')
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    # 激活窗口
    win32gui.SetForegroundWindow(hwnd)
    win32gui.SetActiveWindow(hwnd)
    # 创建OCR扫描工具
    operator = parser.EasyOCRParser()
    # 进入角色信息界面
    # helper.press('c')
    character_scan(hwnd, left, top, operator)

    # print("executes")

    # 兼容性处理
    # 将扫描结果导出json文件


def character_scan(hwnd, left, top, op):
    # 角色信息扫描
    sc = scanner.AttrScanner(hwnd, left, top, callback)
    sc.scan(op)
    # 武器信息扫描
    sc = scanner.WeaponScanner(hwnd, left, top, callback)
    sc.scan(op)
    # 天赋信息扫描
    sc = scanner.TalentsScanner(hwnd, left, top, callback)
    sc.scan(op)


def callback(result, packager: scanner.BasePackager):
    print("call back")
    print(result)
    packager.do(result, character_user_dict)
