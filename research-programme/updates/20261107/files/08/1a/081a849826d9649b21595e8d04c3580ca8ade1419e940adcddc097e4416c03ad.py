import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
import argparse
import importlib
import sys
sys.dont_write_bytecode = True


def main():
    targets = {"forecast": "run_hybrid_forecast", "compare": "run_hybrid_check",
               "rates": "run_rate_derivation", "validate": "run_temperature_validation",
               "seal": "seal_temperature_law"}
    parser = argparse.ArgumentParser(description="Single-thread Stage169 entry point; existing outputs are never overwritten.")
    parser.add_argument("operation", choices=targets)
    arguments, remaining = parser.parse_known_args()
    sys.argv = [sys.argv[0], *remaining]
    module = importlib.import_module(targets[arguments.operation])
    if arguments.operation == "forecast":
        module.runner.main()
    elif arguments.operation == "compare":
        module.test_hybrid_forecast.main()
    elif arguments.operation == "validate":
        module.validator.main()
    elif arguments.operation == "rates":
        import derive_temperature_rates
        derive_temperature_rates.main()
    else:
        module.main()


if __name__ == "__main__":
    main()
