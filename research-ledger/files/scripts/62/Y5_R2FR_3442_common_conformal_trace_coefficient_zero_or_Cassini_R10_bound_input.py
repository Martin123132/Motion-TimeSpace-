from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv"
DOC = ROOT / "3442-Y5-R2FR-common-conformal-trace-coefficient-zero-or-Cassini-R10-bound-input-under-AX1090.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCES = {
    "doc_3441": ROOT / "3441-Y5-R2FR-one-channel-no-linear-X-signature-or-BHX-coefficient-pack-under-AX1090.md",
    "next_3441": OUT / "P8_Y5_R2FR_3441_NEXT_TARGET.csv",
    "ctrace_3441": OUT / "P8_Y5_R2FR_3441_TRACE_COUPLING_COEFFICIENT_DEFINITION.csv",
    "bhx_pack_3441": OUT / "P8_Y5_R2FR_3441_BHX_COEFFICIENT_PACK.csv",
    "score_interface_3441": OUT / "P8_Y5_R2FR_3441_R10_PPN_SCORE_INTERFACE.csv",
    "newton_gr_3441": OUT / "P8_Y5_R2FR_3441_NEWTON_GR_IMPACT.csv",
    "doc_1029": ROOT / "1029-Y5-R10-cg-no-shadow-frame-theorem-or-first-numeric-coupling-row.md",
    "no_shadow_1029": OUT / "P8_Y5_R10_1029_NO_SHADOW_FRAME_THEOREM_AUDIT.csv",
    "cg_intake_1029": OUT / "P8_Y5_R10_1029_CG_INTAKE_TEMPLATE.csv",
    "tau_requirements_1029": OUT / "P8_Y5_R10_1029_TAU_PROJECTION_REQUIREMENTS.csv",
    "doc_1030": ROOT / "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md",
    "spm_contract_1030": OUT / "P8_Y5_R10_1030_PUBLIC_METRIC_ACTION_CONTRACT.csv",
    "spm_audit_1030": OUT / "P8_Y5_R10_1030_SINGLE_PUBLIC_METRIC_DERIVATION_AUDIT.csv",
    "cg_gate_1030": OUT / "P8_Y5_R10_1030_CG_PROVENANCE_GATE_BINDING.csv",
    "doc_1088": ROOT / "1088-Y5-R10-minimal-parent-ordinary-matter-signature-clause-or-finite-coefficient-intake.md",
    "moms_clause_1088": OUT / "P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv",
    "moms_countermodels_1088": OUT / "P8_Y5_R10_1088_COUNTERMODEL_RETENTION.csv",
    "local_bounds": LOCAL_BOUNDS,
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3442_SOURCE_REGISTER.csv",
    "cconf_zero_theorem_attempt": OUT / "P8_Y5_R2FR_3442_CCONF_ZERO_THEOREM_ATTEMPT.csv",
    "terminal_metric_signature_audit": OUT / "P8_Y5_R2FR_3442_TERMINAL_METRIC_SIGNATURE_AUDIT.csv",
    "cconf_finite_bound_input": OUT / "P8_Y5_R2FR_3442_CCONF_FINITE_BOUND_INPUT.csv",
    "cassini_translation_nonclaim": OUT / "P8_Y5_R2FR_3442_CASSINI_TRANSLATION_NONCLAIM.csv",
    "r10_wep_interface": OUT / "P8_Y5_R2FR_3442_R10_WEP_INTERFACE.csv",
    "ctrace_update": OUT / "P8_Y5_R2FR_3442_CTRACE_UPDATE.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3442_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3442_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3442_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3442_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3442_VALIDATION.csv",
}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def local_bound(row_id: str) -> dict[str, str]:
    for row in read_csv(LOCAL_BOUNDS):
        if row.get("row_id") == row_id:
            return row
    return {}


def parse_float(value: str | None) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields = list(rows[0].keys())

    def clean(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "/")

    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |",
            *["| " + " | ".join(clean(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def source_register() -> list[dict[str, Any]]:
    roles = {
        "doc_3441": "one-channel trace/mass-source handoff",
        "next_3441": "machine-readable 3442 target",
        "ctrace_3441": "C_trace component definition including C_conf",
        "bhx_pack_3441": "trace-channel B_HX coefficient pack",
        "score_interface_3441": "R10/PPN/WEP score interfaces for trace channel",
        "newton_gr_3441": "Newton/GR impact from selected trace channel",
        "doc_1029": "conditional c_g/no-shadow theorem text",
        "no_shadow_1029": "conditional no-shadow-frame theorem audit",
        "cg_intake_1029": "finite c_g intake template",
        "tau_requirements_1029": "tau_R10/tau_PPN projection requirements",
        "doc_1030": "strict demotion of c_g zero absent terminal public metric",
        "spm_contract_1030": "single-public-metric action contract",
        "spm_audit_1030": "single-public-metric derivation audit",
        "cg_gate_1030": "finite c_g provenance gate",
        "doc_1088": "ordinary matter signature and shadow-frame countermodels",
        "moms_clause_1088": "minimal ordinary matter signature clauses",
        "moms_countermodels_1088": "surviving ordinary matter countermodels",
        "local_bounds": "R1/R3/R10 bound anchors",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[source_id],
            "valid_for_claim": False,
        }
        for source_id, path in SOURCES.items()
    ]


def cconf_zero_theorem_attempt() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "CZT3442_0_define",
            "claim_piece": "common conformal trace coefficient",
            "derivation": "g_m = exp(2 A_T(X_T)) g_pub; C_conf := a_T := dA_T/dX_T|0 after fixing X_T normalization",
            "result": "DEFINITION_SHARP",
            "current_status": "not_a_claim",
            "gap": "X_T normalization and matter-frame ownership must be fixed before scoring",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CZT3442_1_terminal_metric_zero",
            "claim_piece": "terminal public metric kills A_T representative dependence",
            "derivation": "If ordinary matter is a functor on Q_obs with terminal e_pub(q(Phi)), then any allowed matter frame either equals/factors through e_pub or is an explicit extra observable object. For v_X in ker(Dq), Lie_v A_T(q(Phi))=DA_T[Dq(v_X)]=0.",
            "result": "C_conf=a_T=0 if terminal-public-metric/no-extra-frame clause is parent-signed",
            "current_status": "EXACT_CONDITIONAL_THEOREM",
            "gap": "1030 says terminal e_pub/no-extra-frame is a contract, not a parent-signed theorem",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CZT3442_2_common_frame_countermodel",
            "claim_piece": "why covariance/WEP cannot kill C_conf",
            "derivation": "S_m[Psi,exp(2a_T X_T)g_pub] is diffeomorphism covariant and universal across species, so WEP composition spread can be quiet while Shapiro/R10/source normalization are shifted",
            "result": "COMMON_FRAME_COUNTERMODEL_SURVIVES",
            "current_status": "zero_not_promoted",
            "gap": "no-shadow-frame must be derived from parent action domain, not from covariance or WEP",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CZT3442_3_frame_rename_guard",
            "claim_piece": "do not hide C_conf by frame choice",
            "derivation": "Choosing the Jordan frame removes A_T from g_m but moves the same derivative into masses, alpha_EM, G_eff or source normalization unless a same-frame ledger closes every slot",
            "result": "C_conf requires same-frame matter/constants/source ledger",
            "current_status": "GUARD_RETAINED",
            "gap": "constant superselection and source-normalization owner remain separate gates",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CZT3442_4_verdict",
            "claim_piece": "current C_conf zero",
            "derivation": "The theorem route is clean: terminal public metric plus no-extra-frame gives C_conf=0 by chain rule. Current corpus does not sign that terminal object, so finite C_conf remains live.",
            "result": "ZERO_THEOREM_NOT_PROMOTED_FINITE_BOUND_ROW_REQUIRED",
            "current_status": "nonclaim",
            "gap": "derive terminal metric/no-shadow from parent action or bound a_T/C_conf",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def terminal_metric_signature_audit() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "TMS3442_0_public_metric_object",
            "required_signature": "e_pub=e_obs(q(Phi)) is the unique public coframe/metric for ordinary rods, clocks, photons, free fall and source readout",
            "source_status": "SPM1030_0_CONTRACT_WRITTEN_NOT_PARENT_SIGNED",
            "if_signed": "A_T(X_T)g_pub is not an independent ordinary matter argument",
            "if_unsigned": "common Jordan/scalar-tensor frame remains legal",
            "valid_for_claim": False,
        },
        {
            "clause_id": "TMS3442_1_matter_functor_domain",
            "required_signature": "S_matter: Q_obs x MatterFields x Theta_Q -> R, not S_matter[Phi_rep]",
            "source_status": "SPM1030_1_CONTRACT_WRITTEN_NOT_PARENT_SIGNED",
            "if_signed": "representative X_T cannot enter matter frame",
            "if_unsigned": "A_T(X_T) can be a hidden matter-frame slot",
            "valid_for_claim": False,
        },
        {
            "clause_id": "TMS3442_2_no_shadow_frame_slot",
            "required_signature": "Allowed[S_matter] excludes independent A_T(X_T), B_T(X_T), and U_mu shadow-frame coefficients",
            "source_status": "SPM1030_2_EXACT_CLOSURE_CLAUSE_NOT_DERIVED",
            "if_signed": "C_conf=0 and disformal sibling is separately absent/retained",
            "if_unsigned": "C_conf must be bounded and cannot be zeroed by notation",
            "valid_for_claim": False,
        },
        {
            "clause_id": "TMS3442_3_same_frame_ledger",
            "required_signature": "masses, charges, clocks, G_eff/kappa and active source use the same public-frame convention",
            "source_status": "SPM1030_3_TO_5_CONDITIONAL_OR_OPEN",
            "if_signed": "frame rename cannot move C_conf into constants/source normalization",
            "if_unsigned": "C_conf can reappear as b_A, b_alpha, C_src or support tail",
            "valid_for_claim": False,
        },
        {
            "clause_id": "TMS3442_4_verdict",
            "required_signature": "TMS3442_0 through TMS3442_3 parent-signed together",
            "source_status": "NOT_PARENT_SIGNED_CURRENT_CORPUS",
            "if_signed": "C_conf branch closes",
            "if_unsigned": "finite nonclaim bound input is mandatory",
            "valid_for_claim": False,
        },
    ]


def cconf_finite_bound_input() -> list[dict[str, Any]]:
    return [
        {
            "bound_input_id": "CFB3442_0_Cconf",
            "symbol": "C_conf",
            "definition": "common conformal trace coupling in g_m=exp(2 A_T(X_T))g_pub, with C_conf=dA_T/dX_T|0",
            "units": "1/[X_T_units]; dimensionless only if X_T is dimensionless/canonically normalized by source",
            "value": "MISSING_PARENT_NUMERIC_CCONF_OR_ZERO_THEOREM",
            "required_source": "parent action/frame clause defining A_T and X_T normalization, or terminal-public-metric zero theorem",
            "arena_projection": "Cassini gamma; R10 alpha(lambda); common clock/source response; WEP only through differences/markers",
            "current_status": "SOURCE_READY_NONCLAIM_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "bound_input_id": "CFB3442_1_alpha_ST",
            "symbol": "alpha_ST_eff",
            "definition": "standard scalar-tensor effective coupling used only as a translation scaffold: gamma-1=-2 alpha_ST^2/(1+alpha_ST^2)",
            "units": "dimensionless",
            "value": "derived_from_R3_gamma_only_under_standard_massless_ST_mapping",
            "required_source": "MTS-to-standard-ST normalization, long-range/screening profile, disformal/tail separation",
            "arena_projection": "Cassini gamma translation",
            "current_status": "NONCLAIM_TRANSLATION_SCAFFOLD",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "bound_input_id": "CFB3442_2_tau_R10",
            "symbol": "tau_R10_conf",
            "definition": "maps C_conf into R10 Yukawa alpha(lambda)",
            "units": "depends_on_profile_normalization",
            "value": "MISSING_TAU_R10_CONF",
            "required_source": "K_X(lambda), Qbar_XH, source/test profile convention, Z_T and lambda_T",
            "arena_projection": "R10 alpha(lambda)",
            "current_status": "MISSING_ARENA_PROJECTION",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "bound_input_id": "CFB3442_3_tau_PPN",
            "symbol": "tau_PPN_conf",
            "definition": "maps C_conf into gamma_minus_1/beta_minus_1 in chosen weak-field gauge",
            "units": "dimensionless response per normalized C_conf",
            "value": "MISSING_TAU_PPN_CONF",
            "required_source": "PPN response matrix, range/screening regime, gauge and disformal separation",
            "arena_projection": "Cassini gamma and planetary PPN",
            "current_status": "MISSING_PPN_RESPONSE_MATRIX",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def cassini_translation_nonclaim() -> list[dict[str, Any]]:
    gamma_row = local_bound("R3_gamma")
    gamma_bound = parse_float(gamma_row.get("upper_bound"))
    alpha_bound = None
    if gamma_bound is not None and 0 < gamma_bound < 2:
        alpha_bound = math.sqrt(gamma_bound / (2 - gamma_bound))
    return [
        {
            "translation_id": "CAS3442_0_bound_anchor",
            "source_row": "local_bound_claims.csv:R3_gamma",
            "gamma_abs_bound": gamma_bound if gamma_bound is not None else "MISSING_R3_GAMMA_BOUND",
            "gamma_units": gamma_row.get("units", "MISSING"),
            "reference": gamma_row.get("reference_path_or_url", "MISSING"),
            "standard_relation": "not_applied_anchor_row",
            "derived_alpha_ST_abs_bound": "not_applied_anchor_row",
            "status": "BOUND_ANCHOR_PRESENT" if gamma_bound is not None else "BOUND_ANCHOR_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "translation_id": "CAS3442_1_standard_ST_alpha_bound",
            "source_row": "local_bound_claims.csv:R3_gamma",
            "gamma_abs_bound": gamma_bound if gamma_bound is not None else "MISSING_R3_GAMMA_BOUND",
            "gamma_units": gamma_row.get("units", "MISSING"),
            "reference": gamma_row.get("reference_path_or_url", "MISSING"),
            "standard_relation": "|gamma-1| = 2 alpha_ST^2/(1+alpha_ST^2)",
            "derived_alpha_ST_abs_bound": f"{alpha_bound:.12g}" if alpha_bound is not None else "MISSING_ALPHA_BOUND",
            "status": "NUMERIC_TRANSLATION_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "translation_id": "CAS3442_2_MTS_mapping_blocker",
            "source_row": "P8_Y5_R2FR_3442_CCONF_FINITE_BOUND_INPUT.csv:CFB3442_0_Cconf",
            "gamma_abs_bound": gamma_bound if gamma_bound is not None else "MISSING_R3_GAMMA_BOUND",
            "gamma_units": gamma_row.get("units", "MISSING"),
            "reference": gamma_row.get("reference_path_or_url", "MISSING"),
            "standard_relation": "alpha_ST_eff = C_conf/sqrt(4*pi*G_obs*Z_T) only if MTS normalization, range, screening and matter-frame conventions are signed",
            "derived_alpha_ST_abs_bound": f"{alpha_bound:.12g}" if alpha_bound is not None else "MISSING_ALPHA_BOUND",
            "status": "MTS_CCONF_NOT_CLAIM_READY",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def r10_wep_interface() -> list[dict[str, Any]]:
    return [
        {
            "interface_id": "RWI3442_0_R10",
            "arena": "R10 inverse-square / Yukawa",
            "bound_anchor": "local_bound_claims.csv:R10_fifth_force",
            "C_conf_projection": "alpha_conf(lambda_T)=K_R10(lambda_T) Qbar_H^conf qbar_T^conf/(4*pi*G_obs*Z_T)",
            "what_is_missing": "claim-valid alpha(lambda) curve; Z_T; lambda_T; K_R10; Qbar_H; qbar_T; source paths",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "interface_id": "RWI3442_1_WEP",
            "arena": "MICROSCOPE / source-charge",
            "bound_anchor": "local_bound_claims.csv:R1_WEP_source_charge",
            "C_conf_projection": "common C_conf is composition-blind at leading order; WEP only bites if C_conf differs by material, leaks into constants, or combines with marker/source tails",
            "what_is_missing": "material-difference coefficients, marker ledger, no-cancellation split from C_src/b_A/b_alpha",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "interface_id": "RWI3442_2_clock_source",
            "arena": "clock/common-mode/source normalization",
            "bound_anchor": "local_bound_claims.csv:R2_clock_redshift and source-normalization ledgers",
            "C_conf_projection": "frame choice can move common C_conf into clock constants or G_eff/kappa unless same-frame ledger is signed",
            "what_is_missing": "constant superselection, measured-GM protocol, source-owner theorem",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def ctrace_update() -> list[dict[str, Any]]:
    return [
        {
            "update_id": "CTU3442_0_Cconf_status",
            "prior_component": "CT3441_3_C_conf",
            "before": "MISSING_COMMON_FRAME_COEFFICIENT_OR_TERMINAL_METRIC_THEOREM",
            "after": "EXACT_CONDITIONAL_ZERO_OR_CASSINI_TRANSLATION_NONCLAIM",
            "effect_on_C_trace": "C_trace remains finite/nonclaim until C_conf is parent-signed zero or source-normalized; no cancellation with other components allowed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "update_id": "CTU3442_1_Ctrace_envelope",
            "prior_component": "CT3441_0_C_trace",
            "before": "|C_trace| <= |C_XR|+|C_XT|+|C_conf|+|C_src|+|C_bdy|",
            "after": "|C_trace| <= |C_XR|+|C_XT|+|C_conf_bound|+|C_src|+|C_bdy| with C_conf_bound currently nonclaim",
            "effect_on_C_trace": "one component now has a standard Cassini translation scaffold but no MTS-normalized bound value",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    alpha_bound = cassini_translation_nonclaim()[1]["derived_alpha_ST_abs_bound"]
    return [
        {
            "gate_id": "PG3442_0_sources",
            "claim": "all 3442 sources exist",
            "gate_pass": all(path.exists() for path in SOURCES.values()),
            "reason": "source register path check",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3442_1_Cconf_zero",
            "claim": "C_conf=0 is parent-signed",
            "gate_pass": False,
            "reason": "terminal-public-metric/no-shadow-frame remains a 1030 contract, not a signed parent theorem",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3442_2_Cassini_bound",
            "claim": "Cassini produces a claim-ready MTS C_conf bound",
            "gate_pass": False,
            "reason": f"standard-ST translation alpha_ST<={alpha_bound} exists, but MTS-to-ST normalization/range/projection is missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3442_3_local_GR",
            "claim": "local GR/Newton source coupling is established for this channel",
            "gate_pass": False,
            "reason": "C_conf is controlled only conditionally/nonclaim; C_src, C_XR, C_XT and C_bdy remain open",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3442_0_zero_route",
            "decision": "Keep the C_conf zero theorem as an exact conditional theorem, not a claim.",
            "because": "terminal public metric/no-extra-frame naturality would kill C_conf by chain rule, but 1030 shows that parent signature is not signed",
            "next_action": "do not use common WEP silence or covariance as proof",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3442_1_bound_route",
            "decision": "Use Cassini as the first nonclaim translation scaffold for C_conf.",
            "because": "common conformal coupling is hit harder by PPN gamma than by composition WEP",
            "next_action": "source MTS normalization/range/projection before any numeric C_conf claim",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3442_2_next_component",
            "decision": "Move next to C_src/source normalization.",
            "because": "even if C_conf closes, Newtonian mechanics needs calibrated G/kappa/M_eff source ownership; this directly matches the GR/Newton bridge",
            "next_action": "derive source-owner zero or stage measured-GM/Gdot/source-flux bound inputs",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3443-Y5-R2FR-source-normalization-Csrc-zero-or-measured-GM-bound-input-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3443_source_normalization_Csrc_zero_or_measured_GM_bound_input.py",
            "objective": "attack C_src in the same trace channel: derive source-owner/G_eff/kappa/M_eff zero from parent Hilbert-source ownership, or stage a nonclaim measured-GM/Gdot/source-flux bound input",
            "success_condition": "C_src is either parent-signed zero in the selected trace channel or represented by schema-valid nonclaim bound rows linked to measured GM, Gdot and source-normalization ledgers",
            "valid_for_claim": False,
        }
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3442_0_Cconf",
            "branch_id": "OC3441_trace_mass_source",
            "zero_claim": False,
            "cassini_numeric_translation": True,
            "mts_score": False,
            "result": "NOT_SCORED",
            "why": "C_conf zero theorem unsigned and Cassini translation lacks MTS normalization/range/projection",
            "valid_for_claim": False,
        }
    ]


def local_bound_row_ids() -> set[str]:
    return {row.get("row_id", "") for row in read_csv(LOCAL_BOUNDS)}


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], start_utc: datetime) -> list[dict[str, Any]]:
    modified_count = 0
    if FORMALIZATION.exists():
        start_timestamp = start_utc.timestamp()
        modified_count = sum(
            1 for checked_path in FORMALIZATION.rglob("*") if checked_path.is_file() and checked_path.stat().st_mtime >= start_timestamp
        )

    nonclaim_ok = True
    for output_name, rows in rows_by_name.items():
        if output_name == "validation":
            continue
        for row in rows:
            if row.get("valid_for_claim") is True or str(row.get("valid_for_claim", "")).lower() == "true":
                nonclaim_ok = False
            if row.get("claim_allowed") is True or str(row.get("claim_allowed", "")).lower() == "true":
                nonclaim_ok = False

    bound_ids = local_bound_row_ids()
    cassini_alpha = rows_by_name["cassini_translation_nonclaim"][1]["derived_alpha_ST_abs_bound"]
    validations = [
        {
            "check_id": "VAL3442_0_sources_exist",
            "condition": "all cited 3442 source paths exist",
            "passed": all(path.exists() for path in SOURCES.values()),
            "detail": f"{sum(1 for path in SOURCES.values() if path.exists())}/{len(SOURCES)} source paths exist",
        },
        {
            "check_id": "VAL3442_1_zero_conditional",
            "condition": "C_conf zero theorem is present but not promoted",
            "passed": any(row["theorem_id"] == "CZT3442_4_verdict" and row["result"] == "ZERO_THEOREM_NOT_PROMOTED_FINITE_BOUND_ROW_REQUIRED" for row in rows_by_name["cconf_zero_theorem_attempt"]),
            "detail": "terminal metric chain-rule theorem retained as conditional",
        },
        {
            "check_id": "VAL3442_2_signature_unsigned",
            "condition": "terminal metric/no-shadow signature remains unsigned",
            "passed": any(row["clause_id"] == "TMS3442_4_verdict" and row["source_status"] == "NOT_PARENT_SIGNED_CURRENT_CORPUS" for row in rows_by_name["terminal_metric_signature_audit"]),
            "detail": "1030 stricter verdict preserved",
        },
        {
            "check_id": "VAL3442_3_cconf_bound_row",
            "condition": "finite C_conf bound input row exists",
            "passed": any(row["bound_input_id"] == "CFB3442_0_Cconf" and row["current_status"] == "SOURCE_READY_NONCLAIM_VALUES_MISSING" for row in rows_by_name["cconf_finite_bound_input"]),
            "detail": "C_conf acquisition row staged",
        },
        {
            "check_id": "VAL3442_4_cassini_translation",
            "condition": "Cassini standard-ST numeric translation exists but is nonclaim",
            "passed": cassini_alpha != "MISSING_ALPHA_BOUND" and any(row["translation_id"] == "CAS3442_2_MTS_mapping_blocker" for row in rows_by_name["cassini_translation_nonclaim"]),
            "detail": f"alpha_ST_bound_nonclaim={cassini_alpha}",
        },
        {
            "check_id": "VAL3442_5_bound_anchors",
            "condition": "R1/R3/R10 bound anchors are present",
            "passed": {"R1_WEP_source_charge", "R3_gamma", "R10_fifth_force"}.issubset(bound_ids),
            "detail": "local_bound_claims.csv anchors checked",
        },
        {
            "check_id": "VAL3442_6_nonclaim",
            "condition": "all generated rows remain nonclaim",
            "passed": nonclaim_ok,
            "detail": "valid_for_claim=false and claim_allowed=false wherever present",
        },
        {
            "check_id": "VAL3442_7_next_target_Csrc",
            "condition": "next target moves to C_src/source normalization",
            "passed": rows_by_name["next_target"][0]["target_doc"].startswith("3443-Y5-R2FR-source-normalization-Csrc"),
            "detail": rows_by_name["next_target"][0]["target_doc"],
        },
        {
            "check_id": "VAL3442_8_formalization_untouched",
            "condition": "formalization-workbench modified-file count remains 0 during this run",
            "passed": modified_count == 0,
            "detail": f"modified_count_since_start={modified_count}",
        },
    ]
    validations.append(
        {
            "check_id": "VAL3442_9_overall",
            "condition": "3442 C_conf checkpoint is internally valid",
            "passed": all(row["passed"] for row in validations),
            "detail": "PASS" if all(row["passed"] for row in validations) else "FAIL",
        }
    )
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    text = f"""# 3442 - Common Conformal Trace Coefficient Zero or Cassini/R10 Bound Input

## Summary
- This checkpoint attacks the `C_conf` part of the trace channel from 3441.
- The zero route is clean but conditional: if ordinary matter only sees the terminal public metric/coframe and no `A_T(X_T)` shadow-frame slot exists, then `C_conf=dA_T/dX_T=0` follows by vertical chain rule.
- The current corpus does not parent-sign that terminal-public-metric/no-shadow-frame clause, so `C_conf=0` is not claimed.
- The finite route is now sharper: Cassini gives a standard scalar-tensor translation `alpha_ST <= {rows_by_name["cassini_translation_nonclaim"][1]["derived_alpha_ST_abs_bound"]}`, but this is nonclaim until MTS supplies the normalization, range/screening and projection map.
- Next target moves to `C_src`, because even a killed `C_conf` does not give Newton/GR unless source normalization, measured `GM`, `G_eff/kappa`, and conserved mass flux are owned.

## Source Register
{md_table(rows_by_name["source_register"])}

## Cconf Zero Theorem Attempt
{md_table(rows_by_name["cconf_zero_theorem_attempt"])}

## Terminal Metric Signature Audit
{md_table(rows_by_name["terminal_metric_signature_audit"])}

## Cconf Finite Bound Input
{md_table(rows_by_name["cconf_finite_bound_input"])}

## Cassini Translation Nonclaim
{md_table(rows_by_name["cassini_translation_nonclaim"])}

## R10 / WEP Interface
{md_table(rows_by_name["r10_wep_interface"])}

## Ctrace Update
{md_table(rows_by_name["ctrace_update"])}

## Promotion Gates
{md_table(rows_by_name["promotion_gates"])}

## Decision Ledger
{md_table(rows_by_name["decision_ledger"])}

## Next Target
{md_table(rows_by_name["next_target"])}

## Runner Nonclaim
{md_table(rows_by_name["runner_nonclaim"])}

## Validation
{md_table(rows_by_name["validation"])}

## Bottom Line
`C_conf` is not solved, but it is no longer fog. It has a clean conditional death route and a concrete Cassini-facing finite route. The next most valuable move is `C_src`, because that is where Newton's measured source strength, `G`, `kappa`, and conserved mass flux either become derived structure or remain explicit residuals.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    start_utc = datetime.now(timezone.utc)
    rows_by_name = {
        "source_register": source_register(),
        "cconf_zero_theorem_attempt": cconf_zero_theorem_attempt(),
        "terminal_metric_signature_audit": terminal_metric_signature_audit(),
        "cconf_finite_bound_input": cconf_finite_bound_input(),
        "cassini_translation_nonclaim": cassini_translation_nonclaim(),
        "r10_wep_interface": r10_wep_interface(),
        "ctrace_update": ctrace_update(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    rows_by_name["validation"] = validation_rows(rows_by_name, start_utc)
    for output_name, rows in rows_by_name.items():
        write_csv(OUTPUTS[output_name], rows)
    write_doc(rows_by_name)
    failed_rows = [row for row in rows_by_name["validation"] if not row["passed"]]
    if failed_rows:
        raise SystemExit(f"3442 validation failed: {failed_rows}")
    print(f"wrote {DOC}")
    print(f"wrote {len(OUTPUTS)} csv outputs")


if __name__ == "__main__":
    main()
