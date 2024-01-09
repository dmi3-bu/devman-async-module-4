import asyncio
import json
import logging

import configargparse

logger = logging.getLogger('sender')
logging.basicConfig(level=logging.DEBUG)


async def server():
    reader, writer = await asyncio.open_connection(args.host, args.port)
    greeting_prompt = await reader.readline()
    logger.debug(greeting_prompt.decode())

    if args.token is None:
        await register(reader, writer)
    else:
        await authorise(reader, writer)

    message = "Hello world!" + '\n\n'
    await submit_message(message, writer)


async def register(reader, writer):
    message = '\n'
    await submit_message(message, writer)

    new_user_prompt = await reader.readline()
    logger.debug(new_user_prompt.decode())

    nickname = input('Введите ник нового пользователя:') + '\n'

    await submit_message(nickname, writer)

    json_response = await reader.readline()
    logger.debug(json_response.decode())
    account_hash = json.loads(json_response.decode())["account_hash"]
    with open('send_config.ini', 'a') as f:
        f.write(f'\ntoken={account_hash}\n')


async def authorise(reader, writer):
    message = args.token + '\n'
    await submit_message(message, writer)

    json_response = await reader.readline()
    logger.debug(json_response.decode())
    if json.loads(json_response.decode()) is None:
        print("Неизвестный токен. Проверьте его или зарегистрируйте заново.")
        return


async def submit_message(text, writer):
    writer.write(text.encode())
    await writer.drain()
    logger.debug(text)


def prepare_args():
    parser = configargparse.ArgParser(default_config_files=['send_config.ini'])
    parser.add_argument('--host', type=str, default='minechat.dvmn.org',
                        help='host')
    parser.add_argument('-p', '--port', type=int, default=5050,
                        help='port')
    parser.add_argument('-t', '--token', type=str,
                        help='token')
    return parser.parse_args()


if __name__ == '__main__':
    args = prepare_args()
    try:
        asyncio.run(server())
    except KeyboardInterrupt:
        quit()
