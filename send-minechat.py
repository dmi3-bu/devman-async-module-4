import asyncio

import configargparse


async def server():
    reader, writer = await asyncio.open_connection(args.host, args.port)
    await reader.readline()
    message = args.token + '\n'
    writer.write(message.encode())
    await writer.drain()

    message = "Hello world!" + '\n\n'
    writer.write(message.encode())
    await writer.drain()


def prepare_args():
    parser = configargparse.ArgParser(default_config_files=['send_config.ini'])
    parser.add_argument('--host', type=str, default='minechat.dvmn.org',
                        help='host')
    parser.add_argument('-p', '--port', type=int, default=5050,
                        help='port')
    parser.add_argument('-t', '--token', type=str, required=True,
                        help='token')
    return parser.parse_args()


if __name__ == '__main__':
    args = prepare_args()
    try:
        asyncio.run(server())
    except KeyboardInterrupt:
        quit()
