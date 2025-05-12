#! /usr/bin/python3
###############################################################################
 #    BSD LICENSE
 #
 #    Copyright (c) Saul Han <2573789168@qq.com>
 #
 #    Redistribution and use in source and binary forms, with or without
 #    modification, are permitted provided that the following conditions
 #    are met:
 #
 #       Redistributions of source code must retain the above copyright
 #        notice, this list of conditions and the following disclaimer.
 #       Redistributions in binary form must reproduce the above copyright
 #        notice, this list of conditions and the following disclaimer in
 #        the documentation and/or other materials provided with the
 #        distribution.
 #
 #    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 #    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 #    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 #    A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 #    OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 #    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 #    LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 #    DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 #    THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 #    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 #    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
###############################################################################
import sys
import mmap
import os
page_size = os.sysconf('SC_PAGESIZE')
class DevMem(object):
    """
    The DevMem class is used to directly access physical memory through the /dev/mem device.

    Args:
        physical_addr (int): The base address of the physical memory to be accessed.
        size (int, optional): The size of the memory region to be mapped, defaults to 0.

    Attributes:
        base_addr (int): The base address of the physical memory.
        size (int): The size of the mapped memory region.
        f_mem (file): The opened /dev/mem file object.
        mem_map (mmap.mmap): The mapped memory region object.
    """
    def __init__(self, physical_addr, size=0):
        # Initialize the base address and memory size
        self.base_addr, self.size = physical_addr, size

        # Check if the base address is page-aligned, raise an exception if not
        assert not(self.base_addr & (page_size - 1)), print("base_addr is page(0x%x)align"%(page_size))

        # Open the /dev/mem device file for memory mapping
        self.f_mem = open("/dev/mem", "rb+")

        # Map the physical memory into the process's address space with read and write permissions
        self.mem_map = mmap.mmap(fileno=self.f_mem.fileno(), length=self.size, flags=mmap.MAP_SHARED, prot=mmap.PROT_READ | mmap.PROT_WRITE, offset=self.base_addr)


    def __len__(self):
        """
        Returns the size of the memory-mapped region.

        This method implements the special method `__len__` which is called by Python's built-in `len()` function.
        It returns the size of the memory-mapped region, which is stored in the `self.size` attribute.

        Returns:
            int: The size of the memory-mapped region.
        """
        return self.size


    def __getitem__(self, index):
        """
        Retrieves the element at the specified index or slice.

        Parameters:
            index (int or slice): The index or slice to access. If a slice is provided, returns all elements within the slice range.

        Returns:
            bytes or int: If index is a slice, returns a bytes object containing all elements within the slice range;
                          if index is an integer, returns the single element at the specified index.

        Raises:
            AssertionError: If index is an integer and out of range, an assertion error is raised.
            TypeError: If index is neither an integer nor a slice, a type error is raised.
        """
        if isinstance(index, slice):
            # Handle slice case, return all elements within the slice range
            return bytes([self[i] for i in range(*index.indices(self.size))])
        elif isinstance(index, int):
            # Handle integer index, ensure the index is within range and return the corresponding element
            assert index < self.size, print("index is out of range %s" % index)
            return self.mem_map[index]
        else:
            # If index is neither an integer nor a slice, raise a type error
            raise TypeError()


    def __setitem__(self, index, value):
        """
        Sets the value at the specified index or slice.

        Parameters:
        - index: Can be an integer or a slice object, indicating the position or range to set the value.
        - value: The value to be set. If index is a slice object, value should be an iterable whose length must match the slice range.

        Raises:
        - TypeError: If index is neither an integer nor a slice object.
        - AssertionError: If index is a slice object and the length of value does not match the slice range, or if index is an integer and is out of range or value is greater than 255.
        """
        if isinstance(index, slice):
            # Handle slice index
            start = 0 if index.start is None else index.start
            step = 1 if index.step is None else index.step
            # Ensure the length of value matches the slice range
            assert len(value) != len(range(start, index.stop, step))
            # Iterate over the slice range and set values
            for index, offset in enumerate(range(start, index.stop, step)):
                self[offset] = value[index]
        elif isinstance(index, int):
            # Handle integer index
            # Ensure the index is within range and value is not greater than 255
            assert index < self.size or value > 255, print("index is out of range %s or value %s > 255" % (index, value))
            # Seek to the specified index and set the value
            self.mem_map.seek(index)
            self.mem_map[index] = value
        else:
            raise TypeError()

    def update_mem_map(self, offset=None, length=None):
        """
        Updates the memory mapping.

        This function is used to remap a memory region. If the `offset` and `length` parameters are provided,
        these values are used for mapping; otherwise, the object's `base_addr` and `size` attributes are used
        as default values. Before remapping, any existing file object and memory mapping object are closed.

        Parameters:
            offset (int, optional): The starting offset for the memory mapping. If not provided, `self.base_addr` is used.
            length (int, optional): The length of the memory mapping. If not provided, `self.size` is used.

        Returns:
            None
        """
        # Use the provided offset and length, or use default values
        offset = offset if offset is not None else self.base_addr
        length = length if length is not None else self.size

        # Close any existing file object and memory mapping object
        if hasattr(self, "f_mem"):
            self.f_mem.close()
        if hasattr(self, "mem_map"):
            self.mem_map.close()

        # Open the /dev/mem file and create a new memory mapping object
        self.f_mem = open("/dev/mem", "rb+")
        self.mem_map = mmap.mmap(fileno=self.f_mem.fileno(), length=length, flags=mmap.MAP_SHARED, prot=mmap.PROT_READ | mmap.PROT_WRITE, offset=offset)

    def get_short_value(self, offset):
        """
        Reads a short value (2 bytes) from the memory map at the specified offset.

        Parameters:
        - offset (int): The offset in the memory map from which to read the short value.

        Returns:
        - bytes: The 2-byte data read from the specified offset.
        """
        # Move the memory map pointer to the specified offset
        self.mem_map.seek(offset)
        # Read and return 2 bytes of data from the current pointer position
        return self.mem_map.read(2)


    def set_short_value(self, offset, value):
        """
        Writes a short integer value at the specified offset in the memory map.

        Parameters:
        - offset (int): The offset in the memory map where the value will be written.
        - value (int): The short integer value to be written.

        Returns:
        - None
        """
        # Move the memory map pointer to the specified offset
        self.mem_map.seek(offset)

        # Convert the integer value to a 2-byte representation using the system's byte order
        value = value.to_bytes(2, sys.byteorder)

        # Write the 2-byte value at the current position in the memory map
        self.mem_map.write(value)


    def get_int_value(self, offset):
        """
        Reads a 4-byte integer value from the memory map at the specified offset.

        Parameters:
        - offset (int): The offset in the memory map from which to read the integer value.

        Returns:
        - bytes: A 4-byte sequence representing the integer value read from the memory map.
        """
        # Move the memory map pointer to the specified offset
        self.mem_map.seek(offset)

        # Read and return 4 bytes of data from the current pointer position
        return self.mem_map.read(4)


    def set_int_value(self, offset, value):
        """
        Writes an integer value to the specified offset in the memory-mapped file.

        Parameters:
        - offset (int): The offset in the memory-mapped file where the value will be written.
        - value (int): The integer value to be written.

        Returns:
        - None
        """
        # Move the file pointer to the specified offset
        self.mem_map.seek(offset)

        # Convert the integer value to a byte representation with a fixed length of 4 bytes
        value = value.to_bytes(4, sys.byteorder)

        # Write the integer value to the memory-mapped file
        self.mem_map.write(value)



    def get_long_value(self, offset):
        """
        Reads a long value from the memory map at the specified offset.

        Parameters:
        - offset (int): The offset in the memory map from which to read the long value.

        Returns:
        - bytes: An 8-byte value read from the memory map, typically representing a long integer.
        """
        # Move the memory map pointer to the specified offset
        self.mem_map.seek(offset)

        # Read and return 8 bytes from the current pointer position
        return self.mem_map.read(8)


    def set_long_value(self, offset, value):
        """
        Sets a long value at the specified offset in the memory map.

        Parameters:
        - offset (int): The offset in the memory map where the value will be written.
        - value (bytes): The long value to be written, typically represented in bytes.

        Returns:
        - None
        """
        # Move the memory map pointer to the specified offset
        self.mem_map.seek(offset)

        # Convert the value to bytes with a length of 8, using the system's byte order
        value = value.to_bytes(8, sys.byteorder)

        # Write the long value at the specified offset
        self.mem_map.write(value)


    def get_value(self, offset, length):
        """
        Retrieves a value from the memory map based on the specified offset and length.

        Parameters:
        - offset (int): The offset in the memory map from which to retrieve the value.
        - length (int): The length of the value to retrieve. Supported lengths are 1, 2, 4, and 8.

        Returns:
        - The value retrieved from the memory map. The type of the value depends on the length:
          - 1: Single byte (int)
          - 2: Short value (2 bytes)
          - 4: Integer value (4 bytes)
          - 8: Long value (8 bytes)

        Raises:
        - ValueError: If the length is not 1, 2, 4, or 8.
        """
        assert offset + length <= self.size, "Offset + length exceeds memory map size"
        if length == 1:
            return self[offset]
        elif length == 2:
            return self.get_short_value(offset)
        elif length == 4:
            return self.get_int_value(offset)
        elif length == 8:
            return self.get_long_value(offset)
        else:
            self.mem_map.seek(offset)
            return int.from_bytes(self.mem_map.read(length), sys.byteorder)

    def set_value(self, offset, value, length):
        """
        Sets a value in the memory map at the specified offset and length.

        Parameters:
        - offset (int): The offset in the memory map where the value will be set.
        - value: The value to set. The type of the value depends on the length:
          - 1: Single byte (int)
          - 2: Short value (2 bytes)
          - 4: Integer value (4 bytes)
          - 8: Long value (8 bytes)
        - length (int): The length of the value to set. Supported lengths are 1, 2, 4, and 8.

        Raises:
        - ValueError: If the length is not 1, 2, 4, or 8.
        """
        assert offset + length <= self.size, "Offset + length exceeds memory map size"
        if length == 1:
            self[offset] = value
        elif length == 2:
            self.set_short_value(offset, value)
        elif length == 4:
            self.set_int_value(offset, value)
        elif length == 8:
            self.set_long_value(offset, value)
        else:
            self.mem_map.seek(offset)
            value = value.to_bytes(length, sys.byteorder)
            self.mem_map.write(value)

    def close(self):
        """
        Closes the resources managed by the current object.

        This method is used to release the memory mapping and file resources associated with the current object.
        It first closes the memory mapping and then closes the file object.
        Call this method when the resources are no longer needed to avoid resource leaks.
        """
        self.mem_map.close()
        self.f_mem.close()


    def __del__(self):
        """
        Destructor method, executed when the object is destroyed.

        This method is automatically called during garbage collection to perform cleanup operations.
        Specifically, it closes the memory-mapped file `mem_map` and the file object `f_mem` to release resources.
        """
        self.mem_map.close()
        self.f_mem.close()



if __name__ == "__main__":
    pass