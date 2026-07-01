from unittest.mock import MagicMock
from uuid import uuid4

import pytest

import across.sdk.v1 as sdk
from across.client.apis import Observation


class TestGet:
    """
    Unit tests for the `Observation.get`.

    These tests validate the behavior of the `Observation` wrapper
    around the Across SDK by mocking out the underlying API calls.
    """

    def test_should_return_observation(self, fake_observation: sdk.Observation) -> None:
        """
        Ensure that `Observation.get()` returns the expected observation
        object when the SDK call is mocked.

        Args:
            fake_observation(sdk.Observation):
                A mocked `sdk.Observation` instance returned by the patched API.
        """
        observation = Observation(across_client=MagicMock())
        result = observation.get(str(uuid4()))
        assert result == fake_observation

    def test_should_be_called_with_value(self, mock_observation_api: MagicMock) -> None:
        """
        Verify that `Observation.get()` calls the underlying
        `ObservationApi.get_observation()` with the correct
        observation ID.

        Args:
            mock_observation_api (MagicMock):
                A mocked instance of `ObservationApi`.
        """
        id = str(uuid4())
        observation = Observation(across_client=MagicMock())
        observation.get(id)
        mock_observation_api.get_observation.assert_called_once_with(observation_id=id)


class TestGetMany:
    """
    Unit tests for the `Observation.get_many`.
    """

    def test_should_return_observations(self, fake_page_observation: sdk.PageObservation) -> None:
        """
        Ensure that `Observation.get_many()` returns a list of
        observations when the SDK call is mocked.
        Args:
            fake_page_observation (sdk.PageObservation):
                A mocked `sdk.PageObservation` instance returned by the patched API.
        """
        observation = Observation(across_client=MagicMock())
        result = observation.get_many()
        assert result == fake_page_observation


class TestContainsPoint:
    """
    Unit tests for the `Observation.contains_point`.
    """

    def test_should_return_observations(self, fake_page_observation: sdk.PageObservation) -> None:
        """
        Ensure that `Observation.contains_point()` returns a list of
        observations when the SDK call is mocked.
        Args:
            fake_page_observation (sdk.PageObservation):
                A mocked `sdk.PageObservation` instance returned by the patched API.
        """
        observation = Observation(across_client=MagicMock())
        result = observation.contains_point(ra=123.45, dec=-65.43)
        assert result == fake_page_observation

    @pytest.mark.parametrize(
        "field, value",
        [
            ("page", 1),
            ("page_limit", 50),
            ("external_id", "test-id"),
            ("schedule_ids", ["schedule-1", "schedule-2"]),
            ("observatory_ids", ["obs-1"]),
            ("telescope_ids", ["tel-1"]),
            ("instrument_ids", ["inst-1"]),
            ("status", sdk.ObservationStatus.SCHEDULED),
            ("proposal", "test-proposal"),
            ("object_name", "test-object"),
            ("date_range_begin", "2023-01-01"),
            ("date_range_end", "2023-12-31"),
            ("bandpass_min", 400.0),
            ("bandpass_max", 700.0),
            ("bandpass_type", sdk.WavelengthUnit.NM),
            ("type", sdk.ObservationType.IMAGING),
            ("depth_value", 20.0),
            ("depth_unit", sdk.DepthUnit.AB_MAG),
            ("include_footprints", True),
        ],
    )
    def test_should_be_called_with_inputs(
        self,
        mock_observation_api: MagicMock,
        field: str,
        value: object,
    ) -> None:
        """
        Verify that `Observation.contains_point()` correctly passes
        input parameters to the underlying API call.

        Args:
            mock_observation_api (MagicMock):
                A mocked instance of `ObservationApi`.
            field (str):
                The field name to test.
            value (object):
                The value to pass for the field.
        """
        observation = Observation(across_client=MagicMock())
        observation.contains_point(ra=123.45, dec=-65.43, **{field: value})  # type: ignore[arg-type]
        assert mock_observation_api.contains_point.call_args.kwargs[field] == value
