from across.client import Client
from across.client.apis import Observatory
from across.sdk.v1.api_client_wrapper import ApiClientWrapper


class TestClient:
    """
    Unit tests for the `Client` class.

    These tests validate that the `Client` correctly initializes
    its internal API client and provides access to service objects
    such as `Observatory`.
    """

    def test_client_should_return_client(self) -> None:
        """
        Verify that instantiating a `Client` creates a valid
        `ApiClientWrapper` instance and assigns it to
        `client.across_client`.
        """
        client = Client()
        assert isinstance(client.across_client, ApiClientWrapper)

    def test_client_observatory_should_return_observatory(self) -> None:
        """
        Verify that the `observatory` property of a `Client`
        returns an instance of the `Observatory` service client.
        """
        client = Client()
        assert isinstance(client.observatory, Observatory)
