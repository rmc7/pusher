# -*- coding: utf-8 -*-
import os
from datetime import timedelta

class Config(object):
    SECRET_KEY = "secret_keys"

    debug = False
    # PERMANENT_SESSION_LIFETIME = timedelta(minutes=2)
# 영구세션을 통해 어느 기간동안 세션이 유지될지 설정함
# timedelta = 마지막 사용시간부터 N분까지 세션 유지
# timedelta(seconds=30) / 보통 1~2일 유지함(days=2)

class Production(Config):
    DEBUG = True
    ADMIN = "wow@wow.com"