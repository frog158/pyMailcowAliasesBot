#!/usr/bin/env python3
from tg_mailcow_aliases.sqlite import get_all_users
import logging


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def main():
    rows = get_all_users()
    for row in rows:
        logging.info(row)


if __name__ == "__main__":
    main()
