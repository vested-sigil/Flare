from Flare import integration
from Flare.integration import Integration, portal

root_page = portal.get_entity("pages", portal.rootuuid)
index_database = portal.get_entity("databases", portal.indexID)

def UnitTestOne():
    
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
    portal.append_block_children(portal.rootuuid, [test_block])

     
