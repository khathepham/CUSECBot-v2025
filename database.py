import os

import pymongo
import dotenv
from pymongo.server_api import ServerApi

from Guild import Guild

dotenv.load_dotenv()

uri = f"mongodb+srv://{os.environ.get('DATABASE_USERNAME')}:{os.environ.get('DATABASE_PASSWORD')}@cusecbot.z72vt.mongodb.net/?retryWrites=true&w=majority&appName=CUSECBot"


my_client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
my_client.admin.command('ping')

mydb = my_client["CUSECBot"]

guilds = mydb["guilds"]


def add_update_guild(guild: Guild):
    global guilds
    if get_guild_by_guild(guild).retrieved == 0:
        result = guilds.insert_one(guild.to_json())
    else:
        db_filter = {"guild_id": guild.guild_id}
        result = guilds.replace_one(db_filter, guild.to_json(), True)
    return result


def get_guild_by_guild(guild: Guild):
    global guilds
    result = guilds.find({"guild_id": guild.guild_id})
    return result


def get_guild_by_id(guild_id: int):
    global guilds
    result = guilds.find({"guild_id": guild_id})
    return result
