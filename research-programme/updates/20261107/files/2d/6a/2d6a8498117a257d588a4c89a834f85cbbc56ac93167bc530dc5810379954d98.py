import ast
import ctypes
import sys
from common import *
import numpy as np

POINTER = ctypes.POINTER(ctypes.c_double)
INTEGER_POINTER = ctypes.POINTER(ctypes.c_int)


def pointer(values):
    return values.ctypes.data_as(POINTER)


def row_error(left, right):
    return float(np.max(abs(left - right) / np.maximum(np.max(abs(right), axis=1, keepdims=True), 1e-80)))


def assign_name(node, name):
    return isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == name for target in node.targets)


def factory(folder="native-contexts"):
    path = SECOND / "run_second.py"
    tree = ast.parse(path.read_text())
    owner = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "main")
    begin = next(index for index, node in enumerate(owner.body) if assign_name(node, "build"))
    end = next(index for index, node in enumerate(owner.body) if assign_name(node, "destination"))
    setup = owner.body[begin:end]
    wrapped = next(node for node in owner.body if isinstance(node, ast.Try))
    model_loop = next(node for node in wrapped.body if isinstance(node, ast.For) and isinstance(node.target, ast.Name) and node.target.id == "model")
    wave_loop = next(node for node in model_loop.body if isinstance(node, ast.For))
    case_index = next(index for index, node in enumerate(wave_loop.body) if assign_name(node, "cases"))
    body = setup + wave_loop.body[:case_index] + [ast.Return(value=ast.Call(func=ast.Name(id="locals", ctx=ast.Load()), args=[], keywords=[]))]
    arguments = ast.arguments(posonlyargs=[], args=[ast.arg(arg="model"), ast.arg(arg="wave_label"), ast.arg(arg="wave")], kwonlyargs=[], kw_defaults=[], defaults=[])
    function = ast.FunctionDef(name="open_context", args=arguments, body=body, decorator_list=[])
    module = ast.fix_missing_locations(ast.Module(body=[function], type_ignores=[]))
    namespace = globals().copy()
    namespace["destination"] = ROOT / folder
    exec(compile(module, str(path), "exec"), namespace)
    return namespace["open_context"]
