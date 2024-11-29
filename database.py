import os

import pymongo
import dotenv
from infisical_sdk import InfisicalSDKClient
from pymongo.server_api import ServerApi

from Guild import Guild

dotenv.load_dotenv()

print("[INFO] Connecting to Infisical")
i_client = InfisicalSDKClient(host="https://app.infisical.com")
i_client.auth.universal_auth.login(client_id=os.environ.get("I_CLIENT_ID"),
                                   client_secret=os.environ.get("I_CLIENT_SECRET"))
i_response = i_client.secrets.get_secret_by_name(secret_name="MONGODB_CLOUD_USERNAME",
                                                 project_id="fcdb0041-ad1d-4fa6-854d-0745640829d0",
                                                 environment_slug="prod", secret_path="/")
print("[INFO] Received MONGODB_CLOUD_USERNAME")
database_username = i_response.secret.secret_value

i_response2 = i_client.secrets.get_secret_by_name(secret_name="MONGODB_CLOUD_PASSWORD",
                                                  project_id="fcdb0041-ad1d-4fa6-854d-0745640829d0",
                                                  environment_slug="prod", secret_path="/")
database_password = i_response2.secret.secret_value
print("[INFO] Received MONGODB_CLOUD_USERNAME")

uri = f"mongodb+srv://{database_username}:{database_password}@cusecbot.z72vt.mongodb.net/?retryWrites=true&w=majority&appName=CUSECBot"

my_client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
my_client.admin.command('ping')

mydb = my_client["CUSECBot"]

guilds = mydb["guilds"]


def add_update_guild(guild: Guild):
    global guilds
    if get_guild_by_guild(guild) is None:
        result = guilds.insert_one(guild.to_json())
    else:
        db_filter = {"_id": guild.guild_id}

        guild_json = guild.to_json()

        keys = list(guild_json.keys())
        for k in keys:
            if guild_json[k] is None:
                guild_json.pop(k)

        result = guilds.replace_one(db_filter, guild_json, True)
    return result


def get_guild_by_guild(guild: Guild):
    global guilds
    result = guilds.find_one({"_id": guild.guild_id})
    return result


def get_guild_by_id(guild_id: int):
    global guilds
    result = guilds.find_one({"_id": guild_id})
    return result
