from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
MICROSCOPE_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1860"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1860-Y5-R2FR-Gamma-Khat-q-loc-action-existence-bridge-to-local-EH-fixed-point.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1860_SOURCE_REGISTER.csv",
    "qloc_zero_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1860_QLOC_ZERO_ROUTE_AUDIT.csv",
    "activation_contract": RESIDUALS / "P8_Y5_PARENT_QLOC_1860_ACTIVATION_CONTRACT.csv",
    "eh_bridge": RESIDUALS / "P8_Y5_PARENT_QLOC_1860_LOCAL_EH_BRIDGE_IMPACT.csv",
    "residual_retention": RESIDUALS / "P8_Y5_PARENT_QLOC_1860_EPSILON_GK_QLOC_RETENTION.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1860_CLAIM_GATE.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1860_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1860_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1860_VALIDATION.csv",
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def source_path(relative_path: str) -> str:
    return rel(ROOT / relative_path)


def ensure_dirs() -> None:
    for path in [RESIDUALS, MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
        path.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def boolish(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def build_rows_map() -> dict[str, list[dict[str, Any]]]:
    source_rows = [
        {
            "source_id": "SRC1860_0_1859_handoff",
            "source_path": source_path("1859-Y5-R2FR-motion-load-phase-volume-parent-origin-no-GR-import-derivation.md"),
            "needle": "NEXT1859_0_primary",
            "role": "handoff into Gamma/Khat/q_loc extra-sector silence bridge",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1860_1_1010_theorem",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_R10_1010_THEOREM_ATTEMPT.csv"),
            "needle": "GKT1010_6_verdict",
            "role": "original action/Helmholtz/Euler/double-zero q_loc theorem attempt",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1860_2_1280_q_loc",
            "source_path": source_path("1280-Y5-R10-RAB-Gamma-Khat-qloc-action-existence-or-extra-residual-bound.md"),
            "needle": "QLOC_ZERO_NOT_DERIVED",
            "role": "RAB Gamma/Khat/q_loc action-existence checkpoint",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1860_3_1619_normal_form",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1619_POSITIVE_AUXILIARY_NORMAL_FORM.csv"),
            "needle": "NF1619_6_verdict",
            "role": "positive auxiliary/response-doublet formal mechanism",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1860_4_1664_source_formula",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1664_GAMMA_KHAT_SOURCE_FORMULA_AUDIT.csv"),
            "needle": "SFA1664_5_verdict",
            "role": "live Gamma/Khat source-formula obstruction",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1860_5_1664_routes",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1664_RESCUE_ROUTE_MATRIX.csv"),
            "needle": "RRM1664_2_positive_response_doublet",
            "role": "best rescue route if Z maps to actual vertical generator",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1860_6_1665_parent_signature",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1665_PARENT_SIGNATURE_CLAUSE_AUDIT.csv"),
            "needle": "PSC1665_7_residual_vector_lock",
            "role": "parent signature and physical residual lock requirements",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1860_7_1665_z_route",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1665_Z_ROUTE_SIGNATURE_AUDIT.csv"),
            "needle": "ZRA1665_7_physical_residual_lock",
            "role": "Z-route formal/live distinction",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1860_8_1791_activation",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1791_ACTIVATION_AUDIT.csv"),
            "needle": "ACT1791_7_verdict",
            "role": "response-displacement activation clauses",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1860_9_1791_profile",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1791_QLOC_CR2_PROFILE_PACK.csv"),
            "needle": "QCP1791_7_acceptance",
            "role": "q_loc/c_R2 profile pack rejection criteria",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1860_10_A511",
            "source_path": source_path("source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv"),
            "needle": "A511_3_extra_field_silence",
            "role": "local EH fixed-point action block impacted by q_loc",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1860_11_1834_no_hypermomentum",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1834_NO_HYPERMOMENTUM_THEOREM_ATTEMPT.csv"),
            "needle": "NHM1834_6_verdict",
            "role": "matter/source connection-current obstruction",
            "status": "FOUND",
            "valid_for_claim": False,
        },
    ]

    qloc_zero_rows = [
        {
            "audit_id": "QZA1860_0_identity",
            "claim_piece": "q_loc definition",
            "required_statement": "q_loc^nu = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})",
            "current_evidence": "1010/1280/1791 agree on the definition",
            "status": "DEFINITION_RECORDED",
            "effect": "defines the local force/source residual to be zeroed or bounded",
            "valid_for_claim": False,
        },
        {
            "audit_id": "QZA1860_1_action_existence",
            "claim_piece": "S_GK exists",
            "required_statement": "Gamma_eff is a source-signed scalar density/function of parent fields with units, derivative order and boundary terms",
            "current_evidence": "SFA1664_0 fails; ACT1791_0 open; 1010 candidate contract only",
            "status": "NOT_LIVE_PARENT_SIGNED",
            "effect": "q_loc cannot be a Ward/Euler residual of a real sector yet",
            "valid_for_claim": False,
        },
        {
            "audit_id": "QZA1860_2_metric_response",
            "claim_piece": "K_hat equals metric response",
            "required_statement": "K_hat^{mu nu} = 2/sqrt(-g) delta(sqrt(-g) Gamma_eff)/delta g_{mu nu} with derivative/boundary terms included",
            "current_evidence": "MRM1280_1 and SFA1664_1 fail current symbol match; ACT1791_3 open",
            "status": "FAIL_CURRENT_SYMBOL_MATCH",
            "effect": "Gamma_eff and K_hat remain independent knobs rather than a single variational stress",
            "valid_for_claim": False,
        },
        {
            "audit_id": "QZA1860_3_Helmholtz",
            "claim_piece": "variational integrability",
            "required_statement": "second variations of the proposed stress are symmetric up to boundary/gauge terms",
            "current_evidence": "HOB1664_5 says Helmholtz cannot run on absent live inputs; NF1619 closes only inside constructed normal form",
            "status": "FORMAL_ONLY_NOT_LIVE",
            "effect": "normal-form action is coherent, but current MTS Gamma/Khat is not promoted",
            "valid_for_claim": False,
        },
        {
            "audit_id": "QZA1860_4_Euler_double_zero",
            "claim_piece": "Euler closure and F1/double-zero",
            "required_statement": "E_A=0, local fixed point, Gamma0 subtraction, T_GK(Phi0)=0, partial_A T_GK(Phi0)=0",
            "current_evidence": "NF1619_4 proves formal double-zero; GKA1280_4 and ACT1791_1/2 keep live component/source activation open",
            "status": "FORMAL_DOUBLE_ZERO_NOT_ACTIVATED",
            "effect": "F1=0 is not yet a physical q_loc/local-vacuum theorem",
            "valid_for_claim": False,
        },
        {
            "audit_id": "QZA1860_5_source_boundary",
            "claim_piece": "source-current and boundary silence",
            "required_statement": "J_Z=0, B_Z=0, no source-normalization/species/readout linear coupling, and local boundary/projector no-flux",
            "current_evidence": "GAP1619_2/4, PSC1665_5/6, ACT1791_2/5 and NHM1834_6 remain unsigned",
            "status": "COUPLING_LOCK_OPEN",
            "effect": "bulk formal zero can leak into matter/source/readout/local tests",
            "valid_for_claim": False,
        },
        {
            "audit_id": "QZA1860_6_physical_lock",
            "claim_piece": "Z/phi controls the actual local residual vector",
            "required_statement": "Z or phi maps onto q_loc/PPN/source-normalization/clock/orbital residuals with full-rank observable lock",
            "current_evidence": "ZRA1665_7 and ACT1791_1 keep component lock unproved; QCP1791 profile pack is rejected",
            "status": "PHYSICAL_LOCK_NOT_DERIVED",
            "effect": "formal Z might be a shadow variable rather than the dangerous physical residual",
            "valid_for_claim": False,
        },
        {
            "audit_id": "QZA1860_7_verdict",
            "claim_piece": "q_loc parent-zero on local branch",
            "required_statement": "QZA1860_1 through QZA1860_6 close in one parent branch",
            "current_evidence": "multiple action, metric, coupling, boundary and component-lock clauses remain unsigned",
            "status": "QLOC_ZERO_NOT_DERIVED_CURRENT_CORPUS",
            "effect": "retain epsilon_GK_q_loc and keep local EH/GR inheritance blocked",
            "valid_for_claim": False,
        },
    ]

    activation_rows = [
        {
            "clause_id": "ACTC1860_0_formal_mechanism",
            "activation_clause": "positive auxiliary / response doublet normal form",
            "what_is_available": "explicit formal action, metric response by definition, Helmholtz readiness, Ward profile and double-zero inside the constructed class",
            "what_is_missing": "not parent-signed as actual MTS variables",
            "current_status": "PASS_FORMAL_ONLY",
            "blocks_claim": False,
            "valid_for_claim": False,
        },
        {
            "clause_id": "ACTC1860_1_parent_variable_map",
            "activation_clause": "actual MTS residuals map to Z^A or phi route",
            "what_is_available": "formal Z/phi rescue candidates",
            "what_is_missing": "Phi_parent chart, q(Phi), Dq[Z/phi], Omega/DCdagger/field action",
            "current_status": "MISSING_PARENT_SIGNATURE",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
        {
            "clause_id": "ACTC1860_2_live_GammaKhat",
            "activation_clause": "Gamma_eff and K_hat are one live variational pair",
            "what_is_available": "candidate scalar-density route and trace-free improvement algebra",
            "what_is_missing": "source-signed Gamma_eff formula and tensor equality K_hat=K_metric[Gamma_eff]",
            "current_status": "LIVE_ADOPTION_NOT_CLOSED",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
        {
            "clause_id": "ACTC1860_3_coupling_evenness",
            "activation_clause": "matter/source/readout/boundary functionals are even or quotient-descended in Z",
            "what_is_available": "chain-rule theorem and no-hypermomentum route as conditional contracts",
            "what_is_missing": "matter functor, source-current zero, no species weights, projective/connection descent",
            "current_status": "COUPLING_LOCK_OPEN",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
        {
            "clause_id": "ACTC1860_4_projector_boundary",
            "activation_clause": "P_loc owner and boundary no-flux before readout",
            "what_is_available": "P_loc and boundary terms are named",
            "what_is_missing": "parent projector, derivative silence, boundary class, linked-sphere/source-worldtube flux proof",
            "current_status": "BOUNDARY_PROJECTOR_OPEN",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
        {
            "clause_id": "ACTC1860_5_observable_lock",
            "activation_clause": "q_loc/DeltaGamma/PPN/source-normalization components have common units and projection maps",
            "what_is_available": "1834-1836 component/projection skeletons",
            "what_is_missing": "numeric/source-backed component values, common units and WEP/clock/lightcone/PPN projection operators",
            "current_status": "OBSERVABLE_LOCK_OPEN",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
        {
            "clause_id": "ACTC1860_6_verdict",
            "activation_clause": "formal mechanism activates as physical q_loc zero",
            "what_is_available": "mathematical normal-form route",
            "what_is_missing": "all live adoption/coupling/projector/observable clauses together",
            "current_status": "NOT_ACTIVATED",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
    ]

    eh_rows = [
        {
            "bridge_id": "EHB1860_0_A511_3",
            "dependency": "A511_3_extra_field_silence",
            "current_status": "BLOCKED_BY_EPSILON_GK_QLOC",
            "effect_on_local_EH": "EH fixed-point inheritance cannot be claimed while q_loc is a retained extra-sector force residual",
            "needed_to_unblock": "q_loc parent-zero theorem or source-backed epsilon_GK_q_loc bound below arena thresholds",
            "valid_for_claim": False,
        },
        {
            "bridge_id": "EHB1860_1_A511_6",
            "dependency": "A511_6_metric_readout",
            "current_status": "READOUT_LOCK_NOT_CLOSED",
            "effect_on_local_EH": "even if bulk q_loc were small, readout/projection leakage can re-enter Newton/PPN/clock channels",
            "needed_to_unblock": "P_loc/readout derivative silence and observable projection maps",
            "valid_for_claim": False,
        },
        {
            "bridge_id": "EHB1860_2_Euler_difference",
            "dependency": "1859 parent E_time-E_radial route",
            "current_status": "HELD_UNTIL_EXTRA_SILENCE",
            "effect_on_local_EH": "parent Euler/source-map derivation of C_R=0 cannot promote while q_loc contaminates the source side",
            "needed_to_unblock": "close q_loc or carry it explicitly into S_R[source,residual,boundary]",
            "valid_for_claim": False,
        },
        {
            "bridge_id": "EHB1860_3_verdict",
            "dependency": "local EH / GR inheritance",
            "current_status": "NOT_REOPENED",
            "effect_on_local_EH": "formal q_loc mechanism is useful but not enough to derive GR/Newton",
            "needed_to_unblock": "A511_0..6 parent-signed with q_loc and DeltaGamma components theorem-zero or source-bounded",
            "valid_for_claim": False,
        },
    ]

    residual_rows = [
        {
            "residual_id": "RET1860_0_epsilon_GK_q_loc",
            "residual_symbol": "epsilon_GK_q_loc",
            "definition": "norm of P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu}) after local projection, source-current and boundary terms",
            "current_status": "RETAIN_NONCLAIM",
            "missing_inputs": "Gamma_eff density; K_hat operator; P_loc owner; source vector J_Z/B_Z; boundary no-flux; units; arena maps",
            "maps_to_tests": "local_GR;PPN;clock;orbital;WEP;R10/source-normalization",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "RET1860_1_DeltaGamma_overlap",
            "residual_symbol": "DeltaGamma_source_connection",
            "definition": "connection/hypermomentum source-current leakage overlapping q_loc and readout residuals",
            "current_status": "RETAIN_NONCLAIM",
            "missing_inputs": "matter functor, connection descent, spin/projective silence, common units, projection matrices",
            "maps_to_tests": "WEP;clock;lightcone;PPN_gamma;local_GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "RET1860_2_profile_pack",
            "residual_symbol": "q_loc/c_R2 profile pack",
            "definition": "fallback profile rows for q_loc theorem/profile slot, source vector, operator, c_R2 coefficient, R10/PPN/clock/orbital projections",
            "current_status": "REJECT_CURRENT_PROFILE_PACK",
            "missing_inputs": "source vector; operator inverse; coefficient normalization; arena projections; source paths",
            "maps_to_tests": "R10;PPN;clock;orbital",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gate_rows = [
        {
            "gate_id": "CG1860_0_formal_mechanism",
            "claim": "formal normal-form q_loc mechanism exists",
            "gate_pass": True,
            "reason": "1619 supplies a calculable action/metric-response/Helmholtz/double-zero shape inside the constructed class",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1860_1_live_action",
            "claim": "live MTS S_GK/Gamma_eff/K_hat action pair is parent-signed",
            "gate_pass": False,
            "reason": "Gamma_eff scalar density and K_hat metric-response equality remain unsigned/failed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1860_2_q_loc_zero",
            "claim": "q_loc is theorem-zero on local branch",
            "gate_pass": False,
            "reason": "action, metric response, source-current, boundary, projector and physical-lock clauses do not close together",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1860_3_A511_extra_silence",
            "claim": "A511_3 extra-sector silence is derived",
            "gate_pass": False,
            "reason": "epsilon_GK_q_loc and DeltaGamma/source-current residuals remain active",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1860_4_EH_inheritance",
            "claim": "local EH/GR/Newton inheritance reopens",
            "gate_pass": False,
            "reason": "q_loc zero/bound, coupling lock, readout lock and local source maps are not signed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC1860_0_formal_not_physical",
            "decision": "keep the response-doublet/positive-auxiliary normal form as the preferred mechanism shape",
            "because": "it genuinely supplies action, metric response and double-zero algebra in a calculable class",
            "next_action": "do not promote it until live MTS symbol, coupling and boundary activation clauses close",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1860_1_q_loc_status",
            "decision": "retain epsilon_GK_q_loc as an explicit residual",
            "because": "q_loc parent-zero is not derived and profile rows are not source-ready",
            "next_action": "carry epsilon_GK_q_loc into local EH/source-map and empirical fallback gates",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1860_2_next_route",
            "decision": "attack coupling lock next, with live Khat metric variation as a parallel route",
            "because": "source-functional evenness/J_Z/B_Z controls whether formal double-zero becomes physical; Khat matching controls variational ownership",
            "next_action": "derive exchange-even matter/source/boundary functionals or emit finite coefficient rows",
            "valid_for_claim": False,
        },
    ]

    next_rows = [
        {
            "next_id": "NEXT1860_0_primary",
            "target_file": "1861-Y5-R2FR-source-functional-evenness-JZ-BZ-coupling-lock-or-profile-acquisition.md",
            "target_script": "scripts/Y5_R2FR_source_functional_evenness_JZ_BZ_coupling_lock_or_profile_acquisition_1861.py",
            "task": "try to prove matter, source-normalization, species, readout and boundary functionals are exchange-even or quotient-descended in the local residual Z; if not, create strict nonclaim J_Z/B_Z/Y5/Y6 coefficient acquisition rows",
            "success_condition": "parent-signed no-linear-source theorem for the q_loc normal form, or source-backed finite coupling/profile rows with units and arena maps",
            "do_not": "do not claim F1=0 or q_loc=0 from the formal normal form alone",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "next_id": "NEXT1860_1_parallel",
            "target_file": "1861b-Y5-R2FR-live-Khat-metric-variation-comparison.md",
            "target_script": "scripts/Y5_R2FR_live_Khat_metric_variation_comparison_1861b.py",
            "task": "compute K_metric from any chosen Gamma_eff scalar density candidate and compare against live K_hat tensor components including boundary/improvement terms",
            "success_condition": "term-by-term metric-response match or explicit mismatch ledger",
            "do_not": "do not adopt K_hat as a stress tensor without a scalar density and Helmholtz/second-variation check",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    return {
        "source_register": source_rows,
        "qloc_zero_audit": qloc_zero_rows,
        "activation_contract": activation_rows,
        "eh_bridge": eh_rows,
        "residual_retention": residual_rows,
        "claim_gate": claim_gate_rows,
        "decision": decision_rows,
        "next_target": next_rows,
    }


def copy_outputs(include_validation: bool = False) -> None:
    keys = list(OUTPUTS)
    if not include_validation:
        keys = [key for key in keys if key != "validation"]
    for key in keys:
        src = OUTPUTS[key]
        if not src.exists():
            continue
        for dst_dir in [MICROSCOPE_RESIDUALS, QUARANTINE]:
            shutil.copy2(src, dst_dir / src.name)
        shutil.copy2(src, RAB_QUEUE / f"JR1860_{src.name}")


def check_sources(source_rows: list[dict[str, Any]]) -> tuple[bool, str]:
    missing: list[str] = []
    for row in source_rows:
        path = ROOT / str(row["source_path"])
        if not path.exists():
            missing.append(str(row["source_path"]))
    return not missing, "missing: " + "; ".join(missing) if missing else "all cited source paths exist"


def check_needles(source_rows: list[dict[str, Any]]) -> tuple[bool, str]:
    missing: list[str] = []
    for row in source_rows:
        path = ROOT / str(row["source_path"])
        needle = str(row["needle"])
        if path.exists() and needle not in path.read_text(encoding="utf-8", errors="ignore"):
            missing.append(f"{row['source_path']}::{needle}")
    return not missing, "missing: " + "; ".join(missing) if missing else "all cited source needles are present"


def check_csv_parse() -> tuple[bool, str]:
    malformed: list[str] = []
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        try:
            read_csv(path)
        except Exception as exc:  # pragma: no cover
            malformed.append(f"{path.name}: {exc}")
    return not malformed, "malformed: " + "; ".join(malformed) if malformed else "all generated 1860 CSVs parse"


def check_branch_copies() -> tuple[bool, str]:
    missing: list[str] = []
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        expected = [
            MICROSCOPE_RESIDUALS / path.name,
            QUARANTINE / path.name,
            RAB_QUEUE / f"JR1860_{path.name}",
        ]
        for item in expected:
            if not item.exists():
                missing.append(str(item))
    return not missing, "missing copies: " + "; ".join(missing) if missing else "branch/quarantine/queue copies exist"


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = []
    ok, detail = check_sources(rows_map["source_register"])
    checks.append(("VAL1860_0_sources_exist", ok, detail))
    ok, detail = check_needles(rows_map["source_register"])
    checks.append(("VAL1860_1_needles_present", ok, detail))
    checks.append(
        (
            "VAL1860_2_formal_mechanism_present",
            any(row["clause_id"] == "ACTC1860_0_formal_mechanism" and row["current_status"] == "PASS_FORMAL_ONLY" for row in rows_map["activation_contract"]),
            "formal q_loc normal-form mechanism is recorded",
        )
    )
    checks.append(
        (
            "VAL1860_3_q_loc_zero_blocked",
            any(row["audit_id"] == "QZA1860_7_verdict" and row["status"] == "QLOC_ZERO_NOT_DERIVED_CURRENT_CORPUS" for row in rows_map["qloc_zero_audit"]),
            "q_loc parent-zero is not promoted",
        )
    )
    checks.append(
        (
            "VAL1860_4_coupling_lock_open",
            any(row["clause_id"] == "ACTC1860_3_coupling_evenness" and row["current_status"] == "COUPLING_LOCK_OPEN" for row in rows_map["activation_contract"]),
            "source/boundary coupling lock remains open",
        )
    )
    checks.append(
        (
            "VAL1860_5_eh_bridge_blocked",
            any(row["bridge_id"] == "EHB1860_3_verdict" and row["current_status"] == "NOT_REOPENED" for row in rows_map["eh_bridge"]),
            "local EH inheritance remains blocked",
        )
    )
    checks.append(
        (
            "VAL1860_6_residual_retained",
            any(row["residual_id"] == "RET1860_0_epsilon_GK_q_loc" and row["current_status"] == "RETAIN_NONCLAIM" for row in rows_map["residual_retention"]),
            "epsilon_GK_q_loc retained as nonclaim residual",
        )
    )
    checks.append(
        (
            "VAL1860_7_claim_gates_safe",
            any(row["gate_id"] == "CG1860_0_formal_mechanism" and boolish(row["gate_pass"]) for row in rows_map["claim_gate"])
            and any(row["gate_id"] == "CG1860_4_EH_inheritance" and not boolish(row["gate_pass"]) for row in rows_map["claim_gate"])
            and all(not boolish(row["claim_allowed"]) for row in rows_map["claim_gate"]),
            "only formal mechanism gate passes; q_loc/local-GR claims remain blocked",
        )
    )
    checks.append(
        (
            "VAL1860_8_next_target_selected",
            any(row["next_id"] == "NEXT1860_0_primary" for row in rows_map["next_target"]),
            "1861 coupling-lock target selected",
        )
    )
    checks.append(
        (
            "VAL1860_9_no_claim_flags",
            all(not boolish(row.get("valid_for_claim", False)) for rows in rows_map.values() for row in rows),
            "no valid_for_claim flags are true",
        )
    )
    ok, detail = check_csv_parse()
    checks.append(("VAL1860_10_csv_parse", ok, detail))
    ok, detail = check_branch_copies()
    checks.append(("VAL1860_11_branch_copies", ok, detail))
    pycache_path = ROOT / "scripts" / "__pycache__"
    checks.append(("VAL1860_12_pycache_absent", not pycache_path.exists(), "scripts __pycache__ absent"))
    formalization_outputs: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in [
            "*P8_Y5*1860*",
            "*1860-Y5-R2FR-Gamma-Khat-q-loc-action-existence-bridge-to-local-EH-fixed-point*",
            "*Y5_R2FR_Gamma_Khat_qloc_action_existence_bridge_to_local_EH_fixed_point_1860.py",
        ]:
            formalization_outputs.extend(FORMALIZATION.rglob(pattern))
    formalization_detail = (
        "found generated outputs: " + "; ".join(str(path) for path in formalization_outputs)
        if formalization_outputs
        else "no generated 1860 outputs found under formalization-workbench"
    )
    checks.append(("VAL1860_13_formalization_untouched", not formalization_outputs, formalization_detail))
    overall = all(result for _, result, _ in checks)
    validation_rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    validation_rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1860_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1860 Gamma/Khat/q_loc action-existence bridge to local EH fixed point",
        }
    )
    return validation_rows


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    lines = [header, sep]
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    return "\n".join(
        [
            "# 1860: Gamma/Khat/q_loc Action-Existence Bridge To Local EH Fixed Point",
            "",
            "**Current verdict:** the formal q_loc zero mechanism exists, but current MTS has not activated it as a physical local-GR theorem. The response-doublet/positive-auxiliary normal form gives a real action/metric-response/Helmholtz/double-zero shape inside a constructed class. The live branch still fails the parent-signature, Gamma/Khat metric-response, source-current, boundary/projector, and observable-lock gates. Therefore `epsilon_GK_q_loc` remains an explicit nonclaim residual and local EH/GR/Newton inheritance is not reopened.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_path", "needle", "role", "status", "valid_for_claim"]),
            "",
            "## q_loc Zero Route Audit",
            markdown_table(rows_map["qloc_zero_audit"], ["audit_id", "claim_piece", "required_statement", "current_evidence", "status", "effect", "valid_for_claim"]),
            "",
            "## Activation Contract",
            markdown_table(rows_map["activation_contract"], ["clause_id", "activation_clause", "what_is_available", "what_is_missing", "current_status", "blocks_claim", "valid_for_claim"]),
            "",
            "## Local EH Bridge Impact",
            markdown_table(rows_map["eh_bridge"], ["bridge_id", "dependency", "current_status", "effect_on_local_EH", "needed_to_unblock", "valid_for_claim"]),
            "",
            "## Residual Retention",
            markdown_table(rows_map["residual_retention"], ["residual_id", "residual_symbol", "definition", "current_status", "missing_inputs", "maps_to_tests", "valid_for_claim", "claim_allowed"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "",
            "## Decisions",
            markdown_table(rows_map["decision"], ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This narrows the real fight. We are not missing a poetic statement that motion balances time and space; we are missing a coupling lock. The formal double-zero can become physical only if matter/source/readout/boundary functionals are even or quotient-descended in the local residual, and if live `K_hat` is the metric response of a parent-owned `Gamma_eff`. Until then, `q_loc` is a retained residual, not a plateau axiom.",
            "",
        ]
    )


def main() -> None:
    ensure_dirs()
    rows_map = build_rows_map()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs(include_validation=False)
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    copy_outputs(include_validation=True)
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1860 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
