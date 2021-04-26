from arrow import get
from main.models import db
from main.models import Guild


def resolve_create_guild(obj, info, **kwargs):
    try:
        guild = Guild(**kwargs)

        db.session.add(guild)
        db.session.commit()

        payload = {
            'success': True,
            'guild': guild.as_dict()
        }

    except ValueError:
        payload = {
            'success': False,
            'errors': [f'Incorrect']
        }

    return payload


def resolve_guilds(obj, info):
    try:
        guilds = [guild.as_dict() for guild in Guild.query.all()]

        payload = {
            'success': True,
            'guilds': guilds
        }

    except Exception as error:
        payload = {
            'success': False,
            'errors': str(error)
        }

    return payload


def resolve_guild(obj, info, guild_id):
    try:
        guild = Guild.query.filter_by(guild_id = guild_id).first()

        payload = {
            'success': True,
            'guild': guild.as_dict(),
        }

    except AttributeError:
        payload = {
            'success': False,
            'errors': [f'Guild matching id {guild_id} cannot be found.']
        }

    return payload


def resolve_update_guild(obj, info, guild_id, **data):
    try:
        guild = Guild.query.filter_by(guild_id = guild_id).first()

        for k, v in data.items():
            if k == 'last_activity_ts':
                v = get(v).to('US/Central').datetime

            setattr(guild, k, v)

        db.session.add(guild)
        db.session.commit()

        payload = {
            'success': True,
            'success_msg': f'Guild matching id {guild_id} has been modified.',
            'guild': guild.as_dict()
        }

    except AttributeError:
        payload = {
            'success': False,
            'errors': [f'Guild matching id {guild_id} was unable to be found.'],
        }

    except ValueError:
        payload = {
            'success': False,
            'errors': [f'You stuck up, half-witted, scruffy-looking nerf herder! You provided me with incorrect data!']
        }

    except TypeError:
        payload = {
            'success': False,
            'errors': ['Bot tried to do something obscene with an object.']
        }

    return payload


def resolve_delete_guild(obj, info, guild_id):
    try:
        guild = Guild.query.filter_by(guild_id = guild_id).first()

        db.session.delete(guild)
        db.session.commit()

        payload = {
            'success': True,
            'success_msg': f'Guild matching id {guild_id} has successfully been deleted.',
        }

    except AttributeError:
        payload = {
            'success': False,
            'errors': [f'Guild matching id {guild_id} could not be found.']
        }

    return payload
