import requests
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


def episode(episode_id):
    r = requests.get('https://overcast.fm/%s' % episode_id, headers={
        'Cookie': 'o=%s' % settings.OVERCAST_COOKIE
    })

    epidex = BeautifulSoup(r.text, 'lxml')

    episode = {}

    podcast_title_tag = epidex.findAll('h3', {"class": "marginbottom05"})
    podcast_title = podcast_title_tag[0].string if len(podcast_title_tag) == 1 else None
    podcast_link = podcast_title_tag[0].a['href'] if len(podcast_title_tag) == 1 else None

    episode['podcast_title'] = podcast_title
    episode['podcast_link'] = podcast_link

    episode_title_tag = epidex.findAll('h2', {"class": "margintop0 marginbottom0"})
    episode_title = episode_title_tag[0].string if len(episode_title_tag) == 1 else None

    episode['episode_title'] = episode_title

    episode_date_tag = epidex.findAll('div', {"class": "margintop0 lighttext"})
    episode_date = episode_date_tag[0].string.strip() if len(episode_date_tag) == 1 else None

    episode['episode_date'] = episode_date

    podcast_art_tag = epidex.findAll('img', {"class": "art fullart"})
    podcast_art = podcast_art_tag[0]['src'] if len(podcast_art_tag) == 1 else None

    episode['podcast_art'] = podcast_art

    episode_website_tag = epidex.findAll('div', {"class": "centertext lighttext margintop1"})
    episode_website = None

    if len(episode_website_tag) == 1:
        for link in episode_website_tag[0]:
            if link.string == 'Website':
                episode_website = link['href']


    episode['episode_website'] = episode_website

    return episode


def episodes(show_url):
    """
    Get all episodes for a given show URL

    TODO need to grab the episode URL and add to the episode object

    :param show_url: a show url in the form /itunes<itunes_id>/<title>
    :param verbose: should we print some stuff?
    :return: a podcast object which contains the title, art, description and episodes list
    """
    r = requests.get('https://overcast.fm/%s' % show_url, headers={
        'Cookie': 'o=%s' % settings.OVERCAST_COOKIE
    })

    epidex = BeautifulSoup(r.text, 'lxml')

    podcast = {}

    podcast_title_tag = epidex.findAll('h2', {"class": "centertext"})
    podcast_title = podcast_title_tag[0].string if len(podcast_title_tag) == 1 else None

    podcast_art_tag = epidex.findAll("img", {"class": "art fullart"})
    podcast_art = podcast_art_tag[0]['src'] if len(podcast_art_tag) == 1 else None

    podcast_desc_tag = epidex.findAll('div', {"class": "margintop1 marginbottom1 lighttext"})
    podcast_desc = podcast_desc_tag[0].string.strip() if len(podcast_desc_tag) == 1 else None

    podcast['art'] = podcast_art
    podcast['title'] = podcast_title
    podcast['description'] = podcast_desc

    episodes = []

    podcast['episodes'] = episodes
    for tag in epidex.find_all('h2'):
        if tag['class'] == ['margintop05', 'marginbottom0']:
            for next_epi in tag.next_siblings:
                if isinstance(next_epi, Tag):
                    episode = {}

                    if 'href' in next_epi.attrs:
                        episode['link'] = next_epi.attrs['href'][1:]

                    title_tag = next_epi.findAll("div", {"class": "title singleline"})
                    caption_tag = next_epi.findAll("div", {"class": "caption2 singleline"})
                    description_tag = next_epi.findAll("div", {"class": "lighttext margintop05"})

                    if len(title_tag) == 1:
                        episode['title'] = title_tag[0].string.strip()
                    if len(caption_tag) == 1:
                        episode['caption'] = caption_tag[0].string.strip()
                    if len(description_tag) == 1:
                        episode['description'] = description_tag[0].string.strip()

                    if episode:
                        episodes.append(episode)

    return podcast


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

                    podcast['href'] = podcast_href[1:]

                    if podcast['href'] == 'uploads':
                        continue

                    art_img = next_podcast.findAll("img")
                    title_tag = next_podcast.findAll("div", {"class": "title"})

                    podcast['art'] = art_img[0]['src']
                    podcast['title'] = title_tag[0].string

                    podcasts.append(podcast)

    return podcasts
