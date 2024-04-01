.. _nbsfiles:

=======================================
The BIDS relmat metadata file templates
=======================================

As mentioned before, one of the core aspects of ``bids_relmat`` are the ``relmat metadata template files``. 
These are based on the `BIDS relationship matrix BEP <https://docs.google.com/document/d/1ugBdUF6dhElXdj3u9vw0iWjE6f_Bibsro3ah7sRV0GA/view>`_ and entail the
``metadata`` outlined and proposed by this ``BEP``. Specifically, the rationale behind the ``BIDS relationship matrix BEP`` is to add and 
adapt ``metadata`` of existing ``BIDS``-compliant derivative datasets to make them ``BIDS relationship matrix`` compliant, ie sufficiently capturing and describing
``relationship matrix`` data.

To streamline and standardize the process of adapting and adding the respective ``metadata``, the ``bids_relmat`` toolbox includes
a set of ``relmat metadata template`` files that are utilized in the following manner:

1. The ``relmat metadata template`` files are added to the ``sourcedata/`` directory of an existing ``BIDS`` dataset 
2. Users fill out the respective information, ie ``values`` of the ``metadata`` ``keys`` based on their respective experiment/data
3. The files are used within the conversion of an existing ``BIDS`` derivatives dataset to an ``BIDS relationship matrix`` dataset, the provided ``metadata`` information is added/apdated
   in the ``metadata`` files of the existing ``BIDS`` derivatives dataset 

Below, the ``BIDS relmat metadata`` file is shown. Specifically, on the left you can see the contents of ``metadata template`` file and on the
right an example with all ``metadata`` information filled out based on an actual example dataset.


.. tabs::

    .. tab:: ``relmat`` metadata template

        Below you can see the template for the ``_relmat metadata``.

        .. literalinclude:: ../../bids_relmat/data/relmat_template.json
            :language: json
            :linenos:

    .. tab:: ``relmat`` metadata example

        Below you can see an example for the ``_relmat metadata``.

        .. literalinclude:: ../../bids_relmat/data/relmat_example.json
            :language: json
            :linenos:
