import keyring
from typing import Optional
import click
import logging

toof = "toof"
logger = logging.getLogger(__name__)

def does_account_exist(account_id: str) -> bool:
    logger.debug(f"does_account_exist account_id '{account_id}'")
    if account_id is None:
        return false
    account_id = account_id.lower() # configparser only stores lowercase
    credential = keyring.get_credential(toof, account_id)
    return credential is not None

def get_account_secret(account_id: str) -> Optional[str]:
    logger.debug(f"get_account_secret account_id '{account_id}'")
    if account_id is None:
        return None
    account_id = account_id.lower() # configparser only stores lowercase
    credential = keyring.get_credential(toof, account_id)
    if credential is not None:
        return credential.password
    else:
        return None

def set_account_secret(account_id: str, secret: str) -> str:
    logger.debug(f"set_account_secret account_id '{account_id}' secret '{secret}'")
    account_id = account_id.lower() # configparser only stores lowercase
    if keyring.get_credential(toof, account_id) is None:
        return keyring.set_password(toof, account_id, secret)
    else:
        return f"Account '{account_id}' already exists"

def delete_account(account_id: str) -> str:
    logger.debug(f"delete_account account_id '{account_id}'")
    account_id = account_id.lower() # configparser only stores lowercase
    if keyring.get_credential(toof, account_id) is not None:
        return keyring.delete_password(toof, account_id)