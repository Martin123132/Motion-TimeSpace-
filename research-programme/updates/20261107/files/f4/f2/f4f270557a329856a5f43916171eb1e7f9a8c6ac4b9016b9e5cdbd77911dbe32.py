from common import *
import ast

owner=BACKGROUND/'common.py'
tree=ast.parse(owner.read_text())
functions=[node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name in ('native_background','other_density','dense_values')]
require(len(functions)==3,'owned background adapter')
namespace=globals().copy()
exec(compile(ast.Module(body=functions,type_ignores=[]),str(owner),'exec'),namespace)
native_background=namespace['native_background']
other_density=namespace['other_density']
dense_values=namespace['dense_values']
