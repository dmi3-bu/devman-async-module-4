import asyncio
import json
import logging

import configargparse

logger = logging.getLogger('sender')
logging.basicConfig(level=logging.DEBUG)


async def server():
    reader, writer = await asyncio.open_connection(args.host, args.port)
    prompt = await reader.readline()
    logger.debug(prompt.decode())

    if args.token is None:
        message = '\n'
        writer.write(message.encode())
        await writer.drain()
        logger.debug(message)

        new_user_prompt = await reader.readline()
        logger.debug(new_user_prompt.decode())

        nickname = input('Введите ник нового пользователя:') + '\n'
        writer.write(nickname.encode())
        await writer.drain()
        logger.debug(nickname)

        json_response = await reader.readline()
        logger.debug(json_response.decode())
        account_hash = json.loads(json_response.decode())["account_hash"]
        with open('send_config.ini', 'a') as f:
            f.write(f'\ntoken={account_hash}\n')
    else:
        message = args.token + '\n'
        writer.write(message.encode())
        await writer.drain()
        logger.debug(message)

        json_response = await reader.readline()
        logger.debug(json_response.decode())
        if json.loads(json_response.decode()) is None:
            print("Неизвестный токен. Проверьте его или зарегистрируйте заново.")
            return

    message = "Hello world!" + '\n\n'
    writer.write(message.encode())
    await writer.drain()
    logger.debug(message)


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
