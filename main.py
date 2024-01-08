import asyncio


async def server():
    reader, _ = await asyncio.open_connection('minechat.dvmn.org', 5000)

    while True:
        data = await reader.readline()
        print(data.decode(), end="")


if __name__ == '__main__':
    asyncio.run(server())
