from datetime import datetime

import plotly.graph_objects as go

import across.sdk.v1 as sdk
from across.sdk.v1.api_client_wrapper import ApiClientWrapper
from across.tools.core.plotting import plot_joint_visibility_windows, plot_visibility_windows


class CustomVisibilityResult(sdk.VisibilityResult):
    """
    Class to extend the sdk.VisibilityResult object to add
    plotting functionality.
    """

    def plot(
        self,
        observatory_name: str | None = None,
        begin: datetime | None = None,
        end: datetime | None = None,
        fig: go.Figure | None = None,
        offset: int | float = 0,
        width: int = 700,
        height: int = 1000,
    ) -> go.Figure:
        """
        Method to visualize visibility windows using plotly.

        Parameters
        ----------
        fig : go.Figure, optional
            An existing plotly figure to add to, by default None
        observatory_name: str, optional
            The name of the observatory for these window, by default None
        begin: datetime, optional
            The start datetime to plot, by default None
        end: datetime, optional
            The end datetime to plot, by default None
        offset : int | float, optional
            The x-axis offset to plot new visibility windows, by default 0
        width: int, optional
            The width of the plot, in pixels. Defaults to 700
        height: int, optional
            The height of the plot, in pixels. Defaults to 1000

        Returns
        -------
        go.Figure
            The plotly figure containing the footprint plot
        """
        if fig is None:
            fig = go.Figure()

        fig = plot_visibility_windows(
            visibility_windows=[window.model_dump() for window in self.visibility_windows],
            observatory_name=observatory_name,
            fig=fig,
            offset=offset,
        )

        fig.update_layout(
            title="Visibility Windows",
            yaxis=dict(
                title="Time (UTC)",
                range=[end, begin],  # descending time
                type="date",
                autorange=False,  # don't resize
            ),
            xaxis=dict(
                title="Visibility Windows",
                tickvals=[offset],
                ticktext=[observatory_name if observatory_name is not None else ""],
            ),
            width=width,
            height=height,
        )
        return fig


class CustomJointVisibilityResult(sdk.JointVisibilityResult):
    """
    Class to extend the sdk.JointVisibilityResult object to add
    plotting functionality.
    """

    def plot(
        self,
        observatory_names: list[str] | None = None,
        begin: datetime | None = None,
        end: datetime | None = None,
        fig: go.Figure | None = None,
        offset: int | float = 0,
        width: int = 700,
        height: int = 1000,
    ) -> go.Figure:
        """
        Plot the resulting joint and single-instrument visibility windows.

        Parameters
        ----------
        fig : go.Figure, optional
            An existing plotly figure to add to, by default None
        observatory_names: list[str], optional
            The names of the observatories for these windows, by default None
        begin: datetime, optional
            The start datetime to plot, by default None
        end: datetime, optional
            The end datetime to plot, by default None
        offset : int | float, optional
            The x-axis offset to plot new visibility windows, by default 0
        width: int, optional
            The width of the plot, in pixels. Defaults to 700
        height: int, optional
            The height of the plot, in pixels. Defaults to 1000

        Returns
        -------
        go.Figure
            The plotly figure containing the footprint plot
        """
        if fig is None:
            fig = go.Figure()

        tickvals = []
        ticktext = []
        for i, visibility_windows in enumerate(self.observatory_visibility_windows.values()):
            if observatory_names is not None:
                try:
                    observatory_name = observatory_names[i]
                except IndexError:
                    observatory_name = None
            else:
                observatory_name = None

            fig = plot_visibility_windows(
                visibility_windows=[window.model_dump() for window in visibility_windows],
                observatory_name=observatory_name,
                fig=fig,
                offset=offset + i + 1,
            )
            tickvals.append(offset + i + 1)
            ticktext.append(observatory_name)

        min_extent = min(tickvals)
        max_extent = max(tickvals)
        fig = plot_joint_visibility_windows(
            visibility_windows=[window.model_dump() for window in self.visibility_windows],
            min_extent=min_extent,
            max_extent=max_extent,
            fig=fig,
        )

        fig.update_layout(
            title="Visibility Windows",
            yaxis=dict(
                title="Time (UTC)",
                range=[end, begin],  # descending time
                type="date",
                autorange=False,  # don't resize
            ),
            xaxis=dict(
                title="Visibility Windows",
                tickvals=tickvals,
                ticktext=ticktext,
            ),
            width=width,
            height=height,
        )
        return fig


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
    ) -> CustomVisibilityResult:
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
        tools_result = sdk.ToolsApi(
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

        result_with_plots = CustomVisibilityResult(
            instrument_id=tools_result.instrument_id,
            visibility_windows=tools_result.visibility_windows,
        )
        return result_with_plots

    def calculate_joint_windows(
        self,
        instrument_ids: list[str | None],
        ra: float | int,
        dec: float | int,
        date_range_begin: datetime,
        date_range_end: datetime,
        hi_res: bool | None = None,
        min_visibility_duration: int | None = None,
    ) -> CustomJointVisibilityResult:
        """
        Retrieve joint visibility windows for a target and multiple instruments.

        Args:
            instrument_ids (list[str]):
                List of unique identifiers of the instruments in the ACROSS core-server.
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
        tools_result = sdk.ToolsApi(
            self.across_client
        ).calculate_joint_windows_tools_visibility_calculator_windows_get(
            instrument_ids=instrument_ids,
            ra=ra,
            dec=dec,
            date_range_begin=date_range_begin,
            date_range_end=date_range_end,
            hi_res=hi_res,
            min_visibility_duration=min_visibility_duration,
        )

        result_with_plots = CustomJointVisibilityResult(
            instrument_ids=tools_result.instrument_ids,
            visibility_windows=tools_result.visibility_windows,
            observatory_visibility_windows=tools_result.observatory_visibility_windows,
        )
        return result_with_plots
