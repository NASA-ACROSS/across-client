from datetime import datetime

import across.sdk.v1 as sdk
from across.sdk.v1.api_client_wrapper import ApiClientWrapper


class VisibilityCalculator:
    """
    Client for interacting with Visibility Calculator resources in the Across API.

    Provides methods to calculate individual instrument
    visibility windows by instrument ID.
    """

    def __init__(self, across_client: ApiClientWrapper):
        """
        Initialize a VisibilityCalculator client.

        Args:
            across_client (ApiClientWrapper):
                API client wrapper used to make requests to the Across API.
        """
        self.across_client = across_client

    def calculate_windows(
        self,
        instrument_id: str,
        ra: float | int,
        dec: float | int,
        date_range_begin: datetime,
        date_range_end: datetime,
        hi_res: bool | None = None,
        min_visibility_duration: int | None = None,
    ) -> sdk.VisibilityResult:
        """
        Retrieve visibility windows for a target and a single instrument.

        Args:
            instrument_id (str):
                The unique identifier of the instrument in the ACROSS core-server.
            ra (float | int):
                The Right Ascension of the target.
            dec (float | int):
                The Declination of the target.
            date_range_begin (datetime):
                The beginning of the date range to calculate the visibility windows.
            date_range_end (datetime):
                The end of the date range to calculate the visibility windows.
            hi_res (bool | None, optional):
                Flag to calculate high resolution windows (default is False)
            min_visibility_duration (int | None, optional):
                The minimum duration visibility windows to return, in seconds (default is 0).

        Returns:
            sdk.VisibilityResult:
                The requested visibility windows.
        """
        return sdk.ToolsApi(
            self.across_client
        ).calculate_windows_tools_visibility_calculator_windows_instrument_id_get(
            instrument_id=instrument_id,
            ra=ra,
            dec=dec,
            date_range_begin=date_range_begin,
            date_range_end=date_range_end,
            hi_res=hi_res,
            min_visibility_duration=min_visibility_duration,
        )
