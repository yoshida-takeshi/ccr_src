# Open JTalk関連パッケージ

## サンプルプログラム(test_jtalk_v1.py)
`ubuntu% ./test_jtalk_v1.py`  
  引数なし → 現在時刻を読み上げ

`ubuntu% ./test_jtalk_v1.py sample.txt`  
  ファイル名指定 → テキストファイルの内容を読み上げ


## Open JTalk インストールメモ
#### パッケージインストール
`ubuntu% sudo apt-get install open-jtalk open-jtalk-mecab-naist-jdic hts-voice-nitech-jp-atr503-m001`  

#### 音声モデル追加
`ubuntu% wget http://sourceforge.net/projects/mmdagent/files/MMDAgent_Example/MMDAgent_Example-1.7/MMDAgent_Example-1.7.zip`  
`ubuntu% unzip MMDAgent_Example-1.7.zip`  
`ubuntu% sudo cp -r MMDAgent_Example-1.7/Voice/mei/ /usr/share/hts-voice/`  
