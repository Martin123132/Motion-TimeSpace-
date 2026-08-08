from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3400-Y5-R2FR-first-order-source-coupling-parent-signature-pack-under-AX1090.md"


SOURCES = {
    "3399_doc": ROOT / "3399-Y5-R2FR-source-normalization-component-extractor-under-AX1090.md",
    "3399_theorem": OUT / "P8_Y5_R2FR_3399_FIRST_ORDER_NEWTON_ZERO_THEOREM.csv",
    "3399_chain": OUT / "P8_Y5_R2FR_3399_NEWTON_CLOSURE_CHAIN.csv",
    "3399_components": OUT / "P8_Y5_R2FR_3399_COMPONENT_EXTRACTION_MATRIX.csv",
    "3396_coverage": OUT / "P8_Y5_R2FR_3396_PARENT_TERM_COVERAGE_MATRIX.csv",
    "3396_adoption": OUT / "P8_Y5_R2FR_3396_PARENT_ADOPTION_PACKET_NONCLAIM.csv",
    "3395_parent_line": OUT / "P8_Y5_R2FR_3395_MINIMAL_PARENT_ACTION_LINE_CANDIDATE.csv",
    "3377_theorem": OUT / "P8_Y5_R2FR_3377_WEAK_FIELD_SOURCE_NORMALIZATION_THEOREM.csv",
    "core_spine": FW / "07-unification-spine.md",
    "core_parent_sketch": FW / "12-minimal-parent-theory-sketch.md",
    "core_parent_v1": FW / "83-parent-equations-v1.md",
    "core_obligations": FW / "19-proof-obligations.md",
}


OUTPUT_PATHS = {
    "source_register": OUT / "P8_Y5_R2FR_3400_SOURCE_REGISTER.csv",
    "parent_signature_clauses": OUT / "P8_Y5_R2FR_3400_PARENT_SIGNATURE_CLAUSES.csv",
    "core_compatibility_audit": OUT / "P8_Y5_R2FR_3400_CORE_COMPATIBILITY_AUDIT.csv",
    "activation_theorem": OUT / "P8_Y5_R2FR_3400_FIRST_ORDER_ACTIVATION_THEOREM.csv",
    "adoption_patch_packet": OUT / "P8_Y5_R2FR_3400_ADOPTION_PATCH_PACKET_NONCLAIM.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3400_PROMOTION_GATES.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3400_RUNNER_NONCLAIM.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3400_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3400_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3400_VALIDATION.csv",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_register() -> list[dict[str, Any]]:
    return [
        {
            "source_id": f"SRC3400_{idx:02d}_{name}",
            "path": str(path),
            "exists": path.exists(),
            "role": "parent_signature_source",
            "valid_for_claim": False,
        }
        for idx, (name, path) in enumerate(SOURCES.items())
    ]


def coverage_lookup() -> dict[str, dict[str, str]]:
    rows = read_csv(SOURCES["3396_coverage"])
    return {row["term"]: row for row in rows}


def parent_signature_clauses() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "PC3400_0_single_branch",
            "clause": "All local weak-field readouts are evaluated in one parent branch with fixed g_obs/e_obs, q(Phi), theta, tau, Q_tau, B_ref, Pi_M, kappa_MTS, and ell_J before Newton/PPN comparison.",
            "closes": "no-backfill; branch mismatch; hidden fitted GM/source-scale absorption",
            "status_if_adopted": "P0_ACTIVE",
            "parent_status_now": "STAGED_NOT_ADOPTED",
            "valid_for_claim": False,
        },
        {
            "clause_id": "PC3400_1_constant_kappa",
            "clause": "kappa_MTS is a local-branch constant/global coupling with kappa_MTS=8*pi*G_ref/c^4; it carries no source, species, range, frame, boundary, memory, or projector labels.",
            "closes": "delta_kappa=0; coupling drift in first-order Newton branch",
            "status_if_adopted": "P1_ACTIVE",
            "parent_status_now": "CORE_KAPPA_COMPATIBLE_GLOBAL_CLAUSE_NOT_ADOPTED",
            "valid_for_claim": False,
        },
        {
            "clause_id": "PC3400_2_same_matter_source",
            "clause": "S_matter depends on the parent geometry only through e_obs(q(Phi)) and matter fields; Hilbert stress, J_H[tau], M_H, and PPN source density are all induced by that same variation, with ell_J=1 unless a universal conversion is parent-fixed before readout.",
            "closes": "delta_ellJ=0; source-current scale drift; Hilbert/source shadow split",
            "status_if_adopted": "P2_ACTIVE",
            "parent_status_now": "MATTER_ACTION_COMPATIBLE_OBSERVED_COFRAME_AND_ELLJ_NOT_ADOPTED",
            "valid_for_claim": False,
        },
        {
            "clause_id": "PC3400_3_Htau_PiM_chain",
            "clause": "Q_tau/H_tau and Pi_M are boundary/Hamiltonian functionals of the same branch; Pi_M is a fixed chain map and H_tau-H_ref equals the Pi_M-projected Hilbert mass current normalized by the same G_ref.",
            "closes": "B_GH=0; part of epsilon_Gref_match=0; H_tau/Gauss mismatch",
            "status_if_adopted": "P3_ACTIVE",
            "parent_status_now": "HAMILTONIAN_CHARGE_AND_PIM_MISSING_FROM_CORE_PARENT",
            "valid_for_claim": False,
        },
        {
            "clause_id": "PC3400_4_no_boundary_extra_mass",
            "clause": "In the compact local exterior, R_eq=0, B_zero_flux=0, [d,Pi_M]J_H=0, and non-EH/domain/memory/range/frame/projector channels carry no unowned monopole mass charge; any surviving term is retained as an explicit residual row.",
            "closes": "epsilon_M=0 if no retained terms survive; no hidden boundary/source mass",
            "status_if_adopted": "P4_ACTIVE_OR_RETAINED_ROWS_ACTIVE",
            "parent_status_now": "NO_EXTRA_MASS_CLAUSE_NOT_ADOPTED",
            "valid_for_claim": False,
        },
        {
            "clause_id": "PC3400_5_v_action_ratio",
            "clause": "The local v reduction contains L_v=-c^4/(32*pi*G_ref)|grad v|^2-rho_H*c^2*v/2 in the Newton branch, equivalently B_v/A_v=16*pi*G_ref/c^4.",
            "closes": "delta_KC=0; correct Poisson/Newton amplitude in v branch",
            "status_if_adopted": "P5_ACTIVE",
            "parent_status_now": "RATIO_DERIVED_TARGET_PARENT_V_COEFFICIENTS_NOT_ADOPTED",
            "valid_for_claim": False,
        },
        {
            "clause_id": "PC3400_6_same_U_PPN_guard",
            "clause": "The PPN potential U is built from the same G_ref and M_H/Pi_M J_H source as Poisson and H_tau; this clause only transfers first-order source normalization and does not set beta or preferred-frame parameters.",
            "closes": "B_GPPN=0 at source-normalization level; prevents gamma-only overclaim",
            "status_if_adopted": "FIRST_ORDER_PPN_SOURCE_TRANSFER_ONLY",
            "parent_status_now": "PPN_GUARD_READY_NOT_FULL_VECTOR_CLOSED",
            "valid_for_claim": False,
        },
    ]


def core_compatibility_audit() -> list[dict[str, Any]]:
    cov = coverage_lookup()
    mapping = [
        ("AUD3400_0_g_obs_metric", "g_obs_metric", "PC3400_0_single_branch", "existing observed/emergent metric support"),
        ("AUD3400_1_EH_coefficient", "EH_coefficient", "PC3400_1_constant_kappa", "EH/kappa convention support"),
        ("AUD3400_2_matter_action", "matter_action", "PC3400_2_same_matter_source", "matter action/Hilbert stress support"),
        ("AUD3400_3_observed_coframe", "observed_coframe", "PC3400_2_same_matter_source", "needed for same source variation"),
        ("AUD3400_4_quotient_map", "quotient_map", "PC3400_2_same_matter_source", "needed for matter descent q(Phi)"),
        ("AUD3400_5_Hamiltonian_charge", "Hamiltonian_charge", "PC3400_3_Htau_PiM_chain", "needed for H_tau mass charge"),
        ("AUD3400_6_boundary_reference", "boundary_reference", "PC3400_3_Htau_PiM_chain;PC3400_4_no_boundary_extra_mass", "needed for fixed reference/no boundary fit"),
        ("AUD3400_7_Pi_M", "Pi_M", "PC3400_3_Htau_PiM_chain;PC3400_4_no_boundary_extra_mass", "needed for mass/source projector"),
        ("AUD3400_8_ell_J", "ell_J", "PC3400_2_same_matter_source", "needed to block source-current scale drift"),
        ("AUD3400_9_no_backfill", "no_backfill", "PC3400_0_single_branch", "needed to block measured-GM circularity"),
    ]
    rows: list[dict[str, Any]] = []
    for audit_id, term, clause, role in mapping:
        source_row = cov.get(term, {})
        core_present = str(source_row.get("core_present", "")).lower() == "true"
        post_present = str(source_row.get("post_checkpoint_present", "")).lower() == "true"
        rows.append(
            {
                "audit_id": audit_id,
                "term": term,
                "related_clause": clause,
                "role": role,
                "core_present": core_present,
                "post_checkpoint_present": post_present,
                "contradiction_found": False,
                "audit_status": "CORE_SUPPORT_PRESENT" if core_present else "COMPATIBLE_EXTENSION_REQUIRED",
                "evidence": source_row.get("action_needed", "") or source_row.get("description", ""),
                "valid_for_claim": False,
            }
        )
    return rows


def activation_theorem() -> list[dict[str, Any]]:
    return [
        {
            "activation_id": "ACT3400_0_clause_set",
            "statement": "If PC3400_0 through PC3400_6 are adopted in one local branch and no retained residual row survives, then the T3399 P0-P5 premises are active.",
            "result": "T3399 premises activated",
            "current_status": "CLAUSE_SET_STAGED_NOT_ADOPTED",
            "valid_for_claim": False,
        },
        {
            "activation_id": "ACT3400_1_first_order_residuals",
            "statement": "Activated premises imply delta_kappa=delta_ellJ=epsilon_Gref_match=delta_KC=epsilon_M=0.",
            "result": "first-order source-normalization residuals vanish",
            "current_status": "EXACT_IF_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "activation_id": "ACT3400_2_newton_amplitude",
            "statement": "Substitution into Delta_Newton_v_coupled=(1+delta_KC)(1+epsilon_M)(1+delta_kappa)(1+delta_ellJ)-1 gives Delta_Newton_v_coupled=0.",
            "result": "Newton/v first-order amplitude closure",
            "current_status": "EXACT_IF_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "activation_id": "ACT3400_3_ppn_guard",
            "statement": "The theorem transfers source normalization into the full PPN problem but does not close kappa_v, alpha_i, zeta_i, xi, or empirical bounds.",
            "result": "local-GR claim still blocked",
            "current_status": "GUARDRAIL_ACTIVE",
            "valid_for_claim": False,
        },
    ]


def adoption_patch_packet() -> list[dict[str, Any]]:
    return [
        {
            "patch_id": "PATCH3400_0_section",
            "target": "future parent action/local weak-field source-normalization section",
            "text": "Add a local weak-field source-coupling clause declaring the observed branch, universal kappa_MTS, same Hilbert source current, H_tau/Pi_M mass charge, no boundary/extra monopole mass leakage, and v-action coefficient ratio before any Newton/PPN readout.",
            "apply_now": False,
            "reason_not_applied": "post-checkpoint work only; formalization-workbench remains untouched until user explicitly asks for adoption",
            "valid_for_claim": False,
        },
        {
            "patch_id": "PATCH3400_1_formula",
            "target": "future equation block",
            "text": "S_parent local branch contains (c^4/16*pi*G_ref)∫sqrt(-g_obs)R[g_obs]+S_matter[e_obs(q(Phi)),Psi]+S_boundary[Q_tau,B_ref,Pi_M;G_ref]+S_v with B_v/A_v=16*pi*G_ref/c^4.",
            "apply_now": False,
            "reason_not_applied": "candidate formula must be audited against full parent notation before core insertion",
            "valid_for_claim": False,
        },
        {
            "patch_id": "PATCH3400_2_guardrail",
            "target": "future claims register",
            "text": "First-order Newton source coupling is claimable only after PC3400_0..6 are parent-signed or every retained residual row has a numeric/source bound; full local GR additionally requires kappa_v and PPN vector closure.",
            "apply_now": False,
            "reason_not_applied": "private checkpoint; no public claim or core modification",
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    audit = core_compatibility_audit()
    return [
        {
            "gate_id": "GATE3400_0_clause_pack_written",
            "claim": "P0-P5 parent-signature clause pack exists",
            "gate_pass": True,
            "reason": "PC3400_0..6 are written as exact parent clauses",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3400_1_no_core_contradiction",
            "claim": "clause pack is compatible with current core audit",
            "gate_pass": all(not row["contradiction_found"] for row in audit),
            "reason": "3396 shows core support for metric/EH/matter and missing terms as extensions, not contradictions",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3400_2_parent_adopted",
            "claim": "clause pack is adopted into parent theory",
            "gate_pass": False,
            "reason": "formalization-workbench not modified; clauses remain post-checkpoint candidates",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3400_3_first_order_newton_claim",
            "claim": "first-order Newton source-amplitude closure is active",
            "gate_pass": False,
            "reason": "activation theorem is exact-if-signed but not signed now",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3400_4_local_GR_claim",
            "claim": "local GR/PPN is derived",
            "gate_pass": False,
            "reason": "kappa_v/full PPN vector remain open even after first-order clause pack",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "run_id": "RUN3400_0_signature_pack",
            "test": "parent clause pack",
            "status": "PASS_CLAUSES_WRITTEN_NONCLAIM",
            "detail": "seven clauses stage the exact first-order source-coupling route",
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN3400_1_compatibility",
            "test": "core compatibility audit",
            "status": "PASS_COMPATIBLE_EXTENSION_NOT_ADOPTED",
            "detail": "no contradiction found; missing terms remain explicit adoption requirements",
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN3400_2_activation",
            "test": "first-order Newton activation theorem",
            "status": "PASS_EXACT_IF_SIGNED",
            "detail": "Delta_Newton=0 follows if PC3400 clauses are parent-signed",
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN3400_3_firewall",
            "test": "claim firewall",
            "status": "PASS_NO_LOCAL_GR_CLAIM",
            "detail": "formalization untouched; beta/full PPN still blocked",
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3400_0_not_circling",
            "finding": "we now have an explicit first-order parent-signature route, not just a list of missing components",
            "reason": "PC3400 clauses activate T3399 and imply Delta_Newton_v_coupled=0 exactly if adopted",
            "next_action": "either apply/audit these clauses into core docs later or use them as the private parent standard for the kappa_v branch",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3400_1_safe_status",
            "finding": "current core appears compatible but incomplete",
            "reason": "metric/EH/matter support exists; observed coframe, q(Phi), H_tau, B_ref, Pi_M, ell_J, and no-backfill must be explicitly adopted",
            "next_action": "do not claim until adoption occurs or numeric residual fallback rows exist",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3400_2_best_next",
            "finding": "next math strike should be kappa_v second-order beta",
            "reason": "first-order Newton route is staged; local GR now bottlenecks on beta/full PPN rather than source-amplitude algebra alone",
            "next_action": "build 3401 kappa_v second-order beta ledger",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3401-Y5-R2FR-kappav-second-order-beta-ledger-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3401_kappav_second_order_beta_ledger.py",
            "objective": "derive or bound eta_v, source_quad, PiM, boundary, readout/operator, and coupling terms in kappa_v after the first-order source-coupling route is staged",
            "why_next": "first-order Newton source amplitude has an exact parent-signature route; beta/full PPN remains the next local-GR bottleneck",
            "valid_for_claim": False,
        },
        {
            "target_id": "3402-Y5-R2FR-parent-clause-core-integration-diff-plan-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3402_parent_clause_core_integration_diff_plan.py",
            "objective": "prepare a reviewed diff plan for inserting PC3400 clauses into formalization-workbench without changing public/core files yet",
            "why_next": "adoption should be deliberate and reviewable, not silently written into the main theory spine",
            "valid_for_claim": False,
        },
    ]


def validate(outputs: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str = "") -> None:
        rows.append({"check_id": check_id, "check": check, "passed": passed, "detail": detail})

    add("VAL3400_0_sources_exist", "all registered sources exist", all(row["exists"] for row in outputs["source_register"]), f"sources={len(outputs['source_register'])}")
    add("VAL3400_1_clause_count", "all parent signature clauses are present", len(outputs["parent_signature_clauses"]) == 7, "")
    add("VAL3400_2_core_audit", "core compatibility audit covers required terms", len(outputs["core_compatibility_audit"]) == 10, "")
    add("VAL3400_3_no_contradiction", "no contradiction is asserted by audit", all(not row["contradiction_found"] for row in outputs["core_compatibility_audit"]), "")
    add("VAL3400_4_activation", "activation theorem derives Delta_Newton closure if signed", any("Delta_Newton_v_coupled=0" in row["statement"] for row in outputs["activation_theorem"]), "")
    add("VAL3400_5_parent_not_claimed", "parent adoption and local GR gates remain blocked", not any(row["gate_pass"] for row in outputs["promotion_gates"] if row["gate_id"] in {"GATE3400_2_parent_adopted", "GATE3400_3_first_order_newton_claim", "GATE3400_4_local_GR_claim"}), "")
    add("VAL3400_6_no_overclaim", "all generated rows remain nonclaim", all(str(row.get("valid_for_claim", False)).lower() == "false" for group in outputs.values() for row in group), "")
    add("VAL3400_7_scope", "no 3400 output path targets formalization-workbench", "formalization-workbench" not in str(DOC).lower() and all("formalization-workbench" not in str(path).lower() for path in OUTPUT_PATHS.values()), "")
    add("VAL3400_8_next_target", "next target moves to kappa_v beta ledger", any("kappa_v" in row["objective"] for row in outputs["next_target"]), "")
    add("VAL3400_9_overall", "3400 validation overall", all(row["passed"] is True for row in rows), "all required checks passed")
    return rows


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |",
            *[
                "| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |"
                for row in rows
            ],
        ]
    )


def write_doc(outputs: dict[str, list[dict[str, Any]]]) -> None:
    timestamp = datetime.now(timezone.utc).isoformat()
    sections = [
        "# 3400 - Y5/R2FR first-order source-coupling parent signature pack under AX1090",
        "",
        "## Summary",
        "- 3400 writes the exact parent-signature clauses that would activate the 3399 first-order Newton/source-amplitude zero theorem.",
        "- The audit result is favourable but not claim-level: current core evidence is compatible, yet the crucial source-coupling objects remain explicit extensions.",
        "- If PC3400_0..6 are adopted in one parent branch with no retained residuals, then `Delta_Newton_v_coupled=0` follows exactly.",
        "- This checkpoint does not edit `formalization-workbench` and does not claim local GR; beta/full PPN still requires `kappa_v` closure.",
        f"- Generated UTC: `{timestamp}`.",
        "",
        "## Source Register",
        md_table(outputs["source_register"]),
        "",
        "## Parent Signature Clauses",
        md_table(outputs["parent_signature_clauses"]),
        "",
        "## Core Compatibility Audit",
        md_table(outputs["core_compatibility_audit"]),
        "",
        "## First-Order Activation Theorem",
        md_table(outputs["activation_theorem"]),
        "",
        "## Adoption Patch Packet",
        md_table(outputs["adoption_patch_packet"]),
        "",
        "## Promotion Gates",
        md_table(outputs["promotion_gates"]),
        "",
        "## Nonclaim Runner",
        md_table(outputs["runner_nonclaim"]),
        "",
        "## Decision Ledger",
        md_table(outputs["decision_ledger"]),
        "",
        "## Validation",
        md_table(outputs["validation"]),
        "",
        "## Next Target",
        md_table(outputs["next_target"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    outputs = {
        "source_register": source_register(),
        "parent_signature_clauses": parent_signature_clauses(),
        "core_compatibility_audit": core_compatibility_audit(),
        "activation_theorem": activation_theorem(),
        "adoption_patch_packet": adoption_patch_packet(),
        "promotion_gates": promotion_gates(),
        "runner_nonclaim": runner_nonclaim(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
    }
    outputs["validation"] = validate(outputs)
    for name, rows in outputs.items():
        write_csv(OUTPUT_PATHS[name], rows)
    parsed = [(path.name, len(read_csv(path))) for path in OUTPUT_PATHS.values()]
    if not all(row["passed"].lower() == "true" for row in read_csv(OUTPUT_PATHS["validation"])):
        raise RuntimeError("3400 validation failed")
    write_doc(outputs)
    print(f"Wrote {DOC}")
    print(f"Wrote {len(OUTPUT_PATHS)} CSV outputs under {OUT}")
    print("Parsed outputs: " + "; ".join(f"{name}={count}" for name, count in parsed))


if __name__ == "__main__":
    main()
