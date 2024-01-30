from Flare import integration
from Flare.integration import Integration, portal

root_page = portal.get_entity("pages", portal.rootuuid)
index_database = portal.get_entity("databases", portal.indexID)

def UnitTestOne():
    # Assert that the root page and index database were retrieved successfully
    assert root_page is not None
    assert index_database is not None
    print("Root Page:", root_page)

def UnitTestTwo():
    test_block = {
        "type": "paragraph",
        "paragraph": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": "test"
                    }
                }
            ]
        }
    }
    
     response = portal.append_block_children(portal.rootuuid, [test_block])

# Assert that the block was added successfully
    assert response is not None
    assert response["object"] == "list"
    assert len(response["results"]) > 0
    assert response["results"][0]["object"] == "block"

# Store the UUID of the appended block
    if response["results"][0]["id"] == portal.rootuuid:
    # If the appended block is the root block, find the UUID of the last child
        children = portal.get_entity("block", portal.rootuuid, recursive=True)['children']
        assert len(children) > 0
        testblock.id = children[-1]["id"]
    else:
        testblock.id = response["results"][0]["id"]

# Clean up: Remove the test block if it's not the root block
    if testblock.id != portal.rootuuid:
        portal.remove_block(testblock.id, response["results"][0]["id"])
