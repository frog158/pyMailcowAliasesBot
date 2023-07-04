#!/usr/bin/env python3
from tg_mailcow_aliases.sqlite import add_user
from sys import argv, exit
import logging

NUMBER_OF_ARGUMENT = 5

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def main():
    if len(argv) != NUMBER_OF_ARGUMENT:
        logging.error("Usage: add_user <user_id> <user name> <domain> <email>")
        exit(1)
    user_id = argv[1]
    user_name = argv[2]
    domain = argv[3]
    goto = argv[4]
    add_user(user_id, user_name, domain, goto)


if __name__ == "__main__":
    main()
