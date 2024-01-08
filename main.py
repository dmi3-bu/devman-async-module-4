import asyncio
from datetime import datetime

import aiofiles


async def server():
    reader, _ = await asyncio.open_connection('minechat.dvmn.org', 5000)

    async with aiofiles.open("chat_log.txt", "a", buffering=1) as output_file:
        await log_line('Установлено соединение\n', output_file)
        while True:
            chat_line = await reader.readline()
            await log_line(chat_line.decode(), output_file)


async def log_line(message, output_file):
    now = datetime.now().strftime("%d.%m.%y %H:%M")
    line = f"[{now}] {message}"
    print(line, end="")
    await output_file.write(line)

if __name__ == '__main__':
    try:
        asyncio.run(server())
    except KeyboardInterrupt:
        quit()
