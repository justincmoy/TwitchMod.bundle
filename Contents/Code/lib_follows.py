from lib_common import TWITCH_CLIENT_ID
from lib_common import APIError
from lib_common import get_games_by_ids, get_streams_by_userids, get_userid_by_name, get_users_by_ids

FOLLOWS_URL = 'https://api.twitch.tv/helix/users/follows?from_id={}'

def get_follows(oc):
    data = get_follows_data()
    follows_user_ids = [ x['to_id'] for x in data['data'] ]

    users = get_users_by_ids(follows_user_ids)
    streams_data = get_streams_by_userids(follows_user_ids)

    game_ids = [ x['game_id'] for x in streams_data['data'] ]
    games = get_games_by_ids(game_ids)

    # display streams by viewer count, remove from users dict
    from __init__ import ChannelMenu

    for stream in sorted(streams_data['data'], key=lambda k: k['viewer_count'], reverse=True):
        stream['user'] = users.pop(stream['user_id'])
        stream['game'] = games[stream['game_id']]
        oc.add(DirectoryObject(
            key=Callback(ChannelMenu, channel_name=stream['user']['display_name'], stream=stream),
            title=unicode(L('{}: {}'.format(stream['user']['display_name'], stream['game']['name']))),
            thumb=Resource.ContentsOfURLWithFallback(
                stream['thumbnail_url'].format(width=320, height=180), fallback=R('icon-default.png')
            )
        ))

    # display offline users by view count
    for _, user in sorted(users.items(), key=lambda k: k[1]['view_count'], reverse=True):
        stream['user'] = user
        oc.add(DirectoryObject(
            key=Callback(ChannelMenu, channel_name=stream['user']['display_name']),
            title=unicode(L(user['display_name'])),
            thumb=Resource.ContentsOfURLWithFallback(
                user['profile_image_url'], fallback=R('icon-default.png')
            )
        ))
    return data

def get_follows_data():
    user_id = get_userid_by_name(Prefs['username'])
    url = FOLLOWS_URL.format(user_id)

    try:
        data = JSON.ObjectFromURL(url, cacheTime=CACHE_1MINUTE, headers={'Client-ID': TWITCH_CLIENT_ID})
    except Exception as e:
        Log.Error('TWITCH: API request failed. {} - {}'.format(e.message, e.args))
        raise APIError(str(e))

    return data
