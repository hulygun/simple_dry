from typing import List

from . import Context
from .returns import Failure


class Error:
    error_type: int
    step: List[str]
    reason: str
    context: Context

    def __init__(self, error_type, step, reason, context):
        self.error_type = error_type
        self.step = step
        self.reason = reason
        self.context = context

    def __repr__(self):
        output = "Process: \n"
        for step in self.step:
            output += f'  {step}\n'

        output += '\nContext:\n'
        for k, v in self.context.__dict__.items():
            output += f'  {k}: {v}\n'

        output += f'\n{self.error_type}: {self.reason}'

        return output


class ErrorsCollector:
    errors = {}

    def register_error(self, error: Failure, step):
        self.errors[error.error_type] = Error(
            error_type=error.error_type,
            step=step,
            reason=error.reason,
            context=Context(**error.context)
        )

    def __getattr__(self, item):
        return self.errors.get(item, None)

    def __call__(self):
        return self.errors.values()

    def has_errors(self, *types):
        errors = self.errors.keys()
        if types and errors:
            errors = [err_type for err_type in types if err_type in errors]
        return bool(errors)
