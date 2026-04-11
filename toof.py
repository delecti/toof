import click
from totp import TOTP_SHA1
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
    print(f"cli! ctx: {repr(ctx)}")
    account_id = aliases.lookup_by_alias(ctx.obj)
    # print(f"result account {account_id} for nickname {ctx.obj}")
    if account_id is not None:
        print(f"found account {account_id} for nickname {repr(ctx)}")
        exit()
    pass
    # if ctx.invoked_subcommand is None:
    #     account_id = loader.lookup(ctx.obj)
    #     if account_id is not None:
    #         # if we recognize the alias, generate a code for it
    #         print(f"AccountId is {account_id}")
    #         ctx.invoke(generate, name=account_id)
    #     else:
    #         # if we don't recognize the alias, assume the user messed up
    #         click.echo(f"Error: alias {ctx.obj} not found", err=True)
    #         raise SystemExit(1)
    # else:
    #     print(f"invoked subcommand is not none?")
    #     # ctx.invoke(generate, name=None)

@cli.command()
@click.argument("name")
@click.argument("secret")
@click.argument("alias")
def add(name, secret, alias=None):
    print(f"Add account {name}")
    secrets.set_account_secret(account_id=name, secret=secret)

@cli.command()
@click.argument("name")
@click.argument("alias")
def alias(name, alias):
    print(f"Add alias {alias} to account {name}")

@cli.command()
@click.argument("name")
@click.argument("alias")
def dealias(name, alias):
    print(f"Remove alias {alias} from account {name}")

@cli.command()
@click.argument("name")
def remove(name):
    print(f"Remove account {name}")

@cli.command()
@click.argument("name", required=False, default=None)
@click.pass_context
def generate(ctx, name):
    if name is None:
        name = ctx.obj
    totp = TOTP_SHA1()
    totp.K = base64.b32decode(secrets.get_account_secret(name), casefold=True)
    code = str(totp.hotp(totp.counter_now())).zfill(6)
    print(f"Outputting code for {name}, {code}")
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