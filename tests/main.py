import os
import json
import sys
import ast
import unittest

cwd = os.path.dirname(__file__)
os.chdir(cwd)

sys.path.append('/home/leejiajie/dev/scripts/pleco_to_anki/pleco_to_anki')

import models


class TestPhraseExtraction(unittest.TestCase):
    def test(self):
        with open('./expected.json', 'r') as f:
            expected = json.load(f)
        with open('./in.txt', 'r+') as f:
            phrases = []
            for line in f.readlines():
                if line.startswith('//'):
                    continue
                phrases.append(models.Phrase.from_string(line))
            obj = ast.literal_eval(str(phrases))
            # s = json.dumps(obj, indent=4)
        self.assertListEqual(obj, expected)


unittest.main()
