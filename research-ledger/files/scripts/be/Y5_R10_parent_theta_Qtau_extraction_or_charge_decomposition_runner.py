from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: object) -> bool:
    return str(value).strip().lower() == "true"


def missing(value: object) -> bool:
    text = str(value or "").strip()
    return text == "" or text.upper().startswith("MISSING")


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path_text: str) -> str:
    path = source_path(path_text)
    return path.read_text(encoding="utf-8", errors="replace")


def path_list_exists(path_text: str) -> bool:
    text = str(path_text or "").strip()
    if missing(text):
        return False
    forbidden = {
        "EH_REFERENCE_ONLY",
        "FITTED_AFTER_READOUT",
        "POST_READOUT_FITTED_REFERENCE",
        "UNOWNED_EXTRA_SECTOR",
        "UNOWNED_PROJECTOR_SECTOR",
    }
    if text in forbidden:
        return False
    return all(source_path(piece.strip()).exists() for piece in text.split(";") if piece.strip())


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def md_cell(value: object) -> str:
    text = str(value).replace("\n", " ").replace("|", "\\|")
    return text


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md_cell(row.get(col, "")) for col in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body]) + "\n"


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        (
            "SRC1008_0_1007_doc",
            "1007-Y5-R10-Htau-integrability-fixed-reference-theorem-or-symplectic-residual-row.md",
            "H_tau integrability/fixed-reference theorem attempted",
            "1007 handoff: H_tau blocked until parent theta/Q_tau is extracted.",
        ),
        (
            "SRC1008_1_1007_next",
            "source-intake/mts_residuals/P8_Y5_R10_1007_NEXT_TARGET.csv",
            "extract parent MTS theta",
            "Explicit 1008 target row.",
        ),
        (
            "SRC1008_2_1007_claim_gate",
            "source-intake/mts_residuals/P8_Y5_R10_1007_CLAIM_GATE.csv",
            "CG1007_0_Htau_integrability",
            "H_tau and downstream local-GR gates remain blocked.",
        ),
        (
            "SRC1008_3_owner_audit",
            "source-intake/mts_residuals/P8_Y5_R10_771_THETA_QTAU_CURRENT_OWNER_AUDIT.csv",
            "TQ771_0_parent_variation",
            "Earlier owner audit for theta_total/Q_tau current extraction.",
        ),
        (
            "SRC1008_4_extraction_test",
            "source-intake/mts_residuals/P8_Y5_R10_771_NOETHER_EXTRACTION_TEST.csv",
            "NET771_0_parent_variation",
            "Existing Noether extraction test.",
        ),
        (
            "SRC1008_5_noether_variation",
            "source-intake/mts_residuals/P8_Y5_R10_824_NOETHER_VARIATION_AUDIT.csv",
            "N824_0_diffeomorphism_identity",
            "Noether/Ward identity warning: ownership is not zero-proof.",
        ),
        (
            "SRC1008_6_Qtau_decomposition",
            "source-intake/mts_residuals/P8_Y5_R10_993_QTAU_DECOMPOSITION_LEDGER.csv",
            "QDEC993_5_total",
            "Current Q_tau piece ledger.",
        ),
        (
            "SRC1008_7_parent_noether_chain",
            "source-intake/mts_residuals/P8_PARENT_NOETHER_CLOSURE_DERIVATION_CHAIN.csv",
            "D505_2_charge_form",
            "Parent charge-form chain.",
        ),
        (
            "SRC1008_8_momentum_map",
            "source-intake/mts_residuals/P8_Y5_R10_583_NOETHER_MOMENTUM_MAP_CONTRACT.csv",
            "NMC583_0_symplectic_potential",
            "Momentum-map contract for parent symplectic potential/current.",
        ),
        (
            "SRC1008_9_gauge_identity",
            "source-intake/mts_residuals/P8_Y5_R10_917_GAUGE_NOETHER_IDENTITY_ATTEMPT.csv",
            "NIA917_1_mass_gauge_symmetry",
            "Gauge/source identity route for Hilbert-current ownership.",
        ),
        (
            "SRC1008_10_local_current_noether",
            "source-intake/mts_residuals/P8_YLOC_SOURCE_CURRENT_NOETHER_AUDIT.csv",
            "N5_verdict",
            "Noether alone is discipline, not a zero-current theorem.",
        ),
        (
            "SRC1008_11_hamiltonian_contract",
            "source-intake/mts_residuals/P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv",
            "HC2_differentiable_integrable_Hxi",
            "Hamiltonian boundary charge contract.",
        ),
        (
            "SRC1008_12_1007_validation",
            "source-intake/mts_residuals/P8_Y5_BRR545_1007_VALIDATION.csv",
            "V1007_SUMMARY",
            "Prior validation gate passed.",
        ),
    ]
    rows: list[dict[str, str]] = []
    for source_id, path_text, needle, role in specs:
        path = source_path(path_text)
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        rows.append(
            {
                "source_id": source_id,
                "source_path": path_text,
                "exists": str(path.exists()).lower(),
                "needle": needle,
                "needle_found": str(needle in text).lower(),
                "role": role,
                "generated_utc": stamp(),
            }
        )
    return rows


def parent_variation_audit_rows() -> list[dict[str, str]]:
    rows = [
        {
            "audit_id": "PVA1008_0_parent_action",
            "object": "L_parent",
            "required_equation": "delta L_parent = E_A delta Phi^A + d theta_MTS(delta Phi)",
            "current_evidence": "771 says the explicit current-chain L_parent with EH, matter, extra, boundary/reference, and coupling sectors is not filled.",
            "status": "missing_explicit_current_chain",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "PVA1008_1_theta_MTS",
            "object": "theta_MTS",
            "required_equation": "theta_MTS = theta_EH + theta_boundary + theta_extra + theta_projector + theta_matter/source",
            "current_evidence": "583 and 771 require parent symplectic potential; no full sector variation owns all pieces.",
            "status": "template_available_not_extracted",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "PVA1008_2_J_tau",
            "object": "J_tau",
            "required_equation": "J_tau = theta_MTS(L_tau Phi) - i_tau L_parent",
            "current_evidence": "Noether current shape is available, but tau action across metric, matter, representative, boundary/reference fields is not parent-owned.",
            "status": "formal_shape_no_owner",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "PVA1008_3_Q_tau_piece_split",
            "object": "Q_tau^MTS",
            "required_equation": "J_tau = dQ_tau^MTS + C_tau, Q_tau^MTS = Q_EH + Q_boundary + Q_extra + Q_projector + Q_matter/source",
            "current_evidence": "993 only has Q_EH as conditional GR reference; boundary, extra, projector, and matter/source pieces are not extracted.",
            "status": "piece_split_not_promoted",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "PVA1008_4_Noether_identity_limit",
            "object": "Noether/Ward identity",
            "required_equation": "dJ_tau = -E_A L_tau Phi^A plus boundary terms",
            "current_evidence": "824 and YLOC audit confirm identities assign ownership but do not prove piecewise silence or zero residual current.",
            "status": "ownership_not_zero_theorem",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "PVA1008_5_EH_import_limit",
            "object": "EH covariant phase-space charge",
            "required_equation": "Q_tau^MTS -> Q_tau^EH only after parent reduction/silence/topological clauses are signed",
            "current_evidence": "1007 explicitly refused EH-only import without MTS parent theta/Q_tau.",
            "status": "reference_only_guard_active",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "PVA1008_6_verdict",
            "object": "parent theta_MTS/Q_tau^MTS extraction",
            "required_equation": "PVA1008_0 through PVA1008_5 pass with source/equation paths and parent signatures",
            "current_evidence": "Corpus supports a disciplined extraction contract, not an extracted charge theorem.",
            "status": "fail_current_claim",
            "valid_for_claim": "false",
        },
    ]
    for row in rows:
        row["generated_utc"] = stamp()
    return rows


def charge_piece_rows() -> list[dict[str, str]]:
    rows = [
        {
            "piece_id": "QTA1008_0_L_parent",
            "Q_piece": "parent action variation",
            "status": "missing_explicit_current_chain",
            "role": "owns theta_MTS and all Noether charges",
            "not_enough_because": "no single parent action is varied across EH, matter/source, extra, projector, boundary/reference, and coupling sectors",
            "valid_for_claim": "false",
        },
        {
            "piece_id": "QTA1008_1_theta_total",
            "Q_piece": "theta_MTS",
            "status": "not_extracted",
            "role": "symplectic potential in delta H_tau",
            "not_enough_because": "theta_EH is not enough; theta_extra, theta_projector, theta_boundary, and matter/source terms remain unowned",
            "valid_for_claim": "false",
        },
        {
            "piece_id": "QTA1008_2_J_tau",
            "Q_piece": "J_tau",
            "status": "formal_shape_only",
            "role": "Noether current for observed tau",
            "not_enough_because": "tau action on all parent and boundary/reference fields is not fixed",
            "valid_for_claim": "false",
        },
        {
            "piece_id": "QTA1008_3_Q_EH",
            "Q_piece": "Q_tau^EH[g_obs,tau]",
            "status": "conditional_GR_reference",
            "role": "baseline charge form",
            "not_enough_because": "does not include MTS residual, projector, boundary/reference, or coupling sectors",
            "valid_for_claim": "false",
        },
        {
            "piece_id": "QTA1008_4_Q_boundary",
            "Q_piece": "Q_tau^boundary + delta B_ref",
            "status": "not_parent_fixed",
            "role": "finite charge and subtraction convention",
            "not_enough_because": "reference/counterterm can absorb normalization unless fixed before readout",
            "valid_for_claim": "false",
        },
        {
            "piece_id": "QTA1008_5_Q_extra",
            "Q_piece": "Q_tau^extra + C_extra",
            "status": "not_extracted",
            "role": "motion/time/domain/memory/range leakage",
            "not_enough_because": "extra-sector theta, charge, and silence theorem are missing",
            "valid_for_claim": "false",
        },
        {
            "piece_id": "QTA1008_6_Q_projector",
            "Q_piece": "Q_tau^projector + C_projector",
            "status": "not_extracted",
            "role": "mass projector/source-current channel",
            "not_enough_because": "Pi_M chain map, commutator, and variation terms remain residuals",
            "valid_for_claim": "false",
        },
        {
            "piece_id": "QTA1008_7_Q_matter_source",
            "Q_piece": "C_tau^matter[J_H] and source glue",
            "status": "conditional_not_glued",
            "role": "links parent charge to observed mass/source",
            "not_enough_because": "Hilbert-current equality, worldtube denominator, and matter coupling descent remain unsigned",
            "valid_for_claim": "false",
        },
        {
            "piece_id": "QTA1008_8_Q_total",
            "Q_piece": "Q_tau^MTS=sum extracted pieces",
            "status": "not_promoted",
            "role": "candidate physical Hamiltonian mass charge",
            "not_enough_because": "only EH shape is conditional; all MTS-owned retained pieces must be extracted or explicitly zero/bounded",
            "valid_for_claim": "false",
        },
    ]
    for row in rows:
        row["generated_utc"] = stamp()
    return rows


def decomposition_schema_rows() -> list[dict[str, str]]:
    rows = [
        {
            "schema_id": "CDS1008_0_parent_variation",
            "target": "theta_MTS",
            "required_fields": "L_parent_source; field_list; variation_variables; theta_source; equation_ref; action_decomposition_certificate",
            "pass_condition": "delta L_parent is supplied and theta_MTS is explicit for every retained sector",
            "claim_effect": "allows H_tau integrability to be evaluated rather than placeholder-refused",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "CDS1008_1_Noether_charge",
            "target": "Q_tau^MTS",
            "required_fields": "J_tau equation; Q_tau_EH; Q_tau_boundary; Q_tau_extra; Q_tau_projector; Q_tau_matter/source; constraints",
            "pass_condition": "J_tau=dQ_tau^MTS+C_tau and every retained C_tau piece is zero, bounded, or sourced",
            "claim_effect": "turns Q_tau total from ledger into candidate theorem object",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "CDS1008_2_EH_import_guard",
            "target": "EH_REFERENCE_ONLY",
            "required_fields": "MTS parent reduction; silent/topological residual certificate; extra/projector/matter certificates",
            "pass_condition": "EH charge can be used only after MTS reduction is parent-signed",
            "claim_effect": "prevents GR formulas being smuggled in as MTS proof",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "CDS1008_3_reference_guard",
            "target": "boundary/reference convention",
            "required_fields": "fixed_before_readout counterterm policy; improvement ambiguity certificate; boundary flux condition",
            "pass_condition": "reference cannot be tuned after the source/orbit/clock readout",
            "claim_effect": "protects M_H_ref and Delta_ref from fitted-counterterm cancellation",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "CDS1008_4_total_promoter",
            "target": "Q_tau^MTS total",
            "required_fields": "PARENT_SIGNED_QTAU_TOTAL_TRUE or all sector certificates plus valid source paths",
            "pass_condition": "total theorem is signed, or the decomposition runner proves every retained piece is owned",
            "claim_effect": "only then may H_tau/M_H_ref/local-GR gates reopen",
            "valid_for_claim": "false",
        },
    ]
    for row in rows:
        row["generated_utc"] = stamp()
    return rows


def candidate_rows() -> list[dict[str, str]]:
    base = {
        "target": "Q_tau^MTS_total_extraction",
        "L_parent_source": "MISSING_L_PARENT_SOURCE",
        "theta_source": "MISSING_THETA_SOURCE",
        "Q_tau_EH_source": "MISSING_Q_TAU_EH_SOURCE",
        "Q_tau_boundary_source": "MISSING_Q_TAU_BOUNDARY_SOURCE",
        "Q_tau_extra_source": "MISSING_Q_TAU_EXTRA_SOURCE",
        "Q_tau_projector_source": "MISSING_Q_TAU_PROJECTOR_SOURCE",
        "Q_tau_matter_source": "MISSING_Q_TAU_MATTER_SOURCE",
        "constraint_source": "MISSING_CONSTRAINT_SOURCE",
        "equation_ref": "MISSING_EQUATION_REF",
        "action_decomposition_certificate": "MISSING_ACTION_DECOMPOSITION_CERTIFICATE",
        "theta_extraction_certificate": "MISSING_THETA_EXTRACTION_CERTIFICATE",
        "Noether_current_certificate": "MISSING_NOETHER_CURRENT_CERTIFICATE",
        "charge_piece_ownership_certificate": "MISSING_CHARGE_PIECE_OWNERSHIP_CERTIFICATE",
        "extra_sector_silence_certificate": "MISSING_EXTRA_SECTOR_SILENCE_CERTIFICATE",
        "boundary_reference_certificate": "MISSING_BOUNDARY_REFERENCE_CERTIFICATE",
        "matter_source_glue_certificate": "MISSING_MATTER_SOURCE_GLUE_CERTIFICATE",
        "projector_chain_certificate": "MISSING_PROJECTOR_CHAIN_CERTIFICATE",
        "tau_action_certificate": "MISSING_TAU_ACTION_CERTIFICATE",
        "improvement_ambiguity_certificate": "MISSING_IMPROVEMENT_AMBIGUITY_CERTIFICATE",
        "theorem_total": "false",
        "total_authority": "MISSING_PARENT_QTAU_TOTAL_AUTHORITY",
        "counterterm_policy": "MISSING_COUNTERTERM_POLICY",
        "EH_import_guard": "MISSING_MTS_PARENT_REDUCTION",
        "valid_for_claim": "false",
    }
    rows: list[dict[str, str]] = []

    def add(candidate_id: str, candidate: str, **updates: str) -> None:
        row = dict(base)
        row.update({"candidate_id": candidate_id, "candidate": candidate, "generated_utc": stamp()})
        row.update(updates)
        rows.append(row)

    add("CDC1008_0_missing_parent_L", "no explicit parent current-chain action is supplied")
    add(
        "CDC1008_1_EH_only_import",
        "EH covariant phase-space charge is used as the whole MTS charge",
        L_parent_source="source-intake/mts_residuals/P8_PARENT_NOETHER_CLOSURE_DERIVATION_CHAIN.csv",
        theta_source="EH_REFERENCE_ONLY",
        Q_tau_EH_source="source-intake/mts_residuals/P8_Y5_R10_993_QTAU_DECOMPOSITION_LEDGER.csv",
        Q_tau_boundary_source="EH_REFERENCE_ONLY",
        counterterm_policy="FIXED_BEFORE_READOUT",
    )
    add(
        "CDC1008_2_boundary_reference_unsigned",
        "boundary/reference contribution is named but not fixed before readout",
        L_parent_source="source-intake/mts_residuals/P8_PARENT_NOETHER_CLOSURE_DERIVATION_CHAIN.csv",
        Q_tau_EH_source="source-intake/mts_residuals/P8_Y5_R10_993_QTAU_DECOMPOSITION_LEDGER.csv",
        Q_tau_boundary_source="source-intake/mts_residuals/P8_Y5_R10_993_QTAU_DECOMPOSITION_LEDGER.csv",
        counterterm_policy="MISSING_FIXED_BEFORE_READOUT_CERTIFICATE",
    )
    add(
        "CDC1008_3_extra_projector_unsigned",
        "extra/projector pieces are retained but not extracted",
        L_parent_source="source-intake/mts_residuals/P8_PARENT_NOETHER_CLOSURE_DERIVATION_CHAIN.csv",
        Q_tau_EH_source="source-intake/mts_residuals/P8_Y5_R10_993_QTAU_DECOMPOSITION_LEDGER.csv",
        Q_tau_extra_source="UNOWNED_EXTRA_SECTOR",
        Q_tau_projector_source="UNOWNED_PROJECTOR_SECTOR",
        counterterm_policy="FIXED_BEFORE_READOUT",
    )
    add(
        "CDC1008_4_matter_source_unsigned",
        "matter/source constraint is conditional but not glued",
        L_parent_source="source-intake/mts_residuals/P8_Y5_R10_917_GAUGE_NOETHER_IDENTITY_ATTEMPT.csv",
        Q_tau_matter_source="source-intake/mts_residuals/P8_Y5_R10_993_QTAU_DECOMPOSITION_LEDGER.csv",
        constraint_source="source-intake/mts_residuals/P8_Y5_R10_917_GAUGE_NOETHER_IDENTITY_ATTEMPT.csv",
        counterterm_policy="FIXED_BEFORE_READOUT",
    )
    add(
        "CDC1008_5_total_theorem_unsigned",
        "Q_tau total is promoted by theorem_zero style switch without parent signature",
        theorem_total="true",
        total_authority="MISSING_PARENT_QTAU_TOTAL_SIGNATURE",
        counterterm_policy="FIXED_BEFORE_READOUT",
    )
    add(
        "CDC1008_6_fitted_counterterm_attempt",
        "reference/counterterm is fitted after the readout",
        L_parent_source="source-intake/mts_residuals/P8_PARENT_NOETHER_CLOSURE_DERIVATION_CHAIN.csv",
        counterterm_policy="FITTED_AFTER_READOUT",
    )
    add(
        "CDC1008_7_live_placeholder",
        "current live MTS theta/Q_tau row is still placeholder-only",
        L_parent_source="source-intake/mts_residuals/P8_Y5_R10_771_THETA_QTAU_CURRENT_OWNER_AUDIT.csv",
        theta_source="source-intake/mts_residuals/P8_Y5_R10_771_NOETHER_EXTRACTION_TEST.csv",
        Q_tau_EH_source="source-intake/mts_residuals/P8_Y5_R10_993_QTAU_DECOMPOSITION_LEDGER.csv",
        counterterm_policy="FIXED_BEFORE_READOUT",
    )
    return rows


def evaluate_candidate(row: dict[str, str]) -> dict[str, str]:
    reasons: list[str] = []
    source_fields = [
        "L_parent_source",
        "theta_source",
        "Q_tau_EH_source",
        "Q_tau_boundary_source",
        "Q_tau_extra_source",
        "Q_tau_projector_source",
        "Q_tau_matter_source",
        "constraint_source",
    ]
    for field in source_fields:
        value = row.get(field, "")
        if not path_list_exists(value):
            reasons.append(f"MISSING_EXISTING_{field.upper()}")
    if missing(row.get("equation_ref")):
        reasons.append("MISSING_EQUATION_REF")

    cert_fields = [
        "action_decomposition_certificate",
        "theta_extraction_certificate",
        "Noether_current_certificate",
        "charge_piece_ownership_certificate",
        "extra_sector_silence_certificate",
        "boundary_reference_certificate",
        "matter_source_glue_certificate",
        "projector_chain_certificate",
        "tau_action_certificate",
        "improvement_ambiguity_certificate",
    ]
    for field in cert_fields:
        value = str(row.get(field, "")).strip()
        if not value.startswith("PARENT_SIGNED_"):
            reasons.append(f"MISSING_PARENT_SIGNED_{field.upper()}")

    if row.get("theta_source") == "EH_REFERENCE_ONLY" or row.get("Q_tau_boundary_source") == "EH_REFERENCE_ONLY":
        reasons.append("EH_IMPORT_WITHOUT_PARENT_MTS_REDUCTION_REJECTED")
    if row.get("EH_import_guard") != "MTS_PARENT_REDUCTION_SIGNED":
        reasons.append("MISSING_MTS_PARENT_REDUCTION_GUARD")
    if row.get("counterterm_policy") != "FIXED_BEFORE_READOUT":
        reasons.append("FITTED_OR_UNFIXED_COUNTERTERM_REJECTED")
    if row.get("counterterm_policy") == "FITTED_AFTER_READOUT":
        reasons.append("FITTED_COUNTERTERM_REJECTED")
    if flag(row.get("theorem_total")) and row.get("total_authority") != "PARENT_SIGNED_QTAU_TOTAL_TRUE":
        reasons.append("TOTAL_QTAU_THEOREM_REJECTED_WITHOUT_PARENT_SIGNED_QTAU_TOTAL")
    if not flag(row.get("valid_for_claim")):
        reasons.append("VALID_FOR_CLAIM_FALSE")

    verdict = "PASS_PARENT_QTAU_EXTRACTION" if not reasons else "REFUSED_MISSING_PARENT_THETA_QTAU_EXTRACTION"
    return {
        "runner_id": row["candidate_id"].replace("CDC", "CDR"),
        "candidate_id": row["candidate_id"],
        "target": row["target"],
        "verdict": verdict,
        "score_ready": str(not reasons).lower(),
        "Q_tau_total_promoted": str(not reasons and row.get("total_authority") == "PARENT_SIGNED_QTAU_TOTAL_TRUE").lower(),
        "claim_allowed": str(not reasons and flag(row.get("valid_for_claim"))).lower(),
        "valid_for_claim": str(not reasons and flag(row.get("valid_for_claim"))).lower(),
        "failure_reasons": ";".join(reasons),
        "generated_utc": stamp(),
    }


def runner_rows(candidates: list[dict[str, str]]) -> list[dict[str, str]]:
    return [evaluate_candidate(row) for row in candidates]


def refusal_rows(runner: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for row in runner:
        rows.append(
            {
                "refusal_id": row["runner_id"].replace("CDR", "CDF"),
                "candidate_id": row["candidate_id"],
                "verdict": row["verdict"],
                "failure_reasons": row["failure_reasons"],
                "required_to_promote": "explicit L_parent variation, theta_MTS, J_tau, all Q_tau pieces, fixed reference, tau action, improvement convention, source constraints, and parent signatures",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def claim_gate_rows(runner: list[dict[str, str]], variation: list[dict[str, str]]) -> list[dict[str, str]]:
    all_refused = all(row["verdict"].startswith("REFUSED") for row in runner)
    variation_failed = any(row["audit_id"] == "PVA1008_6_verdict" and row["status"] == "fail_current_claim" for row in variation)
    rows = [
        {
            "gate_id": "CG1008_0_parent_theta",
            "claim": "theta_MTS is extracted from parent MTS action",
            "gate_pass": "false",
            "reason": "explicit current-chain parent action and sector variations remain missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1008_1_Qtau_total",
            "claim": "Q_tau^MTS total is promoted",
            "gate_pass": "false",
            "reason": "boundary, extra, projector, matter/source, and improvement pieces are not parent-owned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1008_2_EH_import_guard",
            "claim": "EH charge alone proves MTS charge",
            "gate_pass": "false",
            "reason": "EH is a reference template only without parent MTS reduction/silence certificates",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1008_3_charge_decomposition_runner",
            "claim": "current charge decomposition rows can be used for claims",
            "gate_pass": "false",
            "reason": "every candidate row is refused or nonclaim",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1008_4_Htau_integrability",
            "claim": "H_tau integrability can reopen",
            "gate_pass": "false",
            "reason": "H_tau requires parent theta_MTS and Q_tau^MTS first",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1008_5_MHref",
            "claim": "M_H_ref denominator can pass",
            "gate_pass": "false",
            "reason": "positive same-frame denominator depends on integrable fixed-reference H_tau",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1008_6_RC994_0",
            "claim": "RC994_0 residual current passes",
            "gate_pass": "false",
            "reason": "parent charge and source-current chain remain unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1008_7_FB554_0_local_GR",
            "claim": "FB554_0/local-GR branch passes",
            "gate_pass": "false",
            "reason": "local-GR route still lacks parent Hamiltonian charge and source-measure bridge",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1008_8_guardrail",
            "claim": "parent theta/Q_tau guardrail is installed",
            "gate_pass": str(all_refused and variation_failed).lower(),
            "reason": "theorem is not promoted and all shortcut/placeholder charge rows are refused",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]
    for row in rows:
        row["generated_utc"] = stamp()
    return rows


def decision_rows() -> list[dict[str, str]]:
    rows = [
        {
            "decision_id": "DEC1008_0_parent_charge_not_claimed",
            "decision": "Q_tau^MTS is not extracted or promoted in the current corpus.",
            "because": "theta_MTS, J_tau, retained sector charges, source constraints, and fixed reference are not all parent-signed.",
            "next_action": "build a sector-by-sector parent current-chain action contract rather than importing EH charge alone",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1008_1_EH_kept_as_template",
            "decision": "EH covariant phase-space charge remains useful as the comparison shape, not as the MTS proof.",
            "because": "MTS must prove its own reduction/silence/topological clauses before using EH as the full charge.",
            "next_action": "separate EH baseline, topological/boundary improvements, and residual sector charges",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1008_2_next_action_contract",
            "decision": "The least-cheatable next target is the parent current-chain action contract.",
            "because": "without a concrete L_parent variation there is no honest way to score theta_MTS, Q_tau^MTS, or H_tau integrability.",
            "next_action": "write 1009 parent sector variation contract with strict source/equation slots",
            "valid_for_claim": "false",
        },
    ]
    for row in rows:
        row["generated_utc"] = stamp()
    return rows


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
            "objective": "write the minimal parent action/current-chain contract that can own theta_MTS and Q_tau sector-by-sector, or demote H_tau to explicit closure-only status",
            "include": "L_EH, L_boundary/ref, L_extra, L_projector, L_matter/source, L_mass_gauge/BF, field list, variation variables, tau action, boundary conditions, improvement convention, source/equation paths",
            "exclude": "EH-only import, post-readout counterterm, unowned silent sectors, H_tau pass, M_H_ref pass, RC994_0 pass, FB554_0 pass, local-GR claim, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def formalization_changed_after_start() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    changed = []
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            if modified >= STARTED:
                changed.append(path)
    return changed


def validation_rows(
    sources: list[dict[str, str]],
    variation: list[dict[str, str]],
    charge_pieces: list[dict[str, str]],
    schema: list[dict[str, str]],
    candidates: list[dict[str, str]],
    runner: list[dict[str, str]],
    refusals: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    changed = formalization_changed_after_start()
    validations = [
        (
            "V1008_0_sources_exist",
            all(flag(row["exists"]) and flag(row["needle_found"]) for row in sources),
            "all source paths exist and needles are present",
        ),
        (
            "V1008_1_variation_audit_blocks_claim",
            any(row["audit_id"] == "PVA1008_6_verdict" and row["status"] == "fail_current_claim" for row in variation)
            and all(not flag(row["valid_for_claim"]) for row in variation),
            "parent variation audit keeps theta_MTS/Q_tau extraction nonclaim",
        ),
        (
            "V1008_2_charge_piece_total_blocked",
            any(row["piece_id"] == "QTA1008_8_Q_total" and row["status"] == "not_promoted" for row in charge_pieces)
            and all(not flag(row["valid_for_claim"]) for row in charge_pieces),
            "charge piece ledger includes blocked total Q_tau",
        ),
        (
            "V1008_3_schema_ready",
            {"CDS1008_0_parent_variation", "CDS1008_1_Noether_charge", "CDS1008_2_EH_import_guard", "CDS1008_4_total_promoter"}.issubset(
                {row["schema_id"] for row in schema}
            ),
            "parent variation, Noether charge, EH guard, and promoter schemas are present",
        ),
        (
            "V1008_4_candidates_nonclaim",
            len(candidates) >= 8 and all(not flag(row["valid_for_claim"]) for row in candidates),
            "candidate charge decomposition rows remain nonclaim",
        ),
        (
            "V1008_5_runner_refuses_placeholders",
            len(runner) == len(candidates)
            and all(row["verdict"].startswith("REFUSED") and not flag(row["score_ready"]) for row in runner),
            "runner refuses every placeholder or shortcut charge row",
        ),
        (
            "V1008_6_EH_import_guard",
            any(
                row["candidate_id"] == "CDC1008_1_EH_only_import"
                and "EH_IMPORT_WITHOUT_PARENT_MTS_REDUCTION_REJECTED" in row["failure_reasons"]
                for row in runner
            ),
            "EH-only import is refused without parent MTS reduction",
        ),
        (
            "V1008_7_fitted_counterterm_guard",
            any(
                row["candidate_id"] == "CDC1008_6_fitted_counterterm_attempt"
                and "FITTED_COUNTERTERM_REJECTED" in row["failure_reasons"]
                for row in runner
            ),
            "post-readout fitted counterterm is refused",
        ),
        (
            "V1008_8_total_theorem_guard",
            any(
                row["candidate_id"] == "CDC1008_5_total_theorem_unsigned"
                and "TOTAL_QTAU_THEOREM_REJECTED_WITHOUT_PARENT_SIGNED_QTAU_TOTAL" in row["failure_reasons"]
                for row in runner
            ),
            "total Q_tau theorem switch is refused without parent signature",
        ),
        (
            "V1008_9_refusal_ledger_nonclaim",
            len(refusals) == len(runner) and all(row["verdict"].startswith("REFUSED") and not flag(row["claim_allowed"]) for row in refusals),
            "refusal ledger mirrors runner and keeps claims false",
        ),
        (
            "V1008_10_claim_gates_blocked",
            all(not flag(row["claim_allowed"]) and not flag(row["valid_for_claim"]) for row in claims),
            "H_tau, M_H_ref, RC994_0, and local-GR claims stay blocked",
        ),
        (
            "V1008_11_guardrail_written",
            any(row["gate_id"] == "CG1008_8_guardrail" and flag(row["gate_pass"]) for row in claims),
            "parent theta/Q_tau guardrail is installed",
        ),
        (
            "V1008_12_decision_written",
            any(row["decision_id"] == "DEC1008_2_next_action_contract" for row in decisions),
            "next parent action/current-chain contract decision is written",
        ),
        (
            "V1008_13_next_target_written",
            len(next_target) == 1 and "1009-Y5-R10-parent-current-chain-action-contract" in next_target[0]["next_target"],
            "1009 target row is present and nonclaim",
        ),
        (
            "V1008_14_formalization_untouched",
            len(changed) == 0,
            f"formalization-workbench modified-file count since script start is {len(changed)}",
        ),
    ]
    rows = [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "generated_utc": stamp(),
        }
        for check_id, passed, detail in validations
    ]
    rows.insert(
        0,
        {
            "check_id": "V1008_SUMMARY",
            "result": "pass" if all(row["result"] == "pass" for row in rows) else "fail",
            "detail": "1008 parent theta/Q_tau extraction validation summary",
            "generated_utc": stamp(),
        },
    )
    return rows


def write_doc(
    sources: list[dict[str, str]],
    variation: list[dict[str, str]],
    charge_pieces: list[dict[str, str]],
    schema: list[dict[str, str]],
    candidates: list[dict[str, str]],
    runner: list[dict[str, str]],
    refusals: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validations: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1008 Y5 R10 parent theta/Qtau extraction or charge decomposition runner",
            "",
            f"**Status:** parent `theta_MTS` and `Q_tau^MTS` extraction attempted; not closed. A strict charge-decomposition runner is installed and keeps all current rows nonclaim.",
            "",
            "**Claim ceiling:** no H_tau integrability, M_H_ref denominator, RC994_0, FB554_0, R10, PPN, WEP, clock, orbital, or local-GR claim is allowed from 1008.",
            "",
            "## Source register",
            md_table(sources, ["source_id", "source_path", "exists", "needle_found", "role"]),
            "## Parent variation audit",
            md_table(variation, ["audit_id", "object", "required_equation", "current_evidence", "status", "valid_for_claim"]),
            "## Charge piece ledger",
            md_table(charge_pieces, ["piece_id", "Q_piece", "status", "role", "not_enough_because", "valid_for_claim"]),
            "## Decomposition schema",
            md_table(schema, ["schema_id", "target", "required_fields", "pass_condition", "claim_effect", "valid_for_claim"]),
            "## Candidate charge decomposition template",
            md_table(
                candidates,
                [
                    "candidate_id",
                    "candidate",
                    "target",
                    "L_parent_source",
                    "theta_source",
                    "Q_tau_EH_source",
                    "counterterm_policy",
                    "theorem_total",
                    "total_authority",
                    "valid_for_claim",
                ],
            ),
            "## Charge decomposition runner",
            md_table(
                runner,
                [
                    "runner_id",
                    "candidate_id",
                    "verdict",
                    "score_ready",
                    "Q_tau_total_promoted",
                    "claim_allowed",
                    "failure_reasons",
                ],
            ),
            "## Refusal ledger",
            md_table(refusals, ["refusal_id", "candidate_id", "verdict", "required_to_promote", "claim_allowed", "valid_for_claim"]),
            "## Claim gate",
            md_table(claims, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "## Decision ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "## Validation",
            md_table(validations, ["check_id", "result", "detail", "generated_utc"]),
            "## Next target",
            md_table(next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    variation = parent_variation_audit_rows()
    charge_pieces = charge_piece_rows()
    schema = decomposition_schema_rows()
    candidates = candidate_rows()
    runner = runner_rows(candidates)
    refusals = refusal_rows(runner)
    claims = claim_gate_rows(runner, variation)
    decisions = decision_rows()
    next_target = next_target_rows()
    validations = validation_rows(sources, variation, charge_pieces, schema, candidates, runner, refusals, claims, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_1008_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_1008_PARENT_VARIATION_AUDIT.csv", variation)
    write_csv(OUT / "P8_Y5_R10_1008_CHARGE_PIECE_LEDGER.csv", charge_pieces)
    write_csv(OUT / "P8_Y5_R10_1008_CHARGE_DECOMPOSITION_SCHEMA.csv", schema)
    write_csv(OUT / "P8_Y5_R10_1008_CANDIDATE_CHARGE_DECOMPOSITION_TEMPLATE.csv", candidates)
    write_csv(OUT / "P8_Y5_R10_1008_CHARGE_DECOMPOSITION_RUNNER.csv", runner)
    write_csv(OUT / "P8_Y5_R10_1008_REFUSAL_LEDGER.csv", refusals)
    write_csv(OUT / "P8_Y5_R10_1008_CLAIM_GATE.csv", claims)
    write_csv(OUT / "P8_Y5_R10_1008_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_1008_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_1008_VALIDATION.csv", validations)
    write_doc(sources, variation, charge_pieces, schema, candidates, runner, refusals, claims, decisions, next_target, validations)


if __name__ == "__main__":
    main()
