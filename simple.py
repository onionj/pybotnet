from pybotnet import TelegramProxyEngine

engine_1 = TelegramProxyEngine(TOKEN="adscajkdfvbeb4uv", CHAT_ID="165161")
engine_2 = TelegramProxyEngine(TOKEN="ss")

print(id(engine_1), engine_1)
print(id(engine_2), engine_2)
