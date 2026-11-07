from common import *
import importlib.util
from native_context import factory

specification = importlib.util.spec_from_file_location("retained_poisson_driver", ORIGINAL_POISSON / "poisson_driver.py")
retained = importlib.util.module_from_spec(specification)
specification.loader.exec_module(retained)
PoissonDriver = retained.PoissonDriver


def open_system(model, folder):
    require(LABEL in ("half", "double") and WAVE is not None, "prospective family")
    return PoissonDriver(factory(folder)(model, LABEL, WAVE), model, WAVE)
