import asyncio
import logging
from datetime import datetime

import aiofiles
import configargparse


logger = logging.getLogger('listener')
logging.basicConfig(level=logging.DEBUG)


async def listen_to_chat():
    reader, writer = await asyncio.open_connection(args.host, args.port)

    try:
        async with aiofiles.open(args.file, "a", buffering=1) as output_file:
            await log_line('Установлено соединение', output_file)
            while True:
                chat_line = await reader.readline()
                await log_line(chat_line.decode().rstrip(), output_file)
    except Exception as e:
        logger.debug(f'{type(e)}: {e}')
    finally:
        writer.close()


async def log_line(message, output_file):
    now = datetime.now().strftime("%d.%m.%y %H:%M")
    line = f"[{now}] {message}"
    logger.info(line)
    await output_file.write(line)


def prepare_args():
    parser = configargparse.ArgParser(default_config_files=['listen_config.ini'])
    parser.add_argument('--host', type=str, default='minechat.dvmn.org',
                        help='host')
    parser.add_argument('-p', '--port', type=int, default=5000,
                        help='port')
    parser.add_argument('-f', '--file', type=str, default='./history.txt',
                        help='file path to save logs')
    return parser.parse_args()


if __name__ == '__main__':
    args = prepare_args()
    try:
        asyncio.run(listen_to_chat())
    except KeyboardInterrupt:
        quit()
