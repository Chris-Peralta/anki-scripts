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
"""

model = genanki.Model(
    1607392319545645645,
    'Kokanu model',
    fields=list(map(lambda x: {'name': x.value}, Field)),
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{' + Field.WORD.value + '}}<br>{{' + Field.TYPE.value + '}}<br>',
            'afmt': '{{FrontSide}}<hr id="answer"> {{' + Field.MEANING.value + ' }}',
        },
        {
            'name': 'Card 2',
            'qfmt': '{{' + Field.WORD.value + '}}<br>' + Field.NOUN.name + '<br>',
            'afmt': '{{FrontSide}}<hr id="answer"> {{' + Field.NOUN.value + ' }}',
        },
        {
            'name': 'Card 3',
            'qfmt': '{{' + Field.WORD.value + '}}<br>' + Field.VERB.name + '<br>',
            'afmt': '{{FrontSide}}<hr id="answer"> {{' + Field.VERB.value + ' }}',
        },
        {
            'name': 'Card 4',
            'qfmt': '{{' + Field.MODIFIER.value + '}}<br>' + Field.MODIFIER.name + '<br>',
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

df = pd.read_csv(url).fillna('')

kokanu_deck = genanki.Deck(
    4564564565445,
    'Kokanu Vocab')

for index, row in df.iterrows():
    note = genanki.Note(
        model=model,
        fields=list(map(lambda x: html.escape(row[x.value]), Field)))
    kokanu_deck.add_note(note)

genanki.Package(kokanu_deck).write_to_file('kokanu/kokanu_deck.apkg')
