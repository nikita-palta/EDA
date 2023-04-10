import json
import time
import allure
import requests
import wget
from ed_catalog_requests import catalog_request
from ed_product_requests import product_request
from properties import properties as prop


class ed_general_operations:

	def get_api_response(self, url):
		failures = []
		response = (requests.get(url))
		if response.status_code == 200:
			response = response.json()
		else:
			failures.append(f"Error retrieving data from {url}. Status code: {response.status_code}")
		return response, failures

	def compare_record_status(self, prev_result, current_result, complete_status_labels, incomplete_status_labels):
		workflow_complete = []
		workflow_incomplete = []
		message = []
		for id, details in prev_result.items():
			if id in current_result.keys():
				current_state = current_result.get(id).get('status')
				if current_state in complete_status_labels:
					workflow_complete.append(id)
				elif current_state in incomplete_status_labels:
					workflow_incomplete.append(id)
				else:
					message.append(f'{current_state} is not handled by testflow')
		if len(workflow_complete) == len(prev_result.keys()):
			return (True, message, workflow_complete, workflow_incomplete)
		else:
			return (False, message, workflow_complete, workflow_incomplete)

	def get_and_conclude_work_status(self, url, initial_response, complete_status_labels, incomplete_status_labels,
	                                 work):
		failures = []
		retry_count = 1
		while retry_count <= prop.max_retry:
			with allure.step(f'Wait for {prop.retry_time}secs'):
				time.sleep(prop.retry_time)
			with allure.step(f'Query the records from API request after {prop.retry_time}sec'):
				current_records, message = general_operations.get_api_response(url)
				if message:
					failures.append(f'Unable to fetch api response on retry {retry_count} due to {message}')
				else:
					allure.attach(json.dumps(current_records, indent=4), 'Catalog Response')
			with allure.step("Get id and status for each record"):
				if (work == 'catalog'):
					current_response = catalog_request.get_dict_from_json_catalog(json.dumps(current_records))
				if (work == 'product'):
					current_response = product_request.get_dict_from_json_product(json.dumps(current_records))
			with allure.step('Check if the status is completed/Failed for all previous records'):
				(status, message, completed_id_list, incomplete_id_list) = general_operations.compare_record_status(
					initial_response, current_response, complete_status_labels, incomplete_status_labels)
				if status == False:
					with allure.step(f'Retry {retry_count} as all existing records are not completed yet'):
						allure.attach(f'{str(incomplete_id_list)}', f'Incomplete Id on retry{retry_count}')
						retry_count += 1
				else:
					break
		if status == False:
			failures.append(f'{work} work status did not complete in {retry_count} retries')
		return status, failures, completed_id_list, incomplete_id_list, current_response

	def check_and_get_assets(self,response):
		failures = []
		asset_details = {}
		for id, details in response.items():
			if details.get('status') == 'complete':
				assets = details.get('assets')
				if not assets:
					failures.append(f'Asset not found for {id}')
				else:
					asset_details[id] = assets
		return failures,asset_details

	def download_assets(self,asset_details):
		failures = []
		print(type(asset_details))

		for id, assets in asset_details.items():
			i = 1
			for url in assets:
				print(url)
				filename = f'{prop.path_to_download}'
				wget.download(url,out=filename)
				i+=1
general_operations = ed_general_operations()
