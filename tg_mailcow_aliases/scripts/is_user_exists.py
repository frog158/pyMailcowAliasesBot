#!/usr/bin/env python3
from tg_mailcow_aliases.sqlite import is_user_exist
from sys import argv, exit
import logging

NUMBER_OF_ARGUMENT = 2

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def main():
    if len(argv) != NUMBER_OF_ARGUMENT:
        logging.error("Usage: is_user_exists <user_id>")
        exit(1)
    user_id = argv[1]
    result = is_user_exist(user_id)
    if result:
        msg = f"User ID - {user_id} - exists"
    else:
        msg = f"User ID - {user_id} not found"
    logging.info(msg)


if __name__ == "__main__":
    main()
