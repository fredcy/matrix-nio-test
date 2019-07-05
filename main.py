"""
See https://matrix.org/docs/guides/usage-of-matrix-nio
and https://github.com/poljar/matrix-nio
"""

from importlib import util
import asyncio
from nio import (AsyncClient, LoginResponse, SyncResponse, RoomMessageText)

import configparser
import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def main():
    config = configparser.ConfigParser()
    config.read("config")
    logger.debug(f"{config['client']['homeserver'], config['client']['username']}")

    async_client = AsyncClient(config['client']['homeserver'], config['client']['username'])
    try:
        asyncio.run(amain(async_client, config))
    except KeyboardInterrupt:
        logger.info("keyboard interrupt")
    except:
        logger.exception("async.run failed")


async def amain(client, config):
    try:
        response = await client.login(config['client']['password'])
        if isinstance(response, LoginResponse):
            handle_login_response(client, response)
        else:
            logger.error(f"unexpected login response: {type(response)}: {response}")
            return

        try:
            with open ("next_batch","r") as next_batch_token:
                client.next_batch = next_batch_token.read()
        except FileNotFoundError:
            pass

        while (True):
            response = await client.sync(30000)
            if isinstance(response, SyncResponse):
                handle_sync_response(response)
            else:
                logger.error(f"unexpected response type: {type(response)}: {response}")

    except asyncio.CancelledError:
        logger.info(f"asyncio cancellederror")
    except KeyboardInterrupt:
        logger.info(f"keyboard interrupt")
    except Exception as exc:
        logger.exception(f"async failure: {type(exc)}: {exc}")
    finally:
        # It seems that we can only close our async client from within this
        # async function, which is why we catch exceptions here.
        await client.close()


def handle_login_response(client, response):
    logger.info(f"login response: {response}")


def handle_sync_response(response):
    logger.debug(f"sync response: {response}")

    with open("next_batch","w") as next_batch_token:
        next_batch_token.write(response.next_batch)

    if len(response.rooms.join) > 0:
        joins = response.rooms.join
        for room_id in joins:
            for event in joins[room_id].timeline.events:
                logger.debug(f"event: {event}")

if __name__ == "__main__":
    main()
