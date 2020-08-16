# ReleaseTagMaker

## Description
Given a release tag and a release schedule ReleaseTagMaker attempts to generate the next release tag so that you don't have to. Hotfix release tags won't get incremented.

## Usage

### Bump Version

```
>>> from rtm import ReleaseTagMaker
>>> rt = ReleaseTagMaker('release.07.30.20v3')
>>> rt.bump_version()
'release.7.30.20v4'
```

### New tag
Incrememt the given release tag by an optionally provided `schedule` parameter. If `schedule` is not defined then 30 days is assumed.

#### New tag without specifying a schedule

```
>>> from rtm import ReleaseTagMaker
>>> rt = ReleaseTagMaker('release.07.30.20v3)
>>> rt.new_tag()
'release.08.29.20v1'
```

#### New tag with a specified schedule

```
>>> from rtm import ReleaseTagMaker
>>> rt = ReleaseTagMaker('release.07.30.20v3, schedule=60)
>>> rt.new_tag()
'release.09.28.20v1'
```


