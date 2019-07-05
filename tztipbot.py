import sys

sys.path.append('./vendor/pytezos')
from pytezos.tools.keychain import Keychain


def received_message(message):
    print(f"message: {message}")

    outputs = []
    body = message['body'].strip()

    if body.startswith("!ping"):
        outputs += ping(message)

    elif body.startswith("!keys"):
        outputs += keys(message)

    elif body.startswith("!key"):
        outputs += key(message)

    return outputs


def ping(message):
    content = {
        "body": "pong",
        "msgtype": "m.notice",
    }
    return [content]


def keys(message):
    keychain = Keychain("vendor/secret_keys")
    content = {
        "body": str(keychain.list_keys()),
        "msgtype": "m.notice",
    }
    return [content]


def key(message):
    keychain = Keychain("vendor/secret_keys")
    key = keychain.get_key('foobar')
    pk = key.public_key()
    pkh = key.public_key_hash()

    content = {
        "body": f"pkh = {pkh}",
        "msgtype": "m.notice",
    }
    return [content]

