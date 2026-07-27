from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2211"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2211-Y5-R2FR-parent-quadratic-residue-ZM-owner-or-constraint-branch.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2211_SOURCE_REGISTER.csv",
    "zm_owner_audit": OUT / "P8_Y5_PARENT_QLOC_2211_ZM_OWNER_AUDIT.csv",
    "hessian_range_lemma": OUT / "P8_Y5_PARENT_QLOC_2211_HESSIAN_VS_RANGE_LEMMA.csv",
    "coefficient_acquisition": OUT / "P8_Y5_PARENT_QLOC_2211_COEFFICIENT_ACQUISITION_ROWS.csv",
    "branch_demoter": OUT / "P8_Y5_PARENT_QLOC_2211_RANGE_BRANCH_DEMOTER.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2211_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2211_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2211_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2211_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2211_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2211_ZM_COEFFICIENT_ACQUISITION_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2211_HESSIAN_RANGE_LEMMA_NONCLAIM.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_ZM_OWNER_AUDIT_2211_NONCLAIM.csv",
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


def formalization_has_2211_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2211-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2211*",
        "*P8_Y5_BRR545_2211*",
        "*Y5_R2FR_parent_quadratic_residue_ZM_owner_or_constraint_branch_2211*",
        "*JR2211*",
        "*PARENT_QLOC_ZM_OWNER_AUDIT_2211*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2210_handoff",
            ROOT / "2210-Y5-R2FR-lambda-X-range-owner-or-R10-source-map-first-row.md",
            ["NEXT2210_0_2211", "M_AB v_i^B = mu_i^2 Z_AB", "VAL2210_OVERALL"],
            "2210 selects parent Z_AB/M_AB ownership or constraint demotion.",
        ),
        (
            "2207_response_doublet",
            ROOT / "2207-Y5-R2FR-Gamma-eff-metric-variation-or-first-q-loc-response-operator-row.md",
            ["Gamma_eff = Gamma0 + 1/2 M_AB", "KMR2207_2_Khat_identity", "VAL2207_OVERALL"],
            "2207 gives the response-doublet Hessian candidate but blocks live Khat promotion.",
        ),
        (
            "2110_owner_bundle",
            ROOT / "2110-Y5-R2FR-Gamma-Khat-q_loc-parent-action-owner-or-DqZ-GK-tail-bound.md",
            ["GKO2110_3_Khat_match", "QNR2110_2_Q_cdb", "VAL2110_OVERALL"],
            "2110 shows fixed-L0 algebraic progress but leaves Khat/CDB owner debts.",
        ),
        (
            "2111_khat_match",
            ROOT / "2111-Y5-R2FR-fixed-L0-Khat-metric-response-match-or-Qcdb-bound.md",
            ["KMG2111_8_verdict", "QCB2111_1_Q_cdb", "VAL2111_OVERALL"],
            "older 2111 rejects live Khat=Kmetric promotion and isolates CDB components.",
        ),
        (
            "1010_action_gate",
            ROOT / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
            ["GKT1010_0_variational_route", "GKT1010_2_Helmholtz_integrability", "V1010_SUMMARY"],
            "action/Helmholtz route is a contract, not a signed parent action.",
        ),
        (
            "1011_doublet_source",
            ROOT / "1011-Y5-R10-response-doublet-source-current-zero-or-q_loc-bound-fill.md",
            ["RDT1011_5_positive_operator", "RDT1011_7_verdict", "V1011_SUMMARY"],
            "response-doublet source-current zero theorem remains unclosed.",
        ),
        (
            "562_scalar_mass_gap",
            ROOT / "562-Y5-R10-ZX-lambda-mass-gap-and-bound-curve-fill-or-theorem-zero.md",
            ["PR562_2_canonical_mass_and_range", "E562_3_mass_gap_value", "V562_3_lambda_prefactor_relations_written"],
            "scalar Z_X/M_X^2 relation exists conditionally and values remain missing.",
        ),
        (
            "2210_coefficient_audit",
            OUT / "P8_Y5_PARENT_QLOC_2210_PARENT_COEFFICIENT_AUDIT.csv",
            ["PCA2210_0_Z_AB", "PCA2210_1_M_AB", "MISSING_PARENT_HESSIAN"],
            "machine-readable handoff: both Z_AB and M_AB ownership fail current claim.",
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


def zm_owner_audit_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            audit_id="ZMO2211_0_parent_quadratic_form",
            object="parent local quadratic operator",
            test="Does the parent action supply S2=1/2 int sqrt(g)[G_AB^{ij} grad_i Z^A grad_j Z^B + H_AB Z^A Z^B] plus source terms on the physical quotient?",
            result="CONTRACT_WRITTEN_NOT_SOURCE_SIGNED",
            what_passes="2210 range law identifies the needed principal symbol and Hessian.",
            what_fails="no current source signs G_AB/Z_AB, H_AB/M_AB, domain, or source split for the q_loc branch.",
            repair="extract second variation/principal symbol from parent action or demote finite-range R10",
            passes_now=False,
        ),
        base_row(
            audit_id="ZMO2211_1_M_from_response_doublet",
            object="M_AB algebraic Hessian",
            test="For Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B+O(Z^4), can M_AB be read as the local Hessian H_AB?",
            result="ALGEBRAIC_HESSIAN_CANDIDATE_ONLY",
            what_passes="the response-doublet gives a clean double-zero and a candidate second derivative in Z.",
            what_fails="Gamma_eff is not fully parent-adopted, K_hat is not live-matched, and units/domain/source convention are unsigned.",
            repair="derive H_AB := second_Z Gamma_eff on a parent-owned quotient field basis, with units and sign",
            passes_now=False,
        ),
        base_row(
            audit_id="ZMO2211_2_Z_kinetic_principal_symbol",
            object="Z_AB kinetic/gradient residue",
            test="Does the same parent branch contain a gradient/principal-symbol term that gives -Z_AB Delta in the static operator?",
            result="NOT_FOUND_CURRENT_CLAIM",
            what_passes="none beyond the general range-owner law.",
            what_fails="fixed-L0 response-doublet evidence is algebraic; derivative/connection/domain/boundary terms are unresolved residuals, not a signed kinetic residue.",
            repair="hunt principal symbol in Gamma_eff/Khat/CDB terms; if absent, classify as algebraic constraint/rank-zero branch",
            passes_now=False,
        ),
        base_row(
            audit_id="ZMO2211_3_Khat_metric_response_route",
            object="K_hat as metric response",
            test="Can K_hat=K_metric[Gamma_eff] turn the response-doublet Hessian into a parent operator?",
            result="BLOCKED_BY_DELTA_K_AND_QCDB",
            what_passes="2111 decomposes the Hilbert response and closes algebraic volume/m/L pieces conditionally.",
            what_fails="live Khat, K_conn, K_domain, K_boundary, K_comm and projector/readout leakage remain unsigned.",
            repair="derive CDB zeros/bounds and live Khat component match before using Khat to own Z/M",
            passes_now=False,
        ),
        base_row(
            audit_id="ZMO2211_4_Helmholtz_and_source",
            object="action existence and source-current closure",
            test="Is the stress variational and source-free enough for the quadratic operator to be physical?",
            result="BLOCKED_BY_HELMHOLTZ_AND_SOURCE_CURRENT",
            what_passes="1010/1011 define exact Helmholtz/Euler/source-current tests.",
            what_fails="Helmholtz symmetry, J_Z=0, B_Z=0, Y5/Y6 source silence and PPN lock are not parent-signed.",
            repair="prove action/Helmholtz/source theorem or retain coefficient/source rows",
            passes_now=False,
        ),
        base_row(
            audit_id="ZMO2211_5_verdict",
            object="Z_AB/M_AB ownership",
            test="Can 2211 source-sign a finite-range R10 operator?",
            result="NO_COEFFICIENT_OWNER_SIGNED_FINITE_RANGE_DEMOTED",
            what_passes="M_AB is a useful algebraic Hessian candidate and the required Z/M contract is now exact.",
            what_fails="no kinetic principal symbol or live parent operator is signed, so lambda_i cannot be computed or selected.",
            repair="demote finite-range R10 to coefficient-acquisition; open rank-zero/constraint proof if Z_AB stays absent",
            passes_now=False,
        ),
    ]


def hessian_range_lemma_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            lemma_id="HVR2211_0_hessian_not_range",
            statement="An algebraic Hessian H_AB=M_AB by itself does not define a Yukawa range.",
            proof_sketch="Range comes from the inverse of a differential operator. Without a nonzero principal symbol Z_AB multiplying the spatial Laplacian, the equation is algebraic/constraint-like rather than (-Z Delta+M)Z=J.",
            implication="response-doublet M_AB cannot be used as lambda_X evidence by itself.",
            status="PROVED_AS_GATE_LEMMA",
        ),
        base_row(
            lemma_id="HVR2211_1_finite_range_case",
            statement="If Z_AB is positive on the quotient and M_AB is self-adjoint/positive on the same domain, finite ranges are eigenvalues of M v=mu^2 Z v.",
            proof_sketch="The static Green operator diagonalizes in the generalized eigenbasis, giving kernels exp(-mu_i r)/(4 pi r) with lambda_i=1/mu_i.",
            implication="R10 is allowed only after Z_AB, M_AB, domain and units are parent-owned.",
            status="CONDITIONAL_THEOREM_RESTATED",
        ),
        base_row(
            lemma_id="HVR2211_2_rank_zero_constraint_case",
            statement="If Z_AB has no physical quotient rank, no Yukawa lambda exists.",
            proof_sketch="The local equation reduces to M_AB Z^B=J_A plus constraints/boundary equations; any suppression must come from source-current silence or algebraic elimination, not finite range.",
            implication="this may be a cleaner GR-reduction route than an R10 fifth-force branch, but it must be proved.",
            status="CONSTRAINT_BRANCH_OPENED",
        ),
        base_row(
            lemma_id="HVR2211_3_hidden_derivative_case",
            statement="If derivative/connection/domain terms hide the principal symbol, they must be extracted or bounded before branch selection.",
            proof_sketch="K_conn/K_domain/K_boundary can change the operator order, boundary domain and source map; deleting them would smuggle in the plateau axiom.",
            implication="CDB terms are not nuisance bookkeeping; they decide whether a range exists.",
            status="GUARDRAIL_ACTIVE",
        ),
        base_row(
            lemma_id="HVR2211_4_verdict",
            statement="M_AB is currently an algebraic curvature candidate, not a range owner.",
            proof_sketch="The corpus supplies M_AB-shape evidence but not Z_AB/principal-symbol ownership or live action/Khat matching.",
            implication="finite-range R10 remains nonclaim and coefficient-acquisition; next proof target is Z_AB principal symbol or rank-zero constraint.",
            status="RANGE_NOT_NUMERIC",
        ),
    ]


def coefficient_acquisition_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            coeff_id="ZMC2211_0_Z_AB_principal_symbol",
            symbol="Z_AB",
            definition_needed="coefficient of the static physical quotient principal symbol, L_AB includes -Z_AB Delta",
            current_value="MISSING_PARENT_DERIVED",
            units_needed="operator units matching M_AB so mu^2=M/Z has units length^-2",
            source_required="second variation of parent action including derivative/connection/domain terms",
            blocks="numeric lambda_i;finite-range R10 branch;ghost-free local proof",
            valid_row_now=False,
        ),
        base_row(
            coeff_id="ZMC2211_1_M_AB_Hessian",
            symbol="M_AB",
            definition_needed="second derivative/Hessian of parent scalar density or potential on physical quotient at local fixed point",
            current_value="CANDIDATE_M_AB_FROM_RESPONSE_DOUBLET_NOT_PARENT_SIGNED",
            units_needed="same parent normalization as Z_AB",
            source_required="Gamma_eff parent density adoption plus field basis and sign convention",
            blocks="lambda_i eigenvalues;positive operator no-hair theorem",
            valid_row_now=False,
        ),
        base_row(
            coeff_id="ZMC2211_2_domain_self_adjoint",
            symbol="Dom(L_AB)",
            definition_needed="quotient, boundary and support domain making L_AB self-adjoint",
            current_value="MISSING_DOMAIN_CERTIFICATE",
            units_needed="local norm and measure convention",
            source_required="boundary/no-flux/domain descent theorem or explicit boundary charge row",
            blocks="real spectrum;integration by parts;no hidden source theorem",
            valid_row_now=False,
        ),
        base_row(
            coeff_id="ZMC2211_3_source_current",
            symbol="J_A",
            definition_needed="matter/projector/memory/domain source driving each physical eigenmode",
            current_value="MISSING_SOURCE_SPLIT",
            units_needed="same source normalization as alpha law",
            source_required="Euler/source-current owner theorem or coefficient row",
            blocks="theorem-zero vs nonzero Yukawa branch",
            valid_row_now=False,
        ),
        base_row(
            coeff_id="ZMC2211_4_q_loc_map",
            symbol="S_i[q_loc,T_GK]",
            definition_needed="map from q_loc/T_GK residual to eigenmode source J_i",
            current_value="MISSING_CURRENT_OWNER",
            units_needed="R10/PPN/source-normalization response units",
            source_required="inverse-divergence, tau_i, or T_GK source-current map before readout",
            blocks="alpha(lambda) prediction from q_loc",
            valid_row_now=False,
        ),
    ]


def branch_demoter_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            branch_id_local="RBD2211_0_response_doublet_finite_range",
            old_status="candidate finite-range route",
            new_status="DEMOTED_TO_COEFFICIENT_ACQUISITION",
            reason="M_AB shape exists but Z_AB principal symbol and domain/source owner are missing.",
            next_proof="derive Z_AB from principal symbol or stop treating response-doublet as R10 range owner",
            claim_effect="no R10 score",
        ),
        base_row(
            branch_id_local="RBD2211_1_response_doublet_constraint",
            old_status="held possibility",
            new_status="PROMOTED_TO_NEXT_PROOF_FORK",
            reason="if Z_AB rank is zero/absent, local GR must come from source-current identity or algebraic elimination, not Yukawa suppression.",
            next_proof="prove rank-zero constraint algebra plus J_A/B_A silence",
            claim_effect="could support local-GR route only after source identity closes",
        ),
        base_row(
            branch_id_local="RBD2211_2_CDB_principal_symbol",
            old_status="residual nuisance",
            new_status="OPERATOR_DECISION_COMPONENT",
            reason="K_conn/K_domain/K_boundary may contain or obstruct the kinetic/principal symbol.",
            next_proof="extract derivative order and norm from CDB terms",
            claim_effect="cannot delete CDB by fixed-L0 algebraic closure",
        ),
        base_row(
            branch_id_local="RBD2211_3_massless_or_wrong_sign",
            old_status="unselected",
            new_status="REJECT_OR_ROUTE_TO_PPN_IF_FOUND",
            reason="mu^2<=0 is not a short-range R10 suppression branch.",
            next_proof="positivity/rank certificate",
            claim_effect="local branch unsafe unless gauge/nonphysical or theorem-zero",
        ),
        base_row(
            branch_id_local="RBD2211_4_verdict",
            old_status="finite-range R10 next by default",
            new_status="NO_BRANCH_SELECTED",
            reason="parent coefficients do not choose finite-range, constraint, massless, wrong-sign or spectral branch yet.",
            next_proof="principal-symbol Z_AB owner or rank-zero constraint proof",
            claim_effect="no local-GR/Newton/R10 claim",
        ),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            gate_id="CG2211_0_M_candidate",
            gate="M_AB algebraic Hessian candidate exists",
            status="PASS_NONCLAIM",
            implication="response-doublet gives a useful mass/Hessian target, not a range by itself.",
        ),
        base_row(
            gate_id="CG2211_1_Z_owner",
            gate="Z_AB principal-symbol owner exists",
            status="BLOCKED_NONCLAIM",
            implication="no finite range or ghost-free local operator can be claimed.",
        ),
        base_row(
            gate_id="CG2211_2_Khat_action_owner",
            gate="Gamma_eff/Khat action owner is signed",
            status="BLOCKED_NONCLAIM",
            implication="Delta_K/Q_cdb remain live and can feed q_loc.",
        ),
        base_row(
            gate_id="CG2211_3_constraint_zero",
            gate="rank-zero/source-current constraint route closes",
            status="BLOCKED_NONCLAIM",
            implication="constraint route is promising but J_A/B_A/source silence is not proved.",
        ),
        base_row(
            gate_id="CG2211_4_R10_score",
            gate="R10 alpha(lambda) can be scored",
            status="BLOCKED_NONCLAIM",
            implication="lambda_i, source map, charges and bound curve remain incomplete.",
        ),
        base_row(
            gate_id="CG2211_5_local_GR",
            gate="local GR/Newton reduction can be claimed",
            status="BLOCKED_NONCLAIM",
            implication="operator/source closure is still missing.",
        ),
        base_row(
            gate_id="CG2211_6_GitHub",
            gate="public/github update",
            status="BLOCKED_NONCLAIM",
            implication="private derivation work only; no GitHub action.",
        ),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            decision_id="DEC2211_0_gain",
            decision="HESSIAN_NOT_RANGE_LEMMA_INSTALLED",
            rationale="The response-doublet M_AB can be a Hessian candidate, but range requires a kinetic/principal-symbol residue Z_AB.",
            next_action="stop treating M_AB alone as lambda evidence",
        ),
        base_row(
            decision_id="DEC2211_1_demote",
            decision="FINITE_RANGE_R10_DEMOTED_TO_COEFFICIENT_ACQUISITION",
            rationale="No current parent source signs Z_AB, domain, source split, live Khat match or Helmholtz closure.",
            next_action="fill coefficient rows or prove rank-zero constraint branch",
        ),
        base_row(
            decision_id="DEC2211_2_promising_fork",
            decision="CONSTRAINT_ROUTE_PROMOTED_AS_CLEAN_FORK",
            rationale="If the physical quotient has no propagating Z_AB rank, local GR could come from source-current/algebraic silence rather than fifth-force suppression.",
            next_action="derive principal-symbol rank and source-current identity next",
        ),
        base_row(
            decision_id="DEC2211_3_no_claim",
            decision="NO_R10_LOCAL_GR_CLAIM",
            rationale="2211 is a derivation discipline gain and branch demotion, not empirical success.",
            next_action="keep all rows valid_for_claim=false until branch selection and source map close",
        ),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2211_0_2212",
            selection_status="selected",
            target_file="2212-Y5-R2FR-principal-symbol-ZAB-owner-or-rank-zero-constraint-proof.md",
            target_script="scripts/Y5_R2FR_principal_symbol_ZAB_owner_or_rank_zero_constraint_proof_2212.py",
            objective="extract the principal symbol of the response-doublet/Gamma_eff/Khat/CDB parent branch; either source-sign a physical Z_AB kinetic residue or prove the physical quotient has rank zero and must close through a constraint/source-current identity",
            success_condition="Z_AB owner row becomes source-signed nonclaim, or finite-range R10 is explicitly rejected for this branch and a rank-zero constraint theorem contract is written",
            do_not_do="do not infer kinetic residue from algebraic M_AB; do not delete CDB terms; do not claim R10/local GR; do not use GitHub action",
        ),
        base_row(
            route_id="NEXT2211_1_data_parallel",
            selection_status="held_parallel",
            target_file="2212b-Y5-R2FR-R10-bound-curve-acquisition-only.md",
            target_script="scripts/Y5_R2FR_R10_bound_curve_acquisition_only_2212b.py",
            objective="acquire full R10 alpha_bound(lambda) data independently of theory branch selection",
            success_condition="source-backed dense bound rows remain available but nonclaim until alpha(lambda) is parent-derived",
            do_not_do="do not let external data hide missing theory coefficients",
        ),
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["coefficient_acquisition"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["hessian_range_lemma"], BRANCH_COPIES["branch_wep"]),
        ("beta_docs", OUTPUTS["zm_owner_audit"], BRANCH_COPIES["beta_docs"]),
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
    owner_rows: list[dict[str, Any]],
    lemma_rows: list[dict[str, Any]],
    coeff_rows: list[dict[str, Any]],
    demoter_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(validation_id: str, status: bool, detail: str) -> None:
        rows.append(base_row(validation_id=validation_id, status="PASS" if status else "FAIL", detail=detail))

    add("VAL2211_00_sources_exist", all(truthy(row.get("path_exists")) for row in source_rows), f"{sum(truthy(row.get('path_exists')) for row in source_rows)}/{len(source_rows)} sources exist")
    add("VAL2211_01_needles_found", all(truthy(row.get("needles_found")) for row in source_rows), f"{sum(truthy(row.get('needles_found')) for row in source_rows)}/{len(source_rows)} source needle sets found")

    owner_ok = (
        any(row.get("audit_id") == "ZMO2211_1_M_from_response_doublet" and row.get("result") == "ALGEBRAIC_HESSIAN_CANDIDATE_ONLY" for row in owner_rows)
        and any(row.get("audit_id") == "ZMO2211_2_Z_kinetic_principal_symbol" and row.get("result") == "NOT_FOUND_CURRENT_CLAIM" for row in owner_rows)
        and any(row.get("audit_id") == "ZMO2211_5_verdict" and "DEMOTED" in str(row.get("result")) for row in owner_rows)
    )
    add("VAL2211_02_zm_owner_audit", owner_ok, "M_AB candidate retained, Z_AB owner missing, finite-range branch demoted")

    lemma_ok = any(row.get("lemma_id") == "HVR2211_0_hessian_not_range" and row.get("status") == "PROVED_AS_GATE_LEMMA" for row in lemma_rows)
    lemma_ok = lemma_ok and any(row.get("lemma_id") == "HVR2211_2_rank_zero_constraint_case" for row in lemma_rows)
    add("VAL2211_03_hessian_range_lemma", lemma_ok, "Hessian-not-range and rank-zero constraint cases recorded")

    coeff_ok = len(coeff_rows) == 5 and all(not truthy(row.get("valid_row_now")) for row in coeff_rows)
    add("VAL2211_04_coefficient_rows", coeff_ok, f"coefficient acquisition rows={len(coeff_rows)} all nonclaim")

    demoter_ok = any(row.get("branch_id_local") == "RBD2211_0_response_doublet_finite_range" and "DEMOTED" in str(row.get("new_status")) for row in demoter_rows)
    demoter_ok = demoter_ok and any(row.get("branch_id_local") == "RBD2211_1_response_doublet_constraint" and "PROMOTED" in str(row.get("new_status")) for row in demoter_rows)
    add("VAL2211_05_branch_demoter", demoter_ok, "finite-range response-doublet branch demoted; constraint fork promoted")

    claim_ok = any(row.get("gate_id") == "CG2211_4_R10_score" and row.get("status") == "BLOCKED_NONCLAIM" for row in claim_rows)
    claim_ok = claim_ok and any(row.get("gate_id") == "CG2211_5_local_GR" and row.get("status") == "BLOCKED_NONCLAIM" for row in claim_rows)
    add("VAL2211_06_claim_gate", claim_ok, "R10 and local-GR claims remain blocked")

    decision_ok = any(row.get("decision") == "HESSIAN_NOT_RANGE_LEMMA_INSTALLED" for row in decision_rows_) and any(row.get("decision") == "CONSTRAINT_ROUTE_PROMOTED_AS_CLEAN_FORK" for row in decision_rows_)
    add("VAL2211_07_decision", decision_ok, "decision ledger records real gain and next clean fork")

    next_ok = any(row.get("route_id") == "NEXT2211_0_2212" and "principal symbol" in str(row.get("objective")) for row in next_rows)
    add("VAL2211_08_next_target", next_ok, "2212 principal-symbol Z_AB owner or rank-zero constraint proof selected")

    csv_details: list[str] = []
    csv_ok = True
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        csv_ok = csv_ok and ok
        csv_details.append(f"{path.name}:{count if ok else detail}")
    add("VAL2211_09_csv_parse", csv_ok, "; ".join(csv_details))

    branch_ok = all(truthy(row.get("copied")) and truthy(row.get("parse_ok")) for row in branch_rows)
    add("VAL2211_10_branch_copies", branch_ok, ";".join(str(row.get("target_path")) for row in branch_rows))

    generated_groups = [source_rows, owner_rows, lemma_rows, coeff_rows, demoter_rows, claim_rows, decision_rows_, next_rows, branch_rows]
    flags_false = all(
        not truthy(row.get("valid_for_claim")) and not truthy(row.get("claim_allowed"))
        for group in generated_groups
        for row in group
    )
    add("VAL2211_11_claim_flags_false", flags_false, "all generated rows keep valid_for_claim=false and claim_allowed=false")

    formalization_clean = not formalization_has_2211_artifacts()
    add("VAL2211_12_formalization_clean", formalization_clean, "formalization-workbench has no 2211 artifacts")

    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    add("VAL2211_13_pycache_absent", pycache_absent, str(ROOT / "scripts" / "__pycache__"))

    pass_so_far = all(row.get("status") == "PASS" for row in rows)
    rows.append(
        base_row(
            validation_id="VAL2211_OVERALL",
            status="PASS" if pass_so_far else "FAIL",
            detail="2211 proves M_AB-alone is not a range owner, demotes finite-range R10 to coefficient acquisition, and selects Z_AB principal symbol or rank-zero constraint proof next",
        )
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    owner_rows: list[dict[str, Any]],
    lemma_rows: list[dict[str, Any]],
    coeff_rows: list[dict[str, Any]],
    demoter_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
    validation_rows_: list[dict[str, Any]],
) -> None:
    lines = [
        "# 2211 - Y5/R2FR Parent Quadratic Residue ZM Owner Or Constraint Branch",
        "",
        "## Current Verdict",
        "",
        "2211 rejects a subtle but dangerous shortcut: the response-doublet `M_AB` is not a range owner by itself. It can be a local algebraic Hessian candidate, but a Yukawa range requires a parent principal symbol/kinetic residue `Z_AB` on the same physical quotient domain.",
        "",
        "The useful lemma is:",
        "",
        "`M_AB` alone gives curvature of the algebraic fixed point; `(-Z_AB Delta + M_AB)` gives a finite-range operator.",
        "",
        "Current evidence supplies the first shape condition but not the second. So the finite-range R10 interpretation of the response-doublet branch is demoted to coefficient acquisition. The cleaner next fork is now explicit: either find `Z_AB` in the principal symbol/CDB terms, or prove the physical quotient is rank-zero and close the branch by a constraint/source-current identity rather than by fifth-force suppression.",
        "",
        "## Source Register",
        "",
        md_table(source_rows, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
        "",
        "## ZM Owner Audit",
        "",
        md_table(owner_rows, ["audit_id", "object", "test", "result", "what_passes", "what_fails", "repair", "passes_now", "valid_for_claim"]),
        "",
        "## Hessian Vs Range Lemma",
        "",
        md_table(lemma_rows, ["lemma_id", "statement", "proof_sketch", "implication", "status", "valid_for_claim"]),
        "",
        "## Coefficient Acquisition Rows",
        "",
        md_table(coeff_rows, ["coeff_id", "symbol", "definition_needed", "current_value", "units_needed", "source_required", "blocks", "valid_row_now", "valid_for_claim"]),
        "",
        "## Range Branch Demoter",
        "",
        md_table(demoter_rows, ["branch_id_local", "old_status", "new_status", "reason", "next_proof", "claim_effect", "valid_for_claim"]),
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
        "This is not circling; it is removing a false bridge. If the theory wants a short-range local residual, it must show the kinetic/principal symbol that creates a range. If that symbol is absent, the better route is not to force R10; it is to prove the residual is a constraint/current identity. That is exactly the kind of derivable route that could connect back to GR without post-hoc patching.",
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    remove_pycache()

    source_rows = source_register_rows()
    owner_rows = zm_owner_audit_rows()
    lemma_rows = hessian_range_lemma_rows()
    coeff_rows = coefficient_acquisition_rows()
    demoter_rows = branch_demoter_rows()
    claim_rows = claim_gate_rows()
    decision_rows_ = decision_rows()
    next_rows = next_target_rows()

    for path, rows in [
        (OUTPUTS["source_register"], source_rows),
        (OUTPUTS["zm_owner_audit"], owner_rows),
        (OUTPUTS["hessian_range_lemma"], lemma_rows),
        (OUTPUTS["coefficient_acquisition"], coeff_rows),
        (OUTPUTS["branch_demoter"], demoter_rows),
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
        owner_rows,
        lemma_rows,
        coeff_rows,
        demoter_rows,
        claim_rows,
        decision_rows_,
        next_rows,
        branch_rows,
    )
    write_csv(OUTPUTS["validation"], validation_rows_)

    write_doc(
        source_rows,
        owner_rows,
        lemma_rows,
        coeff_rows,
        demoter_rows,
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
