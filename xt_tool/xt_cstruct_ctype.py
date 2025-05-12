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
from pycparser import parse_file, c_ast

CTYPES_MAP = {
    # basic type
    'char': 'c_char', 'short': 'c_short', 'int': 'c_int', 'long': 'c_long', 'float': 'c_float', 'double': 'c_double',
    '__s8' :'c_int8', '__s16':'c_int16',  '__s32':'c_int32', '__s64':'c_int64',

    # unsigned type
    'unsigned char': 'c_ubyte', 'unsigned short': 'c_ushort', 'unsigned int': 'c_uint', 'unsigned long': 'c_ulong',
    '__u8':'c_uint8', '__u16':'c_uint16', '__u32':'c_uint32',  '__u64':'c_uint64', '__le16':'c_uint16', '__le32':'c_uint32',
    '__le64':'c_uint64', '__be16':'c_uint16', '__be32':'c_uint32', '__be64':'c_uint64',

    # point
    'void': 'c_void_p',

    # Windows type
    'DWORD': 'c_ulong', 'WORD': 'c_ushort', 'BYTE': 'c_ubyte'
}

class StructCollector(c_ast.NodeVisitor):
    def __init__(self):
        self.structs = {}
        self.pack_stack = [None]  # 对齐值栈

    def visit_Struct(self, node):
        struct_name = node.name or f'AnonymousStruct_{id(node)}'
        self.structs[struct_name] = {
            'fields': [],
            'pack': self.pack_stack[-1]
        }
        if node.name and 'nvme_ns_mgmt_host_sw_specified' in node.name:
            print(node)
        if node.decls is not None:
            for decl in node.decls:
                field_type = self.parse_type(decl.type)
                field_name = decl.name
                self.structs[struct_name]['fields'].append(
                    (field_name, field_type)
                )
        else:
            print(f"警告: 结构体 '{node.name}' 无成员或定义不完整")

    def visit_Pragma(self, node):
        if 'pack' in node.string:
            pack_val = node.string.split('(')[1].split(')')[0]
            if pack_val == 'push':
                self.pack_stack.append(self.pack_stack[-1])
            elif pack_val == 'pop':
                if len(self.pack_stack) > 1:
                    self.pack_stack.pop()
            else:
                self.pack_stack[-1] = int(pack_val)

    def parse_type(self, typ):
        if isinstance(typ, c_ast.TypeDecl):
            type_name = self.get_typename(typ.type)
            return CTYPES_MAP.get(type_name, type_name)

        elif isinstance(typ, c_ast.PtrDecl):
            pointed_type = self.parse_type(typ.type)
            return f'POINTER({pointed_type})'

        elif isinstance(typ, c_ast.ArrayDecl):
            base_type = self.parse_type(typ.type)
            dim = self.eval_constant(typ.dim)
            return f'{base_type} * {dim}'

        elif isinstance(typ, c_ast.IdentifierType):
            return CTYPES_MAP.get(' '.join(typ.names), ' '.join(typ.names))

        return 'UNKNOWN_TYPE'

    def get_typename(self, typ):
        if isinstance(typ, c_ast.IdentifierType):
            return ' '.join(typ.names)
        return 'UNKNOWN'

    def eval_constant(self, expr):
        if isinstance(expr, c_ast.Constant):
            return expr.value
        elif isinstance(expr, c_ast.UnaryOp):
            return self.eval_constant(expr.expr)
        return '?'


def generate_code(structs, output_file):
    with open(output_file, 'w') as f:
        f.write("from ctypes import *\n\n")

        # 生成结构体定义
        for name, data in structs.items():
            fields = []
            for field in data['fields']:
                if isinstance(field[1], tuple):  # 处理位域
                    fields.append(f'("{field[0]}", {field[1][0]}, {field[1][1]})')
                else:
                    fields.append(f'("{field[0]}", {field[1]})')

            pack = data['pack']
            pack_str = f'\n    _pack_ = {pack}' if pack else ''
            _struct_fields = ',\n        '.join(fields)
            code = f"""
class {name}(StructureBase):{pack_str}
    _fields_ = [
        {_struct_fields}
    ]\n\n"""
            f.write(code)


def main(input_file, output_file):
    ast = parse_file(input_file, use_cpp=True, cpp_args=r'-I/home/hyc/code/pycparser/utils/fake_libc_include')

    collector = StructCollector()
    collector.visit(ast)

    generate_code(collector.structs, output_file)
    print(f"Generated {len(collector.structs)} structures in {output_file}")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python c_struct_to_ctypes.py input.h output.py")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])