import base64
import json
import random
import binascii
import requests
from Crypto.Cipher import AES


class WangYiSpider(object):

    def __init__(self):

        self.base_url = 'https://music.163.com/weapi/song/enhance/player/url?csrf_token='
        self.first_param = {
            "ids": '',
            "br": 12800,
            "csrf_token": ""
        }
        self.second_param = '010001'
        self.third_param = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        self.forth_param = '0CoJUm6Qyw8W8jud'

        self.headers = {
            'Referer': 'http://music.163.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }

    def get_params(self, secret_key, song_id=None):
        if not song_id:
            song_id = input("输入歌曲id")

        self.first_param["ids"] = [int(song_id)]

        data = json.dumps(self.first_param)

        params = self.aes_encrypt(data, self.forth_param)

        params = self.aes_encrypt(params, secret_key)

        return params

    @staticmethod
    def aes_encrypt(text, key):
        pad = 16 - len(text)%16

        if isinstance(text, str):
            text = text + pad * chr(pad)
        else:
            text = text.decode('utf-8') + pad * chr(pad)

        encryptor = AES.new(key, AES.MODE_CBC, "0102030405060708")
        encrypt_text = base64.b64encode(encryptor.encrypt(text))

        return encrypt_text

    @staticmethod
    def get_random_key():
        return bytes(''.join(random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',16)),'utf-8')

    def ras_encrypt(self, text):
        text = text[::-1]
        # 明文处理，反序并hex编码
        rsa = int(binascii.hexlify(text), 16) ** int(self.second_param, 16) % int(self.third_param, 16)
        return format(rsa, 'x').zfill(256)

    def save_song(self, name=None, song_id=None):

        secret_key = self.get_random_key()

        data = {
            "params" : self.get_params(secret_key, song_id=song_id),
            "encSecKey": self.ras_encrypt(secret_key)
        }

        try:
            res = requests.post(url=self.base_url, headers=self.headers, data=data).json()
        except Exception as e:
            print("歌曲url获取失败")
            print(e)
            return
        
        if not name:
            name = res['data'][0].get('id')
            
        url = res['data'][0].get('url')

        try:
            song_res = requests.get(url=url, headers=self.headers)
        except Exception as e:
            print("歌曲下载失败")
            print(e)
            return
        try:
            with open("music/{}.mp3".format(name), 'wb') as f:
                f.write(song_res.content)
                print('{} 下载成功'.format(name))
        except Exception as e:
            print('保存失败')
            print(e)


if __name__ == "__main__":
    spider = WangYiSpider()
    spider.save_song()




