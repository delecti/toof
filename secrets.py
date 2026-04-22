import keyring
from typing import Optional
import click

toof = "toof"

def get_account_secret(account_id: str) -> Optional[str]:
    credential = keyring.get_credential(toof, account_id)
    if credential is not None:
        return credential.password
    else:
        raise click.ClickException(f"No credential stored for account '{account_id}'")

def set_account_secret(account_id: str, secret: str) -> str:
    if keyring.get_credential(toof, account_id) is None:
        return keyring.set_password(toof, account_id, secret)
    else:
        return f"Account '{account_id}' already exists"

def delete_account(account_id: str) -> str:
    if keyring.get_credential(toof, account_id) is not None:
        return keyring.delete_password(toof, account_id)