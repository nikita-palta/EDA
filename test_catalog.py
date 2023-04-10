import json
import time
import allure
import pytest
from ed_aws_operations import aws
from ed_catalog_requests import catalog_request
from ed_general_operations import general_operations
from ed_product_requests import product_request
from properties import properties as prop


@pytest.fixture(scope="function", autouse=False)
def upload_file_to_aws():
	with allure.step('Upload the file'):
		aws.get_bucket_list()
		aws.upload_file_to_s3(prop.bucket_name, prop.file_name)

@pytest.mark.parametrize(
	"catalog_url",
	[
		pytest.param(prop.mock_catalog_url_completed,id="Expected to complete successfully"),
		pytest.param(prop.mock_catalog_url_incomplete,id="Expected Failure as workflow won't complete"),
	],
)
@pytest.mark.P1
@allure.testcase('Check that the catalog workflow works as expected')
@allure.title('Check that the catalog workflow works as expected')
def test_catalog_flow_state_completes(catalog_url):
	failures = []
	with allure.step("Query the records from the catalog request"):
		prev_records, message = general_operations.get_api_response(url=prop.catalog_url)
		if message:
			failures.append(failures)
		else:
			allure.attach(json.dumps(prev_records, indent=4), 'Catalog Response')
	with allure.step("Get id and status for each record"):
		original_response = catalog_request.get_dict_from_json_catalog(json.dumps(prev_records))
	with allure.step('Check work status is complete'):
		(status, message, completed_id_list, incomplete_id_list,
		 current_record) = general_operations.get_and_conclude_work_status(
			catalog_url, original_response, prop.catalog_completed_status_labels,
			prop.catalog_incomplete_status_labels, 'catalog')
		if status is False:
			failures.append(message)
	with allure.step('Check each completed request has an asset'):
		message, asset_details = general_operations.check_and_get_assets(current_record)
		if message != []:
			failures.append(message)
	with allure.step('Download the product assets'):
		general_operations.download_assets(asset_details)
	with allure.step('Check for failures'):
		allure.attach(str(failures), 'Failure message: ')
		assert not failures, failures


@pytest.mark.P1
@allure.testcase('Check that the product workflow works as expected')
@allure.title('Check that the product workflow works as expected')
@pytest.mark.parametrize(
	"product_url",
	[
		pytest.param(prop.mock_product_url_completed,id="Expected to complete successfully"),
		pytest.param(prop.mock_product_url_incomplete,id="Expected Failure as workflow won't complete"),
	],
)
def test_product_flow_state_completes(product_url):
	failures = []
	with allure.step("Query the records from the product request"):
		prev_records, message = general_operations.get_api_response(url=prop.product_url)
		if message:
			failures.append(message)
		else:
			allure.attach(json.dumps(prev_records, indent=4), 'Product API Response')
	with allure.step("Get id and status for each record"):
		original_response = product_request.get_dict_from_json_product(json.dumps(prev_records))
	with allure.step('Check work status is complete'):
		(status, message, completed_id_list, incomplete_id_list,
		 current_record) = general_operations.get_and_conclude_work_status(
			product_url, original_response, prop.product_completed_status_labels,
			prop.product_incomplete_status_labels, 'product')
		if status is False:
			failures.append(message)
	with allure.step('Check each completed request has an asset'):
		message, asset_details = general_operations.check_and_get_assets(current_record)
		if message != []:
			failures.append(message)
	with allure.step('Download the product assets'):
		general_operations.download_assets(asset_details)
	with allure.step('Check for failures'):
		allure.attach(str(failures), 'Failure message: ')
		assert not failures, failures


@pytest.mark.P1
@allure.testcase('Check that the successful catalog records ONLY appear in product work')
@allure.title('Check that the successful catalog records ONLY appear in product work')
@pytest.mark.parametrize(
	"product_url",
	[
		pytest.param(prop.mock_product_url_completed,id="Expected to complete successfully"),
		pytest.param(prop.mock_product_url_incomplete,id="Expected Failure as workflow wont complete"),
	],
)
def test_workflow_completed_records_appear_in_product_workflow(product_url):
	failures = []
	with allure.step("Query the records from the catalog request"):
		prev_records, message = general_operations.get_api_response(url=prop.catalog_url)
		if message:
			failures.append(message)
		else:
			allure.attach(json.dumps(prev_records, indent=4), 'Catalog Response')
	with allure.step("Get id and status for each record"):
		original_response = catalog_request.get_dict_from_json_catalog(json.dumps(prev_records))
	with allure.step('Check catalog work status is complete'):
		(status, message, completed_id_list, incomplete_id_list,
		 current_record) = general_operations.get_and_conclude_work_status(
			prop.mock_catalog_url_completed, original_response, prop.catalog_completed_status_labels,
			prop.catalog_incomplete_status_labels, 'catalog')
	with allure.step("Query the records from the product request"):
		initial_product_records, message = general_operations.get_api_response(url=prop.product_url)
		if message:
			failures.append(message)
		else:
			allure.attach(json.dumps(initial_product_records, indent=4), 'Product API Response')
	with allure.step("Get id and status for each record"):
		initial_product_response = product_request.get_dict_from_json_product(json.dumps(initial_product_records))

	with allure.step('Check that only completed records from catalog exist in product response'):
		expected_product_id_list = []
		for id in completed_id_list:
			if current_record.get(id).get('status') != 'failed':
				expected_product_id_list.append(id)
		allure.attach(f'{expected_product_id_list}', 'Expected list of ids in product api')
		input_id_list = []
		for id, details in initial_product_response.items():
			input_id_list.append(details['input_id'])
		for id in expected_product_id_list:
			if id not in input_id_list:
				failures.append(f'Expected {id} in product response but got {initial_product_response}')
	with allure.step('Check that failed records from catalog work do not exist in product response'):
		for id in incomplete_id_list:
			if id in input_id_list:
				failures.append(f'{id} not expected in product response but got {initial_product_response}')
	with allure.step('Check product work status is complete'):
		(status, message, completed_id_list, incomplete_id_list,
		 current_record) = general_operations.get_and_conclude_work_status(product_url, initial_product_response, prop.product_completed_status_labels,
			prop.product_incomplete_status_labels, 'product')
		if status is False:
			failures.append(message)
	with allure.step('Check each completed request has an asset'):
		message, asset_details = general_operations.check_and_get_assets(current_record)
		if message != []:
			failures.append(message)
	with allure.step('Download the product assets'):
		general_operations.download_assets(asset_details)
	with allure.step('Check for failures'):
		print(failures)
		allure.attach(str(failures), 'Failure message: ')
		assert not failures, failures


@pytest.mark.P1
@allure.testcase('Check that the entire workflow completes in 180 sec')
@allure.title('Check that the entire workflow completes in 180 sec')
@pytest.mark.timeout(180)
def test_workflow_efficiency(upload_file_to_aws):
	test_workflow_completed_records_appear_in_product_workflow(prop.mock_product_url_completed)

