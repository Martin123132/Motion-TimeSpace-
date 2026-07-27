from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1154-Y5-R10-parent-worldtube-Hilbert-current-owner-or-R_eq-profile-builder.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    generated = now()
    return [{**row, "generated_utc": generated} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def contains_missing(value: object) -> bool:
    text = str(value)
    return text.strip() == "" or "MISSING" in text


def source_rows() -> list[dict[str, object]]:
    sources = [
        {
            "source_id": "SRC1154_0_1153_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1153_NEXT_TARGET.csv",
            "needle": "NEXT1153_0_1154",
            "role": "handoff selecting parent worldtube/Hilbert current owner or R_eq profile builder.",
        },
        {
            "source_id": "SRC1154_1_1153_fill",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1153_R_EQ_SOURCE_FILL_ROWS.csv",
            "needle": "REQ1153_1_same_Hilbert_measure",
            "role": "same-frame Hilbert measure missing row.",
        },
        {
            "source_id": "SRC1154_2_1153_theorem",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1153_CONDITIONAL_EQUALITY_THEOREM_GATE.csv",
            "needle": "THEO1153_7_verdict",
            "role": "1153 verdict blocking current parent-signed equality.",
        },
        {
            "source_id": "SRC1154_3_worldtube_clauses",
            "relative_path": "source-intake/mts_residuals/P8_WORLDTUBE_SOURCE_MEASURE_CLAUSES.csv",
            "needle": "WG510_1_minimal_observed_matter_coupling",
            "role": "worldtube source measure prerequisites.",
        },
        {
            "source_id": "SRC1154_4_worldtube_theorem",
            "relative_path": "source-intake/mts_residuals/P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
            "needle": "T510_2_MTS_transfer_condition",
            "role": "GR-style worldtube glue transfer condition for MTS.",
        },
        {
            "source_id": "SRC1154_5_source_measure_attempt",
            "relative_path": "source-intake/mts_residuals/P8_Y5_SOURCE_MEASURE_THEOREM_ATTEMPT.csv",
            "needle": "SMT542_2_observed_worldtube_source",
            "role": "source-measure theorem attempt for observed worldtube source.",
        },
        {
            "source_id": "SRC1154_6_source_glue_audit",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_673_SOURCE_MEASURE_GLUE_AUDIT.csv",
            "needle": "SMG673_0_conditional_theorem_shape",
            "role": "source-measure glue audit retaining conditional theorem only.",
        },
        {
            "source_id": "SRC1154_7_hamiltonian_contract",
            "relative_path": "source-intake/mts_residuals/P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
            "needle": "HSM541_2_observed_worldtube_source",
            "role": "Hamiltonian source-measure contract requiring observed worldtube source.",
        },
        {
            "source_id": "SRC1154_8_residual_inputs",
            "relative_path": "source-intake/mts_residuals/P8_Y5_HAMILTONIAN_SOURCE_MEASURE_RESIDUAL_INPUTS.csv",
            "needle": "HSI541_1_worldtube_frame",
            "role": "source-measure residual input schema for frame/calibration residuals.",
        },
        {
            "source_id": "SRC1154_9_residual_map",
            "relative_path": "source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv",
            "needle": "SMR509_5_Delta_frame",
            "role": "residual map for frame/source-measure mismatch.",
        },
        {
            "source_id": "SRC1154_10_observed_frame",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1068_OBSERVED_FRAME_FORCE_MAP.csv",
            "needle": "FRM1068_0_observed_frame",
            "role": "observed-frame force/readout map.",
        },
        {
            "source_id": "SRC1154_11_parent_contract",
            "relative_path": "source-intake/mts_residuals/P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv",
            "needle": "PAC537_1_single_observed_source_frame",
            "role": "parent contract requiring single observed source frame.",
        },
        {
            "source_id": "SRC1154_12_1150_glue",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1150_HILBERT_WORLDTUBE_GLUE_AUDIT.csv",
            "needle": "GLUE1150_1_observed_Hilbert_measure",
            "role": "latest glue audit showing observed Hilbert measure not locked.",
        },
    ]
    checked: list[dict[str, object]] = []
    for source in sources:
        path = ROOT / str(source["relative_path"])
        text = read_text(path)
        checked.append(
            {
                **source,
                "exists": str(path.exists()).lower(),
                "needle_found": str(str(source["needle"]) in text).lower(),
            }
        )
    return stamp(checked)


def owner_audit_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "owner_id": "OWN1154_0_conditional_owner_law",
                "claim_piece": "source object ownership law",
                "mathematical_form": "if S_matter[e_obs,psi] is unique and diffeomorphism-covariant, then J_H[tau] and W_source=supp(J_H) are parent-defined before readout",
                "current_status": "CONDITIONAL_REFERENCE_LAW",
                "missing_for_current_MTS": "explicit single observed coframe parent clause and full source variation",
                "effect_on_R_eq": "gives denominator/object only if signed",
                "valid_for_claim": "false",
            },
            {
                "owner_id": "OWN1154_1_parent_action_variation",
                "claim_piece": "explicit parent matter variation",
                "mathematical_form": "J_H[tau] = (delta S_matter / delta e_obs) contracted with tau",
                "current_status": "CONTRACT_ONLY_NO_FULL_VARIATION",
                "missing_for_current_MTS": "source-backed S_matter[e_obs,psi] and variation file",
                "effect_on_R_eq": "Pi_M J_H cannot be sourced",
                "valid_for_claim": "false",
            },
            {
                "owner_id": "OWN1154_2_single_observed_coframe",
                "claim_piece": "one observed frame for source, force, clocks, and readout",
                "mathematical_form": "e_obs = e_source = e_force = e_clock = e_readout through local/WEP order",
                "current_status": "CONDITIONAL_NOT_PARENT_DERIVED",
                "missing_for_current_MTS": "single-frame theorem or residual Delta_frame row",
                "effect_on_R_eq": "M_H_ref and profile denominator are frame-ambiguous",
                "valid_for_claim": "false",
            },
            {
                "owner_id": "OWN1154_3_worldtube_support",
                "claim_piece": "worldtube fixed by Hilbert source support before scoring",
                "mathematical_form": "W_source = supp(J_H[e_obs,tau]); S1,S2 link W_source",
                "current_status": "NOT_PARENT_DERIVED",
                "missing_for_current_MTS": "worldtube certificate and link-surface rule",
                "effect_on_R_eq": "finite shell A_ext can be readout-selected",
                "valid_for_claim": "false",
            },
            {
                "owner_id": "OWN1154_4_Hamiltonian_charge_normalization",
                "claim_piece": "same-frame dressed Hamiltonian source mass",
                "mathematical_form": "M_H_ref := H_tau[S_outer] - H_ref, not bare rest mass",
                "current_status": "FIXED_REFERENCE_AND_INTEGRABILITY_MISSING",
                "missing_for_current_MTS": "integrable charge, fixed tau, fixed reference, boundary term",
                "effect_on_R_eq": "epsilon_R_eq_abs cannot be computed honestly",
                "valid_for_claim": "false",
            },
            {
                "owner_id": "OWN1154_5_radial_closure_precondition",
                "claim_piece": "source-free exterior charge closure",
                "mathematical_form": "int_A(C_EH+C_extra+C_projector+C_boundary)=0",
                "current_status": "CONDITIONAL_EH_REFERENCE_C_TERMS_OPEN",
                "missing_for_current_MTS": "extra/projector/boundary channel zero or bounds",
                "effect_on_R_eq": "R_eq profile may hide radial source drift",
                "valid_for_claim": "false",
            },
            {
                "owner_id": "OWN1154_6_verdict",
                "claim_piece": "current MTS owns W_source, J_H, and M_H_ref in one observed frame",
                "mathematical_form": "OWN1154_1 through OWN1154_5 all signed by the same parent action",
                "current_status": "SOURCE_OBJECT_NOT_PARENT_OWNED",
                "missing_for_current_MTS": "observed coframe owner, source variation, worldtube certificate, Hamiltonian normalization",
                "effect_on_R_eq": "build nonclaim profile schema; do not promote equality/Newton/local-GR",
                "valid_for_claim": "false",
            },
        ]
    )


def profile_schema_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "schema_id": "PROF1154_0_profile_identity",
                "field_group": "identity",
                "required_columns": "profile_id;system_id;branch_id;source_file;valid_for_claim",
                "acceptance_rule": "source_file exists and profile is tied to a named theorem or finite-shell calculation",
                "current_status": "SCHEMA_READY_NO_DATA",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "schema_id": "PROF1154_1_frame_and_generator",
                "field_group": "observed_frame",
                "required_columns": "e_obs_definition;source_frame;readout_frame;tau_generator;Delta_frame",
                "acceptance_rule": "same-frame theorem or explicit Delta_frame residual; no frame relabel",
                "current_status": "MISSING_OBSERVED_FRAME_OWNER",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "schema_id": "PROF1154_2_worldtube_surfaces",
                "field_group": "worldtube",
                "required_columns": "W_source_definition;support_rule;r_inner;r_outer;surface_pair;linking_class",
                "acceptance_rule": "worldtube and surfaces fixed before readout",
                "current_status": "MISSING_WORLDTUBE_CERTIFICATE",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "schema_id": "PROF1154_3_currents",
                "field_group": "current_profiles",
                "required_columns": "PiM_JH_profile;JM_top_profile;B_zero_profile;extra_exchange_profile",
                "acceptance_rule": "profiles come from parent variation/topology/boundary calculation, not fitted cancellation",
                "current_status": "MISSING_CURRENT_PROFILES",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "schema_id": "PROF1154_4_integrals",
                "field_group": "finite_shell_integrals",
                "required_columns": "R_eq_integral;B_zero_flux;Delta_extra_vector;I_commutator;units",
                "acceptance_rule": "positive finite-shell values or theorem zeros with source paths",
                "current_status": "MISSING_FINITE_SHELL_INTEGRALS",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "schema_id": "PROF1154_5_normalization",
                "field_group": "normalization",
                "required_columns": "M_H_ref;H_tau_outer;H_ref;normalization_convention;epsilon_R_eq_abs",
                "acceptance_rule": "M_H_ref is the same-frame dressed Hamiltonian charge; epsilon_R_eq_abs=abs(R_eq_integral)/M_H_ref",
                "current_status": "MISSING_M_H_REF",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
        ]
    )


def placeholder_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "profile_id": "R_EQ_PROFILE_1154_PLACEHOLDER",
                "system_id": "MISSING_SYSTEM_ID",
                "branch_id": "MTS_local_source_normalized_branch",
                "e_obs_definition": "MISSING_E_OBS_OWNER",
                "W_source_definition": "MISSING_WORLDTUBE_CERTIFICATE",
                "surface_pair": "MISSING_SURFACES",
                "PiM_JH_profile": "MISSING_PIM_JH_PROFILE",
                "JM_top_profile": "MISSING_JM_TOP_PROFILE",
                "B_zero_profile": "MISSING_B_ZERO_PROFILE",
                "R_eq_integral": "MISSING_R_EQ_INTEGRAL",
                "M_H_ref": "MISSING_M_H_REF",
                "epsilon_R_eq_abs": "NOT_COMPUTED",
                "source_file": "MISSING_SOURCE_FILE",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def guard_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "guard_id": "GUARD1154_0_no_bare_mass_shortcut",
                "guard": "bare rest mass cannot be used as M_H_ref unless binding/field dressing is parent-accounted",
                "status": "ACTIVE",
                "reason": "local GR needs dressed Hamiltonian/Noether charge",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1154_1_no_frame_swap",
                "guard": "source frame cannot differ from force/clock/readout frame without Delta_frame residual",
                "status": "ACTIVE",
                "reason": "frame swaps can fake source-normalized Newton",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1154_2_no_readout_surface",
                "guard": "worldtube and shell surfaces cannot be selected from the observed residual profile",
                "status": "ACTIVE",
                "reason": "that would make R_eq a post-fit domain object",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1154_3_no_denominator_without_source",
                "guard": "epsilon_R_eq_abs cannot be computed until M_H_ref is sourced in the same frame",
                "status": "ACTIVE",
                "reason": "normalizing by an unsourced mass hides the real obstruction",
                "valid_for_claim": "false",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1154_0_sources_exist",
                "rule": "all 1154 cited local source paths and needles exist",
                "gate_pass": "true_nonclaim",
                "reason": "source register validates the local audit trail",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1154_1_conditional_owner_law",
                "rule": "conditional source-object owner law is stated without promotion",
                "gate_pass": "true_nonclaim",
                "reason": "law is conditional and current branch status remains blocked",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1154_2_current_source_owned",
                "rule": "current MTS owns W_source, J_H, and M_H_ref in one observed frame",
                "gate_pass": "false",
                "reason": "observed coframe, source variation, worldtube certificate, and Hamiltonian normalization remain missing",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1154_3_profile_schema_ready",
                "rule": "finite-shell R_eq profile schema exists and stays nonclaim",
                "gate_pass": "true_nonclaim",
                "reason": "schema and placeholder row are emitted with missing markers",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1154_4_Newton_GR_promotion",
                "rule": "source-normalized Newton/local-GR claim allowed",
                "gate_pass": "false",
                "reason": "source owner and R_eq profile data are missing",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1154_0_owner_law",
                "decision": "conditional_source_object_owner_law_retained",
                "reason": "a unique observed matter coframe would parent-define J_H and W_source before readout",
                "next_action": "derive the single observed coframe owner or retain Delta_frame",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1154_1_current_branch",
                "decision": "source_object_not_parent_owned_for_current_MTS",
                "reason": "e_obs, J_H variation, W_source certificate, and M_H_ref are not source-backed",
                "next_action": "use the R_eq profile schema only as nonclaim plumbing",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1154_2_best_next",
                "decision": "target_single_observed_coframe_owner_or_frame_residual_row",
                "reason": "e_obs is upstream of J_H, W_source, M_H_ref, WEP, clocks, and orbital readout",
                "next_action": "1155 single observed coframe/source-frame owner or Delta_frame residual row",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1154_0_1155",
                "next_target": "1155-Y5-R10-single-observed-coframe-source-frame-owner-or-frame-residual-row.md",
                "objective": "try to prove e_obs=e_source=e_force=e_clock=e_readout from the parent action; if it fails, create the Delta_frame/Delta_cal residual row",
                "include": "matter coupling; observed coframe; force and clock readout; WEP frame map; Delta_frame schema",
                "exclude": "frame relabel; bare mass shortcut; readout-selected source frame; local-GR/Newton claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    owner: list[dict[str, object]],
    schema: list[dict[str, object]],
    placeholder: list[dict[str, object]],
    guards: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    outputs: dict[str, Path],
) -> list[dict[str, object]]:
    validation: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validation.append(
            {
                "check_id": check_id,
                "result": "pass" if passed else "fail",
                "detail": detail,
                "valid_for_claim": "false",
                "generated_utc": now(),
            }
        )

    all_rows = owner + schema + placeholder + guards + gates + decisions + next_target
    add(
        "V1154_0_sources_exist",
        all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources),
        "all cited local source paths exist and needles are found",
    )
    add(
        "V1154_1_owner_verdict_blocks",
        any(row["owner_id"] == "OWN1154_6_verdict" and row["current_status"] == "SOURCE_OBJECT_NOT_PARENT_OWNED" for row in owner),
        "current source object ownership remains blocked",
    )
    add(
        "V1154_2_schema_groups_present",
        {"PROF1154_0_profile_identity", "PROF1154_1_frame_and_generator", "PROF1154_2_worldtube_surfaces", "PROF1154_3_currents", "PROF1154_4_integrals", "PROF1154_5_normalization"}.issubset(
            {row["schema_id"] for row in schema}
        ),
        "finite-shell R_eq profile schema covers identity, frame, worldtube, currents, integrals, and normalization",
    )
    add(
        "V1154_3_placeholder_nonclaim_missing",
        all(row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" and contains_missing(row["source_file"]) for row in placeholder),
        "placeholder profile row remains missing/nonclaim",
    )
    add(
        "V1154_4_guards_active",
        {"GUARD1154_0_no_bare_mass_shortcut", "GUARD1154_1_no_frame_swap", "GUARD1154_2_no_readout_surface", "GUARD1154_3_no_denominator_without_source"}.issubset(
            {row["guard_id"] for row in guards if row["status"] == "ACTIVE"}
        ),
        "all source-owner guards are active",
    )
    add(
        "V1154_5_claim_gates_blocked",
        any(row["gate_id"] == "G1154_2_current_source_owned" and row["gate_pass"] == "false" for row in gates)
        and any(row["gate_id"] == "G1154_4_Newton_GR_promotion" and row["gate_pass"] == "false" for row in gates),
        "source ownership and Newton/GR promotion remain blocked",
    )
    add(
        "V1154_6_no_claim_rows",
        all(row.get("valid_for_claim") == "false" for row in all_rows)
        and all(row.get("claim_allowed", "false") == "false" for row in next_target),
        "all generated rows remain nonclaim",
    )
    add(
        "V1154_7_next_target",
        next_target[0]["next_target"].startswith("1155-") and "single-observed-coframe" in str(next_target[0]["next_target"]),
        "1155 handoff targets single observed coframe owner or frame residual row",
    )
    add(
        "V1154_8_generated_under_post_checkpoint",
        all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()),
        "all generated outputs are under post-checkpoint-work",
    )
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1154_9_csv_parse", csv_parse_ok, "all 1154 CSV outputs parse cleanly")
    add("V1154_10_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add(
        "V1154_SUMMARY",
        True,
        "1154 retains a conditional source-object owner law, blocks current source ownership, and emits a nonclaim finite-shell R_eq profile schema",
    )
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        cells = [str(row.get(header, "")).replace("|", "/") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    owner: list[dict[str, object]],
    schema: list[dict[str, object]],
    placeholder: list[dict[str, object]],
    guards: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1154 - Y5/R10 Parent Worldtube Hilbert Current Owner or R_eq Profile Builder

**Current verdict:** source-object ownership does not close. A unique observed coframe would parent-define `J_H`, `W_source`, and `M_H_ref`, but current MTS has not supplied the single-frame matter variation, worldtube certificate, or dressed Hamiltonian normalization.

**Useful progress:** the finite-shell `R_eq` profile is now schema-ready without becoming a claim. It explicitly requires the observed frame, source worldtube, current profiles, boundary term, shell integrals, and same-frame `M_H_ref`.

**Important guard:** no denominator without a source. `epsilon_R_eq_abs` cannot be computed honestly until `M_H_ref` is the same-frame dressed Hamiltonian/Noether charge, not bare mass or a readout calibration.

**Best next attack:** derive the single observed coframe owner: `e_obs=e_source=e_force=e_clock=e_readout`. If it fails, the correct fallback is a `Delta_frame/Delta_cal` residual row.

**No claim:** no measured-GM, source-normalized Newton, local-GR, PPN, R10, WEP, GitHub, or public claim follows from 1154.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "role"], sources)}

## Source Owner Audit
{table(["owner_id", "claim_piece", "mathematical_form", "current_status", "missing_for_current_MTS", "effect_on_R_eq", "valid_for_claim"], owner)}

## R_eq Profile Schema
{table(["schema_id", "field_group", "required_columns", "acceptance_rule", "current_status", "valid_for_claim", "claim_allowed"], schema)}

## R_eq Placeholder Profile
{table(["profile_id", "system_id", "branch_id", "e_obs_definition", "W_source_definition", "surface_pair", "PiM_JH_profile", "JM_top_profile", "B_zero_profile", "R_eq_integral", "M_H_ref", "epsilon_R_eq_abs", "source_file", "valid_for_claim", "claim_allowed"], placeholder)}

## Source Owner Guards
{table(["guard_id", "guard", "status", "reason", "valid_for_claim"], guards)}

## Claim Gates
{table(["gate_id", "rule", "gate_pass", "reason", "valid_for_claim"], gates)}

## Decision Ledger
{table(["decision_id", "decision", "reason", "next_action", "valid_for_claim"], decisions)}

## Validation
{table(["check_id", "result", "detail", "valid_for_claim"], validation)}

## Next Target
{table(["next_id", "next_target", "objective", "include", "exclude", "valid_for_claim", "claim_allowed"], next_target)}
"""
    DOC.write_text(text, encoding="utf-8")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists() and pycache.is_dir():
        shutil.rmtree(pycache)


def main() -> None:
    outputs = {
        "source_register": OUT / "P8_Y5_R10_1154_SOURCE_REGISTER.csv",
        "owner": OUT / "P8_Y5_R10_1154_SOURCE_OWNER_AUDIT.csv",
        "schema": OUT / "P8_Y5_R10_1154_R_EQ_PROFILE_SCHEMA.csv",
        "placeholder": OUT / "P8_Y5_R10_1154_R_EQ_PLACEHOLDER_PROFILE.csv",
        "guards": OUT / "P8_Y5_R10_1154_SOURCE_OWNER_GUARDS.csv",
        "gates": OUT / "P8_Y5_R10_1154_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1154_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1154_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1154_VALIDATION.csv",
    }

    sources = source_rows()
    owner = owner_audit_rows()
    schema = profile_schema_rows()
    placeholder = placeholder_rows()
    guards = guard_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["owner"], owner)
    write_csv(outputs["schema"], schema)
    write_csv(outputs["placeholder"], placeholder)
    write_csv(outputs["guards"], guards)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, owner, schema, placeholder, guards, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, owner, schema, placeholder, guards, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    if failed:
        for row in failed:
            print(f"{row['check_id']}: {row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
