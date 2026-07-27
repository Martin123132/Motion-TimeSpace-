from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2217"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2217-Y5-R2FR-response-doublet-parent-density-and-Khat-identity-construction.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2217_SOURCE_REGISTER.csv",
    "density_candidate": OUT / "P8_Y5_PARENT_QLOC_2217_RESPONSE_DOUBLET_PARENT_DENSITY_CANDIDATE.csv",
    "metric_variation": OUT / "P8_Y5_PARENT_QLOC_2217_FORMAL_METRIC_VARIATION.csv",
    "identity_comparison": OUT / "P8_Y5_PARENT_QLOC_2217_KHAT_IDENTITY_COMPARISON.csv",
    "mismatch_residual": OUT / "P8_Y5_PARENT_QLOC_2217_KHAT_MISMATCH_RESIDUAL_ROWS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2217_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2217_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2217_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2217_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2217_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2217_KHAT_MISMATCH_RESIDUAL_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2217_DENSITY_KHAT_IDENTITY_NONCLAIM.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_RESPONSE_DOUBLET_DENSITY_2217_NONCLAIM.csv",
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


def formalization_has_2217_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2217-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2217*",
        "*P8_Y5_BRR545_2217*",
        "*Y5_R2FR_response_doublet_parent_density_and_Khat_identity_construction_2217*",
        "*JR2217*",
        "*PARENT_QLOC_RESPONSE_DOUBLET_DENSITY_2217*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2216_handoff",
            ROOT / "2216-Y5-R2FR-parent-Hessian-signature-extraction-or-null-bound-rows.md",
            ["NEXT2216_0_2217", "PHS2216_2_Khat_identity", "VAL2216_OVERALL"],
            "2216 selects response-doublet parent density and Khat identity construction.",
        ),
        (
            "1010_action_guard",
            ROOT / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
            ["GKT1010_0_variational_route", "GKT1010_1_metric_response_identity", "V1010_SUMMARY"],
            "action-existence and metric-response guardrail.",
        ),
        (
            "2207_metric_variation",
            ROOT / "2207-Y5-R2FR-Gamma-eff-metric-variation-or-first-q-loc-response-operator-row.md",
            ["GMV2207_0_response_doublet_setup", "KMR2207_2_Khat_identity", "VAL2207_OVERALL"],
            "formal response-doublet metric variation already written, Khat identity blocked.",
        ),
        (
            "gamma_owner_candidates",
            OUT / "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv",
            ["GO516_A_response_doublet_quadratic_density", "GO516_D_residual_bound_runner", "best_candidate_not_current_MTS_derived"],
            "candidate density routes and residual fallback.",
        ),
        (
            "gk_action_candidates",
            OUT / "P8_GK_STRESS_ACTION_CANDIDATES.csv",
            ["GK514_A_metric_response_scalar_density", "GK514_D_residual_branch", "fallback_required"],
            "candidate parent S_GK action routes.",
        ),
        (
            "gk_metric_contract",
            OUT / "P8_GK_METRIC_RESPONSE_CONTRACT.csv",
            ["MR514_0_scalar_density", "MR514_1_Khat_metric_response", "MR514_5_double_zero"],
            "metric-response pass/fail contract.",
        ),
        (
            "gk_metric_audit",
            OUT / "P8_GK_METRIC_RESPONSE_MATCH_AUDIT.csv",
            ["MA515_0_Gamma_scalar_density_owner", "MA515_1_Khat_metric_response", "MA515_6_units_and_readout"],
            "current source audit: density owner, Khat response and units not found.",
        ),
        (
            "gk_metric_evidence",
            OUT / "P8_GK_METRIC_RESPONSE_SOURCE_EVIDENCE.csv",
            ["E515_4_source_current_audit", "E515_5_current_contract", "promising_template"],
            "evidence map: response-field template is promising but not a match.",
        ),
        (
            "response_doublet_contract",
            OUT / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv",
            ["RD516_1_even_scalar_density", "RD516_2_metric_response", "RD516_4_zero_odd_source"],
            "response-doublet clauses for density, metric response and source zero.",
        ),
        (
            "response_doublet_variation",
            OUT / "P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv",
            ["AV517_1_scalar_density", "AV517_2_first_variation_Z", "AV517_4_Euler_equation"],
            "formal variation rows for response-doublet density.",
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


def density_candidate_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            candidate_id="RDP2217_0_parent_action_ansatz",
            object="response-doublet parent scalar density",
            formula="S_GK[g,Z,R_even,D] = - integral_D sqrt(-g) Gamma_eff, Gamma_eff = Gamma0 + 1/2 M_AB(g,R_even,D,...) Z^A Z^B + O(Z^4)",
            constructed_piece="formal local scalar-density ansatz copied from GO516_A/AV517_1",
            missing_piece="source-owned field content, units, boundary convention, domain D and parent adoption",
            status="CONSTRUCTED_AS_CANDIDATE_NOT_PARENT_SIGNED",
            promotes_parent_density=False,
        ),
        base_row(
            candidate_id="RDP2217_1_exchange_evenness",
            object="exchange-even density",
            formula="E: Z^A -> -Z^A, R_even^A -> R_even^A, so Gamma_eff-Gamma0 is even in Z",
            constructed_piece="evenness implies no linear Z term in the candidate density",
            missing_piece="exchange symmetry is not shown to be a parent symmetry for every physical local residual component",
            status="CONDITIONAL_EVENNESS_ONLY",
            promotes_parent_density=False,
        ),
        base_row(
            candidate_id="RDP2217_2_fixed_point_subtraction",
            object="background subtraction",
            formula="Gamma0 is constant/background-subtracted so nabla^nu Gamma0 does not source q_loc",
            constructed_piece="subtraction rule can be stated for a local fixed point",
            missing_piece="EH/Lambda/background compatibility and boundary/readout convention are not parent-signed",
            status="CONDITIONAL_BACKGROUND_SUBTRACTION",
            promotes_parent_density=False,
        ),
        base_row(
            candidate_id="RDP2217_3_Hessian_owner",
            object="candidate Hessian",
            formula="H_AB := partial_A partial_B Gamma_eff|_{Z=0} = M_AB if units/basis/domain are owned",
            constructed_piece="formal Hessian extraction is immediate from the ansatz",
            missing_piece="Z basis, pairing, units, self-adjoint domain and rank/sign theorem",
            status="FORMAL_HESSIAN_NOT_PARENT_LOCK",
            promotes_parent_density=False,
        ),
        base_row(
            candidate_id="RDP2217_4_density_verdict",
            object="density construction verdict",
            formula="response-doublet density can be written, but current corpus does not adopt it as the MTS parent density",
            constructed_piece="candidate is now explicit and reusable",
            missing_piece="actual parent action signature and Khat match",
            status="CANDIDATE_WRITTEN_PROMOTION_BLOCKED",
            promotes_parent_density=False,
        ),
    ]


def metric_variation_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            variation_id="FMV2217_0_definition",
            object="metric response definition",
            formula="K_metric^{mu nu} := 2/sqrt(-g) delta(sqrt(-g) Gamma_eff)/delta g_{mu nu} minus declared volume/sign convention",
            derivation_piece="defines the only legal object that can be identified with K_hat",
            unresolved_piece="sign convention, volume subtraction and derivative/boundary accounting",
            status="FORMAL_DEFINITION_WRITTEN",
            parent_signed=False,
        ),
        base_row(
            variation_id="FMV2217_1_algebraic_response",
            object="non-derivative M_AB dependence",
            formula="K_metric^{mu nu} includes volume term plus 1/2 (delta_g M_AB) Z^A Z^B + M_AB Z^A delta_g Z^B",
            derivation_piece="at Z=0 this part is double-zero after Gamma0 subtraction if delta_g Z is regular",
            unresolved_piece="existing K_hat has not been shown to contain exactly these terms",
            status="FORMAL_DOUBLE_ZERO_CANDIDATE",
            parent_signed=False,
        ),
        base_row(
            variation_id="FMV2217_2_derivative_boundary_terms",
            object="derivative/boundary response",
            formula="if M_AB or Z depends on nabla fields, K_metric also contains integration-by-parts, symplectic and boundary terms",
            derivation_piece="these terms must be included before comparing to K_hat",
            unresolved_piece="corpus keeps boundary/projector/domain terms live",
            status="BOUNDARY_TERMS_UNEXTRACTED",
            parent_signed=False,
        ),
        base_row(
            variation_id="FMV2217_3_Ward_residual",
            object="q_loc Ward expression",
            formula="q_loc^nu = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu}); if K_hat=K_metric then this is controlled by Euler/boundary residuals",
            derivation_piece="action route would make q_loc a Ward/Euler residual",
            unresolved_piece="Khat identity, Helmholtz, Euler closure, P_loc and boundary no-flux are unsigned",
            status="WARD_ROUTE_CONDITIONAL",
            parent_signed=False,
        ),
        base_row(
            variation_id="FMV2217_4_verdict",
            object="formal metric variation verdict",
            formula="K_metric can be written for the candidate density, but it cannot be identified with current K_hat from existing sources",
            derivation_piece="formal construction successful",
            unresolved_piece="source-backed tensor equality to K_hat missing",
            status="FORMAL_VARIATION_WRITTEN_IDENTITY_BLOCKED",
            parent_signed=False,
        ),
    ]


def identity_comparison_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            comparison_id="KIC2217_0_scalar_density_owner",
            requirement="Gamma_eff accepted as parent scalar density",
            current_evidence="MA515_0 fail; GKT1010_0 candidate_contract_not_claim",
            comparison_result="FAIL_CURRENT_CLAIM",
            mismatch="Gamma_eff appears as route/readout/relaxation symbol, not owned density with units",
            repair="write parent action density with field content and metric dependence",
            identity_pass_now=False,
        ),
        base_row(
            comparison_id="KIC2217_1_tensor_equality",
            requirement="K_hat^{mu nu}=K_metric^{mu nu}[Gamma_eff]",
            current_evidence="MA515_1 fail; KMR2207_2 blocked; CG1010_1 false",
            comparison_result="FAIL_CURRENT_CLAIM",
            mismatch="no source derives existing K_hat from metric variation under same convention",
            repair="compare explicit tensor terms: volume, delta M_AB, delta Z, derivative, boundary",
            identity_pass_now=False,
        ),
        base_row(
            comparison_id="KIC2217_2_units_and_convention",
            requirement="Gamma_eff/K_hat stress-density units and sign/volume convention fixed",
            current_evidence="MA515_6 fail; 2216 NBR2216_3 missing pairing/units",
            comparison_result="FAIL_CURRENT_CLAIM",
            mismatch="unit-normalized stress/readout map missing",
            repair="declare dimensions and normalization for Gamma_eff, K_hat, Z, M and q_loc",
            identity_pass_now=False,
        ),
        base_row(
            comparison_id="KIC2217_3_boundary_derivative_terms",
            requirement="derivative/boundary pieces of K_metric match K_hat or are zero/bounded",
            current_evidence="MR514_1 requires boundary terms; RD516_6 open; 2216 keeps domain open",
            comparison_result="FAIL_CURRENT_CLAIM",
            mismatch="boundary/projector/domain pieces remain live and can alter q_loc",
            repair="extract derivative order and boundary primitive or keep mismatch residual rows",
            identity_pass_now=False,
        ),
        base_row(
            comparison_id="KIC2217_4_Helmholtz_integrability",
            requirement="proposed stress is variational with symmetric second variation",
            current_evidence="GKT1010_2 not_checked_current_claim; GK513_1 not_checked",
            comparison_result="NOT_CHECKED_BLOCKS_PROMOTION",
            mismatch="even if a tensor is written, integrability is not certified",
            repair="compute Helmholtz symmetry for proposed K_metric/Khat stress",
            identity_pass_now=False,
        ),
        base_row(
            comparison_id="KIC2217_5_Euler_source_closure",
            requirement="Euler equations plus source/boundary zero close q_loc",
            current_evidence="GKT1010_3/GKT1010_4 not matched; AV517_4 blocked_by_source_current_rows",
            comparison_result="FAIL_CURRENT_CLAIM",
            mismatch="source-current and boundary work can drive q_loc even after formal density",
            repair="derive J_A=B_A=0 or retain source/boundary coefficients",
            identity_pass_now=False,
        ),
        base_row(
            comparison_id="KIC2217_6_verdict",
            requirement="full Khat identity",
            current_evidence="combined 2217 comparison",
            comparison_result="IDENTITY_NOT_PARENT_SIGNED",
            mismatch="candidate density construction is not enough to identify current K_hat",
            repair="carry Delta_Khat residual and target explicit tensor comparison next",
            identity_pass_now=False,
        ),
    ]


def mismatch_residual_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            residual_id="DK2217_0_density_owner_gap",
            residual_symbol="Delta_density",
            definition="accepted_parent_Gamma_eff - candidate_response_doublet_Gamma_eff",
            source_evidence="MA515_0;GKT1010_0;PHS2216_1",
            physical_effect="without density owner, M_AB is not a parent Hessian and q_loc Ward route is not active",
            required_to_close="explicit parent scalar density or formal candidate demoted permanently",
            score_ready=False,
            valid_prediction_row=False,
        ),
        base_row(
            residual_id="DK2217_1_Khat_tensor_gap",
            residual_symbol="Delta_Khat^{mu nu}",
            definition="K_hat^{mu nu} - K_metric^{mu nu}[Gamma_eff_candidate]",
            source_evidence="MA515_1;KMR2207_2;CG1010_1",
            physical_effect="enters q_loc through -P_loc nabla_mu Delta_Khat^{mu nu}",
            required_to_close="source-backed tensor comparison including sign, volume, derivative and boundary terms",
            score_ready=False,
            valid_prediction_row=False,
        ),
        base_row(
            residual_id="DK2217_2_units_gap",
            residual_symbol="Delta_units",
            definition="missing normalization map for Gamma_eff, K_hat, M_AB, Z and q_loc",
            source_evidence="MA515_6;NBR2216_3",
            physical_effect="blocks conversion to Newton/PPN/R10/WEP/clock/orbital units",
            required_to_close="declare units and pairing or emit arena coefficient rows",
            score_ready=False,
            valid_prediction_row=False,
        ),
        base_row(
            residual_id="DK2217_3_boundary_gap",
            residual_symbol="Delta_boundary^{mu nu}",
            definition="unmatched derivative, integration-by-parts, domain, projector and boundary terms in metric variation",
            source_evidence="MR514_1;RD516_6;PHS2216_5",
            physical_effect="can feed local force/mass flux even if bulk double-zero holds",
            required_to_close="boundary primitive/no-flux theorem or finite edge coefficient rows",
            score_ready=False,
            valid_prediction_row=False,
        ),
        base_row(
            residual_id="DK2217_4_Helmholtz_gap",
            residual_symbol="H_GK",
            definition="antisymmetric second-variation obstruction for proposed stress",
            source_evidence="GKT1010_2;GK513_1",
            physical_effect="if nonzero, no parent action exists for the claimed Khat stress",
            required_to_close="Helmholtz integrability calculation",
            score_ready=False,
            valid_prediction_row=False,
        ),
        base_row(
            residual_id="DK2217_5_source_boundary_gap",
            residual_symbol="J_GK+B_GK",
            definition="source-current and boundary forcing left after candidate density variation",
            source_evidence="AV517_4;RD516_4;GKT1010_5",
            physical_effect="keeps q_loc/local-GR/Newton blocked even if Khat identity later closes",
            required_to_close="J_A=B_A=0 theorem or finite source/bound rows",
            score_ready=False,
            valid_prediction_row=False,
        ),
        base_row(
            residual_id="DK2217_6_verdict",
            residual_symbol="Delta_Khat_total",
            definition="all unmatched density, tensor, unit, boundary, Helmholtz and source terms",
            source_evidence="2217 combined comparison",
            physical_effect="official residual obstruction to parent-Hessian promotion",
            required_to_close="2218 tensor comparison or residual coefficient acquisition",
            score_ready=False,
            valid_prediction_row=False,
        ),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            gate_id="CG2217_0_candidate_density",
            gate="response-doublet density candidate written",
            status="PASS_NONCLAIM",
            reason="S_GK and Gamma_eff candidate are explicit, but not parent-adopted.",
        ),
        base_row(
            gate_id="CG2217_1_formal_variation",
            gate="formal K_metric variation written",
            status="PASS_NONCLAIM",
            reason="K_metric structure is stated with algebraic and boundary/derivative pieces.",
        ),
        base_row(
            gate_id="CG2217_2_Khat_identity",
            gate="K_hat equals K_metric[Gamma_eff]",
            status="BLOCKED_NONCLAIM",
            reason="no source-backed tensor equality, units or boundary convention exists.",
        ),
        base_row(
            gate_id="CG2217_3_parent_Hessian",
            gate="M_AB parent Hessian promoted",
            status="BLOCKED_NONCLAIM",
            reason="density owner and Khat identity are not signed.",
        ),
        base_row(
            gate_id="CG2217_4_local_GR_Newton",
            gate="local GR/Newton reduction claim",
            status="BLOCKED_NONCLAIM",
            reason="Khat mismatch, Helmholtz, source and boundary gaps remain live.",
        ),
        base_row(
            gate_id="CG2217_5_GitHub",
            gate="GitHub/public update",
            status="BLOCKED_NONCLAIM",
            reason="private derivation checkpoint only.",
        ),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            decision_id="DEC2217_0_gain",
            decision="RESPONSE_DOUBLET_DENSITY_CANDIDATE_CONSTRUCTED",
            rationale="the candidate parent density is now explicit enough to audit rather than hand-wave.",
            next_action="use it as the object for tensor comparison, not as a claimed parent action.",
        ),
        base_row(
            decision_id="DEC2217_1_failure",
            decision="KHAT_IDENTITY_NOT_SIGNED",
            rationale="formal K_metric can be written, but current K_hat has no source-backed equality to it.",
            next_action="carry Delta_Khat residual rows.",
        ),
        base_row(
            decision_id="DEC2217_2_next",
            decision="TENSOR_COMPARISON_AND_HELMHOLTZ_NEXT",
            rationale="the next non-circular step is explicit term-by-term tensor matching and integrability, not more symbol relabeling.",
            next_action="2218 should build K_metric component table versus all known K_hat/Khat appearances and Helmholtz symmetry gates.",
        ),
        base_row(
            decision_id="DEC2217_3_scope",
            decision="NO_PARENT_LOCK_PROMOTION",
            rationale="density candidate plus formal variation still fails parent identity and local claims.",
            next_action="keep M^+/null branch and Delta_Khat residual active.",
        ),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2217_0_2218",
            selection_status="selected",
            target_file="2218-Y5-R2FR-Kmetric-vs-Khat-tensor-comparison-and-Helmholtz-gate.md",
            target_script="scripts/Y5_R2FR_Kmetric_vs_Khat_tensor_comparison_and_Helmholtz_gate_2218.py",
            objective="build a component table for K_metric[Gamma_eff_candidate] versus every sourced K_hat/Khat definition or appearance, including volume, delta M_AB, delta Z, derivative/boundary terms, sign convention and Helmholtz symmetry.",
            success_condition="one tensor component match becomes source-signed or Delta_Khat residual components become explicit acquisition rows.",
            do_not_do="do not assume identity by notation, do not claim local GR/Newton, do not use GitHub.",
        ),
        base_row(
            route_id="NEXT2217_1_units_parallel",
            selection_status="held_parallel",
            target_file="2218b-Y5-R2FR-Gamma-Khat-Z-M-units-and-pairing-normalization.md",
            target_script="scripts/Y5_R2FR_Gamma_Khat_Z_M_units_and_pairing_normalization_2218b.py",
            objective="derive units and pairing for Gamma_eff, K_hat, Z, M_AB, source S_A and q_loc.",
            success_condition="unit-normalized rows can be checked dimensionally or remain explicit blockers.",
            do_not_do="do not compute scores from dimensionless placeholders.",
        ),
        base_row(
            route_id="NEXT2217_2_source_parallel",
            selection_status="held_parallel",
            target_file="2218c-Y5-R2FR-response-doublet-source-boundary-zero-or-coefficients.md",
            target_script="scripts/Y5_R2FR_response_doublet_source_boundary_zero_or_coefficients_2218c.py",
            objective="derive J_A=B_A=0 for the response-doublet sector or emit finite source/boundary coefficient rows.",
            success_condition="source/boundary theorem-zero or coefficient rows become source-backed.",
            do_not_do="do not use double-zero of Gamma alone as source-current zero.",
        ),
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["mismatch_residual"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["identity_comparison"], BRANCH_COPIES["branch_wep"]),
        ("beta_docs", OUTPUTS["density_candidate"], BRANCH_COPIES["beta_docs"]),
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
    density_rows: list[dict[str, Any]],
    variation_rows: list[dict[str, Any]],
    comparison_rows: list[dict[str, Any]],
    residual_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(validation_id: str, status: bool, detail: str) -> None:
        rows.append(base_row(validation_id=validation_id, status="PASS" if status else "FAIL", detail=detail))

    add("VAL2217_00_sources_exist", all(truthy(row.get("path_exists")) for row in source_rows), f"{sum(truthy(row.get('path_exists')) for row in source_rows)}/{len(source_rows)} sources exist")
    add("VAL2217_01_needles_found", all(truthy(row.get("needles_found")) for row in source_rows), f"{sum(truthy(row.get('needles_found')) for row in source_rows)}/{len(source_rows)} source needle sets found")

    density_ok = any(row.get("candidate_id") == "RDP2217_0_parent_action_ansatz" and "Gamma_eff" in str(row.get("formula")) for row in density_rows)
    density_ok = density_ok and any(row.get("candidate_id") == "RDP2217_4_density_verdict" and row.get("status") == "CANDIDATE_WRITTEN_PROMOTION_BLOCKED" for row in density_rows)
    density_ok = density_ok and all(not truthy(row.get("promotes_parent_density")) for row in density_rows)
    add("VAL2217_02_density_candidate", density_ok, "response-doublet density candidate written but not promoted")

    variation_ok = any(row.get("variation_id") == "FMV2217_0_definition" and "K_metric" in str(row.get("formula")) for row in variation_rows)
    variation_ok = variation_ok and any(row.get("variation_id") == "FMV2217_4_verdict" and row.get("status") == "FORMAL_VARIATION_WRITTEN_IDENTITY_BLOCKED" for row in variation_rows)
    variation_ok = variation_ok and all(not truthy(row.get("parent_signed")) for row in variation_rows)
    add("VAL2217_03_metric_variation", variation_ok, "formal K_metric variation written and identity blocked")

    comparison_ok = any(row.get("comparison_id") == "KIC2217_6_verdict" and row.get("comparison_result") == "IDENTITY_NOT_PARENT_SIGNED" for row in comparison_rows)
    comparison_ok = comparison_ok and all(not truthy(row.get("identity_pass_now")) for row in comparison_rows)
    add("VAL2217_04_identity_comparison", comparison_ok, "Khat identity comparison refuses promotion")

    residual_ok = len(residual_rows) == 7
    residual_ok = residual_ok and any(row.get("residual_id") == "DK2217_1_Khat_tensor_gap" and "Delta_Khat" in str(row.get("residual_symbol")) for row in residual_rows)
    residual_ok = residual_ok and all(not truthy(row.get("score_ready")) and not truthy(row.get("valid_prediction_row")) for row in residual_rows)
    add("VAL2217_05_mismatch_residual", residual_ok, "Delta_Khat residual rows staged and non-score-ready")

    claim_ok = any(row.get("gate_id") == "CG2217_2_Khat_identity" and row.get("status") == "BLOCKED_NONCLAIM" for row in claim_rows)
    claim_ok = claim_ok and any(row.get("gate_id") == "CG2217_4_local_GR_Newton" and row.get("status") == "BLOCKED_NONCLAIM" for row in claim_rows)
    add("VAL2217_06_claim_gate", claim_ok, "Khat identity and local-GR/Newton claims remain blocked")

    decision_ok = any(row.get("decision") == "TENSOR_COMPARISON_AND_HELMHOLTZ_NEXT" for row in decision_rows_)
    add("VAL2217_07_decision", decision_ok, "decision ledger selects tensor comparison and Helmholtz gate next")

    next_ok = any(row.get("route_id") == "NEXT2217_0_2218" and "Kmetric" in str(row.get("target_file")) for row in next_rows)
    add("VAL2217_08_next_target", next_ok, "2218 Kmetric-vs-Khat tensor comparison selected")

    csv_details: list[str] = []
    csv_ok = True
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        csv_ok = csv_ok and ok
        csv_details.append(f"{path.name}:{count if ok else detail}")
    add("VAL2217_09_csv_parse", csv_ok, "; ".join(csv_details))

    branch_ok = all(truthy(row.get("copied")) and truthy(row.get("parse_ok")) for row in copy_rows)
    add("VAL2217_10_branch_copies", branch_ok, ";".join(str(row.get("target_path")) for row in copy_rows))

    generated_groups = [source_rows, density_rows, variation_rows, comparison_rows, residual_rows, claim_rows, decision_rows_, next_rows, copy_rows]
    flags_false = all(
        not truthy(row.get("valid_for_claim")) and not truthy(row.get("claim_allowed"))
        for group in generated_groups
        for row in group
    )
    add("VAL2217_11_claim_flags_false", flags_false, "all generated rows keep valid_for_claim=false and claim_allowed=false")

    no_missing_promoted = all(not truthy(row.get("score_ready")) and not truthy(row.get("valid_prediction_row")) for row in residual_rows)
    add("VAL2217_12_missing_not_promoted", no_missing_promoted, "mismatch residual rows are not promoted to score-ready")

    formalization_clean = not formalization_has_2217_artifacts()
    add("VAL2217_13_formalization_clean", formalization_clean, "formalization-workbench has no 2217 artifacts")

    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    add("VAL2217_14_pycache_absent", pycache_absent, str(ROOT / "scripts" / "__pycache__"))

    pass_so_far = all(row.get("status") == "PASS" for row in rows)
    rows.append(
        base_row(
            validation_id="VAL2217_OVERALL",
            status="PASS" if pass_so_far else "FAIL",
            detail="2217 constructs the response-doublet density candidate, writes formal K_metric variation, refuses Khat identity promotion, emits Delta_Khat residual rows, and selects tensor comparison/Helmholtz next",
        )
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    density_rows: list[dict[str, Any]],
    variation_rows: list[dict[str, Any]],
    comparison_rows: list[dict[str, Any]],
    residual_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
    validation_rows_: list[dict[str, Any]],
) -> None:
    lines = [
        "# 2217 - Y5/R2FR Response-Doublet Parent Density And Khat Identity Construction",
        "",
        "## Current Verdict",
        "",
        "2217 successfully writes the response-doublet parent-density candidate as an explicit object:",
        "",
        "`S_GK = - integral_D sqrt(-g) Gamma_eff`, with `Gamma_eff = Gamma0 + 1/2 M_AB Z^A Z^B + O(Z^4)`.",
        "",
        "It also writes the only legal identity target:",
        "",
        "`K_metric^{mu nu} := 2/sqrt(-g) delta(sqrt(-g) Gamma_eff)/delta g_{mu nu}` up to the declared volume/sign convention.",
        "",
        "But current MTS still does not source-sign `K_hat = K_metric[Gamma_eff]`. So 2217 does not promote the parent Hessian route. It stages `Delta_Khat^{mu nu}=K_hat^{mu nu}-K_metric^{mu nu}` as the next official obstruction.",
        "",
        "## Source Register",
        "",
        md_table(source_rows, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
        "",
        "## Response-Doublet Parent Density Candidate",
        "",
        md_table(density_rows, ["candidate_id", "object", "formula", "constructed_piece", "missing_piece", "status", "promotes_parent_density", "valid_for_claim"]),
        "",
        "## Formal Metric Variation",
        "",
        md_table(variation_rows, ["variation_id", "object", "formula", "derivation_piece", "unresolved_piece", "status", "parent_signed", "valid_for_claim"]),
        "",
        "## Khat Identity Comparison",
        "",
        md_table(comparison_rows, ["comparison_id", "requirement", "current_evidence", "comparison_result", "mismatch", "repair", "identity_pass_now", "valid_for_claim"]),
        "",
        "## Khat Mismatch Residual Rows",
        "",
        md_table(residual_rows, ["residual_id", "residual_symbol", "definition", "source_evidence", "physical_effect", "required_to_close", "score_ready", "valid_prediction_row", "valid_for_claim"]),
        "",
        "## Claim Gate",
        "",
        md_table(claim_rows, ["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"]),
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
        md_table(copy_rows, ["copy_id", "source_path", "target_path", "copied", "parse_ok", "row_count", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(validation_rows_, ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"]),
        "",
        "## Working Interpretation",
        "",
        "This is useful. We did not prove the identity, but we stopped treating it as a vibe. There is now a concrete object to compare term-by-term. The next move is therefore surgical: build the `K_metric` component table and see whether any sourced `K_hat` term actually matches it. If not, `Delta_Khat` becomes the local residual owner.",
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    remove_pycache()

    source_rows = source_register_rows()
    density_rows = density_candidate_rows()
    variation_rows = metric_variation_rows()
    comparison_rows = identity_comparison_rows()
    residual_rows = mismatch_residual_rows()
    claim_rows = claim_gate_rows()
    decision_rows_ = decision_rows()
    next_rows = next_target_rows()

    for path, rows in [
        (OUTPUTS["source_register"], source_rows),
        (OUTPUTS["density_candidate"], density_rows),
        (OUTPUTS["metric_variation"], variation_rows),
        (OUTPUTS["identity_comparison"], comparison_rows),
        (OUTPUTS["mismatch_residual"], residual_rows),
        (OUTPUTS["claim_gate"], claim_rows),
        (OUTPUTS["decision"], decision_rows_),
        (OUTPUTS["next_target"], next_rows),
    ]:
        write_csv(path, rows)

    copy_rows = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], copy_rows)

    remove_pycache()
    validation_rows_ = validation_rows(
        source_rows,
        density_rows,
        variation_rows,
        comparison_rows,
        residual_rows,
        claim_rows,
        decision_rows_,
        next_rows,
        copy_rows,
    )
    write_csv(OUTPUTS["validation"], validation_rows_)

    write_doc(
        source_rows,
        density_rows,
        variation_rows,
        comparison_rows,
        residual_rows,
        claim_rows,
        decision_rows_,
        next_rows,
        copy_rows,
        validation_rows_,
    )

    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
