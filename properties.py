class properties:
	bucket_name = 'nikita-bucket1'
	file_name = 'test1.txt'

	MockServerURL = 'https://84b93b1c-99fa-4d2f-87f2-f65eb00d93a9.mock.pstmn.io'

	# catalog
	catalog_url = f'{MockServerURL}/input'
	mock_catalog_url_completed = f'{MockServerURL}/input_complete'
	mock_catalog_url_incomplete= f'{MockServerURL}/input_incomplete'
	# mock_catalog_url_completed = catalog_url
	catalog_completed_status_labels = ('complete', 'failed')
	catalog_incomplete_status_labels = ('ingesting')

	# product
	product_url = f'{MockServerURL}/product'
	mock_product_url_completed = f'{MockServerURL}/product_complete'
	mock_product_url_incomplete = f'{MockServerURL}/product_incomplete'
	# mock_product_url_completed = product_url
	product_completed_status_labels = ('complete')
	product_incomplete_status_labels = ('processing')
	retry_time = 2  # in sec
	max_retry = 3
	max_time = 180

	path_to_download = "C:\\Nikita\\Mine\\MyWork\\Pytest_Workspace\\EDA\\download\\"
