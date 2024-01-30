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
    
    # Append the test block to the root page
    response = portal.append_block_children(rootpage["id"], [test_block])
    
    # Assert that the block was added successfully
    assert response is not None
    assert response["object"] == "list"
    assert len(response["results"]) > 0
    assert response["results"][0]["object"] == "block"

    # Clean up: Remove the test block
    portal.remove_block(rootpage["id"], response["results"][0]["id"])
