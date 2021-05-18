CARD_FRONT = r'''<span class="very-large center">{chinese}</span>'''

CARD_BACK = r'''<h1 class="chinese">{chinese}</h1>
<h2>{pinyin}</h2>
<div class="divider"></div>
<span class="type">{type}</span>
<ol>
    {definitions}
</ol>'''

DEFINITION = r'''<li>
    <span class="definition-num">{num}</span>
    <div class="definition-column">
        {english_def}
        <ul>
        {examples}
        </ul>
    </div>
    </li>'''

EXAMPLE = r'''<li class="example">
            <div class="bullet-point"></div>
            <div class="example-column">
            <span class="chinese">{chinese}</span>
            <span class="pinyin">{pinyin}</span>
            <span class="definition">{english_def}</span>
            </div>
        </li>'''
