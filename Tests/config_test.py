from Core.Tools.config import Config

config = Config()
#
# print(type(config.read()), config.read())
#
# print(config.modify(key="a", value=2))
#
# print(type(config.read()), config.read())
#
# print(config.modify(key="b", value=3))

print(f"{config:init}")
print(f"{config:path}")
print(f"{config:config}")
print(config)

