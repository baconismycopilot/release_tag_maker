from datetime import datetime, timedelta


class ReleaseTagMaker:
    """
    Provide methods to manipulate release tags.
    If a schedule isn't provided then 30 days is assumed.

    ex: ReleaseTagMaker('release.07.30.20v3[.hf]')
    """

    def __init__(self, old_release_tag, schedule=None):
        self.old_release_tag = old_release_tag
        self.new_release_tag = None
        self.schedule = schedule
        if schedule is None:
            self.schedule = 30
        else:
            if not isinstance(schedule, int):
                raise TypeError("Parameter schedule must be int.")

    @property
    def exploded(self):
        """
        Explode a release tag and send its bits all over the place.
        Expected release tag looks like release.mm.dd.YYv1[.hf]

        :return: list
        """

        return self.old_release_tag.split('.')

    def bump_version(self):
        """
        Increment the version of a release tag.
        Hotfix release tags won't get bumped.

        :return: str
        """

        if 'hf' not in self.exploded:
            tag = '.'.join(self.exploded[0:4]).split('v')[:1]
            version = int(self.exploded[3].split('v')[1])
            version += 1

            return f"{'.'.join(tag)}v{version}"

        return f"{'.'.join(self.exploded)}"

    def new_tag(self):
        """
        Use the exploded bits of a release tag and make it born again.

        :return: str
        """

        if 'hf' in self.exploded:
            return '.'.join(self.exploded)

        if 'hf' not in self.exploded:
            previous_date: str = f'{self.exploded[1]}.{self.exploded[2]}.{self.exploded[3].split("v")[0]}'
            previous_release: datetime = datetime.strptime(previous_date, '%m.%d.%y')
            next_release: datetime = previous_release + timedelta(days=self.schedule)
            self.new_release_tag = f"release.{next_release.strftime('%m.%d.%y')}v1"

        return self.new_release_tag
