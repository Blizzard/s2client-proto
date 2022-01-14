# Lint as: python3
"""Download replay packs via Blizzard Game Data APIs."""

# pylint: disable=bad-indentation, line-too-long

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import collections
import csv
import itertools
import json
import logging
import os
import requests
import shutil
import subprocess
import sys
import zipfile

try:
    import mpyq
except ImportError:
    logging.warning(
        'Failed to import mpyq; version and corruption detection is disabled.')
    mpyq = None
from six import print_ as print  # To get access to `flush` in python 2.

API_BASE_URL = 'https://us.api.blizzard.com'
API_NAMESPACE = 's2-client-replays'


class RequestError(Exception):
    pass


def mkdirs(path):
    if not os.path.exists(path):
        os.makedirs(path)


def print_part(*args):
    print(*args, end='', flush=True)


class BnetAPI(object):
    """Represents a handle to the battle.net api."""

    def __init__(self, key, secret):
        headers = {'Content-Type': 'application/json'}
        params = {'grant_type': 'client_credentials'}
        response = requests.post('https://us.battle.net/oauth/token',
                                 headers=headers, params=params,
                                 auth=requests.auth.HTTPBasicAuth(key, secret))
        if response.status_code != requests.codes.ok:
            raise RequestError(
                'Failed to get oauth access token. response={}'.format(response))
        response = json.loads(response.text)
        if 'access_token' in response:
            self._token = response['access_token']
        else:
            raise RequestError(
                'Failed to get oauth access token. response={}'.format(response))

    def get(self, url, params=None):
        """Make an autorized get request to the api by url."""
        params = params or {}
        params['namespace'] = API_NAMESPACE,
        headers = {'Authorization': 'Bearer ' + self._token}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != requests.codes.ok:
            raise RequestError(
                'Request to "{}" failed. response={}'.format(url, response))
        response_json = json.loads(response.text)
        if response_json.get('status') == 'nok':
            raise RequestError(
                'Request to "{}" failed. response={}'.format(
                    url, response_json.get('reason')))
        return response_json

    def url(self, path):
        return requests.compat.urljoin(API_BASE_URL, path)

    def get_base_url(self):
        return self.get(self.url('/data/sc2/archive_url/base_url'))['base_url']

    def search_by_client_version(self, client_version):
        """Search for replay archives by version."""
        meta_urls = []
        for page in itertools.count(1):
            params = {
                'client_version': client_version,
                '_pageSize': 100,
                '_page': page,
            }
            response = self.get(self.url('/data/sc2/search/archive'), params)
            for result in response['results']:
                assert result['data']['client_version'] == client_version
                meta_urls.append(result['key']['href'])
            if response['pageCount'] <= page:
                break
        return meta_urls


def download(key, secret, version, replays_dir, download_dir, extract=False,
             remove=False, filter_version='keep', replayset_csv=None):
    """Download the replays for a specific version. Check help below."""
    # Get OAuth token from us region
    api = BnetAPI(key, secret)

    # Get meta file infos for the give client version
    print('Searching replay packs with client version:', version)
    meta_file_urls = api.search_by_client_version(version)
    if len(meta_file_urls) == 0:
        sys.exit('No matching replay packs found for the client version!')

    # Parse replayset.
    if replayset_csv is not None:
        files = []
        with open(replayset_csv, 'r') as csv_file:
            for row in csv.reader(csv_file):
                if row[0] == version:
                    files.append(row[1] + '.SC2Replay')
        files = set(files)
    else:
        files = None

    # Download replay packs.
    download_base_url = api.get_base_url()
    print('Found {} replay packs'.format(len(meta_file_urls)))
    print('Downloading to:', download_dir)
    print('Extracting to:', replays_dir)
    mkdirs(download_dir)
    for i, meta_file_url in enumerate(sorted(meta_file_urls), 1):
        # Construct full url to download replay packs
        meta_file_info = api.get(meta_file_url)
        archive_url = requests.compat.urljoin(download_base_url,
                                              meta_file_info['path'])

        print_part('{}/{}: {} ... '.format(i, len(meta_file_urls), archive_url))

        file_name = archive_url.split('/')[-1]
        file_path = os.path.join(download_dir, file_name)

        with requests.get(archive_url, stream=True) as response:
            content_length = int(response.headers['Content-Length'])
            print_part(content_length // 1024**2, 'Mb ... ')
            if (not os.path.exists(file_path) or
                    os.path.getsize(file_path) != content_length):
                with open(file_path, 'wb') as f:
                    shutil.copyfileobj(response.raw, f)
                print_part('downloaded')
            else:
                print_part('found')

        if extract:
            print_part(' ... extracting')
            if os.path.getsize(file_path) <= 22:  # Size of an empty zip file.
                print_part(' ... zip file is empty')
            elif files:
               with zipfile.ZipFile(file_path) as zip_file:
                   for member in zip_file.namelist():
                       if member in files:
                           zip_file.extract(
                               member, path=replays_dir, pwd=b'iagreetotheeula')
            else:
                subprocess.call(['unzip', '-P', 'iagreetotheeula', '-u', '-o',
                                 '-q', '-d', replays_dir, file_path])
            if remove:
                os.remove(file_path)
        print()

    if mpyq is not None and filter_version != 'keep':
        print('Filtering replays.')
        found_versions = collections.defaultdict(int)
        found_str = lambda: ', '.join('{}: {}'.format(v, c)
                                      for v, c in sorted(found_versions.items()))
        all_replays = [f for f in os.listdir(replays_dir) if f.endswith('.SC2Replay')]
        for i, file_name in enumerate(all_replays):
            if i % 100 == 0:
                print_part('\r{}/{}: {:.1f}%, found: {}'.format(
                    i, len(all_replays), 100 * i / len(all_replays), found_str()))
            file_path = os.path.join(replays_dir, file_name)
            with open(file_path, 'rb') as fd:
                try:
                    archive = mpyq.MPQArchive(fd).extract()
                    metadata = json.loads(
                        archive[b'replay.gamemetadata.json'].decode('utf-8'))
                except KeyboardInterrupt:
                  raise
                except:  # pylint: disable=bare-except
                    found_versions['corrupt'] += 1
                    os.remove(file_path)
                    continue
            game_version = '.'.join(metadata['GameVersion'].split('.')[:-1])
            found_versions[game_version] += 1
            if filter_version == 'sort':
                version_dir = os.path.join(replays_dir, game_version)
                if found_versions[game_version] == 1:  # First one of this version.
                    mkdirs(version_dir)
                os.rename(file_path, os.path.join(version_dir, file_name))
            elif filter_version == 'delete':
                if game_version != version:
                    os.remove(file_path)
        print('\nFound replays:', found_str())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', required=True, help='Battle.net API key.')
    parser.add_argument('--secret', required=True, help='Battle.net API secret.')
    parser.add_argument('--version', required=True,
                        help=('Download all replays from this StarCraft 2 game'
                              'version, eg: "4.8.3".'))
    parser.add_argument('--replays_dir', default='./replays',
                        help='Where to save the replays.')
    parser.add_argument('--download_dir', default='./download',
                        help='Where to save the zip files.')
    parser.add_argument('--extract', action='store_true',
                        help='Whether to extract the zip files.')
    parser.add_argument('--remove', action='store_true',
                        help='Whether to delete the zip files after extraction.')
    parser.add_argument('--filter_version', default='keep',
                        choices=['keep', 'delete', 'sort'],
                        help=("What to do with replays that don't match the "
                              "requested version. Keep is fast, but does no "
                              "filtering. Delete deletes any that don't match. "
                              "Sort puts them in sub-directories based on "
                              "their version."))
    parser.add_argument('--replayset_csv', default=None,
                        help=("Path to a csv file containing version, replay hash. "
                              "If specified, only those replays listed for the "
                              "requested game version will be extracted."))
    args = parser.parse_args()
    args_dict = dict(vars(args).items())
    download(**args_dict)


if __name__ == '__main__':
    main()
