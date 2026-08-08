from __future__ import annotations

import csv
import subprocess
from pathlib import Path
from typing import Iterable


BRANCH_ID = "MTS_R2FR_READOUT_TAIL_ZERO_PROOF_OR_FIRST_ALPHA_READOUT_BOUND_2370"
POST_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = POST_ROOT.parent
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2370-Y5-R2FR-readout-tail-zero-proof-or-first-alpha-readout-bound.md"
FORMALIZATION_WORKBENCH = PROJECT_ROOT / "formalization-workbench"


def rel(path: Path) -> str:
    try:
        return path.relative_to(POST_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    return path.exists() and needle in path.read_text(encoding="utf-8", errors="replace")


def no_claim(extra: dict[str, object] | None = None) -> dict[str, object]:
    row: dict[str, object] = {
        "parent_signed": "false",
        "theorem_zero": "false",
        "numeric_prediction_present": "false",
        "same_branch_locked": "false",
        "projection_ready": "false",
        "score_ready": "false",
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }
    if extra:
        row.update(extra)
    return row


def source_register() -> list[dict[str, object]]:
    sources = [
        ("SRC2370_2369_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2369_NEXT_TARGET.csv", "NEXT2369_0_selected", "2369 selected alpha_readout/readout-tail route"),
        ("SRC2370_2369_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2369_VALIDATION.csv", "VAL2369_OVERALL", "2369 validation"),
        ("SRC2370_2324_zero", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2324_ALPHA_READOUT_ZERO_PROOF_ATTEMPT.csv", "ARZ2324_4_verdict", "alpha_readout zero proof conditional only"),
        ("SRC2370_2324_bound", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2324_FIRST_ALPHA_READOUT_BOUND_ROW.csv", "ARB2324_3_score_gate", "first alpha_readout bound row"),
        ("SRC2370_2324_inputs", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2324_READOUT_INPUT_ACQUISITION_LEDGER.csv", "RIA2324_4_vector_completion", "readout input acquisition ledger"),
        ("SRC2370_2324_vector", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2324_PPN_VECTOR_UPDATE.csv", "PVU2324_2_absolute_vector", "PPN vector update"),
        ("SRC2370_2325_gauge", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2325_PPN_GAUGE_CALIBRATION_BOUND_ROW.csv", "PGB2325_3_bound_contract", "PPN gauge/calibration bound contract"),
        ("SRC2370_2325_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2325_NEXT_TARGET.csv", "NEXT2325_0", "epsilon_sigma next target"),
        ("SRC2370_2326_eps", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2326_EPSILON_SIGMA_ZERO_CERTIFICATE_ATTEMPT.csv", "ESZ2326_4_verdict", "epsilon_sigma zero certificate not derived"),
        ("SRC2370_2326_leak", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2326_FIRST_PROTOCOL_LEAKAGE_ROW.csv", "PLR2326_0_source_GM", "first protocol leakage row"),
        ("SRC2370_2328_nosource", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2328_NO_SOURCE_ONLY_SPECIES_SLOT_DERIVATION_ATTEMPT.csv", "NSOS2328_6_verdict", "parallel no-source-only syntax route"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, source_path, needle, role in sources:
        path = POST_ROOT / source_path
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_id,
                "source_path": source_path,
                "needle": needle,
                "role": role,
                "path_exists": str(path.exists()).lower(),
                "needle_found": str(contains(path, needle)).lower(),
                "valid_for_claim": "false",
            }
        )
    return rows


def alpha_readout_zero_audit() -> list[dict[str, object]]:
    rows = [
        ("ARZ2370_0_exact_zero", "readout-tail zero theorem", "If Pi_gamma, sigma_A, GM calibration, and PPN gauge/readout maps descend through fixed (q,e_obs,theta) or are fixed external protocol after variation, then D_v readout=0 and alpha_readout=0.", "EXACT_CONDITIONAL_THEOREM", "descent certificates are not parent-signed"),
        ("ARZ2370_1_projector_support", "projector/support descent", "Pi_A=Pi_bar_A(q,e_obs,theta) and sigma_A=sigma_bar_A(q,e_obs,theta) imply D_v(Pi_A J_A)=0 for v in ker(Dq).", "CONDITIONAL_ZERO_VALID", "source worldtube, support mask, boundary transport and material/source weights unsigned"),
        ("ARZ2370_2_fixed_readout", "fixed-before-readout map", "pure postprocessing readout has no arrow into S_parent, coefficient extraction, source normalization or calibration.", "ZERO_BY_TYPE_FOR_POSTPROCESSING_ONLY", "GM/source/gauge feedback maps are not pure postprocessing"),
        ("ARZ2370_3_GM_guard", "measured-GM guard", "only universal common-mode source calibration can be absorbed into measured G/GM; relative or protocol tails cannot.", "GUARD_DERIVED_NOT_ZERO", "relative source vector and calibration equation missing"),
        ("ARZ2370_4_verdict", "alpha_readout zero active branch", "all readout/support/GM/gauge descent certificates pass together", "NOT_DERIVED_RETAIN_BOUND_ROW", "first alpha_readout bound/input rows required"),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "proof_piece": piece,
            "formal_statement": statement,
            "proof_status": status,
            "gap_or_effect": gap,
        }
        for row_id, piece, statement, status, gap in rows
    ]


def first_alpha_readout_bound_row() -> list[dict[str, object]]:
    rows = [
        ("ARB2370_0_target", "alpha_readout_abs_target", "abs(alpha_readout) <= 0.005788015401465051 as one component inside the PPN absolute-vector budget", "0.005788015401465051", "dimensionless", "SOURCE_BACKED_TARGET_NOT_MTS_PREDICTION"),
        ("ARB2370_1_normal_form", "alpha_readout", "alpha_readout = Pi_gamma[Delta_cal + Delta_PPN + C_feedback + C_protocol]", "MISSING_COMPONENT_VALUES", "dimensionless", "NORMAL_FORM_DERIVED_VALUES_MISSING"),
        ("ARB2370_2_triangle_bound", "alpha_readout_abs_envelope", "abs(alpha_readout) <= abs(Pi_gamma Delta_cal)+abs(Pi_gamma Delta_PPN)+abs(Pi_gamma C_feedback)+abs(Pi_gamma C_protocol)", "MISSING_TERM_BOUNDS", "dimensionless", "BOUND_FORM_DERIVED_VALUES_MISSING"),
        ("ARB2370_3_score_gate", "alpha_readout_pass_condition", "alpha_readout_abs_envelope <= target and all other PPN vector components are theorem-zero or independently bounded", "MISSING_VECTOR_COMPONENTS", "dimensionless", "CLAIM_BLOCKED_UNTIL_VECTOR_COMPLETE"),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "quantity": quantity,
            "formula_or_bound": formula,
            "numeric_value": value,
            "units": units,
            "status": status,
        }
        for row_id, quantity, formula, value, units, status in rows
    ]


def readout_input_ledger() -> list[dict[str, object]]:
    rows = [
        ("RIA2370_0_Delta_cal", "Delta_cal", "calibration mismatch between closed parent source charge and observed GM/PPN mass", "MISSING_GAUSS_ORBITAL_PPN_RESIDUAL", "Gauss/orbital calibration theorem or numeric residual bound"),
        ("RIA2370_1_Delta_PPN", "Delta_PPN", "second-order PPN readout/source-normalization tail after measured-GM normalization", "MISSING_PPN_GAUGE_AND_SOURCE_NORMALIZATION", "observed PPN gauge transform and source-normalization row"),
        ("RIA2370_2_C_feedback", "C_feedback", "source-feedback commutator kernel from D_v(Pi_A J_A)", "NORMAL_FORM_DERIVED_VALUES_MISSING", "operator norm and epsilon_sigma_A for source/readout protocol"),
        ("RIA2370_3_C_protocol", "C_protocol", "support/mask/orbit-window/boundary transport protocol tail", "CLOSURE_OR_SOURCE_REQUIRED", "parent protocol declaration, q/e_obs descent proof, or finite source-backed bound"),
        ("RIA2370_4_vector_completion", "all sibling PPN components", "alpha_readout cannot pass by cancellation against alpha_cg/disformal/nonH/support/boundary", "ABSOLUTE_VECTOR_COMPONENTS_MISSING", "component-wise zero theorems or source-backed bounds"),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "needed_input": needed,
            "meaning": meaning,
            "current_status": status,
            "next_evidence": evidence,
        }
        for row_id, needed, meaning, status, evidence in rows
    ]


def epsilon_sigma_bridge() -> list[dict[str, object]]:
    rows = [
        ("EPS2370_0_exact_zero", "epsilon_sigma_A", "epsilon_sigma_A=||D_v sigma_A||=0 if sigma_A descends through q/e_obs/theta or is fixed external protocol before variation", "EXACT_CONDITIONAL_ZERO", "need per-channel descent/fixed-protocol certificates"),
        ("EPS2370_1_source_profile", "sigma_source_profile", "Earth/source density, composition, support profile, and source worldtube are fixed q/e_obs data before readout", "NOT_PARENT_SIGNED", "source profile/composition obstruction active"),
        ("EPS2370_2_GM_common", "sigma_GM_common_mode", "GM/G calibration contains only one universal common-mode source factor", "GUARD_WRITTEN_NOT_NUMERIC", "calibration equation and no-relative-source-hiding proof missing"),
        ("EPS2370_3_protocol_boundary", "sigma_mask_orbit_attitude + sigma_boundary_domain", "masks, orbit windows, attitude, support tube, boundary transport and projector domain are fixed protocol or q/e_obs descendants", "CLOSURE_OR_SOURCE_REQUIRED", "official arrays/boundary certificates missing"),
        ("EPS2370_4_first_leakage", "epsilon_sigma_source_GM", "|C_source_GM| <= L_source_GM * epsilon_sigma_source_GM", "CONTRACT_READY_VALUES_MISSING", "first concrete leakage row"),
        ("EPS2370_5_verdict", "epsilon_sigma active zero", "all sigma channels required by alpha_readout have epsilon_sigma_A=0", "NOT_DERIVED_RETAIN_LEAKAGE_ROW", "source_GM channel remains unsigned"),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "sigma_channel": channel,
            "statement_or_bound": statement,
            "status": status,
            "effect_or_missing": missing,
        }
        for row_id, channel, statement, status, missing in rows
    ]


def ppn_vector_update() -> list[dict[str, object]]:
    rows = [
        ("PVU2370_0_alpha_readout_live", "alpha_readout", "LIVE_NONCLAIM_COMPONENT_WITH_SOURCE_TARGET", "abs(alpha_readout) target <= 0.005788015401465051; prediction missing", "local GR blocked unless zero theorem or bound gate closes"),
        ("PVU2370_1_no_tau_activation", "tau_PPN=1 activation", "BLOCKED_BY_READOUT_DESCENT", "2322 conditional tau remains inactive until alpha_readout/readout descent closes", "cannot score alpha_cg as strict scalar-tensor branch yet"),
        ("PVU2370_2_absolute_vector", "alpha_PPN_total_abs", "VECTOR_SCHEMA_READY_VALUES_MISSING", "sum_abs(alpha_cg,alpha_dis,alpha_nonH,alpha_support,alpha_boundary,alpha_readout)", "no single-component local-GR pass allowed"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "component": component,
            "status": status,
            "current_best_object": obj,
            "effect_on_local_GR": effect,
            "score_ready": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, component, status, obj, effect in rows
    ]


def route_selection() -> list[dict[str, object]]:
    rows = [
        ("DEC2370_0_zero", "alpha_readout zero theorem", 1, "KEEP_CONDITIONAL_UNSIGNED", "exact if readout/support/projector descent certificates close"),
        ("DEC2370_1_bound", "first alpha_readout bound row", 1, "TARGET_IMPORTED_VALUES_MISSING", "source-backed target exists but prediction/envelope values missing"),
        ("DEC2370_2_epsilon", "epsilon_sigma/source-feedback leakage row", 1, "SELECT_NEXT_TARGET", "C_feedback is the most concrete missing input in the readout envelope"),
        ("DEC2370_3_ppn_gauge", "Delta_cal/Delta_PPN gauge calibration row", 2, "PARALLEL_NONCLAIM", "needed if source-feedback stalls"),
        ("DEC2370_4_nosource", "NoSourceOnlySpeciesSlot syntax route", 2, "PARALLEL_CLEANER_ROUTE", "could remove relative source-weight countermodel upstream"),
        ("DEC2370_5_empirical", "PPN/local-GR score", 5, "DEFER", "absolute vector components incomplete"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "route": route,
            "rank": rank,
            "decision": decision,
            "reason": reason,
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, route, rank, decision, reason in rows
    ]


def claim_gates() -> list[dict[str, object]]:
    rows = [
        ("CG2370_0_zero", "alpha_readout=0", "BLOCKED", "descent certificates not parent-signed"),
        ("CG2370_1_bound", "alpha_readout finite bound score-ready", "BLOCKED", "component values and full vector completion missing"),
        ("CG2370_2_epsilon", "epsilon_sigma source-feedback zero/bound ready", "BLOCKED", "source_GM/profile/protocol leakage values missing"),
        ("CG2370_3_tau", "tau_PPN=1 active branch", "BLOCKED", "readout descent not closed"),
        ("CG2370_4_local_GR", "local GR/Newton reduction derived", "BLOCKED", "absolute PPN/local residual vector incomplete"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "gate_pass": "false",
            "passes_public_claim": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, claim, status, reason in rows
    ]


def refusal_runner() -> list[dict[str, object]]:
    rows = [
        ("REF2370_0_zero", "set alpha_readout=0", "needs parent-signed readout/support/GM/gauge descent", "REFUSED"),
        ("REF2370_1_bound_pass", "claim alpha_readout passes bound", "needs Delta_cal, Delta_PPN, C_feedback, C_protocol bounds and full vector completion", "REFUSED"),
        ("REF2370_2_tau", "activate tau_PPN=1", "needs readout descent/common-frame closure", "REFUSED"),
        ("REF2370_3_single_component", "claim local GR from alpha_readout target alone", "absolute PPN vector cannot pass by one component or cancellation", "REFUSED"),
        ("REF2370_4_github", "public/GitHub claim", "private nonclaim checkpoint only", "REFUSED"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "attempted_claim": claim,
            "missing_evidence": missing,
            "refusal_result": result,
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, claim, missing, result in rows
    ]


def next_target() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2370_0_selected",
            "next_file": "2371-Y5-R2FR-source-feedback-epsilon-sigma-or-PPN-gauge-bound-row.md",
            "next_script": "scripts/Y5_R2FR_source_feedback_epsilon_sigma_or_PPN_gauge_bound_row_2371.py",
            "selected_reason": "2370 reduces alpha_readout to a concrete envelope; the next useful input is epsilon_sigma/operator norm for C_feedback or a source-backed PPN gauge/calibration residual bound",
            "success_condition": "prove epsilon_sigma_A=0 for required support/readout variables, or fill the first source-backed protocol leakage row for C_feedback/source_GM",
            "fallback_condition": "if protocol descent stalls, source Delta_cal/Delta_PPN as a PPN gauge-calibration bound row while keeping alpha_readout nonclaim",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2370_1_parallel",
            "next_file": "2371b-Y5-R2FR-NoSourceOnlySpeciesSlot-parent-syntax-proof.md",
            "next_script": "scripts/Y5_R2FR_NoSourceOnlySpeciesSlot_parent_syntax_proof_2371b.py",
            "selected_reason": "parallel cleaner route: eliminate relative source-weight countermodel before it feeds C_feedback and Delta_cal",
            "success_condition": "derive parent syntax excluding source-only species weights or stage finite source-profile vector",
            "fallback_condition": "retain finite source-profile/source-weight row as nonclaim",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        },
    ]


def formalization_status() -> tuple[bool, str]:
    if not FORMALIZATION_WORKBENCH.exists():
        return True, "formalization-workbench path not found; generator has no write targets there"
    try:
        result = subprocess.run(
            ["git", "-C", str(PROJECT_ROOT), "status", "--short", "--", "formalization-workbench"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        return True, f"git unavailable ({exc}); generator writes only under post-checkpoint-work"
    if result.returncode == 0:
        changed = [line for line in result.stdout.splitlines() if line.strip()]
        return len(changed) == 0, "git modified-file count for formalization-workbench is 0" if not changed else f"formalization-workbench has {len(changed)} status rows"
    return True, "project is not a git worktree here; generator writes only under post-checkpoint-work"


def parse_csv_ok(paths: Iterable[Path]) -> tuple[bool, str]:
    for path in paths:
        try:
            rows = read_csv(path)
        except Exception as exc:
            return False, f"{rel(path)} failed to parse: {exc}"
        if not rows:
            return False, f"{rel(path)} has no rows"
    return True, "all generated CSV files parse and contain rows"


def no_positive_claim_flags(paths: Iterable[Path]) -> tuple[bool, str]:
    flag_columns = [
        "parent_signed",
        "theorem_zero",
        "numeric_prediction_present",
        "same_branch_locked",
        "projection_ready",
        "score_ready",
        "valid_for_claim",
        "claim_allowed",
        "gate_pass",
        "passes_public_claim",
    ]
    offenders: list[str] = []
    for path in paths:
        for row in read_csv(path):
            row_name = row.get("row_id") or row.get("source_id") or "?"
            for column in flag_columns:
                if row.get(column, "").strip().lower() == "true":
                    offenders.append(f"{rel(path)}:{row_name}:{column}")
    if offenders:
        return False, "; ".join(offenders[:10])
    return True, "all generated claim/readiness flags remain negative"


def validation_rows(outputs: dict[str, Path], sources: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(row_id: str, ok: bool, detail: str) -> None:
        rows.append({"row_id": row_id, "status": "PASS" if ok else "FAIL", "detail": detail, "valid_for_claim": "false"})

    missing_sources = [str(row["source_path"]) for row in sources if row["path_exists"] != "true"]
    missing_needles = [str(row["source_id"]) for row in sources if row["needle_found"] != "true"]
    add("VAL2370_00_required_sources_exist", not missing_sources, "all required source paths exist" if not missing_sources else "; ".join(missing_sources))
    add("VAL2370_01_required_needles_found", not missing_needles, "all source needles found" if not missing_needles else "; ".join(missing_needles))

    generated = [path for key, path in outputs.items() if key != "validation"]
    add("VAL2370_02_outputs_exist", all(path.exists() for path in generated), "all 2370 output files written")
    parse_ok, parse_detail = parse_csv_ok([path for path in generated if path.suffix == ".csv"])
    add("VAL2370_03_csv_parse", parse_ok, parse_detail)

    zero = {row["row_id"]: row["proof_status"] for row in read_csv(outputs["zero"])}
    add("VAL2370_04_zero_conditional", zero.get("ARZ2370_0_exact_zero") == "EXACT_CONDITIONAL_THEOREM", "alpha_readout zero theorem retained as conditional")
    add("VAL2370_05_zero_not_promoted", zero.get("ARZ2370_4_verdict") == "NOT_DERIVED_RETAIN_BOUND_ROW", "active alpha_readout zero not promoted")

    bound = {row["row_id"]: row["status"] for row in read_csv(outputs["bound"])}
    add("VAL2370_06_bound_target_imported", bound.get("ARB2370_0_target") == "SOURCE_BACKED_TARGET_NOT_MTS_PREDICTION", "source-backed target imported as nonclaim")
    add("VAL2370_07_bound_values_missing", bound.get("ARB2370_3_score_gate") == "CLAIM_BLOCKED_UNTIL_VECTOR_COMPLETE", "bound score gate remains blocked")

    eps = {row["row_id"]: row["status"] for row in read_csv(outputs["epsilon"])}
    add("VAL2370_08_epsilon_selected", eps.get("EPS2370_5_verdict") == "NOT_DERIVED_RETAIN_LEAKAGE_ROW", "epsilon_sigma leakage row remains live")

    route = {row["row_id"]: row["decision"] for row in read_csv(outputs["decision"])}
    add("VAL2370_09_next_decision", route.get("DEC2370_2_epsilon") == "SELECT_NEXT_TARGET", "epsilon_sigma/source-feedback route selected next")

    flag_ok, flag_detail = no_positive_claim_flags([path for path in generated if path.suffix == ".csv"])
    add("VAL2370_10_no_positive_claim_flags", flag_ok, flag_detail)

    formal_ok, formal_detail = formalization_status()
    add("VAL2370_11_formalization_untouched", formal_ok, formal_detail)
    add("VAL2370_12_next_selected", read_csv(outputs["next"])[0].get("row_id") == "NEXT2370_0_selected", "2371 epsilon_sigma/gauge target selected")

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "row_id": "VAL2370_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "2370 valid: alpha_readout zero conditional only, first bound target imported nonclaim, epsilon_sigma/source-feedback selected next" if overall else "one or more validation gates failed",
            "valid_for_claim": "false",
        }
    )
    return rows


def write_markdown(outputs: dict[str, Path]) -> None:
    def table(headers: list[str], rows: list[dict[str, str]]) -> str:
        lines = [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join("---" for _ in headers) + " |",
        ]
        for row in rows:
            lines.append("| " + " | ".join(row.get(header, "").replace("|", "/") for header in headers) + " |")
        return "\n".join(lines)

    zero = read_csv(outputs["zero"])
    bound = read_csv(outputs["bound"])
    inputs = read_csv(outputs["inputs"])
    epsilon = read_csv(outputs["epsilon"])
    vector = read_csv(outputs["vector"])
    decisions = read_csv(outputs["decision"])
    next_rows = read_csv(outputs["next"])

    md = f"""# 2370 - Readout Tail Zero Proof Or First alpha_readout Bound

## Result

`alpha_readout` is now in a concrete nonclaim envelope:

`alpha_readout = Pi_gamma[Delta_cal + Delta_PPN + C_feedback + C_protocol]`.

There is an exact conditional zero theorem: if the readout, support, source profile, GM calibration and PPN gauge maps descend through fixed `(q,e_obs,theta)` data or are fixed external protocol after variation, then `alpha_readout=0`.

That theorem is not active.  The first target bound is source-backed as a PPN component ceiling, but it is not an MTS prediction:

`abs(alpha_readout) <= 0.005788015401465051`.

The missing real inputs are `Delta_cal`, `Delta_PPN`, `C_feedback`, `C_protocol`, and sibling PPN vector components.  The next clean input is `epsilon_sigma`: either prove protocol/support variables are fixed/descended, or fill the first finite source-feedback leakage row.

## Zero-Proof Audit

{table(["row_id", "proof_piece", "proof_status", "gap_or_effect"], zero)}

## First Bound Row

{table(["row_id", "quantity", "numeric_value", "status"], bound)}

## Input Acquisition Ledger

{table(["row_id", "needed_input", "current_status", "next_evidence"], inputs)}

## epsilon_sigma Bridge

{table(["row_id", "sigma_channel", "status", "effect_or_missing"], epsilon)}

## PPN Vector Update

{table(["row_id", "component", "status", "effect_on_local_GR"], vector)}

## Route Selection

{table(["row_id", "route", "rank", "decision", "reason"], decisions)}

## Next Target

{table(["row_id", "next_file", "success_condition", "fallback_condition"], next_rows)}

## Generated Files

- `{rel(outputs["source"])}`
- `{rel(outputs["zero"])}`
- `{rel(outputs["bound"])}`
- `{rel(outputs["inputs"])}`
- `{rel(outputs["epsilon"])}`
- `{rel(outputs["vector"])}`
- `{rel(outputs["decision"])}`
- `{rel(outputs["claims"])}`
- `{rel(outputs["refusal"])}`
- `{rel(outputs["next"])}`
- `{rel(outputs["validation"])}`

## Practical Status

This is a real narrowing, not a win.  The readout tail has a zero theorem, a bound target, and a named first missing input.  Local GR remains blocked until the readout tail is zeroed/bounded and the full absolute PPN vector is completed.
"""
    DOC_PATH.write_text(md, encoding="utf-8")


def main() -> int:
    sources = source_register()
    outputs = {
        "source": RESIDUALS / "P8_Y5_PARENT_QLOC_2370_SOURCE_REGISTER.csv",
        "zero": RESIDUALS / "P8_Y5_PARENT_QLOC_2370_ALPHA_READOUT_ZERO_AUDIT.csv",
        "bound": RESIDUALS / "P8_Y5_PARENT_QLOC_2370_FIRST_ALPHA_READOUT_BOUND_ROW.csv",
        "inputs": RESIDUALS / "P8_Y5_PARENT_QLOC_2370_READOUT_INPUT_ACQUISITION_LEDGER.csv",
        "epsilon": RESIDUALS / "P8_Y5_PARENT_QLOC_2370_EPSILON_SIGMA_BRIDGE.csv",
        "vector": RESIDUALS / "P8_Y5_PARENT_QLOC_2370_PPN_VECTOR_UPDATE.csv",
        "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_2370_DECISION_LEDGER.csv",
        "claims": RESIDUALS / "P8_Y5_PARENT_QLOC_2370_CLAIM_GATES.csv",
        "refusal": RESIDUALS / "P8_Y5_PARENT_QLOC_2370_REFUSAL_RUNNER.csv",
        "next": RESIDUALS / "P8_Y5_PARENT_QLOC_2370_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_2370_VALIDATION.csv",
    }

    write_csv(outputs["source"], sources)
    write_csv(outputs["zero"], alpha_readout_zero_audit())
    write_csv(outputs["bound"], first_alpha_readout_bound_row())
    write_csv(outputs["inputs"], readout_input_ledger())
    write_csv(outputs["epsilon"], epsilon_sigma_bridge())
    write_csv(outputs["vector"], ppn_vector_update())
    write_csv(outputs["decision"], route_selection())
    write_csv(outputs["claims"], claim_gates())
    write_csv(outputs["refusal"], refusal_runner())
    write_csv(outputs["next"], next_target())
    validation = validation_rows(outputs, sources)
    write_csv(outputs["validation"], validation)
    write_markdown(outputs)

    for row in validation:
        line = f"{row['row_id']},{row['status']},{row['detail']}"
        print(line.encode("ascii", errors="replace").decode("ascii"))
    return 0 if validation[-1]["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
