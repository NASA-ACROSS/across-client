from unittest.mock import MagicMock
from uuid import uuid4

import across.sdk.v1 as sdk
from across.client.apis import Instrument


class TestGet:
    """
    Unit tests for the `Instrument.get`.

    These tests validate the behavior of the `Instrument` wrapper
    around the Across SDK by mocking out the underlying API calls.
    """

    def test_should_return_instrument(self, fake_instrument: sdk.Instrument) -> None:
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

    def test_should_return_instruments(self, fake_instrument: sdk.Instrument) -> None:
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
