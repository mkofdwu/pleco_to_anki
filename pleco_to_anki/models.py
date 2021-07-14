import re

from utils import remove_links, splice_string, convert_alphanum_to_pinyin
from constants import html_templates

pleco_tags = ['verb', 'adjective', 'noun',
              'idiom', 'conjunction', 'literary', 'dialect', 'colloquial', 'adverb', 'pronoun', 'preposition']

chinese_phrase_pattern = '[\u4e00-\u9fff][\u4e00-\u9fff, 。？]+'
tags_and_definition_pattern = f'(?P<tags>(({"|".join(pleco_tags)}) )+)(?P<definitions_and_examples>.*?)(?=$|{"|".join(pleco_tags)})'
line_pattern = f'(?P<chinese>.*?)\t(?P<pinyin>.*?)\t(?P<all_meanings>.*)'
single_definition_pattern = r'\d .*?(?=( \d |$))'
pinyin_special_chars = 'āáǎàēéěèīíǐìōóǒòūúǔùüǖǘǚǜ'
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
            print(f'ERROR <{string}>')

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

    def __repr__(self):
        return self.__str__()


class Phrase:
    r'''
    Example:
    凭                                     # chinese
    píng                                   # pinyin

    -----
    NOUN                                   # tags
    1 go by; base on; take as the basis    # definition
      * 凭良心说                            # example chinese
        píng liángxīn shuō                 # example pinyin
        in all fairness                    # example english
      * 凭票付款                            # example (2)
        Píng piào fùkuǎn
        payable to bearer

    -----
    VERB                                   # tags (2)
    1 lean on; lean against
      * 凭几
        píngjī
        lean on a small table
    '''

    def __init__(self, chinese: str, pinyin: str, tags_and_definitions: list):
        # tags_and_definitions: ['pleco_tag', [...defs]]
        self.chinese = chinese
        self.pinyin = pinyin
        self.tags_and_definitions = tags_and_definitions

    @staticmethod
    def from_string(line):
        match = re.match(line_pattern, line)
        all_meanings = match.group('all_meanings')
        tags_and_definitions = Phrase._extract_tags_and_definitions(all_meanings)
        return Phrase(
            match.group('chinese'),
            convert_alphanum_to_pinyin(match.group('pinyin')),
            tags_and_definitions,
        )

    @staticmethod
    def _extract_tags_and_definitions(all_meanings: str):
        tags_and_definitions = []
        for match in re.finditer(tags_and_definition_pattern, all_meanings):
            tags = ', '.join(match.group('tags').strip().split())
            def_and_exs_str = match.group('definitions_and_examples')
            all_meanings = def_and_exs_str.strip()
            if def_and_exs_str.startswith('1 '):
                definitions = []
                for match in re.finditer(single_definition_pattern, def_and_exs_str):
                    string = match.group(0)[2:]  # remove the number
                    definitions.append(Definition.from_string(string))
            elif ' 1 ' in def_and_exs_str:
                first_num_i = def_and_exs_str.find(' 1 ')
                definitions = [Definition.from_string(
                    def_and_exs_str[:first_num_i])]
                for match in re.finditer(single_definition_pattern, def_and_exs_str):
                    string = match.group(0)[2:]  # remove the number
                    definitions.append(Definition.from_string(string))
            else:
                definitions = [Definition.from_string(def_and_exs_str)]
            tags_and_definitions.append([tags, definitions])
        if len(tags_and_definitions) == 0:
            tags_and_definitions.append(['', [Definition.from_string(all_meanings)]])
        return tags_and_definitions

    def front_html(self):
        return html_templates.CARD_FRONT.format(chinese=self.chinese)

    def back_html(self):
        tags_and_definitions_formatted = ''
        for tags, definitions in self.tags_and_definitions:
            tags_and_definitions_formatted += html_templates.CARD_TAGS_AND_DEFINITIONS.format(
                tags=tags,
                definitions='\n'.join(defn.to_html(i + 1, self.chinese) for i, defn in enumerate(definitions))
            )
        return html_templates.CARD_BACK.format(
            chinese=self.chinese,
            pinyin=self.pinyin,
            tags_and_definitions=tags_and_definitions_formatted
        )

    def __repr__(self):
        return str(self.__dict__)
