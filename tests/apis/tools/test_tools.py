from unittest.mock import MagicMock

import pytest

import across.sdk.v1 as sdk
from across.client.apis import VisibilityCalculator


class TestVisibilityCalculator:
    """
    Unit tests for the `VisibilityCalculator`.

    These tests validate the behavior of the `VisibilityCalculator` wrapper
    around the Across SDK by mocking out the underlying API calls.
    """

    def test_should_return_visibility_windows(
        self,
        fake_instrument_id: str,
        fake_coordinate: sdk.Coordinate,
        fake_date_range: sdk.DateRange,
        fake_visibility_result: sdk.VisibilityResult,
    ) -> None:
        """
        Ensure that `VisibilityCalculator.calculate_windows()` returns
        visibility results when the SDK call is mocked.

        Args:
            fake_instrument_id (str):
                A mocked instrument UUID
            fake_coordinate (sdk.Coordinate):
                A mocked `sdk.Coordinate` instance
            fake_date_range (sdk.DateRange):
                A mocked `sdk.DateRange` instance
            fake_visibility_result (sdk.VisibilityResut):
                A mocked sdk.VisibilityResult instance
        """
        visibility_calculator = VisibilityCalculator(across_client=MagicMock())
        result = visibility_calculator.calculate_windows(
            fake_instrument_id,
            fake_coordinate.ra,  # type: ignore[arg-type]
            fake_coordinate.dec,  # type: ignore[arg-type]
            fake_date_range.begin,
            fake_date_range.end,
        )
        assert result == fake_visibility_result

    @pytest.mark.parametrize(
        "input_arg, index",
        [
            ("instrument_id", 0),
            ("ra", 1),
            ("dec", 2),
            ("date_range_begin", 3),
            ("date_range_end", 4),
        ],
    )
    def test_should_be_called_with_value(
        self,
        input_arg: str,
        index: int,
        mock_visibility_calculator_api: MagicMock,
        fake_instrument_id: str,
        fake_coordinate: sdk.Coordinate,
        fake_date_range: sdk.DateRange,
    ) -> None:
        """
        Verify that `VisibilityCalculator.calculate_windows()` calls the underlying
        `ToolsApi.calculate_windows_tools_visibility_calculator_windows_instrument_id_get()`
        with the correct parameters.

        Args:
            input_arg (str):
                Parametrized string giving name of input to the mocked API call
            index (int):
                The index of the parametrized input arg to the API call input
            mock_visibility_calculator_api (MagicMock):
                A mocked instance of `ToolsApi`
            fake_instrument_id (str):
                A mocked instrument UUID
            fake_coordinate (sdk.Coordinate):
                A mocked `sdk.Coordinate` instance
            fake_date_range (sdk.DateRange):
                A mocked `sdk.DateRange` instance
        """
        vis_calc = VisibilityCalculator(across_client=MagicMock())

        # Make a list of inputs that we can index for our asserts later
        fixture_inputs = {
            "instrument_id": fake_instrument_id,
            "ra": fake_coordinate.ra,
            "dec": fake_coordinate.dec,
            "date_range_begin": fake_date_range.begin,
            "date_range_end": fake_date_range.end,
        }
        vis_calc.calculate_windows(**fixture_inputs)  # type: ignore[arg-type]
        assert (
            mock_visibility_calculator_api.calculate_windows_tools_visibility_calculator_windows_instrument_id_get.call_args.kwargs[
                input_arg
            ]
            == fixture_inputs[input_arg]
        )
