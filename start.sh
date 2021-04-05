#! /bin/bash

echo "Setting up environment"
export PIN_ROOT=$(pwd)/pin/pin/

echo "Dont't forget to change kernel/yama/ptrace_scope and kernel/randomize_va_space back to 1"
echo 0 > sudo /proc/sys/kernel/yama/ptrace_scope
echo 0 > sudo /proc/sys/kernel/randomize_va_space
echo "Additional info"
gcc --version
python run.py --ptl '/PATH_TO_vuzzer-code/bin/who %s' --input 'datatemp/utmp/' --weight  'idafiles/who.pkl' -n idafiles/who.names -o '0x00000000'
echo 1 > sudo /proc/sys/kernel/yama/ptrace_scope
echo 1 > sudo /proc/sys/kernel/randomize_va_space


