import json


class ed_product_requests:

	def get_dict_from_json_product(self, json_input):
		data = json.loads(json_input)
		result = {}
		# Loop through each item in the array
		for record in data:
			if 'id' in record:
				id_value = record['id']
				if "assets" in record:
					item_dict = {'input_id': record['input_id'], 'status': record['status'],
					             'assets': record.get('assets', [])}
				else:
					item_dict = {'input_id': record['input_id'], 'status': record['status']}

				result[id_value] = item_dict

		for key, value in result.items():
			print(f'{key}: {value}')
		return result


product_request = ed_product_requests()
