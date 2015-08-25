from dump_json import dump_yelp, lat_long_yelp, dump_three_words
from insert_mongo import final_json_to_mongo


zips = [92603, 92614]

# create yelp json
dump_yelp(zips)

# match to foursquare and get long and lat
lat_long_yelp()

# get threewords
dump_three_words()

# push into mongodb
final_json_to_mongo()
