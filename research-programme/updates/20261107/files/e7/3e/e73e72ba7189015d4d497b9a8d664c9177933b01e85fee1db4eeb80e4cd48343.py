from scipy import interpolate
import hybrid_reference_common
import hybrid_temperature_common
import freeze_hybrid_forecast as runner
hybrid_temperature_common.interpolate = interpolate


if __name__ == "__main__":
    runner.main()
