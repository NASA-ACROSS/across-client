from datetime import datetime

import plotly.graph_objects as go

import across.sdk.v1 as sdk
from across.sdk.v1.api_client_wrapper import ApiClientWrapper
from across.tools.core.plotting import plot_footprint
from across.tools.core.schemas import Coordinate, Polygon


class CustomInstrument(sdk.Instrument):
    """
    Class to extend the sdk.Instrument object to add
    plotting functionality.
    """

    def plot_footprint(
        self,
        fig: go.Figure | None = None,
        name: str | None = None,
        color: str | None = None,
        lat_axis_tick: int = 30,
        lon_axis_tick: int = 60,
    ) -> go.Figure:
        """
        Method to plot the footprint using plotly.
        Calls the across-tools plotting core functionality and configures the plot
        layout to user specifications.

        Parameters
        ----------
        fig : go.Figure, optional
            An existing plotly figure to add the footprint to, by default None
        name : str | None, optional
            The name to assign to the detector traces, by default None
        color : str | None, optional
            The color to assign to the detector traces, by default None
        lat_axis_tick : int, optional
            The latitude axis tick interval, by default 30
        lon_axis_tick : int, optional
            The longitude axis tick interval, by default 60
        Returns
        -------
        go.Figure
            The plotly figure containing the footprint plot
        """
        if fig is None:
            fig = go.Figure()
            fig.update_layout(
                title="Footprint Visualization",
                geo=dict(
                    projection_type="mollweide",
                    showland=False,
                    showcountries=False,
                    showcoastlines=False,
                    lataxis=dict(showgrid=True, dtick=lat_axis_tick),
                    lonaxis=dict(showgrid=True, dtick=lon_axis_tick),
                ),
            )

        if self.footprints is not None:
            detectors = []
            for footprint in self.footprints:
                coordinates = [Coordinate(ra=coord.x, dec=coord.y) for coord in footprint]
                detectors.append(Polygon(coordinates=coordinates))

            fig = plot_footprint(
                detectors=[detector.model_dump() for detector in detectors],
                name=name,
                fig=fig,
                color=color,
            )

        return fig


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

    def get(self, id: str) -> CustomInstrument:
        """
        Retrieve a single Instrument by ID.

        Args:
            id (str):
                The unique identifier of the Instrument to retrieve.

        Returns:
            sdk.Instrument:
                The requested Instrument object.
        """
        sdk_instrument = sdk.InstrumentApi(self.across_client).get_instrument(instrument_id=id)
        return CustomInstrument(
            id=sdk_instrument.id,
            created_on=sdk_instrument.created_on,
            name=sdk_instrument.name,
            short_name=sdk_instrument.short_name,
            telescope=sdk_instrument.telescope,
            footprints=sdk_instrument.footprints,
            filters=sdk_instrument.filters,
            constraints=sdk_instrument.constraints,
            visibility_type=sdk_instrument.visibility_type,
        )

    def get_many(
        self,
        name: str | None = None,
        telescope_name: str | None = None,
        telescope_id: str | None = None,
        created_on: datetime | None = None,
    ) -> list[CustomInstrument]:
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
        sdk_instruments = sdk.InstrumentApi(self.across_client).get_instruments(
            name=name,
            telescope_name=telescope_name,
            telescope_id=telescope_id,
            created_on=created_on,
        )
        return [
            CustomInstrument(
                id=sdk_instrument.id,
                created_on=sdk_instrument.created_on,
                name=sdk_instrument.name,
                short_name=sdk_instrument.short_name,
                telescope=sdk_instrument.telescope,
                footprints=sdk_instrument.footprints,
                filters=sdk_instrument.filters,
                constraints=sdk_instrument.constraints,
                visibility_type=sdk_instrument.visibility_type,
            )
            for sdk_instrument in sdk_instruments
        ]
