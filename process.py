from . import Context
from .errors import ErrorsCollector
from .exceptions import ProcessUnknownKey, ProcessMissingKey
from .returns import Result, Success, Failure


class Process:
    process_errors = ErrorsCollector()  # Сборщик ошибок
    result = Result()

    def __init__(self, *args, context=Context):
        self.availables_args = args   # Доступные аргументы
        self.context_class = context  # Класс контекста

    def __call__(self, method):
        steps = []

        class Collector(object):
            """Сборщик методов бизнес процесса"""
            def __getattr__(self, item):
                steps.append(item)

        method(Collector())

        def inner(instance, **kwargs):
            context = self.init_context(kwargs)
            next_step = None
            finished_steps = []
            for step in steps:  # Проход по шагам процесса
                finished_steps.append(step)  # Добавляем выполненный шаг в лог
                if next_step and step != next_step:
                    continue
                step_result = getattr(instance, step)(context)
                if isinstance(step_result, (Success, Failure)):
                    if isinstance(step_result, Failure):
                        self.process_errors.register_error(step_result, finished_steps)
                        if not step_result.to:
                            break
                    next_step = step_result.to

                elif isinstance(step_result, Result):
                    self.result = step_result

            self.result.apply_errors(self.process_errors)
            return self.result

        return inner

    def check_context_data(self, kwargs: dict) -> None:
        """Исключительно для упоротых по валидации"""
        args = self.availables_args
        keys = sorted(kwargs.keys())
        if args != keys:  # Если набор ключей при вызове процесса не совпадает с объявленными в процессе
            excess_keys = set(keys) - set(args)
            missing_keys = set(args) - set(keys)
            if excess_keys:  # Если присутствуют кейворды, необъявленные в процессе
                raise ProcessUnknownKey(list(excess_keys).__str__())
            if missing_keys:  # Если не хватает ключей при вызове процесса
                raise ProcessMissingKey(list(excess_keys).__str__())

    def init_context(self, kwargs):
        """Собираем объект контекста"""
        self.check_context_data(kwargs)
        return self.context_class(**kwargs)



class AsyncProcess(Process):
    def __call__(self, method):
        steps = []

        class Collector(object):
            """Сборщик методов бизнес процесса"""
            def __getattr__(self, item):
                steps.append(item)

        method(Collector())

        async def inner(instance, **kwargs):
            context = self.init_context(kwargs)
            next_step = None
            finished_steps = []
            for step in steps:  # Проход по шагам процесса
                finished_steps.append(step)  # Добавляем выполненный шаг в лог
                if next_step and step != next_step:
                    continue
                step_result = await getattr(instance, step)(context)
                if isinstance(step_result, (Success, Failure)):
                    if isinstance(step_result, Failure):
                        self.process_errors.register_error(step_result, finished_steps)
                        if not step_result.to:
                            break
                    next_step = step_result.to

                elif isinstance(step_result, Result):
                    self.result = step_result

            self.result.apply_errors(self.process_errors)
            return self.result

        return inner

