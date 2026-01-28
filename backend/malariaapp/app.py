from flask import Flask, jsonify, request, make_response
import sqlite3
import datetime

from core import create_app
from seeders import run_all



app = create_app()


@app.cli.command("seed")
def seed():
    run_all()


if __name__ == '__main__':
    app.run(debug=True) 