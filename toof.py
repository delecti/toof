import click
from totp import quickgen
import aliases
import secrets
import pyperclip
import logging

logger = logging.getLogger(__name__)

class DefaultGroup(click.Group):
    def get_command(self, ctx, cmd_name):
        logger.debug(f"get_command! ctx: {ctx} and cmd_name: {cmd_name}")
        account_id = aliases.lookup_by_alias(cmd_name)
        if account_id is not None:
            # if we recognize the alias, generate a code for it
            logger.debug(f"AccountId is {account_id}")
            ctx.invoke(generate, name=account_id)
            raise SystemExit(1)
        else:
            cmd = super().get_command(ctx, cmd_name)
            if cmd is None:
                ctx.obj = cmd_name
                return super().get_command(ctx, "generate")
            else:
                return cmd

@click.group(invoke_without_command=True, cls=DefaultGroup)
@click.pass_context
@click.option("--debug", is_flag=True, help="Enable debug logging")
def cli(ctx, debug):
    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
    account_id = aliases.lookup_by_alias(ctx.obj)
    logger.debug(f"Found account {account_id} for nickname {ctx.obj}")
    if account_id is not None:
        logger.debug(f"found account {account_id} for nickname {repr(ctx)}")
        exit()
    pass

@cli.command()
@click.argument("name")
@click.argument("secret")
@click.argument("alias", required=False, default=None)
def add(name, secret, alias=None):
    """Adds a new account, optionally with an alias.\n
    Usage: toof add <account> <secret> [alias]\n
    Example: toof add Google ONXGKYLLPEFA==== goog"""
    err = secrets.set_account_secret(account_id=name, secret=secret)
    if err is not None:
        raise click.ClickException(err)
    if alias is not None:
        aliases.add_alias(name, alias)
    print(f"Added account {name}.")

@cli.command()
@click.argument("name")
@click.argument("alias")
def alias(name, alias):
    """Adds an alias for a given account.\n
    Usage: toof alias <account> <alias>\n
    Example: toof alias Google goog"""
    aliases.add_alias(name, alias)
    print(f"Alias {alias} added to account {name}.")

@cli.command()
@click.argument("name")
@click.argument("alias")
def dealias(name, alias):
    """Remove an alias for a given account.\n
    Usage: toof dealias <account> <alias>\n
    Example: toof dealias Google goog"""
    account = aliases.lookup_by_alias(alias)
    if not name == account:
        print(f"Alias {alias} is not an alias for account {name}")
        return
    elif not click.confirm(f"Remove alias {alias} from account {name}?"):
        return
    aliases.remove_alias(name, alias)
    print(f"Alias {alias} removed from account {name}.")

@cli.command()
@click.argument("name")
def remove(name):
    """Remove an account's entry along with all aliases.\n
    Note this is not yet implemented.\n
    Usage: toof remove <account>
    Example: toof remove Google"""
    account = aliases.lookup_by_alias(name)
    if account is not None:
        aliaslist = ', '.join(aliases.get_all_aliases(account).split())
        if secrets.does_account_exist(account):
            # ask to delete both
            if not click.confirm(f"Account {name} has aliases: {aliaslist}. Remove account and all its aliases?"):
                return
            secrets.delete_account(name)
            aliases.delete_account(name)
            print(f"Removed account {name} and its aliases.")
        else: 
            # no secret, but ask to delete aliases
            if not click.confirm(f"No secret found. Clean up aliases '{aliaslist}' for account {name}?"):
                return
            aliases.delete_account(name)
            print(f"Cleaned up lingering aliases for account {name}.")
    else:
        # print error that it doesn't exist
        print(f"Nothing found to delete for account {name}.")

@cli.command()
@click.argument("name", required=False, default=None)
@click.pass_context
def generate(ctx, name):
    """Generate a code for an account or alias. This is also the default
    behavior if no command is specified. It will display the code and place
    it in the system clipboard for pasting.\n
    Usage: toof [generate] <alias/account>\n
    Example: toof goog
    """
    if name is None:
        name = ctx.obj
        if name is None:
            click.echo(ctx.get_help())
            return
    secret = secrets.get_account_secret(name)
    if (secret is not None):
        code = quickgen(secret)
        print(f"Outputting code for {name}: {code}")
        pyperclip.copy(code)
    else:
        click.echo(ctx.get_help())

@cli.command()
@click.argument("secret", required=True)
def rawgen(secret):
    code = quickgen(secret)
    print(f"Generated code: {code}")
    pyperclip.copy(code)

if __name__ == "__main__":
    cli()
