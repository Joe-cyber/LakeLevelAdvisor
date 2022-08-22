import requests
import boto3
import datetime
import json
import datetime 
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")

table_name = "Lakes"

lakes = ['Garda', 'Maggiore', 'Como', 'Tresimeno', 'Bolsena']

table = dynamodb.Table(table_name)
key = "eULRB3yHmiztaKV6kWLRFPyAMZG-O614StHh_lnrcaO"
url = "https://maker.ifttt.com/trigger/dangerous-water-level/with/key/"+key

LOW = 100
HIGH = 150

def lambda_handler(event, context):
	for lake in lakes:
		try:
			response = table.get_item(Key={'lake': lake})
		except ClientError as e:
			print(e.response['Error']['Message'])
		if float(response['Item']['avarage_water_level']) < LOW:
			req = requests.post(url, json={"value1": lake, "value2": response['Item']['avarage_water_level'], "value3": "low"})
		elif float(response['Item']['avarage_water_level']) > HIGH:
			req = requests.post(url, json={"value1": lake, "value2": response['Item']['avarage_water_level'], "value3": "high"})
		
	   		
