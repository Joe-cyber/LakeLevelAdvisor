import boto3
import datetime
import random

sqs = boto3.resource('sqs', endpoint_url='http://localhost:4566')

# The number of sensors is equal to the surface of the lake divided 25, the objective is to have a sensor every 25 km^2
lakes = [('Garda', 10), ('Maggiore', 8), ('Como', 6), ('Tresimeno', 5), ('Bolsena', 5)]

for lake, device_id in lakes:
	queue = sqs.get_queue_by_name(QueueName=lake)
	measure_date = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
	for i in range(device_id):
			water_level = random.randint(10, 200)
			msg_body = '{"device_id": "%s_%s","measure_date": "%s","lake": "%s","water_level": "%s"}' \
				% (lake, str(i), measure_date, lake, str(water_level))
			print(msg_body)
			queue.send_message(MessageBody=msg_body)
