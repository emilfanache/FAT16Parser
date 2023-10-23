#!/usr/bin/env python3

# FROM: https://www.win.tue.nl/~aeb/linux/fs/fat/fat-1.html
# Bytes   Content
# 0-2     Jump to bootstrap (E.g. eb 3c 90; on i86: JMP 003E NOP.
#         One finds either eb xx 90, or e9 xx xx.
#         The position of the bootstrap varies.)
# 3-10    OEM name/version (E.g. "IBM  3.3", "IBM 20.0", "MSDOS5.0", "MSWIN4.0".
#         Various format utilities leave their own name, like "CH-FOR18".
#         Sometimes just garbage. Microsoft recommends "MSWIN4.1".)
#         /* BIOS Parameter Block starts here */
# 11-12   Number of bytes per sector (512)
#         Must be one of 512, 1024, 2048, 4096.
# 13      Number of sectors per cluster (1)
#         Must be one of 1, 2, 4, 8, 16, 32, 64, 128.
#         A cluster should have at most 32768 bytes. In rare cases 65536 is OK.
# 14-15   Number of reserved sectors (1)
#         FAT12 and FAT16 use 1. FAT32 uses 32.
# 16      Number of FAT copies (2)
# 17-18   Number of root directory entries (224)
#         0 for FAT32. 512 is recommended for FAT16.
# 19-20   Total number of sectors in the filesystem (2880)
#         (in case the partition is not FAT32 and smaller than 32 MB)
# 21      Media descriptor type (f0: 1.4 MB floppy, f8: hard disk; see below)
# 22-23   Number of sectors per FAT (9)
#         0 for FAT32.
# 24-25   Number of sectors per track (12)
# 26-27   Number of heads (2, for a double-sided diskette)
# 28-29   Number of hidden sectors (0)
#         Hidden sectors are sectors preceding the partition.
#         /* BIOS Parameter Block ends here */
# 30-509  Bootstrap
# 510-511 Signature 55 aa

import sys
from enum import IntEnum

class FAT16FieldBytes(IntEnum):
    JUMP_TO_BOOTSTRAP = 0
    OEM = 3
    BYTES_PER_SECTOR = 11
    SECTORS_PER_CLUSTER = 13
    RESERVED_SECTORS = 14
    NUMBER_OF_FATS = 16
    ROOTDIR_ENTRIES = 17
    TOTAL_FS_SECTORS = 19
    MEDIA_DESCRIPTOR_TYPE = 21
    SECTORS_PER_FAT = 22
    SECTORS_PER_TRACK = 24
    NUM_HEADS = 26
    NUM_HIDDEN_SECTORS = 28
    BOOTSTRAP = 30
    SIGNATURE = 510

FAT16FieldBytesCount = {
    FAT16FieldBytes.JUMP_TO_BOOTSTRAP : 2,
    FAT16FieldBytes.OEM : 8,
    FAT16FieldBytes.BYTES_PER_SECTOR : 2,
    FAT16FieldBytes.SECTORS_PER_CLUSTER : 1,
    FAT16FieldBytes.RESERVED_SECTORS : 2,
    FAT16FieldBytes.NUMBER_OF_FATS : 1,
    FAT16FieldBytes.ROOTDIR_ENTRIES : 2,
    FAT16FieldBytes.TOTAL_FS_SECTORS : 2,
    FAT16FieldBytes.MEDIA_DESCRIPTOR_TYPE : 1,
    FAT16FieldBytes.SECTORS_PER_FAT : 2,
    FAT16FieldBytes.SECTORS_PER_TRACK : 2,
    FAT16FieldBytes.NUM_HEADS : 2,
    FAT16FieldBytes.NUM_HIDDEN_SECTORS : 2,
    FAT16FieldBytes.BOOTSTRAP : 480,
    FAT16FieldBytes.SIGNATURE : 2
}
