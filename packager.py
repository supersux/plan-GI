# 数据处理中心，将扫描结果进行归纳整理
import router

CHARACTER_TRAVELER = '10000007'
CHARACTER_WANDERER = '10000075'

CHARACTER_KEY_WEAPON = 'weapon'
CHARACTER_KEY_TALENTS = 'talents'


def query_character_code(src):
    name = src['name']
    # 读取角色编码
    if name in router.character_router_dict.keys():
        return router.character_router_dict[name]
    else:
        # 旅行者和流浪者的特殊处理
        return CHARACTER_TRAVELER if src['isTraveler'] else CHARACTER_WANDERER


class BasePackager:
    def __init__(self, parent):
        self.parent = parent

    def package(self, src, des):
        pass


class CharacterPackager(BasePackager):
    def package(self, src, des):
        code = query_character_code(src)
        if code in des.keys():
            des.update((code, src))
        else:
            des[code] = src
        des[code]['sid'] = code


class WeaponPackager(BasePackager):
    def package(self, src, des):
        name = src['name']
        # 读取武器编码
        if name in router.weapon_router_dict.keys():
            code = router.weapon_router_dict[name]
            src['sid'] = code
        # 将weapon信息写入character
        if CHARACTER_KEY_WEAPON in des[self.parent].keys():
            des.update((CHARACTER_KEY_WEAPON, src))
        else:
            des[self.parent][CHARACTER_KEY_WEAPON] = src


class TalentsPackager(BasePackager):
    def package(self, src, des):
        # 将天赋信息写入character
        if CHARACTER_KEY_TALENTS in des[self.parent].keys():
            des.update((CHARACTER_KEY_TALENTS, src))
        else:
            des[self.parent][CHARACTER_KEY_TALENTS] = src


def gen_character_code(src):
    name = src['name']
    if name in router.character_router_dict.keys():
        return router.character_router_dict[name]
    else:
        # 旅行者和流浪者的特殊处理
        return CHARACTER_TRAVELER if src['isTraveler'] else CHARACTER_WANDERER
