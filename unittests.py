from Flare import integration
from Flare.integration import Integration, portal

root_page = portal.get_entity("pages", portal.rootuuid)
index_database = portal.get_entity("databases", portal.indexID)
testblock = {'id': None}

def create_test_block():
    test_block_content = {
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"type": "text", "text": {"content": "test block"}}]
        }
    }
    response = portal.append_block_children(portal.rootuuid, [test_block_content])
    return response['results'][0]['id']

def UnitTestOne():
    # Assert that the root page and index database were retrieved successfully
    assert root_page is not None
    assert index_database is not None
    print("Root Page:", root_page)

def UnitTestTwo():
    # Create a single test block
    test_block_id = create_test_block()

    # Modify the test block
    modified_content = "modified test"
    modified_block = {
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"type": "text", "text": {"content": modified_content}}]
        }
    }
    portal.update_block(test_block_id, modified_block)

    # Retrieve and assert the modified block's content
    modified_block_retrieved = portal.get_block(test_block_id)
    assert modified_block_retrieved is not None
    assert modified_block_retrieved.object == "block"
    assert modified_block_retrieved.id == test_block_id
    assert "modified test" in modified_block_retrieved.content  # Assuming 'content' is the correct field

    # Append a nested block to the modified block
    nested_block = {
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"type": "text", "text": {"content": "nested test"}}]
        }
    }
    portal.append_block_children(test_block_id, [nested_block])

    # Retrieve and assert the nested block's presence
    block_with_nested = portal.get_block(test_block_id)
    assert block_with_nested is not None
    assert "nested test" in block_with_nested.content  # Assuming 'content' includes nested block content

    # Remove the test block
    remove_response = portal.remove_block(test_block_id)
    assert remove_response is not None
    assert remove_response["object"] == "block"
    assert remove_response["deleted"] == True
