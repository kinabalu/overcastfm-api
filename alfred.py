import overcast
import json
import argparse


def episode(episode_id):
    episode = overcast.episode(episode_id)

    items = []

    item = {
        'title': episode['episode_title'],
        'subtitle': episode['episode_date'],
        'text': {
            "copy": """
- Show:: %s
- Speaker(s)::
- Topic::
- Tags:: #podcast
- Overcast URL:: https://overcast.fm/%s
- URL:: %s
- Timestamps:: 
- Summary::
""" % (episode['episode_title'], episode_id, episode['episode_website'],)
        },
        'valid': True
    }

    items.append(item)

    print(json.dumps({"items": items}))


def episodes(show_url):
    episodes = overcast.episodes(show_url)

    items = []

    for episode in episodes['episodes']:
        item = {
            'title': episode['title'],
            'arg': episode['link'],
            'subtitle': episode['description'],
            'valid': True
        }

        items.append(item)

    print(json.dumps({"items": items}))


def podcasts():
    podcasts = overcast.podcasts()

    items = []

    for podcast in podcasts:
        item = {
            'title': podcast['title'],
            'arg': podcast['href'],
            'valid': True
        }

        items.append(item)

    print(json.dumps({"items": items}))


def main():
    parser = argparse.ArgumentParser(
        description="Alfred"
    )
    parser.add_argument('command', nargs='?', help='initial command')
    parser.add_argument('--show_url', type=str)
    parser.add_argument('--episode_id', type=str)
    args = parser.parse_args()

    if args.command == 'podcasts':
        podcasts()
    elif args.command == 'episodes':
        episodes(args.show_url)
    elif args.command == 'episode':
        episode(args.episode_id)


if __name__ == '__main__':
    main()
