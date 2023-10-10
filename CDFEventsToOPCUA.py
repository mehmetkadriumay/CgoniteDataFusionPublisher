from cognite.client import CogniteClient
c = CogniteClient(api_key="<APIKey>", client_name="cedar", project="publicdata")

import time
from opcua import ua, Server


server = Server()
server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

# get Objects node, this is where we should put our custom stuff
objects = server.get_objects_node()

uri = "http://cedar.microsoft.com"
idx = server.register_namespace(uri)

# populating our address space
myobj = objects.add_object(idx,"Business Events")

custom_etype = server.nodes.base_event_type.add_object_type(1, 'BusinessEvents')

custom_etype.add_property(1, 'type', ua.Variant(True, ua.VariantType.String))
custom_etype.add_property(1, 'subtype', ua.Variant(True, ua.VariantType.String))
custom_etype.add_property(1, 'external_id', ua.Variant(True, ua.VariantType.String))
custom_etype.add_property(1, 'source', ua.Variant(True, ua.VariantType.String))
#custom_etype.add_property(1, 'createdtime', ua.Variant(True, ua.VariantType.String))
#custom_etype.add_property(1, 'lastupdatedtime', ua.Variant(True, ua.VariantType.String))

evgen = server.get_event_generator(custom_etype, myobj)

# starting!
server.start()

try:
    for event in c.events:
        time.sleep(1)
        if not (event.external_id is None):
            evgen.event.type = event.type
            evgen.event.subtype = event.subtype
            evgen.event.external_id = event.external_id
            evgen.event.source = event.source
            #evgen.event.startime = event.created_time
            #evgen.event.endtime = event.last_updated_time
            evgen.trigger()
finally:
    server.stop()
