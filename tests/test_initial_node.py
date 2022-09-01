# -*- coding: utf-8 -*-
import pytest
from fika_profile_engine import Fika
from .mock_driver import FikaMockDriver


import unittest


class TestProfileEngine(unittest.TestCase):
    initial_state = {"has_water": True, "piston_position": 0, "water_temp": 0,
                     "water_flow": 0, "water_pressure": 0, "weight": 0, "piston_speed": 0, "motor_encoder": 0}

    def test_simple_profile(self):
        driver = FikaMockDriver(self.initial_state)
        mock_profile = {"stages": [
            {
                "id": "initialize",
                "nodes": [
                    {
                        "id": "start",
                        "controllers": [],
                        "triggers": [{
                            "kind": "piston_position",
                            "operator": ">=",
                            "value": 0,
                            "target": "1"
                        }]
                    },
                    {
                        "id": "1",
                        "controllers": [],
                        "triggers": [{
                            "kind": "piston_position",
                            "operator": ">=",
                            "value": 0,
                            "target": "end"
                        }]
                    },
                    {
                        "id": "end",
                        "controllers": [],
                        "triggers": []
                    }
                ]
            }
        ]}

        profile = Fika(mock_profile, driver)

        # Initializes the iterator and starts the profile
        # this will set the profile initial node to the start node
        profile_iterator = iter(profile)

        # Tracking the states to verify the profile is working as expected
        # inserting the first node
        visited_nodes = [profile_iterator.current_node["id"]]

        for x in profile_iterator:
            # Inserting the current node to the states list
            visited_nodes.append(x["id"])

        # Verifying that the sequence of visited nodes is the expected
        assert visited_nodes == ["start", "1" , "end"]

if __name__ == '__main__':
    unittest.main()
