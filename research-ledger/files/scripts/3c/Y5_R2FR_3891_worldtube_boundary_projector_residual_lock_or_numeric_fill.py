from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3891"
BRANCH = "MTS_R2FR_Y5_WORLDTUBE_BOUNDARY_PROJECTOR_RESIDUAL_LOCK_OR_NUMERIC_FILL_3891"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3891-Y5-R2FR-worldtube-boundary-projector-residual-lock-or-numeric-fill.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

CSV_3890_NEXT = OUT / "P8_Y5_R2FR_3890_NEXT_TARGET.csv"
CSV_3890_REMAINING = OUT / "P8_Y5_R2FR_3890_REMAINING_SOURCE_CHANNELS.csv"
CSV_3890_INPUT = OUT / "P8_Y5_R2FR_3890_NUMERIC_COEFFICIENT_INPUT_PRIORITY_QUEUE.csv"
CSV_3890_GATE = OUT / "P8_Y5_R2FR_3890_LOCAL_GR_DECISION_GATE.csv"
CSV_3890_VALIDATION = OUT / "P8_Y5_BRR545_3890_VALIDATION.csv"
CSV_HWT = OUT / "P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv"
CSV_WSM = OUT / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv"
CSV_PWT = OUT / "P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv"
CSV_LOCAL_ZERO = OUT / "P8_LOCAL_ZERO_BOUNDARY_R11_IMPLICATION_AUDIT.csv"
CSV_BOUNDARY_ALPHA3 = OUT / "P8_BOUNDARY_ALPHA3_NOFLUX_THEOREM_ATTEMPT.csv"
CSV_BOUNDARY_DECISION = OUT / "P8_BOUNDARY_ALPHA3_DECISION.csv"
CSV_BCOH = OUT / "P8_Y5_BRR545_BOUNDARY_COHOMOLOGY_NOHAIR_THEOREM_ATTEMPT.csv"
CSV_BFLUX = OUT / "P8_Y5_BRR545_BOUNDARY_FLUX_BOUND_FILL_ROW.csv"
CSV_PIM_CONTRACT = OUT / "P8_PiM_projector_variation_stress_CONTRACT.csv"
CSV_PIM_SILENCE = OUT / "P8_Y5_BRR545_PROJECTOR_SYMPLECTIC_SILENCE_THEOREM_ATTEMPT.csv"
CSV_R11_FILL = OUT / "P8_R11_BOUNDARY_STRESS_CLOSURE_FILL_PACK.csv"
CSV_3884_FLUX = OUT / "P8_Y5_R2FR_3884_PIM_HILBERT_FLUX_CLOSURE_THEOREM.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3891_SOURCE_REGISTER.csv",
    "worldtube": OUT / "P8_Y5_R2FR_3891_WORLDTUBE_SUPPORT_DESCENT_ATTEMPT.csv",
    "boundary_projector": OUT / "P8_Y5_R2FR_3891_BOUNDARY_PROJECTOR_SILENCE_ATTEMPT.csv",
    "residual_lock": OUT / "P8_Y5_R2FR_3891_RESIDUAL_LOCK_MAP.csv",
    "numeric_fill": OUT / "P8_Y5_R2FR_3891_NUMERIC_FILL_ROWS.csv",
    "gate": OUT / "P8_Y5_R2FR_3891_LOCAL_GR_DECISION_GATE.csv",
    "runner": OUT / "P8_Y5_R2FR_3891_RUNNER_UPDATE.csv",
    "next": OUT / "P8_Y5_R2FR_3891_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3891_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3891_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3891_00_next", CSV_3890_NEXT, "NEXT3890_0", "3890 selected worldtube/boundary/projector target"),
    ("SRC3891_01_remaining", CSV_3890_REMAINING, "REM3890_0_worldtube", "remaining channel ledger"),
    ("SRC3891_02_input", CSV_3890_INPUT, "INP3890_0_worldtube", "numeric input queue"),
    ("SRC3891_03_gate", CSV_3890_GATE, "LGG3890_7_local_GR", "3890 local-GR gate"),
    ("SRC3891_04_validation", CSV_3890_VALIDATION, "VAL3890_15_next_target", "3890 validation"),
    ("SRC3891_05_HWT", CSV_HWT, "HWT536_0_parent_worldtube_fixed", "Hilbert worldtube theorem attempt"),
    ("SRC3891_06_WSM", CSV_WSM, "T510_2_MTS_transfer_condition", "worldtube source measure theorem"),
    ("SRC3891_07_PWT", CSV_PWT, "W504_3_exterior_closure_equation", "parent worldtube glue clauses"),
    ("SRC3891_08_local_zero", CSV_LOCAL_ZERO, "I2_boundary_alpha3_preferred_momentum", "boundary scalar/no-flux limitation"),
    ("SRC3891_09_boundary_alpha3", CSV_BOUNDARY_ALPHA3, "T5_parent_owner_audit", "boundary alpha3 no-flux theorem attempt"),
    ("SRC3891_10_boundary_decision", CSV_BOUNDARY_DECISION, "D1_parent_ownership", "boundary parent ownership decision"),
    ("SRC3891_11_BCOH", CSV_BCOH, "BCT549_6_certificate_verdict", "boundary cohomology/nohair result"),
    ("SRC3891_12_BFLUX", CSV_BFLUX, "FB549_0_boundary_flux_bound", "boundary flux fill row"),
    ("SRC3891_13_PIM_contract", CSV_PIM_CONTRACT, "PV6_modified_exterior_residual_map", "PiM projector variation contract"),
    ("SRC3891_14_PIM_silence", CSV_PIM_SILENCE, "PST550_7_certificate_verdict", "projector silence theorem attempt"),
    ("SRC3891_15_R11_fill", CSV_R11_FILL, "F6_projector_stress", "projector stress fill row"),
    ("SRC3891_16_3884_flux", CSV_3884_FLUX, "PFC3884_1_product_rule", "PiM Hilbert flux product rule"),
]

WORLDTUBE_DESCENT = "W_source := supp J_H[tau] before Pi_M/orbital readout; if J_H and tau are q-basic, then delta_y W_source=0 for y in ker(Dq), up to support-jump/corner terms"
BOUNDARY_GUARD = "scalar volume no-flux does not imply n_mu P_loc_nu K_boundary^{mu nu}=0; vector/shear/normal-exchange boundary channels must be topological/no-flux or retained"
PROJECTOR_GUARD = "delta(Pi_M J_H)=Pi_M delta J_H+(delta Pi_M)J_H and d(Pi_M J_H)=Pi_M dJ_H+[d,Pi_M]J_H; projector silence needs delta Pi_M=0 and [d,Pi_M]=0 by parent/topology"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PCW))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return ""
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, sep]
    for row in rows:
        cells = [str(row.get(col, "")).replace("\n", " ").replace("|", "\\|") for col in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows = []
    for source_id, path, needle, role in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "checkpoint": CHECKPOINT,
                "path": rel(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "claim_use": "nonclaim_worldtube_boundary_projector_residual_lock",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def worldtube_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("WSD3891_0_definition", "worldtube support owner", "define W_source from same Hilbert current before readout", "W_source=supp J_H[tau]", "CANDIDATE_DEFINITION_INSERTED", "not a fitted orbital mask"),
        ("WSD3891_1_descent", "quotient descent", WORLDTUBE_DESCENT, "delta_y W_source=0 if support is regular and q-basic", "PASS_CANDIDATE_BRANCH_WITH_REGULAR_SUPPORT", "corner/support jumps remain retained"),
        ("WSD3891_2_charge", "dressed source charge", "M_source[W]=H_tau[S_outer]-H_tau[reference], not bare rest mass", "measured mass is dressed Hamiltonian/Hilbert charge", "DEFINITION_GUARDRAIL", "source charge equality still needs exterior glue"),
        ("WSD3891_3_exterior", "exterior closure", "dQ_M[tau]=C_EH+C_extra+C_projector+C_boundary+C_Lambda_sub", "radial independence only if every C term is zero/bounded", "OPEN_EXTRA_TERMS", "projector/boundary/R11/memory still live"),
        ("WSD3891_4_update", "A_worldtube_matter", "A_worldtube_matter=0 in the 3891 candidate branch if W_source=supp J_H[tau] is q-basic and support-regular", "candidate zero for support variation only", "CANDIDATE_ZERO_NOT_GLOBAL", "not valid for claim until support regularity and charge glue are adopted"),
    ]
    return [
        {
            "worldtube_id": row_id,
            "piece": piece,
            "statement_or_math": statement,
            "effect": effect,
            "status": status,
            "remaining_failure": failure,
            "candidate_branch_signed": "CANDIDATE" in status or "PASS_CANDIDATE" in status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, piece, statement, effect, status, failure in raw_rows
    ]


def boundary_projector_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("BPS3891_0_boundary_guard", "boundary preferred momentum", BOUNDARY_GUARD, "BOUNDARY_VECTOR_CHANNEL_RETAINED", "alpha3/xi/Gdot boundary rows remain live"),
        ("BPS3891_1_scalar_boundary", "scalar stationary boundary lemma", "S_B=int_boundary sqrt(|gamma|)F(scalars), D_A scalars=0 => tau_AB proportional gamma_AB and no normal preferred-momentum flux", "CONDITIONAL_LEMMA_ONLY", "parent action has not signed scalar-only marker-free boundary class"),
        ("BPS3891_2_boundary_cohomology", "relative cohomology/no-hair", "[B_imp]=0 and int_S2 B_imp-int_S1 B_imp=0 if exact relative class is parent-fixed", "CONDITIONAL_NOT_PARENT_OWNED", "finite surface charge/corner/reference terms remain possible"),
        ("BPS3891_3_boundary_fill", "boundary numeric fill", "epsilon_B_flux_abs plus c_B_flux_to_{alpha3,xi,beta} and time/radial profiles required if no-flux fails", "FILL_REQUIRED_IF_CERTIFICATE_FAILS", "FB549 row still missing numeric values"),
        ("BPS3891_4_projector_product", "projector product rule", PROJECTOR_GUARD, "EXACT_GUARD_RETAINED", "cannot drop delta Pi_M or commutator by notation"),
        ("BPS3891_5_projector_topological", "topological projector route", "Pi_M J=ell_M(J) omega_M_top with d omega_M_top=0, delta_g Pi_M=0, [d,Pi_M]=0", "CONDITIONAL_ROUTE_AVAILABLE", "charge functional/source equality/domain owner not parent-derived"),
        ("BPS3891_6_projector_fill", "projector numeric fill", "T_extra_munu or P_PPN[T_extra_munu] must be mapped into gamma,beta,alpha_i,xi,zeta_i if topological route fails", "FILL_REQUIRED_IF_CERTIFICATE_FAILS", "projector PPN component map missing"),
    ]
    return [
        {
            "bp_id": row_id,
            "piece": piece,
            "statement_or_math": statement,
            "status": status,
            "remaining_failure": failure,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, piece, statement, status, failure in raw_rows
    ]


def residual_lock_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("RLM3891_0_direct_matter", "direct hidden matter/source", "3890 candidate grammar zeros A_direct_matter, delta_w_A, hidden frames, alpha/mass vertices", "LOCKED_IN_CANDIDATE_BRANCH", "does not close boundary/projector/memory/R11"),
        ("RLM3891_1_worldtube", "worldtube support", "W_source=supp J_H[tau] q-basic gives candidate delta_y W_source=0", "PARTIAL_LOCK_CANDIDATE", "support jumps/corners and source charge equality still open"),
        ("RLM3891_2_boundary", "boundary flux residual", "scalar volume no-flux is insufficient for preferred momentum; alpha3/xi/Gdot boundary pieces stay physical residuals", "RETAINED_RESIDUAL", "needs topological/no-flux certificate or numeric fill"),
        ("RLM3891_3_projector", "projector/readout residual", "Pi_M variation and commutator terms stay physical unless topological absolute projector is parent-owned", "RETAINED_RESIDUAL", "needs source-charge equality and stress map"),
        ("RLM3891_4_memory", "memory/time residual", "compact local memory silence not proved by matter grammar or worldtube support", "RETAINED_RESIDUAL", "needs Gdot/clock profile or theorem-zero"),
        ("RLM3891_5_R11", "non-EH operator residual", "Sigma_loc factorization still required for all R11 families", "RETAINED_RESIDUAL", "needs universal factorization or gamma/beta/R10 fill"),
        ("RLM3891_6_total", "full Y_loc physical residual-lock", "Y_loc now partially locks direct source and candidate worldtube support, but boundary/projector/memory/R11 remain physical residuals", "PARTIAL_LOCK_NO_LOCAL_GR", "no local-GR claim"),
    ]
    return [
        {
            "lock_id": row_id,
            "component": component,
            "lock_statement": statement,
            "status": status,
            "remaining_failure": failure,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, component, statement, status, failure in raw_rows
    ]


def numeric_fill_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("NF3891_0_worldtube_corner", "A_worldtube_corner", "E_star_norm", "support jump/corner/source-measure leak", "||delta_y W_source||_{E*}", "if regular q-basic support fails", "source support variation or bound"),
        ("NF3891_1_boundary_alpha3", "epsilon_B_flux_abs;c_B_flux_to_alpha3", "dimensionless", "boundary preferred-momentum flux", "abs(c_B_flux_to_alpha3*epsilon_B_flux_abs)<=4e-20", "if scalar/topological no-flux fails", "boundary flux coefficient/product"),
        ("NF3891_2_boundary_xi_beta_Gdot", "c_B_flux_to_xi;c_B_flux_to_beta;partial_t epsilon_B_flux_abs", "mixed", "boundary preferred-location/source/time channels", "xi<=4e-09, beta<=7.8e-05, |Gdot/G|<=9.6e-15/yr", "if derivative silence fails", "boundary coefficient/profile"),
        ("NF3891_3_projector_PPN", "P_PPN[T_extra_munu]", "dimensionless_vector", "projector stress PPN vector", "each gamma,beta,alpha_i,xi,zeta_i component below bound", "if topological projector fails", "projector weak-field component map"),
        ("NF3891_4_memory_Gdot", "partial_t K_history", "yr^-1", "local memory/time drift", "|partial_t K_history + ...|<=9.6e-15/yr", "if compact local memory silence fails", "time profile/frame lock"),
        ("NF3891_5_R11_gamma_beta_R10", "C_gamma^F;c_F;K_X(lambda);Q_X^H;q_X^test", "mixed", "non-EH/R11 weak-field and range residuals", "gamma,beta,R10 rows pass individually", "if Sigma_loc factorization fails", "operator coefficients and source charges"),
    ]
    return [
        {
            "fill_id": row_id,
            "needed_input": needed,
            "units": units,
            "residual_channel": channel,
            "pass_rule": rule,
            "trigger": trigger,
            "required_data_or_derivation": required,
            "current_status": "MISSING_NUMERIC_INPUT_OR_THEOREM_ZERO",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, needed, units, channel, rule, trigger, required in raw_rows
    ]


def gate_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("LGG3891_0_direct_source", "direct hidden matter/source", "3890 grammar-signed candidate zero", "PASS_CANDIDATE_BRANCH_NONCLAIM"),
        ("LGG3891_1_worldtube_support", "worldtube support descent", WORLDTUBE_DESCENT, "PASS_CANDIDATE_WITH_REGULAR_SUPPORT_NONCLAIM"),
        ("LGG3891_2_source_charge_glue", "worldtube source charge equality", "same dressed Hilbert/Noether charge controls exterior monopole", "FAIL_OPEN"),
        ("LGG3891_3_boundary", "boundary no-flux/topological silence", BOUNDARY_GUARD, "FAIL_OPEN_RETAINED"),
        ("LGG3891_4_projector", "projector fixed/q-basic/topological silence", PROJECTOR_GUARD, "FAIL_OPEN_RETAINED"),
        ("LGG3891_5_residual_lock", "full physical residual-lock", "Y_loc equals all physical PPN/R10/R11 residuals", "PARTIAL_LOCK_ONLY"),
        ("LGG3891_6_numeric_fill", "numeric fill fallback", "rows exist for worldtube corner, boundary, projector, memory and R11", "PASS_QUEUE_READY_NONCLAIM"),
        ("LGG3891_7_local_GR", "local-GR promotion", "all remaining channels theorem-zero or bounded", "BLOCKED_NO_CLAIM"),
    ]
    return [
        {
            "gate_id": row_id,
            "gate": gate,
            "requirement": req,
            "status": status,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, gate, req, status in raw_rows
    ]


def runner_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("RUNU3891_0_worldtube", "worldtube_support", "treat A_worldtube_matter as candidate-zero only when W_source=supp J_H[tau] is q-basic and support-regular before readout", "CONDITIONAL_RULE"),
        ("RUNU3891_1_boundary", "boundary_guard", "never convert scalar volume no-flux into alpha3/vector no-flux without scalar-only marker-free boundary certificate", "NO_SCALAR_TO_VECTOR_SHORTCUT"),
        ("RUNU3891_2_projector", "projector_guard", "retain delta Pi_M and [d,Pi_M]J_H unless topological absolute projector certificate is signed", "NO_DROPPED_PROJECTOR_STRESS"),
        ("RUNU3891_3_fill", "numeric_fill", "if certificate fails, fill numeric rows in the 3891 queue with no cancellation credit", "QUEUE_READY"),
        ("RUNU3891_4_next", "next_attack", "attack boundary/projector topological certificates first, then numeric coefficient fills", "NEXT_3892"),
    ]
    return [
        {
            "update_id": row_id,
            "runner_field": field,
            "rule": rule,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, field, rule, status in raw_rows
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3891_0",
            "target_checkpoint": "3892-Y5-R2FR-boundary-projector-topological-certificate-or-fill-alpha3-projector-inputs.md",
            "script": "scripts/Y5_R2FR_3892_boundary_projector_topological_certificate_or_fill_alpha3_projector_inputs.py",
            "objective": "try to sign the scalar/topological boundary no-flux certificate and the absolute/topological projector certificate; if either fails, begin filling alpha3/xi/beta/Gdot boundary products and projector PPN component maps",
            "why_next": "3891 candidate-closes direct source and worldtube support descent but leaves boundary preferred-momentum and projector stress as the dominant local-GR blockers",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "status_id": "STATUS3891_0",
            "branch": BRANCH,
            "summary": "worldtube support descent is candidate-closed if defined as q-basic Hilbert support before readout; boundary no-flux and projector stress remain retained blockers; residual-lock is partial; numeric fill rows prepared",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    worldtube: list[dict[str, object]],
    boundary_projector: list[dict[str, object]],
    residual_lock: list[dict[str, object]],
    numeric_fill: list[dict[str, object]],
    gate: list[dict[str, object]],
    runner: list[dict[str, object]],
    next_target: list[dict[str, object]],
    timestamp: str,
) -> None:
    resolved = sum(1 for row in sources if row["exists"] and row["needle_found"])
    doc = f"""# 3891 - Worldtube, Boundary, Projector Residual-Lock or Numeric Fill

Generated: `{timestamp}`

## Result

3891 narrows the remaining local source problem.

Worldtube support descent:

`{WORLDTUBE_DESCENT}`

Boundary guard:

`{BOUNDARY_GUARD}`

Projector guard:

`{PROJECTOR_GUARD}`

The useful win is worldtube support: in the candidate branch, if the source worldtube is defined as the support of the same q-basic Hilbert current before readout, then vertical hidden variations do not move it except for explicit support-jump/corner terms. The non-win is equally important: scalar volume no-flux still does not kill boundary preferred momentum, and projector stress still cannot be dropped unless Pi_M is parent-owned as a topological/fixed projector.

## Worldtube Support Descent Attempt

{markdown_table(worldtube, ["worldtube_id", "piece", "statement_or_math", "effect", "status", "remaining_failure"])}

## Boundary and Projector Silence Attempt

{markdown_table(boundary_projector, ["bp_id", "piece", "statement_or_math", "status", "remaining_failure"])}

## Residual Lock Map

{markdown_table(residual_lock, ["lock_id", "component", "lock_statement", "status", "remaining_failure"])}

## Numeric Fill Rows

{markdown_table(numeric_fill, ["fill_id", "needed_input", "units", "residual_channel", "pass_rule", "trigger"])}

## Local-GR Decision Gate

{markdown_table(gate, ["gate_id", "gate", "requirement", "status", "claim_allowed"])}

## Runner Update

{markdown_table(runner, ["update_id", "runner_field", "rule", "status"])}

## Source Register

Resolved `{resolved}/{len(sources)}` source rows.

{markdown_table(sources, ["source_id", "path", "needle_found", "role"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_checkpoint", "objective", "why_next"])}

## Bottom Line

This is a real tightening of the route. Direct hidden matter/source is candidate-zero from 3890, and worldtube support can be candidate-zero if it is Hilbert/q-basic before readout. The dominant blockers are now boundary preferred-momentum flux and projector stress. Those need either topological/no-flux certificates or actual numeric coefficient products.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    start = "<!-- BEGIN 3891 WORLDTUBE BOUNDARY PROJECTOR -->"
    end = "<!-- END 3891 WORLDTUBE BOUNDARY PROJECTOR -->"
    block = f"""{start}

## 3891 - Worldtube support descent, boundary/projector guards

Worldtube support descent:

`{WORLDTUBE_DESCENT}`

Boundary guard:

`{BOUNDARY_GUARD}`

Projector guard:

`{PROJECTOR_GUARD}`

Status: worldtube support descent is candidate-closed under q-basic Hilbert support before readout and support regularity. Boundary preferred-momentum flux and projector stress remain live blockers. Residual-lock is partial, not enough for local GR.

Generated outputs:
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3891_WORLDTUBE_SUPPORT_DESCENT_ATTEMPT.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3891_BOUNDARY_PROJECTOR_SILENCE_ATTEMPT.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3891_RESIDUAL_LOCK_MAP.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3891_NUMERIC_FILL_ROWS.csv`
- `source-intake\\mts_residuals\\P8_Y5_BRR545_3891_VALIDATION.csv`

Next gate: `3892`, boundary/projector topological certificate or alpha3/projector numeric fills.

<!-- Generated by 3891 at {timestamp} -->
{end}
"""
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else "# Local GR Coupling Spine Current State\n"
    if start in existing and end in existing:
        before = existing.split(start)[0].rstrip()
        after = existing.split(end, 1)[1].lstrip()
        new_text = f"{before}\n\n{block}\n\n{after}".rstrip() + "\n"
    else:
        new_text = existing.rstrip() + "\n\n" + block + "\n"
    SPINE_PATH.write_text(new_text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    worldtube: list[dict[str, object]],
    boundary_projector: list[dict[str, object]],
    residual_lock: list[dict[str, object]],
    numeric_fill: list[dict[str, object]],
    gate: list[dict[str, object]],
    runner: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    checks: list[tuple[str, str, bool, str]] = []
    resolved = sum(1 for row in sources if row["exists"] and row["needle_found"])
    checks.append(("VAL3891_0_sources", "all cited source paths exist and needles are found", resolved == len(sources), f"{resolved}/{len(sources)} sources resolved"))
    checks.append(("VAL3891_1_worldtube", "worldtube support descent candidate is explicit", any("delta_y W_source=0" in str(row["statement_or_math"]) for row in worldtube), "WSD3891_1"))
    checks.append(("VAL3891_2_boundary_guard", "boundary scalar-to-vector shortcut is rejected", any("scalar volume no-flux" in str(row["statement_or_math"]) for row in boundary_projector), "BPS3891_0"))
    checks.append(("VAL3891_3_projector_guard", "projector product/commutator rule is retained", any("delta(Pi_M J_H)" in str(row["statement_or_math"]) and "[d,Pi_M]" in str(row["statement_or_math"]) for row in boundary_projector), "BPS3891_4"))
    required_locks = {"direct hidden matter/source", "worldtube support", "boundary flux residual", "projector/readout residual", "memory/time residual", "non-EH operator residual", "full Y_loc physical residual-lock"}
    found_locks = {str(row["component"]) for row in residual_lock}
    checks.append(("VAL3891_4_residual_lock", "residual lock map covers direct/worldtube/boundary/projector/memory/R11/total", required_locks.issubset(found_locks), f"{len(found_locks)} locks"))
    required_fills = {"A_worldtube_corner", "epsilon_B_flux_abs;c_B_flux_to_alpha3", "c_B_flux_to_xi;c_B_flux_to_beta;partial_t epsilon_B_flux_abs", "P_PPN[T_extra_munu]", "partial_t K_history", "C_gamma^F;c_F;K_X(lambda);Q_X^H;q_X^test"}
    found_fills = {str(row["needed_input"]) for row in numeric_fill}
    checks.append(("VAL3891_5_numeric_fill", "numeric fill rows cover remaining local blockers", required_fills.issubset(found_fills), f"{len(found_fills)} fill rows"))
    checks.append(("VAL3891_6_local_gr_no_claim", "local GR remains blocked", any(row["gate_id"] == "LGG3891_7_local_GR" and "BLOCKED" in str(row["status"]) for row in gate), "LGG3891_7"))
    checks.append(("VAL3891_7_all_nonclaim", "all generated analytic rows are nonclaim", all(str(row.get("valid_for_claim")) == "False" for collection in [worldtube, boundary_projector, residual_lock, numeric_fill, gate, runner] for row in collection), "valid_for_claim=false"))
    checks.append(("VAL3891_8_runner", "runner forbids scalar no-flux shortcut", any(row["runner_field"] == "boundary_guard" and "scalar volume no-flux" in str(row["rule"]) for row in runner), "RUNU3891_1"))
    checks.append(("VAL3891_9_doc", "markdown checkpoint exists with bottom line", DOC_PATH.exists() and "dominant blockers are now boundary preferred-momentum flux and projector stress" in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3891_10_spine", "spine updated with 3891 block", SPINE_PATH.exists() and "BEGIN 3891 WORLDTUBE BOUNDARY PROJECTOR" in read_text(SPINE_PATH), rel(SPINE_PATH)))
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_parse_ok = True
    parse_details = []
    for path in csv_outputs:
        try:
            parse_details.append(f"{path.name}:{len(read_csv_rows(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parse_details.append(f"{path.name}:{exc}")
    checks.append(("VAL3891_11_csv_parse", "all generated CSV outputs parse", csv_parse_ok, "; ".join(parse_details)))
    formalization_hits = []
    if FWB.exists():
        formalization_hits = [path for path in FWB.rglob("*3891*") if path.is_file() and ("3891-Y5" in path.name or "P8_Y5_R2FR_3891" in path.name or "P8_Y5_BRR545_3891" in path.name)]
    checks.append(("VAL3891_12_formalization_untouched", "no generated 3891 files appear in formalization-workbench", not formalization_hits, f"{len(formalization_hits)} hits"))
    pycache_hits = [path for path in (PCW / "scripts").rglob("__pycache__") if path.is_dir()]
    checks.append(("VAL3891_13_no_pycache", "scripts __pycache__ removed", not pycache_hits, f"{len(pycache_hits)} pycache dirs"))
    checks.append(("VAL3891_14_next_target", "next target attacks boundary/projector certificate or numeric fill", any("boundary-projector-topological-certificate" in str(row["target_checkpoint"]) for row in next_rows(timestamp)), "3892 boundary/projector"))
    return [
        {
            "check_id": check_id,
            "description": description,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for check_id, description, passed, detail in checks
    ]


def main() -> int:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    worldtube = worldtube_rows(timestamp)
    boundary_projector = boundary_projector_rows(timestamp)
    residual_lock = residual_lock_rows(timestamp)
    numeric_fill = numeric_fill_rows(timestamp)
    gate = gate_rows(timestamp)
    runner = runner_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["worldtube"], worldtube)
    write_csv(OUTPUTS["boundary_projector"], boundary_projector)
    write_csv(OUTPUTS["residual_lock"], residual_lock)
    write_csv(OUTPUTS["numeric_fill"], numeric_fill)
    write_csv(OUTPUTS["gate"], gate)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, worldtube, boundary_projector, residual_lock, numeric_fill, gate, runner, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, worldtube, boundary_projector, residual_lock, numeric_fill, gate, runner, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_WORLDTUBE_CANDIDATE_BOUNDARY_PROJECTOR_RETAINED")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
