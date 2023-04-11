import json


class ed_catalog_requests:
	'''Parse the json to dictionary for subsequent use'''
	def get_dict_from_json_catalog(self, json_input):
		data = json.loads(json_input)
		result = {}
		# Loop through each item in the array
		for record in data:
			if 'id' in record:
				id_value = record['id']
				if "assets" in record:
					item_dict = {'status': record['status'], 'assets': record.get('assets', [])}
				else:
					item_dict = {'status': record['status']}

				result[id_value] = item_dict

		for key, value in result.items():
			print(f'{key}: {value}')
		return result


catalog_request = ed_catalog_requests()
