# -*- coding: utf-8 -*-
import pytest
from fika_profile_engine import Fika
from .mock_driver import FikaMockDriver


import unittest


class TestProfileEngine(unittest.TestCase):
    def test_simple_profile(self):
        driver = FikaMockDriver()
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
