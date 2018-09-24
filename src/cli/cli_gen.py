"""
base on Click 6.x

.. warning::
    notice that need ``LC_ALL=en_US.UTF-8`` in sys env

in this package, its set in ``src.__init__`` by locale.setlocale

use ``ops()`` os ``click.option()`` to add options

use ``@cli.resultcallback()`` to add callback function while parse cli params

Usage as typical example:

.. code:: python

    from sniputils.cli import cli, ops

    cli.help = '''
        this is the typical example of sniputils.cli
    '''

    ops('--test', is_flag=True, default=False, help='use test model')

    @cli.resultcallback()
    def callback_parse_config(_, **options):
        print('cli parse callback!', options)
        parse_config(options)


.. code:: bash

    $ python cli.py --test
    # output -> 'cli parse callback!', {'test': True}
"""

import click

click.disable_unicode_literals_warning = True
LENIENT_CONTEXT = dict(terminal_width=167, ignore_unknown_options=True, allow_extra_args=True)


@click.group(name='click cli', invoke_without_command=True,
             context_settings=LENIENT_CONTEXT)
@click.option('--test', is_flag=True, default=False, expose_value=False,
              help='set this flag to use test config and env')
@click.argument('unknown', nargs=-1)
@click.pass_context
def cli(ctx, **options):
    """
    this is a cli help docs which need be overwrite with assign ``cli.help`` attribute

    use ``@cli.resultcallback()`` decorator to add callback function while parse cli params
    """

    def chain_callback():
        cli.result_callback(None, **options)

    if not cli.chain and cli.result_callback:
        ctx.call_on_close(chain_callback)


def ops(*args, **kwargs):
    """
    add options to cli, all params same as :func:`click.option`, but without decorator

    example:

    .. code:: python

        ops('--test', is_flag=True, default=False, help='use test model')

    more usage see this module docs
    """
    click.option(*args, **kwargs)(cli)


# parse params and invoke callback, but not exit
_cli_main = cli.main
cli.main = lambda *args, **kwargs: _cli_main(*args, standalone_mode=False, **kwargs)
