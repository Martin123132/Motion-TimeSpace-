from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
C3_TEX = POST / "source-intake" / "functional_rg" / "4929" / "src2312" / "ess_cubic.tex"
PHOTON_TEX = POST / "source-intake" / "functional_rg" / "4932" / "src-2405.08860" / "WGCqg.tex"
OUTPUT_DIR = POST / "source-intake" / "functional_rg" / "4934"
OUTPUT_JSON = OUTPUT_DIR / "c3_photon_projection_selection_results.json"
MARKER = "MTS_4934_C3_PHOTON_PROJECTION_SELECTION"


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    c3_text = C3_TEX.read_text(encoding="utf-8")
    photon_text = PHOTON_TEX.read_text(encoding="utf-8")
    required_c3 = (
        "G_{C^3} C^{\\rho \\sigma}",
        "g_{C^3} = k^2 G_{C^3}",
        "propagator on a conformally flat spacetime coincides",
    )
    required_photon = (
        "G_{CFF} \\, C^{\\mu\\nu\\rho\\sigma} F_{\\mu\\nu} F_{\\rho\\sigma}",
        "F^{\\mu\\nu} \\Delta F_{\\mu\\nu}",
        "S^{\\mu\\nu} F_{\\mu\\alpha} F^\\alpha_{\\phantom{\\alpha}\\nu}",
    )
    missing_markers = [marker for marker in required_c3 if marker not in c3_text]
    missing_markers.extend(marker for marker in required_photon if marker not in photon_text)
    if missing_markers:
        raise RuntimeError(f"source markers missing: {missing_markers}")

    projections = [
        {
            "row": "F2",
            "photon_order": 2,
            "curvature_irrep": "none",
            "direct_C3_Hessian_allowed": False,
            "reason": "the row is evaluated at curvature degree zero while delta2(C3) vanishes at Cbar=0",
        },
        {
            "row": "FDeltaF",
            "photon_order": 2,
            "curvature_irrep": "none",
            "direct_C3_Hessian_allowed": False,
            "reason": "photon derivatives do not supply a background Weyl tensor and delta2(C3) vanishes at Cbar=0",
        },
        {
            "row": "RFF",
            "photon_order": 2,
            "curvature_irrep": "Ricci scalar",
            "direct_C3_Hessian_allowed": False,
            "reason": "the Hessian linear in background curvature is Weyl-linear and cannot project onto the scalar-curvature irrep",
        },
        {
            "row": "SFF",
            "photon_order": 2,
            "curvature_irrep": "tracefree Ricci",
            "direct_C3_Hessian_allowed": False,
            "reason": "the Hessian linear in background curvature is Weyl-linear and cannot project onto the tracefree-Ricci irrep",
        },
        {
            "row": "F2sq",
            "photon_order": 4,
            "curvature_irrep": "none",
            "direct_C3_Hessian_allowed": False,
            "reason": "four photon fields do not replace the required background Weyl tensor",
        },
        {
            "row": "F4",
            "photon_order": 4,
            "curvature_irrep": "none",
            "direct_C3_Hessian_allowed": False,
            "reason": "four photon fields do not replace the required background Weyl tensor",
        },
        {
            "row": "CFF",
            "photon_order": 2,
            "curvature_irrep": "Weyl",
            "direct_C3_Hessian_allowed": True,
            "reason": "this is the unique parity-even scalar linear in Cbar and quadratic in F",
        },
    ]
    forbidden_rows = [row["row"] for row in projections if not row["direct_C3_Hessian_allowed"]]
    allowed_rows = [row["row"] for row in projections if row["direct_C3_Hessian_allowed"]]
    result = {
        "marker": MARKER,
        "c3_source": C3_TEX.relative_to(ROOT).as_posix(),
        "c3_source_sha256": digest(C3_TEX),
        "photon_source": PHOTON_TEX.relative_to(ROOT).as_posix(),
        "photon_source_sha256": digest(PHOTON_TEX),
        "same_variation_formula": {
            "action": "I_C3=h int sqrt(g) Tr(C^3)",
            "second_variation": "delta2 I_C3=h int sqrt(g)[6 Tr(Cbar deltaC deltaC)+3 Tr(Cbar^2 delta2C)+measure/index terms of order Cbar^2 or Cbar^3]",
            "conformally_flat_value": "delta2 I_C3|Cbar=0=0",
            "linear_curvature_value": "delta2 I_C3|O(curvature)=6h int sqrt(g) Tr(Cbar deltaC deltaC)",
        },
        "projection_theorem": {
            "statement": "At first order in background curvature and any photon order retained by the four-derivative source basis, the direct C3 Hessian can feed only the CFF projection.",
            "assumptions": [
                "parity even source action",
                "background-field expansion analytic at Cbar=0",
                "regulator independent of h_C3 as in the source minimal-essential setup",
                "projection basis separates scalar Ricci tracefree Ricci and Weyl irreducible curvature",
            ],
            "forbidden_rows": forbidden_rows,
            "allowed_rows": allowed_rows,
            "rows_eliminated": len(forbidden_rows),
            "rows_remaining": len(allowed_rows),
        },
        "rows": projections,
        "claim_boundary": {
            "CFF_coefficient_derived": False,
            "full_direct_block_closed": False,
            "reason": "the unique CFF source coefficient still requires the C3 metric Hessian contraction with the photon-background trace",
        },
    }
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"{MARKER}_ZERO_ROWS={forbidden_rows}", flush=True)
    print(f"{MARKER}_REMAINING_ROWS={allowed_rows}", flush=True)
    print(f"{MARKER}_OUTPUT_SHA256={digest(OUTPUT_JSON)}", flush=True)
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
