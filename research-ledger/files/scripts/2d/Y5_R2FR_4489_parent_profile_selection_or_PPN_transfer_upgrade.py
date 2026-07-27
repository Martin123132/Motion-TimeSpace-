from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from parent_profile_transfer_gate import (  # noqa: E402
    claim_gate_rows,
    decision_ledger_rows,
    el_profile_rows,
    interface_gluing_rows,
    parent_requirement_rows,
    profile_selection_rows,
    read_csv,
    transfer_sensitivity_rows,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4489"
CLAIM_ID = "L-331"
MARKER = "PPC4161_PARENT_PROFILE_SELECTION_OR_PPN_TRANSFER_UPGRADE_4489"
PACKET_MARKER = "PPC4161_PACKET_PARENT_PROFILE_SELECTION_OR_PPN_TRANSFER_UPGRADE_4489"
DECISION = "TOY_PROFILE_EL_SOLVED_NATURAL_INTERFACE_REJECTED_GLUING_MULTIPLIER_ROUTE_AND_TRANSFER_CRITICALS_NONCLAIM"
NEXT_TARGET = "4490-Y5-R2FR-gluing-multiplier-parent-origin-or-PPN-transfer-matrix.md"

FORMAL_PATH = FORMAL / "505-PPC4161-parent-profile-selection-or-PPN-transfer-upgrade.md"
DOC_PATH = POST / "4489-Y5-R2FR-parent-profile-selection-or-PPN-transfer-upgrade.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4489_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4489_SOURCE_REGISTER.csv"
EL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4489_EL_PROFILE_DERIVATION.csv"
SELECTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4489_PROFILE_SELECTION_ROWS.csv"
INTERFACE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4489_INTERFACE_GLUING_ROWS.csv"
TRANSFER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4489_TRANSFER_SENSITIVITY_ROWS.csv"
REQ_CSV = SOURCE_DIR / "P8_Y5_R2FR_4489_PARENT_REQUIREMENT_ROWS.csv"
DECISION_LEDGER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4489_DECISION_LEDGER.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4489_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4489_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4489_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4489_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "parent_profile_transfer_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4489_parent_profile_selection_or_PPN_transfer_upgrade.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

FORMAL_504 = FORMAL / "504-PPC4161-PH-source-profile-row-or-parent-zero-transfer-upgrade.md"
NEXT_4488 = SOURCE_DIR / "P8_Y5_R2FR_4488_NEXT_TARGET.csv"
PROFILE_4488 = SOURCE_DIR / "P8_Y5_R2FR_4488_SMOOTH_PROFILE_ROWS.csv"
TRANSFER_4488 = SOURCE_DIR / "P8_Y5_R2FR_4488_TRANSFER_STATUS.csv"
DOC_3190 = POST / "3190-Y5-R2FR-parent-profile-selection-or-PPN-transfer-upgrade-under-AX1090.md"
SEL_3190 = SOURCE_DIR / "P8_Y5_R2FR_3190_PROFILE_SELECTION_CANDIDATE.csv"
PT_3190 = SOURCE_DIR / "P8_Y5_R2FR_3190_PPN_TRANSFER_UPGRADE_CONTRACT.csv"
SCAN_3190 = SOURCE_DIR / "P8_Y5_R2FR_3190_SMOOTHSTEP_WIDTH_SCAN.csv"
DOC_3191 = POST / "3191-Y5-R2FR-selected-profile-transfer-runner-or-parent-action-profile-equation-under-AX1090.md"
RUN_3191 = SOURCE_DIR / "P8_Y5_R2FR_3191_SELECTED_PROFILE_TRANSFER_RUNNER.csv"
CRIT_3191 = SOURCE_DIR / "P8_Y5_R2FR_3191_TRANSFER_TIGHTENING_CRITICALS.csv"
PE_3191 = SOURCE_DIR / "P8_Y5_R2FR_3191_PARENT_PROFILE_EQUATION_CONTRACT.csv"
DOC_3192 = POST / "3192-Y5-R2FR-solve-quadratic-profile-EL-or-upgrade-slip-transfer-bound-under-AX1090.md"
EL_3192 = SOURCE_DIR / "P8_Y5_R2FR_3192_EL_OPERATOR_DERIVATION.csv"
SEL_3192 = SOURCE_DIR / "P8_Y5_R2FR_3192_EL_STATIONARY_SELECTION.csv"
DEC_3192 = SOURCE_DIR / "P8_Y5_R2FR_3192_PROFILE_DECISION.csv"
DOC_3193 = POST / "3193-Y5-R2FR-parent-boundary-regularity-or-natural-boundary-layer-under-AX1090.md"
IC_3193 = SOURCE_DIR / "P8_Y5_R2FR_3193_INTERFACE_CONDITION_DERIVATION.csv"
SEL_3193 = SOURCE_DIR / "P8_Y5_R2FR_3193_BOUNDARY_MOMENTUM_SELECTION.csv"
DEC_3193 = SOURCE_DIR / "P8_Y5_R2FR_3193_DECISION.csv"
DOC_3194 = POST / "3194-Y5-R2FR-source-owned-boundary-layer-action-or-modified-parent-profile-functional-under-AX1090.md"
GLUE_3194 = SOURCE_DIR / "P8_Y5_R2FR_3194_C1_GLUING_MULTIPLIER_DERIVATION.csv"
SOL_3194 = SOURCE_DIR / "P8_Y5_R2FR_3194_MULTIPLIER_SOLUTIONS.csv"
CLASS_3194 = SOURCE_DIR / "P8_Y5_R2FR_3194_CLOSURE_CLASSIFICATION.csv"


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
        {"source_id": "SRC4489_00_next4488", "ref": NEXT_4488, "needle": "4489-Y5-R2FR-parent-profile-selection-or-PPN-transfer-upgrade.md", "role": "4488 selected parent profile/transfer target."},
        {"source_id": "SRC4489_01_formal504", "ref": FORMAL_504, "needle": "parent_profile_selection_coupling_owner_or_PPN_transfer_upgrade", "role": "4488 status frontier."},
        {"source_id": "SRC4489_02_profile4488", "ref": PROFILE_4488, "needle": "SP4488_width_0.40", "role": "4488 smooth profile rows."},
        {"source_id": "SRC4489_03_transfer4488", "ref": TRANSFER_4488, "needle": "TR4488_0_current_proxy", "role": "4488 transfer proxy status."},
        {"source_id": "SRC4489_04_doc3190", "ref": DOC_3190, "needle": "w = 0.435", "role": "3190 min-N4 smoothstep profile candidate."},
        {"source_id": "SRC4489_05_sel3190", "ref": SEL_3190, "needle": "SEL3190_0_min_N4_candidate", "role": "3190 profile selection row."},
        {"source_id": "SRC4489_06_pt3190", "ref": PT_3190, "needle": "PT3190_0_observable_transfer", "role": "3190 PPN transfer contract."},
        {"source_id": "SRC4489_07_scan3190", "ref": SCAN_3190, "needle": "SCAN3190_w0.435", "role": "3190 width scan selected row."},
        {"source_id": "SRC4489_08_doc3191", "ref": DOC_3191, "needle": "D2^dagger[x^4 D2[F]] = 0", "role": "3191 parent profile equation contract."},
        {"source_id": "SRC4489_09_run3191", "ref": RUN_3191, "needle": "RUN3191_c1.000000e+09_tf1e+00", "role": "3191 selected profile transfer runner."},
        {"source_id": "SRC4489_10_crit3191", "ref": CRIT_3191, "needle": "CRIT3191_c1e+09", "role": "3191 transfer criticals."},
        {"source_id": "SRC4489_11_pe3191", "ref": PE_3191, "needle": "PE3191_2_Euler_Lagrange_contract", "role": "3191 EL contract."},
        {"source_id": "SRC4489_12_doc3192", "ref": DOC_3192, "needle": "F_EL(x)=A+B x^2+C/x+D/x^3", "role": "3192 exact EL profile solution."},
        {"source_id": "SRC4489_13_el3192", "ref": EL_3192, "needle": "EL3192_7_general_transition_solution", "role": "3192 machine EL solution."},
        {"source_id": "SRC4489_14_sel3192", "ref": SEL_3192, "needle": "SEL3192_1_min_N4_exact_EL_scan", "role": "3192 exact EL profile selections."},
        {"source_id": "SRC4489_15_dec3192", "ref": DEC_3192, "needle": "DEC3192_3_boundary_regularization_gate", "role": "3192 boundary regularization decision."},
        {"source_id": "SRC4489_16_doc3193", "ref": DOC_3193, "needle": "pure natural-interface route is rejected", "role": "3193 natural interface no-go."},
        {"source_id": "SRC4489_17_ic3193", "ref": IC_3193, "needle": "IC3193_5_interface_condition", "role": "3193 interface condition derivation."},
        {"source_id": "SRC4489_18_sel3193", "ref": SEL_3193, "needle": "SEL3193_0_3190_width", "role": "3193 boundary momentum selections."},
        {"source_id": "SRC4489_19_dec3193", "ref": DEC_3193, "needle": "DEC3193_1_no_go", "role": "3193 no-go decision."},
        {"source_id": "SRC4489_20_doc3194", "ref": DOC_3194, "needle": "C1 gluing multiplier action", "role": "3194 gluing multiplier mechanism."},
        {"source_id": "SRC4489_21_glue3194", "ref": GLUE_3194, "needle": "GLUE3194_5_multiplier_solution", "role": "3194 multiplier solution law."},
        {"source_id": "SRC4489_22_sol3194", "ref": SOL_3194, "needle": "GLUE3194_1_balanced_Fpp_jump", "role": "3194 multiplier solutions."},
        {"source_id": "SRC4489_23_class3194", "ref": CLASS_3194, "needle": "CLASS3194_2_gluing_multiplier", "role": "3194 closure classification."},
        {"source_id": "SRC4489_24_gate", "ref": GATE_PATH, "needle": "def el_profile_rows", "role": "4489 helper gate."},
        {"source_id": "SRC4489_25_generator", "ref": GENERATOR_PATH, "needle": 'CHECKPOINT = "4489"', "role": "4489 generator script."},
    ]


def source_rows() -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for spec in source_specs():
        source_path = Path(spec["ref"])
        needle = str(spec["needle"])
        line_number = line_of(source_path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": spec["source_id"],
                "source_kind": "local",
                "source_ref": str(source_path),
                "local_path_exists": source_path.exists(),
                "needle": needle,
                "needle_found": line_number > 0,
                "line_number": line_number,
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
            "proof_result": "toy quadratic profile EL equation solved and pure natural interface matching rejected",
            "fallback_result": "C1 gluing multiplier mechanism closes interface equations if parent-owned; transfer tightening criticals imported",
            "claim_status": "private_nonclaim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def status_rows(selection_rows: Sequence[Mapping[str, object]], transfer_rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    exact_rows = [row for row in selection_rows if row.get("profile_type") == "exact_interior_EL"]
    best_n4 = min(float(row["N4_D2"]) for row in exact_rows)
    order_one = next(row for row in transfer_rows if row["abs_sK2_kappaSTF"] == "1.000000000000000e+00")
    c1e9 = next(row for row in transfer_rows if row["abs_sK2_kappaSTF"] == "1.000000000000000e+09")
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "best_exact_EL_N4_D2": f"{best_n4:.15e}",
            "identity_order_one_tightening_margin": order_one["equivalent_max_tightening_factor"],
            "identity_1e9_tightening_margin": c1e9["equivalent_max_tightening_factor"],
            "local_GR_claim": False,
            "sharpest_open_clause": "parent_gluing_multiplier_origin_or_PPN_transfer_matrix",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4489_0",
            "target": NEXT_TARGET,
            "objective": "Either derive the parent origin of the C1 gluing multipliers/finite edge stress, or build a PPN/orbital/light-time transfer matrix for induced slip plus DeltaKTF leakage.",
            "derive_first": "prove S_parent supplies S_glue or a finite-layer limit with lambda_i=-[Pi_i]",
            "fallback": "construct conservative observable-transfer matrix using Psi-Phi=2Sigma_H r^-3P2 and no-cancellation DeltaKTF terms",
            "risk": "mistaking toy EL plus gluing closure for parent-derived local GR",
            "valid_for_claim": False,
        }
    ]


def append_section_once(path: Path, marker: str, title: str, body: str) -> None:
    current = text(path)
    if marker in current:
        return
    addition = f"\n\n## {title}\n\nMarker: `{marker}`  \n{body}\n"
    write_text(path, current.rstrip() + addition + "\n")


def update_claims_register() -> None:
    rows = read_csv(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    rows.append(
        {
            "claim_id": CLAIM_ID,
            "domain": "local_gr_newton_r10_scalar_source_coupling",
            "claim": "4489 solves the toy quadratic profile EL equation, rejects pure natural interface matching, identifies C1 gluing multipliers as the current interface mechanism if parent-owned, and imports transfer-tightening criticals while keeping all local-GR/J2/PPN claims blocked.",
            "current_evidence": "4489 source register, EL profile derivation rows, profile selection rows, interface gluing rows, transfer sensitivity rows, parent requirements, claim gates, decision/status/next CSVs and validation.",
            "status": "private_profile_EL_solved_gluing_multiplier_route_transfer_criticals_nonclaim",
            "next_test": NEXT_TARGET,
            "key_risk": "treating toy functional, ansatz profile, or gluing multipliers as parent-signed local GR before source/coupling/transfer proof.",
            "sector": "local_gr_newton_r10_scalar_source_coupling",
            "evidence": str(FORMAL_PATH),
            "next_action": NEXT_TARGET,
            "risk": "parent gluing origin, coupling product, DeltaKTF and PPN/orbital transfer remain unsigned",
        }
    )
    write_csv(CLAIMS_PATH, rows)


def formal_body(
    sources: Sequence[Mapping[str, object]],
    el_rows: Sequence[Mapping[str, object]],
    selection_rows: Sequence[Mapping[str, object]],
    interface_rows: Sequence[Mapping[str, object]],
    transfer_rows: Sequence[Mapping[str, object]],
    req_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 505 PPC4161 - Parent Profile Selection Or PPN Transfer Upgrade

Private checkpoint: `{CHECKPOINT}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Generated UTC: `{STAMP}`

## Result

4489 upgrades the profile branch beyond the smoothstep ansatz.

For the toy quadratic projected-source functional:

```text
J[F]=integral x^4(D2[F])^2 dx,
D2[F]=(2/5)F''+2F'/x+6F/(5x^2),
```

the Euler-Lagrange normal equation gives:

```text
D2dagger[x^4D2[F]]=0,
D2dagger[u]=(2/5)u''-(2u/x)'+6u/(5x^2).
```

The power-law identity is:

```text
D2dagger[x^4D2[x^p]]
  =(4/25)p(p-2)(p+1)(p+3)x^p,
```

so the interior transition family is exactly:

```text
F_EL=A+B*x^2+C/x+D/x^3.
```

That is a real derivation. It is still not the MTS parent action.

The natural-interface route fails: matching to the exterior `x^-3` branch forces the transition to collapse to exterior-only and cannot match the core `x^2` branch. A boundary/interface mechanism is required.

The best current mechanism is:

```text
S_glue=sum_interfaces(lambda_0[F]+lambda_1[F']),
lambda_i=-[Pi_i],
Pi_1=(4/5)u,
Pi_0=4u/x-(4/5)u',
u=x^4D2[F].
```

This closes the interface equations exactly if the parent supplies constrained gluing domains or finite edge stress. It is not yet a local-GR claim.

Transfer sensitivity is also now quantified: for the selected profile, order-one coupling can survive a future transfer bound tightened by `5.744839923640726e10`, and `1e9` coupling can survive tightening by about `57.44839923640726`, before failing the current pressure-normalized bound.

## EL Profile Derivation

{table(el_rows)}

## Profile Selection Rows

{table(selection_rows)}

## Interface And Gluing Rows

{table(interface_rows)}

## Transfer Sensitivity Rows

{table(transfer_rows)}

## Parent Requirement Rows

{table(req_rows)}

## Decision Ledger

{table(ledger)}

## Claim Gates

{table(gates)}

## Status

{table(statuses)}

## Next Target

{table(next_targets)}

## Source Register

{table(sources)}

## Decision Row

{table(decisions)}
"""


def post_body(
    sources: Sequence[Mapping[str, object]],
    el_rows: Sequence[Mapping[str, object]],
    selection_rows: Sequence[Mapping[str, object]],
    interface_rows: Sequence[Mapping[str, object]],
    transfer_rows: Sequence[Mapping[str, object]],
    req_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4489 Y5/R2FR - Parent Profile Selection Or PPN Transfer Upgrade

Private post-checkpoint mirror for:

`{FORMAL_PATH}`

## What Actually Moved

4489 solves the toy profile EL branch and identifies the real interface obstruction. The interior solution is `F_EL=A+B*x^2+C/x+D/x^3`; pure natural joining fails; `C1` gluing multipliers close the equations only if parent-owned. Transfer tightening criticals are staged without promoting a PPN/local-GR claim.

## EL And Selection

{table(el_rows)}

{table(selection_rows)}

## Interface, Transfer, Requirements

{table(interface_rows)}

{table(transfer_rows)}

{table(req_rows)}

## Gates And Decisions

{table(gates)}

{table(ledger)}

{table(decisions)}

## Status And Next Target

{table(statuses)}

{table(next_targets)}

## Sources

{table(sources)}
"""


def validate(
    sources: Sequence[Mapping[str, object]],
    el_rows: Sequence[Mapping[str, object]],
    selection_rows: Sequence[Mapping[str, object]],
    interface_rows: Sequence[Mapping[str, object]],
    transfer_rows: Sequence[Mapping[str, object]],
    req_rows: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
    csv_paths: Sequence[Path],
) -> List[Dict[str, object]]:
    validations: List[Dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append({"checkpoint": CHECKPOINT, "check_id": check_id, "passed": passed, "detail": detail, "valid_for_claim": False})

    add("VAL4489_0_sources_exist_and_needles_found", all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources), "every cited source path exists and its needle is found")
    add("VAL4489_1_EL_solution_written", any(row.get("el_id") == "EL4489_3_power_modes" for row in el_rows), "EL normal modes and solution family exist")
    add("VAL4489_2_profile_selection_rows_written", len(selection_rows) >= 8, "smoothstep, exact EL and boundary audit rows exist")
    add("VAL4489_3_interface_no_go_written", any(row.get("interface_id") == "IF4489_1_natural_no_go" for row in interface_rows), "natural interface no-go exists")
    add("VAL4489_4_gluing_mechanism_written", any(row.get("interface_id") == "IF4489_2_gluing_multiplier_action" for row in interface_rows), "C1 gluing multiplier mechanism exists")
    add("VAL4489_5_transfer_criticals_written", len(transfer_rows) >= 5 and any(row.get("abs_sK2_kappaSTF") == "1.000000000000000e+09" for row in transfer_rows), "transfer critical rows include 1e9 coupling")
    add("VAL4489_6_parent_requirements_written", len(req_rows) >= 4, "parent requirement rows exist")
    add("VAL4489_7_claim_gates_block_local_GR", all(str(row.get("claim_allowed")).lower() == "false" for row in gates), "claim gates block promotion")
    add(
        "VAL4489_8_no_generated_claim_rows",
        all(
            str(row.get("valid_for_claim")).lower() == "false"
            for group in [sources, el_rows, selection_rows, interface_rows, transfer_rows, req_rows, gates, decisions, statuses, next_targets]
            for row in group
        ),
        "all generated rows remain private/nonclaim",
    )
    csv_ok = True
    csv_detail: List[str] = []
    for csv_path in csv_paths:
        try:
            parsed_rows = read_csv(csv_path)
            csv_detail.append(f"{csv_path.name}:{len(parsed_rows)}")
        except Exception as exc:  # pragma: no cover
            csv_ok = False
            csv_detail.append(f"{csv_path.name}:ERROR:{exc}")
    add("VAL4489_9_csvs_parse", csv_ok, "; ".join(csv_detail))
    add("VAL4489_10_docs_written", FORMAL_PATH.exists() and DOC_PATH.exists(), "formal and post checkpoint docs exist")
    add("VAL4489_11_claim_register_updated", any(row.get("claim_id") == CLAIM_ID for row in read_csv(CLAIMS_PATH)), "claims register contains L-331")
    add("VAL4489_12_spine_and_packet_updated", MARKER in text(SPINE_PATH) and PACKET_MARKER in text(PACKET_PATH), "spine and packet contain 4489 markers")
    add("VAL4489_13_next_target_selected", bool(next_targets) and next_targets[0].get("target") == NEXT_TARGET, NEXT_TARGET)
    add("VAL4489_14_pycache_removed", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generation")
    return validations


def main() -> None:
    sources = source_rows()
    el_rows = el_profile_rows()
    sel3190 = read_csv(SEL_3190)[0]
    selection_rows = profile_selection_rows(sel3190, read_csv(SEL_3192), read_csv(SEL_3193), read_csv(SOL_3194))
    interface_rows = interface_gluing_rows()
    transfer_rows = transfer_sensitivity_rows(read_csv(CRIT_3191))
    req_rows = parent_requirement_rows()
    ledger = decision_ledger_rows(NEXT_TARGET)
    gates = claim_gate_rows(sources, el_rows, selection_rows, interface_rows, transfer_rows, req_rows)
    decisions = decision_rows()
    statuses = status_rows(selection_rows, transfer_rows)
    next_targets = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(EL_CSV, el_rows)
    write_csv(SELECTION_CSV, selection_rows)
    write_csv(INTERFACE_CSV, interface_rows)
    write_csv(TRANSFER_CSV, transfer_rows)
    write_csv(REQ_CSV, req_rows)
    write_csv(DECISION_LEDGER_CSV, ledger)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)

    write_text(FORMAL_PATH, formal_body(sources, el_rows, selection_rows, interface_rows, transfer_rows, req_rows, ledger, gates, decisions, statuses, next_targets))
    write_text(DOC_PATH, post_body(sources, el_rows, selection_rows, interface_rows, transfer_rows, req_rows, ledger, gates, decisions, statuses, next_targets))
    update_claims_register()

    append_section_once(
        SPINE_PATH,
        MARKER,
        "4489 Parent Profile Selection Or Transfer Upgrade",
        "4489 solves the toy quadratic profile EL branch: `D2dagger[x^4D2[F]]=0` has interior family `F_EL=A+B*x^2+C/x+D/x^3`. Pure natural interface matching fails against the exterior `x^-3` branch, so a boundary/interface mechanism is required. `C1` gluing multipliers with `lambda_i=-[Pi_i]` close the interface equations if parent-owned. Transfer criticals show order-one coupling survives a `5.74e10` tightening and `1e9` coupling survives about `57` tightening, but all rows remain nonclaim.",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        "4489 Packet Integration",
        "The private packet now has a solved toy profile equation plus a concrete interface mechanism instead of a generic profile-selection gap. The next hard fork is parent origin of gluing/edge stress, or a conservative PPN/orbital/light-time transfer matrix for induced slip and `DeltaK_TF`.",
    )

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    csv_paths = [SOURCE_REGISTER, EL_CSV, SELECTION_CSV, INTERFACE_CSV, TRANSFER_CSV, REQ_CSV, DECISION_LEDGER_CSV, CLAIM_GATES_CSV, DECISION_CSV, STATUS_CSV, NEXT_CSV]
    validations = validate(sources, el_rows, selection_rows, interface_rows, transfer_rows, req_rows, gates, decisions, statuses, next_targets, csv_paths)
    write_csv(VALIDATION_PATH, validations)

    failed = [row for row in validations if str(row.get("passed")).lower() != "true"]
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Generated {CHECKPOINT}: {FORMAL_PATH}")
    print(f"Validation: {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
