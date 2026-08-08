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
QUARANTINE = MICROSCOPE / "quarantine" / "1638"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1638-Y5-R2FR-PiR-bound-source-acquisition-and-qR-normalization.md"

SOURCE_FILES = {
    "1637_doc": ROOT / "1637-Y5-R2FR-no-independent-RAB-slot-grammar-or-first-PiR-bound-row.md",
    "1637_validation": OUT / "P8_Y5_BRR545_1637_VALIDATION.csv",
    "1637_next": OUT / "P8_Y5_PARENT_QLOC_1637_NEXT_TARGET.csv",
    "1637_first_bound": OUT / "P8_Y5_PARENT_QLOC_1637_FIRST_PIR_BOUND_ROW_SCHEMA.csv",
    "06_source_neutrality": ROOT / "06-reciprocal-charge-source-neutrality.md",
    "05_reciprocity": ROOT / "05-reciprocity-theorem-attempt.md",
    "13_ppn_benchmark": ROOT / "13-local-closure-PPN-benchmark.md",
    "1629_prior_widths": OUT / "P8_Y5_PARENT_QLOC_1629_FINITE_JR_PIR_PRIOR_WIDTH_ROWS.csv",
    "1635_residual": OUT / "P8_Y5_PARENT_QLOC_1635_PIR_RESIDUAL_ENVELOPE.csv",
    "1636_bound_pack": OUT / "P8_Y5_PARENT_QLOC_1636_PIR_BOUND_INPUT_PACK.csv",
}

NEEDLES = {
    "1637_doc": [
        "NEXT_1638_PIR_BOUND_SOURCE_ACQUISITION_AND_QR_NORMALIZATION",
        "Pi_R_boundary_abs",
    ],
    "1637_validation": ["VAL1637_OVERALL", "PASS"],
    "1637_next": [
        "1638-Y5-R2FR-PiR-bound-source-acquisition-and-qR-normalization.md",
        "do not set tau/projection to one",
    ],
    "1637_first_bound": [
        "PIRB1637_0_boundary_first_row",
        "MISSING_WORLDTUBE_BOUNDARY_TO_QR_QR_TO_QRLOCAL_PROJECTION",
    ],
    "06_source_neutrality": ["Q_R = -Pi_R", "gamma - 1 ~= q_R", "|q_R| <= 1e-5"],
    "05_reciprocity": ["W R_AB' = Q_R", "R_AB ~ Q_R/r", "Asymptotic flatness alone"],
    "13_ppn_benchmark": ["R_AB approx q_R L", "gamma approx 1 + q_R", "closure assumptions"],
    "1629_prior_widths": ["PW1629_2_PiR", "MISSING_PIR_PRIOR_WIDTH"],
    "1635_residual": ["PIRRES1635_4_boundary", "MISSING_BOUNDARY_ZERO_OR_ABSOLUTE_TAIL"],
    "1636_bound_pack": ["PIRBP1636_4_boundary", "MISSING_BOUNDARY_ZERO_OR_ABSOLUTE_TAIL"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1638_SOURCE_REGISTER.csv"
CHAIN = OUT / "P8_Y5_PARENT_QLOC_1638_PIR_TO_QR_QRLOCAL_CHAIN.csv"
BOUND_INTAKE = OUT / "P8_Y5_PARENT_QLOC_1638_PIR_BOUND_SOURCE_INTAKE.csv"
BLOCKERS = OUT / "P8_Y5_PARENT_QLOC_1638_QR_NORMALIZATION_BLOCKER_LEDGER.csv"
PPN_TEMPLATE = OUT / "P8_Y5_PARENT_QLOC_1638_LOCAL_PPN_PROJECTION_TEMPLATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1638_DECISION.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1638_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1638_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1638_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    CHAIN,
    BOUND_INTAKE,
    BLOCKERS,
    PPN_TEMPLATE,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    CHAIN,
    BOUND_INTAKE,
    BLOCKERS,
    PPN_TEMPLATE,
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


def local_paths_from_semicolon(value: str) -> list[Path]:
    if value.startswith("MISSING_") or value == "":
        return []
    return [Path(part.strip()) for part in value.split(";") if part.strip() and not part.strip().startswith("MISSING_")]


def source_paths_exist(value: str) -> bool:
    paths = local_paths_from_semicolon(value)
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
                "role": "1638 Pi_R boundary source acquisition and q_R normalization",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def chain_rows() -> list[dict[str, object]]:
    symbolic_sources = ";".join(
        [
            str(SOURCE_FILES["06_source_neutrality"]),
            str(SOURCE_FILES["05_reciprocity"]),
            str(SOURCE_FILES["13_ppn_benchmark"]),
        ]
    )
    return [
        {
            "branch_id": BRANCH_ID,
            "chain_id": "PIRQR1638_0_boundary_variation",
            "relation": "delta S_boundary = [W R_AB' + Pi_R] delta R_AB at the surface",
            "status": "CORPUS_SYMBOLIC_RELATION_FOUND",
            "source_paths": str(SOURCE_FILES["06_source_neutrality"]),
            "source_anchor": "boundary variation term",
            "missing_input": "PARENT_SIGNED_BOUNDARY_SILENCE_OR_ABSOLUTE_PIR_BOUND",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "chain_id": "PIRQR1638_1_boundary_charge",
            "relation": "Q_R = -Pi_R",
            "status": "PIR_TO_QR_CHAIN_SYMBOLIC_ONLY",
            "source_paths": symbolic_sources,
            "source_anchor": "06 source neutrality plus 05 exterior charge notation",
            "missing_input": "UNITS_AND_SIGN_CONVENTION_FOR_ABSOLUTE_BOUNDARY_MOMENTUM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "chain_id": "PIRQR1638_2_exterior_tail",
            "relation": "R_AB ~ Q_R/r outside the source when the reciprocal charge is not killed",
            "status": "MASSLESS_TAIL_NOT_R10_FINITE_RANGE",
            "source_paths": str(SOURCE_FILES["05_reciprocity"]),
            "source_anchor": "asymptotic flatness alone does not kill Q_R",
            "missing_input": "SOURCE_OR_BOUNDARY_CONDITION_THAT_SETS_Q_R_TO_ZERO_OR_BOUNDS_IT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "chain_id": "PIRQR1638_3_local_parameter",
            "relation": "R_AB = q_R L_N",
            "status": "LOCAL_PARAMETERIZATION_FOUND",
            "source_paths": str(SOURCE_FILES["06_source_neutrality"]),
            "source_anchor": "local reciprocal residual parameterization",
            "missing_input": "DENOMINATOR_N_R_MAPPING_Q_R_TO_DIMENSIONLESS_q_R",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "chain_id": "PIRQR1638_4_ppn_projection",
            "relation": "Delta gamma ~= q_R",
            "status": "LOCAL_PPN_SYMBOLIC_MAP_FOUND",
            "source_paths": ";".join([str(SOURCE_FILES["06_source_neutrality"]), str(SOURCE_FILES["13_ppn_benchmark"])]),
            "source_anchor": "gamma residual proportional to q_R",
            "missing_input": "NORMALIZED_q_R_BOUND_AND_EXTERNAL_PPN_SOURCE_FOR_PUBLIC_CLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "chain_id": "PIRQR1638_5_normalization_bridge",
            "relation": "q_R = N_R Q_R = -N_R Pi_R",
            "status": "Q_R_TO_q_R_NORMALIZATION_MISSING",
            "source_paths": symbolic_sources,
            "source_anchor": "required bridge inferred from Q_R=-Pi_R and R_AB=q_R L_N",
            "missing_input": "N_R_FROM_W_RAB_EQUATION_LOCAL_SOURCE_MASS_CONVENTION_AND_WORLDTUBE_RADIUS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def bound_intake_rows() -> list[dict[str, object]]:
    symbolic_sources = ";".join(
        [
            str(SOURCE_FILES["1637_first_bound"]),
            str(SOURCE_FILES["06_source_neutrality"]),
            str(SOURCE_FILES["05_reciprocity"]),
            str(SOURCE_FILES["1635_residual"]),
            str(SOURCE_FILES["1636_bound_pack"]),
        ]
    )
    return [
        {
            "branch_id": BRANCH_ID,
            "intake_id": "PIRBI1638_0_boundary_abs",
            "coefficient_id": "Pi_R_boundary_abs",
            "arena": "local_GR;PPN;orbital",
            "projection_chain": "Pi_R -> Q_R -> q_R -> Delta gamma",
            "bound_or_value": "MISSING_BOUND_VALUE",
            "bound_units": "boundary reciprocal momentum units after W R_AB' normalization",
            "symbolic_source_paths": symbolic_sources,
            "bound_source_path": "MISSING_PARENT_OR_EMPIRICAL_BOUND_SOURCE_PATH",
            "extraction_method": "not extracted; symbolic chain only",
            "confidence_level": "blocker",
            "source_backed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "intake_id": "PIRBI1638_1_qR_abs_template",
            "coefficient_id": "q_R_abs",
            "arena": "PPN;local_GR;orbital",
            "projection_chain": "q_R = N_R Q_R = -N_R Pi_R",
            "bound_or_value": "MISSING_QR_TO_qR_NORMALIZED_VALUE",
            "bound_units": "dimensionless",
            "symbolic_source_paths": ";".join([str(SOURCE_FILES["06_source_neutrality"]), str(SOURCE_FILES["13_ppn_benchmark"])]),
            "bound_source_path": "MISSING_NORMALIZATION_DENOMINATOR_AND_EXTERNAL_PPN_SOURCE",
            "extraction_method": "template only; do not set N_R=1",
            "confidence_level": "blocker",
            "source_backed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "intake_id": "PIRBI1638_2_delta_gamma_template",
            "coefficient_id": "Delta_gamma_abs",
            "arena": "PPN",
            "projection_chain": "|Delta gamma| ~= |q_R|",
            "bound_or_value": "INTERNAL_ROUGH_TARGET_ONLY_|q_R|<=1e-5_NOT_PUBLIC_SOURCE",
            "bound_units": "dimensionless",
            "symbolic_source_paths": ";".join([str(SOURCE_FILES["06_source_neutrality"]), str(SOURCE_FILES["13_ppn_benchmark"])]),
            "bound_source_path": "MISSING_CURRENT_EXTERNAL_PPN_BOUND_SOURCE_FOR_PUBLIC_CLAIM",
            "extraction_method": "internal benchmark only",
            "confidence_level": "nonclaim internal target",
            "source_backed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
    ]


def blocker_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "blocker_id": "QRN1638_0_worldtube_projection",
            "missing_input": "WORLDTUBE_BOUNDARY_TO_QR_PROJECTION",
            "why_it_matters": "Pi_R is a boundary object; a local source projection is needed before it can be compared with PPN/orbital data",
            "required_form": "explicit boundary surface, orientation, sign convention, and projection functional",
            "current_status": "MISSING_PARENT_INPUT",
            "next_action": "derive boundary silence/absolute-tail coefficient from parent matter boundary term",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "blocker_id": "QRN1638_1_W_normalization",
            "missing_input": "W_RAB_EQUATION_NORMALIZATION",
            "why_it_matters": "Q_R = W R_AB' fixes the units of Q_R and therefore the units of Pi_R",
            "required_form": "declared W(r) or normalized radial equation in the local weak-field branch",
            "current_status": "MISSING_PARENT_INPUT",
            "next_action": "derive W(r) from the parent kinetic term or mark it as a closure coefficient",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "blocker_id": "QRN1638_2_qR_denominator",
            "missing_input": "N_R_DENOMINATOR_FOR_QR_TO_qR",
            "why_it_matters": "without N_R, q_R cannot be computed from Q_R and Delta gamma cannot be scored",
            "required_form": "q_R = N_R Q_R with N_R built from L_N, source mass convention, radius/domain, and W normalization",
            "current_status": "MISSING_ARENA_PROJECTION",
            "next_action": "derive q_R denominator or acquire empirical q_R/Pi_R bound row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "blocker_id": "QRN1638_3_source_convention",
            "missing_input": "LOCAL_SOURCE_MASS_AND_L_N_CONVENTION",
            "why_it_matters": "R_AB=q_R L_N is dimensionless only after the Newtonian load convention is fixed",
            "required_form": "definition of L_N and whether it is GM/(rc^2), potential, or another normalized load",
            "current_status": "MISSING_ARENA_PROJECTION",
            "next_action": "tie L_N to the local GR/Newton weak-field expansion used by the observer map",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "blocker_id": "QRN1638_4_external_bound_source",
            "missing_input": "CURRENT_EXTERNAL_PPN_OR_ORBITAL_BOUND_SOURCE",
            "why_it_matters": "the internal |q_R| <= 1e-5 line is useful as a discipline target but is not a sourced public evidence row",
            "required_form": "source-backed bound, DOI/URL/local path, extraction method, units, and valid_for_claim eligibility",
            "current_status": "MISSING_BOUND_SOURCE",
            "next_action": "source PPN/orbital bound after N_R exists; do not score before normalization",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "blocker_id": "QRN1638_5_no_cancellation_envelope",
            "missing_input": "NO_CANCELLATION_OR_ABSOLUTE_ENVELOPE",
            "why_it_matters": "a small net Delta gamma cannot be claimed if unrelated residuals cancel the Pi_R tail",
            "required_form": "absolute-value budget or theorem that all other local residuals vanish independently",
            "current_status": "MISSING_PARENT_INPUT",
            "next_action": "combine with residual-vector ledger before any local-GR pass",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def ppn_template_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "template_id": "PPNT1638_0_direct_chain",
            "observable": "PPN_gamma_residual",
            "formula": "Delta_gamma ~= q_R = N_R Q_R = -N_R Pi_R",
            "required_inputs": "Pi_R_boundary_abs; W_RAB_equation_normalization; N_R_denominator; local L_N convention; external gamma bound",
            "available_inputs": "symbolic Q_R=-Pi_R; symbolic R_AB=q_R L_N; symbolic Delta gamma ~= q_R",
            "blocked_by": "Q_R_TO_q_R_NORMALIZATION_MISSING",
            "do_not_do": "do not set N_R=1; do not use R10 alpha(lambda); do not claim local GR",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "template_id": "PPNT1638_1_if_zero_theorem_closes",
            "observable": "PPN_gamma_residual",
            "formula": "Pi_R=0 -> Q_R=0 -> q_R=0 -> Delta_gamma=0",
            "required_inputs": "parent-signed boundary silence plus bulk no-source theorem plus projection silence",
            "available_inputs": "conditional theorem shape only",
            "blocked_by": "PARENT_SIGNED_BOUNDARY_SILENCE_MISSING",
            "do_not_do": "do not treat closure assumption as theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1638_0_chain",
            "decision": "PIR_TO_QR_CHAIN_SYMBOLIC_ONLY",
            "reason": "the corpus contains Q_R=-Pi_R and the exterior Q_R/r tail, but not the parent-signed bound/projection",
            "next_action": "preserve the symbolic chain and derive the missing normalization bridge",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1638_1_bound_source",
            "decision": "PIR_BOUND_SOURCE_NOT_FOUND_CURRENT_CORPUS",
            "reason": "the current files name Pi_R_boundary_abs but only as a missing fallback row",
            "next_action": "derive boundary silence/absolute tail from parent matter action or source a bound row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1638_2_normalization",
            "decision": "Q_R_TO_q_R_NORMALIZATION_MISSING",
            "reason": "N_R requires W(r), L_N, source mass/radius/domain, and sign/absolute conventions",
            "next_action": "make 1639 a denominator derivation gate before any PPN scoring",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1638_3_template",
            "decision": "LOCAL_PPN_TEMPLATE_STAGED_NONCLAIM",
            "reason": "Delta gamma ~= q_R can be used as a template after N_R exists, but not as evidence now",
            "next_action": "keep template nonclaim and blocked until normalization/source rows exist",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1638_0_local_GR",
            "claim": "local GR recovery from Pi_R/Q_R branch",
            "status": "BLOCKED",
            "blocker": "Pi_R=0 or normalized small q_R has not been derived/source-bounded",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1638_1_PPN_score",
            "claim": "score Delta gamma against PPN bound",
            "status": "BLOCKED",
            "blocker": "N_R denominator and external bound source are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1638_2_R10_alpha",
            "claim": "use massless Q_R/r as finite-range R10 alpha(lambda)",
            "status": "BLOCKED",
            "blocker": "massless reciprocal tail is PPN/local/orbital, not finite-range R10 alpha(lambda)",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1638_3_orbital",
            "claim": "orbital residual pass from Pi_R boundary bound",
            "status": "BLOCKED",
            "blocker": "worldtube projection and no-cancellation envelope are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1639-Y5-R2FR-qR-normalization-denominator-or-PiR-source-acquisition.md",
            "script": "scripts/Y5_R2FR_qR_normalization_denominator_or_PiR_source_acquisition.py",
            "objective": "derive the denominator N_R mapping Pi_R/Q_R to q_R using W(r), L_N, source mass/radius/domain, and sign conventions; if impossible, source a nonclaim empirical Pi_R/q_R bound row",
            "success_condition": "either q_R=N_R Q_R is derived with units/projection metadata, or the blocker ledger proves which W, L_N, worldtube, or bound source is missing",
            "guardrails": "do not set N_R=1, do not score Delta gamma, do not claim local GR, do not route massless Q_R/r through R10 alpha(lambda)",
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
    shutil.copy2(BOUND_INTAKE, QUEUE / "JR1638_PIR_BOUND_SOURCE_INTAKE_NONCLAIM.csv")
    shutil.copy2(BLOCKERS, QUEUE / "JR1638_QR_NORMALIZATION_BLOCKER_LEDGER_NONCLAIM.csv")
    shutil.copy2(NEXT_TARGET, QUEUE / "JR1638_NEXT_TARGET_NONCLAIM.csv")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows() -> list[dict[str, object]]:
    source_rows = csv_rows(SOURCE_REGISTER)
    chain = csv_rows(CHAIN)
    bound_intake = csv_rows(BOUND_INTAKE)
    blockers = csv_rows(BLOCKERS)
    ppn_template = csv_rows(PPN_TEMPLATE)
    decisions = csv_rows(DECISION)
    gates = csv_rows(CLAIM_GATE)
    next_targets = csv_rows(NEXT_TARGET)

    checks = [
        (
            "VAL1638_0_sources_exist",
            all(bool_string(row["path_exists"]) == "true" for row in source_rows),
            "all 1638 cited source paths exist",
        ),
        (
            "VAL1638_1_needles_found",
            all(bool_string(row["needles_found"]) == "true" for row in source_rows),
            "all 1638 source needles found",
        ),
        (
            "VAL1638_2_symbolic_sources_exist",
            all(source_paths_exist(row["source_paths"]) for row in chain),
            "all chain symbolic source paths exist",
        ),
        (
            "VAL1638_3_chain_has_required_relations",
            any(row["relation"] == "Q_R = -Pi_R" for row in chain)
            and any(row["status"] == "Q_R_TO_q_R_NORMALIZATION_MISSING" for row in chain)
            and any(row["relation"] == "Delta gamma ~= q_R" for row in chain),
            "Pi_R to Q_R to q_R to Delta gamma chain is staged",
        ),
        (
            "VAL1638_4_bound_intake_nonclaim",
            all(
                bool_string(row["source_backed"]) == "false"
                and bool_string(row["valid_for_claim"]) == "false"
                and row["bound_source_path"].startswith("MISSING_")
                for row in bound_intake
            ),
            "Pi_R/q_R bound intake rows remain missing-source nonclaim rows",
        ),
        (
            "VAL1638_5_bound_symbolic_paths_exist",
            all(source_paths_exist(row["symbolic_source_paths"]) for row in bound_intake),
            "symbolic source paths in bound intake exist",
        ),
        (
            "VAL1638_6_required_blockers_listed",
            all(
                required in {row["missing_input"] for row in blockers}
                for required in [
                    "WORLDTUBE_BOUNDARY_TO_QR_PROJECTION",
                    "W_RAB_EQUATION_NORMALIZATION",
                    "N_R_DENOMINATOR_FOR_QR_TO_qR",
                    "LOCAL_SOURCE_MASS_AND_L_N_CONVENTION",
                    "CURRENT_EXTERNAL_PPN_OR_ORBITAL_BOUND_SOURCE",
                    "NO_CANCELLATION_OR_ABSOLUTE_ENVELOPE",
                ]
            ),
            "all normalization/source blockers are explicit",
        ),
        (
            "VAL1638_7_ppn_template_blocked",
            all(row["blocked_by"] != "" and bool_string(row["valid_for_claim"]) == "false" for row in ppn_template),
            "PPN projection template is staged but blocked",
        ),
        (
            "VAL1638_8_decisions_recorded",
            all(
                required in {row["decision"] for row in decisions}
                for required in [
                    "PIR_TO_QR_CHAIN_SYMBOLIC_ONLY",
                    "PIR_BOUND_SOURCE_NOT_FOUND_CURRENT_CORPUS",
                    "Q_R_TO_q_R_NORMALIZATION_MISSING",
                    "LOCAL_PPN_TEMPLATE_STAGED_NONCLAIM",
                ]
            ),
            "required 1638 decisions are recorded",
        ),
        (
            "VAL1638_9_claim_gates_closed",
            all(row["status"] == "BLOCKED" for row in gates),
            "all 1638 claim gates remain blocked",
        ),
        (
            "VAL1638_10_next_target_selected",
            next_targets[0]["next_target"] == "1639-Y5-R2FR-qR-normalization-denominator-or-PiR-source-acquisition.md",
            "next target selects q_R normalization denominator or Pi_R source acquisition",
        ),
        (
            "VAL1638_11_csv_parse",
            all(len(csv_rows(path)) > 0 for path in GENERATED),
            "all generated 1638 CSVs parse",
        ),
        (
            "VAL1638_12_nonclaim_flags",
            all_claim_flags_false(CLAIM_CHECKED),
            "all 1638 generated rows remain nonclaim/no-score",
        ),
        (
            "VAL1638_13_branch_copies",
            all((QUARANTINE / path.name).exists() and (BRANCH_RESIDUALS / path.name).exists() for path in GENERATED),
            "branch/quarantine copies exist",
        ),
        (
            "VAL1638_14_queue_copies",
            all(
                path.exists()
                for path in [
                    QUEUE / "JR1638_PIR_BOUND_SOURCE_INTAKE_NONCLAIM.csv",
                    QUEUE / "JR1638_QR_NORMALIZATION_BLOCKER_LEDGER_NONCLAIM.csv",
                    QUEUE / "JR1638_NEXT_TARGET_NONCLAIM.csv",
                ]
            ),
            "acquisition queue nonclaim copies exist",
        ),
        (
            "VAL1638_15_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
        ),
        (
            "VAL1638_16_formalization_untouched",
            not any(FORMALIZATION.rglob("*1638*")) if FORMALIZATION.exists() else True,
            "no 1638 outputs found under formalization-workbench",
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
            "check_id": "VAL1638_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1638 Pi_R bound source acquisition and q_R normalization validation",
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
    chain = csv_rows(CHAIN)
    bound_intake = csv_rows(BOUND_INTAKE)
    blockers = csv_rows(BLOCKERS)
    ppn_template = csv_rows(PPN_TEMPLATE)
    decisions = csv_rows(DECISION)
    gates = csv_rows(CLAIM_GATE)
    next_targets = csv_rows(NEXT_TARGET)
    validation = csv_rows(VALIDATION)

    content = f"""# 1638 - Pi_R Bound Source Acquisition And q_R Normalization

**Private status:** nonclaim checkpoint. No `Pi_R` bound, `Q_R=0`, `q_R` bound, local-GR, PPN, orbital, WEP, clock, EM, or R10 pass is claimed.

## Verdict

The useful derivation chain is real but still symbolic:

```text
Pi_R -> Q_R -> R_AB exterior tail -> q_R local parameter -> Delta gamma
Q_R = -Pi_R
R_AB ~ Q_R/r
R_AB = q_R L_N
Delta gamma ~= q_R
```

That is progress because it tells us exactly where the coupling/normalization problem lives. The current corpus does **not** yet contain the denominator `N_R` needed for `q_R = N_R Q_R = -N_R Pi_R`, and it does not contain a source-backed absolute `Pi_R_boundary_abs` bound. So this checkpoint stages the bridge and blocks the claim rather than smuggling in `N_R=1`.

## Source Register

{markdown_table(source_rows, ["source_id", "path", "path_exists", "needles_found", "role"])}

## Pi_R To q_R Chain

{markdown_table(chain, ["chain_id", "relation", "status", "source_anchor", "missing_input"])}

## Bound Source Intake

{markdown_table(bound_intake, ["intake_id", "coefficient_id", "arena", "projection_chain", "bound_or_value", "bound_source_path", "source_backed"])}

## Normalization Blockers

{markdown_table(blockers, ["blocker_id", "missing_input", "why_it_matters", "required_form", "current_status"])}

## Local PPN Projection Template

{markdown_table(ppn_template, ["template_id", "observable", "formula", "required_inputs", "blocked_by", "do_not_do"])}

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
        CHAIN: chain_rows(),
        BOUND_INTAKE: bound_intake_rows(),
        BLOCKERS: blocker_rows(),
        PPN_TEMPLATE: ppn_template_rows(),
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
