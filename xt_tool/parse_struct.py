import sys
from pycparser import parse_file, c_ast
from collections import OrderedDict

CTYPES_MAP = {
    '__u8': 'c_uint8', '__u16': 'c_uint16', '__u32': 'c_uint32', '__u64': 'c_uint64',
    '__le16': 'c_uint16', '__le32': 'c_uint32', '__le64': 'c_uint64',
    'char': 'c_char', 'int': 'c_int', 'short': 'c_short', 'long': 'c_long',
    'float': 'c_float', 'double': 'c_double', 'void': 'c_void_p'
}

class StructCollector(c_ast.NodeVisitor):
    def __init__(self):
        self.structs = OrderedDict()  # 确保顺序敏感
        self.unions = OrderedDict()
        self.pack_stack = [None]
        self.current_parent = None    # 当前处理的父结构体/联合体
        self.current_field_name = None  # 当前字段名（用于匿名类型命名）

    def get_anon_name(self, prefix):
        return f'{prefix}_{self.current_field_name}'

    def visit_Struct(self, node):
        # 优先处理嵌套类型
        orig_parent = self.current_parent
        self.current_parent = 'struct'

        # 动态生成匿名结构体名称
        if not node.name:
            if not self.current_field_name:
                node.name = f'Struct_Anonymous_{len(self.structs) + 1}'
            else:
                node.name = self.get_anon_name('struct')

        if node.name not in self.structs:
            self.structs[node.name] = {
                'fields': [],
                'pack': self.pack_stack[-1]
            }

            # 递归处理成员
            if node.decls:
                for decl in node.decls:
                    self.current_field_name = decl.name  # 传递字段名
                    field_type = self.parse_type(decl.type)
                    self.structs[node.name]['fields'].append( (decl.name, field_type) )

        self.current_parent = orig_parent

    def visit_Union(self, node):
        orig_parent = self.current_parent
        self.current_parent = 'union'

        # 动态生成匿名联合体名称
        if not node.name:
            if not self.current_field_name:
                node.name = f'Union_Anonymous_{len(self.unions) + 1}'
            else:
                node.name = self.get_anon_name('union')

        if node.name not in self.unions:
            self.unions[node.name] = {
                'fields': [],
                'pack': self.pack_stack[-1]
            }

            if node.decls:
                for decl in node.decls:
                    self.current_field_name = decl.name  # 传递字段名
                    field_type = self.parse_type(decl.type)
                    self.unions[node.name]['fields'].append( (decl.name, field_type) )

        self.current_parent = orig_parent

    def parse_type(self, typ):
        if isinstance(typ, c_ast.TypeDecl):
            if isinstance(typ.type, (c_ast.Struct, c_ast.Union)):
                # 触发嵌套类型解析
                self.visit(typ.type)
                return typ.type.name  # 直接返回动态生成的名称
            else:
                return CTYPES_MAP.get(' '.join(typ.type.names), 'UNKNOWN_TYPE')
        elif isinstance(typ, c_ast.ArrayDecl):
            base_type = self.parse_type(typ.type)
            dim = self._eval_dim(typ.dim)
            return f'{base_type} * {dim}'
        elif isinstance(typ, c_ast.PtrDecl):
            return f'POINTER({self.parse_type(typ.type)})'
        elif isinstance(typ, (c_ast.Struct, c_ast.Union)):
            self.visit(typ)
            return typ.name
        return 'UNKNOWN_TYPE'

    def _eval_dim(self, dim):
        if isinstance(dim, c_ast.Constant):
            return dim.value
        return '?'  # 简化处理复杂表达式

    def visit_Pragma(self, node):
        if 'pack' in node.string:
            # 简化的pack指令处理
            pass

def generate_code(structs, unions, output_file):
    with open(output_file, 'w') as f:
        f.write("from ctypes import *\n\n")

        # 按依赖顺序生成：联合体 -> 结构体
        for name, data in unions.items():
            fields = [f'("{f[0]}", {f[1]})' for f in data['fields']]
            pack = f"\n    _pack_ = {data['pack']}" if data['pack'] else ""
            f.write(f"class {name}(Union):{pack}\n    _fields_ = [\n        {', '.join(fields)}\n    ]\n\n")

        for name, data in structs.items():
            fields = [f'("{f[0]}", {f[1]})' for f in data['fields']]
            pack = f"\n    _pack_ = {data['pack']}" if data['pack'] else ""
            f.write(f"class {name}(Structure):{pack}\n    _fields_ = [\n        {', '.join(fields)}\n    ]\n\n")

def main(input_file, output_file):
    ast = parse_file(
        input_file,
        use_cpp=True,
        cpp_args=[
            '-I/home/hyc/code/pycparser/utils/fake_libc_include',
        ]
    )

    collector = StructCollector()
    collector.visit(ast)

    generate_code(collector.structs, collector.unions, output_file)
    print(f"Generated {len(collector.structs) + len(collector.unions)} types")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python fix_nested.py input.h output.py")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])