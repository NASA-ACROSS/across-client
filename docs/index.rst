
.. across-client documentation main file.

across-client Documentation
========================================================================================

**across-client** is a Python library used to access and manipulate data products from NASA-ACROSS's ``core-server``.
It provides functionality to easily retrieve and push data from the server combined with
functionality from the ``across-tools`` package to manipulate the data to enable a variety of scientific use cases.

**across-client** is developed and maintained by NASA's Astrophysics
Cross Observatory Science Support (ACROSS) Team, and is part of the larger
ACROSS software ecosystem, which includes APIs and scientific tools for accessing
information about astronomical observatories, instruments, and observation
planning. **across-client** is designed to be a module that enables users to easily access the data products
and conduct the scientific analyses needed for their individual use cases.

Features
--------

**across-client** provides access to Science Situational Awareness (SSA) model data, broadly
encompassing state and status information of NASA's fleet of observatories. This includes:

- **Observing Facility Data**: Retrieve real-time information about NASA's observing fleet, including observatory, telescope, and instrument metadata.
- **Planned and Performed Schedules and Observations**: Search for telescope observation schedules, both past and future.
- **Visibility Computation**: Calculate target visibility windows based on instrument constraints to aid in scheduling submitting observation requests.

Installation
-------------

Install from PyPI:

.. code-block:: console

   >> pip install across-client

Or install from source:

.. code-block:: console

   >> git clone https://github.com/NASA-ACROSS/across-client.git
   >> cd across-client
   >> pip install -e .


Quickstart
-----------

Retrieving Observatory Information
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from across.client import Client

   client = Client()
   # GET an observatory by name
   observatories = client.observatory.get_many(name="JWST")
   observatory = observatories[0]

   # GET an observatory by telescope name
   observatories = client.observatory.get_many(telescope_name="UVOT")
   observatory = observatories[0]


Retrieving Schedules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from across.client import Client

   client = Client()
   # GET schedules with given fidelity and status
   schedules = client.schedule.get_many(page=1, page_limit=10, fidelity="low", status="planned")
   print(f"Page: {schedules.page}")
   print(f"Number of schedules returned: {len(schedules.items)}")
   print(f"Total number of schedules: {schedules.total_number}")


Computing Target Visibility
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from across.client import Client
   from datetime import datetime

   client = Client()

   # Set target and query parameters
   target_ra = 83.86662
   target_dec = -69.26986

   date_range_begin = datetime(2025, 12, 23, 0, 0, 0)
   date_range_end = datetime(2025, 12, 24, 0, 0, 0)
   
   uvot = client.instrument.get_many(name="UVOT")[0]
   
   # Calculate windows
   visibility_windows = client.visibility_calculator.calculate_windows(
      instrument_id=uvot.id,
      ra=target_ra,
      dec=target_dec,
      date_range_begin=date_range_begin,
      date_range_end=date_range_end,
   )
   print(visibility_windows.model_dump_json(indent=4))

Development
-----------

Setting Up Development Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you wish to help development or contribute to the project, follow these steps to set up
a development environment using a python virtual environment:

.. code-block:: console

   # Clone the repo
   >> git clone git@github.com:NASA-ACROSS/across-client.git
   >> cd across-client
   # Create and activate a virtual environment
   >> python -m venv .venv
   >> source .venv/bin/activate 
   # Install development dependencies
   >> pip install -e .
   # Install pre-commit hooks
   >> pre-commit install

Note: please be sure in to run the last command to install the pre-commit hooks, which will
help ensure code quality and consistency. 

.. toctree::
   :hidden:

   Home page <self>
   Observing Facility Data <ssa>
   Schedule and Observation Retrieval <schedules>
   Visibility Calculation <visibility>
   API Reference <autoapi/index>
   Notebooks <notebooks>
