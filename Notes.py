from notion_client import Client
from notion_client.helpers import collect_paginated_api


from google.colab import userdata

token = userdata.get('token')
rootuuid = userdata.get('rootuuid')
    
class Notes:
    def __init__(self):
        self.client = Client(token)

    def retrieve_block(self, block_id):
        return self.client.blocks.retrieve(block_id=block_id)

    def update_block(self, block_id, block_data):
        return self.client.blocks.update(block_id=block_id, **block_data)

    def append_child_blocks(self, block_id, children):
        return self.client.blocks.children.append(block_id=block_id, children=children)

    def query_database(self, database_id, filter=None, sorts=None):
        payload = {"database_id": database_id}
        if filter is not None:
            payload["filter"] = filter
        if sorts is not None:
            payload["sorts"] = sorts
        return self.client.databases.query(**payload)

    def retrieve_page(self, page_id):
        return self.client.pages.retrieve(page_id=page_id)

    def update_page_properties(self, page_id, properties):
        return self.client.pages.update(page_id=page_id, properties=properties)
    @staticmethod
    def help():
        help_text = """
        Available methods in the Notes class:
        
        - retrieve_block(block_id): Retrieve a block using its ID.
        - update_block(block_id, block_data): Update a block with new data.
        - append_child_blocks(block_id, children): Append child blocks to a parent block.
        - query_database(database_id, filter=None, sorts=None): Query a database.
        - retrieve_page(page_id): Retrieve a page using its ID.
        - update_page_properties(page_id, properties): Update page properties.
        
        For more detailed information on each method, please refer to the Notion API documentation.
        """
        print(help_text)
