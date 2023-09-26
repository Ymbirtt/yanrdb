#! /usr/bin/env python
import sys
import argparse
import os
from pprint import pprint

from PIL import Image
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import white

import lib.nrdb as nrdb

def recursive_search_file(dirname, filename):
    ret = []

    for f in os.scandir(dirname):
        if f.is_dir():
            ret.extend(recursive_search_file(f, filename))
        elif f.is_file():
            if os.path.splitext(f.name)[0] == filename:
                ret.append(f)
    return ret


def find_image_for_card(card_name):
    paths = recursive_search_file('data/sets', card_name)
    if len(paths) == 0:
        raise RuntimeError(f"Couldn't find a card file for {card_name}")
    if len(paths) > 1:
        raise RuntimeError(f"Found several card files for {card_name}: {','.join(path.path for path in paths)}")

    path = paths[0].path
    return path

def draw_pdf(deck_name, cards, bleed_mm):
    num_rows = 3
    num_cols = 3
    row_idx = 0
    col_idx = 0

    card_width = 63.5 * mm
    card_height = 88 * mm
    bleed = bleed_mm * mm

    bleed_box_width = card_width * num_cols + bleed * (num_cols + 1)
    bleed_box_height = card_height * num_rows + bleed * (num_rows + 1)
    bleed_box_x = (A4[0] - bleed_box_width) / 2
    bleed_box_y = (A4[1] - bleed_box_height) / 2
    bleed_box = (bleed_box_x, bleed_box_y, bleed_box_width, bleed_box_height)

    canvas = Canvas(deck_name + '.pdf', pagesize=A4)
    canvas.setTitle(deck_name)

    first_page = True
    for card in cards:
        if row_idx == 0 and col_idx == 0:
            if not first_page:
                canvas.showPage()
            if bleed:
                canvas.rect(*bleed_box, fill=1)

        first_page = False

        card_x = bleed_box_x + bleed + ((card_width + bleed) * col_idx)
        card_y = bleed_box_y + bleed + ((card_height + bleed) * (num_rows - row_idx - 1))
        canvas.drawImage(card, card_x, card_y, card_width, card_height)

        col_idx += 1
        if col_idx >= num_cols:
            col_idx = 0
            row_idx += 1

        if row_idx >= num_rows:
            row_idx = 0

    canvas.setFillColor(white)
    while row_idx != 0 or col_idx != 0:
        card_x = bleed_box_x + bleed + ((card_width + bleed) * col_idx)
        card_y = bleed_box_y + bleed + ((card_height + bleed) * (num_rows - row_idx - 1))
        canvas.rect(card_x, card_y, card_width, card_height, fill=1, stroke=0)

        col_idx += 1
        if col_idx >= num_cols:
            col_idx = 0
            row_idx += 1

        if row_idx >= num_rows:
            row_idx = 0

    canvas.save()

def fetch_deck_from_id(deck_id):
    deck = nrdb.get_deck(deck_id)
    print(f"Found deck called {deck['name']}")
    card_names = [card_name for card_id, qty in deck['cards'].items()
            for card_name in [nrdb.get_card(card_id)['title']]*qty]
    for card_name in card_names:
        print(f"    {card_name}")
    return deck['name'], card_names

def fetch_deck_from_jnet_file(deck_id):
    deck_name = os.path.splitext(deck_id)[0]
    with open(deck_id) as f:
        decklist = [line.strip().split(' ', 1) for line in f if line.strip()]
    card_names = [card_name for qty, title in decklist
            for card_name in [title]*int(qty)]
    return deck_name, card_names

def build_deck(deck_id, id_type, bleed):
    if id_type == 'nrdb_id':
        deck_name, card_names = fetch_deck_from_id(deck_id)
    elif id_type == 'jnet_file':
        deck_name, card_names = fetch_deck_from_jnet_file(deck_id)

    card_imgs = [find_image_for_card(card_name) for card_name in card_names]
    draw_pdf(deck_name, card_imgs, bleed)

    print("Produced PDF!")

def main(argv):
    supported_id_types = ['nrdb_id', 'jnet_file']
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bleed', help="Bleed between cards in mm", default=0, type=float)
    parser.add_argument('-t', '--type', help=f"Type of deck id - supported: {', '.join(supported_id_types)}")
    parser.add_argument('deck_id')
    args = parser.parse_args(argv)

    if args.type not in supported_id_types:
        print(f"Don't know what to do with an ID type of {args.type}")
        print(f"Supported types are: {', '.join(supported_id_types)}")

    build_deck(args.deck_id, args.type, args.bleed)


if __name__ == '__main__':
    main(sys.argv[1:])
