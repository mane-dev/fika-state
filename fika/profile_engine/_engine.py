from threading import Thread
import time
from fika.profile_engine._fika_state import FikaSensorState
from fika.profile_engine._node import Controller, Node, Profile
from typing import Iterable
from fika.profile_engine._driver_interface import Driver
from fika.profile_engine._trigger import Trigger

"""
The Fika class is the main entry point for the Fika profile engine.
"""
class Fika:
    def __init__(self, profile: Profile, driver: Driver):
        self.__driver = driver
        self.state: FikaSensorState =  driver.get_sensor_data()
        profile: Profile = profile
        self.nodes: Iterable[Node] = self.__get_profile_nodes(profile)
        
    
    def set_sensor_data(self, new_state: FikaSensorState):
            self.state = new_state

    def get_sensor_state(self) -> FikaSensorState:
        return self.state

    def __iter__(self):
        self.current_node: Node = self.__get_start_node()
        return self

    def __next__(self):
        if self.current_node["id"] == "end":
            raise StopIteration
        
        self.__step()
        return self.current_node

    def __step(self):
        if self.current_node["id"]  == "end":
            print('Reached end of profile')
            return

        next_node = self.__evaluate_triggers()

        # A trigger has been met, move to the next state
        if next_node != None:
            self.current_node = self.nodes[next_node]
            print(f'A trigger has been met, move to the next state: {next_node}')
            return

        # No trigger has been met, execute the current node's controllers
        self.__execute_controllers()

    def __get_start_node(self) -> Node:
        start = self.nodes.get("start", None)

        if start == None:
            raise Exception("No start node defined")

        return start

    def __get_profile_nodes(self, profile) -> Iterable[Node]:
        nodes = {}
        for stage in profile["stages"]:
            for node in stage["nodes"]:
                nodes[node["id"]] = node
        
        return nodes

    def __evaluate_triggers(self):
        for item in self.current_node["triggers"]:
            if(item["kind"] == "wake"):
                return item["target"]
            trigger = Trigger(operator=item["operator"], value=item.get("value"), tag=item.get("tag", None), kind=item["kind"])
            print(f'Evaluating trigger {item["kind"]}')
            if trigger.evaluate(payload=self.get_sensor_state()) == True:
                return item["target"]

    def update_state(self, state: FikaSensorState):
            updated = {**self.state, **state}
            self.state = updated

    def __execute_controllers(self):
        controllers = self.current_node["controllers"]
        threads: list[Thread] = list()
        for controller in controllers:
            task = Thread(target=self.__execute_controller, args=(controller,))
            threads.append(task)
            task.start()
        
        for thread in threads:
             thread.join() # waits for thread to complete its task
             self.update_state(self.__driver.get_sensor_data())

    def __execute_controller(self, controller: Controller):
        if controller["kind"] == "move_piston":
            return self.__driver.move_piston(controller["parameters"])
        
        if controller["kind"] == "set_water_temp":
            return self.__driver.set_water_temp(controller["parameters"])
        
        if controller["kind"] == "set_water_flow":
            return self.__driver.set_water_flow(controller["parameters"])
        
        if controller["kind"] == "set_water_pressure":
            return self.__driver.set_water_pressure(controller["parameters"])

        if controller["kind"] == "log":
            return self.__driver.log(controller["parameters"])

        if controller["kind"] == "weight":
            return self.__driver.set_weight(controller["parameters"])
            
        if controller["kind"] == "tare":
            return self.__driver.tare(controller["parameters"])

        if controller["kind"] == "timer":
            timeInSeconds = controller["parameters"]["timeInMs"]/1000
            print(f'Executing Timer {timeInSeconds}') 
            time.sleep(timeInSeconds)
            return self.state

        raise Exception(f'Unknown controller kind: {controller["kind"]}')



