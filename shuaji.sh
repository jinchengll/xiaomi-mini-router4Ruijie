#!/bin/bash
des_pass=123456789

python getssh.py

rm -rf ~/.ssh/known_hosts

expect -c "
spawn scp breed.bin root@192.168.31.1:/tmp
expect {
        \"yes/no\" {send \"yes\r\"; exp_continue}
        \"password:\" {send \"$des_pass\r\"}
}
expect eof
"

expect -c "
spawn ssh root@192.168.31.1 \"mtd -r write /tmp/breed.bin Bootloader\"
expect { 
	\"(yes/no)\" {send \"yes\r\"; exp_continue}
	\"password:\" {send \"$des_pass\r\"}
}
expect eof
"
