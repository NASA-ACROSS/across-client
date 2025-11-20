from datetime import datetime
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

import across.sdk.v1 as sdk


@pytest.fixture
def fake_instrument_id() -> str:
    """
    Create a fake instrument ID for testing.
    """
    return str(uuid4())


@pytest.fixture
def fake_observatory_id() -> str:
    """
    Create a fake observatory ID for testing
    """
    return str(uuid4())


@pytest.fixture
def fake_coordinate() -> sdk.Coordinate:
    """
    Create a fake coordinate for testing
    """
    return sdk.Coordinate(ra=123.45, dec=-76.54)


@pytest.fixture
def fake_date_range() -> sdk.DateRange:
    """
    Create a fake date range for testing
    """
    return sdk.DateRange(begin=datetime(2025, 10, 23, 0, 0, 0), end=datetime(2025, 10, 23, 1, 0, 0))


@pytest.fixture
def fake_visibility_window(
    fake_date_range: sdk.DateRange,
    fake_observatory_id: str,
) -> sdk.VisibilityWindow:
    """
    Create a fake `sdk.VisibilityWindow` instance for testing.
    """
    return sdk.VisibilityWindow(
        window=sdk.Window(
            begin=sdk.ConstrainedDate(
                datetime=fake_date_range.begin,
                constraint=sdk.ConstraintType.TEST_CONSTRAINT,
                observatory_id=fake_observatory_id,
            ),
            end=sdk.ConstrainedDate(
                datetime=fake_date_range.end,
                constraint=sdk.ConstraintType.TEST_CONSTRAINT,
                observatory_id=fake_observatory_id,
            ),
        ),
        max_visibility_duration=60,
        constraint_reason=sdk.ConstraintReason(
            start_reason=sdk.ConstraintType.TEST_CONSTRAINT,
            end_reason=sdk.ConstraintType.TEST_CONSTRAINT,
        ),
    )


@pytest.fixture
def fake_visibility_result(
    fake_instrument_id: str,
    fake_visibility_window: sdk.VisibilityWindow,
) -> sdk.VisibilityResult:
    """
    Create a fake `sdk.VisibilityResult` instance for testing.

    This fixture returns a fully populated VisibilityResult object with
    mock values for instrument ID and VisibilityWindows.
    It is used as a predictable return value in
    tests that require a VisibilityResult.
    """
    return sdk.VisibilityResult(
        instrument_id=fake_instrument_id,
        visibility_windows=[fake_visibility_window],
    )


@pytest.fixture
def mock_visibility_calculator_api(fake_visibility_result: sdk.VisibilityResult) -> MagicMock:
    """
    Mock implementation of the `tools.VisibilityCalculator` API.

    This fixture creates a `MagicMock` with preconfigured
    `calculate_windows` method that returns the `fake_visibility_result`.
    It simulates API calls without making real network requests.
    """
    mock = MagicMock()
    mock.calculate_windows_tools_visibility_calculator_windows_instrument_id_get = MagicMock(
        return_value=fake_visibility_result
    )
    return mock


@pytest.fixture
def mock_tools_api_cls(mock_visibility_calculator_api: MagicMock) -> MagicMock:
    """
    Mock class for `sdk.ToolsApi`.

    This fixture returns a `MagicMock` constructor that produces
    the `mock_tools_api` instance when called. It allows
    tests to patch the SDK API client at the class level.
    """
    mock_cls = MagicMock(return_value=mock_visibility_calculator_api)
    return mock_cls


@pytest.fixture(autouse=True)
def patch_sdk(
    monkeypatch: pytest.MonkeyPatch,
    mock_tools_api_cls: MagicMock,
) -> None:
    """
    Automatically patch the `sdk.ToolsApi` class with a mock.

    This fixture is applied to all tests (`autouse=True`).
    It replaces `sdk.ToolsApi` with the `mock_tools_api_cls`,
    ensuring that all tools-related API calls are mocked
    throughout the test suite.
    """
    monkeypatch.setattr(sdk, "ToolsApi", mock_tools_api_cls)
