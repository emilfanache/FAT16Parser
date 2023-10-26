#!/usr/bin/env python3

import sys
from .FAT16Defines import *


class FAT16Parser:
    def __init__(self, filename, offset = 0):
        if not filename:
            raise("Filename doesn't exist.")

        try:
            self.fd = open(filename, 'rb')
        except:
            raise("Error opening file:", sys.exc_info()[0])

        self.offset = offset

    def __get_data_from_bytes(self, start_byte):
        '''
        The bytes in the FAT16 boot partition are represented in little endian.
        '''
        self.fd.seek(start_byte + self.offset)
        binary_data = self.fd.read(FAT16FieldBytesCount[start_byte])
        return int.from_bytes(binary_data, byteorder='little')

    def get_number_of_bytes_per_sector(self):
        return self.__get_data_from_bytes(FAT16FieldBytes.BYTES_PER_SECTOR)

    def get_number_of_sectors_per_cluster(self):
        return self.__get_data_from_bytes(FAT16FieldBytes.SECTORS_PER_CLUSTER)

    def get_number_of_reserved_sectors(self):
        return self.__get_data_from_bytes(FAT16FieldBytes.RESERVED_SECTORS)

    def get_number_of_fats(self):
        return self.__get_data_from_bytes(FAT16FieldBytes.NUMBER_OF_FATS)

    def get_number_of_rootdir_entries(self):
        return self.__get_data_from_bytes(FAT16FieldBytes.ROOTDIR_ENTRIES)

    def get_total_fs_sectors(self):
        return self.__get_data_from_bytes(FAT16FieldBytes.TOTAL_FS_SECTORS)

    def get_media_descriptor_type(self):
        return self.__get_data_from_bytes(FAT16FieldBytes.MEDIA_DESCRIPTOR_TYPE)

    def get_number_of_sectors_per_fat(self):
        return self.__get_data_from_bytes(FAT16FieldBytes.SECTORS_PER_FAT)

    def get_number_of_sectors_per_track(self):
        return self.__get_data_from_bytes(FAT16FieldBytes.SECTORS_PER_TRACK)

    def get_number_of_heads(self):
        return self.__get_data_from_bytes(FAT16FieldBytes.NUM_HEADS)

    def get_number_of_hidden_sectors(self):
        return self.__get_data_from_bytes(FAT16FieldBytes.NUM_HIDDEN_SECTORS)

    def get_root_dir_ranges(self):
        '''
        In order to find the root directory ranges we need to take into account
        BOOT parition organization:
            - Reserved Area
            - First FAT
            - Second FAT
            - Root Directory
        Each entry in the Root Directory has 32MB. The total number of entries
        multiplied by 32 will give us the size in MB. But we need the size in
        sectors, hence the division to bytes_per_sector
        '''
        reserved = self.get_number_of_reserved_sectors()
        num_fats = self.get_number_of_fats()
        sectors_per_fat = self.get_number_of_sectors_per_fat()
        # reserved sectors at the start + fat area
        # but because the reserved area is 0 based we have to decrease 1
        # then the next sector (+1) is the first reserved area sector
        start = reserved - 1 + num_fats * sectors_per_fat + 1

        root_dir_entries = self.get_number_of_rootdir_entries()
        bytes_per_sector = self.get_number_of_bytes_per_sector()
        if not bytes_per_sector:
            raise("Invalid data, possible divison by zero!")
        end = reserved - 1 + num_fats * sectors_per_fat + int(root_dir_entries * 32 / bytes_per_sector)
        return start, end

    def print_data(self):
        print(f"Number of bytes per sector: {self.get_number_of_bytes_per_sector()}")
        print(f"Number of sectors per cluster: {self.get_number_of_sectors_per_cluster()}")
        print(f"Number of reserved sectors: {self.get_number_of_reserved_sectors()}")
        print(f"Number of sectors in the filesystem: {self.get_total_fs_sectors()}")
        print(f"Media descriptor type: {self.get_media_descriptor_type()}")
        print(f"Number of sectors per track: {self.get_number_of_sectors_per_track()}")
        print(f"Number of heads: {self.get_number_of_heads()}")
        print(f"Number of hidden sectors: {self.get_number_of_hidden_sectors()}")

        print("FAT area:")
        print(f"Number of FATs: {self.get_number_of_fats()}")
        print(f"Number of sectors per FAT: {self.get_number_of_sectors_per_fat()}")
        start_fat_area = self.get_number_of_reserved_sectors()
        start_sector = start_fat_area
        for fat_num in range(0, self.get_number_of_fats()):
            print(f"\tFAT{fat_num + 1} sectors: {start_sector} - {start_sector + self.get_number_of_sectors_per_fat() - 1}")
            start_sector += self.get_number_of_sectors_per_fat()

        print("Root directory data:")
        print(f"\tNumber of Root directory entries: {self.get_number_of_rootdir_entries()}")
        print(f"\tSize of a Root directory entry: 32MB")
        try:
            start_root_dir, end_root_dir = self.get_root_dir_ranges()
        except:
            print("Exiting...")
            return 0
        print(f"\tStart sector of root dir (starting from the offset): {start_root_dir}")
        print(f"\tEnd sector of root dir(starting from the offset): {end_root_dir}")

