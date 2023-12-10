import re
import time

import helper as helper

# 属性的坐标
POS_ATTR = (130, 183)
# 武器的坐标
POS_WEAPON = (130, 252)
# 命座的坐标
POS_TELL = (130, 392)
# 天赋的坐标
POS_TALE = (130, 464)
# 翻页坐标
POS_TURN_PAGE = (87, 568)
# 名称匹配
POS_ID_MATCH = (140, 32, 490, 120)
# 详细信息匹配
CHARACTER_DETAIL_RECT = (1450, 142, 1837, 620)
# 详细信息区域
WEAPON_DETAIL_RECT = (1450, 142, 1837, 493)
# 天赋详细信息区域
TALENTS_DETAIL_RECT = (1613, 148, 1718, 518)
# 角色名称图像
IMG_CHARACTER = "./tmp/character.jpg"
# 角色信息图像
IMG_DETAIL = "./tmp/detail.jpg"


def content_ocr(hwnd, pos, rect, parser):
    # 切换界面
    helper.click_pos(pos)
    time.sleep(0.5)
    # 区域截图
    helper.screenshot_rect(hwnd, rect, IMG_DETAIL)
    time.sleep(0.1)
    # OCR识别
    return parser.parse(IMG_DETAIL)


def extract_num(item):
    dig_group = re.search(r'\d+', item)
    if dig_group and len(dig_group.group()) > 0:
        result = int(dig_group.group(0))
        return result // 100 if result > 90 else result
    else:
        return 1


# 扫描器基类
class BaseScanner(object):
    def __init__(self, hwnd, offset_x, offset_y, _on_completed=None):
        self.hwnd = hwnd
        self.offset_x = offset_x
        self.offset_y = offset_y
        self._on_completed = _on_completed

    def scan(self, parser):
        pass


# 属性扫描器
class AttrScanner(BaseScanner):
    def scan(self, parser):
        print("基础属性读取中!")
        pos = (POS_ATTR[0] + self.offset_x, POS_ATTR[1] + self.offset_y)
        result = content_ocr(self.hwnd, pos, CHARACTER_DETAIL_RECT, parser)
        character = {'isTraveler': True}
        # 处理识别结果，这里只解析角色名称以及角色等级
        for index, item in enumerate(result):
            if index == 0:
                character['name'] = item[1]
                continue
            if isinstance(item[1], str):
                start = item[1].find('Level')
                if start >= 0:
                    character['level'] = extract_num(item[1])
                    continue
                # 判断是否是旅行者
                if item[1].find('Friend') >= 0:
                    character['isTraveler'] = False

        # 回调解析结果
        if self._on_completed and callable(self._on_completed):
            self._on_completed(character, CharacterPackager())


# 天赋扫描器
class WeaponScanner(BaseScanner):
    def scan(self, parser):
        print("武器读取中!")
        pos = (POS_WEAPON[0] + self.offset_x, POS_WEAPON[1] + self.offset_y)
        result = content_ocr(self.hwnd, pos, WEAPON_DETAIL_RECT, parser)
        weapon = {}
        # 处理识别结果
        for index, item in enumerate(result):
            if index == 0:
                weapon['name'] = item[1]
                continue
            if index == 1:
                weapon['type'] = item[1]
                continue
            if isinstance(item[1], str):
                start = item[1].find('Lv')
                if start >= 0:
                    weapon['level'] = extract_num(item[1])
                    continue
                start = item[1].find('Rank')
                if start >= 0:
                    weapon['rank'] = extract_num(item[1])
                    continue

                # 回调解析结果
        if self._on_completed and callable(self._on_completed):
            self._on_completed(weapon, WeaponPackager())


# 命座扫描器
class ConstellationScanner(BaseScanner):
    # 需要图像识别训练
    def scan(self, parser):
        print("命座读取中!")

        # 按下坐标(130,392)
        # 截图读取
        # 塞入对象中
        pass


# 天赋扫描器
class TalentsScanner(BaseScanner):
    def scan(self, parser):
        print("天赋读取中!")
        pos = (POS_TALE[0] + self.offset_x, POS_TALE[1] + self.offset_y)
        result = content_ocr(self.hwnd, pos, TALENTS_DETAIL_RECT, parser)
        talents = []
        # 处理识别结果
        for index, item in enumerate(result):
            start = item[1].find('Lv')
            if start >= 0:
                talents.append(extract_num(item[1]))

        if len(talents) == 4:
            talents[2] = max(talents[2], talents[3])
            talents.pop()

        # 回调解析结果
        if self._on_completed and callable(self._on_completed):
            self._on_completed(talents, TalentsPackager())


class BasePackager:
    def do(self, content, destination):
        pass


class CharacterPackager(BasePackager):
    def do(self, content, destination):
        pass


class WeaponPackager(BasePackager):
    def do(self, content, destination):
        pass


class TalentsPackager(BasePackager):
    def do(self, content, destination):
        pass
