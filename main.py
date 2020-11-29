import requests
from tqdm import tqdm
import json
from urllib.parse import quote


API_VK_TOKEN = "<Your VK api token>"
API_VERSION = "5.126"
API_YA_TOKEN = input('Введите свой токен для Ya api: ')
user_id = input('Введите свой VK id: ')


def write_json(data):
  with open('photos.json', 'w') as file:
    json.dump(data, file, indent=2, ensure_ascii=False)


def main():
  requests.put(
      "https://cloud-api.yandex.net/v1/disk/resources",
      params={"path": "upload_files"},
      headers={"Authorization": f"OAuth {API_YA_TOKEN}"})
  response = requests.get(
    "https://api.vk.com/method/photos.get",
    params={
      "owner_id": user_id,
      "album_id": "profile",
      "extended": True,
      "access_token": API_VK_TOKEN,
      "v": API_VERSION
      }
    )
  sizes = []
  likes = {}
  photos = response.json()['response']['items']
  for photo in tqdm(photos, leave=False):
    size = max(photo['sizes'], key=lambda s: s['height'] * s['width'])
    likes_count = photo['likes']['count']
    file_info = {}
    if likes_count not in likes:
      file_info['file_name'] = f'{likes_count}.jpg'
      likes[likes_count] = 1
    else:
      file_info['file_name'] = f'{likes_count}_{likes[likes_count]}.jpg'
      likes[likes_count] += 1
    file_info['size'] = size['type']
    requests.post(
      "https://cloud-api.yandex.net/v1/disk/resources/upload",
      params={"path": quote("/upload_files/" + file_info['file_name']),
              "url": size['url'],
              "overwrite": "True"},
      headers={"Authorization": f"OAuth {API_YA_TOKEN}"}).raise_for_status()
    sizes.append(file_info)
  write_json(sizes)
  print('\nФайлы успешно загружены')


if __name__ == '__main__':
  main()