from datetime import datetime
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

import across.sdk.v1 as sdk


@pytest.fixture
def fake_filter() -> sdk.Filter:
    """
    Create a fake `sdk.Filter` instance for testing.

    This fixture returns a fully populated Filter object with
    mock values for ID, creation date, name, type, observatory, and
    filters. It is used as a predictable return value in
    tests that require an Filter.
    """
    return sdk.Filter(
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


@pytest.fixture
def mock_filter_api(fake_filter: sdk.Filter) -> MagicMock:
    """
    Mock implementation of the `FilterApi`.

    This fixture creates a `MagicMock` with preconfigured
    `get_many_filter_get` and `get_filter_filter_id_get` methods that
    return the `fake_filter`. It simulates API calls
    without making real network requests.
    """
    mock = MagicMock()
    mock.get_many_filter_get = MagicMock(return_value=[fake_filter])
    mock.get_filter_filter_id_get = MagicMock(return_value=fake_filter)
    return mock


@pytest.fixture
def mock_filter_api_cls(mock_filter_api: MagicMock) -> MagicMock:
    """
    Mock class for `sdk.FilterApi`.

    This fixture returns a `MagicMock` constructor that produces
    the `mock_filter_api` instance when called. It allows
    tests to patch the SDK API client at the class level.
    """
    mock_cls = MagicMock(return_value=mock_filter_api)
    return mock_cls


@pytest.fixture(autouse=True)
def patch_sdk(
    monkeypatch: pytest.MonkeyPatch,
    mock_filter_api_cls: MagicMock,
) -> None:
    """
    Automatically patch the `sdk.FilterApi` class with a mock.

    This fixture is applied to all tests (`autouse=True`).
    It replaces `sdk.FilterApi` with the `mock_filter_api_cls`,
    ensuring that all filter-related API calls are mocked
    throughout the test suite.
    """
    monkeypatch.setattr(sdk, "FilterApi", mock_filter_api_cls)
