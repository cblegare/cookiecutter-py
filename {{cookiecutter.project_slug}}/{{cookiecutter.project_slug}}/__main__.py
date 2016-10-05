#!/usr/bin/python3
# coding: utf8


"""
Cookiecutter template tests
"""


import click


@click.command()
def main(args=None):
    """Console script for {{cookiecutter.project_slug}}"""
    click.echo("Replace this message by putting your code into "
               "{{cookiecutter.project_slug}}.__main__.main")
    click.echo("See click documentation at http://click.pocoo.org/")


if __name__ == "__main__":
    main()
