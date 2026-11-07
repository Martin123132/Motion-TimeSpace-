import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
import importlib
import validate_temperature_law as validator

validator.previous = importlib.import_module("stage168_common")


if __name__ == "__main__":
    validator.main()
