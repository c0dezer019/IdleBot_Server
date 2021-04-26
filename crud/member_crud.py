from datetime import datetime
from flask import jsonify
from main.models import db
from main.models import Member, Guild


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

        for k, v in data.items():
            if k == 'last_activity_ts':
                v = datetime.fromisoformat(v)

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
            'errors': ['It\'s probably that you gave me bad data, or something. check to make sure you\'re passing me the correct data']
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


def get_all_members():
    all_members = Member.query.all()
    results = [member.as_dict() for member in all_members]

    return jsonify(results)


def get_member(member_id):
    member = Member.query.filter_by(member_id = member_id).first()

    if member:
        member_dict = member.as_dict()

        if member_dict['last_activity_ts'] is not None:
            member_dict['last_activity_ts'] = member_dict['last_activity_ts'].isoformat()

        return jsonify(member_dict)
    else:
        return f'No member at id: {member_id}', 404


def add_member(**data):
    member = Member.query.filter_by(member_id = data['member_id']).first()
    guild = Guild.query.filter_by(guild_id = data['guild_id']).first()

    if not member:
        try:
            member = Member(member_id = data['member_id'], username = data['username'], nickname = data['nickname'])

            guild.members.append(member)
            db.session.add(member)
            db.session.flush()
            db.session.commit()

        except ValueError:
            return f'Guild with id #{data["guild_id"]} not found.', 404

        except AttributeError:
            return 'An association error has occurred.', 400

        else:
            return jsonify(member.as_dict())
    else:
        guild.members.append(member)
        db.session.add(member)
        db.session.commit()

        return jsonify(guild.as_dict())


def update_member(member_id, **data):
    member = Member.query.filter_by(member_id = member_id).first()

    if member:
        for k, v in data.items():
            if k != 'last_activity_ts':
                setattr(member, k, v)
            else:
                v = datetime.fromisoformat(v)
                member.update(v)

        db.session.commit()

        return jsonify(member.as_dict())
    else:
        raise Exception(f'No member at id {member_id}')


def remove_member(member_id, **data):
    member = Member.query.filter_by(member_id = member_id).first()

    if member:
        for v in data.keys():
            if v != 'hard_delete':
                guild = Guild.query.filter_by(**data).first()

                if guild:
                    guild.members.remove(member)
                    db.session.commit()

                    return f'Member {member.username}(id #{member.member_id}) successfully removed from guild' \
                           f' {guild.name} (id #{guild.guild_id}).', 200
                else:
                    raise Exception('A valid guild id was not provided.')
        else:
            db.session.delete(member)
            db.session.commit()

            return f'Member {member.username}(id #{member.member_id}) successfully purged from database.', 200
    else:
        raise Exception(f'Nothing found with the args: {data}')
