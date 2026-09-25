from datetime import datetime
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

import across.sdk.v1 as sdk


@pytest.fixture
def fake_instrument() -> sdk.Instrument:
    """
    Create a fake `sdk.Instrument` instance for testing.

    This fixture returns a fully populated Instrument object with
    mock values for ID, creation date, name, type, observatory, and
    instruments. It is used as a predictable return value in
    tests that require an Instrument.
    """
    return sdk.Instrument(
        id=str(uuid4()),
        created_on=datetime.fromisoformat("2025-07-15T00:00:00"),
        name="Treedome Instrument",
        short_name="TI",
        telescope=sdk.IDNameSchema(id=str(uuid4()), name="Treedome Telescope", short_name="TT"),
        filters=[
            sdk.Filter(
                id=str(uuid4()),
                created_on=datetime.fromisoformat("2025-07-15T00:00:00"),
                name="Treedome Filter",
                peak_wavelength=6500,
                min_wavelength=6000,
                max_wavelength=7000,
                is_operational=True,
                instrument_id=str(uuid4()),
                sensitivity_depth=24,
                sensitivity_depth_unit=1,
                sensitivity_time_seconds=600,
                reference_url="omegle.com",
            )
        ],
        footprints=[
            [
                sdk.Point(x=-1, y=1),
                sdk.Point(x=1, y=1),
                sdk.Point(x=1, y=-1),
                sdk.Point(x=-1, y=-1),
                sdk.Point(x=-1, y=1),
            ]
        ],
    )


@pytest.fixture
def mock_instrument_api(fake_instrument: sdk.Instrument) -> MagicMock:
    """
    Mock implementation of the `InstrumentApi`.

    This fixture creates a `MagicMock` with preconfigured
    `get_instruments` and `get_instrument` methods that
    return the `fake_instrument`. It simulates API calls
    without making real network requests.
    """
    mock = MagicMock()
    mock.get_instruments = MagicMock(return_value=[fake_instrument])
    mock.get_instrument = MagicMock(return_value=fake_instrument)
    return mock


@pytest.fixture
def mock_instrument_api_cls(mock_instrument_api: MagicMock) -> MagicMock:
    """
    Mock class for `sdk.InstrumentApi`.

    This fixture returns a `MagicMock` constructor that produces
    the `mock_instrument_api` instance when called. It allows
    tests to patch the SDK API client at the class level.
    """
    mock_cls = MagicMock(return_value=mock_instrument_api)
    return mock_cls


@pytest.fixture(autouse=True)
def patch_sdk(
    monkeypatch: pytest.MonkeyPatch,
    mock_instrument_api_cls: MagicMock,
) -> None:
    """
    Automatically patch the `sdk.InstrumentApi` class with a mock.

    This fixture is applied to all tests (`autouse=True`).
    It replaces `sdk.InstrumentApi` with the `mock_instrument_api_cls`,
    ensuring that all instrument-related API calls are mocked
    throughout the test suite.
    """
    monkeypatch.setattr(sdk, "InstrumentApi", mock_instrument_api_cls)
