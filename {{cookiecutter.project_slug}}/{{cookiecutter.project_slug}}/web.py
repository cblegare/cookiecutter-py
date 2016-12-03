#!/usr/bin/python3
# coding: utf8


"""Cookiecutter template tests."""

from flask import Flask


def create_app():
    """Create a new Flask web application and returns it."""
    app = Flask(__name__)
    return app
