"""Модуль для считывания .env"""

from envparse import Env

env = Env()
env.read_envfile(path=".env")

OPENAI_TOKEN = env.str("OPENAI_TOKEN")
OPENAI_MODEL = env.str("OPENAI_MODEL")
