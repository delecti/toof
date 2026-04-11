import json
from pathlib import Path
from typing import Optional
from configparser import ConfigParser

aliasesgroup = "aliases"
_config = None
_configpath = None

def lookup_by_alias(alias: str) -> Optional[str]:
    config = load()
    if not config.has_section(aliasesgroup):
        return None
    data = config.items(aliasesgroup)
    for accountid in data:
        if alis in accountid[1].split():
            return accountid[0]
    return None


def add_alias(account: str, alias: str):
    config = load()
    if not config.has_section(aliasesgroup):
        return
    aliasstr = config.get(aliasesgroup, account)
    if aliasstr is not None:
        aliases = aliasstr.split()
        aliases.append(alias)
    else:
        aliases = [alias]
    load().set(aliasesgroup, account, ' '.join(aliases))
    write()

def remove_alias(account: str, alias: str):
    accounts = load().items(aliasesgroup)

def load():
    global _configpath,_config
    if _configpath is None:
        _configpath = Path.home() / ".config/toof/config.ini"
    if _config is None:
        _config = ConfigParser()
        _config.read(_configpath)
    return _config

def write():
    global _configpath
    load().write(_configpath)


# def get_secret(nickname: str) -> str:
#     with open(Path.home() / ".config/toof/prettyauth.json") as f:
#         data = json.load(f)
#     for accountid in data["nicknames"]:
#         if nickname in data["nicknames"][accountid]:
#             account_id = accountid
#             break
#     if account_id is None:
#         raise ValueError(f"Account {account_id} not found")
#     for account in data["accounts"]:
#         if account["accountID"] == account_id:
#             return account["secret"]
#     raise ValueError(f"Account {account_id} not found")

# def lookup_by_alias(alias: str) -> Optional[str]:
#     with open(Path.home() / ".config/toof/prettyauth.json") as f:
#         data = json.load(f)
#     for accountid in data["nicknames"]:
#         # print(f"looking for nickname {alias} in account {accountid}")
#         if alias in data["nicknames"][accountid]:
#             return accountid
#     return None