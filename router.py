import helper

# 路由字典
character_router_dict = {}
weapon_router_dict = {}

# 固定信息字典
character_origin_dict = {}
weapon_origin_dict = {}


def gen_code_dict(src, des_router, des_origin):
    content = helper.read_from_json(src)

    for key, value in content.items():
        des_router[value['route']] = key
        des_origin[key] = value


def init():
    # 创建角色相关字典
    gen_code_dict('./src/character.json', character_router_dict, character_origin_dict)
    # 创建武器相关字典
    gen_code_dict('./src/weapon.json', weapon_router_dict, weapon_origin_dict)
