from Flare import integration
from Flare.integration import Integration, portal

portal = integration.Integration()

def UnitTestOne():
  
  root_page = portal.get_page(portal.rootuuid)
  index_database = portal.get_database(portal.indexID)
  print("Root Page:", root_page)
  print("Index Database:", index_database)

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

     
