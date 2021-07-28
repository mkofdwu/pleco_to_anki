import os
import platform
import sqlite3

from unidecode import unidecode

HOME_PATH = os.path.expanduser('~')
system = platform.system()
if system == 'Linux':
    path = '.local/share/Anki2/User 1/collection.anki2'
elif system == 'Darwin':
    path = 'Library/Application Support/Anki2/User 1/collection.anki2'
elif system == 'Windows':
    path = 'AppData/Roaming/Anki2/User 1/collection.anki2'
else:
    raise Exception(f'Unrecognised operating system {system}')
DB_PATH = os.path.join(HOME_PATH, path)


def unicase_compare(x, y):
    x_ = unidecode(x).lower()
    y_ = unidecode(y).lower()
    return 1 if x_ > y_ else -1 if x_ < y_ else 0


def get_existing_phrases(deck_name):
    conn = sqlite3.connect(DB_PATH)
    conn.create_collation("unicase", unicase_compare)
    cur = conn.cursor()
    try:
        model_id = cur.execute(f'SELECT id FROM notetypes WHERE name = "{deck_name} model"').fetchone()
    except sqlite3.OperationalError:
        print('Could not read database, please make sure Anki is closed.')
        raise
    else:
        if model_id is None:
            return ()
        existing_phrases = sum(cur.execute(f'SELECT sfld FROM notes WHERE mid = {model_id[0]}'), ())
        return existing_phrases
