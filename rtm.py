from datetime import datetime, timedelta

import attr
import cattr


@attr.s(slots=True)
class ReleaseTag:
    """
    Create an object from release_tag release tag.
    """
    prefix: str = attr.ib()
    month: int = attr.ib(converter=int)
    day: int = attr.ib(converter=int)
    year: int = attr.ib(converter=int)
    release_date: str = attr.ib()
    version: int = attr.ib(converter=int)
    schedule: int = attr.ib(converter=int)
    hotfix: str = attr.ib(default=None)

    @classmethod
    def from_dict(cls, data: dict):
        return cattr.structure_attrs_fromdict(data, cls)


class ReleaseTagMaker:
    """
    Provide methods to manipulate release tags.
    If a schedule isn't provided then 30 days is assumed.

    ex: ReleaseTagMaker('release.07.30.20v3[.hf]')
    """

    def __init__(self, old_release_tag: str, schedule=None):
        self.old_release_tag: str = old_release_tag
        self.new_release_tag = None
        if schedule is None:
            self.schedule = 30
        else:
            self.schedule = schedule

    @property
    def prefix(self):
        return self.release_tag().prefix

    @property
    def month(self):
        return self.release_tag().month

    @property
    def day(self):
        return self.release_tag().day

    @property
    def year(self):
        return self.release_tag().year

    @property
    def release_date(self):
        return self.release_tag().release_date

    @property
    def version(self):
        return self.release_tag().version

    @property
    def hotfix(self):
        return self.release_tag().hotfix

    def release_tag(self) -> ReleaseTag:
        """
        Turn the list into an object.

        :return: ReleaseTag
        """

        release_dict = {}
        release_list = self.old_release_tag.split('.')

        if 'hf' not in release_list:
            release_dict = {
                "prefix": release_list[0],
                "month": release_list[1],
                "day": release_list[2],
                "year": release_list[3].split('v')[0],
                "release_date": f"{release_list[1]}.{release_list[2]}.{release_list[3].split('v')[0]}",
                "version": release_list[3].split('v')[1],
                "schedule": self.schedule
            }

        if 'hf' in release_list:
            release_dict = {
                "prefix": release_list[0],
                "month": release_list[1],
                "day": release_list[2],
                "year": release_list[3].split('v')[0],
                "release_date": f"{release_list[1]}.{release_list[2]}.{release_list[3].split('v')[0]}",
                "version": release_list[3].split('v')[1],
                "hotfix": release_list[4],
                "schedule": self.schedule
            }

        return ReleaseTag(**release_dict)

    def bump_version(self) -> str:
        """
        Increment the version of a release tag.
        Hotfix release tags won't get bumped.

        :return: str
        """

        new_version = self.version + 1 if self.hotfix is None else self.version
        self.new_release_tag: str = f"{self.prefix}.{self.month}.{self.day}.{self.year}v{new_version}"

        return self.new_release_tag

    def new_tag(self) -> str:
        """
        Generate a new release tag reflective of schedule.

        :return: str
        """

        if self.hotfix is None:
            previous_release: datetime = datetime.strptime(self.release_date, '%m.%d.%y')
            next_release: datetime = previous_release + timedelta(days=self.schedule)
            self.new_release_tag: str = f"{self.prefix}.{next_release.strftime('%m.%d.%y')}v1"

        return self.new_release_tag
