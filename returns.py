class Success:
    def __init__(self, to=None):
        self.to=to


class Failure:
    def __init__(self, error_type, reason, context=None, to=None):
        self.error_type = error_type
        self.reason = reason
        self.to = to
        self.context = context or {}


class Result:
    errors = None

    def __init__(self, value=None):
        self.value = value

    def apply_errors(self, errors):
        self.errors = errors

    def has_errors(self, **types):
        return self.errors.has_errors(**types)

    @property
    def error(self):
        if self.has_errors():
            return list(self.errors())[0]
