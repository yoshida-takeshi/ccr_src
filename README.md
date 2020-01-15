# ccr制御パッケージ

## Open JTalk インストールメモ
#### パッケージインストール
`ubuntu% sudo apt-get install open-jtalk open-jtalk-mecab-naist-jdic hts-voice-nitech-jp-atr503-m001`  

#### 音声モデル追加
`ubuntu% wget http://sourceforge.net/projects/mmdagent/files/MMDAgent_Example/MMDAgent_Example-1.7/MMDAgent_Example-1.7.zip`  
`ubuntu% unzip MMDAgent_Example-1.7.zip`  
`ubuntu% sudo cp -r MMDAgent_Example-1.7/Voice/mei/ /usr/share/hts-voice/`  


## 起動手順
事前準備  
roslaunch crane_plus_src controller_manager.launch  
roslaunch crane_plus_src start_tilt_controller.launch  
roslaunch navi_param ccr.launch  

メイン実行
rosrun ccr_src ccr_main_ctrl_v1.py ccr_cmd.txt  


