from datetime import datetime, timedelta

import attr


@attr.s(slots=True)
class ReleaseTagMaker:
    """
    Provide methods to manipulate release tags.
    If schedule is not provided then 30 days is assumed.

    ex: ReleaseTagMaker('release.07.30.20v3[.hf]')
    """

    old_release_tag: str = attr.ib()
    schedule: int = attr.ib(default=30, converter=int)

    @property
    def release_list(self):
        return self.old_release_tag.split('.')

    @property
    def prefix(self):
        return self.release_list[0]

    @property
    def month(self):
        return int(self.release_list[1])

    @property
    def day(self):
        return int(self.release_list[2])

    @property
    def year(self):
        return int(self.release_list[3].split('v')[0])

    @property
    def release_date(self):
        return f"{self.release_list[1]}.{self.release_list[2]}.{self.release_list[3].split('v')[0]}"

    @property
    def version(self):
        return int(self.release_list[3].split('v')[1])

    @property
    def hotfix(self):
        try:
            return self.release_list[4]
        except IndexError:
            return None

    def bump_version(self) -> str:
        """
        Increment the version and return a new release tag.
        Hotfix release tags won't get bumped.

        :return: str
        """

        new_version: int = self.version + 1 if self.hotfix is None else self.version
        new_release_tag: str = f"{self.prefix}.{self.month}.{self.day}.{self.year}v{new_version}"

        return new_release_tag

    def new_release_tag(self) -> str:
        """
        Generate a new release tag based on the schedule.

        :return: str
        """

        if self.hotfix is None:
            previous_release: datetime = datetime.strptime(self.release_date, '%m.%d.%y')
            next_release: datetime = previous_release + timedelta(days=self.schedule)
            release_date = self.__release_date_maker(previous_release, next_release)

            return f"{self.prefix}.{release_date.strftime('%m.%d.%y')}v1"

        return '.'.join(self.release_list)

    @staticmethod
    def __release_date_maker(start_date, end_date):
        """
        Return a release date that excludes Saturday and Sunday
        so that we get a new release date during the week.
        """

        weekend: tuple = (6, 7)
        days: list = []
        while start_date <= end_date:
            if start_date.isoweekday() not in weekend:
                days.append(start_date)
            start_date += timedelta(days=1)

        return days[-1]
