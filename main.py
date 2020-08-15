from rtm import ReleaseTagMaker

rt = ReleaseTagMaker('release.07.30.20v3', schedule=30)
print(rt.exploded)
print(rt.bump_version())
print(rt.new_tag())
