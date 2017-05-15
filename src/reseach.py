import string
from pprint import pprint
import pandas
import simplejson

import requests

# with open('../data/AllSets.json') as fp:
#     db = simplejson.load(fp)
#
# df = pandas.DataFrame()
#
# for i in db:
#     ndf = pandas.DataFrame.from_dict(db[i]['cards'])
#     df = pandas.concat([df, ndf])
#     # print df.shape
#
# df.index = range(df.shape[0])

# print df
# alljson = []
# pageno = 0
# hasdata = True
# while hasdata:
#     r = requests.get('https://api.deckbrew.com/mtg/cards?page={0}'.format(pageno))
#     print r.json()
#     if len(r.json()) == 0:
#         hasdata = False
#     alljson.append(r.json())
#     pageno += 1
#
# with open('outie.json', 'w') as o:
#     simplejson.dump(alljson, o)

with open('outie.json') as fp:
    db = simplejson.load(fp)

df = pandas.DataFrame()

for i in db:
    ndf = pandas.DataFrame.from_dict(i)
    df = pandas.concat([df, ndf])

# df.index = range(df.shape[0])
#
# print df['editions'][100]
# df['price_high'] = df['editions'].map(lambda x: x[0]['price']['high'])
#
# print df['price_high'].describe()

prices = pandas.read_csv('../data/mtgsprices-2017-05-12.csv')

#  convert a dollar
prices['Market'] = prices['Market'].apply(lambda x: x[1:].replace(',', '')).astype(float)

gp = prices.groupby(by='Name')['Market'].agg([pandas.np.mean, pandas.np.max, pandas.np.min])

m = pandas.merge(left=df, right=gp, left_on='name', right_index=True)

m.index = range(m.shape[0])


print df.shape
print m


m.to_csv('../data/joined.csv', encoding='utf-8')