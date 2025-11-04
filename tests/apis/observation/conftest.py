from datetime import datetime
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

import across.sdk.v1 as sdk


@pytest.fixture
def fake_observation() -> sdk.Observation:
    """
    Create a fake `sdk.Observation` instance for testing.

    This fixture returns a fully populated Observation object with
    mock values for ID, creation date, name, type, observatory, and
    observations. It is used as a predictable return value in
    tests that require an observation.
    """
    return sdk.Observation(
        id=str(uuid4()),
        created_on=datetime.fromisoformat("2025-07-15T00:00:00"),
        instrument_id=str(uuid4()),
        schedule_id=str(uuid4()),
        object_name="super star",
        pointing_position=sdk.Coordinate(ra=42, dec=42),
        object_position=sdk.Coordinate(ra=42, dec=42),
        date_range=sdk.DateRange(
            begin=datetime.fromisoformat("2025-07-15T00:00:00"),
            end=datetime.fromisoformat("2025-07-15T00:15:00"),
        ),
        exposure_time=15 * 60,
        external_observation_id="super_star_obsid",
        type=sdk.ObservationType.IMAGING,
        status=sdk.ObservationStatus.PLANNED,
        pointing_angle=42.0,
        bandpass=sdk.Bandpass(
            sdk.WavelengthBandpass(
                filter_name="Treedome Filter",
                min=6000,
                max=7000,
                central_wavelength=6500,
                unit=sdk.WavelengthUnit.ANGSTROM,
            )
        ),
    )


@pytest.fixture
def fake_page_observation(fake_observation: sdk.Observation) -> sdk.PageObservation:
    """
    Create a fake `sdk.PageObservation` instance for testing.
    """
    return sdk.PageObservation(total_number=1, page=0, page_limit=1, items=[fake_observation])


@pytest.fixture
def mock_observation_api(
    fake_observation: sdk.Observation, fake_page_observation: sdk.PageObservation
) -> MagicMock:
    """
    Mock implementation of the `ObservationApi`.

    This fixture creates a `MagicMock` with preconfigured
    `get_observations` and `get_obseravtion` methods that
    return the `fake_observation`. It simulates API calls
    without making real network requests.
    """
    mock = MagicMock()
    mock.get_observations = MagicMock(return_value=fake_page_observation)
    mock.get_observation = MagicMock(return_value=fake_observation)
    return mock


@pytest.fixture
def mock_observation_api_cls(mock_observation_api: MagicMock) -> MagicMock:
    """
    Mock class for `sdk.ObservationApi`.

    This fixture returns a `MagicMock` constructor that produces
    the `mock_observation_api` instance when called. It allows
    tests to patch the SDK API client at the class level.
    """
    mock_cls = MagicMock(return_value=mock_observation_api)
    return mock_cls


@pytest.fixture(autouse=True)
def patch_sdk(
    monkeypatch: pytest.MonkeyPatch,
    mock_observation_api_cls: MagicMock,
) -> None:
    """
    Automatically patch the `sdk.ObservationApi` class with a mock.

    This fixture is applied to all tests (`autouse=True`).
    It replaces `sdk.ObservationApi` with the `mock_observation_api_cls`,
    ensuring that all observation-related API calls are mocked
    throughout the test suite.
    """
    monkeypatch.setattr(sdk, "ObservationApi", mock_observation_api_cls)
