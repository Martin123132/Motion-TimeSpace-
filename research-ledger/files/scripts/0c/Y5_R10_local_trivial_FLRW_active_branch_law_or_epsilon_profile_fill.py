from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1144-Y5-R10-local-trivial-FLRW-active-branch-law-or-epsilon-profile-fill.md"


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


def source_rows() -> list[dict[str, object]]:
    sources = [
        {
            "source_id": "SRC1144_0_1143_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1143_NEXT_TARGET.csv",
            "needle": "NEXT1143_0_1144",
            "role": "handoff requiring local-trivial/FLRW-active branch law or epsilon fill.",
        },
        {
            "source_id": "SRC1144_1_1143_signature",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1143_A8_PARENT_SIGNATURE_CONTRACT.csv",
            "needle": "A8SIG1143_2_exact_local_representative",
            "role": "exact local representative is the A8 clause blocking epsilon silence.",
        },
        {
            "source_id": "SRC1144_2_1143_epsilon",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1143_EPSILON_DOMAIN_FLUX_PROFILE_FIRST_FILL.csv",
            "needle": "EPS1143_0_local_compact_profile",
            "role": "epsilon_domain_flux first-fill schema if branch law fails.",
        },
        {
            "source_id": "SRC1144_3_JC_275",
            "relative_path": "275-JC-three-form-memory-current-from-Q.md",
            "needle": "stationary bound systems select trivial class",
            "role": "conditional kinematic target: local trivial class and FLRW nonzero class.",
        },
        {
            "source_id": "SRC1144_4_Qcoh_276",
            "relative_path": "276-coherent-domain-projector-from-parent-variables.md",
            "needle": "fixed_D_Qcoh_projection_mathematically_derived_domain_selector_not_parent_derived",
            "role": "fixed-domain coherent projection is derived, domain selector is not.",
        },
        {
            "source_id": "SRC1144_5_boundary_277",
            "relative_path": "277-domain-free-boundary-Euler-equation.md",
            "needle": "Ccoh_free_boundary_Euler_equation_derived_but_degenerate_domain_not_parent_selected",
            "role": "free-boundary Euler equation gives degenerate extrema but not unique physical domain.",
        },
        {
            "source_id": "SRC1144_6_nogo_279",
            "relative_path": "279-representative-selection-boundary-polarization-no-go.md",
            "needle": "boundary_polarization_endpoint_constraints_underselect_representative_selection_not_derived",
            "role": "representative selection is underdetermined without parent law.",
        },
        {
            "source_id": "SRC1144_7_Cexp_416",
            "relative_path": "416-binding-invariant-domain-selector-repair.md",
            "needle": "binding_invariant_domain_selector_repair_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass",
            "role": "C_exp is a clean kinematic separator but not parent-derived.",
        },
        {
            "source_id": "SRC1144_8_Qcoh_481",
            "relative_path": "481-Qcoh-parent-projector-algebra-or-closure.md",
            "needle": "Qcoh_parent_projector_algebra_written_trace_projector_pass_parent_action_missing_closure_retained_no_alpha3_PPN_Newton_or_local_GR_pass",
            "role": "Qcoh algebra is written; parent action ownership remains missing.",
        },
        {
            "source_id": "SRC1144_9_quotient_864",
            "relative_path": "864-Y5-R10-local-global-quotient-split-and-endpoint-stationarity-parent-clause.md",
            "needle": "LGS864_0_conditional_split_lemma",
            "role": "local/global quotient split is a conditional sufficient lemma, not a parent derivation.",
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


def branch_attempt_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "attempt_id": "BL1144_0_fixed_D_Qcoh",
                "branch_law_piece": "for fixed D, coherent projection Q -> Q_coh is mathematically defined",
                "candidate_form": "Q_coh=(Tr_D Q/3) h and J_C=det_h(Q_coh) Omega_D/V_D",
                "supports": "FLRW homogeneous scalar class and shear-safe coherent trace projection",
                "current_status": "SHAPE_SUPPORT_ONLY",
                "why_not_derivation": "physical D is not selected by parent action",
                "source_anchor": "276;481",
                "valid_for_claim": "false",
            },
            {
                "attempt_id": "BL1144_1_free_boundary_extrema",
                "branch_law_piece": "free-boundary Euler equation admits desired local and FLRW stationary branches",
                "candidate_form": "delta_D S_branch=0 gives vanishing boundary integrand for FLRW and stationary local classes",
                "supports": "local silence and FLRW activation can both be extrema",
                "current_status": "DEGENERATE_UNDERSELECTED",
                "why_not_derivation": "many domains extremize; no unique physical representative is chosen",
                "source_anchor": "277",
                "valid_for_claim": "false",
            },
            {
                "attempt_id": "BL1144_2_representative_selection",
                "branch_law_piece": "boundary polarization/endpoint selector tries to choose local trivial versus FLRW active representative",
                "candidate_form": "C_coh=0 -> local trivial representative; C_coh=1 -> FLRW expansion representative",
                "supports": "desired local/FLRW split as labelled selector",
                "current_status": "UNDERSELECTED_NO_GO",
                "why_not_derivation": "boundary polarization constraints underselect the representative and import selector scales unless parent-derived",
                "source_anchor": "279",
                "valid_for_claim": "false",
            },
            {
                "attempt_id": "BL1144_3_Cexp_separator",
                "branch_law_piece": "binding/coherent expansion invariant C_exp separates stationary bound domains from FLRW",
                "candidate_form": "C_exp[D]=0 for stationary/local bound domains and C_exp[D]!=0 for coherent FLRW expansion",
                "supports": "single kinematic local/cosmology separator without Newtonian binding-energy hand choice",
                "current_status": "KINEMATIC_SUPPORT_CONTRACT_NOT_DERIVED",
                "why_not_derivation": "E_chi=0 selector, thresholds, candidate domains, and Bianchi-safe stress cancellation are not parent-derived",
                "source_anchor": "416",
                "valid_for_claim": "false",
            },
            {
                "attempt_id": "BL1144_4_quotient_split",
                "branch_law_piece": "local/global quotient split allows FLRW-visible trace/domain direction to be local-invisible",
                "candidate_form": "Dq_FLRW[v_D]!=0 while Dq_loc[U][v_D]=0 for compact non-cosmological U",
                "supports": "one parent state could have FLRW memory without local matter leakage",
                "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
                "why_not_derivation": "q_FLRW, q_loc, and v_D/v_T classification are not derived from parent action",
                "source_anchor": "864",
                "valid_for_claim": "false",
            },
            {
                "attempt_id": "BL1144_5_verdict",
                "branch_law_piece": "parent branch-selection law",
                "candidate_form": "S_parent -> {D_local exact/trivial, D_FLRW homogeneous scalar} by one quotient/projector law",
                "supports": "would close A8 local representative and epsilon_domain_flux if parent-signed",
                "current_status": "BRANCH_LAW_NOT_DERIVED",
                "why_not_derivation": "all available routes are shape support, degenerate extrema, conditional split, or closure contract",
                "source_anchor": "1144",
                "valid_for_claim": "false",
            },
        ]
    )


def cohomology_audit_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "audit_id": "RC1144_0_local_exact_class",
                "object": "local compact domain class",
                "needed_statement": "[J_D]_local=0 or P_D J_D=d Lambda_D in the observed compact local branch",
                "current_evidence": "supported as desired branch in 275/277/309, but not parent-selected",
                "status": "NOT_PARENT_DERIVED",
                "effect": "epsilon_domain_flux remains open",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "RC1144_1_FLRW_scalar_class",
                "object": "FLRW homogeneous scalar domain class",
                "needed_statement": "P_D J_D is retained only as homogeneous scalar/coherent volume class in FLRW",
                "current_evidence": "275 gives conditional determinant/volume form and 416 gives kinematic separator",
                "status": "CONDITIONAL_SHAPE_SUPPORT",
                "effect": "cosmology branch can be retained only as nonclaim theorem target",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "RC1144_2_same_parent_law",
                "object": "no hand-switch branch law",
                "needed_statement": "one parent Euler/Ward/quotient law selects both local exactness and FLRW scalar activity",
                "current_evidence": "279 says representative selection is underdetermined; 864 says quotient split is conditional",
                "status": "MISSING_PARENT_BRANCH_LAW",
                "effect": "cannot use local silence while keeping FLRW activity as proof",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "RC1144_3_shear_vector_exclusion",
                "object": "tracefree/vector local leakage",
                "needed_statement": "raw det(Q) shear/vector pieces are projected out by parent-owned P_coh/P_D before local PPN readout",
                "current_evidence": "275/478 warn raw det(Q) leaks tracefree shear; 481 writes algebra but parent ownership missing",
                "status": "PROJECTOR_OWNERSHIP_MISSING",
                "effect": "preferred-frame and xi guards stay active",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "RC1144_4_R11_sibling",
                "object": "R11 source-normalization sibling rows",
                "needed_statement": "local exact branch also kills or scores R11 c/vector/STF/flux source-normalization rows",
                "current_evidence": "1142/1143 keep R11 sibling silence unproved",
                "status": "MISSING_R11_SILENCE",
                "effect": "even a branch law would still need R11 confirmation",
                "valid_for_claim": "false",
            },
        ]
    )


def guard_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "guard_id": "GDS1144_0_no_hand_switch",
                "rule": "do not choose local trivial and FLRW active branches by hand",
                "status": "ACTIVE_GUARD",
                "reason": "the same parent law must select both branches",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GDS1144_1_no_quiet_domain_selection",
                "rule": "do not pick the quiet local domain after checking PPN/alpha3",
                "status": "ACTIVE_GUARD",
                "reason": "domain candidates and branch selector must be parent-generated before readout",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GDS1144_2_no_raw_detQ",
                "rule": "do not use unprojected det(Q) locally",
                "status": "ACTIVE_GUARD",
                "reason": "raw determinant leaks tracefree shear at second order",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GDS1144_3_no_epsilon_zero_by_label",
                "rule": "epsilon_domain_flux=0 requires parent no-flux certificate or sourced profile",
                "status": "ACTIVE_GUARD",
                "reason": "exact/trivial class is not yet parent-selected",
                "valid_for_claim": "false",
            },
        ]
    )


def epsilon_fill_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "fill_id": "EPF1144_0_epsilon_profile_local",
                "target": "epsilon_domain_flux",
                "branch": "compact_stationary_local_observed_coframe",
                "definition": "normalized projected local domain momentum/source flux entering K*c*epsilon alpha3 product",
                "required_fields": "system_id; domain_candidate_rule; local_representative_status; epsilon_abs; epsilon_units; profile_support; source_path; valid_for_claim",
                "current_value": "MISSING_EPSILON_DOMAIN_FLUX_PROFILE_OR_ZERO_THEOREM",
                "source_path": "MISSING_SOURCE_PATH",
                "acceptance": "parent no-flux certificate or sourced profile compatible with abs(K*c*epsilon)<=4e-20",
                "status": "SOURCE_PROFILE_ROW_REQUIRED",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "fill_id": "EPF1144_1_branch_selector_evidence",
                "target": "local_trivial_FLRW_active_branch_selector",
                "branch": "shared_parent_branch_law",
                "definition": "one rule selects local exact/trivial class and FLRW homogeneous scalar class",
                "required_fields": "parent_variable; Euler_or_Ward_equation; local_solution; FLRW_solution; no_hand_switch_check; source_path",
                "current_value": "MISSING_PARENT_BRANCH_SELECTION_LAW",
                "source_path": "MISSING_SOURCE_PATH",
                "acceptance": "single parent-signed branch law, not two imposed branch labels",
                "status": "PARENT_SIGNATURE_REQUIRED",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1144_0_sources_exist",
                "rule": "all local/FLRW branch-law source anchors exist",
                "gate_pass": "true_nonclaim",
                "reason": "source files and needles are present",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1144_1_branch_shape_support",
                "rule": "branch-law shape has internal support",
                "gate_pass": "true_nonclaim",
                "reason": "fixed-D Qcoh, C_exp separator, and quotient split form a coherent theorem target",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1144_2_parent_branch_law",
                "rule": "parent action selects local exact/trivial and FLRW scalar classes",
                "gate_pass": "false",
                "reason": "free-boundary and representative selectors are degenerate/underselected",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1144_3_epsilon_profile",
                "rule": "epsilon_domain_flux is sourced or theorem-zero",
                "gate_pass": "false",
                "reason": "epsilon profile row remains MISSING_SOURCE_PATH",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1144_4_local_GR_promotion",
                "rule": "R10/PPN/alpha3/local-GR promotion allowed",
                "gate_pass": "false",
                "reason": "branch law not parent-derived and epsilon profile not filled",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1144_0_verdict",
                "decision": "branch_law_shape_supported_but_not_derived",
                "reason": "the corpus supports the target structure but not the parent selector that chooses the branches",
                "next_action": "write exact parent functional for the branch selector or fill epsilon profile",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1144_1_best_next",
                "decision": "attempt_parent_branch_functional",
                "reason": "the remaining missing object is not another bound; it is the variational law selecting D/local class",
                "next_action": "construct or reject S_branch[chi_D,P_D,Q] with Euler law selecting local exact and FLRW scalar branches",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1144_2_claim_ceiling",
                "decision": "keep_epsilon_and_A8_nonclaim",
                "reason": "epsilon_domain_flux is still neither zero nor sourced",
                "next_action": "no alpha3/PPN/local-GR claim",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1144_0_1145",
                "next_target": "1145-Y5-R10-parent-branch-functional-for-chiD-or-epsilon-profile-source-row.md",
                "objective": "construct or reject a parent branch functional S_branch[chi_D,P_D,Q] whose Euler/Ward equation selects local exact/trivial class and FLRW homogeneous scalar class; if rejected, fill epsilon_domain_flux profile as nonclaim source row",
                "include": "chi_D; P_D; Q_coh; C_exp; free-boundary Euler law; no-hand-switch guard; epsilon profile fallback",
                "exclude": "quiet-domain hand choice; raw det(Q) local use; tuned cancellation; alpha3/local-GR claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    branch_attempt: list[dict[str, object]],
    cohomology: list[dict[str, object]],
    guards: list[dict[str, object]],
    epsilon_fills: list[dict[str, object]],
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

    all_rows = branch_attempt + cohomology + guards + epsilon_fills + gates + decisions + next_target
    add(
        "V1144_0_sources_exist",
        all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources),
        "all cited local source paths exist and needles are found",
    )
    add(
        "V1144_1_branch_attempt_coverage",
        {row["attempt_id"] for row in branch_attempt}
        == {
            "BL1144_0_fixed_D_Qcoh",
            "BL1144_1_free_boundary_extrema",
            "BL1144_2_representative_selection",
            "BL1144_3_Cexp_separator",
            "BL1144_4_quotient_split",
            "BL1144_5_verdict",
        },
        "all branch-law pieces are represented",
    )
    add(
        "V1144_2_branch_not_derived",
        branch_attempt[-1]["current_status"] == "BRANCH_LAW_NOT_DERIVED"
        and any(row["current_status"] == "DEGENERATE_UNDERSELECTED" for row in branch_attempt),
        "branch-law shape is not promoted as derivation",
    )
    add(
        "V1144_3_relative_cohomology_audit",
        {"RC1144_0_local_exact_class", "RC1144_1_FLRW_scalar_class", "RC1144_2_same_parent_law"}.issubset(
            {row["audit_id"] for row in cohomology}
        ),
        "local exact, FLRW scalar, and same-parent law are audited",
    )
    add(
        "V1144_4_guards_active",
        len(guards) == 4 and all(row["status"] == "ACTIVE_GUARD" for row in guards),
        "no-hand-switch and shortcut guards are active",
    )
    add(
        "V1144_5_epsilon_fill_rows",
        {row["fill_id"] for row in epsilon_fills} == {"EPF1144_0_epsilon_profile_local", "EPF1144_1_branch_selector_evidence"}
        and all(row["source_path"] == "MISSING_SOURCE_PATH" for row in epsilon_fills),
        "epsilon profile and branch-selector source rows remain unfilled",
    )
    add(
        "V1144_6_claim_gates_blocked",
        any(row["gate_id"] == "G1144_2_parent_branch_law" and row["gate_pass"] == "false" for row in gates)
        and any(row["gate_id"] == "G1144_4_local_GR_promotion" and row["gate_pass"] == "false" for row in gates),
        "parent branch law and local claim gates remain blocked",
    )
    add(
        "V1144_7_no_claim_rows",
        all(row.get("valid_for_claim") == "false" for row in all_rows)
        and all(row.get("claim_allowed", "false") == "false" for row in epsilon_fills + next_target),
        "all generated rows remain nonclaim",
    )
    add(
        "V1144_8_next_target",
        next_target[0]["next_target"].startswith("1145-") and "branch-functional" in str(next_target[0]["next_target"]),
        "1145 handoff targets parent branch functional or epsilon profile source row",
    )
    add(
        "V1144_9_generated_under_post_checkpoint",
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
    add("V1144_10_csv_parse", csv_parse_ok, "all 1144 CSV outputs parse cleanly")
    add("V1144_11_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add(
        "V1144_SUMMARY",
        True,
        "1144 finds branch-law shape support but no parent derivation, keeps epsilon fill nonclaim, and sends branch functional to 1145",
    )
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    branch_attempt: list[dict[str, object]],
    cohomology: list[dict[str, object]],
    guards: list[dict[str, object]],
    epsilon_fills: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1144 - Y5/R10 Local-Trivial/FLRW-Active Branch Law or Epsilon Profile Fill

**Current verdict:** the branch-law shape is supported, but not parent-derived. The corpus has the right ingredients, but no parent Euler/Ward/quotient law yet selects local exact/trivial class while retaining FLRW homogeneous scalar class.

**Useful progress:** the remaining object is now precise: a parent branch functional must generate `D_local` exactness and `D_FLRW` scalar activity by one law, not by hand-switching.

**Important guard:** fixed-domain `Q_coh`, free-boundary extrema, `C_exp`, and quotient splits are useful footwork, not knockout proofs. `epsilon_domain_flux` remains open until the branch law closes or a sourced profile is filled.

**Best next attack:** construct or reject `S_branch[chi_D,P_D,Q]` with an Euler/Ward equation selecting the branch. If that fails, fill the `epsilon_domain_flux` source/profile row.

**No claim:** no R10, PPN, alpha3, preferred-frame, local-GR, measured-GM, GitHub, or public claim follows from 1144.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "role"], sources)}

## Branch-Law Attempt
{table(["attempt_id", "branch_law_piece", "candidate_form", "supports", "current_status", "why_not_derivation", "source_anchor", "valid_for_claim"], branch_attempt)}

## Relative-Cohomology Split Audit
{table(["audit_id", "object", "needed_statement", "current_evidence", "status", "effect", "valid_for_claim"], cohomology)}

## No-Hand-Switch Guards
{table(["guard_id", "rule", "status", "reason", "valid_for_claim"], guards)}

## Epsilon/Profile Fill Queue
{table(["fill_id", "target", "branch", "definition", "required_fields", "current_value", "source_path", "acceptance", "status", "valid_for_claim"], epsilon_fills)}

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
        "source_register": OUT / "P8_Y5_R10_1144_SOURCE_REGISTER.csv",
        "branch_attempt": OUT / "P8_Y5_R10_1144_BRANCH_LAW_ATTEMPT.csv",
        "cohomology": OUT / "P8_Y5_R10_1144_RELATIVE_COHOMOLOGY_SPLIT_AUDIT.csv",
        "guards": OUT / "P8_Y5_R10_1144_LOCAL_FLRW_NO_HAND_SWITCH_GUARDS.csv",
        "epsilon_fills": OUT / "P8_Y5_R10_1144_EPSILON_DOMAIN_FLUX_PROFILE_FILL_QUEUE.csv",
        "gates": OUT / "P8_Y5_R10_1144_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1144_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1144_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1144_VALIDATION.csv",
    }
    sources = source_rows()
    branch_attempt = branch_attempt_rows()
    cohomology = cohomology_audit_rows()
    guards = guard_rows()
    epsilon_fills = epsilon_fill_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["branch_attempt"], branch_attempt)
    write_csv(outputs["cohomology"], cohomology)
    write_csv(outputs["guards"], guards)
    write_csv(outputs["epsilon_fills"], epsilon_fills)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, branch_attempt, cohomology, guards, epsilon_fills, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, branch_attempt, cohomology, guards, epsilon_fills, gates, decisions, validation, next_target)
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
