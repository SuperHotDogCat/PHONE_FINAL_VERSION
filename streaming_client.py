# coding:utf-8
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.window import Window
import sys
import cv2
import numpy as np
import socket
import configparser
#ほぼ https://qiita.com/tocoteron/items/bb27351b393f087650a9 のパクリです。
class StreamView(Image):
    #Bytes型の扱いとか意識してなかった
    def __init__(self, server_ip, server_port, image_width, image_height, view_fps, view_width, view_height, **kwargs):
        super(StreamView, self).__init__(**kwargs)


        self.buff = bytes() #pythonはbytes型でバイトを操作する
        self.PACKET_HEADER_SIZE = 4
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SERVER_IP = server_ip
        self.SERVER_PORT = server_port
        self.IMAGE_WIDTH = image_width
        self.IMAGE_HEIGHT = image_height


        self.allow_stretch = True
        self.VIEW_FPS = view_fps
        self.VIEW_WIDTH = view_width
        self.VIEW_HEIGHT = view_height


        Clock.schedule_interval(self.update, 1.0 / view_fps)


        try:
            self.soc.connect((self.SERVER_IP, self.SERVER_PORT))
        except socket.error as e:
            print('Connection failed.')
            sys.exit(-1)

    def update(self, dt):
        data = self.soc.recv(self.IMAGE_HEIGHT * self.IMAGE_WIDTH * 3)
        self.buff += data

        packet_head = 0
        packets_info = list()
        while True:
            if len(self.buff) >= packet_head + self.PACKET_HEADER_SIZE:
                binary_size = int.from_bytes(self.buff[packet_head:packet_head + self.PACKET_HEADER_SIZE], 'big')
                if len(self.buff) >= packet_head + self.PACKET_HEADER_SIZE + binary_size:
                    packets_info.append((packet_head, binary_size))
                    packet_head += self.PACKET_HEADER_SIZE + binary_size
                else:
                    break
            else:
                break


        
        if len(packets_info) > 0:
            # 最新の完成したパケットの情報を取得
            packet_head, binary_size = packets_info.pop()
            # パケットから画像のバイナリを取得
            img_bytes = self.buff[packet_head + self.PACKET_HEADER_SIZE:packet_head + self.PACKET_HEADER_SIZE + binary_size]
            # バッファから不要なバイナリを削除
            self.buff = self.buff[packet_head + self.PACKET_HEADER_SIZE + binary_size:]

            # 画像をバイナリから復元
            img = np.frombuffer(img_bytes, dtype=np.uint8)
            img = cv2.imdecode(img, 1)
            # 画像を表示用に加工
            img = cv2.flip(img, 0)
            img = cv2.resize(img, (self.VIEW_WIDTH, self.VIEW_HEIGHT))
            # 画像をバイナリに変換
            img = img.tostring()

            # 作成した画像をテクスチャに設定
            img_texture = Texture.create(size=(self.VIEW_WIDTH, self.VIEW_HEIGHT), colorfmt='bgr')
            img_texture.blit_buffer(img, colorfmt='bgr', bufferfmt='ubyte')
            self.texture = img_texture

    def disconnect(self):

        self.soc.shutdown(socket.SHUT_RDWR)
        self.soc.close()

class StreamingClientApp(App):

    def __init__(self, view_fps, view_width, view_height, **kwargs):
        super(StreamingClientApp, self).__init__(**kwargs)
        self.VIEW_FPS = view_fps
        self.VIEW_WIDTH = view_width
        self.VIEW_HEIGHT = view_height

    def build(self):

        config = configparser.ConfigParser()
        config.read('./connection.ini', 'UTF-8')
        config_server_ip = config.get('server', 'ip')
        config_server_port = int(config.get('server', 'port'))
        config_header_size = int(config.get('packet', 'header_size'))
        config_image_width = int(config.get('packet', 'image_width'))
        config_image_height = int(config.get('packet', 'image_height'))

        Window.size = (self.VIEW_WIDTH, self.VIEW_HEIGHT)


        self.stream_view = StreamView(
            server_ip=config_server_ip,
            server_port=config_server_port,
            image_width=config_image_width,
            image_height=config_image_height,
            view_fps=self.VIEW_FPS,
            view_width=self.VIEW_WIDTH,
            view_height=self.VIEW_HEIGHT
        )
        return self.stream_view

    def on_stop(self):

        self.stream_view.disconnect()

if __name__ == '__main__':
    StreamingClientApp(view_fps=30, view_width=800, view_height=600).run()