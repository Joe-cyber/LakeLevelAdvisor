from pprint import pprint
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")

table_name = "Lakes"

print("Hi, this is the Lake Level Advisor application.")
print("Enter the name of one or more lakes you want to know the water level")
lakes = input("(lakes must be separated by one space):\n")
lakes = lakes.split()
table = dynamodb.Table(table_name)
print("------------------------------------------------------------------------------------------------")
for lake in lakes:
	try:
		response = table.get_item(Key={'lake': lake})
	except ClientError as e:
		print(e.response['Error']['Message'])

	print("Average water level in %s is %s" % (response['Item']['lake'], response['Item']['avarage_water_level']))
	print("Maximum water level in %s is %s" % (response['Item']['lake'], response['Item']['max_water_level']))
	print("Minimum water level in %s is %s" % (response['Item']['lake'], response['Item']['min_water_level']))
	print("-measured at %s" % (response['Item']['measure_date']))
	print("--based on the following devices", response['Item']['device_id'])
	print("------------------------------------------------------------------------------------------------")
