from rtm import ReleaseTagMaker, ObjectFromReleaseTag

rt = ReleaseTagMaker('release.07.30.20v3')
# ro = ObjectFromReleaseTag(rt.exploded)
print(rt.from_dict())
# print(ro)

# print(rt.bump_version())
# print(rt.new_tag())
# print(rt.schedule)