from pathlib import PosixPath
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
        if alias in accountid[1].split() or alias == accountid[0]:
            return accountid[0]
    return None

def add_alias(account: str, alias: str):
    config = load()
    if not config.has_section(aliasesgroup):
        config.add_section(aliasesgroup)
        aliases = []
    else:
        aliases = config.get(aliasesgroup, account).split()
    if alias not in aliases:
        aliases.append(alias)
        config.set(aliasesgroup, account, ' '.join(aliases))
        write()

def remove_alias(account: str, alias: str):
    config = load()
    print('remove_alias')
    if not config.has_section(aliasesgroup):
        print('entry already didn\'t exist')
        return
    aliases = config.get(aliasesgroup, account).split()
    if alias in aliases:
        aliases.remove(alias)
        config.set(aliasesgroup, account, ' '.join(aliases))
        write()
    else:
        print('alias already didn\'t exist')

def load():
    global _configpath,_config
    if _configpath is None:
        _configpath = PosixPath("~/.config/toof/config.ini").expanduser()
    if _config is None:
        _config = ConfigParser()
        _config.read(_configpath)
    return _config

def write():
    global _configpath
    print("doing a write? " + str(_configpath))
    # if not _configpath.exists():

    load().write(_configpath.open('w+'))


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