from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3890"
BRANCH = "MTS_R2FR_Y5_SIGN_PARENT_GRAMMAR_IN_ACTION_OR_FILL_NUMERIC_COEFFICIENT_INPUTS_3890"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3890-Y5-R2FR-sign-parent-grammar-in-action-or-fill-numeric-coefficient-inputs.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

CSV_3889_NEXT = OUT / "P8_Y5_R2FR_3889_NEXT_TARGET.csv"
CSV_3889_THEOREM = OUT / "P8_Y5_R2FR_3889_PARENT_OBJECT_LANGUAGE_NO_DIRECT_SOURCE_THEOREM.csv"
CSV_3889_GRAMMAR = OUT / "P8_Y5_R2FR_3889_DIRECT_SLOT_EXCLUSION_MATRIX.csv"
CSV_3889_PRED = OUT / "P8_Y5_R2FR_3889_PREDICTION_SIDE_COEFFICIENT_ROWS.csv"
CSV_3889_DECISION = OUT / "P8_Y5_R2FR_3889_ROUTE_DECISION_GATE.csv"
CSV_3889_VALIDATION = OUT / "P8_Y5_BRR545_3889_VALIDATION.csv"
CSV_3882_ACTION = OUT / "P8_Y5_R2FR_3882_PARENT_ACTION_CSTAR_THREEFORM_STACK.csv"
CSV_3883_HILBERT = OUT / "P8_Y5_R2FR_3883_SAME_HILBERT_SOURCE_LOCK.csv"
CSV_3884_FLUX = OUT / "P8_Y5_R2FR_3884_PIM_HILBERT_FLUX_CLOSURE_THEOREM.csv"
CSV_3887_CLAUSES = OUT / "P8_Y5_R2FR_3887_PARENT_ACTION_CLAUSE_REQUIREMENTS.csv"
CSV_3888_CHANNELS = OUT / "P8_Y5_R2FR_3888_SOURCE_CHANNEL_SPLIT.csv"
CSV_2612_COEF = OUT / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_AMATTER_COEFFICIENT_PACK.csv"
CSV_2611_AMATTER = OUT / "P8_Y5_MATTER_DESCENT_GATE_2611_AMATTER_BOUND_INTERFACE.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3890_SOURCE_REGISTER.csv",
    "insertion": OUT / "P8_Y5_R2FR_3890_PARENT_ACTION_GRAMMAR_INSERTION.csv",
    "direct_zero": OUT / "P8_Y5_R2FR_3890_DIRECT_SOURCE_ZERO_UPDATE.csv",
    "remaining": OUT / "P8_Y5_R2FR_3890_REMAINING_SOURCE_CHANNELS.csv",
    "input_queue": OUT / "P8_Y5_R2FR_3890_NUMERIC_COEFFICIENT_INPUT_PRIORITY_QUEUE.csv",
    "gate": OUT / "P8_Y5_R2FR_3890_LOCAL_GR_DECISION_GATE.csv",
    "runner": OUT / "P8_Y5_R2FR_3890_RUNNER_UPDATE.csv",
    "next": OUT / "P8_Y5_R2FR_3890_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3890_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3890_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3890_00_next", CSV_3889_NEXT, "NEXT3889_0", "3889 selected parent grammar signing target"),
    ("SRC3890_01_theorem", CSV_3889_THEOREM, "OLT3889_2_no_Hom", "Hom/no-marker theorem"),
    ("SRC3890_02_grammar", CSV_3889_GRAMMAR, "GEX3889_1_relative_w", "direct slot exclusion matrix"),
    ("SRC3890_03_predictions", CSV_3889_PRED, "PRED3889_1_delta_w", "prediction-side coefficient rows"),
    ("SRC3890_04_decision", CSV_3889_DECISION, "DEC3889_4_local_GR", "3889 route decision"),
    ("SRC3890_05_validation", CSV_3889_VALIDATION, "VAL3889_14_next_target", "3889 validation"),
    ("SRC3890_06_action", CSV_3882_ACTION, "ACT3882_1_action", "candidate parent action"),
    ("SRC3890_07_action_restrict", CSV_3882_ACTION, "ACT3882_2_no_direct_C_matter", "candidate matter/source restriction"),
    ("SRC3890_08_hilbert_action", CSV_3883_HILBERT, "HSL3883_0_action", "same observed matter action"),
    ("SRC3890_09_hilbert_same", CSV_3883_HILBERT, "HSL3883_2_same_source", "same Hilbert source lock"),
    ("SRC3890_10_flux_limits", CSV_3884_FLUX, "PFC3884_4_limits", "remaining flux/projector limits"),
    ("SRC3890_11_y_clauses", CSV_3887_CLAUSES, "PAC3887_5_residual_lock", "residual-lock clause"),
    ("SRC3890_12_channels", CSV_3888_CHANNELS, "SRCCH3888_6_projector", "remaining projector source channel"),
    ("SRC3890_13_coef", CSV_2612_COEF, "CP2612_6_A_direct_matter", "direct coefficient pack"),
    ("SRC3890_14_Amatter", CSV_2611_AMATTER, "AM2611_8_A_matter", "A_matter interface"),
]

ACTION_3890 = (
    "S_3890 = S_core^0[g_obs,Theta,Psi] + S_EH[C_*,g_obs] + sigma int C_*F_4 "
    "+ S_y[y;H,M] + S_R11[Sigma_loc(y),g_obs,Psi] + S_matter^q[Psi,e_obs(q(Phi)),theta_q]"
)
GRAMMAR_SIGN = "Domain(S_matter^q)=Fun(Q_obs,Matter); Hom_parent(H_hidden,M_source)=0 is a domain rule of the candidate action, not a tunable coupling"
DIRECT_ZERO = "For y in ker(Dq), delta_y S_matter^q=0 and the direct slots V_m,w_A,g_A,alpha_EM,m_A are undefined; hence A_direct_matter=delta_w_A=A_shadow=A_alpha_mass=0 in the 3890 candidate branch"


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
                "claim_use": "nonclaim_candidate_parent_grammar_signing",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def insertion_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("INS3890_0_action", "candidate parent action with grammar-signed matter sector", ACTION_3890, "INSERTED_IN_CANDIDATE_BRANCH", "extends 3882/3883 rather than adding a fitted local closure"),
        ("INS3890_1_domain_rule", "matter-sector domain restriction", GRAMMAR_SIGN, "SIGNED_IN_3890_CANDIDATE_ACTION", "a syntax/domain rule, not a dynamical equation or tuned coefficient"),
        ("INS3890_2_no_tuned_zero", "absence beats coefficient tuning", "direct hidden matter/source terms are ill-typed; no free coefficient is set to zero after variation", "NO_TUNED_ZERO_GUARD", "prevents a fake local-GR pass"),
        ("INS3890_3_variation", "vertical matter variation", DIRECT_ZERO, "DIRECT_SOURCE_ZERO_IN_CANDIDATE_BRANCH", "valid only for true quotient-vertical y and q-basic readouts"),
        ("INS3890_4_common_mode", "common source normalization", "a universal common prefactor w_* may be absorbed into kappa/G calibration, but relative w_A is absent in the grammar-signed branch", "COMMON_MODE_ALLOWED_RELATIVE_MODE_ZERO", "calibration still needs source/readout ownership"),
        ("INS3890_5_scope", "scope guard", "3890 signs the grammar inside the post-checkpoint candidate branch; it does not assert the whole historical corpus already obeys this syntax", "CANDIDATE_BRANCH_ONLY", "no public local-GR/Newton/PPN claim"),
    ]
    return [
        {
            "insertion_id": row_id,
            "piece": piece,
            "statement_or_math": statement,
            "status": status,
            "guardrail": guard,
            "candidate_branch_signed": True,
            "global_corpus_adopted": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, piece, statement, status, guard in raw_rows
    ]


def direct_zero_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("DZU3890_0_A_direct", "A_direct_matter", "||delta_y V_m[X,rho_A,W_source]|_{X=0}||_{E*}", "0", "ZERO_BY_ABSENT_TYPED_SLOT", "direct V_m slot not in S_matter^q"),
        ("DZU3890_1_delta_w", "delta_w_A", "w_A/w_* - 1", "0", "ZERO_BY_ABSENT_RELATIVE_PREFactor_SLOT", "relative species/source prefactor not in S_matter^q"),
        ("DZU3890_2_delta_w_species", "delta_w_species", "species-label source prefactor leakage", "0", "ZERO_BY_SPECIES_BLIND_FUNCTOR", "species labels are representation data over q-basic geometry"),
        ("DZU3890_3_delta_w_hidden", "delta_w_hidden", "hidden invariant source coefficient leakage", "0", "ZERO_BY_NO_HIDDEN_HOM", "Hom_parent(H_hidden,M_source)=0"),
        ("DZU3890_4_delta_w_marker", "delta_w_marker", "material/domain/boundary marker source leakage", "0", "ZERO_BY_NO_MARKER_GRAMMAR", "hidden marker/domain labels absent from ordinary matter functor"),
        ("DZU3890_5_shadow_frame", "A_shadow_frame", "hidden conformal/disformal matter frame leakage", "0", "ZERO_BY_ONE_OBSERVED_COFRAME", "matter couples to e_obs(q) only"),
        ("DZU3890_6_alpha_mass", "A_alpha_mass", "alpha_EM(y), m_A(y), q_A y_mu J_A^mu", "0", "ZERO_BY_Q_BASIC_CONSTANTS", "constants/charges are q-basic representation data"),
    ]
    return [
        {
            "zero_id": row_id,
            "quantity": quantity,
            "definition": definition,
            "candidate_value": value,
            "candidate_status": status,
            "reason": reason,
            "global_corpus_adopted": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, quantity, definition, value, status, reason in raw_rows
    ]


def remaining_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("REM3890_0_worldtube", "A_worldtube_matter", "source support/worldtube owner", "not killed by no-direct matter grammar", "derive Hilbert worldtube support descent or retain coefficient"),
        ("REM3890_1_boundary", "A_boundary_matter;epsilon_B_flux_abs", "boundary/corner/reference flux", "not killed by no-direct matter grammar", "prove no-flux/topological boundary or bound alpha3/xi/Gdot"),
        ("REM3890_2_nonHilbert", "A_nonHilbert_matter", "non-Hilbert/source-current leakage", "not killed by observed matter grammar", "derive same-current theorem or retain source residual"),
        ("REM3890_3_projector", "T_extra_munu_or_c_projector_domain_stress", "Pi_M/readout/projector stress", "not killed by matter functor domain", "prove projector is fixed/q-basic/topological or score PPN stress vector"),
        ("REM3890_4_memory", "K_history;partial_t K_history", "nonlocal/history/private clock-frame response", "not killed by ordinary matter syntax", "derive compact local memory silence or fill Gdot/clock rows"),
        ("REM3890_5_R11", "c_F;DeltaE_munu", "non-EH operator factorization", "not killed by matter direct-source zero", "prove Sigma_loc factorization or fill gamma/beta/R10 coefficients"),
        ("REM3890_6_residual_lock", "Y_loc^A physical residual-lock", "auxiliary-to-observable residual identification", "not killed by matter grammar", "prove y^A equals physical PPN/R10/R11 residual vector"),
    ]
    return [
        {
            "remaining_id": row_id,
            "quantity": quantity,
            "channel": channel,
            "why_remaining": why,
            "next_resolution": resolution,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, quantity, channel, why, resolution in raw_rows
    ]


def input_queue_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("INP3890_0_worldtube", 1, "A_worldtube_matter", "E_star_norm", "worldtube/source support descent fails", "source support variation or theorem-zero certificate", "AM2611_5_A_worldtube"),
        ("INP3890_1_boundary_alpha3", 2, "epsilon_B_flux_abs;c_B_flux_to_alpha3", "dimensionless", "boundary no-flux fails", "boundary flux magnitude and map to alpha3", "BRL547_0_boundary_alpha3"),
        ("INP3890_2_beta", 3, "A_source;B_source", "dimensionless", "source residual-lock/source stability fails", "linear and quadratic source response", "PRED3889_4_beta_source"),
        ("INP3890_3_gamma", 4, "C_gamma^F;c_F", "dimensionless", "R11 factorization fails", "weak-field map from R11 operators to gamma", "PRED3889_3_gamma_R11"),
        ("INP3890_4_R10", 5, "K_X(lambda);Q_X^H;q_X^test;alpha_bound(lambda)", "range-dependent", "bulk/source charge zero fails", "prediction charges plus real bound curve", "PRED3889_5_R10_alpha"),
        ("INP3890_5_Gdot", 6, "partial_t K_history;partial_t epsilon_B_flux;partial_t ln(Pi_M M_H)", "yr^-1", "memory/boundary/source time drift fails", "time profile and frame lock", "PRED3889_6_Gdot"),
        ("INP3890_6_projector", 7, "P_PPN[T_extra_munu]", "dimensionless_vector", "projector stress proof fails", "component map to gamma,beta,alpha_i,xi,zeta_i", "PRED3889_7_projector"),
        ("INP3890_7_direct_fallback", 8, "delta_w_A;A_direct_matter", "dimensionless/E_star", "3890 grammar branch rejected", "direct-source coefficient values", "PRED3889_0_A_direct;PRED3889_1_delta_w"),
    ]
    return [
        {
            "input_id": row_id,
            "priority": priority,
            "needed_input": needed,
            "units": units,
            "trigger": trigger,
            "required_data_or_derivation": required,
            "source_anchor": anchor,
            "current_status": "MISSING_NUMERIC_INPUT_OR_THEOREM_ZERO",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, priority, needed, units, trigger, required, anchor in raw_rows
    ]


def gate_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("LGG3890_0_candidate_grammar", "Hom/no-marker grammar inside candidate action", "S_matter^q domain excludes hidden source arrows", "PASS_CANDIDATE_BRANCH_NONCLAIM"),
        ("LGG3890_1_direct_source", "direct hidden/source coefficients", "A_direct_matter=delta_w_A=A_shadow=A_alpha_mass=0 in candidate branch", "PASS_CANDIDATE_BRANCH_NONCLAIM"),
        ("LGG3890_2_observed_matter", "observed q-basic matter source", "delta_y S_matter^q=0 for y in kerDq", "PASS_CANDIDATE_BRANCH_NONCLAIM"),
        ("LGG3890_3_worldtube_boundary", "worldtube/boundary/nonHilbert channels", "must be theorem-zero or bounded", "FAIL_OPEN"),
        ("LGG3890_4_projector_memory_R11", "projector/memory/R11 channels", "must be theorem-zero or bounded", "FAIL_OPEN"),
        ("LGG3890_5_residual_lock", "Yloc physical residual-lock", "candidate y variables equal actual PPN/R10/R11 residuals", "FAIL_UNSIGNED"),
        ("LGG3890_6_numeric_inputs", "numeric input queue", "priority list exists but values not filled", "PASS_QUEUE_READY_NONCLAIM"),
        ("LGG3890_7_local_GR", "local-GR promotion", "all source, lock, boundary, projector, memory and R11 gates close", "BLOCKED_NO_CLAIM"),
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
        ("RUNU3890_0_branch", "candidate_branch_selector", "if using S_3890, direct hidden matter/source coefficients are candidate zeros by grammar; do not request numeric delta_w unless this grammar branch is rejected", "IMPLEMENTED"),
        ("RUNU3890_1_scope", "global_scope_guard", "candidate_branch_signed=true does not imply global_corpus_adopted=true", "NO_PUBLIC_CLAIM"),
        ("RUNU3890_2_remaining", "remaining_channel_guard", "worldtube, boundary, nonHilbert, projector, memory, R11 and residual-lock stay live", "OPEN_CHANNELS_RETAINED"),
        ("RUNU3890_3_input_queue", "numeric_queue", "if a remaining channel fails theorem-zero, fill inputs in priority order without cancellation credit", "QUEUE_READY"),
        ("RUNU3890_4_next", "next_attack", "attack worldtube/boundary/projector residual-lock next, because direct hidden matter is now candidate-zeroed", "NEXT_3891"),
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
            "next_id": "NEXT3890_0",
            "target_checkpoint": "3891-Y5-R2FR-worldtube-boundary-projector-residual-lock-or-numeric-fill.md",
            "script": "scripts/Y5_R2FR_3891_worldtube_boundary_projector_residual_lock_or_numeric_fill.py",
            "objective": "derive worldtube support descent, boundary no-flux/topological silence, projector fixed/q-basic stress silence, and residual-lock for y^A; if any fails, fill the corresponding numeric coefficient inputs from the 3890 priority queue",
            "why_next": "3890 candidate-signs the direct hidden matter/source grammar, so the live blockers have moved to source support, boundary, projector, memory, R11 factorization and residual-lock",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "status_id": "STATUS3890_0",
            "branch": BRANCH,
            "summary": "Hom/no-marker grammar inserted into the candidate parent action; direct hidden matter/source coefficients are candidate-zero by typed slot absence, not tuning; local GR remains blocked by worldtube, boundary, nonHilbert, projector, memory, R11 and residual-lock channels",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    insertion: list[dict[str, object]],
    direct_zero: list[dict[str, object]],
    remaining: list[dict[str, object]],
    input_queue: list[dict[str, object]],
    gate: list[dict[str, object]],
    runner: list[dict[str, object]],
    next_target: list[dict[str, object]],
    timestamp: str,
) -> None:
    resolved = sum(1 for row in sources if row["exists"] and row["needle_found"])
    doc = f"""# 3890 - Sign Parent Grammar in Action or Fill Numeric Coefficient Inputs

Generated: `{timestamp}`

## Result

3890 makes the strongest candidate-branch move so far on the direct matter/source coupling problem.

Candidate parent action:

`{ACTION_3890}`

Grammar insertion:

`{GRAMMAR_SIGN}`

Direct zero consequence:

`{DIRECT_ZERO}`

So, inside this post-checkpoint candidate branch, direct hidden matter/source coefficients are not merely "small"; they are absent by object-language typing. That is a real improvement over a missing-coefficient ledger. The guardrail is equally important: this is not yet a global claim about every historical MTS note, and it does not close worldtube, boundary, projector, memory, R11 or residual-lock channels.

## Parent Action Grammar Insertion

{markdown_table(insertion, ["insertion_id", "piece", "statement_or_math", "status", "guardrail", "candidate_branch_signed", "global_corpus_adopted"])}

## Direct Source Zero Update

{markdown_table(direct_zero, ["zero_id", "quantity", "definition", "candidate_value", "candidate_status", "reason"])}

## Remaining Source Channels

{markdown_table(remaining, ["remaining_id", "quantity", "channel", "why_remaining", "next_resolution"])}

## Numeric Coefficient Input Priority Queue

{markdown_table(input_queue, ["input_id", "priority", "needed_input", "units", "trigger", "required_data_or_derivation", "current_status"])}

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

This is an actual step toward derivability: direct hidden matter/source couplings are now candidate-zeroed by a typed parent action, not hidden under a closure assumption. The live problem has moved downstream: prove the support/boundary/projector/residual-lock pieces, or start filling their numeric inputs.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    start = "<!-- BEGIN 3890 SIGNED CANDIDATE MATTER GRAMMAR -->"
    end = "<!-- END 3890 SIGNED CANDIDATE MATTER GRAMMAR -->"
    block = f"""{start}

## 3890 - Candidate parent grammar signed for direct matter/source slots

Candidate action:

`{ACTION_3890}`

Grammar insertion:

`{GRAMMAR_SIGN}`

Direct zero:

`{DIRECT_ZERO}`

Status: in the post-checkpoint candidate branch, direct hidden matter/source coefficients are zero by typed slot absence. This is not a global corpus/local-GR claim. Remaining live blockers: worldtube support, boundary/corner flux, non-Hilbert source current, projector/readout stress, memory/time drift, R11 factorization and physical residual-lock.

Generated outputs:
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3890_PARENT_ACTION_GRAMMAR_INSERTION.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3890_DIRECT_SOURCE_ZERO_UPDATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3890_REMAINING_SOURCE_CHANNELS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3890_NUMERIC_COEFFICIENT_INPUT_PRIORITY_QUEUE.csv`
- `source-intake\\mts_residuals\\P8_Y5_BRR545_3890_VALIDATION.csv`

Next gate: `3891`, worldtube/boundary/projector residual-lock or numeric fill.

<!-- Generated by 3890 at {timestamp} -->
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
    insertion: list[dict[str, object]],
    direct_zero: list[dict[str, object]],
    remaining: list[dict[str, object]],
    input_queue: list[dict[str, object]],
    gate: list[dict[str, object]],
    runner: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    checks: list[tuple[str, str, bool, str]] = []
    resolved = sum(1 for row in sources if row["exists"] and row["needle_found"])
    checks.append(("VAL3890_0_sources", "all cited source paths exist and needles are found", resolved == len(sources), f"{resolved}/{len(sources)} sources resolved"))
    checks.append(("VAL3890_1_action", "candidate parent action includes S_matter^q grammar", any("S_3890" in str(row["statement_or_math"]) and "S_matter^q" in str(row["statement_or_math"]) for row in insertion), "INS3890_0"))
    checks.append(("VAL3890_2_domain_rule", "Hom no-source rule is signed in candidate branch", any("Hom_parent(H_hidden,M_source)=0" in str(row["statement_or_math"]) and row["candidate_branch_signed"] for row in insertion), "INS3890_1"))
    required_zero = {"A_direct_matter", "delta_w_A", "delta_w_species", "delta_w_hidden", "delta_w_marker", "A_shadow_frame", "A_alpha_mass"}
    found_zero = {str(row["quantity"]) for row in direct_zero if str(row["candidate_value"]) == "0"}
    checks.append(("VAL3890_3_direct_zero", "direct hidden/source coefficients are candidate-zeroed", required_zero.issubset(found_zero), f"{len(found_zero)} zero rows"))
    required_remaining = {"A_worldtube_matter", "A_boundary_matter;epsilon_B_flux_abs", "A_nonHilbert_matter", "T_extra_munu_or_c_projector_domain_stress", "K_history;partial_t K_history", "c_F;DeltaE_munu", "Y_loc^A physical residual-lock"}
    found_remaining = {str(row["quantity"]) for row in remaining}
    checks.append(("VAL3890_4_remaining_channels", "remaining source channels are retained", required_remaining.issubset(found_remaining), f"{len(found_remaining)} remaining rows"))
    required_inputs = {"A_worldtube_matter", "epsilon_B_flux_abs;c_B_flux_to_alpha3", "A_source;B_source", "C_gamma^F;c_F", "K_X(lambda);Q_X^H;q_X^test;alpha_bound(lambda)", "partial_t K_history;partial_t epsilon_B_flux;partial_t ln(Pi_M M_H)", "P_PPN[T_extra_munu]"}
    found_inputs = {str(row["needed_input"]) for row in input_queue}
    checks.append(("VAL3890_5_input_queue", "numeric input priority queue covers remaining arenas", required_inputs.issubset(found_inputs), f"{len(found_inputs)} inputs"))
    checks.append(("VAL3890_6_local_gr_no_claim", "local GR remains blocked", any(row["gate_id"] == "LGG3890_7_local_GR" and "BLOCKED" in str(row["status"]) for row in gate), "LGG3890_7"))
    checks.append(("VAL3890_7_scope_guard", "candidate signing is not global adoption", all(str(row.get("global_corpus_adopted")) == "False" for row in insertion), "global_corpus_adopted=false"))
    checks.append(("VAL3890_8_all_nonclaim", "all generated analytic rows are nonclaim", all(str(row.get("valid_for_claim")) == "False" for collection in [insertion, direct_zero, remaining, input_queue, gate, runner] for row in collection), "valid_for_claim=false"))
    checks.append(("VAL3890_9_runner", "runner sends next work to remaining channels", any(row["runner_field"] == "remaining_channel_guard" and "worldtube" in str(row["rule"]) for row in runner), "RUNU3890_2"))
    checks.append(("VAL3890_10_doc", "markdown checkpoint exists with bottom line", DOC_PATH.exists() and "direct hidden matter/source couplings are now candidate-zeroed" in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3890_11_spine", "spine updated with 3890 block", SPINE_PATH.exists() and "BEGIN 3890 SIGNED CANDIDATE MATTER GRAMMAR" in read_text(SPINE_PATH), rel(SPINE_PATH)))
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_parse_ok = True
    parse_details = []
    for path in csv_outputs:
        try:
            parse_details.append(f"{path.name}:{len(read_csv_rows(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parse_details.append(f"{path.name}:{exc}")
    checks.append(("VAL3890_12_csv_parse", "all generated CSV outputs parse", csv_parse_ok, "; ".join(parse_details)))
    formalization_hits = []
    if FWB.exists():
        formalization_hits = [path for path in FWB.rglob("*3890*") if path.is_file() and ("3890-Y5" in path.name or "P8_Y5_R2FR_3890" in path.name or "P8_Y5_BRR545_3890" in path.name)]
    checks.append(("VAL3890_13_formalization_untouched", "no generated 3890 files appear in formalization-workbench", not formalization_hits, f"{len(formalization_hits)} hits"))
    pycache_hits = [path for path in (PCW / "scripts").rglob("__pycache__") if path.is_dir()]
    checks.append(("VAL3890_14_no_pycache", "scripts __pycache__ removed", not pycache_hits, f"{len(pycache_hits)} pycache dirs"))
    checks.append(("VAL3890_15_next_target", "next target attacks worldtube/boundary/projector residual-lock", any("worldtube-boundary-projector" in str(row["target_checkpoint"]) for row in next_rows(timestamp)), "3891 worldtube/boundary/projector"))
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
    insertion = insertion_rows(timestamp)
    direct_zero = direct_zero_rows(timestamp)
    remaining = remaining_rows(timestamp)
    input_queue = input_queue_rows(timestamp)
    gate = gate_rows(timestamp)
    runner = runner_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["insertion"], insertion)
    write_csv(OUTPUTS["direct_zero"], direct_zero)
    write_csv(OUTPUTS["remaining"], remaining)
    write_csv(OUTPUTS["input_queue"], input_queue)
    write_csv(OUTPUTS["gate"], gate)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, insertion, direct_zero, remaining, input_queue, gate, runner, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, insertion, direct_zero, remaining, input_queue, gate, runner, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_CANDIDATE_GRAMMAR_SIGNED_DIRECT_SOURCE_ZERO")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
