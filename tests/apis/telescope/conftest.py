from datetime import datetime
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

import across.sdk.v1 as sdk


@pytest.fixture
def fake_telescope() -> sdk.Telescope:
    """
    Create a fake `sdk.Telescope` instance for testing.

    This fixture returns a fully populated Telescope object with
    mock values for ID, creation date, name, type, observatory, and
    instruments. It is used as a predictable return value in
    tests that require an Telescope.
    """
    return sdk.Telescope(
        id=str(uuid4()),
        created_on=datetime.fromisoformat("2025-07-15T00:00:00"),
        name="Treedome Telescope",
        short_name="TST",
        observatory=sdk.IDNameSchema(id=str(uuid4()), name="Treedome Space Observatory", short_name="TST"),
        instruments=[
            sdk.TelescopeInstrument(
                id=str(uuid4()),
                name="Treedome Instrument",
                short_name="ti",
                created_on=datetime.fromisoformat("2025-07-15T00:00:00"),
            )
        ],
    )


@pytest.fixture
def mock_telescope_api(fake_telescope: sdk.Telescope) -> MagicMock:
    """
    Mock implementation of the `TelescopeApi`.

    This fixture creates a `MagicMock` with preconfigured
    `get_telescopes` and `get_telescope` methods that
    return the `fake_telescope`. It simulates API calls
    without making real network requests.
    """
    mock = MagicMock()
    mock.get_telescopes = MagicMock(return_value=[fake_telescope])
    mock.get_telescope = MagicMock(return_value=fake_telescope)
    return mock


@pytest.fixture
def mock_telescope_api_cls(mock_telescope_api: MagicMock) -> MagicMock:
    """
    Mock class for `sdk.TelescopeApi`.

    This fixture returns a `MagicMock` constructor that produces
    the `mock_telescope_api` instance when called. It allows
    tests to patch the SDK API client at the class level.
    """
    mock_cls = MagicMock(return_value=mock_telescope_api)
    return mock_cls


@pytest.fixture(autouse=True)
def patch_sdk(
    monkeypatch: pytest.MonkeyPatch,
    mock_telescope_api_cls: MagicMock,
) -> None:
    """
    Automatically patch the `sdk.TelescopeApi` class with a mock.

    This fixture is applied to all tests (`autouse=True`).
    It replaces `sdk.TelescopeApi` with the `mock_telescope_api_cls`,
    ensuring that all telescope-related API calls are mocked
    throughout the test suite.
    """
    monkeypatch.setattr(sdk, "TelescopeApi", mock_telescope_api_cls)
