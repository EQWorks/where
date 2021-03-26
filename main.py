import os

import requests


def filter_member(member):
    return not member.get('is_bot') \
        and not member.get('deleted') \
        and not member.get('name') == 'slackbot' \
        and member.get('profile', {}).get('email').endswith('@eqworks.com')


def get_members(token, cursor=None, team_id=None):
    members = []
    r = requests.get(
        'https://slack.com/api/users.list',
        params={
            'token': token,
            'cursor': cursor,
            'team_id': team_id,
        },
    )

    if not r.ok:
        return members

    r = r.json()
    _members = r.get('members')
    if not _members:
        return members

    members += filter(filter_member, _members)

    # recursively concatenate all "pages" of available Slack members
    if cursor := r.get('response_metadata', {}).get('next_cursor'):
        return members + get_members(cursor=cursor, team_id=team_id)

    return members
