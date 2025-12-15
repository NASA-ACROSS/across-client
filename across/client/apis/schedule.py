from datetime import datetime

import across.sdk.v1 as sdk
from across.sdk.v1.api_client_wrapper import ApiClientWrapper


class Schedule:
    """
    Client for interacting with Schedule resources in the Across API.

    Provides methods to retrieve single or multiple schedules
    by ID, name, instrument information, or creation date.
    """

    def __init__(self, across_client: ApiClientWrapper):
        """
        Initialize an Schedule client.

        Args:
            across_client (ApiClientWrapper):
                API client wrapper used to make requests to the Across API.
        """
        self.across_client = across_client

    def get(self, id: str) -> sdk.Schedule:
        """
        Retrieve a single Schedule by ID.

        Args:
            id (str):
                The unique identifier of the Schedule to retrieve.

        Returns:
            sdk.Schedule:
                The requested Schedule object.
        """
        return sdk.ScheduleApi(self.across_client).get_schedule(schedule_id=id)

    def get_many(
        self,
        page: int | None = None,
        page_limit: int | None = None,
        date_range_begin: datetime | None = None,
        date_range_end: datetime | None = None,
        status: sdk.ScheduleStatus | None = None,
        external_id: str | None = None,
        fidelity: sdk.ScheduleFidelity | None = None,
        created_on: datetime | None = None,
        observatory_ids: list[str | None] | None = None,
        observatory_names: list[str | None] | None = None,
        telescope_ids: list[str | None] | None = None,
        telescope_names: list[str | None] | None = None,
        name: str | None = None,
        include_observations: bool | None = None,
    ) -> sdk.PageSchedule:
        """
        Retrieve all unique schedules filtered by optional criteria.
            - unique is defined as the most-recently submitted schedule per
            telescope in a specified date-range

        Args:
            page (int | None, optional):
                Page number for paginated results.
            page_limit (int | None, optional):
                Maximum number of results to return per page.
            date_range_begin (datetime | None, optional):
                Filter for schedules starting on or after this date.
            date_range_end (datetime | None, optional):
                Filter for schedules ending on or before this date.
            status (sdk.ScheduleStatus | None, optional):
                Filter by schedule status.
            external_id (str | None, optional):
                Filter by external identifier.
            fidelity (sdk.ScheduleFidelity | None, optional):
                Filter by schedule fidelity level.
            created_on (datetime | None, optional):
                Filter by creation timestamp.
            observatory_ids (list[str | None] | None, optional):
                Filter by one or more observatory IDs.
            observatory_names (list[UUID | None] | None, optional):
                Filter by one or more observatory names.
            telescope_ids (list[str | None] | None, optional):
                Filter by one or more telescope IDs.
            telescope_names (list[str | None] | None, optional):
                Filter by one or more telescope names.
            name (str | None, optional):
                Filter by schedule name.
            include_observations (bool | None, optional):
                Include observations in returned schedules
                (defaults to False)

        Returns:
            sdk.PageSchedule:
                A paginated collection of schedules matching the given filters.
        """
        return sdk.ScheduleApi(self.across_client).get_schedules(
            page=page,
            page_limit=page_limit,
            date_range_begin=date_range_begin,
            date_range_end=date_range_end,
            status=status,
            external_id=external_id,
            fidelity=fidelity,
            created_on=created_on,
            observatory_ids=observatory_ids,
            observatory_names=observatory_names,
            telescope_ids=telescope_ids,
            telescope_names=telescope_names,
            name=name,
            include_observations=include_observations,
        )

    def get_history(
        self,
        page: int | None = None,
        page_limit: int | None = None,
        date_range_begin: datetime | None = None,
        date_range_end: datetime | None = None,
        status: sdk.ScheduleStatus | None = None,
        external_id: str | None = None,
        fidelity: sdk.ScheduleFidelity | None = None,
        created_on: datetime | None = None,
        observatory_ids: list[str | None] | None = None,
        observatory_names: list[str | None] | None = None,
        telescope_ids: list[str | None] | None = None,
        telescope_names: list[str | None] | None = None,
        name: str | None = None,
        include_observations: bool | None = None,
    ) -> sdk.PageSchedule:
        """
        Retrieve all schedules filtered by optional criteria.

        Args:
            page (int | None, optional):
                Page number for paginated results.
            page_limit (int | None, optional):
                Maximum number of results to return per page.
            date_range_begin (datetime | None, optional):
                Filter for schedules starting on or after this date.
            date_range_end (datetime | None, optional):
                Filter for schedules ending on or before this date.
            status (sdk.ScheduleStatus | None, optional):
                Filter by schedule status.
            external_id (str | None, optional):
                Filter by external identifier.
            fidelity (sdk.ScheduleFidelity | None, optional):
                Filter by schedule fidelity level.
            created_on (datetime | None, optional):
                Filter by creation timestamp.
            observatory_ids (list[str | None] | None, optional):
                Filter by one or more observatory IDs.
            observatory_names (list[str | None] | None, optional):
                Filter by one or more observatory names.
            telescope_ids (list[str | None] | None, optional):
                Filter by one or more telescope IDs.
            telescope_names (list[str | None] | None, optional):
                Filter by one or more telescope names.
            name (str | None, optional):
                Filter by schedule name.
            include_observations (bool | None, optional):
                Include observations in returned schedules
                (defaults to False)

        Returns:
            sdk.PageSchedule:
                A paginated collection of schedules matching the given filters.
        """
        return sdk.ScheduleApi(self.across_client).get_schedules_history(
            page=page,
            page_limit=page_limit,
            date_range_begin=date_range_begin,
            date_range_end=date_range_end,
            status=status,
            external_id=external_id,
            fidelity=fidelity,
            created_on=created_on,
            observatory_ids=observatory_ids,
            observatory_names=observatory_names,
            telescope_ids=telescope_ids,
            telescope_names=telescope_names,
            name=name,
            include_observations=include_observations,
        )

    def post(self, schedule: sdk.ScheduleCreate) -> str:
        """
        Creates a schedule in the across api.

        Args:
            schedule (sdk.ScheduleCreate):
                a ScheduleCreate object with the following arguments:
                    telescope_id: StrictStr,
                    name: StrictStr,
                    date_range: DateRange,
                    status: ScheduleStatus,
                    external_id: StrictStr | None,
                    fidelity: ScheduleFidelity | None,
                    observations: List[ObservationCreate]
        Returns:
            schedule_id (str | uuid)
                model id for the newly created schedule
        """
        return sdk.ScheduleApi(self.across_client).create_schedule(schedule_create=schedule)

    def post_many(self, schedules: sdk.ScheduleCreateMany) -> list[str]:
        """
        Creates many schedules in the across api.

        Args:
            schedules (sdk.ScheduleCreateMany):
                a ScheduleCreateMany object with the following arguments:
                    schedules: list[sdk.ScheduleCreate]
        Returns:
            list[str]
                model ids for the newly created schedules
        """
        return sdk.ScheduleApi(self.across_client).create_many_schedules(schedule_create_many=schedules)
