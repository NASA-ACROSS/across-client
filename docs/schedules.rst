Schedules and Observations
========================================================================================

The ``across-client`` library contains functionality to retrieve and post schedules and
observations for supported telescopes and instruments via the ACROSS ``core-server``.

Overview
---------
In the ACROSS system, ``Observations`` record parameters related to the period of
time an ``Instrument`` takes data of an astronomical source. These include, among other
things, the begin and end time of the exposure; the target name and its celestial coordinates;
the instrument and filter used to take data; and metdadata such as any proposal or external
ID it is associated with. 

``Observations`` correspond to discrete periods of data-taking; multiple observations can be
grouped in ``Schedules``. ``Schedules`` belong to a ``Telescope`` and associate ``Observations``
based on time range, status, and fidelity. For example, a ``Telescope`` may have both a "planned"
schedule, for observations to be taken in the future, as well as an "as-flown" schedule, for
observations that have been completed. ``Schedules`` also have a fidelity--either "low" or "high"--
describing the "likelihood" the schedule was (or will be) executed as shown. As the time to a planned schedule gets closer, the fidelity
is expected to rise, and all "as-flown" schedules should be high fidelity, as they should be accurate
records of what a telescope observed in the past. Note that all ``Observation`` objects in the ACROSS
system must belong to a ``Schedule``.

``across-client`` currently supports functionality to both retrieve and post ``Schedules`` from/to the
``core-server``, as well as to retrieve ``Observations`` from the server. 

Retrieving Schedules
----------------------

To access ``Schedule`` data from the ``core-server``, ``across-client`` has a ``schedule`` module with
methods to get one or many ``Schedule`` objects that meet the input parameters.

Retrieving a Schedule by ID
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To get a single ``Schedule``, use the ``client.schedule.get()`` method. ``schedule.get()`` takes a 
unique identifier (``UUID``), corresponding to the ID of the object in the ACROSS system, as input. 

.. code-block:: python
    
    from across.client import Client

    client = Client()
    # A fake schedule ID
    schedule_id = "cac5cec1-b0c5-4bc0-a8c9-3dbbbfe9cec7"
    schedule = client.schedule.get(id=schedule_id)
    print(schedule)

Retrieving Most Recent Schedules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To filter and retrieve the most recent ``Schedules`` for a given telescope, date range, and fidelity, 
use the ``client.schedule.get_many()`` method. ``schedule.get_many()`` will only return the
most recent ``Schedules`` added to the ACROSS ``core-server`` for each combination of telescope, fidelity, 
date range, and status that meet the input parameters.

**Use when**: you only want to retrieve the most up-to-date ``Schedule`` for a telescope, either planned
or as-flown.

.. code-block:: python
    
    from across.client import Client
    from datetime import datetime

    client = Client()
    schedule = client.schedule.get_many(
        date_range_begin=datetime(2025, 12, 12),
        date_range_end=datetime(2025, 12, 19),
        telescope_names=["UVOT"],
        status="performed",
    )
    print(schedule.items[0])

This will return a data payload with an ``items`` attribute containing a list of the returned ``Schedules``.
This is because ``client.schedule.get_many()`` `paginates` results by default. As the number of returned schedules can be
quite large, depending on the filtering parameters inputted, users can limit the number of returned
objects through the ``page`` and ``page_limit`` parameters. Every ``client.schedule.get_many()``
call will return, as part of the payload, the total number of schedules that match the filtering criteria in 
the ``total_number`` field. This enables programmatic queries to iterate over each returned "page" of ``Schedule``
results.

For example, here is how to limit the results to the first 10 matches:

.. code-block:: python
    
    from across.client import Client
    from datetime import datetime

    client = Client()
    schedule = client.schedule.get_many(
        page=1,
        page_limit=10,
        date_range_begin=datetime(2025, 12, 12),
        date_range_end=datetime(2025, 12, 19),
        telescope_names=["UVOT"],
        status="performed",
    )
    print(f"Number of schedules returned: {len(schedule.items)}")
    print(f"Total number of schedules matching parameters: {schedule.total_number}")

Retrieving All Schedules
^^^^^^^^^^^^^^^^^^^^^^^^^

To retrieve all schedules that match the input parameters, not just the most recent ones,
use the ``client.schedule.get_history()`` method. Unlike ``client.schedule.get_many()``, this
method will return `all` schedules that meet the filtering criteria. 

**Use when:** you want to retrieve all ``Schedule`` objects, including prior ``Schedules``
that were ingested into the ACROSS ``core-server`` with potentially out-of-date parameters.
This is useful for gaining information about how and when a ``Telescope's`` observing plans
may have changed.

.. code-block:: python
    
    from across.client import Client
    from datetime import datetime

    client = Client()
    schedule = client.schedule.get_history(
        date_range_begin=datetime(2025, 12, 12),
        date_range_end=datetime(2025, 12, 19),
        telescope_names=["UVOT"],
        status="planned",
    )
    print(schedule.items[0])

The returned data structure is the same as the ``client.schedule.get_many()`` method, and is
described in more detail below.

Example: Retrieve Swift planned observations in the last week
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Say a user would like to know everything that `Swift` planned to observe over the past week,
in pages of 10 results each. This can be done using ``client.schedule.get_many()``,
which will return only the most up-to-date planned schedules. The user can filter by observatory 
name to only retrieve those schedules from the three `Swift` telescopes, and can return the 
observations along with the schedules with the `include_observations` flag:

.. code-block:: python

    from across.client import Client
    from datetime import datetime, timedelta

    client = Client()

    past_week = datetime.now() - timedelta(days=7)
    schedule_page = client.schedule.get_many(
        page=1,
        page_limit=10,
        date_range_begin=past_week,
        status="planned",
        observatory_names=["Swift"],
        include_observations=True,
    )

    schedules = schedule_page.items
    print(schedules[0].model_dump_json())


Method Parameters
^^^^^^^^^^^^^^^^^^
While the ``client.schedule.get()`` method only takes a schedule ID, the ``client.schedule.get_many()``
and ``client.schedule.get_history()`` methods take a number of optional parameters as input. These are
shown below:

.. list-table:: schedule.get_many() and schedule.get_history() Parameters
   :widths: 20 25 65
   :header-rows: 1

   * - Attribute
     - Type
     - Description
   * - ``page``
     - int | None
     - The page of ``Schedule`` results to return
   * - ``page_limit``
     - int | None
     - The maximum number of ``Schedule`` objects per page to return
   * - ``date_range_begin``
     - datetime | None
     - Datetime for ``Schedules`` beginning on or after this date
   * - ``date_range_end``
     - datetime | None
     - Datetime for ``Schedules`` ending before or on this date
   * - ``status``
     - str | None
     - ``Schedule`` status (``planned``, ``scheduled``, or ``performed``)
   * - ``external_id``
     - str | None
     - Any external ID associated with the ``Schedule``
   * - ``fidelity``
     - str | None
     - Fidelity of the ``Schedule`` (``low`` or ``high``)
   * - ``created_on``
     - datetime | None
     - Datetime of creation in the ACROSS ``core-server``
   * - ``observatory_ids``
     - list[str] | None
     - Include only ``Schedules`` for ``Telescopes`` belonging to the ``Observatories`` with these IDs
   * - ``observatory_names``
     - list[str] | None
     - Include only ``Schedules`` for ``Telescopes`` belonging to the ``Observatories`` with these names
   * - ``telescope_ids``
     - list[str] | None
     - Include only ``Schedules`` for ``Telescopes`` with these IDs
   * - ``telescope_names``
     - list[str] | None
     - Include only ``Schedules`` for ``Telescopes`` with these names
   * - ``name``
     - str | None
     - Name of the ``Schedule``
   * - ``include_observations``
     - bool | None
     - Optionally include ``Observations`` with the returned ``Schedules``


``Schedule`` objects
^^^^^^^^^^^^^^^^^^^^^
The ``client.schedule.get()`` method returns a ``Schedule`` class object, while the 
``client.schedule.get_many()`` and ``client.schedule.get_history()`` methods return,
among other things, a list of ``Schedules``. Below are the attributes of a ``Schedule`` object:

.. list-table:: Schedule Attributes
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
     - Name of the schedule
   * - ``telescope_id``
     - str
     - ID of the ``Telescope`` this schedule belongs to in the ACROSS ``core-server``
   * - ``date_range``
     - DateRange
     - ``DateRange`` object containing begin and end times for the schedule
   * - ``external_id``
     - str | None
     - Any external ID associated with the schedule
   * - ``fidelity``
     - str | None
     - Fidelity of the schedule (``low`` or ``high``)
   * - ``observations``
     - list[Observation] | None
     - List of ``Observation`` objects belonging to the schedule
   * - ``observation_count``
     - int
     - Number of observations belonging to the schedule
   * - ``created_by_id``
     - str | None
     - ID of user that created the schedule in the ACROSS ``core-server``
   * - ``checksum``
     - str | None
     - Checksum to guarantee uniqueness of the schedule in the ACROSS ``core-server``

``PageSchedule`` objects
^^^^^^^^^^^^^^^^^^^^^^^^^

The ``client.schedule.get_many()`` and ``client.schedule.get_history()`` methods return paginated
``Schedules`` as a ``PageSchedule`` objects, described below:

.. list-table:: PageSchedule Attributes
   :widths: 20 25 65
   :header-rows: 1

   * - Attribute
     - Type
     - Description
   * - ``total_number``
     - int
     - Total number of schedules that match the filtering criteria
   * - ``page``
     - int
     - Current page of returned ``Schedules``
   * - ``page_limit``
     - int
     - Maximum number of returned ``Schedules`` for a page
   * - ``items``
     - list[Schedule]
     - The returned ``Schedules`` for this page

Creating Schedules
^^^^^^^^^^^^^^^^^^^

Authorized users may create and submit ``Schedules`` to the ACROSS ``core-server``. Unlike
the previous methods described so far, this action requires authentication. The ``client`` class
is built to handle authentication of user credentials in a number of ways:

  1. Passing your ``client_id`` and ``client_secret`` directly to the ``Client`` class
  2. The ``CredentialsStorage`` interface, which stores an ACROSS ``core-server`` access token
  3. Your local ``ACROSS_SERVER_ID`` and ``ACROSS_SERVER_SECRET`` environment variables

For example:

.. code-block:: python
    
    from across.client import Client

    ACROSS_CLIENT_ID = "your-service-account-uuid"
    ACROSS_CLIENT_SECRET = "your-service-account-secret"
    
    client = Client(
        client_id=ACROSS_CLIENT_ID,
        client_secret=ACROSS_CLIENT_SECRET,
    )

The ``Client`` will handle authenticating your credentials with the ``core-server`` and authorizing
access to restricted endpoints. For example, ``POSTing`` a new schedule to the ``core-server`` is
as easy as running

.. code-block:: python

    client.schedule.post(schedule=schedule)

where ``schedule`` is a ``ScheduleCreate`` object, containing many of the same fields
as the ``Schedule`` object described above.

If a user wants to batch submit multiple schedules, they can use the ``client.schedule.post_many()``
method, which takes a ``ScheduleCreateMany`` object, containing both a telescope ID and 
a list of ``ScheduleCreates``. 

Retrieving Observations
------------------------

Much like ``Schedules``, ``across-client`` has an ``observation`` module with
methods to get one or many ``Observation`` objects.

Retrieving an Observation by ID
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To get a single ``Observation``, use the ``client.observation.get()`` method, which takes a 
single ID of an ``Observation`` in the ACROSS system as input. This works analogously to the
``client.schedule.get()`` method demonstrated above.

Retrieving Many Observations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Users can filter for ``Observations`` across a number of input parameters using
``client.observation.get_many()``. **Note:** the results returned from this method are
not limited to a single ``Schedule`` object. Therefore, this method should be used when
users wish to query for all ``Observations`` of a target, area of sky, or time period across
multiple ``Schedules``.

Like ``client.schedule.get_many()``, this method returns paginated results. The pagination
parameters can be set by the user via the method arguments, and the ``Observations``
are again listed in the ``items`` attribute of the returned object.

Example #1: Retrieve completed observations of an area of the sky
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's say a user knows of an interesting astronomical object, and wants to know what
resources in the ACROSS system observed it in the last week. This can be done via a cone search, which
is supported through the arguments of the ``client.observation.get_many()`` method:

.. code-block:: python

    from across.client import Client
    from datetime import datetime, timedelta

    last_week = datetime.now() - timedelta(days=7)
    target_ra = 123.45
    target_dec = -54.32

    client = Client()
    observations_page = client.observation.get_many(
        status="performed",
        date_range_begin=last_week,
        cone_search_ra=target_ra,
        cone_search_dec=target_dec,
        cone_search_radius=5.0/3600.0,  # 5 arcseconds
    )
    observations = observations_page.items

Example #2: Retrieve observations by bandpass and type
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Suppose there's an interesting AGN, and a user would like to retrieve all spectroscopic
observations of it, planned or completed, in the optical wavelength regime. This is also
supported through the ``client.observation.get_many()`` method:

.. code-block:: python

    from across.client import Client

    target_ra = 87.65
    target_dec = 12.34

    client = Client()
    observations_page = client.observation.get_many(
        cone_search_ra=target_ra,
        cone_search_dec=target_dec,
        cone_search_radius=1.0,
        bandpass_min=2500.0,
        bandpass_max=9000.0,
        bandpass_type="angstrom",
        type="spectroscopy",
    )
    observations = observations_page.items

Method Parameters
^^^^^^^^^^^^^^^^^^
The ``client.observation.get_many()`` method takes a number of optional parameters as input. 
These are shown below:

.. list-table:: observation.get_many() Parameters
   :widths: 20 25 65
   :header-rows: 1

   * - Attribute
     - Type
     - Description
   * - ``page``
     - int | None
     - The page of ``Observation`` results to return
   * - ``page_limit``
     - int | None
     - The maximum number of ``Observation`` objects per page to return
   * - ``external_id``
     - str | None
     - Any external ID associated with the ``Observation``
   * - ``schedule_ids``
     - list[str] | None
     - Include only ``Observations`` for ``Schedules`` with these IDs
   * - ``observatory_ids``
     - list[str] | None
     - Include only ``Observations`` for ``Instruments`` on ``Telescopes`` belonging to the ``Observatories`` with these IDs
   * - ``telescope_ids``
     - list[str] | None
     - Include only ``Observations`` for ``Instruments`` on ``Telescopes`` with these IDs   
   * - ``instrument_ids``
     - list[str] | None
     - Include only ``Observations`` for ``Instruments`` with these IDs  
   * - ``status``
     - str | None
     - ``Observation`` status (``planned``, ``scheduled``, ``unscheduled``, ``performed``, or ``aborted``) 
   * - ``proposal``
     - str | None
     - Any external proposal name under which this ``Observation`` was submitted
   * - ``object_name``
     - str | None
     - Name of target object, if it exists  
   * - ``date_range_begin``
     - datetime | None
     - Datetime for ``Observations`` beginning on or after this date
   * - ``date_range_end``
     - datetime | None
     - Datetime for ``Observations`` ending before or on this date
   * - ``bandpass_min``
     - float | None
     - Minimum wavelength of bandpass for the ``Observation`` (in Angstroms)
   * - ``bandpass_max``
     - float | None
     - Maximum wavelength of bandpass for the ``Observation`` (in Angstroms)
   * - ``bandpass_type``
     - str | None
     - Unit of ``bandpass_min`` and ``bandpass_max`` (one of ``angstrom``, ``nm``, ``um``, or ``mm``)
   * - ``cone_search_ra``
     - float | None
     - Right Ascension of the center of the cone search (in degrees)
   * - ``cone_search_dec``
     - float | None
     - Declination of the center of the cone search (in degrees)
   * - ``cone_search_radius``
     - float | None
     - Radius of the cone search (in degrees)
   * - ``type``
     - str | None
     - Type of the ``Observation`` (one of ``imaging``, ``spectroscopy``, ``timing``, or ``slew``)
   * - ``depth_value``
     - float | None
     - Depth of the ``Observation``, in units of ``depth_unit``
   * - ``depth_unit``
     - str | None
     - Unit for the depth of the ``Observation`` (one of ``ab_mag``, ``vega_mag``, ``flux_erg``, or ``flux_jy``)

``Observation`` objects
^^^^^^^^^^^^^^^^^^^^^^^^
Below are some of the more relevant attributes of an ``Observation`` object:

.. list-table:: Observation Attributes
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
   * - ``object_name``
     - str
     - Name of the target object, if it exists
   * - ``instrument_id``
     - str
     - ID of the ``Instrument`` this observation belongs to in the ACROSS ``core-server``
   * - ``date_range``
     - DateRange
     - ``DateRange`` object containing begin and end times for the observation
   * - ``external_observation_id``
     - str | None
     - Any external ID associated with the observation
   * - ``pointing_position``
     - Coordinate | None
     - The coordinate (RA, dec) of the center of the observation, in degrees
   * - ``pointing_angle``
     - float | None
     - Roll angle of the observation, in degrees  
   * - ``object_position``
     - Coordinate | None
     - The coordinate (RA, dec) of the observation target, in degrees   
   * - ``exposure_time``
     - float | None
     - Duration of the observation
   * - ``depth``
     - UnitValue | None
     - A UnitValue (value, unit pair) describing the depth of the observation
   * - ``bandpass``
     - Bandpass
     - The bandpass (``WavelengthBandpass``) of the observation, describing minimum and maximum wavelengths of coverage
   * - ``schedule_id``
     - str | None
     - Id of the ``Schedule`` the observation belongs to
   * - ``created_by_id``
     - str | None
     - ID of user that created the schedule in the ACROSS ``core-server``

IVOA compliance
^^^^^^^^^^^^^^^

The ACROSS system also ensures IVOA compliance by including IVOA ObsLocTap
parameters in the ``Observation`` class. These include:

  - t_resolution
  - em_res_power
  - o_ucd
  - pol_states
  - pol_xel
  - category
  - priority
  - tracking_type

These parameters are ingested for observations when available, depending on the
source of the data.

API Reference
-------------

See the :doc:`Schedule API Reference </autoapi/across/client/apis/schedule/index>` 
and :doc:`Observation API Reference </autoapi/across/client/apis/observation/index>`
for complete class and function documentation.
