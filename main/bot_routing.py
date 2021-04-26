from ariadne import load_schema_from_path, make_executable_schema, graphql_sync, snake_case_fallback_resolvers, \
    ObjectType
from ariadne.constants import PLAYGROUND_HTML
from crud.member_crud import resolve_create_member, resolve_members, resolve_member, resolve_update_member, \
    resolve_delete_member
from crud.guild_crud import resolve_create_guild, resolve_guild, resolve_guilds, resolve_update_guild, \
    resolve_delete_guild
from flask import Blueprint, jsonify, request

bot = Blueprint('bot', __name__, url_prefix = '/bot')
type_defs = load_schema_from_path('main/schema.graphql')

query = ObjectType("Query")
query.set_field("members", resolve_members)
query.set_field('member', resolve_member)
query.set_field('guilds', resolve_guilds)
query.set_field('guild', resolve_guild)

mutation = ObjectType("Mutation")
mutation.set_field('createGuild', resolve_create_guild)
mutation.set_field('updateGuild', resolve_update_guild)
mutation.set_field('deleteGuild', resolve_delete_guild)
mutation.set_field('createMember', resolve_create_member)
mutation.set_field('updateMember', resolve_update_member)
mutation.set_field('deleteMember', resolve_delete_member)

schema = make_executable_schema(type_defs, query, mutation, snake_case_fallback_resolvers)


@bot.route('/api', methods=['GET'])
def playground():
    return PLAYGROUND_HTML, 200


@bot.route('/api', methods=['POST', 'PATCH', 'DELETE'])
def server():
    data = request.get_json()

    success, result = graphql_sync(
        schema,
        data,
        context_value = request,
    )

    status_code = 200 if success else 400

    return jsonify(result), status_code


@bot.route('/api/postman', methods=['POST', 'GET', 'PATCH', 'DELETE'])
def postman():
    data = request.get_json()

    success, result = graphql_sync(
        schema,
        data,
        context_value = request,
    )

    status_code = 200 if success else 400

    return jsonify(result), status_code


@bot.route('/members', methods = ['GET'])
def user_index():
    if request.method == 'GET':
        return get_all_members()
    else:
        raise Exception('That method isn\'t allowed here.')


@bot.route('/members/add', methods = ['POST'])
def create_user():
    if request.method == 'POST':
        return add_member(**request.get_json())
    else:
        raise Exception('That method isn\'t allowed here.')


@bot.route('/members/<int:member_id>', methods = ['GET', 'PATCH', 'DELETE'])
def manage_user(member_id):
    if request.method == 'GET':
        return get_member(member_id)
    elif request.method == 'PATCH':
        return update_member(member_id, **request.get_json())
    elif request.method == 'DELETE':
        return remove_member(member_id, **request.get_json())
    else:
        raise Exception('That method isn\'t allowed here.')


@bot.route('/guilds', methods = ['GET'])
def guild_index():
    if request.method == 'GET':
        return get_all_guilds()
    else:
        raise Exception('That method isn\'t allowed here.')


@bot.route('guilds/add', methods = ['POST'])
def create_guild():
    if request.method == 'POST':
        return add_guild(**request.get_json())
    else:
        raise Exception('That method isn\'t allowed here.')


@bot.route('/guilds/<int:guild_id>', methods = ['GET', 'PATCH', 'DELETE'])
def manage_guild(guild_id):
    if request.method == 'GET':
        return get_guild(guild_id)
    elif request.method == 'PATCH':
        return update_guild(guild_id, **request.get_json())
    elif request.method == 'DELETE':
        return remove_guild(guild_id)
    else:
        raise Exception('That method isn\'t allowed here.')
