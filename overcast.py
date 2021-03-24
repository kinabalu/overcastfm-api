#!/usr/bin/env python3

import sys
import requests
import click
from bs4 import BeautifulSoup, Tag

import settings

import logging

# try:
#     import http.client as http_client
# except ImportError:
#     # Python 2
#     import httplib as http_client
# http_client.HTTPConnection.debuglevel = 1
#
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True


@click.group()
def cli():
    pass


@cli.command()
@click.argument("username")
@click.argument("password")
def login(username, password):
    r = requests.post('https://overcast.fm/login',
                      data={
                          'then': 'podcasts',
                          'email': username,
                          'password': password
                      },
                      allow_redirects=False)

    cookies = dict(r.cookies)
    settings.update_key("OVERCAST_COOKIE", "%s" % cookies['o'])


@cli.command()
@click.argument("show_url")
def episodes(show_url):
    r = requests.get('https://overcast.fm/%s' % show_url, headers={
        'Cookie': 'o=%s' % settings.OVERCAST_COOKIE
    })

    epidex = BeautifulSoup(r.text, 'lxml')
    # print(epidex)

    episodes = []
    for tag in epidex.find_all('h2'):
        if tag['class'] == ['margintop05', 'marginbottom0']:
            for next_epi in tag.next_siblings:
                if isinstance(next_epi, Tag):
                    episode = {}
                    episode_link = next_epi.findAll("a")
                    title_tag = next_epi.findAll("div", {"class": "title singleline"})
                    caption_tag = next_epi.findAll("div", {"class": "caption2 singleline"})
                    description_tag = next_epi.findAll("div", {"class": "lighttext margintop05"})

                    if len(episode_link) == 1:
                        episode['link'] = episode_link[0]['href']
                    if len(title_tag) == 1:
                        episode['title'] = title_tag[0].string.strip()
                    if len(caption_tag) == 1:
                        episode['caption'] = caption_tag[0].string.strip()
                    if len(description_tag) == 1:
                        episode['description'] = description_tag[0].string.strip()
                    episodes.append(episode)
    import pprint
    pprint.pprint(episodes)
    return episodes


@cli.command()
def podcasts():
    r = requests.get('https://overcast.fm/podcasts', headers={
        'Cookie': 'o=%s' % settings.OVERCAST_COOKIE
    })

    overcast_index = BeautifulSoup(r.text, 'lxml')

    podcasts = []
    podcast_count = 0
    for tag in overcast_index.find_all('h2'):
        if tag.text == 'Podcasts':
            for next_podcast in tag.next_siblings:
                if next_podcast.name != 'h2' and next_podcast.name is not None:
                    podcast = {}
                    podcast_count += 1
                    podcast_href = next_podcast['href']

                    podcast['href'] = podcast_href

                    art_img = next_podcast.findAll("img")
                    title_tag = next_podcast.findAll("div", {"class": "title"})

                    podcast['art'] = art_img[0]['src']
                    podcast['title'] = title_tag[0].string

                    podcasts.append(podcast)

    import pprint
    pprint.pprint(podcasts)
    return podcasts


if __name__ == '__main__':
    cli()
