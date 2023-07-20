# PHONE_FINAL_VERSION

授業で作ったものです <br>
この制作物ではカメラ通話、書き起こしの他に書き起こしの言語が日本語以外の時に翻訳機能が使えます。<br>
実行方法(まずはクローンすること)<br>
まずbrewで必要なアプリを入れましょう。<br>
`
brew install ffmpeg
`
<br>
仮想環境構築(これをしないとPython環境を破壊しうる可能性があります。)<br>
`
python3 -v venv env
`<br>
必ず仮想環境を有効にしてからライブラリをインストールしてください33.4分ぐらいかかります<br>
`
source env/bin/activate
`<br>
`
pip -r install requirements.txt
`<br>
シェルコマンドに実行許可を与えます<br>
`
chmod +x phone_serv_test.sh
`<br>
`
chmod +x phone_client_test.sh
`
<br>
上手く書き起こし、翻訳機能が使えるかを確認しましょう。<br>
`
python3 write_down.py obama.wav write_down.txt
`<br>
しばらくするとwrite_down.txtに書き起こしした内容と翻訳した内容が書き込まれるはずです。<br>
<br>
ここまでを実行した後、<br>
`./phone_serv_test.sh
./phone_client_test.sh`
<br>の順でシェルコマンドを実行すれば使えます。<br>
友達と通話したい時はconnnection.iniを編集しましょう。<br>


