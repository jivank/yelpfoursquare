import json
from miner import get_yelp_restaurants, yelp_to_foursquare
from what3words import get3words


def pretty_dump(obj):
    return json.dumps(obj, sort_keys=True,
                      indent=4, separators=(',', ': '))


def dump_yelp(zips):
    yelp = []
    # foursquare = []
    for z in zips:
        yelp.extend(get_yelp_restaurants(z))
        # foursquare.extend(get_foursquare_restaurants(z))
    # remove duplicates
    yelp = [dict(tupleized) for tupleized in set(tuple(item.items()) for item in yelp)]

    yelpfile = open('yelp.json', 'w')
    # fsfile = open('foursquare.json', 'w')

    yelpfile.write(pretty_dump(yelp))
    # fsfile.write(pretty_dump(foursquare))

    yelpfile.close()
    # fsfile.close()


def lat_long_yelp():
    yelp = json.loads(open(r'yelp.json').read())
    for y in yelp:
        try:
            yelp_to_foursquare(y)
        except:
            print 'couldnt get match'
    yll = open(r'yelp_latlong.json', 'w')
    yll.write(pretty_dump(yelp))
    yll.close()


def dump_three_words():
    businesses = json.loads(open(r'yelp_latlong.json').read())
    for business in businesses:
        if business['lat'] == 0 and business['long'] == 0:
            continue
        try:
            business['3words'] = get3words(business['lat'],
                                           business['long'])
        except:
            print 'couldnt get 3 words'
    final = open(r'final.json', 'w')
    final.write(pretty_dump(businesses))
    final.close()
