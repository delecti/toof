import keyring
from typing import Optional

toof = "toof"

def get_account_secret(account_id: str) -> Optional[str]:
    return keyring.get_credential(toof, account_id).password

def set_account_secret(account_id: str, secret: str) -> str:
    return keyring.set_password(toof, account_id, secret)

def delete_account(account_id: str) -> str:
    if keyring.get_credential(toof, account_id) is not None:
        return keyring.delete_password(toof, account_id)