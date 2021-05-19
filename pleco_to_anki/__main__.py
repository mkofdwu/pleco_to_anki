import os
import sys

import genanki

from constants import css
from models import Phrase


def read_and_extract_phrases(path):
    with open(path, 'r+') as f:
        phrases = []
        for line in f.readlines():
            if line.startswith('//'):
                continue
            phrases.append(Phrase.from_string(line))
        return phrases


def get_existing_phrases(deck_name):
    path = f'./out/{deck_name}_existing_phrases.txt'
    if not os.path.isfile(path):
        return []
    with open(path, 'r') as f:
        return f.read().split('\n')


def save_existing_phrases(deck_name, phrases):
    path = f'./out/{deck_name}_existing_phrases.txt'
    with open(path, 'w') as f:
        f.write('\n'.join(phrase.chinese for phrase in phrases))


def format_pleco_export(path, deck_name):
    phrases = read_and_extract_phrases(path)
    existing_phrases = get_existing_phrases(deck_name)
    model = genanki.Model(
        1324780,
        name=deck_name + ' model',
        fields=[
            {'name': 'Front'},
            {'name': 'Back'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Front}}',
                'afmt': '{{Back}}',
            },
        ],
        css=css.CSS,
    )
    deck = genanki.Deck(1472890, deck_name)
    for phrase in phrases:
        if phrase.chinese in existing_phrases:
            continue
        note = genanki.Note(
            model=model,
            fields=[
                phrase.front_html(),
                phrase.back_html()
            ],
        )
        deck.add_note(note)
    genanki.Package(deck).write_to_file('out/' + deck_name + '.apkg')

    # save list of generated phrases to prevent duplicates
    save_existing_phrases(deck_name, phrases)


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) != 2:
        print('Usage: python3 pleco_to_anki.py <pleco_export_file> <deck_name>')
    else:
        format_pleco_export(*args)
