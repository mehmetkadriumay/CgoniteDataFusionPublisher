import sys
sys.path.insert(0, "..")
import time
from opcua import ua, Server

server = Server()
server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")
uri = "http://cedar.microsoft.com"
idx = server.register_namespace(uri)
objects = server.get_objects_node()
myobj = objects.add_object(idx, "Metering")
myobj2 = myobj.add_object(idx, "Nested Node")
myvar = myobj.add_variable(idx, "Flow", 6.7)
myvar2 = myobj2.add_variable(idx, "Zort", 7.8)
myvar.set_writable()
myvar2.set_writable()
server.start()

from cognite.client import CogniteClient
c = CogniteClient(api_key="ZjE4M2M1ZDAtMjhhNC00MDk5LThmYmUtZmEyZjM5YjAwMDVi", client_name="cedar", project="publicdata")
status = c.login.status()
print(status)

ts_list = c.time_series.list(include_metadata=True)
#print(ts_list)

my_timeseries = c.time_series.retrieve(id=138649441615650)
if not (my_timeseries is None):
    print(my_timeseries)
    #my_timeseries.plot(start="365d-ago", end="now", aggregates=["average"], granularity="1d")

my_datapoints = c.datapoints.retrieve(id=138649441615650, start="20d-ago", end="now")

try:
    for val in my_datapoints:
        time.sleep(1)
        myvar.set_value(val.value)
finally:
    server.stop()

#print(my_datapoints)

#live_data_generator Function which continously polls latest datapoint of a timeseries and yields new datapoints

