
import click
from flask import current_app, g
from flask.cli import with_appcontext

import sqlite3

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(add_column_construction_command)

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

@click.command('add-column-construction')
@with_appcontext
def add_column_construction_command():
    """Clear the existing data and create new tables."""
    if 'db' not in g:
        g.db = sqlite3.connect(
            'instance/materialRecorder.sqlite',
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    cursor = g.db.cursor()
    sqlStr = "ALTER TABLE material ADD COLUMN construction TEXT DEFAULT \"\""
    cursor.execute(sqlStr)
    g.db.commit()
    click.echo('Add Column Construction..')

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            'instance/materialRecorder.sqlite',
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

