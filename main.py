#from src.FAT16Defines import *
from src.FAT16Parser import *

def main():
    try:
        fat16_parser = FAT16Parser("/dev/sda1", 1049000)
    except:
        print("Exiting...");
        return 0

    fat16_parser.print_data()

if __name__ == "__main__":
    sys.exit(main())
