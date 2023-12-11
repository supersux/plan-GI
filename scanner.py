import re
import time

import helper
import packager

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
# 粉球
POS_ACQUAINT = (87, 568)
# 蓝球
POS_INTERTWINED = (87, 568)
# 名称匹配
RECT_ID_MATCH = (140, 32, 490, 120)
# 详细信息匹配
RECT_CHARACTER_DETAIL = (1450, 142, 1837, 620)
# 详细信息区域
RECT_WEAPON_DETAIL = (1450, 142, 1837, 493)
# 天赋详细信息区域
RECT_TALENTS_DETAIL = (1613, 148, 1718, 518)
# 星辉和星尘信息区域
RECT_STAR_DETAIL = (55, 978, 316, 1020)
# 原石信息区域
RECT_PRIMO_DETAIL = (1457, 48, 1792, 98)

# 角色名称图像
IMG_CHARACTER = "./tmp/character.jpg"
# 角色信息图像
IMG_DETAIL = "./tmp/detail.jpg"


def content_ocr(hwnd, x, y, rect, parser):
    # 切换界面
    helper.click(x, y)
    time.sleep(0.8)
    # 区域截图
    helper.screenshot_rect(hwnd, rect, IMG_DETAIL)
    time.sleep(0.1)
    # OCR识别
    return parser.parse(IMG_DETAIL)


def extract_num(item, default):
    dig_group = re.search(r'\d+', item)
    if dig_group and len(dig_group.group()) > 0:
        return int(dig_group.group(0))
    else:
        return default


def limit_floor(num):
    return num // 100 if num > 90 else num


# 扫描器基类
class BaseScanner(object):
    def __init__(self, hwnd, offset_x, offset_y, _on_completed=None):
        self.hwnd = hwnd
        self._on_completed = _on_completed
        self.offset_x = offset_x
        self.offset_y = offset_y

    def scan(self, parser, parent):
        result = content_ocr(self.hwnd, self.offset_x, self.offset_y, RECT_CHARACTER_DETAIL, parser)
        payload = self.gen_payload(result)
        return self.fire(payload, parent)

    def gen_payload(self, result):
        return ""

    def fire(self, payload, parent):
        return parent


# 属性扫描器
class AttrScanner(BaseScanner):
    def __init__(self, hwnd, offset_x, offset_y, _on_completed=None):
        super().__init__(hwnd, offset_x, offset_y, _on_completed)
        self.offset_x = POS_ATTR[0] + offset_x
        self.offset_y = POS_ATTR[1] + offset_y

    def gen_payload(self, result):
        character = {'isTraveler': True}
        for index, item in enumerate(result):
            if index == 0:
                character['name'] = item[1]
                continue
            if isinstance(item[1], str):
                start = item[1].find('Level')
                if start >= 0:
                    character['level'] = limit_floor(extract_num(item[1], 1))
                    continue
                # 判断是否是旅行者
                if item[1].find('Friend') >= 0:
                    character['isTraveler'] = False
        return character

    def fire(self, payload, parent):
        payload['parent'] = parent
        # 回调解析结果
        if self._on_completed and callable(self._on_completed):
            self._on_completed(payload, packager.CharacterPackager(parent))
        return packager.query_character_code(payload)


# 天赋扫描器
class WeaponScanner(BaseScanner):
    def __init__(self, hwnd, offset_x, offset_y, _on_completed=None):
        super().__init__(hwnd, offset_x, offset_y, _on_completed)
        self.offset_x = POS_WEAPON[0] + offset_x
        self.offset_y = POS_WEAPON[1] + offset_y

    def gen_payload(self, result):
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
                    weapon['level'] = limit_floor(extract_num(item[1], 1))
                    continue
                start = item[1].find('Rank')
                if start >= 0:
                    weapon['rank'] = limit_floor(extract_num(item[1], 1))
        return weapon

    def fire(self, payload, parent):
        if self._on_completed and callable(self._on_completed):
            self._on_completed(payload, packager.WeaponPackager(parent))


# 命座扫描器
class ConstellationScanner(BaseScanner):
    # 需要图像识别训练
    def scan(self, parser, parent):
        print("命座读取中!")

        # 按下坐标(130,392)
        # 截图读取
        # 塞入对象中
        pass


# 天赋扫描器
class TalentsScanner(BaseScanner):
    def __init__(self, hwnd, offset_x, offset_y, _on_completed=None):
        super().__init__(hwnd, offset_x, offset_y, _on_completed)
        self.offset_x = POS_TALE[0] + offset_x
        self.offset_y = POS_TALE[1] + offset_y

    def gen_payload(self, result):
        talents = []
        # 处理识别结果
        for index, item in enumerate(result):
            start = item[1].find('Lv')
            if start >= 0:
                talents.append(limit_floor(extract_num(item[1], 1)))
        print(talents)

        if len(talents) > 3:
            if talents[3] > talents[2]:
                talents[2] = talents[3]
            while len(talents) > 3:
                talents.pop()

        return talents

    def fire(self, payload, parent):
        # 回调解析结果
        if self._on_completed and callable(self._on_completed):
            self._on_completed(payload, packager.TalentsPackager(parent))
