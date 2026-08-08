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
QUARANTINE = MICROSCOPE / "quarantine" / "1639"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1639-Y5-R2FR-qR-normalization-denominator-or-PiR-source-acquisition.md"

SOURCE_FILES = {
    "1638_doc": ROOT / "1638-Y5-R2FR-PiR-bound-source-acquisition-and-qR-normalization.md",
    "1638_validation": OUT / "P8_Y5_BRR545_1638_VALIDATION.csv",
    "1638_next": OUT / "P8_Y5_PARENT_QLOC_1638_NEXT_TARGET.csv",
    "1638_chain": OUT / "P8_Y5_PARENT_QLOC_1638_PIR_TO_QR_QRLOCAL_CHAIN.csv",
    "1638_blockers": OUT / "P8_Y5_PARENT_QLOC_1638_QR_NORMALIZATION_BLOCKER_LEDGER.csv",
    "05_reciprocity": ROOT / "05-reciprocity-theorem-attempt.md",
    "06_source_neutrality": ROOT / "06-reciprocal-charge-source-neutrality.md",
    "02_motion_load": ROOT / "02-motion-load-local-GR-reduction.md",
    "10_observer": ROOT / "10-observer-map-symplectic-contract.md",
    "1006_denominator_guard": ROOT / "1006-Y5-R10-MHref-positive-same-frame-denominator-or-Htau-source-row.md",
}

NEEDLES = {
    "1638_doc": ["q_R = N_R Q_R = -N_R Pi_R", "denominator `N_R`"],
    "1638_validation": ["VAL1638_OVERALL", "PASS"],
    "1638_next": ["1639-Y5-R2FR-qR-normalization-denominator-or-PiR-source-acquisition.md", "do not set N_R=1"],
    "1638_chain": ["Q_R = -Pi_R", "Q_R_TO_q_R_NORMALIZATION_MISSING"],
    "1638_blockers": ["N_R_DENOMINATOR_FOR_QR_TO_qR", "W_RAB_EQUATION_NORMALIZATION"],
    "05_reciprocity": ["W R_AB' = Q_R", "R_AB ~ Q_R/r"],
    "06_source_neutrality": ["R_AB = q_R L", "L = 2GM/(rc^2).", "gamma - 1 ~= q_R"],
    "02_motion_load": ["L = 2GM/(rc^2) = 2U/c^2", "gamma = p"],
    "10_observer": ["T^2 = 1 - 2U/c^2", "gamma - 1 = 0 after R_AB=0"],
    "1006_denominator_guard": ["orbital GM substitution is explicitly rejected", "M_H_ref denominator"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1639_SOURCE_REGISTER.csv"
DERIVATION = OUT / "P8_Y5_PARENT_QLOC_1639_NR_DENOMINATOR_DERIVATION.csv"
NR_LAW = OUT / "P8_Y5_PARENT_QLOC_1639_NR_LAW_CONDITIONAL.csv"
BOUND_TEMPLATE = OUT / "P8_Y5_PARENT_QLOC_1639_PIR_QR_QRLOCAL_BOUND_TEMPLATE.csv"
BLOCKERS = OUT / "P8_Y5_PARENT_QLOC_1639_SOURCE_MASS_AND_TAIL_BLOCKERS.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1639_DECISION.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1639_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1639_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1639_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    DERIVATION,
    NR_LAW,
    BOUND_TEMPLATE,
    BLOCKERS,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    DERIVATION,
    NR_LAW,
    BOUND_TEMPLATE,
    BLOCKERS,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]


def ensure_dirs() -> None:
    for directory_path in [OUT, QUARANTINE, BRANCH_RESIDUALS, QUEUE]:
        directory_path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


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


def source_paths_exist(value: str) -> bool:
    if value.startswith("MISSING_") or value == "":
        return False
    paths = [Path(part.strip()) for part in value.split(";") if part.strip() and not part.strip().startswith("MISSING_")]
    return bool(paths) and all(path.exists() for path in paths)


def source_register_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
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
                "role": "1639 q_R normalization denominator derivation and guardrail",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def derivation_rows() -> list[dict[str, object]]:
    sources_tail = ";".join([str(SOURCE_FILES["05_reciprocity"]), str(SOURCE_FILES["1638_chain"])])
    sources_load = ";".join([str(SOURCE_FILES["06_source_neutrality"]), str(SOURCE_FILES["02_motion_load"])])
    return [
        {
            "branch_id": BRANCH_ID,
            "step_id": "NRD1639_0_exterior_tail",
            "input_relation": "R_AB(r) ~ Q_R/r",
            "operation": "read Q_R as the coefficient of the exterior 1/r reciprocal strain tail",
            "output_relation": "C_R = Q_R under the current corpus tail normalization",
            "status": "TAIL_COEFFICIENT_NORMALIZATION_CONDITIONAL",
            "source_paths": sources_tail,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "step_id": "NRD1639_1_local_load",
            "input_relation": "R_AB = q_R L_N and L_N(r)=2GM_*/(r c^2)",
            "operation": "solve q_R = R_AB/L_N",
            "output_relation": "q_R = R_AB r c^2/(2 G M_*)",
            "status": "LOCAL_LOAD_DENOMINATOR_FOUND_IN_CORPUS",
            "source_paths": sources_load,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "step_id": "NRD1639_2_compare_coefficients",
            "input_relation": "R_AB(r)~Q_R/r and L_N(r)=2GM_*/(r c^2)",
            "operation": "match the common 1/r radial dependence and cancel r",
            "output_relation": "q_R = Q_R c^2/(2 G M_*)",
            "status": "N_R_CONDITIONAL_DERIVED",
            "source_paths": ";".join([str(SOURCE_FILES["05_reciprocity"]), str(SOURCE_FILES["06_source_neutrality"]), str(SOURCE_FILES["02_motion_load"])]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "step_id": "NRD1639_3_boundary_momentum",
            "input_relation": "Q_R = -Pi_R",
            "operation": "substitute the boundary relation into the local PPN parameter",
            "output_relation": "q_R = -Pi_R c^2/(2 G M_*)",
            "status": "PIR_TO_qR_AMPLITUDE_LAW_CONDITIONAL",
            "source_paths": ";".join([str(SOURCE_FILES["06_source_neutrality"]), str(SOURCE_FILES["1638_chain"])]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "step_id": "NRD1639_4_ppn_projection",
            "input_relation": "Delta gamma ~= q_R",
            "operation": "compose local PPN projection with the denominator law",
            "output_relation": "Delta gamma ~= -Pi_R c^2/(2 G M_*)",
            "status": "PPN_AMPLITUDE_TEMPLATE_CONDITIONAL",
            "source_paths": ";".join([str(SOURCE_FILES["06_source_neutrality"]), str(SOURCE_FILES["13_placeholder"])])
            if "13_placeholder" in SOURCE_FILES
            else str(SOURCE_FILES["06_source_neutrality"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def nr_law_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "law_id": "NRL1639_0_geometrized_mass",
            "quantity": "N_R",
            "law": "N_R = 1/(2 m_*) with m_* = G M_*/c^2",
            "equivalent_law": "N_R = c^2/(2 G M_*)",
            "uses": "q_R = N_R Q_R = -N_R Pi_R",
            "status": "CONDITIONAL_DENOMINATOR_DERIVED_UNDER_CORPUS_TAIL_NORMALIZATION",
            "conditions": "R_AB tail coefficient equals Q_R; L_N=2GM_*/(r c^2); M_* is same-frame parent source mass; no orbital-GM backfill",
            "source_paths": ";".join(
                [
                    str(SOURCE_FILES["05_reciprocity"]),
                    str(SOURCE_FILES["06_source_neutrality"]),
                    str(SOURCE_FILES["02_motion_load"]),
                    str(SOURCE_FILES["1006_denominator_guard"]),
                ]
            ),
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        }
    ]


def bound_template_rows() -> list[dict[str, object]]:
    symbolic_sources = ";".join(
        [
            str(SOURCE_FILES["05_reciprocity"]),
            str(SOURCE_FILES["06_source_neutrality"]),
            str(SOURCE_FILES["02_motion_load"]),
            str(SOURCE_FILES["1638_chain"]),
        ]
    )
    return [
        {
            "branch_id": BRANCH_ID,
            "template_id": "PQT1639_0_qR_from_QR",
            "target": "q_R_abs",
            "formula": "|q_R| = |Q_R| c^2/(2 G M_*)",
            "required_inputs": "Q_R tail coefficient; same-frame M_*; G/c convention; tail normalization sign/absolute convention",
            "current_value": "MISSING_Q_R_VALUE_AND_SAME_FRAME_MASS",
            "source_paths": symbolic_sources,
            "status": "TEMPLATE_READY_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "template_id": "PQT1639_1_qR_from_PiR",
            "target": "q_R_abs",
            "formula": "|q_R| = |Pi_R| c^2/(2 G M_*)",
            "required_inputs": "Pi_R_boundary_abs; same-frame M_*; boundary-to-tail projection; no-cancellation envelope",
            "current_value": "MISSING_Pi_R_BOUND_AND_SAME_FRAME_MASS",
            "source_paths": symbolic_sources,
            "status": "TEMPLATE_READY_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "template_id": "PQT1639_2_PiR_allowed_by_gamma",
            "target": "Pi_R_boundary_abs_max",
            "formula": "|Pi_R| <= (2 G M_*/c^2) |Delta gamma|_max",
            "required_inputs": "external PPN gamma bound; same-frame M_*; boundary projection; absolute residual budget",
            "current_value": "MISSING_EXTERNAL_GAMMA_BOUND_AND_MASS_CALIBRATION",
            "source_paths": symbolic_sources,
            "status": "BOUND_TEMPLATE_READY_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "template_id": "PQT1639_3_exact_GR_condition",
            "target": "local_GR_exact_condition",
            "formula": "Pi_R=0 -> Q_R=0 -> q_R=0 -> Delta gamma=0",
            "required_inputs": "parent-signed boundary silence or no independent boundary/source slot",
            "current_value": "MISSING_PARENT_Pi_R_ZERO_THEOREM",
            "source_paths": symbolic_sources,
            "status": "EXACT_GR_ROUTE_IDENTIFIED_NOT_PROVED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
    ]


def blocker_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "blocker_id": "NRB1639_0_tail_normalization",
            "missing_or_conditional_input": "TAIL_COEFFICIENT_EQUALS_Q_R",
            "why_it_matters": "N_R=c^2/(2GM_*) only follows directly if Q_R is the 1/r coefficient of R_AB",
            "current_status": "CONDITIONAL_FROM_CORPUS_NOT_PARENT_SIGNED",
            "next_action": "derive W(r) so that W R_AB'=Q_R integrates to the stated R_AB~Q_R/r coefficient, or retain a k_W factor",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "blocker_id": "NRB1639_1_same_frame_mass",
            "missing_or_conditional_input": "SAME_FRAME_PARENT_SOURCE_MASS_M_STAR",
            "why_it_matters": "using observed orbital GM to normalize q_R would borrow the Newtonian limit to prove the Newtonian limit",
            "current_status": "MISSING_PARENT_SOURCE_MASS_CALIBRATION",
            "next_action": "derive M_* from parent source measure/Hamiltonian charge or keep M_* as a nonclaim symbol",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "blocker_id": "NRB1639_2_boundary_projection",
            "missing_or_conditional_input": "Pi_R_BOUNDARY_TO_Q_R_PROJECTION",
            "why_it_matters": "Q_R=-Pi_R is symbolic unless the worldtube boundary convention fixes sign, units, and orientation",
            "current_status": "MISSING_WORLDTUBE_PROJECTION",
            "next_action": "derive the boundary variation convention or source an absolute Pi_R bound row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "blocker_id": "NRB1639_3_external_gamma_bound",
            "missing_or_conditional_input": "CURRENT_EXTERNAL_PPN_GAMMA_BOUND",
            "why_it_matters": "the internal |q_R| target is not a public evidence row",
            "current_status": "MISSING_BOUND_SOURCE",
            "next_action": "source a current PPN gamma bound only after the parent normalization row exists",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "blocker_id": "NRB1639_4_no_cancellation_budget",
            "missing_or_conditional_input": "ABSOLUTE_LOCAL_RESIDUAL_VECTOR",
            "why_it_matters": "Delta gamma cannot pass by cancellation between Pi_R and unrelated residuals",
            "current_status": "MISSING_ABSOLUTE_PRODUCT_GUARD",
            "next_action": "fold Pi_R into the no-cancellation local residual vector before scoring",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1639_0_denominator",
            "decision": "N_R_CONDITIONAL_DERIVED",
            "reason": "matching R_AB~Q_R/r to R_AB=q_R 2GM_*/(r c^2) gives q_R=Q_R c^2/(2GM_*)",
            "next_action": "carry the law forward with same-frame mass and tail-normalization guardrails",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1639_1_not_claim",
            "decision": "DENOMINATOR_NOT_CLAIM_READY",
            "reason": "Q_R coefficient normalization and M_* source mass are not parent-signed",
            "next_action": "do not score PPN/orbital/local-GR from this law yet",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1639_2_exact_route",
            "decision": "EXACT_GR_ROUTE_REDUCES_TO_Pi_R_ZERO",
            "reason": "the derived law shows exact GR is recovered if Pi_R=0, independent of numeric denominator size",
            "next_action": "try the parent boundary-silence theorem before empirical bound filling",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1639_0_N_R",
            "claim": "N_R is a claim-ready denominator",
            "status": "BLOCKED",
            "blocker": "tail coefficient and same-frame source mass are conditional",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1639_1_local_GR",
            "claim": "local GR recovered from Pi_R branch",
            "status": "BLOCKED",
            "blocker": "Pi_R=0 is not parent-signed and finite Pi_R is not source-bounded",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1639_2_PPN",
            "claim": "PPN gamma pass",
            "status": "BLOCKED",
            "blocker": "external gamma bound/source mass/boundary projection/no-cancellation budget are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1639_3_R10",
            "claim": "massless Q_R/r tail can be scored as R10 alpha(lambda)",
            "status": "BLOCKED",
            "blocker": "massless reciprocal hair remains a PPN/local/orbital channel, not finite-range R10",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1640-Y5-R2FR-PiR-zero-boundary-silence-or-normalized-PPN-bound-runner.md",
            "script": "scripts/Y5_R2FR_PiR_zero_boundary_silence_or_normalized_PPN_bound_runner.py",
            "objective": "attempt the parent boundary-silence theorem Pi_R=0 using the new q_R=-Pi_R c^2/(2GM_*) amplitude law; if it fails, stage a normalized nonclaim PPN bound runner with explicit M_*, tail normalization, and no-cancellation inputs",
            "success_condition": "either Pi_R=0 is parent-signed, or a normalized Pi_R/q_R/Delta_gamma bound template exists with every missing input explicit and unscored",
            "guardrails": "do not use orbital GM as parent mass, do not claim PPN/local GR, do not score missing placeholders, do not route massless Q_R/r through R10",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        }
    ]


def all_claim_flags_false(paths: list[Path]) -> bool:
    for path in paths:
        for row in csv_rows(path):
            for column_name in ["valid_for_claim", "claim_allowed", "score_allowed"]:
                if column_name in row and bool_string(row[column_name]) == "true":
                    return False
    return True


def copy_outputs() -> None:
    paths = GENERATED + ([VALIDATION] if VALIDATION.exists() else [])
    for path in paths:
        for target_dir in [QUARANTINE, BRANCH_RESIDUALS]:
            shutil.copy2(path, target_dir / path.name)
    shutil.copy2(NR_LAW, QUEUE / "JR1639_NR_LAW_CONDITIONAL_NONCLAIM.csv")
    shutil.copy2(BOUND_TEMPLATE, QUEUE / "JR1639_PIR_QR_QRLOCAL_BOUND_TEMPLATE_NONCLAIM.csv")
    shutil.copy2(NEXT_TARGET, QUEUE / "JR1639_NEXT_TARGET_NONCLAIM.csv")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows() -> list[dict[str, object]]:
    source_rows = csv_rows(SOURCE_REGISTER)
    derivation = csv_rows(DERIVATION)
    nr_law = csv_rows(NR_LAW)
    templates = csv_rows(BOUND_TEMPLATE)
    blockers = csv_rows(BLOCKERS)
    decisions = csv_rows(DECISION)
    gates = csv_rows(CLAIM_GATE)
    next_targets = csv_rows(NEXT_TARGET)

    checks = [
        (
            "VAL1639_0_sources_exist",
            all(bool_string(row["path_exists"]) == "true" for row in source_rows),
            "all 1639 cited source paths exist",
        ),
        (
            "VAL1639_1_needles_found",
            all(bool_string(row["needles_found"]) == "true" for row in source_rows),
            "all 1639 source needles found",
        ),
        (
            "VAL1639_2_derivation_sources_exist",
            all(source_paths_exist(row["source_paths"]) for row in derivation),
            "all denominator derivation source paths exist",
        ),
        (
            "VAL1639_3_denominator_law_present",
            any(row["output_relation"] == "q_R = Q_R c^2/(2 G M_*)" for row in derivation)
            and nr_law[0]["equivalent_law"] == "N_R = c^2/(2 G M_*)",
            "conditional N_R denominator law is recorded",
        ),
        (
            "VAL1639_4_PiR_amplitude_law_present",
            any(row["output_relation"] == "q_R = -Pi_R c^2/(2 G M_*)" for row in derivation),
            "Pi_R to q_R amplitude law is recorded",
        ),
        (
            "VAL1639_5_law_conditional_nonclaim",
            nr_law[0]["status"] == "CONDITIONAL_DENOMINATOR_DERIVED_UNDER_CORPUS_TAIL_NORMALIZATION"
            and bool_string(nr_law[0]["valid_for_claim"]) == "false"
            and "no orbital-GM backfill" in nr_law[0]["conditions"],
            "N_R law is conditional and nonclaim with anti-circularity condition",
        ),
        (
            "VAL1639_6_bound_templates_nonclaim",
            all(
                bool_string(row["valid_for_claim"]) == "false"
                and bool_string(row["score_allowed"]) == "false"
                and row["current_value"].startswith("MISSING_")
                for row in templates
                if row["template_id"] != "PQT1639_3_exact_GR_condition"
            ),
            "finite Pi_R/q_R bound templates remain missing-value nonclaim rows",
        ),
        (
            "VAL1639_7_exact_GR_condition_staged",
            any(row["formula"] == "Pi_R=0 -> Q_R=0 -> q_R=0 -> Delta gamma=0" for row in templates),
            "exact local-GR condition is staged as Pi_R zero route",
        ),
        (
            "VAL1639_8_required_blockers_listed",
            all(
                required in {row["missing_or_conditional_input"] for row in blockers}
                for required in [
                    "TAIL_COEFFICIENT_EQUALS_Q_R",
                    "SAME_FRAME_PARENT_SOURCE_MASS_M_STAR",
                    "Pi_R_BOUNDARY_TO_Q_R_PROJECTION",
                    "CURRENT_EXTERNAL_PPN_GAMMA_BOUND",
                    "ABSOLUTE_LOCAL_RESIDUAL_VECTOR",
                ]
            ),
            "all source-mass/tail/bound blockers are explicit",
        ),
        (
            "VAL1639_9_decisions_recorded",
            all(
                required in {row["decision"] for row in decisions}
                for required in [
                    "N_R_CONDITIONAL_DERIVED",
                    "DENOMINATOR_NOT_CLAIM_READY",
                    "EXACT_GR_ROUTE_REDUCES_TO_Pi_R_ZERO",
                ]
            ),
            "required 1639 decisions are recorded",
        ),
        (
            "VAL1639_10_claim_gates_closed",
            all(row["status"] == "BLOCKED" for row in gates),
            "all 1639 claim gates remain blocked",
        ),
        (
            "VAL1639_11_next_target_selected",
            next_targets[0]["next_target"] == "1640-Y5-R2FR-PiR-zero-boundary-silence-or-normalized-PPN-bound-runner.md",
            "next target selects Pi_R zero theorem or normalized PPN bound runner",
        ),
        (
            "VAL1639_12_csv_parse",
            all(len(csv_rows(path)) > 0 for path in GENERATED),
            "all generated 1639 CSVs parse",
        ),
        (
            "VAL1639_13_nonclaim_flags",
            all_claim_flags_false(CLAIM_CHECKED),
            "all 1639 generated rows remain nonclaim/no-score",
        ),
        (
            "VAL1639_14_branch_copies",
            all((QUARANTINE / path.name).exists() and (BRANCH_RESIDUALS / path.name).exists() for path in GENERATED),
            "branch/quarantine copies exist",
        ),
        (
            "VAL1639_15_queue_copies",
            all(
                path.exists()
                for path in [
                    QUEUE / "JR1639_NR_LAW_CONDITIONAL_NONCLAIM.csv",
                    QUEUE / "JR1639_PIR_QR_QRLOCAL_BOUND_TEMPLATE_NONCLAIM.csv",
                    QUEUE / "JR1639_NEXT_TARGET_NONCLAIM.csv",
                ]
            ),
            "acquisition queue nonclaim copies exist",
        ),
        (
            "VAL1639_16_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
        ),
        (
            "VAL1639_17_formalization_untouched",
            not any(FORMALIZATION.rglob("*1639*")) if FORMALIZATION.exists() else True,
            "no 1639 outputs found under formalization-workbench",
        ),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1639_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1639 q_R normalization denominator validation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        cells = [str(row.get(column, "")).replace("\n", " ") for column in columns]
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body])


def write_doc() -> None:
    source_rows = csv_rows(SOURCE_REGISTER)
    derivation = csv_rows(DERIVATION)
    nr_law = csv_rows(NR_LAW)
    templates = csv_rows(BOUND_TEMPLATE)
    blockers = csv_rows(BLOCKERS)
    decisions = csv_rows(DECISION)
    gates = csv_rows(CLAIM_GATE)
    next_targets = csv_rows(NEXT_TARGET)
    validation = csv_rows(VALIDATION)

    content = f"""# 1639 - q_R Normalization Denominator Or Pi_R Source Acquisition

**Private status:** nonclaim checkpoint. No local-GR, PPN, Newton, orbital, WEP, clock, EM, or R10 pass is claimed.

## Verdict

The denominator is no longer just a foggy missing symbol. Under the existing corpus normalization

```text
R_AB(r) ~ Q_R/r
R_AB = q_R L_N
L_N = 2GM_*/(r c^2)
```

coefficient matching gives:

```text
q_R = Q_R c^2/(2GM_*) = -Pi_R c^2/(2GM_*)
N_R = c^2/(2GM_*) = 1/(2m_*)
```

This is useful, but it is **conditional**, not claim-ready. The remaining guardrails are serious: `Q_R` must really be the `1/r` tail coefficient, `M_*` must be the same-frame parent source mass, and orbital `GM` cannot be used to backfill the denominator before the Newton/GR bridge is derived.

## Source Register

{markdown_table(source_rows, ["source_id", "path", "path_exists", "needles_found", "role"])}

## Denominator Derivation

{markdown_table(derivation, ["step_id", "input_relation", "operation", "output_relation", "status"])}

## Conditional N_R Law

{markdown_table(nr_law, ["law_id", "quantity", "law", "equivalent_law", "uses", "status", "conditions"])}

## Bound Templates

{markdown_table(templates, ["template_id", "target", "formula", "required_inputs", "current_value", "status"])}

## Remaining Blockers

{markdown_table(blockers, ["blocker_id", "missing_or_conditional_input", "why_it_matters", "current_status", "next_action"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "claim", "status", "blocker"])}

## Next Target

{markdown_table(next_targets, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    outputs = {
        SOURCE_REGISTER: source_register_rows(),
        DERIVATION: derivation_rows(),
        NR_LAW: nr_law_rows(),
        BOUND_TEMPLATE: bound_template_rows(),
        BLOCKERS: blocker_rows(),
        DECISION: decision_rows(),
        CLAIM_GATE: claim_gate_rows(),
        NEXT_TARGET: next_target_rows(),
    }
    for path, rows in outputs.items():
        write_csv(path, rows)

    copy_outputs()
    remove_pycache()
    write_csv(VALIDATION, validation_rows())
    copy_outputs()
    write_doc()
    remove_pycache()
    print(f"wrote {rel(DOC)}")
    print(f"validation {rel(VALIDATION)}")


if __name__ == "__main__":
    main()
