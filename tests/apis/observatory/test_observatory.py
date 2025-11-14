from unittest.mock import MagicMock
from uuid import uuid4

import across.sdk.v1 as sdk
from across.client.apis import Observatory


class TestGet:
    """
    Unit tests for the `Observatory.get`.

    These tests validate the behavior of the `Observatory` wrapper
    around the Across SDK by mocking out the underlying API calls.
    """

    def test_should_return_observatory(self, fake_observatory: sdk.Observatory) -> None:
        """
        Ensure that `Observatory.get()` returns the expected observatory
        object when the SDK call is mocked.

        Args:
            fake_observatory (sdkObservatory):
                A mocked `sdkObservatory` instance returned by the patched API.
        """
        observatory = Observatory(across_client=MagicMock())
        result = observatory.get(str(uuid4()))
        assert result == fake_observatory

    def test_should_be_called_with_value(self, mock_observatory_api: MagicMock) -> None:
        """
        Verify that `Observatory.get()` calls the underlying
        `ObservatoryApi.get_observatory()` with the correct
        observatory ID.

        Args:
            mock_observatory_api (MagicMock):
                A mocked instance of `ObservatoryApi`.
        """
        id = str(uuid4())
        observatory = Observatory(across_client=MagicMock())
        observatory.get(id)
        mock_observatory_api.get_observatory.assert_called_once_with(observatory_id=id)


class TestGetMany:
    """
    Unit tests for the `Observatory.get_many`.
    """

    def test_should_return_observatories(self, fake_observatory: sdk.Observatory) -> None:
        """
        Ensure that `Observatory.get_many()` returns a list of
        observatories when the SDK call is mocked.
        Args:
            fake_observatory (sdkObservatory):
                A mocked `sdkObservatory` instance returned by the patched API.
        """
        observatory = Observatory(across_client=MagicMock())
        result = observatory.get_many()
        assert result == [fake_observatory]
