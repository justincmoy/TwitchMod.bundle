TWITCH_CLIENT_ID = 'r797t9e3qhgxayiisuqdxxkh5tj7mlz'

GAMES_ID_URL = 'https://api.twitch.tv/helix/games?id={}'
STREAMS_UID_URL = 'https://api.twitch.tv/helix/streams?user_id={}'
USERS_ID_URL = 'https://api.twitch.tv/helix/users?id={}'
USERS_LOGIN_URL = 'https://api.twitch.tv/helix/users?login={}'

class APIError(Exception):
    pass

# TODO: handle pagination for all of the below gets
def get_games_by_ids(ids):
    url = GAMES_ID_URL.format('&id='.join(ids))

    try:
        data = JSON.ObjectFromURL(url, cacheTime=CACHE_1MINUTE, headers={'Client-ID': TWITCH_CLIENT_ID})
    except Exception as e:
        Log.Error('TWITCH: API request failed. {} - {}'.format(e.message, e.args))
        raise APIError(str(e))

    games = {}
    for game in data['data']:
        games[game['id']] = game
    return games

def get_userid_by_name(name):
    url = USERS_LOGIN_URL.format(name)

    try:
        data = JSON.ObjectFromURL(url, cacheTime=CACHE_1MINUTE, headers={'Client-ID': TWITCH_CLIENT_ID})
        return data['data'][0]['id']
    except APIError:
        return error_message(oc.title2, "Error")

def get_users_by_ids(ids):
    url = USERS_ID_URL.format('&id='.join(ids))

    try:
        data = JSON.ObjectFromURL(url, cacheTime=CACHE_1MINUTE, headers={'Client-ID': TWITCH_CLIENT_ID})
    except Exception as e:
        Log.Error('TWITCH: API request failed. {} - {}'.format(e.message, e.args))
        raise APIError(str(e))

    users = {}
    for user in data['data']:
        users[user['id']] = user
    return users

def get_streams_by_userids(user_ids):
    url = STREAMS_UID_URL.format('&user_id='.join(user_ids))

    try:
        data = JSON.ObjectFromURL(url, cacheTime=CACHE_1MINUTE, headers={'Client-ID': TWITCH_CLIENT_ID})
    except Exception as e:
        Log.Error('TWITCH: API request failed. {} - {}'.format(e.message, e.args))
        raise APIError(str(e))

    return data
