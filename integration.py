import requests
import json
import logging
from google.colab import userdata
from msgspec.json import decode
from tenacity import retry, stop_after_attempt, wait_exponential
from Flare.blocks import Block, extract_info

# Improved logging setup
logging.basicConfig(level=logging.INFO)

class Integration:
    def __init__(self, token, indexID, rootuuid, config):
        self.token = token
        self.indexID = indexID
        self.rootuuid = rootuuid
        self.default_page_id = self.rootuuid
        self.base_url = config['API_BASE_URL']
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": config['API_VERSION']
        }

    @retry(stop=stop_after_attempt(3), wait=wait_exponential())
    def _make_request(self, method: str, endpoint: str, params=None, json=None) -> dict:
        try:
            response = requests.request(method, self.base_url + endpoint, headers=self.headers, params=params, json=json)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Failed to make request {method} {endpoint}: {str(e)}")
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_exponential())
    def get_entity(self, entity_type: str, entity_id: str, recursive=False) -> dict:
        entity = self._make_request("GET", f"/{entity_type}/{entity_id}")

        if recursive and 'has_more' in entity and entity['has_more']:
            entity['children'] += self.get_entity(entity_type, entity_id, recursive=recursive)['children']

        return entity
    @retry(stop=stop_after_attempt(3), wait=wait_exponential())
    def remove_block(self, block_id: str) -> dict:
        if not block_id:
            raise ValueError("Block ID cannot be empty")
        try:
            response = self._make_request("DELETE", f"/blocks/{block_id}")
            return response
        except requests.RequestException as e:
            logging.error(f"Failed to remove block {block_id}: {str(e)}")
            raise
    @retry(stop=stop_after_attempt(3), wait=wait_exponential())
    def get_block(self, block_id: str) -> Block:
        if not block_id:
            raise ValueError("Block ID cannot be empty")
        try:
            response = requests.get(f"{self.base_url}/blocks/{block_id}", headers=self.headers)
            response.raise_for_status()
            return decode(response.content, type=Block)
        except requests.RequestException as e:
            logging.error(f"Failed to get block {block_id}: {str(e)}")
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_exponential())
    def update_row(self, database_id: str, page_id: str, row_properties: dict) -> dict:
        if not database_id or not page_id:
            raise ValueError("Database ID and Page ID cannot be empty")
        try:
            response = self._make_request("PATCH", f"/pages/{page_id}", json={"properties": row_properties})
            return response
        except requests.RequestException as e:
            logging.error(f"Failed to update row in database {database_id}: {str(e)}")
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_exponential())
    def create_page(self, parent_id: str, title: str, content=None) -> dict:
        payload = {
            "parent": {"page_id": parent_id},
            "properties": {"title": {"title": [{"text": {"content": title}}]}},
        }
        if content:
            payload["children"] = content
        response = self._make_request("POST", "/pages", json=payload)
        return response

    @retry(stop=stop_after_attempt(3), wait=wait_exponential())
    def append_block_children(self, block_id: str, children: list) -> dict:
        response = self._make_request("PATCH", f"/blocks/{block_id}/children", json={"children": children})
        return response

# Example usage
config = {
    'API_BASE_URL': "https://api.notion.com/v1",
    'API_VERSION': "2022-06-28"
}
portal = Integration(token=userdata.get('token'), indexID=userdata.get('indexID'), rootuuid=userdata.get('rootuuid'), config=config)

# Example function call
rootpage = portal.get_entity("pages", portal.default_page_id)
print("Root page of integration")
print(json.dumps(rootpage, indent=4))
