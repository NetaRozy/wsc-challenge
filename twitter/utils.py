import json



def read_json(path):
    with open(path) as json_data:
        data = json.load(json_data)

    return data

def write_json(path, data):
    with open(path, 'w') as outfile:
        json.dump(data, outfile)

def add_to_blacklist(filtered_tweets_id):
    for event in filtered_tweets_id:
        with open("id.history", "a") as myfile:
            myfile.write(str(event) + '\n')

def filtered_tweets_id():
    return open('id.history', 'r').read().split('\n')

DATA = read_json('files/db.json')