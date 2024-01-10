import asyncio
import json
import logging

import configargparse

logger = logging.getLogger('sender')
logging.basicConfig(level=logging.DEBUG)


async def send_to_chat():
    reader, writer = await asyncio.open_connection(args.host, args.port)
    try:
        greeting_prompt = await reader.readline()
        logger.debug(greeting_prompt.decode())

        if args.token is None:
            await register(reader, writer)
        else:
            success = await authorise(reader, writer)
            if not success:
                return

        message = sanitize_input(args.message) + '\n'
        await submit_message(message, writer)
    except Exception as e:
        logger.debug(f'{type(e)}: {e}')
    finally:
        writer.close()


async def register(reader, writer):
    await submit_message('', writer)

    new_user_prompt = await reader.readline()
    logger.debug(new_user_prompt.decode())

    nickname = sanitize_input(args.nickname)
    await submit_message(nickname, writer)

    json_response = await reader.readline()
    logger.debug(json_response.decode())
    account_hash = json.loads(json_response.decode())["account_hash"]
    with open('send_config.ini', 'a') as f:
        f.write(f'\ntoken={account_hash}\n')


async def authorise(reader, writer):
    await submit_message(args.token, writer)

    json_response = await reader.readline()
    logger.debug(json_response.decode())
    if json.loads(json_response.decode()) is None:
        print("Неизвестный токен. Проверьте его или зарегистрируйте заново.")
        return False

    return True


async def submit_message(text, writer):
    writer.write(f'{text}\n'.encode())
    await writer.drain()
    logger.debug(text)


def sanitize_input(text):
    return text.replace('\n', '')


def prepare_args():
    parser = configargparse.ArgParser(default_config_files=['send_config.ini'])
    parser.add_argument('-m', '--message', type=str, required=True,
                        help='message text to send')
    parser.add_argument('-t', '--token', type=str,
                        help='token of existing user')
    parser.add_argument('--host', type=str, default='minechat.dvmn.org',
                        help='host')
    parser.add_argument('-p', '--port', type=int, default=5050,
                        help='port')
    parser.add_argument('-n', '--nickname', type=str, default="newbie",
                        help='nickname for a new user')
    return parser.parse_args()


if __name__ == '__main__':
    args = prepare_args()
    try:
        asyncio.run(send_to_chat())
    except KeyboardInterrupt:
        quit()
