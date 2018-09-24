from itertools import chain

import click


class Separate(click.Option):
    """
    Usage: ``ops(cls=Separate, **kwargs)``

    ..

        option: ``'1,3,5,7,what,the,hell'``

        click params: ``['1', '3', '5', '7', 'what', 'the', 'hell']``

    ..

        option: ``'single'``

        click params: ``['single']``
    """

    def type_cast_value(self, ctx, value):
        try:
            if not value:
                return []
            return value.split(',')
        except Exception:
            raise click.BadParameter(value)

    def __repr__(self):
        return 'CSV'


class FlowRange(click.Option):
    """
    Usage: ``ops(cls=FlowRange, **kwargs)``

    ..
        option: ``1``

        click params: ``[1]``

    ..

        option: ``2-5``

        click params: ``[2, 3, 4, 5]``

    ..

        option: ``1,2-5,3-6``

        click params: ``[1, 2, 3, 4, 5, 3, 4, 5, 6]``
    """

    def parse_range(self, series):
        parts = list(map(int, series.split('-')))
        if 1 > len(parts) > 2:
            raise click.BadParameter(series)
        if len(parts) == 1:
            return parts
        start, end = parts
        if start > end:
            raise click.BadParameter(series)
        return range(start, end + 1)

    def type_cast_value(self, ctx, value):
        try:
            if not value:
                return
            return chain(*map(self.parse_range, value.split(',')))
        except Exception:
            raise click.BadParameter(value)

    def __repr__(self):
        return 'NUM-Range'


class TypeChose(click.Choice):
    """
    Usage: ``ops(type=TypeChose(click.IntParamType, click.File), **kwargs)``


        option: ``34``

        click params: ``34``

    ..

        option: ``'./output.log'``

        click params: ``<_io.TextIOWrapper name='./output.log'>``

    Usage: ``ops(type=TypeChose(int, list), **kwargs)``

        option: ``['what', 'the', 'hell']``

        click params: ``['what', 'the', 'hell']``

    ..

        option: ``12``

        click params: ``12``
    """

    def __init__(self, *choices: click.ParamType):
        super().__init__(choices)

    def convert(self, value, param, ctx):
        for choice in self.choices:
            if value is choice:
                return value
            if isinstance(value, choice):
                return value
            try:
                return choice(value, param, ctx)
            except (click.BadParameter, Exception):
                pass
            try:
                return choice(value)
            except (click.BadParameter, Exception):
                pass
            try:
                return choice.convert(value, param, ctx)
            except (click.BadParameter, Exception):
                pass
        else:
            self.fail('{value} is not a valid choice type in {choices}'.format(value=value, choices=self.choices))
