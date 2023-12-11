import helper

CHARACTER_TRAVELER = '10000007'
CHARACTER_WANDERER = '10000075'

# {'name':'code'}
character_router_dict = {}
# {'code':'name'}
character_reverse_router_dict = {}
weapon_router_dict = {}

# 固定信息字典
character_origin_dict = {}
weapon_origin_dict = {}


def init():
    # 创建角色相关字典
    gen_code_dict('assets/character.json', character_router_dict, character_origin_dict)
    character_reverse_router_dict.update(dict(zip(character_router_dict.values(), character_router_dict.keys())))
    # 创建武器相关字典
    gen_code_dict('assets/weapon.json', weapon_router_dict, weapon_origin_dict)


def gen_code_dict(src, des_router, des_origin):
    content = helper.read_from_json(src)

    for key, value in content.items():
        des_router[value['route']] = key
        des_origin[key] = value


def query_character_code(src):
    name = src['name']
    # 读取角色编码
    if name in character_router_dict.keys():
        return character_router_dict[name]
    else:
        # 旅行者和流浪者的特殊处理
        return CHARACTER_TRAVELER if src['isTraveler'] else CHARACTER_WANDERER
