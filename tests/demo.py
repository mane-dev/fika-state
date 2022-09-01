import pytest
from ..fika_profile_engine._engine import Fika 
from tests.mock_driver import FikaMockDriver

driver = FikaMockDriver()
profile = Fika(profile_path="/home/joheredi/prototypes/statemachine/initialize.json", driver=driver)

profile.run()