import click
from totp import quickgen
import aliases
import secrets
import base64
import pyperclip

class DefaultGroup(click.Group):
    def get_command(self, ctx, cmd_name):
        print(f"get_command! ctx: {ctx} and cmd_name: {cmd_name}")
        account_id = aliases.lookup_by_alias(cmd_name)
        if account_id is not None:
            # if we recognize the alias, generate a code for it
            print(f"AccountId is {account_id}")
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
def cli(ctx):
    # print(f"cli! ctx: {repr(ctx)}")
    account_id = aliases.lookup_by_alias(ctx.obj)
    # print(f"result account {account_id} for nickname {ctx.obj}")
    if account_id is not None:
        print(f"found account {account_id} for nickname {repr(ctx)}")
        exit()
    pass

@cli.command()
@click.argument("name")
@click.argument("secret")
@click.argument("alias")
def add(name, secret, alias=None):
    """Adds a new account, optionally with an alias.\n
    Usage: toof add <account> <secret> [alias]\n
    Example: toof add Google ONXGKYLLPEFA==== goog"""
    err = secrets.set_account_secret(account_id=name, secret=secret)
    if err is not None:
        raise click.ClickException(err)
    if alias is not None:
        aliases.add_alias(name, alias)

@cli.command()
@click.argument("name")
@click.argument("alias")
def alias(name, alias):
    """Adds an alias for a given account.\n
    Usage: toof alias <account> <alias>\n
    Example: toof alias Google goog"""
    aliases.add_alias(name, alias)

@cli.command()
@click.argument("name")
@click.argument("alias")
def dealias(name, alias):
    """Remove an alias for a given account.\n
    Usage: toof dealias <account> <alias>\n
    Example: toof dealias Google goog"""
    aliases.remove_alias(name, alias)

@cli.command()
@click.argument("name")
def remove(name):
    """Remove an account's entry along with all aliases.\n
    Usage: toof remove <account>
    Example: toof remove Google"""
    # TODO: Implement
    print(f"Remove account {name}")

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
    secret = secrets.get_account_secret(name)
    code = quickgen(secret)
    print(f"Outputting code for {name}, {code}")
    pyperclip.copy(code)

@cli.command()
@click.argument("secret", required=True)
def rawgen(secret):
    code = quickgen(secret)
    print(f"Raw generated code: {code}")
    pyperclip.copy(code)

if __name__ == "__main__":
    cli()

"""
{"add", "adds the specified OTP entry", "<name>", "<},
{"alias", "adds an alias to the specified OTP entry", "<name> <alias>"},
{"dealias", "deletes an alias from the specified OTP entry", "<name> <alias>"},
{"help", "prints this output, or instructions for a command", "<command>"},
{"remove", "remove the specified OTP entry", "<name>"},
"""