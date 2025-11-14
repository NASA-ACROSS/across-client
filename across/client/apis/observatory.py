from datetime import datetime

import across.sdk.v1 as sdk
from across.sdk.v1.api_client_wrapper import ApiClientWrapper


class Observatory:
    """
    Client for interacting with Observatory resources in the Across API.

    Provides methods to retrieve single or multiple observatories
    by ID, name, type, telescope information, ephemeris type, or
    creation date.
    """

    def __init__(self, across_client: ApiClientWrapper):
        """
        Initialize an Observatory client.

        Args:
            across_client (ApiClientWrapper):
                API client wrapper used to make requests to the Across API.
        """
        self.across_client = across_client

    def get(self, id: str) -> sdk.Observatory:
        """
        Retrieve a single Observatory by ID.

        Args:
            id (str):
                The unique identifier of the observatory to retrieve.

        Returns:
            sdk.Observatory:
                The requested observatory object.
        """
        return sdk.ObservatoryApi(self.across_client).get_observatory(observatory_id=id)

    def get_many(
        self,
        name: str | None = None,
        type: sdk.ObservatoryType | None = None,
        telescope_name: str | None = None,
        telescope_id: str | None = None,
        ephemeris_type: list[sdk.EphemerisType] | None = None,
        created_on: datetime | None = None,
    ) -> list[sdk.Observatory]:
        """
        Retrieve multiple observatories filtered by optional criteria.

        Args:
            name (str | None, optional):
                Filter by observatory name.
            type (sdk.ObservatoryType | None, optional):
                Filter by observatory type.
            telescope_name (str | None, optional):
                Filter by telescope name.
            telescope_id (str | None, optional):
                Filter by telescope ID.
            ephemeris_type (list[sdk.EphemerisType] | None, optional):
                Filter by one or more ephemeris types.
            created_on (datetime | None, optional):
                Filter by creation timestamp.

        Returns:
            list[sdk.Observatory]:
                A list of observatories matching the given filters.
        """
        return sdk.ObservatoryApi(self.across_client).get_observatories(
            name=name,
            type=type,
            telescope_name=telescope_name,
            telescope_id=telescope_id,
            ephemeris_type=ephemeris_type,
            created_on=created_on,
        )
