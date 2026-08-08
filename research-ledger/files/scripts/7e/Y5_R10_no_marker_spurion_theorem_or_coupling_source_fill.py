from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "763-Y5-R10-no-marker-spurion-theorem-or-coupling-source-fill.md"
NEXT_TARGET = "764-Y5-R10-constant-superselection-and-charge-normalization-or-source-fill.md"
STATUS = "Y5_R10_763_no_marker_spurion_theorem_attempt_not_parent_signed_qbarXT_channels_retained"
CLAIM_CEILING = "classification_contract_only_no_qbarXT_zero_no_cg_zero_no_EM_charge_no_PPN_Newton_or_local_GR_pass"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

MARKER_CLASSIFIER_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_763_MARKER_CLASSIFIER_INPUT_CANDIDATE.csv"
CONSTANT_CHARGE_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_763_CONSTANT_CHARGE_INPUT_CANDIDATE.csv"
SOURCE_WEIGHT_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_763_SOURCE_WEIGHT_INPUT_CANDIDATE.csv"
NONHILBERT_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_763_NONHILBERT_CURRENT_INPUT_CANDIDATE.csv"
POST_READOUT_EFT_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_763_POST_READOUT_EFT_BRANCH_CANDIDATE.csv"
EM_INTERFACE_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_759_EM_CHARGE_INTERFACE_INPUT_CANDIDATE.csv"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_763_SOURCE_REGISTER.csv"
THEOREM_ATTEMPT_PATH = RESIDUALS / "P8_Y5_R10_763_NO_MARKER_SPURION_THEOREM_ATTEMPT.csv"
CLASSIFICATION_GATE_PATH = RESIDUALS / "P8_Y5_R10_763_SPURION_CLASSIFICATION_GATE.csv"
QBARXT_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_763_QBARXT_CHANNEL_UPDATE.csv"
SOURCE_FILL_PATH = RESIDUALS / "P8_Y5_R10_763_COUPLING_SOURCE_FILL_SCHEMA.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_763_DECISION_MATRIX.csv"
ROUTE_PATH = RESIDUALS / "P8_Y5_R10_763_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_763_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_763_VALIDATION.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "762_doc": {
        "path": POST_CHECKPOINT / "762-Y5-R10-geometry-stack-descent-or-coupling-source-fill.md",
        "needles": [
            "Current result: **geometry-stack descent is not parent-signed**",
            "763-Y5-R10-no-marker-spurion-theorem-or-coupling-source-fill.md",
        ],
        "role": "immediate no-marker/no-spurion handoff",
    },
    "762_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_762_VALIDATION.csv",
        "needles": ["V762_15_validation_rows_ready", "V762_13_formalization_workbench_untouched"],
        "role": "prior validation guard",
    },
    "762_counterexamples": {
        "path": RESIDUALS / "P8_Y5_R10_762_GEOMETRY_STACK_COUNTEREXAMPLE_LEDGER.csv",
        "needles": ["GCE762_3_charge_normalization_derivative", "fine-structure/charge residual survives"],
        "role": "charge-normalization derivative leak",
    },
    "762_source_fill": {
        "path": RESIDUALS / "P8_Y5_R10_762_COUPLING_SOURCE_FILL_SCHEMA.csv",
        "needles": ["GSF762_4_EM_charge_interface", "schema_only_candidate_missing=true"],
        "role": "open EM/charge interface artifact",
    },
    "622_parent_contract": {
        "path": RESIDUALS / "P8_Y5_R10_622_PARENT_MATTER_CONTRACT.csv",
        "needles": ["PMC622_3_marker_taxonomy", "PMC622_4_constant_superselection", "PMC622_5_universal_source"],
        "role": "parent matter marker/constants/source contract",
    },
    "621_normal_form": {
        "path": POST_CHECKPOINT / "621-Y5-R10-matter-coupling-normal-form-theorem-or-residual-coefficient-priors.md",
        "needles": ["NMF621_2_no_material_marker", "NMF621_3_constant_triviality", "NMF621_4_universal_source_current"],
        "role": "normal-form theorem clauses",
    },
    "620_residual_envelope": {
        "path": POST_CHECKPOINT / "620-Y5-R10-qbarXT-residual-envelope-after-no-marker-failure.md",
        "needles": ["qbar_XT_vec = (b_g, b_theta, b_m, b_kappa, b_NH, b_EFT)", "QXT620_2_marker"],
        "role": "residual vector after no-marker failure",
    },
    "619_no_marker_attempt": {
        "path": POST_CHECKPOINT / "619-Y5-R10-no-marker-minimal-quotient-theorem-or-qbarXT-residual-fill.md",
        "needles": ["NMT619_2_no_natural_marker", "NMT619_5_no_marker_theorem_verdict"],
        "role": "earlier no-marker theorem attempt",
    },
    "410_quotient_functor_attempt": {
        "path": POST_CHECKPOINT / "410-quotient-matter-functor-theorem-attempt.md",
        "needles": ["marker_extended_quotient", "no_marker_theorem_derived"],
        "role": "older marker counterexample record",
    },
}


def utc_stamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def text_contains(path: Path, needles: list[str]) -> bool:
    text = read_text(path)
    return bool(text) and all(needle in text for needle in needles)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def bool_string(value: bool) -> str:
    return "true" if value else "false"


def markdown_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(markdown_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, divider, *body])


def under_post(path: Path) -> bool:
    try:
        path.resolve().relative_to(POST_CHECKPOINT.resolve())
        return True
    except ValueError:
        return False


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return -1
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > FORMALIZATION_CUTOFF:
            count += 1
    return count


def make_source_register(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(spec["path"]),
            "exists": bool_string(Path(spec["path"]).exists()),
            "needle_check": bool_string(text_contains(Path(spec["path"]), spec["needles"])),
            "role": spec["role"],
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for source_id, spec in SOURCES.items()
    ]


def theorem_attempt_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "NMS763_0_classification_theorem",
            "claim_shape": "Hidden marker/spurion channels close only if every matter-visible marker, constant, coupling, source weight, and post-readout term is classified.",
            "mathematical_form": "For every vertical v in ker(Dq), Lie_v S_matter=0 if each visible spurion sigma is absent, pure gauge with observable-zero action, Q-only with Lie_v sigma=0, source-independent auxiliary with zero projection, or retained in R_phys.",
            "current_status": "valid_conditional_theorem_shape_not_parent_signed",
            "blocker": "the current parent branch has not classified theta_A, alpha_EM, charge normalization, mass ratios, source weights, non-Hilbert currents, or marker fields",
            "residual_channel": "qbar_XT_vec",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "NMS763_1_no_material_marker",
            "claim_shape": "No matter-visible marker with nonzero vertical derivative is allowed unless retained as a physical residual field.",
            "mathematical_form": "m visible to ordinary matter implies Lie_v m=0, gauge/exact, source-independent zero-projection, or m in R_phys.",
            "current_status": "not_parent_signed",
            "blocker": "marker-extended quotient remains a legal counterexample until the parent action supplies a marker taxonomy",
            "residual_channel": "b_m",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "NMS763_2_constant_superselection",
            "claim_shape": "Ordinary constants are selector-trivial superselection labels rather than vertical fields.",
            "mathematical_form": "Lie_v theta_A=Lie_v alpha_EM=Lie_v q_A=Lie_v(m_A/m_B)=0 for ordinary-sector labels.",
            "current_status": "not_parent_signed",
            "blocker": "charge normalization and mass-ratio derivatives can still leak through D_m even when the metric descends",
            "residual_channel": "b_theta",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "NMS763_3_universal_source_weight",
            "claim_shape": "All ordinary matter sources one universal Hilbert/coframe current with one universal kappa.",
            "mathematical_form": "S_source=sum_A kappa T_A -> kappa sum_A T_A; no kappa_A(X) source splitting.",
            "current_status": "not_parent_signed",
            "blocker": "species-weighted sources remain legal without Ward/Noether ownership of the universal current",
            "residual_channel": "b_kappa",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "NMS763_4_nonHilbert_current",
            "claim_shape": "Spin, torsion, edge, or topological currents are absent, exact/gauge, zero-projection, or retained.",
            "mathematical_form": "J_NH visible implies P_A J_NH=0 by theorem/gauge/exactness or J_NH in R_phys with a sourced projection.",
            "current_status": "not_parent_signed",
            "blocker": "boundary/local projection silence is not parent-owned for every matter arena",
            "residual_channel": "b_NH",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "NMS763_5_post_readout_EFT",
            "claim_shape": "No post-readout EFT counterterm receives theorem credit in the parent-derived local branch.",
            "mathematical_form": "Delta L_EFT is either absent from the parent branch, explicitly phenomenological, or retained as b_EFT; it is never silently used as descent.",
            "current_status": "policy_signed_not_positive_theorem_evidence",
            "blocker": "policy can prevent cheating, but it cannot prove the parent action has the desired coupling structure",
            "residual_channel": "b_EFT",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "NMS763_6_verdict",
            "claim_shape": "No-marker/no-spurion theorem closes qbar_XT only when all clauses NMS763_1..NMS763_5 are parent-signed.",
            "mathematical_form": "qbar_XT_vec=(b_g,b_theta,b_m,b_kappa,b_NH,b_EFT)=0 only after geometry-stack descent and all marker/spurion/source clauses close.",
            "current_status": "no_marker_spurion_theorem_not_parent_signed",
            "blocker": "b_g from geometry stack and b_theta/b_m/b_kappa/b_NH remain open",
            "residual_channel": "qbar_XT_vec",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def classification_gate_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "SCG763_0_absent",
            "classification": "absent",
            "allowed_if": "the parent branch contains no matter-visible instance of the marker/spurion",
            "effect_on_vertical_derivative": "zero by absence",
            "required_evidence": "source path showing term absent from the parent matter action",
            "if_not_proved": "retain the corresponding residual channel",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "SCG763_1_pure_gauge",
            "classification": "pure_gauge_or_exact",
            "allowed_if": "vertical motion is gauge, boundary exact, and observable-zero in the local arena",
            "effect_on_vertical_derivative": "zero after quotient/gauge projection",
            "required_evidence": "Ward identity, gauge generator, boundary condition, and local projection proof",
            "if_not_proved": "retain b_NH or marker residual",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "SCG763_2_Q_only",
            "classification": "Q_only_quotient_data",
            "allowed_if": "the object is a function only of q(Phi), not the representative",
            "effect_on_vertical_derivative": "Lie_v sigma=0 for v in ker(Dq)",
            "required_evidence": "factorization certificate sigma(Phi)=sigmabar(q(Phi))",
            "if_not_proved": "retain the relevant qbar_XT channel",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "SCG763_3_auxiliary",
            "classification": "source_independent_auxiliary_zero_projection",
            "allowed_if": "auxiliary solves algebraically/universally and has zero observable projection in the local arena",
            "effect_on_vertical_derivative": "zero after elimination/projection",
            "required_evidence": "auxiliary EOM plus source-independence and arena projection proof",
            "if_not_proved": "retain b_m or b_NH",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "SCG763_4_retained",
            "classification": "retained_physical_field_or_residual",
            "allowed_if": "the object is promoted into R_phys/source pack with units, projection, and bound route",
            "effect_on_vertical_derivative": "not zero; carried explicitly",
            "required_evidence": "residual coefficient definition, source path, projection matrix, and bound data",
            "if_not_proved": "blocked, not claimable",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "SCG763_5_forbidden_hidden_spurion",
            "classification": "forbidden_hidden_spurion",
            "allowed_if": "never allowed as theorem credit",
            "effect_on_vertical_derivative": "unknown/nonzero",
            "required_evidence": "classification into one of SCG763_0..SCG763_4",
            "if_not_proved": "local branch remains residual-only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def qbarxt_update_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "channel_id": "QCU763_0_b_g",
            "component": "b_g",
            "current_status": "open_from_geometry_stack_762",
            "why_open": "measure/coframe/connection/derivative stack is not parent-signed",
            "allowed_next_move": "geometry-stack certificate or sourced coupling bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "channel_id": "QCU763_1_b_theta",
            "component": "b_theta",
            "current_status": "open_constants_charge_normalization",
            "why_open": "theta_A, alpha_EM, q_A, and mass-ratio derivatives are not proved selector-trivial",
            "allowed_next_move": "constant superselection and charge-normalization descent proof, or source rows/bounds",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "channel_id": "QCU763_2_b_m",
            "component": "b_m",
            "current_status": "open_marker_projection",
            "why_open": "matter-visible markers are not classified as absent/gauge/Q-only/auxiliary/retained",
            "allowed_next_move": "marker classifier certificate or composition/R10 residual bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "channel_id": "QCU763_3_b_kappa",
            "component": "b_kappa",
            "current_status": "open_source_weight_splitting",
            "why_open": "universal Hilbert/coframe current with one kappa is not parent-derived",
            "allowed_next_move": "Ward/Noether universal-source proof or WEP/source-material bound rows",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "channel_id": "QCU763_4_b_NH",
            "component": "b_NH",
            "current_status": "open_nonHilbert_current",
            "why_open": "spin/torsion/topological/edge currents are not proved absent, exact, or zero-projection",
            "allowed_next_move": "boundary/projection silence proof or current residual bound rows",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "channel_id": "QCU763_5_b_EFT",
            "component": "b_EFT",
            "current_status": "phenomenology_only_if_used",
            "why_open": "post-readout EFT terms cannot be counted as parent-derived closure",
            "allowed_next_move": "exclude from derived branch or label as explicit phenomenological residual",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "channel_id": "QCU763_6_vector",
            "component": "qbar_XT_vec",
            "current_status": "residual_vector_retained",
            "why_open": "multiple components remain unsigned",
            "allowed_next_move": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def source_fill_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "fill_id": "CSF763_0_marker_classifier_certificate",
            "artifact": str(MARKER_CLASSIFIER_CANDIDATE_PATH),
            "required_columns": "marker_id;visible_to_matter;classification;vertical_derivative;observable_projection;source_path;valid_for_claim",
            "claim_gate": "every matter-visible marker is classified into SCG763_0..SCG763_4",
            "current_status": f"schema_only_candidate_missing={bool_string(not MARKER_CLASSIFIER_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "CSF763_1_constants_charge_normalization",
            "artifact": str(CONSTANT_CHARGE_CANDIDATE_PATH),
            "required_columns": "constant_id;sector;superselection_status;vertical_derivative;normalization_owner;source_path;valid_for_claim",
            "claim_gate": "theta_A, alpha_EM, q_A, mass ratios are selector-trivial or retained as residuals",
            "current_status": f"schema_only_candidate_missing={bool_string(not CONSTANT_CHARGE_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "CSF763_2_species_source_weight",
            "artifact": str(SOURCE_WEIGHT_CANDIDATE_PATH),
            "required_columns": "species_or_class;kappa_A_over_kappa;source_current_owner;projection;bound_or_theorem;source_path;valid_for_claim",
            "claim_gate": "one universal source current or explicit bounded kappa_A splitting",
            "current_status": f"schema_only_candidate_missing={bool_string(not SOURCE_WEIGHT_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "CSF763_3_nonHilbert_edge_current",
            "artifact": str(NONHILBERT_CANDIDATE_PATH),
            "required_columns": "current_id;type;absent_exact_or_retained;projection;arena;source_path;valid_for_claim",
            "claim_gate": "spin/torsion/topological/edge current is zero-projection or explicitly retained",
            "current_status": f"schema_only_candidate_missing={bool_string(not NONHILBERT_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "CSF763_4_post_readout_EFT_branch",
            "artifact": str(POST_READOUT_EFT_CANDIDATE_PATH),
            "required_columns": "term_id;parent_branch_or_post_readout;phenomenology_flag;projection;source_path;valid_for_claim",
            "claim_gate": "post-readout terms are excluded from derived closure or labelled phenomenological",
            "current_status": f"schema_only_candidate_missing={bool_string(not POST_READOUT_EFT_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "CSF763_5_EM_charge_interface",
            "artifact": str(EM_INTERFACE_CANDIDATE_PATH),
            "required_columns": "sector;charge_current_owner;metric_or_coframe_used;normalization;alpha_or_charge_response;source_path;valid_for_claim",
            "claim_gate": "charge/current derivative operator descends or b_theta is bounded",
            "current_status": f"schema_only_candidate_missing={bool_string(not EM_INTERFACE_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D763_0_theorem_attempt",
            "decision": "write no-marker/no-spurion theorem as a classification theorem",
            "reason": "a blanket no-marker axiom would smuggle in the result; classification is the auditable version",
            "claim_status": "conditional_theorem_shape_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D763_1_no_qbarXT_zero",
            "decision": "do not promote qbar_XT_vec=0",
            "reason": "constants, charge normalization, markers, source weights, and non-Hilbert currents are not parent-signed",
            "claim_status": "not_promoted",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D763_2_next",
            "decision": "attack constant superselection and charge normalization next",
            "reason": "the sharpest concrete leak after 762 is D_m=d+iq_A(X)A+omega[E(q)], which can move alpha_EM/charge while geometry descends",
            "claim_status": "next_target_selected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU763_0_allowed",
            "allowed_after_763": "treat no-marker/no-spurion as a classification contract",
            "forbidden_after_763": "set hidden marker or constant derivatives to zero without source-backed classification",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU763_1_allowed",
            "allowed_after_763": "keep qbar_XT_vec as a residual vector with open components",
            "forbidden_after_763": "collapse qbar_XT_vec to a scalar zero before component proofs or bounds",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU763_2_allowed",
            "allowed_after_763": "focus next on constants, charge normalization, and alpha_EM ownership",
            "forbidden_after_763": "claim EM/charge or local-GR closure from geometry descent alone",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def summary_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "no-marker/no-spurion route is a valid classification theorem shape but not parent-signed",
            "hard_blocker": "theta/charge/constants, material markers, source weights, and non-Hilbert currents remain unclassified",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    qbarxt: list[dict[str, Any]],
    source_fill: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    validation: list[dict[str, str]] = []
    validation.append({"check_id": "V763_0_source_paths_exist", "result": "pass" if all(row["exists"] == "true" for row in sources) else "fail", "detail": f"source_rows={len(sources)}"})
    validation.append({"check_id": "V763_1_source_needles_present", "result": "pass" if all(row["needle_check"] == "true" for row in sources) else "fail", "detail": "all local source needles present"})
    prior_762 = read_csv_rows(RESIDUALS / "P8_Y5_BRR545_762_VALIDATION.csv")
    validation.append({"check_id": "V763_2_prior_762_clean", "result": "pass" if prior_762 and all(row.get("result") == "pass" for row in prior_762) else "fail", "detail": "762 validation has no failures"})
    validation.append({"check_id": "V763_3_theorem_shape_written", "result": "pass" if len(theorem) == 7 and any(row["theorem_id"] == "NMS763_6_verdict" for row in theorem) else "fail", "detail": "no-marker/spurion theorem rows present"})
    validation.append({"check_id": "V763_4_theorem_not_parent_signed", "result": "pass" if any(row["theorem_id"] == "NMS763_6_verdict" and row["current_status"] == "no_marker_spurion_theorem_not_parent_signed" for row in theorem) else "fail", "detail": "theorem remains nonclaim"})
    validation.append({"check_id": "V763_5_classification_gate_complete", "result": "pass" if len(gates) == 6 and {row["classification"] for row in gates} == {"absent", "pure_gauge_or_exact", "Q_only_quotient_data", "source_independent_auxiliary_zero_projection", "retained_physical_field_or_residual", "forbidden_hidden_spurion"} else "fail", "detail": "spurion classifications enumerated"})
    expected_components = {"b_g", "b_theta", "b_m", "b_kappa", "b_NH", "b_EFT", "qbar_XT_vec"}
    validation.append({"check_id": "V763_6_qbarXT_channels_retained", "result": "pass" if {row["component"] for row in qbarxt} == expected_components and all(row["valid_for_claim"] == "false" for row in qbarxt) else "fail", "detail": "qbarXT components remain residuals"})
    validation.append({"check_id": "V763_7_source_fill_schema_written", "result": "pass" if len(source_fill) == 6 and all(row["valid_for_claim"] == "false" for row in source_fill) else "fail", "detail": "source-fill rows schema-only"})
    candidate_paths = [MARKER_CLASSIFIER_CANDIDATE_PATH, CONSTANT_CHARGE_CANDIDATE_PATH, SOURCE_WEIGHT_CANDIDATE_PATH, NONHILBERT_CANDIDATE_PATH, POST_READOUT_EFT_CANDIDATE_PATH, EM_INTERFACE_CANDIDATE_PATH]
    validation.append({"check_id": "V763_8_candidate_artifacts_not_faked", "result": "pass" if not any(path.exists() for path in candidate_paths) else "fail", "detail": "no claim-input artifacts fabricated"})
    all_generated = theorem + gates + qbarxt + source_fill + decisions + routes + summary
    validation.append({"check_id": "V763_9_no_claim_rows_promoted", "result": "pass" if all(row.get("valid_for_claim") == "false" for row in all_generated) else "fail", "detail": "all generated rows valid_for_claim=false"})
    validation.append({"check_id": "V763_10_no_local_arena_claim", "result": "pass" if "no_PPN_Newton_or_local_GR_pass" in CLAIM_CEILING else "fail", "detail": "local claims remain blocked"})
    validation.append({"check_id": "V763_11_next_target_selected", "result": "pass" if all(row.get("next_action") == NEXT_TARGET for row in routes) and all(row.get("next_target") == NEXT_TARGET for row in decisions) and summary[0].get("next_target") == NEXT_TARGET else "fail", "detail": NEXT_TARGET})
    output_paths = [
        Path(__file__),
        OUTPUT_DOC,
        SOURCE_REGISTER_PATH,
        THEOREM_ATTEMPT_PATH,
        CLASSIFICATION_GATE_PATH,
        QBARXT_UPDATE_PATH,
        SOURCE_FILL_PATH,
        DECISION_PATH,
        ROUTE_PATH,
        SUMMARY_PATH,
        VALIDATION_PATH,
    ]
    validation.append({"check_id": "V763_12_outputs_scoped", "result": "pass" if all(under_post(path) for path in output_paths) else "fail", "detail": "all outputs under post-checkpoint-work"})
    fw_count = formalization_changed_after_cutoff()
    validation.append({"check_id": "V763_13_formalization_workbench_untouched", "result": "pass" if fw_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={fw_count}"})
    validation.append({"check_id": "V763_14_charge_next", "result": "pass" if "constant-superselection-and-charge-normalization" in NEXT_TARGET else "fail", "detail": "next attacks constant/charge leak"})
    validation.append({"check_id": "V763_15_validation_rows_ready", "result": "pass", "detail": "validation table constructed"})
    return validation


def build_doc(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    qbarxt: list[dict[str, Any]],
    source_fill: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 763 - Y5 R10 No-Marker/Spurion Theorem Or Coupling Source Fill

Start point: 762 showed that geometry-stack descent is necessary but not enough. Even if the matter measure/coframe/connection descends, a hidden material marker, an `X`-dependent constant, a charge normalization, a species source weight, or a non-Hilbert current can still leak into local observables.

Current result: **the no-marker/no-spurion theorem is only a classification theorem shape, not a parent-signed theorem**. The honest rule is not "there are no markers"; it is "every marker/spurion must be classified as absent, pure gauge/exact, quotient-only, source-independent zero-projection auxiliary, or retained as a real residual." Until that is done, `qbar_XT_vec` remains open.

## Summary

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target"])}

## No-Marker/Spurion Theorem Attempt

{markdown_table(theorem, ["theorem_id", "claim_shape", "mathematical_form", "current_status", "blocker", "residual_channel", "valid_for_claim"])}

## Spurion Classification Gate

{markdown_table(gates, ["gate_id", "classification", "allowed_if", "effect_on_vertical_derivative", "required_evidence", "if_not_proved", "valid_for_claim"])}

## qbar_XT Channel Update

{markdown_table(qbarxt, ["channel_id", "component", "current_status", "why_open", "allowed_next_move", "valid_for_claim"])}

## Coupling Source-Fill Schema

{markdown_table(source_fill, ["fill_id", "artifact", "required_columns", "claim_gate", "current_status", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim"])}

## Route Update

{markdown_table(routes, ["route_id", "allowed_after_763", "forbidden_after_763", "next_action", "valid_for_claim"])}

## Local Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Plain-English Verdict

This is a useful result, but not a win-claim. It turns the "coupling" gut feeling into a clean audit target: hidden constants and charge normalization are now the sharpest leak. Next we either prove `alpha_EM`, charge/current normalization, mass ratios, and `theta_A` are true superselection/quotient data, or we keep them as explicit residual source rows. No sleight of hand, no fake knockout — just footwork and a nasty little counterpunch.
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = make_source_register(generated_utc)
    theorem = theorem_attempt_rows(generated_utc)
    gates = classification_gate_rows(generated_utc)
    qbarxt = qbarxt_update_rows(generated_utc)
    source_fill = source_fill_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    routes = route_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validate(sources, theorem, gates, qbarxt, source_fill, decisions, routes, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(THEOREM_ATTEMPT_PATH, theorem, ["theorem_id", "claim_shape", "mathematical_form", "current_status", "blocker", "residual_channel", "valid_for_claim", "generated_utc"])
    write_csv(CLASSIFICATION_GATE_PATH, gates, ["gate_id", "classification", "allowed_if", "effect_on_vertical_derivative", "required_evidence", "if_not_proved", "valid_for_claim", "generated_utc"])
    write_csv(QBARXT_UPDATE_PATH, qbarxt, ["channel_id", "component", "current_status", "why_open", "allowed_next_move", "valid_for_claim", "generated_utc"])
    write_csv(SOURCE_FILL_PATH, source_fill, ["fill_id", "artifact", "required_columns", "claim_gate", "current_status", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_PATH, routes, ["route_id", "allowed_after_763", "forbidden_after_763", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, theorem, gates, qbarxt, source_fill, decisions, routes, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        print(f"wrote {OUTPUT_DOC}")
        print(f"wrote {VALIDATION_PATH}")
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")
        raise SystemExit(1)
    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")


if __name__ == "__main__":
    main()
