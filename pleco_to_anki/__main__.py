import os
import sys

import genanki

from constants import css
from models import Phrase
from existing_phrases import get_existing_phrases


def save_extracted_phrases_as_json(phrases):
    # write to file
    import json
    import ast
    obj = ast.literal_eval(str(phrases))
    with open('./out/result.json', 'w', encoding='utf-8') as f:
        json.dump(obj, f, indent=4, ensure_ascii=False)


def read_and_extract_phrases(path):
    with open(path, 'r+', encoding='utf-8') as f:
        phrases = []
        for line in f.readlines():
            if line.startswith('//') or line == '\n' or line == '':
                continue
            phrases.append(Phrase.from_string(line))
        return phrases


def format_pleco_export(path, deck_name):
    phrases = read_and_extract_phrases(path)
    # save_extracted_phrases_as_json(phrases)
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


if __name__ == '__main__':
    wd = os.path.dirname(os.path.dirname(__file__))
    os.chdir(wd)
    args = sys.argv[1:]
    if len(args) != 2:
        print('Usage: python3 pleco_to_anki.py <pleco_file> <deck_name>')
    else:
        format_pleco_export(*args)
