import click
from totp import TOTP_SHA1
from loader import get_secret
import base64

@click.command()
@click.argument("input")
def main(input):
    """toof"""
    print(input)
    totp = TOTP_SHA1()
    # totp.K = base64.b32decode("M5YL5GJZECM3AMB5JPMQWQOKKZ6OBH4Z", casefold=True)
    totp.K = base64.b32decode(get_secret("fusion"), casefold=True)
    print(totp.hotp(totp.counter_now()))


if __name__ == "__main__":
    main()
