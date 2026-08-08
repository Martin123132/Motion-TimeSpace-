from __future__ import annotations

import csv
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "996-Y5-R10-relative-boundary-class-owner-or-Bref-source-bound-pack.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def md_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def source_path(relative_path: str) -> Path:
    return ROOT / relative_path


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "995_doc",
            "path": "995-Y5-R10-boundary-reference-current-zero-theorem-or-residual-bound-row.md",
            "role": "handoff selecting relative boundary class/B_ref owner or source-bound pack",
            "needle": "996-Y5-R10-relative-boundary-class-owner-or-Bref-source-bound-pack.md",
        },
        {
            "source_id": "995_zero_gate",
            "path": "source-intake/mts_residuals/P8_Y5_R10_995_BOUNDARY_REFERENCE_ZERO_THEOREM_GATE.csv",
            "role": "zero theorem blocker list",
            "needle": "ZT995_3_relative_cohomology_exactness",
        },
        {
            "source_id": "995_bound_schema",
            "path": "source-intake/mts_residuals/P8_Y5_R10_995_RC9940_RESIDUAL_BOUND_ROW_SCHEMA.csv",
            "role": "RC994_0 residual-bound schema",
            "needle": "BR995_5_RC9940_total_abs",
        },
        {
            "source_id": "545_contract",
            "path": "source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_MINIMAL_ACTION_CONTRACT.csv",
            "role": "minimal boundary/reference action clauses",
            "needle": "MAC545_2_reference_lock",
        },
        {
            "source_id": "549_theorem_attempt",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_BOUNDARY_COHOMOLOGY_NOHAIR_THEOREM_ATTEMPT.csv",
            "role": "failed cohomology/nohair certificate",
            "needle": "BCT549_6_certificate_verdict",
        },
        {
            "source_id": "552_zero_contract",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_PARENT_ACTION_ZERO_THEOREM_CONTRACT.csv",
            "role": "BRR545 parent-action zero-theorem clauses",
            "needle": "BZTC552_3_boundary_relative_nohair",
        },
        {
            "source_id": "667_action_ansatz",
            "path": "source-intake/mts_residuals/P8_Y5_R10_667_PARENT_BOUNDARY_ACTION_ANSATZ.csv",
            "role": "explicit parent-boundary action scaffold",
            "needle": "PBA667_2_boundary_action",
        },
        {
            "source_id": "667_variation_ledger",
            "path": "source-intake/mts_residuals/P8_Y5_R10_667_VARIATION_LEDGER.csv",
            "role": "variation ledger for B_ref and boundary flux",
            "needle": "VL667_6_boundary_flux",
        },
        {
            "source_id": "668_boundary_lock",
            "path": "source-intake/mts_residuals/P8_Y5_R10_668_BOUNDARY_CONDITION_LOCK.csv",
            "role": "failed boundary condition lock rows",
            "needle": "BCL668_2_relative_class",
        },
        {
            "source_id": "677_boundary_class_audit",
            "path": "source-intake/mts_residuals/P8_Y5_R10_677_BEDGE_BOUNDARY_CLASS_OWNERSHIP_AUDIT.csv",
            "role": "parent-owned boundary class audit",
            "needle": "BBC677_6_verdict",
        },
        {
            "source_id": "678_silence_stack",
            "path": "source-intake/mts_residuals/P8_Y5_R10_678_SILENCE_STACK_AUDIT.csv",
            "role": "boundary class/nohair/projector silence stack",
            "needle": "SSA678_7_verdict",
        },
        {
            "source_id": "678_source_gate",
            "path": "source-intake/mts_residuals/P8_Y5_R10_678_BX_SOURCE_ROW_GATE.csv",
            "role": "first source row gate for boundary/edge factor",
            "needle": "BXG678_4_no_shortcut_guard",
        },
    ]
    rows: list[dict[str, str]] = []
    for spec in specs:
        path = source_path(spec["path"])
        text = read_text(path)
        rows.append(
            {
                "source_id": spec["source_id"],
                "role": spec["role"],
                "path": spec["path"],
                "exists": flag(path.exists()),
                "needle_found": flag(spec["needle"] in text),
                "needle": spec["needle"],
                "valid_for_claim": "false",
            }
        )
    return rows


def relative_boundary_owner_attempt_rows() -> list[dict[str, str]]:
    return [
        {
            "owner_id": "RBO996_0_parent_boundary_action",
            "candidate_owner": "S_parent boundary sector",
            "mathematical_contract": "B_total=B_GHY[g]+B_ref[gamma_ref,tau_ref,C_top]+B_class[chi_B,C_top]+B_ct[fixed_branch]",
            "what_it_would_prove": "places reference subtraction and relative boundary class inside the parent action before readout",
            "current_evidence": "667 writes this as a scaffold",
            "missing_signature": "unique parent principle selecting B_ref, B_class, C_top, and allowed variations",
            "owner_status": "scaffold_only",
            "accepted_for_claim": "false",
            "valid_for_claim": "false",
        },
        {
            "owner_id": "RBO996_1_Ctop_superselection",
            "candidate_owner": "relative/topological class C_top",
            "mathematical_contract": "delta C_top=0 and partial_source,r,t,frame,lambda C_top=0 on the local branch",
            "what_it_would_prove": "prevents the trivial boundary class from being selected after seeing the source/readout",
            "current_evidence": "668 marks relative class C_top as fail_current_claim",
            "missing_signature": "parent Euler/Ward/topological selector fixing C_top before the branch is fitted",
            "owner_status": "not_signed",
            "accepted_for_claim": "false",
            "valid_for_claim": "false",
        },
        {
            "owner_id": "RBO996_2_exact_proper_boundary",
            "candidate_owner": "proper exact boundary sector",
            "mathematical_contract": "B_imp=d_partial b with [B_imp]_{H_rel}=0 and integral_S2 B_imp-integral_S1 B_imp=integral_A dB_imp=0",
            "what_it_would_prove": "B_zero_flux=0 without a plateau axiom",
            "current_evidence": "549 and 677 state the conditional Stokes route",
            "missing_signature": "proof that the MTS boundary representative is exact in the parent-selected relative class",
            "owner_status": "conditional_not_owned",
            "accepted_for_claim": "false",
            "valid_for_claim": "false",
        },
        {
            "owner_id": "RBO996_3_no_improper_charge_guard",
            "candidate_owner": "proper/improper charge split",
            "mathematical_contract": "exact boundary zero acts only on proper-gauge/topological edge data and cannot erase H_tau, ADM/Komar mass, or M_H_ref",
            "what_it_would_prove": "the zero is physically legal rather than a reference subtraction trick",
            "current_evidence": "677/678 mark proper-charge guard as not signed",
            "missing_signature": "same-frame Hamiltonian/source-mass equality plus fixed reference branch",
            "owner_status": "not_signed",
            "accepted_for_claim": "false",
            "valid_for_claim": "false",
        },
        {
            "owner_id": "RBO996_4_boundary_nohair",
            "candidate_owner": "boundary no-hair / boundary Euler equation",
            "mathematical_contract": "T_B^TF=T_B^vector=T_B^shear=T_B^radial=T_B^time=T_B^frame=0 on allowed local shell",
            "what_it_would_prove": "prevents B_zero_flux or Delta_symp from leaking into PPN/preferred-frame/source-normalization channels",
            "current_evidence": "549/668/678 keep nohair unsigned",
            "missing_signature": "parent-owned homogeneous marker-free boundary action or coefficient vector",
            "owner_status": "not_derived",
            "accepted_for_claim": "false",
            "valid_for_claim": "false",
        },
        {
            "owner_id": "RBO996_5_projector_same_domain",
            "candidate_owner": "same-domain projector/quotient/Hamiltonian charge",
            "mathematical_contract": "Dq[v_B]=0 and Pi_M^H[d_partial b]=0 on the same boundary domain used by Q_tau and the local arena",
            "what_it_would_prove": "prevents an exact boundary primitive from reappearing as projector symplectic stress",
            "current_evidence": "678 marks domain/projector lock as not signed",
            "missing_signature": "single parent-owned boundary domain for quotient, projector, Hamiltonian charge, and readout",
            "owner_status": "not_signed",
            "accepted_for_claim": "false",
            "valid_for_claim": "false",
        },
        {
            "owner_id": "RBO996_6_Bref_derivative_vector",
            "candidate_owner": "B_ref superselection",
            "mathematical_contract": "partial_source Delta_ref=partial_r Delta_ref=partial_t Delta_ref=partial_frame Delta_ref=partial_lambda Delta_ref=0",
            "what_it_would_prove": "Delta_ref_over_MH=0 as a theorem rather than a chosen subtraction",
            "current_evidence": "667 writes the derivative test; 668 marks fixed branch as fail_current_claim",
            "missing_signature": "B_ref normalization rule from the parent action/topology/stationarity",
            "owner_status": "not_signed",
            "accepted_for_claim": "false",
            "valid_for_claim": "false",
        },
        {
            "owner_id": "RBO996_7_verdict",
            "candidate_owner": "relative boundary class plus B_ref owner theorem",
            "mathematical_contract": "RBO996_0 through RBO996_6 all accepted before readout",
            "what_it_would_prove": "Delta_ref=B_zero_flux=boundary hair=projector boundary tail=0 for RC994_0",
            "current_evidence": "scaffold exists, owner signatures do not",
            "missing_signature": "unique parent boundary action and signed silence stack",
            "owner_status": "failed_current_claim",
            "accepted_for_claim": "false",
            "valid_for_claim": "false",
        },
    ]


def bref_superselection_test_rows() -> list[dict[str, str]]:
    derivatives = [
        ("BST996_0_source", "partial_source Delta_ref", "source-dependent reference drift"),
        ("BST996_1_radius", "partial_r Delta_ref", "surface/radius-dependent reference drift"),
        ("BST996_2_time", "partial_t Delta_ref", "clock/time-dependent reference drift"),
        ("BST996_3_frame", "partial_frame Delta_ref", "frame/coframe-dependent reference drift"),
        ("BST996_4_range", "partial_lambda Delta_ref", "range/scale-dependent reference drift"),
    ]
    rows = [
        {
            "test_id": test_id,
            "derivative_test": derivative,
            "needed_zero": "0",
            "current_value": "MISSING_PARENT_BREF_RULE",
            "failure_mode": failure_mode,
            "source_requirement": "B_ref rule plus equation/source path or theorem_zero certificate",
            "status": "blocked_nonclaim",
            "valid_for_claim": "false",
        }
        for test_id, derivative, failure_mode in derivatives
    ]
    rows.append(
        {
            "test_id": "BST996_5_Bref_vector_verdict",
            "derivative_test": "all B_ref derivative tests",
            "needed_zero": "all zero componentwise",
            "current_value": "MISSING_PARENT_BREF_RULE",
            "failure_mode": "Delta_ref cannot be zeroed by reference choice",
            "source_requirement": "componentwise theorem-zero or source-backed Delta_ref bound",
            "status": "fail_current_claim",
            "valid_for_claim": "false",
        }
    )
    return rows


def silence_stack_bridge_rows() -> list[dict[str, str]]:
    return [
        {
            "stack_id": "SSB996_0_exactness",
            "borrowed_clause": "SSA678_0_boundary_primitive;BBC677_1_exact_boundary_class",
            "applies_to_RC9940": "yes",
            "needed_for": "B_zero_flux_over_MH",
            "current_status": "candidate_formula_not_primitive",
            "nonclaim_reason": "boundary representative is not parent-owned as an exact primitive",
            "valid_for_claim": "false",
        },
        {
            "stack_id": "SSB996_1_relative_class",
            "borrowed_clause": "SSA678_1_relative_class;BCL668_2_relative_class",
            "applies_to_RC9940": "yes",
            "needed_for": "B_zero_flux_over_MH",
            "current_status": "not_signed",
            "nonclaim_reason": "relative class C_top is still selectable, not parent-selected",
            "valid_for_claim": "false",
        },
        {
            "stack_id": "SSB996_2_nohair",
            "borrowed_clause": "SSA678_2_no_vector_tensor_hair;MAC545_4",
            "applies_to_RC9940": "yes",
            "needed_for": "B_TF_vector_radial_hair_over_MH",
            "current_status": "not_derived",
            "nonclaim_reason": "scalar/trace no-flux does not kill vector/tensor/derivative hair",
            "valid_for_claim": "false",
        },
        {
            "stack_id": "SSB996_3_projector_stress",
            "borrowed_clause": "SSA678_3_projector_stress_silence;MAC545_5",
            "applies_to_RC9940": "yes",
            "needed_for": "projector_boundary_commutator_over_MH",
            "current_status": "conditions_written_not_closed",
            "nonclaim_reason": "projector stress may still live on the boundary",
            "valid_for_claim": "false",
        },
        {
            "stack_id": "SSB996_4_proper_charge_guard",
            "borrowed_clause": "SSA678_5_proper_charge_guard",
            "applies_to_RC9940": "yes",
            "needed_for": "do not erase H_tau/M_H_ref",
            "current_status": "not_signed",
            "nonclaim_reason": "same-frame source-mass equality and reference branch are still open",
            "valid_for_claim": "false",
        },
        {
            "stack_id": "SSB996_5_stack_verdict",
            "borrowed_clause": "SSA678_7_verdict",
            "applies_to_RC9940": "yes",
            "needed_for": "RC994_0 theorem-zero route",
            "current_status": "not_derived_nonclaim",
            "nonclaim_reason": "all silence stack clauses are useful but unsigned",
            "valid_for_claim": "false",
        },
    ]


def source_bound_input_pack_rows() -> list[dict[str, str]]:
    return [
        {
            "input_id": "SBI996_0_Delta_ref",
            "target": "Delta_ref_over_MH",
            "required_columns": "system_id;surface_pair;Delta_ref;M_H_ref;units;B_ref_rule;derivative_vector;source_path;equation_ref;valid_for_claim",
            "acceptance_rule": "numeric finite dimensionless bound or theorem_zero=true; all B_ref derivative channels sourced; M_H_ref same-frame positive",
            "current_fill": "MISSING_DELTA_REF_VALUE_AND_BREF_RULE",
            "blocks": "RC994_0;DeltaH;FB554_0",
            "valid_for_claim": "false",
        },
        {
            "input_id": "SBI996_1_B_zero_flux",
            "target": "B_zero_flux_over_MH",
            "required_columns": "system_id;surface_pair;B_zero_flux;M_H_ref;units;relative_class_rule;boundary_primitive;source_path;equation_ref;valid_for_claim",
            "acceptance_rule": "relative class theorem-zero or sourced boundary flux profile with no MISSING markers",
            "current_fill": "MISSING_BOUNDARY_FLUX_VALUE_OR_RELATIVE_CLASS_ZERO",
            "blocks": "RC994_0;R7/R8/R4/R9/R11 boundary rows",
            "valid_for_claim": "false",
        },
        {
            "input_id": "SBI996_2_boundary_hair",
            "target": "B_TF_vector_radial_hair_over_MH",
            "required_columns": "system_id;hair_channel;coefficient;profile;bound;M_H_ref;mapped_lock_row;source_path;equation_ref;valid_for_claim",
            "acceptance_rule": "each vector/tensor/shear/time/radial/frame channel theorem-zero or sourced; no cancellation credit",
            "current_fill": "MISSING_BOUNDARY_HAIR_COEFFICIENTS",
            "blocks": "PPN preferred-frame/source-normalization safety",
            "valid_for_claim": "false",
        },
        {
            "input_id": "SBI996_3_projector_boundary",
            "target": "projector_boundary_commutator_over_MH",
            "required_columns": "system_id;surface_pair;projector_commutator;deltaPiM_boundary;domain_rule;M_H_ref;source_path;equation_ref;valid_for_claim",
            "acceptance_rule": "same boundary domain and Hamiltonian Pi_M projector owned, or finite sourced commutator value",
            "current_fill": "MISSING_PROJECTOR_BOUNDARY_COMMUTATOR",
            "blocks": "Delta_symp_boundary;Hamiltonian integrability",
            "valid_for_claim": "false",
        },
        {
            "input_id": "SBI996_4_Delta_symp_boundary",
            "target": "Delta_symp_boundary_over_MH",
            "required_columns": "system_id;surface_pair;Delta_symp_boundary;Theta_rule;B_ref_rule;projector_rule;M_H_ref;source_path;equation_ref;valid_for_claim",
            "acceptance_rule": "theta/B_ref/projector boundary terms all theorem-zero or numeric, sourced, same-frame",
            "current_fill": "MISSING_SYMPLECTIC_BOUNDARY_VALUE",
            "blocks": "RC994_0;DeltaH curl",
            "valid_for_claim": "false",
        },
        {
            "input_id": "SBI996_5_RC9940_total_abs",
            "target": "RC994_0_reference_boundary_over_MH",
            "required_columns": "SBI996_0 through SBI996_4 valid, numeric/theorem-zero, same-frame, no MISSING markers",
            "acceptance_rule": "sum absolute component bounds; no cancellation allowed",
            "current_fill": "MISSING_COMPONENT_VALUES",
            "blocks": "deltaH curl bound; local-GR reduction",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG996_0_relative_boundary_owner",
            "claim": "relative boundary class is parent-owned and trivial",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "C_top selector, exact primitive, nohair, proper-charge guard, and same-domain projector remain unsigned",
        },
        {
            "gate_id": "CG996_1_Bref_superselection",
            "claim": "B_ref derivative vector vanishes",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "B_ref rule is named by the ansatz but not parent-derived",
        },
        {
            "gate_id": "CG996_2_RC9940_source_bound",
            "claim": "RC994_0 has a source-backed bound",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "source-bound input pack is schema-only and contains MISSING rows",
        },
        {
            "gate_id": "CG996_3_downstream_local_GR",
            "claim": "deltaH, FB554_0, Newton, PPN, R10, R11, orbital, or local-GR pass",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "996 only resolves the exact ownership contract and first bound inputs for RC994_0; no source-current equality is supplied",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC996_0_derivation_attempt",
            "decision": "do not promote relative boundary class or B_ref owner theorem",
            "reason": "the scaffold exists but the parent action does not uniquely select C_top/B_ref/nohair/projector silence",
            "effect": "RC994_0 remains a retained residual",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC996_1_contract_gain",
            "decision": "keep the exact parent-action contract as the future proof target",
            "reason": "RBO996_0 through RBO996_6 specify the precise conditions under which Stokes/cohomology would honestly close the boundary route",
            "effect": "future derivation can sign clauses rather than debate wording",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC996_2_source_pack",
            "decision": "stage source-backed RC994_0 input pack",
            "reason": "if the proof remains unsigned, the only honest alternative is componentwise sourced bounds",
            "effect": "997 can target the first missing component instead of reopening the whole boundary stack",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "997-Y5-R10-Bref-derivative-vector-theorem-or-Delta-ref-source-row.md",
            "objective": "either derive the B_ref derivative-vector zero theorem, or fill the first source-backed Delta_ref_over_MH row",
            "include": "partial_source/r/t/frame/lambda Delta_ref, B_ref parent rule, same-frame M_H_ref, equation/source path, no-cancellation guard",
            "exclude": "RC994_0 pass, FB554_0 pass, Newton/PPN/R10/local-GR pass, orbital GM substitution, hidden EH import, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
        }
    ]


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    start_timestamp = SCRIPT_START_UTC.timestamp()
    for dirpath, _, filenames in os.walk(FORMALIZATION):
        for filename in filenames:
            path = Path(dirpath) / filename
            try:
                if path.stat().st_mtime > start_timestamp:
                    count += 1
            except OSError:
                count += 1
    return count


def validation_rows(
    sources: list[dict[str, str]],
    owner_attempt: list[dict[str, str]],
    bref_tests: list[dict[str, str]],
    stack_bridge: list[dict[str, str]],
    source_pack: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    owner_ok = (
        len(owner_attempt) >= 8
        and any(row["owner_id"] == "RBO996_7_verdict" and row["owner_status"] == "failed_current_claim" for row in owner_attempt)
        and all(row["accepted_for_claim"] == "false" and row["valid_for_claim"] == "false" for row in owner_attempt)
    )
    bref_ok = (
        len(bref_tests) >= 6
        and any(row["test_id"] == "BST996_5_Bref_vector_verdict" and row["status"] == "fail_current_claim" for row in bref_tests)
        and all(row["valid_for_claim"] == "false" and "MISSING" in row["current_value"] for row in bref_tests)
    )
    stack_ok = all(row["valid_for_claim"] == "false" and row["current_status"] for row in stack_bridge)
    pack_ok = (
        len(source_pack) >= 6
        and all(row["valid_for_claim"] == "false" for row in source_pack)
        and all("MISSING" in row["current_fill"] for row in source_pack)
        and any(row["input_id"] == "SBI996_5_RC9940_total_abs" and "sum absolute" in row["acceptance_rule"] for row in source_pack)
    )
    claims_ok = all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claims)
    decisions_ok = any(row["decision_id"] == "DEC996_2_source_pack" for row in decisions)
    next_ok = bool(next_target) and next_target[0]["valid_for_claim"] == "false"
    formalization_count = formalization_changed_after_start()
    checks = [
        {"check_id": "V996_0_sources", "result": "pass" if sources_ok else "fail", "detail": "all cited local source files exist and expected needles are found"},
        {"check_id": "V996_1_owner_attempt_fail_closed", "result": "pass" if owner_ok else "fail", "detail": "relative boundary/B_ref owner theorem is attempted but not promoted"},
        {"check_id": "V996_2_Bref_derivative_vector_blocked", "result": "pass" if bref_ok else "fail", "detail": "B_ref derivative vector remains MISSING and nonclaim"},
        {"check_id": "V996_3_silence_stack_bridge_nonclaim", "result": "pass" if stack_ok else "fail", "detail": "exactness/nohair/projector stack is mapped but unsigned"},
        {"check_id": "V996_4_source_pack_fail_closed", "result": "pass" if pack_ok else "fail", "detail": "RC994_0 input pack is source-ready but MISSING and valid_for_claim=false"},
        {"check_id": "V996_5_claim_gates_safe", "result": "pass" if claims_ok else "fail", "detail": "relative class, B_ref, RC994_0, and local-GR claims are blocked"},
        {"check_id": "V996_6_decision_written", "result": "pass" if decisions_ok else "fail", "detail": "source-pack decision is recorded"},
        {"check_id": "V996_7_next_target_written", "result": "pass" if next_ok else "fail", "detail": "997 target row is present and nonclaim"},
        {"check_id": "V996_8_formalization_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization-workbench modified-file count since script start is {formalization_count}"},
    ]
    ready = all(row["result"] == "pass" for row in checks)
    return [
        {**row, "generated_utc": stamp()}
        for row in checks
    ] + [
        {
            "check_id": "V996_READY",
            "result": "pass" if ready else "fail",
            "detail": "996 relative boundary/B_ref owner gate validation summary",
            "generated_utc": stamp(),
        }
    ]


def write_doc(
    sources: list[dict[str, str]],
    owner_attempt: list[dict[str, str]],
    bref_tests: list[dict[str, str]],
    stack_bridge: list[dict[str, str]],
    source_pack: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> None:
    lines = [
        "# 996 Y5 R10: Relative Boundary Class Owner or B_ref Source Bound Pack",
        "",
        "Status: `Y5_R10_996_relative_boundary_Bref_owner_theorem_failed_contract_locked_RC9940_source_pack_staged_nonclaim`",
        "",
        "Claim ceiling: no parent-owned relative boundary class, no `B_ref` superselection, no `RC994_0=0`, no source-backed `RC994_0` bound, no `deltaH` curl closure, no `FB554_0=0`, no Newton/PPN/R10/R11/orbit/local-GR pass.",
        "",
        "## Readout",
        "",
        "996 tries the proper derivation route again, but not in a loop. The useful result is a sharper contract: a future parent action must select `C_top`, `B_ref`, the exact/proper boundary sector, the no-hair boundary Euler condition, the same-domain projector, and the `B_ref` derivative vector before readout.",
        "",
        "That contract is not signed by the current corpus. So the path does not close, but the fog is thinner: the next useful move is the first component row, `Delta_ref_over_MH`, unless a new parent action input can actually sign `B_ref`.",
        "",
        "## Source Register",
        "",
        md_table(sources, ["source_id", "role", "exists", "needle_found", "path"]),
        "",
        "## Relative Boundary Owner Attempt",
        "",
        md_table(owner_attempt, ["owner_id", "candidate_owner", "mathematical_contract", "what_it_would_prove", "current_evidence", "missing_signature", "owner_status", "accepted_for_claim", "valid_for_claim"]),
        "",
        "## B_ref Superselection Derivative Test",
        "",
        md_table(bref_tests, ["test_id", "derivative_test", "needed_zero", "current_value", "failure_mode", "source_requirement", "status", "valid_for_claim"]),
        "",
        "## Silence Stack Bridge",
        "",
        md_table(stack_bridge, ["stack_id", "borrowed_clause", "applies_to_RC9940", "needed_for", "current_status", "nonclaim_reason", "valid_for_claim"]),
        "",
        "## RC994_0 Source-Bound Input Pack",
        "",
        md_table(source_pack, ["input_id", "target", "required_columns", "acceptance_rule", "current_fill", "blocks", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        md_table(claims, ["gate_id", "claim", "gate_pass", "claim_allowed", "why_not"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decisions, ["decision_id", "decision", "reason", "effect", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(validation, ["check_id", "result", "detail", "generated_utc"]),
        "",
        "## Next Target",
        "",
        md_table(next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register()
    owner_attempt = relative_boundary_owner_attempt_rows()
    bref_tests = bref_superselection_test_rows()
    stack_bridge = silence_stack_bridge_rows()
    source_pack = source_bound_input_pack_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, owner_attempt, bref_tests, stack_bridge, source_pack, claims, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_996_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_996_RELATIVE_BOUNDARY_OWNER_ATTEMPT.csv", owner_attempt)
    write_csv(OUT / "P8_Y5_R10_996_BREF_SUPERSELECTION_DERIVATIVE_TEST.csv", bref_tests)
    write_csv(OUT / "P8_Y5_R10_996_SILENCE_STACK_BRIDGE.csv", stack_bridge)
    write_csv(OUT / "P8_Y5_R10_996_RC9940_SOURCE_BOUND_INPUT_PACK.csv", source_pack)
    write_csv(OUT / "P8_Y5_R10_996_CLAIM_GATE.csv", claims)
    write_csv(OUT / "P8_Y5_R10_996_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_996_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_996_VALIDATION.csv", validation)
    write_doc(sources, owner_attempt, bref_tests, stack_bridge, source_pack, claims, decisions, validation, next_target)


if __name__ == "__main__":
    main()
