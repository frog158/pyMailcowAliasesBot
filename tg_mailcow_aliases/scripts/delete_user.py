#!/usr/bin/env python3
from tg_mailcow_aliases.sqlite import delete_user
from sys import argv, exit
import logging

NUMBER_OF_ARGUMENT = 2

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def main():
    if len(argv) != NUMBER_OF_ARGUMENT:
        logging.error("Usage: delete_user <user_id>")
        exit(1)
    user_id = argv[1]
    delete_user(user_id)
    logging.info("User was deleted")


if __name__ == "__main__":
    main()
