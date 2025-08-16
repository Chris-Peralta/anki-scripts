import random

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
    padding: 10px;
}
"""

model = genanki.Model(
    random.randint(1, 10000000000),
    'Kokanu model',
    fields=list(map(lambda x: {'name': x.value}, Field)),
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{' + Field.WORD.value + '}}<br><div class="pos">{{' + Field.TYPE.value + '}}</div><br>',
            'afmt': '{{FrontSide}}<hr id="answer"> {{' + Field.MEANING.value + ' }}',
        },
        {
            'name': 'Card 2',
            'qfmt': '{{' + Field.WORD.value + '}}<br><div class="pos">' + Field.NOUN.name + '</div><br>',
            'afmt': '{{FrontSide}}<hr id="answer"> {{' + Field.NOUN.value + ' }}',
        },
        {
            'name': 'Card 3',
            'qfmt': '{{' + Field.WORD.value + '}}<br><div class="pos">' + Field.VERB.name + '</div><br>',
            'afmt': '{{FrontSide}}<hr id="answer"> {{' + Field.VERB.value + ' }}',
        },
        {
            'name': 'Card 4',
            'qfmt': '{{' + Field.MODIFIER.value + '}}<br><div class="pos">' + Field.MODIFIER.name + '</div><br>',
            'afmt': '{{FrontSide}}<hr id="answer"> {{' + Field.MODIFIER.value + ' }}',
        },
        {
            'name': 'Card 5',
            'qfmt': '{{' + Field.LIKANU.value + '}}<br>',
            'afmt': '{{FrontSide}}<hr id="answer"> {{' + Field.WORD.value + ' }}',
        }
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
