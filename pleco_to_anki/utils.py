import re

alphanum_to_pinyin = {
    'a1': 'ā',
    'a2': 'á',
    'a3': 'ǎ',
    'a4': 'à',
    'e1': 'ē',
    'e2': 'é',
    'e3': 'ě',
    'e4': 'è',
    'i1': 'ī',
    'i2': 'í',
    'i3': 'ǐ',
    'i4': 'ì',
    'o1': 'ō',
    'o2': 'ó',
    'o3': 'ǒ',
    'o4': 'ò',
    'u1': 'ū',
    'u2': 'ú',
    'u3': 'ǔ',
    'u4': 'ù',
    'ü1': 'ǖ',
    'ü2': 'ǘ',
    'ü3': 'ǚ',
    'ü4': 'ǜ',
}
link_pattern = r'\d+(?P<chinese>[\u4e00-\u9fff]+).*?'


def splice_string(string, start, end, replace):
    return string[:start] + replace + string[end:]


def convert_alphanum_to_pinyin(alphanum):
    alphanum = alphanum.replace('-', '').replace('//', '')
    word_pinyin_pattern = r'(^| |\d)(?P<main>[a-zA-Zü]+?[1-5])'
    while True:
        match = re.search(word_pinyin_pattern, alphanum)
        if match is None:
            break
        s = match.group('main')
        start = match.start('main')
        end = match.end('main')
        if s.endswith('5'):
            # no sound
            alphanum = splice_string(alphanum, end - 1, end, ' ')
            continue

        if s[-3:-1] == 'iu':
            alphanum = splice_string(alphanum, start, end, s[:-2] +
                                     alphanum_to_pinyin['u' + s[-1]] + ' ')
        elif s[-3:-1] == 'ui':
            alphanum = splice_string(alphanum, start, end, s[:-2] +
                                     alphanum_to_pinyin['i' + s[-1]] + ' ')
        else:
            for vowel in 'aeoiuü':
                if vowel in s:
                    alphanum = splice_string(alphanum, start, end, s.replace(
                        vowel, alphanum_to_pinyin[vowel + s[-1]])[:-1] + ' ')
                    break
    return alphanum


def remove_links(string):
    # replace links like 'See ... which produces invalid characters'
    while True:
        m = re.search(link_pattern, string)
        if m is None:
            break
        string = splice_string(string, m.start(), m.end(), m.group('chinese'))
    return string
