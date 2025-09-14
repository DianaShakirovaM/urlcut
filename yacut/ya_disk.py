import os
import urllib

import asyncio
import aiohttp


API_HOST = os.getenv('API_HOST', 'https://cloud-api.yandex.net/')
API_VERSION = os.getenv('API_VERSION', 'v1')
REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'
DISK_TOKEN = os.getenv('DISK_TOKEN', 'your token')
AUTH_HEADERS = {
    'Authorization': f'OAuth {DISK_TOKEN}'
}


async def upload_files_to_disk(files):
    if files is not None:
        async with aiohttp.ClientSession() as session:
            tasks = [
                asyncio.ensure_future(upload_file_and_get_url(session, file))
                for file in files
            ]
            urls = await asyncio.gather(*tasks)
        return urls


async def upload_file_and_get_url(session, file):
    payload = {
        'path': f'app:/{file.filename}',
        'overwrite': 'True'
    }
    async with session.get(
        headers=AUTH_HEADERS,
        params=payload,
        url=REQUEST_UPLOAD_URL
    ) as response:
        response_serialized = await response.json()
        upload_url = response_serialized['href']
    async with session.put(
        data=file.read(),
        url=upload_url,
    ) as response:
        response_headers = response.headers
        location = urllib.parse.unquote(
            response_headers['Location']
        ).replace('/disk', '')
    async with session.get(
        headers=AUTH_HEADERS,
        url=DOWNLOAD_LINK_URL,
        params={'path': location}
    ) as response:
        response_serialized = await response.json()
        return response_serialized['href']
