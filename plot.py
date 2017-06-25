import pandas as pd
from collections import defaultdict
import plotly
import plotly.graph_objs as go


def load_mtg_json():
    df = pd.read_json('AllCards-x.json', orient='index')
    return df


def load_mtg_sets():
    df = pd.read_json('AllSets-x.json', orient='index')
    return df


def get_meta():
    with open('meta.txt') as meta:
        return meta.read().splitlines()


def get_first_printing(df, card):
    printings = df.loc[card.replace(r'/', r'//')].printings
    for printing in printings:
        if not printing.startswith('p'):
            return printing


meta = get_meta()
cards = load_mtg_json()
sets = load_mtg_sets()

per_set = defaultdict(list)
for card in meta:
    set = get_first_printing(cards, card)
    per_set[set].append(card)

sorted_sets = [set for set in sets.sort_values('releaseDate').index if set in per_set]

data = [go.Bar(
    x=list(per_set.keys()),
    y=list([len(l) for l in per_set.values()]),
    text=([', '.join(l) for l in per_set.values()])
)]
layout = go.Layout(
    xaxis=dict(
        categoryarray=sorted_sets
    )
)
fig = go.Figure(data=data, layout=layout)
plotly.offline.plot(fig, filename='docs/index.html')
