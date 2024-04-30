import json


tracking_data = {
        'name_to_id': 0,
        'last_id': 0
}
with open('tracker.json', 'w') as tracking_file:
            json.dump(tracking_data, tracking_file)