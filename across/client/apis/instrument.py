from datetime import datetime

import across.sdk.v1 as sdk
from across.sdk.v1.api_client_wrapper import ApiClientWrapper


class Instrument:
    """
    Client for interacting with Instrument resources in the Across API.

    Provides methods to retrieve single or multiple instrument
    by ID, name, instrument information, or creation date.
    """

    def __init__(self, across_client: ApiClientWrapper):
        """
        Initialize an Instrument client.

        Args:
            across_client (ApiClientWrapper):
                API client wrapper used to make requests to the Across API.
        """
        self.across_client = across_client

    def get(self, id: str) -> sdk.Instrument:
        """
        Retrieve a single Instrument by ID.

        Args:
            id (str):
                The unique identifier of the Instrument to retrieve.

        Returns:
            sdk.Instrument:
                The requested Instrument object.
        """
        return sdk.InstrumentApi(self.across_client).get_instrument(instrument_id=id)

    def get_many(
        self,
        name: str | None = None,
        telescope_name: str | None = None,
        telescope_id: str | None = None,
        created_on: datetime | None = None,
    ) -> list[sdk.Instrument]:
        """
        Retrieve multiple instruments filtered by optional criteria.

        Args:
            name (str | None, optional):
                Filter by instrument name.
            telescope_name (str | None, optional):
                Filter by telescope name.
            telescope_id (str | None, optional):
                Filter by telescope ID.
            created_on (datetime | None, optional):
                Filter by creation timestamp.

        Returns:
            list[sdk.Instrument]:
                A list of instruments matching the given filters.
        """
        return sdk.InstrumentApi(self.across_client).get_instruments(
            name=name,
            telescope_name=telescope_name,
            telescope_id=telescope_id,
            created_on=created_on,
        )
