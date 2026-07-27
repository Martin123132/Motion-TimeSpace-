from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3138_QOBS_REP_INPUTS.csv"
CONSTRUCTION = OUT / "P8_Y5_R2FR_3138_TYPED_QOBS_CONSTRUCTION.csv"
CERTIFICATE = OUT / "P8_Y5_R2FR_3138_REP_QOBS_CERTIFICATE_MATRIX.csv"
FALLBACK = OUT / "P8_Y5_R2FR_3138_QOBS_REP_FALLBACK_ROWS.csv"
GATE = OUT / "P8_Y5_R2FR_3138_GATE.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3138_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
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


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path_text


def input_rows() -> list[dict[str, Any]]:
    sources = [
        ("SRC3138_0", "3137_material_constants", "3137-Y5-R2FR-material-constant-superselection-owner-under-AX1090.md", "material constants require Rep(Q_obs) owner"),
        ("SRC3138_1", "3137_theorem", "source-intake\\mts_residuals\\P8_Y5_R2FR_3137_MATERIAL_STANDARD_SUPERSELECTION_THEOREM.csv", "Rep(Q_obs) theorem reduction"),
        ("SRC3138_2", "945_q_candidate", "945-Y5-R10-parent-q-map-Obs-e-functor-construction-or-first-frame-leak-bound-pack.md", "candidate q map and projection-by-declaration trap"),
        ("SRC3138_3", "945_qmap_rows", "source-intake\\mts_residuals\\P8_Y5_R10_945_Q_MAP_CANDIDATE_CONSTRUCTION.csv", "q_candidate construction rows"),
        ("SRC3138_4", "945_obs_rows", "source-intake\\mts_residuals\\P8_Y5_R10_945_OBS_E_FUNCTOR_AUDIT.csv", "Obs_e functor audit"),
        ("SRC3138_5", "946_kernel_audit", "source-intake\\mts_residuals\\P8_Y5_R10_946_KERNEL_CERTIFICATE_AUDIT.csv", "kernel certificate failure rows"),
        ("SRC3138_6", "946_bound_interface", "source-intake\\mts_residuals\\P8_Y5_R10_946_CG_BA_BOUND_INTERFACE.csv", "c_g/b_A fallback interface"),
        ("SRC3138_7", "623_coframe_functor", "source-intake\\mts_residuals\\P8_Y5_R10_623_COFRAME_FUNCTOR_THEOREM_ATTEMPT.csv", "coframe functor conditional lemma"),
        ("SRC3138_8", "622_parent_matter_contract", "source-intake\\mts_residuals\\P8_Y5_R10_622_PARENT_MATTER_CONTRACT.csv", "parent matter contract clauses"),
        ("SRC3138_9", "711_descent_audit", "source-intake\\mts_residuals\\P8_Y5_R10_711_QUOTIENT_DESCENT_DERIVATION_AUDIT.csv", "quotient descent audit"),
        ("SRC3138_10", "898_matter_descent", "source-intake\\mts_residuals\\P8_Y5_R10_898_MATTER_DESCENT_SIGNATURE.csv", "matter descent signature"),
        ("SRC3138_11", "3134_reduction", "source-intake\\mts_residuals\\P8_Y5_R2FR_3134_PROOF_REDUCTION_MATRIX.csv", "q and matter pullback reduction"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, role, source_file, evidence_use in sources:
        path = source_path(source_file)
        rows.append(
            {
                "source_id": source_id,
                "role": role,
                "source_file": source_file,
                "resolved_path": str(path),
                "exists": str(path.exists()).lower(),
                "row_count": len(read_csv(path)) if path.exists() and path.suffix.lower() == ".csv" else "",
                "evidence_use": evidence_use,
                "valid_for_claim": "false",
            }
        )
    return rows


def construction_rows() -> list[dict[str, Any]]:
    now = stamp()
    rows = [
        (
            "QOBS3138_0_parent_config",
            "Phi_parent",
            "parent configuration before quotient",
            "fields include candidate observed geometry, relation/topological data, cell orbit data, boundary/domain data, matter fields, and representation labels",
            "inventory_only_not_parent_action",
            "field inventory still needs variational action and kernel certificate",
        ),
        (
            "QOBS3138_1_typed_Qobs",
            "Q_obs",
            "typed quotient observable object",
            "Q_obs=(M,e_obs mod local Lorentz,omega_obs if owned,[C]_PD,Orbit_27(h),[J_rel]_local,boundary_class,Rep_labels)",
            "candidate_object_written",
            "including e_obs as a quotient coordinate is allowed only if ker(Dq) is proved gauge/null",
        ),
        (
            "QOBS3138_2_q_map",
            "q: Phi_parent -> Q_obs",
            "candidate quotient map",
            "q(Phi) forgets representative fibre data, material markers, Weyl/disformal frame choices, source labels, and boundary tails unless owned in Q_obs",
            "candidate_map_written_not_signed",
            "forgetting is physical only if forgotten directions are presymplectic-null and matter-invisible",
        ),
        (
            "QOBS3138_3_Obs_e",
            "Obs_e: Q_obs -> Coframe/Lorentz",
            "observed coframe functor",
            "Obs_e(Q_obs)=e_obs up to local Lorentz gauge",
            "formal_functor_written",
            "projection-by-declaration unless parent proves e_obs is the only matter-visible coframe",
        ),
        (
            "QOBS3138_4_Rep_Qobs",
            "Rep(Q_obs)",
            "ordinary matter representation category over Q_obs",
            "objects are (Psi_A,theta_A) where theta_A are fixed representation/superselection labels, not parent fields",
            "candidate_rep_category_written",
            "must forbid marker-indexed representation choice theta_A(marker,Xhat)",
        ),
        (
            "QOBS3138_5_matter_functor",
            "S_matter over Rep(Q_obs)",
            "matter action descent target",
            "S_matter=sum_A S_A[Psi_A,Obs_e(Q_obs),omega[Obs_e],theta_A]",
            "conditional_chain_rule_ready",
            "parent action has not signed this as the only ordinary matter coupling",
        ),
        (
            "QOBS3138_6_source_functor",
            "F_src over Q_obs",
            "source current readout target",
            "F_src(T_H)=kappa_univ T_H after source-label forgetting",
            "candidate_source_functor_written",
            "labelled source countermodel F_src({(T_A,A)})=sum_A kappa_A T_A remains legal",
        ),
        (
            "QOBS3138_7_verdict",
            "q_to_Obs_e_to_Rep",
            "construction verdict",
            "typed construction is coherent and useful, but not parent-signed",
            "typed_candidate_only_no_claim",
            "kernel certificate and no-marker/EM/source-label clauses still block promotion",
        ),
    ]
    return [
        {
            "construction_id": row_id,
            "object": obj,
            "role": role,
            "mathematical_form": form,
            "current_status": status,
            "failure_if_used_as_proof": failure,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for row_id, obj, role, form, status, failure in rows
    ]


def certificate_rows() -> list[dict[str, Any]]:
    now = stamp()
    rows = [
        ("CERT3138_0_kernel_null", "ker(Dq) is presymplectic-null", "i_v Omega_parent=0 and i_v Theta_parent=dB_v with zero compact flux", "failed_current_corpus", "946 KCERT rows fail total certificate"),
        ("CERT3138_1_no_projection_trap", "e_obs is not merely inserted into q", "e_obs must be parent-owned and all omitted frame directions must be gauge/null", "open_guard_active", "945 explicitly warns projection-by-declaration"),
        ("CERT3138_2_coframe_functor", "Obs_e is the only matter-visible coframe functor up to local Lorentz gauge", "all matter frames factor through Q_obs or are retained residuals", "conditional_not_signed", "623/945 retain Weyl/disformal counterexamples"),
        ("CERT3138_3_rep_labels", "theta_A are fixed representation labels of Rep(Q_obs)", "Lie_v theta_A=0 and no marker-indexed choices", "conditional_not_signed", "3137 retained marker-dependent constants as countermodels"),
        ("CERT3138_4_matter_action", "ordinary matter action descends to Rep(Q_obs)", "S_matter=sum_A S_A[Psi_A,Obs_e(Q_obs),theta_A]", "conditional_not_signed", "622/898 keep matter functor and geometry stack unsigned"),
        ("CERT3138_5_source_label_forgetting", "source functor forgets species labels", "F_src(T_H)=kappa_univ T_H", "conditional_countermodel_retained", "953 labelled additive source functor remains legal"),
        ("CERT3138_6_boundary_no_tail", "vertical variations have no boundary/source tail", "Pi_local dB_v=0 and no post-readout EFT counterterm", "not_signed", "946/898 retain boundary/EFT tails"),
        ("CERT3138_7_total", "Q_obs and Rep(Q_obs) are parent-owned", "CERT3138_0 through CERT3138_6 all pass in one parent branch", "not_claim_ready", "typed construction exists but certificate package fails"),
    ]
    return [
        {
            "certificate_id": row_id,
            "required_clause": clause,
            "mathematical_requirement": requirement,
            "current_status": status,
            "blocking_evidence": evidence,
            "passes_certificate": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for row_id, clause, requirement, status, evidence in rows
    ]


def fallback_rows() -> list[dict[str, Any]]:
    now = stamp()
    rows = [
        ("QRF3138_0_cg", "c_g/b_g", "representative Weyl/common-frame leakage if Obs_e uniqueness/factorization fails", "R10;PPN;WEP;clock", "MISSING_PARENT_ZERO_OR_NUMERIC_CG"),
        ("QRF3138_1_b_dis", "b_dis", "representative disformal matter-frame leakage", "PPN;preferred-frame;clock", "MISSING_DISFORMAL_ZERO_OR_NUMERIC_BOUND"),
        ("QRF3138_2_b_clock", "b_clock", "marker/representative derivative of material clock transition", "clock/redshift/alpha drift", "MISSING_REP_LABEL_CLOCK_STANDARD_ZERO_OR_BOUND"),
        ("QRF3138_3_b_alpha", "b_alpha", "alpha_EM derivative if EM-lock/Rep(Q_obs) fails", "clock;WEP;R10;EM stress", "MISSING_EM_LOCK_ZERO_OR_ALPHA_PRODUCT_INPUT"),
        ("QRF3138_4_Delta_kappa_AB", "Delta_kappa_AB", "relative source weight if source labels survive", "WEP;Newton/source normalization", "MISSING_LABEL_FORGETTING_OR_FINITE_SOURCE_WEIGHT_BOUND"),
        ("QRF3138_5_q_nonH", "q_nonH", "non-Hilbert or boundary source projection", "R10;PPN;source normalization", "MISSING_NONHILBERT_ZERO_FLUX_OR_NUMERIC_SOURCE"),
        ("QRF3138_6_Delta_W_support", "Delta_W_support", "source support shift under observed frame choices", "orbital;local_GR", "MISSING_SUPPORT_EQUIVALENCE_OR_NUMERIC_BOUND"),
    ]
    return [
        {
            "fallback_id": row_id,
            "symbol": symbol,
            "definition": definition,
            "observable_link": observable,
            "current_status": status,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "next_action": "prove parent zero certificate or provide source-backed finite coefficient/projection",
            "generated_utc": now,
        }
        for row_id, symbol, definition, observable, status in rows
    ]


def gate_rows(certificates: list[dict[str, Any]], fallbacks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    now = stamp()
    failed = sum(1 for row in certificates if row["passes_certificate"] == "false")
    missing = sum(1 for row in fallbacks if "MISSING" in row["current_status"])
    return [
        {
            "gate_id": "QRG3138_0_typed_construction",
            "gate": "q_to_Obs_e_to_Rep_candidate",
            "status": "typed_candidate_written",
            "claim_allowed": "false",
            "reason": "Q_obs, Obs_e, and Rep(Q_obs) can be typed coherently.",
            "next_action": "prove kernel/null and matter-invisibility certificates.",
            "generated_utc": now,
        },
        {
            "gate_id": "QRG3138_1_parent_ownership",
            "gate": "parent_owned_Qobs_Rep",
            "status": "fail_for_claim",
            "claim_allowed": "false",
            "reason": f"{failed} certificate rows remain unpassed; typed object is not a parent quotient proof.",
            "next_action": "attack kernel null/no-marker/source-label certificates or use finite fallback rows.",
            "generated_utc": now,
        },
        {
            "gate_id": "QRG3138_2_residual_fallback",
            "gate": "finite_residual_interface",
            "status": "active_nonclaim",
            "claim_allowed": "false",
            "reason": f"{missing} fallback rows remain missing source-backed values or theorem-zero proofs.",
            "next_action": "first fallback row should be c_g/b_g or b_clock depending on whether geometry or constants route is attacked next.",
            "generated_utc": now,
        },
        {
            "gate_id": "QRG3138_3_total",
            "gate": "local_GR_Newton_clock_source_readout",
            "status": "not_claim_ready",
            "claim_allowed": "false",
            "reason": "typed quotient helps the spine but does not close source mass, Newton, PPN, EM, or local-GR claims.",
            "next_action": "3139 should target kernel null certificate or unique Maxwell F2 inheritance.",
            "generated_utc": now,
        },
    ]


def validation_rows(inputs: list[dict[str, Any]], constructions: list[dict[str, Any]], certificates: list[dict[str, Any]], fallbacks: list[dict[str, Any]], gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    now = stamp()
    all_sources = all(row["exists"] == "true" for row in inputs)
    required_objects = {"Q_obs", "q: Phi_parent -> Q_obs", "Obs_e: Q_obs -> Coframe/Lorentz", "Rep(Q_obs)"}
    object_set = {row["object"] for row in constructions}
    no_claim = all(str(row.get("claim_allowed", "")).lower() == "false" and str(row.get("valid_for_claim", "false")).lower() == "false" for row in constructions + certificates + fallbacks)
    gates_no_claim = all(str(row.get("claim_allowed", "")).lower() == "false" for row in gates)
    certificate_fail_retained = any(row["certificate_id"] == "CERT3138_7_total" and row["current_status"] == "not_claim_ready" for row in certificates)
    fallback_missing = all("MISSING" in row["current_status"] for row in fallbacks)
    return [
        {
            "check_id": "VAL3138_0_sources_exist",
            "status": "pass" if all_sources else "fail",
            "details": json.dumps({row["source_id"]: {"exists": row["exists"], "path": row["resolved_path"]} for row in inputs}, ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3138_1_typed_objects_present",
            "status": "pass" if required_objects.issubset(object_set) else "fail",
            "details": json.dumps(sorted(object_set), ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3138_2_certificate_failure_retained",
            "status": "pass" if certificate_fail_retained else "fail",
            "details": f"certificate_rows={len(certificates)}",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3138_3_fallback_rows_missing_nonclaim",
            "status": "pass" if fallback_missing and len(fallbacks) >= 7 else "fail",
            "details": json.dumps([row["symbol"] for row in fallbacks], ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3138_4_no_claim_leak",
            "status": "pass" if no_claim and gates_no_claim else "fail",
            "details": "",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def main() -> None:
    inputs = input_rows()
    constructions = construction_rows()
    certificates = certificate_rows()
    fallbacks = fallback_rows()
    gates = gate_rows(certificates, fallbacks)
    validations = validation_rows(inputs, constructions, certificates, fallbacks, gates)
    write_csv(INPUTS, inputs)
    write_csv(CONSTRUCTION, constructions)
    write_csv(CERTIFICATE, certificates)
    write_csv(FALLBACK, fallbacks)
    write_csv(GATE, gates)
    write_csv(VALIDATION, validations)


if __name__ == "__main__":
    main()

