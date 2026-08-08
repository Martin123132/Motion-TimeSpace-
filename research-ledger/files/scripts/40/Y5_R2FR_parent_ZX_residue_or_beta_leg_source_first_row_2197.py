from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2197"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2197-Y5-R2FR-parent-ZX-residue-or-beta-leg-source-first-row.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2197_SOURCE_REGISTER.csv",
    "residue_owner_contract": OUT / "P8_Y5_PARENT_QLOC_2197_ZX_RESIDUE_OWNER_CONTRACT.csv",
    "residue_derivation_gate": OUT / "P8_Y5_PARENT_QLOC_2197_ZX_DERIVATION_GATE.csv",
    "rescaling_invariant_ledger": OUT / "P8_Y5_PARENT_QLOC_2197_RESCALING_INVARIANT_LEDGER.csv",
    "zx_acquisition_row": OUT / "P8_Y5_PARENT_QLOC_2197_ZX_SOURCE_ACQUISITION_ROW.csv",
    "beta_leg_fallback_row": OUT / "P8_Y5_PARENT_QLOC_2197_BETA_LEG_SOURCE_FIRST_ROW.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2197_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2197_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2197_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2197_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2197_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2197_ZX_OWNER_BLOCK_AND_BETA_LEG_NEXT_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2197_BETA_LEG_SOURCE_FIRST_ROW_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "PARENT_QLOC_ZX_RESIDUE_OWNER_CONTRACT_2197_NONCLAIM.csv",
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


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


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
        values = []
        for column in columns:
            values.append(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|"))
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def formalization_has_2197_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2197-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2197*",
        "*P8_Y5_BRR545_2197*",
        "*Y5_R2FR_parent_ZX_residue_or_beta_leg_source_first_row_2197*",
        "*JR2197*",
        "*PARENT_QLOC_ZX_RESIDUE_OWNER_CONTRACT_2197*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2196_doc",
            ROOT / "2196-Y5-R2FR-KX-normalization-or-beta-leg-source-first-row.md",
            ["Best next attack: derive/source `Z_X`", "K_X^R10(lambda)=s_X*F_ST(lambda)*Pi_R10(lambda)/(4*pi*G_N*Z_X)", "VAL2196_OVERALL"],
            "2196 selects Z_X as the denominator/sign/unit bottleneck for K_X.",
        ),
        (
            "2196_factor_status",
            OUT / "P8_Y5_PARENT_QLOC_2196_KX_FACTOR_STATUS.csv",
            ["KXF2196_0_ZX_residue", "MISSING_PARENT_KINETIC_RESIDUE", "SYMBOLIC_CONTRACT_NOT_NUMERIC"],
            "Machine-readable current Z_X/K_X block.",
        ),
        (
            "2156_hessian_doc",
            ROOT / "2156-Y5-R2FR-parent-Xhat-owner-and-Hessian-ZX-MX2-range-or-alpha-source-row.md",
            ["Z_X>0", "MISSING_PARENT_HESSIAN_SIGN", "Next target is parent metric/eigenvalue"],
            "Latest active-branch parent Xhat/Hessian audit.",
        ),
        (
            "2156_hessian_audit",
            OUT / "P8_Y5_PARENT_QLOC_2156_PARENT_HESSIAN_AUDIT.csv",
            ["PHA2156_1_ZX_positive", "MISSING_PARENT_HESSIAN_SIGN", "PHA2156_8_verdict"],
            "Machine-readable Hessian sign and ownership failure.",
        ),
        (
            "2157_metric_doc",
            ROOT / "2157-Y5-R2FR-parent-metric-ZXfX2-beta-eigenvalue-or-source-zero-return.md",
            ["Z_X f_X^2=rho_vac^(1/2)", "FINITE_ROUTE_FROZEN_NONCLAIM", "source-zero/bounded coupling"],
            "Metric/eigenvalue route sharpened then frozen.",
        ),
        (
            "2157_source_zero",
            OUT / "P8_Y5_PARENT_QLOC_2157_SOURCE_ZERO_RETURN.csv",
            ["SZR2157_1_qbarXT_JX_zero", "STILL_STRONGEST_IF_PARENT_SIGNED", "SOURCE_ZERO_OR_BOUNDED_COUPLING_SELECTED"],
            "Fallback route after finite metric/eigenvalue route fails.",
        ),
        (
            "2106_hessian_doc",
            ROOT / "2106-Y5-R2FR-ZX-MX2-parent-Hessian-source-row-or-no-pole-return.md",
            ["NO_CLAIM_GRADE_ZX_MX2_SOURCE_ROW_FOUND", "Z_X/M_X^2", "VAL2106_OVERALL"],
            "Earlier consolidated Hessian source-row failure.",
        ),
        (
            "1854_extraction_doc",
            ROOT / "1854-Y5-R2FR-parent-Hessian-input-extraction-for-ZX-MX2.md",
            ["NO_CLAIM_GRADE_ZX_OR_MX2_FOUND", "Z_X is parent-owned and positive", "VAL1854_OVERALL"],
            "Corpus extraction found formulae but not parent-owned coefficients.",
        ),
        (
            "2023_schema",
            OUT / "P8_Y5_PARENT_QLOC_2023_ZX_MX2_FIRST_ROW_SCHEMA.csv",
            ["ZMR2023_3_ZX", "MISSING_ZX_VALUE_OR_SIGN_THEOREM", "ZMR2023_10_acceptance"],
            "Active coefficient-row schema for the fallback finite branch.",
        ),
        (
            "1036_parent_action_audit",
            OUT / "P8_Y5_R10_1036_PARENT_X_ACTION_AUDIT.csv",
            ["PX1036_1_quadratic_residue", "MISSING_PARENT_KINETIC_RESIDUE", "FAIL_CURRENT_CLAIM_PARENT_ROW_NOT_OWNED"],
            "R10 predecessor says the parent finite-X row is not owned.",
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


def residue_owner_contract_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            contract_id="ZOC2197_0_field_coordinate",
            object="Xhat",
            required_statement="one parent branch declares the physical finite local response coordinate before readout",
            mathematical_role="Z_X is meaningless unless it is the residue of the same Xhat used in beta_s, beta_t, lambda_X and K_X",
            current_status="MISSING_PARENT_X_VARIABLE",
            missing_for_claim="field owner, normalization, allowed redefinitions, source path",
        ),
        base_row(
            contract_id="ZOC2197_1_second_variation",
            object="Z_X",
            required_statement="Z_X = coefficient of h^{ij} partial_i Xhat partial_j Xhat in delta^2 S_parent around the local GR/Newton branch",
            mathematical_role="kinetic/gradient residue that sets the Green-kernel denominator and ghost/elliptic sign",
            current_status="MISSING_PARENT_KINETIC_RESIDUE",
            missing_for_claim="explicit parent Lagrangian, gauge fixing, second variation, units and sign convention",
        ),
        base_row(
            contract_id="ZOC2197_2_schur_complement",
            object="Z_X^eff",
            required_statement="mixed metric, trace, projector, boundary and matter Hessian blocks vanish or are integrated into a positive Schur complement",
            mathematical_role="prevents a one-scalar residue from hiding coupled residual channels",
            current_status="MISSING_BLOCK_DIAGONAL_OR_SCHUR_PROOF",
            missing_for_claim="cross-Hessian matrix and positive orthogonal block theorem",
        ),
        base_row(
            contract_id="ZOC2197_3_metric_lock",
            object="G_X or Z_X f_X^2",
            required_statement="field-space metric/amplitude lock is parent-owned, e.g. the invariant X-direction norm is fixed before local tests",
            mathematical_role="removes the field-rescaling degeneracy that otherwise makes raw Z_X arbitrary",
            current_status="CLEAN_CONTRACT_NOT_SIGNED",
            missing_for_claim="parent M_AB, e_X, f_X, Ward/metric theorem, stress/Bianchi variation",
        ),
        base_row(
            contract_id="ZOC2197_4_source_same_branch",
            object="J_X, beta_s, beta_t",
            required_statement="source/test couplings are varied in the same Xhat normalization as Z_X",
            mathematical_role="ties amplitude, range and matter response so alpha cannot be chosen after the fact",
            current_status="MISSING_SOURCE_ZERO_OR_BETA_SPLIT",
            missing_for_claim="J_X law or source-zero theorem, beta source/test row, no-marker/tail silence",
        ),
        base_row(
            contract_id="ZOC2197_5_verdict",
            object="parent Z_X ownership",
            required_statement="all ZOC2197_0 through ZOC2197_4 close from one parent branch",
            mathematical_role="would make K_X normalization physically meaningful",
            current_status="FAIL_CURRENT_CLAIM_ZX_OWNER_UNSIGNED",
            missing_for_claim="same-branch parent action residue, Schur complement, metric lock, source law and boundary/tail policy",
        ),
    ]


def residue_derivation_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            gate_row_id="ZDG2197_0_formula_known",
            derivation_clause="second variation gives a candidate residue",
            attempted_derivation="delta^2 S_parent contains 1/2 int sqrt(h) Z_X h^{ij} partial_i Xhat partial_j Xhat",
            evidence_status="FORMULA_CONTRACT_KNOWN",
            result="PASS_CONDITIONAL",
            why_not_claim="the formula exists as a contract but the parent action clause is not signed",
        ),
        base_row(
            gate_row_id="ZDG2197_1_positive_sign",
            derivation_clause="Z_X>0 or positive Schur complement",
            attempted_derivation="positivity of the quadratic operator would exclude ghost/anti-elliptic branches",
            evidence_status="MISSING_PARENT_HESSIAN_SIGN",
            result="FAIL_CURRENT_CORPUS",
            why_not_claim="no source fixes the sign and cross-block positivity in one branch",
        ),
        base_row(
            gate_row_id="ZDG2197_2_units",
            derivation_clause="units/source convention",
            attempted_derivation="Z_X units must match Xhat normalization and measured-G/Newton calibration used in K_X",
            evidence_status="MISSING_UNIT_CONVENTION",
            result="FAIL_CURRENT_CORPUS",
            why_not_claim="raw Z_X can be changed by field rescaling unless the unit convention is parent-owned",
        ),
        base_row(
            gate_row_id="ZDG2197_3_metric_spectrum",
            derivation_clause="parent metric/eigenvalue lock",
            attempted_derivation="G_X=M_AB e_X^A e_X^B and beta_eff in Spec(M^{-1} Hessian)",
            evidence_status="CLEAN_CONTRACT_NOT_SIGNED",
            result="FAIL_CURRENT_CORPUS",
            why_not_claim="M_AB, e_X, f_X, V_eff spectrum and stress/Bianchi variation are not signed",
        ),
        base_row(
            gate_row_id="ZDG2197_4_same_branch_alpha",
            derivation_clause="same branch supplies K_X and source/test legs",
            attempted_derivation="K_X^R10=s_X F_ST Pi_R10/(4*pi G_N Z_X) and alpha=K_X beta_s beta_t + epsilon_tail",
            evidence_status="MISSING_KX_BETA_SOURCE_BETA_TEST_TAILS",
            result="FAIL_CURRENT_CORPUS",
            why_not_claim="Z_X, F_ST, Pi_R10, beta_s, beta_t and tail envelope are not linked by one source",
        ),
        base_row(
            gate_row_id="ZDG2197_5_derivation_verdict",
            derivation_clause="derive Z_X now",
            attempted_derivation="derive the parent kinetic residue, sign and unit convention from current corpus",
            evidence_status="NO_NEW_OWNER_FOUND",
            result="ZX_DERIVATION_REJECTED_CURRENT_CORPUS",
            why_not_claim="current evidence proves formula discipline, not parent ownership",
        ),
    ]


def rescaling_invariant_ledger_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            invariant_id="RIL2197_0_coordinate_rescale",
            transformation="Xhat -> a Xhat",
            residue_effect="Z_X -> Z_X/a^2",
            source_effect="J_X -> J_X/a and beta_i -> beta_i/a unless absorbed conventions are explicitly declared",
            invariant_content="lambda_X=sqrt(Z_X/M_X^2) and alpha only after the same normalization fixes Z_X, M_X^2, beta_s, beta_t and K_X",
            guardrail="raw Z_X, raw beta and raw c_g are not observable by themselves",
        ),
        base_row(
            invariant_id="RIL2197_1_metric_norm",
            transformation="change field coordinate but keep physical direction fixed",
            residue_effect="the coordinate residue changes while the parent field-space norm of the physical direction is invariant",
            source_effect="source/test sensitivities must transform contragrediently",
            invariant_content="G_X=M_AB e_X e_X, or an explicitly parent-declared equivalent lock, is the object to own",
            guardrail="do not claim Z_X from a chosen coordinate gauge",
        ),
        base_row(
            invariant_id="RIL2197_2_schur_projection",
            transformation="integrate out or project coupled residual directions",
            residue_effect="Z_X is replaced by an effective Schur-complement residue",
            source_effect="source vector projects through the same Schur complement",
            invariant_content="single-channel K_X exists only after cross-block silence or positive Schur projection",
            guardrail="do not score a one-scalar Yukawa row when hidden coupled channels survive",
        ),
        base_row(
            invariant_id="RIL2197_3_public_alpha",
            transformation="switch to absorbed-alpha beta units",
            residue_effect="Z_X can be absorbed into beta_i^alpha only by explicit convention",
            source_effect="beta_i^alpha=beta_i/sqrt(4*pi*G_N*abs(Z_X)) in the 2196 convention",
            invariant_content="alpha_R10 is invariant only after both legs and signs are accounted for",
            guardrail="absorbing Z_X is allowed as notation, not as evidence",
        ),
    ]


def zx_acquisition_row_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            row_id="ZXA2197_0_ZX",
            symbol="Z_X",
            required_payload="parent coefficient or theorem-zero; sign; units; field coordinate; source path; cross-block policy",
            current_status="MISSING_PARENT_KINETIC_RESIDUE",
            acceptable_source="explicit second variation of a parent X/q_loc sector action, or a positive Schur-complement residue from a full Hessian matrix",
            unacceptable_source="setting Z_X=1 by coordinate choice, importing rho_vac by dimensional preference, or fitting after R10/PPN pressure",
            observable_link="K_X denominator; c_g/beta normalization; ghost/elliptic sign",
            valid_for_claim=False,
            score_ready=False,
        ),
        base_row(
            row_id="ZXA2197_1_GX_metric",
            symbol="G_X=M_AB e_X e_X",
            required_payload="parent field-space metric, normalized physical direction e_X, units, stress/Bianchi variation",
            current_status="MISSING_PARENT_METRIC_OBJECT",
            acceptable_source="one parent action derives M_AB and the X direction before readout",
            unacceptable_source="post-hoc field metric chosen to make beta or lambda attractive",
            observable_link="field-rescaling invariant residue owner",
            valid_for_claim=False,
            score_ready=False,
        ),
        base_row(
            row_id="ZXA2197_2_Schur",
            symbol="Z_X^eff",
            required_payload="cross-Hessian matrix; gauge/projector constraints; positive orthogonal block; source projection",
            current_status="MISSING_BLOCK_DIAGONAL_OR_SCHUR_PROOF",
            acceptable_source="explicit Hessian block decomposition from the parent variation",
            unacceptable_source="assuming all non-X residuals are silent",
            observable_link="legality of scalar Yukawa/R10 row",
            valid_for_claim=False,
            score_ready=False,
        ),
        base_row(
            row_id="ZXA2197_3_units",
            symbol="unit convention",
            required_payload="SI/natural-unit bridge; G_obs/G_N choice; beta absorbed or mass-normalized convention",
            current_status="MISSING_UNIT_AND_G_CONVENTION",
            acceptable_source="single normalization ledger used by lambda_X, K_X and beta_s/beta_t",
            unacceptable_source="changing convention between range and amplitude",
            observable_link="R10/PPN/clock/orbital comparison consistency",
            valid_for_claim=False,
            score_ready=False,
        ),
    ]


def beta_leg_fallback_row_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            beta_row_id="BLF2197_0_beta_source_leg",
            leg="beta_s",
            definition="source-body sensitivity to Xhat in the same normalization as Z_X or in a declared absorbed-alpha convention",
            current_status="MISSING_BETA_SOURCE",
            fallback_formula="alpha_R10 <= K_X^R10 beta_s beta_t + absolute tails; if one beta leg is sourced, the other can be bounded conditionally",
            required_source="matter/source current variation or source-zero theorem",
            no_cancellation_policy="unknown tails subtract from available alpha budget; no signed cancellation credit",
            valid_for_claim=False,
            score_ready=False,
        ),
        base_row(
            beta_row_id="BLF2197_1_beta_test_leg",
            leg="beta_t",
            definition="test/readout sensitivity including material, torsion/torque and marker terms",
            current_status="MISSING_BETA_TEST",
            fallback_formula="universal Weyl branch gives beta_s beta_t ~ c_g^2 profile_s profile_t, not linear c_g",
            required_source="readout/matter functor descent or bounded component row",
            no_cancellation_policy="composition/readout tails enter absolute envelope",
            valid_for_claim=False,
            score_ready=False,
        ),
        base_row(
            beta_row_id="BLF2197_2_qbarXT_source_zero",
            leg="qbar_XT/J_X",
            definition="source-zero route: ordinary matter sees only quotient observables and no marker/tail channel",
            current_status="STILL_STRONGEST_IF_PARENT_SIGNED",
            fallback_formula="if qbar_XT=J_X=0 and no-pole/vertical clauses close, the local branch avoids finite alpha rather than bounding it",
            required_source="parent q-kernel, observed coframe, matter functor, no-marker constants and hidden-tail silence",
            no_cancellation_policy="zero must be theorem-zero, not small-number fitting",
            valid_for_claim=False,
            score_ready=False,
        ),
        base_row(
            beta_row_id="BLF2197_3_verdict",
            leg="fallback selection",
            definition="Z_X failed as current derivation, so the next non-circular route is a beta/source-zero component row",
            current_status="SELECT_BETA_OR_SOURCE_ZERO_NEXT",
            fallback_formula="build component rows for beta_s, beta_t, qbar_geom, qbar_marker, qbar_source_weight and qbar_nonH",
            required_source="units, source paths, observable links and no-cancellation envelope",
            no_cancellation_policy="all rows stay valid_for_claim=false until sourced",
            valid_for_claim=False,
            score_ready=False,
        ),
    ]


def claim_gate_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    owner_verdict = any(row["contract_id"] == "ZOC2197_5_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM_ZX_OWNER_UNSIGNED" for row in rows_by_name["residue_owner_contract"])
    derivation_rejected = any(row["gate_row_id"] == "ZDG2197_5_derivation_verdict" and row["result"] == "ZX_DERIVATION_REJECTED_CURRENT_CORPUS" for row in rows_by_name["residue_derivation_gate"])
    return [
        base_row(
            gate_id="CG2197_0_ZX_owned",
            gate="Z_X parent-owned/sign-positive",
            status="BLOCKED_NONCLAIM" if owner_verdict else "FAIL",
            implication="K_X denominator and ghost/elliptic sign remain unresolved.",
        ),
        base_row(
            gate_id="CG2197_1_residue_derivation",
            gate="derive Z_X from current corpus",
            status="BLOCKED_NONCLAIM" if derivation_rejected else "FAIL",
            implication="2197 proves why the derivation is not yet earned; it does not promote a value.",
        ),
        base_row(
            gate_id="CG2197_2_beta_fallback",
            gate="beta/source-zero fallback staged",
            status="PASS_NONCLAIM",
            implication="fallback rows are ready but remain nonclaim and source-missing.",
        ),
        base_row(
            gate_id="CG2197_3_local_GR_claim",
            gate="local GR/Newton or R10 pass",
            status="BLOCKED_NONCLAIM",
            implication="No local-GR, R10, PPN, clock, orbital, WEP or public claim follows from 2197.",
        ),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            decision_id="DEC2197_0_gain",
            decision="ZX_OWNER_CONTRACT_EXACT",
            rationale="Z_X is now defined as a same-branch second-variation residue or Schur-complement residue, not a free normalization knob.",
            selection_status="selected",
        ),
        base_row(
            decision_id="DEC2197_1_result",
            decision="ZX_DERIVATION_FAILS_CURRENT_CORPUS",
            rationale="Existing files supply formulae, rescaling guards and metric-lock targets, but no parent-owned Xhat, positive residue, units, cross-block policy and source law from one branch.",
            selection_status="selected",
        ),
        base_row(
            decision_id="DEC2197_2_next",
            decision="MOVE_TO_BETA_SOURCE_ZERO_COMPONENT_PACK",
            rationale="Since raw Z_X remains arbitrary under field rescaling, the lower-scrutiny path is to prove qbar_XT/J_X source-zero or stage every beta/source component as a bounded residual.",
            selection_status="selected",
        ),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2197_0_2198",
            selection_status="selected",
            target_file="2198-Y5-R2FR-beta-source-zero-or-bounded-component-pack.md",
            target_script="scripts/Y5_R2FR_beta_source_zero_or_bounded_component_pack_2198.py",
            objective="try to derive qbar_XT=0/J_X=0 from parent matter/coframe/no-marker/hidden-tail descent; if unsigned, create bounded beta_s/beta_t/qbar component rows with units and observable links",
            success_condition="one coupling component is theorem-zero, source-backed, or explicitly staged as bounded nonclaim input; no local-GR or R10 pass is claimed",
            do_not_do="do not set beta=0 by preference, do not use WEP smallness as source-zero, do not use linear c_g, do not ignore marker/constants/tails, do not promote review R10 curves",
        )
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["zx_acquisition_row"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["beta_leg_fallback_row"], BRANCH_COPIES["branch_wep"]),
        ("source_weight", OUTPUTS["residue_owner_contract"], BRANCH_COPIES["source_weight"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(base_row(copy_id=copy_id, source_path=str(source), target_path=str(target), copied=target.exists()))
    return rows


def all_claim_flags_false(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if truthy(row.get("claim_allowed", False)):
                return False
            if truthy(row.get("valid_for_claim", False)):
                return False
    return True


def all_score_flags_false(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            for key in ("score_ready", "numeric_ready"):
                if key in row and truthy(row[key]):
                    return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    validations: list[dict[str, Any]] = []
    sources = rows_by_name["source_register"]
    validations.append(base_row(validation_id="VAL2197_00_sources_exist", status="PASS" if all(row["path_exists"] for row in sources) else "FAIL", detail=f"{sum(bool(row['path_exists']) for row in sources)}/{len(sources)} sources exist"))
    validations.append(base_row(validation_id="VAL2197_01_needles_found", status="PASS" if all(row["needles_found"] for row in sources) else "FAIL", detail=f"{sum(bool(row['needles_found']) for row in sources)}/{len(sources)} source needle sets found"))

    contract = rows_by_name["residue_owner_contract"]
    owner_fail = any(row["contract_id"] == "ZOC2197_5_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM_ZX_OWNER_UNSIGNED" for row in contract)
    z_contract = any(row["contract_id"] == "ZOC2197_1_second_variation" and "delta^2 S_parent" in row["required_statement"] for row in contract)
    validations.append(base_row(validation_id="VAL2197_02_owner_contract", status="PASS" if owner_fail and z_contract else "FAIL", detail=f"owner_fail={owner_fail};second_variation_contract={z_contract}"))

    derivation = rows_by_name["residue_derivation_gate"]
    derivation_rejected = any(row["gate_row_id"] == "ZDG2197_5_derivation_verdict" and row["result"] == "ZX_DERIVATION_REJECTED_CURRENT_CORPUS" for row in derivation)
    formula_conditional = any(row["gate_row_id"] == "ZDG2197_0_formula_known" and row["result"] == "PASS_CONDITIONAL" for row in derivation)
    validations.append(base_row(validation_id="VAL2197_03_derivation_gate", status="PASS" if derivation_rejected and formula_conditional else "FAIL", detail=f"formula_conditional={formula_conditional};derivation_rejected={derivation_rejected}"))

    invariant_rows = rows_by_name["rescaling_invariant_ledger"]
    rescale_guard = any(row["invariant_id"] == "RIL2197_0_coordinate_rescale" and "Z_X -> Z_X/a^2" in row["residue_effect"] for row in invariant_rows)
    schur_guard = any(row["invariant_id"] == "RIL2197_2_schur_projection" for row in invariant_rows)
    validations.append(base_row(validation_id="VAL2197_04_rescaling_guards", status="PASS" if rescale_guard and schur_guard else "FAIL", detail=f"rescale_guard={rescale_guard};schur_guard={schur_guard}"))

    acquisition = rows_by_name["zx_acquisition_row"]
    acquisition_ok = any(row["row_id"] == "ZXA2197_0_ZX" and row["current_status"] == "MISSING_PARENT_KINETIC_RESIDUE" and not truthy(row["score_ready"]) for row in acquisition)
    validations.append(base_row(validation_id="VAL2197_05_zx_acquisition", status="PASS" if acquisition_ok else "FAIL", detail="Z_X acquisition row remains source-missing and nonclaim"))

    beta = rows_by_name["beta_leg_fallback_row"]
    beta_ok = any(row["beta_row_id"] == "BLF2197_3_verdict" and row["current_status"] == "SELECT_BETA_OR_SOURCE_ZERO_NEXT" for row in beta)
    validations.append(base_row(validation_id="VAL2197_06_beta_fallback", status="PASS" if beta_ok else "FAIL", detail="beta/source-zero fallback row selected"))

    gates = rows_by_name["claim_gate"]
    gates_ok = any(row["gate_id"] == "CG2197_0_ZX_owned" and row["status"] == "BLOCKED_NONCLAIM" for row in gates) and any(row["gate_id"] == "CG2197_2_beta_fallback" and row["status"] == "PASS_NONCLAIM" for row in gates)
    validations.append(base_row(validation_id="VAL2197_07_claim_gate", status="PASS" if gates_ok else "FAIL", detail="Z_X claim blocked; beta fallback staged only as nonclaim"))

    decisions = {row["decision"] for row in rows_by_name["decision"] if row["selection_status"] == "selected"}
    validations.append(base_row(validation_id="VAL2197_08_decision", status="PASS" if "MOVE_TO_BETA_SOURCE_ZERO_COMPONENT_PACK" in decisions else "FAIL", detail="decision moves to beta/source-zero component pack"))

    routes = {row["route_id"] for row in rows_by_name["next_target"] if row["selection_status"] == "selected"}
    validations.append(base_row(validation_id="VAL2197_09_next_target", status="PASS" if "NEXT2197_0_2198" in routes else "FAIL", detail="2198 beta/source-zero target selected"))

    validations.append(base_row(validation_id="VAL2197_10_claim_flags_false", status="PASS" if all_claim_flags_false(rows_by_name) else "FAIL", detail="all generated rows keep valid_for_claim=false and claim_allowed=false"))
    validations.append(base_row(validation_id="VAL2197_11_score_flags_false", status="PASS" if all_score_flags_false(rows_by_name) else "FAIL", detail="no generated row is score-ready or numeric-ready"))

    parse_details: list[str] = []
    parse_pass = True
    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        parse_pass = parse_pass and ok and count > 0
        parse_details.append(f"{path.name}:{count if ok else detail}")
    validations.append(base_row(validation_id="VAL2197_12_csv_parse", status="PASS" if parse_pass else "FAIL", detail="; ".join(parse_details)))

    copies = rows_by_name["branch_copies"]
    validations.append(base_row(validation_id="VAL2197_13_branch_copies", status="PASS" if copies and all(row["copied"] for row in copies) else "FAIL", detail=";".join(str(row["target_path"]) for row in copies)))

    validations.append(base_row(validation_id="VAL2197_14_formalization_clean", status="PASS" if not formalization_has_2197_artifacts() else "FAIL", detail="formalization-workbench has no 2197 artifacts"))

    remove_pycache()
    validations.append(base_row(validation_id="VAL2197_15_pycache_absent", status="PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL", detail=str(ROOT / "scripts" / "__pycache__")))

    overall = "PASS" if all(row["status"] == "PASS" for row in validations) else "FAIL"
    validations.append(base_row(validation_id="VAL2197_OVERALL", status=overall, detail="2197 defines the exact Z_X ownership contract, rejects current Z_X derivation, stages acquisition rows, and selects beta/source-zero component pack next"))
    return validations


def render_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> str:
    return "\n".join(
        [
            "# 2197 - Y5/R2FR Parent Z_X Residue Or Beta-Leg Source First Row",
            "",
            "## Current Verdict",
            "",
            "2197 tries the `Z_X` route and does **not** promote it. The useful result is sharper: `Z_X` is not a number we are missing; it is a parent-ownership contract. It becomes physical only as the same-branch second-variation residue, or positive Schur-complement residue, of the same `Xhat` coordinate used by `lambda_X`, `K_X`, `beta_s`, `beta_t`, and the source law.",
            "",
            "The current corpus has formula discipline but not ownership. It has the second-variation form, the range relation, and the rescaling trap, but it still lacks parent-owned `Xhat`, positive `Z_X`, units/sign convention, cross-Hessian control, field-space metric lock, source law, and tail/boundary policy from one branch.",
            "",
            "So the honest move is: keep `Z_X` as a source-acquisition row, block numeric `K_X`, and move the next local-GR attack to coupling silence or bounded beta components.",
            "",
            "## Source Register",
            "",
            md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "",
            "## Z_X Residue Owner Contract",
            "",
            md_table(rows_by_name["residue_owner_contract"], ["contract_id", "object", "required_statement", "mathematical_role", "current_status", "missing_for_claim", "valid_for_claim"]),
            "",
            "## Z_X Derivation Gate",
            "",
            md_table(rows_by_name["residue_derivation_gate"], ["gate_row_id", "derivation_clause", "attempted_derivation", "evidence_status", "result", "why_not_claim", "valid_for_claim"]),
            "",
            "## Rescaling Invariant Ledger",
            "",
            md_table(rows_by_name["rescaling_invariant_ledger"], ["invariant_id", "transformation", "residue_effect", "source_effect", "invariant_content", "guardrail", "valid_for_claim"]),
            "",
            "## Z_X Source Acquisition Row",
            "",
            md_table(rows_by_name["zx_acquisition_row"], ["row_id", "symbol", "required_payload", "current_status", "acceptable_source", "unacceptable_source", "observable_link", "score_ready", "valid_for_claim"]),
            "",
            "## Beta-Leg Fallback Row",
            "",
            md_table(rows_by_name["beta_leg_fallback_row"], ["beta_row_id", "leg", "definition", "current_status", "fallback_formula", "required_source", "no_cancellation_policy", "score_ready", "valid_for_claim"]),
            "",
            "## Claim Gate",
            "",
            md_table(rows_by_name["claim_gate"], ["gate_id", "gate", "status", "implication", "valid_for_claim"]),
            "",
            "## Decision Ledger",
            "",
            md_table(rows_by_name["decision"], ["decision_id", "decision", "rationale", "selection_status", "valid_for_claim"]),
            "",
            "## Next Target",
            "",
            md_table(rows_by_name["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do", "valid_for_claim"]),
            "",
            "## Branch Copies",
            "",
            md_table(rows_by_name["branch_copies"], ["copy_id", "source_path", "target_path", "copied", "valid_for_claim"]),
            "",
            "## Validation",
            "",
            md_table(rows_by_name["validation"], ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"]),
            "",
            "## Interpretation",
            "",
            "This is the right kind of negative result. It does not say the finite branch is nonsense; it says the finite branch is not allowed to hide normalization freedom. If `Z_X` is not parent-owned, `K_X` is not numeric. The cleaner fight now is coupling silence: prove `qbar_XT=0/J_X=0`, or make every surviving coupling component a source-backed bounded residual.",
            "",
            "Best next attack: build the beta/source-zero component pack. If one component closes by theorem, the local-GR route strengthens. If none close, the residual vector becomes explicit enough to test without pretending it was derived.",
            "",
        ]
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "residue_owner_contract": residue_owner_contract_rows(),
        "residue_derivation_gate": residue_derivation_gate_rows(),
        "rescaling_invariant_ledger": rescaling_invariant_ledger_rows(),
        "zx_acquisition_row": zx_acquisition_row_rows(),
        "beta_leg_fallback_row": beta_leg_fallback_row_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }
    rows_by_name["claim_gate"] = claim_gate_rows(rows_by_name)

    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])

    DOC.write_text(render_doc(rows_by_name), encoding="utf-8")
    remove_pycache()


if __name__ == "__main__":
    main()
