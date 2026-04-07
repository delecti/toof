import json

def get_secret(nickname: str) -> str:
    with open("prettyauth.json") as f:
        data = json.load(f)
    for accountid in data["nicknames"]:
        if nickname in data["nicknames"][accountid]:
            account_id = accountid
            break
    if account_id is None:
        raise ValueError(f"Account {account_id} not found")
    for account in data["accounts"]:
        if account["accountID"] == account_id:
            return account["secret"]
    raise ValueError(f"Account {account_id} not found")