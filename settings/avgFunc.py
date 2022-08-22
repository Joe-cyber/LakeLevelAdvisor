import boto3
import datetime
import json

def lambda_handler(event, context):
	sqs = boto3.resource('sqs', endpoint_url='http://localhost:4566')
	dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")

	table = dynamodb.Table('Lakes')

	lakes = ['Garda', 'Maggiore', 'Como', 'Tresimeno', 'Bolsena']

	for lake in lakes:
		queue = sqs.get_queue_by_name(QueueName=lake)
		messages = []
		while True:
			response = queue.receive_messages(MaxNumberOfMessages=10, VisibilityTimeout=10, WaitTimeSeconds=10)
			if response:
				messages.extend(response)
				device_ids = ""
				avg_water_level = 0
				min_water_level = 201
				max_water_level = 0
				last_measured_data = datetime.datetime.combine(datetime.date.min, datetime.datetime.min.time())
				for message in messages:
					content = json.loads(message.body)
					device_ids = device_ids + content["device_id"] + " "

					measure_data = datetime.datetime.strptime(content["measure_date"], "%Y-%m-%d %H:%M:%S")
					if measure_data > last_measured_data:
						last_measured_data = measure_data
					water_level = int(content["water_level"])
					avg_water_level += water_level
					if max_water_level < water_level:
						max_water_level = water_level
					if min_water_level > water_level:
						min_water_level = water_level
					message.delete()

				avg_water_level = avg_water_level / len(messages)
				item = {
					'lake': lake,
					'measure_date': str(last_measured_data), 
					'avarage_water_level': str(avg_water_level),
					'max_water_level': str(max_water_level),
					'min_water_level': str(min_water_level),
					'device_id': device_ids
				}
				table.put_item(Item=item)
			else:
				break	
