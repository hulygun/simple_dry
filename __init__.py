class Context:
    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)

    def __getattr__(self, item):
        try:
            return super().__getattr__(item)
        except AttributeError:
            return None
