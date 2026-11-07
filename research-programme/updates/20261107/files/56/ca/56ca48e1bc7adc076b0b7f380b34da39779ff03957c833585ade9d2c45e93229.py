import hybrid_temperature_common as legacy
from hybrid_temperature_common import *


def trace_path(model, match):
    return ROOT / "results/legacy-reference" / f"{model}-m{match}" / "trace.npz"


legacy.trace_path = trace_path
