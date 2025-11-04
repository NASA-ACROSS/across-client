from unittest.mock import MagicMock
from uuid import uuid4

import across.sdk.v1 as sdk
from across.client.apis import Filter


class TestGet:
    """
    Unit tests for the `Filter.get`.

    These tests validate the behavior of the `Filter` wrapper
    around the Across SDK by mocking out the underlying API calls.
    """

    def test_should_return_filter(self, fake_filter: sdk.Filter) -> None:
        """
        Ensure that `Filter.get()` returns the expected filter
        object when the SDK call is mocked.

        Args:
            fake_filter(sdk.Filter):
                A mocked `sdk.Filter` instance returned by the patched API.
        """
        filter = Filter(across_client=MagicMock())
        result = filter.get(str(uuid4()))
        assert result == fake_filter

    def test_should_be_called_with_value(self, mock_filter_api: MagicMock) -> None:
        """
        Verify that `Filter.get()` calls the underlying
        `FilterApi.get_filter()` with the correct
        filter ID.

        Args:
            mock_filter_api (MagicMock):
                A mocked instance of `FilterApi`.
        """
        id = str(uuid4())
        filter = Filter(across_client=MagicMock())
        filter.get(id)
        mock_filter_api.get_filter_filter_id_get.assert_called_once_with(filter_id=id)


class TestGetMany:
    """
    Unit tests for the `Filter.get_many`.
    """

    def test_should_return_filters(self, fake_filter: sdk.Filter) -> None:
        """
        Ensure that `Filter.get_many()` returns a list of
        filters when the SDK call is mocked.
        Args:
            fake_filter (sdk.Filter):
                A mocked `sdk.Filter` instance returned by the patched API.
        """
        filter = Filter(across_client=MagicMock())
        result = filter.get_many()
        assert result == [fake_filter]
