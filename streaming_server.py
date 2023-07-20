# coding:utf-8
import socket
import numpy as np
import cv2
import time
import configparser
config = configparser.ConfigParser()
config.read('./connection.ini', 'UTF-8')
#ほぼ https://qiita.com/tocoteron/items/bb27351b393f087650a9 のパクリです。

FPS = 12
INDENT = '    '


CAMERA_ID = 0
CAMERA_FPS = 12
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720


SERVER_IP = '127.0.0.1'
SERVER_PORT = int(config.get('server', 'port'))


HEADER_SIZE = int(config.get('packet', 'header_size'))


IMAGE_WIDTH = int(config.get('packet', 'image_width'))
IMAGE_HEIGHT = int(config.get('packet', 'image_height'))
IMAGE_QUALITY = 30


cam = cv2.VideoCapture(CAMERA_ID) #カメラ制御を行うためのもの、VideoCaptureClass
cam.set(cv2.CAP_PROP_FPS, CAMERA_FPS) #fps指定
cam.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH) #サイズ指定
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)


print('Camera {')
print(INDENT + 'ID    : {},'.format(CAMERA_ID))
print(INDENT + 'FPS   : {},'.format(cam.get(cv2.CAP_PROP_FPS)))
print(INDENT + 'WIDTH : {},'.format(cam.get(cv2.CAP_PROP_FRAME_WIDTH)))
print(INDENT + 'HEIGHT: {}'.format(cam.get(cv2.CAP_PROP_FRAME_HEIGHT)))
print('}')

#ソケット制作、PyとCで同時に起動することにしている
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((SERVER_IP, SERVER_PORT))
s.listen(1)
soc, addr = s.accept()

print('Server {')
print(INDENT + 'IP   : {},'.format(SERVER_IP))
print(INDENT + 'PORT : {}'.format(SERVER_PORT))
print('}')


print('Client {')
print(INDENT + 'IP   : {},'.format(addr[0]))
print(INDENT + 'PORT : {}'.format(addr[1]))
print('}')


while True:
    loop_start_time = time.time()

    # 送信用画像データ作成
    flag, img = cam.read() #1フレーム分のカメラ映像を取り込む
    resized_img = cv2.resize(img, (IMAGE_WIDTH, IMAGE_HEIGHT))
    (status, encoded_img) = cv2.imencode('.jpg', resized_img, [int(cv2.IMWRITE_JPEG_QUALITY), IMAGE_QUALITY]) #圧縮する

    # パケット構築(ここで詰まった)
    packet_body = encoded_img.tostring()
    packet_header = len(packet_body).to_bytes(HEADER_SIZE, 'big') #バイトにして送る
    packet = packet_header + packet_body


    try:
        soc.sendall(packet)
    except socket.error as e:
        print('Connection closed.')
        break


    time.sleep(max(0, 1 / FPS - (time.time() - loop_start_time)))

s.close()
