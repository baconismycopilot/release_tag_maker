from datetime import datetime, timedelta
from typing import List

import attr
import cattr


@attr.s(slots=True)
class ObjectFromReleaseTag:
    """
    Create an object from exploded release tag.
    """
    prefix: str = attr.ib()
    month: int = attr.ib()
    day: int = attr.ib()
    year: int = attr.ib()
    version: int = attr.ib()
    schedule: int = attr.ib()
    hotfix: str = attr.ib(default=None)

    @classmethod
    def from_dict(cls, data: dict):
        return cattr.structure_attrs_fromdict(data, ObjectFromReleaseTag)


@attr.s(slots=True)
class ReleaseTagMaker:
    """
    Provide methods to manipulate release tags.
    If a schedule isn't provided then 30 days is assumed.

    ex: ReleaseTagMaker('release.07.30.20v3[.hf]')
    """

    def __init__(self, old_release_tag: str, schedule=None):
        self.old_release_tag: str = old_release_tag
        self.new_release_tag = None
        self.schedule: int = schedule
        if schedule is None:
            self.schedule = 30
        else:
            if not isinstance(schedule, int):
                raise TypeError("Parameter schedule must be int.")


    @classmethod
    def from_dict(cls, **release_dict):
        """
        Explode a release tag and send its bits all over the place.
        Expected release tag looks like release.mm.dd.YYv1[.hf]

        :return: list
        """

        release_dict = {}
        release_list = self.old_release_tag.split('.')

        if 'hf' not in release_list:
            release_dict = {
                "prefix": release_list[0],
                "month": release_list[1],
                "day": release_list[2],
                "year": release_list[3].split('v')[0],
                "version": release_list[3].split('v')[1],
                "schedule": self.schedule
            }

        if 'hf' in release_list:
            release_dict = {
                "prefix": release_list[0],
                "month": release_list[1],
                "day": release_list[2],
                "year": release_list[3].split('v')[0],
                "version": release_list[3].split('v')[1],
                "hotfix": release_list[4],
                "schedule": self.schedule
            }
        return ObjectFromReleaseTag.from_dict(**release_dict)

    def bump_version(self) -> ObjectFromReleaseTag:
        """
        Increment the version of a release tag.
        Hotfix release tags won't get bumped.

        :return: str
        """
        if self.exploded.hotfix is None:
            self.exploded.version += 1

        return self.exploded

    def new_tag(self) -> str:
        """
        Use the exploded bits of a release tag and born it again.

        :return: str
        """

        if 'hf' in self.exploded:
            return '.'.join(self.exploded)

        if 'hf' not in self.exploded:
            previous_date: str = f'{self.exploded[1]}.{self.exploded[2]}.{self.exploded[3].split("v")[0]}'
            previous_release: datetime = datetime.strptime(previous_date, '%m.%d.%y')
            next_release: datetime = previous_release + timedelta(days=self.schedule)
            self.new_release_tag: str = f"release.{next_release.strftime('%m.%d.%y')}v1"

        return self.new_release_tag
