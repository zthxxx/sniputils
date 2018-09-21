=============
API Reference
=============

conffor
----------

.. autofunction:: sniputils.conffor.load
.. autofunction:: sniputils.conffor.dump
.. autofunction:: sniputils.conffor.read_list_csv
.. autofunction:: sniputils.conffor.save_list_csv

logsetting
----------

.. autofunction:: sniputils.logsetting.reset_logbase
.. autofunction:: sniputils.logsetting.clear_logsetting

cli
----------

.. automodule:: sniputils.cli.cli_gen

.. autodata:: sniputils.cli.cli

.. autoclass:: sniputils.cli.Separate
.. autoclass:: sniputils.cli.FlowRange
.. autoclass:: sniputils.cli.TypeChose

database
----------

.. autofunction:: sniputils.database.create_session
.. autofunction:: sniputils.database.mongo_connect
.. autofunction:: sniputils.database.doc2dict
.. autofunction:: sniputils.database.add_log4mongo
.. autofunction:: sniputils.database.remove_log4mongo

concurrent
----------

.. autoclass:: sniputils.concurrent.Parallel
    :members:

daemon
----------

.. automodule:: sniputils.daemon

.. autodata:: sniputils.daemon.daemon

import_hook
-----------

.. autofunction:: sniputils.import_hook.which_import_me
.. autofunction:: sniputils.import_hook.set_reimport
.. autofunction:: sniputils.import_hook.disreimport

import_hook.upstream
####################

.. automodule:: sniputils.import_hook.upstream
    :members:

snippets
---------

.. automodule:: sniputils.snippets
    :members:
    :undoc-members:
    :show-inheritance:

