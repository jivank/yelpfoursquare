import json
from collections import defaultdict
from copy import copy


def _choose_address(addresses):
    unique = list(set(addresses))
    score = defaultdict(int)
    if len(unique) == 1:
        return unique[0]
    for addy in unique:
        if not addy:
            addy = '?'
        split = addy.split()
        if split[0].isdigit():
            score[addy] += 10
        score[addy] += len(split)
    return max(score, key=score.get)


def _choose_city(cities):
    unique = list(set(cities))
    score = defaultdict(int)
    if len(unique) == 1:
        return unique[0]
    for city in unique:
        split = city.split()
        score[city] += len(split)
        score[city] += len(city)
    return max(score, key=score.get)


def _choose_zip(zips):
    unique = list(set(zips))
    score = defaultdict(int)
    if len(unique) == 1:
        return unique[0]
    for zipp in unique:
        if zipp.isdigit() and len(zipp) == 5:
            score[zipp] += 10
    return max(score, key=score.get)


def index_by_key(target, key):
    defdict = defaultdict(list)
    for item in target:
        defdict[item[key]].append(item)
    return defdict






# def clean_zips(index):
#     notzip = []
#     delete = []
#     for key in index.keys():
#         if not re.match(re.compile(r'\b\d{5}\b'), key):
#             notzip.extend(index[key])
#             delete.append(key)
#     index['?'] = notzip
#     for key in delete:
#         del index[key]

yelp = json.loads(open(r'yelp.json').read())
fs = json.loads(open(r'foursquare.json').read())

# indices
fs_name_index = index_by_key(fs, 'name')
fs_tel_index = index_by_key(fs, 'tel')
fs_zip_index = index_by_key(fs, 'zipcode')
yelp_name_index = index_by_key(yelp, 'name')
yelp_tel_index = index_by_key(yelp, 'tel')
yelp_zip_index = index_by_key(yelp, 'zipcode')

# telephone merge
merged_tel_index = copy(yelp_tel_index)
merged_tel_index.update(fs_tel_index)
for k, v in merged_tel_index.items():
    merged_tel_index[k] = [dict(tupleized) for tupleized in set(tuple(item.items()) for item in v)]

non = merged_tel_index.pop('?')
















