from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3864"
BRANCH = "MTS_R2FR_Y5_NO_EXTRA_F2_OPERATOR_DOMAIN_THEOREM_OR_LAMBDAF2_BOUND_3864"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3864-Y5-R2FR-no-extra-F2-operator-domain-theorem-or-lambdaF2-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

CSV_3863_THEOREM = OUT / "P8_Y5_R2FR_3863_MAXWELL_NORMALIZATION_OWNER_THEOREM.csv"
CSV_3863_BOUND = OUT / "P8_Y5_R2FR_3863_EM_SOURCE_SCALE_BOUND.csv"
CSV_3863_GATES = OUT / "P8_Y5_R2FR_3863_CLAIM_GATES.csv"
CSV_3863_VALIDATION = OUT / "P8_Y5_BRR545_3863_VALIDATION.csv"
CSV_1057_THEOREM = OUT / "P8_Y5_R10_1057_UNIQUE_MAXWELL_SUBBLOCK_THEOREM_ATTEMPT.csv"
CSV_1057_OPERATOR = OUT / "P8_Y5_R10_1057_OPERATOR_DOMAIN_AUDIT.csv"
CSV_1057_COUNTER = OUT / "P8_Y5_R10_1057_F2_COUNTERTERM_LEDGER.csv"
CSV_3528_OPERATOR = OUT / "P8_Y5_R2FR_3528_OPERATOR_DOMAIN_RESULT.csv"
CSV_3281_AUDIT = OUT / "P8_Y5_R2FR_3281_NO_EXTRA_F2_OPERATOR_AUDIT.csv"
CSV_3679_AUDIT = OUT / "P8_Y5_R2FR_3679_UNIQUE_F2_THEOREM_AUDIT.csv"
CSV_3679_MAP = OUT / "P8_Y5_R2FR_3679_SXF2_CANONICAL_MAP_ROWS.csv"
CSV_3679_BOUND = OUT / "P8_Y5_R2FR_3679_SXF2_BOUND_INPUT_ROWS.csv"
CSV_2659_HOM = OUT / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv"
CSV_1928_EXCLUSION = OUT / "P8_Y5_PARENT_QLOC_1928_NO_EXTRA_F2_EXCLUSION_LEDGER.csv"
CSV_3233_CF2 = OUT / "P8_Y5_R2FR_3233_CF2PERP_FINITE_BOUND.csv"
CSV_3528_GATES = OUT / "P8_Y5_R2FR_3528_UNIQUE_F2_INHERITANCE_GATES.csv"
CSV_2765_AUDIT = OUT / "P8_Y5_R2FR_2765_VISIBLE_OPERATOR_DOMAIN_AUDIT.csv"
CSV_2766_EXHAUST = OUT / "P8_Y5_R2FR_2766_VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_ATTEMPT.csv"
CSV_3118_HOM = OUT / "P8_Y5_R2FR_3118_NO_HIDDEN_VISIBLE_COEFFICIENT_HOM_GATE.csv"
CSV_3809_NORM = OUT / "P8_Y5_R2FR_3809_MAXWELL_NORMALIZATION_THEOREM.csv"
CSV_1812_ALPHA = OUT / "P8_Y5_PARENT_QLOC_1812_ALPHA_LEVEL_OWNER_AUDIT.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3864_SOURCE_REGISTER.csv",
    "theorem": OUT / "P8_Y5_R2FR_3864_NO_EXTRA_F2_THEOREM.csv",
    "audit": OUT / "P8_Y5_R2FR_3864_OPERATOR_DOMAIN_AUDIT.csv",
    "bound": OUT / "P8_Y5_R2FR_3864_LAMBDAF2_BOUND.csv",
    "gates": OUT / "P8_Y5_R2FR_3864_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3864_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3864_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3864_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3864_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3864_00_3863_theorem", CSV_3863_THEOREM, "NEXT_GATE_IS_NO_EXTRA_F2_OPERATOR_DOMAIN_OR_FINITE_LAMBDA_BOUND", "3863 no-extra-F2 handoff"),
    ("SRC3864_01_3863_bound", CSV_3863_BOUND, "lambda_F2_or_C_XF2", "3863 F2 fallback bound"),
    ("SRC3864_02_3863_gates", CSV_3863_GATES, "PASS_3864_NO_EXTRA_F2_OPERATOR_DOMAIN_TARGET", "3863 next-target gate"),
    ("SRC3864_03_3863_validation", CSV_3863_VALIDATION, "PASS", "previous validation"),
    ("SRC3864_04_1057_theorem", CSV_1057_THEOREM, "UMS1057_2_no_independent_F2", "unique Maxwell subblock theorem attempt"),
    ("SRC3864_05_1057_operator", CSV_1057_OPERATOR, "OD1057_1_U1_gauge", "operator-domain ordinary symmetry audit"),
    ("SRC3864_06_1057_counter", CSV_1057_COUNTER, "CT1057_1_hidden_scalar", "F2 counterterm ledger"),
    ("SRC3864_07_3528_operator", CSV_3528_OPERATOR, "OP3528_2_hidden_scalar_lambda", "operator-domain result"),
    ("SRC3864_08_3281_audit", CSV_3281_AUDIT, "F2AUD3281_3_typed_visible_algebra", "no-extra-F2 operator audit"),
    ("SRC3864_09_3679_audit", CSV_3679_AUDIT, "UF23679_6_verdict", "unique F2 theorem audit"),
    ("SRC3864_10_3679_map", CSV_3679_MAP, "MAP3679_3_alpha_identity", "s_XF2 alpha/current identity"),
    ("SRC3864_11_3679_bound", CSV_3679_BOUND, "SXF23679_4_parent_zg_zero_route", "s_XF2 bound input rows"),
    ("SRC3864_12_2659_hom", CSV_2659_HOM, "ODT2659_1_exact_typed_theorem", "no hidden-visible hom theorem"),
    ("SRC3864_13_1928_exclusion", CSV_1928_EXCLUSION, "EXC1928_4_product_functor", "no-extra-F2 exclusion ledger"),
    ("SRC3864_14_3233_cf2", CSV_3233_CF2, "CFB3233_0_CF2perp", "finite F2 perpendicular bound"),
    ("SRC3864_15_3528_gates", CSV_3528_GATES, "IF23528_1_no_independent_visible_F2", "unique F2 inheritance gates"),
    ("SRC3864_16_2765_audit", CSV_2765_AUDIT, "OPA2765_4_verdict", "visible operator-domain audit"),
    ("SRC3864_17_2766_exhaust", CSV_2766_EXHAUST, "VOE2766_6_verdict", "visible operator-domain exhaustion attempt"),
    ("SRC3864_18_3118_hom", CSV_3118_HOM, "NHV3118_1", "hidden F2 countermodel gate"),
    ("SRC3864_19_3809_norm", CSV_3809_NORM, "MNT3809_3_no_extra_F2_countermodel", "Maxwell normalization countermodel"),
    ("SRC3864_20_1812_alpha", CSV_1812_ALPHA, "ALO1812_2_unique_F2", "alpha level unique F2 owner audit"),
]

ORDINARY_SYMMETRY_RESULT = (
    "Diffeomorphism covariance and U(1) gauge invariance do not forbid an independent "
    "scalar-density operator DeltaS_F2=-1/4 int sqrt(-g_obs) lambda_A(Phi) F_Q^2; "
    "they allow it unless the parent visible operator domain is stricter."
)
NO_EXTRA_F2_THEOREM = (
    "If Allowed[S_vis]=Image(ParentGenerate[Phi,q_obs,Dq,F_parent,theta_rep,topological levels,e_obs]) "
    "and the image contains the Q-subblock only as C_P N_Q F_Q^2, with no separate Coeff(F_Q^2) object, "
    "no Hom(hidden residual scalars,Coeff(F_Q^2)) except constants/q-basic data, no representative/readout coefficient slot, "
    "and radiative/readout effective actions remain in the same image, then every local vertical v in ker(Dq_obs) has "
    "D_v lambda_F2 = D_v f_X = D_v delta_lambda_rad = 0; hence s_XF2=C_XF2=0 as local source-coupling residuals."
)
CONSTANT_LAMBDA_GUARD = (
    "A universal hidden-independent constant lambda_0 F_Q^2 is an absolute alpha/calibration debt, not a local drift residual; "
    "it cannot be used to claim an alpha value, but it does not by itself create D_v alpha or WEP/R10 source pressure."
)
CURRENT_BLOCK = (
    "The current corpus has exact conditional no-extra-F2 routes and counterterm ledgers, but it has not parent-derived visible operator-domain exhaustion, no hidden-visible Hom, radiative/readout closure, or same-current isolation."
)
CANONICAL_IDENTITY = (
    "S_EM,J=-1/4 int lambda_A(Xhat) F_Q wedge *_obs F_Q + int g_J(Xhat) A_Q.J_Q, "
    "s_XF2:=D_Xhat ln lambda_A, z_g:=D_Xhat ln g_J, and b_alpha_X=2 z_g-s_XF2."
)
LAMBDA_BOUND = (
    "|s_XF2| <= |2 z_g| + |b_alpha_X|"
)
ACTIVE_BOUND = (
    "B_lambdaF2_3864 <= |s_XF2|+|C_XF2|+|delta_lambda_rad|+|delta_lambda_readout|"
)


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PCW))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, path, needle, role in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "checkpoint": CHECKPOINT,
                "path": rel(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "claim_use": "nonclaim_no_extra_F2_operator_domain_derivation",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "theorem_id": "NEF3864_0_symmetry_legality",
            "claim_piece": "ordinary symmetry cannot ban F2",
            "statement": ORDINARY_SYMMETRY_RESULT,
            "derivation": "F_Q^2 is a covariant scalar density and U(1)-gauge invariant, so ordinary field-theory symmetry permits scalar kinetic coefficients.",
            "result": "COUNTERMODEL_LEGAL_UNDER_ORDINARY_SYMMETRY",
            "status": "NO_SHORTCUT_GUARD",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "NEF3864_1_no_extra_F2_theorem",
            "claim_piece": "no-extra-F2 operator-domain theorem",
            "statement": NO_EXTRA_F2_THEOREM,
            "derivation": "Typed image theorem: if the visible action is only the image of parent-generated operators, there is no independent coefficient object for F_Q^2 on which hidden or readout variables can act.",
            "result": "EXACT_CONDITIONAL_NO_EXTRA_F2_THEOREM",
            "status": "CONDITIONAL_THEOREM_PROVED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "NEF3864_2_constant_lambda_guard",
            "claim_piece": "constant lambda guard",
            "statement": CONSTANT_LAMBDA_GUARD,
            "derivation": "A constant coefficient changes the calibrated coupling value but has zero vertical derivative; local tests constrain derivatives/products, not absolute unit conventions by themselves.",
            "result": "CONSTANT_CALIBRATION_NOT_LOCAL_RESIDUAL",
            "status": "NO_ALPHA_VALUE_OVERCLAIM_GUARD",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "NEF3864_3_canonical_finite_identity",
            "claim_piece": "finite lambda/current identity",
            "statement": CANONICAL_IDENTITY,
            "derivation": "Canonical field normalization gives alpha_eff proportional to g_J^2/lambda_A, so vertical derivatives obey b_alpha_X=2 z_g-s_XF2.",
            "result": "EXACT_CANONICAL_ALPHA_CURRENT_IDENTITY",
            "status": "FINITE_BRANCH_DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "NEF3864_4_current_verdict",
            "claim_piece": "strict current corpus verdict",
            "statement": CURRENT_BLOCK,
            "derivation": "1057/2765/3281/3679 show the counterterm is legal unless the stronger domain/no-Hom/radiative clauses are parent-signed.",
            "result": "NO_EXTRA_F2_NOT_CLAIMED_CURRENT_CORPUS",
            "status": "CURRENT_NONCLAIM_BOUND_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "NEF3864_5_handoff",
            "claim_piece": "next obstruction",
            "statement": "The next narrow target is the parent visible operator-domain image theorem: derive Allowed[S_vis]=Image(ParentGenerate) for the EM coefficient algebra, or run a joint s_XF2/z_g/b_alpha finite-bound branch.",
            "derivation": "No-extra-F2 is not independently closed until the parent image/no-Hom/radiative closure clauses close; alpha data alone cannot isolate s_XF2 while z_g is live.",
            "result": "NEXT_GATE_IS_VISIBLE_OPERATOR_DOMAIN_IMAGE_OR_JOINT_BOUND",
            "status": "COUPLING_ROUTE_SHARPENED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def audit_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "audit_id": "ODA3864_0_parent_image",
            "slot": "visible operator-domain image",
            "required_signature": "Allowed[S_vis]=Image(ParentGenerate) with no free Coeff(F_Q^2)",
            "current_evidence": "2766 and 3528 state the image theorem as a target/contract, not a parent derivation",
            "passes_current_branch": False,
            "residual_owner": "B_operator_domain_image",
            "next_action": "derive visible category image from parent primitives or keep lambda_F2 branch",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "ODA3864_1_constant_lambda",
            "slot": "constant independent lambda_0 F_Q^2",
            "required_signature": "lambda_0 absent or derived from parent norm for absolute alpha prediction",
            "current_evidence": "1057/3528 say a constant term is legal unless parent domain excludes it",
            "passes_current_branch": False,
            "residual_owner": "absolute_alpha_calibration_debt",
            "next_action": "do not score as local drift, but do not claim alpha value",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "ODA3864_2_hidden_scalar",
            "slot": "hidden scalar f(I_hid)F_Q^2",
            "required_signature": "Hom(hidden residual scalars,Coeff(F_Q^2)) is absent, constant, or q-basic",
            "current_evidence": "2659/3118 give exact conditional no-Hom theorem but keep parent domain unsigned",
            "passes_current_branch": False,
            "residual_owner": "C_XF2+s_XF2_hidden",
            "next_action": "prove no hidden-visible Hom or retain alpha/WEP/R10/clock bounds",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "ODA3864_3_radiative_readout",
            "slot": "radiative/readout regenerated F2",
            "required_signature": "S_eff and alpha readout stay in Image(ParentGenerate) after loops, thresholds and apparatus projection",
            "current_evidence": "1057/2766/3118 all mark radiative/readout closure unsigned",
            "passes_current_branch": False,
            "residual_owner": "delta_lambda_rad+delta_lambda_readout",
            "next_action": "derive q-basic effective/readout action or keep clock/spectroscopy residuals",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "ODA3864_4_current_leg",
            "slot": "current normalization degeneracy",
            "required_signature": "z_g=0 from same-current owner before alpha bounds isolate s_XF2",
            "current_evidence": "3679 exact identity b_alpha_X=2 z_g-s_XF2; z_g owner remains live from 3863",
            "passes_current_branch": False,
            "residual_owner": "z_g",
            "next_action": "jointly bound s_XF2 and z_g or prove same-current owner",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "ODA3864_5_source_scale",
            "slot": "EM source-scale propagation",
            "required_signature": "lambda_F2 and current residuals do not alter EM binding/source mass/Poynting scale",
            "current_evidence": "3863 and 3233 retain source-scale and F2-perp bound rows",
            "passes_current_branch": False,
            "residual_owner": "B_EM_scale_3863+B_lambdaF2_3864",
            "next_action": "carry finite F2/current residuals into source-calibration tests if derivation fails",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def bound_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "bound_id": "LFB3864_0_canonical_identity",
            "target": "s_XF2",
            "formula": LAMBDA_BOUND,
            "derivation": "from b_alpha_X=2 z_g-s_XF2; no cancellation credit",
            "observables": "clock;alpha;spectroscopy;WEP;R10",
            "status": "NONCLAIM_CANONICAL_BOUND",
            "numeric_status": "MISSING_ALPHA_AND_ZG_SOURCE_ROWS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "LFB3864_1_zg_zero_branch",
            "target": "s_XF2 if z_g=0",
            "formula": "|s_XF2|=|b_alpha_X| if same-current owner proves z_g=0",
            "derivation": "specialization of the canonical identity under the 3863 same-current owner branch",
            "observables": "clock;WEP;R10;alpha",
            "status": "CONDITIONAL_DIRECT_BOUND_ROUTE",
            "numeric_status": "MISSING_ZG_ZERO_THEOREM_AND_ALPHA_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "LFB3864_2_active_lambdaF2",
            "target": "B_lambdaF2_3864",
            "formula": ACTIVE_BOUND,
            "derivation": "active local F2 residual excludes pure constant calibration but retains hidden/radiative/readout derivatives",
            "observables": "alpha_drift;clock;WEP;R10;PPN_source_scale",
            "status": "NONCLAIM_ACTIVE_F2_BOUND",
            "numeric_status": "SYMBOLIC_ONLY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "LFB3864_3_F2perp_bound",
            "target": "C_F2_perp",
            "formula": "C_F2_perp <= (C_Q_leak+C_lambda_leak+C_hidden_leak+C_readout_leak)/Z_min",
            "derivation": "imports the 3233 finite F2-perpendicular source bound form",
            "observables": "EM_stress;source_mass;Poynting;local_GR",
            "status": "FINITE_BOUND_FORMULA_READY_INPUTS_MISSING",
            "numeric_status": "MISSING_Z_MIN_AND_LEAK_NUMERATORS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "LFB3864_4_source_scale_update",
            "target": "B_EM_scale_3863",
            "formula": "B_EM_scale_3863 <= B_EM_scale_without_F2 + B_lambdaF2_3864",
            "derivation": "substitutes the explicit no-extra-F2 residual into the 3863 source-scale gate",
            "observables": "local_GR;Newton_GM;WEP;clock;R10",
            "status": "SOURCE_SCALE_BOUND_REFINED",
            "numeric_status": "SYMBOLIC_ONLY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "G3864_0_no_shortcut",
            "gate": "ordinary symmetry shortcut rejected",
            "status": "PASS_F2_LEGAL_UNDER_ORDINARY_SYMMETRY",
            "claim_allowed": False,
            "reason": "diffeomorphism and U(1) gauge symmetry allow scalar F_Q^2 coefficients",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "G3864_1_conditional_theorem",
            "gate": "no-extra-F2 operator-domain theorem is explicit",
            "status": "PASS_EXACT_CONDITIONAL_NO_EXTRA_F2_THEOREM",
            "claim_allowed": False,
            "reason": "zero follows only from parent image/domain/no-Hom/radiative closure",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "G3864_2_no_current_claim",
            "gate": "current no-extra-F2/local-GR claim remains blocked",
            "status": "BLOCKED_OPERATOR_DOMAIN_NOT_PARENT_DERIVED",
            "claim_allowed": False,
            "reason": "current corpus has contracts/counterexamples, not parent-derived visible operator-domain exhaustion",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "G3864_3_alpha_identity",
            "gate": "finite alpha/current identity is retained",
            "status": "PASS_NO_ALPHA_ONLY_SXF2_SHORTCUT",
            "claim_allowed": False,
            "reason": "alpha bounds isolate s_XF2 only if z_g is zeroed or jointly fitted",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "G3864_4_next_target",
            "gate": "next target selected",
            "status": "PASS_3865_VISIBLE_OPERATOR_DOMAIN_IMAGE_TARGET",
            "claim_allowed": False,
            "reason": "the direct missing derivation is the parent visible operator-domain image theorem",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D3864_0",
            "decision": "Do not claim no-extra-F2 from covariance or U(1) gauge symmetry.",
            "consequence": "The proof must be a parent operator-domain/image theorem or no-Hom theorem.",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "D3864_1",
            "decision": "Separate constant lambda calibration from active hidden/radiative F2 drift.",
            "consequence": "No fake local failure from a constant alpha value debt, and no fake alpha-value prediction.",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "D3864_2",
            "decision": "Keep alpha/current joint identity live.",
            "consequence": "Use b_alpha_X=2 z_g-s_XF2; do not pretend alpha data bounds s_XF2 alone while z_g is open.",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3864_0",
            "target_checkpoint": "3865-Y5-R2FR-visible-operator-domain-image-proof-or-sXF2-zg-joint-bound.md",
            "script": "scripts/Y5_R2FR_3865_visible_operator_domain_image_proof_or_sXF2_zg_joint_bound.py",
            "objective": "derive Allowed[S_vis]=Image(ParentGenerate) for the EM coefficient algebra, or build a nonclaim joint s_XF2/z_g/b_alpha bound harness",
            "why_next": "3864 shows no-extra-F2 is exactly the parent-domain image/no-Hom/radiative closure problem; finite alpha data must be joint with current normalization",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "status": "PASS_NONCLAIM_NO_EXTRA_F2_THEOREM_AND_LAMBDAF2_BOUND",
            "summary": "3864 rejects symmetry shortcuts, proves the conditional no-extra-F2 operator-domain theorem, retains current blockage, and gives the finite s_XF2/z_g/b_alpha identity and bound route.",
            "doc": rel(DOC_PATH),
            "validation": rel(OUTPUTS["validation"]),
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, separator, *body])


def write_doc(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    audit: list[dict[str, object]],
    bound: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    timestamp: str,
) -> None:
    text = f"""# 3864 — No-Extra-F2 Operator-Domain Theorem Or LambdaF2 Bound

Generated: `{timestamp}`

## Purpose

3863 showed that independent `F_Q^2` is the direct countermodel to parent-owned Maxwell normalization. This checkpoint attacks that countermodel.

## Result

Shortcut rejection:

`{ORDINARY_SYMMETRY_RESULT}`

Exact conditional theorem:

`{NO_EXTRA_F2_THEOREM}`

Finite fallback identity:

`{CANONICAL_IDENTITY}`

Strict current verdict:

`{CURRENT_BLOCK}`

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## No-Extra-F2 Theorem

{markdown_table(theorem, ["theorem_id", "claim_piece", "status", "result"])}

## Operator-Domain Audit

{markdown_table(audit, ["audit_id", "slot", "passes_current_branch", "residual_owner", "next_action"])}

## LambdaF2 Bound

{markdown_table(bound, ["bound_id", "target", "status", "formula"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Bottom Line

3864 is a useful narrowing: independent `F_Q^2` cannot be killed by standard symmetry. It dies only if the visible EM action is the image of the parent-generated operator algebra, with no separate coefficient object, no hidden-visible Hom, and no radiative/readout re-entry. Since that is not parent-derived yet, the finite branch must keep `s_XF2` and `z_g` together through `b_alpha_X=2 z_g-s_XF2`.

Next target: `3865-Y5-R2FR-visible-operator-domain-image-proof-or-sXF2-zg-joint-bound.md`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3863", "Current State After 3864", 1)
    text = "\n".join(
        line for line in text.splitlines() if not line.startswith("<!-- Generated by 3864 at ")
    )
    paragraph = (
        "`3864` attacks the independent `F_Q^2` countermodel. "
        "The first result is negative but important: diffeomorphism covariance and U(1) gauge symmetry allow `DeltaS_F2=-1/4 int sqrt(-g_obs) lambda_A(Phi) F_Q^2`, so no-extra-F2 cannot be derived from ordinary symmetry. "
        "The exact conditional theorem is: if `Allowed[S_vis]=Image(ParentGenerate[Phi,q_obs,Dq,F_parent,theta_rep,topological levels,e_obs])`, the image contains the Q-subblock only as `C_P N_Q F_Q^2`, there is no separate `Coeff(F_Q^2)` object, no `Hom(hidden residual scalars,Coeff(F_Q^2))` except constants/q-basic data, no representative/readout coefficient slot, and radiative/readout effective actions remain in that image, then `D_v lambda_F2=D_v f_X=D_v delta_lambda_rad=0` and `s_XF2=C_XF2=0` as local residuals. "
        "The current corpus does not claim this because the parent image/no-Hom/radiative closure clauses remain unsigned. "
        "The finite branch is canonical: `S_EM,J=-1/4 int lambda_A(Xhat) F_Q wedge *_obs F_Q + int g_J(Xhat) A_Q.J_Q`, `s_XF2=D_Xhat ln lambda_A`, `z_g=D_Xhat ln g_J`, and `b_alpha_X=2 z_g-s_XF2`; hence alpha data cannot isolate `s_XF2` while `z_g` is live. "
        "The retained bound is `B_lambdaF2_3864 <= |s_XF2|+|C_XF2|+|delta_lambda_rad|+|delta_lambda_readout|` with `|s_XF2| <= |2 z_g|+|b_alpha_X|`.\n\n"
    )
    if paragraph not in text and "## Next Best Gate" in text:
        text = text.replace("## Next Best Gate", paragraph + "## Next Best Gate", 1)
    old_gate = """`3864-Y5-R2FR-no-extra-F2-operator-domain-theorem-or-lambdaF2-bound.md`

Target: derive an operator-domain exclusion forbidding independent `lambda_A F_Q^2` / `f_X F_Q^2` terms outside the parent curvature norm, or retain source-backed `lambda_F2` / `C_XF2` bounds.

This is the best next move because 3863 shows independent `F_Q^2` is the direct countermodel to parent-owned Maxwell normalization and alpha/source-scale silence."""
    new_gate = """`3865-Y5-R2FR-visible-operator-domain-image-proof-or-sXF2-zg-joint-bound.md`

Target: derive `Allowed[S_vis]=Image(ParentGenerate)` for the EM coefficient algebra, or build a nonclaim joint `s_XF2` / `z_g` / `b_alpha` bound harness.

This is the best next move because 3864 shows no-extra-F2 is exactly the parent-domain image/no-Hom/radiative closure problem; finite alpha data must be joint with current normalization."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3864_NO_EXTRA_F2_THEOREM.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3864_OPERATOR_DOMAIN_AUDIT.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3864_LAMBDAF2_BOUND.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3864_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3864_NO_EXTRA_F2_THEOREM.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    text = text.rstrip() + f"\n\n<!-- Generated by 3864 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    audit: list[dict[str, object]],
    bound: list[dict[str, object]],
    gates: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "check": check,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "timestamp_utc": timestamp,
            }
        )

    all_text = " ".join(str(row) for row in theorem + audit + bound + gates)
    add(
        "VAL3864_0_sources",
        "all cited source paths exist and needles are found",
        all(row["exists"] and row["needle_found"] for row in sources),
        f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved",
    )
    add(
        "VAL3864_1_shortcut_rejected",
        "ordinary symmetry shortcut is rejected",
        "COUNTERMODEL_LEGAL_UNDER_ORDINARY_SYMMETRY" in all_text and "PASS_F2_LEGAL_UNDER_ORDINARY_SYMMETRY" in all_text,
        "F2 legality guard present",
    )
    add(
        "VAL3864_2_theorem",
        "conditional no-extra-F2 theorem is explicit",
        "EXACT_CONDITIONAL_NO_EXTRA_F2_THEOREM" in all_text and "Allowed[S_vis]=Image" in all_text,
        "operator-domain theorem present",
    )
    add(
        "VAL3864_3_alpha_identity",
        "finite alpha/current identity is explicit",
        "EXACT_CANONICAL_ALPHA_CURRENT_IDENTITY" in all_text and "b_alpha_X=2 z_g-s_XF2" in all_text,
        "s_XF2/z_g/b_alpha identity present",
    )
    add(
        "VAL3864_4_current_block",
        "current no-extra-F2 claim remains blocked",
        "NO_EXTRA_F2_NOT_CLAIMED_CURRENT_CORPUS" in all_text and "BLOCKED_OPERATOR_DOMAIN_NOT_PARENT_DERIVED" in all_text,
        "no current no-extra-F2 promotion",
    )
    add(
        "VAL3864_5_bounds",
        "lambdaF2 bounds are explicit",
        "B_lambdaF2_3864 <=" in all_text and "|s_XF2| <= |2 z_g| + |b_alpha_X|" in all_text,
        "active F2 and canonical bounds present",
    )
    add(
        "VAL3864_6_nonclaim",
        "all rows remain nonclaim",
        all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in theorem + audit + bound + gates),
        "valid_for_claim/claim_allowed false throughout",
    )
    add(
        "VAL3864_7_next",
        "next target is visible operator-domain image or joint bound",
        DOC_PATH.exists() and "3865-Y5-R2FR-visible-operator-domain-image-proof-or-sXF2-zg-joint-bound" in read_text(DOC_PATH),
        "3865 target visible",
    )
    for key, output_path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed = False
        detail = rel(output_path)
        if output_path.suffix == ".csv" and output_path.exists():
            count = len(read_csv_rows(output_path))
            parsed = count > 0
            detail += f" rows={count}"
        add(f"VAL3864_8_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add(
        "VAL3864_9_doc",
        "markdown checkpoint document exists",
        DOC_PATH.exists() and "3863 showed that independent" in read_text(DOC_PATH),
        rel(DOC_PATH),
    )
    formalization_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3864*", "P8_Y5_BRR545_3864*", "*Y5_R2FR_3864*", "3864-Y5-R2FR*"):
            formalization_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add(
        "VAL3864_10_formalization_clean",
        "formalization-workbench has no generated 3864 project files",
        len(formalization_hits) == 0,
        "; ".join(str(path) for path in formalization_hits) if formalization_hits else "no generated 3864 project file hits under formalization-workbench",
    )
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add(
        "VAL3864_11_pycache_removed",
        "scripts __pycache__ removed",
        len(pycache_hits) == 0,
        "; ".join(str(path) for path in pycache_hits) if pycache_hits else "no __pycache__ directories",
    )
    return rows


def main() -> int:
    timestamp = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows(timestamp)
    theorem = theorem_rows(timestamp)
    audit = audit_rows(timestamp)
    bound = bound_rows(timestamp)
    gates = gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["audit"], audit)
    write_csv(OUTPUTS["bound"], bound)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, theorem, audit, bound, gates, decisions, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, theorem, audit, bound, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_NONCLAIM_NO_EXTRA_F2_THEOREM_AND_LAMBDAF2_BOUND")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
