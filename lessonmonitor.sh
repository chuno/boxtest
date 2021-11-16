export LEANCLOUD_API_SERVER=http://192.168.124.48:7000
export BOX_ID=3dcc6b61375ee359
export devicepass=626364
cd /home/ubuntu/boxtest
sudo adb kill-server
sudo adb start-server
sleep 30
source ~/jncloudvenv3/bin/activate
nohup python -u lessonmonitor.py>>lessonmonitor.out  2>&1 &
