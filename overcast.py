import sys
import requests
import click
from bs4 import BeautifulSoup

import settings


@click.group()
def cli():
    pass


@click.command()
def login(username, password):
    r = requests.post('https://overcast.fm/login', headers={
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Cookie': 'o=%s' % settings.OVERCAST_COOKIE
    })



@click.command()
def episodes(itunes_id):
    r = requests.get('https://overcast.fm/itunes%s' % itunes_id, headers={
        'Cookie': 'o=%s' % settings.OVERCAST_COOKIE
    })

    epidex = BeautifulSoup(r.text, 'lxml')
    print(epidex)
    for tag in epidex.find_all('h2'):
        print(tag)


@click.command()
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

    return podcasts


if __name__ == '__main__':
    cli()
