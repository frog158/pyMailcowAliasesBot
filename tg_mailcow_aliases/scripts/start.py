from tg_mailcow_aliases.bot import start_bot
from tg_mailcow_aliases.sqlite import create_tabel
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def main():
    logging.info("Create database")
    create_tabel()
    logging.info("Start bot")
    start_bot()


if __name__ == "__main__":
    main()
