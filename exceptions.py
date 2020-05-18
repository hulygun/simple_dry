class ProcessUnknownKey(Exception):
    def __init__(self, key):
        self.message = f'Unknown keys "{key}" is present in context'


class ProcessMissingKey(Exception):
    def __init__(self, key):
        self.message = f'Missing keys "{key}" in process'
