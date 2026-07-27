from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2210"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2210-Y5-R2FR-lambda-X-range-owner-or-R10-source-map-first-row.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2210_SOURCE_REGISTER.csv",
    "range_derivation": OUT / "P8_Y5_PARENT_QLOC_2210_RANGE_OPERATOR_DERIVATION.csv",
    "coefficient_audit": OUT / "P8_Y5_PARENT_QLOC_2210_PARENT_COEFFICIENT_AUDIT.csv",
    "branch_classifier": OUT / "P8_Y5_PARENT_QLOC_2210_RANGE_BRANCH_CLASSIFIER.csv",
    "source_map_first": OUT / "P8_Y5_PARENT_QLOC_2210_R10_SOURCE_MAP_FIRST_ROW.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2210_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2210_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2210_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2210_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2210_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2210_RANGE_OWNER_BLOCKER_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2210_RANGE_OPERATOR_NONCLAIM.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_RANGE_THEOREM_2210_NONCLAIM.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def csv_rows_parse(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body: list[str] = []
    for row in rows:
        body.append(
            "| "
            + " | ".join(
                str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
                for column in columns
            )
            + " |"
        )
    return "\n".join([header, sep, *body])


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def formalization_has_2210_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2210-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2210*",
        "*P8_Y5_BRR545_2210*",
        "*Y5_R2FR_lambda_X_range_owner_or_R10_source_map_first_row_2210*",
        "*JR2210*",
        "*PARENT_QLOC_RANGE_THEOREM_2210*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2209_handoff",
            ROOT / "2209-Y5-R2FR-R10-q-loc-Yukawa-source-map-or-bound-curve-blocker.md",
            ["NEXT2209_0_2210", "lambda_X/range owner exists", "VAL2209_OVERALL"],
            "2209 selects lambda_X/range ownership as the next clean discriminator.",
        ),
        (
            "2207_response_doublet",
            ROOT / "2207-Y5-R2FR-Gamma-eff-metric-variation-or-first-q-loc-response-operator-row.md",
            ["Gamma_eff = Gamma0 + 1/2 M_AB", "K_hat equals K_metric", "VAL2207_OVERALL"],
            "response-doublet quadratic density is the leading future parent-action owner candidate.",
        ),
        (
            "562_mass_gap_relation",
            ROOT / "562-Y5-R10-ZX-lambda-mass-gap-and-bound-curve-fill-or-theorem-zero.md",
            ["lambda_X = 1/mu_X = sqrt(Z_X/M_X^2)", "PR562_2_canonical_mass_and_range", "MG562_1_mass_positive"],
            "scalar mass-gap/range relation and positive-operator no-hair guardrail.",
        ),
        (
            "560_alpha_law",
            ROOT / "560-Y5-R10-source-normalized-alpha-law-from-parent-or-runner-real-data-fill.md",
            ["alpha_X(lambda_X)=s_X Pi_M^H[Q_X^H(lambda_X)] q_X^T", "AL560_2_exterior_green_function", "PI560_1_mX"],
            "source-normalized R10 force law with parent-owned lambda and charges still missing.",
        ),
        (
            "561_numerator_gate",
            ROOT / "561-Y5-R10-source-test-charge-and-PiM-projection-zero-or-coefficient-fill.md",
            ["N_X(lambda)=Pi_M^H[Q_X^H(lambda)] q_X^T", "NC561_7_alpha_prefactor_guard", "O561_5_prefactor_and_range_deferred"],
            "source/test/PiM numerator factorization and coefficient fallback.",
        ),
        (
            "380_bulk_X_contract",
            ROOT / "380-bulk-X-mass-gap-source-normalized-force-law.md",
            ["lambda_X = 1 / m_X", "source-normalized force-law contract written", "mass-gap no-hair identity written"],
            "earlier local mass-gap versus source-normalized Yukawa route contract.",
        ),
        (
            "380_gate_results",
            ROOT / "runs" / "20260602-004500-bulk-X-mass-gap-source-normalized-force-law" / "results" / "gate_results.csv",
            ["positive_X_operator_parent_derived,fail", "alphaX_lambdaX_parent_derived,fail", "claim_ceiling_enforced,pass"],
            "machine-readable prior verdict: contract exists, parent derivation/numeric alpha-lambda missing.",
        ),
        (
            "2208_kernel_scaffold",
            OUT / "P8_Y5_PARENT_QLOC_2208_R10_RANGE_KERNEL_SCAFFOLD.csv",
            ["R10K2208_0_yukawa_kernel_form", "K_lambda(r)", "alpha_R10_q(lambda)"],
            "standard Yukawa kernel and alpha(lambda) comparison shape.",
        ),
        (
            "563_bound_anchor",
            ROOT / "563-Y5-R10-real-bound-curve-acquisition-and-alpha-row-smoke-runner.md",
            ["E563_2_mts_parent_coefficients_missing", "B563_0_no_full_bound_curve", "Z_X, M_X^2"],
            "real anchor provenance plus parent-coefficient blocker.",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needles, role in specs:
        text = read_text(path)
        found = [needle for needle in needles if needle in text]
        rows.append(
            base_row(
                source_id=source_id,
                source_path=str(path),
                path_exists=path.exists(),
                required_needles=";".join(needles),
                found_needles=";".join(found),
                needles_found=path.exists() and len(found) == len(needles),
                role=role,
            )
        )
    return rows


def range_derivation_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            derivation_id="ROD2210_0_parent_static_operator",
            object="local residual mode operator",
            exact_statement="After quotient/domain projection, any local finite-range residual branch must linearize to L_AB X^B = J_A with L_AB=-Z_AB Delta+M_AB plus controlled lower-derivative terms.",
            derivation_status="CONDITIONAL_OPERATOR_FORM_DERIVED",
            what_is_new="lambda is owned by the parent operator spectrum, not by the R10 fit.",
            required_parent_inputs="quotient projector;local field basis X^A;Z_AB;M_AB;boundary domain;source split J_A",
            missing_inputs="MISSING_PARENT_Z_AB;MISSING_PARENT_M_AB;MISSING_DOMAIN_CERTIFICATE",
            score_ready=False,
        ),
        base_row(
            derivation_id="ROD2210_1_generalized_range_spectrum",
            object="lambda_X range owner",
            exact_statement="For a healthy local branch, solve M_AB v_i^B = mu_i^2 Z_AB v_i^B; each positive eigenvalue gives lambda_i=1/sqrt(mu_i^2).",
            derivation_status="GENERALIZED_RANGE_OWNER_THEOREM_WRITTEN",
            what_is_new="the earlier scalar law lambda_X=sqrt(Z_X/M_X^2) is the one-mode reduction of the generalized eigenvalue problem.",
            required_parent_inputs="positive semidefinite Z_AB on physical quotient;self-adjoint M_AB on same domain;units convention for X^A",
            missing_inputs="MISSING_NUMERIC_OR_SYMBOLIC_EIGENVALUES;MISSING_UNITS_OWNER",
            score_ready=False,
        ),
        base_row(
            derivation_id="ROD2210_2_scalar_reduction",
            object="single X mode",
            exact_statement="If the quotient leaves one scalar-equivalent mode with constant Z_X and M_X^2, then mu_X^2=M_X^2/Z_X and lambda_X=sqrt(Z_X/M_X^2).",
            derivation_status="SCALAR_RELATION_RECOVERED_FROM_SPECTRUM",
            what_is_new="562 relation is retained but now explicitly tied to a parent spectral owner.",
            required_parent_inputs="Z_X>0;M_X^2>0;same branch convention;source-free or source-retained decision",
            missing_inputs="MISSING_Z_X;MISSING_M_X_SQUARED",
            score_ready=False,
        ),
        base_row(
            derivation_id="ROD2210_3_constraint_branch",
            object="rank-zero or first-order constraint route",
            exact_statement="If Z_AB has no physical quotient eigenmode, lambda_X is not a Yukawa range; the branch must close through a constraint/source identity or remain a non-propagating residual.",
            derivation_status="NO_RANGE_BRANCH_CLASSIFIER_WRITTEN",
            what_is_new="a missing lambda is not automatically failure; it may mean R10 is the wrong arena and the proof target is source silence.",
            required_parent_inputs="rank certificate for Z_AB on physical quotient;constraint algebra;boundary primitive",
            missing_inputs="MISSING_RANK_CERTIFICATE;MISSING_CONSTRAINT_ALGEBRA",
            score_ready=False,
        ),
        base_row(
            derivation_id="ROD2210_4_spectral_memory_branch",
            object="nonlocal or memory kernel",
            exact_statement="If the parent gives a spectral kernel instead of finite matrices, the R10 object is d rho(mu) with lambda=1/mu and alpha(lambda) must be an envelope over the spectral measure.",
            derivation_status="SPECTRAL_RANGE_GENERALIZATION_WRITTEN",
            what_is_new="memory cannot be squeezed into a single convenience lambda without a spectrum.",
            required_parent_inputs="spectral density;positive weights;source/test charge density over mu;bound-envelope rule",
            missing_inputs="MISSING_SPECTRAL_MEASURE;MISSING_ENVELOPE_RULE",
            score_ready=False,
        ),
        base_row(
            derivation_id="ROD2210_5_verdict",
            object="range-owner status",
            exact_statement="Operator-level range ownership is derived; numeric or branch-selecting lambda_X is still blocked until Z/M/domain/source data are parent-signed.",
            derivation_status="RANGE_OWNER_LAW_DERIVED_VALUES_BLOCKED",
            what_is_new="one quartet member moves from vague missing variable to exact theorem/input contract.",
            required_parent_inputs="parent Z_AB/M_AB or rank/spectral replacement;source map;charges;full bound curve",
            missing_inputs="MISSING_PARENT_COEFFICIENTS;MISSING_QLOC_TO_SOURCE_MAP;MISSING_CHARGES;MISSING_FULL_BOUND_CURVE",
            score_ready=False,
        ),
    ]


def coefficient_audit_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            coefficient_id="PCA2210_0_Z_AB",
            symbol="Z_AB",
            role="kinetic/gradient residue on physical quotient",
            required_for="eigenvalue problem and ghost-free local branch",
            current_status="MISSING_PARENT_RESIDUE",
            evidence="562 and 560 use Z_X conditionally; no current source gives parent-owned Z_AB for q_loc branch.",
            repair="derive from second variation of parent action or demote to coefficient acquisition row",
            passes_now=False,
        ),
        base_row(
            coefficient_id="PCA2210_1_M_AB",
            symbol="M_AB",
            role="mass/Hessian residue around local vacuum",
            required_for="finite real lambda_i and branch classification",
            current_status="MISSING_PARENT_HESSIAN",
            evidence="562 records M_X^2 missing; 2207 has M_AB in Gamma_eff density but not as a proven kinetic/mass operator.",
            repair="map response-doublet M_AB to physical Hessian with units, or keep lambda numeric blocked",
            passes_now=False,
        ),
        base_row(
            coefficient_id="PCA2210_2_domain",
            symbol="Dom(L_X)",
            role="self-adjoint quotient/boundary domain",
            required_for="real spectrum, integration by parts, no hidden boundary source",
            current_status="MISSING_DOMAIN_CERTIFICATE",
            evidence="380/562 no-hair identities require zero boundary flux and domain silence; not parent-signed.",
            repair="derive boundary primitive/no-flux or include boundary charge in Q_X^H(lambda)",
            passes_now=False,
        ),
        base_row(
            coefficient_id="PCA2210_3_source_split",
            symbol="J_A",
            role="matter/projector/memory/domain source driving the range mode",
            required_for="theorem-zero versus nonzero Yukawa source decision",
            current_status="MISSING_PARENT_SOURCE_SPLIT",
            evidence="561 keeps Q_X^H, q_X^T, PiM leakage and boundary/memory source as retained coefficients.",
            repair="prove J_A=0 channelwise or write source-normalized coefficient rows",
            passes_now=False,
        ),
        base_row(
            coefficient_id="PCA2210_4_q_loc_projection",
            symbol="S_A[q_loc,T_GK]",
            role="maps q_loc/T_GK residual into scalar/eigenmode source",
            required_for="R10 alpha(lambda) from q_loc rather than a placeholder X",
            current_status="MISSING_QLOC_TO_EIGENSOURCE_MAP",
            evidence="2208/2209 identify q_loc as vector/projected divergence; no inverse-divergence or T_GK owner is signed.",
            repair="derive current owner/inverse-divergence map or keep q_loc residual vector unscored",
            passes_now=False,
        ),
    ]


def branch_classifier_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            branch_id_local="RBC2210_0_finite_positive",
            branch_condition="Z_AB positive on quotient and mu_i^2>0",
            arena_decision="finite-range Yukawa/R10 if lambda_i lies in short-range apparatus band; otherwise use the arena matching the scale",
            current_status="POSSIBLE_NOT_SELECTED",
            missing_for_selection="MISSING_EIGENVALUES;MISSING_UNITS;MISSING_SOURCE_CHARGE",
            local_gr_implication="safe only if source/test/projection zero or alpha envelope is below bounds",
            valid_branch_now=False,
        ),
        base_row(
            branch_id_local="RBC2210_1_massless",
            branch_condition="mu_i^2=0",
            arena_decision="not R10; long-range PPN/orbital/GM-calibration branch unless coupling is theorem-zero",
            current_status="DANGER_BRANCH_UNRESOLVED",
            missing_for_selection="MISSING_MASSLESS_GAUGE_OR_UNIVERSAL_CALIBRATION_THEOREM",
            local_gr_implication="cannot be hidden as short-range suppression",
            valid_branch_now=False,
        ),
        base_row(
            branch_id_local="RBC2210_2_wrong_sign",
            branch_condition="negative Z direction or mu_i^2<0",
            arena_decision="reject for local-GR route unless parent proves it is gauge/nonphysical",
            current_status="REJECT_UNLESS_PARENT_EXCLUDES",
            missing_for_selection="MISSING_POSITIVITY_CERTIFICATE",
            local_gr_implication="tachyon/ghost/growing exterior mode would break local branch",
            valid_branch_now=False,
        ),
        base_row(
            branch_id_local="RBC2210_3_constraint_rank_zero",
            branch_condition="no propagating quotient eigenmode or first-order constraint only",
            arena_decision="range is absent; prove source/current identity rather than run R10",
            current_status="POSSIBLE_CLEAN_ROUTE_NOT_PROVED",
            missing_for_selection="MISSING_RANK_ZERO_CERTIFICATE;MISSING_CONSTRAINT_SOURCE_IDENTITY",
            local_gr_implication="best local-GR route if it zeros the physical source before readout",
            valid_branch_now=False,
        ),
        base_row(
            branch_id_local="RBC2210_4_spectral_memory",
            branch_condition="continuum or memory kernel d rho(mu)",
            arena_decision="R10 needs envelope over alpha(mu), not one lambda",
            current_status="UNSCORED_SPECTRAL_RESIDUAL",
            missing_for_selection="MISSING_SPECTRAL_DENSITY;MISSING_WEIGHT_POSITIVITY;MISSING_BOUND_ENVELOPE",
            local_gr_implication="can still pass, but only as an integral/envelope bound",
            valid_branch_now=False,
        ),
        base_row(
            branch_id_local="RBC2210_5_verdict",
            branch_condition="current corpus",
            arena_decision="no R10/PPN/screened branch selected yet",
            current_status="BRANCH_SELECTION_BLOCKED_BY_PARENT_COEFFICIENTS",
            missing_for_selection="MISSING_Z_AB;MISSING_M_AB;MISSING_DOMAIN;MISSING_SOURCE_MAP",
            local_gr_implication="local GR remains a derivation target, not a claim",
            valid_branch_now=False,
        ),
    ]


def source_map_first_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            map_id="SM2210_0_eigenmode_source_slot",
            object="range-indexed source map",
            conditional_form="J_i = v_i^A J_A, with (M_AB-mu_i^2 Z_AB)v_i^B=0 and lambda_i=1/mu_i",
            relation_to_q_loc="q_loc can source R10 only after the parent identifies J_A or T_GK/inverse-divergence as the scalar source feeding v_i.",
            current_status="FIRST_ROW_WRITTEN_NOT_PARENT_SIGNED",
            missing_inputs="MISSING_J_A;MISSING_V_i;MISSING_TGK_OR_INVERSE_DIVERGENCE;MISSING_UNITS",
            score_ready=False,
        ),
        base_row(
            map_id="SM2210_1_alpha_row_shape",
            object="range-indexed alpha(lambda)",
            conditional_form="alpha_i=s_i N_i/(4*pi*Z_i*G_obs*M_H*m_T), lambda_i=1/mu_i, N_i=Pi_M^H[Q_i^H(lambda_i)] q_i^T",
            relation_to_q_loc="inherits 561 numerator and 560/562 prefactor once eigenmode normalization is parent-owned.",
            current_status="SCHEMA_READY_VALUES_MISSING",
            missing_inputs="MISSING_Z_i;MISSING_N_i;MISSING_SOURCE_TEST_CHARGES;MISSING_FULL_BOUND_CURVE",
            score_ready=False,
        ),
        base_row(
            map_id="SM2210_2_no_scalar_proxy_guard",
            object="q_loc vector to scalar guard",
            conditional_form="S_i[q_loc] is illegal unless parent supplies tau_i_nu, T_GK inverse-divergence, or current-owner map before readout.",
            relation_to_q_loc="prevents replacing q_loc^nu by a hand-picked scalar amplitude.",
            current_status="GUARDRAIL_ACTIVE",
            missing_inputs="MISSING_TAU_i;MISSING_CURRENT_OWNER;MISSING_PROJECTOR_DOMAIN",
            score_ready=False,
        ),
        base_row(
            map_id="SM2210_3_verdict",
            object="first q_loc-to-source row",
            conditional_form="source map row is range-indexed but nonclaim",
            relation_to_q_loc="q_loc is now pointed at an eigenmode source contract, but the map is not filled.",
            current_status="SOURCE_MAP_FIRST_ROW_STAGED_VALUES_BLOCKED",
            missing_inputs="MISSING_PARENT_COEFFICIENTS;MISSING_SOURCE_OWNER",
            score_ready=False,
        ),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            gate_id="CG2210_0_range_law",
            gate="operator-level lambda owner exists",
            status="PASS_NONCLAIM",
            implication="lambda is now a parent spectrum problem: M v = mu^2 Z v; scalar lambda=sqrt(Z/M^2) is a reduction.",
        ),
        base_row(
            gate_id="CG2210_1_numeric_lambda",
            gate="numeric or branch-selecting lambda_i exists",
            status="BLOCKED_NONCLAIM",
            implication="Z_AB, M_AB, quotient/domain and units are not parent-signed.",
        ),
        base_row(
            gate_id="CG2210_2_source_map",
            gate="q_loc-to-eigenmode source map exists",
            status="BLOCKED_NONCLAIM",
            implication="R10 alpha remains symbolic until J_A/T_GK/inverse-divergence source owner is supplied.",
        ),
        base_row(
            gate_id="CG2210_3_R10_score",
            gate="R10 alpha(lambda) can be scored",
            status="BLOCKED_NONCLAIM",
            implication="range law improved, but source charges and full bound curve are still missing.",
        ),
        base_row(
            gate_id="CG2210_4_local_GR",
            gate="local GR/Newton reduction can be claimed",
            status="BLOCKED_NONCLAIM",
            implication="no theorem-zero or bounded residual proof is complete.",
        ),
        base_row(
            gate_id="CG2210_5_GitHub",
            gate="public/github update",
            status="BLOCKED_NONCLAIM",
            implication="private derivation work only; no GitHub action.",
        ),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            decision_id="DEC2210_0_gain",
            decision="RANGE_OWNER_OPERATOR_LEVEL_DERIVED",
            rationale="The range scale is no longer an inserted parameter: finite local modes use the generalized eigenvalue problem M_AB v=mu^2 Z_AB v and lambda=1/mu.",
            next_action="hunt parent Z_AB/M_AB/domain ownership rather than invent lambda values",
        ),
        base_row(
            decision_id="DEC2210_1_limit",
            decision="NUMERIC_RANGE_AND_BRANCH_SELECTION_BLOCKED",
            rationale="The current corpus does not parent-sign Z_AB, M_AB, quotient rank/domain, source split, or units for the q_loc branch.",
            next_action="keep R10, PPN, screened and constraint branches open until parent coefficients select one",
        ),
        base_row(
            decision_id="DEC2210_2_source_map",
            decision="FIRST_R10_EIGENSOURCE_ROW_STAGED_NONCLAIM",
            rationale="The q_loc source-map can now be written in eigenmode-indexed form, but no scalar proxy is allowed without parent current ownership.",
            next_action="derive J_A/T_GK/inverse-divergence owner after or alongside Z/M coefficient hunt",
        ),
        base_row(
            decision_id="DEC2210_3_no_claim",
            decision="NO_R10_LOCAL_GR_CLAIM",
            rationale="2210 is a derivation/input-contract gain, not an empirical pass.",
            next_action="keep all rows valid_for_claim=false until range, source, charges and bounds are real",
        ),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2210_0_2211",
            selection_status="selected",
            target_file="2211-Y5-R2FR-parent-quadratic-residue-ZM-owner-or-constraint-branch.md",
            target_script="scripts/Y5_R2FR_parent_quadratic_residue_ZM_owner_or_constraint_branch_2211.py",
            objective="try to identify parent Z_AB and M_AB from the response-doublet/Gamma_eff/K_hat route; if no physical quotient residue exists, classify the branch as constraint/rank-zero rather than finite-range R10",
            success_condition="one coefficient-owner clause is source-signed or the range branch is explicitly demoted to coefficient acquisition/constraint-only, with valid_for_claim=false",
            do_not_do="do not choose lambda by convenience, do not use a scalar proxy for q_loc, do not claim local GR/R10, do not use GitHub action",
        ),
        base_row(
            route_id="NEXT2210_1_data_parallel",
            selection_status="held_parallel",
            target_file="2210b-Y5-R2FR-EotWash-2020-bound-curve-digitization-ledger.md",
            target_script="scripts/Y5_R2FR_EotWash_2020_bound_curve_digitization_ledger_2210b.py",
            objective="acquire a full alpha_bound(lambda) curve while theory coefficients remain private/nonclaim",
            success_condition="dense positive bound rows with provenance and interpolation policy, still unusable for claim until theory alpha exists",
            do_not_do="do not promote alpha=1 threshold anchors as a full bound curve",
        ),
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["coefficient_audit"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["range_derivation"], BRANCH_COPIES["branch_wep"]),
        ("beta_docs", OUTPUTS["source_map_first"], BRANCH_COPIES["beta_docs"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        copied = False
        parse_ok = False
        count = 0
        if source.exists():
            shutil.copyfile(source, target)
            copied = True
            parse_ok, count, _ = csv_rows_parse(target)
        rows.append(
            base_row(
                copy_id=copy_id,
                source_path=str(source),
                target_path=str(target),
                copied=copied,
                parse_ok=parse_ok,
                row_count=count,
            )
        )
    return rows


def validation_rows(
    source_rows: list[dict[str, Any]],
    range_rows: list[dict[str, Any]],
    coeff_rows: list[dict[str, Any]],
    classifier_rows: list[dict[str, Any]],
    source_map_rows_: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(validation_id: str, status: bool, detail: str) -> None:
        rows.append(base_row(validation_id=validation_id, status="PASS" if status else "FAIL", detail=detail))

    sources_exist = all(truthy(row.get("path_exists")) for row in source_rows)
    needles_found = all(truthy(row.get("needles_found")) for row in source_rows)
    add("VAL2210_00_sources_exist", sources_exist, f"{sum(truthy(row.get('path_exists')) for row in source_rows)}/{len(source_rows)} sources exist")
    add("VAL2210_01_needles_found", needles_found, f"{sum(truthy(row.get('needles_found')) for row in source_rows)}/{len(source_rows)} source needle sets found")

    spectrum_ok = any(row.get("derivation_id") == "ROD2210_1_generalized_range_spectrum" and "M_AB v_i" in str(row.get("exact_statement")) for row in range_rows)
    scalar_ok = any(row.get("derivation_id") == "ROD2210_2_scalar_reduction" and "sqrt(Z_X/M_X^2)" in str(row.get("exact_statement")) for row in range_rows)
    verdict_ok = any(row.get("derivation_id") == "ROD2210_5_verdict" and row.get("derivation_status") == "RANGE_OWNER_LAW_DERIVED_VALUES_BLOCKED" for row in range_rows)
    add("VAL2210_02_range_derivation", spectrum_ok and scalar_ok and verdict_ok, "generalized range spectrum written, scalar 562 relation recovered, values blocked")

    coeff_ok = len(coeff_rows) == 5 and all(not truthy(row.get("passes_now")) for row in coeff_rows)
    add("VAL2210_03_coefficient_audit", coeff_ok, f"parent coefficient rows={len(coeff_rows)} all remain unpassed")

    classifier_ok = len(classifier_rows) == 6 and any(row.get("branch_id_local") == "RBC2210_5_verdict" and "BLOCKED" in str(row.get("current_status")) for row in classifier_rows)
    add("VAL2210_04_branch_classifier", classifier_ok, "finite/massless/wrong-sign/constraint/spectral branches classified without selection")

    source_map_ok = any(row.get("map_id") == "SM2210_0_eigenmode_source_slot" for row in source_map_rows_) and all(not truthy(row.get("score_ready")) for row in source_map_rows_)
    add("VAL2210_05_source_map_first_row", source_map_ok, "eigenmode source-map row staged and kept nonclaim")

    claim_ok = any(row.get("gate_id") == "CG2210_3_R10_score" and row.get("status") == "BLOCKED_NONCLAIM" for row in claim_rows)
    add("VAL2210_06_claim_gate", claim_ok, "R10/local claims remain blocked")

    decision_ok = any(row.get("decision") == "RANGE_OWNER_OPERATOR_LEVEL_DERIVED" for row in decision_rows_) and any(row.get("decision") == "NUMERIC_RANGE_AND_BRANCH_SELECTION_BLOCKED" for row in decision_rows_)
    add("VAL2210_07_decision", decision_ok, "decision ledger records theorem-level gain and numeric blocker")

    next_ok = any(row.get("route_id") == "NEXT2210_0_2211" and "Z_AB" in str(row.get("objective")) for row in next_rows)
    add("VAL2210_08_next_target", next_ok, "2211 parent quadratic residue Z/M owner selected")

    csv_details: list[str] = []
    csv_ok = True
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        csv_ok = csv_ok and ok
        csv_details.append(f"{path.name}:{count if ok else detail}")
    add("VAL2210_09_csv_parse", csv_ok, "; ".join(csv_details))

    branch_ok = all(truthy(row.get("copied")) and truthy(row.get("parse_ok")) for row in branch_rows)
    add("VAL2210_10_branch_copies", branch_ok, ";".join(str(row.get("target_path")) for row in branch_rows))

    generated_groups = [source_rows, range_rows, coeff_rows, classifier_rows, source_map_rows_, claim_rows, decision_rows_, next_rows, branch_rows]
    flags_false = all(
        not truthy(row.get("valid_for_claim")) and not truthy(row.get("claim_allowed"))
        for group in generated_groups
        for row in group
    )
    add("VAL2210_11_claim_flags_false", flags_false, "all generated rows keep valid_for_claim=false and claim_allowed=false")

    formalization_clean = not formalization_has_2210_artifacts()
    add("VAL2210_12_formalization_clean", formalization_clean, "formalization-workbench has no 2210 artifacts")

    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    add("VAL2210_13_pycache_absent", pycache_absent, str(ROOT / "scripts" / "__pycache__"))

    pass_so_far = all(row.get("status") == "PASS" for row in rows)
    rows.append(
        base_row(
            validation_id="VAL2210_OVERALL",
            status="PASS" if pass_so_far else "FAIL",
            detail="2210 derives the operator-level lambda owner, keeps numeric range/source-map scoring blocked, and selects parent Z/M residue ownership next",
        )
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    range_rows: list[dict[str, Any]],
    coeff_rows: list[dict[str, Any]],
    classifier_rows: list[dict[str, Any]],
    source_map_rows_: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
    validation_rows_: list[dict[str, Any]],
) -> None:
    lines = [
        "# 2210 - Y5/R2FR lambda_X Range Owner Or R10 Source Map First Row",
        "",
        "## Current Verdict",
        "",
        "2210 is a real narrowing move: `lambda_X` is not allowed to be a hand-set fifth-force knob. For any healthy local finite-range branch, the range is owned by the parent quadratic operator:",
        "",
        "`M_AB v_i^B = mu_i^2 Z_AB v_i^B`, hence `lambda_i = 1/sqrt(mu_i^2)`.",
        "",
        "The old one-mode result `lambda_X=sqrt(Z_X/M_X^2)` is recovered as a special case, but the current corpus still does not parent-sign `Z_AB`, `M_AB`, the quotient/domain, or the source split. So 2210 improves the derivation contract but does not produce a numeric R10 score or a local-GR claim.",
        "",
        "## Source Register",
        "",
        md_table(source_rows, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
        "",
        "## Range Operator Derivation",
        "",
        md_table(range_rows, ["derivation_id", "object", "exact_statement", "derivation_status", "what_is_new", "required_parent_inputs", "missing_inputs", "score_ready", "valid_for_claim"]),
        "",
        "## Parent Coefficient Audit",
        "",
        md_table(coeff_rows, ["coefficient_id", "symbol", "role", "required_for", "current_status", "evidence", "repair", "passes_now", "valid_for_claim"]),
        "",
        "## Range Branch Classifier",
        "",
        md_table(classifier_rows, ["branch_id_local", "branch_condition", "arena_decision", "current_status", "missing_for_selection", "local_gr_implication", "valid_branch_now", "valid_for_claim"]),
        "",
        "## R10 Source Map First Row",
        "",
        md_table(source_map_rows_, ["map_id", "object", "conditional_form", "relation_to_q_loc", "current_status", "missing_inputs", "score_ready", "valid_for_claim"]),
        "",
        "## Claim Gate",
        "",
        md_table(claim_rows, ["gate_id", "gate", "status", "implication", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decision_rows_, ["decision_id", "decision", "rationale", "next_action", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(next_rows, ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(branch_rows, ["copy_id", "source_path", "target_path", "copied", "parse_ok", "row_count", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(validation_rows_, ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"]),
        "",
        "## Working Interpretation",
        "",
        "This is the kind of step we want: it does not win by assertion, but it removes wiggle room. If MTS has a local finite-range residual, its `lambda` must come from the parent spectrum. If it has no physical spectrum, then the route is constraint/source-silence, not R10. That makes the next target sharper: find the parent quadratic residue `Z_AB/M_AB`, or demote finite-range R10 to a coefficient-acquisition branch.",
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    remove_pycache()

    source_rows = source_register_rows()
    range_rows = range_derivation_rows()
    coeff_rows = coefficient_audit_rows()
    classifier_rows = branch_classifier_rows()
    source_map_rows_ = source_map_first_rows()
    claim_rows = claim_gate_rows()
    decision_rows_ = decision_rows()
    next_rows = next_target_rows()

    for path, rows in [
        (OUTPUTS["source_register"], source_rows),
        (OUTPUTS["range_derivation"], range_rows),
        (OUTPUTS["coefficient_audit"], coeff_rows),
        (OUTPUTS["branch_classifier"], classifier_rows),
        (OUTPUTS["source_map_first"], source_map_rows_),
        (OUTPUTS["claim_gate"], claim_rows),
        (OUTPUTS["decision"], decision_rows_),
        (OUTPUTS["next_target"], next_rows),
    ]:
        write_csv(path, rows)

    branch_rows = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], branch_rows)

    remove_pycache()
    validation_rows_ = validation_rows(
        source_rows,
        range_rows,
        coeff_rows,
        classifier_rows,
        source_map_rows_,
        claim_rows,
        decision_rows_,
        next_rows,
        branch_rows,
    )
    write_csv(OUTPUTS["validation"], validation_rows_)

    write_doc(
        source_rows,
        range_rows,
        coeff_rows,
        classifier_rows,
        source_map_rows_,
        claim_rows,
        decision_rows_,
        next_rows,
        branch_rows,
        validation_rows_,
    )

    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
