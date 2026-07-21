from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4527"
CLAIM_ID = "L-369"
MARKER = "PPC4161_SCALAR_ACTION_ASYMMETRY_COEFFICIENT_OR_AUXILIARY_Z_PRINCIPAL_SYMBOL_HUNT_4527"
PACKET_MARKER = "PPC4161_PACKET_SCALAR_ACTION_ASYMMETRY_COEFFICIENT_OR_AUXILIARY_Z_PRINCIPAL_SYMBOL_HUNT_4527"
DECISION = "ACTION_ODD_FORCE_AND_VERTICAL_PRINCIPAL_SYMBOL_LAWS_DERIVED_NO_EXISTING_PARENT_ZERO_SOURCE_YET_DUAL_RUNNER_INPUTS_READY"
NEXT_TARGET = "4528-Y5-R2FR-existing-parent-Z-kinetic-block-source-sweep-or-epsilonI-first-bound-row.md"

FORMAL_PATH = FORMAL / "543-PPC4161-scalar-action-asymmetry-coefficient-or-auxiliary-Z-principal-symbol-hunt.md"
DOC_PATH = POST / "4527-Y5-R2FR-scalar-action-asymmetry-coefficient-or-auxiliary-Z-principal-symbol-hunt.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4527_SOURCE_REGISTER.csv"
ACTION_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4527_ACTION_ODD_FORCE_THEOREM.csv"
PRINCIPAL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4527_AUXILIARY_Z_PRINCIPAL_SYMBOL_TEST.csv"
BRANCH_CSV = SOURCE_DIR / "P8_Y5_R2FR_4527_BRANCH_DECISION_MATRIX.csv"
COEFFICIENT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4527_COEFFICIENT_UPDATE_ROWS.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4527_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4527_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4527_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4527_NEXT_TARGET.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4527_VALIDATION.csv"

DOC_4526 = POST / "4526-Y5-R2FR-vertical-involution-source-hunt-or-first-source-normalized-coefficient-fill.md"
FORMAL_4526 = FORMAL / "542-PPC4161-vertical-involution-source-hunt-or-first-source-normalized-coefficient-fill.md"
VALIDATION_4526 = SOURCE_DIR / "P8_Y5_BRR545_4526_VALIDATION.csv"
BRIDGE_4526 = SOURCE_DIR / "P8_Y5_R2FR_4526_ZL_TO_Z_PARENT_BRIDGE_THEOREM.csv"
COEFF_4526 = SOURCE_DIR / "P8_Y5_R2FR_4526_FIRST_SOURCE_NORMALIZED_COEFFICIENT_ROWS.csv"
HUNT_4526 = SOURCE_DIR / "P8_Y5_R2FR_4526_VERTICAL_INVOLUTION_SOURCE_HUNT.csv"

THEOREM_4525 = SOURCE_DIR / "P8_Y5_R2FR_4525_QUOTIENT_EVEN_MORSE_BOTT_Z_THEOREM.csv"
SIGNATURE_4525 = SOURCE_DIR / "P8_Y5_R2FR_4525_PARENT_SIGNATURE_REQUIREMENTS.csv"
CLASSIFIER_4519 = SOURCE_DIR / "P8_Y5_R2FR_4519_FINITE_RANGE_OR_RANK_ZERO_BRANCH_CLASSIFIER.csv"
RESIDUAL_4519 = SOURCE_DIR / "P8_Y5_R2FR_4519_RANK_ZERO_ALGEBRAIC_RESIDUAL_VECTOR.csv"
DERIVATION_4451 = SOURCE_DIR / "P8_Y5_R2FR_4451_DERIVATION_ROWS.csv"
OUTCOME_4451 = SOURCE_DIR / "P8_Y5_R2FR_4451_OUTCOME_ROWS.csv"
DOC_1192 = POST / "1192-Y5-R10-parent-phi-source-or-active-Gamma-bound-first-score-row.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def line_of(path: Path, needle: str) -> int:
    for line_number, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return line_number
    return 0


def snippet(path: Path, needle: str) -> str:
    for line in text(path).splitlines():
        if needle in line:
            return line.strip()
    return ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        out.append("| " + " | ".join(str(row.get(header, "")).replace("\n", "<br>") for header in headers) + " |")
    return "\n".join(out)


def append_once(path: Path, marker: str, body: str) -> None:
    current = text(path)
    if marker in current:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="") as handle:
        if current and not current.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + body.strip() + "\n")


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC4527_00_formal4526", "4526 formal handoff", FORMAL_4526, "PPC4161_VERTICAL_INVOLUTION_SOURCE_HUNT_OR_FIRST_SOURCE_NORMALIZED_COEFFICIENT_FILL_4526", "vertical involution source hunt"),
        ("SRC4527_01_post4526", "4526 post handoff", DOC_4526, "4527-Y5-R2FR-scalar-action-asymmetry-coefficient-or-auxiliary-Z-principal-symbol-hunt.md", "declared 4527 target"),
        ("SRC4527_02_val4526", "4526 validation", VALIDATION_4526, "VAL4526_OVERALL", "previous validation pass"),
        ("SRC4527_03_bridge4526", "4526 bridge theorem", BRIDGE_4526, "BRG4526_1_action_evenness", "action evenness bridge"),
        ("SRC4527_04_coeff4526", "4526 coefficient rows", COEFF_4526, "COF4526_0_epsilon_I", "action asymmetry coefficient"),
        ("SRC4527_05_hunt4526", "4526 source hunt", HUNT_4526, "HUNT4526_4_parent_action_invariance", "parent action invariance not found"),
        ("SRC4527_06_theorem4525", "4525 parent Z theorem", THEOREM_4525, "QEZ4525_2_rank_zero_from_auxiliary_verticality", "rank zero from auxiliary verticality"),
        ("SRC4527_07_sig4525", "4525 signature rows", SIGNATURE_4525, "SIG4525_1_auxiliary_vertical_coordinate", "auxiliary vertical coordinate needed"),
        ("SRC4527_08_classifier4519", "4519 branch classifier", CLASSIFIER_4519, "FRC4519_1_finite_range", "finite range if rank Z positive"),
        ("SRC4527_09_residual4519", "4519 residual vector", RESIDUAL_4519, "RZR4519_0_normal_form", "rank zero residual equation"),
        ("SRC4527_10_torsion4451", "4451 no-kinetic auxiliary analogy", DERIVATION_4451, "D4451_0_local_action", "no kinetic term gives algebraic branch in torsion analogy"),
        ("SRC4527_11_torsion_outcome4451", "4451 failure mode", OUTCOME_4451, "OUT4451_3_failure_mode", "kinetic or kernel reopens finite/contact branch"),
        ("SRC4527_12_aux_caution1192", "1192 auxiliary closure caution", DOC_1192, "D1192_1_phi_source_not_parent_signed", "do not add parentless auxiliary constraint"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, role, path, needle, note in specs:
        body = text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in body,
                "line": line_of(path, needle),
                "evidence_snippet": snippet(path, needle),
                "note": note,
                "valid_for_claim": False,
            }
        )
    return rows


def action_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "AOF4527_0_odd_even_split",
            "statement": "In a parent vertical collar, split the action into I_q-even and I_q-odd pieces.",
            "formula": "S_even=(S[z]+S[I_q z])/2; S_odd=(S[z]-S[I_q z])/2",
            "consequence": "only S_odd can source the first vertical force at z=0",
            "status": "DERIVED",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "AOF4527_1_first_force",
            "statement": "The dangerous scalar/action residual is the first variation of S_odd at the local section.",
            "formula": "A_A := delta S_odd/delta z^A |_{z=0}; F_A(0)=A_A",
            "consequence": "F_1=0 follows if and only if A_A=0 in every physical vertical source direction",
            "status": "DERIVED",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "AOF4527_2_epsilon_link",
            "statement": "The 4526 action-asymmetry scalar epsilon_I is not itself the force, but it bounds the force only after a local Lipschitz/diameter control is sourced.",
            "formula": "||A|| <= C_I epsilon_I / ell_z, with C_I and ell_z sourced from the parent collar",
            "consequence": "epsilon_I needs collar constants before entering alpha/PPN scoring numerically",
            "status": "BOUND_FORM_DERIVED_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "AOF4527_3_scalar_channel_projection",
            "statement": "The 128 scalar survivor coefficients are the components of A_A projected onto z_theta, z_dotB and z_Lcg.",
            "formula": "a_i = e_i^A A_A / N_i, i in {theta,dotB,Lcg}",
            "consequence": "a_theta, a_dotB and a_Lcg are no longer vague blockers; they are action-odd force components",
            "status": "PROJECTION_DERIVED_NORMALIZATION_MISSING",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "AOF4527_4_no_parentless_auxiliary",
            "statement": "Adding a new Lagrange multiplier or auxiliary action can force A_A=0, but 1192 shows that this is closure unless the variable, stress, Ward identity and matter readout are already parent-owned.",
            "formula": "new constraint action != MTS derivation unless it descends from existing S_parent",
            "consequence": "4527 refuses the magic auxiliary shortcut",
            "status": "NO_CLOSURE_SHORTCUT",
            "valid_for_claim": False,
        },
    ]


def principal_rows() -> list[dict[str, Any]]:
    return [
        {
            "test_id": "APS4527_0_vertical_quadratic_form",
            "test": "extract vertical second-order parent Lagrangian",
            "formula": "L_z^(2)=1/2 K_AB^{mu nu} nabla_mu z^A nabla_nu z^B + 1/2 M_AB z^A z^B + A_A z^A",
            "if_zero_or_signed": "K=0 gives auxiliary/rank-zero branch; M_AB and A_A decide lock/residual",
            "if_nonzero": "rank/sign of K selects finite-range or instability branch",
            "current_status": "FORMULA_DERIVED_PARENT_K_MISSING",
            "valid_for_claim": False,
        },
        {
            "test_id": "APS4527_1_principal_symbol",
            "test": "compute physical vertical principal symbol",
            "formula": "Z_AB(xi)=K_AB^{mu nu} xi_mu xi_nu on Q_phys after gauge/constraint reduction",
            "if_zero_or_signed": "rank(Z_AB)=0 becomes parent-derived",
            "if_nonzero": "use 4519 finite-range classifier",
            "current_status": "SOURCE_SWEEP_REQUIRED",
            "valid_for_claim": False,
        },
        {
            "test_id": "APS4527_2_rank_zero_gate",
            "test": "rank-zero algebraic branch",
            "formula": "rank Z=0 and M_AB coercive => M_AB z^B=-A_A-R_A^other",
            "if_zero_or_signed": "if A_A and other RHS vanish, z=0",
            "if_nonzero": "finite algebraic residual bound via m_min^{-1} sum_abs RHS",
            "current_status": "MISSING_K_ZERO_MMIN_A_ZERO",
            "valid_for_claim": False,
        },
        {
            "test_id": "APS4527_3_finite_range_gate",
            "test": "finite-range branch",
            "formula": "M_AB v_i = mu_i^2 Z_AB v_i; lambda_i=1/mu_i",
            "if_zero_or_signed": "not applicable if rank Z=0",
            "if_nonzero": "alpha_i(lambda_i) runner must score source/test charges and bound curve",
            "current_status": "READY_IF_K_NONZERO_VALUES_SOURCED",
            "valid_for_claim": False,
        },
        {
            "test_id": "APS4527_4_torsion_analogy_limit",
            "test": "use 4451 only as structural analogy",
            "formula": "no kinetic term -> algebraic equation, but only for the sector whose parent action actually lacks kinetic terms",
            "if_zero_or_signed": "helps define the required proof shape",
            "if_nonzero": "does not prove parent Z is auxiliary",
            "current_status": "ANALOGY_NOT_SOURCE",
            "valid_for_claim": False,
        },
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": "BDM4527_0_parent_even_auxiliary",
            "condition": "A_A=0, K_AB^{mu nu}=0, M_AB coercive/constraint-owned in one existing parent branch",
            "result": "rank-zero local GR/Newton route becomes materially stronger",
            "current_status": "NOT_PROVED",
            "next_input": "existing parent action source for A_A=0 and K=0",
            "valid_for_claim": False,
        },
        {
            "branch_id": "BDM4527_1_action_odd_rank_zero",
            "condition": "K=0 but A_A or scalar components survive",
            "result": "algebraic residual z=-M^{-1}A feeds PPN/R10/clock/orbit via 4524",
            "current_status": "SCORING_BRANCH_READY_VALUES_MISSING",
            "next_input": "A_A components and m_min",
            "valid_for_claim": False,
        },
        {
            "branch_id": "BDM4527_2_finite_range",
            "condition": "rank K > 0 with positive generalized eigenvalues",
            "result": "finite range alpha(lambda) branch; no rank-zero claim",
            "current_status": "SCORING_BRANCH_READY_VALUES_MISSING",
            "next_input": "Z_AB, M_AB, Qbar_XS, qbar_XT, bound curve",
            "valid_for_claim": False,
        },
        {
            "branch_id": "BDM4527_3_bad_sign_or_zero_mode",
            "condition": "K or M has wrong sign, massless physical zero mode, or unconstrained null",
            "result": "stability/long-range local-test branch opens",
            "current_status": "GUARD_READY_VALUES_MISSING",
            "next_input": "constraint algebra, spectrum and local-test residual vector",
            "valid_for_claim": False,
        },
        {
            "branch_id": "BDM4527_4_current_verdict",
            "condition": "current corpus",
            "result": "no parent-zero source found; dual runner/input route remains live",
            "current_status": "NO_CLAIM",
            "next_input": NEXT_TARGET,
            "valid_for_claim": False,
        },
    ]


def coefficient_rows() -> list[dict[str, Any]]:
    return [
        {
            "coefficient_id": "COF4527_0_A_odd_force",
            "quantity": "A_A",
            "definition": "vertical action-odd force vector",
            "formula": "A_A=delta S_odd/delta z^A|_0",
            "source_needed": "existing parent action in vertical collar and I_q action",
            "status": "FORMULA_FILLED_VALUE_MISSING",
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "COF4527_1_CI_over_ellz",
            "quantity": "C_I/ell_z",
            "definition": "collar constant converting epsilon_I action defect to force norm",
            "formula": "||A|| <= (C_I/ell_z) epsilon_I",
            "source_needed": "local collar diameter/norm and action regularity constant",
            "status": "BOUND_FORM_FILLED_VALUE_MISSING",
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "COF4527_2_Kvert",
            "quantity": "K_AB^{mu nu}",
            "definition": "vertical kinetic/principal coefficient",
            "formula": "partial^2 L / partial(nabla_mu z^A) partial(nabla_nu z^B)",
            "source_needed": "parent quadratic action expansion",
            "status": "PRINCIPAL_SYMBOL_ROW_READY_VALUE_MISSING",
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "COF4527_3_rankZ",
            "quantity": "rank Z_AB",
            "definition": "rank of physical vertical principal symbol after gauge/constraint reduction",
            "formula": "rank[K_AB^{mu nu} xi_mu xi_nu] on Q_phys",
            "source_needed": "Kvert plus constraint/gauge reduction",
            "status": "CLASSIFIER_READY_VALUE_MISSING",
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "COF4527_4_mu_lambda",
            "quantity": "mu_i, lambda_i",
            "definition": "finite-range generalized eigenvalues if rankZ>0",
            "formula": "M v_i=mu_i^2 Z v_i; lambda_i=1/mu_i",
            "source_needed": "Z/M eigenpair with units",
            "status": "FINITE_RANGE_ROW_READY_IF_RANK_POSITIVE",
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "COF4527_5_alpha_projection",
            "quantity": "alpha_i(lambda_i)",
            "definition": "observable finite-range or algebraic residual projection",
            "formula": "rankZ>0: alpha_i=K_i Qbar_iS qbar_iT/(G_N M_S m_T M_i^2); rankZ=0: |delta O|<=K_obs m_min^{-1} sum_abs RHS",
            "source_needed": "source/test charges, calibration, K_obs/K_i, m_min or M_i, bound curve",
            "status": "RUNNER_LINK_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG4527_0_action_theorem",
            "gate": "action odd force theorem derived",
            "status": "PASS_CONDITIONAL",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4527_1_principal_test",
            "gate": "vertical principal symbol test derived",
            "status": "PASS_CONDITIONAL",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4527_2_parent_zero",
            "gate": "existing parent source proves A_A=0 and K=0",
            "status": "BLOCKED_NOT_FOUND",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4527_3_no_closure_auxiliary",
            "gate": "no new parentless auxiliary constraint promoted",
            "status": "PASS_FIREWALL",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4527_4_local_GR",
            "gate": "local GR/Newton/R10/PPN claim",
            "status": "BLOCKED",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4527_0",
            "decision": DECISION,
            "meaning": "The action-asymmetry and vertical-principal-symbol laws are now explicit. If existing parent action yields A_A=0 and K=0, the rank-zero route strengthens; if not, the same terms feed finite residual or finite-range scoring. No new auxiliary closure is adopted.",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
        }
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "claim_id": CLAIM_ID,
            "marker": MARKER,
            "decision": DECISION,
            "claim_status": "private_conditional_nonclaim_action_symbol_laws_ready",
            "created_at_utc": now(),
            "next_target": NEXT_TARGET,
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "route": "source-sweep existing parent action for Kvert=0 and A_A=0; otherwise fill epsilon_I first bound row",
            "why": "This directly decides whether the parent-Z route is a derivation or an empirical residual branch.",
            "valid_for_claim": False,
        }
    ]


def validate(sources: list[dict[str, Any]], gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    csv_paths = [
        SOURCE_REGISTER,
        ACTION_THEOREM_CSV,
        PRINCIPAL_CSV,
        BRANCH_CSV,
        COEFFICIENT_CSV,
        CLAIM_GATES_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    parse_issues: list[str] = []
    for path in csv_paths:
        try:
            rows = read_csv(path)
            if not rows:
                parse_issues.append(f"{path.name}:empty")
        except Exception as error:
            parse_issues.append(f"{path.name}:{error}")

    theorem_ids = {row.get("theorem_id") for row in read_csv(ACTION_THEOREM_CSV)}
    test_ids = {row.get("test_id") for row in read_csv(PRINCIPAL_CSV)}
    coeff_ids = {row.get("coefficient_id") for row in read_csv(COEFFICIENT_CSV)}
    rows = [
        {
            "validation_id": "VAL4527_00_sources",
            "status": "PASS" if all(row["exists"] and row["needle_found"] for row in sources) else "FAIL",
            "detail": "all source paths exist and source needles are found",
        },
        {
            "validation_id": "VAL4527_01_action_theorem",
            "status": "PASS" if {"AOF4527_1_first_force", "AOF4527_4_no_parentless_auxiliary"}.issubset(theorem_ids) else "FAIL",
            "detail": "action odd force theorem and no-closure firewall present",
        },
        {
            "validation_id": "VAL4527_02_principal_test",
            "status": "PASS" if {"APS4527_1_principal_symbol", "APS4527_3_finite_range_gate"}.issubset(test_ids) else "FAIL",
            "detail": "principal symbol and finite-range gate present",
        },
        {
            "validation_id": "VAL4527_03_coefficients",
            "status": "PASS" if {"COF4527_0_A_odd_force", "COF4527_2_Kvert", "COF4527_5_alpha_projection"}.issubset(coeff_ids) else "FAIL",
            "detail": "force, Kvert and runner projection rows present",
        },
        {
            "validation_id": "VAL4527_04_claims_blocked",
            "status": "PASS" if all(str(row.get("valid_for_claim", "")).lower() == "false" for row in gates) else "FAIL",
            "detail": "all claim gates remain blocked",
        },
        {
            "validation_id": "VAL4527_05_csv_parse",
            "status": "PASS" if not parse_issues else "FAIL",
            "detail": ";".join(parse_issues) if parse_issues else "all generated CSV files parse and have rows",
        },
        {
            "validation_id": "VAL4527_06_pycache_absent",
            "status": "PASS" if not (SCRIPT_DIR / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent after cleanup",
        },
    ]
    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append({"validation_id": "VAL4527_OVERALL", "status": overall, "detail": "4527 action asymmetry and principal symbol laws"})
    return rows


def build_doc(
    sources: list[dict[str, Any]],
    action: list[dict[str, Any]],
    principal: list[dict[str, Any]],
    branches: list[dict[str, Any]],
    coefficients: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return f"""# 4527 — Scalar Action-Asymmetry Coefficient Or Auxiliary Z Principal-Symbol Hunt

Marker: `{MARKER}`  
Packet marker: `{PACKET_MARKER}`  
Decision: `{DECISION}`  
Claim: `{CLAIM_ID}`  
Status: private conditional non-claim; action/principal-symbol laws derived, parent values not sourced.

## What Moved

4527 turns the remaining parent-Z gap into a hard field-theory fork.

```text
S_odd = (S[z] - S[I_q z]) / 2
A_A = delta S_odd / delta z^A |_{{z=0}}
K_AB^{{mu nu}} = d^2 L / d(nabla_mu z^A)d(nabla_nu z^B)
```

If `A_A=0` and `K_AB^{{mu nu}}=0` are found in the existing parent action, the rank-zero local branch becomes much more derivable. If either survives, it is no longer a vague missing piece: `A_A` feeds the algebraic residual and `K_AB` selects either finite-range scoring or a stability/long-range guard. A new auxiliary constraint is explicitly refused unless it descends from existing MTS variables with stress/Ward/matter readout included.

## Action Odd-Force Theorem

{table(action)}

## Auxiliary Z Principal-Symbol Test

{table(principal)}

## Branch Decision Matrix

{table(branches)}

## Coefficient Updates

{table(coefficients)}

## Claim Gates

{table(gates)}

## Decision

{table(decisions)}

## Sources

{table(sources)}

## Validation

{table(validation)}

## Next

`{NEXT_TARGET}`.
"""


def append_claim_once() -> None:
    current = text(CLAIMS_PATH)
    if f"{CLAIM_ID}," in current:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_newton_r2fr_action_symbol",
        "claim": "4527 derives the action-odd force law and vertical principal-symbol test that decide whether the parent-Z route is algebraic/rank-zero or finite-range residual scoring.",
        "current_evidence": "Generated action theorem, auxiliary-Z principal symbol test, branch decision matrix, coefficient updates, claim gates and validation P8_Y5_BRR545_4527_VALIDATION.csv.",
        "status": "conditional_internal_nonclaim_laws_ready_values_missing",
        "next_test": NEXT_TARGET,
        "key_risk": "No existing parent source yet proves A_A=0 or Kvert=0; adding a new auxiliary constraint would be closure.",
        "sector": "local_gr_newton",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "Promoting a formula-level action/principal-symbol law into a local-GR proof without parent action coefficients.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writerow(row)


def main() -> None:
    sources = source_rows()
    action = action_theorem_rows()
    principal = principal_rows()
    branches = branch_rows()
    coefficients = coefficient_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    status = status_rows()
    next_target = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(ACTION_THEOREM_CSV, action)
    write_csv(PRINCIPAL_CSV, principal)
    write_csv(BRANCH_CSV, branches)
    write_csv(COEFFICIENT_CSV, coefficients)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_CSV, next_target)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validate(sources, gates)
    write_csv(VALIDATION_PATH, validation)

    body = build_doc(sources, action, principal, branches, coefficients, gates, decisions, validation)
    FORMAL_PATH.write_text(body, encoding="utf-8")
    DOC_PATH.write_text(body, encoding="utf-8")

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4527 Scalar Action-Asymmetry Coefficient Or Auxiliary Z Principal-Symbol Hunt

Marker: `{MARKER}`  
The local parent-Z fork is now explicit: the action-odd force `A_A=delta S_odd/delta z^A|_0` decides first-order scalar/action leakage, while the vertical principal symbol `K_AB^{{mu nu}}` decides rank-zero versus finite-range scoring. Existing parent sources have not yet supplied `A_A=0` or `K=0`, and new auxiliary constraints are rejected as closure unless parent-owned.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4527 Packet Integration

Marker: `{PACKET_MARKER}`  
The PPC4161 packet now has the field-theory fork needed for the next source sweep: prove existing parent `A_A=0` and `Kvert=0`, or score `A_A`, `Kvert`, `mu_i/lambda_i` and source/test charges through the residual runners. Next target: `{NEXT_TARGET}`.
""",
    )

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()
