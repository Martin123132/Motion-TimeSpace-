from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1663"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1663-Y5-R2FR-parent-q_loc-tensor-action-clause-or-frame-leak-coefficient.md"

SOURCE_FILES = {
    "1662_doc": ROOT / "1662-Y5-R2FR-q_loc-covariance-and-apparatus-transfer-map.md",
    "1662_validation": OUT / "P8_Y5_BRR545_1662_VALIDATION.csv",
    "1662_covariance_contract": OUT / "P8_Y5_PARENT_QLOC_1662_QLOC_COVARIANCE_CONTRACT.csv",
    "1662_frame_leak": OUT / "P8_Y5_PARENT_QLOC_1662_FRAME_LEAK_FALLBACK.csv",
    "1010_action_existence": ROOT / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
    "356_parent_ward": ROOT / "356-parent-action-ward-identity-and-projector-variation.md",
    "429_ward_owner": ROOT / "429-Ward-Bianchi-exchange-owner-for-Poisson-source.md",
    "1003_frame_guard": ROOT / "1003-Y5-R10-Bref-covariant-frame-theorem-or-Delta-ref-frame-profile-row.md",
}

NEEDLES = {
    "1662_doc": ["parent-action gated", "epsilon_frame_leak"],
    "1662_validation": ["VAL1662_OVERALL", "PASS"],
    "1662_covariance_contract": ["QC1662_1_scalar_descent", "MISSING_PARENT_SIGNATURE"],
    "1662_frame_leak": ["FLF1662_0_retained_frame_leak_if_transfer_unsigned", "2.43238775e-13"],
    "1010_action_existence": ["S_GK = - integral sqrt(-g) Gamma_eff", "K_hat is the metric response of Gamma_eff", "q_loc residual is retained rather than hidden"],
    "356_parent_ward": ["metric-dependent projector + dropped stress = fake GR", "parent Ward identity with projector variation"],
    "429_ward_owner": ["Ward/Bianchi ownership tells us exactly where every local force must live", "It does not by itself prove that each owned force vanishes"],
    "1003_frame_guard": ["covariant-frame zero theorem attempted, not closed", "THEOREM_ZERO_REJECTED_WITHOUT_PARENT_SIGNED_COVARIANT_FRAME"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1663_SOURCE_REGISTER.csv"
PARENT_ACTION_CLAUSES = OUT / "P8_Y5_PARENT_QLOC_1663_PARENT_ACTION_CLAUSES.csv"
TENSOR_DESCENT_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1663_TENSOR_DESCENT_AUDIT.csv"
APPARATUS_TRANSFER_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_1663_APPARATUS_TRANSFER_CONTRACT.csv"
FRAME_LEAK_COEFFICIENT = OUT / "P8_Y5_PARENT_QLOC_1663_FRAME_LEAK_COEFFICIENT.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1663_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1663_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1663_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1663_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    PARENT_ACTION_CLAUSES,
    TENSOR_DESCENT_AUDIT,
    APPARATUS_TRANSFER_CONTRACT,
    FRAME_LEAK_COEFFICIENT,
    CLAIM_GATE,
    DECISION,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    PARENT_ACTION_CLAUSES,
    TENSOR_DESCENT_AUDIT,
    APPARATUS_TRANSFER_CONTRACT,
    FRAME_LEAK_COEFFICIENT,
    CLAIM_GATE,
    DECISION,
    NEXT_TARGET,
]

COPY_TARGETS = {
    PARENT_ACTION_CLAUSES: [
        QUARANTINE / "PARENT_ACTION_CLAUSES_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_parent_action_clauses_nonclaim_1663.csv",
        QUEUE / "JR1663_PARENT_ACTION_CLAUSES_NONCLAIM.csv",
    ],
    TENSOR_DESCENT_AUDIT: [
        QUARANTINE / "TENSOR_DESCENT_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_tensor_descent_audit_nonclaim_1663.csv",
        QUEUE / "JR1663_TENSOR_DESCENT_AUDIT_NONCLAIM.csv",
    ],
    APPARATUS_TRANSFER_CONTRACT: [
        QUARANTINE / "APPARATUS_TRANSFER_CONTRACT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_apparatus_transfer_contract_nonclaim_1663.csv",
        QUEUE / "JR1663_APPARATUS_TRANSFER_CONTRACT_NONCLAIM.csv",
    ],
    FRAME_LEAK_COEFFICIENT: [
        QUARANTINE / "FRAME_LEAK_COEFFICIENT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_frame_leak_coefficient_nonclaim_1663.csv",
        QUEUE / "JR1663_FRAME_LEAK_COEFFICIENT_NONCLAIM.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_nonclaim_1663.csv",
        QUEUE / "JR1663_NEXT_TARGET_NONCLAIM.csv",
    ],
}

EPSILON_FRAME_LEAK_M1 = 2.43238775e-13
CONDITIONAL_CURVATURE_BOUND_M1 = 1.23573661e-23
FRAME_RATIO = 1.96837071e10


def ensure_dirs() -> None:
    for directory_path in [OUT, QUARANTINE, BRANCH_RESIDUALS, QUEUE]:
        directory_path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def bool_string(value: object) -> str:
    return str(value).strip().lower()


def all_claim_flags_false(paths: list[Path]) -> bool:
    flag_names = {
        "accepted_for_scoring",
        "claim_allowed",
        "claim_ready",
        "parent_signed",
        "score_allowed",
        "score_ready",
        "theorem_closed_for_claim",
        "transfer_signed_for_claim",
        "valid_for_claim",
        "valid_for_mts_claim",
        "valid_for_runner",
    }
    for path in paths:
        for row in csv_rows(path):
            for flag_name in flag_names.intersection(row):
                if bool_string(row[flag_name]) == "true":
                    return False
    return True


def find_line(path: Path, pattern: str) -> int:
    for index, line in enumerate(read_text(path).splitlines(), start=1):
        if pattern in line:
            return index
    return -1


def source_register_rows() -> list[dict[str, object]]:
    rows = []
    for source_id, path in SOURCE_FILES.items():
        text = read_text(path)
        needles = NEEDLES[source_id]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needles_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "role": "1663 parent q_loc tensor action clause or frame leak coefficient",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def parent_action_clause_rows() -> list[dict[str, object]]:
    rows = [
        (
            "PAC1663_0_parent_action_form",
            "S_parent = S_EH[g] + S_matter[g,Psi] + S_GK[g,Phi] + S_projector[P_loc,Phi,g] + S_boundary",
            "exact sector exposure with no hidden dropped stress",
            "REQUIRED_CONTRACT_NOT_PARENT_DERIVED",
            "356 requires every projector/boundary/domain force channel to be exposed",
        ),
        (
            "PAC1663_1_Gamma_scalar_descent",
            "Gamma_eff = gamma(Q(Phi)) is a scalar density contribution after quotient map Q; Lie_v Gamma_eff = 0 for vertical frame directions",
            "turns nabla^nu Gamma_eff into a tensorial vector source",
            "SUFFICIENT_CLAUSE_NOT_SOURCED",
            "1662 marks Gamma_eff scalar descent as missing parent signature",
        ),
        (
            "PAC1663_2_Khat_metric_response",
            "K_hat^{mu nu} = K_metric^{mu nu}[Gamma_eff] := 2/sqrt(-g) delta(sqrt(-g) Gamma_eff)/delta g_{mu nu}, with derivative and boundary terms accounted",
            "makes nabla_mu K_hat^{mu nu} the variational stress divergence rather than bookkeeping stress",
            "SUFFICIENT_CLAUSE_NOT_MATCHED_TO_CURRENT_SYMBOLS",
            "1010 identifies metric-response identity as not matched",
        ),
        (
            "PAC1663_3_Helmholtz_integrability",
            "delta(sqrt(-g)K_hat^{mu nu})/delta g_{alpha beta} is symmetric under exchange of metric variations up to declared boundary terms",
            "proves a local action exists for the proposed stress/current",
            "NOT_CHECKED_CURRENT_CORPUS",
            "1010 keeps Helmholtz integrability unchecked",
        ),
        (
            "PAC1663_4_Euler_double_zero",
            "local compact branch has E_A=0, Gamma_eff(Phi0)=0, K_hat(Phi0)=0, and first variations dGamma_eff|Phi0=dK_hat|Phi0=0",
            "turns q_loc into an on-shell second-order residual rather than a plateau axiom",
            "SUFFICIENT_CLAUSE_NOT_DERIVED",
            "1010 marks Euler/double-zero missing",
        ),
        (
            "PAC1663_5_Ploc_parent_projector",
            "P_loc^nu_rho = delta^nu_rho + u^nu u_rho or tetrad equivalent, with u/e generated by parent matter clock/Fermi reference and no external Earth-frame filter",
            "prevents the projector from injecting preferred-frame leakage",
            "MISSING_PARENT_PROJECTOR_CERTIFICATE",
            "1662 and 1003 keep P_loc/coframe descent unsigned",
        ),
        (
            "PAC1663_6_boundary_symplectic_no_flux",
            "int_boundary Delta(theta_GK,Q_GK,tau)=0 and n_mu P_loc_nu K_hat^{mu nu}=0 on compact local collar unless retained",
            "prevents boundary work from re-entering q_loc as alpha3/frame flux",
            "MISSING_BOUNDARY_NO_FLUX_CERTIFICATE",
            "1010 and 469 retain boundary/source-current gaps",
        ),
        (
            "PAC1663_7_no_shadow_frame",
            "no Weyl/disformal/species/connection-frame channel survives outside Gamma_eff/K_hat/P_loc and the declared transfer map",
            "prevents a second metric/coframe from faking covariance",
            "MISSING_NO_SHADOW_FRAME_CERTIFICATE",
            "1003 rejects theorem-zero without no-shadow-frame certificate",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "clause_id": clause_id,
            "mathematical_clause": clause,
            "local_effect_if_true": effect,
            "status": status,
            "source_reason": source_reason,
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for clause_id, clause, effect, status, source_reason in rows
    ]


def tensor_descent_audit_rows() -> list[dict[str, object]]:
    rows = [
        ("TD1663_0_Gamma_eff", "Gamma_eff", "scalar quotient object", "PAC1663_1", "MISSING_SOURCE_FORMULA_OR_PARENT_SIGNATURE", "cannot prove nabla Gamma_eff is the same object in lab/Fermi frames"),
        ("TD1663_1_K_hat", "K_hat^{mu nu}", "metric-response tensor current", "PAC1663_2;PAC1663_3", "MISSING_METRIC_RESPONSE_AND_HELMHOLTZ", "bookkeeping stress can satisfy Ward but fail local GR"),
        ("TD1663_2_P_loc", "P_loc^nu_rho", "parent-owned projector/tetrad split", "PAC1663_5", "MISSING_PLOC_CERTIFICATE", "external projection can create or hide frame leakage"),
        ("TD1663_3_boundary", "boundary/symplectic flux", "zero or retained source row", "PAC1663_6", "MISSING_BOUNDARY_NO_FLUX", "projected K_hat flux can survive as alpha3/frame leak"),
        ("TD1663_4_frame_vertical", "Dq(v_frame)=0", "vertical frame directions are gauge of quotient map", "PAC1663_1;PAC1663_5;PAC1663_7", "MISSING_PARENT_FRAME_SIGNATURE", "frame-choice-by-convention remains forbidden"),
        ("TD1663_5_verdict", "q_loc tensor descent", "all clauses pass jointly", "PAC1663_0..PAC1663_7", "NOT_PARENT_SIGNED", "q_loc remains explicit residual/coefficient route"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "object": obj,
            "required_descent": required_descent,
            "depends_on": depends_on,
            "status": status,
            "failure_mode": failure_mode,
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for audit_id, obj, required_descent, depends_on, status, failure_mode in rows
    ]


def apparatus_transfer_contract_rows() -> list[dict[str, object]]:
    rows = [
        (
            "ATC1663_0_map_definition",
            "A_lab_to_Fermi: e_lab^a_mu -> e_F^a_mu by local Lorentz/transport map plus calibration terms",
            "maps lab components into the same freefall residual q_F^a = e_F^a_mu q_loc^mu",
            "MISSING_EXPLICIT_MAP",
        ),
        (
            "ATC1663_1_acceleration_term",
            "a_earth/c^2 is assigned to apparatus calibration only if A_lab_to_Fermi proves it does not enter q_F^a",
            "removes universal support acceleration from physical q_loc source",
            "MISSING_TRANSFER_CERTIFICATE",
        ),
        (
            "ATC1663_2_rotation_term",
            "Omega_earth/c is assigned to tetrad rotation/Sagnac transfer only if A_lab_to_Fermi proves it does not enter q_F^a",
            "removes the dominant frame fallback term",
            "MISSING_TRANSFER_CERTIFICATE",
        ),
        (
            "ATC1663_3_observable_equivalence",
            "R10/PPN/WEP observable residual equals the transformed freefall q_loc residual plus declared calibration terms",
            "prevents comparing different observables",
            "MISSING_OBSERVABLE_EQUIVALENCE",
        ),
        (
            "ATC1663_4_no_cancellation",
            "acceleration and rotation contributions are individually projected/transferred or individually retained",
            "blocks cancellation-by-fit",
            "POLICY_PASS_NONCLAIM",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "transfer_id": transfer_id,
            "transfer_clause": clause,
            "effect_if_true": effect,
            "status": status,
            "transfer_signed_for_claim": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for transfer_id, clause, effect, status in rows
    ]


def frame_leak_coefficient_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "FLC1663_0_frame_leak_coefficient_retained",
            "coefficient": "epsilon_frame_leak",
            "value_m1": f"{EPSILON_FRAME_LEAK_M1:.8e}",
            "source": "1662 retained max(a_earth/c^2, Omega_earth/c)",
            "conditional_curvature_bound_m1": f"{CONDITIONAL_CURVATURE_BOUND_M1:.8e}",
            "ratio_to_curvature_bound": f"{FRAME_RATIO:.8e}",
            "status": "RETAINED_NONCLAIM_COEFFICIENT_UNTIL_PARENT_TRANSFER_SIGNS",
            "use_if_derivation_fails": "blocks local GR/Newton/R10/PPN scoring unless bounded against the relevant observable denominator",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def claim_rows() -> list[dict[str, object]]:
    rows = [
        ("CG1663_0_parent_clause_written", "exact sufficient parent q_loc tensor contract is written", "CONTRACT_ONLY", "NONCLAIM", "clauses are sufficient targets but not parent-derived"),
        ("CG1663_1_Gamma_descent", "Gamma_eff descends as scalar quotient object", False, "BLOCKED", "missing source formula/parent signature"),
        ("CG1663_2_Khat_metric_response", "K_hat is metric response satisfying Helmholtz", False, "BLOCKED", "metric response and second variation not matched"),
        ("CG1663_3_Ploc_transfer", "P_loc and A_lab_to_Fermi are parent-signed", False, "BLOCKED", "projector certificate and apparatus transfer map missing"),
        ("CG1663_4_frame_leak_zero", "epsilon_frame_leak is zero/projected out", False, "NO_CLAIM", "coefficient retained"),
        ("CG1663_5_local", "local GR/Newton/PPN/R10/WEP follows", False, "NO_CLAIM", "q_loc tensor contract not parent-signed and M_H_ref still absent"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": gate_pass,
            "status": status,
            "blocker": blocker,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim, gate_pass, status, blocker in rows
    ]


def decision_rows() -> list[dict[str, object]]:
    rows = [
        ("DEC1663_0_contract", "EXACT_SUFFICIENT_PARENT_CONTRACT_WRITTEN", "the tensor descent route is now a concrete clause list rather than vague covariance language", "try to source/match Gamma_eff and K_hat metric-response formulas"),
        ("DEC1663_1_not_signed", "PARENT_SIGNATURES_MISSING", "1010 already shows S_GK/metric-response/Helmholtz/Euler/double-zero are not closed", "do not promote q_loc=0 or local-GR"),
        ("DEC1663_2_frame_leak", "FRAME_LEAK_COEFFICIENT_RETAINED", "apparatus transfer is not signed and Omega/c dominates", "carry epsilon_frame_leak as nonclaim penalty/coefficient"),
        ("DEC1663_3_next", "NEXT_1664_GAMMA_KHAT_METRIC_RESPONSE_MATCH", "the smallest decisive proof is to match actual Gamma_eff/K_hat formulas to a variational action", "run metric-response/Helmholtz source-formula obstruction test"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for decision_id, decision, reason, next_action in rows
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1664-Y5-R2FR-Gamma-Khat-metric-response-source-formula-or-Helmholtz-obstruction.md",
            "script": "scripts/Y5_R2FR_Gamma_Khat_metric_response_source_formula_or_Helmholtz_obstruction.py",
            "objective": "find or construct explicit Gamma_eff and K_hat formulas, test whether K_hat is the metric response of sqrt(-g)Gamma_eff and whether the Helmholtz symmetry can pass; otherwise keep q_loc/frame leak as explicit coefficients",
            "success_condition": "metric-response and Helmholtz clauses become source-backed, or the obstruction is recorded with retained q_loc/frame coefficients",
            "forbidden_shortcuts": "no plateau axiom; no bookkeeping stress; no Ward-ownership-as-zero; no local-GR/PPN/R10/WEP claim",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        }
    ]


def validation_rows(source_rows, clauses, descent, transfer, frame_leak, claim, decisions, next_targets):
    generated_csv_parse = True
    try:
        for generated_path in GENERATED:
            csv_rows(generated_path)
    except Exception:
        generated_csv_parse = False

    formalization_dirty = any(FORMALIZATION.rglob("*1663*")) if FORMALIZATION.exists() else False
    exact_contract_written = len(clauses) >= 8 and any(row["clause_id"] == "PAC1663_2_Khat_metric_response" for row in clauses)
    not_parent_signed = all(row["parent_signed"] is False for row in clauses + descent)
    transfer_blocked = any(str(row["status"]).startswith("MISSING") for row in transfer)
    frame_leak_retained = frame_leak[0]["status"] == "RETAINED_NONCLAIM_COEFFICIENT_UNTIL_PARENT_TRANSFER_SIGNS" and float(frame_leak[0]["ratio_to_curvature_bound"]) > 1.0

    checks = [
        ("VAL1663_0_sources_exist", all(row["path_exists"] and row["needles_found"] for row in source_rows), "all cited 1663 source paths exist and needles are present"),
        ("VAL1663_1_1662_passed", any(row["source_id"] == "1662_validation" and row["needles_found"] for row in source_rows), "1662 validation is source-registered as PASS"),
        ("VAL1663_2_contract_written", exact_contract_written, "sufficient parent q_loc tensor contract is written"),
        ("VAL1663_3_not_parent_signed", not_parent_signed, "contract rows remain unpromoted/nonclaim"),
        ("VAL1663_4_transfer_blocked", transfer_blocked, "apparatus transfer map remains explicitly blocked"),
        ("VAL1663_5_frame_leak_retained", frame_leak_retained, "epsilon_frame_leak coefficient remains retained and nonclaim"),
        ("VAL1663_6_claim_gates_safe", all(row["claim_allowed"] is False and row["valid_for_claim"] is False for row in claim), "all claim gates keep MTS claims false"),
        ("VAL1663_7_next_target_selected", next_targets[0]["next_target"] == "1664-Y5-R2FR-Gamma-Khat-metric-response-source-formula-or-Helmholtz-obstruction.md", "next target selects Gamma/Khat metric-response source-formula test"),
        ("VAL1663_8_csv_parse", generated_csv_parse, "all generated 1663 CSVs parse"),
        ("VAL1663_9_no_mts_claim_flags", all_claim_flags_false(CLAIM_CHECKED), "all 1663 generated rows keep MTS claim/no-score flags false"),
        ("VAL1663_10_branch_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" not in str(target)), "branch/quarantine copies exist"),
        ("VAL1663_11_queue_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" in str(target)), "acquisition queue nonclaim copies exist"),
        ("VAL1663_12_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1663_13_formalization_untouched", not formalization_dirty, "no 1663 outputs found under formalization-workbench"),
    ]
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1663_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1663 parent q_loc tensor action clause/frame leak coefficient validation",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row[column]) for column in columns) + " |")
    return "\n".join(lines)


def write_doc(source_rows, clauses, descent, transfer, frame_leak, claim, decisions, next_targets, validation) -> None:
    text = f"""# 1663 - Parent q_loc Tensor Action Clause Or Frame Leak Coefficient

**Private status:** parent-action contract checkpoint. No `q_loc=0`, local-GR pass, Newton pass, PPN pass, R10 pass, WEP pass, or public claim is made.

## Verdict

`1663` writes the exact sufficient parent-action contract, but does not promote it.

The route that would work is:

```text
Gamma_eff descends as a scalar quotient object.
K_hat is the metric response of sqrt(-g) Gamma_eff and passes Helmholtz.
P_loc is a parent-owned tetrad/projector, not an external Earth-frame filter.
A_lab_to_Fermi transfers Earth-fixed apparatus observables into the same freefall residual.
Boundary/symplectic flux and shadow-frame channels are zero or retained explicitly.
```

That is strong progress as a contract. It is not yet a derivation. The older `1010` action-existence gate already says the current corpus does not close `S_GK`, metric response, Helmholtz, Euler/double-zero, `P_loc`, and boundary clauses.

So the retained coefficient remains:

```text
epsilon_frame_leak = {frame_leak[0]["value_m1"]} m^-1
ratio_to_curvature_bound = {frame_leak[0]["ratio_to_curvature_bound"]}
```

## Source Register

{markdown_table(source_rows, ["source_id", "path", "path_exists", "needles_found", "role"])}

## Parent Action Clauses

{markdown_table(clauses, ["clause_id", "mathematical_clause", "local_effect_if_true", "status", "source_reason"])}

## Tensor Descent Audit

{markdown_table(descent, ["audit_id", "object", "required_descent", "depends_on", "status", "failure_mode"])}

## Apparatus Transfer Contract

{markdown_table(transfer, ["transfer_id", "transfer_clause", "effect_if_true", "status"])}

## Frame Leak Coefficient

{markdown_table(frame_leak, ["row_id", "coefficient", "value_m1", "conditional_curvature_bound_m1", "ratio_to_curvature_bound", "status", "use_if_derivation_fails"])}

## Claim Gates

{markdown_table(claim, ["gate_id", "claim", "gate_pass", "status", "blocker"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Next Target

{markdown_table(next_targets, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Working Interpretation

This is a narrowing, not a victory lap. The local branch now has an exact parent-action target. If MTS can source/match `Gamma_eff` and `K_hat` to a real variational density and pass Helmholtz, the local GR/Newton route becomes much more serious. If it cannot, `q_loc` and `epsilon_frame_leak` stay as explicit residual coefficients instead of hidden assumptions.
"""
    DOC.write_text(text, encoding="utf-8")


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)


def main() -> None:
    ensure_dirs()
    source_rows = source_register_rows()
    clauses = parent_action_clause_rows()
    descent = tensor_descent_audit_rows()
    transfer = apparatus_transfer_contract_rows()
    frame_leak = frame_leak_coefficient_rows()
    claim = claim_rows()
    decisions = decision_rows()
    next_targets = next_rows()

    for path, rows in [
        (SOURCE_REGISTER, source_rows),
        (PARENT_ACTION_CLAUSES, clauses),
        (TENSOR_DESCENT_AUDIT, descent),
        (APPARATUS_TRANSFER_CONTRACT, transfer),
        (FRAME_LEAK_COEFFICIENT, frame_leak),
        (CLAIM_GATE, claim),
        (DECISION, decisions),
        (NEXT_TARGET, next_targets),
    ]:
        write_csv(path, rows)

    copy_outputs()
    validation = validation_rows(source_rows, clauses, descent, transfer, frame_leak, claim, decisions, next_targets)
    write_csv(VALIDATION, validation)
    write_doc(source_rows, clauses, descent, transfer, frame_leak, claim, decisions, next_targets, validation)

    if any(row["result"] == "FAIL" for row in validation):
        raise SystemExit("1663 validation failed; see P8_Y5_BRR545_1663_VALIDATION.csv")

    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    print("1663 validation PASS")


if __name__ == "__main__":
    main()
