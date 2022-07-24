export LEANCLOUD_API_SERVER=http://192.168.124.48:7000
export BOX_ID=27043b125bbab5a1
export devicepass=626364
cd /home/ubuntu/boxtest
sudo adb kill-server
sleep 30
sudo adb start-server
source ~/jncloudvenv3/bin/activate
nohup python3 androidmonitor.py>>amonitor.out  2>&1 &
