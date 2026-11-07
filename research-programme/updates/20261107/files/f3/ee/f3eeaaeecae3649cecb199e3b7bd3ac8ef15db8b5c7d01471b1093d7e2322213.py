import derive_temperature_rates as original
import tail_common
from stage169_common import ROOT
original.integrated_dc = tail_common.integrated_dc
original.ROOT = ROOT / "rate-audit"


if __name__ == "__main__":
    original.main()
