import os
import requests
import json
import argparse
import urlparse
import shutil

API_BASE_URL = 'https://us.api.battle.net'
API_NAMESPACE = 's2-client-replays'


def get_bnet_oauth_access_token(url, key, secret):
  headers = { "Content-Type": "application/json"}
  params = {
    "grant_type": "client_credentials",
    "client_id" : key,
    "client_secret" : secret
  }
  response = requests.post(url=url, headers=headers, params=params)
  response = json.loads(response.text)
  if 'access_token' in response:
    return response['access_token']
  raise Exception('Failed to get oauth access token. response={}'.format(response))


def get_base_url(access_token):
  headers = {"Authorization": "Bearer " + access_token}
  params = {
    'namespace' : API_NAMESPACE,
  }
  response = requests.get(urlparse.urljoin(API_BASE_URL, "/data/sc2/archive_url/base_url"), headers=headers,
                          params=params)
  return json.loads(response.text)["base_url"]


def search_by_client_version(access_token, client_version):
  headers = {"Authorization": "Bearer " + access_token}
  params = {
    'namespace' : API_NAMESPACE,
    'client_version' : client_version,
    '_pageSize' : 25
  }
  response = requests.get(urlparse.urljoin(API_BASE_URL, "/data/sc2/search/archive"), headers=headers, params=params)
  response = json.loads(response.text)
  meta_urls = []
  for result in response['results']:
    assert result['data']['client_version'] == client_version
    meta_urls.append(result['key']['href'])
  return meta_urls


def get_meta_file_info(access_token, url):
  headers = { "Authorization": "Bearer " + access_token}
  params = {
    'namespace' : API_NAMESPACE,
  }

  response = requests.get(url, headers=headers, params=params)
  return json.loads(response.text)


def download_file(url, output_dir):
  # Create output_dir if not exists.
  if not os.path.exists(output_dir):
    os.makedirs(output_dir)

  file_name = url.split('/')[-1]
  file_path = os.path.join(output_dir, file_name)

  response = requests.get(url, stream=True)
  with open(file_path, 'wb') as f:
    shutil.copyfileobj(response.raw, f)


def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('--client_key', dest='client_key', action='store', type=str, help='Battle.net API key')
  parser.add_argument('--client_secret', dest='client_secret', action='store', type=str, help='Battle.net API secret')
  parser.add_argument('--s2-client-version', dest='s2_client_version', action='store', type=str,
                      help='Starcraft2 client version for searching replay archives with')
  parser.add_argument('--replays-dir', dest='replays_dir', action='store', type=str, default='./replays', help='the directory for saving downloaded replay archives')
  return parser.parse_args()


def main():
  args = parse_args()

  try:
    # Get OAuth token from us region
    access_token = get_bnet_oauth_access_token("https://us.battle.net/oauth/token", args.client_key, args.client_secret)

    # Get the base url for downloading replay packs
    download_base_url = get_base_url(access_token)

    # Get meta file infos for the give client version
    print 'Searching replay packs with client version=' + args.s2_client_version
    meta_file_urls = search_by_client_version(access_token, args.s2_client_version)
    if len(meta_file_urls) == 0:
      print 'No matching replay packs found for the client version!'
      return

    # For each meta file, construct full url to download replay packs
    print 'Building urls for downloading replay packs. num_files={0}'.format(len(meta_file_urls))
    download_urls=[]
    for meta_file_url in meta_file_urls:
      meta_file_info = get_meta_file_info(access_token, meta_file_url)
      file_path = meta_file_info['path']
      download_urls.append(urlparse.urljoin(download_base_url, file_path))

    # Download replay packs.
    for archive_url in sorted(download_urls):
      print 'Downloading replay packs. url='  + archive_url
      download_file(archive_url, args.replays_dir)

  except Exception as e:
    import traceback
    print 'Failed to download replay packs. traceback={}'.format(traceback.format_exc())


if __name__ == '__main__':
  main()
