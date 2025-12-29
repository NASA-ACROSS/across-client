Observing Facility Data
========================================================================================

The ``across-client`` provides API functionality for accessing and working 
with observing facilitity model data by filtering and retrieving
objects based on query parameters.

Overview
--------

Science Situational Awareness (SSA) models broadly capture data about the observatories, 
telescopes, and instruments in the ACROSS ``core-server``, summarizing information about 
their observing capabilities. These models include:

- **Observatories**: The top-level data model, encapsulating a system of observational resources located in the same physical area (either on ground or aboard a spacecraft).
- **Telescopes**: The model describing a single physical telescope. An observatory may have many telescopes.
- **Instruments**: The model describing a single instrument used to take scientific data. A telescope may have multiple instruments.
- **Filters**: The model describing the physical parameters an instrument may observe in, including the wavelength, energy, or frequency regime and unit.

Initializing the Client
------------------------

To use the ``across-client`` to access the ACROSS ``core-server``, you must first instantiate
a ``Client`` object. This provides access to the API modules used to retrieve information from
the server. Note that performing ``GET`` requests to fetch SSA data does not require credentials.

.. code-block:: python

    from across.client import Client

    client = Client()

Accessing Observatory Data
---------------------------

To access the top-level ``Observatory`` data, users may call the ``get`` or ``get_many`` methods
of the ``client.observatory`` module:

Using ``client.observatory.get()``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``observatory.get()`` method fetches a single ``Observatory`` object by its unique identifier, or ID:

.. code-block:: python

    from across.client import Client

    client = Client()
    # The UUID of the Hubble Space Telescope observatory in the ACROSS core-server
    hst_uuid = "eb43bec9-0002-4c05-b294-de71453d95b6"
    hst_observatory = client.observatory.get(id=hst_uuid)
    print(hst_observatory)


Using ``client.observatory.get_many()``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``observatory.get_many()`` method fetches multiple ``Observatory`` objects that meet
the input parameters. For example, users can search by name:

.. code-block:: python

    from across.client import Client

    client = Client()
    observatories = client.observatory.get_many(name="HST")
    print(observatories[0])

or users can search by type, such as space-based observatories:

.. code-block:: python

    from across.client import Client

    client = Client()
    # GET a list of observatories by type
    space_based_observatories = client.observatory.get_many(type="SPACE_BASED")
    for obs in space_based_observatories:
        print(obs.name)

Here is a complete list of arguments for the ``client.observatory.get_many()`` method:

.. list-table:: observatory.get_many() Parameters
   :widths: 20 15 65
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - ``name``
     - str (optional)
     - Name or short name of the observatory (case insensitive)
   * - ``type``
     - str (optional)
     - Type of the observatory (either ``SPACE_BASED`` or ``GROUND_BASED``)
   * - ``telescope_name``
     - str (optional)
     - Name or short name of a telescope belonging to an observatory (case insensitive)
   * - ``telescope_id``
     - uuid (optional)
     - UUID of a telescope belonging to an observatory
   * - ``ephemeris_type``
     - str (optional)
     - Ephemeris type stored for the observatory (one of ``tle``, ``spice``, ``jpl``, or ``ground``)
   * - ``created_on``
     - datetime (optional)
     - Datetime of observatory creation in the ACROSS ``core-server``

``Observatory`` Data Structure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``client.observatory.get()`` and ``client.observatory.get_many()`` methods return an
``Observatory`` and a list of ``Observatory`` objects, respectively. Below are the attributes
of the ``Observatory`` model, all of which can be accessed for the returned data:

.. list-table:: Observatory Attributes
   :widths: 20 25 65
   :header-rows: 1

   * - Attribute
     - Type
     - Description
   * - ``id``
     - UUID
     - Unique identifier in the ACROSS ``core-server`` 
   * - ``created_on``
     - datetime
     - Datetime of creation in the ACROSS ``core-server``
   * - ``name``
     - str
     - Full name of the observatory
   * - ``short_name``
     - str
     - Short name of the observatory
   * - ``type``
     - str
     - Type of the observatory (either ``SPACE_BASED`` or ``GROUND_BASED``)
   * - ``telescopes``
     - list[Telescope] | None
     - List of ``Telescope`` objects belonging to the Observatory
   * - ``ephemeris_types``
     - list[str] | None
     - List of ephemeris types belonging to the observatory (``tle``, ``spice``, ``jpl``, or ``ground``)
   * - ``reference_url``
     - str | None
     - URL containing more information about the observatory
   * - ``operational``
     - DateRange | None
     - DateRange object with ``begin_time`` and ``end_time``, describing the observatory's operational period

Accessing Telescope Data
---------------------------

To access ``Telescope`` data, users may call the ``get`` or ``get_many`` methods
of the ``client.telescope`` module. The ``get`` methods behaves analogously to the
``client.observatory.get()`` method, taking a UUID belonging to a ``Telescope`` in 
the ACROSS ``core-server``.

Using ``client.telescope.get_many()``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``telescope.get_many()`` method fetches multiple ``Telescope`` objects that meet
the input parameters. For example, users can search by name:

.. code-block:: python

    from across.client import Client

    client = Client()
    telescopes = client.telescope.get_many(name="UVOT")
    print(telescopes[0])

or users can search for telescopes that contain a specific instrument, by name:

.. code-block:: python

    from across.client import Client

    client = Client()
    
    telescopes = client.telescope.get_many(instrument_name="nircam")
    print(telescopes[0])

Here is a complete list of arguments for the ``client.telescope.get_many()`` method:

.. list-table:: telescope.get_many() Parameters
   :widths: 20 15 65
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - ``name``
     - str (optional)
     - Name or short name of the telescope (case insensitive)
   * - ``instrument_name``
     - str (optional)
     - Name or short name of an instrument belonging to a telescope (case insensitive)
   * - ``instrument_id``
     - uuid (optional)
     - UUID of an instrument belonging to a telescope
   * - ``created_on``
     - datetime (optional)
     - Datetime of telescope creation in the ACROSS ``core-server``
   * - ``include_filters``
     - bool (optional)
     - Include instrument filters in the returned data (default is ``False``)
   * - ``include_footprints``
     - bool (optional)
     - Include instrument footprints in the returned data (default is ``False``)

``Telescope`` Data Structure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``client.telescope.get()`` and ``client.telescope.get_many()`` methods return a
``Telescope`` and a list of ``Telescope`` objects, respectively. Below are the attributes
of the ``Telescope`` model:

.. list-table:: Telescope Attributes
   :widths: 20 25 65
   :header-rows: 1

   * - Attribute
     - Type
     - Description
   * - ``id``
     - UUID
     - Unique identifier in the ACROSS ``core-server`` 
   * - ``created_on``
     - datetime
     - Datetime of creation in the ACROSS ``core-server``
   * - ``name``
     - str
     - Full name of the telescope
   * - ``short_name``
     - str
     - Short name of the telescope
   * - ``schedule_cadence``
     - list[ScheduleCadence] | None
     - ``ScheduleCadence`` objects containing the frequency and status of schedule ingestion tasks for this telescope
   * - ``observatory``
     - Observatory | None
     - The ``Observatory`` object the telescope belongs to
   * - ``instruments``
     - list[Instrument] | None
     - List of ``Instrument`` objects belonging to the telescope

Accessing Instrument Data
---------------------------

To access ``Instrument`` data, users again may use either the ``get`` or ``get_many`` methods
of the ``client.instrument`` module, in analogous ways to the ``client.observatory`` and
``client.telescope`` modules. Again, ``client.instrument.get()`` takes a UUID belonging 
to an ``Instrument`` in the ACROSS ``core-server``.

Using ``client.instrument.get_many()``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``instrument.get_many()`` method fetches multiple ``Instrument`` objects that meet
the input parameters. For example, users can search by name:

.. code-block:: python

    from across.client import Client

    client = Client()
    instruments = client.instrument.get_many(name="GBM")
    print(instruments[0])

or by telescope name:

.. code-block:: python

    from across.client import Client

    client = Client()
    
    instruments = client.instrument.get_many(telescope_name="chandra")
    print(instruments[0])

Here is a complete list of arguments for the ``client.instrument.get_many()`` method:

.. list-table:: instrument.get_many() Parameters
   :widths: 20 15 65
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - ``name``
     - str (optional)
     - Name or short name of the instrument (case insensitive)
   * - ``telescope_name``
     - str (optional)
     - Name or short name of a telescope (case insensitive)
   * - ``telescope_id``
     - uuid (optional)
     - UUID of a telescope
   * - ``created_on``
     - datetime (optional)
     - Datetime of instrument creation in the ACROSS ``core-server``

``Instrument`` Data Structure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``client.instrument.get()`` and ``client.instrument.get_many()`` methods return an
``Instrument`` and a list of ``Instrument`` objects, respectively. Below are the attributes
of the returned ``Instrument`` model:

.. list-table:: Instrument Attributes
   :widths: 20 25 65
   :header-rows: 1

   * - Attribute
     - Type
     - Description
   * - ``id``
     - UUID
     - Unique identifier in the ACROSS ``core-server`` 
   * - ``created_on``
     - datetime
     - Datetime of creation in the ACROSS ``core-server``
   * - ``name``
     - str
     - Full name of the instrument
   * - ``short_name``
     - str
     - Short name of the instrument
   * - ``telescope``
     - Telescope | None
     - The ``Telescope`` object the instrument belongs to
   * - ``footprints``
     - list[list[Point]] | None
     - List of ``Point`` objects, corresponding to coordinates (in degrees) of the vertices of a polygon on the sky, representing the instrument's observational footprint
   * - ``filters``
     - list[Filter] | None
     - The ``Filter`` objects belonging to the instrument
   * - ``constraints``
     - list[Constraint] | None
     - ``Constraint`` objects representing conditions that must be met for a target to be observable with the instrument
   * - ``visibility_type``
     - str | None
     - How target visibility is calculated for the instrument (either ``EPHEMERIS``, ``VO``, or ``CUSTOM``)

Accessing Filter Data
---------------------------

Finally, users may access ``Filter`` data through either the ``get`` or ``get_many`` methods
of the ``client.filter`` module, analogously to the previous examples. Below are several example
use cases for the ``client.filter.get_many()`` method:

Using ``client.filter.get_many()``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``filter.get_many()`` method fetches multiple ``Filter`` objects that meet
the input parameters. For example, users can search by name:

.. code-block:: python

    from across.client import Client

    client = Client()
    filters = client.filter.get_many(name="Swift UVOT UVW2")
    print(filters[0])

or by a specific wavelength (in Angstroms) that it covers:

.. code-block:: python

    from across.client import Client

    client = Client()
    
    filters = client.filter.get_many(covers_wavelength=3000.0)
    for filt in filters:
        print(filt.name)

Here is a complete list of arguments for the ``client.filter.get_many()`` method:

.. list-table:: filter.get_many() Parameters
   :widths: 20 15 65
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - ``name``
     - str (optional)
     - Name of the filter (case insensitive)
   * - ``contains_wavelength``
     - float (optional)
     - A wavelength value (in Angstroms) that the filter covers
   * - ``instrument_name``
     - str (optional)
     - Name of an instrument the filter belongs to
   * - ``instrument_id``
     - uuid (optional)
     - UUID of an instrument the filter belongs to

``Filter`` Data Structure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``client.filter.get()`` and ``client.filter.get_many()`` methods return a
``Filter`` and a list of ``Filter`` objects, respectively. Below are the attributes
of the returned ``Filter`` model. **NOTE:** All wavelength values are stored and returned
in units of Angstroms.

.. list-table:: Filter Attributes
   :widths: 20 25 65
   :header-rows: 1

   * - Attribute
     - Type
     - Description
   * - ``id``
     - UUID
     - Unique identifier in the ACROSS ``core-server`` 
   * - ``created_on``
     - datetime
     - Datetime of creation in the ACROSS ``core-server``
   * - ``name``
     - str
     - Name of the filter
   * - ``peak_wavelength``
     - float | None
     - Wavelength of peak transmission of the filter (in Angstroms)
   * - ``min_wavelength``
     - float | None
     - Blueward cutoff wavelength of the filter (in Angstroms)
   * - ``max_wavelength``
     - float | None
     - Redward cutoff wavelength of the filter (in Angstroms)
   * - ``is_operational``
     - bool | None
     - The current operational state of the filter
   * - ``sensitivity_depth_unit``
     - str | None
     - Unit of the sensitivity depth value
   * - ``sensitivity_depth``
     - float | int | None
     - Maximum depth the instrument can observe in this filter
   * - ``sensitivity_depth_seconds``
     - float | int | None
     - Exposure time (in seconds) needed to reach the sensitivity depth of the filter
   * - ``reference_url``
     - str | None
     - URL containing reference information about the filter
   * - ``instrument_id``
     - uuid | None
     - UUID of the instrument for the filter

API Reference
-------------

See the :doc:`Observatory API Reference </autoapi/across/client/apis/observatory/index>`, 
:doc:`Telescope API Reference </autoapi/across/client/apis/telescope/index>`,
:doc:`Instrument API Reference </autoapi/across/client/apis/instrument/index>`,
and :doc:`Filter API Reference </autoapi/across/client/apis/filter/index>`
for complete class and function documentation.
