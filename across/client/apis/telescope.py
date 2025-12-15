from datetime import datetime

import across.sdk.v1 as sdk
from across.sdk.v1.api_client_wrapper import ApiClientWrapper


class Telescope:
    """
    Client for interacting with Telescope resources in the Across API.

    Provides methods to retrieve single or multiple telescopes
    by ID, name, instrument information, or creation date.
    """

    def __init__(self, across_client: ApiClientWrapper):
        """
        Initialize an Telescope client.

        Args:
            across_client (ApiClientWrapper):
                API client wrapper used to make requests to the Across API.
        """
        self.across_client = across_client

    def get(self, id: str) -> sdk.Telescope:
        """
        Retrieve a single Telescope by ID.

        Args:
            id (str):
                The unique identifier of the Telescope to retrieve.

        Returns:
            sdk.Telescope:
                The requested Telescope object.
        """
        return sdk.TelescopeApi(self.across_client).get_telescope(telescope_id=id)

    def get_many(
        self,
        name: str | None = None,
        instrument_name: str | None = None,
        instrument_id: str | None = None,
        created_on: datetime | None = None,
        include_filters: bool | None = None,
        include_footprints: bool | None = None,
    ) -> list[sdk.Telescope]:
        """
        Retrieve multiple telescopes filtered by optional criteria.

        Args:
            name (str | None, optional):
                Filter by telescope name.
            instrument_name (str | None, optional):
                Filter by instrument name.
            instrument_id (str | None, optional):
                Filter by instrument ID.
            created_on (datetime | None, optional):
                Filter by creation timestamp.
            include_filters (bool | None, optional):
                Include telescope instrument filters with the
                returned values (defaults to False)
            include_footprints (bool | None, optional):
                Include telescope instrument footprints with the
                returned values (defaults to False)

        Returns:
            list[sdk.Telescope]:
                A list of telescopes matching the given filters.
        """
        return sdk.TelescopeApi(self.across_client).get_telescopes(
            name=name,
            instrument_name=instrument_name,
            instrument_id=instrument_id,
            created_on=created_on,
            include_filters=include_filters,
            include_footprints=include_footprints,
        )
