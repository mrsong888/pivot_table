# !/usr/bin/env python
# *-* coding:utf-8 *-*
from config.default import Config

class DevConfig(Config):
    DEBUG = True
    SECRET_KEY = "changeme"

    SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/avc_analysis.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    JWT_ALGORITHM="RS256"
    JWT_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAmB5q52yH+FQjBzHhPZVf
    tO54ClXBrRx9l/wTj0BW8/M/yLG0/Z4eIghjumHIm+Fe/fdLi4NQgvBRKDkkKS+X
    1KDzso/rl8Kk5dv3tEFHBumhyvp4AB+U3aoNlr+PUXX/A/dl9aLZhygNpeapJatf
    JmvVzGTZBi7DmoUkATPItvklI0IFe3J5ywLvWQunBwNzhnflWq3L99C0Af3NmmAr
    PJ+L4Dhx+b6uEWasDeIB5goZQXUNiCX2VwBP4NrlLLwMukITkmO81dHD8oHnxmtQ
    HUUzX8wh9QNRbQmMI56PpJVSE3xY8X0WPQ5jlRM1NAmvZHB365TjAiZ5pelUJquJ
    zwIDAQAB
    -----END PUBLIC KEY-----
    """
    JWT_DECODE_AUDIENCE="openid"
    DATABLOCK_CLIENT_ID=""
    DATABLOCK_CLIENT_SECRET=""
    DATABLOCK_BASE_URL="http://117.23.4.139:20000"
    DATABLOCK_CACHE_DIR="./cache"
