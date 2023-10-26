# FAT16Parser

This is a FAT16 Parser implemented in Python. Initial purpose was for it to parse a corrupted partition of a drive. There are other parsers online,<br/>
but I needed an implementation that's maybe a bit more descriptive.


## Requirements
Python3

## Quick start
First of all make sure you have the right permission to run the script. It needs the drive path and the offset for the FAT partition<br/>
If the offset is not specified it will be set to 0. You can specify the offset in 2 ways:<br/>
- by specifying the number of bytes<br/>
```
sudo python3 main.py -f /dev/sda -b 8388608
```
    
- by specifying the number of sectors and the number of bytes per sector<br/>
```
sudo python3 main.py -f /dev/sda -s 16384 -l 512
# by default sector size is 512
sudo python3 main.py -f /dev/sda -s 16384
```

<br/>

## Limitations
In theory it should work with FAT & FAT32, not just FAT16, but I didn't test it further.

## Special thanks
https://www.win.tue.nl/~aeb/linux/fs/fat/fat-1.html<br/>
http://www.c-jump.com/CIS24/Slides/FAT/FAT.html#F01_0050_fat12_fat16_fat32_lay<br/>
https://stackoverflow.com/<br/>
