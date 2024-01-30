from notion_client import Client
from notion_client.helpers import collect_paginated_api
import os

def is_running_in_notebook():
    try:
        from IPython import get_ipython
        if 'IPKernelApp' not in get_ipython().config:
            raise ImportError("Not running in a notebook")
        return True
    except:
        return False

# Determine the environment and get the tokens and IDs
if is_running_in_notebook():
    from google.colab import userdata
    token = userdata.get('token')
    rootuuid = userdata.get('rootuuid')
    indexID = userdata.get('indexID')
else:
    from dotenv import load_dotenv
    load_dotenv()
    token = os.getenv('NOTION_TOKEN')
    rootuuid = os.getenv('ROOT_UUID')
    indexID = os.getenv('INDEX_ID')

# Initialize the Notion client with the token
notion = Client(auth=token)


class Integration:
    def __init__(self, token, rootuuid, indexID):
        self.client = Client(auth=token)
        self.home = rootuuid
        self.index = indexID
        self.cache = {}

    def retrieve_home_page(self):
        return self.client.pages.retrieve(self.home)

    def check_index(self):
        return self.client.databases.retrieve(self.index)

    def query_database_with_pagination(self, database_id, filter=None, sorts=None):
        return collect_paginated_api(
            self.client.databases.query, database_id=database_id, filter=filter, sorts=sorts
        )

    # Example method to handle rich content like images
    def add_image_to_page(self, page_id, image_url):
        image_block = {
            "type": "image",
            "image": {"type": "external", "external": {"url": image_url}}
        }
        return self.client.blocks.children.append(page_id, children=[image_block])

    # Cache management methods
    def get_cached_data(self, key):
        return self.cache.get(key)

    def set_cache_data(self, key, value):
        self.cache[key] = value

    # Additional methods for page and block manipulation
    def delete_page(self, page_id):
        return self.client.pages.delete(page_id)

    def retrieve_user(self, user_id):
        return self.client.users.retrieve(user_id)

    def search(self, query):
        return self.client.search(query=query)

    def update_block(self, block_id, block_content):
        return self.client.blocks.update(block_id, block=block_content)

    def list_block_children(self, block_id):
        return self.client.blocks.children.list(block_id)

    def delete_all_pages_in_database(self, database_id):
        # First, query all pages in the database
        pages = self.query_database_with_pagination(database_id)

        # Then, iterate over each page and delete it
        for page in pages:
            self.delete_page(page["id"])

        return "All pages deleted from the database."

    def append_block_children(self, block_id, children):
        return self.client.blocks.children.append(block_id, children=children)

    def retrieve_block(self, block_id):
        return self.client.blocks.retrieve(block_id)

# Instantiate Integration class with the retrieved token and IDs
integration = Integration(token, rootuuid, indexID)

# Example usage of the Integration class
home_page = integration.retrieve_home_page()
