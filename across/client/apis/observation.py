from datetime import datetime

import across.sdk.v1 as sdk
from across.sdk.v1.api_client_wrapper import ApiClientWrapper


class Observation:
    """
    Client for interacting with Observation resources in the Across API.

    Provides methods to retrieve single or multiple observations
    by ID, name, observation information, or creation date.
    """

    def __init__(self, across_client: ApiClientWrapper):
        """
        Initialize an Observation client.

        Args:
            across_client (ApiClientWrapper):
                API client wrapper used to make requests to the Across API.
        """
        self.across_client = across_client

    def get(self, id: str, include_footprints: bool | None = None) -> sdk.Observation:
        """
        Retrieve a single Observation by ID.

        Args:
            id (str):
                The unique identifier of the Observation to retrieve.
            include_footprints (bool | None):
                Optionally include footprint of the observation.

        Returns:
            sdk.Observation:
                The requested Observation object.
        """
        return sdk.ObservationApi(self.across_client).get_observation(
            observation_id=id, include_footprints=include_footprints
        )

    def get_many(
        self,
        page: int | None = None,
        page_limit: int | None = None,
        external_id: str | None = None,
        schedule_ids: list[str | None] | None = None,
        observatory_ids: list[str] | None = None,
        telescope_ids: list[str] | None = None,
        instrument_ids: list[str] | None = None,
        status: sdk.ObservationStatus | None = None,
        proposal: str | None = None,
        object_name: str | None = None,
        date_range_begin: datetime | None = None,
        date_range_end: datetime | None = None,
        bandpass_min: float | None = None,
        bandpass_max: float | None = None,
        bandpass_type: sdk.WavelengthUnit | sdk.EnergyUnit | sdk.FrequencyUnit | None = None,
        cone_search_ra: float | None = None,
        cone_search_dec: float | None = None,
        cone_search_radius: float | None = None,
        type: sdk.ObservationType | None = None,
        depth_value: float | None = None,
        depth_unit: sdk.DepthUnit | None = None,
        include_footprints: bool | None = None,
    ) -> sdk.PageObservation:
        """
        Retrieve multiple observations filtered by optional criteria.

        Args:
            page (int | None):
                Filter by pagination page
            page_limit (int | None):
                Filter by number of records per page
            external_id (str | None):
                Filter by an external identifier.
            schedule_ids (list[str | None] | None):
                Filter by one or more schedule IDs.
            observatory_ids (list[str] | None):
                Filter by one or more observatory IDs.
            telescope_ids (list[str] | None):
                Filter by one or more telescope IDs.
            instrument_ids (list[str] | None):
                Filter by one or more instrument IDs.
            status (sdk.ObservationStatus | None):
                Filter by observation status.
            proposal (str | None):
                Filter by proposal identifier or name.
            object_name (str | None):
                Filter by target object name.
            date_range_begin (datetime | None):
                Filter for observations starting on or after this date.
            date_range_end (datetime | None):
                Filter for observations ending on or before this date.
            bandpass_min (float | None):
                Minimum bandpass value (in the unit defined by `bandpass_type`).
            bandpass_max (float | None):
                Maximum bandpass value (in the unit defined by `bandpass_type`).
            bandpass_type (sdk.WavelengthUnit | sdk.EnergyUnit| sdk.FrequencyUnit | None):
                Unit of bandpass measurement (wavelength, energy, or frequency unit).
            cone_search_ra (float | None):
                Right Ascension (RA) for cone search, in degrees.
            cone_search_dec (float | None):
                Declination (Dec) for cone search, in degrees.
            cone_search_radius (float | None):
                Search radius for cone search, in degrees.
            type (sdk.ObservationType | None):
                Filter by observation type.
            depth_value (float | None):
                Sensitivity or depth threshold value.
            depth_unit (sdk.DepthUnit | None):
                Unit for `depth_value`.
            include_footprints (bool | None):
                Optionally include footprint of the observation.

        Returns:
            list[sdk.Observation]:
                A list of observations matching the given filters.
        """
        return sdk.ObservationApi(self.across_client).get_observations(
            page=page,
            page_limit=page_limit,
            external_id=external_id,
            schedule_ids=schedule_ids,
            observatory_ids=observatory_ids,
            telescope_ids=telescope_ids,
            instrument_ids=instrument_ids,
            status=status,
            proposal=proposal,
            object_name=object_name,
            date_range_begin=date_range_begin,
            date_range_end=date_range_end,
            bandpass_min=bandpass_min,
            bandpass_max=bandpass_max,
            bandpass_type=bandpass_type,
            cone_search_ra=cone_search_ra,
            cone_search_dec=cone_search_dec,
            cone_search_radius=cone_search_radius,
            type=type,
            depth_value=depth_value,
            depth_unit=depth_unit,
            include_footprints=include_footprints,
        )

    def contains_point(
        self,
        ra: float,
        dec: float,
        page: int | None = None,
        page_limit: int | None = None,
        external_id: str | None = None,
        schedule_ids: list[str] | None = None,
        observatory_ids: list[str] | None = None,
        telescope_ids: list[str] | None = None,
        instrument_ids: list[str] | None = None,
        status: sdk.ObservationStatus | None = None,
        proposal: str | None = None,
        object_name: str | None = None,
        date_range_begin: datetime | None = None,
        date_range_end: datetime | None = None,
        bandpass_min: float | None = None,
        bandpass_max: float | None = None,
        bandpass_type: sdk.WavelengthUnit | sdk.EnergyUnit | sdk.FrequencyUnit | None = None,
        type: sdk.ObservationType | None = None,
        depth_value: float | None = None,
        depth_unit: sdk.DepthUnit | None = None,
        include_footprints: bool | None = None,
    ) -> sdk.PageObservation:
        """
        Retrieve multiple observations that contain a given point,
        filtered by optional criteria.

        Args:
            ra (float | None):
                Right Ascension (RA) of the point, in degrees.
            dec (float | None):
                Declination (Dec) of the point, in degrees.
            page (int | None):
                Filter by pagination page
            page_limit (int | None):
                Filter by number of records per page
            external_id (str | None):
                Filter by an external identifier.
            schedule_ids (list[str | None] | None):
                Filter by one or more schedule IDs.
            observatory_ids (list[str] | None):
                Filter by one or more observatory IDs.
            telescope_ids (list[str] | None):
                Filter by one or more telescope IDs.
            instrument_ids (list[str] | None):
                Filter by one or more instrument IDs.
            status (sdk.ObservationStatus | None):
                Filter by observation status.
            proposal (str | None):
                Filter by proposal identifier or name.
            object_name (str | None):
                Filter by target object name.
            date_range_begin (datetime | None):
                Filter for observations starting on or after this date.
            date_range_end (datetime | None):
                Filter for observations ending on or before this date.
            bandpass_min (float | None):
                Minimum bandpass value (in the unit defined by `bandpass_type`).
            bandpass_max (float | None):
                Maximum bandpass value (in the unit defined by `bandpass_type`).
            bandpass_type (sdk.WavelengthUnit | sdk.EnergyUnit | sdk.FrequencyUnit | None):
                Unit of the bandpass measurement.
            type (sdk.ObservationType | None):
                Filter by observation type.
            depth_value (float | None):
                Sensitivity or depth threshold value.
            depth_unit (sdk.DepthUnit | None):
                Unit for `depth_value`.
            include_footprints (bool | None):
                Optionally include footprint of the observation.

        Returns:
            list[sdk.Observation]:
                A list of observations matching the given filters that overlap with the
                given point.
        """
        return sdk.ObservationApi(self.across_client).contains_point(
            ra=ra,
            dec=dec,
            page=page,
            page_limit=page_limit,
            external_id=external_id,
            schedule_ids=schedule_ids,
            observatory_ids=observatory_ids,
            telescope_ids=telescope_ids,
            instrument_ids=instrument_ids,
            status=status,
            proposal=proposal,
            object_name=object_name,
            date_range_begin=date_range_begin,
            date_range_end=date_range_end,
            bandpass_min=bandpass_min,
            bandpass_max=bandpass_max,
            bandpass_type=bandpass_type,
            type=type,
            depth_value=depth_value,
            depth_unit=depth_unit,
            include_footprints=include_footprints,
        )
