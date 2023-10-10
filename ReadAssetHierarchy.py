from cognite.client import CogniteClient
from treelib import Node, Tree
tree = Tree()

c = CogniteClient(api_key="<APIKey>", client_name="cedar", project="publicdata") 
res2 = c.assets.retrieve_subtree(id=4650652196144007, depth=50)
tree.create_node("Valhall Platform", 4650652196144007)

for asset in res2:
    if not asset.id == 4650652196144007:
        tree.create_node(asset.name + ":" + asset.description, asset.id, parent=4650652196144007)
        #print("root_asset_id:" + "4650652196144007")
        #print("child_asset_id:" + str(asset.id))
        #print("child_asset_name:" + asset.name)
        #print("child_asset_parent_id:" + str(asset.parent_id))
        #print("child_asset_description:" + asset.description)

for asset in res2:
    if not asset.id == 4650652196144007:
        tree.move_node(asset.id, asset.parent_id)

tree.show()
