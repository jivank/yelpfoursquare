import yelp
import foursquare
from difflib import SequenceMatcher
from collections import defaultdict


def _none_value_handler(x):
    if x is None:
        return '?'
    else:
        return x


def _ratio(a, b):
    m = SequenceMatcher(None, a, b)
    return m.ratio()


def _try_get_value(somedict, somekey):
    value = '?'
    if somekey in somedict.keys():
        value = somedict[somekey]
    return value


def yelp_to_json(business):
    jsondict = {}
    jsondict['name'] = business.name
    jsondict['lat'] = 0
    jsondict['long'] = 0
    jsondict['tel'] = business.phone
    jsondict['zipcode'] = business.location.postal_code
    jsondict['city'] = business.location.city
    jsondict['address'] = ' '.join(business.location.address)
    jsondict = {k: _none_value_handler(v) for k, v in jsondict.items()}

    return jsondict


def foursquare_to_json(business):
    jsondict = {}
    if 'venue' in business.keys():
        venue = business['venue']
    else:
        venue = business
    jsondict['name'] = venue['name']
    jsondict['lat'] = venue['location']['lat']
    jsondict['long'] = venue['location']['lng']
    jsondict['tel'] = _try_get_value(venue['contact'], 'phone')
    jsondict['zipcode'] = _try_get_value(venue['location'], 'postalCode').split('-')[0]
    jsondict['city'] = _try_get_value(venue['location'], 'city')
    jsondict['address'] = _try_get_value(venue['location'], 'address')
    return jsondict


def get_yelp_restaurants(zipcode):
    result = []
    MY_CONSUMER_KEY = 'i_zD_0DNf1Jv54g_Ib329g'
    MY_CONSUMER_SECRET = 'rWhgvl3XlSEzwMzaT0D6y2zBEks'
    MY_ACCESS_TOKEN = 'm0FpajjIklHnzr9jSF20Dot0Cxte5718'
    MY_ACCESS_SECRET = 'HA7eypHeXDkqi_hxxqdMnJfhLVo'
    yelp_api = yelp.Api(consumer_key=MY_CONSUMER_KEY,
                        consumer_secret=MY_CONSUMER_SECRET,
                        access_token_key=MY_ACCESS_TOKEN,
                        access_token_secret=MY_ACCESS_SECRET)
    for i in range(0, 1000, 20):
        search_results = yelp_api.Search(term="restaurant", location=zipcode,
                                         limit=20, offset=i)
        for business in search_results.businesses:
            # print business.name, business.snippet_text
            result.append(yelp_to_json(business))
        if len(search_results.businesses) < 20:
            break
    return result


def get_foursquare_restaurants(zipcode):
    cid = 'CR35KTWYW2ORWUVSKYRO2DBJQS5IHUGZ0L3AUD1NNEJ1DFVO'
    csec = '0CJSR410CJYIF3YQBPFBCPAUAXTCJW5JXMJ4ABRDXAKWPZVF'
    result = []
    client = foursquare.Foursquare(client_id=cid,
                                   client_secret=csec)
    auth_uri = client.oauth.auth_url()
    # ex['groups'][0]['items'][0]['venue']['location']
    limit = client.venues.explore(params={'query': 'restaurant', 'near': str(zipcode),
                                          'limit': '1', 'offset': '0'})['totalResults']
    limit = int(limit)
    for i in range(0, limit, 50):
        restaurants = client.venues.explore(params={'query': 'restaurant',
                                                    'limit': '50',
                                                    'offset': str(i),
                                                    'near': str(zipcode)})['groups'][0]['items']
        for restaurant in restaurants:
            result.append(foursquare_to_json(restaurant))
    return result


# get lat long for yelp
def yelp_to_foursquare(yelpitem):
    cid = 'CR35KTWYW2ORWUVSKYRO2DBJQS5IHUGZ0L3AUD1NNEJ1DFVO'
    csec = '0CJSR410CJYIF3YQBPFBCPAUAXTCJW5JXMJ4ABRDXAKWPZVF'
    result = []
    client = foursquare.Foursquare(client_id=cid,
                                   client_secret=csec)
    auth_uri = client.oauth.auth_url()
    total = len([val for val in yelpitem.values() if val != '?'])
    if yelpitem['zipcode'] == '?' or yelpitem['zipcode'][:1] == '2':
        return
    restaurants = client.venues.search(params={'query': yelpitem['name'],
                                               'near': str(yelpitem['zipcode'])})
    restaurants = restaurants['venues']
    for restaurant in restaurants:
        result.append(foursquare_to_json(restaurant))
    score = defaultdict(float)
    for i, item in enumerate(result):
        telscore = _ratio(yelpitem['tel'], item['tel'])
        namescore = _ratio(yelpitem['name'], item['name'])
        zipscore = _ratio(yelpitem['zipcode'], item['zipcode'])
        addressscore = _ratio(yelpitem['address'], item['address'])
        cityscore = _ratio(yelpitem['city'], item['city'])
        for sco in [telscore, namescore, zipscore, addressscore, cityscore]:
            if sco == 1:
                score[i] += 2
            else:
                score[i] += sco
        score[i] /= total
    if len(score) == 0:
        return
    candidate = max(score, key=score.get)
    # print score
    if max(score.values()) >= 0.80:
        # print yelpitem, result[candidate]
        yelpitem['lat'] = result[candidate]['lat']
        yelpitem['long'] = result[candidate]['long']
        if yelpitem['tel'] == '?':
            yelpitem = result[candidate]['tel']
        if yelpitem['city'] == '?':
            yelpitem = result[candidate]['city']
        if yelpitem['address'] == '?':
            yelpitem = result[candidate]['address']

