import boto3
import datetime
import random

dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")

table = dynamodb.Table('Lakes')

lakes = [('Garda', 10), ('Maggiore', 8), ('Como', 6), ('Tresimeno', 5), ('Bolsena', 5)]

device_ids = []

for lake, device_id in lakes:
    lake_devices = ""
    for i in range(device_id):
        lake_devices = lake_devices + ("%s_%s") % (lake, str(i)) + " "
    device_ids.append(lake_devices)

for i in range(len(lakes)):
    measure_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    avg_water_level = random.randint(10, 200)
    min_water_level = random.randint(10, 200)
    max_water_level = random.randint(10, 200)
    item = {
		'lake': lakes[i][0],
		'measure_date': str(measure_date), 
		'avarage_water_level': str(avg_water_level),
		'max_water_level': str(max_water_level),
		'min_water_level': str(min_water_level),
		'device_id': device_ids[i]
	}
    table.put_item(Item=item)

    print("Stored item", item)
