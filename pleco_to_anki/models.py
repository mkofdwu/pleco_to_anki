import re

from utils import splice_string, convert_alphanum_to_pinyin
from constants import html_templates

pleco_tags = ['verb', 'adjective', 'noun',
              'idiom', 'conjunction', 'literary', 'dialect']

chinese_phrase_pattern = '[\u4e00-\u9fff][\u4e00-\u9fff, 。？]+'
line_pattern = f'(?P<chinese>.*?)\t(?P<pinyin>.*?)\t(?P<tags>(({"|".join(pleco_tags)}) )*)(?P<definition_and_examples>.*)'
single_definition_pattern = ' \d .*?(?= \d |$)'
pinyin_special_chars = 'āáǎàēéěèīíǐìōóǒòūúǔùüǖǘǚǜ'
# pinyin_phrase_pattern = f'[a-zA-Z{pinyin_special_chars}, ]*[{pinyin_special_chars}][a-zA-Z]*?'
# non_pinyin_pattern = ' [a-zA-Z\',]+? '
english_defn_pattern = f' [^{pinyin_special_chars}]+$'


class Example:

    def __init__(self, chinese_phrase: str, pinyin: str, english: str):
        self.chinese_phrase = chinese_phrase.strip()
        self.pinyin = pinyin.strip()
        self.english = english.strip()

    @staticmethod
    def from_string(string):
        try:
            chinese_end = re.match(chinese_phrase_pattern, string).end()
            english_start = re.search(english_defn_pattern, string).start()
            return Example(string[:chinese_end], string[chinese_end:english_start], string[english_start:])
        except:
            print('ERROR', string)

    def to_html(self, main_chinese):
        i = self.chinese_phrase.find(main_chinese)
        formatted_chinese = splice_string(
            self.chinese_phrase, i, i + len(main_chinese), '<b>' + main_chinese + '</b>')
        return html_templates.EXAMPLE.format(
            chinese=formatted_chinese,
            pinyin=self.pinyin,
            english_def=self.english,
        )

    def __str__(self):
        return f'CHINESE: {self.chinese_phrase}\nPINYIN: {self.pinyin}\nENGLISH: {self.english}'

    def __repr__(self):
        return self.__str__()


class Definition:

    def __init__(self, defn: str, examples: list):
        self.defn = defn.strip()
        self.examples = examples

    @staticmethod
    def from_string(string):
        chinese_indexes = [m.start()
                           for m in re.finditer(chinese_phrase_pattern, string)]
        if len(chinese_indexes) == 0:
            return Definition(string, [])
        defn = string[:chinese_indexes[0]]
        examples = []
        for i in range(len(chinese_indexes) - 1):
            example_str = string[chinese_indexes[i]: chinese_indexes[i+1]]
            examples.append(Example.from_string(example_str))
        examples.append(Example.from_string(string[chinese_indexes[-1]:]))
        return Definition(defn, examples)

    def to_html(self, def_num, main_chinese):
        return html_templates.DEFINITION.format(
            num=def_num,
            english_def=self.defn,
            examples='\n'.join(example.to_html(main_chinese)
                               for example in self.examples if example is not None),
        )

    def __str__(self):
        return f'DEFN: {self.defn}\n==========\nEXAMPLES: {self.examples}\n'

    def __repr__(self):
        return self.__str__()


class Phrase:

    def __init__(self, chinese: str, pinyin: str, tags: str, definitions: list):
        self.chinese = chinese
        self.pinyin = pinyin
        self.tags = tags
        self.definitions = definitions

    @staticmethod
    def from_string(line):
        match = re.match(line_pattern, line)
        definition_and_examples = match.group(
            'definition_and_examples')
        definitions = Phrase._extract_definitions(definition_and_examples)
        return Phrase(
            match.group('chinese'),
            convert_alphanum_to_pinyin(match.group('pinyin')),
            ', '.join(match.group('tags').split()),
            definitions,
        )

    @staticmethod
    def _extract_definitions(definition_and_examples_str):
        if ' 1 ' in definition_and_examples_str:
            definitions = []
            for match in re.finditer(single_definition_pattern, definition_and_examples_str):
                string = match.group(0)[1:]  # remove the number
                definitions.append(Definition.from_string(string))
        else:
            definitions = [Definition.from_string(definition_and_examples_str)]
        return definitions

    def front_html(self):
        return html_templates.CARD_FRONT.format(chinese=self.chinese)

    def back_html(self):
        return html_templates.CARD_BACK.format(
            chinese=self.chinese,
            pinyin=self.pinyin,
            tags=self.tags,
            definitions='\n'.join(definition.to_html(i + 1, self.chinese)
                                  for i, definition in enumerate(self.definitions)),
        )
