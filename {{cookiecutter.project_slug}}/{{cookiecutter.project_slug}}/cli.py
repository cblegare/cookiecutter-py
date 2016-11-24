#!/usr/bin/python3
# coding: utf8


"""Command line interface for {{ cookiecutter.project_name }}."""


import click

from {% if cookiecutter.namespace %}{{ cookiecutter.namespace }}.{{ cookiecutter.project_slug }}{% else %}{{ cookiecutter.project_slug }}{% endif %} import __project__, __version__, greetings


@click.group(__project__)
@click.version_option(version=__version__)
def main():
    """Console script for {% if cookiecutter.namespace %}{{ cookiecutter.namespace }}.{{ cookiecutter.project_slug }}{% else %}{{ cookiecutter.project_slug }}{% endif %}."""
    click.echo("Replace this message by putting your code into "
               "{{cookiecutter.project_slug}}.__main__.main")
    click.echo("See click documentation at http://click.pocoo.org/")


@main.command()
@click.argument("name", default="World")
@click.option("--formal", is_flag=True, default=False)
@click.option("--slang", is_flag=True, default=False)
def greet(name, formal, slang):
    """Command line greeter."""
    if formal:
        click.echo(greetings.Formal(name))
    elif slang:
        click.echo(greetings.Slang(name))
    else:
        click.echo(greetings.Greetings(name))


if __name__ == "__main__":
    main(prog_name=__project__)
