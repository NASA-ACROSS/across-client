from datetime import datetime
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

import across.sdk.v1 as sdk


@pytest.fixture
def fake_schedule() -> sdk.Schedule:
    """
    Create a fake `sdk.Schedule` instance for testing.

    This fixture returns a fully populated Schedule object with
    mock values for ID, creation date, name, type, observatory, and
    schedules. It is used as a predictable return value in
    tests that require an schedule.
    """
    return sdk.Schedule(
        id=str(uuid4()),
        created_on=datetime.fromisoformat("2025-07-15T00:00:00"),
        telescope_id=str(uuid4()),
        created_by_id=str(uuid4()),
        name="Treedome Telescope Schedule",
        date_range=sdk.DateRange(
            begin=datetime.fromisoformat("2025-07-15T00:00:00"),
            end=datetime.fromisoformat("2025-07-16T00:00:00"),
        ),
        status=sdk.ScheduleStatus.PLANNED,
        external_id="treedome_telescope_schedule_id",
        fidelity=sdk.ScheduleFidelity.LOW,
        observation_count=1,
        observations=[
            sdk.Observation(
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
        ],
    )


@pytest.fixture
def fake_page_schedule(fake_schedule: sdk.Schedule) -> sdk.PageSchedule:
    """
    Create a fake `sdk.PageSchedule` instance for testing.
    """
    return sdk.PageSchedule(items=[fake_schedule], total_number=1, page=0, page_limit=1)


@pytest.fixture
def mock_schedule_api(fake_schedule: sdk.Schedule, fake_page_schedule: sdk.PageSchedule) -> MagicMock:
    """
    Mock implementation of the `ScheduleApi`.

    This fixture creates a `MagicMock` with preconfigured
    `get_many_filter_get` and `get_filter_filter_id_get` methods that
    return the `fake_filter`. It simulates API calls
    without making real network requests.
    """
    mock = MagicMock()
    mock.get_schedules = MagicMock(return_value=fake_page_schedule)
    mock.get_schedules_history = MagicMock(return_value=fake_page_schedule)
    mock.get_schedule = MagicMock(return_value=fake_schedule)
    mock.create_schedule = MagicMock(return_value=str(uuid4()))
    mock.create_many_schedules = MagicMock(return_value=[str(uuid4())])
    return mock


@pytest.fixture
def mock_schedule_api_cls(mock_schedule_api: MagicMock) -> MagicMock:
    """
    Mock class for `sdk.ScheduleApi`.

    This fixture returns a `MagicMock` constructor that produces
    the `mock_schedule_api` instance when called. It allows
    tests to patch the SDK API client at the class level.
    """
    mock_cls = MagicMock(return_value=mock_schedule_api)
    return mock_cls


@pytest.fixture(autouse=True)
def patch_sdk(
    monkeypatch: pytest.MonkeyPatch,
    mock_schedule_api_cls: MagicMock,
) -> None:
    """
    Automatically patch the `sdk.ScheduleApi` class with a mock.

    This fixture is applied to all tests (`autouse=True`).
    It replaces `sdk.ScheduleApi` with the `mock_schedule_api_cls`,
    ensuring that all schedule-related API calls are mocked
    throughout the test suite.
    """
    monkeypatch.setattr(sdk, "ScheduleApi", mock_schedule_api_cls)
