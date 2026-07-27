from __future__ import annotations

import csv
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from connection_hinge_scalaron_gate import (  # noqa: E402
    as_float,
    claim_gate_rows,
    fork_decision_rows,
    owner_theorem_rows,
    read_csv,
    scalaron_map_rows,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4461"
CLAIM_ID = "L-303"
MARKER = "PPC4161_CONNECTION_HINGE_REFINEMENT_OWNER_OR_C2_SCALARON_MAP_4461"
PACKET_MARKER = "PPC4161_PACKET_CONNECTION_HINGE_REFINEMENT_OWNER_OR_C2_SCALARON_MAP_4461"
DECISION = "CONNECTION_HINGE_OWNER_REDUCED_TO_PARENT_INVENTORY_AND_C2_SCALARON_MAP_FILLED_NONCLAIM"
NEXT_TARGET = "4462-Y5-R2FR-universal-source-coupling-and-Newton-G-normalization-or-residual-bound-row.md"

FORMAL_PATH = FORMAL / "477-PPC4161-connection-hinge-refinement-owner-or-c2-scalaron-map.md"
DOC_PATH = POST / "4461-Y5-R2FR-connection-hinge-refinement-owner-or-c2-scalaron-map.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4461_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4461_SOURCE_REGISTER.csv"
OWNER_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4461_OWNER_COMPATIBILITY_THEOREM.csv"
SCALARON_MAP_CSV = SOURCE_DIR / "P8_Y5_R2FR_4461_C2_SCALARON_OBSERVABLE_MAP.csv"
FORK_DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4461_FORK_DECISION.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4461_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4461_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4461_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4461_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "connection_hinge_scalaron_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4461_connection_hinge_refinement_owner_or_c2_scalaron_map.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4460 = SOURCE_DIR / "P8_Y5_R2FR_4460_NEXT_TARGET.csv"
FORMAL_476 = FORMAL / "476-PPC4161-parent-refinement-gauge-signature-or-visible-c2-finite-row.md"
REGION_4458 = SOURCE_DIR / "P8_Y5_R2FR_4458_MTS_BASIS_COEFFICIENT_REGION.csv"
BOUNDS_4457 = SOURCE_DIR / "P8_Y5_R2FR_4457_COEFFICIENT_REGION_BOUNDS.csv"
DOC_1826 = POST / "1826-Y5-R2FR-log-holonomy-action-owner-or-trace-norm-c2-prior.md"
DOC_1827 = POST / "1827-Y5-R2FR-Palatini-Regge-field-match-or-c2-scalaron-map.md"
DOC_1828 = POST / "1828-Y5-R2FR-connection-hinge-bivector-owner-or-c2-map-fill.md"
DOC_2149 = POST / "2149-Y5-R2FR-connection-hinge-bivector-owner-or-c2-map-fill.md"
DOC_1836 = POST / "1836-Y5-R2FR-DeltaGamma-WEP-clock-lightcone-projection-skeleton.md"


def text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for line_number, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return line_number
    return 0


def md(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def table(rows: Sequence[Mapping[str, object]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    output = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        output.append("| " + " | ".join(md(row.get(header, "")) for header in headers) + " |")
    return "\n".join(output)


def source_specs() -> List[Dict[str, object]]:
    return [
        {"source_id": "SRC4461_00_next4460", "ref": NEXT_4460, "needle": "4461-Y5-R2FR-connection-hinge-refinement-owner-or-c2-scalaron-map.md", "role": "4460 selected connection/hinge ownership or c2 scalaron map."},
        {"source_id": "SRC4461_01_formal476", "ref": FORMAL_476, "needle": "RGC4460_4_geometry_owner", "role": "parent refinement contract names the geometry owner gap."},
        {"source_id": "SRC4461_02_region4458", "ref": REGION_4458, "needle": "REG4458_2_pure_R2_scalar_only", "role": "pure R2 normalization and D0=12*c_R2 guard."},
        {"source_id": "SRC4461_03_bounds4457", "ref": BOUNDS_4457, "needle": "QB4457_0_scalar_D0", "role": "private scalar D0 bound pressure used for lambda_R2 pressure."},
        {"source_id": "SRC4461_04_log1826", "ref": DOC_1826, "needle": "Log(U_h) is gauge-covariant", "role": "log-holonomy scalar requires an owned bivector contraction."},
        {"source_id": "SRC4461_05_field1827", "ref": DOC_1827, "needle": "MISSING_CONNECTION_COMPATIBILITY", "role": "Palatini field match blocker."},
        {"source_id": "SRC4461_06_hinge1828", "ref": DOC_1828, "needle": "MTS cell/domain grammar does not yet define Regge hinges", "role": "hinge owner blocker."},
        {"source_id": "SRC4461_07_delta2149", "ref": DOC_2149, "needle": "distortion equation", "role": "independent connection falls into DeltaGamma residual-vector equation."},
        {"source_id": "SRC4461_08_wep1836", "ref": DOC_1836, "needle": "P_WEP", "role": "source-coupling response remains the live local projection gap."},
        {"source_id": "SRC4461_09_gate", "ref": GATE_PATH, "needle": "def owner_theorem_rows", "role": "4461 theorem/scalaron gate."},
        {"source_id": "SRC4461_10_generator", "ref": GENERATOR_PATH, "needle": 'CHECKPOINT = "4461"', "role": "4461 generator script."},
    ]


def source_rows() -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for spec in source_specs():
        path = Path(spec["ref"])
        needle = str(spec["needle"])
        line = line_of(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": spec["source_id"],
                "source_kind": "local",
                "source_ref": str(path),
                "local_path_exists": path.exists(),
                "needle": needle,
                "needle_found": line > 0,
                "line_number": line,
                "role": spec["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def d0_bound() -> float | None:
    try:
        rows = read_csv(BOUNDS_4457)
    except FileNotFoundError:
        return None
    scalar = next((row for row in rows if row.get("bound_id") == "QB4457_0_scalar_D0"), None)
    return as_float(scalar.get("coefficient_upper_bound_m2")) if scalar else None


def c_r2_bound_from_d0(d0_bound_m2: float | None) -> float | None:
    if d0_bound_m2 is None:
        return None
    return d0_bound_m2 / 12.0


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "connection_result": "exact owner criterion written; parent inventory/source silence unsigned",
            "hinge_result": "B_h/A_h and Log(U_h) scalar contraction derived conditionally; cell/orientation/refinement owner unsigned",
            "scaloron_result": "finite c2 branch now maps to c_R2_eff, lambda_R2, alpha_eff, Yukawa potential and PPN/R10 guards",
            "local_GR_public_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "geometry_status": "conditional_owner_theorems_written_not_parent_signed",
            "finite_c2_status": "scaloron_observable_map_filled_symbolically_nonclaim",
            "coupling_status": "C_matter_and_Newton_G_normalization_selected_next",
            "local_GR_public_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4461_0",
            "target": NEXT_TARGET,
            "objective": "Derive the universal matter/source coupling that fixes Newton G, scalaron alpha_eff and DeltaGamma WEP/source-frame response, or retain a sourced residual-bound row.",
            "derive_first": "prove ordinary matter, clocks, photons and orbital source charge descend through one observed coframe with one Hilbert/Noether mass normalization",
            "fallback": "stage C_matter, G_eff, eta_AB, alpha(lambda), PPN gamma and orbital GM residual rows with valid_for_claim=false",
            "risk": "absorbing coupling errors into fitted G or assuming universal metric coupling without parent proof",
            "valid_for_claim": False,
        }
    ]


def update_claims_register() -> None:
    rows = read_csv(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    fieldnames = list(rows[0].keys()) if rows else ["claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk", "sector", "evidence", "next_action", "risk"]
    claim_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_derivation",
        "claim": "MTS connection/hinge ownership reduces either to a parent coframe-only/Palatini geometry theorem or to explicit DeltaGamma plus finite c2 scalaron residual maps.",
        "current_evidence": "4461 writes the exact owner criteria and fills the c2-to-scalaron/Yukawa/PPN/R10 formula map, but no parent coupling or coefficient value is sourced.",
        "status": "private_nonclaim_checkpoint",
        "next_test": NEXT_TARGET,
        "key_risk": "universal matter coupling or Newton G normalization may be assumed rather than derived.",
        "sector": "local_gr_newton_source_coupling",
        "evidence": str(FORMAL_PATH),
        "next_action": NEXT_TARGET,
        "risk": "smuggled metric coupling or fitted-G absorption",
    }
    rows.append({key: claim_row.get(key, "") for key in fieldnames})
    write_csv(CLAIMS_PATH, rows)


def append_section_once(path: Path, marker: str, title: str, body: str) -> None:
    current = text(path)
    if marker in current:
        return
    addition = f"\n\n## {title}\n\nMarker: `{marker}`\n\n{body.strip()}\n"
    write_text(path, current.rstrip() + addition + "\n")


def formal_body(
    sources: List[Dict[str, object]],
    owner_rows: List[Dict[str, object]],
    scalaron_rows: List[Dict[str, object]],
    fork_rows: List[Dict[str, object]],
    claim_rows: List[Dict[str, object]],
    decisions: List[Dict[str, object]],
    statuses: List[Dict[str, object]],
    next_targets: List[Dict[str, object]],
) -> str:
    return f"""# 477 - PPC4161 Connection Hinge Refinement Owner Or c2 Scalaron Map

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4461 does the next non-circular move. It does not merely say that `Gamma_eff`, `Log(U_h)`, `B_h/A_h`, `c2_visible`, and the scalar coupling are missing. It writes the exact mathematical contract under which the local-GR route would close, and it fills the fallback finite-`c2` branch into an actual scalaron/Yukawa/PPN/R10 map.

The clean route is now precise: either the parent field inventory is coframe/metric-only, or an independent connection is varied and forced to zero by a signed, positive algebraic connection equation with no source/projective/boundary leakage. The hinge route is also precise: an owned oriented two-chain plus descended coframe gives `B_h`; an owned connection gives `Log(U_h)`; their invariant contraction gives the signed deficit. Only then does the refinement theorem kill same-channel `c2`.

The fallback is also sharper: if the parent owns a trace/norm/even holonomy cost or a physical grain, the finite branch maps through `c_R2_eff`, `lambda_R2`, `alpha_eff`, a Yukawa potential, and PPN/R10 gates. That map is formula-ready but not claim-ready because the parent has not supplied `c2_visible`, `ell_cell`, `N_EH`, `C_matter`, or the live bound curve.

## Owner Compatibility Theorem

{table(owner_rows)}

## Finite c2 Scalaron Observable Map

{table(scalaron_rows)}

## Fork Decision

{table(fork_rows)}

## Claim Gates

{table(claim_rows)}

## Decision

{table(decisions)}

## Status

{table(statuses)}

## Next Target

{table(next_targets)}

## Source Register

{table(sources)}
"""


def post_body(*args: object) -> str:
    return formal_body(*args).replace("# 477 - PPC4161", "# 4461 - Y5/R2FR")


def validation_rows(
    sources: List[Dict[str, object]],
    owner_rows: List[Dict[str, object]],
    scalaron_rows: List[Dict[str, object]],
    fork_rows: List[Dict[str, object]],
    claim_rows: List[Dict[str, object]],
    csv_paths: Sequence[Path],
) -> List[Dict[str, object]]:
    no_claim_true = all(str(row.get("valid_for_claim")).lower() != "true" for rows in [sources, owner_rows, scalaron_rows, fork_rows, claim_rows] for row in rows)
    no_claim_allowed = all(str(row.get("claim_allowed")).lower() != "true" for row in owner_rows + claim_rows)
    parsed_ok = True
    malformed = []
    for path in csv_paths:
        try:
            read_csv(path)
        except Exception as exc:  # pragma: no cover - validation report
            parsed_ok = False
            malformed.append(f"{path.name}:{exc}")
    lambda_row = next((row for row in scalaron_rows if row.get("map_id") == "SM4461_2_scalon_range"), None)
    lambda_present = False
    if lambda_row is None:
        lambda_row = next((row for row in scalaron_rows if row.get("map_id") == "SM4461_2_scalaron_range"), None)
    if lambda_row is not None:
        lambda_present = as_float(lambda_row.get("derived_value")) is not None and as_float(lambda_row.get("derived_value")) > 0
    rows = [
        {"check_id": "VAL4461_0_local_sources_exist", "passed": all(bool(row["local_path_exists"]) for row in sources), "detail": "all source paths exist"},
        {"check_id": "VAL4461_1_local_needles_found", "passed": all(bool(row["needle_found"]) for row in sources), "detail": "all source needles found"},
        {"check_id": "VAL4461_2_owner_theorems_present", "passed": len(owner_rows) >= 5, "detail": "connection, distortion, hinge, log and refinement theorem rows present"},
        {"check_id": "VAL4461_3_connection_not_promoted", "passed": any(row.get("theorem_id") == "OCT4461_0_connection_owner" and not bool(row.get("claim_allowed")) for row in owner_rows), "detail": "connection owner remains conditional"},
        {"check_id": "VAL4461_4_hinge_log_not_promoted", "passed": any(row.get("theorem_id") == "OCT4461_3_log_holonomy_scalar" and not bool(row.get("claim_allowed")) for row in owner_rows), "detail": "log-holonomy scalar derivation is nonclaim"},
        {"check_id": "VAL4461_5_scalaron_formulas_filled", "passed": all(any(token in str(row.get("formula")) for row in scalaron_rows) for token in ["lambda_R2", "alpha_eff", "V(r)", "gamma(r)-1"]), "detail": "finite c2 branch has range, coupling, Yukawa and PPN formulas"},
        {"check_id": "VAL4461_6_bound_pressure_numeric", "passed": lambda_present, "detail": "current D0 pressure produces a positive lambda_R2 pressure number"},
        {"check_id": "VAL4461_7_forks_declared", "passed": len(fork_rows) == 3, "detail": "clean GR, connection residual and finite c2 forks declared"},
        {"check_id": "VAL4461_8_claims_blocked", "passed": no_claim_true and no_claim_allowed, "detail": "no generated row allows a public/local-GR claim"},
        {"check_id": "VAL4461_9_csv_parse", "passed": parsed_ok, "detail": "all generated CSVs parse" if parsed_ok else ";".join(malformed)},
        {"check_id": "VAL4461_10_formal_doc_written", "passed": FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "detail": str(FORMAL_PATH)},
        {"check_id": "VAL4461_11_post_doc_written", "passed": DOC_PATH.exists() and MARKER in text(DOC_PATH), "detail": str(DOC_PATH)},
        {"check_id": "VAL4461_12_claims_register_updated", "passed": CLAIM_ID in text(CLAIMS_PATH), "detail": CLAIM_ID},
        {"check_id": "VAL4461_13_next_selected", "passed": NEXT_TARGET in text(NEXT_CSV), "detail": NEXT_TARGET},
        {"check_id": "VAL4461_14_pycache_absent", "passed": not (SCRIPT_DIR / "__pycache__").exists(), "detail": "scripts __pycache__ absent"},
    ]
    rows.append({"check_id": "VAL4461_OVERALL", "passed": all(bool(row["passed"]) for row in rows), "detail": "4461 connection/hinge owner or c2 scalaron map checkpoint"})
    return rows


def main() -> None:
    d0 = d0_bound()
    c_r2 = c_r2_bound_from_d0(d0)
    sources = source_rows()
    owner_rows = owner_theorem_rows()
    scalaron_rows = scalaron_map_rows(d0, c_r2)
    fork_rows = fork_decision_rows()
    claim_rows = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(OWNER_THEOREM_CSV, owner_rows)
    write_csv(SCALARON_MAP_CSV, scalaron_rows)
    write_csv(FORK_DECISION_CSV, fork_rows)
    write_csv(CLAIM_GATES_CSV, claim_rows)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)

    write_text(FORMAL_PATH, formal_body(sources, owner_rows, scalaron_rows, fork_rows, claim_rows, decisions, statuses, next_targets))
    write_text(DOC_PATH, post_body(sources, owner_rows, scalaron_rows, fork_rows, claim_rows, decisions, statuses, next_targets))
    update_claims_register()

    append_section_once(
        SPINE_PATH,
        MARKER,
        "4461 Connection Hinge And c2 Scalaron Map",
        "4461 writes the exact conditional owner theorem for the local geometry route and fills the finite c2 fallback into scalaron/Yukawa/PPN/R10 formulas. It does not claim local GR: parent ownership, source coupling and Newton normalization remain open.",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        "4461 Packet Integration",
        "The local packet now has a concrete fork: parent-owned coframe/connection/hinge plus linear signed deficit would activate the refinement zero-selector; otherwise finite c2 maps to c_R2_eff, lambda_R2, alpha_eff, Yukawa, PPN gamma and R10 gates as nonclaim residuals.",
    )

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    csv_paths = [
        SOURCE_REGISTER,
        OWNER_THEOREM_CSV,
        SCALARON_MAP_CSV,
        FORK_DECISION_CSV,
        CLAIM_GATES_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    validations = validation_rows(sources, owner_rows, scalaron_rows, fork_rows, claim_rows, csv_paths)
    write_csv(VALIDATION_PATH, validations)

    failed = [row for row in validations if not bool(row["passed"])]
    if failed:
        raise SystemExit(f"4461 validation failed: {failed}")
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
