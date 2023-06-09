import aiohttp


class AsyncHelper:

    @staticmethod
    async def post(endpoint_uri, **kwargs):
        async with aiohttp.ClientSession() as session:
            return await session.post(endpoint_uri, timeout=15, **kwargs)

    @staticmethod
    async def get(endpoint_uri, params, **kwargs):
        async with aiohttp.ClientSession() as session:
            return await session.get(endpoint_uri, params=params, **kwargs)
