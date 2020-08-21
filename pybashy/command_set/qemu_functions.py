# one type hdd
qemu-img create debian.img 2G

# qcow format
qemu-img create -f qcow2 debian.qcow 2G
# download image

# boot image
 qemu-system-x86_64 -hda debian.img -cdrom debian-testing-amd64-netinst.iso -boot d -m 512

# get SWAP UUID
 blkid | awk -F\" '/swap/ {print $2}'

 # add swap UUID to /etc/initramfs-tools/conf.d/resume

 printf "RESUME=UUID=$(blkid | awk -F\" '/swap/ {print $2}')\n" | sudo tee /etc/initramfs-tools/conf.d/resume

#  update the kernels on the system:
 sudo update-initramfs -u -k all

# start with interface set
#ifname=tap0 - the tap name here corresponds with the name in the bridge stanza above.
#script=no,downscript=no disable the scripts /etc/qemu-ifup and /etc/qemu-ifdown as they are not needed.
 qemu-system-x86_64 -hda imagefile.img -net nic -net tap,ifname=tap0,script=no,downscript=no