.. _usage:

======
Usage
======

The general usage of ``bids_relmat`` is ADD DESCRIPTION HERE.
The exact command to run ``bids_relmat`` depends on the Installation method and user. Regarding the latter, ``bids_relmat`` 
can either be used as a ``command line tool`` or directly within ``python``. Please refer to the `Tutorial <https://peerherholz.github.io/bids_relmat/walkthrough>`_ for a more detailed walkthrough.

Here's a very conceptual example of running ``bids_relmat`` via ``CLI``: ::

    bids_relmat 
    bids_relmat optional_arguments

and here from within ``python``: ::

    from bids_relmat import bids_relmat_function
    from bids_relmat import bids_relmat_function

    result = bids_relmat_function(input)

    result = bids_relmat_function(input, optional_arguments)

Below, we will focus on the ``CLI`` version. Thus, if you are interested in using ``bids_relmat`` directly within ``python``,
please check the `Examples <https://peerherholz.github.io/bids_relmat/auto_examples/index>`_.

Sub-section of Usage focusing on CLI
===========================================

Command-Line Arguments
======================
.. argparse::
  :ref: bids_relmat.bids_relmat_cli.get_parser
  :prog: bids_relmat
  :nodefault:
  :nodefaultconst:

Example Call(s)
---------------

Below you'll find two examples calls that hopefully help
you to familiarize yourself with ``bids_relmat`` and its options.

Example 1
~~~~~~~~~

.. code-block:: bash

    bids_relmat \
    input
    optional_arguments

Here's what's in this call:

- The 1st positional argument is 
- The 2nd positional argument indicates that 


Example 2
~~~~~~~~~

.. code-block:: bash

    bids_relmat \
    input
    optional_arguments
    optional_arguments

Here's what's in this call:

- The 1st positional argument is 
- The 2nd positional argument indicates that 
- The 3rd positional argument indicates that 


Support and communication
=========================

The documentation of this project is found here: https://peerherholz.github.io/bids_relmat.

All bugs, concerns and enhancement requests for this software can be submitted here:
https://github.com/peerherholz/bids_relmat/issues.

If you have a problem or would like to ask a question about how to use ``bids_relmat``,
please submit a question to `NeuroStars.org <http://neurostars.org/tags/bids_relmat>`_ with an ``bids_relmat`` tag.
NeuroStars.org is a platform similar to StackOverflow but dedicated to neuroinformatics.

All previous ``bids_relmat`` questions are available here:
http://neurostars.org/tags/bids_relmat/

Not running on a local machine? - Data transfer
===============================================

Please contact you local system administrator regarding
possible and favourable transfer options (e.g., `rsync <https://rsync.samba.org/>`_
or `FileZilla <https://filezilla-project.org/>`_).

A very comprehensive approach would be `Datalad
<http://www.datalad.org/>`_, which will handle data transfers with the
appropriate settings and commands.
Datalad also performs version control over your data.