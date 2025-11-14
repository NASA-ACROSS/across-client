from datetime import datetime
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

import across.sdk.v1 as sdk


@pytest.fixture
def fake_observatory() -> sdk.Observatory:
    """
    Create a fake `sdk.Observatory` instance for testing.

    This fixture returns a fully populated Observatory object with
    mock values for ID, creation date, name, type, telescopes, and
    ephemeris types. It is used as a predictable return value in
    tests that require an Observatory.
    """
    return sdk.Observatory(
        id=str(uuid4()),
        created_on=datetime.fromisoformat("2025-07-15T00:00:00"),
        name="Treedome Space Observatory",
        short_name="MT",
        type=sdk.ObservatoryType.SPACE_BASED,
        telescopes=[sdk.IDNameSchema(id=str(uuid4()), name="Treedome Telescope", short_name="tree")],
        reference_url="cartoonnetwork.com",
        ephemeris_types=[
            sdk.ObservatoryEphemerisType(
                ephemeris_type=sdk.EphemerisType.TLE,
                priority=1,
                parameters=sdk.Parameters(sdk.TLEParameters(norad_id=123456, norad_satellite_name="MOCK")),
            )
        ],
        operational=sdk.NullableDateRange(
            begin=datetime(2020, 1, 1, 0, 0, 0),
            end=None,
        ),
    )


@pytest.fixture
def mock_observatory_api(fake_observatory: sdk.Observatory) -> MagicMock:
    """
    Mock implementation of the `ObservatoryApi`.

    This fixture creates a `MagicMock` with preconfigured
    `get_observatories` and `get_observatory` methods that
    return the `fake_observatory`. It simulates API calls
    without making real network requests.
    """
    mock = MagicMock()
    mock.get_observatories = MagicMock(return_value=[fake_observatory])
    mock.get_observatory = MagicMock(return_value=fake_observatory)
    return mock


@pytest.fixture
def mock_observatory_api_cls(mock_observatory_api: MagicMock) -> MagicMock:
    """
    Mock class for `sdk.ObservatoryApi`.

    This fixture returns a `MagicMock` constructor that produces
    the `mock_observatory_api` instance when called. It allows
    tests to patch the SDK API client at the class level.
    """
    mock_cls = MagicMock(return_value=mock_observatory_api)
    return mock_cls


@pytest.fixture(autouse=True)
def patch_sdk(
    monkeypatch: pytest.MonkeyPatch,
    mock_observatory_api_cls: MagicMock,
) -> None:
    """
    Automatically patch the `sdk.ObservatoryApi` class with a mock.

    This fixture is applied to all tests (`autouse=True`).
    It replaces `sdk.ObservatoryApi` with the `mock_observatory_api_cls`,
    ensuring that all observatory-related API calls are mocked
    throughout the test suite.
    """
    monkeypatch.setattr(sdk, "ObservatoryApi", mock_observatory_api_cls)
