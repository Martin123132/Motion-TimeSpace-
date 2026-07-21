from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4680"
CLAIM_ID = "L-522"
MARKER = "PPC4161_NON_SOURCE_PPN_SURVIVOR_MAP_CURRENT_BRANCH_4680"
PACKET_MARKER = "PPC4161_PACKET_NON_SOURCE_PPN_SURVIVOR_MAP_CURRENT_BRANCH_4680"
DECISION = "NON_SOURCE_SURVIVORS_IMPORTED_A_MF_PRIVATE_BRANCH_AND_RESIDUAL_COEFFICIENT_LEDGER_cT_SPIN_SELECTED_NEXT_NONCLAIM"
NEXT_TARGET = "4681-Y5-R2FR-torsion-spin-residual-cT-zero-or-contact-bound.md"

DOC_PATH = POST / "4680-Y5-R2FR-non-source-PPN-residual-survivor-map-or-first-material-Req-value.md"
FORMAL_PATH = FORMAL / "696-PPC4161-non-source-PPN-residual-survivor-map-or-first-material-Req-value.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

CSV_4679_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4679_NEXT_TARGET.csv"
CSV_4679_SURVIVORS = SOURCE_DIR / "P8_Y5_R2FR_4679_NON_SOURCE_SURVIVOR_VECTOR.csv"
CSV_4679_TAILS = SOURCE_DIR / "P8_Y5_R2FR_4679_REQ_MATERIAL_TAIL_INPUTS.csv"
CSV_4679_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4679_STATUS.csv"
CSV_4448_SURVIVOR = SOURCE_DIR / "P8_Y5_R2FR_4448_SURVIVOR_MAP_OUTPUT.csv"
CSV_4448_DECISION = SOURCE_DIR / "P8_Y5_R2FR_4448_DECISION.csv"
CSV_4449_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4449_STATUS.csv"
CSV_4449_DECISION = SOURCE_DIR / "P8_Y5_R2FR_4449_DECISION.csv"
CSV_4450_COEFF = SOURCE_DIR / "P8_Y5_R2FR_4450_COEFFICIENT_STATUS_OUTPUT.csv"
CSV_4450_TARGET = SOURCE_DIR / "P8_Y5_R2FR_4450_TARGET_SCORE_OUTPUT.csv"
CSV_4450_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4450_STATUS.csv"
CSV_4450_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4450_NEXT_TARGET.csv"
FORMAL_464 = FORMAL / "464-PPC4161-non-source-PPN-residual-survivor-map-or-first-material-Req-value.md"
FORMAL_465 = FORMAL / "465-PPC4161-parent-motion-frame-A-MF-adoption-or-derived-flow-symmetry.md"
FORMAL_466 = FORMAL / "466-PPC4161-extra-invariant-residual-coefficient-map-to-PPN-R10-clocks-or-parent-scale-law.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4680_SOURCE_REGISTER.csv"
DERIVATION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4680_DERIVATION_ROWS.csv"
SURVIVOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4680_NON_SOURCE_SURVIVOR_MAP.csv"
AMF_CSV = SOURCE_DIR / "P8_Y5_R2FR_4680_AMF_IMPORT_STATUS.csv"
COEFF_CSV = SOURCE_DIR / "P8_Y5_R2FR_4680_RESIDUAL_COEFFICIENT_IMPORT.csv"
TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4680_TARGET_RANKING.csv"
VECTOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4680_REDUCED_LOCAL_VECTOR.csv"
MATERIAL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4680_MATERIAL_REQ_FALLBACK_ROWS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4680_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4680_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4680_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4680_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4680_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def line_of(path: Path, needle: str) -> int:
    for index, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return index
    return 0


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def table(rows: Iterable[dict[str, Any]]) -> str:
    rows = list(rows)
    if not rows:
        return ""
    headers = list(rows[0].keys())
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(header, "")).replace("|", "\\|").replace("\n", " ") for header in headers) + " |")
    return "\n".join(output)


def append_once(path: Path, marker: str, body: str) -> None:
    existing = text(path)
    if marker in existing:
        return
    path.write_text(existing.rstrip() + "\n\n" + body.strip() + "\n", encoding="utf-8")


def source_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4680_00_4679_next", CSV_4679_NEXT, "4680-Y5-R2FR-non-source-PPN-residual-survivor-map-or-first-material-Req-value.md", "4679 handoff to non-source survivor map."),
        ("SRC4680_01_4679_survivors", CSV_4679_SURVIVORS, "SURV4679_0_metric_principal", "current branch survivor classes after nonEM source-subvector zero."),
        ("SRC4680_02_4679_tails", CSV_4679_TAILS, "TAIL4679_0_R_eq_compact", "material/R_eq fallback rows from current branch."),
        ("SRC4680_03_4679_status", CSV_4679_STATUS, "non_source_residuals_closed", "4679 status keeps non-source residuals open."),
        ("SRC4680_04_4448_survivor_map", CSV_4448_SURVIVOR, "SURV4448_0_A_MF_parent_motion_frame", "older survivor map found the actual A_MF blocker."),
        ("SRC4680_05_4448_decision", CSV_4448_DECISION, "NON_SOURCE_SURVIVORS_RANKED_PRIVATE_CLOSURES_RECOVERED_A_MF_PARENT_SIGNATURE_SELECTED", "4448 survivor-map decision."),
        ("SRC4680_06_4449_status", CSV_4449_STATUS, "A_MF_private_adopted", "4449 adopted A_MF only as private branch axiom candidate."),
        ("SRC4680_07_4449_decision", CSV_4449_DECISION, "A_MF_ADOPTED_AS_EXPLICIT_PRIVATE_PARENT_AXIOM_CANDIDATE", "4449 no-public-derivation decision."),
        ("SRC4680_08_4450_coefficients", CSV_4450_COEFF, "C4450_6_cT_spin", "4450 residual coefficient ledger and cT spin row."),
        ("SRC4680_09_4450_target", CSV_4450_TARGET, "T4450_0_cT_spin", "4450 target score selects torsion-spin branch."),
        ("SRC4680_10_4450_status", CSV_4450_STATUS, "c_T_spin", "4450 status after A_MF coefficient split."),
        ("SRC4680_11_4450_next", CSV_4450_NEXT, "4451-Y5-R2FR-torsion-spin-residual-cT-zero-or-contact-bound.md", "older next target imported into current 4681 numbering."),
        ("SRC4680_12_formal464", FORMAL_464, "Actual derivation blocker: A_MF", "formal 4448 map."),
        ("SRC4680_13_formal465", FORMAL_465, "A_MF is now adopted only as an explicit private", "formal 4449 A_MF adoption."),
        ("SRC4680_14_formal466", FORMAL_466, "The next derivation target is `c_T_spin`", "formal 4450 coefficient split."),
    ]
    rows = []
    for source_id, path, needle, role in specs:
        line = line_of(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": line > 0,
                "line_number": line,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def derivation_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "D4680_0_current_source_subvector_done",
            "claim": "The current branch has already narrowed the source-weight problem.",
            "derivation": "4679 imports the connected nonEM graph plus GR-parity/no-source-prefactor trail into 4678, so relative nonEM source weights and material source re-entry are zero inside the private branch.",
            "consequence": "4680 does not reopen source weights; it starts from the non-source survivor vector.",
            "status": "CURRENT_BRANCH_SOURCE_SUBVECTOR_ZERO_PRIVATE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "D4680_1_4448_survivor_import",
            "claim": "The survivor map has already separated closed-private rows from real blockers.",
            "derivation": "4448 ranks Poynting, quotient/projector, boundary, kappa/deltaZH and private PPN readout as closed-private/guarded rows; the actual local-GR parent-origin blocker is A_MF.",
            "consequence": "Do not circle back into Poynting/projector/source coupling unless a guard fails.",
            "status": "NON_SOURCE_SURVIVORS_RANKED_IMPORTED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "D4680_2_4449_AMF_import",
            "claim": "A_MF is usable only as a private branch axiom candidate.",
            "derivation": "4449 found no older scalar/flow proof of A_MF, but adopted it explicitly inside PPC4161 because the conditional compensator theorem makes omega/B/coframe variables branch-owned if A_MF is signed.",
            "consequence": "Private derivations may use the Cartan branch, but public local-GR proof remains blocked by the IR selector and coefficient ledger.",
            "status": "A_MF_PRIVATE_BRANCH_IMPORTED_PUBLIC_DERIVATION_FALSE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "D4680_3_4450_coeff_import",
            "claim": "The post-A_MF coefficient problem is smaller and sharper.",
            "derivation": "4450 routes c_D, delta_kappa, c_bdy and c_Poynt_extra into private guarded rows, while c_Gamma, c_R2/M_R, c_T_spin and nonEH/material fallback remain finite/open.",
            "consequence": "The next derivation should attack the selected finite survivor c_T_spin rather than re-auditing every residual.",
            "status": "RESIDUAL_COEFFICIENT_LEDGER_IMPORTED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def survivor_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("S4680_0_source_weight_subvector", "source coupling/source weights", "relative nonEM + material source re-entry", "ZERO_PRIVATE_CURRENT_BRANCH", "4679", "do_not_reopen_unless_GR_parity_or_no_source_prefactor_guard_fails", 0),
        ("S4680_1_poynting_projector_boundary_kappa", "guarded non-source closures", "Poynting/projector/boundary/kappa/deltaZH", "CLOSED_PRIVATE_GUARDED", "4448/4450", "keep guards; do not choose as next target", 1),
        ("S4680_2_A_MF", "parent motion-frame origin", "EH principal block ownership", "PRIVATE_AXIOM_CANDIDATE_PUBLIC_DERIVATION_FALSE", "4449", "use private Cartan branch; do not claim public proof", 2),
        ("S4680_3_private_routed_coefficients", "private-routed coefficient subset", "c_D;delta_kappa;c_bdy;c_Poynt_extra", "PRIVATE_ROUTED_PARENT_ADOPTION_OPEN", "4450", "do not reattack unless reactivation guard fails", 3),
        ("S4680_4_cT_spin", "torsion/spin contact channel", "last clean local-GR finite survivor after A_MF", "SELECTED_NEXT_DERIVATION_TARGET", "4450", "prove auxiliary/spin-only/zero/heavy/contact-bound", 4),
        ("S4680_5_cGamma_cR2", "memory and higher-derivative tails", "c_Gamma;c_R2/M_R", "FINITE_SURVIVOR_OPEN_SECONDARY", "4450", "handle after c_T_spin or if torsion branch fails", 5),
        ("S4680_6_material_Req_nonEH", "empirical fallback", "R_eq/material values;nonEH_R11", "EMPIRICAL_FALLBACK_OPEN", "4679/4448/4450", "source numeric projection/bound rows if derivation stalls", 6),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": row_id,
            "family": family,
            "piece": piece,
            "current_status": status,
            "source_checkpoint": source,
            "next_action": action,
            "priority_rank": priority,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, family, piece, status, source, action, priority in data
    ]


def amf_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "amf_id": "AMF4680_0",
            "private_adopted": True,
            "older_scalar_flow_derivation_found": False,
            "omega_B_forced_if_A_MF": True,
            "Palatini_EH_forced_by_A_MF_alone": False,
            "public_local_GR_claim": False,
            "import_source": str(CSV_4449_STATUS),
            "current_status": "PRIVATE_AXIOM_CANDIDATE_IMPORTED_IR_SELECTOR_STILL_OPEN",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def coeff_rows(timestamp: str) -> list[dict[str, Any]]:
    selected = {
        "c_D": ("private_routed", "same-coframe/Hilbert descent zero inside private selector", False),
        "delta_kappa": ("private_routed", "universal calibrated G mode; numeric G not predicted", False),
        "c_bdy": ("private_routed", "Hamiltonian/no-flux boundary routing", False),
        "c_Poynt_extra": ("private_routed", "Poynting once-only Maxwell-Hodge Hilbert stress", False),
        "c_Gamma": ("finite_survivor", "memory/profile/source-coefficient scale or bound missing", False),
        "c_R2/M_R": ("finite_survivor", "curvature-square parent scale or R10/orbital bound missing", False),
        "c_T_spin": ("finite_survivor", "torsion spin zero/heavy/contact route selected next", True),
        "nonEH_R11/material": ("empirical_fallback", "material/R_eq/nonEH scoring rows remain fallback", False),
    }
    rows = []
    for index, (coefficient, (kind, status, selected_next)) in enumerate(selected.items()):
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "coefficient_id": f"C4680_{index}",
                "coefficient": coefficient,
                "current_class": kind,
                "current_status": status,
                "selected_next": selected_next,
                "source_checkpoint": "4450",
                "claim_allowed": False,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def target_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("T4680_0", "torsion-spin residual c_T_spin zero/heavy/contact-bound", 1, True, NEXT_TARGET, "best derivational lever after A_MF; clean local-GR reduction needs torsion eliminated, spin-only, heavy, or contact-bounded"),
        ("T4680_1", "c_R2/M_R parent scale or R10/orbital bound", 2, False, "later-cR2-MR-parent-scale-or-R10-bound.md", "important but needs reviewed short-range/orbital projection"),
        ("T4680_2", "c_Gamma profile/source coefficient fill", 3, False, "later-cGamma-source-coefficients-or-profile-bound.md", "important but already heavily chased; source coefficients remain open"),
        ("T4680_3", "material/R_eq/nonEH empirical fallback", 4, False, "later-nonEH-R11-or-material-bound-runner.md", "useful for scoring if derivation stalls"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "target_id": row_id,
            "target": target,
            "priority_rank": rank,
            "selected": selected,
            "next_artifact": artifact,
            "why": why,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, target, rank, selected, artifact, why in data
    ]


def vector_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "vector_id": "V4680_0_after_source_and_private_routes",
            "symbol": "R_local_private_remaining",
            "formula": "|R_T_spin| + |R_Gamma| + |R_R2| + |R_material/R_eq/nonEH| + Guard(A_MF public origin and IR selector)",
            "meaning": "private branch after current source-subvector zero plus imported A_MF/coefficient ledger; finite survivors remain explicit",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "vector_id": "V4680_1_selected_next_piece",
            "symbol": "R_T_spin",
            "formula": "0 if torsion is auxiliary algebraic spin-current-only and spinless macroscopic branch is used; otherwise bounded by spin/contact scale",
            "meaning": "next derivation target, not yet closed in current branch",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def material_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("M4680_0_R_eq_compact", "R_eq[varphi]=<Pi_M J_H-J_M_top-dB_zero,varphi>", "MISSING_PROJECTION_COEFF", "MISSING_RESIDUAL_VALUE", "MISSING_ARENA_BOUND"),
        ("M4680_1_material_projection", "R_material=Pi_material(T_H)-Pi_material(T_inventory)", "MISSING_MATERIAL_PROJECTION_COEFF", "MISSING_MATERIAL_VALUE", "MISSING_ARENA_BOUND"),
        ("M4680_2_nonEH_R11", "nonEH/R11 coefficient vector for public scoring", "MISSING_PARENT_ZERO_OR_SCALE", "MISSING_NUMERIC_BOUND", "MISSING_SOURCE_BACKED_SCORE"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": row_id,
            "quantity": quantity,
            "projection_or_parent_input": input_gap,
            "value_gap": value_gap,
            "bound_gap": bound_gap,
            "fallback_only": True,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, quantity, input_gap, value_gap, bound_gap in data
    ]


def control_rows(timestamp: str) -> list[dict[str, Any]]:
    controls = [
        ("CTRL4680_0", "No GitHub/public action; this is a local private checkpoint only."),
        ("CTRL4680_1", "Do not treat private A_MF adoption as public local-GR proof."),
        ("CTRL4680_2", "Do not reopen Poynting/projector/source coupling unless a recorded guard fails."),
        ("CTRL4680_3", "Do not claim numerical G_N prediction; keep universal calibrated G as calibration mode."),
        ("CTRL4680_4", "Next work must attempt the torsion-spin derivation or write explicit spin/contact bounds."),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": control_id,
            "rule": rule,
            "status": "ACTIVE",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for control_id, rule in controls
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision": DECISION,
            "summary": "4680 imports the older 4448-4450 survivor/A_MF/coefficient trail into the current 4679 branch. Source weights are not reopened. A_MF is available only as a private axiom candidate, not public proof. The post-A_MF residual coefficient ledger is split into private-routed rows and finite survivors. The clean next target is c_T_spin.",
            "next_target": NEXT_TARGET,
            "public_claim": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "current_branch_source_subvector_zero_private": True,
            "A_MF_private_adopted": True,
            "A_MF_public_derivation_found": False,
            "residual_coefficients_mapped": True,
            "private_routed_subset": "c_D;delta_kappa;c_bdy;c_Poynt_extra",
            "finite_survivors": "c_T_spin;c_Gamma;c_R2/M_R;nonEH/material_fallback",
            "selected_next": "c_T_spin",
            "public_local_GR_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_id": "NT4680_0",
            "target": NEXT_TARGET,
            "objective": "Try to prove the torsion-spin residual is auxiliary, algebraic, spin-current-only and zero/contact-suppressed for spinless macroscopic local test bodies.",
            "derive_first": "derive the Cartan torsion field equation under A_MF/IR selector and show torsion has no propagating/source-independent local branch",
            "fallback": "write PPN preferred-frame, spin-clock and R10/contact bound rows for finite c_T_spin",
            "risk": "pretending GR torsionlessness is inherited automatically rather than derived or bounded",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_documents(rows: dict[str, list[dict[str, Any]]]) -> None:
    body = f"""# 4680 - Y5/R2FR Non-Source PPN Residual Survivor Map or First Material Req Value

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

This checkpoint keeps the work local/private and imports the useful older ladder into the current 4679 branch.

```text
4679: source-weight/material-reentry subvector is zero inside the private branch.
4448: non-source survivors are ranked; A_MF is the real parent-origin blocker.
4449: A_MF is adopted only as a private axiom candidate, not a public derivation.
4450: post-A_MF residuals split into private-routed rows and finite survivors.
4680: current next target is c_T_spin.
```

The important move is that we stop circling source coupling, Poynting and projector rows unless their guards fail. The next actual leap is the torsion-spin residual: prove it is auxiliary/spin-only/zero/heavy/contact-bounded, or keep local GR explicitly blocked.

## Source Register

{table(rows["sources"])}

## Derivation Rows

{table(rows["derivations"])}

## Survivor Map

{table(rows["survivors"])}

## A_MF Import Status

{table(rows["amf"])}

## Residual Coefficient Import

{table(rows["coefficients"])}

## Target Ranking

{table(rows["targets"])}

## Reduced Local Vector

{table(rows["vectors"])}

## Material / Req Fallback Rows

{table(rows["materials"])}

## Controls

{table(rows["controls"])}

## Decision

{table(rows["decisions"])}

## Status

{table(rows["statuses"])}

## Next Target

{table(rows["next"])}

## Validation

{table(rows.get("validations", []))}
"""
    DOC_PATH.write_text(body, encoding="utf-8")
    FORMAL_PATH.write_text(body.replace("# 4680 - Y5/R2FR", "# 696 - PPC4161"), encoding="utf-8")


def update_registers(timestamp: str) -> None:
    claims = read_csv(CLAIMS_PATH)
    if not any(row.get("claim_id") == CLAIM_ID for row in claims):
        fieldnames = list(claims[0].keys())
        new_row = {field: "" for field in fieldnames}
        new_row.update(
            {
                "claim_id": CLAIM_ID,
                "domain": "local_gr_empirical_interface",
                "claim": "4680 imports the non-source survivor map, A_MF private-branch adoption, and post-A_MF residual coefficient ledger into the current 4679 branch. Source weights are not reopened; A_MF remains a private axiom candidate rather than public derivation; private-routed rows are guarded; finite survivors remain, with c_T_spin selected as the next derivation target.",
                "current_evidence": "Generated source register, derivation rows, non-source survivor map, A_MF import status, residual coefficient import, target ranking, reduced local vector, material fallback rows, controls, decision, status, next target and validation.",
                "status": DECISION.lower(),
                "next_test": NEXT_TARGET,
                "key_risk": "Treating private A_MF adoption as public GR proof, reopening closed-private Poynting/projector/source rows, or assuming torsionlessness instead of deriving or bounding c_T_spin.",
                "sector": "local_gr",
                "evidence": str(DOC_PATH),
                "next_action": NEXT_TARGET,
            }
        )
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writerow(new_row)

    append_once(
        SPINE_PATH,
        MARKER,
        f"""## Local GR Parent-Derivation Update - Current Non-Source Survivor Map

Marker: `{MARKER}`

4680 imports the 4448-4450 survivor/A_MF/coefficient ladder into the current 4679 branch. The active current-branch local vector is now:

```text
R_local_private_remaining
  = |R_T_spin| + |R_Gamma| + |R_R2|
    + |R_material/R_eq/nonEH|
    + Guard(A_MF public origin and IR selector).
```

The selected next target is `c_T_spin`: derive torsion as auxiliary/spin-only/zero/heavy/contact-bounded, or keep local GR blocked.

- claim id: `{CLAIM_ID}`
- checkpoint: `{DOC_PATH.name}`
- next: `{NEXT_TARGET}`
- timestamp_utc: `{timestamp}`
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## PPC4161 Packet Addendum - Current Non-Source Survivor Map

Marker: `{PACKET_MARKER}`

After 4679, do not reopen source coupling by default. The private branch now imports A_MF and the residual coefficient ledger; private-routed rows stay guarded, while finite survivors remain explicit. The next packet attack is `c_T_spin`.

- source csv: `{SURVIVOR_CSV.name}`
- coefficient csv: `{COEFF_CSV.name}`
- next: `{NEXT_TARGET}`
""",
    )


def validation_rows(rows: dict[str, list[dict[str, Any]]], csv_paths: list[Path]) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL4680_0_sources_exist", all(row["path_exists"] for row in rows["sources"]), "every cited source path exists"))
    checks.append(("VAL4680_1_needles_found", all(row["needle_found"] for row in rows["sources"]), "every cited source needle is present"))
    checks.append(("VAL4680_2_amf_imported_private", rows["amf"][0]["private_adopted"] and not rows["amf"][0]["older_scalar_flow_derivation_found"], "A_MF imported as private axiom, not older public derivation"))
    checks.append(("VAL4680_3_coefficients_mapped", any(row["coefficient"] == "c_T_spin" and row["selected_next"] for row in rows["coefficients"]), "c_T_spin finite survivor selected"))
    checks.append(("VAL4680_4_private_routes_not_reopened", any(row["family"] == "private-routed coefficient subset" for row in rows["survivors"]), "private-routed rows retained as guarded"))
    checks.append(("VAL4680_5_material_fallback_open", all(row["fallback_only"] and not row["valid_for_claim"] for row in rows["materials"]), "material/R_eq rows remain fallback-only"))
    checks.append(("VAL4680_6_next_target", rows["next"][0]["target"] == NEXT_TARGET, "4681 torsion-spin target written"))
    checks.append(("VAL4680_7_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-522"))
    checks.append(("VAL4680_8_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker"))
    checks.append(("VAL4680_9_post_doc", DOC_PATH.exists() and MARKER in text(DOC_PATH), "post checkpoint doc exists with marker"))
    checks.append(("VAL4680_10_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"))
    checks.append(("VAL4680_11_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"))
    for path in csv_paths:
        try:
            parsed = read_csv(path)
            checks.append((f"VAL4680_parse_{path.name}", bool(parsed), f"rows={len(parsed)}"))
        except Exception as exc:
            checks.append((f"VAL4680_parse_{path.name}", False, repr(exc)))
    checks.append(("VAL4680_12_pycache_absent", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"))
    overall = all(passed for _, passed, _ in checks)
    checks.append(("VAL4680_OVERALL", overall, "PASS" if overall else "FAIL"))
    return [
        {
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "passed": passed,
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]


def main() -> None:
    timestamp = stamp()
    rows = {
        "sources": source_rows(timestamp),
        "derivations": derivation_rows(timestamp),
        "survivors": survivor_rows(timestamp),
        "amf": amf_rows(timestamp),
        "coefficients": coeff_rows(timestamp),
        "targets": target_rows(timestamp),
        "vectors": vector_rows(timestamp),
        "materials": material_rows(timestamp),
        "controls": control_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "statuses": status_rows(timestamp),
        "next": next_rows(timestamp),
    }
    csv_map = {
        SOURCE_REGISTER: rows["sources"],
        DERIVATION_CSV: rows["derivations"],
        SURVIVOR_CSV: rows["survivors"],
        AMF_CSV: rows["amf"],
        COEFF_CSV: rows["coefficients"],
        TARGET_CSV: rows["targets"],
        VECTOR_CSV: rows["vectors"],
        MATERIAL_CSV: rows["materials"],
        CONTROL_CSV: rows["controls"],
        DECISION_CSV: rows["decisions"],
        STATUS_CSV: rows["statuses"],
        NEXT_CSV: rows["next"],
    }
    for path, data in csv_map.items():
        write_csv(path, data)
    write_documents(rows)
    update_registers(timestamp)
    cache = POST / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    rows["validations"] = validation_rows(rows, list(csv_map))
    write_csv(VALIDATION_CSV, rows["validations"])
    write_documents(rows)
    print(f"{CHECKPOINT} complete: {DOC_PATH}")
    print(f"validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
