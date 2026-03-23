FROM python:3.11-alpine
ADD dist/tg_mailcow_aliases-0.1.1-py3-none-any.whl .
RUN pip install tg_mailcow_aliases-0.1.1-py3-none-any.whl
CMD ["start"]
