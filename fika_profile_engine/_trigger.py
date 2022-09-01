class Trigger:
    def __init__(self, kind, operator, value, tag=None):
        self.operator = operator
        self.value = value
        self.tag = tag
        self.kind = kind

    def evaluate(self, payload):
        if payload == None:
            return False

        entry = payload.get(self.kind, None)
        if entry == None:
            return False

        # tag = entry.get("tag", None)

        # if tag != self.tag:
        #     return False
        return _evaluate(self.operator, entry, self.value)



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
