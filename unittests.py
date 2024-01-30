from Flare import integration
from Flare.integration import Integration, portal


def UnitTestOne():
    root_page = portal.get_entity("pages", portal.rootuuid)
    index_database = portal.get_entity("databases", portal.indexID)
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
    portal.append_block_children(rootpage["id"], [test_block])

     
