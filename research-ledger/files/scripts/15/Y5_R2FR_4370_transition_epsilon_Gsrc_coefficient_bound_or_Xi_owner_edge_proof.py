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
MICRO_RESIDUALS = POST / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"

CHECKPOINT = "4370"
CLAIM_ID = "L-211"
BRANCH = "MTS_R2FR_Y5_TRANSITION_EPSILON_GSRC_COEFFICIENT_BOUND_OR_XI_OWNER_EDGE_PROOF_4370"
MARKER = "PPC4161_TRANSITION_EPSILON_GSRC_COEFFICIENT_BOUND_OR_XI_OWNER_EDGE_PROOF_4370"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_EPSILON_GSRC_COEFFICIENT_BOUND_OR_XI_OWNER_EDGE_PROOF_4370"
DECISION = "EPSILON_GSRC_MONOPOLE_SUBTRACTED_BOUND_GATE_DERIVED_XI_OWNER_EDGE_UNSIGNED_NONCLAIM"
NEXT_TARGET = "4371-Y5-R2FR-transition-source-worldtube-support-bound-or-measure-owner-edge-proof.md"

FORMAL_PATH = FORMAL / "386-PPC4161-transition-epsilon-Gsrc-coefficient-bound-or-Xi-owner-edge-proof.md"
DOC_PATH = POST / "4370-Y5-R2FR-transition-epsilon-Gsrc-coefficient-bound-or-Xi-owner-edge-proof.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4370_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4370_00_4369_formal": (
        FORMAL / "385-PPC4161-transition-nonproduct-Csrc-source-normalization-row-or-owner-no-wA-activation.md",
        "epsilon_Gsrc_perp = epsilon_Gsrc - epsilon_bar_H",
        "4369 defines the physical noncommon source-normalization residual.",
    ),
    "SRC4370_01_4369_green": (
        SOURCE_DIR / "P8_Y5_R2FR_4369_NEWTON_GREEN_TRANSFER_ROWS.csv",
        "NG4369_5_fractional_far_field_bound",
        "4369 gives the coarse far-field acceleration bound.",
    ),
    "SRC4370_02_4369_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4369_NEXT_TARGET.csv",
        "4370-Y5-R2FR-transition-epsilon-Gsrc-coefficient-bound-or-Xi-owner-edge-proof.md",
        "4369 selects coefficient bound or owner-edge proof as the next target.",
    ),
    "SRC4370_03_4369_owner": (
        SOURCE_DIR / "P8_Y5_R2FR_4369_OWNER_NO_WA_ACTIVATION_AUDIT.csv",
        "OWN4369_3_owner_no_wA_graph",
        "owner/no-wA graph route remains unsigned.",
    ),
    "SRC4370_04_4361_premise": (
        SOURCE_DIR / "P8_Y5_R2FR_4361_PREMISE_AUDIT.csv",
        "P4361_2_measure_owner",
        "measure/Jacobian owner premise is required but unsigned.",
    ),
    "SRC4370_05_1606_edges": (
        MICRO_RESIDUALS / "R2FR_parent_owned_edge_audit_nonclaim_1606.csv",
        "EDGE1606_5_measure",
        "parent-owned source-relevant graph edge audit does not certify the measure edge.",
    ),
    "SRC4370_06_4178_guards": (
        SOURCE_DIR / "P8_Y5_R2FR_4178_ANTI_CIRCULARITY_GUARDS.csv",
        "AC4178_2_no_source_label_absorption",
        "source labels cannot be hidden in calibrated G.",
    ),
    "SRC4370_07_4178_reactivation": (
        SOURCE_DIR / "P8_Y5_R2FR_4178_REACTIVATION_LEDGER.csv",
        "RE4178_1_ZH_leak",
        "source-measure leak reopens WEP/source-normalization rows.",
    ),
    "SRC4370_08_formal_194": (
        FORMAL / "194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md",
        "No orbital `GM`",
        "source mass/coupling must be defined before readout.",
    ),
    "SRC4370_09_4334_contract": (
        SOURCE_DIR / "P8_Y5_R2FR_4334_PROJECTION_MATRIX_SOURCE_CONTRACT.csv",
        "PI4334_1_PPN",
        "PPN and local-test projections still need source-backed matrices before scoring.",
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


def theorem_rows() -> List[Dict[str, str]]:
    return [
        {
            "theorem_id": "TH4370_0_zero_monopole_identity",
            "statement": "epsilon_Gsrc_perp has zero Hilbert-source monopole by construction.",
            "formula": "int_W rho_H epsilon_Gsrc_perp dV = 0",
            "derivation": "epsilon_Gsrc_perp = epsilon_Gsrc - M_Hdress^{-1} int_W rho_H epsilon_Gsrc dV",
            "result": "common G/M calibration mode removed before finite scoring",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4370_1_monopole_subtracted_potential_bound",
            "statement": "For support |y|<=R and observation r>R, the zero-monopole residual has a sharper potential gate.",
            "formula": "|deltaPhi_perp|/|Phi_N| <= E_perp * s/(1-s), where s=R/r",
            "derivation": "use int rho_H epsilon_perp dV=0 and |1/|x-y|-1/r| <= R/[r(r-R)]",
            "result": "source-shape residual is suppressed by R/r in far field",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4370_2_monopole_subtracted_acceleration_bound",
            "statement": "For support |y|<=R and observation r>R, the acceleration residual obeys a zero-monopole geometry gate.",
            "formula": "|deltaa_perp|/|a_N| <= E_perp * 2s/(1-s)^3, where s=R/r",
            "derivation": "apply the Lipschitz bound |grad(1/|x-y|)-grad(1/r)| <= 2R/(r-R)^3",
            "result": "far-field acceleration residual is O((R/r)E_perp) instead of O(E_perp)",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4370_3_safe_bound_selector",
            "statement": "Use the smaller of the coarse 4369 gate and the zero-monopole gate, fixed before scoring.",
            "formula": "K_N(s)=min((1-s)^-2, 2s(1-s)^-3); require E_perp <= delta_N/K_N(s)",
            "derivation": "both inequalities are valid for 0<s<1; selecting the tighter source-independent upper bound is not data fitting",
            "result": "dimensionless coefficient gate for Newton/source-normalization tests",
            "valid_for_claim": "False",
        },
    ]


def geometry_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for s in [0.5, 0.25, 0.1, 0.03, 0.01, 0.001]:
        coarse = (1.0 - s) ** -2
        mono = 2.0 * s * (1.0 - s) ** -3
        best = min(coarse, mono)
        rows.append(
            {
                "geometry_id": f"GEO4370_s_{str(s).replace('.', 'p')}",
                "s_R_over_r": f"{s:.6g}",
                "coarse_acceleration_factor": f"{coarse:.12g}",
                "zero_monopole_acceleration_factor": f"{mono:.12g}",
                "selected_K_N": f"{best:.12g}",
                "required_E_perp_for_delta_N": f"E_perp <= delta_N/{best:.12g}",
                "interpretation": "smaller K_N means a larger source-shape envelope can survive the same observed fractional acceleration bound",
                "valid_for_claim": "False",
            }
        )
    return rows


def bound_gate_rows() -> List[Dict[str, str]]:
    return [
        {
            "gate_id": "BG4370_0_Newton_acceleration",
            "observable": "fractional Newton acceleration/source-normalization residual",
            "residual_bound_formula": "|deltaa_perp|/|a_N| <= K_N(s) E_perp",
            "coefficient_gate": "E_perp <= delta_N_obs/K_N(s)",
            "required_inputs": "delta_N_obs; source support radius R; observation radius r; fixed source/worldtube map",
            "current_numeric_status": "TEMPLATE_NO_DELTA_N_OR_SUPPORT_INPUT",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "BG4370_1_Newton_potential",
            "observable": "fractional Newton potential/range residual",
            "residual_bound_formula": "|deltaPhi_perp|/|Phi_N| <= E_perp*s/(1-s)",
            "coefficient_gate": "E_perp <= delta_Phi_obs*(1-s)/s",
            "required_inputs": "delta_Phi_obs; source support radius R; observation radius r; potential convention",
            "current_numeric_status": "TEMPLATE_NO_DELTA_PHI_OR_SUPPORT_INPUT",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "BG4370_2_PPN_metric",
            "observable": "PPN gamma/beta/preferred-frame source-shape response",
            "residual_bound_formula": "|R_PPN_j| <= B_j(s,source,readout) E_perp",
            "coefficient_gate": "E_perp <= bound_j/B_j after B_j is source-backed",
            "required_inputs": "metric Green operator; PPN readout convention; source support; B_j coefficients",
            "current_numeric_status": "BLOCKED_TRANSFER_COEFFICIENTS_MISSING",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "BG4370_3_time_frame_drift",
            "observable": "Gdot/G, clocks, frame/range/source-label leakage",
            "residual_bound_formula": "|R_A| <= B_A |D_A epsilon_Gsrc|",
            "coefficient_gate": "D_A epsilon_Gsrc=0 by theorem or source-backed derivative bound",
            "required_inputs": "time/frame/range/source derivative law or finite derivative envelope",
            "current_numeric_status": "BLOCKED_DERIVATIVE_INPUTS_MISSING",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def owner_edge_rows() -> List[Dict[str, str]]:
    return [
        {
            "edge_id": "EDGE4370_0_measure_owner",
            "candidate_edge": "matter sectors to measure/Jacobian owner",
            "source_status": "EDGE1606_5_measure parent_owned=False; P4361_2 parent_signed=False",
            "would_zero": "source-measure part of epsilon_Gsrc_perp and Xi_open",
            "current_result": "NOT_SIGNED",
            "next_proof_input": "species-blind measure/Jacobian/hbar theorem with no field-normalization source slot",
            "activates_zero_now": "False",
            "valid_for_claim": "False",
        },
        {
            "edge_id": "EDGE4370_1_current_readout_owner",
            "candidate_edge": "Hilbert source to current/readout owner",
            "source_status": "EDGE1606_6_current is partial only",
            "would_zero": "post-variation readout reentry tail",
            "current_result": "PARTIAL_NOT_SUFFICIENT",
            "next_proof_input": "pre-variation source weights and post-readout projector reentry excluded together",
            "activates_zero_now": "False",
            "valid_for_claim": "False",
        },
        {
            "edge_id": "EDGE4370_2_same_source_mass",
            "candidate_edge": "Hamiltonian/Hilbert worldtube mass equals source charge before orbital readout",
            "source_status": "private selector available in 186/187/194; transition/source-hair closure not global",
            "would_zero": "wrong-mass-charge part of epsilon_Gsrc_perp",
            "current_result": "PRIVATE_NOT_GLOBAL",
            "next_proof_input": "same-worldtube support and no non-Hilbert source hair",
            "activates_zero_now": "False",
            "valid_for_claim": "False",
        },
        {
            "edge_id": "EDGE4370_3_full_zero_package",
            "candidate_edge": "measure owner + same source mass + no readout reentry + common-mode derivative silence",
            "source_status": "not assembled as parent-owned in current corpus",
            "would_zero": "epsilon_Gsrc_perp=0",
            "current_result": "SUFFICIENCY_THEOREM_ONLY",
            "next_proof_input": "all clauses signed on the same branch",
            "activates_zero_now": "False",
            "valid_for_claim": "False",
        },
    ]


def runner_rows() -> List[Dict[str, str]]:
    return [
        {
            "runner_id": "RUN4370_0_inputs",
            "step": "input collection",
            "formula": "delta_N_obs, R, r, E_perp_bound",
            "status": "WAITING_FOR_SOURCE_WORLD_TUBE_INPUT",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4370_1_geometry",
            "step": "geometry factor",
            "formula": "s=R/r; K_N(s)=min((1-s)^-2, 2s(1-s)^-3)",
            "status": "DERIVED_READY",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4370_2_acceptance",
            "step": "Newton acceleration acceptance",
            "formula": "pass if E_perp_bound <= delta_N_obs/K_N(s)",
            "status": "SCHEMA_READY_NONCLAIM",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4370_3_owner_zero",
            "step": "zero route",
            "formula": "if full owner package signed then E_perp_bound=0",
            "status": "BLOCKED_UNSIGNED",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> List[Dict[str, str]]:
    return [
        {
            "gate_id": "GATE4370_0_monopole_subtraction",
            "claim_tested": "epsilon_Gsrc_perp has zero source monopole",
            "required_inputs": "4369 definition of epsilon_bar_H",
            "status": "PASS_DERIVED_IDENTITY",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE4370_1_bound_gate",
            "claim_tested": "Newton/source-normalization coefficient gate is available",
            "required_inputs": "compact support R<r and fixed geometry factor",
            "status": "PASS_SYMBOLIC_GATE",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE4370_2_numeric_acceptance",
            "claim_tested": "source-normalization residual passes a real bound",
            "required_inputs": "source-backed E_perp_bound, R, r and delta_N_obs",
            "status": "BLOCKED_INPUTS_MISSING",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE4370_3_owner_edge_zero",
            "claim_tested": "owner/no-wA edge zeroes epsilon_Gsrc_perp",
            "required_inputs": "measure owner, same source mass, no readout reentry and derivative silence signed on same branch",
            "status": "BLOCKED_UNSIGNED",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE4370_4_public_local_GR",
            "claim_tested": "public local-GR/Newton/PPN pass",
            "required_inputs": "epsilon_Gsrc bound/zero plus Xi_open/T_open/Bianchi/boundary closure",
            "status": "FORBIDDEN",
            "claim_allowed": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4370_0",
            "decision": DECISION,
            "summary": (
                "4370 turns epsilon_Gsrc_perp into a sharper coefficient-bound problem. Because the common monopole is subtracted, "
                "the far-field source-normalization residual has a zero-monopole geometry factor. For s=R/r, the safe Newton acceleration "
                "gate is K_N(s)=min((1-s)^-2, 2s(1-s)^-3), requiring E_perp<=delta_N/K_N(s). The owner-edge route was checked against "
                "4361/1606/4178 and remains unsigned: the measure edge, current/readout edge, same-source-mass edge and no-reentry package "
                "do not activate epsilon_Gsrc_perp=0 now. No public local-GR/Newton/PPN claim fires."
            ),
            "next_target": NEXT_TARGET,
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4370_0",
            "object": "epsilon_Gsrc_perp bound",
            "status": "COEFFICIENT_GATE_DERIVED",
            "note": "Newton/source-normalization acceptance reduces to E_perp <= delta_N/K_N(s).",
        },
        {
            "status_id": "STAT4370_1",
            "object": "monopole subtraction",
            "status": "FAR_FIELD_SUPPRESSION_DERIVED",
            "note": "zero common source monopole gives an R/r suppression factor away from the source.",
        },
        {
            "status_id": "STAT4370_2",
            "object": "owner edge",
            "status": "UNSIGNED",
            "note": "measure/current/source-mass/no-reentry edges do not currently prove epsilon_Gsrc_perp=0.",
        },
        {
            "status_id": "STAT4370_3",
            "object": "next work",
            "status": "SOURCE_SUPPORT_OR_MEASURE_OWNER",
            "note": "need source/worldtube support inputs or a real measure-owner edge proof.",
        },
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_id": "NT4370_0",
            "target": NEXT_TARGET,
            "question": "Can we supply source/worldtube support parameters for the epsilon_Gsrc gate, or prove the measure-owner edge that sets the envelope to zero?",
            "preferred_route": "derive/source R/r and E_perp inputs for the Newton/source-normalization gate",
            "alternate_zero_route": "try a concrete species-blind measure/Jacobian owner proof",
            "avoid": "calling the symbolic K_N(s) gate a local-GR pass",
            "valid_for_claim": "False",
        }
    ]


def write_formal_doc(
    sources: List[Dict[str, str]],
    theorem: List[Dict[str, str]],
    geometry: List[Dict[str, str]],
    bound_gates: List[Dict[str, str]],
    owner_edges: List[Dict[str, str]],
    runner: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    statuses: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    text = f"""# PPC4161 transition: epsilon_Gsrc coefficient bound or Xi owner edge proof

Marker: `{MARKER}`

Private checkpoint: `{CHECKPOINT}`  
UTC stamp: `{STAMP}`  
Decision: `{DECISION}`

## Result

4369 gave the Green operator for `epsilon_Gsrc_perp`. 4370 sharpens it into a coefficient gate.

Since

```text
epsilon_Gsrc_perp = epsilon_Gsrc - epsilon_bar_H,
int_W rho_H epsilon_Gsrc_perp dV = 0.
```

the common source monopole is gone before scoring. For a source inside radius `R` and an observation point with `r>R`, define:

```text
s = R/r,
E_perp = ||epsilon_Gsrc_perp||_inf.
```

The coarse 4369 acceleration gate is:

```text
|deltaa_perp|/|a_N| <= E_perp (1-s)^-2.
```

The zero-monopole gate is stronger in the far field:

```text
|deltaa_perp|/|a_N| <= E_perp 2s(1-s)^-3.
```

So the fixed pre-score gate is:

```text
K_N(s)=min((1-s)^-2, 2s(1-s)^-3),
E_perp <= delta_N_obs/K_N(s).
```

That is a real test contract: once `E_perp`, `R/r`, and an observed fractional Newton/source residual bound are sourced, the branch can be scored without touching the quarantined WEP product.

The owner-edge route was checked too. It does not fire: the measure edge, current/readout edge, same-source-mass edge and no-reentry package are not parent-signed on the same branch.

## Source Register

{md_table(sources, ["source_id", "path", "path_exists", "needle", "needle_found", "line_number", "role"])}

## Bound Theorems

{md_table(theorem, ["theorem_id", "statement", "formula", "derivation", "result"])}

## Geometry Factor Table

{md_table(geometry, ["geometry_id", "s_R_over_r", "coarse_acceleration_factor", "zero_monopole_acceleration_factor", "selected_K_N", "required_E_perp_for_delta_N"])}

## Bound Gate Template

{md_table(bound_gates, ["gate_id", "observable", "residual_bound_formula", "coefficient_gate", "required_inputs", "current_numeric_status", "claim_allowed"])}

## Owner Edge Audit

{md_table(owner_edges, ["edge_id", "candidate_edge", "source_status", "would_zero", "current_result", "next_proof_input", "activates_zero_now"])}

## Runner

{md_table(runner, ["runner_id", "step", "formula", "status", "valid_for_claim"])}

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
    text = f"""# 4370: epsilon_Gsrc coefficient bound or Xi owner edge proof

Marker: `{MARKER}`

## What changed

- Used `int_W rho_H epsilon_Gsrc_perp dV=0` to derive a sharper zero-monopole far-field gate.
- Converted the Newton/source-normalization obstruction to `E_perp <= delta_N/K_N(s)`.
- Added geometry factors for representative `R/r` values.
- Audited the owner-edge zero route and kept it unsigned.

## Decision row

{md_table(decisions, ["decision_id", "decision", "summary", "next_target"])}

## Next target

{md_table(next_targets, ["next_id", "target", "question", "preferred_route", "alternate_zero_route", "avoid"])}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def write_spine_update() -> None:
    block = f"""
## 4370 Transition epsilon_Gsrc coefficient gate

Marker: `{MARKER}`

4370 sharpens the `epsilon_Gsrc_perp` route. Because the common Hilbert-source monopole is subtracted, `int_W rho_H epsilon_Gsrc_perp dV=0`; the far-field acceleration residual can use a zero-monopole geometry factor rather than the coarser source envelope alone:

```text
K_N(s)=min((1-s)^-2, 2s(1-s)^-3),  s=R/r,
E_perp <= delta_N_obs/K_N(s).
```

The owner-edge route remains unsigned: the measure/Jacobian owner, current/readout owner, same-source-mass and no-reentry clauses are not parent-certified on one branch. The next target is therefore concrete: source `R/r` and `E_perp` for this bound gate, or prove the measure-owner edge. Next target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, block)


def write_packet_update() -> None:
    block = f"""
## 4370 packet update: zero-monopole epsilon_Gsrc gate

Marker: `{PACKET_MARKER}`

Packet update: `epsilon_Gsrc_perp` now has a scoreable coefficient gate. The common monopole is removed, giving far-field suppression controlled by `K_N(s)=min((1-s)^-2,2s(1-s)^-3)`. This still is not a local-GR pass: the packet needs source/worldtube support inputs or a real measure-owner edge proof.
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
                "4370 turns the epsilon_Gsrc_perp Newton/source-normalization obstruction into a coefficient-bound gate. "
                "Because epsilon_Gsrc_perp has zero Hilbert-source monopole, the far-field acceleration residual obeys "
                "K_N(s)=min((1-s)^-2,2s(1-s)^-3) with s=R/r, so a real Newton/source bound can be scored by E_perp<=delta_N_obs/K_N(s). "
                "The owner-edge zero route was checked against 4361/1606/4178 and remains unsigned. "
                "No local-GR/Newton/PPN/WEP/clock/orbital/R10 claim fires."
            ),
            "4370 source register, bound theorem rows, geometry factor table, bound gate template, owner edge audit, runner, claim gates, decision, status, next target and validation CSV.",
            "epsilon_Gsrc_monopole_subtracted_bound_gate_derived_owner_edge_unsigned_nonclaim",
            "Source R/r and E_perp inputs for the Newton/source-normalization gate, or prove the species-blind measure/Jacobian owner edge.",
            "Calling the symbolic gate a pass; fitting R/r or E_perp after seeing data; absorbing noncommon source labels into G_cal; ignoring Xi_open/T_open/Bianchi/boundary tails.",
        ],
    )


def validation_rows(csv_paths: List[Path]) -> List[Dict[str, str]]:
    validations: List[Dict[str, str]] = []
    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4370_SOURCE_REGISTER.csv")
    theorem = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4370_BOUND_THEOREMS.csv")
    geometry = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4370_GEOMETRY_FACTOR_TABLE.csv")
    owner = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4370_OWNER_EDGE_AUDIT.csv")
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4370_CLAIM_GATES.csv")

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append(
            {
                "checkpoint": CHECKPOINT,
                "check_id": check_id,
                "passed": str(bool(passed)),
                "detail": detail,
            }
        )

    add("VAL4370_0_all_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source path exists")
    add("VAL4370_1_all_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited source needle resolves")
    add(
        "VAL4370_2_zero_monopole_theorem",
        any(row["theorem_id"] == "TH4370_0_zero_monopole_identity" and "int_W" in row["formula"] for row in theorem),
        "zero-monopole identity row exists",
    )
    add(
        "VAL4370_3_acceleration_gate",
        any(row["theorem_id"] == "TH4370_3_safe_bound_selector" and "K_N" in row["formula"] for row in theorem),
        "safe acceleration bound selector exists",
    )
    add(
        "VAL4370_4_geometry_positive",
        all(float(row["selected_K_N"]) > 0 for row in geometry),
        "all geometry factors are positive",
    )
    add(
        "VAL4370_5_owner_edges_unsigned",
        all(row["activates_zero_now"] == "False" for row in owner),
        "no owner edge falsely activates the zero route",
    )
    add("VAL4370_6_claim_gates_false", all(row["claim_allowed"] == "False" for row in gates), "all claim gates false")
    add("VAL4370_7_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4370_8_post_marker", MARKER in read_text(DOC_PATH), "post marker present")
    add("VAL4370_9_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4370_10_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4370_11_claim_row", f"\n{CLAIM_ID}," in read_text(CLAIMS_PATH), "claim row appended")
    add(
        "VAL4370_12_no_valid_claim_rows",
        all("True" not in [row.get("valid_for_claim", ""), row.get("claim_allowed", "")] for path in csv_paths for row in read_csv(path)),
        "generated rows remain nonclaim",
    )
    add(
        "VAL4370_13_csv_parse",
        all(len(read_csv(path)) > 0 for path in csv_paths),
        "all generated CSVs parse",
    )
    return validations


def main() -> None:
    sources = source_rows()
    theorem = theorem_rows()
    geometry = geometry_rows()
    bound_gates = bound_gate_rows()
    owner_edges = owner_edge_rows()
    runner = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    csv_payloads: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4370_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4370_BOUND_THEOREMS.csv": theorem,
        "P8_Y5_R2FR_4370_GEOMETRY_FACTOR_TABLE.csv": geometry,
        "P8_Y5_R2FR_4370_BOUND_GATE_TEMPLATE.csv": bound_gates,
        "P8_Y5_R2FR_4370_OWNER_EDGE_AUDIT.csv": owner_edges,
        "P8_Y5_R2FR_4370_RUNNER.csv": runner,
        "P8_Y5_R2FR_4370_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4370_DECISION.csv": decisions,
        "P8_Y5_R2FR_4370_STATUS.csv": statuses,
        "P8_Y5_R2FR_4370_NEXT_TARGET.csv": next_targets,
    }

    csv_paths: List[Path] = []
    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)

    write_formal_doc(sources, theorem, geometry, bound_gates, owner_edges, runner, gates, decisions, statuses, next_targets)
    write_post_doc(decisions, next_targets)
    write_spine_update()
    write_packet_update()
    write_claim()

    write_csv(VALIDATION_PATH, validation_rows(csv_paths))


if __name__ == "__main__":
    main()
