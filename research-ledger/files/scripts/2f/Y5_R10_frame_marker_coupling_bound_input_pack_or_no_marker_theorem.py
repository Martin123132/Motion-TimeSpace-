from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1028-Y5-R10-frame-marker-coupling-bound-input-pack-or-no-marker-theorem.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: object) -> bool:
    return str(value).strip().lower() == "true"


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


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
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1028_0_1027_next", "source-intake/mts_residuals/P8_Y5_R10_1027_NEXT_TARGET.csv", "1028-Y5-R10-frame-marker", "1027 handoff to frame/marker coupling pack."),
        ("SRC1028_1_1027_qbar_schema", "source-intake/mts_residuals/P8_Y5_R10_1027_BOUNDED_QBARXT_ROW_SCHEMA.csv", "BQT1027_3_total_abs_guard", "1027 no-cancellation qbarXT envelope."),
        ("SRC1028_2_1027_counterexamples", "source-intake/mts_residuals/P8_Y5_R10_1027_COUNTEREXAMPLE_GUARD.csv", "CE1027_0_common_Weyl", "1027 surviving frame and marker counterexamples."),
        ("SRC1028_3_565_vertical", "565-Y5-R10-coframe-pullback-zero-or-finite-alpha-coefficient.md", "VT565_2_no_hidden_marker_clause", "565 conditional vertical observation theorem and no-marker debt."),
        ("SRC1028_4_566_nomarker", "566-Y5-R10-primitive-quotient-no-marker-parent-clause-or-alpha-coefficient-fill.md", "NM566_3_verdict", "566 no-marker theorem attempt and failure mode."),
        ("SRC1028_5_943_contract", "source-intake/mts_residuals/P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv", "CFC943_3_constants_and_masses", "943 coframe/constants coupling contract."),
        ("SRC1028_6_944_frame_pack", "source-intake/mts_residuals/P8_Y5_R10_944_FRAME_LEAK_BOUND_PACK.csv", "FLB944_0_cg_weyl", "944 frame-leak bound schema."),
        ("SRC1028_7_945_frame_rows", "source-intake/mts_residuals/P8_Y5_R10_945_FIRST_FRAME_LEAK_BOUND_ROWS.csv", "BND945_0_cg_value", "945 first c_g/tau/b_A/b_dis/q_nonH rows."),
        ("SRC1028_8_945_doc", "945-Y5-R10-parent-q-map-Obs-e-functor-construction-or-first-frame-leak-bound-pack.md", "BND945_7_score_gate", "945 nonclaim score gate."),
        ("SRC1028_9_953_source_functor", "source-intake/mts_residuals/P8_Y5_R10_953_SOURCE_FUNCTOR_THEOREM_ATTEMPT.csv", "NSF953_5_verdict", "953 conditional source functor theorem."),
        ("SRC1028_10_954_label_forgetting", "source-intake/mts_residuals/P8_Y5_R10_954_PARENT_LABEL_FORGETTING_ATTEMPT.csv", "PLF954_5_verdict", "954 parent label-forgetting contract."),
        ("SRC1028_11_955_matter_action", "source-intake/mts_residuals/P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv", "MMA955_6_verdict", "955 minimal matter action lemma."),
        ("SRC1028_12_956_gr_newton_spine", "source-intake/mts_residuals/P8_Y5_R10_956_SOURCE_SIDE_GR_NEWTON_SPINE.csv", "SSG956_3_minimal_matter_action", "956 source-side GR/Newton spine."),
    ]
    rows: list[dict[str, str]] = []
    for source_id, path_text, needle, role in specs:
        path = source_path(path_text)
        exists = path.exists()
        text = path.read_text(encoding="utf-8", errors="ignore") if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(exists).lower(),
                "needle": needle,
                "needle_found": str(needle in text).lower(),
                "role": role,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def no_marker_theorem_audit_rows() -> list[dict[str, str]]:
    return [
        {
            "audit_id": "NM1028_0_parent_q_kernel",
            "theorem_clause": "X is vertical to the parent quotient",
            "mathematical_form": "v_X in ker(Dq) before matter/source variation",
            "current_evidence": "945 writes a q_candidate but keeps kernel ownership unsigned.",
            "status": "MISSING_PARENT_Q_KERNEL_CERTIFICATE",
            "missing_signature": "presymplectic-null/gauge kernel plus boundary silence",
            "if_unsigned": "a physical X mode may couple through observed geometry or source support",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "NM1028_1_observed_coframe_descent",
            "theorem_clause": "ordinary rods/clocks/free-fall use only descended observed geometry",
            "mathematical_form": "e_obs(Phi)=Obs_e(q(Phi)); Lie_vX e_obs=0",
            "current_evidence": "943/945 give a clean contract, not a parent-signed theorem.",
            "status": "CONDITIONAL_DESCENT_ONLY",
            "missing_signature": "unique parent Obs_e functor and no representative frame channel",
            "if_unsigned": "common Weyl/disformal leakage is still legal",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "NM1028_2_matter_functor_descent",
            "theorem_clause": "ordinary matter action is a functor of descended structures only",
            "mathematical_form": "S_matter=Sbar[Psi,e_obs,omega[e_obs],theta]",
            "current_evidence": "953/954/955 sharpen the exact source-side contract but call it unsigned.",
            "status": "EXACT_CONTRACT_NOT_PARENT_SIGNED",
            "missing_signature": "parent action excludes source-only matter slots and hidden current spurions",
            "if_unsigned": "species/source prefactors or source-only channels can survive",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "NM1028_3_quotient_owned_constants",
            "theorem_clause": "masses, material constants, EM constants, and clock markers descend through q",
            "mathematical_form": "Lie_vX theta_A=0; Lie_vX m_A=0; Lie_vX alpha_EM=0",
            "current_evidence": "565 identifies the no-hidden-marker clause; 566 shows covariance/universality alone do not prove it.",
            "status": "MISSING_NO_MARKER_THEOREM",
            "missing_signature": "quotient-owned constants or explicit b_A/b_alpha rows",
            "if_unsigned": "ordinary matter can carry X charge through material/clock/EM markers",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "NM1028_4_no_shadow_frame",
            "theorem_clause": "there is no observationally active representative Weyl/disformal frame",
            "mathematical_form": "A_g'(0)=0 and dB_g/dXhat=0, or the coefficients are retained",
            "current_evidence": "944/945 retain c_g and b_dis rows rather than proving them zero.",
            "status": "MISSING_NO_SHADOW_FRAME_THEOREM",
            "missing_signature": "parent no-representative-frame theorem or numeric c_g/b_dis bounds",
            "if_unsigned": "WEP can look clean while a common fifth-force source remains",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "NM1028_5_hidden_source_tail",
            "theorem_clause": "non-Hilbert, boundary, projector, and support-shift tails are zero or retained",
            "mathematical_form": "q_nonH=0 and Delta_W_support=0, or both enter the bound pack",
            "current_evidence": "943/956 keep connection/source-support silence as open gates.",
            "status": "MISSING_HIDDEN_SOURCE_ZERO_OR_BOUND",
            "missing_signature": "boundary/local projection theorem or sourced q_nonH/support bounds",
            "if_unsigned": "the local source can move even if the Hilbert matter pullback is zero",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "NM1028_6_verdict",
            "theorem_clause": "no-marker/constant-descent theorem for ordinary matter",
            "mathematical_form": "all clauses NM1028_0 through NM1028_5 are parent-signed together",
            "current_evidence": "the chain-rule theorem is sharp, but the parent signature is still not in the corpus.",
            "status": "FAIL_CURRENT_CLAIM",
            "missing_signature": "single parent certificate for q-kernel, e_obs descent, S_matter descent, constants, frame, and tails",
            "if_unsigned": "build claim-blocked frame/marker/source bound rows",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def frame_marker_bound_rows() -> list[dict[str, str]]:
    source_945 = str(source_path("source-intake/mts_residuals/P8_Y5_R10_945_FIRST_FRAME_LEAK_BOUND_ROWS.csv"))
    source_944 = str(source_path("source-intake/mts_residuals/P8_Y5_R10_944_FRAME_LEAK_BOUND_PACK.csv"))
    source_1027 = str(source_path("source-intake/mts_residuals/P8_Y5_R10_1027_BOUNDED_QBARXT_ROW_SCHEMA.csv"))
    return [
        {
            "row_id": "FMB1028_0_cg",
            "symbol": "c_g",
            "definition": "common Weyl/frame derivative d ln A_g/dXhat for ordinary matter or source readout",
            "units": "dimensionless",
            "required_inputs": "system_id;branch_id;Xhat_normalization;c_g;units;zero_theorem_path_or_numeric_source;arena_projection",
            "source_path": f"{source_945};{source_944}",
            "observable_link": "R10;PPN;WEP;clock",
            "bound_or_use": "|qbar_geom| contains |tau_R10 c_g| and PPN/clock projections",
            "current_status": "MISSING_PARENT_ZERO_OR_NUMERIC_CG",
            "score_ready": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "FMB1028_1_tau_R10",
            "symbol": "tau_R10",
            "definition": "short-range R10 projection from frame/marker coupling into alpha(lambda)",
            "units": "dimensionless",
            "required_inputs": "test_body;source_body;lambda;profile_convention;tau_R10;units;source_path",
            "source_path": source_945,
            "observable_link": "R10",
            "bound_or_use": "alpha_R10 ~ K_X(lambda) Qbar_XH tau_R10 c_g plus retained marker/source terms",
            "current_status": "MISSING_ARENA_PROJECTION",
            "score_ready": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "FMB1028_2_tau_PPN",
            "symbol": "tau_PPN",
            "definition": "weak-field/local metric projection of common frame and disformal response",
            "units": "dimensionless",
            "required_inputs": "gauge;weak_field_order;tau_PPN;units;source_path;residual_vector",
            "source_path": source_945,
            "observable_link": "PPN;orbital;local_GR",
            "bound_or_use": "PPN residual vector receives tau_PPN c_g and disformal terms",
            "current_status": "MISSING_ARENA_PROJECTION",
            "score_ready": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "FMB1028_3_tau_clock",
            "symbol": "tau_clock",
            "definition": "clock/readout projection of material, EM, and common-frame X dependence",
            "units": "dimensionless",
            "required_inputs": "clock_pair;sensitivities;tau_clock;units;source_path;normalization",
            "source_path": source_944,
            "observable_link": "clock;EM;WEP",
            "bound_or_use": "delta ln nu receives tau_clock c_g plus S_A b_A and S_alpha b_alpha",
            "current_status": "MISSING_CLOCK_PROJECTION",
            "score_ready": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "FMB1028_4_tau_orbital",
            "symbol": "tau_orbital",
            "definition": "orbital/source-support projection of hidden current and support-frame shifts",
            "units": "dimensionless",
            "required_inputs": "orbital_system;support_rule;tau_orbital;units;source_path;normalization",
            "source_path": source_944,
            "observable_link": "orbital;source_normalization;local_GR",
            "bound_or_use": "Delta GM or source support residual receives tau_orbital Delta_W_support/q_nonH",
            "current_status": "MISSING_ORBITAL_PROJECTION",
            "score_ready": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "FMB1028_5_b_dis",
            "symbol": "b_dis",
            "definition": "representative disformal derivative or profile-normalized disformal coupling",
            "units": "model_dependent",
            "required_inputs": "disformal_profile;normalization;b_dis;units;zero_theorem_path_or_numeric_source;arena_projection",
            "source_path": f"{source_945};{source_944}",
            "observable_link": "PPN;preferred_frame;clock;orbital",
            "bound_or_use": "|qbar_geom| contains |tau_dis b_dis|; preferred-frame channels must not be hidden",
            "current_status": "MISSING_DISFORMAL_ZERO_OR_NUMERIC_BOUND",
            "score_ready": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "FMB1028_6_b_A",
            "symbol": "b_A",
            "definition": "vertical derivative of material mass or species constants d ln m_A^obs/dXhat",
            "units": "dimensionless",
            "required_inputs": "species_or_material;mass_or_constant;b_A;sensitivity;units;source_path",
            "source_path": f"{source_945};{source_944}",
            "observable_link": "WEP;clock;composition;R10",
            "bound_or_use": "|qbar_marker| contains sum_A |s_A b_A|",
            "current_status": "MISSING_CONSTANT_DESCENT_OR_NUMERIC_BA",
            "score_ready": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "FMB1028_7_b_alpha",
            "symbol": "b_alpha",
            "definition": "vertical derivative of EM/fine-structure or electromagnetic binding marker",
            "units": "dimensionless",
            "required_inputs": "EM_constant_or_binding_channel;b_alpha;sensitivity;units;source_path",
            "source_path": source_944,
            "observable_link": "clock;EM;WEP;composition",
            "bound_or_use": "|qbar_marker| contains |s_alpha b_alpha|",
            "current_status": "MISSING_EM_CONSTANT_DESCENT_OR_NUMERIC_BOUND",
            "score_ready": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "FMB1028_8_q_nonH",
            "symbol": "q_nonH",
            "definition": "ordinary source projection carried by non-Hilbert current, torsion/nonmetricity, or boundary tail",
            "units": "source_current_units",
            "required_inputs": "arena;current_definition;q_nonH;units;source_path;flux_or_boundary_convention",
            "source_path": f"{source_945};{source_944}",
            "observable_link": "R10;PPN;source_normalization;local_GR",
            "bound_or_use": "|qbar_nonH| contains |q_nonH|",
            "current_status": "MISSING_NONHILBERT_ZERO_FLUX_OR_NUMERIC_SOURCE",
            "score_ready": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "FMB1028_9_Delta_W_support",
            "symbol": "Delta_W_support",
            "definition": "source/worldtube support shift under allowed observed-frame choices",
            "units": "dimensionless",
            "required_inputs": "system_id;support_rule;Delta_W_support;units;source_path;frame_equivalence_theorem_or_bound",
            "source_path": f"{source_945};{source_944}",
            "observable_link": "orbital;local_GR;source_normalization",
            "bound_or_use": "|qbar_nonH| contains |Delta_W_support| and support/domain tails",
            "current_status": "MISSING_SUPPORT_EQUIVALENCE_OR_NUMERIC_BOUND",
            "score_ready": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "FMB1028_10_total_qbarXT_envelope",
            "symbol": "qbar_XT_bound_abs",
            "definition": "absolute no-cancellation envelope over visible geometry, markers, non-Hilbert tails, and hidden support terms",
            "units": "dimensionless_or_declared_profile_units",
            "required_inputs": "abs_qbar_geom;abs_qbar_marker;abs_qbar_nonH;abs_qbar_hidden;source_paths;normalization;units",
            "source_path": source_1027,
            "observable_link": "R10;WEP;clock;PPN;orbital;local_GR",
            "bound_or_use": "|qbar_XT| <= |qbar_geom|+|qbar_marker|+|qbar_nonH|+|qbar_hidden|",
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "score_ready": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "FMB1028_11_claim_gate",
            "symbol": "claim_gate",
            "definition": "no local or R10 claim until all component rows are theorem-zero or numeric/source-backed",
            "units": "policy",
            "required_inputs": "no_MISSING_markers;positive_units;real_source_paths;arena_projection;no_cancellation_policy",
            "source_path": source_1027,
            "observable_link": "all_local_arenas",
            "bound_or_use": "valid_for_claim may become true only after all inputs are real and pass their arena bounds",
            "current_status": "CLAIM_BLOCKED",
            "score_ready": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def observable_link_rows() -> list[dict[str, str]]:
    return [
        {
            "link_id": "OL1028_0_R10_alpha",
            "quantity": "c_g;tau_R10;b_A;b_alpha;q_nonH",
            "arena": "R10 short-range fifth-force comparator",
            "observable_link": "alpha(lambda) bound",
            "required_projection": "K_X(lambda) Qbar_XH [tau_R10 c_g + marker/source terms]",
            "current_status": "BLOCKED_NUMERIC_INPUTS_MISSING",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "link_id": "OL1028_1_PPN",
            "quantity": "c_g;tau_PPN;b_dis;q_nonH",
            "arena": "local weak-field metric/PPN",
            "observable_link": "gamma,beta,preferred-frame,residual vector",
            "required_projection": "gauge-fixed weak-field map from retained coupling rows to PPN residuals",
            "current_status": "BLOCKED_ARENA_PROJECTION_MISSING",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "link_id": "OL1028_2_clocks_EM",
            "quantity": "b_A;b_alpha;tau_clock;c_g",
            "arena": "clock/EM/material marker tests",
            "observable_link": "delta ln nu, alpha_EM drift, material sensitivity",
            "required_projection": "clock sensitivities S_A and S_alpha with units and source paths",
            "current_status": "BLOCKED_MARKER_DESCENT_OR_SENSITIVITY_ROWS_MISSING",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "link_id": "OL1028_3_WEP_composition",
            "quantity": "b_A;b_alpha;c_g",
            "arena": "WEP/composition",
            "observable_link": "eta_AB and differential material response",
            "required_projection": "composition sensitivities and material-pair source/test conventions",
            "current_status": "BLOCKED_SENSITIVITY_ROWS_MISSING",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "link_id": "OL1028_4_orbital_support",
            "quantity": "q_nonH;Delta_W_support;tau_orbital",
            "arena": "orbital/source-normalization/local-GR",
            "observable_link": "Delta GM, source support residual, local-GR reduction gate",
            "required_projection": "same-worldtube/source-measure map with hidden-current silence or finite bound",
            "current_status": "BLOCKED_SOURCE_SUPPORT_THEOREM_OR_NUMERIC_BOUND_MISSING",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1028_0_sources_exist",
            "claim": "1028 evidence sources are locally present",
            "gate_pass": "true",
            "reason": "all cited private checkpoint sources are required to exist with expected needles",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1028_1_no_marker_theorem",
            "claim": "ordinary matter no-marker/constant-descent theorem is parent-signed",
            "gate_pass": "false",
            "reason": "NM1028_6 remains FAIL_CURRENT_CLAIM",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1028_2_bound_pack_schema",
            "claim": "frame/marker/source bound input pack is schema-ready",
            "gate_pass": "true",
            "reason": "rows exist for c_g, projections, b_dis, b_A, b_alpha, q_nonH, support, and total envelope",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1028_3_numeric_inputs",
            "claim": "numeric/source-backed coupling rows can be scored",
            "gate_pass": "false",
            "reason": "all retained coupling rows still contain MISSING theorem-zero or numeric input statuses",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1028_4_arena_projections",
            "claim": "R10/PPN/clock/orbital projections are sourced",
            "gate_pass": "false",
            "reason": "tau_R10, tau_PPN, tau_clock, and tau_orbital are staged but not sourced",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1028_5_no_cancellation_guard",
            "claim": "unknown components may cancel in the local score",
            "gate_pass": "true",
            "reason": "cancellation is forbidden; only an absolute component-sum envelope is allowed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1028_6_local_GR_or_R10_pass",
            "claim": "local-GR, R10, WEP, clock, PPN, or orbital pass is established",
            "gate_pass": "false",
            "reason": "1028 is theorem audit plus nonclaim input pack, not a pass runner",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def branch_verdict_rows() -> list[dict[str, str]]:
    return [
        {
            "verdict_id": "BV1028_0_no_marker_theorem",
            "branch": "derive no-marker theorem",
            "status": "FAIL_CURRENT_CLAIM",
            "because": "a clean conditional theorem exists, but no single parent certificate signs q-kernel, matter functor, constants, no-shadow frame, and hidden-tail silence.",
            "allowed_statement": "MTS may use the no-marker chain as a parent-action contract.",
            "forbidden_statement": "MTS has derived ordinary matter qbar_XT=0 or local-GR from the current corpus.",
            "next_action": "try parent no-shadow/no-marker closure or fill numeric source rows",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "verdict_id": "BV1028_1_bound_pack",
            "branch": "build coupling bound input pack",
            "status": "SCHEMA_READY_NONCLAIM",
            "because": "the surviving counterexamples map to named rows with units, observable links, source paths, and no-cancellation policy.",
            "allowed_statement": "the local coupling gap is now an explicit row-acquisition problem.",
            "forbidden_statement": "any finite-alpha, R10, PPN, clock, orbital, WEP, or local-GR claim from placeholder rows.",
            "next_action": "source/derive the first concrete c_g, b_A, b_alpha, b_dis, q_nonH, or support row",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "verdict_id": "BV1028_2_test_readiness",
            "branch": "near-term empirical testing",
            "status": "BLOCKED_BUT_STRUCTURED",
            "because": "R10/PPN/clock/orbital tests now have named input slots, but no row is score-ready.",
            "allowed_statement": "future smoke runners can fail safely until rows are sourced.",
            "forbidden_statement": "claiming a pass because the row schema exists.",
            "next_action": "attack c_g/no-shadow frame first, because it feeds R10, PPN, WEP, and clocks",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "verdict_id": "BV1028_3_next_target",
            "branch": "next target",
            "status": "1029_selected",
            "because": "c_g is the broadest coupling: if parent no-shadow closes it, several local arenas simplify; if not, it becomes the first real bound row.",
            "allowed_statement": "1029 should focus on c_g/no-shadow frame theorem versus first numeric c_g and tau_R10/tau_PPN rows.",
            "forbidden_statement": "jumping to local-GR pass before c_g and marker/source tails are controlled.",
            "next_action": "1029-Y5-R10-cg-no-shadow-frame-theorem-or-first-numeric-coupling-row.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1028_0_theorem_status",
            "decision": "The no-marker/constant-descent theorem is not parent-signed yet.",
            "because": "565/566/943/953/954/955/956 provide sharp conditional contracts, but they do not close the parent no-spurion/no-shadow/hidden-tail clauses.",
            "next_action": "do not claim qbar_XT=0; use the bound input pack",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1028_1_bound_pack_status",
            "decision": "The frame/marker/source coupling gap has a first complete nonclaim input pack.",
            "because": "every surviving 1027 counterexample is mapped to a named row and observable arena.",
            "next_action": "source or derive rows one by one without cancellation",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1028_2_best_order",
            "decision": "Go after c_g/no-shadow frame first.",
            "because": "c_g is a common coupling that touches R10, PPN, WEP, and clock arenas, so it has the highest leverage.",
            "next_action": "try no-shadow frame theorem; if it fails, create first numeric c_g/tau_R10 acquisition rows",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1028_3_next_target",
            "decision": "Next target is 1029 c_g no-shadow frame theorem or first numeric coupling row.",
            "because": "1028 demotes the global no-marker route to a contract and stages the bounded fallback.",
            "next_action": "1029-Y5-R10-cg-no-shadow-frame-theorem-or-first-numeric-coupling-row.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1029-Y5-R10-cg-no-shadow-frame-theorem-or-first-numeric-coupling-row.md",
            "objective": "try to prove the parent no-shadow-frame theorem that sets c_g=0; if it cannot be signed, stage the first numeric/source-backed c_g row with tau_R10/tau_PPN projection requirements",
            "include": "representative Weyl/common matter frame, A_g'(0), q-kernel action invariance, observed-frame uniqueness, R10 tau_R10, PPN tau_PPN, source paths, units, no-cancellation policy",
            "exclude": "WEP-only zero, field rename proof, placeholder numeric values, cancellation between c_g and marker/source tails, R10/PPN/local-GR claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def formalization_changed_after_start() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    changed = []
    for candidate in FORMALIZATION.rglob("*"):
        if candidate.is_file():
            modified = datetime.fromtimestamp(candidate.stat().st_mtime, timezone.utc)
            if modified >= STARTED:
                changed.append(candidate)
    return changed


def validation_rows(
    sources: list[dict[str, str]],
    theorem: list[dict[str, str]],
    bound_pack: list[dict[str, str]],
    links: list[dict[str, str]],
    gates: list[dict[str, str]],
    verdicts: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    changed = formalization_changed_after_start()
    theorem_required = {f"NM1028_{idx}_{name}" for idx, name in [
        (0, "parent_q_kernel"),
        (1, "observed_coframe_descent"),
        (2, "matter_functor_descent"),
        (3, "quotient_owned_constants"),
        (4, "no_shadow_frame"),
        (5, "hidden_source_tail"),
        (6, "verdict"),
    ]}
    bound_required = {f"FMB1028_{idx}_{name}" for idx, name in [
        (0, "cg"),
        (1, "tau_R10"),
        (2, "tau_PPN"),
        (3, "tau_clock"),
        (4, "tau_orbital"),
        (5, "b_dis"),
        (6, "b_A"),
        (7, "b_alpha"),
        (8, "q_nonH"),
        (9, "Delta_W_support"),
        (10, "total_qbarXT_envelope"),
        (11, "claim_gate"),
    ]}
    link_required = {f"OL1028_{idx}_{name}" for idx, name in [
        (0, "R10_alpha"),
        (1, "PPN"),
        (2, "clocks_EM"),
        (3, "WEP_composition"),
        (4, "orbital_support"),
    ]}
    verdict_required = {f"BV1028_{idx}_{name}" for idx, name in [
        (0, "no_marker_theorem"),
        (1, "bound_pack"),
        (2, "test_readiness"),
        (3, "next_target"),
    ]}
    checks = [
        ("V1028_0_sources_exist", all(flag(row["exists"]) and flag(row["needle_found"]) for row in sources), "all cited source paths exist and expected needles are present"),
        ("V1028_1_theorem_rows_complete", theorem_required.issubset({row["audit_id"] for row in theorem}), "no-marker theorem audit covers q-kernel, coframe, matter, constants, frame, hidden tails, and verdict"),
        ("V1028_2_theorem_not_claimed", any(row["audit_id"] == "NM1028_6_verdict" and row["status"] == "FAIL_CURRENT_CLAIM" for row in theorem) and all(row["valid_for_claim"] == "false" for row in theorem), "no-marker theorem remains a contract, not a current claim"),
        ("V1028_3_bound_rows_complete", bound_required.issubset({row["row_id"] for row in bound_pack}), "bound pack includes c_g, tau projections, marker rows, hidden-source rows, total envelope, and claim gate"),
        ("V1028_4_bound_rows_nonclaim", all(row["valid_for_claim"] == "false" and row["score_ready"] == "false" and row["claim_allowed"] == "false" for row in bound_pack), "every bound row remains nonclaim and unscoreable"),
        ("V1028_5_bound_rows_missing_inputs", any(row["row_id"] == "FMB1028_0_cg" and "MISSING" in row["current_status"] for row in bound_pack) and any(row["row_id"] == "FMB1028_10_total_qbarXT_envelope" for row in bound_pack), "pack blocks c_g until theorem-zero or numeric inputs exist and carries total envelope"),
        ("V1028_6_observable_links_complete", link_required.issubset({row["link_id"] for row in links}), "observable map covers R10, PPN, clocks/EM, WEP/composition, and orbital/source-support"),
        ("V1028_7_claim_gates_blocked", all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in gates), "all claim gates refuse promotion"),
        ("V1028_8_no_cancellation_guard", any(row["gate_id"] == "CG1028_5_no_cancellation_guard" and flag(row["gate_pass"]) for row in gates), "no-cancellation guard is active"),
        ("V1028_9_verdicts_complete", verdict_required.issubset({row["verdict_id"] for row in verdicts}), "branch verdicts are complete"),
        ("V1028_10_decisions_written", any(row["decision_id"] == "DEC1028_3_next_target" for row in decisions), "decision ledger selects the 1029 target"),
        ("V1028_11_next_target_written", len(next_target) == 1 and "1029-Y5-R10-cg-no-shadow" in next_target[0]["next_target"], "1029 next target row is present"),
        ("V1028_12_no_overclaim", all(row.get("valid_for_claim", "false") == "false" for group in [sources, theorem, bound_pack, links, gates, verdicts, decisions, next_target] for row in group), "all generated rows remain valid_for_claim=false"),
        ("V1028_13_formalization_untouched", len(changed) == 0, f"formalization-workbench modified-file count since script start is {len(changed)}"),
    ]
    passed_all = all(passed for _, passed, _ in checks)
    rows = [{"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()} for check_id, passed, detail in checks]
    rows.insert(0, {"check_id": "V1028_SUMMARY", "result": "pass" if passed_all else "fail", "detail": "1028 frame/marker coupling bound input pack validation summary", "generated_utc": stamp()})
    return rows


def write_doc(
    sources: list[dict[str, str]],
    theorem: list[dict[str, str]],
    bound_pack: list[dict[str, str]],
    links: list[dict[str, str]],
    gates: list[dict[str, str]],
    verdicts: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validations: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1028 Y5 R10 frame marker coupling bound input pack or no-marker theorem",
            "",
            "**Status:** The no-marker/constant-descent route is clean as a conditional theorem but not parent-signed. The current branch therefore stages the first explicit, claim-blocked frame/marker/source coupling input pack: `c_g`, `tau_R10`, `tau_PPN`, `tau_clock`, `tau_orbital`, `b_dis`, `b_A`, `b_alpha`, `q_nonH`, `Delta_W_support`, and the total absolute `qbar_XT` envelope.",
            "",
            "**Claim ceiling:** no R10, WEP, clock, EM, PPN, orbital, local-GR/Newton, finite-alpha, or source-zero pass is allowed from 1028.",
            "",
            "## Source register",
            md_table(sources, ["source_id", "source_path", "exists", "needle_found", "role"]),
            "## No-marker theorem audit",
            md_table(theorem, ["audit_id", "theorem_clause", "mathematical_form", "current_evidence", "status", "missing_signature", "if_unsigned", "valid_for_claim"]),
            "## Frame marker bound input pack",
            md_table(bound_pack, ["row_id", "symbol", "definition", "units", "required_inputs", "source_path", "observable_link", "bound_or_use", "current_status", "score_ready", "claim_allowed", "valid_for_claim"]),
            "## Observable link map",
            md_table(links, ["link_id", "quantity", "arena", "observable_link", "required_projection", "current_status", "claim_allowed", "valid_for_claim"]),
            "## Claim gates",
            md_table(gates, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "## Branch verdicts",
            md_table(verdicts, ["verdict_id", "branch", "status", "because", "allowed_statement", "forbidden_statement", "next_action", "valid_for_claim"]),
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
    theorem = no_marker_theorem_audit_rows()
    bound_pack = frame_marker_bound_rows()
    links = observable_link_rows()
    gates = claim_gate_rows()
    verdicts = branch_verdict_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validations = validation_rows(sources, theorem, bound_pack, links, gates, verdicts, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_1028_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_1028_NO_MARKER_THEOREM_AUDIT.csv", theorem)
    write_csv(OUT / "P8_Y5_R10_1028_FRAME_MARKER_BOUND_INPUT_PACK.csv", bound_pack)
    write_csv(OUT / "P8_Y5_R10_1028_OBSERVABLE_LINK_MAP.csv", links)
    write_csv(OUT / "P8_Y5_R10_1028_CLAIM_GATES.csv", gates)
    write_csv(OUT / "P8_Y5_R10_1028_BRANCH_VERDICTS.csv", verdicts)
    write_csv(OUT / "P8_Y5_R10_1028_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_1028_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_1028_VALIDATION.csv", validations)
    write_doc(sources, theorem, bound_pack, links, gates, verdicts, decisions, next_target, validations)


if __name__ == "__main__":
    main()
