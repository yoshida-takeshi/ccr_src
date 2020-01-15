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



roslaunch crane_plus_src controller_manager.launch
roslaunch crane_plus_src start_tilt_controller.launch
roslaunch navi_param ccr.launch

rosrun ccr_src ccr_main_ctrl_v1.py ccr_cmd.txt


