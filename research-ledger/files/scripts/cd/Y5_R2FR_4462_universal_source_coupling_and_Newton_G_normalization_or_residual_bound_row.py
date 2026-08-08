from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from source_coupling_newton_gate import (  # noqa: E402
    claim_gate_rows,
    coupling_theorem_rows,
    read_csv,
    residual_rows,
    source_law_rows,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4462"
CLAIM_ID = "L-304"
MARKER = "PPC4161_UNIVERSAL_SOURCE_COUPLING_AND_NEWTON_G_NORMALIZATION_4462"
PACKET_MARKER = "PPC4161_PACKET_UNIVERSAL_SOURCE_COUPLING_AND_NEWTON_G_NORMALIZATION_4462"
DECISION = "SOURCE_COUPLING_THEOREM_STRUCTURAL_G_CAL_AND_WEP_OPERATOR_FILLED_NUMERIC_G_NOT_PREDICTED_NONCLAIM"
NEXT_TARGET = "4463-Y5-R2FR-parent-kappa-scale-law-or-calibrated-G-residual-runner.md"

FORMAL_PATH = FORMAL / "478-PPC4161-universal-source-coupling-and-Newton-G-normalization-or-residual-bound-row.md"
DOC_PATH = POST / "4462-Y5-R2FR-universal-source-coupling-and-Newton-G-normalization-or-residual-bound-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4462_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4462_SOURCE_REGISTER.csv"
COUPLING_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4462_SOURCE_COUPLING_THEOREM.csv"
SOURCE_LAWS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4462_NEWTON_SOURCE_LAWS.csv"
RESIDUALS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4462_SOURCE_COUPLING_RESIDUAL_ROWS.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4462_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4462_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4462_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4462_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "source_coupling_newton_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4462_universal_source_coupling_and_Newton_G_normalization_or_residual_bound_row.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4461 = SOURCE_DIR / "P8_Y5_R2FR_4461_NEXT_TARGET.csv"
FORMAL_477 = FORMAL / "477-PPC4161-connection-hinge-refinement-owner-or-c2-scalaron-map.md"
FORMAL_184 = FORMAL / "184-PPC4161-parent-adopted-topological-kappa-sector.md"
FORMAL_186 = FORMAL / "186-PPC4161-Hamiltonian-worldtube-mass-readout-glue.md"
FORMAL_187 = FORMAL / "187-PPC4161-Poisson-Gauss-Newton-readout-from-Hamiltonian-source-charge.md"
FORMAL_188 = FORMAL / "188-PPC4161-full-PPN-readout-vector.md"
FORMAL_191 = FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md"
FORMAL_194 = FORMAL / "194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md"
FORMAL_195 = FORMAL / "195-PPC4161-local-GR-private-closure-summary-and-parent-adoption-burden-map.md"
FORMAL_200 = FORMAL / "200-PPC4161-Palatini-IR-normal-form-selector-under-AMF.md"
FORMAL_202 = FORMAL / "202-PPC4161-same-coframe-source-memory-zero-law.md"
DOC_1045 = POST / "1045-Y5-R10-parent-matter-functor-descent-signature-or-qbar-component-fill.md"
DOC_1012 = POST / "1012-Y5-R10-Y5-source-normalization-owner-or-q_loc-bound-implementation.md"
DOC_1013 = POST / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md"


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
        {"source_id": "SRC4462_00_next4461", "ref": NEXT_4461, "needle": "4462-Y5-R2FR-universal-source-coupling-and-Newton-G-normalization-or-residual-bound-row.md", "role": "4461 selected source coupling and Newton G normalization."},
        {"source_id": "SRC4462_01_formal477", "ref": FORMAL_477, "needle": "C_matter_and_Newton_G_normalization_selected_next", "role": "4461 handoff to C_matter and Newton G."},
        {"source_id": "SRC4462_02_kappa184", "ref": FORMAL_184, "needle": "D_A ln kappa_* = 0", "role": "topological kappa lock source."},
        {"source_id": "SRC4462_03_mass186", "ref": FORMAL_186, "needle": "Pi_M/H_tau/worldtube glue = 0 residual", "role": "Hamiltonian/Hilbert worldtube mass glue."},
        {"source_id": "SRC4462_04_newton187", "ref": FORMAL_187, "needle": "nabla^2 Phi_N = 4*pi G_N rho_H", "role": "weak-field Poisson/Newton readout."},
        {"source_id": "SRC4462_05_ppn188", "ref": FORMAL_188, "needle": "R_PPN =", "role": "formal PPN readout inside private packet."},
        {"source_id": "SRC4462_06_em191", "ref": FORMAL_191, "needle": "Poynting vector is not a separate background field", "role": "Maxwell-Hodge/Poynting Hilbert stress owner."},
        {"source_id": "SRC4462_07_g194", "ref": FORMAL_194, "needle": "G_cal := c^4 kappa_eff/(8*pi)", "role": "calibrated source-coupling law."},
        {"source_id": "SRC4462_08_summary195", "ref": FORMAL_195, "needle": "coherent private selector route", "role": "private local-GR closure burden map."},
        {"source_id": "SRC4462_09_palatini200", "ref": FORMAL_200, "needle": "structural Newton/GR reduction", "role": "Palatini IR selector source-coupling context."},
        {"source_id": "SRC4462_10_zero202", "ref": FORMAL_202, "needle": "delta_kappa = 0", "role": "same-coframe/source zero law."},
        {"source_id": "SRC4462_11_functor1045", "ref": DOC_1045, "needle": "parent matter functor contract is now exact", "role": "matter functor descent contract."},
        {"source_id": "SRC4462_12_y51012", "ref": DOC_1012, "needle": "Y5O1012_0_same_frame", "role": "source-normalization owner theorem attempt."},
        {"source_id": "SRC4462_13_flux1013", "ref": DOC_1013, "needle": "d(Pi_M J_H)=0", "role": "measured-GM flux closure obstruction."},
        {"source_id": "SRC4462_14_gate", "ref": GATE_PATH, "needle": "def coupling_theorem_rows", "role": "4462 source coupling gate."},
        {"source_id": "SRC4462_15_generator", "ref": GENERATOR_PATH, "needle": 'CHECKPOINT = "4462"', "role": "4462 generator script."},
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


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "structural_coupling_result": "G_cal=c^4*kappa_eff/(8*pi) and Newton/Poisson readout derived conditionally from same Hilbert source",
            "WEP_result": "eta_AB response operator filled symbolically; universal Hilbert coupling zeros it, species charge reopens it",
            "EM_result": "Poynting flux routed as Maxwell-Hodge Hilbert stress under same coframe",
            "numeric_G_prediction": False,
            "public_local_GR_claim": False,
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
            "coupling_status": "structural_calibrated_G_law_written",
            "matter_status": "same_Hilbert_source_theorem_conditional_not_global_parent_signed",
            "residual_status": "source_charge_species_frame_DeltaGamma_scalar_EM_residuals_retained",
            "numeric_G_prediction": False,
            "public_local_GR_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4462_0",
            "target": NEXT_TARGET,
            "objective": "Try to derive a parent scale law fixing kappa_eff numerically; if not, lock G as a calibrated constant and build the residual runner for delta_kappa, species charge, scalar alpha and WEP/PPN/R10/orbital bounds.",
            "derive_first": "seek a parent dimensionful invariant or topological flux quantization that fixes kappa_* without importing measured G",
            "fallback": "declare numeric G empirical like GR, while scoring only residual drift/coupling deviations",
            "risk": "pretending calibrated G is a prediction or hiding range/species dependence inside measured GM",
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
        "domain": "local_gr_newton_source_coupling",
        "claim": "MTS has a structural calibrated source-coupling route to Newton/Poisson dynamics inside the private selector, plus a symbolic WEP response operator for nonuniversal coupling.",
        "current_evidence": "4462 derives the Hilbert-source, kappa-to-G_cal, worldtube mass, Poisson/Newton, EM stress and WEP response laws conditionally; numeric G and global parent adoption remain unclaimed.",
        "status": "private_nonclaim_checkpoint",
        "next_test": NEXT_TARGET,
        "key_risk": "calibrated G may be mistaken for a numerical prediction; source residuals may be hidden inside fitted GM.",
        "sector": "local_gr_newton_em_wep",
        "evidence": str(FORMAL_PATH),
        "next_action": NEXT_TARGET,
        "risk": "fitted-G absorption or unsourced kappa scale law",
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
    theorem_rows: List[Dict[str, object]],
    law_rows: List[Dict[str, object]],
    residual_rows_: List[Dict[str, object]],
    claim_rows: List[Dict[str, object]],
    decisions: List[Dict[str, object]],
    statuses: List[Dict[str, object]],
    next_targets: List[Dict[str, object]],
) -> str:
    return f"""# 478 - PPC4161 Universal Source Coupling And Newton G Normalization Or Residual Bound Row

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4462 pins down the coupling. The local branch is no longer allowed to wave at "source coupling" as a vague missing piece. There are now two honest possibilities.

First, if the private selector is parent-adopted, ordinary matter, EM, clocks, photons and orbital readouts all see the same observed coframe. The source is one Hilbert tensor, the Poynting vector is the EM Hilbert momentum flux, the Hamiltonian worldtube charge defines mass before orbital readout, and the weak-field 00 equation gives `nabla^2 Phi_N = 4*pi G_cal rho_H` with `G_cal = c^4 kappa_eff/(8*pi)`.

Second, if that same-source route is not parent-signed, the failure is not a vibe. It is a residual vector: `delta_kappa`, species charge `C_A-C_B`, source charge `C_S`, frame leak `c_D/qbar_geom`, `DeltaGamma_WEP`, finite scalar `alpha_eff(lambda_R2)`, and EM side-channel leakage.

This still does not predict the numerical value of Newton's constant. It does something more modest but necessary: it derives the structural Newton/GR coupling law from a calibrated constant and makes every nonuniversal coupling leak testable instead of absorbable into fitted `GM`.

## Source Coupling Theorem

{table(theorem_rows)}

## Newton And Source Laws

{table(law_rows)}

## Residual Bound Rows

{table(residual_rows_)}

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
    return formal_body(*args).replace("# 478 - PPC4161", "# 4462 - Y5/R2FR")


def validation_rows(
    sources: List[Dict[str, object]],
    theorem_rows: List[Dict[str, object]],
    law_rows: List[Dict[str, object]],
    residual_rows_: List[Dict[str, object]],
    claim_rows: List[Dict[str, object]],
    csv_paths: Sequence[Path],
) -> List[Dict[str, object]]:
    parsed_ok = True
    malformed = []
    for path in csv_paths:
        try:
            read_csv(path)
        except Exception as exc:  # pragma: no cover - validation report
            parsed_ok = False
            malformed.append(f"{path.name}:{exc}")
    no_claim_true = all(str(row.get("valid_for_claim")).lower() != "true" for rows in [sources, theorem_rows, law_rows, residual_rows_, claim_rows] for row in rows)
    no_claim_allowed = all(str(row.get("claim_allowed")).lower() != "true" for row in theorem_rows + claim_rows)
    law_text = "\n".join(str(row) for row in law_rows)
    theorem_text = "\n".join(str(row) for row in theorem_rows)
    residual_symbols = {str(row.get("symbol")) for row in residual_rows_}
    rows = [
        {"check_id": "VAL4462_0_local_sources_exist", "passed": all(bool(row["local_path_exists"]) for row in sources), "detail": "all source paths exist"},
        {"check_id": "VAL4462_1_local_needles_found", "passed": all(bool(row["needle_found"]) for row in sources), "detail": "all source needles found"},
        {"check_id": "VAL4462_2_theorem_rows_present", "passed": len(theorem_rows) >= 8, "detail": "source coupling theorem rows present"},
        {"check_id": "VAL4462_3_newton_laws_present", "passed": "G_cal" in law_text and "nabla^2 Phi_N" in law_text and "a_r=-G_cal" in law_text, "detail": "G, Poisson and orbital laws present"},
        {"check_id": "VAL4462_4_EM_stress_present", "passed": "T_EM" in law_text and "Poynting" in formal_body(sources, theorem_rows, law_rows, residual_rows_, claim_rows, decision_rows(), status_rows(), next_rows()), "detail": "Maxwell/Poynting source law present"},
        {"check_id": "VAL4462_5_WEP_operator_present", "passed": "eta_AB" in theorem_text and "C_A-C_B" in theorem_text, "detail": "symbolic WEP response operator present"},
        {"check_id": "VAL4462_6_residual_vector_present", "passed": {"delta_kappa", "Delta_C_AB = C_A-C_B", "C_S", "c_D/qbar_geom", "DeltaGamma_WEP", "alpha_eff(lambda_R2)", "epsilon_EM_extra_inner"}.issubset(residual_symbols), "detail": "source coupling residual vector present"},
        {"check_id": "VAL4462_7_numeric_G_not_claimed", "passed": any(row.get("gate_id") == "CG4462_3_numeric_G" and not bool(row.get("gate_pass")) for row in claim_rows), "detail": "numeric G prediction is blocked"},
        {"check_id": "VAL4462_8_claims_blocked", "passed": no_claim_true and no_claim_allowed, "detail": "no generated row allows a public/local-GR claim"},
        {"check_id": "VAL4462_9_csv_parse", "passed": parsed_ok, "detail": "all generated CSVs parse" if parsed_ok else ";".join(malformed)},
        {"check_id": "VAL4462_10_formal_doc_written", "passed": FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "detail": str(FORMAL_PATH)},
        {"check_id": "VAL4462_11_post_doc_written", "passed": DOC_PATH.exists() and MARKER in text(DOC_PATH), "detail": str(DOC_PATH)},
        {"check_id": "VAL4462_12_claims_register_updated", "passed": CLAIM_ID in text(CLAIMS_PATH), "detail": CLAIM_ID},
        {"check_id": "VAL4462_13_next_selected", "passed": NEXT_TARGET in text(NEXT_CSV), "detail": NEXT_TARGET},
        {"check_id": "VAL4462_14_pycache_absent", "passed": not (SCRIPT_DIR / "__pycache__").exists(), "detail": "scripts __pycache__ absent"},
    ]
    rows.append({"check_id": "VAL4462_OVERALL", "passed": all(bool(row["passed"]) for row in rows), "detail": "4462 universal source coupling and Newton G normalization checkpoint"})
    return rows


def main() -> None:
    sources = source_rows()
    theorem_rows = coupling_theorem_rows()
    law_rows = source_law_rows()
    residual_rows_ = residual_rows()
    claim_rows = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(COUPLING_THEOREM_CSV, theorem_rows)
    write_csv(SOURCE_LAWS_CSV, law_rows)
    write_csv(RESIDUALS_CSV, residual_rows_)
    write_csv(CLAIM_GATES_CSV, claim_rows)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)

    write_text(FORMAL_PATH, formal_body(sources, theorem_rows, law_rows, residual_rows_, claim_rows, decisions, statuses, next_targets))
    write_text(DOC_PATH, post_body(sources, theorem_rows, law_rows, residual_rows_, claim_rows, decisions, statuses, next_targets))
    update_claims_register()

    append_section_once(
        SPINE_PATH,
        MARKER,
        "4462 Universal Source Coupling",
        "4462 derives the structural calibrated source-coupling route: same Hilbert source, Maxwell-Hodge/Poynting stress ownership, Hamiltonian worldtube mass, Poisson/Newton readout and G_cal=c^4 kappa_eff/(8*pi). It also fills the symbolic WEP response operator and retains all nonuniversal coupling leaks as residual rows. Numeric G is not predicted.",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        "4462 Packet Integration",
        "The private local packet now has a source-coupling spine: universal same-coframe Hilbert matter gives Newton/Poisson with calibrated G, while any nonuniversal scalar/source/frame/connection/EM leakage becomes an explicit WEP/PPN/R10/clock/orbital residual rather than a fitted-G shortcut.",
    )

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    csv_paths = [
        SOURCE_REGISTER,
        COUPLING_THEOREM_CSV,
        SOURCE_LAWS_CSV,
        RESIDUALS_CSV,
        CLAIM_GATES_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    validations = validation_rows(sources, theorem_rows, law_rows, residual_rows_, claim_rows, csv_paths)
    write_csv(VALIDATION_PATH, validations)

    failed = [row for row in validations if not bool(row["passed"])]
    if failed:
        raise SystemExit(f"4462 validation failed: {failed}")
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
