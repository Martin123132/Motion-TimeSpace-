from __future__ import annotations

import csv
import math
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1006-Y5-R10-MHref-positive-same-frame-denominator-or-Htau-source-row.md"
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


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "S1006_0_handoff_doc",
            "path": "1005-Y5-R10-Delta-ref-derivative-vector-norm-gate.md",
            "role": "1005 handoff selecting positive same-frame M_H_ref target",
            "needle": "1006-Y5-R10-MHref-positive-same-frame-denominator-or-Htau-source-row.md",
        },
        {
            "source_id": "S1006_1_next_target",
            "path": "source-intake/mts_residuals/P8_Y5_R10_1005_NEXT_TARGET.csv",
            "role": "machine-readable 1006 target",
            "needle": "M_H_ref=H_tau[S_link]-H_ref",
        },
        {
            "source_id": "S1006_2_MHref_provenance",
            "path": "source-intake/mts_residuals/P8_Y5_R10_999_DELTA_REF_SOURCE_COEFFICIENT_PROVENANCE.csv",
            "role": "positive same-frame M_H_ref provenance requirement",
            "needle": "DCP999_3_MHref",
        },
        {
            "source_id": "S1006_3_MHref_attempt",
            "path": "source-intake/mts_residuals/P8_Y5_R10_683_MH_REF_DENOMINATOR_ATTEMPT.csv",
            "role": "M_H_ref denominator attempt and anti-circularity rule",
            "needle": "MH683_6_verdict",
        },
        {
            "source_id": "S1006_4_same_frame_gate",
            "path": "source-intake/mts_residuals/P8_Y5_R10_683_SAME_FRAME_GM_GATE.csv",
            "role": "same-frame GM/denominator blocker gate",
            "needle": "SFG683_6_final",
        },
        {
            "source_id": "S1006_5_frame_lock",
            "path": "source-intake/mts_residuals/P8_Y5_R10_684_FRAME_LOCK_CONTRACT.csv",
            "role": "observed frame lock contract",
            "needle": "FLC684_6_verdict",
        },
        {
            "source_id": "S1006_6_tau_lock",
            "path": "source-intake/mts_residuals/P8_Y5_R10_685_TAU_GENERATOR_CONTRACT.csv",
            "role": "tau/Hamiltonian generator lock contract",
            "needle": "TGC685_6_verdict",
        },
        {
            "source_id": "S1006_7_integrability",
            "path": "source-intake/mts_residuals/P8_Y5_R10_664_INTEGRABILITY_ATTEMPT.csv",
            "role": "Hamiltonian charge integrability attempt",
            "needle": "HCI664_6_integrability_verdict",
        },
        {
            "source_id": "S1006_8_source_measure",
            "path": "source-intake/mts_residuals/P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
            "role": "Hamiltonian source measure contract",
            "needle": "HSM541_1_integrable_charge",
        },
        {
            "source_id": "S1006_9_boundary_status",
            "path": "source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv",
            "role": "boundary/reference first-row M_H_ref status",
            "needle": "M_H_ref",
        },
        {
            "source_id": "S1006_10_prior_denominator_fill",
            "path": "source-intake/mts_residuals/P8_Y5_R10_697_DENOMINATOR_FILL_ROW.csv",
            "role": "prior unfilled denominator source row",
            "needle": "MHR697_0_source_normalization_certificate_fill",
        },
        {
            "source_id": "S1006_11_vector_gate",
            "path": "source-intake/mts_residuals/P8_Y5_R10_1005_CLAIM_GATE.csv",
            "role": "vector norm gate requiring M_H_ref",
            "needle": "CG1005_1_vector_norm_bound",
        },
        {
            "source_id": "S1006_12_prior_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_1005_VALIDATION.csv",
            "role": "1005 validation pass",
            "needle": "V1005_SUMMARY",
        },
    ]
    rows: list[dict[str, str]] = []
    for spec in specs:
        path = source_path(spec["path"])
        text = read_text(path)
        rows.append(
            {
                **spec,
                "absolute_path": str(path),
                "exists": flag(path.exists()),
                "needle_found": flag(spec["needle"] in text),
                "valid_for_claim": "false",
            }
        )
    return rows


def mhref_theorem_audit_rows() -> list[dict[str, str]]:
    return [
        {
            "audit_id": "MHA1006_0_definition",
            "object": "M_H_ref",
            "needed_for_claim": "M_H_ref := H_tau[S_link] - H_ref is a finite source charge in one observed frame",
            "current_evidence": "683 defines the target but marks it blocked/nonclaim",
            "status": "definition_only",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "MHA1006_1_integrability",
            "object": "H_tau",
            "needed_for_claim": "delta H_tau = integral_S(delta Q_tau - i_tau theta) is integrable with fixed reference",
            "current_evidence": "664/HSM541 mark integrability and parent theta/Q_tau as not derived",
            "status": "fail_current_claim",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "MHA1006_2_tau_frame_lock",
            "object": "tau_obs and e_obs",
            "needed_for_claim": "same observed tau/coframe controls source, clocks, boundary charge, and orbital readout",
            "current_evidence": "684/685 write contracts but keep parent signature missing",
            "status": "unsigned",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "MHA1006_3_fixed_reference",
            "object": "H_ref and boundary/counterterm convention",
            "needed_for_claim": "H_ref is fixed once and cannot absorb source/radius/time/frame/lambda readout changes",
            "current_evidence": "boundary/reference first-row status has zero claim-valid M_H_ref rows",
            "status": "unsigned",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "MHA1006_4_positivity",
            "object": "M_H_ref > 0",
            "needed_for_claim": "positive source energy after reference subtraction with no boundary/extra-sector contamination",
            "current_evidence": "683 positivity gate is not signed; reference shift and extra-sector channels remain open",
            "status": "unsigned",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "MHA1006_5_anti_circularity",
            "object": "GM_orbit/G_ref",
            "needed_for_claim": "orbital GM can be used only after M_H_ref -> Poisson/Gauss -> orbital readout is derived",
            "current_evidence": "683 explicitly forbids backfilling the denominator from observed GM alone",
            "status": "guardrail_pass_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "MHA1006_6_theorem_verdict",
            "object": "positive same-frame M_H_ref",
            "needed_for_claim": "integrability, tau/coframe lock, fixed reference, positivity, no orbital-GM import, Poisson/Gauss bridge, universal G, and extra-sector silence all signed",
            "current_evidence": "not enough parent Hamiltonian/source geometry to promote denominator",
            "status": "fail_current_claim",
            "valid_for_claim": "false",
        },
    ]


def denominator_schema_rows() -> list[dict[str, str]]:
    return [
        {
            "schema_id": "MHS1006_0_Htau_minus_Href",
            "target": "M_H_ref",
            "formula": "M_H_ref = H_tau[S_link] - H_ref",
            "required_columns": "system_id;H_tau;H_tau_units;H_ref;H_ref_units;M_H_ref;M_H_ref_units;tau_frame_id;coframe_id;boundary_domain;counterterm_convention;source_path;equation_ref;valid_for_claim",
            "acceptance_rule": "finite numeric H_tau and H_ref, positive difference, same units/frame, sourced equation path, valid_for_claim=true",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "MHS1006_1_parent_certificates",
            "target": "denominator theorem certificates",
            "formula": "M_H_ref is claimable only after certificate vector is fully parent-signed",
            "required_columns": "integrability_certificate;tau_lock_certificate;coframe_lock_certificate;fixed_reference_certificate;positivity_certificate;poisson_gauss_certificate;universal_G_certificate;extra_sector_silence_certificate",
            "acceptance_rule": "no MISSING markers and every certificate source path exists",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "MHS1006_2_anti_circularity",
            "target": "GM_orbit/G_ref",
            "formula": "GM_orbit/G_ref is not an M_H_ref source unless Poisson/Gauss/orbital bridge is already derived",
            "required_columns": "not_orbital_GM_imported=true;GM_bridge_certificate_if_used;source_path;equation_ref",
            "acceptance_rule": "empirical GM substitution is rejected as denominator laundering",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "MHS1006_3_component_compatibility",
            "target": "component-bound denominator compatibility",
            "formula": "same M_H_ref must be compatible with 1000-1005 component/vector gates",
            "required_columns": "component_gate_ids;M_H_ref_source_path;frame_match;units_match;no_cancellation_guard",
            "acceptance_rule": "one denominator for all components; no fitted per-component denominator",
            "valid_for_claim": "false",
        },
    ]


def candidate_denominator_rows() -> list[dict[str, str]]:
    base = {
        "system_id": "R10_local_reference_branch",
        "H_tau": "MISSING_H_TAU",
        "H_tau_units": "MISSING_H_TAU_UNITS",
        "H_ref": "MISSING_H_REF",
        "H_ref_units": "MISSING_H_REF_UNITS",
        "M_H_ref": "MISSING_M_H_REF",
        "M_H_ref_units": "MISSING_M_H_REF_UNITS",
        "tau_frame_id": "MISSING_TAU_FRAME_ID",
        "coframe_id": "MISSING_COFRAME_ID",
        "boundary_domain": "MISSING_BOUNDARY_DOMAIN",
        "counterterm_convention": "MISSING_COUNTERTERM_CONVENTION",
        "integrability_certificate": "MISSING_INTEGRABILITY_CERTIFICATE",
        "tau_lock_certificate": "MISSING_TAU_LOCK_CERTIFICATE",
        "coframe_lock_certificate": "MISSING_COFRAME_LOCK_CERTIFICATE",
        "fixed_reference_certificate": "MISSING_FIXED_REFERENCE_CERTIFICATE",
        "positivity_certificate": "MISSING_POSITIVITY_CERTIFICATE",
        "poisson_gauss_certificate": "MISSING_POISSON_GAUSS_CERTIFICATE",
        "universal_G_certificate": "MISSING_UNIVERSAL_G_CERTIFICATE",
        "extra_sector_silence_certificate": "MISSING_EXTRA_SECTOR_SILENCE_CERTIFICATE",
        "GM_orbit": "MISSING_GM_ORBIT",
        "G_ref": "MISSING_G_REF",
        "denominator_source_method": "MISSING_DENOMINATOR_SOURCE_METHOD",
        "not_orbital_GM_imported": "false",
        "source_path": "MISSING_SOURCE_PATH",
        "equation_ref": "MISSING_EQUATION_REF",
        "component_gate_ids": "MISSING_COMPONENT_GATE_IDS",
        "no_cancellation_guard": "MISSING_DENOMINATOR_GUARD",
        "valid_for_claim": "false",
    }
    variants = [
        ("MHC1006_0_missing_Htau", "H_tau is missing"),
        ("MHC1006_1_missing_Href", "H_ref is missing"),
        ("MHC1006_2_missing_same_frame", "tau/coframe/boundary frame ids are missing"),
        ("MHC1006_3_orbital_GM_substitution", "GM_orbit/G_ref substitution is attempted without bridge"),
        ("MHC1006_4_negative_denominator", "H_tau-H_ref is non-positive"),
        ("MHC1006_5_missing_parent_certificates", "parent integrability/tau/coframe/reference/positivity certificates are missing"),
        ("MHC1006_6_live_placeholder", "live denominator row is schema-only and cannot be scored"),
    ]
    rows: list[dict[str, str]] = []
    for row_id, purpose in variants:
        row = {**base, "candidate_id": row_id, "target": "M_H_ref", "purpose": purpose}
        if row_id == "MHC1006_3_orbital_GM_substitution":
            row["GM_orbit"] = "1.0"
            row["G_ref"] = "1.0"
            row["M_H_ref"] = "1.0"
            row["M_H_ref_units"] = "mass"
            row["denominator_source_method"] = "ORBITAL_GM_SUBSTITUTION"
        if row_id == "MHC1006_4_negative_denominator":
            row["H_tau"] = "1.0"
            row["H_tau_units"] = "mass"
            row["H_ref"] = "2.0"
            row["H_ref_units"] = "mass"
            row["M_H_ref"] = "-1.0"
            row["M_H_ref_units"] = "mass"
            row["denominator_source_method"] = "H_TAU_MINUS_H_REF"
        rows.append(row)
    return rows


def is_missing(value: str) -> bool:
    stripped = str(value).strip()
    return not stripped or stripped.upper().startswith("MISSING") or stripped.upper().startswith("SCHEMA_ONLY")


def finite_float(value: str) -> tuple[bool, float | None]:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return False, None
    return math.isfinite(number), number


def path_list_exists(value: str) -> bool:
    if is_missing(value):
        return False
    paths = [item.strip() for item in value.split(";") if item.strip()]
    if not paths:
        return False
    for item in paths:
        path = Path(item)
        if not path.is_absolute():
            path = ROOT / item
        if not path.exists():
            return False
    return True


def evaluate_denominator(row: dict[str, str]) -> dict[str, str]:
    reasons: list[str] = []
    h_tau_ok, h_tau = finite_float(row.get("H_tau", ""))
    h_ref_ok, h_ref = finite_float(row.get("H_ref", ""))
    mhref_ok, mhref = finite_float(row.get("M_H_ref", ""))
    if not h_tau_ok or h_tau is None:
        reasons.append("MISSING_FINITE_H_TAU")
    if not h_ref_ok or h_ref is None:
        reasons.append("MISSING_FINITE_H_REF")
    if h_tau_ok and h_ref_ok and h_tau is not None and h_ref is not None:
        derived = h_tau - h_ref
        if derived <= 0:
            reasons.append("NONPOSITIVE_H_TAU_MINUS_H_REF")
        if mhref_ok and mhref is not None and abs(derived - mhref) > 1e-12 * max(1.0, abs(derived), abs(mhref)):
            reasons.append("M_H_REF_DOES_NOT_MATCH_H_TAU_MINUS_H_REF")
    if not mhref_ok or mhref is None or mhref <= 0:
        reasons.append("MISSING_POSITIVE_SAME_FRAME_M_H_REF")
    if row.get("H_tau_units") != row.get("H_ref_units") or row.get("H_tau_units") != row.get("M_H_ref_units"):
        reasons.append("MISMATCHED_OR_MISSING_DENOMINATOR_UNITS")
    for field in [
        "tau_frame_id",
        "coframe_id",
        "boundary_domain",
        "counterterm_convention",
        "equation_ref",
        "component_gate_ids",
    ]:
        if is_missing(row.get(field, "")):
            reasons.append(f"MISSING_{field.upper()}")
    certificates = [
        "integrability_certificate",
        "tau_lock_certificate",
        "coframe_lock_certificate",
        "fixed_reference_certificate",
        "positivity_certificate",
        "poisson_gauss_certificate",
        "universal_G_certificate",
        "extra_sector_silence_certificate",
    ]
    for field in certificates:
        value = row.get(field, "")
        if is_missing(value):
            reasons.append(f"MISSING_{field.upper()}")
        elif not value.startswith("PARENT_SIGNED_"):
            reasons.append(f"UNSIGNED_{field.upper()}")
    if row.get("denominator_source_method") != "H_TAU_MINUS_H_REF_PARENT_SIGNED":
        reasons.append("DENOMINATOR_METHOD_NOT_PARENT_SIGNED_H_TAU_MINUS_H_REF")
    if row.get("not_orbital_GM_imported") != "true":
        reasons.append("ORBITAL_GM_IMPORT_NOT_EXCLUDED")
    if row.get("denominator_source_method") == "ORBITAL_GM_SUBSTITUTION":
        reasons.append("ORBITAL_GM_SUBSTITUTION_REJECTED_AS_CIRCULAR")
    if not path_list_exists(row.get("source_path", "")):
        reasons.append("MISSING_EXISTING_SOURCE_PATH")
    if row.get("no_cancellation_guard") != "NO_FITTED_ORBITAL_GM_DENOMINATOR":
        reasons.append("MISSING_NO_FITTED_DENOMINATOR_GUARD")
    if row.get("valid_for_claim") != "true":
        reasons.append("VALID_FOR_CLAIM_FALSE")
    computed = "NOT_SCORED"
    if not reasons and h_tau is not None and h_ref is not None:
        computed = f"{h_tau - h_ref:.16e}"
    verdict = "ACCEPT_POSITIVE_SAME_FRAME_MHREF" if not reasons else "REFUSED_MISSING_POSITIVE_SAME_FRAME_MHREF"
    return {
        "runner_id": row["candidate_id"].replace("MHC", "MHR"),
        "candidate_id": row["candidate_id"],
        "target": row["target"],
        "verdict": verdict,
        "score_ready": flag(not reasons),
        "claim_allowed": "false",
        "valid_for_claim": "false",
        "computed_M_H_ref": computed,
        "failure_reasons": ";".join(reasons) if reasons else "none",
        "generated_utc": stamp(),
    }


def denominator_runner_rows(candidates: list[dict[str, str]]) -> list[dict[str, str]]:
    return [evaluate_denominator(row) for row in candidates]


def refusal_ledger_rows(runner: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        {
            "refusal_id": row["runner_id"].replace("MHR", "MRF"),
            "candidate_id": row["candidate_id"],
            "refusal": row["verdict"],
            "why": row["failure_reasons"],
            "required_exit": "finite parent-signed H_tau-H_ref, same tau/coframe/boundary frame, fixed reference, positivity, no orbital-GM import, source path, and equation ref",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        }
        for row in runner
    ]


def claim_gate_rows(runner: list[dict[str, str]], theorem: list[dict[str, str]]) -> list[dict[str, str]]:
    runner_refuses = all(row["verdict"] == "REFUSED_MISSING_POSITIVE_SAME_FRAME_MHREF" for row in runner)
    theorem_fails = any(row["audit_id"] == "MHA1006_6_theorem_verdict" and row["status"] == "fail_current_claim" for row in theorem)
    return [
        {
            "gate_id": "CG1006_0_MHref_positive_same_frame",
            "claim": "M_H_ref is a positive same-frame denominator",
            "gate_pass": "false",
            "reason": "H_tau/H_ref values, integrability, tau/coframe lock, fixed reference, positivity, and source path are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1006_1_orbital_GM_substitution",
            "claim": "GM_orbit/G_ref may fill M_H_ref before a Poisson/Gauss bridge",
            "gate_pass": "false",
            "reason": "orbital GM substitution is explicitly rejected as circular denominator laundering",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1006_2_vector_norm",
            "claim": "||D_ref Delta_ref||_1/M_H_ref can now score",
            "gate_pass": "false",
            "reason": "positive same-frame M_H_ref remains blocked",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1006_3_RC994_0",
            "claim": "RC994_0 residual current passes",
            "gate_pass": "false",
            "reason": "denominator and component vector remain nonclaim",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1006_4_FB554_0_local_GR",
            "claim": "FB554_0/local-GR branch passes",
            "gate_pass": "false",
            "reason": "M_H_ref denominator is not source-backed or parent-signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1006_5_guardrail",
            "claim": "M_H_ref denominator guardrail is installed",
            "gate_pass": flag(runner_refuses and theorem_fails),
            "reason": "theorem is not promoted and all placeholder/shortcut rows are refused",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1006_0_denominator_not_claimed",
            "decision": "do not claim positive same-frame M_H_ref",
            "reason": "the denominator is structurally identified but not parent-signed or source-filled",
            "effect": "vector norm, RC994_0, and local-GR remain blocked",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1006_1_orbital_GM_forbidden",
            "decision": "reject GM_orbit/G_ref as a denominator source until the bridge is derived",
            "reason": "using orbital GM now would borrow Newton to prove the Newton/local-GR source normalization",
            "effect": "future rows must show H_tau-H_ref or a parent-signed Poisson/Gauss bridge first",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1006_2_next_integrability_target",
            "decision": "move to H_tau integrability and fixed-reference theorem",
            "reason": "integrability/reference lock is the first upstream certificate needed for any M_H_ref value",
            "effect": "1007 should try to sign delta H_tau or stage a sharper symplectic/reference residual row",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1007-Y5-R10-Htau-integrability-fixed-reference-theorem-or-symplectic-residual-row.md",
            "objective": "derive integrable H_tau with fixed H_ref, or stage a strict symplectic/reference residual row without claiming a denominator",
            "include": "delta H_tau, Q_tau, theta, fixed H_ref, boundary/counterterm convention, tau lock, source/equation paths, compatibility with M_H_ref",
            "exclude": "EH import without MTS parent theta, fitted reference, orbital GM substitution, M_H_ref pass, RC994_0 pass, FB554_0 pass, local-GR claim, GitHub action",
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
    theorem: list[dict[str, str]],
    schema: list[dict[str, str]],
    candidates: list[dict[str, str]],
    runner: list[dict[str, str]],
    refusals: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    theorem_ok = any(row["audit_id"] == "MHA1006_6_theorem_verdict" and row["status"] == "fail_current_claim" for row in theorem) and all(row["valid_for_claim"] == "false" for row in theorem)
    schema_ok = any(row["schema_id"] == "MHS1006_0_Htau_minus_Href" for row in schema) and any(row["schema_id"] == "MHS1006_2_anti_circularity" for row in schema)
    candidates_ok = len(candidates) >= 7 and all(row["valid_for_claim"] == "false" for row in candidates)
    runner_ok = all(row["verdict"] == "REFUSED_MISSING_POSITIVE_SAME_FRAME_MHREF" and row["score_ready"] == "false" for row in runner)
    orbital_reject_ok = any(
        row["candidate_id"] == "MHC1006_3_orbital_GM_substitution"
        and "ORBITAL_GM_SUBSTITUTION_REJECTED_AS_CIRCULAR" in row["failure_reasons"]
        for row in runner
    )
    positivity_ok = any("MISSING_POSITIVE_SAME_FRAME_M_H_REF" in row["failure_reasons"] or "NONPOSITIVE_H_TAU_MINUS_H_REF" in row["failure_reasons"] for row in runner)
    refusals_ok = len(refusals) == len(runner) and all(row["claim_allowed"] == "false" for row in refusals)
    claims_ok = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in claims)
    mhref_gate_ok = any(row["gate_id"] == "CG1006_0_MHref_positive_same_frame" and row["gate_pass"] == "false" for row in claims)
    decisions_ok = any(row["decision_id"] == "DEC1006_2_next_integrability_target" for row in decisions)
    next_ok = bool(next_target) and next_target[0]["valid_for_claim"] == "false"
    formalization_count = formalization_changed_after_start()
    checks = [
        {"check_id": "V1006_0_sources_exist", "result": "pass" if sources_ok else "fail", "detail": "all source paths exist and needles are present"},
        {"check_id": "V1006_1_theorem_audit_nonclaim", "result": "pass" if theorem_ok else "fail", "detail": "positive same-frame M_H_ref theorem remains blocked rather than promoted"},
        {"check_id": "V1006_2_schema_ready", "result": "pass" if schema_ok else "fail", "detail": "H_tau-H_ref and anti-circularity schema rows are present"},
        {"check_id": "V1006_3_candidate_rows_nonclaim", "result": "pass" if candidates_ok else "fail", "detail": "candidate denominator rows remain valid_for_claim=false"},
        {"check_id": "V1006_4_runner_refuses_placeholders", "result": "pass" if runner_ok else "fail", "detail": "runner refuses every current denominator placeholder/shortcut row"},
        {"check_id": "V1006_5_orbital_GM_rejected", "result": "pass" if orbital_reject_ok else "fail", "detail": "orbital GM substitution is refused as circular"},
        {"check_id": "V1006_6_positivity_guard", "result": "pass" if positivity_ok else "fail", "detail": "positive H_tau-H_ref is demanded"},
        {"check_id": "V1006_7_refusal_ledger_nonclaim", "result": "pass" if refusals_ok else "fail", "detail": "refusal ledger mirrors runner and keeps claims false"},
        {"check_id": "V1006_8_claim_gates_blocked", "result": "pass" if claims_ok else "fail", "detail": "M_H_ref, vector, RC994_0, and local-GR claims stay blocked"},
        {"check_id": "V1006_9_MHref_gate_written", "result": "pass" if mhref_gate_ok else "fail", "detail": "M_H_ref gate is present and blocked"},
        {"check_id": "V1006_10_decision_written", "result": "pass" if decisions_ok else "fail", "detail": "H_tau integrability target decision is written"},
        {"check_id": "V1006_11_next_target_written", "result": "pass" if next_ok else "fail", "detail": "1007 target row is present and nonclaim"},
        {"check_id": "V1006_12_formalization_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization-workbench modified-file count since script start is {formalization_count}"},
    ]
    ready = all(row["result"] == "pass" for row in checks)
    checks.append(
        {
            "check_id": "V1006_SUMMARY",
            "result": "pass" if ready else "fail",
            "detail": "1006 M_H_ref positive same-frame denominator validation summary",
            "generated_utc": stamp(),
        }
    )
    for row in checks:
        row.setdefault("generated_utc", stamp())
    return checks


def write_doc(
    sources: list[dict[str, str]],
    theorem: list[dict[str, str]],
    schema: list[dict[str, str]],
    candidates: list[dict[str, str]],
    runner: list[dict[str, str]],
    refusals: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> None:
    lines = [
        "# 1006 Y5 R10 MHref Positive Same-Frame Denominator Or Htau Source Row",
        "",
        "**Status:** positive same-frame M_H_ref theorem attempted, not closed; strict denominator source row staged as nonclaim.",
        "",
        "**Claim ceiling:** this checkpoint does not claim M_H_ref, vector norm, RC994_0, FB554_0, R10, PPN, WEP, clock, orbital, or local-GR pass.",
        "",
        "## Source Register",
        "",
        md_table(sources, ["source_id", "path", "role", "needle", "exists", "needle_found", "valid_for_claim"]),
        "",
        "## MHref Denominator Theorem Audit",
        "",
        md_table(theorem, ["audit_id", "object", "needed_for_claim", "current_evidence", "status", "valid_for_claim"]),
        "",
        "## Denominator Source Schema",
        "",
        md_table(schema, ["schema_id", "target", "formula", "required_columns", "acceptance_rule", "valid_for_claim"]),
        "",
        "## Candidate Denominator Template",
        "",
        md_table(candidates, ["candidate_id", "purpose", "target", "H_tau", "H_ref", "M_H_ref", "denominator_source_method", "not_orbital_GM_imported", "source_path", "valid_for_claim"]),
        "",
        "## Denominator Runner",
        "",
        md_table(runner, ["runner_id", "candidate_id", "verdict", "score_ready", "claim_allowed", "computed_M_H_ref", "failure_reasons", "generated_utc"]),
        "",
        "## Refusal Ledger",
        "",
        md_table(refusals, ["refusal_id", "candidate_id", "refusal", "why", "required_exit", "claim_allowed", "valid_for_claim"]),
        "",
        "## Claim Gate",
        "",
        md_table(claims, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
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
    sources = source_register_rows()
    theorem = mhref_theorem_audit_rows()
    schema = denominator_schema_rows()
    candidates = candidate_denominator_rows()
    runner = denominator_runner_rows(candidates)
    refusals = refusal_ledger_rows(runner)
    claims = claim_gate_rows(runner, theorem)
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, theorem, schema, candidates, runner, refusals, claims, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_1006_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_1006_MHREF_DENOMINATOR_THEOREM_AUDIT.csv", theorem)
    write_csv(OUT / "P8_Y5_R10_1006_DENOMINATOR_SOURCE_SCHEMA.csv", schema)
    write_csv(OUT / "P8_Y5_R10_1006_CANDIDATE_DENOMINATOR_TEMPLATE.csv", candidates)
    write_csv(OUT / "P8_Y5_R10_1006_DENOMINATOR_RUNNER.csv", runner)
    write_csv(OUT / "P8_Y5_R10_1006_REFUSAL_LEDGER.csv", refusals)
    write_csv(OUT / "P8_Y5_R10_1006_CLAIM_GATE.csv", claims)
    write_csv(OUT / "P8_Y5_R10_1006_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_1006_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_1006_VALIDATION.csv", validation)
    write_doc(sources, theorem, schema, candidates, runner, refusals, claims, decisions, validation, next_target)


if __name__ == "__main__":
    main()
