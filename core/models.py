from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from typing import Callable
from arrow import get, now


class PSQLAlchemy(SQLAlchemy):
    Column: Callable
    Integer: Callable
    String: Callable
    DateTime: Callable
    Table: Callable
    ForeignKey: Callable
    relationship: Callable
    backref: Callable


db = PSQLAlchemy()

member_guild_association = db.Table(
    'associationTable',
    db.Model.metadata,
    db.Column('member_id', db.Integer, db.ForeignKey('members.id'), primary_key = True),
    db.Column('guild_id', db.Integer, db.ForeignKey('guilds.id'), primary_key = True)
)


class Member(db.Model):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key = True, nullable = False)
    member_id = db.Column(db.BigInteger, nullable = False, unique = True)
    username = db.Column(db.String, nullable = False, unique = True)
    nickname = db.Column(db.String, nullable = True, unique = False)
    admin_access = db.Column(db.Boolean, default = False)
    last_activity = db.Column(db.String, server_default = 'None')
    last_activity_loc = db.Column(db.String, server_default = 'None')
    last_activity_ts = db.Column(db.DateTime(timezone = True), default = get(datetime(1970, 1, 1, 0, 0)).datetime)
    # Overall Discord status. Not representative of individual servers.
    status = db.Column(db.String, nullable = False, server_default = 'new')
    date_added = db.Column(db.DateTime(timezone = True), default = now('US/Central').datetime)

    def __repr__(self):
        return f'<Member (id = {self.id}, member_id = {self.member_id}, username = {self.username}, ' \
               f' last_activity = {self.last_activity}, last_activity_loc = {self.last_activity_loc}, ' \
               f' last_activity_ts = {self.last_activity_ts.isoformat()}), status = {self.status}, ' \
               f'date_added = {self.date_added.isoformat()}>'

    def as_dict(self):
        member_dict = { c.name: getattr(self, c.name) for c in self.__table__.columns }
        member_dict['last_activity_ts'] = member_dict['last_activity_ts'].isoformat()
        member_dict['date_added'] = member_dict['date_added'].isoformat()

        return member_dict

    def update(self, new_timestamp):
        self.last_activity_ts = new_timestamp


class Guild(db.Model):
    __tablename__ = 'guilds'

    id = db.Column(db.Integer, primary_key = True)
    guild_id = db.Column(db.BigInteger, nullable = False, unique = True)
    name = db.Column(db.String, nullable = False)
    last_activity = db.Column(db.String, server_default = 'None')
    last_activity_loc = db.Column(db.String, server_default = 'None')
    last_activity_ts = db.Column(db.DateTime(timezone = True), default = get(datetime(1970, 1, 1, 0, 0)).datetime)
    status = db.Column(db.String, nullable = False, server_default = 'new')
    settings = db.Column(db.JSON, default = { })
    members = db.relationship(Member, secondary = member_guild_association, lazy = 'joined',
                              backref = db.backref('guilds', lazy = True))
    date_added = db.Column(db.DateTime(timezone = True), default = now('US/Central').datetime)

    def __repr__(self):
        return f'<Guild (id = {self.id}, guild_id = {self.guild_id},  name = {self.name}, ' \
               f'last_activity = {self.last_activity}, last_activity_loc = {self.last_activity_loc}, ' \
               f'last_activity_ts = {self.last_activity_ts}, status = {self.status}, settings = {self.settings}, ' \
               f'members = {self.members}, date_added = {self.date_added.isoformat()})>'

    def as_dict(self):
        guild_dict = { c.name: getattr(self, c.name) for c in self.__table__.columns }
        guild_dict['last_activity_ts'] = guild_dict['last_activity_ts'].isoformat()
        guild_dict['date_added'] = guild_dict['date_added'].isoformat()
        guild_dict['members'] = []

        for member in self.members:
            member_dict = member.as_dict()
            guild_dict['members'].append(member_dict)

        return guild_dict
