#Enable static_mode to try the app without a connection to a Bluesound player.
static_mode_conf = False

#Replace the part "192.168.190.10" with the ip-adress of your Bluesound player.
base_url_conf = "http://192.168.190.10:11000/"

#If you want to use the app on Windows, replace this with the drive letter of 
#your network shared music-folder.
windows_path_conf = "S:/"

#If you want to use the app on Linux (like Raspbian on an Raspberry pi), 
#replace this with the path of your network shared music-folder.
linux_path_conf = "/mnt/mynas/"

#The network share as used in the official Bluesound app
bluesound_path_conf = "//mynas/music/"

#The network share as found in the status.xml, using [ip adress of player]:11000/Status
#This line is found in the fn-tag.
bluesound_path2_conf = "/var/mnt/mynas-music/"

#Insert your last-fm api key if you want to use their online album art.
last_fm_api_key_conf = ""
