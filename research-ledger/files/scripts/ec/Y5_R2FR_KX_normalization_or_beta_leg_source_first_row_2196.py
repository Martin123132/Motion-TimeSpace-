from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2196"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2196-Y5-R2FR-KX-normalization-or-beta-leg-source-first-row.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2196_SOURCE_REGISTER.csv",
    "normalization_derivation": OUT / "P8_Y5_PARENT_QLOC_2196_KX_NORMALIZATION_DERIVATION.csv",
    "factor_status": OUT / "P8_Y5_PARENT_QLOC_2196_KX_FACTOR_STATUS.csv",
    "shortcut_quarantine": OUT / "P8_Y5_PARENT_QLOC_2196_KX_SHORTCUT_QUARANTINE.csv",
    "pressure_update": OUT / "P8_Y5_PARENT_QLOC_2196_PRESSURE_ROW_UPDATE.csv",
    "fallback_queue": OUT / "P8_Y5_PARENT_QLOC_2196_BETA_LEG_FALLBACK_QUEUE.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2196_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2196_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2196_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2196_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2196_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2196_KX_NORMALIZATION_BLOCK_AND_ZX_NEXT_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2196_PRESSURE_ROW_UPDATE_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "PARENT_QLOC_R10_KX_NORMALIZATION_2196_NONCLAIM.csv",
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


def safe_float(value: Any) -> float | None:
    try:
        return float(str(value))
    except (TypeError, ValueError):
        return None


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def formalization_has_2196_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2196-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2196*",
        "*P8_Y5_BRR545_2196*",
        "*Y5_R2FR_KX_normalization_or_beta_leg_source_first_row_2196*",
        "*JR2196*",
        "*PARENT_QLOC_R10_KX_NORMALIZATION_2196*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "1035_doc",
            ROOT / "1035-Y5-R10-KX-green-kernel-normalization-and-profile-integral.md",
            ["K_X^R10(lambda)=K_X^pt * F_ST(lambda) * Pi_R10", "K_X^pt=1/(4 pi G_N Z_X)", "NOT_NUMERIC_CURRENT_CORPUS"],
            "Primary source for the conditional Green-kernel and R10 projection factorization.",
        ),
        (
            "1035_kx_csv",
            OUT / "P8_Y5_R10_1035_KX_FACTORIZATION_ROWS.csv",
            ["KXF1035_0_KX_point", "KXF1035_4_total", "NOT_NUMERIC_CURRENT_CORPUS"],
            "Machine-readable KX factor status used as 2196 input.",
        ),
        (
            "1035_profile_csv",
            OUT / "P8_Y5_R10_1035_PROFILE_INTEGRAL_CONTRACT.csv",
            ["PROF1035_2_pair_overlap", "PROF1035_3_R10_harmonic", "Newton normalization"],
            "Profile/harmonic/Newton calibration contract for R10 scoring.",
        ),
        (
            "1036_doc",
            ROOT / "1036-Y5-R10-parent-X-quadratic-action-and-beta-source-test-split.md",
            ["no numeric `K_X`", "beta_s=beta_t=c_g", "FAIL_CURRENT_CLAIM_PARENT_ROW_NOT_OWNED"],
            "Parent X action audit and c_g squared correction.",
        ),
        (
            "1036_parent_audit_csv",
            OUT / "P8_Y5_R10_1036_PARENT_X_ACTION_AUDIT.csv",
            ["PX1036_1_quadratic_residue", "PX1036_4_source_test_betas", "FAIL_CURRENT_CLAIM_PARENT_ROW_NOT_OWNED"],
            "Machine-readable parent finite-X row ownership audit.",
        ),
        (
            "2194_factorization_doc",
            ROOT / "2194-Y5-R2FR-parent-q_loc-alpha-coefficient-profile-or-theorem-zero.md",
            ["alpha_predicted(lambda)=s_X K_X^R10(lambda)", "choose c_q_alpha=s_X/(4*pi*G_N*Z_X)", "FAC2194_2_universal_cg_warning"],
            "q_loc to R10 factorization contract and universal-branch guard.",
        ),
        (
            "2195_pressure_doc",
            ROOT / "2195-Y5-R2FR-parent-quotient-no-pole-certificate-or-first-beta-bound-row.md",
            ["abs(beta_s beta_t) <=", "MISSING_KX_R10", "Best next attack: derive/source `K_X^R10`"],
            "First R10 beta-product pressure row and 2196 target.",
        ),
        (
            "2195_pressure_csv",
            OUT / "P8_Y5_PARENT_QLOC_2195_FIRST_BETA_PRODUCT_PRESSURE_ROW.csv",
            ["BETA2195_0_R10_beta_product_pressure_at_38p6um", "0.9915372447041295", "MISSING_KX_R10"],
            "Machine-readable R10 pressure wall inherited by 2196.",
        ),
        (
            "2195_next_csv",
            OUT / "P8_Y5_PARENT_QLOC_2195_NEXT_TARGET.csv",
            ["NEXT2195_0_2196", "do not set K_X=1", "do not promote the review curve"],
            "Explicit do-not-do guard for this checkpoint.",
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


def pressure_seed() -> dict[str, str]:
    rows = read_csv(OUT / "P8_Y5_PARENT_QLOC_2195_FIRST_BETA_PRODUCT_PRESSURE_ROW.csv")
    return rows[0] if rows else {}


def normalization_derivation_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            derivation_id="KXN2196_0_parent_quadratic_start",
            step="finite local response quadratic row",
            formula="S_X^(2)=-1/2 int [Z_X (partial X)^2 + Z_X lambda_X^-2 X^2] + int X J_X",
            required_convention="X normalization, sign_sX, positive/negative kinetic residue convention, and source current J_X must come from the parent action",
            result="CONDITIONAL_ONLY",
            missing_for_numeric="parent-signed Z_X, M_X^2/lambda_X, J_X, sign_sX",
        ),
        base_row(
            derivation_id="KXN2196_1_static_inverse",
            step="static Green inverse",
            formula="(nabla^2-lambda_X^-2)X=-J_X/Z_X -> G_lambda(r)=exp(-r/lambda_X)/(4*pi*r)",
            required_convention="operator must be scalar finite pole, not derivative/disformal/tensor response",
            result="DERIVED_IF_PARENT_OPERATOR_EXISTS",
            missing_for_numeric="proof that the MTS local branch owns this scalar operator",
        ),
        base_row(
            derivation_id="KXN2196_2_point_yukawa_match_mass_beta",
            step="match to alpha convention with mass-normalized beta legs",
            formula="V_X(r)=-s_X beta_s beta_t m_s m_t exp(-r/lambda_X)/(4*pi*Z_X*r); alpha_X=s_X beta_s beta_t/(4*pi*G_N*Z_X)",
            required_convention="beta_i are dimensionless mass/readout sensitivities and do not absorb sqrt(4*pi*G_N*Z_X)",
            result="CONDITIONAL_NORMALIZATION_SPLIT",
            missing_for_numeric="Z_X sign/value, beta source/test definitions, and measured-G/Newton local calibration",
        ),
        base_row(
            derivation_id="KXN2196_3_R10_projection",
            step="map point Yukawa alpha to R10 torque/readout",
            formula="K_X^R10(lambda)=s_X*F_ST(lambda)*Pi_R10(lambda)/(4*pi*G_N*Z_X)",
            required_convention="F_ST and Pi_R10 use the same alpha normalization and same source/test support as beta_s,beta_t",
            result="BEST_CURRENT_SYMBOLIC_KX_CONTRACT",
            missing_for_numeric="F_ST(lambda), Pi_R10(lambda), R10 geometry/support, and source/test material density rule",
        ),
        base_row(
            derivation_id="KXN2196_4_abs_pressure_form",
            step="convert 2195 wall into normalization-aware pressure",
            formula="abs(beta_s beta_t) <= (alpha_bound-abs(epsilon_tail))*4*pi*G_N*abs(Z_X)/abs(F_ST Pi_R10)",
            required_convention="same convention as KXN2196_2, positive remaining alpha budget, and absolute tail envelope",
            result="SYMBOLIC_PRESSURE_ONLY",
            missing_for_numeric="Z_X, F_ST, Pi_R10, epsilon_tail",
        ),
        base_row(
            derivation_id="KXN2196_5_absorbed_beta_convention",
            step="alternative convention where beta absorbs kernel normalization",
            formula="beta_i^alpha=beta_i/sqrt(4*pi*G_N*abs(Z_X)); alpha_X=s_X sign(Z_X) F_ST Pi_R10 beta_s^alpha beta_t^alpha + epsilon_tail",
            required_convention="parent must explicitly declare absorbed factors and units",
            result="CONVENTION_ALLOWED_NOT_A_SHORTCUT",
            missing_for_numeric="declaration that both source and test legs use absorbed-alpha beta units",
        ),
        base_row(
            derivation_id="KXN2196_6_verdict",
            step="decide whether K_X^R10 is numeric",
            formula="K_X^R10 is symbolically split but not numerically owned",
            required_convention="one parent branch signs Z_X/range/current and one R10 branch signs F_ST/Pi_R10",
            result="KX_NUMERIC_BLOCKED_CURRENT_CORPUS",
            missing_for_numeric="MISSING_ZX;MISSING_PARENT_OPERATOR;MISSING_FST;MISSING_PI_R10;MISSING_TAIL_ENVELOPE",
        ),
    ]


def factor_status_rows() -> list[dict[str, Any]]:
    kx_rows = {row.get("factor_id", ""): row for row in read_csv(OUT / "P8_Y5_R10_1035_KX_FACTORIZATION_ROWS.csv")}
    parent_rows = {row.get("audit_id", ""): row for row in read_csv(OUT / "P8_Y5_R10_1036_PARENT_X_ACTION_AUDIT.csv")}
    return [
        base_row(
            factor_id="KXF2196_0_ZX_residue",
            factor="Z_X",
            inherited_source="PX1036_1_quadratic_residue;KXF1035_0_KX_point",
            inherited_status=parent_rows.get("PX1036_1_quadratic_residue", {}).get("result", "MISSING_SOURCE_ROW"),
            current_status="MISSING_PARENT_KINETIC_RESIDUE",
            numeric_ready=False,
            consequence="K_X^pt cannot be numeric and sign/ghost/elliptic branch is not parent-owned.",
        ),
        base_row(
            factor_id="KXF2196_1_lambdaX_range",
            factor="lambda_X",
            inherited_source="PX1036_2_mass_gap_range;KXF1035_1_range",
            inherited_status=parent_rows.get("PX1036_2_mass_gap_range", {}).get("result", "MISSING_SOURCE_ROW"),
            current_status="RELATION_DERIVED_VALUES_MISSING",
            numeric_ready=False,
            consequence="R10 lambda target cannot be predicted by the parent branch; only external seed comparisons are possible.",
        ),
        base_row(
            factor_id="KXF2196_2_FST_profile",
            factor="F_ST(lambda)",
            inherited_source="PROF1035_2_pair_overlap;KXF1035_2_profile",
            inherited_status=kx_rows.get("KXF1035_2_profile", {}).get("status", "MISSING_SOURCE_ROW"),
            current_status="SYMBOLIC_PROFILE_ONLY",
            numeric_ready=False,
            consequence="Extended-body source/test geometry cannot be replaced by point-body unity for R10.",
        ),
        base_row(
            factor_id="KXF2196_3_Pi_R10_harmonic",
            factor="Pi_R10(lambda)",
            inherited_source="PROF1035_3_R10_harmonic;KXF1035_3_harmonic",
            inherited_status=kx_rows.get("KXF1035_3_harmonic", {}).get("status", "MISSING_SOURCE_ROW"),
            current_status="MISSING_R10_HARMONIC_KERNEL",
            numeric_ready=False,
            consequence="The experiment-specific torque/readout projection is not known.",
        ),
        base_row(
            factor_id="KXF2196_4_tail_envelope",
            factor="epsilon_tail(lambda)",
            inherited_source="FAC2194_4_tail_envelope;CGSQ2195_1_no_cancellation_tail_rule",
            inherited_status="MISSING_ABSOLUTE_TAIL_ENVELOPE",
            current_status="MISSING_ABSOLUTE_TAIL_ENVELOPE",
            numeric_ready=False,
            consequence="Unknown tails cannot be credited as cancellations against alpha_bound.",
        ),
        base_row(
            factor_id="KXF2196_5_total_KX",
            factor="K_X^R10(lambda)",
            inherited_source="KXF1035_4_total;KXN2196_3_R10_projection",
            inherited_status=kx_rows.get("KXF1035_4_total", {}).get("status", "MISSING_SOURCE_ROW"),
            current_status="SYMBOLIC_CONTRACT_NOT_NUMERIC",
            numeric_ready=False,
            consequence="Use K_X^R10=s_X F_ST Pi_R10/(4*pi G_N Z_X) only as a nonclaim contract.",
        ),
    ]


def shortcut_quarantine_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            shortcut_id="KXQ2196_0_KX_equals_one",
            shortcut="K_X^R10(lambda)=1",
            verdict="REJECTED_SHORTCUT",
            reason="K_X=1 only follows from a declared absorbed-beta convention plus F_ST=Pi_R10=1; neither is parent-signed or R10-sourced.",
            allowed_replacement="write the convention explicitly or keep K_X=s_X F_ST Pi_R10/(4*pi G_N Z_X)",
            score_ready=False,
        ),
        base_row(
            shortcut_id="KXQ2196_1_point_body_profile",
            shortcut="F_ST(lambda)=1",
            verdict="REJECTED_FOR_R10",
            reason="R10 is an extended-body torque experiment; the point-body limit is not the measured geometry.",
            allowed_replacement="source the R10 support/material density rule or official kernel",
            score_ready=False,
        ),
        base_row(
            shortcut_id="KXQ2196_2_harmonic_projection_unity",
            shortcut="Pi_R10(lambda)=1",
            verdict="REJECTED_FOR_R10",
            reason="The measured observable is a harmonic torque/readout projection, not the raw potential coefficient.",
            allowed_replacement="derive or source the Fourier-Bessel/official torque kernel",
            score_ready=False,
        ),
        base_row(
            shortcut_id="KXQ2196_3_linear_cg",
            shortcut="alpha_R10 proportional to c_g",
            verdict="REJECTED_UNLESS_SOURCE_LEG_ABSORBED",
            reason="A two-body finite exchange has source and test legs; universal Weyl response gives c_g^2.",
            allowed_replacement="source one absorbed leg explicitly or score alpha proportional to c_g^2 with no-cancellation tails",
            score_ready=False,
        ),
        base_row(
            shortcut_id="KXQ2196_4_tail_cancellation",
            shortcut="epsilon_tail cancels beta_s beta_t",
            verdict="REJECTED_WITHOUT_SIGNED_CORRELATION",
            reason="No parent theorem signs tail correlations; comparison must subtract absolute tail budget first.",
            allowed_replacement="derive a theorem-zero or source an absolute tail envelope",
            score_ready=False,
        ),
    ]


def pressure_update_rows() -> list[dict[str, Any]]:
    seed = pressure_seed()
    alpha = seed.get("alpha_bound_review_candidate", "")
    target_lambda = seed.get("target_lambda_m", "")
    nearest_lambda = seed.get("nearest_curve_lambda_m", "")
    relative_error = seed.get("lambda_relative_error", "")
    return [
        base_row(
            pressure_id="KXP2196_0_R10_pressure_with_KX_split",
            parent_pressure_row=seed.get("beta_row_id", "MISSING_2195_PRESSURE_ROW"),
            arena=seed.get("arena", "R10_short_range"),
            target_lambda_m=target_lambda,
            nearest_curve_lambda_m=nearest_lambda,
            lambda_relative_error=relative_error,
            alpha_bound_review_candidate=alpha,
            original_2195_formula=seed.get("conditional_bound_formula", ""),
            kx_split_formula="K_X^R10(lambda)=s_X*F_ST(lambda)*Pi_R10(lambda)/(4*pi*G_N*Z_X)",
            normalization_aware_bound="abs(beta_s*beta_t) <= (alpha_bound_review_candidate-abs(epsilon_tail))*4*pi*G_N*abs(Z_X)/abs(F_ST*Pi_R10)",
            numeric_beta_bound_status="BLOCKED_NONCLAIM",
            missing_for_numeric="MISSING_ZX;MISSING_FST;MISSING_PI_R10;MISSING_ABSOLUTE_TAIL_ENVELOPE;MISSING_BETA_SOURCE;MISSING_BETA_TEST",
            curve_status=seed.get("curve_status", "REVIEW_CANDIDATE_NONCLAIM"),
            score_ready=False,
            notes="2196 improves the pressure row by exposing where K_X lives, but it still does not create a numeric beta or R10 score.",
        )
    ]


def fallback_queue_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            queue_id="FB2196_0_parent_ZX_residue",
            priority=1,
            target="Z_X",
            objective="derive the parent kinetic residue and sign of the finite local X/q_loc response mode",
            why_first="without Z_X there is no owned K_X normalization, no ghost/elliptic sign, and no numeric beta pressure",
            success_condition="one parent action row supplies Z_X, sign_sX, field normalization, and measured-G convention",
            fallback_if_failed="demote finite-X numeric branch further and move to source/test beta envelopes",
        ),
        base_row(
            queue_id="FB2196_1_beta_source_leg",
            priority=2,
            target="beta_s",
            objective="derive or bound the source-body matter-current sensitivity to the local mode",
            why_first="a single sourced beta leg can convert the product pressure into a one-leg bound",
            success_condition="source material/current law with units and no hidden absorbed leg",
            fallback_if_failed="stage beta_s as acquisition row and attack beta_t/readout",
        ),
        base_row(
            queue_id="FB2196_2_beta_test_leg",
            priority=3,
            target="beta_t",
            objective="derive or bound the test/readout response including torsion/torque projection",
            why_first="R10 readout can differ from source mass coupling and must not be assumed equal",
            success_condition="readout sensitivity row with units, sign policy, and profile ownership",
            fallback_if_failed="stage beta_t as acquisition row and attack R10 kernel geometry",
        ),
        base_row(
            queue_id="FB2196_3_R10_kernel_geometry",
            priority=4,
            target="F_ST and Pi_R10",
            objective="source the extended-body form factor and harmonic torque projection",
            why_first="this turns the external R10 curve into a true comparison at the measured observable level",
            success_condition="source/test support, material densities, and harmonic projection from official or reconstructed kernel",
            fallback_if_failed="keep pressure row nonnumeric and move to less geometry-heavy local tests",
        ),
        base_row(
            queue_id="FB2196_4_tail_envelope",
            priority=5,
            target="epsilon_tail",
            objective="derive an absolute bound on retained disformal/marker/support leakage",
            why_first="unknown tails reduce the allowed beta budget and cannot be counted as cancellation",
            success_condition="absolute tail envelope with source path and no-cancellation sign policy",
            fallback_if_failed="all R10 beta bounds remain conditional upper-pressure only",
        ),
    ]


def claim_gate_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    factor_numeric = all(truthy(row.get("numeric_ready", False)) for row in rows_by_name["factor_status"])
    pressure_ready = all(truthy(row.get("score_ready", False)) for row in rows_by_name["pressure_update"])
    shortcuts_clear = all(row.get("verdict") != "ALLOWED_SHORTCUT" for row in rows_by_name["shortcut_quarantine"])
    return [
        base_row(
            gate_id="CG2196_0_KX_numeric",
            gate="K_X^R10 numeric/source-backed",
            status="BLOCKED_NONCLAIM" if not factor_numeric else "PASS_CANDIDATE",
            implication="K_X split is derived as a symbolic contract only; no numeric K_X or R10 score.",
        ),
        base_row(
            gate_id="CG2196_1_pressure_score",
            gate="normalization-aware beta pressure numeric",
            status="BLOCKED_NONCLAIM" if not pressure_ready else "PASS_CANDIDATE",
            implication="alpha wall is real-shaped review data, but theory-side factors are missing.",
        ),
        base_row(
            gate_id="CG2196_2_shortcut_quarantine",
            gate="no unity/linear/cancellation shortcuts",
            status="PASS_NONCLAIM" if shortcuts_clear else "FAIL",
            implication="K_X=1, F_ST=1, Pi_R10=1, linear c_g, and tail cancellation are barred unless separately sourced.",
        ),
        base_row(
            gate_id="CG2196_3_R10_local_GR_claim",
            gate="R10/local-GR pass claim",
            status="BLOCKED_NONCLAIM",
            implication="No R10, WEP, PPN, clock, orbital, or local-GR claim follows from 2196.",
        ),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            decision_id="DEC2196_0_gain",
            decision="KX_NORMALIZATION_SPLIT_DERIVED_AS_CONTRACT",
            rationale="The current best law is K_X^R10=s_X F_ST Pi_R10/(4*pi G_N Z_X) in mass-normalized beta units, with an allowed absorbed-beta convention only if parent-declared.",
            selection_status="selected",
        ),
        base_row(
            decision_id="DEC2196_1_block",
            decision="KX_NUMERIC_VALUE_BLOCKED",
            rationale="No current source signs Z_X, F_ST, Pi_R10, measured-G convention, and absolute tails together; K_X=1 is explicitly rejected.",
            selection_status="selected",
        ),
        base_row(
            decision_id="DEC2196_2_next",
            decision="ATTACK_PARENT_ZX_RESIDUE_NEXT",
            rationale="Z_X is the first denominator of the coupling normalization and controls the physical sign/ghost status; without it every beta pressure row stays symbolic.",
            selection_status="selected",
        ),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2196_0_2197",
            selection_status="selected",
            target_file="2197-Y5-R2FR-parent-ZX-residue-or-beta-leg-source-first-row.md",
            target_script="scripts/Y5_R2FR_parent_ZX_residue_or_beta_leg_source_first_row_2197.py",
            objective="try to derive the parent kinetic residue Z_X/sign_sX/unit convention for the finite local response mode; if that fails, stage the first beta_s or beta_t source/test leg row",
            success_condition="Z_X is parent-derived/source-backed or explicitly demoted, and the next beta-leg acquisition path is selected without R10/local-GR claims",
            do_not_do="do not set Z_X=1, do not absorb factors into beta without a convention row, do not assume F_ST or Pi_R10 are unity, do not use linear c_g, do not promote R10 curve rows",
        )
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["fallback_queue"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["pressure_update"], BRANCH_COPIES["branch_wep"]),
        ("source_weight", OUTPUTS["normalization_derivation"], BRANCH_COPIES["source_weight"]),
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
    validations.append(base_row(validation_id="VAL2196_00_sources_exist", status="PASS" if all(row["path_exists"] for row in sources) else "FAIL", detail=f"{sum(bool(row['path_exists']) for row in sources)}/{len(sources)} sources exist"))
    validations.append(base_row(validation_id="VAL2196_01_needles_found", status="PASS" if all(row["needles_found"] for row in sources) else "FAIL", detail=f"{sum(bool(row['needles_found']) for row in sources)}/{len(sources)} source needle sets found"))

    normalization = rows_by_name["normalization_derivation"]
    split_ok = any(row["derivation_id"] == "KXN2196_3_R10_projection" and "4*pi*G_N*Z_X" in row["formula"] and "F_ST" in row["formula"] and "Pi_R10" in row["formula"] for row in normalization)
    verdict_ok = any(row["derivation_id"] == "KXN2196_6_verdict" and row["result"] == "KX_NUMERIC_BLOCKED_CURRENT_CORPUS" for row in normalization)
    validations.append(base_row(validation_id="VAL2196_02_kx_split", status="PASS" if split_ok and verdict_ok else "FAIL", detail=f"split_ok={split_ok};verdict_ok={verdict_ok}"))

    factor_rows = rows_by_name["factor_status"]
    factor_block_ok = any(row["factor_id"] == "KXF2196_5_total_KX" and row["current_status"] == "SYMBOLIC_CONTRACT_NOT_NUMERIC" for row in factor_rows)
    factor_numeric_false = all(not truthy(row.get("numeric_ready", False)) for row in factor_rows)
    validations.append(base_row(validation_id="VAL2196_03_factor_status", status="PASS" if factor_block_ok and factor_numeric_false else "FAIL", detail=f"total_kx_blocked={factor_block_ok};numeric_false={factor_numeric_false}"))

    quarantines = rows_by_name["shortcut_quarantine"]
    required_shortcuts = {"K_X^R10(lambda)=1", "F_ST(lambda)=1", "Pi_R10(lambda)=1", "alpha_R10 proportional to c_g", "epsilon_tail cancels beta_s beta_t"}
    seen_shortcuts = {row["shortcut"] for row in quarantines}
    quarantine_ok = required_shortcuts.issubset(seen_shortcuts) and all("REJECTED" in row["verdict"] for row in quarantines)
    validations.append(base_row(validation_id="VAL2196_04_shortcut_quarantine", status="PASS" if quarantine_ok else "FAIL", detail=f"{len(required_shortcuts.intersection(seen_shortcuts))}/{len(required_shortcuts)} shortcuts rejected"))

    pressure = rows_by_name["pressure_update"][0]
    alpha = safe_float(pressure.get("alpha_bound_review_candidate", ""))
    pressure_ok = (
        alpha is not None
        and alpha > 0
        and "4*pi*G_N*abs(Z_X)" in pressure["normalization_aware_bound"]
        and pressure["numeric_beta_bound_status"] == "BLOCKED_NONCLAIM"
        and not truthy(pressure["score_ready"])
    )
    validations.append(base_row(validation_id="VAL2196_05_pressure_update", status="PASS" if pressure_ok else "FAIL", detail=f"alpha={pressure.get('alpha_bound_review_candidate')};status={pressure['numeric_beta_bound_status']};score_ready={pressure['score_ready']}"))

    queue = rows_by_name["fallback_queue"]
    queue_ok = queue and queue[0]["target"] == "Z_X" and queue[0]["priority"] == 1
    validations.append(base_row(validation_id="VAL2196_06_fallback_queue", status="PASS" if queue_ok else "FAIL", detail="Z_X residue is first next target"))

    gates = rows_by_name["claim_gate"]
    gates_ok = any(row["gate_id"] == "CG2196_0_KX_numeric" and row["status"] == "BLOCKED_NONCLAIM" for row in gates) and any(row["gate_id"] == "CG2196_2_shortcut_quarantine" and row["status"] == "PASS_NONCLAIM" for row in gates)
    validations.append(base_row(validation_id="VAL2196_07_claim_gate", status="PASS" if gates_ok else "FAIL", detail="KX numeric blocked; shortcut quarantine passes as nonclaim"))

    decisions = {row["decision"] for row in rows_by_name["decision"] if row["selection_status"] == "selected"}
    validations.append(base_row(validation_id="VAL2196_08_decision", status="PASS" if "ATTACK_PARENT_ZX_RESIDUE_NEXT" in decisions else "FAIL", detail="decision selects parent Z_X residue next"))

    routes = {row["route_id"] for row in rows_by_name["next_target"] if row["selection_status"] == "selected"}
    validations.append(base_row(validation_id="VAL2196_09_next_target", status="PASS" if "NEXT2196_0_2197" in routes else "FAIL", detail="2197 parent Z_X / beta-leg target selected"))

    validations.append(base_row(validation_id="VAL2196_10_claim_flags_false", status="PASS" if all_claim_flags_false(rows_by_name) else "FAIL", detail="all generated rows keep valid_for_claim=false and claim_allowed=false"))
    validations.append(base_row(validation_id="VAL2196_11_score_flags_false", status="PASS" if all_score_flags_false(rows_by_name) else "FAIL", detail="no generated row is score-ready or numeric-ready"))

    parse_details: list[str] = []
    parse_pass = True
    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        parse_pass = parse_pass and ok and count > 0
        parse_details.append(f"{path.name}:{count if ok else detail}")
    validations.append(base_row(validation_id="VAL2196_12_csv_parse", status="PASS" if parse_pass else "FAIL", detail="; ".join(parse_details)))

    copies = rows_by_name["branch_copies"]
    validations.append(base_row(validation_id="VAL2196_13_branch_copies", status="PASS" if copies and all(row["copied"] for row in copies) else "FAIL", detail=";".join(str(row["target_path"]) for row in copies)))

    validations.append(base_row(validation_id="VAL2196_14_formalization_clean", status="PASS" if not formalization_has_2196_artifacts() else "FAIL", detail="formalization-workbench has no 2196 artifacts"))

    remove_pycache()
    validations.append(base_row(validation_id="VAL2196_15_pycache_absent", status="PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL", detail=str(ROOT / "scripts" / "__pycache__")))

    overall = "PASS" if all(row["status"] == "PASS" for row in validations) else "FAIL"
    validations.append(base_row(validation_id="VAL2196_OVERALL", status=overall, detail="2196 derives the K_X normalization split as a symbolic contract, rejects unity/linear shortcuts, blocks numeric R10 claims, and selects parent Z_X residue next"))
    return validations


def render_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> str:
    return "\n".join(
        [
            "# 2196 - Y5/R2FR KX Normalization Or Beta-Leg Source First Row",
            "",
            "## Current Verdict",
            "",
            "2196 makes the coupling gap sharper rather than pretending it is solved. The best current R10 finite-exchange normalization is:",
            "",
            "`K_X^R10(lambda)=s_X*F_ST(lambda)*Pi_R10(lambda)/(4*pi*G_N*Z_X)`",
            "",
            "in mass-normalized beta units, giving:",
            "",
            "`alpha_predicted(lambda)=K_X^R10(lambda)*beta_s(lambda)*beta_t(lambda)+epsilon_tail(lambda)`.",
            "",
            "That is real progress, but it is still **not numeric**. The corpus does not yet parent-sign `Z_X`, does not source the R10 extended-body form factor `F_ST`, does not source the harmonic projection `Pi_R10`, and does not bound the absolute tail envelope. So `K_X=1`, `F_ST=1`, `Pi_R10=1`, linear `c_g`, and tail-cancellation shortcuts are explicitly rejected.",
            "",
            "## Source Register",
            "",
            md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "",
            "## KX Normalization Derivation",
            "",
            md_table(rows_by_name["normalization_derivation"], ["derivation_id", "step", "formula", "required_convention", "result", "missing_for_numeric", "valid_for_claim"]),
            "",
            "## KX Factor Status",
            "",
            md_table(rows_by_name["factor_status"], ["factor_id", "factor", "inherited_source", "inherited_status", "current_status", "numeric_ready", "consequence", "valid_for_claim"]),
            "",
            "## Shortcut Quarantine",
            "",
            md_table(rows_by_name["shortcut_quarantine"], ["shortcut_id", "shortcut", "verdict", "reason", "allowed_replacement", "score_ready", "valid_for_claim"]),
            "",
            "## Pressure Row Update",
            "",
            md_table(rows_by_name["pressure_update"], ["pressure_id", "arena", "target_lambda_m", "alpha_bound_review_candidate", "kx_split_formula", "normalization_aware_bound", "numeric_beta_bound_status", "missing_for_numeric", "score_ready", "valid_for_claim"]),
            "",
            "## Fallback Queue",
            "",
            md_table(rows_by_name["fallback_queue"], ["queue_id", "priority", "target", "objective", "why_first", "success_condition", "fallback_if_failed", "valid_for_claim"]),
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
            "This checkpoint does take a leap forward, but not the dishonest leap. It turns the vague `coupling` problem into a denominator-and-projection problem. If the next branch can parent-own `Z_X`, we have the first genuinely physical normalization handle. If it cannot, the theory must admit the finite local response branch is closure-only until a parent action supplies it.",
            "",
            "Best next attack: derive/source `Z_X` and the sign/unit convention from the parent local action. If `Z_X` fails, move immediately to a beta-leg source/test acquisition row rather than circling `K_X` again.",
            "",
        ]
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "normalization_derivation": normalization_derivation_rows(),
        "factor_status": factor_status_rows(),
        "shortcut_quarantine": shortcut_quarantine_rows(),
        "pressure_update": pressure_update_rows(),
        "fallback_queue": fallback_queue_rows(),
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
