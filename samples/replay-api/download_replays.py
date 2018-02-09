"""Download replay packs via Blizzard Game Data APIs."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import json
import os
import requests
import shutil
import subprocess
import sys

API_BASE_URL = 'https://us.api.battle.net'
API_NAMESPACE = 's2-client-replays'


class BnetAPI(object):

    def __init__(self, key, secret):
        headers = {"Content-Type": "application/json"}
        params = {
            "grant_type": "client_credentials",
            "client_id" : key,
            "client_secret" : secret,
        }
        response = requests.post("https://us.battle.net/oauth/token", headers=headers, params=params)
        response = json.loads(response.text)
        if 'access_token' in response:
            self._token = response['access_token']
        else:
            raise Exception('Failed to get oauth access token. response={}'.format(response))

    def get(self, url, params=None):
        params = params or {}
        params['namespace'] = API_NAMESPACE,
        headers = {"Authorization": "Bearer " + self._token}
        response = requests.get(url, headers=headers, params=params)
        return json.loads(response.text)

    def url(self, path):
        return requests.compat.urljoin(API_BASE_URL, path)

    def get_base_url(self):
        return self.get(self.url("/data/sc2/archive_url/base_url"))["base_url"]

    def search_by_client_version(self, client_version):
        params = {
            'client_version' : client_version,
            '_pageSize' : 100,
        }
        response = self.get(self.url("/data/sc2/search/archive"), params)
        meta_urls = []
        for result in response['results']:
            assert result['data']['client_version'] == client_version
            meta_urls.append(result['key']['href'])
        return meta_urls


def download_file(url, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_name = url.split('/')[-1]
    file_path = os.path.join(output_dir, file_name)

    response = requests.get(url, stream=True)
    if (not os.path.exists(file_path) or
        os.path.getsize(file_path) != int(response.headers['Content-Length'])):
        with open(file_path, 'wb') as f:
            shutil.copyfileobj(response.raw, f)

    return file_path


def main():
    args = parse_args()

    # Get OAuth token from us region
    api = BnetAPI(args.key, args.secret)

    # Get the base url for downloading replay packs
    download_base_url = api.get_base_url()

    # Get meta file infos for the give client version
    print('Searching replay packs with client version:', args.version)
    meta_file_urls = api.search_by_client_version(args.version)
    if len(meta_file_urls) == 0:
        print('No matching replay packs found for the client version!')
        return

    # For each meta file, construct full url to download replay packs
    print('Building urls for downloading replay packs. Number of packs:', len(meta_file_urls))
    download_urls = []
    for meta_file_url in meta_file_urls:
        meta_file_info = api.get(meta_file_url)
        download_urls.append(requests.compat.urljoin(download_base_url, meta_file_info['path']))

    # Download replay packs.
    files = []
    for archive_url in sorted(download_urls):
        print('Downloading replay pack:', archive_url)
        files.append(download_file(archive_url, args.replays_dir))

    if args.extract:
        for file in files:
            print('Extracting replay pack:', file)
            subprocess.call(['unzip', '-P', 'iagreetotheeula', '-o', '-d', os.path.dirname(file), file])
            os.remove(file)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', required=True, help='Battle.net API key.')
    parser.add_argument('--secret', required=True, help='Battle.net API secret.')
    parser.add_argument('--version', required=True, help='Download all replays from this Starcraft2 game version.')
    parser.add_argument('--replays_dir', default='./replays', help='Where to save the replays.')
    parser.add_argument('--extract', action='store_true', help='Whether to extract the zip files.')
    return parser.parse_args()


if __name__ == '__main__':
  main()
