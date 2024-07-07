==========
Quickstart
==========

.. code-block:: bash

    scripts-fabq [foo,bar] [-del] [-foo:foo,bar] [-bar:foo,bar]

** Warning dont do this other thing **

default options are:

.. code-block:: bash

    -foo:foo
    -bar:

Examples:

.. code-block:: bash

    # Do this
    scripts-fabq foo -del -foo:bar -bar:foo
    # Do that
    scripts-fabq bar -foo:foo

More examples in :doc:`use_cases`