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
import os
import re
import json
import ctypes
import sys
from ctypes import *
from collections import OrderedDict

STRUCT_INCREASE  = 0x7FFFFFFFFFFFFFFF
STRUCT_DECREASE  = -0x7FFFFFFFFFFFFFFF
STRUCT_CHANGE    = 0xFFFFFFFFFFFFFFFF
STRUCT_EQUAL     = 0
STRUCT_NOTCHECK = None
compare_dict = {STRUCT_INCREASE:"increase", STRUCT_DECREASE:"decrease", STRUCT_CHANGE:"change", STRUCT_EQUAL:"equal", STRUCT_NOTCHECK:"no check"}
XT_STRUCT_FIRST_INST = 0
XT_STRUCT_LAST_INST = 1

def encode_dump(data, offset=0, length=None, unit=1, log_info=print, line_length=32):
    """
    Encodes binary data according to a specified format and outputs it.

    Args:
        data: The binary data to be encoded.
        offset: The starting offset of the data, default is 0.
        length: The length of the data to be encoded. If None, encodes from the offset to the end of the data.
        unit: The size of each data unit, used to determine the number of bytes per group, default is 1.
        log_info: The function used to output the log, default is print.
        line_length: The number of data groups to display per line, default is 32.

    Returns:
        No return value, the encoded data is output through log_info.
    """
    # Check input parameters
    if not callable(log_info):
        raise ValueError("log_info must be a callable function")
    if not isinstance(unit, int) or unit <= 0:
        raise ValueError("unit must be a positive integer")
    if offset < 0 or offset >= len(data):
        raise ValueError("offset is out of bounds")
    if length is not None and length < 0:
        raise ValueError("length must be non-negative")
    # Calculate the actual length of data to be encoded
    length = len(data) - offset if length is None else min(length, len(data) - offset)

    # If the unit size is not 1 and not a list, recombine the data according to the unit size
    if unit != 1:
        _data = []
        for index in range(offset, offset + length, unit):
            value = 0
            for sub_index in range(unit):
                value = value << 8 | data[sub_index + index]
            _data.append(value)
        data = _data

    # Update the data length to ensure it does not exceed the actual length of the data
    length = length if length < len(data) else len(data)

    # Generate and output the header, including data indices and addresses
    line_str = " " * 11
    for i in range(line_length):
        line_str = line_str + ("{:^%sx}" % (2 * unit + 1)).format(i)
    log_info(line_str)
    log_info(" " * 12 + "-" * (line_length * (2 * unit + 1) - 1))

    # Initialize the address string and index
    line_str, i = "0x%08x: "%offset, 0

    # Iterate over the data, encode it according to the specified format, and output it
    while length > 0:
        if 0 == i % line_length and i: # print address
            log_info(line_str)
            # begin print new line
            line_str = "0x%08x: " % (offset)
        line_str = line_str + ("{:0%sx} "%(2 * unit)).format(data[i])
        length, i, offset = length - 1, i + 1, offset + unit
    else:
        if i % line_length:
            log_info(line_str)


class Pointer(object):
    """
    The Pointer class is used to manage the length information of a pointer and provides functionality to retrieve the length and check for changes.

    Attributes:
        elem_type: The type of the element that the pointer points to.
        length_field: The field or value used to determine the length of the pointer. It can be an integer, an instance attribute, or an expression.
        last_pointer_length: The length of the pointer from the previous retrieval.
        current_pointer_length: The current length of the pointer.
    """

    def __init__(self, elem_type, length_field):
        """
        Initializes an instance of the Pointer class.

        Args:
            elem_type: The type of the element that the pointer points to.
            length_field: The field or value used to determine the length of the pointer. It can be an integer, an instance attribute, or an expression.
        """
        self.elem_type = elem_type
        self.length_field = length_field
        self.last_pointer_length = None
        self.current_pointer_length = None

    def get_length(self, instance):
        """
        Retrieves the length of the pointer.

        Depending on the type of `length_field`, it retrieves or calculates the length of the pointer from the instance and updates `last_pointer_length` and `current_pointer_length`.

        Args:
            instance: The instance object that contains the `length_field`.

        Returns:
            int: The length of the pointer.

        Raises:
            AttributeError: If the `length_field` cannot be found in the instance or if the evaluation fails.
        """
        if isinstance(self.length_field, int):
            # If `length_field` is an integer, use it directly as the length
            self.last_pointer_length = self.length_field
            self.current_pointer_length = self.length_field
            return self.length_field
        elif hasattr(instance, self.length_field):
            # If `length_field` is an attribute of the instance, retrieve its value as the length
            self.last_pointer_length = self.current_pointer_length
            self.current_pointer_length = getattr(instance, self.length_field)
            return getattr(instance, self.length_field)
        else:
            try:
                # Attempt to evaluate `length_field` as an expression and ensure the result is positive
                length = eval(self.length_field)
                assert length > 0, "length_field must be greater than 0"
                self.last_pointer_length = self.current_pointer_length
                self.current_pointer_length = length
                return length
            except AttributeError:
                # If `length_field` cannot be found or evaluated, raise an exception
                raise AttributeError(f"{self.length_field} not found")

    def pointer_change_check(self,):
        """
        Checks if the pointer length has changed.

        Returns:
            bool: Returns True if `last_pointer_length` is different from `current_pointer_length`, otherwise returns False.
        """
        return self.last_pointer_length != self.current_pointer_length


class PointerMeta(type(Structure)):
    """
    A metaclass for handling `Pointer` type fields in ctypes structures.

    This metaclass processes the `_fields_` attribute of a class, converting `Pointer`-type fields
    into ctypes pointer fields. It also generates property accessors for these pointer fields,
    allowing for easy access to the underlying data.

    Args:
        cls (type): The metaclass instance.
        name (str): The name of the new class.
        bases (tuple): The base classes of the new class.
        namespace (dict): The namespace containing the class attributes.

    Returns:
        type: The newly created class with processed `Pointer` fields and generated properties.
    """
    def __new__(cls, name, bases, namespace):
        fields = []
        length_pointers = []

        # Process each field in `_fields_`, converting Pointer-type fields to ctypes pointer fields
        for item in namespace.get('_fields_', []):
            if isinstance(item[1], Pointer):
                ptr_field = f'{item[0]}_ptr'
                fields.append((ptr_field, POINTER(item[1].elem_type)))
                length_pointers.append((item[0], item[1], ptr_field))
            else:
                fields.append(item)
        namespace['_fields_'] = fields

        # Create the new class object
        new_cls = super().__new__(cls, name, bases, namespace)

        # Generate property accessors for each Pointer field
        for key, lp, ptr_field in length_pointers:
            def make_pointer_property(lp, ptr_field):
                """
                Creates a property for accessing the data pointed to by a `Pointer` field.

                Args:
                    lp (Pointer): The `Pointer` instance containing metadata about the field.
                    ptr_field (str): The name of the pointer field in the structure.

                Returns:
                    property: A property that allows getting and setting the data pointed to by the pointer.
                """
                def getter(instance):
                    length = int(lp.length_field) if isinstance(lp.length_field, int) else getattr(instance, lp.length_field)
                    length = lp.get_length(instance)
                    ptr = getattr(instance, ptr_field)
                    array_type = lp.elem_type * length
                    return array_type.from_address(ctypes.addressof(ptr.contents))
                def setter(instance, value):
                    expected_type = lp.elem_type
                    if isinstance(value, ctypes.Array):
                        actual_elem_type = value._type_
                        if actual_elem_type != expected_type and actual_elem_type._type_ != expected_type:
                            raise TypeError(f"Array element type mismatch: {actual_elem_type} vs {expected_type}")
                        ptr = cast(value, POINTER(expected_type))
                    elif isinstance(value, ctypes._Pointer):
                        ptr_type = value._type_
                        if ptr_type != expected_type and ptr_type._type_ != expected_type:
                            raise TypeError(f"Pointer element type mismatch: {ptr_type} vs {expected_type}")
                        ptr = cast(value, POINTER(expected_type))
                    else:
                        raise TypeError("Expected ctypes array or pointer")
                    setattr(instance, ptr_field, ptr)
                return property(getter, setter)
            setattr(new_cls, key, make_pointer_property(lp, ptr_field))

            def make_pointer_address_property(ptr_field):
                """
                Creates a property for accessing the address of a pointer field.

                Args:
                    ptr_field (str): The name of the pointer field in the structure.

                Returns:
                    property: A property that returns the address of the pointer.
                """
                def getter(instance):
                    ptr = getattr(instance, ptr_field)
                    if ptr is None:
                        return 0
                    ptr_address = cast(ptr, c_void_p).value
                    return ptr_address
                return property(getter)
            setattr(new_cls, f'{ptr_field}_addr', make_pointer_address_property(ptr_field))

            def make_pointer_length_property(lp):
                """
                Creates a property for accessing the length of a pointer field.

                Args:
                    lp (Pointer): The `Pointer` instance containing metadata about the field.

                Returns:
                    property: A property that returns the length of the pointer.
                """
                def getter(instance):
                    return lp.get_length(instance)
                return property(getter)
            setattr(new_cls, f'{ptr_field}_length', make_pointer_length_property(lp))

            def make_pointer_inst_property(lp):
                """
                Creates a property for accessing the `Pointer` instance itself.

                Args:
                    lp (Pointer): The `Pointer` instance containing metadata about the field.

                Returns:
                    property: A property that returns the `Pointer` instance.
                """
                def getter(instance):
                    return lp
                return property(getter)
            setattr(new_cls, f'{ptr_field}_inst', make_pointer_inst_property(lp))

        return new_cls




class StructureBase(Structure, metaclass=PointerMeta):
    """
    StructureBase is a base class for defining structured data with specific byte alignment and fields.
    It inherits from `Structure` and uses `PointerMeta` as its metaclass.

    Attributes:
        _pack_ (int): Specifies the byte alignment of the structure as 1 byte.
        _fields_ (list): Defines the list of fields in the structure, initially empty.
    """

    _pack_ = 1  # Specifies the byte alignment of the structure as 1 byte
    _fields_ = []  # Defines the list of fields in the structure, initially empty

    def __init__(self, byteorder='little', log_info=print):
        """
        Initializes the StructureBase instance.

        Args:
            byteorder (str, optional): Specifies the byte order for the structure. Defaults to 'little'. If not provided, it uses the system's byte order.
            log_info (function, optional): Specifies the logging function. Defaults to the built-in `print` function.
        """
        super(StructureBase, self).__init__()
        # Initialize various attributes used for storing different types of information
        self.info_header = None  # Used to store the information header
        self.diff_header = None  # Used to store the difference header
        self.union_dict_match = None  # Used to store union dictionary matches
        self.format_dict = {}  # Used to store formatting dictionaries
        self.byteorder = byteorder if byteorder else sys.byteorder  # Sets the byte order, defaults to system byte order
        self.log_info = log_info  # Sets the logging function
        self._raw_data = None  # Used to store raw data
        self._last_inst = None  # Used to store the last instance
        self._first_inst = None  # Used to store the first instance
        self.pointer_field_map = None  # Used to map pointer fields
        self.fields_offset_size_map = None  # Used to map fields to their offsets and sizes
        self.multi_level_max_name_map = None  # Used to map multi-level maximum names
        self.multi_level_max_name_list = None  # Used to store a list of multi-level maximum names
        self.skip_reserved_pattern = re.compile(r'reserved|rsvd')

    def get_max_size_union_struct(self, union_ctype_obj, field_path=None, union_dict_match=None):
        """
        Retrieves the field with the maximum size from a given ctypes Union object.

        This function iterates through all fields of the Union object and returns the field
        that occupies the largest memory size. If a specific field path is provided and matches
        a field in the Union, that field is returned directly.

        Parameters:
        - union_ctype_obj (ctypes.Union): The ctypes Union object to analyze.
        - field_path (str, optional): A specific field path to retrieve directly. Defaults to None.
        - union_dict_match (dict, optional): A dictionary mapping field paths to field names. Defaults to None.

        Returns:
        - max_union_obj (ctypes._CData): The field object with the maximum size in the Union.

        Raises:
        - AssertionError: If the input `union_ctype_obj` is not a valid ctypes Union object.
        """
        # Assert to ensure the input is a valid ctypes Union object
        assert isinstance(union_ctype_obj, ctypes.Union), print("get a invalid union type %s" % union_ctype_obj)

        # If a union_dict_match is provided, attempt to retrieve the field path
        if union_dict_match:
            field_path = union_dict_match.get(field_path, None) if field_path else None
            if field_path:
                return getattr(union_ctype_obj, field_path)

        # Initialize max_union_obj with the first field in the Union
        max_union_obj = getattr(union_ctype_obj, union_ctype_obj._fields_[0][0])

        # Iterate through all fields in the Union to find the one with the maximum size
        for union_filed in union_ctype_obj._fields_:
            cur_obj = getattr(union_ctype_obj, union_filed[0])
            # Compare and update max_union_obj if a larger field is found
            if sizeof(max_union_obj) < sizeof(cur_obj):
                max_union_obj = cur_obj
            elif sizeof(max_union_obj) == sizeof(cur_obj):
                # If sizes are equal and max_union_obj is not a Structure, update to cur_obj
                if not isinstance(max_union_obj, ctypes.Structure):
                    max_union_obj = cur_obj

        # Return the field object with the maximum size
        return max_union_obj


    def pointer_check(self, ctype_obj=None, field=None):
        """
        Checks if the specified field represents a pointer type.

        This function verifies whether the given field has the characteristics of a pointer type.
        Typically, a pointer field ends with '_ptr' and has associated attributes '_inst', '_addr', and '_length'.

        Args:
            ctype_obj (object, optional): The object to check. If not provided, the instance itself is used.
            field (str): The name of the field to check.

        Returns:
            bool: True if the field represents a pointer type, otherwise False.
        """
        # Use the provided ctype_obj or default to self
        ctype_obj = ctype_obj if ctype_obj else self

        # Check if the field ends with '_ptr' and has the required attributes
        if field.endswith('_ptr') and hasattr(ctype_obj, f'{field}_inst') and hasattr(ctype_obj, f'{field}_addr') and hasattr(ctype_obj, f'{field}_length'):
            return True
        else:
            return False


    def field_trav_return(self, trav_ret, fields_map, fields_name, fields_list_map, return_list=False, return_dict=True, transform_tuple=True, struct=False, struct_list=False,):
        """
        Processes and returns traversal results based on the specified parameters, determining the format and structure of the returned values.

        Args:
            trav_ret: The traversal result, typically a list or tuple.
            fields_map: A dictionary used to store field mappings.
            fields_name: The field name, used as the key in `fields_map`.
            fields_list_map: A list used to store field lists.
            return_list: Whether to return the result in list format. Defaults to False.
            return_dict: Whether to return the result in dictionary format. Defaults to True.
            transform_tuple: Whether to transform the result into tuple format. Defaults to True.
            struct: Whether the result is structured data. Defaults to False.
            struct_list: Whether the result is a structured list. Defaults to False.

        Returns:
            No return value. The results are directly stored in `fields_map` and `fields_list_map`.
        """
        # Store `trav_ret` in `fields_map` based on `return_dict` and `return_list` parameters
        if return_dict and return_list:
            fields_map[fields_name] = [item[0] for item in trav_ret] if struct_list else trav_ret[0] if struct else trav_ret
        else:
            fields_map[fields_name] = trav_ret

        # If `return_list` is True, process and store `trav_ret` in `fields_list_map`
        if return_list:
            if return_dict:
                fields_value = [item[1] for item in trav_ret] if struct_list else trav_ret[1] if struct else trav_ret
            else:
                fields_value = [item for item in trav_ret] if struct_list else trav_ret

            # Store `fields_value` in `fields_list_map` based on `struct_list` and `struct` parameters
            if struct_list:
                if transform_tuple:
                    fields_list_map.append(tuple([tuple(item) for item in fields_value]))
                else:
                    fields_list_map += fields_value
            else:
                if struct:
                    if transform_tuple:
                        fields_list_map.append(tuple(fields_value))
                    else:
                        fields_list_map += [fields_value, ]
                else:
                    fields_list_map.append(trav_ret)

    def fields_traversal(self, ctype_obj=None, cb_func=None, cb_kwargs=None, field_kwargs=None, skip_null=True, field_path=False, return_list=False,
                         return_dict=True, struct_set=False):
        """
        Traverses and processes the fields of a given ctypes object (e.g., Structure or Union).

        Args:
            ctype_obj (ctypes.Structure/ctypes.Union, optional): The ctypes object to traverse. If not provided, `self` is used.
            cb_func (callable, optional): A callback function to process each field. If not provided, only traversal is performed.
            cb_kwargs (dict, optional): Additional arguments to pass to the callback function.
            field_kwargs (dict/list/tuple, optional): Specific arguments for each field. Can be a dictionary, list, or tuple.
            skip_null (bool, optional): Whether to skip null pointer fields. Defaults to True.
            field_path (bool/str, optional): Whether to generate field paths. If a string, it is used as the base path. Defaults to False.
            return_list (bool, optional): Whether to return a list of field values. Defaults to False.
            return_dict (bool, optional): Whether to return a dictionary of field values. Defaults to True.
            struct_set (bool, optional): Whether to set structure fields during traversal. Defaults to False.

        Returns:
            Depending on `return_list` and `return_dict`, returns a dictionary, list, or both of field values.
        """
        ctype_obj = ctype_obj if ctype_obj else self
        fields_map, fields_list_map, null_ptr_cnt = {}, [], 0
        transform_tuple = cb_kwargs.get("transform_tuple", None) if cb_kwargs else None
        base_field = field_path if isinstance(field_path, str) else "" if field_path else None

        # Handle array index in field path
        if base_field and cb_kwargs and cb_kwargs.get(field_path, None) and cb_kwargs[field_path].get("arr_index", None) is not None:
            arr_index = cb_kwargs[field_path]["arr_index"]
            base_field = base_field + f"[{arr_index}]"

        # Traverse each field in the ctype object
        for field_index, field in enumerate(ctype_obj._fields_):
            # Get field-specific arguments
            if field_kwargs:
                if isinstance(field_kwargs, dict):
                    _field_kwargs = field_kwargs.get(field[0], None)
                elif isinstance(field_kwargs, list) or isinstance(field_kwargs, tuple):
                    _field_kwargs = field_kwargs[field_index-null_ptr_cnt] if (field_index - null_ptr_cnt) < len(field_kwargs) else None
            else:
                _field_kwargs = None

            # Generate field path
            field_path = False if not field_path else f"{base_field}.{field[0]}" if base_field else field[0]
            field_ctype_obj = getattr(ctype_obj, field[0])

            # If field path is in cb_func_dict, use the specified callback function
            if field_path and isinstance(cb_kwargs, dict) and cb_kwargs.get('cb_func_dict', None) and cb_kwargs['cb_func_dict'].get(field_path, None):
                field_cb_info = cb_kwargs['cb_func_dict'][field_path]
                if len(field_cb_info) > 2:
                    if callable(field_cb_info[0]):
                        fields_map[field[0]] = field_cb_info[0](ctype_obj, field_ctype_obj, field_path, _field_kwargs, *field_cb_info[1:])
                    else:
                        fields_map[field[0]] = field_cb_info
                elif callable(field_cb_info):
                    fields_map[field[0]] = field_cb_info(ctype_obj, field_ctype_obj, field_path, _field_kwargs)
                else:
                    fields_map[field[0]] = field_cb_info
                fields_list_map += [fields_map[field[0]],]
                continue

            # Handle pointer fields
            if self.pointer_check(ctype_obj, field[0]):
                length, address, pointer_inst = getattr(ctype_obj, f'{field[0]}_length'), getattr(ctype_obj, f'{field[0]}_addr'), getattr(ctype_obj, f'{field[0]}_inst')
                if struct_set:
                    if pointer_inst.pointer_change_check() and length:
                        elems = (pointer_inst.elem_type() * length)()
                        setattr(ctype_obj, field[0], elems)
                        address = getattr(ctype_obj, f'{field[0]}_addr')
                    if length == 0:
                        null_ptr_cnt = null_ptr_cnt if _field_kwargs and "NULL" in _field_kwargs else null_ptr_cnt + 1
                        continue
                if not (address and length):
                    elem, length = pointer_inst.elem_type() if not skip_null else None, 0
                else:
                    field_ctype_obj, elem = getattr(ctype_obj, field[0]), field_ctype_obj[0]

                # Handle pointer fields that are structures or unions
                if isinstance(elem, Structure) or isinstance(elem, ctypes.Union):
                    if field_path:
                        if cb_kwargs and cb_kwargs.get(field_path, None):
                            cb_kwargs[field_path] = cb_kwargs[field_path] if cb_kwargs and isinstance(cb_kwargs[field_path], dict) else {"arr_index": None}
                        else:
                            if cb_kwargs:
                                cb_kwargs[field_path] = {"arr_index": None}
                            else:
                                cb_kwargs = {field_path: {"arr_index": None}}
                    pointer_list = []
                    for index in range(length):
                        elem = self.get_max_size_union_struct(field_ctype_obj[index]) if isinstance(field_ctype_obj[0], ctypes.Union) else field_ctype_obj[index]
                        if field_path: cb_kwargs[field_path]['arr_index'] = index
                        sub_field_kwargs = _field_kwargs[index] if isinstance(_field_kwargs, list) else _field_kwargs
                        pointer_list.append(self.fields_traversal(elem, cb_func, cb_kwargs, sub_field_kwargs, skip_null, field_path, return_list, return_dict, struct_set))
                    if length == 0 and elem is not None:
                        trav_ret = self.fields_traversal(elem, cb_func, cb_kwargs, _field_kwargs, skip_null, field_path, return_list, return_dict, struct_set)
                        self.field_trav_return(trav_ret, fields_map, field[0], fields_list_map, return_list, return_dict, transform_tuple, struct=True)
                    else:
                        self.field_trav_return(pointer_list, fields_map, field[0], fields_list_map, return_list, return_dict, transform_tuple, struct_list=True)
                else:
                    if cb_func and callable(cb_func):
                        _field = field_path if field_path else field[0]
                        if address:
                            trav_ret = cb_func(ctype_obj, field_ctype_obj, _field, cb_kwargs, _field_kwargs)
                            self.field_trav_return(trav_ret, fields_map, field[0], fields_list_map, return_list, return_dict, transform_tuple)
                        else:
                            if not skip_null:
                                self.field_trav_return("NULL", fields_map, field[0], fields_list_map, return_list, return_dict, transform_tuple)
                            else:
                                null_ptr_cnt += 1
                if field_path and ((self.pointer_field_map is None) or (field_path not in self.pointer_field_map)):
                    if self.pointer_field_map is None: self.pointer_field_map = OrderedDict()
                    field_path_list = [item.split("[")[0] for item in field_path.split(".")]
                    multi_level_pointer_map = [".".join(field_path_list[0:index+1]) for index in range(len(field_path_list))]
                    self.pointer_field_map[field_path] = (getattr(ctype_obj,  f'{field[0]}_inst'), multi_level_pointer_map)
            else:
                # Handle non-pointer fields
                if isinstance(field_ctype_obj, Structure) or isinstance(field_ctype_obj, ctypes.Union):
                    if isinstance(field_ctype_obj, ctypes.Union):
                        if field_path and isinstance(cb_kwargs, dict) and cb_kwargs.get('union_dict_match', None) and cb_kwargs['union_dict_match'].get(field_path, None):
                            full_field_path = ".".join([item.split("[")[0] for item in field_path.split(".")])
                            field_ctype_obj = getattr(field_ctype_obj, cb_kwargs['union_dict_match'].get(full_field_path))
                        else:
                            field_ctype_obj = self.get_max_size_union_struct(field_ctype_obj)
                    trav_ret = self.fields_traversal(field_ctype_obj, cb_func, cb_kwargs, _field_kwargs, skip_null, field_path, return_list, return_dict, struct_set)
                    self.field_trav_return(trav_ret, fields_map, field[0], fields_list_map, return_list, return_dict, transform_tuple, struct=True)
                elif isinstance(field_ctype_obj, ctypes.Array):
                    assert not isinstance(field_ctype_obj._type_, ctypes.Array), print("fields traversal not supported for multi-level Array")
                    if isinstance(field_ctype_obj[0], Structure) or isinstance(field_ctype_obj[0], ctypes.Union):
                        if field_path:
                            if cb_kwargs and cb_kwargs.get(field_path, None):
                                cb_kwargs[field_path] = cb_kwargs[field_path] if cb_kwargs and isinstance(cb_kwargs[field_path], dict) else {"arr_index": None}
                            else:
                                if cb_kwargs:
                                    cb_kwargs[field_path] = {"arr_index": None}
                                else:
                                    cb_kwargs = {field_path: {"arr_index": None}}
                        struct_list = []
                        for index, elem in enumerate(field_ctype_obj):
                            elem_ctype_obj = self.get_max_size_union_struct(field_ctype_obj[index]) if isinstance(field_ctype_obj[0], ctypes.Union) else field_ctype_obj[index]
                            if field_path: cb_kwargs[field_path]['arr_index'] = index
                            sub_field_kwargs = _field_kwargs[index] if _field_kwargs and isinstance(_field_kwargs, list) or isinstance(_field_kwargs, tuple) else _field_kwargs
                            struct_list.append(self.fields_traversal(elem_ctype_obj, cb_func, cb_kwargs, sub_field_kwargs, skip_null, field_path, return_list, return_dict,
                                                                     struct_set))
                        self.field_trav_return(struct_list, fields_map, field[0], fields_list_map, return_list, return_dict, transform_tuple, struct_list=True)
                    else:
                        if cb_func and callable(cb_func):
                            _field = field_path if field_path else field[0]
                            trav_ret = cb_func(ctype_obj, field_ctype_obj, _field, cb_kwargs, _field_kwargs)
                            self.field_trav_return(trav_ret, fields_map, field[0], fields_list_map, return_list, return_dict, transform_tuple)
                else:
                    if cb_func and callable(cb_func):
                        _field = field_path if field_path else field[0]
                        trav_ret = cb_func(ctype_obj, field_ctype_obj, _field, cb_kwargs, _field_kwargs)
                        self.field_trav_return(trav_ret, fields_map, field[0], fields_list_map, return_list, return_dict, transform_tuple)
        return (fields_map, fields_list_map) if return_dict and return_list else fields_list_map if return_list else fields_map

    def get_multi_level_max_name_map(self, ctype_obj=None):
        """
        Generates a multi-level maximum name map for the given ctype object.

        This function traverses the fields of the ctype object and calculates the maximum length of field names at each level.
        The results are stored in `self.multi_level_max_name_list` and `self.multi_level_max_name_map`.

        Parameters:
            ctype_obj (object, optional): The ctype object to traverse. If not provided, `self` is used.

        Returns:
            None
        """

        def cb_func(ctype_obj, field_ctype_obj, field_name, cb_kwargs, field_kwargs):
            """
            Callback function to return the field name during traversal.

            Parameters:
                ctype_obj (object): The parent ctype object.
                field_ctype_obj (object): The current field object.
                field_name (str): The name of the current field.
                cb_kwargs (dict): Additional callback arguments (not used here).
                field_kwargs (dict): Additional field arguments (not used here).

            Returns:
                str: The field name.
            """
            return field_name

        def get_multi_level_max_name_list(ctype_dict=None):
            """
            Recursively calculates the maximum length of field names at each level.

            This function traverses the ctype dictionary and updates `self.multi_level_max_name_list` with the maximum length of field names at each level.

            Parameters:
                ctype_dict (dict, optional): The ctype dictionary to traverse. If not provided, `self.multi_level_max_name_map` is used.

            Returns:
                None
            """
            ctype_dict = ctype_dict if ctype_dict else self.multi_level_max_name_map
            if isinstance(ctype_dict, dict):
                for key in ctype_dict:
                    if isinstance(ctype_dict[key], dict):
                        # Recursively process nested dictionaries
                        get_multi_level_max_name_list(ctype_dict[key])
                    elif isinstance(ctype_dict[key], list):
                        # Recursively process lists
                        get_multi_level_max_name_list(ctype_dict[key][0])
                    else:
                        # Calculate the level and length of the field name
                        level, level_length = len(ctype_dict[key].split('.')), len(ctype_dict[key])
                        if not self.multi_level_max_name_list:
                            # Initialize the list if it doesn't exist
                            self.multi_level_max_name_list = [0] * level
                            self.multi_level_max_name_list[level - 1] = level_length + level * 4
                        else:
                            if level > len(self.multi_level_max_name_list):
                                # Extend the list if the current level exceeds its length
                                self.multi_level_max_name_list = self.multi_level_max_name_list + [0] * (level - len(self.multi_level_max_name_list))
                            # Update the maximum length for the current level
                            self.multi_level_max_name_list[level - 1] = max(self.multi_level_max_name_list[level - 1], level_length + level * 4)
                        # Update the maximum length for the first level
                        self.multi_level_max_name_list[0] = max(self.multi_level_max_name_list[0], len(ctype_dict[key].split('.')[-1]) + (level - 1) * 6)
            elif isinstance(ctype_dict, list):
                # Recursively process lists
                get_multi_level_max_name_list(ctype_dict[0])

        # Initialize the multi-level maximum name map if it hasn't been initialized yet
        if self.multi_level_max_name_map is None:
            ctype_obj = ctype_obj if ctype_obj else self
            # Traverse the fields of the ctype object and generate the multi-level maximum name map
            self.multi_level_max_name_map = self.fields_traversal(ctype_obj, cb_func, None, None, False, True)
            # Calculate the maximum length of field names at each level
            get_multi_level_max_name_list(self.multi_level_max_name_map)
            # Generate the fields offset and size map
            self.fields_offset_size_map = self.get_fields_offset_size_map()

    def pointer_path_check(self, field_path):
        """
        Checks if the given field path exists in the multi-level pointer map.

        This function iterates through the `pointer_field_map` to determine if the specified `field_path`
        is present in any of the multi-level pointer maps. If found, it returns `True`; otherwise, it returns `False`.

        Args:
            field_path (str): The field path to check in the multi-level pointer map.

        Returns:
            bool: `True` if the field path exists in the multi-level pointer map, otherwise `False`.
        """
        for key in self.pointer_field_map:
            multi_level_pointer_map = self.pointer_field_map[key][1]
            if field_path in multi_level_pointer_map:
                return True
        return False

    def struct_zero_check(self, ctype_obj=None):
        """
        Checks if the given ctype object is filled with zero values.

        This function compares the memory content of the provided ctype object with a zero-filled byte array of the same size.
        If the memory content matches the zero-filled array, it returns True; otherwise, it returns False.

        Args:
            ctype_obj (ctypes object, optional): The ctype object to check. If not provided, the instance itself is used.

        Returns:
            bool: True if the ctype object is filled with zero values, otherwise False.
        """
        # If no ctype object is provided, use the instance itself
        ctype_obj = ctype_obj if ctype_obj else self

        # Get the size of the ctype object
        size = sizeof(ctype_obj)

        # Compare the memory content of the ctype object with a zero-filled byte array of the same size
        return string_at(addressof(ctype_obj), size) == bytes(size)


    def get_pointer_info_by_field(self, ctype_obj, field_name):
        """
        Retrieves the pointer information for a specific field in a given ctype object.

        This function checks if the specified field represents a pointer (either by ending with '_ptr' or having a corresponding pointer field).
        If the field is a pointer, it returns the pointer instance, address, and length. If the field is not a pointer, it returns None.

        Args:
            ctype_obj: The ctype object containing the field. If None, the instance itself is used.
            field_name (str): The name of the field to check.

        Returns:
            tuple: A tuple containing the pointer instance, address, and length if the field is a pointer; otherwise, returns None.
        """
        # Use the provided ctype_obj or default to self
        ctype_obj = ctype_obj if ctype_obj else self

        # Check if the field name ends with '_ptr' or has a corresponding pointer field
        if field_name.endswith('_ptr') or hasattr(ctype_obj, f'{field_name}_ptr'):
            # Normalize the field name to ensure it ends with '_ptr'
            field_name = field_name if field_name.endswith('_ptr') else f'{field_name}_ptr'

            # Verify if the field is a valid pointer
            if self.pointer_check(ctype_obj, field_name):
                # Retrieve the pointer instance, address, and length
                pointer_inst = getattr(ctype_obj,  f'{field_name}_inst')
                address = getattr(ctype_obj, f'{field_name}_addr')
                length = getattr(ctype_obj, f'{field_name}_length')
                return pointer_inst, address, length

        # Return None if the field is not a pointer
        return None

    def pointer_init(self, ctype_obj, decode_raw_data=None, field_path="", field_offset_size_map=None):
        """
        Initializes or decodes pointer fields within a ctypes object.

        This function handles the initialization or decoding of pointer fields within a ctypes object,
        including nested structures, unions, and arrays. It supports both reading from memory and
        decoding from raw data.

        Parameters:
            ctype_obj (ctypes.Structure/ctypes.Union): The ctypes object containing the pointer fields.
            decode_raw_data (bytearray, optional): Raw data to decode into the ctypes object. If None, data is read from memory.
            field_path (str, optional): The path of the current field, used for nested structures. Defaults to an empty string.
            field_offset_size_map (dict, optional): A mapping of field paths to their offsets and sizes.If None, the function uses the object's internal map.

        Returns:
            bytearray or int: If `decode_raw_data` is None, returns the raw data read from memory. Otherwise, returns the offset after decoding the data.
        """
        raw_data, raw_offset, base_field, bits_field_path_start = bytearray(), 0, field_path, None

        # Handle union types
        if isinstance(ctype_obj, ctypes.Union):
            ctype_obj = self.get_max_size_union_struct(ctype_obj)
            if isinstance(ctype_obj, ctypes.Union) or isinstance(ctype_obj, Structure):
                # Recursively handle nested unions or structures
                if decode_raw_data is None:
                    return self.pointer_init(ctype_obj, None, field_path, field_offset_size_map)
                else:
                    return self.pointer_init(ctype_obj, decode_raw_data[raw_offset:], field_path, field_offset_size_map)
            else:
                # Check for unsupported union structures containing pointers
                for key in self.pointer_field_map:
                    multi_level_pointer_map = self.pointer_field_map[key][1]
                    assert field_path != multi_level_pointer_map[-2], print("Does not support union struct directly containing pointers")

                # Handle union data
                field_size = sizeof(ctype_obj)
                if decode_raw_data is None:
                    return bytearray(string_at(addressof(ctype_obj), sizeof(ctype_obj)))
                else:
                    memmove(addressof(ctype_obj), decode_raw_data[raw_offset:raw_offset + field_size], field_size)
                    return raw_offset + field_size
        else:
            # Handle structure types
            for field_index, field in enumerate(ctype_obj._fields_):
                field_path = f"{base_field}.{field[0]}" if base_field else field[0]
                if len(field) == 3:
                    # Handle bit fields
                    bits_field_path_start = bits_field_path_start if bits_field_path_start else field_path
                    continue
                else:
                    if bits_field_path_start:
                        # Handle bit field data
                        offset = field_offset_size_map[bits_field_path_start][0] // 8
                        bits_field_path_end = f"{base_field}.{ctype_obj._fields_[field_index - 1][0]}"
                        bits_size = field_offset_size_map[bits_field_path_end][0] // 8 - offset
                        if decode_raw_data is None:
                            raw_data = raw_data + bytearray(string_at(addressof(ctype_obj) + offset, bits_size))
                        else:
                            memmove(addressof(ctype_obj) + offset, decode_raw_data[raw_offset:raw_offset + bits_size], bits_size)
                            raw_offset += bits_size

                        bits_field_path_start = None

                    # Handle pointer fields
                    if self.pointer_path_check(field_path):
                        if self.pointer_check(ctype_obj, field[0]):
                            length, address, pointer_inst = getattr(ctype_obj, f'{field[0]}_length'), getattr(ctype_obj, f'{field[0]}_addr'), getattr(ctype_obj, f'{field[0]}_inst')
                            if not address:
                                continue
                            else:
                                field_ctype_obj = getattr(ctype_obj, f'{field[0]}')
                                if isinstance(field_ctype_obj[0], Structure):
                                    # Handle nested structures
                                    for index in range(length):
                                        sub_field_ctype_obj, sub_field_offset_size_map = field_ctype_obj[index], field_offset_size_map[field_path][2]
                                        if decode_raw_data is None:
                                            raw_data += self.pointer_init(sub_field_ctype_obj, None, field_path, sub_field_offset_size_map)
                                        else:
                                            raw_offset += self.pointer_init(sub_field_ctype_obj, decode_raw_data[raw_offset:], field_path, sub_field_offset_size_map)
                                else:
                                    # Handle pointer arrays
                                    if decode_raw_data is None:
                                        raw_data += bytearray(string_at(address, length * sizeof(pointer_inst.elem_type)))
                                    else:
                                        field_size = length * sizeof(pointer_inst.elem_type)
                                        memmove(address, decode_raw_data[raw_offset:raw_offset + field_size], field_size)
                                        raw_offset += field_size
                        else:
                            # Handle non-pointer fields
                            field_ctype_obj, sub_field_offset_size_map = getattr(ctype_obj, f'{field[0]}'), field_offset_size_map[field_path][2]
                            if isinstance(field_ctype_obj, ctypes.Array):
                                # Handle array fields
                                for sub_ctype_obj in field_ctype_obj:
                                    if decode_raw_data is None:
                                        raw_data += self.pointer_init(sub_ctype_obj, None, field_path, sub_field_offset_size_map)
                                    else:
                                        raw_offset += self.pointer_init(sub_ctype_obj, decode_raw_data[raw_offset:], field_path, sub_field_offset_size_map)
                            else:
                                # Handle nested structures
                                if decode_raw_data is None:
                                    raw_data += self.pointer_init(field_ctype_obj, None, field_path, sub_field_offset_size_map)
                                else:
                                    raw_offset += self.pointer_init(field_ctype_obj, decode_raw_data[raw_offset:], field_path, sub_field_offset_size_map)
                    else:
                        # Handle regular fields
                        offset, field_size = field_offset_size_map[field_path][0] // 8, field_offset_size_map[field_path][1] // 8
                        if decode_raw_data is None:
                            raw_data += bytearray(string_at(addressof(ctype_obj) + offset, field_size))
                        else:
                            memmove(addressof(ctype_obj) + offset, decode_raw_data[raw_offset:raw_offset + field_size], field_size)
                            raw_offset += field_size
        return raw_data if decode_raw_data is None else raw_offset


    def encode(self):
        """
        Encodes the current object into a byte sequence.

        This method converts the object into a byte sequence based on its internal state.
        If the object contains pointer fields, it uses the `pointer_init` method to generate
        the byte sequence; otherwise, it directly returns the memory representation of the object.

        Returns:
            bytes: The encoded byte sequence.
        """
        # Initialize the multi-level maximum name map if it hasn't been initialized yet
        if self.multi_level_max_name_map is None: self.get_multi_level_max_name_map()

        # If the object contains pointer fields, use `pointer_init` to generate the byte sequence
        if self.pointer_field_map:
            return bytes(self.pointer_init(self, field_path="", field_offset_size_map=self.fields_offset_size_map))
        else:
            # Otherwise, return the memory representation of the object
            return string_at(addressof(self), sizeof(self))


    def decode(self, data, length=None):
        """
        Decodes the given data and maps it to the current object's structure.

        Args:
            data: The raw data to be decoded, typically a byte array or similar iterable.
            length: Optional parameter specifying the length of the data to decode. If not provided, it is determined based on the object's size or pointer field map.

        Returns:
            None, but the decoded data is mapped to the current object's fields, and internal state may be updated.
        """

        # If the multi-level maximum name map is not initialized, initialize it first
        if self.multi_level_max_name_map is None:
            self.get_multi_level_max_name_map()

        # If there is a pointer field map and no length is specified, perform pointer initialization
        if self.pointer_field_map and length is None:
            self.pointer_init(self, data, field_path="", field_offset_size_map=self.fields_offset_size_map)
        else:
            # If no length is specified, use the object's size as the default length
            length = sizeof(self) if length is None else length
            # Copy data from the source address to the target address
            memmove(addressof(self), data, length)

        # Update the raw data, using the provided raw data if no length is specified
        self._raw_data = self._raw_data if length is not None else data

    def to_kelvin(self, value):
        """
        Converts the given Celsius temperature value to Kelvin and returns a formatted string.

        Args:
            value (int/float): The Celsius temperature value to be converted to Kelvin.

        Returns:
            str: A formatted string representing the Kelvin temperature in the format "(x Kelvin)", where x is the converted Kelvin value.
        """
        return "({:} Kelvin)".format(value + 273)


    def to_percent(self, value):
        """
        Converts the given integer value to a percentage format string.

        Args:
            value (int): The integer value to be converted to a percentage.

        Returns:
            str: A formatted string representing the percentage, right-aligned with a width of 3 characters.
                 For example, if the input is 5, the output will be "  5%".
        """
        return "{:>3d}%".format(value)


    def to_celsius(self, value):
        """
        Converts the given temperature value to a string representation in Celsius.

        Args:
            value (int): The temperature value to be converted, typically an integer.

        Returns:
            str: A string formatted as "{value} C", where {value} is the input temperature.
        """
        return "{:d} C".format(value)

    def to_int(self, ctype_obj=None, byteorder=None, cb_format=False):
        """
        Converts the given ctype object or integer to an integer or a formatted integer string.

        Parameters:
            ctype_obj (object, optional): The ctype object or integer to convert. If not provided, `self` is used.
            byteorder (str, optional): The byte order to use for conversion. If not provided, `self.byteorder` is used.
            cb_format (bool or callable, optional): If True, returns a formatted integer string. If a callable, applies the callable to the value. Defaults to False.

        Returns:
            int or str: The converted integer or formatted integer string.
        """
        # Determine which byte order to use
        byteorder = byteorder if byteorder else self.byteorder
        ctype_obj = ctype_obj if ctype_obj else self

        # If the input is an integer, use it directly; otherwise, convert the ctype object to an integer
        if isinstance(ctype_obj, int):
            value = ctype_obj
        else:
            value = int.from_bytes(string_at(addressof(ctype_obj), sizeof(ctype_obj)), byteorder=byteorder)

        # If the input is a ctype object, convert it to an integer or a formatted integer string
        return cb_format(value) if callable(cb_format) else "{:,d}".format(value) if cb_format else value

    def fields_to_buf(self, buffer):
        """
        Writes the encoded data of the current object into the specified buffer.

        Parameters:
        - buffer: Can be a list or a single buffer object. If it is a list, the function writes the encoded data in segments to each buffer in the list;
                  if it is a single buffer object, the function writes the encoded data directly into that buffer.
        """
        # Encode the current object into raw data
        raw_data = self.encode()

        # If the buffer is a list, write the encoded data in segments to each buffer in the list
        if isinstance(buffer, list):
            raw_offset = 0
            for raw_buf in buffer:
                length = len(raw_data)
                # Decode a portion of the raw data into the current buffer
                raw_buf.decode(raw_data[raw_offset:raw_offset+length])
                # Update the offset to process the next segment of data
                raw_offset = raw_offset + length
        else:
            # If the buffer is not a list, decode the data directly into the buffer
            buffer.decode(raw_data, offset=0, length=len(raw_data))

    def fields_from_buf(self, buffer):
        """
        Process the given buffer to extract and decode fields.

        This function handles two types of buffer inputs:
        - If the buffer is a list, it concatenates all elements into a single byte array and decodes it.
        - If the buffer is not a list, it directly encodes the specified length of data and decodes it.

        Args:
            buffer (list or object): The input buffer to be processed. If it is a list, each element is encoded and concatenated.
                                     If it is not a list, it is directly encoded.
        """
        if isinstance(buffer, list):
            # Initialize an empty byte array to store the byte representation of all buffer data.
            raw_data = bytearray()
            for raw_buf in buffer:
                # Encode each buffer data to a byte string and append it to _data.
                raw_data = raw_data + bytearray(raw_buf.encode())
            # Call the to_decode function to process the concatenated byte data.
            self.decode(raw_data)
        else:
            # For non-list buffer types, directly encode the specified length of data.
            raw_data = buffer.encode(offset=0, length=sizeof(self))
            # Call the to_decode function to process the encoded byte data.
            self.decode(raw_data)

    def fields_to_bin_file(self, bin_path):
        """
        Writes the encoded data of the current object to a specified binary file.

        Parameters:
        - bin_path (str): The path to the binary file where the data will be written.
                          The function checks if the path exists and raises an assertion error if it does not.
        """
        # Check if the binary file path exists
        assert os.path.exists(bin_path), print("get invalid bin path %s" % bin_path)

        # Open the binary file for writing data
        with open(bin_path, 'wb') as f:
            # Get the encoded data
            data = self.encode()
            # Write the encoded data to the binary file
            f.write(data)

    def fields_from_bin_file(self, bin_path):
        """
        Reads and decodes data from a binary file.

        This function reads the contents of a binary file specified by `bin_path` and decodes it using the instance's `decode` method.

        Args:
            bin_path (str): The path to the binary file to be read.

        Raises:
            AssertionError: If the provided binary file path does not exist.
        """
        # Ensure the provided binary file path is valid
        assert os.path.exists(bin_path), print("get invalid bin path %s" % bin_path)

        # Open the binary file and read its contents
        with open(bin_path, 'rb') as f:
            data = f.read()

            # Call the instance's to_decode method to decode the read data
            self.decode(data=data)

    def fields_to_dict(self, ctype_obj=None):
        """
        Converts the fields of a ctypes object (or the current instance) into a dictionary.

        This function traverses the fields of the given ctypes object and processes each field using a callback function.
        The result is a dictionary where the keys are the field names and the values are the processed field values.

        Parameters:
        - ctype_obj (ctypes.Structure/ctypes.Union, optional): The ctypes object whose fields are to be converted into a dictionary.
          If not provided, the function uses the current instance (`self`).

        Returns:
        - fields_dict (dict): A dictionary containing the field names as keys and their processed values as values.
        """
        def cb_func(ctype_obj, field_ctype_obj, field_name, cb_kwargs, field_kwargs):
            """
            Callback function to process each field of the ctypes object.

            This function handles the conversion of ctypes.Array fields into their appropriate Python representations.
            For character arrays, it decodes them into strings. For other arrays, it returns a list of their elements.

            Parameters:
            - ctype_obj: The parent ctypes object containing the field.
            - field_ctype_obj: The specific field object to process.
            - field_name: The name of the field.
            - cb_kwargs: Additional arguments for the callback function (not used in this case).
            - field_kwargs: Additional field-specific arguments (not used in this case).

            Returns:
            - The processed value of the field. For arrays, it returns a decoded string or a list of elements.
              For other fields, it returns the field value as-is.
            """
            if isinstance(field_ctype_obj, ctypes.Array):
                return bytes(bytes(field_ctype_obj) + bytes(1)).decode(ignore_errors=True) if field_ctype_obj._type_ == c_char else field_ctype_obj[:]
            return field_ctype_obj

        # Use the provided ctype_obj or default to self
        ctype_obj = ctype_obj if ctype_obj else self

        # Traverse the fields of the ctype_obj and process them using the callback function
        fields_dict = self.fields_traversal(ctype_obj, cb_func, None, None, True, False)
        return fields_dict


    def fields_from_dict(self, ctype_dict=None, ctype_obj=None):
        """
        Populates the fields of a ctypes object from a dictionary.

        This method traverses the fields of the specified ctypes object and sets their values based on the provided dictionary.
        It handles both regular fields and array fields, ensuring that the values are correctly assigned.

        Parameters:
        - ctype_dict (dict, optional): A dictionary containing field names as keys and their corresponding values.
                                       If None, no fields are populated.
        - ctype_obj (ctypes object, optional): The ctypes object whose fields are to be populated.
                                               If None, the method operates on the instance itself.

        """
        def cb_func(ctype_obj, field_ctype_obj, field_name, cb_kwargs, field_kwargs):
            """
            Callback function to set the value of a field in the ctypes object.

            Parameters:
            - ctype_obj: The ctypes object containing the field.
            - field_ctype_obj: The specific field object to be set.
            - field_name: The name of the field.
            - cb_kwargs: Additional callback arguments (not used in this function).
            - field_kwargs: The value to be assigned to the field, either directly or from a dictionary.

            """
            # Retrieve the field value from the dictionary or directly
            field_value = field_kwargs[field_name] if isinstance(field_kwargs, dict) else field_kwargs

            # Handle array fields
            if isinstance(field_ctype_obj, ctypes.Array):
                # Ensure the length of the array matches the provided value
                assert len(field_ctype_obj) == len(field_value), print("fields from dict not supported for multi-level Array")

                # If the value is a string, encode it and set it as the field value
                if isinstance(field_value, str):
                    setattr(ctype_obj, field_name, field_value.encode())
                else:
                    # Assign each element of the array individually
                    for index, elem in enumerate(field_value):
                        field_ctype_obj[index] = elem
            else:
                # For non-array fields, set the value directly
                setattr(ctype_obj, field_name, field_value)

        # Use the provided ctypes object or default to the instance itself
        ctype_obj = ctype_obj if ctype_obj else self

        # Traverse the fields and apply the callback function to set their values
        self.fields_traversal(ctype_obj, cb_func, None, ctype_dict, True, False, False, True, True)


    def fields_to_json(self, ctype_obj=None, json_path=None):
        """
        Converts the fields of the given ctype object to a JSON string and optionally writes it to a file.

        Parameters:
        - ctype_obj (object, optional): The ctype object whose fields are to be converted to JSON. If not provided, the instance itself is used.
        - json_path (str, optional): The file path where the JSON string will be written. If not provided, the JSON string is not written to a file.

        Returns:
        - fields_dict (dict): A dictionary containing the fields of the ctype object.
        """
        # Use the provided ctype_obj or default to self
        ctype_obj = ctype_obj if ctype_obj else self

        # Convert the fields of the ctype object to a dictionary
        fields_dict = self.fields_to_dict(ctype_obj)

        # Convert the dictionary to a JSON string
        json_string = json.dumps(fields_dict)

        # If a json_path is provided, write the JSON string to the specified file
        if json_path is not None:
            with open(json_path, "w") as f:
                f.write(json_string)

        # Return the dictionary containing the fields
        return fields_dict

    def fields_from_json(self, json_path=None):
        """
        Loads data from a specified JSON file, converts it into a dictionary representation,
        and updates the current object using the `from_dict` method.

        Parameters:
        - json_path (str, optional): The path to the JSON file. If not provided, the function will not execute.

        Raises:
        - AssertionError: If the provided `json_path` does not exist, an assertion error is raised with a message indicating an invalid JSON path.

        """
        # Check if the JSON file path exists
        assert os.path.exists(json_path), print("get invalid json path %s" % json_path)

        # Load the JSON file and convert it into a dictionary representation
        dict_representation = json.loads(json_path)

        # Update the current object using the `from_dict` method
        self.from_dict(dict_representation)

    def fields_to_tuple(self, ctype_obj=None, field_path=False):
        """
        Converts the fields of a ctypes object (or the current instance) into a tuple.

        This function traverses the fields of the given ctypes object and processes each field using a callback function.
        The result is a tuple where each element is either the processed field value or a tuple containing the field name and value,
        depending on the `field_path` parameter.

        Parameters:
        - ctype_obj (ctypes.Structure/ctypes.Union, optional): The ctypes object whose fields are to be converted into a tuple.
          If not provided, the function uses the current instance (`self`).
        - field_path (bool, optional): If True, the returned tuple will contain tuples of (field_name, field_value).
          If False, the returned tuple will contain only the field values. Defaults to False.

        Returns:
        - fields_tuple (tuple): A tuple containing the processed field values or (field_name, field_value) pairs.
        """
        def cb_func(ctype_obj, field_ctype_obj, field_name, cb_kwargs, field_kwargs):
            """
            Callback function to process each field of the ctypes object.

            This function handles the conversion of ctypes.Array fields into their appropriate Python representations.
            For character arrays, it decodes them into strings. For other arrays, it returns a list of their elements.

            Parameters:
            - ctype_obj: The parent ctypes object containing the field.
            - field_ctype_obj: The specific field object to process.
            - field_name: The name of the field.
            - cb_kwargs: Additional arguments for the callback function, including 'field_path'.
            - field_kwargs: Additional field-specific arguments (not used in this case).

            Returns:
            - If 'field_path' is enabled in cb_kwargs, returns a tuple of (field_name, processed_value).
            - Otherwise, returns the processed value directly.
            """
            if isinstance(field_ctype_obj, ctypes.Array):
                if field_ctype_obj._type_ == c_char:
                    cb_ret = bytes(bytes(field_ctype_obj) + bytes(1)).decode(ignore_errors=True)
                else:
                    cb_ret = field_ctype_obj[:]
            else:
                cb_ret = field_ctype_obj
            return (field_name, cb_ret) if cb_kwargs and cb_kwargs.get('field_path', None) else cb_ret

        # Use the provided ctype_obj or default to self
        ctype_obj = ctype_obj if ctype_obj is not None else self

        # Set callback arguments, including 'field_path' and 'transform_tuple'
        cb_kwargs = {"field_path": field_path, "transform_tuple": True}

        # Traverse the fields of the ctype_obj and process them using the callback function
        fields_tuple = self.fields_traversal(ctype_obj, cb_func, cb_kwargs, None, True, False, True, False)

        # Return the processed fields as a tuple
        return tuple(fields_tuple)


    def fields_from_tuple(self, ctype_tuple=None, ctype_obj=None):
        """
        Populates the fields of a ctypes object from a tuple.

        This method traverses the fields of the specified ctypes object and sets their values based on the provided tuple.
        It handles both regular fields and array fields, ensuring that the values are correctly assigned.

        Parameters:
        - ctype_tuple (tuple, optional): A tuple containing field values. If None, no fields are populated.
        - ctype_obj (ctypes object, optional): The ctypes object whose fields are to be populated.
                                               If None, the method operates on the instance itself.

        Raises:
        - AssertionError: If the length of an array field does not match the provided value in the tuple.
        """
        def cb_func(ctype_obj, field_ctype_obj, field_name, cb_kwargs, field_kwargs):
            """
            Callback function to set the value of a field in the ctypes object.

            Parameters:
            - ctype_obj: The ctypes object containing the field.
            - field_ctype_obj: The specific field object to be set.
            - field_name: The name of the field.
            - cb_kwargs: Additional callback arguments (not used in this function).
            - field_kwargs: The value to be assigned to the field, either directly or from a tuple.

            Raises:
            - AssertionError: If the length of an array field does not match the provided value in the tuple.
            """
            # Retrieve the field value from the tuple or directly
            field_value = field_kwargs[field_name] if isinstance(field_kwargs, dict) else field_kwargs

            # Handle array fields
            if isinstance(field_ctype_obj, ctypes.Array):
                # Ensure the length of the array matches the provided value
                assert len(field_ctype_obj) == len(field_value), print("fields from dict not supported for multi-level Array")

                # If the value is a string, encode it and set it as the field value
                if isinstance(field_value, str):
                    setattr(ctype_obj, field_name, field_value.encode())
                else:
                    # Assign each element of the array individually
                    for index, elem in enumerate(field_value):
                        field_ctype_obj[index] = elem
            else:
                # For non-array fields, set the value directly
                setattr(ctype_obj, field_name, field_value)

        # Use the provided ctypes object or default to the instance itself
        ctype_obj = ctype_obj if ctype_obj else self

        # Traverse the fields and apply the callback function to set their values
        self.fields_traversal(ctype_obj, cb_func, None, ctype_tuple, True, False, False, True, True)


    def bytes_dump(self, offset=0, length=None, log_info=None, line_length=32):
        """
        Dumps the byte data of the instance in a formatted manner.

        This function encodes the instance's byte data and then formats it for output.
        The output can be customized using the provided parameters.

        Args:
            offset (int, optional): The starting position in the byte data from which to begin dumping.
                                    Defaults to 0.
            length (int, optional): The number of bytes to dump. If None, dumps all bytes from the offset
                                    to the end of the data. Defaults to None.
            log_info (str, optional): Custom log information to be used during the dump. If not provided,
                                      the instance's log_info attribute will be used. Defaults to None.
            line_length (int, optional): The number of bytes to display per line in the output.
                                         Defaults to 32.
        """
        # Encode the instance's byte data into a processable format
        data = self.encode()

        # Use the provided log_info parameter or the instance's log_info attribute if log_info is not provided
        log_info = log_info if log_info else self.log_info

        # Calculate the actual length of data to dump based on the provided offset and length parameters
        length = len(data) - offset if length is None else length if length + offset < len(data) else len(data) - offset

        # Call the encode_dump function to perform the actual data formatting and output
        encode_dump(data, offset=offset, length=length, unit=1, log_info=log_info, line_length=line_length)

    def short_dump(self, offset=0, length=None, log_info=print, line_length=32, byteorder=None):
        """
        Dumps a portion of the encoded data in a short format.

        This method encodes the object's data, interprets it in the specified byte order, and dumps a portion of it in a formatted manner.

        Args:
            offset (int, optional): The starting position in the encoded data from which to begin dumping. Defaults to 0.
            length (int, optional): The number of 2-byte units to dump. If None, dumps all available data from the offset. Defaults to None.
            log_info (function, optional): The function used to log the dumped data. Defaults to the built-in `print` function.
            line_length (int, optional): The number of 2-byte units to display per line. Defaults to 32.
            byteorder (str, optional): The byte order used to interpret the data. If None, the object's default byte order is used. Defaults to None.
        """
        # Get the encoded data
        data = self.encode()
        # Determine the byte order for data interpretation
        byteorder = byteorder if byteorder else self.byteorder
        # Calculate the length of data to dump
        length = (len(data) - offset) // 2 if length is None else length if length * 2 + offset < len(data) else (len(data) - offset) // 2
        _data = []
        # Convert the encoded data to an integer representation
        for i in range(length):
            _data.append(int.from_bytes(data[i * 2 + offset : (i + 1) * 2 + offset], byteorder=byteorder))
        # Call the function to dump the processed data
        encode_dump(_data, offset=offset, length=length, unit=1, log_info=log_info, line_length=line_length)


    def int_dump(self, offset=0, length=None, log_info=None, line_length=32, byteorder=None):
        """
        Dumps the encoded data as a list of integers in a formatted manner.

        This method encodes the object's data, interprets it in the specified byte order, and dumps a portion of it as a list of integers.

        Args:
            offset (int, optional): The starting position in the encoded data from which to begin dumping. Defaults to 0.
            length (int, optional): The number of 4-byte units to dump. If None, dumps all available data from the offset. Defaults to None.
            log_info (function, optional): The function used to log the dumped data. If not provided, the instance's log_info attribute is used. Defaults to None.
            line_length (int, optional): The number of 4-byte units to display per line. Defaults to 32.
            byteorder (str, optional): The byte order used to interpret the data. If None, the object's default byte order is used. Defaults to None.
        """
        # Convert data to specified encoding format
        data = self.encode()
        # If log_info is not provided, use the instance's log_info attribute
        log_info = log_info if log_info else self.log_info
        # If byteorder is not provided, use the instance's byteorder attribute
        byteorder = byteorder if byteorder else self.byteorder
        # Calculate the number of bytes to convert based on the provided offset and data length
        length = (len(data) - offset) // 4 if length is None else length if length * 4 + offset < len(data) else (len(data) - offset) // 4
        _data = []
        # Convert data to a list of integers according to the byte order
        for i in range(length):
            _data.append(int.from_bytes(data[i * 4 + offset: (i + 1) * 4 + offset], byteorder=byteorder))
        # Call encode_dump function to print the formatted data
        encode_dump(_data, offset=offset, length=length, unit=1, log_info=log_info, line_length=line_length)



    def long_dump(self, offset=0, length=None, log_info=None, line_length=32, byteorder=None):
        """
        Dumps the encoded data as a list of 64-bit integers in a formatted manner.

        This method encodes the object's data, interprets it in the specified byte order, and dumps a portion of it as a list of 64-bit integers.

        Args:
            offset (int, optional): The starting position in the encoded data from which to begin dumping. Defaults to 0.
            length (int, optional): The number of 8-byte units to dump. If None, dumps all available data from the offset. Defaults to None.
            log_info (function, optional): The function used to log the dumped data. If not provided, the instance's log_info attribute is used. Defaults to None.
            line_length (int, optional): The number of 8-byte units to display per line. Defaults to 32.
            byteorder (str, optional): The byte order used to interpret the data. If None, the object's default byte order is used. Defaults to None.
        """
        # Encode the object's data into a byte stream
        data = self.encode()
        # Use the provided log_info or default to the internal log_info if not provided
        log_info = log_info if log_info else self.log_info
        # Use the provided byteorder or default to the internal byteorder if not provided
        byteorder = byteorder if byteorder else self.byteorder
        # Calculate the length of the dump, ensuring it does not exceed the actual data length
        length = (len(data) - offset) // 8 if length is None else length if length * 8 + offset < len(data) else (len(data) - offset) // 8
        _data = []
        # Convert the data into a list of integers based on the specified length and offset
        for i in range(length):
            _data.append(int.from_bytes(data[i * 8 + offset : (i + 1) * 8 + offset], byteorder=byteorder))
        # Call the encode_dump method to perform the actual data dump
        encode_dump(_data, offset=offset, length=length, unit=1, log_info=log_info, line_length=line_length)


    def __len__(self):
        """
        Returns the size of the current object in bytes.

        This method implements the Python `__len__` magic method, which is typically used to support the `len()` function.
        It returns the size of the object in bytes, as determined by the `sizeof()` function.

        Returns:
            int: The size of the object in bytes.
        """
        return sizeof(self)


    def __call__(self, current_ctype_obj, origin_ctype_obj=None, except_value=0, report_error=True, log_info=None, byteorder=None):
        """
         This function is used to compare two C-type objects (current_ctype_obj and origin_ctype_obj) and determine if the comparison meets the expected condition based on the except_value. It supports different types of C-type objects, including strings, integers, and other C-type structures. The function also logs the comparison results and can raise an assertion error if the comparison fails and report_error is set to True.

         Parameters:
            current_ctype_obj: The current C-type object to be compared. It can be a string, integer, or other C-type object.
            origin_ctype_obj: The original C-type object to compare against. If None, the comparison is skipped. Default is None.
            except_value: The expected value or condition for the comparison. If None, the function returns True immediately. Default is 0.
            report_error: If True, an assertion error is raised if the comparison fails. Default is True.
            log_info: The logging function to use for output. If None, the class's log_info attribute is used. Default is None.
            byteorder: The byte order to use for integer conversion. If None, the class's byteorder attribute is used. Default is None.
        Returns:
            bool: Returns True if the comparison is successful, otherwise returns False. If report_error is True and the comparison fails, an assertion error is raised.

        """
        # Use the log_info provided, or the class's log_info attribute if not provided
        log_info = log_info if log_info else self.log_info
        # If except_value is None, the comparison is considered successful
        if except_value is None:
            return True
        # Use the byteorder provided, or the class's byteorder attribute if not provided
        byteorder = byteorder if byteorder else self.byteorder
        # Determine the type of current_ctype_obj and perform corresponding operations
        if isinstance(current_ctype_obj, str):
            # Assert that origin_ctype_obj is None or of the same type as current_ctype_obj
            assert (origin_ctype_obj is None or type(current_ctype_obj) == type(origin_ctype_obj)), print("expect origin_ctype_obj is None or origin_ctype_obj %s, actual %s"%(current_ctype_obj, origin_ctype_obj))

            # Get the original and current values based on the type and content of current_ctype_obj and origin_ctype_obj
            if type(current_ctype_obj) == type(origin_ctype_obj):
                _origin_value = eval('self._last_inst.%s' % origin_ctype_obj)
            else:
                _origin_value = eval('self._last_inst.%s'%current_ctype_obj)
            _current_value = eval('self.%s'%current_ctype_obj)

            # Convert values to integers if they are not already
            if not isinstance(_origin_value, int):
                _current_value = self.to_int(current_ctype_obj, byteorder=byteorder)
                _origin_value = self.to_int(_origin_value, byteorder=byteorder)
        elif isinstance(current_ctype_obj, int):
            # Assert that origin_ctype_obj is an integer
            assert (origin_ctype_obj is int), print("expect origin_ctype_obj is int, actual %s"%(type(origin_ctype_obj)))

            # Directly use the integer values for comparison
            _origin_value, _current_value = origin_ctype_obj, current_ctype_obj
        else:
            # Assert that origin_ctype_obj is None or of the same type as current_ctype_obj
            assert (origin_ctype_obj is None or type(current_ctype_obj) == type(origin_ctype_obj)), print("expect origin_ctype_obj is None or origin_ctype_obj %s, actual %s"%(type(current_ctype_obj), type(origin_ctype_obj)))

            # Convert the values of current_ctype_obj and origin_ctype_obj to integers for comparison
            _current_value = self.to_int(current_ctype_obj, byteorder=byteorder)
            if type(current_ctype_obj) == type(origin_ctype_obj):
                _origin_value = self.to_int(origin_ctype_obj, byteorder=byteorder)
            else:
                _offset = addressof(current_ctype_obj) - addressof(self)
                _origin_value = self.to_int(string_at(addressof(self._last_inst) + _offset, sizeof(current_ctype_obj)), byteorder=byteorder)

        # Calculate the difference between the current and original values
        __difference, _error = _current_value - _origin_value, False

        # Determine the comparison logic based on the value of except_value
        if except_value == STRUCT_INCREASE:
            _error = False if __difference > 0 else True
        elif except_value == STRUCT_DECREASE:
            _error = False if __difference < 0 else True
        elif except_value == STRUCT_CHANGE:
            _error = False if __difference != 0 else True
        elif except_value == STRUCT_EQUAL:
            _error = False if __difference == 0 else True
        else:
            _error = False if __difference == except_value else True

        # Get the check string for logging based on except_value
        check_string = compare_dict[except_value] if except_value in compare_dict.keys() else str(except_value)

        # Log the comparison information
        log_info("current_ctype_obj: %s current_value is %s origin_value is %s expect %s"%(origin_ctype_obj, _current_value, _origin_value, check_string))

        # If report_error is True and there is an error, raise an assertion error
        assert not (report_error and _error)

        # Return the error flag
        return _error

    def fields_trav_string(self, ctype_obj, field_ctype_obj, field_name, cb_kwargs, field_kwargs):
        """
        Traverses and processes a field of a ctypes object, converting it to a string representation.

        This function handles different types of fields, including arrays and character arrays, and converts them into a readable string format.
        It also supports optional field path inclusion in the return value.

        Parameters:
        - ctype_obj: The parent ctypes object containing the field.
        - field_ctype_obj: The specific field object to process.
        - field_name: The name of the field.
        - cb_kwargs: A dictionary of callback options, including 'list_to_int' and 'field_path'.
        - field_kwargs: Additional field-specific arguments.

        Returns:
        - If 'field_path' is enabled in cb_kwargs, returns a tuple of (field_name, processed_value).
        - Otherwise, returns the processed value directly.
        """
        # Handle array fields
        if isinstance(field_ctype_obj, ctypes.Array):
            # Check if the array is zero-filled
            if self.struct_zero_check(field_ctype_obj):
                cb_ret = f"0x00 * {sizeof(field_ctype_obj)}"
            else:
                # Handle character arrays by decoding them to strings
                if field_ctype_obj._type_ == c_char:
                    cb_ret = bytes(bytes(field_ctype_obj) + bytes(1)).decode(ignore_errors=True)
                else:
                    # Convert array to integer if 'list_to_int' is enabled, otherwise return the array as-is
                    cb_ret = self.to_int(field_ctype_obj) if cb_kwargs and cb_kwargs.get('list_to_int', None) else field_ctype_obj[:]
        else:
            # For non-array fields, return the field object directly
            cb_ret = field_ctype_obj

        # Return the result with or without the field name based on 'field_path' option
        return (field_name, cb_ret) if cb_kwargs and cb_kwargs.get('field_path', None) else cb_ret


    def show_info(self, ctype_obj=None, list_to_int=False, indent='', skip_reserved=True, field_path=True, disable_tree=False, log_info=print):
        """
        Displays the structure information of the given ctype object in a tree-like format.

        Parameters:
        - ctype_obj (object, optional): The ctype object to display information for. If not provided, the instance itself is used.
        - list_to_int (bool, optional): If True, converts list fields to integers. Defaults to False.
        - indent (str, optional): The indentation string used for formatting the tree structure. Defaults to an empty string.
        - skip_reserved (bool, optional): If True, skips fields with names containing 'reserved' or 'rsvd'. Defaults to True.
        - field_path (bool, optional): If True, includes the full field path in the output. Defaults to True.
        - disable_tree (bool, optional): If True, disables the tree-like formatting. Defaults to False.
        - log_info (function, optional): The logging function used to output the information. Defaults to the built-in `print` function.

        Returns:
        None, but the structure information is printed or logged in the specified format.
        """
        # Use the provided ctype_obj or default to self
        ctype_obj = ctype_obj if ctype_obj else self

        # Prepare callback arguments for field traversal
        cb_kwargs = {"field_path": True, "list_to_int": list_to_int}

        # Traverse the fields of the ctype object and generate a string map
        fields_string_map = self.fields_traversal(ctype_obj, self.fields_trav_string, cb_kwargs, None, True, True, True, False)

        # Ensure the multi-level maximum name map is initialized
        self.get_multi_level_max_name_map()

        # Initialize the object if it doesn't have an info_header attribute
        if not hasattr(self, "info_header"):
            self.__init__()

        # Use the provided log_info function or default to the instance's log_info
        log_info = log_info if log_info else self.log_info

        # Log the info_header if it exists and the ctype_obj is the instance itself
        if hasattr(self, "info_header") and self.info_header and ctype_obj == self:
            log_info(self.info_header)

        # Print the structure information in a tree-like format
        self.print_tree(fields_string_map, indent=indent, skip_reserved=skip_reserved, field_path=field_path, disable_tree=disable_tree, log_info=log_info)


    def show_diff(self, current_inst=None, origin_inst=None, list_to_int=False, indent='', skip_reserved=True, field_path=True, disable_tree=False, signed="***", log_info=print):
        """
        Displays the differences between the current instance and the original instance in a structured format.

        Parameters:
        - current_inst: The current instance to compare. If not provided, `self` is used.
        - origin_inst: The original instance to compare against. If not provided, `self._last_inst` is used.
        - list_to_int: If True, converts lists to integers during comparison. Defaults to False.
        - indent: The indentation string used for formatting the output. Defaults to an empty string.
        - skip_reserved: If True, skips fields with names containing 'reserved' or 'rsvd'. Defaults to True.
        - field_path: If True, includes the full field path in the output. Defaults to True.
        - disable_tree: If True, disables the tree structure in the output. Defaults to False.
        - signed: The string used to mark differences in the output. Defaults to "***".
        - log_info: The logging function used to output the results. Defaults to the built-in `print` function.

        """
        def cb_max_value_length(current_string_map, origin_string_map, max_value):
            """
            Calculates the maximum length of values in the current and original string maps.

            Parameters:
            - current_string_map: The map of current field values.
            - origin_string_map: The map of original field values.
            - max_value: The current maximum value length.

            Returns:
            The updated maximum value length.
            """
            for index, item in enumerate(current_string_map):
                current_key, current_value = item[0], item[1] if len(item) > 1 else None
                origin_key, origin_value = origin_string_map[index][0], origin_string_map[index][1] if len(origin_string_map[index]) > 1 else None
                if isinstance(item, list) and (len(item) == 1 or isinstance(item[0], tuple)):
                    max_value = cb_max_value_length(item, origin_string_map[index], max_value)
                else:
                    if isinstance(current_value, list) and (len(current_value) == 1 or isinstance(current_value[0], tuple)):
                        max_value = cb_max_value_length(current_value, origin_value, max_value)
                    else:
                        max_value = max(max_value, len(f"{current_value}"), len(f"{origin_value}"))
            return max_value

        # Initialize current and original instances
        current_inst = current_inst if current_inst else self
        origin_inst = origin_inst if origin_inst else self._last_inst
        log_info = log_info if log_info else self.log_info

        # Ensure the types of current and original instances match
        assert type(origin_inst) == type(current_inst), log_info("origin(%s) is not of %s" % (type(origin_inst), type(current_inst)))

        # Initialize the instance if it doesn't have a diff_header
        if not hasattr(self, "diff_header"):
            self.__init__()

        # Log the diff header if it exists
        if hasattr(self, "diff_header") and self.diff_header:
            log_info(self.diff_header)

        # Initialize callback arguments and maximum value length
        cb_kwargs, max_value_length = {"field_path":True, "list_to_int":list_to_int}, 16

        # Traverse the fields of the current and original instances
        current_string_map = self.fields_traversal(current_inst, self.fields_trav_string, cb_kwargs, None, True, True,  True, False)
        origin_string_map = self.fields_traversal(origin_inst, self.fields_trav_string, cb_kwargs, None, True, True, True, False)

        # Calculate the maximum value length for formatting
        max_value_length = cb_max_value_length(current_string_map, origin_string_map, max_value_length)

        # Get the multi-level maximum name map for field alignment
        self.get_multi_level_max_name_map()

        # Print the differences in a tree structure
        self.print_tree(current_string_map, origin_string_map, indent=indent, skip_reserved=skip_reserved, field_path=field_path, disable_tree=disable_tree,
                        max_value_length=max_value_length, signed=signed, log_info=log_info)


    def print_tree(self, current_data, original_data=None, indent='', is_last=False, is_root=True, skip_reserved=True, field_path=True, disable_tree=False, max_value_length=16,
                   signed="***", log_info=print):
        """
        Recursively prints a tree structure of the given data, optionally comparing it with original data.

        Args:
            current_data (list): The current data to be printed, typically a list of key-value pairs.
            original_data (list, optional): The original data to compare against. Defaults to None.
            indent (str, optional): The indentation string for the current level of the tree. Defaults to an empty string.
            is_last (bool, optional): Indicates if the current item is the last in its level. Defaults to False.
            is_root (bool, optional): Indicates if the current item is the root of the tree. Defaults to True.
            skip_reserved (bool, optional): If True, skips fields with names containing 'reserved' or 'rsvd'. Defaults to True.
            field_path (bool, optional): If True, includes the full field path in the output. Defaults to True.
            disable_tree (bool, optional): If True, disables the tree-like formatting. Defaults to False.
            max_value_length (int, optional): The maximum length of the value to be displayed. Defaults to 16.
            signed (str, optional): The string used to mark differences between current and original data. Defaults to "***".
            log_info (function, optional): The logging function used to output the information. Defaults to the built-in `print` function.

        """
        num_keys = len(current_data)
        max_key_length = self.multi_level_max_name_list[-1] if field_path else self.multi_level_max_name_list[0]

        # Iterate through each item in the current data
        for index, item in enumerate(current_data):
            current_key, current_value = item[0], item[1] if len(item) > 1 else None
            origin_value = original_data[index][1] if original_data and len(original_data[index]) > 1 else None
            is_last_key = (index == num_keys - 1)

            # Determine the line prefix and new indentation based on the tree level
            if is_root:
                line_prefix, new_indent = '', indent
            else:
                level = len(current_key.split(".")) if isinstance(current_key, str) else 1
                if not disable_tree:
                    line_prefix = ' └─ ' if is_last else ' ├─ '
                    connector = '    ' * level if is_last else ' │   ' + "   " * (level - 1)
                else:
                    line_prefix, connector = '    ', '    ' * level
                new_indent = indent + connector

            # Handle nested lists or tuples
            if isinstance(item, list) and (len(item) == 1 or isinstance(item[0], tuple)):
                if isinstance(item[0], tuple):
                    log_info(f"{indent}{line_prefix}{item[0][0].split('.')[-2]}")
                original_item = original_data[index] if original_data else None
                self.print_tree(item, original_item, new_indent, is_last_key, is_root=False, field_path=field_path, disable_tree=disable_tree, log_info=log_info)
            else:
                # Handle nested lists or tuples within the current value
                if isinstance(current_value, list) and (len(current_value) == 1 or isinstance(current_value[0], tuple)):
                    self.print_tree(current_value, origin_value, new_indent, is_last_key, is_root=False, field_path=field_path, disable_tree=disable_tree, log_info=log_info)
                    log_info(f"{indent}{line_prefix}{current_key}")
                else:
                    # Skip reserved fields if specified
                    field_name = current_key.split(".")[-1].lower()
                    if skip_reserved and ('reserved' in field_name or 'rsvd' in field_name):
                        continue

                    # Format the key based on whether the full path is included
                    current_key = current_key if field_path else current_key.split(".")[-1]
                    formatted_key = f"{indent}{current_key}" if is_root else f"{indent}{line_prefix}{current_key}"

                    # Print the key-value pair, comparing with original data if provided
                    if original_data is None:
                        log_info(f"{formatted_key:<{max_key_length}}: {current_value}")
                    else:
                        if current_value != origin_value:
                            log_info(f"{formatted_key:<{max_key_length}}: {current_value:<{max_value_length}}   {origin_value:<{max_value_length}}  {signed}")
                        else:
                            log_info(f"{formatted_key:<{max_key_length}}: {current_value:<{max_value_length}}   {origin_value:<{max_value_length}}")


    def get_fields_offset_size_map(self, ctype_obj=None, field_path=True):
        """
        Generates a mapping of field names to their offsets and sizes within a ctypes object.

        This function traverses the fields of the given ctypes object (e.g., Structure or Union) and calculates
        the memory offset and size for each field. It handles pointer fields, nested structures, unions, and arrays,
        ensuring proper alignment and offset adjustments.

        Parameters:
            ctype_obj (ctypes.Structure/ctypes.Union, optional): The ctypes object to analyze. If not provided, `self` is used.
            field_path (bool/str, optional): If True, generates full field paths (e.g., "parent.child.field"). If a string, uses it as the base path. Defaults to True.

        Returns:
            OrderedDict: A dictionary where keys are field paths and values are tuples of (offset, size, Optional[OrderedDict]).
                         - offset: The memory offset of the field.
                         - size: The size of the field in bits.
                         - Optional[OrderedDict]: If the field is a nested structure or union, this contains its offset-size map.
        """
        ctype_obj = ctype_obj if ctype_obj else self
        offset_size_map, offset, point_mask = OrderedDict(), 0, sizeof(c_void_p) * 8 - 1
        base_field = field_path if isinstance(field_path, str) else ""

        # Iterate through each field in the ctypes object
        for field_index, field in enumerate(ctype_obj._fields_):
            # Generate the full field path
            field_path = f"{base_field}.{field[0]}" if base_field else field[0]
            field_ctype_obj = getattr(ctype_obj, field[0])

            # Handle pointer fields
            if self.pointer_check(self, field[0]):
                # Ensure proper alignment for pointer fields
                if offset & point_mask:
                    offset = (offset + point_mask) & point_mask
                pointer_inst = getattr(ctype_obj, f'{field[0]}_inst')
                field_ctype_obj = pointer_inst.elem_type()
                trav_ret = None

                # Handle nested structures or unions
                if isinstance(field_ctype_obj, Structure) or isinstance(field_ctype_obj, ctypes.Union):
                    if isinstance(field_ctype_obj, ctypes.Union):
                        field_ctype_obj = self.get_max_size_union_struct(field_ctype_obj)
                    trav_ret = self.get_fields_offset_size_map(field_ctype_obj, field_path)
                offset_size_map[field_path] = (offset, sizeof(c_void_p) * 8, trav_ret) if trav_ret else (offset, sizeof(c_void_p) * 8)
                offset += sizeof(c_void_p) * 8
            else:
                # Handle non-pointer fields
                if isinstance(field_ctype_obj, Structure) or isinstance(field_ctype_obj, ctypes.Union):
                    if isinstance(field_ctype_obj, ctypes.Union):
                        field_ctype_obj = self.get_max_size_union_struct(field_ctype_obj)
                    trav_ret = self.get_fields_offset_size_map(field_ctype_obj, field_path)
                    offset_size_map[field_path] = (offset, sizeof(field_ctype_obj) * 8, trav_ret)
                elif isinstance(field_ctype_obj, ctypes.Array):
                    if isinstance(field_ctype_obj[0], Structure) or isinstance(field_ctype_obj[0], ctypes.Union):
                        _field_ctype_obj = field_ctype_obj[0]
                        if isinstance(_field_ctype_obj, ctypes.Union):
                            _field_ctype_obj = self.get_max_size_union_struct(_field_ctype_obj)
                        trav_ret = self.get_fields_offset_size_map(_field_ctype_obj, field_path)
                        offset_size_map[field_path] = (offset, sizeof(field_ctype_obj) * 8, trav_ret)
                        offset += sizeof(field_ctype_obj) * 8
                    else:
                        offset_size_map[field_path] = (offset, sizeof(field[1]) * 8)
                        offset += sizeof(field[1]) * 8
                else:
                    # Handle bit fields or regular fields
                    if len(field) == 3:
                        offset_size_map[field_path] = (offset, field[2])
                        offset += field[2]
                    else:
                        offset_size_map[field_path] = (offset, sizeof(field[1]) * 8)
                        offset += sizeof(field[1]) * 8
                        assert (offset & 7) == 0, "pointer type field offset must be 0"
        return offset_size_map

    def get_self_fields_offset_map(self):
        """
        Calculates and returns a mapping of field names to their memory offsets within the current object.

        This function iterates through the `_fields_` attribute of the object, which defines the structure's fields,
        and calculates the memory offset for each field. It handles bit fields, pointer fields, and regular fields,
        ensuring proper alignment and offset adjustments.

        Returns:
            OrderedDict: A dictionary where keys are field names and values are their corresponding memory offsets.
        """
        offset_map, offset, point_mask, bit_type, bit_offset = OrderedDict(), 0, sizeof(c_void_p) * 8 - 1, None, 0

        # Iterate through each field in `_fields_` to calculate offsets
        for index, field in enumerate(self._fields_):
            # Map the field name to its current offset
            offset_map[field[0]] = offset

            # Handle bit fields: adjust offsets based on bit field size and alignment
            if len(field) == 3:
                if bit_type is None:
                    bit_type = sizeof(field[1])
                    bit_offset = field[2]
                else:
                    if bit_type != sizeof(field[1]):
                        if bit_offset % (bit_type * 8):
                            offset_map[self._fields_[index - 1][0]] = offset + (bit_type * 8) - (bit_offset % (bit_type * 8))
                            offset = offset_map[self._fields_[index - 1][0]]
                        bit_type, bit_offset = None, 0
                    else:
                        bit_offset += field[2]
            else:
                if bit_type and bit_offset % (bit_type * 8):
                    offset_map[self._fields_[index - 1][0]] = offset + (bit_type * 8) - (bit_offset % (bit_type * 8))
                    offset = offset_map[self._fields_[index - 1][0]]
                bit_type, bit_offset = None, 0

            # Adjust offset for pointer fields to ensure proper alignment
            if self.pointer_check(self, field[0]):
                if offset & point_mask and index:
                    offset_map[self._fields_[index - 1][0]] = (offset + point_mask) & point_mask
                    offset = offset_map[self._fields_[index - 1][0]]
                offset += sizeof(c_void_p) * 8
            else:
                # Calculate offset for non-pointer fields based on their size
                offset += sizeof(field[1]) * 8 if len(field) == 2 else field[2]
        return offset_map


if __name__ == "__main__":

    class XT_Sub_Union(StructureBase):
        _fields_ = [('sub_c_uint8', c_uint8),
                    ('sub_c_uint16', c_uint16),
                   ]
    class XT_Sub_Struct_Item(StructureBase):
        _fields_ = [('sub_item_c_uint8', c_uint8),
                    ('sub_item_c_uint16', c_uint16),
                    ('sub_item_c_uint32', c_int32),
                    ('sub_item_c_uint16_array', c_uint16 * 2),
                    ('sub_pointer', Pointer(XT_Sub_Union, 2)),
                    ]
    class XT_Struct_Union(Union):
        _fields_ = [('Raw_Value', c_uint8 * 11),
                    ('sub_struct_item', XT_Sub_Struct_Item)
                    ]

    class XT_Sub_Struct(StructureBase):
        _fields_ = [('sub_c_uint8', c_uint8),
                    ('sub_c_uint16', c_uint16),
                    ('struct_union', XT_Struct_Union),
                    ('sub_c_uint16_array', c_uint16 * 2),
                    ('sub_pointer', Pointer(XT_Sub_Struct_Item, 6)),
                    ]
    class Test_Pointer(StructureBase):
        _fields_ = [
                    ("c_uint8", c_uint8),
                    ("c_uint16", c_uint16),
                    ("c_int32", c_int32),
                    ("c_int32_array", c_int32 * 2),
                    ("uint64", c_uint64),
                    ("union_verify", XT_Struct_Union),
                    ("union_verify_array", XT_Struct_Union * 2),
                    ("sub_struct", XT_Sub_Struct),
                    ("sub_struct_array", XT_Sub_Struct * 2),
                    ("sub_struct_item", XT_Sub_Struct_Item),
                    ("sub_struct_item_array", XT_Sub_Struct_Item * 2),
                    ("c_uint64", Pointer(c_uint64, 6)),
                    ("union", Pointer(XT_Struct_Union, 6)),
                    ("struct", Pointer(XT_Sub_Struct, 6)),
                    ]

    test = Test_Pointer()
    # test.get_multi_level_max_name_map()
    # test.fields_to_string()
    # fields_dict = test.fields_to_dict()
    # fields_dict["c_uint8"] = 0x1
    # fields_dict["c_int32"] = 0x12
    # fields_dict["c_int32_array"][0] = 0x1234
    # test.fields_from_dict(fields_dict)
    test.show_diff(test, test)
    raw_data = test.encode()
    test.decode(raw_data)
    # fields_tuple = test.fields_to_tuple()
    # test.fields_from_tuple(fields_tuple)