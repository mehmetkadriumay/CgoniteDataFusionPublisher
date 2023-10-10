from cognite.client import CogniteClient
c = CogniteClient(api_key="<APIKey>", client_name="cedar", project="publicdata")

from cloudevents.http import CloudEvent, to_structured
import requests

import time

# Import required libraries
import json


# Create a CloudEvent
# - The CloudEvent "id" is generated if omitted. "specversion" defaults to "1.0".

for event in c.events:
    time.sleep(1)
    if not (event.external_id is None):
        attributes = {
        "type": event.type,
        "subtype": event.subtype,
        "external_id": event.external_id,
        "source": event.source,
        }
        data = event.metadata,
        cncf_event = CloudEvent(attributes, data)
        # Create Python object from JSON string data

        cncf_event_string=repr(cncf_event).replace("\'","\"").replace("(","").replace(",)","")

        #print(str(cncf_event))
        #print(cncf_event_string)
        obj = json.loads(cncf_event_string)

        # Pretty Print JSON
        json_formatted_str = json.dumps(obj, indent=4)
        print(json_formatted_str)
        #print(cncf_event)
