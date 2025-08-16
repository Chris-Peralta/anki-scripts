import random
from email.policy import default
from tabnanny import verbose

import pandas as pd
import genanki
import html
from enum import Enum


class Field(str, Enum):
    WORD = "Word"
    LIKANU = "xʃxƨſ "
    TYPE = "Type"
    MEANING = "Meaning"
    NOUN = "Noun"
    VERB = "Verb"
    MODIFIER = "Modifier"
    ORIGIN = "Origin"
    FAMILY = "Family"

class Kokanu(str, Enum):
    NOUN = "ikama sin"
    VERB = "ikama tun"
    MODIFIER = "ikama kun"

# Define the CSS for your cards
my_css = """
.card {
  font-family: Arial, sans-serif;
  font-size: 20px;
  text-align: center;
  color: white;
  background-color: #000000;
}
.pos {
    font-size: 12px;
    text-transform: lowercase;
}
"""

def create_meaning_html(part_of_speech: str, meaning_field: str) -> str:
    return '''
<div class="pos">''' + part_of_speech + '''</div>
{{''' + meaning_field + '''}}
'''

default_meaning_html = create_meaning_html('{{' + Field.TYPE.value + '}}', Field.MEANING.value)

verb_meaning_html = create_meaning_html(Kokanu.VERB.value, Field.VERB.value)

noun_meaning_html = create_meaning_html(Kokanu.NOUN.value, Field.NOUN.value)

modifier_meaning_html = create_meaning_html(Kokanu.MODIFIER.value, Field.MODIFIER.value)

# Leaving multi-line formatting to make this readable to the end user
meaning_html = default_meaning_html + '''

<br>
<br>''' + verb_meaning_html + '''

<br>
<br> ''' + noun_meaning_html + '''

<br>
<br>''' + modifier_meaning_html

def create_template(name: str, question_format: str, answer_format: str) -> dict[str, str]:
    return {
        'name': name,
        'qfmt': question_format,
        'afmt': answer_format,
    }

def create_basic_kokanu_first_template() -> dict[str, str]:
    question_format = '{{' + Field.WORD.value + '}}'
    answer_format = '''
{{FrontSide}}

<hr id="answer"> 

<br>''' + meaning_html + '''
'''
    return create_template('Card 1', question_format, answer_format)


def create_basic_typed_meaning_first_template() -> dict[str, str]:
    question_format = '''
<br>''' + meaning_html + '''

<br>
<br>
{{type:''' + Field.WORD.value + '''}}
'''
    answer_format = '{{FrontSide}}<hr id="answer"> {{' + Field.WORD.value + '}}'
    return create_template('Card 2', question_format, answer_format)


model = genanki.Model(
    random.randint(1, 10000000000),
    'Kokanu model',
    fields=list(map(lambda x: {'name': x.value}, Field)),
    templates=[
        create_basic_kokanu_first_template(),
        create_basic_typed_meaning_first_template(),
        create_template(
            'Card 3',
            '{{' + Field.LIKANU.value + '}}<br>',
            '{{FrontSide}}<hr id="answer"> {{' + Field.WORD.value + ' }}'
        )
    ],
    css=my_css,
)

url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTVGXFd17kcvfu__zjshqiV3kW360IclOEfEdWda_K6ZCg4TY6nW2Gwn4_bs1yQeFLwrZI1_xEvSuP0/pub?gid=0&single=true&output=csv'

# Read google sheet and sort at random due to no word frequency data
df = pd.read_csv(url).fillna('').sample(frac=1).reset_index(drop=True)

kokanu_deck = genanki.Deck(
    random.randint(1, 10000000000),
    'Kokanu Vocab')

for index, row in df.iterrows():
    note = genanki.Note(
        model=model,
        fields=list(map(lambda x: html.escape(row[x.value]), Field)),
        tags=[row[Field.TYPE.value].replace(' ', ''), row[Field.FAMILY.value].replace(' ', '')]
    )
    kokanu_deck.add_note(note)

genanki.Package(kokanu_deck).write_to_file('kokanu/kokanu_deck.apkg')
