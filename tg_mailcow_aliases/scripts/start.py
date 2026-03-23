import asyncio
import logging
from tg_mailcow_aliases.bot import start_polling
from tg_mailcow_aliases.sqlite import create_tabel

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def main():
    logging.info("Create database")
    create_tabel()
    logging.info("Start bot")
    asyncio.run(start_polling())


if __name__ == "__main__":
    main()
