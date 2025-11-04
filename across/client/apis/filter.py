import across.sdk.v1 as sdk
from across.sdk.v1.api_client_wrapper import ApiClientWrapper


class Filter:
    """
    Client for interacting with Filter resources in the Across API.

    Provides methods to retrieve single or multiple filters
    by ID, name, wavelength, or instrument information.
    """

    def __init__(self, across_client: ApiClientWrapper):
        """
        Initialize an Instrument client.

        Args:
            across_client (ApiClientWrapper):
                API client wrapper used to make requests to the Across API.
        """
        self.across_client = across_client

    def get(self, id: str) -> sdk.Filter:
        """
        Retrieve a single Filter by ID.

        Args:
            id (str):
                The unique identifier of the Filter to retrieve.

        Returns:
            sdk.Filter:
                The requested Filter object.
        """
        return sdk.FilterApi(self.across_client).get_filter_filter_id_get(filter_id=id)

    def get_many(
        self,
        name: str | None = None,
        covers_wavelength: float | None = None,
        instrument_name: str | None = None,
        instrument_id: str | None = None,
    ) -> list[sdk.Filter]:
        """
        Retrieve multiple filters filtered by optional criteria.

        Args:
            name (str | None, optional):
                Filter by filter name.
            covers_wavelength (float | none, optional):
                Filter by filters that contain wavelength value.
            instrument_name (str | None, optional):
                Filter by telescinstrumentope name.
            instrument_id (str | None, optional):
                Filter by instrument ID.

        Returns:
            list[sdk.Filter]:
                A list of filters matching the given filters.
        """
        return sdk.FilterApi(self.across_client).get_many_filter_get(
            name=name,
            covers_wavelength=covers_wavelength,
            instrument_name=instrument_name,
            instrument_id=instrument_id,
        )
