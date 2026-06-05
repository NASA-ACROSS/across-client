from datetime import datetime
from unittest.mock import MagicMock

import plotly.graph_objects as go
import pytest

import across.sdk.v1 as sdk
from across.client.apis import VisibilityCalculator
from across.client.apis.tools import CustomJointVisibilityResult, CustomVisibilityResult


class TestVisibilityCalculator:
    """
    Unit tests for the `VisibilityCalculator`.

    These tests validate the behavior of the `VisibilityCalculator` wrapper
    around the Across SDK by mocking out the underlying API calls.
    """

    class TestCalculateWindows:
        """
        Unit tests for the `VisibilityCalculator.calculate_windows()` method.
        """

        def test_should_return_visibility_windows(
            self,
            fake_instrument_id: str,
            fake_coordinate: sdk.Coordinate,
            fake_date_range: sdk.DateRange,
            fake_visibility_result: CustomVisibilityResult,
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
                fake_visibility_result (CustomVisibilityResut):
                    A mocked CustomVisibilityResult instance
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

    class TestCalculateJointWindows:
        """
        Unit tests for the `VisibilityCalculator.calculate_joint_windows()` method.
        """

        def test_should_return_joint_visibility_windows(
            self,
            fake_instrument_id: str,
            fake_second_instrument_id: str,
            fake_coordinate: sdk.Coordinate,
            fake_date_range: sdk.DateRange,
            fake_joint_visibility_result: CustomJointVisibilityResult,
        ) -> None:
            """
            Ensure that `VisibilityCalculator.calculate_joint_windows()` returns
            a joint visibility result when the SDK call is mocked.

            Args:
                fake_instrument_id (str):
                    A mocked instrument UUID
                fake_second_instrument_id (str):
                    A mocked second instrument UUID
                fake_coordinate (sdk.Coordinate):
                    A mocked `sdk.Coordinate` instance
                fake_date_range (sdk.DateRange):
                    A mocked `sdk.DateRange` instance
                fake_joint_visibility_result (CustomJointVisibilityResut):
                    A mocked CustomJointVisibilityResult instance
            """
            visibility_calculator = VisibilityCalculator(across_client=MagicMock())
            result = visibility_calculator.calculate_joint_windows(
                [fake_instrument_id, fake_second_instrument_id],
                fake_coordinate.ra,  # type: ignore[arg-type]
                fake_coordinate.dec,  # type: ignore[arg-type]
                fake_date_range.begin,
                fake_date_range.end,
            )
            assert result == fake_joint_visibility_result

        @pytest.mark.parametrize(
            "input_arg, index",
            [
                ("instrument_ids", 0),
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
            fake_second_instrument_id: str,
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
                fake_second_instrument_id (str):
                    A mocked second instrument UUID
                fake_coordinate (sdk.Coordinate):
                    A mocked `sdk.Coordinate` instance
                fake_date_range (sdk.DateRange):
                    A mocked `sdk.DateRange` instance
            """
            vis_calc = VisibilityCalculator(across_client=MagicMock())

            # Make a list of inputs that we can index for our asserts later
            fixture_inputs = {
                "instrument_ids": [fake_instrument_id, fake_second_instrument_id],
                "ra": fake_coordinate.ra,
                "dec": fake_coordinate.dec,
                "date_range_begin": fake_date_range.begin,
                "date_range_end": fake_date_range.end,
            }
            vis_calc.calculate_joint_windows(**fixture_inputs)  # type: ignore[arg-type]
            assert (
                mock_visibility_calculator_api.calculate_joint_windows_tools_visibility_calculator_windows_get.call_args.kwargs[
                    input_arg
                ]
                == fixture_inputs[input_arg]
            )

    class TestPlotVisibilityResult:
        """
        Unit tests for plotting visibility and joint visibility results
        """

        @pytest.mark.parametrize(
            "visibility_result", ["fake_visibility_result", "fake_joint_visibility_result"]
        )
        def test_should_return_plotly_figure(
            self,
            visibility_result: str,
            request: pytest.FixtureRequest,
        ) -> None:
            """
            Ensure that plotting the result of `VisibilityCalculator.calculate_windows()`
            returns a plotly graph object.

            Args:
                visibility_result (str):
                    A mocked VisibilityResult instance
                request: pytest.FixtureRequest
                    Pytest FixtureRequest object to load fixture value.
            """
            fake_visibility_result = request.getfixturevalue(visibility_result)
            fig = fake_visibility_result.plot()

            assert isinstance(fig, go.Figure)

        @pytest.mark.parametrize(
            "visibility_result", ["fake_visibility_result", "fake_joint_visibility_result"]
        )
        def test_should_use_existing_plot(
            self,
            visibility_result: str,
            request: pytest.FixtureRequest,
        ) -> None:
            """
            Plotting should use an input plotly figure.

            Args:
                visibility_result (str):
                    A mocked VisibilityResult instance
                request: pytest.FixtureRequest
                    Pytest FixtureRequest object to load fixture value.
            """
            fake_visibility_result = request.getfixturevalue(visibility_result)
            my_fig = go.Figure()
            fig = fake_visibility_result.plot(fig=my_fig)

            assert fig is my_fig

        @pytest.mark.parametrize(
            "visibility_result", ["fake_visibility_result", "fake_joint_visibility_result"]
        )
        def test_plot_should_set_layout_dimensions(
            self,
            visibility_result: str,
            request: pytest.FixtureRequest,
        ) -> None:
            """
            Should set the layout dimensions when passed as args

            Args:
                visibility_result (sdk.VisibilityResut):
                    A mocked VisibilityResult instance
                request: pytest.FixtureRequest
                    Pytest FixtureRequest object to load fixture value.
            """
            fake_visibility_result = request.getfixturevalue(visibility_result)
            width = 100
            height = 200
            fig = fake_visibility_result.plot(width=width, height=height)

            assert all([fig.layout.width == width, fig.layout.height == height])

        @pytest.mark.parametrize(
            "visibility_result", ["fake_visibility_result", "fake_joint_visibility_result"]
        )
        def test_plot_should_set_date_range(
            self,
            visibility_result: str,
            request: pytest.FixtureRequest,
        ) -> None:
            """
            Should set the yaxis date range when passed as args

            Args:
                visibility_result (str):
                    A mocked VisibilityResult instance
                request: pytest.FixtureRequest
                    Pytest FixtureRequest object to load fixture value.
            """
            fake_visibility_result = request.getfixturevalue(visibility_result)

            end = datetime(2026, 4, 1, 1, 0, 0)
            begin = datetime(2026, 4, 1, 0, 0, 0)
            fig = fake_visibility_result.plot(begin=begin, end=end)

            assert all(
                [
                    fig.layout.yaxis.range[0] == end,
                    fig.layout.yaxis.range[1] == begin,
                ]
            )

        def test_plot_should_set_x_tick_label(
            self,
            fake_visibility_result: CustomVisibilityResult,
        ) -> None:
            """
            Should set the windows' x-axis tick to passed-in name

            Args:
                fake_visibility_result (CustomVisibilityResut):
                    A mocked CustomVisibilityResult instance
            """
            name = "My Observatory"
            fig = fake_visibility_result.plot(observatory_name=name)

            assert fig.layout.xaxis.ticktext[0] == name

        def test_plot_should_set_window_x_offset(
            self,
            fake_visibility_result: CustomVisibilityResult,
        ) -> None:
            """
            Should set the windows' x-axis offset when passed as an arg

            Args:
                fake_visibility_result (CustomVisibilityResut):
                    A mocked CustomVisibilityResult instance
            """
            offset = 10
            fig = fake_visibility_result.plot(offset=offset)

            assert fig.layout.xaxis.tickvals[0] == offset

        def test_plot_joint_visibility_should_set_x_tick_labels(
            self,
            fake_joint_visibility_result: CustomJointVisibilityResult,
        ) -> None:
            """
            Should set the windows' x-axis ticks to passed-in names

            Args:
                fake_joint_visibility_result (CustomJointVisibilityResut):
                    A mocked CustomJointVisibilityResult instance
            """
            names = ["Observatory 1", "Observatory 2"]
            fig = fake_joint_visibility_result.plot(observatory_names=names)

            assert fig.layout.xaxis.ticktext == tuple(names)

        def test_plot_joint_visibility_should_set_window_x_offset(
            self,
            fake_joint_visibility_result: CustomJointVisibilityResult,
        ) -> None:
            """
            Should set the windows' x-axis offset when passed as an arg

            Args:
                fake_joint_visibility_result (CustomJointVisibilityResut):
                    A mocked CustomJointVisibilityResult instance
            """
            offset = 10
            fig = fake_joint_visibility_result.plot(offset=offset)

            assert fig.layout.xaxis.tickvals == (offset + 0 + 1, offset + 1 + 1)

        def test_plot_joint_visibility_should_set_name_to_none_if_not_provided(
            self,
            fake_joint_visibility_result: CustomJointVisibilityResult,
        ) -> None:
            """
            Should set the windows' x-axis tick to None if not passed in

            Args:
                fake_joint_visibility_result (CustomJointVisibilityResut):
                    A mocked CustomJointVisibilityResult instance
            """
            names = ["Observatory 1"]
            fig = fake_joint_visibility_result.plot(observatory_names=names)

            assert fig.layout.xaxis.ticktext == (names[0], None)
