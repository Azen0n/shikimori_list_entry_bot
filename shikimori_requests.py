from requests_cache import CachedSession

from utils import validate_response, get_environment_variable

USER_AGENT = get_environment_variable('USER_AGENT')
HEADERS = {'User-Agent': USER_AGENT}

ANIME_STATUS_TEXT_RESPONSE = {
    'planned': 'has plans to watch',
    'watching': 'is currently watching',
    'rewatching': 'is currently rewatching',
    'completed': 'has completed',
    'on_hold': 'has shelved',
    'dropped': 'dropped',
}

session = CachedSession('demo_cache', expire_after=600)


def get_user(nickname: str) -> dict:
    """Return Shikimori user by nickname."""
    url = f'https://shikimori.one/api/users/{nickname}'
    response = session.get(url, headers=HEADERS)
    validate_response(response)
    return response.json()


def search_animes(query: str, limit: int = 10) -> list[dict]:
    """Search for animes in Shikimori database.
    Returns list of most popular animes.
    """
    url = (f'https://shikimori.one/api/animes/'
           f'?search={query}/'
           f'&order=popularity'
           f'&limit={limit}')
    response = session.get(url, headers=HEADERS)
    validate_response(response)
    return response.json()


def get_user_anime_list(user_id: int) -> list[dict]:
    """Return list of Shikimori user's anime list."""
    url = (f'https://shikimori.one/api/v2/user_rates'
           f'?user_id={user_id}'
           f'&target_type=Anime')
    response = session.get(url, headers=HEADERS)
    validate_response(response)
    return response.json()


def check_anime_entry_in_user_list(user: dict, anime: dict) -> str:
    """Check for anime entry in user's list. If found,
    returns str with current status and score.
    """
    user_anime_list = get_user_anime_list(user_id=user['id'])
    for anime_entry in user_anime_list:
        if anime_entry['target_id'] == anime['id']:
            score = anime_entry['score']
            return (
                f'{user["nickname"]}'
                f' {ANIME_STATUS_TEXT_RESPONSE[anime_entry["status"]]}'
                f' [{anime["name"]}](https://shikimori.one/{anime["url"]})'
                f'{f" with score {score}" if score != 0 else ""}.'
            )
    return (f'Looks like {user["nickname"]} doesn\'t have '
            f'[{anime["name"]}](https://shikimori.one/{anime["url"]}) in their list.')
