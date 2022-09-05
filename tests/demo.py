import json
import time
from fika.profile_engine import Fika
from .mock_driver import FikaMockDriver

# Open the JSON definition of the profile to run
f = open ('/home/joheredi/prototypes/fika-profile-engine/tests/initialize.json', "r")
profile_definition = json.load(f)

start_time = time.time()

# Create a new instance of the Driver implementation
driver = FikaMockDriver()
# Create a new instance of the Fika profile engine with the driver and profile definition
profile =  Fika(profile=profile_definition, driver=driver)

# Create an iterator to run the profile
profile_iterator = iter(profile)

# Run the profile, this will loop until the end node is reached
for node in profile_iterator:
    # Print the current node
    print(node["id"])

print("--- %s seconds ---" % (time.time() - start_time))
