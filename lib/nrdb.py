import requests

NRDB_BASE_URL = "https://netrunnerdb.com/api/2.0"


def query_nrdb(endpoint):
    url = NRDB_BASE_URL + endpoint
    response = requests.get(url).json()
    if not response['success']:
        raise RuntimeError(f"Failed to get {url}")
    return response['data']


def get_deck(deck_id):
    return query_nrdb('/public/decklist/' + deck_id)[0]


def get_card(card_id):
    return query_nrdb('/public/card/' + card_id)[0]


def get_cards():
    return query_nrdb('/public/cards')


def get_pack(pack_id):
    return query_nrdb('/public/pack/' + pack_id)[0]
