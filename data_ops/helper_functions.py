import requests
import json
import os
from operator import itemgetter
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


MY_AIRTABLE_API_KEY = os.environ.get('MY_AIRTABLE_API_KEY')


def query_airtable_data_by_name(first_name, last_name):
	# player_data will be a list of lists where inner list is of the format [player_name, date, pattern]
	player_data = list()
	# fetch all the data from airtable
	data = fetch_data()
	# check to see if there was an error when fetching the data
	if data == 0:
		return 0

	for result in data:
		# check to make sure the data matches the format
		if result['fields']['Notes'].startswith("http://dataops.risesci.com/#/player-page/"):
			# check to see if player name is in the records 
			if (first_name in (result['fields']['Notes'].lower()) 
				and last_name in (result['fields']['Notes'].lower())):
				# from the url, extract the player name and the date
				parsed_url = parse_url(result['fields']['Notes'])
				player_name = parsed_url[0] + " " + parsed_url[1]
				date = parsed_url[2]
				# See if there is a pattern listed in the record, otherwise set pattern to "Blank"
				if result['fields'].get('Todo'):
					pattern = result['fields']['Todo']
				else:
					pattern = "Blank"
				# append data from each instance into player_data
				temp_data = [player_name, date, pattern, find_pattern_color(pattern)]
				player_data.append(temp_data)
	return sorted(player_data, key=itemgetter(1))


def fetch_data():
	records = list()
	try:
		url = 'https://api.airtable.com/v0/appRUJxLeYv9hlyIp/Table%201?api_key=' + MY_AIRTABLE_API_KEY 
		r = requests.get(url)
		data = json.loads(r.text)
		records += data['records']
		while data.get('offset'):
			r = requests.get(url, params={'offset': data.get('offset')})
			data = json.loads(r.text)
			records += data['records']
	except requests.exceptions.RequestException as e:  # This is the correct syntax
		return 0
	return records


def parse_url(url):
	return url.split('/')[-3:]


def find_pattern_color(pattern):
	if pattern == "Blank" or pattern.startswith("No Pattern"):
		return "default"
	elif pattern.startswith('Pattern One'):
		return "danger"
	elif pattern.startswith("Pattern Two"):
		return "warning"
	elif pattern.startswith("Pattern Three"):
		return "success"
	elif pattern.startswith("Pattern Four"):
		return "info"
	elif pattern.startswith("Pattern Five"):
		return "active"
	else:
		return "default"
