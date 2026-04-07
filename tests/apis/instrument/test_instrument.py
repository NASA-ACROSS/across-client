from unittest.mock import MagicMock
from uuid import uuid4

import plotly.graph_objects as go

from across.client.apis import Instrument
from across.client.apis.instrument import CustomInstrument


class TestGet:
    """
    Unit tests for the `Instrument.get`.

    These tests validate the behavior of the `Instrument` wrapper
    around the Across SDK by mocking out the underlying API calls.
    """

    def test_should_return_instrument(self, fake_instrument: CustomInstrument) -> None:
        """
        Ensure that `Instrument.get()` returns the expected instrument
        object when the SDK call is mocked.

        Args:
            fake_instrument (sdk.Instrument):
                A mocked `sdk.Instrument` instance returned by the patched API.
        """
        instrument = Instrument(across_client=MagicMock())
        result = instrument.get(str(uuid4()))
        assert result == fake_instrument

    def test_should_be_called_with_value(self, mock_instrument_api: MagicMock) -> None:
        """
        Verify that `Instrument.get()` calls the underlying
        `InstrumentApi.get_instrument()` with the correct
        instrument ID.

        Args:
            mock_instrument_api (MagicMock):
                A mocked instance of `InstrumentApi`.
        """
        id = str(uuid4())
        instrument = Instrument(across_client=MagicMock())
        instrument.get(id)
        mock_instrument_api.get_instrument.assert_called_once_with(instrument_id=id)


class TestGetMany:
    """
    Unit tests for the `Instrument.get_many`.
    """

    def test_should_return_instruments(self, fake_instrument: CustomInstrument) -> None:
        """
        Ensure that `Instrument.get_many()` returns a list of
        instruments when the SDK call is mocked.
        Args:
            fake_instrument (sdk.Instrument):
                A mocked `sdk.Instrument` instance returned by the patched API.
        """
        instrument = Instrument(across_client=MagicMock())
        result = instrument.get_many()
        assert result == [fake_instrument]


class TestPlotFootprint:
    """
    Unit tests for `CustomInstrument.plot_footprints`.
    """

    def test_should_return_plotly_figure_when_plotting(
        self,
        fake_instrument: CustomInstrument,
    ) -> None:
        """
        Should return a plotly Figure when plotting instrument footprints
        """
        fig = fake_instrument.plot_footprint()

        assert isinstance(fig, go.Figure)

    def test_plot_should_add_to_existing_figure(
        self,
        fake_instrument: CustomInstrument,
    ) -> None:
        """
        Should add the instrument footprint to an existing plotly Figure
        """
        existing_fig = go.Figure()
        fig = fake_instrument.plot_footprint(fig=existing_fig)

        assert fig is existing_fig

    def test_plot_should_set_detector_color_and_name(
        self,
        fake_instrument: CustomInstrument,
    ) -> None:
        """
        Should set the detector color and name when plotting the instrument footprint
        """
        name = "Test Detector"
        color = "red"
        fig = fake_instrument.plot_footprint(name=name, color=color)

        # Check that the detector name and color are set in the figure data
        found = False
        for trace in fig.data:
            if trace.name == name and trace.line.color == color:  # type: ignore[attr-defined]
                found = True
                break

        assert found

    def test_plot_should_only_show_legend_once(
        self,
        fake_instrument: CustomInstrument,
    ) -> None:
        """
        Should only show the legend once when plotting multiple footprints with the same name
        """
        name = "Test Detector"
        fig = fake_instrument.plot_footprint(name=name)
        fig = fake_instrument.plot_footprint(fig=fig, name=name)

        # find the unique legend entries
        legend_count = len(set(trace.name for trace in fig.data if trace.name == name))  # type: ignore[attr-defined]

        assert legend_count == 1

    def test_plot_should_set_lon_lat_ticks(
        self,
        fake_instrument: CustomInstrument,
    ) -> None:
        """
        Should set longitude and latitude ticks
        """
        lon = 30
        lat = 45

        fig = fake_instrument.plot_footprint(lat_axis_tick=lat, lon_axis_tick=lon)
        assert all([fig.layout.geo.lataxis.dtick == lat, fig.layout.geo.lonaxis.dtick == lon])
