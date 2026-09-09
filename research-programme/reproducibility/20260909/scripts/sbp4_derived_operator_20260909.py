import hashlib
import json
from fractions import Fraction
from pathlib import Path

import numpy as numerical


DIRECTORY = Path(__file__).resolve().parents[1] / "source-intake/navier-stokes/20260909/sbp4-operator-derived"
STATUS = json.loads((DIRECTORY / "status.json").read_text())
PAYLOAD = (DIRECTORY / "coefficients.json").read_bytes()
if STATUS["state"] != "complete" or STATUS["passed"] != 8 or not (DIRECTORY / "COMPLETE").is_file() or hashlib.sha256(PAYLOAD).hexdigest() != STATUS["coefficient_sha256"]:
    raise ValueError("Unverified SBP closure")
LEFT = numerical.array([[float(Fraction(value)) for value in row] for row in json.loads(PAYLOAD)["left_derivative"]])


def derivative(values, spacing):
    if values.shape[-1] < 9:
        raise ValueError("SBP fourth-order operator requires at least nine nodes")
    result = numerical.empty_like(values)
    result[..., 4:-4] = (values[..., 2:-6] - 8 * values[..., 3:-5] + 8 * values[..., 5:-3] - values[..., 6:-2]) / (12 * spacing)
    result[..., :4] = numerical.einsum("ij,...j->...i", LEFT, values[..., :6]) / spacing
    result[..., -4:] = -numerical.einsum("ij,...j->...i", LEFT, values[..., -1:-7:-1])[..., ::-1] / spacing
    return result
