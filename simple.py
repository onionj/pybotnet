from pybotnet import TelegramProxyEngine

engine_1 = TelegramProxyEngine(TOKEN="test", CHAT_ID="test")
engine_2 = TelegramProxyEngine(TOKEN="test", CHAT_ID="test")

print(id(engine_1), id(engine_2))
