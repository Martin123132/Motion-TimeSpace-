from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1358"
TITLE = "1358-Y5-R10-RAB-PiM-fixed-chainmap-parent-signature-or-Icommutator-first-profile-row"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
SIGNATURE_ATTEMPT_PATH = OUT_DIR / f"{PACK_ID}_FIXED_CHAINMAP_PARENT_SIGNATURE_ATTEMPT.csv"
PARENT_CONTRACT_PATH = OUT_DIR / f"{PACK_ID}_PARENT_CHAINMAP_CONTRACT.csv"
FIRST_PROFILE_ROW_PATH = OUT_DIR / f"{PACK_ID}_ICOMMUTATOR_FIRST_PROFILE_ROW_SCHEMA.csv"
CLAIM_GATE_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1358_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        out.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ") for header in headers) + " |")
    return "\n".join(out)


def mark_nonclaim(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def source_register() -> list[dict[str, object]]:
    rows = [
        {
            "source_id": "SRC1358_0_1357_doc",
            "source_path": "1357-Y5-R10-RAB-PiM-commutator-fixed-topology-or-Icommutator-source-profile.md",
            "required_anchor": "PCZ1357_8_verdict",
            "purpose": "1357 records the conditional chain-map lemma and current failure.",
        },
        {
            "source_id": "SRC1358_1_1357_next",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1357_NEXT_TARGET.csv",
            "required_anchor": "NEXT1357_0_1358",
            "purpose": "handoff to fixed-chainmap parent-signature attempt.",
        },
        {
            "source_id": "SRC1358_2_1357_profiles",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1357_ICOMMUTATOR_SOURCE_PROFILE_ROWS.csv",
            "required_anchor": "ICP1357_0_fixed_domain_derivative",
            "purpose": "I_commutator source-profile split from 1357.",
        },
        {
            "source_id": "SRC1358_3_topo_certificate",
            "source_path": "source-intake/mts_residuals/P8_Y5_PIM_TOPO_EQUALITY_CERTIFICATE.csv",
            "required_anchor": "PTEC534_0_fixed_parent_domain",
            "purpose": "topological Pi_M certificate clauses needed for chain-map ownership.",
        },
        {
            "source_id": "SRC1358_4_commutator_gate",
            "source_path": "source-intake/mts_residuals/P8_Y5_PIM_COMMUTATOR_GATE.csv",
            "required_anchor": "PC521_2_topological_zero_commutator",
            "purpose": "commutator-zero route and Hodge/readout guardrails.",
        },
        {
            "source_id": "SRC1358_5_input_template",
            "source_path": "source-intake/mts_residuals/P8_Y5_PIM_INPUT_FILL_TEMPLATE.csv",
            "required_anchor": "PIF537_1_I_commutator",
            "purpose": "source-ready columns for an I_commutator row.",
        },
        {
            "source_id": "SRC1358_6_radial_template",
            "source_path": "source-intake/mts_residuals/P8_Y5_PIM_RADIAL_BOUND_INPUT.csv",
            "required_anchor": "PI521_1_commutator_profile",
            "purpose": "finite-annulus commutator profile definition.",
        },
        {
            "source_id": "SRC1358_7_1015_doc",
            "source_path": "1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md",
            "required_anchor": "SOL1015_5_commutator_stress_silence",
            "purpose": "same-object lemma says commutator silence still requires fixed chain-map.",
        },
        {
            "source_id": "SRC1358_8_1017_doc",
            "source_path": "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md",
            "required_anchor": "HRL1017_5_MHref_denominator",
            "purpose": "same-frame denominator/reference lock remains missing.",
        },
    ]
    for row in rows:
        path = source_path(str(row["source_path"]))
        row["exists"] = path.exists()
        row["anchor_found"] = path.exists() and str(row["required_anchor"]) in read_text(path)
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def signature_attempt() -> list[dict[str, object]]:
    rows = [
        {
            "clause_id": "FCM1358_0_parent_selector",
            "claim_piece": "parent action selects the mass/topology channel before observations",
            "required_identity": "S_parent contains or derives a topological selector chi_M / ell_M and compact source support W_M independent of fitted readout",
            "attempt_result": "No current source file supplies a parent term, constraint, or variational principle that selects chi_M and W_M.",
            "status": "NOT_PARENT_SIGNED",
            "blocks": "Pi_M can still be a useful audit map, but not a derived field-theory object",
        },
        {
            "clause_id": "FCM1358_1_fixed_domain",
            "claim_piece": "compact source worldtube and exterior annulus are fixed parent data",
            "required_identity": "delta_readout W_M=0, delta_g [S2]_M=0, and A_ext ~= S2 x I is fixed before orbital fitting",
            "attempt_result": "The certificate states the condition, but current MTS has no parent support theorem fixing it.",
            "status": "NOT_PARENT_SIGNED",
            "blocks": "domain derivative component of I_commutator remains live",
        },
        {
            "clause_id": "FCM1358_2_metric_independent_PiM",
            "claim_piece": "Pi_M is topological rather than Hodge/DeWitt metric machinery",
            "required_identity": "Pi_M J = ell_M(J) omega_M_top with d omega_M_top=0 and delta_g Pi_M=0",
            "attempt_result": "This would be enough to avoid projector stress, but it is not derived from the parent action.",
            "status": "CONDITIONAL_NOT_DERIVED",
            "blocks": "Hodge/metric projector variation remains a source-profile row",
        },
        {
            "clause_id": "FCM1358_3_chainmap_property",
            "claim_piece": "Pi_M commutes with exterior derivative on the owned source complex",
            "required_identity": "d Pi_M = Pi_M d on C_H(W_M,A_ext), so [d,Pi_M]J_H=0",
            "attempt_result": "The algebra is clean if FCM1358_0-2 and current-domain membership are true.",
            "status": "CONDITIONAL_LEMMA_ONLY",
            "blocks": "the lemma has no claim credit until parent ownership is signed",
        },
        {
            "clause_id": "FCM1358_4_physical_current_membership",
            "claim_piece": "the physical Hilbert source current lies in the fixed chain-map domain",
            "required_identity": "J_H[e_obs,tau] in C_H(W_M,A_ext), with extra/source/species/frame/memory channels either included or theorem-zero",
            "attempt_result": "1355-1357 retain source channels and tau/reference drift; membership is not locked.",
            "status": "SOURCE_DOMAIN_NOT_LOCKED",
            "blocks": "physical J_H may escape the topological complex",
        },
        {
            "clause_id": "FCM1358_5_exterior_source_silence",
            "claim_piece": "compact exterior annulus contains no hidden source, anomaly, or boundary support",
            "required_identity": "support(dJ_H), support(A_parent), support(B_flux), support(dPi_M) are absent from A_ext or theorem-zero",
            "attempt_result": "A_parent, B_zero_flux, radial M_eff leakage, and calibration rows remain live.",
            "status": "NOT_DERIVED",
            "blocks": "finite-annulus I_commutator can be nonzero even with a formal topological representative",
        },
        {
            "clause_id": "FCM1358_6_tau_reference_denominator",
            "claim_piece": "same tau and same-frame source denominator normalize the row",
            "required_identity": "tau_source=tau_charge=tau_clock=tau_readout and M_H_ref is a positive same-frame Hamiltonian/Hilbert source charge",
            "attempt_result": "1017 explicitly blocks M_H_ref and tau lock as current claims.",
            "status": "NOT_PARENT_DERIVED",
            "blocks": "no claim-safe normalization for a numeric I_commutator score",
        },
        {
            "clause_id": "FCM1358_7_no_readout_or_idempotence_shortcut",
            "claim_piece": "Pi_M is not a post-readout mask and not justified by Pi_M^2=Pi_M",
            "required_identity": "Pi_M appears before readout in the parent derivation; idempotence is never counted as flux closure",
            "attempt_result": "Guardrail can be enforced, but it does not derive Pi_M.",
            "status": "GUARDRAIL_ONLY",
            "blocks": "prevents cheating but does not reopen local-GR gates",
        },
        {
            "clause_id": "FCM1358_8_verdict",
            "claim_piece": "fixed-chainmap parent signature for current MTS",
            "required_identity": "FCM1358_0 through FCM1358_7 all pass with source paths and parent action ownership",
            "attempt_result": "Current MTS does not parent-sign the fixed-chainmap route. The best honest output is a source-ready first I_commutator row schema.",
            "status": "PARENT_CHAINMAP_SIGNATURE_NOT_PROVED",
            "blocks": "I_commutator remains nonclaim until theorem-zero or sourced numeric profile exists",
        },
    ]
    return mark_nonclaim(rows)


def parent_contract() -> list[dict[str, object]]:
    rows = [
        {
            "contract_id": "PCC1358_0_selector_field_or_constraint",
            "parent_requirement": "topological mass selector exists before readout",
            "minimal_form": "chi_M or ell_M is varied/fixed by S_parent and selects W_M plus the mass channel",
            "would_close": "FCM1358_0_parent_selector",
            "current_status": "MISSING_PARENT_SELECTOR",
            "evidence_needed": "source path to parent action/constraint defining chi_M or ell_M",
        },
        {
            "contract_id": "PCC1358_1_fixed_worldtube_domain",
            "parent_requirement": "source worldtube and exterior linking class are fixed",
            "minimal_form": "delta W_M=0 and delta[S2]_M=0 under metric/readout/orbit variations",
            "would_close": "FCM1358_1_fixed_domain",
            "current_status": "MISSING_DOMAIN_LOCK",
            "evidence_needed": "worldtube support theorem or parent boundary condition",
        },
        {
            "contract_id": "PCC1358_2_closed_representative",
            "parent_requirement": "closed normalized representative is supplied",
            "minimal_form": "d omega_M_top=0, integral_link omega_M_top=1, and omega_M_top is selected independently of g",
            "would_close": "FCM1358_2_metric_independent_PiM",
            "current_status": "CONDITIONAL_TEMPLATE_ONLY",
            "evidence_needed": "topological representative construction tied to the physical source",
        },
        {
            "contract_id": "PCC1358_3_chainmap_proof",
            "parent_requirement": "Pi_M is a chain-map on the Hilbert-current complex",
            "minimal_form": "d(Pi_M J)=Pi_M dJ for every J in C_H(W_M,A_ext)",
            "would_close": "FCM1358_3_chainmap_property",
            "current_status": "CONDITIONAL_LEMMA_ONLY",
            "evidence_needed": "proof that Pi_M maps the physical current complex to a fixed de Rham class",
        },
        {
            "contract_id": "PCC1358_4_physical_current_lock",
            "parent_requirement": "physical J_H belongs to the same fixed complex",
            "minimal_form": "J_H[e_obs,tau] and all source channels are either in C_H or theorem-zero outside it",
            "would_close": "FCM1358_4_physical_current_membership",
            "current_status": "MISSING_CURRENT_DOMAIN_LOCK",
            "evidence_needed": "same-frame Hilbert current theorem including extra/source/species channels",
        },
        {
            "contract_id": "PCC1358_5_exterior_silence",
            "parent_requirement": "finite annulus contains no commutator source",
            "minimal_form": "int_A [d,Pi_M]J_H=0 from support/boundary/anomaly silence, not from fitting",
            "would_close": "FCM1358_5_exterior_source_silence",
            "current_status": "MISSING_EXTERIOR_SILENCE_THEOREM",
            "evidence_needed": "support and boundary theorem for A_parent, B_flux, and extra current",
        },
        {
            "contract_id": "PCC1358_6_tau_MHref_lock",
            "parent_requirement": "same time generator and denominator are parent-owned",
            "minimal_form": "tau_source=tau_charge=tau_clock=tau_readout; M_H_ref is a positive Hilbert/Hamiltonian source charge",
            "would_close": "FCM1358_6_tau_reference_denominator",
            "current_status": "MISSING_TAU_MHREF_LOCK",
            "evidence_needed": "Hamiltonian charge/reference theorem and source denominator row",
        },
    ]
    return mark_nonclaim(rows)


def first_profile_row() -> list[dict[str, object]]:
    rows = [
        {
            "row_id": "IFR1358_0_Icommutator_domain_first_profile",
            "system_id": "MTS_local_source_normalized_branch",
            "component": "I_commutator_domain",
            "definition": "finite-annulus contribution from failure to parent-lock W_M, A_ext, or the linking class before readout",
            "formula": "epsilon_Icomm_domain = abs(int_A (dPi_M)_domain J_H) / M_H_ref",
            "r1": "MISSING_INNER_RADIUS_OR_SURFACE",
            "r2": "MISSING_OUTER_RADIUS_OR_SURFACE",
            "numerator": "MISSING_INT_A_DPiM_DOMAIN_JH",
            "denominator": "MISSING_M_H_REF",
            "units": "dimensionless_after_M_H_ref_normalization",
            "normalization": "no_orbital_GM_denominator; same-frame Hilbert/Hamiltonian source charge required",
            "source_path": "MISSING_SOURCE_PATH",
            "source_anchor": "MISSING_SOURCE_ANCHOR",
            "assumptions": "fixed source worldtube not proven; row is schema-only until parent/source inputs are real",
            "affected_arenas": "R4;R7;R9;R10;R11;orbital;PPN",
            "value_or_theorem": "MISSING",
            "accepted_for_scoring": False,
            "schema_ready": True,
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
        },
        {
            "row_id": "IFR1358_1_acceptance_requirements",
            "system_id": "schema_gate",
            "component": "I_commutator_domain_acceptance",
            "definition": "requirements before IFR1358_0 can be promoted from schema to evidence",
            "formula": "all required fields numeric/source-backed and valid_for_claim=true; no MISSING markers; M_H_ref source-backed",
            "r1": "required",
            "r2": "required",
            "numerator": "required_numeric_or_theorem_zero",
            "denominator": "required_positive_M_H_ref",
            "units": "recognized",
            "normalization": "same-frame source denominator",
            "source_path": "required_existing_local_or_public_source",
            "source_anchor": "required",
            "assumptions": "must not be a post-readout mask, fitted G absorption, or reference-only zero",
            "affected_arenas": "all linked arenas remain blocked until accepted",
            "value_or_theorem": "MISSING_ACCEPTANCE_INPUTS",
            "accepted_for_scoring": False,
            "schema_ready": True,
            "status": "ACCEPTANCE_GATE_NONCLAIM",
        },
    ]
    return mark_nonclaim(rows)


def claim_gates() -> list[dict[str, object]]:
    rows = [
        {
            "gate_id": "GATE1358_0_conditional_chainmap_math",
            "claim": "fixed parent topological chain-map would imply I_commutator=0",
            "gate_pass": True,
            "reason": "conditional theorem is recorded as mathematics only",
        },
        {
            "gate_id": "GATE1358_1_parent_signature_current_MTS",
            "claim": "current MTS parent-signs fixed-domain metric-independent Pi_M on physical J_H",
            "gate_pass": False,
            "reason": "parent selector, domain lock, current-domain lock, exterior silence, and tau/M_H_ref are missing",
        },
        {
            "gate_id": "GATE1358_2_Icommutator_zero",
            "claim": "I_commutator is theorem-zero for current MTS",
            "gate_pass": False,
            "reason": "conditional chain-map lemma cannot be applied to current physical source rows",
        },
        {
            "gate_id": "GATE1358_3_first_profile_claim_ready",
            "claim": "first I_commutator profile row can be scored",
            "gate_pass": False,
            "reason": "row is schema-ready only; numerator, denominator, surfaces, and source path are missing",
        },
        {
            "gate_id": "GATE1358_4_Newton_local_GR",
            "claim": "Newton/local-GR gates can reopen",
            "gate_pass": False,
            "reason": "Pi_M chain-map, R_eq, B_zero, M_H_ref, and calibration remain blocked",
        },
    ]
    return mark_nonclaim(rows)


def decision_rows() -> list[dict[str, object]]:
    rows = [
        {
            "decision_id": "DEC1358_0_parent_signature_not_closed",
            "decision": "Fixed-chainmap parent signature is not proved.",
            "why": "the clean theorem needs parent selector, fixed domain, metric-independent Pi_M, physical current membership, exterior silence, and tau/M_H_ref lock",
            "next_action": "attack the parent topological selector/action directly",
        },
        {
            "decision_id": "DEC1358_1_first_profile_schema_ready",
            "decision": "First I_commutator profile row schema is now explicit.",
            "why": "if derivation stalls, the domain-derivative channel is the first concrete row to source rather than handwave",
            "next_action": "fill numerator/denominator/surface/source fields only with real evidence",
        },
        {
            "decision_id": "DEC1358_2_best_next_target",
            "decision": "Best next target is parent topological selector action or source-intake for the first profile row.",
            "why": "the chain-map theorem cannot become physical without a parent selector; the fallback needs real M_H_ref and annulus data",
            "next_action": "write the minimal parent selector action contract and attempt to source the first row inputs",
        },
    ]
    return mark_nonclaim(rows)


def next_rows() -> list[dict[str, object]]:
    rows = [
        {
            "next_id": "NEXT1358_0_1359",
            "target_file": "1359-Y5-R10-RAB-parent-topological-selector-action-or-Icommutator-source-intake.md",
            "target_script": "scripts/Y5_R10_RAB_parent_topological_selector_action_or_Icommutator_source_intake.py",
            "task": "try to write a minimal parent action/constraint that selects chi_M, W_M, omega_M_top, and Pi_M before readout; if not, build a source-intake ledger for IFR1358_0 numerator, M_H_ref, surfaces, units, and source path",
            "success_condition": "parent selector action contract that would sign Pi_M chain-map ownership, or a nonclaim source-intake ledger for the first I_commutator profile row",
            "do_not": "do not use Pi_M idempotence, Hodge silence, post-readout masks, orbital-GM denominators, formalization-workbench edits, or GitHub action",
        }
    ]
    return mark_nonclaim(rows)


def validate_outputs(
    sources: list[dict[str, object]],
    attempt: list[dict[str, object]],
    contract: list[dict[str, object]],
    first_row: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[dict[str, object]] = []

    def add(check_id: str, check: str, status: bool, details: str) -> None:
        validations.append({"check_id": check_id, "check": check, "status": "PASS" if status else "FAIL", "details": details})

    add(
        "VAL1358_0_sources_exist",
        "registered source paths exist and anchors are found",
        all(row["exists"] and row["anchor_found"] for row in sources),
        ";".join(f"{row['source_id']}={row['exists']}/{row['anchor_found']}" for row in sources),
    )

    verdict = next(row for row in attempt if row["clause_id"] == "FCM1358_8_verdict")
    add(
        "VAL1358_1_parent_signature_not_promoted",
        "fixed-chainmap parent signature is not promoted",
        verdict["status"] == "PARENT_CHAINMAP_SIGNATURE_NOT_PROVED" and not verdict["claim_allowed"],
        str(verdict["blocks"]),
    )

    add(
        "VAL1358_2_contract_complete",
        "parent chain-map contract has selector/domain/representative/chainmap/current/exterior/tau clauses",
        len(contract) == 7 and all(str(row["current_status"]).startswith(("MISSING", "CONDITIONAL")) for row in contract),
        f"contract_rows={len(contract)}",
    )

    schema = next(row for row in first_row if row["row_id"] == "IFR1358_0_Icommutator_domain_first_profile")
    add(
        "VAL1358_3_first_profile_schema_nonclaim",
        "first I_commutator row is source-ready schema but nonclaim",
        schema["schema_ready"] is True and schema["value_or_theorem"] == "MISSING" and not schema["accepted_for_scoring"] and not schema["claim_allowed"],
        str(schema["status"]),
    )

    add(
        "VAL1358_4_first_profile_missing_markers",
        "schema row keeps missing numerator/denominator/surface/source markers",
        all("MISSING" in str(schema[field]) for field in ("r1", "r2", "numerator", "denominator", "source_path", "source_anchor")),
        "missing markers retained so no accidental score is possible",
    )

    add(
        "VAL1358_5_claim_gates_block_claim",
        "current MTS chainmap/profile/Newton claims remain blocked",
        all((row["gate_pass"] is False or row["gate_id"] == "GATE1358_0_conditional_chainmap_math") and not row["claim_allowed"] for row in gates),
        ";".join(f"{row['gate_id']}={row['gate_pass']}" for row in gates),
    )

    all_rows = sources + attempt + contract + first_row + gates + decisions + next_target
    add(
        "VAL1358_6_nonclaim_policy",
        "all generated rows remain nonclaim",
        all(not row.get("valid_for_claim", False) and not row.get("claim_allowed", False) for row in all_rows),
        "valid_for_claim=false and claim_allowed=false across generated rows",
    )

    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ("*P8_Y5_R10_1358*", "*1358-Y5-R10-RAB-PiM-fixed-chainmap*", "*Y5_R10_RAB_PiM_fixed_chainmap*"):
            formalization_hits.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL1358_7_formalization_untouched",
        "formalization-workbench untouched by generated outputs",
        len(formalization_hits) == 0,
        f"formalization_generated_output_count={len(formalization_hits)}",
    )

    add(
        "VAL1358_8_next_target_1359",
        "next target routes to parent topological selector action or source intake",
        bool(next_target) and str(next_target[0]["target_file"]).startswith("1359-Y5-R10-RAB-parent-topological-selector"),
        str(next_target[0]["target_file"]) if next_target else "missing",
    )

    add(
        "VAL1358_9_overall",
        "overall 1358 validation",
        all(row["status"] == "PASS" for row in validations),
        "1358 blocks parent-chainmap claim and creates first I_commutator profile-row schema",
    )

    return validations


def build_doc(
    sources: list[dict[str, object]],
    attempt: list[dict[str, object]],
    contract: list[dict[str, object]],
    first_row: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> str:
    return "\n\n".join(
        [
            f"# {TITLE}",
            "**Current verdict:** 1358 does not parent-sign the fixed-chainmap route. The conditional theorem is still good mathematics, but current MTS lacks a parent selector for `chi_M/W_M/Pi_M`, fixed domain, metric-independent representative, physical-current membership, exterior silence, and same-frame `M_H_ref`.",
            "**Main progress:** the exact parent contract is now written, and the first fallback `I_commutator` row is source-ready as a schema only. No Newton/local-GR credit is taken; the row still has missing surfaces, numerator, denominator, and source path.",
            "## Source register",
            table(["source_id", "source_path", "exists", "anchor_found", "purpose"], sources),
            "## Fixed-chainmap parent-signature attempt",
            table(["clause_id", "claim_piece", "required_identity", "status", "blocks"], attempt),
            "## Parent chain-map contract",
            table(["contract_id", "parent_requirement", "minimal_form", "would_close", "current_status", "evidence_needed"], contract),
            "## First I_commutator profile row schema",
            table(["row_id", "system_id", "component", "definition", "formula", "r1", "r2", "numerator", "denominator", "units", "normalization", "source_path", "source_anchor", "value_or_theorem", "accepted_for_scoring", "schema_ready", "status"], first_row),
            "## Claim gates",
            table(["gate_id", "claim", "gate_pass", "reason", "claim_allowed"], gates),
            "## Decision ledger",
            table(["decision_id", "decision", "why", "next_action"], decisions),
            "## Next target",
            table(["next_id", "target_file", "target_script", "task", "success_condition", "do_not"], next_target),
            "## Validation",
            table(["check_id", "check", "status", "details"], validations),
        ]
    ) + "\n"


def main() -> None:
    sources = source_register()
    attempt = signature_attempt()
    contract = parent_contract()
    first_row = first_profile_row()
    gates = claim_gates()
    decisions = decision_rows()
    next_target = next_rows()
    validations = validate_outputs(sources, attempt, contract, first_row, gates, decisions, next_target)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(SIGNATURE_ATTEMPT_PATH, attempt)
    write_csv(PARENT_CONTRACT_PATH, contract)
    write_csv(FIRST_PROFILE_ROW_PATH, first_row)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_target)
    write_csv(VALIDATION_PATH, validations)
    DOC_PATH.write_text(
        build_doc(sources, attempt, contract, first_row, gates, decisions, next_target, validations),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
