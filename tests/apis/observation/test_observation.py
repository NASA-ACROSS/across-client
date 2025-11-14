from unittest.mock import MagicMock
from uuid import uuid4

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
