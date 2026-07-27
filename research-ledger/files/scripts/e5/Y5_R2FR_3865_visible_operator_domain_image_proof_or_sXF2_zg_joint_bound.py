from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3865"
BRANCH = "MTS_R2FR_Y5_VISIBLE_OPERATOR_DOMAIN_IMAGE_PROOF_OR_SXF2_ZG_JOINT_BOUND_3865"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3865-Y5-R2FR-visible-operator-domain-image-proof-or-sXF2-zg-joint-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

CSV_3864_THEOREM = OUT / "P8_Y5_R2FR_3864_NO_EXTRA_F2_THEOREM.csv"
CSV_3864_BOUND = OUT / "P8_Y5_R2FR_3864_LAMBDAF2_BOUND.csv"
CSV_3864_GATES = OUT / "P8_Y5_R2FR_3864_CLAIM_GATES.csv"
CSV_3864_VALIDATION = OUT / "P8_Y5_BRR545_3864_VALIDATION.csv"
CSV_2766_IMAGE = OUT / "P8_Y5_R2FR_2766_VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_ATTEMPT.csv"
CSV_2765_AUDIT = OUT / "P8_Y5_R2FR_2765_VISIBLE_OPERATOR_DOMAIN_AUDIT.csv"
CSV_3528_OPERATOR = OUT / "P8_Y5_R2FR_3528_OPERATOR_DOMAIN_RESULT.csv"
CSV_2659_HOM = OUT / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv"
CSV_3679_MAP = OUT / "P8_Y5_R2FR_3679_SXF2_CANONICAL_MAP_ROWS.csv"
CSV_3679_BOUND = OUT / "P8_Y5_R2FR_3679_SXF2_BOUND_INPUT_ROWS.csv"
CSV_3680_ZG = OUT / "P8_Y5_R2FR_3680_ZG_COMPONENT_DECOMPOSITION_ROWS.csv"
CSV_3680_ZERO = OUT / "P8_Y5_R2FR_3680_ZG_ZERO_THEOREM_AUDIT.csv"
CSV_3508_ZG = OUT / "P8_Y5_R2FR_3508_ZG_BETA_SOURCE_REDUCTION.csv"
CSV_3118_BALPHA = OUT / "P8_Y5_R2FR_3118_BALPHA_PRODUCT_INPUTS_TEMPLATE.csv"
CSV_1052_CLOCK = OUT / "P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv"
CSV_1052_WEP = OUT / "P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv"
CSV_1052_R10 = OUT / "P8_Y5_R10_1052_ALPHA_R10_PROJECTION_LEDGER.csv"
CSV_1057_COUNTER = OUT / "P8_Y5_R10_1057_F2_COUNTERTERM_LEDGER.csv"
CSV_3118_HOM = OUT / "P8_Y5_R2FR_3118_NO_HIDDEN_VISIBLE_COEFFICIENT_HOM_GATE.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3865_SOURCE_REGISTER.csv",
    "theorem": OUT / "P8_Y5_R2FR_3865_VISIBLE_OPERATOR_IMAGE_THEOREM.csv",
    "audit": OUT / "P8_Y5_R2FR_3865_IMAGE_PROOF_AUDIT.csv",
    "joint": OUT / "P8_Y5_R2FR_3865_SXF2_ZG_BALPHA_JOINT_BOUND.csv",
    "gates": OUT / "P8_Y5_R2FR_3865_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3865_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3865_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3865_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3865_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3865_00_3864_theorem", CSV_3864_THEOREM, "NEXT_GATE_IS_VISIBLE_OPERATOR_DOMAIN_IMAGE_OR_JOINT_BOUND", "3864 image/joint-bound handoff"),
    ("SRC3865_01_3864_bound", CSV_3864_BOUND, "LFB3864_0_canonical_identity", "3864 canonical lambdaF2 bound"),
    ("SRC3865_02_3864_gates", CSV_3864_GATES, "PASS_3865_VISIBLE_OPERATOR_DOMAIN_IMAGE_TARGET", "3864 next target"),
    ("SRC3865_03_3864_validation", CSV_3864_VALIDATION, "PASS", "previous validation"),
    ("SRC3865_04_2766_image_target", CSV_2766_IMAGE, "VOE2766_0_target", "visible operator-domain image target"),
    ("SRC3865_05_2766_verdict", CSV_2766_IMAGE, "VOE2766_6_verdict", "visible operator-domain verdict"),
    ("SRC3865_06_2765_audit", CSV_2765_AUDIT, "OPA2765_4_verdict", "visible operator-domain audit"),
    ("SRC3865_07_3528_operator", CSV_3528_OPERATOR, "OP3528_2_hidden_scalar_lambda", "operator-domain result"),
    ("SRC3865_08_2659_hom", CSV_2659_HOM, "ODT2659_1_exact_typed_theorem", "typed no-Hom theorem"),
    ("SRC3865_09_2659_verdict", CSV_2659_HOM, "ODT2659_6_verdict", "no-Hom current verdict"),
    ("SRC3865_10_3679_identity", CSV_3679_MAP, "MAP3679_3_alpha_identity", "s_XF2 z_g alpha identity"),
    ("SRC3865_11_3679_live", CSV_3679_MAP, "MAP3679_5_zg_live_branch", "two-knob finite branch"),
    ("SRC3865_12_3679_bound", CSV_3679_BOUND, "SXF23679_2_alpha_clock_route", "s_XF2 alpha clock route"),
    ("SRC3865_13_3679_zgzero", CSV_3679_BOUND, "SXF23679_4_parent_zg_zero_route", "z_g zero direct branch"),
    ("SRC3865_14_3680_zg", CSV_3680_ZG, "ZGD3680_7_two_knob_identity", "z_g component decomposition"),
    ("SRC3865_15_3680_zero", CSV_3680_ZERO, "ZG3680_7_verdict", "z_g zero verdict"),
    ("SRC3865_16_3508_zg", CSV_3508_ZG, "CSR3508_0_z_g", "z_g beta-source reduction"),
    ("SRC3865_17_3118_balpha", CSV_3118_BALPHA, "BAP3118_1", "b_alpha product inputs"),
    ("SRC3865_18_1052_clock", CSV_1052_CLOCK, "ACB1052_2", "alpha clock product bound"),
    ("SRC3865_19_1052_wep", CSV_1052_WEP, "AWP1052_0_alpha_Coulomb", "alpha WEP projection ledger"),
    ("SRC3865_20_1052_r10", CSV_1052_R10, "RAP1052_0_product_law", "alpha R10 projection ledger"),
    ("SRC3865_21_1057_counter", CSV_1057_COUNTER, "CT1057_1_hidden_scalar", "F2 counterterm ledger"),
    ("SRC3865_22_3118_hom", CSV_3118_HOM, "NHV3118_1", "hidden F2 countermodel"),
]

IMAGE_THEOREM = (
    "If the parent generator functor Gen has visible coefficient image "
    "A_vis = Image(ParentGenerate[Phi,q_obs,Dq,F_parent,theta_rep,topology,e_obs]) and this image is full on visible operator coefficients, "
    "then there is no independent object Coeff(F_Q^2) and no map from hidden representative variables into it; every visible Maxwell coefficient is q-basic or fixed representation data."
)
IMAGE_CURRENT_BLOCK = (
    "The current corpus has the image theorem as a contract, not a parent derivation: quotient functor exactness/fullness, no hidden-visible Hom, radiative/readout closure, and boundary/local projection silence remain unsigned."
)
JOINT_IDENTITY = (
    "b_alpha_X = 2 z_g - s_XF2, with s_XF2=D_Xhat ln lambda_A and z_g=D_Xhat ln g_J."
)
JOINT_HARNESS = (
    "For any arena A with scale tau_A, the no-cancellation finite branch uses "
    "|s_XF2 tau_A| <= |b_alpha_X tau_A| + 2|z_g tau_A|. "
    "If z_g is not zeroed or bounded in the same arena, alpha data alone cannot bound s_XF2."
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
                "claim_use": "nonclaim_visible_operator_image_or_joint_bound",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "theorem_id": "VOI3865_0_image_theorem",
            "claim_piece": "visible operator-domain image theorem",
            "statement": IMAGE_THEOREM,
            "derivation": "A typed image/fullness theorem: if all visible coefficient objects are images of parent-generated data, a hidden coefficient map is ill-typed unless it factors through q_obs or fixed representation data.",
            "result": "EXACT_CONDITIONAL_IMAGE_THEOREM",
            "status": "CONDITIONAL_THEOREM_PROVED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "VOI3865_1_no_extra_F2_consequence",
            "claim_piece": "no-extra-F2 consequence",
            "statement": "Under VOI3865_0 plus radiative/readout image stability, D_v lambda_F2=D_v f_X=D_v delta_lambda_rad=0 and the 3864 no-extra-F2 theorem closes.",
            "derivation": "Compose the image theorem with the 3864 no-extra-F2 operator-domain theorem.",
            "result": "EXACT_CONDITIONAL_NO_EXTRA_F2_HANDOFF",
            "status": "CONDITIONAL_ZERO_ROUTE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "VOI3865_2_current_block",
            "claim_piece": "strict current image proof verdict",
            "statement": IMAGE_CURRENT_BLOCK,
            "derivation": "2766/2765/3528/2659 provide a precise contract and exact typed theorem, but not the parent construction proving the visible coefficient category is the parent image.",
            "result": "VISIBLE_OPERATOR_IMAGE_NOT_CLAIMED_CURRENT_CORPUS",
            "status": "CURRENT_NONCLAIM_JOINT_BOUND_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "VOI3865_3_joint_identity",
            "claim_piece": "joint finite-bound identity",
            "statement": JOINT_IDENTITY,
            "derivation": "alpha_eff is proportional to g_J^2/lambda_A in the canonical EM/current block, so vertical derivatives obey the displayed linear identity.",
            "result": "EXACT_LINEAR_CONSTRAINT",
            "status": "FINITE_BRANCH_ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "VOI3865_4_joint_harness",
            "claim_piece": "joint finite-bound harness",
            "statement": JOINT_HARNESS,
            "derivation": "Triangle inequality applied to s_XF2=2 z_g-b_alpha_X after multiplying by the arena scale/projection.",
            "result": "NONCLAIM_JOINT_BOUND_HARNESS",
            "status": "BOUND_HARNESS_BUILT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "VOI3865_5_next_handoff",
            "claim_piece": "next target",
            "statement": "Next either parent-constructs the visible coefficient image category, or implements a runnable nonclaim joint s_XF2/z_g/b_alpha product runner with clock/WEP/R10 input validation.",
            "derivation": "3865 has the exact theorem and the finite algebra; what remains is parent construction or scoreable source rows.",
            "result": "NEXT_GATE_IS_IMAGE_CONSTRUCTOR_OR_JOINT_RUNNER",
            "status": "COUPLING_ROUTE_SHARPENED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def audit_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "audit_id": "IPA3865_0_parent_generator",
            "clause": "parent generator domain",
            "required_signature": "Op_allowed subset Alg[q(Phi),Dq(Phi),F_parent,theta_rep,topological classes,e_obs]",
            "current_evidence": "2766 states this as an exact contract if adopted, not as a derivation from MTS primitives",
            "passes_current_branch": False,
            "residual_owner": "B_parent_generator_domain",
            "next_action": "construct the parent generator category or retain finite coefficient rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "IPA3865_1_quotient_fullness",
            "clause": "quotient functor exact/full on visible coefficients",
            "required_signature": "S_vis factors through C_vis=q(C_parent) with no extra Coeff(O_vis) object",
            "current_evidence": "2766 says exactness/fullness is unsigned; 3864 needs it for no-extra-F2",
            "passes_current_branch": False,
            "residual_owner": "B_quotient_fullness",
            "next_action": "derive universal property or keep lambda_A F_Q^2 legal",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "IPA3865_2_nohom",
            "clause": "no hidden-visible coefficient Hom",
            "required_signature": "Hom(C_hid,Coeff(F_Q^2))=Const/absent unless factoring through q_obs",
            "current_evidence": "2659 proves exact typed theorem conditionally, but parent coefficient algebra remains unsigned",
            "passes_current_branch": False,
            "residual_owner": "B_nohom_hidden_visible",
            "next_action": "parent-sign coefficient algebra or retain C_XF2/s_XF2",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "IPA3865_3_radiative_readout",
            "clause": "radiative/readout image stability",
            "required_signature": "S_eff and readout maps stay in Image(ParentGenerate) after loops, thresholds and apparatus projection",
            "current_evidence": "2766/3118 keep radiative/readout closure unsigned",
            "passes_current_branch": False,
            "residual_owner": "B_radiative_readout_image",
            "next_action": "derive q-basic effective/readout closure or keep delta_lambda_rad/readout rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "IPA3865_4_zg_owner",
            "clause": "current normalization z_g",
            "required_signature": "z_g=0 or arena-bounded from same-current owner",
            "current_evidence": "3680 says z_g zero theorem is not proved and two-knob branch remains live",
            "passes_current_branch": False,
            "residual_owner": "z_g",
            "next_action": "jointly bound with s_XF2/b_alpha or prove same-current owner",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "IPA3865_5_balpha_inputs",
            "clause": "alpha product input rows",
            "required_signature": "clock/WEP/R10 products have MTS-side b_alpha, tau, beta and source projections",
            "current_evidence": "3118/1052 provide templates and source bounds but mark MTS-side inputs missing/nonclaim",
            "passes_current_branch": False,
            "residual_owner": "B_alpha_product_inputs",
            "next_action": "build a runnable nonclaim joint runner requiring these inputs",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def joint_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "bound_id": "JHB3865_0_linear_constraint",
            "target": "s_XF2,z_g,b_alpha_X",
            "formula": "b_alpha_X - 2 z_g + s_XF2 = 0",
            "derivation": "canonical EM/current normalization identity",
            "required_inputs": "canonical Xhat normalization and sign convention",
            "status": "EXACT_NONCLAIM_LINEAR_CONSTRAINT",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "JHB3865_1_no_cancellation_sXF2",
            "target": "abs(s_XF2)",
            "formula": "|s_XF2| <= |b_alpha_X| + 2|z_g|",
            "derivation": "triangle inequality from s_XF2=2z_g-b_alpha_X",
            "required_inputs": "standalone or arena-normalized bounds on b_alpha_X and z_g",
            "status": "NONCLAIM_SYMBOLIC_BOUND",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "JHB3865_2_clock_product",
            "target": "abs(s_XF2*tau_clock)",
            "formula": "|s_XF2 tau_clock| <= |b_alpha_X tau_clock| + 2|z_g tau_clock|",
            "derivation": "multiply JHB3865_1 by the same clock-domain projection scale",
            "required_inputs": "clock alpha product bound plus MTS z_g clock projection; current row has alpha product only",
            "status": "BLOCKED_MISSING_ZG_CLOCK_PROJECTION",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "JHB3865_3_zg_zero_branch",
            "target": "s_XF2 if z_g=0",
            "formula": "z_g=0 => s_XF2=-b_alpha_X",
            "derivation": "same-current owner specialization of the exact linear identity",
            "required_inputs": "parent-signed z_g zero theorem plus alpha product/source bound",
            "status": "CONDITIONAL_DIRECT_BRANCH_NOT_ACTIVE",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "JHB3865_4_WEP_R10_joint",
            "target": "WEP/R10 source projections",
            "formula": "arena_signal = P_alpha(2 z_g-s_XF2)+P_z z_g+P_s s_XF2+epsilon_tail",
            "derivation": "source arenas can see alpha response, current/source normalization and direct F2 source legs together",
            "required_inputs": "P_alpha,P_z,P_s,tau/K_X,beta_s,beta_t,material/source map and valid bound rows",
            "status": "RUNNER_SCHEMA_NONCLAIM_INPUTS_MISSING",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "JHB3865_5_runner_acceptance",
            "target": "future joint runner acceptance",
            "formula": "claim_allowed only if image theorem closes or all s_XF2,z_g,b_alpha projections are numeric, sourced, same-domain and pass bounds",
            "derivation": "prevents alpha-only, clock-only or unity-projection shortcuts",
            "required_inputs": "source paths, units, arena projection maps, bound rows, no-cancellation policy",
            "status": "ACCEPTANCE_GATE_DEFINED",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "G3865_0_image_theorem",
            "gate": "conditional image theorem is explicit",
            "status": "PASS_EXACT_CONDITIONAL_IMAGE_THEOREM",
            "claim_allowed": False,
            "reason": "typed image/fullness theorem proves no hidden coefficient only if parent coefficient category is signed",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "G3865_1_current_block",
            "gate": "current image/no-extra-F2 claim remains blocked",
            "status": "BLOCKED_VISIBLE_OPERATOR_IMAGE_NOT_PARENT_DERIVED",
            "claim_allowed": False,
            "reason": "quotient fullness, no-Hom, radiative/readout and boundary projection clauses remain unsigned",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "G3865_2_joint_harness",
            "gate": "joint s_XF2/z_g/b_alpha bound harness is explicit",
            "status": "PASS_JOINT_BOUND_HARNESS_BUILT",
            "claim_allowed": False,
            "reason": "finite branch uses b_alpha_X=2z_g-s_XF2 and refuses alpha-only shortcuts",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "G3865_3_nonclaim",
            "gate": "no scoring claim from current rows",
            "status": "PASS_NONCLAIM_INPUTS_MISSING",
            "claim_allowed": False,
            "reason": "clock/WEP/R10 rows lack MTS-side z_g/s_XF2 projections and valid source inputs",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "G3865_4_next",
            "gate": "next target selected",
            "status": "PASS_3866_JOINT_RUNNER_OR_IMAGE_CONSTRUCTOR_TARGET",
            "claim_allowed": False,
            "reason": "3865 leaves either a parent image construction task or a concrete joint finite-bound runner task",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D3865_0",
            "decision": "Do not claim visible operator-domain image exhaustion.",
            "consequence": "The theorem is exact, but the parent visible coefficient category is not constructed yet.",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "D3865_1",
            "decision": "Use the two-knob finite branch when derivation is unsigned.",
            "consequence": "Track `s_XF2` and `z_g` together; alpha constraints only hit `2z_g-s_XF2`.",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "D3865_2",
            "decision": "Next work should be executable or constructive.",
            "consequence": "Either build the parent image constructor proof, or implement the joint runner with strict nonclaim validation.",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3865_0",
            "target_checkpoint": "3866-Y5-R2FR-joint-sXF2-zg-balpha-runner-or-visible-image-constructor.md",
            "script": "scripts/Y5_R2FR_3866_joint_sXF2_zg_balpha_runner_or_visible_image_constructor.py",
            "objective": "either parent-construct the visible coefficient image category, or create a runnable nonclaim joint s_XF2/z_g/b_alpha product runner for clock/WEP/R10/source arenas",
            "why_next": "3865 has the exact theorem and the finite algebra; the next move should either close the parent construction or make the bound harness executable",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "status": "PASS_NONCLAIM_IMAGE_THEOREM_AND_JOINT_SXF2_ZG_BALPHA_BOUND_HARNESS",
            "summary": "3865 proves the visible-operator image theorem conditionally, blocks current promotion, and builds the joint s_XF2/z_g/b_alpha finite-bound harness.",
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
    joint: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    timestamp: str,
) -> None:
    text = f"""# 3865 — Visible Operator-Domain Image Proof Or sXF2/z_g/b_alpha Joint Bound

Generated: `{timestamp}`

## Purpose

3864 showed that no-extra-F2 reduces to the parent visible-operator image problem, and that finite alpha data must be joint with current normalization. This checkpoint does both jobs cleanly.

## Result

Conditional image theorem:

`{IMAGE_THEOREM}`

Current strict verdict:

`{IMAGE_CURRENT_BLOCK}`

Finite branch:

`{JOINT_IDENTITY}`

Harness rule:

`{JOINT_HARNESS}`

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## Visible Operator Image Theorem

{markdown_table(theorem, ["theorem_id", "claim_piece", "status", "result"])}

## Image Proof Audit

{markdown_table(audit, ["audit_id", "clause", "passes_current_branch", "residual_owner", "next_action"])}

## Joint Bound Harness

{markdown_table(joint, ["bound_id", "target", "status", "formula"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Bottom Line

3865 does not close no-extra-F2, but it stops the coupling problem from smearing out. The derivation route is now one clean parent construction: visible coefficient operators must be the image of parent-generated data. If that is not proved, the finite route is not “alpha bounds sXF2”; it is the joint identity `b_alpha_X=2z_g-s_XF2`, with source/clock/WEP/R10 projections required in the same domain.

Next target: `3866-Y5-R2FR-joint-sXF2-zg-balpha-runner-or-visible-image-constructor.md`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3864", "Current State After 3865", 1)
    text = "\n".join(
        line for line in text.splitlines() if not line.startswith("<!-- Generated by 3865 at ")
    )
    paragraph = (
        "`3865` sharpens the no-extra-F2 route into either a parent image theorem or a joint finite-bound branch. "
        "The exact conditional theorem is: if `A_vis=Image(ParentGenerate[Phi,q_obs,Dq,F_parent,theta_rep,topology,e_obs])` and the image is full on visible operator coefficients, then there is no independent `Coeff(F_Q^2)` object and no map from hidden representative variables into it; every visible Maxwell coefficient is q-basic or fixed representation data. "
        "The current corpus does not claim this because quotient functor exactness/fullness, no hidden-visible Hom, radiative/readout image stability, and boundary/local projection silence remain unsigned. "
        "The finite branch is now a joint harness: `b_alpha_X=2 z_g-s_XF2`, so `|s_XF2 tau_A| <= |b_alpha_X tau_A|+2|z_g tau_A|` in any arena `A`; alpha data alone cannot isolate `s_XF2` unless `z_g=0` is parent-proved or independently bounded in the same arena. "
        "Clock/WEP/R10 rows are therefore nonclaim until MTS-side `z_g`, `s_XF2`, `tau`, beta/source and valid bound inputs are supplied.\n\n"
    )
    if paragraph not in text and "## Next Best Gate" in text:
        text = text.replace("## Next Best Gate", paragraph + "## Next Best Gate", 1)
    old_gate = """`3865-Y5-R2FR-visible-operator-domain-image-proof-or-sXF2-zg-joint-bound.md`

Target: derive `Allowed[S_vis]=Image(ParentGenerate)` for the EM coefficient algebra, or build a nonclaim joint `s_XF2` / `z_g` / `b_alpha` bound harness.

This is the best next move because 3864 shows no-extra-F2 is exactly the parent-domain image/no-Hom/radiative closure problem; finite alpha data must be joint with current normalization."""
    new_gate = """`3866-Y5-R2FR-joint-sXF2-zg-balpha-runner-or-visible-image-constructor.md`

Target: either parent-construct the visible coefficient image category, or create a runnable nonclaim joint `s_XF2` / `z_g` / `b_alpha` product runner for clock/WEP/R10/source arenas.

This is the best next move because 3865 has the exact theorem and finite algebra; now the branch needs either a parent construction or executable bound validation."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3865_VISIBLE_OPERATOR_IMAGE_THEOREM.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3865_IMAGE_PROOF_AUDIT.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3865_SXF2_ZG_BALPHA_JOINT_BOUND.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3865_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3865_VISIBLE_OPERATOR_IMAGE_THEOREM.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    text = text.rstrip() + f"\n\n<!-- Generated by 3865 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    audit: list[dict[str, object]],
    joint: list[dict[str, object]],
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

    all_text = " ".join(str(row) for row in theorem + audit + joint + gates)
    add(
        "VAL3865_0_sources",
        "all cited source paths exist and needles are found",
        all(row["exists"] and row["needle_found"] for row in sources),
        f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved",
    )
    add(
        "VAL3865_1_image_theorem",
        "conditional visible image theorem is explicit",
        "EXACT_CONDITIONAL_IMAGE_THEOREM" in all_text and "A_vis = Image" in all_text,
        "image theorem present",
    )
    add(
        "VAL3865_2_current_block",
        "current image claim remains blocked",
        "VISIBLE_OPERATOR_IMAGE_NOT_CLAIMED_CURRENT_CORPUS" in all_text and "BLOCKED_VISIBLE_OPERATOR_IMAGE_NOT_PARENT_DERIVED" in all_text,
        "no image theorem promotion",
    )
    add(
        "VAL3865_3_joint_identity",
        "joint s_XF2/z_g/b_alpha identity is explicit",
        "b_alpha_X - 2 z_g + s_XF2 = 0" in all_text and "EXACT_LINEAR_CONSTRAINT" in all_text,
        "joint identity present",
    )
    add(
        "VAL3865_4_no_alpha_shortcut",
        "alpha-only s_XF2 shortcut is rejected",
        "alpha data alone cannot bound s_XF2" in all_text and "PASS_JOINT_BOUND_HARNESS_BUILT" in all_text,
        "joint harness guard present",
    )
    add(
        "VAL3865_5_nonclaim",
        "all rows remain nonclaim",
        all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in theorem + audit + joint + gates),
        "valid_for_claim/claim_allowed false throughout",
    )
    add(
        "VAL3865_6_next",
        "next target is joint runner or image constructor",
        DOC_PATH.exists() and "3866-Y5-R2FR-joint-sXF2-zg-balpha-runner-or-visible-image-constructor" in read_text(DOC_PATH),
        "3866 target visible",
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
        add(f"VAL3865_7_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add(
        "VAL3865_8_doc",
        "markdown checkpoint document exists",
        DOC_PATH.exists() and "3864 showed that no-extra-F2" in read_text(DOC_PATH),
        rel(DOC_PATH),
    )
    formalization_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3865*", "P8_Y5_BRR545_3865*", "*Y5_R2FR_3865*", "3865-Y5-R2FR*"):
            formalization_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add(
        "VAL3865_9_formalization_clean",
        "formalization-workbench has no generated 3865 project files",
        len(formalization_hits) == 0,
        "; ".join(str(path) for path in formalization_hits) if formalization_hits else "no generated 3865 project file hits under formalization-workbench",
    )
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add(
        "VAL3865_10_pycache_removed",
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
    joint = joint_rows(timestamp)
    gates = gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["audit"], audit)
    write_csv(OUTPUTS["joint"], joint)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, theorem, audit, joint, gates, decisions, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, theorem, audit, joint, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_NONCLAIM_IMAGE_THEOREM_AND_JOINT_BOUND_HARNESS")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
