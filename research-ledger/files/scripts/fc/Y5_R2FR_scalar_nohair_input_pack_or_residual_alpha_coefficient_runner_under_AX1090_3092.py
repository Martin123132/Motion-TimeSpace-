from __future__ import annotations

import csv
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3092"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "3092-Y5-R2FR-scalar-nohair-input-pack-or-residual-alpha-coefficient-runner-under-AX1090.md"

SOURCES: dict[str, dict[str, Any]] = {
    "SRC3092_00_3091_doc": {
        "path": ROOT / "3091-Y5-R2FR-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice-under-AX1090.md",
        "needles": ["scalar no-hair/source-coefficient branch", "q/v_X/action"],
        "role": "3091 demotes the quotient route and selects scalar no-hair/source coefficients.",
    },
    "SRC3092_01_3091_next": {
        "path": RESIDUALS / "P8_Y5_R2FR_3091_NEXT_TARGET.csv",
        "needles": ["NEXT3091_0_3092", "int_A(Z_X|grad X|^2+M_X^2X^2)"],
        "role": "3091 handoff names this exact 3092 target and its working identity.",
    },
    "SRC3092_02_3091_scalar_pack": {
        "path": RESIDUALS / "P8_Y5_R2FR_3091_SCALAR_SOURCE_INPUT_PACK.csv",
        "needles": ["SNH3091_0_Z_X", "MISSING_PARENT_INPUT"],
        "role": "3091 lists the scalar/source inputs still missing in the active AX1090 branch.",
    },
    "SRC3092_03_1846_precedent": {
        "path": ROOT / "1846-Y5-R2FR-scalar-nohair-input-pack-or-residual-alpha-coefficient-runner.md",
        "needles": ["Scalar no-hair cannot be claimed", "Residual alpha runner is staged"],
        "role": "1846 precedent: same logic for parent q_loc branch, with claim refusal.",
    },
    "SRC3092_04_1024_precedent": {
        "path": ROOT / "1024-Y5-R10-scalar-nohair-input-pack-or-residual-alpha-coefficient-runner.md",
        "needles": ["scalar no-hair route is executable as a conditional energy identity", "residual alpha runner is staged and refuses all claims"],
        "role": "1024 precedent: original R10 scalar no-hair / alpha refusal checkpoint.",
    },
    "SRC3092_05_1042_identity": {
        "path": RESIDUALS / "P8_Y5_R10_1042_POSITIVE_X_NOHAIR_IDENTITY.csv",
        "needles": ["NH1042_5_verdict", "four owner premises"],
        "role": "1042 records the exact conditional positive-X no-hair identity.",
    },
    "SRC3092_06_1092_audit": {
        "path": RESIDUALS / "P8_Y5_R10_1092_SCALAR_NOHAIR_ROUTE_AUDIT.csv",
        "needles": ["SNH1092_4_verdict", "NOHAIR_ROUTE_UNSIGNED"],
        "role": "1092 sharpens no-hair into owner/sign/source/boundary gates.",
    },
    "SRC3092_07_1093_owner": {
        "path": RESIDUALS / "P8_Y5_R10_1093_PARENT_SCALAR_OWNER_ATTEMPT.csv",
        "needles": ["OWN1093_4_verdict", "PARENT_OWNER_NOT_DERIVED"],
        "role": "1093 shows the dangerous scalar owner is still not derived.",
    },
    "SRC3092_08_1093_operator": {
        "path": RESIDUALS / "P8_Y5_R10_1093_POSITIVE_OPERATOR_INPUT_PACK.csv",
        "needles": ["OP1093_4_verdict", "OPERATOR_PACK_UNSIGNED"],
        "role": "1093 shows the positive operator pack remains unsigned.",
    },
    "SRC3092_09_1093_silence": {
        "path": RESIDUALS / "P8_Y5_R10_1093_SOURCE_SILENCE_AUDIT.csv",
        "needles": ["JX1093_4_verdict", "SOURCE_SILENCE_NOT_DERIVED"],
        "role": "1093 shows source-free no-hair premises remain unsigned.",
    },
    "SRC3092_10_1093_doc": {
        "path": ROOT / "1093-Y5-R10-scalar-nohair-input-owner-or-balpha-tau-projection-source.md",
        "needles": ["THM1093_2_zero_result", "EXACT_CONDITIONAL_THEOREM"],
        "role": "1093 doc records the zero result as exact conditional math, not an active MTS claim.",
    },
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3092_SOURCE_REGISTER.csv",
    "scalar_inputs": RESIDUALS / "P8_Y5_R2FR_3092_SCALAR_INPUT_ASSESSMENT.csv",
    "nohair_contract": RESIDUALS / "P8_Y5_R2FR_3092_POSITIVE_NOHAIR_CONTRACT.csv",
    "parent_owner": RESIDUALS / "P8_Y5_R2FR_3092_PARENT_SCALAR_OWNER_AUDIT.csv",
    "operator_pack": RESIDUALS / "P8_Y5_R2FR_3092_POSITIVE_OPERATOR_INPUT_PACK.csv",
    "source_silence": RESIDUALS / "P8_Y5_R2FR_3092_SOURCE_SILENCE_AUDIT.csv",
    "alpha_rows": RESIDUALS / "P8_Y5_R2FR_3092_ALPHA_COEFFICIENT_ROWS.csv",
    "alpha_refusal": RESIDUALS / "P8_Y5_R2FR_3092_ALPHA_RUNNER_REFUSAL.csv",
    "branch_verdicts": RESIDUALS / "P8_Y5_R2FR_3092_BRANCH_VERDICTS.csv",
    "claim_gate": RESIDUALS / "P8_Y5_R2FR_3092_CLAIM_GATE.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3092_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3092_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3092_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3092_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "scalar_inputs_copy": LOCAL_BOUNDS / "scalar_input_assessment_3092_NONCLAIM.csv",
    "alpha_rows_copy": LOCAL_BOUNDS / "alpha_coefficient_rows_3092_NONCLAIM.csv",
    "alpha_refusal_copy": LOCAL_BOUNDS / "alpha_runner_refusal_3092_NONCLAIM.csv",
    "branch_verdicts_copy": LOCAL_BOUNDS / "branch_verdicts_3092_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3092_parent_Xhat_Hessian_or_alpha_source_NEXT_NONCLAIM.csv",
}


def meta() -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "timestamp_utc": RUN_UTC,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def remove_pycache() -> None:
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def file_hash(path: Path) -> str:
    if not path.exists():
        return "MISSING"
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_ok(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        with path.open("r", newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def source_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_ok(path) if path.suffix.lower() == ".csv" else True


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "passed"}


def with_meta(output_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    base = meta()
    return [{**base, **row} for row in output_rows]


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in output_rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in output_rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def source_rows() -> list[dict[str, Any]]:
    output_rows = []
    for source_id, source in SOURCES.items():
        path = Path(source["path"])
        text = read_text(path)
        missing = [needle for needle in source["needles"] if needle not in text]
        output_rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "parse_ok": source_parse_ok(path),
                "sha256": file_hash(path),
                "needles_present": not missing,
                "missing_needles": ";".join(missing),
                "role": source["role"],
            }
        )
    return with_meta(output_rows)


def scalar_input_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "input_id": "SIA3092_0_operator_domain",
                "quantity": "O_X self-adjoint positive operator",
                "required_condition": "O_X=-nabla_i(Z_X nabla^i)+M_X^2 on compact source-free exterior with owned local domain",
                "current_evidence": "1042 gives the identity; 1093 says parent L_X/domain is still missing",
                "current_status": "TEMPLATE_ONLY",
                "missing_for_claim": "parent operator, field units, self-adjoint domain and boundary class",
                "if_missing": "energy identity remains theorem contract only",
            },
            {
                "input_id": "SIA3092_1_parent_owner",
                "quantity": "same Xhat owns visible coefficients and no-hair equation",
                "required_condition": "one parent-normalized Xhat controls dangerous coupling and obeys L_X Xhat=J_X",
                "current_evidence": "1093 owner audit reaches PARENT_OWNER_NOT_DERIVED; 3091 quotient certificate also failed",
                "current_status": "PARENT_OWNER_NOT_DERIVED",
                "missing_for_claim": "identify Xhat as action-owned parent field rather than closure coordinate",
                "if_missing": "no scalar no-hair/local-GR claim",
            },
            {
                "input_id": "SIA3092_2_Z_X",
                "quantity": "Z_X>0",
                "required_condition": "second variation fixes positive kinetic residue with normalization and units",
                "current_evidence": "operator pack has formula language but no AX1090 parent-signed Hessian",
                "current_status": "MISSING_PARENT_INPUT",
                "missing_for_claim": "parent Hessian, sign convention, field normalization and units",
                "if_missing": "ghost/anti-elliptic/indefinite residual branch remains open",
            },
            {
                "input_id": "SIA3092_3_M_X2_lambda",
                "quantity": "M_X^2>0 and lambda_X",
                "required_condition": "mass gap is positive and lambda_X=sqrt(Z_X/M_X^2) has length units",
                "current_evidence": "mass gap and range remain formula-only across 1024/1093/3091",
                "current_status": "MISSING_PARENT_INPUT",
                "missing_for_claim": "parent Hessian curvature, zero-mode handling and range units",
                "if_missing": "long-range/tachyonic/zero-mode branch remains possible",
            },
            {
                "input_id": "SIA3092_4_J_X_zero",
                "quantity": "J_X=0",
                "required_condition": "ordinary matter plus visible/source/readout terms are X-blind channel-by-channel",
                "current_evidence": "source silence audit keeps ordinary matter, alpha, WEP, R10 and readout channels live",
                "current_status": "MISSING_SOURCE_ZERO_PROOF",
                "missing_for_claim": "matter quotient/no-marker theorem or explicit source-current bounds",
                "if_missing": "finite residual must be scored",
            },
            {
                "input_id": "SIA3092_5_boundary_flux_zero",
                "quantity": "boundary_flux_X=0",
                "required_condition": "boundary flux is zero/proper/exact or source-backed bounded",
                "current_evidence": "edge/projector terms remain unsigned after quotient-route demotion",
                "current_status": "MISSING_BOUNDARY_LOCK",
                "missing_for_claim": "boundary class, no-hair/projector silence or flux bound",
                "if_missing": "boundary residual must be retained",
            },
            {
                "input_id": "SIA3092_6_energy_identity",
                "quantity": "positive energy identity",
                "required_condition": "int_A(Z_X|grad X|^2+M_X^2X^2+positive_mix)=int_A XJ_X+Phi_boundary",
                "current_evidence": "1042/1093 derive exact conditional math",
                "current_status": "CONDITIONAL_MATH_VALID",
                "missing_for_claim": "SIA3092_0 through SIA3092_5 together",
                "if_missing": "do not convert identity into MTS theorem-zero",
            },
            {
                "input_id": "SIA3092_7_verdict",
                "quantity": "scalar no-hair theorem",
                "required_condition": "all scalar input rows parent-signed or source-bounded with zero RHS",
                "current_evidence": "the theorem contract is exact, but physical owner/sign/source/boundary premises remain unsigned",
                "current_status": "FAIL_CURRENT_CLAIM",
                "missing_for_claim": "operator, parent owner, Z_X, M_X^2, J_X=0, boundary_flux_X=0 and no-zero-mode gate",
                "if_missing": "stage parent-Hessian/range or residual alpha source row next",
            },
        ]
    )


def nohair_contract_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "theorem_id": "NHC3092_0_operator_setup",
                "step": "retained scalar mode equation",
                "mathematical_statement": "Let Xhat be the parent-owned retained local mode on compact exterior A with L_X Xhat=J_X.",
                "status": "CONDITIONAL_CONTRACT",
                "consequence": "only applies if Xhat is the same parent field that controls visible coefficients",
                "math_valid": True,
            },
            {
                "theorem_id": "NHC3092_1_energy_identity",
                "step": "multiply by Xhat and integrate",
                "mathematical_statement": "int_A[Z_X^{mu nu} nabla_mu Xhat nabla_nu Xhat+M_X^2 Xhat^2+positive_mix] = int_A Xhat J_X + Phi_boundary",
                "status": "EXACT_CONDITIONAL_IDENTITY",
                "consequence": "replaces plateau axiom with explicit sign/source/boundary premises",
                "math_valid": True,
            },
            {
                "theorem_id": "NHC3092_2_zero_result",
                "step": "set RHS to zero with positive gap/no zero mode",
                "mathematical_statement": "Z_X>=Z_min>0, M_X^2>=m_min^2>0, J_X=0, Phi_boundary=0 and no zero mode imply Xhat=0 on A.",
                "status": "EXACT_CONDITIONAL_THEOREM",
                "consequence": "would silence the scalar local branch and reopen the local-GR route if parent-signed",
                "math_valid": True,
            },
            {
                "theorem_id": "NHC3092_3_failure_branch",
                "step": "any premise fails",
                "mathematical_statement": "alpha_X(lambda_X)=K_X Qbar_XH qbar_XT plus edge and FB5540 absolute no-cancellation guard",
                "status": "FINITE_RESIDUAL_BRANCH",
                "consequence": "local tests score residuals instead of accepting a closure",
                "math_valid": True,
            },
            {
                "theorem_id": "NHC3092_4_verdict",
                "step": "MTS no-hair status under AX1090",
                "mathematical_statement": "positive no-hair theorem is derived as mathematics but not activated for MTS",
                "status": "CONDITIONAL_THEOREM_NOT_MTS_CLAIM",
                "consequence": "must derive parent owner/operator/source/boundary clauses first",
                "math_valid": True,
            },
        ]
    )


def parent_owner_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "owner_id": "OWN3092_0_target",
                "candidate_owner": "parent scalar Xhat/I controlling visible coefficients",
                "needed_identity": "d ln(c_visible)=b_X dXhat and the same Xhat enters L_X Xhat=J_X",
                "current_status": "TARGET_SHARP",
                "why_not_closed": "not yet identified as a parent field rather than a closure coordinate",
                "if_closed": "clock, WEP, R10/R11 and local-GR residuals can share one normalization",
            },
            {
                "owner_id": "OWN3092_1_chiX",
                "candidate_owner": "chi_X finite alpha-pressure coordinate",
                "needed_identity": "chi_X is a parent-owned local field with units and action normalization",
                "current_status": "CLOSURE_COORDINATE_ONLY",
                "why_not_closed": "visible coefficient response is defined but not tied to parent state variation",
                "if_closed": "could feed no-hair operator and alpha/WEP projection",
            },
            {
                "owner_id": "OWN3092_2_vertical_norm",
                "candidate_owner": "parent vertical norm or quotient-fixed scalar",
                "needed_identity": "visible scalar pressure equals a vertical-norm response or quotient-fixed observable",
                "current_status": "NOT_DERIVED",
                "why_not_closed": "3091 q/v_X/action/matter/boundary/degree certificate failed as one package",
                "if_closed": "could reopen quotient no-pole route rather than scalar no-hair",
            },
            {
                "owner_id": "OWN3092_3_clock_coframe",
                "candidate_owner": "clock/coframe scalar",
                "needed_identity": "same signed scalar controls observed clock/redshift maps and local source equation",
                "current_status": "THEOREM_TARGET_NOT_DERIVED",
                "why_not_closed": "clock scalar is not parent-derived and may be gauge/closure if not action-owned",
                "if_closed": "could connect clock and local no-hair routes",
            },
            {
                "owner_id": "OWN3092_4_verdict",
                "candidate_owner": "unique parent owner for dangerous scalar coefficient",
                "needed_identity": "one parent-normalized Xhat controls visible coefficients and obeys the no-hair operator",
                "current_status": "PARENT_OWNER_NOT_DERIVED",
                "why_not_closed": "all candidates are closure coordinates, conditional quotient targets, or unsigned theorem targets",
                "if_closed": "would unlock the positive no-hair identity as a local-GR route",
            },
        ]
    )


def operator_pack_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "input_id": "OP3092_0_LX_owner",
                "required_input": "parent L_X selected from second variation",
                "mathematical_role": "defines the self-adjoint operator acting on the same Xhat that controls visible coefficients",
                "current_status": "MISSING_PARENT_LX",
                "source_basis": "NHC3092_0_operator_setup;SIA3092_0_operator_domain",
                "blocks_claim": True,
            },
            {
                "input_id": "OP3092_1_Z_positive",
                "required_input": "Z_X positive kinetic matrix",
                "mathematical_role": "makes int Z_X |grad X|^2 nonnegative",
                "current_status": "FORMULA_ONLY_NOT_PARENT_SIGNED",
                "source_basis": "SIA3092_2_Z_X",
                "blocks_claim": True,
            },
            {
                "input_id": "OP3092_2_mass_gap",
                "required_input": "M_X^2 positive gap or justified zero-mode handling",
                "mathematical_role": "removes long-range scalar zero mode from local exterior",
                "current_status": "FORMULA_ONLY_NOT_PARENT_SIGNED",
                "source_basis": "SIA3092_3_M_X2_lambda",
                "blocks_claim": True,
            },
            {
                "input_id": "OP3092_3_self_adjoint_domain",
                "required_input": "self-adjoint local domain and boundary class",
                "mathematical_role": "permits integration by parts without hidden leakage",
                "current_status": "MISSING_DOMAIN_SIGNATURE",
                "source_basis": "SIA3092_0_operator_domain;SIA3092_5_boundary_flux_zero",
                "blocks_claim": True,
            },
            {
                "input_id": "OP3092_4_verdict",
                "required_input": "claim-grade positive operator pack",
                "mathematical_role": "supports positive no-hair identity for MTS rather than generic math",
                "current_status": "OPERATOR_PACK_UNSIGNED",
                "source_basis": "NHC3092_4_verdict",
                "blocks_claim": True,
            },
        ]
    )


def source_silence_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "silence_id": "JX3092_0_matter",
                "channel": "ordinary matter/source current",
                "needed_zero": "J_X^matter=0",
                "current_status": "CONDITIONAL_ON_PARENT_MATTER_SIGNATURE",
                "obstruction": "ordinary matter signature/descent is not parent-signed in active AX1090 branch",
                "finite_fallback": "J_X_bound source row",
            },
            {
                "silence_id": "JX3092_1_visible_coefficients",
                "channel": "alpha/EM/clock visible coefficient",
                "needed_zero": "partial_X ln(c_visible)=0 or parent-owned coefficient with no local source",
                "current_status": "NOT_DERIVED",
                "obstruction": "dangerous scalar owner and no-extra-coupling theorem remain unsigned",
                "finite_fallback": "b_visible or product source row",
            },
            {
                "silence_id": "JX3092_2_WEP_source",
                "channel": "WEP/source/test material projection",
                "needed_zero": "material response product is zero or bounded",
                "current_status": "PROJECTION_NOT_DERIVED",
                "obstruction": "source worldtube, material tensor and Xhat normalization are not jointly owned",
                "finite_fallback": "direct WEP product row",
            },
            {
                "silence_id": "JX3092_3_R10_source",
                "channel": "R10/Yukawa projection",
                "needed_zero": "beta_s beta_t K_X/Z_X tau_R10=0 or bounded alpha(lambda)",
                "current_status": "PROJECTION_NOT_DERIVED",
                "obstruction": "tau_R10, K_X/Z_X and lambda_X remain definition/template rows",
                "finite_fallback": "alpha_X(lambda) source row",
            },
            {
                "silence_id": "JX3092_4_clock_orbital_readout",
                "channel": "clock/orbital/PPN readout",
                "needed_zero": "readout projection of X is zero or source-bounded",
                "current_status": "PROJECTION_NOT_DERIVED",
                "obstruction": "local readout map and same-X normalization are missing",
                "finite_fallback": "arena-specific residual coefficient rows",
            },
            {
                "silence_id": "JX3092_5_verdict",
                "channel": "source-free no-hair premise",
                "needed_zero": "J_X=0 channelwise",
                "current_status": "SOURCE_SILENCE_NOT_DERIVED",
                "obstruction": "ordinary matter, visible coefficients, WEP, R10, boundary and readout channels are not all parent-silenced",
                "finite_fallback": "residual coefficient/product runner",
            },
        ]
    )


def alpha_coefficient_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "row_id": "ALPHA3092_0_bulk_operator",
                "quantity": "Z_X;M_X2;lambda_X",
                "formula": "lambda_X=sqrt(Z_X/M_X2)",
                "required_columns": "system_id;field_id;Z_X;M_X2;lambda_X;Z_units;M_units;lambda_units;source_path;valid_for_claim",
                "current_status": "MISSING_PARENT_INPUT",
            },
            {
                "row_id": "ALPHA3092_1_source_current",
                "quantity": "J_X or J_X_bound",
                "formula": "O_X X=J_X",
                "required_columns": "system_id;J_X;J_X_bound;source_channel;units;source_path;valid_for_claim",
                "current_status": "MISSING_SOURCE_ZERO_PROOF",
            },
            {
                "row_id": "ALPHA3092_2_boundary_flux",
                "quantity": "boundary_flux_X or boundary_flux_bound",
                "formula": "Phi_boundary=int_boundary X Z_X n.grad X plus edge/projector terms",
                "required_columns": "system_id;boundary_flux_X;boundary_flux_bound;boundary_rule;units;source_path;valid_for_claim",
                "current_status": "MISSING_BOUNDARY_LOCK",
            },
            {
                "row_id": "ALPHA3092_3_bulk_R10_projection",
                "quantity": "K_X;Qbar_XH;qbar_XT",
                "formula": "alpha_bulk(lambda_X)=K_X Qbar_XH qbar_XT",
                "required_columns": "system_id;lambda_X;K_X;Qbar_XH;qbar_XT;alpha_bulk;normalization;units;source_path;valid_for_claim",
                "current_status": "MISSING_ARENA_PROJECTION",
            },
            {
                "row_id": "ALPHA3092_4_edge_projection",
                "quantity": "lambda_edge;K_edge;Qbar_edge_XH;qbar_XT",
                "formula": "alpha_edge(lambda_edge)=K_edge Qbar_edge_XH qbar_XT",
                "required_columns": "system_id;lambda_edge;K_edge;Qbar_edge_XH;qbar_XT;alpha_edge;units;source_path;valid_for_claim",
                "current_status": "MISSING_EDGE_PROJECTION",
            },
            {
                "row_id": "ALPHA3092_5_no_cancellation_guard",
                "quantity": "alpha_total_guard",
                "formula": "abs_alpha_total=|alpha_bulk|+|alpha_edge|+|epsilon_FB5540|+|alpha_R11|",
                "required_columns": "system_id;lambda;abs_alpha_bulk;abs_alpha_edge;abs_FB5540;abs_alpha_R11;component_sum_abs;bound;source_path;valid_for_claim",
                "current_status": "NOT_COMPUTED_COMPONENTS_MISSING",
            },
        ]
    )


def alpha_refusal_rows() -> list[dict[str, Any]]:
    reasons = [
        ("RUN3092_0_bulk_operator", "ALPHA3092_0_bulk_operator", "blocked_missing_operator_inputs", "MISSING_PARENT_INPUT;VALID_FOR_CLAIM_FALSE"),
        ("RUN3092_1_source_current", "ALPHA3092_1_source_current", "blocked_missing_source_zero_or_bound", "MISSING_SOURCE_ZERO_PROOF;VALID_FOR_CLAIM_FALSE"),
        ("RUN3092_2_boundary_flux", "ALPHA3092_2_boundary_flux", "blocked_missing_boundary_flux_zero_or_bound", "MISSING_BOUNDARY_LOCK;VALID_FOR_CLAIM_FALSE"),
        ("RUN3092_3_bulk_R10_projection", "ALPHA3092_3_bulk_R10_projection", "blocked_missing_alpha_projection_inputs", "MISSING_ARENA_PROJECTION;VALID_FOR_CLAIM_FALSE"),
        ("RUN3092_4_edge_projection", "ALPHA3092_4_edge_projection", "blocked_missing_edge_projection_inputs", "MISSING_EDGE_PROJECTION;VALID_FOR_CLAIM_FALSE"),
        ("RUN3092_5_no_cancellation_guard", "ALPHA3092_5_no_cancellation_guard", "blocked_missing_no_cancellation_components", "NOT_COMPUTED_COMPONENTS_MISSING;VALID_FOR_CLAIM_FALSE"),
        ("RUN3092_6_verdict", "ALPHA3092_VERDICT", "REFUSED_NO_CLAIM", "SCALAR_NOHAIR_INPUTS_MISSING;ALPHA_COMPONENTS_MISSING;VALID_FOR_CLAIM_FALSE"),
    ]
    return with_meta(
        [
            {
                "runner_id": runner_id,
                "row_id": row_id,
                "computed_status": status,
                "claim_allowed": False,
                "failure_reasons": failure_reasons,
            }
            for runner_id, row_id, status, failure_reasons in reasons
        ]
    )


def branch_verdict_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "verdict_id": "BV3092_0_scalar_zero",
                "branch": "scalar no-hair theorem",
                "status": "FAIL_CURRENT_CLAIM",
                "because": "parent owner, Z_X, M_X2, J_X=0, boundary_flux_X=0, zero-mode and units are not parent-signed",
                "allowed_statement": "positive energy identity is an exact conditional theorem target only",
                "next_action": "try parent Xhat owner and Hessian/range extraction",
            },
            {
                "verdict_id": "BV3092_1_residual_alpha",
                "branch": "residual alpha scorer",
                "status": "SCHEMA_READY_RUNNER_REFUSES",
                "because": "K_X, Qbar_XH, qbar_XT, lambda_X, edge terms and total guard are missing",
                "allowed_statement": "alpha rows are ready as nonclaim placeholders only",
                "next_action": "fill first parent owner/Hessian/range row before alpha scoring",
            },
            {
                "verdict_id": "BV3092_2_coupling_status",
                "branch": "coupling/source gap",
                "status": "CONFIRMED_AS_LIVE_GAP",
                "because": "J_X, qbar_XT, Qbar_XH and edge projection are exact coupling/source places where local tests bite",
                "allowed_statement": "coupling is now a concrete input class, not a vague objection",
                "next_action": "after owner/Z/M, attack J_X=0 or source product with paths",
            },
            {
                "verdict_id": "BV3092_3_next_target",
                "branch": "next target",
                "status": "PARENT_OWNER_AND_HESSIAN_FIRST",
                "because": "without a parent Xhat and Z_X/M_X2, neither no-hair nor alpha(lambda) can be normalized",
                "allowed_statement": "operator/range owner is the next least-fake derivation target",
                "next_action": "3093-Y5-R2FR-parent-Xhat-owner-and-Hessian-ZX-MX2-range-or-alpha-source-row-under-AX1090.md",
            },
        ]
    )


def claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG3092_0_sources_registered", "3092 source chain exists", "sources prove audit continuity only, not no-hair activation"),
        ("CG3092_1_parent_owner", "dangerous scalar is parent-owned", "OWN3092_4_verdict=PARENT_OWNER_NOT_DERIVED"),
        ("CG3092_2_positive_operator", "positive self-adjoint operator applies to MTS", "OP3092_4_verdict=OPERATOR_PACK_UNSIGNED"),
        ("CG3092_3_source_silence", "J_X=0 channelwise", "JX3092_5_verdict=SOURCE_SILENCE_NOT_DERIVED"),
        ("CG3092_4_boundary_silence", "boundary_flux_X=0", "SIA3092_5_boundary_flux_zero=MISSING_BOUNDARY_LOCK"),
        ("CG3092_5_scalar_nohair_claim", "scalar no-hair theorem closes local branch", "exact conditional theorem lacks parent owner/operator/source/boundary premises"),
        ("CG3092_6_alpha_runner_claim", "residual alpha row can be scored", "alpha runner refusal blocks all rows"),
        ("CG3092_7_local_GR_Newton", "derived local GR/Newton reduction", "no quotient no-pole theorem and no scalar no-hair theorem"),
    ]
    return with_meta(
        [
            {
                "gate_id": gate_id,
                "claim": claim,
                "gate_pass": False,
                "reason": reason,
                "claim_allowed": False,
                "claim_allowed_for_physics": False,
            }
            for gate_id, claim, reason in gates
        ]
    )


def decision_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "decision_id": "DEC3092_0_scalar_result",
                "finding": "Scalar no-hair cannot be claimed from current AX1090 inputs.",
                "because": "the energy identity is exact conditional math, but all physical owner/sign/source/boundary inputs are missing or unsigned",
                "action": "keep no-hair as theorem contract, not evidence",
            },
            {
                "decision_id": "DEC3092_1_runner_result",
                "finding": "Residual alpha runner is staged but refuses all claims.",
                "because": "operator/range, source, projection, edge and total guard rows are missing",
                "action": "fill first parent owner/Hessian/range row before alpha scoring",
            },
            {
                "decision_id": "DEC3092_2_coupling_result",
                "finding": "The coupling gap is the live mathematical problem.",
                "because": "J_X and the source/test/readout products are exactly where local matter can excite the retained mode",
                "action": "derive source silence or keep finite residual rows explicit",
            },
            {
                "decision_id": "DEC3092_3_next_target",
                "finding": "Next target is parent Xhat owner, Hessian signs and range.",
                "because": "Z_X and M_X2 are the first shared inputs for both scalar no-hair and alpha(lambda)",
                "action": "3093-Y5-R2FR-parent-Xhat-owner-and-Hessian-ZX-MX2-range-or-alpha-source-row-under-AX1090.md",
            },
        ]
    )


def next_target_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "next_id": "NEXT3092_0_3093",
                "next_checkpoint": "3093-Y5-R2FR-parent-Xhat-owner-and-Hessian-ZX-MX2-range-or-alpha-source-row-under-AX1090.md",
                "script": "scripts/Y5_R2FR_parent_Xhat_owner_and_Hessian_ZX_MX2_range_or_alpha_source_row_under_AX1090_3093.py",
                "mission": "derive or source the parent Xhat owner, Hessian signs, field units, M_X^2, lambda_X, and first fallback alpha source row if Hessian ownership fails",
                "starting_equation": "lambda_X=sqrt(Z_X/M_X^2); alpha_X(lambda)=K_X Qbar_XH qbar_XT",
                "claim_policy": "no scalar no-hair, residual alpha, R10/R11, WEP, PPN, clock, orbital, Newton or local-GR claim unless parent owner/Hessian/range or fallback source row is real and no-cancellation guard is satisfied",
            }
        ]
    )


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = {
        "scalar_inputs_copy": OUTPUTS["scalar_inputs"],
        "alpha_rows_copy": OUTPUTS["alpha_rows"],
        "alpha_refusal_copy": OUTPUTS["alpha_refusal"],
        "branch_verdicts_copy": OUTPUTS["branch_verdicts"],
        "next_copy": OUTPUTS["next"],
    }
    output_rows = []
    for key, source_path in copies.items():
        target_path = BRANCH_OUTPUTS[key]
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, target_path)
        output_rows.append(
            {
                **meta(),
                "copy_id": f"COPY3092_{key}",
                "source_path": str(source_path),
                "target_path": str(target_path),
                "target_exists": target_path.exists(),
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    write_csv(OUTPUTS["branches"], output_rows)
    return output_rows


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(output_rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in output_rows:
        lines.append("| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 3092 Y5 R2FR scalar no-hair input pack or residual alpha coefficient runner under AX1090",
        "",
        "**Status:** the scalar no-hair identity is now an exact conditional theorem contract, not an MTS claim. Current AX1090 inputs still do not own parent `Xhat`, `Z_X`, `M_X^2`, `J_X=0`, `boundary_flux_X=0`, `lambda_X`, or source-normalized residual alpha coefficients.",
        "",
        "**Claim ceiling:** no scalar no-hair theorem, residual alpha pass, R10/R11 pass, WEP/PPN/clock/orbital pass, local-GR/Newton reduction, GitHub action, or `formalization-workbench` edit is allowed from 3092.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "parse_ok", "needles_present", "missing_needles", "role"]),
        "",
        "## Scalar Input Assessment",
        markdown_table(data["scalar_inputs"], ["input_id", "quantity", "required_condition", "current_evidence", "current_status", "missing_for_claim", "if_missing", "valid_for_claim"]),
        "",
        "## Positive No-Hair Contract",
        markdown_table(data["nohair_contract"], ["theorem_id", "step", "mathematical_statement", "status", "consequence", "math_valid", "valid_for_claim"]),
        "",
        "## Parent Scalar Owner Audit",
        markdown_table(data["parent_owner"], ["owner_id", "candidate_owner", "needed_identity", "current_status", "why_not_closed", "if_closed", "valid_for_claim"]),
        "",
        "## Positive Operator Input Pack",
        markdown_table(data["operator_pack"], ["input_id", "required_input", "mathematical_role", "current_status", "source_basis", "blocks_claim", "valid_for_claim"]),
        "",
        "## Source Silence Audit",
        markdown_table(data["source_silence"], ["silence_id", "channel", "needed_zero", "current_status", "obstruction", "finite_fallback", "valid_for_claim"]),
        "",
        "## Alpha Coefficient Rows",
        markdown_table(data["alpha_rows"], ["row_id", "quantity", "formula", "required_columns", "current_status", "valid_for_claim"]),
        "",
        "## Alpha Runner Refusal",
        markdown_table(data["alpha_refusal"], ["runner_id", "row_id", "computed_status", "claim_allowed", "failure_reasons", "valid_for_claim"]),
        "",
        "## Branch Verdicts",
        markdown_table(data["branch_verdicts"], ["verdict_id", "branch", "status", "because", "allowed_statement", "next_action", "valid_for_claim"]),
        "",
        "## Claim Gate",
        markdown_table(data["claim_gate"], ["gate_id", "claim", "gate_pass", "reason", "claim_allowed_for_physics", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decision"], ["decision_id", "finding", "because", "action", "valid_for_claim"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["next_id", "next_checkpoint", "script", "mission", "starting_equation", "claim_policy"]),
        "",
        "## Validation",
        markdown_table(data["validation"], ["validation_id", "check_pass", "detail", "artifact"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def contains_status(path: Path, field: str, expected: str) -> bool:
    return any(str(row.get(field, "")) == expected for row in rows(path))


def all_false(path: Path, field: str) -> bool:
    table = rows(path)
    return bool(table) and all(not boolish(row.get(field, "")) for row in table)


def validation_rows() -> list[dict[str, Any]]:
    formalization_3092 = list(FORMALIZATION.rglob("*3092*")) if FORMALIZATION.exists() else []
    checks = [
        ("VAL3092_00_sources_csv", csv_ok(OUTPUTS["sources"]), "source register parses", OUTPUTS["sources"]),
        ("VAL3092_01_sources_exist", all(boolish(row["exists"]) for row in rows(OUTPUTS["sources"])), "every cited local source path exists", OUTPUTS["sources"]),
        ("VAL3092_02_sources_parse", all(boolish(row["parse_ok"]) for row in rows(OUTPUTS["sources"])), "every cited csv source parses", OUTPUTS["sources"]),
        ("VAL3092_03_needles_present", all(boolish(row["needles_present"]) for row in rows(OUTPUTS["sources"])), "all source needles found", OUTPUTS["sources"]),
        ("VAL3092_04_doc_created", DOC.exists(), "checkpoint markdown created", DOC),
        ("VAL3092_05_scalar_inputs_parse", csv_ok(OUTPUTS["scalar_inputs"]), "scalar assessment parses", OUTPUTS["scalar_inputs"]),
        ("VAL3092_06_scalar_verdict_fail", contains_status(OUTPUTS["scalar_inputs"], "current_status", "FAIL_CURRENT_CLAIM"), "scalar no-hair verdict refuses claim", OUTPUTS["scalar_inputs"]),
        ("VAL3092_07_contract_parse", csv_ok(OUTPUTS["nohair_contract"]), "positive no-hair contract parses", OUTPUTS["nohair_contract"]),
        ("VAL3092_08_contract_exact", contains_status(OUTPUTS["nohair_contract"], "status", "EXACT_CONDITIONAL_THEOREM"), "conditional zero theorem row exists", OUTPUTS["nohair_contract"]),
        ("VAL3092_09_parent_owner_parse", csv_ok(OUTPUTS["parent_owner"]), "parent owner audit parses", OUTPUTS["parent_owner"]),
        ("VAL3092_10_parent_owner_unsigned", contains_status(OUTPUTS["parent_owner"], "current_status", "PARENT_OWNER_NOT_DERIVED"), "parent owner not derived", OUTPUTS["parent_owner"]),
        ("VAL3092_11_operator_pack_parse", csv_ok(OUTPUTS["operator_pack"]), "operator pack parses", OUTPUTS["operator_pack"]),
        ("VAL3092_12_operator_unsigned", contains_status(OUTPUTS["operator_pack"], "current_status", "OPERATOR_PACK_UNSIGNED"), "operator pack unsigned", OUTPUTS["operator_pack"]),
        ("VAL3092_13_source_silence_parse", csv_ok(OUTPUTS["source_silence"]), "source silence audit parses", OUTPUTS["source_silence"]),
        ("VAL3092_14_source_silence_unsigned", contains_status(OUTPUTS["source_silence"], "current_status", "SOURCE_SILENCE_NOT_DERIVED"), "source silence not derived", OUTPUTS["source_silence"]),
        ("VAL3092_15_alpha_rows_parse", csv_ok(OUTPUTS["alpha_rows"]), "alpha coefficient rows parse", OUTPUTS["alpha_rows"]),
        ("VAL3092_16_alpha_rows_nonclaim", all_false(OUTPUTS["alpha_rows"], "valid_for_claim"), "alpha rows remain nonclaim", OUTPUTS["alpha_rows"]),
        ("VAL3092_17_alpha_refusal_parse", csv_ok(OUTPUTS["alpha_refusal"]), "alpha refusal parses", OUTPUTS["alpha_refusal"]),
        ("VAL3092_18_alpha_refuses", contains_status(OUTPUTS["alpha_refusal"], "computed_status", "REFUSED_NO_CLAIM"), "runner refuses all claims", OUTPUTS["alpha_refusal"]),
        ("VAL3092_19_branch_verdicts_parse", csv_ok(OUTPUTS["branch_verdicts"]), "branch verdicts parse", OUTPUTS["branch_verdicts"]),
        ("VAL3092_20_next_3093_selected", contains_status(OUTPUTS["branch_verdicts"], "status", "PARENT_OWNER_AND_HESSIAN_FIRST"), "branch verdict selects 3093", OUTPUTS["branch_verdicts"]),
        ("VAL3092_21_claim_gate_parse", csv_ok(OUTPUTS["claim_gate"]), "claim gate parses", OUTPUTS["claim_gate"]),
        ("VAL3092_22_claims_blocked", all_false(OUTPUTS["claim_gate"], "claim_allowed_for_physics"), "all physics claims blocked", OUTPUTS["claim_gate"]),
        ("VAL3092_23_decision_parse", csv_ok(OUTPUTS["decision"]), "decision ledger parses", OUTPUTS["decision"]),
        ("VAL3092_24_next_parse", csv_ok(OUTPUTS["next"]), "next target parses", OUTPUTS["next"]),
        ("VAL3092_25_branch_copies_parse", csv_ok(OUTPUTS["branches"]), "branch copy ledger parses", OUTPUTS["branches"]),
        ("VAL3092_26_branch_copies_exist", all(boolish(row["target_exists"]) for row in rows(OUTPUTS["branches"])), "all branch copies exist", OUTPUTS["branches"]),
        ("VAL3092_27_no_formalization_edit", len(formalization_3092) == 0, "no 3092 files created under formalization-workbench", FORMALIZATION),
        ("VAL3092_28_pycache_removed", not PYCACHE.exists(), "scripts __pycache__ absent after run", PYCACHE),
    ]
    return [
        {
            **meta(),
            "validation_id": validation_id,
            "check_pass": bool(check_pass),
            "detail": detail,
            "artifact": str(artifact),
        }
        for validation_id, check_pass, detail, artifact in checks
    ]


def main() -> None:
    remove_pycache()
    for directory in [RESIDUALS, LOCAL_BOUNDS, RAB_QUEUE]:
        directory.mkdir(parents=True, exist_ok=True)

    data = {
        "sources": source_rows(),
        "scalar_inputs": scalar_input_rows(),
        "nohair_contract": nohair_contract_rows(),
        "parent_owner": parent_owner_rows(),
        "operator_pack": operator_pack_rows(),
        "source_silence": source_silence_rows(),
        "alpha_rows": alpha_coefficient_rows(),
        "alpha_refusal": alpha_refusal_rows(),
        "branch_verdicts": branch_verdict_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_target_rows(),
    }

    write_csv(OUTPUTS["sources"], data["sources"])
    write_csv(OUTPUTS["scalar_inputs"], data["scalar_inputs"])
    write_csv(OUTPUTS["nohair_contract"], data["nohair_contract"])
    write_csv(OUTPUTS["parent_owner"], data["parent_owner"])
    write_csv(OUTPUTS["operator_pack"], data["operator_pack"])
    write_csv(OUTPUTS["source_silence"], data["source_silence"])
    write_csv(OUTPUTS["alpha_rows"], data["alpha_rows"])
    write_csv(OUTPUTS["alpha_refusal"], data["alpha_refusal"])
    write_csv(OUTPUTS["branch_verdicts"], data["branch_verdicts"])
    write_csv(OUTPUTS["claim_gate"], data["claim_gate"])
    write_csv(OUTPUTS["decision"], data["decision"])
    write_csv(OUTPUTS["next"], data["next"])

    data["branches"] = copy_branch_outputs()
    data["validation"] = []
    write_doc(data)
    data["validation"] = validation_rows()
    write_csv(OUTPUTS["validation"], data["validation"])
    write_doc(data)
    remove_pycache()

    passed = sum(1 for row in data["validation"] if boolish(row["check_pass"]))
    print(f"3092 scalar no-hair / residual alpha checkpoint written: {passed}/{len(data['validation'])} validation checks passed")
    print(DOC)
    print(OUTPUTS["validation"])


if __name__ == "__main__":
    main()
