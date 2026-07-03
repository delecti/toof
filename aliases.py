from pathlib import PosixPath
from typing import Optional
from configparser import ConfigParser
import logging

aliasesgroup = "aliases"
_config = None
_configpath = None
logger = logging.getLogger(__name__)

def lookup_by_alias(alias: str) -> Optional[str]:
    logger.debug(f"lookup_by_alias alias '{alias}'")
    config = load()
    if not config.has_section(aliasesgroup):
        return None
    data = config.items(aliasesgroup)
    for accountid in data:
        if alias in accountid[1].split() or alias == accountid[0]:
            return accountid[0]
    return None

def get_all_aliases(account: str) -> str:
    logger.debug(f"get_all_aliases account '{account}'")
    config = load()
    if not config.has_section(aliasesgroup):
        return None
    if config.has_option(aliasesgroup, account):
        return config.get(aliasesgroup, account)
    else:
        return ""

def add_alias(account: str, alias: str):
    logger.debug(f"add_alias account '{account}' alias '{alias}'")
    account = account.lower() # configparser only stores lowercase keys
    config = load()
    if not config.has_section(aliasesgroup):
        config.add_section(aliasesgroup)
    if config.has_option(aliasesgroup, account):
        aliases = config.get(aliasesgroup, account).split()
    else:
        aliases = []
    if alias not in aliases:
        aliases.append(alias)
        config.set(aliasesgroup, account, ' '.join(aliases))
        write()

def delete_account(account: str):
    logger.debug(f"delete_account account '{account}'")
    account = account.lower()
    config = load()
    if not config.has_section(aliasesgroup):
        print("No alias data found.")
        return
    if not config.has_option(aliasesgroup, account):
        print(f"No alias data found for account '{account}'")
        return
    config.remove_option(aliasesgroup, account)
    write()

def remove_alias(account: str, alias: str):
    logger.debug(f"remove_alias account '{account}' alias '{alias}'")
    account = account.lower() # configparser only stores lowercase keys
    config = load()
    if not config.has_section(aliasesgroup):
        print(f"Account {account} not found.")
        return
    aliases = config.get(aliasesgroup, account).split()
    if alias in aliases:
        aliases.remove(alias)
        config.set(aliasesgroup, account, ' '.join(aliases))
        print(f"Alias {alias} removed from account {account}.")
        write()
    else:
        print(f"Alias {alias} not found for account {account}.")

def load():
    logger.debug("load")
    global _configpath,_config
    if _configpath is None:
        _configpath = PosixPath("~/.config/toof/config.ini").expanduser()
    if _config is None:
        _config = ConfigParser()
        _config.read(_configpath)
    return _config

def write():
    logger.debug("write")
    global _configpath
    logger.debug("Writing config to path: " + str(_configpath))
    load().write(_configpath.open('w+'))
