#!/bin/sh
touch input1.raw
touch input2.raw
touch input1.wav
touch input2.wav
gcc phone2.c -o phone2
python3 streaming_server.py &
./phone2 100
sox -b 16 -c 1 -e s -r 48000 input1.raw -b 16 -c 1 -e s -r 48000 input1.wav
sox -b 16 -c 1 -e s -r 48000 input2.raw -b 16 -c 1 -e s -r 48000 input2.wav
python3 write_down.py input1.wav interview.txt
python3 write_down.py input2.wav interview2.txt
rm input1.raw
rm input2.raw