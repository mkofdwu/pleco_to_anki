import re

from utils import remove_links, splice_string, convert_alphanum_to_pinyin
from constants import html_templates

pleco_tags = ['verb', 'adjective', 'noun',
              'idiom', 'conjunction', 'literary', 'dialect', 'colloquial', 'adverb', 'pronoun', 'preposition']

chinese_phrase_pattern = '[\u4e00-\u9fff][\u4e00-\u9fff, 。？]+'
line_pattern = f'(?P<chinese>.*?)\t(?P<pinyin>.*?)\t(?P<tags>(({"|".join(pleco_tags)}) )*)(?P<definition_and_examples>.*)'
single_definition_pattern = r'\d .*?(?=( \d |$))'
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
        return str(self.__dict__)
        # return f'chinese: {self.chinese_phrase}\npinyin: {self.pinyin}\nenglish: {self.english}'

    def __repr__(self):
        return self.__str__()


class Definition:

    def __init__(self, defn: str, examples: list):
        self.defn = defn.strip()
        self.examples = examples

    @staticmethod
    def from_string(string):
        string = remove_links(string)
        chinese_indexes = [m.start()
                           for m in re.finditer(chinese_phrase_pattern, string)]
        if len(chinese_indexes) == 0:
            return Definition(string, [])
        defn = string[:chinese_indexes[0]]
        examples = []
        for i in range(len(chinese_indexes) - 1):
            example_str = string[chinese_indexes[i]: chinese_indexes[i + 1]]
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
        return str(self.__dict__)
        # examples_str = '\n\t'.join(str(example) for example in self.examples)
        # return f'defn: {self.defn}\n==========\nexamples: \n\t{examples_str}\n'

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
    def _extract_definitions(definition_and_examples_str: str):
        # TODO: cards with multiple types (can be used as a noun / verb / adjective in different ways, etc)
        definition_and_examples_str = definition_and_examples_str.strip()
        if definition_and_examples_str.startswith('1 '):
            definitions = []
            for match in re.finditer(single_definition_pattern, definition_and_examples_str):
                string = match.group(0)[2:]  # remove the number
                definitions.append(Definition.from_string(string))
        elif ' 1 ' in definition_and_examples_str:
            first_num_i = definition_and_examples_str.find(' 1 ')
            definitions = [Definition.from_string(
                definition_and_examples_str[:first_num_i])]
            for match in re.finditer(single_definition_pattern, definition_and_examples_str):
                string = match.group(0)[2:]  # remove the number
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

    def __repr__(self):
        return str(self.__dict__)
        # definitions_str = '\n\t'.join(str(definition)
        #                               for definition in self.definitions)
        # return f'chinese: {self.chinese}\npinyin: {self.pinyin}\ntags: {self.tags}\ndefinitions: \n\t{definitions_str}'
