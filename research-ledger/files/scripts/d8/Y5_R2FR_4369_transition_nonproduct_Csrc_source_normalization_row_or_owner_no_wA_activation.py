from __future__ import annotations

import csv
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4369"
CLAIM_ID = "L-210"
BRANCH = "MTS_R2FR_Y5_TRANSITION_NONPRODUCT_CSRC_SOURCE_NORMALIZATION_ROW_OR_OWNER_NO_WA_ACTIVATION_4369"
MARKER = "PPC4161_TRANSITION_NONPRODUCT_CSRC_SOURCE_NORMALIZATION_ROW_OR_OWNER_NO_WA_ACTIVATION_4369"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_NONPRODUCT_CSRC_SOURCE_NORMALIZATION_ROW_OR_OWNER_NO_WA_ACTIVATION_4369"
DECISION = "NONPRODUCT_EPSILON_GSRC_NEWTON_GREEN_TRANSFER_DERIVED_OWNER_ZERO_NOT_PARENT_ACTIVATED_NONCLAIM"
NEXT_TARGET = "4370-Y5-R2FR-transition-epsilon-Gsrc-coefficient-bound-or-Xi-owner-edge-proof.md"

FORMAL_PATH = FORMAL / "385-PPC4161-transition-nonproduct-Csrc-source-normalization-row-or-owner-no-wA-activation.md"
DOC_PATH = POST / "4369-Y5-R2FR-transition-nonproduct-Csrc-source-normalization-row-or-owner-no-wA-activation.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4369_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4369_00_4368_formal": (
        FORMAL / "384-PPC4161-transition-parent-sign-common-source-normalization-or-final-WEP-product-quarantine.md",
        "NEXT4368_0_epsilon_Gsrc",
        "4368 selects epsilon_Gsrc_open as the next non-product source-coupling lane.",
    ),
    "SRC4369_01_4368_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4368_NEXT_TARGET.csv",
        "derive/project epsilon_Gsrc_open",
        "4368 next target asks for epsilon_Gsrc projection before scoring local GR.",
    ),
    "SRC4369_02_4362_csrc_basis": (
        SOURCE_DIR / "P8_Y5_R2FR_4362_CSRC_VECTOR_BASIS.csv",
        "CSRC4362_3_epsilon_Gsrc_open",
        "4362 defines epsilon_Gsrc_open as the non-product source/coupling drift envelope.",
    ),
    "SRC4369_03_4362_arena_contract": (
        SOURCE_DIR / "P8_Y5_R2FR_4362_CSRC_ARENA_PROJECTION_CONTRACT.csv",
        "ARENA4362_6_Newton_source",
        "Newton/source-normalization arena waiting for parent-owned source normalization and source mass owner.",
    ),
    "SRC4369_04_4178_chain": (
        SOURCE_DIR / "P8_Y5_R2FR_4178_COUPLING_DERIVATION_CHAIN.csv",
        "KGL4178_4_Poisson",
        "4178 derives the private Poisson coefficient from EH block plus same Hilbert source.",
    ),
    "SRC4369_05_4178_reactivation": (
        SOURCE_DIR / "P8_Y5_R2FR_4178_REACTIVATION_LEDGER.csv",
        "RE4178_1_ZH_leak",
        "source-measure leaks reopen source-normalization rows.",
    ),
    "SRC4369_06_4178_guards": (
        SOURCE_DIR / "P8_Y5_R2FR_4178_ANTI_CIRCULARITY_GUARDS.csv",
        "AC4178_2_no_source_label_absorption",
        "4178 guard forbids hiding source labels in G.",
    ),
    "SRC4369_07_formal_194": (
        FORMAL / "194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md",
        "nabla^2 Phi_N = 4*pi G_cal rho_H",
        "formal calibrated source-coupling law.",
    ),
    "SRC4369_08_formal_187": (
        FORMAL / "187-PPC4161-Poisson-Gauss-Newton-readout-from-Hamiltonian-source-charge.md",
        "No observed orbital `GM`",
        "Newton source mass must be defined before orbital readout.",
    ),
    "SRC4369_09_formal_188": (
        FORMAL / "188-PPC4161-full-PPN-readout-vector.md",
        "gamma = 1",
        "PPN vector exists in the private packet when source/conservation clauses hold.",
    ),
    "SRC4369_10_4334_contract": (
        SOURCE_DIR / "P8_Y5_R2FR_4334_PROJECTION_MATRIX_SOURCE_CONTRACT.csv",
        "PI4334_1_PPN",
        "projection-matrix discipline for local tests.",
    ),
    "SRC4369_11_4361_owner": (
        SOURCE_DIR / "P8_Y5_R2FR_4361_THEOREM_ROWS.csv",
        "TH4361_3_full_owner_no_wA",
        "owner/no-wA theorem remains conditional and unsigned.",
    ),
}


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def find_line(path: Path, needle: str) -> str:
    text = read_text(path)
    index = text.find(needle)
    if index < 0:
        return ""
    return str(text[:index].count("\n") + 1)


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: str(row.get(field, "")) for field in fields})


def csv_line(row: Iterable[str]) -> str:
    buffer = StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(list(row))
    return buffer.getvalue()


def md_cell(value: object) -> str:
    return str(value).replace("|", r"\|").replace("\n", "<br>")


def md_table(rows: List[Dict[str, str]], fields: List[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + block.strip() + "\n", encoding="utf-8")


def append_claim_once(path: Path, claim_id: str, row: List[str]) -> None:
    text = read_text(path)
    if f"\n{claim_id}," in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + csv_line(row), encoding="utf-8")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        line_number = find_line(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(bool(line_number)),
                "line_number": line_number,
                "role": role,
                "valid_for_claim": "False",
            }
        )
    return rows


def definition_rows() -> List[Dict[str, str]]:
    return [
        {
            "definition_id": "DEF4369_0_epsilon_Gsrc",
            "symbol": "epsilon_Gsrc(x)",
            "definition": "fractional defect in the local calibrated source product after the GR-form EH/Hilbert source branch is chosen",
            "formula": "G_eff(x) rho_eff(x) = G_cal rho_H(x) [1 + epsilon_Gsrc(x)]",
            "units": "dimensionless",
            "status": "DEFINED_NONPRODUCT_CSRC_COMPONENT",
            "valid_for_claim": "False",
        },
        {
            "definition_id": "DEF4369_1_common_mode",
            "symbol": "epsilon_bar_H",
            "definition": "Hilbert-mass weighted common monopole/source-normalization mode",
            "formula": "epsilon_bar_H = M_Hdress^{-1} int_W rho_H(y) epsilon_Gsrc(y) dV_y",
            "units": "dimensionless",
            "status": "DERIVED_COMMON_MODE_SPLIT",
            "valid_for_claim": "False",
        },
        {
            "definition_id": "DEF4369_2_shape_residual",
            "symbol": "epsilon_Gsrc_perp",
            "definition": "source-normalization part not removable as common calibrated mass/coupling normalization",
            "formula": "epsilon_Gsrc_perp(y)=epsilon_Gsrc(y)-epsilon_bar_H",
            "units": "dimensionless",
            "status": "PHYSICAL_SHAPE_RESIDUAL_DEFINED",
            "valid_for_claim": "False",
        },
    ]


def projection_rows() -> List[Dict[str, str]]:
    return [
        {
            "projection_id": "PI4369_Gsrc_source_normalization",
            "arena": "Newton/source-normalization",
            "input_vector": "C_src_product_basis",
            "input_order": "Delta_w_component_vector; Xi_open; p_WEP_TiPt; epsilon_Gsrc_open",
            "projection_matrix_row": "0;0;0;1",
            "projected_quantity": "epsilon_Gsrc_open",
            "projection_formula": "P_Gsrc = epsilon_Gsrc_open",
            "source_backed_numeric": "False",
            "fixed_before_scoring": "True",
            "valid_prediction_row": "False",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "projection_id": "PI4369_Gsrc_shape_residual",
            "arena": "Newton/source-normalization",
            "input_vector": "epsilon_Gsrc_open plus Hilbert source density",
            "input_order": "epsilon_Gsrc_open; rho_H; W_H; M_Hdress",
            "projection_matrix_row": "mass-weighted common-mode subtraction",
            "projected_quantity": "epsilon_Gsrc_perp",
            "projection_formula": "epsilon_Gsrc_perp = epsilon_Gsrc - M_Hdress^{-1} int_W rho_H epsilon_Gsrc dV",
            "source_backed_numeric": "False",
            "fixed_before_scoring": "True",
            "valid_prediction_row": "False",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def newton_transfer_rows() -> List[Dict[str, str]]:
    return [
        {
            "transfer_id": "NG4369_0_poisson_residual",
            "statement": "epsilon_Gsrc_open enters the weak-field source equation as an additive Poisson source.",
            "formula": "nabla^2 deltaPhi_Gsrc = 4*pi*G_cal*rho_H*epsilon_Gsrc",
            "assumptions": "same EH block; same Hilbert source density; small source-normalization defect",
            "result_status": "EXACT_LINEAR_TRANSFER_DERIVED",
            "valid_for_claim": "False",
        },
        {
            "transfer_id": "NG4369_1_green_solution",
            "statement": "The potential residual is the Newton Green transform of the source-normalization defect.",
            "formula": "deltaPhi_Gsrc(x) = -G_cal int_W rho_H(y) epsilon_Gsrc(y)/|x-y| dV_y",
            "assumptions": "compact source support W_H; standard asymptotically flat Newton Green function",
            "result_status": "EXACT_GREEN_TRANSFER_DERIVED",
            "valid_for_claim": "False",
        },
        {
            "transfer_id": "NG4369_2_common_monopole",
            "statement": "Only the Hilbert-mass weighted common monopole is degenerate with calibrated source mass/coupling.",
            "formula": "deltaM_epsilon = int_W rho_H epsilon_Gsrc dV = epsilon_bar_H M_Hdress",
            "assumptions": "common mode is source/frame/range/time/readout blind and fixed before scoring",
            "result_status": "CALIBRATION_DEGENERACY_DERIVED_NOT_NUMERIC_G_CLAIM",
            "valid_for_claim": "False",
        },
        {
            "transfer_id": "NG4369_3_shape_residual",
            "statement": "The locally physical Newton/source-normalization residual is the noncommon shape piece.",
            "formula": "deltaPhi_perp(x) = -G_cal int_W rho_H(y) epsilon_Gsrc_perp(y)/|x-y| dV_y",
            "assumptions": "common monopole subtracted; no hidden cancellation with WEP product or T_open",
            "result_status": "PHYSICAL_RESIDUAL_OPERATOR_DERIVED",
            "valid_for_claim": "False",
        },
        {
            "transfer_id": "NG4369_4_exterior_bound",
            "statement": "For source support radius R and observation radius r>R, the source-normalization potential and acceleration residuals are bounded by the supremum norm of epsilon_Gsrc_perp.",
            "formula": "|deltaPhi_perp(x)| <= G_cal*M_Hdress*||epsilon_Gsrc_perp||_inf/(r-R); |deltaa_perp(x)| <= G_cal*M_Hdress*||epsilon_Gsrc_perp||_inf/(r-R)^2",
            "assumptions": "compact support; no cancellation; Euclidean weak-field distance bound |x-y|>=r-R",
            "result_status": "FINITE_BOUND_DERIVED_SYMBOLIC_CONSTANTS",
            "valid_for_claim": "False",
        },
        {
            "transfer_id": "NG4369_5_fractional_far_field_bound",
            "statement": "Relative to the monopole Newton acceleration, the far-field residual is controlled by epsilon_Gsrc_perp times a geometric support factor.",
            "formula": "|deltaa_perp|/|a_N| <= ||epsilon_Gsrc_perp||_inf * [r/(r-R)]^2",
            "assumptions": "a_N=G_cal*M_Hdress/r^2; r>R; source support known",
            "result_status": "DIMENSIONLESS_SCORE_GATE_DERIVED",
            "valid_for_claim": "False",
        },
    ]


def ppn_contract_rows() -> List[Dict[str, str]]:
    return [
        {
            "contract_id": "PPN4369_0_common_scalar_zero",
            "input": "epsilon_Gsrc is constant, source-blind, range-blind, time-stationary and absorbed before PPN U is defined",
            "output": "T_gamma=T_beta=T_alpha_i=0 for this source-normalization mode",
            "status": "CONDITIONAL_ZERO_ROUTE_INHERITED_FROM_4366_4367",
            "required_for_activation": "parent-signed common source normalization and conservation/Bianchi closure",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "PPN4369_1_noncommon_shape_route",
            "input": "epsilon_Gsrc_perp nonzero",
            "output": "R_PPN includes Pi_PPN^Gsrc[epsilon_Gsrc_perp]",
            "status": "TRANSFER_OPERATOR_REQUIRED_NOT_NUMERIC",
            "required_for_activation": "source-backed metric Green operator and PPN readout convention fixed before scoring",
            "valid_for_claim": "False",
        },
        {
            "contract_id": "PPN4369_2_time_or_frame_drift",
            "input": "D_A epsilon_Gsrc nonzero for time, frame, range, species, source or readout direction",
            "output": "Gdot/G, clock, preferred-frame or WEP/source-normalization rows reopen",
            "status": "REACTIVATION_RULE_IMPORTED_FROM_4178",
            "required_for_activation": "bounds on D_A epsilon_Gsrc or parent theorem D_A epsilon_Gsrc=0",
            "valid_for_claim": "False",
        },
    ]


def owner_audit_rows() -> List[Dict[str, str]]:
    return [
        {
            "audit_id": "OWN4369_0_EH_Hilbert_selector",
            "candidate_zero_clause": "same EH block and same Hilbert source define G_cal rho_H",
            "evidence": "4178/194 derive this inside the private selector",
            "current_status": "PRIVATE_BRANCH_AVAILABLE_NOT_GLOBAL_PARENT_ADOPTION",
            "activates_zero_now": "False",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "OWN4369_1_source_measure_no_leak",
            "candidate_zero_clause": "delta_ZH=0 and D_A delta_ZH=0 for all local-test directions",
            "evidence": "4178 has a private source-measure branch but its reactivation ledger reopens if ZH leaks",
            "current_status": "CONDITIONAL_NOT_GLOBAL",
            "activates_zero_now": "False",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "OWN4369_2_Hamiltonian_source_mass",
            "candidate_zero_clause": "M_Hdress is the same Hilbert/worldtube source charge before orbital readout",
            "evidence": "186/187/194 define the anti-GM-laundering route",
            "current_status": "PRIVATE_SELECTOR_NOT_ALL_TRANSITION_HAIR_CLOSED",
            "activates_zero_now": "False",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "OWN4369_3_owner_no_wA_graph",
            "candidate_zero_clause": "single action-density line plus parent-owned connected ordinary-matter graph kills source weights",
            "evidence": "4361 theorem exact but premise audit and 4362 graph test keep it unsigned",
            "current_status": "UNSIGNED",
            "activates_zero_now": "False",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "OWN4369_4_nonproduct_tails",
            "candidate_zero_clause": "Xi_open, T_open and transition source hair vanish or are separately bounded",
            "evidence": "4362 and 4368 keep these as live local-GR routes",
            "current_status": "OPEN",
            "activates_zero_now": "False",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> List[Dict[str, str]]:
    return [
        {
            "gate_id": "GATE4369_0_projection_defined",
            "claim_tested": "non-product epsilon_Gsrc C_src projection row exists",
            "required_inputs": "C_src_product_basis order and Newton/source arena",
            "status": "PASS_SYMBOLIC_PROJECTION",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE4369_1_newton_transfer",
            "claim_tested": "epsilon_Gsrc has exact Newton transfer law",
            "required_inputs": "Poisson source equation and Newton Green function",
            "status": "PASS_DERIVED_BOUND_OPERATOR",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE4369_2_zero_activation",
            "claim_tested": "epsilon_Gsrc_perp=0",
            "required_inputs": "parent-signed common source normalization or owner/no-wA/measure/source-mass closure",
            "status": "BLOCKED_UNSIGNED",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE4369_3_numeric_score",
            "claim_tested": "Newton/PPN/local-GR score",
            "required_inputs": "numeric epsilon_Gsrc_perp bound, support radius/worldtube map, PPN/source metric transfer",
            "status": "BLOCKED_NUMERIC_INPUTS_MISSING",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE4369_4_public_local_GR",
            "claim_tested": "public local-GR/Newton/PPN pass",
            "required_inputs": "zero or source-backed bounds for epsilon_Gsrc, Xi_open, T_open and Bianchi/boundary closure",
            "status": "FORBIDDEN",
            "claim_allowed": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4369_0",
            "decision": DECISION,
            "summary": (
                "4369 advances the non-product source-coupling route by defining epsilon_Gsrc as the fractional defect in "
                "G_cal rho_H, installing the Newton/source-normalization projection row [0,0,0,1], deriving the exact Poisson/Green "
                "transfer and compact-source bound, and splitting off the common monopole calibration mode. The useful physical residual "
                "is epsilon_Gsrc_perp. It is not zeroed yet: source-measure leaks, source-mass ownership, owner/no-wA graph signatures, "
                "Xi_open, T_open and transition hair remain unsigned/open. No local-GR/Newton/PPN claim fires."
            ),
            "next_target": NEXT_TARGET,
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4369_0",
            "object": "epsilon_Gsrc projection",
            "status": "DERIVED_SYMBOLIC_ROW",
            "note": "Pi_Gsrc^C=[0,0,0,1] selects the non-product source/coupling drift component from C_src.",
        },
        {
            "status_id": "STAT4369_1",
            "object": "Newton transfer",
            "status": "DERIVED_OPERATOR_AND_BOUND",
            "note": "epsilon_Gsrc_perp feeds the Newton potential through an explicit Green operator with compact-support bounds.",
        },
        {
            "status_id": "STAT4369_2",
            "object": "owner zero",
            "status": "NOT_PARENT_ACTIVATED",
            "note": "the private selector suggests the zero route, but current corpus does not globally sign the needed clauses.",
        },
        {
            "status_id": "STAT4369_3",
            "object": "next work",
            "status": "BOUND_OR_EDGE_PROOF",
            "note": "either source a numeric epsilon_Gsrc_perp/support bound or parent-sign one owner/no-wA edge.",
        },
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_id": "NT4369_0",
            "target": NEXT_TARGET,
            "question": "Can epsilon_Gsrc_perp be bounded with a source/worldtube coefficient, or can one parent owner/no-wA edge be signed enough to zero it?",
            "preferred_route": "derive/source a compact-support coefficient bound for epsilon_Gsrc_perp in Newton/source-normalization",
            "alternate_zero_route": "parent-sign one concrete measure/source-mass/no-reentry edge that forces epsilon_Gsrc_perp=0",
            "avoid": "claiming local GR from the symbolic projection row alone",
            "valid_for_claim": "False",
        }
    ]


def write_formal_doc(
    sources: List[Dict[str, str]],
    definitions: List[Dict[str, str]],
    projections: List[Dict[str, str]],
    newton: List[Dict[str, str]],
    ppn: List[Dict[str, str]],
    owner: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    statuses: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    text = f"""# PPC4161 transition: non-product C_src source-normalization row or owner/no-wA activation

Marker: `{MARKER}`

Private checkpoint: `{CHECKPOINT}`  
UTC stamp: `{STAMP}`  
Decision: `{DECISION}`

## Result

4368 quarantined the WEP product, so 4369 moves to the non-product source/coupling lane. The concrete advance is:

```text
C_src_product_basis = (Delta_w_component_vector, Xi_open, p_WEP_TiPt, epsilon_Gsrc_open)
Pi_Gsrc^C = [0,0,0,1].
```

This selects `epsilon_Gsrc_open` directly instead of recycling the WEP product. The source-normalization residual is now an operator, not a vibe:

```text
G_eff rho_eff = G_cal rho_H (1 + epsilon_Gsrc),
nabla^2 deltaPhi_Gsrc = 4*pi*G_cal*rho_H*epsilon_Gsrc,
deltaPhi_Gsrc(x) = -G_cal int_W rho_H(y) epsilon_Gsrc(y)/|x-y| dV_y.
```

The common monopole `epsilon_bar_H` is degenerate with calibrated mass/coupling. The physical Newton/source-normalization obstruction is the noncommon part:

```text
epsilon_Gsrc_perp = epsilon_Gsrc - epsilon_bar_H.
```

For compact support radius `R` and observation radius `r>R`:

```text
|deltaPhi_perp| <= G_cal*M_Hdress*||epsilon_Gsrc_perp||_inf/(r-R),
|deltaa_perp|/|a_N| <= ||epsilon_Gsrc_perp||_inf [r/(r-R)]^2.
```

So the next problem is no longer foggy: either prove `epsilon_Gsrc_perp=0` from parent source ownership, or source/bound `||epsilon_Gsrc_perp||` and the support geometry.

## Source Register

{md_table(sources, ["source_id", "path", "path_exists", "needle", "needle_found", "line_number", "role"])}

## Definitions

{md_table(definitions, ["definition_id", "symbol", "definition", "formula", "units", "status"])}

## Projection Rows

{md_table(projections, ["projection_id", "arena", "input_vector", "input_order", "projection_matrix_row", "projected_quantity", "projection_formula", "fixed_before_scoring", "valid_for_claim"])}

## Newton Green Transfer

{md_table(newton, ["transfer_id", "statement", "formula", "assumptions", "result_status"])}

## PPN / Local Contract

{md_table(ppn, ["contract_id", "input", "output", "status", "required_for_activation"])}

## Owner / No-wA Activation Audit

{md_table(owner, ["audit_id", "candidate_zero_clause", "evidence", "current_status", "activates_zero_now"])}

## Claim Gates

{md_table(gates, ["gate_id", "claim_tested", "required_inputs", "status", "claim_allowed"])}

## Decision

{md_table(decisions, ["decision_id", "decision", "summary", "next_target", "valid_for_claim"])}

## Status

{md_table(statuses, ["status_id", "object", "status", "note"])}

## Next Target

{md_table(next_targets, ["next_id", "target", "question", "preferred_route", "alternate_zero_route", "avoid"])}
"""
    FORMAL_PATH.write_text(text, encoding="utf-8")


def write_post_doc(decisions: List[Dict[str, str]], next_targets: List[Dict[str, str]]) -> None:
    text = f"""# 4369: non-product C_src source-normalization row or owner/no-wA activation

Marker: `{MARKER}`

## What changed

- Installed the non-product Newton/source-normalization projection row `Pi_Gsrc^C=[0,0,0,1]`.
- Defined `epsilon_Gsrc` as the fractional defect in `G_cal rho_H`.
- Derived the exact Poisson/Green transfer and compact-source bound.
- Split common calibration mode from the physical shape residual `epsilon_Gsrc_perp`.
- Kept the zero route conditional because parent source-measure/source-mass/owner graph signatures are still not globally signed.

## Decision row

{md_table(decisions, ["decision_id", "decision", "summary", "next_target"])}

## Next target

{md_table(next_targets, ["next_id", "target", "question", "preferred_route", "alternate_zero_route", "avoid"])}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def write_spine_update() -> None:
    block = f"""
## 4369 Transition non-product source-normalization transfer

Marker: `{MARKER}`

4369 moves past the quarantined WEP product and gives the non-product source/coupling lane its first explicit Newton transfer row. In the refined C_src basis the source-normalization projection is `Pi_Gsrc^C=[0,0,0,1]`, selecting `epsilon_Gsrc_open`.

The derived law is:

```text
nabla^2 deltaPhi_Gsrc = 4*pi*G_cal*rho_H*epsilon_Gsrc,
deltaPhi_Gsrc(x) = -G_cal int_W rho_H(y) epsilon_Gsrc(y)/|x-y| dV_y.
```

Only the Hilbert-mass weighted common mode is calibration-degenerate. The residual that can physically disturb Newton/local-GR is `epsilon_Gsrc_perp=epsilon_Gsrc-epsilon_bar_H`, with a compact-source bound controlled by `||epsilon_Gsrc_perp||`. This is progress: local GR now needs either a parent zero for `epsilon_Gsrc_perp` or a source/worldtube numeric bound, not another WEP-product export. Next target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, block)


def write_packet_update() -> None:
    block = f"""
## 4369 packet update: epsilon_Gsrc Newton Green transfer

Marker: `{PACKET_MARKER}`

Packet update: `epsilon_Gsrc_open` now has an explicit source-normalization projection and Newton Green transfer. The common monopole is calibration-only; the live physical obstruction is `epsilon_Gsrc_perp`. The next packet work should either bound `||epsilon_Gsrc_perp||` with source/worldtube geometry or parent-sign a concrete owner/no-`w_A` edge that forces it to zero.
"""
    append_once(PACKET_PATH, PACKET_MARKER, block)


def write_claim() -> None:
    append_claim_once(
        CLAIMS_PATH,
        CLAIM_ID,
        [
            CLAIM_ID,
            "local_gr",
            (
                "4369 advances the non-product source-coupling route after the WEP product quarantine. "
                "It defines epsilon_Gsrc as the fractional defect in G_cal rho_H, installs the Newton/source-normalization projection row Pi_Gsrc^C=[0,0,0,1], derives nabla^2 deltaPhi_Gsrc=4*pi*G_cal*rho_H*epsilon_Gsrc and the Green solution, then splits off the common calibration monopole epsilon_bar_H. "
                "The physical Newton/source-normalization obstruction is epsilon_Gsrc_perp with a compact-source bound controlled by ||epsilon_Gsrc_perp||. "
                "The owner-zero route remains conditional and unsigned, so no local-GR/Newton/PPN/WEP/clock/orbital/R10 claim fires."
            ),
            "4369 source register, definitions, projection rows, Newton Green transfer rows, PPN/local contract, owner/no-wA audit, claim gates, decision, status, next target and validation CSV.",
            "nonproduct_epsilon_Gsrc_Newton_Green_transfer_derived_owner_zero_unsigned_nonclaim",
            "Source or derive a bound on ||epsilon_Gsrc_perp|| and support geometry, or parent-sign one source-measure/source-mass/owner-no-wA edge that forces epsilon_Gsrc_perp=0.",
            "Treating Pi_Gsrc^C=[0,0,0,1] as a numeric prediction; absorbing noncommon source labels into G_cal; claiming local GR without bounding Xi_open/T_open/Bianchi/boundary tails.",
        ],
    )


def validation_rows(csv_paths: List[Path]) -> List[Dict[str, str]]:
    validations: List[Dict[str, str]] = []
    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4369_SOURCE_REGISTER.csv")
    projections = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4369_NEWTON_SOURCE_PROJECTION_ROWS.csv")
    newton = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4369_NEWTON_GREEN_TRANSFER_ROWS.csv")
    owner = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4369_OWNER_NO_WA_ACTIVATION_AUDIT.csv")
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4369_CLAIM_GATES.csv")

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append(
            {
                "checkpoint": CHECKPOINT,
                "check_id": check_id,
                "passed": str(bool(passed)),
                "detail": detail,
            }
        )

    add("VAL4369_0_all_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source path exists")
    add("VAL4369_1_all_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited source needle resolves")
    add(
        "VAL4369_2_projection_row_installed",
        any(row["projection_id"] == "PI4369_Gsrc_source_normalization" and row["projection_matrix_row"] == "0;0;0;1" for row in projections),
        "non-product epsilon_Gsrc projection row exists",
    )
    add(
        "VAL4369_3_green_transfer_derived",
        any(row["transfer_id"] == "NG4369_1_green_solution" and "int_W" in row["formula"] for row in newton),
        "Newton Green solution row exists",
    )
    add(
        "VAL4369_4_compact_bound_derived",
        any(row["transfer_id"] == "NG4369_4_exterior_bound" and "r-R" in row["formula"] for row in newton),
        "compact-source exterior bound row exists",
    )
    add(
        "VAL4369_5_owner_zero_not_activated",
        all(row["activates_zero_now"] == "False" for row in owner),
        "owner zero remains unsigned/currently inactive",
    )
    add("VAL4369_6_claim_gates_false", all(row["claim_allowed"] == "False" for row in gates), "all claim gates false")
    add("VAL4369_7_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4369_8_post_marker", MARKER in read_text(DOC_PATH), "post-checkpoint marker present")
    add("VAL4369_9_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4369_10_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4369_11_claim_row", f"\n{CLAIM_ID}," in read_text(CLAIMS_PATH), "claim row appended")
    add(
        "VAL4369_12_no_valid_claim_rows",
        all("True" not in [row.get("valid_for_claim", ""), row.get("claim_allowed", "")] for path in csv_paths for row in read_csv(path)),
        "generated rows remain nonclaim",
    )
    add(
        "VAL4369_13_csv_parse",
        all(len(read_csv(path)) > 0 for path in csv_paths),
        "all generated CSVs parse",
    )
    return validations


def main() -> None:
    sources = source_rows()
    definitions = definition_rows()
    projections = projection_rows()
    newton = newton_transfer_rows()
    ppn = ppn_contract_rows()
    owner = owner_audit_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    csv_payloads: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4369_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4369_EPSILON_GSRC_DEFINITIONS.csv": definitions,
        "P8_Y5_R2FR_4369_NEWTON_SOURCE_PROJECTION_ROWS.csv": projections,
        "P8_Y5_R2FR_4369_NEWTON_GREEN_TRANSFER_ROWS.csv": newton,
        "P8_Y5_R2FR_4369_PPN_LOCAL_TRANSFER_CONTRACT.csv": ppn,
        "P8_Y5_R2FR_4369_OWNER_NO_WA_ACTIVATION_AUDIT.csv": owner,
        "P8_Y5_R2FR_4369_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4369_DECISION.csv": decisions,
        "P8_Y5_R2FR_4369_STATUS.csv": statuses,
        "P8_Y5_R2FR_4369_NEXT_TARGET.csv": next_targets,
    }

    csv_paths: List[Path] = []
    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)

    write_formal_doc(sources, definitions, projections, newton, ppn, owner, gates, decisions, statuses, next_targets)
    write_post_doc(decisions, next_targets)
    write_spine_update()
    write_packet_update()
    write_claim()

    write_csv(VALIDATION_PATH, validation_rows(csv_paths))


if __name__ == "__main__":
    main()
