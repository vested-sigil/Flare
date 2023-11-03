import json
import requests

def load_config(file):
    with open(file, 'r') as f:
        return json.load(f)

def save_config(config, file):
    with open(file, 'w') as f:
        json.dump(config, f, indent=4)

def fetch_schema(server_url, app_id, master_key):
    headers = {
        "X-Parse-Application-Id": app_id,
        "X-Parse-Master-Key": master_key,
        "Content-Type": "application/json"
    }
    response = requests.get(f"{server_url}/schemas", headers=headers)
    return response.json()

def map_classes(schema):
    return {cls['className']: cls['fields'] for cls in schema['results']}

def grab(obj):
    return {"key": f"value from server for {obj}"}

def update_cells():
    return {"cell_a": "new_data_a", "cell_b": "new_data_b"}
import json
from noteable import get_content, update_cell, create_cell, run_cell

def load_config(file='config.json'):
    with open(file, 'r') as f:
        return json.load(f)

def save_config(config, file='config.json'):
    with open(file, 'w') as f:
        json.dump(config, f, indent=4)

def fetch_from_noteable_cell(notebook_id, cell_id):
    return get_content(file_id=notebook_id, after_cell_id=cell_id)

def update_noteable_cell(notebook_id, cell_id, new_content):
    update_cell(file_id=notebook_id, cell_id=cell_id, source=new_content)

def create_new_noteable_cell(notebook_id, cell_type, source, before_cell_id=None):
    create_cell(file_id=notebook_id, cell_type=cell_type, source=source, before_cell_id=before_cell_id)

def run_noteable_cell(notebook_id, cell_id):
    run_cell(file_id=notebook_id, cell_id=cell_id)
class Cell:
    def __init__(self, notebook_id, cell_id):
        self.notebook_id = notebook_id
        self.cell_id = cell_id
        self.content = None

    async def load(self):
        response = await get_content(file_id=self.notebook_id, after_cell_id=self.cell_id)
        if response['status'] == 'success':
            self.content = response['data']['content']
        else:
            raise Exception(f"Failed to load content for cell {self.cell_id}: {response['error']}")

    async def edit(self, new_content):
        response = await update_cell(file_id=self.notebook_id, cell_id=self.cell_id, source=new_content)
        if response['status'] == 'success':
            self.content = new_content
        else:
            raise Exception(f"Failed to update content for cell {self.cell_id}: {response['error']}")

    async def run(self):
        response = await run_cell(file_id=self.notebook_id, cell_id=self.cell_id)
        if response['status'] != 'success':
            raise Exception(f"Failed to run cell {self.cell_id}: {response['error']}")
import json
import asyncio

# Helper functions for interacting with Noteable
async def get_content_helper(notebook_id, cell_id):
    try:
        response = await noteable.get_content(file_id=notebook_id, after_cell_id=cell_id)
        if response['status'] == 'success':
            return response['data']['content']
        else:
            raise Exception(f"Failed to get content: {response['error']}")
    except Exception as e:
        print(f"Error getting content: {e}")
        return None

async def update_cell_helper(notebook_id, cell_id, new_content):
    try:
        response = await noteable.update_cell(file_id=notebook_id, cell_id=cell_id, source=new_content, and_run=False)
        if response['status'] == 'success':
            return True
        else:
            raise Exception(f"Failed to update cell: {response['error']}")
    except Exception as e:
        print(f"Error updating cell: {e}")
        return False

async def run_cell_helper(notebook_id, cell_id):
    try:
        response = await noteable.run_cell(file_id=notebook_id, cell_id=cell_id)
        if response['status'] == 'success':
            return True
        else:
            raise Exception(f"Failed to run cell: {response['error']}")
    except Exception as e:
        print(f"Error running cell: {e}")
        return False

# Load configuration from file
def load_config(file='config.json'):
    try:
        with open(file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Save configuration to file
def save_config(config, file='config.json'):
    with open(file, 'w') as f:
        json.dump(config, f)

# Main function to demonstrate the use of helper functions
async def main():
    # Load configuration
    config = load_config()
    notebook_id = config.get('notebook_id')
    cell_id = config.get('cell_id')

    # Get content of a cell
    content = await get_content_helper(notebook_id, cell_id)
    print(f"Content of cell {cell_id}: {content}")

    # Update the content of a cell
    new_content = ["print('Hello, World!')"]
    update_success = await update_cell_helper(notebook_id, cell_id, new_content)
    if update_success:
        print(f"Cell {cell_id} updated successfully.")

    # Run the cell
    run_success = await run_cell_helper(notebook_id, cell_id)
    if run_success:
        print(f"Cell {cell_id} ran successfully.")

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())

