import click
from flask.cli import FlaskGroup
from flask_migrate import MigrateCommand

from avc_analysis.app import create_app


def create_avc_analysis(info):
    return create_app()


@click.group(cls=FlaskGroup, create_app=create_avc_analysis)
def cli():
    """Main entry point"""


@cli.command("init")
def init():
    """Init application, create database tables
    and create a new user named admin with password admin
    """
    from avc_analysis.extensions import db
    click.echo("create database")
    db.create_all()
    click.echo("done")

    click.echo("create user")
    db.session.commit()
    click.echo("created user admin")


@cli.command()
def db():
    """Flask-migrate integration"""
    MigrateCommand()


if __name__ == "__main__":
    cli()
