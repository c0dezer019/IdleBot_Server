from main.models import db
from main.models import Member, Guild
from moment import date


def resolve_create_member(obj, info, guild_id, **data):
    try:
        guild = Guild.query.filter_by(guild_id = guild_id).first()
        member = Member(**data)

        guild.members.append(member)
        db.session.add(member)
        db.session.commit()

        payload = {
            'success': True,
            'member': member.as_dict(),
        }

    except AttributeError:
        payload = {
            'success': False,
            'errors': [f'Guild matching id {guild_id} could not be found.']
        }

    except ValueError:
        payload = {
            'success': False,
            'errors': ['It\'s probably that you gave me bad data, or something. check to make sure you\'re passing me the correct data']
        }

    except Exception as error:
        payload = {
            'success': False,
            'errors': [str(error)],
        }

    return payload


def resolve_members(obj, info):
    try:
        members = [member.as_dict() for member in Member.query.all()]

        payload = {
            'success': True,
            'members': members
        }

    except Exception as error:
        payload = {
            'success': False,
            'errors': [str(error)]
        }

    return payload


def resolve_member(obj, info, member_id):
    try:
        member = Member.query.filter_by(member_id = member_id).first()

        payload = {
            'success': True,
            'member': member.as_dict(),
        }

    except AttributeError:
        payload = {
            'success': False,
            'errors': [f'Member matching id {member_id} could not be found.'],
        }

    return payload


def resolve_update_member(obj, info, member_id, **data):
    try:
        member = Member.query.filter_by(member_id = member_id).first()
        print(data)

        for k, v in data.items():
            if k == 'last_activity_ts':
                v = date(v).timezone('US/Central').datetime

            setattr(member, k, v)

        db.session.add(member)
        db.session.commit()

        payload = {
            'success': True,
            'member': member.as_dict(),
        }

    except AttributeError:
        payload = {
            'success': False,
            'errors': [f'Member matching id {member_id} could not be found.']
        }

    except ValueError:
        payload = {
            'success': False,
            'errors': ['It\'s probably that you gave me bad data, or something. Check to make sure you\'re passing me the correct data']
        }

    except Exception as e:
        payload = {
            'success': False,
            'errors': [str(e)]
        }

    return payload


def resolve_delete_member(obj, info, member_id):
    try:
        member = Member.query.filter_by(member_id = member_id).first()

        db.session.delete(member)
        db.session.commit()

        payload = {
            'success': True,
            'success_msg': f'Member matching id {member_id} has successfully been deleted.',
        }

    except AttributeError:
        payload = {
            'success': False,
            'errors': [f'Member matching id {member_id} could not be found.']
        }

    return payload
