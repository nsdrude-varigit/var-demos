#!/bin/bash
set -e
readonly TARGET_IP="$1"
readonly PROGRAM="$2"
readonly TARGET_DIR="/home/root"

usage() {
    echo "Usage:   ./var-build-and-debug.sh <target ip> <program name>"
    echo "Example: ./var-build-and-debug.sh 192.168.0.134 hello.bin"
    exit 1
}

# Verify build environment
if ! echo ${GDB} | grep -qi aarch64 || ! echo ${CXX} | grep -iq aarch64; then
    echo "Error: Please make sure to source the toolchain setup script in /opt/"
    echo "For Example:"
    echo "source /opt/fsl-imx-xwayland/5.4-zeus/environment-setup-aarch64-poky-linux"
    exit 1
fi

# Verify args
if [ -z ${TARGET_IP} ] || [ -z ${PROGRAM} ]; then
    usage
fi

# rebuild project
make clean; make -j$(nproc)

# kill gdbserver on target
ssh root@${TARGET_IP} "sh -c '/usr/bin/killall -q gdbserver; exit 0'"

# send the program to the target
scp ${PROGRAM} root@${TARGET_IP}:${TARGET_DIR}

# start gdbserver on target
REMOTE_GDB_CMD="ssh -t root@${TARGET_IP} \"sh -c 'cd ${TARGET_DIR}; gdbserver localhost:3000 ${PROGRAM}'\""
gnome-terminal -x bash -c "${REMOTE_GDB_CMD}"
