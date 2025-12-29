Visibility Windows
========================================================================================

The ``across-client`` contains methods to calculate visibility windows for a given target
and instrument. These windows correspond to times when the instrument is not blocked by
any constraints and is therefore able to observe the target. Constraints which the ACROSS
system tracks include sun angle, moon angle, and Earth limb constraints, South Atlantic
Anomaly (SAA) constraints, and Altitude-Azimuth constraints.

Overview
---------

``across-client`` has a ``client.visibility_calculator`` module, which performs
visibility window calculations for a single instrument and target using the 
``calculate_windows()`` method. This method only needs an instrument ID, target
coordinates, a time range, and a few other optional parameters as user input;
all information regarding the instrument's constraints is stored and automatically
retrieved from the ACROSS ``core-server``. 

**Note:** the visibility window calculations return time ranges where the target
is *theoretically* able to be observed by the instrument. However, it does not
account for factors such as scheduling conflicts, turnaround times for targets of
opportunity, or other *feasibility* factors which may otherwise impact a target's 
observability. Therefore, these windows should be treated as necessary, but not
complete, conditions toward guaranteeing target observability.

Calculating Visibility Windows
--------------------------------

Calculating visibility windows using the ``across-client`` has these general steps:

1. Retrieve the instrument ID from the ``core-server``, if not known
2. Define some target and observation parameters
3. Set optional user parameters
4. Calculate

These steps can be shown as follows:

.. code-block:: python
    
    from across.client import Client
    from datetime import datetime, timedelta

    client = Client()

    # Step 1: Retrieve instrument ID from server
    instruments = client.instrument.get_many(name="UVOT")
    instrument_id = instruments[0].id

    # Step 2: Define target and observation parameters
    target_ra = 120.0
    target_dec = -20.0
    
    date_range_begin = datetime.now()
    date_range_end = datetime.now() + timedelta(days=1)

    # Step 3: Set optional parameters
    hi_res = True  # Calculate windows with minute resolution
    min_visibility_duration = 300  # Only return windows at least 300 secs long

    # Step 4: Calculate
    visibility_windows = client.visibility_calculator.calculate_windows(
        instrument_id=instrument_id,
        ra=target_ra,
        dec=target_dec,
        date_range_begin=date_range_begin,
        date_range_end=date_range_end,
        hi_res=hi_res,
        min_visibility_duration=min_visibility_duration,
    )

``calculate_windows()`` Method Parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Below is a description of the arguments to the 
``client.visibility_calculator.calculate_windows()`` method:

.. list-table:: ``visibility_calculator.calculate_windows()`` Parameters
   :widths: 20 25 65
   :header-rows: 1

   * - Attribute
     - Type
     - Description
   * - ``instrument_id``
     - str
     - The UUID of the ``Instrument`` from the ACROSS ``core-server``
   * - ``ra``
     - float
     - Right ascension of the target, in degrees
   * - ``dec``
     - float
     - Declination of the target, in degrees
   * - ``date_range_begin``
     - datetime
     - Datetime to begin the visibility calculation
   * - ``date_range_end``
     - datetime
     - Datetime to end the visibility calculation
   * - ``hi_res``
     - bool | None
     - Flag to calculate high-resolution (minute-resolution) windows instead of the default low-resolution (hour-resolution)
   * - ``min_visibility_duration``
     - int | None
     - Only return windows longer than this duration, in seconds   

Using Visibility Windows
--------------------------------

The ``client.visibility_calculator.calculate_windows()`` method returns a ``VisibilityResult``,
which contains the instrument ID as well as a list of the calculated windows. Each window,
in turn, has a  number of attributes.

First off are the ``begin`` and ``end`` attributes, which contain a ``datetime``, a 
``constraint``, and an ``observatory_id``. These record the times the window begins/ends 
and the constraint that is violated to lead to the window beginning and ending. Here is
an example of ``begin`` and ``end``:

.. code-block:: json
    
    {
        "begin": {
            "datetime": "2025-10-23T00:00:00",
            "constraint": "Window",
            "observatory_id": "d5faadca-c0bb-4bb8-b4e4-75149b435ae8"
        },
        "end": {
            "datetime": "2025-10-23T00:28:00",
            "constraint": "Earth Limb",
            "observatory_id": "d5faadca-c0bb-4bb8-b4e4-75149b435ae8"
        },
    }

In this example, the window begins because it is the start of the calculation 
(i.e. it begins at ``date_range_begin``) and ends when the instrument is 
constrained by the Earth limb.

Next, each window has a ``max_visibility_duration`` attribute which gives
the total duration of the window, in seconds. Finally, it has a ``constraint_reason``
attribute, listing the begin and end constraints that are also given in the window
above, like so:

.. code-block:: json

    {
        "constraint_reason": {
            "start_reason": "Observatory Window",
            "end_reason": "Observatory Earth Limb",
        },
    }

Example: Listing the start and stop times of all visibility windows
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In this example, we will calculate the visibility windows for the same
target as in the above example, and print the begin and end times for each
window in a human-readable way:

.. code-block:: python
    
    from across.client import Client
    from datetime import datetime, timedelta

    client = Client()

    instruments = client.instrument.get_many(name="UVOT")
    instrument_id = instruments[0].id

    target_ra = 120.0
    target_dec = -20.0
    
    date_range_begin = datetime.now()
    date_range_end = datetime.now() + timedelta(days=1)
    hi_res = True

    visibility_windows = client.visibility_calculator.calculate_windows(
        instrument_id=instrument_id,
        ra=target_ra,
        dec=target_dec,
        date_range_begin=date_range_begin,
        date_range_end=date_range_end,
        hi_res=hi_res,
    )

    print("Start time:   End time:   ")
    for window in visibility_windows.visibility_windows:
        print(
            window.window.begin.datetime,
            " | ",
            window.window.end.datetime,
        )

Calculated Visibility objects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Below is a description of the attributes of all objects
returned from a visibility window calculation:

.. list-table:: VisibilityResult Attributes
   :widths: 20 25 65
   :header-rows: 1

   * - Attribute
     - Type
     - Description
   * - ``instrument_id``
     - str
     - The ACROSS ``core-server`` ID of the instrument for the calculated windows
   * - ``visibility_windows``
     - list[VisibilityWindow]
     - The calculated visibility windows

.. list-table:: VisibilityWindow Attributes
   :widths: 20 25 65
   :header-rows: 1

   * - Attribute
     - Type
     - Description
   * - ``window``
     - Window
     - An individual visibility window
   * - ``max_visibility_duration``
     - int
     - The duration of the window, in seconds
   * - ``constraint_reason``
     - ConstraintReason
     - Object describing the start and end constraints for the window

.. list-table:: Window Attributes
   :widths: 20 25 65
   :header-rows: 1

   * - Attribute
     - Type
     - Description
   * - ``begin``
     - ConstrainedDate
     - Object containing the window start time and constraint reason
   * - ``end``
     - ConstrainedDate
     - Object containing the window start time and constraint reason

.. list-table:: ConstrainedDate Attributes
   :widths: 20 25 65
   :header-rows: 1

   * - Attribute
     - Type
     - Description
   * - ``datetime``
     - datetime
     - Datetime of the window boundary
   * - ``constraint``
     - str
     - The constraint type that begins or ends at ``datetime``
   * - ``observatory_id``
     - str
     - the ACROSS ``core-server`` ID of the observatory the instrument belongs to 

.. list-table:: ConstraintReason Attributes
   :widths: 20 25 65
   :header-rows: 1

   * - Attribute
     - Type
     - Description
   * - ``start_reason``
     - str
     - The reason (i.e. the constraint that was lifted) for the window to begin
   * - ``end_reason``
     - str
     - The reason (i.e. the constraint that was violated) for the window to end

API Reference
-------------

See the :doc:`API Reference </autoapi/across/client/apis/tools/index>` for complete 
class and function documentation.
