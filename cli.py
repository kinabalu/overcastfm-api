#!/usr/bin/env python3

import sys
import requests
import click
from bs4 import BeautifulSoup, Tag

import settings

import pprint

import overcast


@click.group()
def cli():
    pass


@cli.command()
@click.argument("username")
@click.argument("password")
def login(username, password):
    overcast.login(username, password)


@cli.command()
@click.argument("episode_id")
@click.option("-v", "--verbose", is_flag=True)
def episode(episode_id, verbose=False):
    episode = overcast.episode(episode_id)

    if verbose:
        pprint.pprint(episode)


@cli.command()
@click.argument("show_url")
@click.option("-v", "--verbose", is_flag=True)
def episodes(show_url, verbose=False):
    episodes = overcast.episodes(show_url)

    if verbose:
        pprint.pprint(episodes)


@cli.command()
@click.option("-v", "--verbose", is_flag=True)
def podcasts(verbose=False):
    podcasts = overcast.podcasts()

    if verbose:
        pprint.pprint(podcasts)


if __name__ == '__main__':
    cli()
