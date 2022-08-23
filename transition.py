class Transition:
    kind = property()

    def __init__(self, operator, value, tag=None):
        self.operator = operator
        self.value = value
        self.tag = tag

    def evaluate(self, payload):
        if payload == None:
            return False

        entry = payload.get(self.kind, None)
        if entry == None:
            return False

        tag = entry.get("tag", None)

        if tag != self.tag:
            return False

        currentValue = entry.get("value", None)
        return _evaluate(self.operator, currentValue, self.value)



def _evaluate(operator, a, b):
    operationSwitch = {
        '>': gt,
        '>=': ge,
        '<': lt,
        '<=': le,
        '==': eq,
        '=': eq,
        '!=': ne,
    }

    evaluation = operationSwitch.get(operator, "Invalid operator")
    return evaluation(a, b)


def gt(a, b):
    return a > b


def ge(a, b):
    return a >= b


def lt(a, b):
    return a < b


def le(a, b):
    return a <= b


def eq(a, b):
    return a == b


def ne(a, b):
    return a != b


class PistonPositionTransition(Transition):
    kind = "piston_position"


class WaterCheckTransition(Transition):
    kind = "water_check"


class WaterTempTransition(Transition):
    kind = "water_temp"


class TimeoutTransition(Transition):
    kind = "timeout"


class WakeTransition(Transition):
    kind = "wake"


# foo = PistonPositionTransition(">=", "c", "end")

# print(foo.evaluate({"piston_position": {"value": "b"}}))
