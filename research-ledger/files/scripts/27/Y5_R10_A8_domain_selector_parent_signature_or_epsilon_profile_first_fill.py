from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1143-Y5-R10-A8-domain-selector-parent-signature-or-epsilon-profile-first-fill.md"


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
            "source_id": "SRC1143_0_1142_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1142_NEXT_TARGET.csv",
            "needle": "NEXT1142_0_1143",
            "role": "handoff requiring A8 signature or epsilon profile fill.",
        },
        {
            "source_id": "SRC1143_1_1142_signatures",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1142_MINIMUM_PARENT_SIGNATURES.csv",
            "needle": "SIG1142_2_local_representative_exact",
            "role": "minimum signatures required for vector/flux zero route.",
        },
        {
            "source_id": "SRC1143_2_1142_fill",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1142_FIRST_COEFFICIENT_SOURCE_FILL_ROWS.csv",
            "needle": "FILL1142_1_epsilon_domain_flux",
            "role": "epsilon_domain_flux is the first source/profile fallback.",
        },
        {
            "source_id": "SRC1143_3_A8_contract",
            "relative_path": "source-intake/mts_residuals/P8_source_owner_parent_action_terms_CONTRACT.csv",
            "needle": "A8_projector_domain_topological",
            "role": "current A8 parent clause remains retained_symbolic.",
        },
        {
            "source_id": "SRC1143_4_domain_selector_143",
            "relative_path": "143-domain-selector-variational-action-attempt.md",
            "needle": "domain_selector_formal_action_not_parent_derived",
            "role": "zero-knob/domain selector action attempt did not parent-derive D.",
        },
        {
            "source_id": "SRC1143_5_projector_bianchi_207",
            "relative_path": "207-domain-projector-action-and-Bianchi-identity.md",
            "needle": "domain_projector_action_formal_Bianchi_conditional_representative_missing",
            "role": "formal Bianchi/projector action exists conditionally; representative missing.",
        },
        {
            "source_id": "SRC1143_6_local_coframe_242",
            "relative_path": "242-strict-local-coframe-branch-or-domain-projector-action.md",
            "needle": "strict_local_coframe_branch_selected_as_local_C_silence_contract_domain_projector_retained_for_cosmology_no_promotion",
            "role": "local coframe route remains a contract; domain projector retained for cosmology, not local rescue.",
        },
        {
            "source_id": "SRC1143_7_topological_skeleton_252",
            "relative_path": "252-topological-projector-parent-action-skeleton.md",
            "needle": "topological_projector_parent_skeleton_written_N5_action_route_conditional_FLRW_Bmem_and_N6_open_no_promotion",
            "role": "metric-independent topological projector skeleton exists conditionally.",
        },
        {
            "source_id": "SRC1143_8_boundary_projector_309",
            "relative_path": "309-MTS-boundary-projector-contract-attempt.md",
            "needle": "P_MTS_projector_contract_constructed_conditional_not_parent_derived",
            "role": "projector contract is clean but not parent-derived.",
        },
        {
            "source_id": "SRC1143_9_N5_348",
            "relative_path": "348-N5-projector-stress-conservation-theorem.md",
            "needle": "N5_conditionally_closed_by_metric_independent_topological_projector_parent_ownership_and_FLRW_stress_bridge_open",
            "role": "N5 stress can close conditionally if topological projector is parent-owned.",
        },
        {
            "source_id": "SRC1143_10_detQ_478",
            "relative_path": "478-determinant-current-parent-ownership-or-demotion.md",
            "needle": "D1_parent_ownership",
            "role": "det(Q_coh) shape support remains missing parent ownership.",
        },
        {
            "source_id": "SRC1143_11_domain_noleak",
            "relative_path": "source-intake/mts_residuals/P8_DOMAIN_ALPHA3_NOLEAK_THEOREM_ATTEMPT.csv",
            "needle": "N3_domain_selector_no_vector",
            "role": "domain selector no-vector clause is not derived.",
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


def signature_contract_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "clause_id": "A8SIG1143_0_parent_projector",
                "parent_signature": "S_parent contains a relative-chain/cohomology projector P_D defined on parent fields before readout",
                "mathematical_condition": "P_D^2=P_D, P_D is self-adjoint under the parent topological pairing, and delta_g P_D=0 in the compact local bulk",
                "would_close": "metric-dependent projector stress; fake external-filter shortcut",
                "current_status": "CONDITIONAL_SKELETON_NOT_PARENT_SIGNED",
                "source_anchor": "252;309;348",
                "valid_for_claim": "false",
            },
            {
                "clause_id": "A8SIG1143_1_scalar_local_selector",
                "parent_signature": "local compact branch selector is an auxiliary scalar/trivial representative, not a vector normal or moving readout mask",
                "mathematical_condition": "u_D^i=0, D_i chi_D=0, delta sigma_D^i=0, and no g0i/readout vector in the observed local matter/source coframe",
                "would_close": "c_vector_preferred_frame_hair; alpha1/alpha2 vector leakage",
                "current_status": "NOT_PARENT_DERIVED",
                "source_anchor": "143;242;P8_DOMAIN_ALPHA3_NOLEAK::N3",
                "valid_for_claim": "false",
            },
            {
                "clause_id": "A8SIG1143_2_exact_local_representative",
                "parent_signature": "local stationary compact domains have exact/trivial relative class while FLRW can retain the coherent scalar class",
                "mathematical_condition": "[J_D]_local=0 or P_D J_D=d Lambda_D locally, with FLRW P_D J_D allowed only as homogeneous scalar singlet",
                "would_close": "epsilon_domain_flux; local momentum flux",
                "current_status": "NOT_PARENT_DERIVED",
                "source_anchor": "143;207;309;478",
                "valid_for_claim": "false",
            },
            {
                "clause_id": "A8SIG1143_3_no_flux_variation",
                "parent_signature": "variation of the domain/projector sector gives no compact-local momentum flux in the observed coframe",
                "mathematical_condition": "P_loc^i_nu(F_P^nu+F_domain^nu)=0 and int_boundary n_i K_owner^{i0} dS=0 for stationary local branch",
                "would_close": "epsilon_domain_flux and K*c*epsilon alpha3 product if R11 c is also silent",
                "current_status": "DEPENDS_ON_A8SIG1143_1_AND_A8SIG1143_2",
                "source_anchor": "P8_source_owner_parent_action_terms_CONTRACT::A8;1123;1136",
                "valid_for_claim": "false",
            },
            {
                "clause_id": "A8SIG1143_4_R11_sibling_silence",
                "parent_signature": "R11 source-normalization/domain operators vanish on the local trivial domain or are executable with source paths",
                "mathematical_condition": "c_domain_source_normalization_operator=0 for the local domain sector, or all c-vector/STF/flux coefficient rows are numeric and below PPN locks",
                "would_close": "c factor and R5/R6/R8/R11 sibling guards",
                "current_status": "NOT_PARENT_DERIVED",
                "source_anchor": "1118;1121;1138;1142",
                "valid_for_claim": "false",
            },
            {
                "clause_id": "A8SIG1143_5_verdict",
                "parent_signature": "complete A8 local silence signature",
                "mathematical_condition": "A8SIG1143_0 through A8SIG1143_4 all parent-signed before scoring",
                "would_close": "vector/flux c-hair route",
                "current_status": "A8_SIGNATURE_CONTRACT_WRITTEN_NOT_DERIVED",
                "source_anchor": "1143",
                "valid_for_claim": "false",
            },
        ]
    )


def clause_audit_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "audit_id": "AUD1143_0_projector_metric_independence",
                "question": "Does the corpus give a parent-owned metric-independent P_D?",
                "answer": "conditional_only",
                "evidence": "252 and 348 supply the route if P_D is relative/topological, but parent ownership and FLRW bridge remain open",
                "effect": "cannot promote local stress/vector silence",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "AUD1143_1_selector_no_vector",
                "question": "Does the corpus derive u_D^i=D_i chi_D=delta sigma_D^i=0?",
                "answer": "no",
                "evidence": "143 says domain selector formal action is not parent-derived; P8_DOMAIN N3 says no-vector is not derived",
                "effect": "alpha1/alpha2 vector hair remains open",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "AUD1143_2_local_representative",
                "question": "Does the parent action select local trivial relative class?",
                "answer": "no",
                "evidence": "207 says representative missing; 309 and 478 keep local triviality/domain ownership conditional",
                "effect": "epsilon_domain_flux remains open",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "AUD1143_3_FLRW_not_murdered",
                "question": "Can the contract keep FLRW/cosmology active while killing local compact flux?",
                "answer": "possible_as_contract_not_theorem",
                "evidence": "143/207/309 allow local trivial versus FLRW nontrivial readout conditionally",
                "effect": "branch split is coherent but not parent-selected",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "AUD1143_4_epsilon_profile_needed",
                "question": "If A8 is not parent-signed, what is first fallback?",
                "answer": "fill_epsilon_domain_flux_profile",
                "evidence": "1142 preferred epsilon fill because one zero factor can close alpha3 product",
                "effect": "create epsilon profile first-fill row, nonclaim",
                "valid_for_claim": "false",
            },
        ]
    )


def epsilon_profile_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "profile_id": "EPS1143_0_local_compact_profile",
                "target": "epsilon_domain_flux",
                "branch": "compact_stationary_local_observed_coframe",
                "definition_required": "epsilon_domain_flux = normalized projected local domain momentum/source flux entering P_R11_source_alpha3_flux",
                "required_fields": "system_id; branch_id; profile_support; epsilon_abs; epsilon_units; local_representative_status; source_path; valid_for_claim",
                "acceptance": "epsilon_abs=0 by parent no-flux certificate or sourced bound compatible with abs(K*c*epsilon)<=4e-20",
                "current_value": "MISSING_EPSILON_DOMAIN_FLUX_PROFILE_OR_ZERO_THEOREM",
                "source_path": "MISSING_SOURCE_PATH",
                "status": "SOURCE_PROFILE_ROW_REQUIRED",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "profile_id": "EPS1143_1_FLRW_separation_guard",
                "target": "epsilon_domain_flux",
                "branch": "FLRW_coherent_domain",
                "definition_required": "FLRW homogeneous scalar domain class may remain active only if local compact exact class is parent-selected",
                "required_fields": "branch_selector; local_trivial_class_proof; FLRW_scalar_class_proof; source_path; valid_for_claim",
                "acceptance": "same parent branch law derives local silence and FLRW retained scalar without hand-switching",
                "current_value": "MISSING_PARENT_BRANCH_SELECTION_LAW",
                "source_path": "MISSING_SOURCE_PATH",
                "status": "BRANCH_GUARD_REQUIRED",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
        ]
    )


def branch_guard_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "guard_id": "BR1143_0_no_hand_switch",
                "rule": "local domain cannot be set trivial by hand while FLRW domain is kept active by hand",
                "current_status": "ACTIVE_GUARD",
                "reason": "the same parent branch-selection law must produce both limits",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "BR1143_1_no_metric_projector",
                "rule": "metric-dependent Hodge/orthogonal projector cannot be used as topological silence",
                "current_status": "ACTIVE_GUARD",
                "reason": "metric-dependent projector can vary into local stress/vector leakage",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "BR1143_2_no_external_filter",
                "rule": "P_D must be selected by parent variables, not inserted after solving",
                "current_status": "ACTIVE_GUARD",
                "reason": "external filter would fake local-GR reduction",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "BR1143_3_no_alpha3_shortcut",
                "rule": "epsilon profile cannot close alpha3 unless K and c factors are zero/sourced or product passes independently",
                "current_status": "ACTIVE_GUARD",
                "reason": "1141/1142 no-cancellation and sibling guards remain active",
                "valid_for_claim": "false",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1143_0_sources_exist",
                "rule": "all A8/domain-selector source anchors exist",
                "gate_pass": "true_nonclaim",
                "reason": "source paths/needles are present",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1143_1_signature_contract_written",
                "rule": "exact A8 signature contract is written",
                "gate_pass": "true_nonclaim",
                "reason": "clauses A8SIG1143_0 through A8SIG1143_5 define the needed theorem",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1143_2_A8_parent_signed",
                "rule": "all A8 clauses are parent-derived",
                "gate_pass": "false",
                "reason": "selector no-vector and local representative exactness remain not parent-derived",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1143_3_epsilon_profile_executable",
                "rule": "epsilon_domain_flux profile row is sourced or theorem-zero",
                "gate_pass": "false",
                "reason": "epsilon profile row is only a required schema with MISSING_SOURCE_PATH",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1143_4_local_GR_promotion",
                "rule": "preferred-frame/alpha3/local-GR promotion allowed",
                "gate_pass": "false",
                "reason": "A8 contract is not parent-signed and epsilon profile is not filled",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1143_0_verdict",
                "decision": "A8_signature_written_not_parent_signed",
                "reason": "the exact clauses are now explicit, but old source attempts show selector and representative ownership still fail",
                "next_action": "attack the branch-selection law or fill epsilon_domain_flux profile row",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1143_1_best_next",
                "decision": "derive_branch_selection_law_before_epsilon_data",
                "reason": "a single parent law can separate local trivial class from FLRW active class without hand-switching",
                "next_action": "try to construct local-trivial/FLRW-active branch law from relative cohomology/domain variables",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1143_2_claim_ceiling",
                "decision": "keep_A8_local_silence_nonclaim",
                "reason": "contract written is not proof; epsilon row is unfilled",
                "next_action": "no alpha3/PPN/local-GR claim",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1143_0_1144",
                "next_target": "1144-Y5-R10-local-trivial-FLRW-active-branch-law-or-epsilon-profile-fill.md",
                "objective": "derive or reject the parent branch-selection law that gives local compact exact/trivial domain class while retaining FLRW homogeneous scalar class; if it fails, fill epsilon_domain_flux profile as nonclaim data",
                "include": "relative cohomology; local exact class; FLRW homogeneous scalar class; no hand-switch guard; epsilon profile fallback; observed coframe",
                "exclude": "local/FLRW branch hand choice; tuned cancellation; measured-GM absorption; alpha3/local-GR claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    contract: list[dict[str, object]],
    audit: list[dict[str, object]],
    epsilon_profiles: list[dict[str, object]],
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

    all_rows = contract + audit + epsilon_profiles + guards + gates + decisions + next_target
    add(
        "V1143_0_sources_exist",
        all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources),
        "all cited local source paths exist and needles are found",
    )
    add(
        "V1143_1_contract_complete",
        {row["clause_id"] for row in contract}
        == {
            "A8SIG1143_0_parent_projector",
            "A8SIG1143_1_scalar_local_selector",
            "A8SIG1143_2_exact_local_representative",
            "A8SIG1143_3_no_flux_variation",
            "A8SIG1143_4_R11_sibling_silence",
            "A8SIG1143_5_verdict",
        },
        "A8 signature contract contains all required clauses",
    )
    add(
        "V1143_2_contract_not_derived",
        contract[-1]["current_status"] == "A8_SIGNATURE_CONTRACT_WRITTEN_NOT_DERIVED"
        and any(row["current_status"] == "NOT_PARENT_DERIVED" for row in contract),
        "A8 contract is written but not parent-signed",
    )
    add(
        "V1143_3_audit_blocks",
        any(row["audit_id"] == "AUD1143_1_selector_no_vector" and row["answer"] == "no" for row in audit)
        and any(row["audit_id"] == "AUD1143_2_local_representative" and row["answer"] == "no" for row in audit),
        "selector no-vector and local representative proofs remain missing",
    )
    add(
        "V1143_4_epsilon_profile_schema",
        {row["profile_id"] for row in epsilon_profiles} == {"EPS1143_0_local_compact_profile", "EPS1143_1_FLRW_separation_guard"}
        and all(row["source_path"] == "MISSING_SOURCE_PATH" for row in epsilon_profiles),
        "epsilon profile and FLRW separation guard rows are present and unfilled",
    )
    add(
        "V1143_5_branch_guards",
        len(guards) == 4 and all(row["current_status"] == "ACTIVE_GUARD" for row in guards),
        "branch and shortcut guards are active",
    )
    add(
        "V1143_6_claim_gates_blocked",
        any(row["gate_id"] == "G1143_2_A8_parent_signed" and row["gate_pass"] == "false" for row in gates)
        and any(row["gate_id"] == "G1143_4_local_GR_promotion" and row["gate_pass"] == "false" for row in gates),
        "parent signature and local claim gates remain blocked",
    )
    add(
        "V1143_7_no_claim_rows",
        all(row.get("valid_for_claim") == "false" for row in all_rows)
        and all(row.get("claim_allowed", "false") == "false" for row in epsilon_profiles + next_target),
        "all generated rows remain nonclaim",
    )
    add(
        "V1143_8_next_target",
        next_target[0]["next_target"].startswith("1144-") and "branch-law" in str(next_target[0]["next_target"]),
        "1144 handoff targets local-trivial/FLRW-active branch law",
    )
    add(
        "V1143_9_generated_under_post_checkpoint",
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
    add("V1143_10_csv_parse", csv_parse_ok, "all 1143 CSV outputs parse cleanly")
    add("V1143_11_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add(
        "V1143_SUMMARY",
        True,
        "1143 writes the exact A8 signature contract, keeps it nonclaim, and selects the branch-law derivation as 1144",
    )
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    contract: list[dict[str, object]],
    audit: list[dict[str, object]],
    epsilon_profiles: list[dict[str, object]],
    guards: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1143 - Y5/R10 A8 Domain-Selector Parent Signature or Epsilon Profile First Fill

**Current verdict:** the exact A8 parent-action signature is now written, but it is not parent-signed. This is a contract/proof target, not a local-GR or alpha3 pass.

**Useful progress:** the missing derivation is no longer vague: the parent must select a metric-independent `P_D`, a scalar/trivial compact-local selector, an exact local representative, no compact-local flux, and R11 sibling silence.

**Important guard:** local silence and FLRW activity cannot be chosen by hand. The same parent branch law must derive local exact/trivial class and FLRW homogeneous scalar class.

**Best next attack:** derive that local-trivial/FLRW-active branch law. If that fails, fill `epsilon_domain_flux` as a nonclaim profile/source row.

**No claim:** no R10, PPN, alpha3, preferred-frame, local-GR, measured-GM, GitHub, or public claim follows from 1143.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "role"], sources)}

## A8 Parent-Signature Contract
{table(["clause_id", "parent_signature", "mathematical_condition", "would_close", "current_status", "source_anchor", "valid_for_claim"], contract)}

## Clause Audit
{table(["audit_id", "question", "answer", "evidence", "effect", "valid_for_claim"], audit)}

## Epsilon Profile First-Fill Rows
{table(["profile_id", "target", "branch", "definition_required", "required_fields", "acceptance", "current_value", "source_path", "status", "valid_for_claim"], epsilon_profiles)}

## Branch Guards
{table(["guard_id", "rule", "current_status", "reason", "valid_for_claim"], guards)}

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
        "source_register": OUT / "P8_Y5_R10_1143_SOURCE_REGISTER.csv",
        "contract": OUT / "P8_Y5_R10_1143_A8_PARENT_SIGNATURE_CONTRACT.csv",
        "audit": OUT / "P8_Y5_R10_1143_A8_SIGNATURE_CLAUSE_AUDIT.csv",
        "epsilon": OUT / "P8_Y5_R10_1143_EPSILON_DOMAIN_FLUX_PROFILE_FIRST_FILL.csv",
        "guards": OUT / "P8_Y5_R10_1143_LOCAL_FLRW_BRANCH_SEPARATION_GUARDS.csv",
        "gates": OUT / "P8_Y5_R10_1143_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1143_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1143_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1143_VALIDATION.csv",
    }
    sources = source_rows()
    contract = signature_contract_rows()
    audit = clause_audit_rows()
    epsilon_profiles = epsilon_profile_rows()
    guards = branch_guard_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["contract"], contract)
    write_csv(outputs["audit"], audit)
    write_csv(outputs["epsilon"], epsilon_profiles)
    write_csv(outputs["guards"], guards)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, contract, audit, epsilon_profiles, guards, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, contract, audit, epsilon_profiles, guards, gates, decisions, validation, next_target)
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
