from importlib import util
import asyncio
from nio import (AsyncClient, SyncResponse, RoomMessageText)

import configparser

def main():
    config = configparser.ConfigParser()
    config.read("config")

    print(f"client = {config.items('client')}")

    async_client = AsyncClient(config['client']['homeserver'], config['client']['username'])

    async def main():
        response = await async_client.login(config['client']['password'])
        print(response)

        while (True):
            sync_response = await async_client.sync(30000)
            print(sync_response)

    asyncio.run(main())


if __name__ == "__main__":
    main()
