from datetime import datetime
from unittest.mock import MagicMock
from uuid import UUID, uuid4

import across.sdk.v1 as sdk
from across.client.apis import Schedule


class TestGet:
    """
    Unit tests for the `Schedule.get`.

    These tests validate the behavior of the `Schedule` wrapper
    around the Across SDK by mocking out the underlying API calls.
    """

    def test_should_return_schedule(self, fake_schedule: sdk.Schedule) -> None:
        """
        Ensure that `Schedule.get()` returns the expected schedule
        object when the SDK call is mocked.

        Args:
            fake_schedule(sdk.Schedule):
                A mocked `sdk.Schedule` instance returned by the patched API.
        """
        schedule = Schedule(across_client=MagicMock())
        result = schedule.get(str(uuid4()))
        assert result == fake_schedule

    def test_should_be_called_with_value(self, mock_schedule_api: MagicMock) -> None:
        """
        Verify that `Schedule.get()` calls the underlying
        `ScheduleApi.get_schedule()` with the correct
        schedule ID.

        Args:
            mock_schedule_api (MagicMock):
                A mocked instance of `ScheduleApi`.
        """
        id = str(uuid4())
        schedule = Schedule(across_client=MagicMock())
        schedule.get(id)
        mock_schedule_api.get_schedule.assert_called_once_with(schedule_id=id)


class TestGetMany:
    """
    Unit tests for the `Schedule.get_many`.
    """

    def test_should_return_schedules(self, fake_page_schedule: sdk.PageSchedule) -> None:
        """
        Ensure that `Schedule.get_many()` returns a list of
        schedules when the SDK call is mocked.
        Args:
            fake_page_schedule (sdk.PageSchedule):
                A mocked `sdk.PageSchedule` instance returned by the patched API.
        """
        schedule = Schedule(across_client=MagicMock())
        result = schedule.get_many()
        assert result == fake_page_schedule

    def test_should_optionally_return_observations(self, mock_schedule_api: MagicMock) -> None:
        """
        Ensure that `Schedule.get_many()` returns a list of
        observations when `include_observations` is set to `True`.
        Args:
            mock_schedule_api (MagicMock):
                A mocked instance of `ScheduleApi`.
        """
        schedule = Schedule(across_client=MagicMock())
        schedule.get_many(include_observations=True)
        call = mock_schedule_api.get_schedules.call_args_list[0]
        assert call.kwargs["include_observations"] is True


class TestGetHistory:
    """
    Unit tests for the `Schedule.get_history`.
    """

    def test_should_return_schedules(self, fake_page_schedule: sdk.PageSchedule) -> None:
        """
        Ensure that `Schedule.get_history()` returns a list of
        schedules when the SDK call is mocked.
        Args:
            fake_page_schedule (sdk.PageSchedule):
                A mocked `sdk.PageSchedule` instance returned by the patched API.
        """
        schedule = Schedule(across_client=MagicMock())
        result = schedule.get_history()
        assert result == fake_page_schedule

    def test_should_optionally_return_observations(self, mock_schedule_api: MagicMock) -> None:
        """
        Ensure that `Schedule.get_history()` returns a list of
        observations when `include_observations` is set to `True`.
        Args:
            mock_schedule_api (MagicMock):
                A mocked instance of `ScheduleApi`.
        """
        schedule = Schedule(across_client=MagicMock())
        schedule.get_history(include_observations=True)
        call = mock_schedule_api.get_schedules_history.call_args_list[0]
        assert call.kwargs["include_observations"] is True


class TestPost:
    """
    Unit tests for the `Schedule.post`
    """

    def test_should_return_uuid(self) -> None:
        """
        Posted schedule should return uuid (as str)
        """
        schedule_create = sdk.ScheduleCreate(
            telescope_id=str(uuid4()),
            name="test schedule",
            date_range=sdk.DateRange(
                begin=datetime.fromisoformat("2025-07-15T00:00:00"),
                end=datetime.fromisoformat("2025-07-15T00:15:00"),
            ),
            status=sdk.ScheduleStatus.PLANNED,
            external_id="test_external",
            fidelity=sdk.ScheduleFidelity.LOW,
            observations=[],
        )
        schedule = Schedule(across_client=MagicMock())
        result = schedule.post(schedule_create)
        assert UUID(result)


class TestPostMany:
    """
    Unit tests for the `Schedule.post_many`
    """

    def test_should_return_list_uuid(self) -> None:
        """
        Posted Schedules should return a list of uuids
        """
        schedule_create = sdk.ScheduleCreate(
            telescope_id=str(uuid4()),
            name="test schedule",
            date_range=sdk.DateRange(
                begin=datetime.fromisoformat("2025-07-15T00:00:00"),
                end=datetime.fromisoformat("2025-07-15T00:15:00"),
            ),
            status=sdk.ScheduleStatus.PLANNED,
            external_id="test_external",
            fidelity=sdk.ScheduleFidelity.LOW,
            observations=[],
        )
        schedule = Schedule(across_client=MagicMock())
        result = schedule.post_many(
            sdk.ScheduleCreateMany(schedules=[schedule_create], telescope_id=str(uuid4()))
        )
        assert isinstance(result, list)
