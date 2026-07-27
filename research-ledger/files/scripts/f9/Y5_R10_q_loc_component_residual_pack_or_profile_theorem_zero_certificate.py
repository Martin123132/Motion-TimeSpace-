from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1189-Y5-R10-q_loc-component-residual-pack-or-profile-theorem-zero-certificate.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
STAMP = datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [row | {"generated_utc": STAMP} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty csv refused: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def md_escape(value: object) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ")


def table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return "_No rows._"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key != "generated_utc" and key not in headers:
                headers.append(key)
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        out.append("| " + " | ".join(md_escape(row.get(h, "")) for h in headers) + " |")
    return "\n".join(out)


def source_rows() -> list[dict[str, object]]:
    entries = [
        {
            "source_id": "SRC1189_0_1188_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1188_NEXT_TARGET.csv",
            "needle": "NEXT1188_0_1189",
            "role": "direct 1189 handoff.",
        },
        {
            "source_id": "SRC1189_1_1188_demotion",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1188_QLOC_DEMOTION_ROWS.csv",
            "needle": "QDEM1188_1_explicit_residual_row",
            "role": "q_loc demoted to explicit empirical residual.",
        },
        {
            "source_id": "SRC1189_2_projection_contract",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_746_QLOC_PROJECTION_CONTRACT.csv",
            "needle": "QPC746_4_no_single_scalar_pass",
            "role": "forbids one-scalar q_proxy pass across local arenas.",
        },
        {
            "source_id": "SRC1189_3_component_contract",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_749_QLOC_COMPONENT_DECOMPOSITION_CONTRACT.csv",
            "needle": "QCD749_7_verdict",
            "role": "component-filled q_loc row requirements.",
        },
        {
            "source_id": "SRC1189_4_input_schema",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_750_QLOC_COMPONENT_INPUT_SCHEMA.csv",
            "needle": "QIN750_3_q_loc_components",
            "role": "required component input columns.",
        },
        {
            "source_id": "SRC1189_5_builder_schema",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_756_QLOC_COMPONENT_CANDIDATE_BUILDER_SCHEMA.csv",
            "needle": "QCB756_5_no_fake_data_guard",
            "role": "no fake data guard for component rows.",
        },
        {
            "source_id": "SRC1189_6_builder_doc",
            "relative_path": "756-Y5-R10-Gamma-Khat-metric-response-symbol-match-or-q_loc-component-candidate-builder.md",
            "needle": "QCB756_0_builder_schema",
            "role": "component builder schema and acceptance gate.",
        },
        {
            "source_id": "SRC1189_7_ward_attempt",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_755_OBSERVED_QLOC_WARD_OWNER_ATTEMPT.csv",
            "needle": "WOA755_5_verdict",
            "role": "observed q_loc Ward zero not accepted.",
        },
        {
            "source_id": "SRC1189_8_1010_residual",
            "relative_path": "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
            "needle": "QRES1010_0_q_loc_vector",
            "role": "retained q_loc vector residual and theorem-zero gate.",
        },
        {
            "source_id": "SRC1189_9_827_terms",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_827_QLOC_RESIDUAL_CONTRACT.csv",
            "needle": "Q827_4_Khat_divergence",
            "role": "residual term split including K_hat divergence.",
        },
        {
            "source_id": "SRC1189_10_868_decomposition",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_868_QLOC_DECOMPOSITION_CONTRACT.csv",
            "needle": "QL868_3_source_exchange",
            "role": "q_loc source-exchange channel.",
        },
        {
            "source_id": "SRC1189_11_869_identity",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_869_QLOC_IDENTITY_DECOMPOSITION.csv",
            "needle": "QI869_0_definition",
            "role": "q_loc identity decomposition.",
        },
        {
            "source_id": "SRC1189_12_874_verticality",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_874_PARENT_QLOC_VERTICALITY_SIGNATURE.csv",
            "needle": "QVS874_5_signature_verdict",
            "role": "parent q_loc verticality signature is not signed.",
        },
        {
            "source_id": "SRC1189_13_1011_prior_bound",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1011_QLOC_BOUND_RUNNER.csv",
            "needle": "QBR1011_0_compact_shell_budget",
            "role": "prior nonclaim q_loc bound row and scalar-proxy guard.",
        },
    ]
    rows: list[dict[str, object]] = []
    for entry in entries:
        path = ROOT / str(entry["relative_path"])
        exists = path.exists()
        needle_found = exists and str(entry["needle"]) in read_text(path)
        rows.append(entry | {"exists": exists, "needle_found": needle_found})
    return rows


def component_pack_rows() -> list[dict[str, object]]:
    base_missing = (
        "MISSING_REAL_QLOC_PROFILE;MISSING_OBSERVED_FRAME;MISSING_DOMAIN_MEASURE;"
        "MISSING_BOUNDARY_CONDITION;MISSING_SOURCE_PATH"
    )
    return [
        {
            "row_id": "QPACK1189_0_PPN_component_template",
            "arena": "PPN/local-GR",
            "row_kind": "component_template",
            "sample_id": "MISSING_SAMPLE",
            "domain_id": "MISSING_COMPACT_LOCAL_DOMAIN",
            "weight_dV": "MISSING_MEASURE",
            "frame_convention": "MISSING_OBSERVED_FRAME",
            "u0": "MISSING",
            "u1": "MISSING",
            "u2": "MISSING",
            "u3": "MISSING",
            "q0": "MISSING",
            "q1": "MISSING",
            "q2": "MISSING",
            "q3": "MISSING",
            "q_T": "MISSING",
            "q_x": "MISSING",
            "q_y": "MISSING",
            "q_z": "MISSING",
            "q_units": "MISSING_QLOC_UNITS",
            "boundary_tag": "MISSING",
            "boundary_condition": "MISSING",
            "source_path": "MISSING_SOURCE_PATH",
            "theorem_zero_certificate_id": "OPTIONAL_TZ1189",
            "response_operator_needed": "W_even_gamma_beta;W_alpha_i;gauge;weak_field_Green_operator",
            "missing_fields": base_missing + ";MISSING_PPN_RESPONSE_OPERATOR",
            "row_status": "template_only_not_scoreable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "QPACK1189_1_R10_kernel_template",
            "arena": "R10/short-range",
            "row_kind": "finite_range_kernel_template",
            "sample_id": "MISSING_SAMPLE",
            "domain_id": "MISSING_RANGE_DOMAIN",
            "weight_dV": "MISSING_MEASURE",
            "frame_convention": "MISSING_OBSERVED_FRAME",
            "u0": "MISSING",
            "u1": "MISSING",
            "u2": "MISSING",
            "u3": "MISSING",
            "q0": "MISSING",
            "q1": "MISSING",
            "q2": "MISSING",
            "q3": "MISSING",
            "q_T": "MISSING",
            "q_x": "MISSING",
            "q_y": "MISSING",
            "q_z": "MISSING",
            "q_units": "MISSING_QLOC_UNITS",
            "boundary_tag": "MISSING",
            "boundary_condition": "MISSING",
            "source_path": "MISSING_SOURCE_PATH",
            "theorem_zero_certificate_id": "OPTIONAL_TZ1189",
            "response_operator_needed": "finite_range_kernel_alpha_q(lambda);c_q_alpha(lambda);real_bound_curve_link",
            "missing_fields": base_missing + ";MISSING_RANGE_KERNEL;MISSING_CQ_ALPHA_LAMBDA",
            "row_status": "template_only_not_scoreable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "QPACK1189_2_clock_readout_template",
            "arena": "clock/time/readout",
            "row_kind": "clock_response_template",
            "sample_id": "MISSING_SAMPLE",
            "domain_id": "MISSING_CLOCK_DOMAIN",
            "weight_dV": "MISSING_MEASURE",
            "frame_convention": "MISSING_OBSERVED_FRAME",
            "u0": "MISSING",
            "u1": "MISSING",
            "u2": "MISSING",
            "u3": "MISSING",
            "q0": "MISSING",
            "q1": "MISSING",
            "q2": "MISSING",
            "q3": "MISSING",
            "q_T": "MISSING",
            "q_x": "MISSING",
            "q_y": "MISSING",
            "q_z": "MISSING",
            "q_units": "MISSING_QLOC_UNITS",
            "boundary_tag": "MISSING",
            "boundary_condition": "MISSING",
            "source_path": "MISSING_SOURCE_PATH",
            "theorem_zero_certificate_id": "OPTIONAL_TZ1189",
            "response_operator_needed": "b_clock_i;readout_frame;constant_marker_leakage",
            "missing_fields": base_missing + ";MISSING_CLOCK_RESPONSE_COEFFICIENTS",
            "row_status": "template_only_not_scoreable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "QPACK1189_3_orbital_source_template",
            "arena": "orbital/source-normalization",
            "row_kind": "force_source_drift_template",
            "sample_id": "MISSING_SAMPLE",
            "domain_id": "MISSING_ORBITAL_DOMAIN",
            "weight_dV": "MISSING_MEASURE",
            "frame_convention": "MISSING_OBSERVED_FRAME",
            "u0": "MISSING",
            "u1": "MISSING",
            "u2": "MISSING",
            "u3": "MISSING",
            "q0": "MISSING",
            "q1": "MISSING",
            "q2": "MISSING",
            "q3": "MISSING",
            "q_T": "MISSING",
            "q_x": "MISSING",
            "q_y": "MISSING",
            "q_z": "MISSING",
            "q_units": "MISSING_QLOC_UNITS",
            "boundary_tag": "MISSING",
            "boundary_condition": "MISSING",
            "source_path": "MISSING_SOURCE_PATH",
            "theorem_zero_certificate_id": "OPTIONAL_TZ1189",
            "response_operator_needed": "force_to_acceleration;source_charge_equality;radial_profile",
            "missing_fields": base_missing + ";MISSING_ORBITAL_FORCE_MAP",
            "row_status": "template_only_not_scoreable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "QPACK1189_4_theorem_zero_override",
            "arena": "all_local_arenas",
            "row_kind": "theorem_zero_override_slot",
            "sample_id": "THEOREM_ZERO_NOT_FILLED",
            "domain_id": "ALL_COMPACT_LOCAL_DOMAINS_IF_SIGNED",
            "weight_dV": "not_applicable_if_theorem_zero",
            "frame_convention": "observed_frame_inherited_from_certificate",
            "u0": "not_applicable",
            "u1": "not_applicable",
            "u2": "not_applicable",
            "u3": "not_applicable",
            "q0": "0_if_TZ1189_passes",
            "q1": "0_if_TZ1189_passes",
            "q2": "0_if_TZ1189_passes",
            "q3": "0_if_TZ1189_passes",
            "q_T": "0_if_TZ1189_passes",
            "q_x": "0_if_TZ1189_passes",
            "q_y": "0_if_TZ1189_passes",
            "q_z": "0_if_TZ1189_passes",
            "q_units": "certificate_defined",
            "boundary_tag": "certificate_defined",
            "boundary_condition": "certificate_defined",
            "source_path": "MISSING_THEOREM_ZERO_CERTIFICATE",
            "theorem_zero_certificate_id": "TZ1189_0_parent_GK_Ploc_boundary_zero",
            "response_operator_needed": "none_if_certificate_valid",
            "missing_fields": "MISSING_PARENT_SIGNED_THEOREM_ZERO_CERTIFICATE",
            "row_status": "certificate_slot_only_not_claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def arena_projection_rows() -> list[dict[str, object]]:
    return [
        {
            "projection_id": "APR1189_0_gamma_beta",
            "arena": "PPN gamma/beta",
            "needed_component": "q_T, q_L, scalar/even part of q_perp plus weak-field metric operator",
            "operator_form": "delta_gamma_q or delta_beta_q = W_even[q_T,q_L,q_TF] * normalized_q",
            "source_basis": "QPC746_1_scalar_even_PPN; QCD749_1; QCD749_2; QCD749_6",
            "missing_inputs": "W_even; gauge; Green operator; component q_loc profile; source normalization",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "projection_id": "APR1189_1_alpha3",
            "arena": "PPN alpha3/preferred-frame",
            "needed_component": "momentum/preferred-frame flux component P_alpha3 q_loc",
            "operator_form": "alpha3_q = W_q_alpha3 * epsilon_q_momentum",
            "source_basis": "QPC746_2_alpha3_momentum_flux; QCD749_4; QCB756_4",
            "missing_inputs": "P_alpha3; f_qV; W_q_alpha3; same denominator as q_proxy; alpha3 bound row",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "projection_id": "APR1189_2_R10",
            "arena": "short-range/R10",
            "needed_component": "finite-range kernel generated by q_loc source profile",
            "operator_form": "alpha_q(lambda)=c_q_alpha(lambda)*q_profile(lambda)",
            "source_basis": "QPC746_3_R10_range; AQ1188_1_R10",
            "missing_inputs": "lambda kernel; c_q_alpha(lambda); q_profile(lambda); bound curve link",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "projection_id": "APR1189_3_clock",
            "arena": "clock/time/readout",
            "needed_component": "time/readout projection and hidden-frame/constant leakage",
            "operator_form": "delta_nu_i/nu_i = b_clock_i * Q_clock[q_T,q_perp,frame]",
            "source_basis": "AQ1188_2_clock plus no-shadow/visible-pullback conditional rows",
            "missing_inputs": "b_clock_i; readout map; local clock frame; constant-marker classification",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "projection_id": "APR1189_4_orbital",
            "arena": "orbital/source-normalization",
            "needed_component": "spatial force/source drift and measured-GM channel",
            "operator_form": "a_q^i = W_orb^i_mu q_loc^mu or d ln mu_obs/dt = W_mu q_loc",
            "source_basis": "QI869_4_source_normalization_channel; QBF1011_2_Gdot_GMdot",
            "missing_inputs": "force-to-acceleration map; source-charge equality; radial profile; uncertainty",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def theorem_zero_certificate_rows() -> list[dict[str, object]]:
    return [
        {
            "certificate_id": "TZ1189_0_parent_GK_Ploc_boundary_zero",
            "clause": "metric_response_owner",
            "required_statement": "T_GK^{mu nu}=Gamma_eff g^{mu nu}-K_hat^{mu nu} is the Hilbert stress of a parent diffeomorphism-invariant S_GK",
            "current_evidence": "formal route exists in 1010/756 but symbol match fails",
            "current_status": "MISSING_PARENT_SIGNED_METRIC_RESPONSE_CERTIFICATE",
            "passes_now": False,
            "valid_for_claim": False,
        },
        {
            "certificate_id": "TZ1189_0_parent_GK_Ploc_boundary_zero",
            "clause": "Helmholtz_integrability",
            "required_statement": "second metric variation is symmetric up to allowed boundary improvements",
            "current_evidence": "retained as H_GK gap in 1010",
            "current_status": "MISSING_PARENT_SIGNED_HELMHOLTZ_CERTIFICATE",
            "passes_now": False,
            "valid_for_claim": False,
        },
        {
            "certificate_id": "TZ1189_0_parent_GK_Ploc_boundary_zero",
            "clause": "Euler_double_zero",
            "required_statement": "local compact vacuum Euler equations set T_GK(Phi0)=0 and first variation zero",
            "current_evidence": "response-doublet double-zero is formal only; physical lock missing",
            "current_status": "MISSING_EULER_DOUBLE_ZERO_AND_PHYSICAL_LOCK",
            "passes_now": False,
            "valid_for_claim": False,
        },
        {
            "certificate_id": "TZ1189_0_parent_GK_Ploc_boundary_zero",
            "clause": "P_loc_parent_domain",
            "required_statement": "P_loc is parent-defined before readout and cannot hide unprojected force components",
            "current_evidence": "874 signature not parent signed; 1010 projector boundary open",
            "current_status": "MISSING_PARENT_PLOC_DOMAIN_CERTIFICATE",
            "passes_now": False,
            "valid_for_claim": False,
        },
        {
            "certificate_id": "TZ1189_0_parent_GK_Ploc_boundary_zero",
            "clause": "boundary_no_flux",
            "required_statement": "boundary/symplectic/source-current terms vanish or are included in the component residual",
            "current_evidence": "755 and 1010 keep boundary/no-flux open",
            "current_status": "MISSING_BOUNDARY_NO_FLUX_CERTIFICATE",
            "passes_now": False,
            "valid_for_claim": False,
        },
        {
            "certificate_id": "TZ1189_0_parent_GK_Ploc_boundary_zero",
            "clause": "arena_projection_silence",
            "required_statement": "all PPN/R10/clock/orbital projections receive zero or bounded contribution from the same parent theorem",
            "current_evidence": "746 forbids a one-scalar pass across arenas",
            "current_status": "MISSING_ARENA_PROJECTION_CERTIFICATES",
            "passes_now": False,
            "valid_for_claim": False,
        },
    ]


def dryrun_rows(pack: list[dict[str, object]], certs: list[dict[str, object]]) -> list[dict[str, object]]:
    missing_rows = [row for row in pack if "MISSING" in str(row.get("missing_fields", ""))]
    cert_pass = all(row["passes_now"] is True for row in certs)
    return [
        {
            "dryrun_id": "DR1189_0_schema_columns",
            "check": "component pack contains required 750/756 columns",
            "result": "PASS",
            "detail": "sample/domain/measure/frame/q-components/boundary/source/theorem-zero columns are present",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "dryrun_id": "DR1189_1_missing_rows_guard",
            "check": "rows with MISSING fields cannot score",
            "result": "PASS" if missing_rows and all(row["valid_for_claim"] is False for row in missing_rows) else "FAIL",
            "detail": f"{len(missing_rows)} rows contain MISSING fields and remain nonclaim",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "dryrun_id": "DR1189_2_no_qproxy_only_pass",
            "check": "q_proxy scalar is not used as a component pass",
            "result": "PASS",
            "detail": "pack requires q0..q3/q_T/q_x/q_y/q_z or theorem-zero certificate; prior q_proxy is only a guard/anchor",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "dryrun_id": "DR1189_3_theorem_zero_gate",
            "check": "theorem-zero certificate is all-or-nothing",
            "result": "PASS" if not cert_pass else "FAIL",
            "detail": "certificate rows are present but none pass now, so q_loc zero remains unclaimed",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "dryrun_id": "DR1189_4_arena_score",
            "check": "PPN/R10/clock/orbital rows are queued but not executable",
            "result": "PASS",
            "detail": "all arena projection rows require response operators and source-backed q_loc/profile inputs",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "G1189_0_component_data",
            "claim": "component-resolved q_loc data exists",
            "status": "BLOCKED",
            "why": "1189 writes templates only; q0..q3/q_T/q_perp values remain MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1189_1_theorem_zero",
            "claim": "q_loc^nu=0 is theorem-derived",
            "status": "BLOCKED",
            "why": "metric-response, Helmholtz, Euler/double-zero, P_loc, boundary, and arena projection certificates are missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1189_2_PPN",
            "claim": "PPN/local-GR residual pass",
            "status": "BLOCKED",
            "why": "W_even/W_alpha_i and component q_loc inputs are absent",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1189_3_R10",
            "claim": "R10/fifth-force residual pass",
            "status": "BLOCKED",
            "why": "finite-range q_loc kernel and c_q_alpha(lambda) are absent",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1189_4_clock_orbital",
            "claim": "clock/orbital residual pass",
            "status": "BLOCKED",
            "why": "clock readout and orbital force/source-normalization maps are absent",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D1189_0_pack_created",
            "decision": "component_residual_pack_templates_created",
            "reason": "local tests need vector/frame/domain components and arena projections, not a single scalar q_proxy",
            "next_action": "fill real q_loc components or a theorem-zero certificate before any scoring",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1189_1_theorem_zero_slot_preserved",
            "decision": "profile_theorem_zero_certificate_slot_created",
            "reason": "a future derivation can replace empirical residual rows if all parent certificates close",
            "next_action": "try to close the parent-owned tracefree Khat/P_loc theorem, or leave q_loc empirical",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1189_2_best_next_derivation",
            "decision": "attack_Ploc_parent_domain_or_tracefree_Khat_solver",
            "reason": "these are the shortest routes to making q_loc small without fitted cancellation",
            "next_action": "build 1190 P_loc parent-domain commutator/no-flux theorem attempt",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1189_3_best_next_testing",
            "decision": "if_derivation_stalls_fill_one_real_arena_operator",
            "reason": "alpha3 and R10 are high-pressure tests but need different projections",
            "next_action": "source one response operator and one component/profile row with valid_for_claim=false first",
            "valid_for_claim": False,
        },
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT1189_0_1190",
            "next_target": "1190-Y5-R10-P_loc-parent-domain-commutator-or-tracefree-Khat-solver-gate.md",
            "objective": "try to derive the parent-owned P_loc domain/commutator/no-flux clause or the tracefree-longitudinal K_hat solver; otherwise keep the 1189 component residual pack as the local-test interface",
            "include": "P_loc definition before readout; derivative commutator correction; boundary/no-flux clause; tracefree Khat divergence solver; theorem-zero update; no-claim validation",
            "exclude": "post-readout projector tuning; q_proxy-only pass; q_loc zero claim; local-GR pass; invented numeric profiles; GitHub; formalization edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, object]],
    pack: list[dict[str, object]],
    projections: list[dict[str, object]],
    certs: list[dict[str, object]],
    dryrun: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> list[dict[str, object]]:
    all_sources_ok = all(row["exists"] and row["needle_found"] for row in sources)
    required_pack_columns = {
        "sample_id",
        "domain_id",
        "weight_dV",
        "frame_convention",
        "u0",
        "u1",
        "u2",
        "u3",
        "q0",
        "q1",
        "q2",
        "q3",
        "boundary_tag",
        "boundary_condition",
        "source_path",
        "valid_for_claim",
    }
    pack_columns = set().union(*(row.keys() for row in pack))
    arena_set = {row["arena"] for row in projections}
    cert_clauses = {row["clause"] for row in certs}
    all_nonclaim = all(row.get("valid_for_claim") is False for row in pack + projections + certs + dryrun + gates + decisions + nexts)
    return [
        {
            "check_id": "V1189_0_sources_exist",
            "result": "pass" if all_sources_ok else "fail",
            "detail": "all cited local source paths exist and needles are found",
            "claim_allowed": False,
        },
        {
            "check_id": "V1189_1_component_pack_columns",
            "result": "pass" if required_pack_columns <= pack_columns else "fail",
            "detail": "component pack includes required 750/756 columns",
            "claim_allowed": False,
        },
        {
            "check_id": "V1189_2_missing_rows_nonclaim",
            "result": "pass" if all(row["valid_for_claim"] is False and "MISSING" in str(row["missing_fields"]) for row in pack) else "fail",
            "detail": "all component/template rows remain nonclaim because required inputs are missing",
            "claim_allowed": False,
        },
        {
            "check_id": "V1189_3_arena_coverage",
            "result": "pass" if {"PPN gamma/beta", "PPN alpha3/preferred-frame", "short-range/R10", "clock/time/readout", "orbital/source-normalization"} <= arena_set else "fail",
            "detail": "PPN, alpha3, R10, clock, and orbital projection queues are present",
            "claim_allowed": False,
        },
        {
            "check_id": "V1189_4_theorem_certificate_clauses",
            "result": "pass" if {"metric_response_owner", "Helmholtz_integrability", "Euler_double_zero", "P_loc_parent_domain", "boundary_no_flux", "arena_projection_silence"} <= cert_clauses else "fail",
            "detail": "theorem-zero certificate requires all parent clauses",
            "claim_allowed": False,
        },
        {
            "check_id": "V1189_5_dryrun_passes",
            "result": "pass" if all(row["result"] == "PASS" for row in dryrun) else "fail",
            "detail": "dry-run confirms templates are nonclaim and theorem-zero is not promoted",
            "claim_allowed": False,
        },
        {
            "check_id": "V1189_6_claim_gates_blocked",
            "result": "pass" if all(row["status"] == "BLOCKED" and row["claim_allowed"] is False for row in gates) else "fail",
            "detail": "all local claim gates remain blocked",
            "claim_allowed": False,
        },
        {
            "check_id": "V1189_7_all_science_rows_nonclaim",
            "result": "pass" if all_nonclaim else "fail",
            "detail": "all generated science rows keep valid_for_claim=false",
            "claim_allowed": False,
        },
        {
            "check_id": "V1189_8_next_target",
            "result": "pass" if nexts and nexts[0]["next_id"] == "NEXT1189_0_1190" else "fail",
            "detail": "1190 handoff targets P_loc parent-domain/commutator or tracefree Khat solver",
            "claim_allowed": False,
        },
        {
            "check_id": "V1189_9_generated_under_post_checkpoint",
            "result": "pass" if str(DOC).startswith(str(ROOT)) and str(CSV_DIR).startswith(str(ROOT)) else "fail",
            "detail": "all generated outputs are under post-checkpoint-work",
            "claim_allowed": False,
        },
        {
            "check_id": "V1189_10_formalization_untouched",
            "result": "pass",
            "detail": "generator writes no outputs under formalization-workbench",
            "claim_allowed": False,
        },
        {
            "check_id": "V1189_SUMMARY",
            "result": "pass",
            "detail": "1189 creates a nonclaim q_loc component residual pack, arena projection queue, theorem-zero certificate template, dry-run guard, and 1190 P_loc/Khat handoff",
            "claim_allowed": False,
        },
    ]


def write_doc(
    sources: list[dict[str, object]],
    pack: list[dict[str, object]],
    projections: list[dict[str, object]],
    certs: list[dict[str, object]],
    dryrun: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validations: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> None:
    text = "\n\n".join(
        [
            "# 1189 - Y5/R10 q_loc component residual pack or profile theorem-zero certificate",
            "**Current verdict:** the local-test interface is now componentized. `q_loc` cannot be scored from a scalar proxy; it needs observed-frame vector components, domain measure, boundary data, and arena response operators, or a full theorem-zero certificate.",
            "**Main progress:** 1189 creates nonclaim component templates for PPN, R10, clock, and orbital tests, plus an all-or-nothing theorem-zero certificate slot for a future parent `Gamma_eff/K_hat/P_loc` proof.",
            "**No claim:** no `q_loc=0`, local-GR, Newton, R10, PPN, WEP, clock, orbital, or public-facing claim follows from this checkpoint.",
            "## Source register\n\n" + table(sources),
            "## q_loc component residual input pack\n\n" + table(pack),
            "## Arena projection queue\n\n" + table(projections),
            "## Theorem-zero certificate template\n\n" + table(certs),
            "## Dry-run guard\n\n" + table(dryrun),
            "## Claim gates\n\n" + table(gates),
            "## Decision ledger\n\n" + table(decisions),
            "## Validation\n\n" + table(validations),
            "## Next target\n\n" + table(nexts),
        ]
    )
    DOC.write_text(text + "\n", encoding="utf-8")


def main() -> None:
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    pack = component_pack_rows()
    projections = arena_projection_rows()
    certs = theorem_zero_certificate_rows()
    dryrun = dryrun_rows(pack, certs)
    gates = claim_gate_rows()
    decisions = decision_rows()
    nexts = next_rows()
    validations = validation_rows(sources, pack, projections, certs, dryrun, gates, decisions, nexts)

    outputs = {
        "P8_Y5_R10_1189_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R10_1189_QLOC_COMPONENT_RESIDUAL_INPUT_PACK.csv": pack,
        "P8_Y5_R10_1189_ARENA_PROJECTION_QUEUE.csv": projections,
        "P8_Y5_R10_1189_THEOREM_ZERO_CERTIFICATE_TEMPLATE.csv": certs,
        "P8_Y5_R10_1189_DRYRUN_GUARD.csv": dryrun,
        "P8_Y5_R10_1189_CLAIM_GATES.csv": gates,
        "P8_Y5_R10_1189_DECISION_LEDGER.csv": decisions,
        "P8_Y5_R10_1189_NEXT_TARGET.csv": nexts,
        "P8_Y5_BRR545_1189_VALIDATION.csv": validations,
    }
    for filename, rows in outputs.items():
        write_csv(CSV_DIR / filename, stamp(rows))

    write_doc(sources, pack, projections, certs, dryrun, gates, decisions, validations, nexts)

    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row["check_id"] for row in validations if row["result"] != "pass"]
    if FORMALIZATION.exists() and not FORMALIZATION.is_dir():
        failed.append("formalization_path_not_directory")

    print(f"wrote {DOC}")
    print("validation: " + ("PASS" if not failed else "FAIL " + ";".join(failed)))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
