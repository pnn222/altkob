import asyncio
import logging

import project.database.creator
import project.api.server

def main():
    loop = asyncio.get_event_loop()
    loop.run_forever()


if __name__ == '__main__':
    main()