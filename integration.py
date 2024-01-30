import requests
import logging
from requests.exceptions import RequestException
from tenacity import retry, stop_after_attempt, wait_exponential
from google.colab import userdata
from blocks import Block, extract_info, serialize_block, deserialize_block

# Constants for API methods and endpoints
METHOD_GET = "GET"
ENDPOINT_PAGES = "/pages/"
ENDPOINT_DATABASES = "/databases/"
ENDPOINT_BLOCKS = "/blocks/"

# Setting up basic logging
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s')

class Integration:
    def __init__(self):
        self.token = userdata.get('token')
        self.indexID = userdata.get('indexID')
        self.rootuuid = userdata.get('rootuuid')
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": "2022-06-28"
        }

    def _log_request(self, method, url, params=None, body=None):
        logging.debug(f"Making {method} request to {url} | Params: {params} | Body: {body}")

    def _log_response(self, response):
        logging.debug(f"Received response - Status: {response.status_code} | Content: {response.text}")

    def _make_request(self, method, endpoint, params=None, json=None):
        url = self.base_url + endpoint
        self._log_request(method, url, params, json)
        try:
            response = requests.request(method, url, headers=self.headers, params=params, json=json)
            response.raise_for_status()
            self._log_response(response)
            return response.json()
        except RequestException as req_err:
            logging.error(f"Request error: {req_err} | URL: {url}")
            raise
        except Exception as err:
            logging.error(f"Unexpected error: {err} | URL: {url}")
            raise
    def get_and_process_block(self, block_id: str) -> dict:
        """
        Retrieves a block using its ID and processes it to extract information.

        :param block_id: The ID of the block to retrieve and process.
        :return: A dictionary containing processed information about the block.
        """
        try:
            # Retrieve the block data using the existing get_block method
            block = self.get_block(block_id)

            # Process the block using functionality from the blocks module
            # For demonstration, we use the extract_info function
            processed_info = extract_info(block)

            return processed_info

        except Exception as e:
            logging.error(f"Error in get_and_process_block: {e}")
            return {"error": str(e)}
    @retry(stop=stop_after_attempt(3), wait=wait_exponential())
    def get_page(self, page_id: str) -> dict:
        return self._make_request(METHOD_GET, ENDPOINT_PAGES + page_id)

    def get_database(self, database_id: str) -> dict:
        return self._make_request(METHOD_GET, ENDPOINT_DATABASES + database_id)

    def get_block(self, block_id: str) -> Block:
        block_data = self._make_request(METHOD_GET, ENDPOINT_BLOCKS + block_id)
        return deserialize_block(block_data)

    def update_block(self, block_id: str, block: Block) -> dict:
        serialized_block = serialize_block(block)
        return self._make_request("PATCH", ENDPOINT_BLOCKS + block_id, json=serialized_block)

    def create_page(self, parent_id: str, title: str, content: list[Block] = None) -> dict:
        children = [serialize_block(block) for block in content] if content else []
        payload = {
            "parent": {"database_id": parent_id},
            "properties": {"title": [{"type": "text", "text": {"content": title}}]},
            "children": children
        }
        return self._make_request("POST", ENDPOINT_PAGES, json=payload)

    def query_database(self, database_id: str, filter: dict = None, sorts: list = None) -> dict:
        query = {"filter": filter, "sorts": sorts} if filter or sorts else {}
        return self._make_request("POST", ENDPOINT_DATABASES + database_id + "/query", json=query)

    def fetch_paginated_data(self, endpoint, params=None, page_size=100):
        """
        Fetches data from a given Notion API endpoint with cursor-based pagination.
        :param endpoint: The API endpoint to fetch the data from.
        :param params: Additional parameters to pass in the request.
        :param page_size: Number of items to fetch per page.
        :return: A list of all items fetched from the endpoint.
        """
        if params is None:
            params = {}

        all_data = []
        has_more = True
        start_cursor = None

        while has_more:
            paginated_params = {**params, "page_size": page_size, "start_cursor": start_cursor}
            response = self._make_request("GET", endpoint, params=paginated_params)
            all_data.extend(response.get('results', []))
            
            has_more = response.get('has_more', False)
            start_cursor = response.get('next_cursor')

        return all_data

# Example usage
# integration = Integration()
# root_page = integration.get_page(integration.rootuuid)
# index_database = integration.get_database(integration.indexID)

# print("Root Page:", root_page)
# print("Index Database:", index_database)
