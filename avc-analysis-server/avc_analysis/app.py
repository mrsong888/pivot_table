from flask import Flask
import os
from avc_analysis import api
from avc_analysis.extensions import db, jwt, block, report
from flask_cors import CORS


import pandas as pd

from config.default import Config
from config.prod import ProdConfig
from config.stage import StageConfig



def create_app(config=None, testing=False):
    # type: (object, object) -> object
    """Application factory, used to create application
    """
    app = Flask('avc_analysis')
    CORS(app)
    df = pd.date_range('20171201', periods=6)

    configure_app(app)
    configure_extensions(app)
    register_blueprints(app)

    return app

def configure_app(app, testing=False):
    """set configuration for application
    """
    app.config.from_object(Config)

    # support DEV STAGE PROD CUSTOM
    profile = (os.getenv('PROFILE') or 'DEV')

    if profile == 'DEV':
        from config.dev import DevConfig
        app.config.from_object(DevConfig)

    if profile == 'STAGE':
        app.config.from_object(StageConfig)

    if profile == 'PROD':
        app.config.from_object(ProdConfig)

    if profile == 'CUSTOM':
        app.config.from_envvar("AVC_ANALYSIS_CONFIG", silent=True)



def configure_extensions(app):
    """configure flask extensions
    """
    db.init_app(app)
    jwt.init_app(app)
    block.init_app(app)
    report.init_app(app)

def register_blueprints(app):
    """register all blueprints for application
    """
    app.register_blueprint(api.views.blueprint)

