import os
import sys
from optparse import OptionParser
from src.FAT16Parser import *

"""
From StackOverflow:
https://stackoverflow.com/questions/33685078/python-check-if-a-dev-disk-device-exists
"""
def exists(path):
    """Test whether a path exists.  Returns False for broken symbolic links"""
    try:
        os.stat(path)
    except OSError:
        return False
    return True


def main():
    parser = OptionParser()
    parser.add_option("-f", "--file-name",
                    dest = "partition_name",
                    default = None,
                    help = "The external partition from where you wnat to read the FAT16 data",
                    metavar = "FILE")
    parser.add_option('-b', "--bytes-offset",
                       dest = "bytes_offset",
                       type = "int",
                       default = 0,
                       help = "Number of bytes to skip at the beginning of the partition")

    parser.add_option('-s', "--sector-offset",
                       dest = "sect_offset",
                       type = "int",
                       default = 0,
                       help = "Number of sectors to skip at the beginning of the partition")

    parser.add_option('-l', "--sector-size",
                   dest = "sect_size",
                   type = "int",
                   default = 512,
                   help = "The size of a sector (in bytes). Default is 512.")

    (options, args) = parser.parse_args()

    if not options.partition_name:
        print("Partition name can not be empty!")
        sys.exit(0)
        
    if not exists(options.partition_name):
        print(f"Unable to find partition {options.partition_name}")
        sys.exit(0)

    offset = 0
    if "-b" in sys.argv or "--bytes-offset" in sys.argv:
        offset = options.bytes_offset
    else:
        offset = options.sect_offset * options.sect_size
    
    try:
        fat16_parser = FAT16Parser(options.partition_name, offset)
    except:
        print("Error parsing FAT16. Check file name, offset or permissions!");
        return 0

    fat16_parser.print_data()

if __name__ == "__main__":
    sys.exit(main())
