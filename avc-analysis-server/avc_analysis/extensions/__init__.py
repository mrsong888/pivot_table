"""Extensions registry

All extensions here are used as singletons and
initialized in application factory
"""
from .datablock import DataBlockApi, ReportAip
from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext
from flask_jwt_simple import JWTManager
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
jwt = JWTManager()
ma = Marshmallow()
pwd_context = CryptContext(schemes=['pbkdf2_sha256'], deprecated='auto')
block = DataBlockApi()
report = ReportAip()
