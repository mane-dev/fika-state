class Action:
    kind = property()

    def start(self):
        print('Starting ', self.kind, self.parameters)
        self.action_event({f'{self.kind}': self.parameters})

    def stop(self):
        print('Stopping ', self.kind)

    def __init__(self, parameters, action_event):
        self.parameters = parameters
        self.action_event = action_event


class MovePistonAction(Action):
    kind = "move_piston"

class ErrorAction(Action):
    kind = "error"

class SleepAction(Action):
    kind = "sleep"

class TimeoutAction(Action):
    kind = "timeout"

class WaterTempPID1Action(Action):
    kind = "water_temp_pid_1"