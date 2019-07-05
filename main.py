from importlib import util
import asyncio
from nio import (AsyncClient, SyncResponse, RoomMessageText)

import configparser

def main():
    config = configparser.ConfigParser()
    config.read("config")

    print(f"{config['client']['homeserver'], config['client']['username']}")

    async_client = AsyncClient(config['client']['homeserver'], config['client']['username'])

    async def main():
        response = await async_client.login(config['client']['password'])
        print(f"login response: {response}")

        while (True):
            sync_response = await async_client.sync(30000)
            print(f"sync response: {sync_response}")

            if len(sync_response.rooms.join) > 0:
                joins = sync_response.rooms.join
                for room_id in joins:
                    for event in joins[room_id].timeline.events:
                        print(f"event: {event}")

    asyncio.run(main())


if __name__ == "__main__":
    main()
