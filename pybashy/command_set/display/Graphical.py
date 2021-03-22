 
# After change to a text console (pressing Ctrl+Alt+F2) and logging in as root, 
# use the following command to disable the graphical target, which is what keeps 
# the display manager running:
#stop x
stop_graphical1 = { 'stop_graphical1' : ['systemctl isolate multi-user.target',"",""]}
# start x
start_x_session = { 'start_x_session' : ['systemctl start graphical.target',"",""]}
# set default to text
set_default_multiuser1 = { 'set_default_multiuser1' : ['sudo systemctl set-default multi-user.target',"",""]}
set_default_multiuser2 = { 'set_default_multiuser2' : ['sudo systemctl set-default runlevel3.target',"",""]}
#set default to x
set_default_graphical1  = { 'set_default_graphical1' : ['sudo systemctl set-default graphical.target',"",""]}
set_default_graphical2  = { 'set_default_graphical2' : ['sudo systemctl set-default runlevel5.target',"",""]}
# unload the Nvidia drivers using modprobe -r (or rmmod directly):
remove_nvidia_drm = { 'remove_nvidia_drm' : ['modprobe -r nvidia-drm',"",""]}
# remove the proprietary Nvidia driver:
remove_nvidia_drivers   = { 'remove_nvidia_drivers' : ["sudo dpkg -P $(dpkg -l | grep nvidia-driver | awk '{print $2}')","",""]}
apt_autoremove          = { 'apt_autoremove' : ["sudo apt autoremove","",""]}
#Locate the installation script used to install the Nvidia driver. In case you cannot locate the
# if you are running nvidia-persistenced, 
# you'll need to stop that too before you can unload the nvidia_drm module.
uninstall_nvidia = {'uninstall_nvidia' : ["sudo ls ./ | grep 'NVIDIA-Linux-x86_64' | xargs -I '{}' bash -exec 'sh {} --uninstall","",""]}
