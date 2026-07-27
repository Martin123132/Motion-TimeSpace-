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
QUARANTINE = MICROSCOPE / "quarantine" / "1683"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1683-Y5-R2FR-first-Rsource-coefficient-fill-or-source-current-owner-derivation.md"

SOURCE_FILES = {
    "1682_doc": ROOT / "1682-Y5-R2FR-source-branch-runner-import-gate-and-parent-clause-search.md",
    "1682_validation": OUT / "P8_Y5_BRR545_1682_VALIDATION.csv",
    "1682_gate_dry": OUT / "P8_Y5_PARENT_QLOC_1682_RUNNER_IMPORT_GATE_DRY_RUN.csv",
    "1682_parent_search": OUT / "P8_Y5_PARENT_QLOC_1682_PARENT_CLAUSE_SEARCH_LEDGER.csv",
    "1682_gate_module": ROOT / "scripts" / "Rsource_runner_gate_1682.py",
    "1680_contract": OUT / "P8_Y5_PARENT_QLOC_1680_FINITE_RSOURCE_COEFFICIENT_CONTRACT_NONCLAIM.csv",
    "1681_result_matrix": OUT / "P8_Y5_PARENT_QLOC_1681_VALIDATOR_RESULT_MATRIX.csv",
    "1417_qbar_acquisition": OUT / "P8_Y5_R10_1417_QBAR_SOURCE_WEIGHT_ACQUISITION_ROWS.csv",
    "1418_qbar_arena": OUT / "P8_Y5_R10_1418_QBAR_SOURCE_WEIGHT_ARENA_ACQUISITION_LEDGER.csv",
    "1604_source_action_weight": OUT / "P8_Y5_PARENT_QLOC_1604_SOURCE_ACTION_WEIGHT_CONTRACT.csv",
    "source_current_ward": OUT / "P8_source_current_Ward_universality_CONTRACT.csv",
    "constant_sector": OUT / "P8_constant_sector_universality_CONTRACT.csv",
    "1311_source_audit": OUT / "P8_Y5_R10_1311_COEFFICIENT_SOURCE_AUDIT.csv",
    "1453_current_owner": OUT / "P8_Y5_R10_1453_CURRENT_SOURCE_NORMALIZATION_OWNER_THEOREM_ATTEMPT.csv",
    "1078_current_owner": OUT / "P8_Y5_R10_1078_CURRENT_OWNER_PROOF_ATTEMPT.csv",
    "1677_owner_attempt": OUT / "P8_Y5_PARENT_QLOC_1677_SOURCE_CURRENT_OWNER_ATTEMPT.csv",
}

NEEDLES = {
    "1682_doc": ["fail-closed runner gate", "first finite `R_source` coefficient"],
    "1682_validation": ["VAL1682_OVERALL", "PASS"],
    "1682_gate_dry": ["DRY1682_WEP", "SOURCE_BRANCH_GATE_REJECTED"],
    "1682_parent_search": ["PCS1682_1_current_owner", "REJECT_MISSING_CURRENT_OWNER"],
    "1682_gate_module": ["def require_source_branch_gate", "SOURCE_BRANCH_GATE_REJECTED"],
    "1680_contract": ["RFC1680_0", "qbar_source_weight"],
    "1681_result_matrix": ["RFC1680_0", "REJECT_MISSING_ZERO_OR_VALUE_SOURCE_PATH_PARENT_BASIS_OR_ARENA_PROJECTION"],
    "1417_qbar_acquisition": ["QSA1417_0_qbar_source_weight", "MISSING_SOURCE_WEIGHT_EXCLUSION_OR_COEFFICIENT"],
    "1418_qbar_arena": ["QAA1418_0_WEP_source_charge", "QBAR_ARENA_LEDGER_SOURCE_READY_BUT_UNSCORED"],
    "1604_source_action_weight": ["CON1604_0_action_density_owner", "UNSIGNED"],
    "source_current_ward": ["SC3_universal_kappa_coupling", "not_parent_derived"],
    "constant_sector": ["C3_universal_source_variation", "not_parent_derived"],
    "1311_source_audit": ["QCSA1311_5_qbar_source_weight", "NONE"],
    "1453_current_owner": ["CSO1453_7_verdict", "PARTIAL_THEOREM_NOT_CLOSED"],
    "1078_current_owner": ["CO1078_4_verdict", "CURRENT_OWNER_NOT_SIGNED"],
    "1677_owner_attempt": ["SCO1677_5_verdict", "SOURCE_CURRENT_OWNER_NOT_DERIVED"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1683_SOURCE_REGISTER.csv"
OWNER_DERIVATION = OUT / "P8_Y5_PARENT_QLOC_1683_SOURCE_CURRENT_OWNER_DERIVATION_ATTEMPT.csv"
FIRST_TARGET = OUT / "P8_Y5_PARENT_QLOC_1683_FIRST_RSOURCE_COEFFICIENT_TARGET.csv"
FILL_ATTEMPT = OUT / "P8_Y5_PARENT_QLOC_1683_QBAR_SOURCE_WEIGHT_FILL_ATTEMPT_NONCLAIM.csv"
ACQUISITION_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1683_QBAR_SOURCE_WEIGHT_ACQUISITION_LEDGER.csv"
GATE_SMOKE = OUT / "P8_Y5_PARENT_QLOC_1683_GATE_SMOKE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1683_DECISION.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1683_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1683_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1683_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    OWNER_DERIVATION,
    FIRST_TARGET,
    FILL_ATTEMPT,
    ACQUISITION_LEDGER,
    GATE_SMOKE,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    OWNER_DERIVATION,
    FIRST_TARGET,
    FILL_ATTEMPT,
    ACQUISITION_LEDGER,
    GATE_SMOKE,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

COPY_TARGETS = {
    OWNER_DERIVATION: [
        QUARANTINE / "SOURCE_CURRENT_OWNER_DERIVATION_ATTEMPT.csv",
        BRANCH_RESIDUALS / "R2FR_source_current_owner_derivation_attempt_1683.csv",
        QUEUE / "JR1683_SOURCE_CURRENT_OWNER_DERIVATION_ATTEMPT.csv",
    ],
    FILL_ATTEMPT: [
        QUARANTINE / "QBAR_SOURCE_WEIGHT_FILL_ATTEMPT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_qbar_source_weight_fill_attempt_nonclaim_1683.csv",
        QUEUE / "JR1683_QBAR_SOURCE_WEIGHT_FILL_ATTEMPT_NONCLAIM.csv",
    ],
    ACQUISITION_LEDGER: [
        QUARANTINE / "QBAR_SOURCE_WEIGHT_ACQUISITION_LEDGER.csv",
        BRANCH_RESIDUALS / "R2FR_qbar_source_weight_acquisition_ledger_1683.csv",
        QUEUE / "JR1683_QBAR_SOURCE_WEIGHT_ACQUISITION_LEDGER.csv",
    ],
    GATE_SMOKE: [
        QUARANTINE / "GATE_SMOKE.csv",
        BRANCH_RESIDUALS / "R2FR_gate_smoke_1683.csv",
        QUEUE / "JR1683_GATE_SMOKE.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_nonclaim_1683.csv",
        QUEUE / "JR1683_NEXT_TARGET_NONCLAIM.csv",
    ],
}

EXPECTED_ARENAS = {"WEP", "R10", "NEWTON_GM", "R11"}
SCORE_FLAGS = [
    "owner_signed",
    "coefficient_filled",
    "gate_pass",
    "accepted_for_scoring",
    "score_ready",
    "valid_prediction_row",
    "valid_for_claim",
    "claim_allowed",
]


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def bool_cell(value: object) -> bool:
    return str(value).strip().lower() == "true"


def blocked_marker(value: object) -> bool:
    text = str(value)
    markers = ["MISSING_", "NOT_", "BLOCKED", "REJECT", "FAIL", "DRY_RUN", "CONDITIONAL", "UNSIGNED", "NONE", "TEMPLATE", "NO_PASS"]
    return any(marker in text for marker in markers)


def source_register_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_key, source_path in SOURCE_FILES.items():
        exists = source_path.exists()
        body = read_text(source_path) if exists else ""
        needles_present = all(needle in body for needle in NEEDLES[source_key])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_key": source_key,
                "source_path": str(source_path),
                "exists": exists,
                "needles_present": needles_present,
                "required_needles": "; ".join(NEEDLES[source_key]),
                "use_in_1683": "first R_source coefficient fill or source-current owner derivation",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def owner_derivation_rows() -> list[dict[str, object]]:
    rows = [
        (
            "OWN1683_0_hilbert",
            "Hilbert source current from variation before readout",
            "T_H := delta S_matter/delta e_obs before detector/material/source selectors",
            "CONDITIONAL_EXACT_SUBTHEOREM",
            "kills post-variation source-current redefinition only if readout order is parent-signed",
            "CSO1453_1_hilbert_variation;CO1078_2_hilbert_source_route",
        ),
        (
            "OWN1683_1_ward",
            "Ward conservation",
            "diffeomorphism/local Lorentz Ward identities conserve the owned Hilbert current on shell",
            "HELPFUL_BUT_INSUFFICIENT",
            "conserved weighted sums w_A T_A remain possible if weights enter before variation",
            "SC2_Ward_conservation_on_matter_shell;CSO1453_2_ward_identity",
        ),
        (
            "OWN1683_2_pre_variation_weights",
            "pre-variation species/source action weights",
            "S_matter=sum_A w_A S_A or kappa_A T_A",
            "COUNTERMODEL_SURVIVES",
            "source-current owner alone cannot remove weights inserted into S_matter before variation",
            "CSO1453_5_pre_variation_weight;CON1604_0_action_density_owner",
        ),
        (
            "OWN1683_3_source_label_forgetting",
            "source labels are forgotten before gravity chooses a current",
            "F_src({(T_A,A)}) = kappa_univ sum_A T_A rather than sum_A kappa_A T_A",
            "NOT_PARENT_SIGNED",
            "would kill qbar_source_weight but remains closure-only",
            "SCO1677_1_source_label_forgetting;SC3_universal_kappa_coupling",
        ),
        (
            "OWN1683_4_current_rescaling",
            "post-variation current rescaling",
            "J_A -> c_A J_A or beta_source,A marker",
            "CURRENT_OWNER_NOT_SIGNED",
            "post-variation rescaling is conditionally controlled, but current owner remains unsigned",
            "SCO1677_2_current_rescaling_guard;CO1078_3_current_rescaling_counterexample",
        ),
        (
            "OWN1683_5_verdict",
            "single source-current owner / NoSourceOnlySpeciesSlot closes",
            "assemble Hilbert variation, Ward identity, source-label forgetting, action-measure owner, readout stability",
            "OWNER_DERIVATION_FAILS_CURRENT_CORPUS",
            "qbar_source_weight cannot be theorem-zero; fill finite row or keep gate locked",
            "CSO1453_7_verdict;CO1078_4_verdict;SCO1677_5_verdict",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": attempt_id,
            "claim": claim,
            "mathematical_form": mathematical_form,
            "current_result": current_result,
            "consequence": consequence,
            "source_anchor": source_anchor,
            "owner_signed": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for attempt_id, claim, mathematical_form, current_result, consequence, source_anchor in rows
    ]


def first_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "target_id": "TARGET1683_0",
            "basis_component": "qbar_source_weight",
            "coefficient_symbol": "zeta_source_weight_I",
            "why_first": "it is the sharpest source-side obstruction and appears in WEP, Newton-GM, R10, R11, PPN, and local-GR links",
            "canonical_definition": "zeta_source_weight_I := partial_{X_I} ln kappa_A or a no-cancellation envelope for partial_{X_I} ln(kappa_A/kappa_B) in the parent source-current basis",
            "zero_route": "NoSourceOnlySpeciesSlot plus single action-measure owner plus source-label forgetting",
            "finite_route": "source-backed coefficient/bound for kappa_A or w_A with species/source tags, sign, units, parent basis, uncertainty, and arena projection",
            "current_status": "FIRST_TARGET_SELECTED_VALUE_MISSING",
            "coefficient_filled": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def fill_attempt_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "fill_id": "FILL1683_0_qbar_source_weight",
            "contract_id": "RFC1680_0",
            "quantity": "qbar_source_weight",
            "coefficient_symbol": "zeta_source_weight_I",
            "candidate_formula": "zeta_source_weight_I = partial_{X_I} ln kappa_A; envelope = sup_{A,B}|partial_{X_I} ln(kappa_A/kappa_B)|",
            "candidate_value": "MISSING_SOURCE_WEIGHT_EXCLUSION_OR_COEFFICIENT",
            "units": "dimensionless in declared parent source-current basis",
            "sign_convention": "MISSING_SIGN_CONVENTION",
            "source_path": "MISSING_VALUE_SOURCE_PATH",
            "source_anchor": "QSA1417_0_qbar_source_weight;QCSA1311_5_qbar_source_weight;RFC1680_0",
            "parent_basis": "MISSING_PARENT_COUPLING_BASIS",
            "arena_projection": "MISSING_WEP_R10_NEWTON_R11_PROJECTION",
            "no_cancellation_policy": "ACTIVE",
            "fill_result": "FILL_FAILED_VALUE_AND_ZERO_THEOREM_MISSING",
            "coefficient_filled": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def acquisition_rows() -> list[dict[str, object]]:
    rows = [
        ("ACQ1683_0_parent_action", "parent action clause forbidding or defining kappa_A/w_A", "source file must state source-label forgetting or one common action-density/source coupling before variation", "MISSING_PARENT_ACTION_OWNER_CLAUSE", "derive NoSourceOnlySpeciesSlot or keep finite row"),
        ("ACQ1683_1_value", "finite value or bound for zeta_source_weight_I", "numeric/symbolic coefficient, uncertainty, sign, material/source tags", "MISSING_COEFFICIENT_VALUE", "source qbar_source_weight or bound as finite residual"),
        ("ACQ1683_2_basis", "parent source-current basis X_I", "basis coordinate, normalization, dimension, and sign convention", "MISSING_PARENT_COUPLING_BASIS", "needed before any arena comparison"),
        ("ACQ1683_3_source_path", "local source path and anchor for value/zero proof", "not a template row; must support the coefficient or theorem-zero claim", "MISSING_VALUE_SOURCE_PATH", "blocks validator pass"),
        ("ACQ1683_4_arena_projection", "WEP/R10/Newton/R11 projection kernels", "tau/material/worldtube, alpha(lambda) pieces, GM calibration, R11 operator projection", "MISSING_ARENA_PROJECTION", "blocks source-side scoring"),
        ("ACQ1683_5_gate", "1682 import gate", "require_source_branch_gate must remain called by downstream runners", "GATE_ACTIVE_REJECTS_CURRENT_BRANCH", "prevents accidental local-GR/source claim"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "acquisition_id": acquisition_id,
            "needed_object": needed_object,
            "acceptance_condition": acceptance_condition,
            "current_status": current_status,
            "next_action": next_action,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for acquisition_id, needed_object, acceptance_condition, current_status, next_action in rows
    ]


def gate_smoke_rows() -> list[dict[str, object]]:
    dry_rows = read_csv(SOURCE_FILES["1682_gate_dry"])
    rows: list[dict[str, object]] = []
    for arena in ["WEP", "R10", "NEWTON_GM", "R11"]:
        matching = next(row for row in dry_rows if row["arena"] == arena)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "smoke_id": f"SMOKE1683_{arena}",
                "arena": arena,
                "gate_module": str(SOURCE_FILES["1682_gate_module"]),
                "gate_pass": matching["gate_pass"],
                "reason": matching["reason"],
                "expected_behavior": "REJECT_UNTIL_FIRST_COEFFICIENT_OR_OWNER_DERIVATION_IS_REAL",
                "accepted_for_scoring": False,
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def decision_rows() -> list[dict[str, object]]:
    rows = [
        ("D1683_0_owner", "OWNER_DERIVATION_FAILS", "Hilbert/Ward route is conditional and cannot kill pre-variation source weights", "do not claim qbar_source_weight theorem-zero"),
        ("D1683_1_first_row", "QBAR_SOURCE_WEIGHT_FIRST_ROW_SELECTED", "qbar_source_weight is the first finite R_source row to fill because it touches WEP/Newton/R10/R11/local-GR", "fill coefficient or derive source-label forgetting"),
        ("D1683_2_fill", "FIRST_FILL_FAILED_NONCLAIM", "no source-backed value, parent basis, sign convention, source path, or arena projection is present", "keep 1682 gate locked"),
        ("D1683_3_next", "ACQUIRE_SOURCE_WEIGHT_VALUE_OR_PROVE_SOURCE_LABEL_FORGETTING", "the next useful move is specific, not broad: attack kappa_A/w_A directly", "move to 1684"),
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


def claim_gate_rows() -> list[dict[str, object]]:
    rows = [
        ("CG1683_0_owner", "source-current owner theorem", "BLOCKED", "owner derivation fails current corpus"),
        ("CG1683_1_qbar_zero", "qbar_source_weight theorem-zero", "BLOCKED", "NoSourceOnlySpeciesSlot/source-label forgetting not parent-signed"),
        ("CG1683_2_qbar_value", "qbar_source_weight finite value", "BLOCKED", "coefficient value/source path/parent basis/sign/projection missing"),
        ("CG1683_3_gate", "1682 source branch gate pass", "BLOCKED", "gate smoke rejects WEP/R10/Newton/R11"),
        ("CG1683_4_local_GR", "local GR/Newton/PPN source-side pass", "BLOCKED", "first source coefficient is not filled or zeroed"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate": gate,
            "gate_pass": False,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate, status, reason in rows
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1684-Y5-R2FR-qbar-source-weight-value-hunt-or-source-label-forgetting-proof.md",
            "script": "scripts/Y5_R2FR_qbar_source_weight_value_hunt_or_source_label_forgetting_proof.py",
            "objective": "focus narrowly on qbar_source_weight: either prove source-label forgetting/NoSourceOnlySpeciesSlot from parent action data, or acquire a source-backed finite kappa_A/w_A coefficient row with units, sign, basis, uncertainty, source path, and WEP/R10/Newton/R11 projection hooks",
            "success_condition": "qbar_source_weight becomes theorem-zero or has a real nonclaim finite coefficient row that the 1681/1682 validator can inspect; no arena scores until the gate passes",
            "why_next": "1683 shows broad owner derivation still fails; the highest-leverage concrete advance is the first source-weight row itself",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def copy_outputs() -> None:
    for source_path, target_paths in COPY_TARGETS.items():
        for target_path in target_paths:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, target_path)


def validate(
    source_rows: list[dict[str, object]],
    owner_rows: list[dict[str, object]],
    target_rows: list[dict[str, object]],
    fill_rows: list[dict[str, object]],
    acquisition_rows_: list[dict[str, object]],
    smoke_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claims: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    sources_ok = all(bool_cell(row["exists"]) and bool_cell(row["needles_present"]) for row in source_rows)
    owner_fails = any(row["current_result"] == "OWNER_DERIVATION_FAILS_CURRENT_CORPUS" for row in owner_rows) and all(not bool_cell(row["owner_signed"]) for row in owner_rows)
    target_exact = len(target_rows) == 1 and target_rows[0]["basis_component"] == "qbar_source_weight"
    fill_failed = len(fill_rows) == 1 and fill_rows[0]["fill_result"] == "FILL_FAILED_VALUE_AND_ZERO_THEOREM_MISSING" and not bool_cell(fill_rows[0]["coefficient_filled"])
    acquisition_complete = {row["needed_object"] for row in acquisition_rows_} == {
        "parent action clause forbidding or defining kappa_A/w_A",
        "finite value or bound for zeta_source_weight_I",
        "parent source-current basis X_I",
        "local source path and anchor for value/zero proof",
        "WEP/R10/Newton/R11 projection kernels",
        "1682 import gate",
    }
    smoke_exact = {row["arena"] for row in smoke_rows} == EXPECTED_ARENAS
    smoke_rejects = all(row["gate_pass"] == "False" and row["reason"] == "SOURCE_BRANCH_GATE_REJECTED" for row in smoke_rows)
    decision_safe = any(row["decision"] == "FIRST_FILL_FAILED_NONCLAIM" for row in decisions)
    claim_gate_safe = all(not bool_cell(row["gate_pass"]) and not bool_cell(row["claim_allowed"]) for row in claims)
    next_target_selected = next_rows[0]["next_target"] == "1684-Y5-R2FR-qbar-source-weight-value-hunt-or-source-label-forgetting-proof.md"
    csv_parse = all(path.exists() and len(read_csv(path)) >= 1 for path in GENERATED)
    branch_copies = all(target_path.exists() for target_paths in COPY_TARGETS.values() for target_path in target_paths)
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_clean = not any(FORMALIZATION.rglob("*1683*")) if FORMALIZATION.exists() else True

    no_claim_flags = True
    blocked_not_ready = True
    for generated_path in CLAIM_CHECKED:
        for generated_row in read_csv(generated_path):
            if generated_row.get("valid_for_claim", "False").lower() == "true" or generated_row.get("claim_allowed", "False").lower() == "true":
                no_claim_flags = False
            if any(blocked_marker(value) for value in generated_row.values()):
                for claim_key in SCORE_FLAGS:
                    if claim_key in generated_row and bool_cell(generated_row[claim_key]):
                        blocked_not_ready = False

    checks = [
        ("VAL1683_0_sources_exist", sources_ok, "all cited 1683 source paths exist and required needles are present"),
        ("VAL1683_1_owner_fails", owner_fails, "source-current owner derivation remains unsigned"),
        ("VAL1683_2_target_exact", target_exact, "first coefficient target is qbar_source_weight"),
        ("VAL1683_3_fill_failed", fill_failed, "first coefficient fill fails because value/zero theorem is missing"),
        ("VAL1683_4_acquisition_complete", acquisition_complete, "qbar acquisition ledger lists all required next objects"),
        ("VAL1683_5_smoke_exact", smoke_exact, "gate smoke covers WEP, R10, Newton-GM, and R11"),
        ("VAL1683_6_smoke_rejects", smoke_rejects, "1682 gate still rejects all source arenas"),
        ("VAL1683_7_decision_safe", decision_safe, "decision records first fill failed as nonclaim"),
        ("VAL1683_8_claim_gate_safe", claim_gate_safe, "all claim gates remain false"),
        ("VAL1683_9_no_claim_flags", no_claim_flags, "all generated rows keep claim flags false"),
        ("VAL1683_10_blocked_not_ready", blocked_not_ready, "no blocked/missing row is marked claim/scoring ready"),
        ("VAL1683_11_next_target_selected", next_target_selected, "next target selects qbar source-weight value hunt or source-label forgetting proof"),
        ("VAL1683_12_csv_parse", csv_parse, "all generated 1683 CSVs parse"),
        ("VAL1683_13_branch_copies", branch_copies, "branch/quarantine/queue copies exist"),
        ("VAL1683_14_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL1683_15_formalization_untouched", formalization_clean, "no 1683 outputs found under formalization-workbench"),
    ]
    overall = all(result for _, result, _ in checks)
    validation_rows = [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, result, detail in checks
    ]
    validation_rows.append(
        {
            "check_id": "VAL1683_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1683 first Rsource coefficient fill or source-current owner derivation validation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return validation_rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    table_rows = []
    for row in rows:
        table_rows.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, separator, *table_rows])


def write_doc(
    source_rows: list[dict[str, object]],
    owner_rows: list[dict[str, object]],
    target_rows: list[dict[str, object]],
    fill_rows: list[dict[str, object]],
    acquisition_rows_: list[dict[str, object]],
    smoke_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    body = f"""# 1683 - First Rsource Coefficient Fill Or Source-Current Owner Derivation

**Private status:** derivation/fill checkpoint. No `q_loc=0`, local-GR pass, Newton pass, PPN pass, WEP pass, R10 pass, R11 pass, clock pass, orbital pass, or public claim is made.

## Verdict

The source-current owner route still does **not** close. Hilbert variation and Ward identities are useful, but they do not remove pre-variation `w_A` / `kappa_A` source weights unless the parent action also signs source-label forgetting, one action-measure owner, readout order, and radiative stability.

The first finite `R_source` coefficient target is therefore `qbar_source_weight`, represented here as `zeta_source_weight_I`. The fill attempt fails honestly: no theorem-zero, no coefficient value, no signed parent basis, no value source path, and no arena projection are present. The 1682 gate remains locked.

## Source Register

{markdown_table(source_rows, ["source_key", "source_path", "exists", "needles_present", "use_in_1683"])}

## Source-Current Owner Derivation Attempt

{markdown_table(owner_rows, ["attempt_id", "claim", "mathematical_form", "current_result", "consequence"])}

## First Coefficient Target

{markdown_table(target_rows, ["target_id", "basis_component", "coefficient_symbol", "why_first", "canonical_definition", "current_status"])}

## Qbar Source-Weight Fill Attempt

{markdown_table(fill_rows, ["fill_id", "quantity", "candidate_formula", "candidate_value", "parent_basis", "arena_projection", "fill_result"])}

## Acquisition Ledger

{markdown_table(acquisition_rows_, ["acquisition_id", "needed_object", "acceptance_condition", "current_status", "next_action"])}

## Gate Smoke

{markdown_table(smoke_rows, ["smoke_id", "arena", "gate_pass", "reason", "expected_behavior"])}

## Decisions

{markdown_table(decision_rows_, ["decision_id", "decision", "reason", "next_action"])}

## Claim Gates

{markdown_table(claim_rows, ["gate_id", "gate", "gate_pass", "status", "reason"])}

## Next Target

{markdown_table(next_rows, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Working Interpretation

We have not won the source-side GR reduction. But we have stopped circling: the first concrete object is now `qbar_source_weight`. Either prove source-label forgetting from the parent action, or fill `zeta_source_weight_I` as a finite coefficient with units/sign/source/projection. Until then, the runner gate is doing its job.
"""
    DOC.write_text(body, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    source_rows = source_register_rows()
    owner_rows = owner_derivation_rows()
    target_rows = first_target_rows()
    fill_rows = fill_attempt_rows()
    acquisition_rows_ = acquisition_rows()
    smoke_rows = gate_smoke_rows()
    decisions = decision_rows()
    claims = claim_gate_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, source_rows, ["branch_id", "source_key", "source_path", "exists", "needles_present", "required_needles", "use_in_1683", "valid_for_claim", "claim_allowed"])
    write_csv(OWNER_DERIVATION, owner_rows, ["branch_id", "attempt_id", "claim", "mathematical_form", "current_result", "consequence", "source_anchor", "owner_signed", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(FIRST_TARGET, target_rows, ["branch_id", "target_id", "basis_component", "coefficient_symbol", "why_first", "canonical_definition", "zero_route", "finite_route", "current_status", "coefficient_filled", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(FILL_ATTEMPT, fill_rows, ["branch_id", "fill_id", "contract_id", "quantity", "coefficient_symbol", "candidate_formula", "candidate_value", "units", "sign_convention", "source_path", "source_anchor", "parent_basis", "arena_projection", "no_cancellation_policy", "fill_result", "coefficient_filled", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(ACQUISITION_LEDGER, acquisition_rows_, ["branch_id", "acquisition_id", "needed_object", "acceptance_condition", "current_status", "next_action", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(GATE_SMOKE, smoke_rows, ["branch_id", "smoke_id", "arena", "gate_module", "gate_pass", "reason", "expected_behavior", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(DECISION, decisions, ["branch_id", "decision_id", "decision", "reason", "next_action", "valid_for_claim", "claim_allowed"])
    write_csv(CLAIM_GATE, claims, ["branch_id", "gate_id", "gate", "gate_pass", "status", "reason", "valid_for_claim", "claim_allowed"])
    write_csv(NEXT_TARGET, next_rows, ["branch_id", "next_target", "script", "objective", "success_condition", "why_next", "valid_for_claim", "claim_allowed"])

    copy_outputs()
    validation_rows = validate(source_rows, owner_rows, target_rows, fill_rows, acquisition_rows_, smoke_rows, decisions, claims, next_rows)
    write_csv(VALIDATION, validation_rows, ["check_id", "result", "detail", "valid_for_claim", "claim_allowed"])
    write_doc(source_rows, owner_rows, target_rows, fill_rows, acquisition_rows_, smoke_rows, decisions, claims, next_rows, validation_rows)

    failed_rows = [row for row in validation_rows if row["result"] != "PASS"]
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    if failed_rows:
        for failed_row in failed_rows:
            print(f"FAIL {failed_row['check_id']}: {failed_row['detail']}")
        raise SystemExit(1)
    print("1683 validation PASS")


if __name__ == "__main__":
    main()
