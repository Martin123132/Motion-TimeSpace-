from __future__ import annotations

import csv
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
RAB_DOCS = ROOT / "source-intake" / "rab-sector" / "docs"
R10_EXTERNAL = ROOT / "source-intake" / "rab-sector" / "external" / "r10"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "2242-Y5-R2FR-RAB-first-internal-ZR-or-tauR10-projection-row.md"
BRANCH_ID = "MTS_R2FR_PARENT_QLOC_RAB_FIRST_INTERNAL_ZR_OR_TAUR10_2242"
START_TS = datetime.now(timezone.utc).timestamp()


OLD_CROSSREF = R10_EXTERNAL / "1569" / "crossref_10.1103_PhysRevLett.126.211101.json"
CURRENT_CROSSREF = R10_EXTERNAL / "2242" / "crossref_10.1103_PhysRevLett.126.211101.json"


SOURCE_FILES = {
    "2241_doc": ROOT / "2241-Y5-R2FR-RAB-parent-contract-derivation-from-MTS-primitives-or-first-live-ZR-row.md",
    "2241_validation": OUT / "P8_Y5_BRR545_2241_VALIDATION.csv",
    "2241_external_bound": OUT / "P8_Y5_PARENT_QLOC_2241_FIRST_EXTERNAL_BOUND_SOURCE_ROW.csv",
    "2241_internal_status": OUT / "P8_Y5_PARENT_QLOC_2241_FIRST_INTERNAL_COEFFICIENT_ROW_STATUS.csv",
    "2241_decision": OUT / "P8_Y5_PARENT_QLOC_2241_DECISION_LEDGER.csv",
    "1569_doc": ROOT / "1569-Y5-RAB-first-internal-ZR-or-tauR10-projection-row.md",
    "1569_validation": OUT / "P8_Y5_BRR545_1569_VALIDATION.csv",
    "1569_source": OUT / "P8_Y5_PARENT_QLOC_1569_SOURCE_REGISTER.csv",
    "1569_zr": OUT / "P8_Y5_PARENT_QLOC_1569_ZR_THEOREM_OR_COEFFICIENT_ATTEMPT.csv",
    "1569_tau": OUT / "P8_Y5_PARENT_QLOC_1569_TAU_R10_PROJECTION_ATTEMPT.csv",
    "1569_template": RAB_DOCS / "ZR1569_TAU_R10_PROJECTION_ROW_TEMPLATE_NONCLAIM.csv",
    "1033_tau_audit": OUT / "P8_Y5_R10_1033_TAU_R10_DERIVATION_AUDIT.csv",
    "1033_profile_contract": OUT / "P8_Y5_R10_1033_R10_PROFILE_NORMALIZATION_CONTRACT.csv",
    "1033_acquisition": OUT / "P8_Y5_R10_1033_R10_ACQUISITION_TEMPLATE.csv",
    "1035_kernel": OUT / "P8_Y5_R10_1035_KERNEL_DERIVATION_AUDIT.csv",
    "1035_charge_split": OUT / "P8_Y5_R10_1035_SOURCE_TEST_CHARGE_SPLIT.csv",
    "1035_factorization": OUT / "P8_Y5_R10_1035_KX_FACTORIZATION_ROWS.csv",
    "1035_validation": OUT / "P8_Y5_BRR545_1035_VALIDATION.csv",
    "current_crossref": CURRENT_CROSSREF,
}


SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_2242_SOURCE_REGISTER.csv"
LOCAL_SOURCE_AUDIT = OUT / "P8_Y5_PARENT_QLOC_2242_LOCAL_SOURCE_AUDIT.csv"
ZR_ATTEMPT = OUT / "P8_Y5_PARENT_QLOC_2242_ZR_THEOREM_OR_COEFFICIENT_ATTEMPT.csv"
TAU_ATTEMPT = OUT / "P8_Y5_PARENT_QLOC_2242_TAU_R10_PROJECTION_ATTEMPT.csv"
SOURCE_TEST_KERNEL_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_2242_SOURCE_TEST_KERNEL_CONTRACT.csv"
EXTERNAL_R10_METADATA = OUT / "P8_Y5_PARENT_QLOC_2242_EXTERNAL_R10_BOUND_METADATA_ROW.csv"
INTERNAL_ROW_STATUS = OUT / "P8_Y5_PARENT_QLOC_2242_FIRST_INTERNAL_ROW_STATUS.csv"
INTERNAL_JOIN_READINESS = OUT / "P8_Y5_PARENT_QLOC_2242_INTERNAL_JOIN_READINESS.csv"
PROJECTION_TEMPLATE = OUT / "P8_Y5_PARENT_QLOC_2242_PROJECTION_TEMPLATE_NONCLAIM.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_2242_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_2242_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_2242_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_2242_NEXT_TARGET.csv"
BRANCH_COPIES = OUT / "P8_Y5_PARENT_QLOC_2242_BRANCH_COPIES.csv"
VALIDATION = OUT / "P8_Y5_BRR545_2242_VALIDATION.csv"


COPY_TARGETS = {
    "queue_external_metadata": QUEUE / "ZR2242_EXTERNAL_R10_BOUND_METADATA_ROW_NONCLAIM.csv",
    "queue_internal_template": QUEUE / "ZR2242_FIRST_INTERNAL_ZR_OR_TAUR10_TEMPLATE_NONCLAIM.csv",
    "rab_docs_template": RAB_DOCS / "ZR2242_TAU_R10_PROJECTION_ROW_TEMPLATE_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "first_internal_ZR_or_tauR10_projection_nonclaim_2242.csv",
    "beta_docs": BETA_DOCS / "FIRST_INTERNAL_ZR_OR_TAUR10_PROJECTION_2242_NONCLAIM.csv",
}


OLD_TO_NEW = [
    (
        "1568-Y5-RAB-parent-contract-derivation-from-MTS-primitives-or-first-live-ZR-row.md",
        "2241-Y5-R2FR-RAB-parent-contract-derivation-from-MTS-primitives-or-first-live-ZR-row.md",
    ),
    (
        "1569-Y5-RAB-first-internal-ZR-or-tauR10-projection-row.md",
        "2242-Y5-R2FR-RAB-first-internal-ZR-or-tauR10-projection-row.md",
    ),
    (
        "1570-Y5-RAB-R10-curve-digitization-or-tau-kernel-source-normalization.md",
        "2243-Y5-R2FR-RAB-parent-finite-quadratic-row-and-source-test-beta-split.md",
    ),
    (
        "scripts/Y5_RAB_first_internal_ZR_or_tauR10_projection_row.py",
        "scripts/Y5_R2FR_RAB_first_internal_ZR_or_tauR10_projection_row_2242.py",
    ),
    (
        "scripts/Y5_RAB_R10_curve_digitization_or_tau_kernel_source_normalization.py",
        "scripts/Y5_R2FR_RAB_parent_finite_quadratic_row_and_source_test_beta_split_2243.py",
    ),
    (
        "source-intake/rab-sector/external/r10/1569",
        "source-intake/rab-sector/external/r10/2242",
    ),
    ("P8_Y5_BRR545_1568", "P8_Y5_BRR545_2241"),
    ("P8_Y5_PARENT_QLOC_1568_", "P8_Y5_PARENT_QLOC_2241_"),
    ("P8_Y5_BRR545_1569", "P8_Y5_BRR545_2242"),
    ("P8_Y5_PARENT_QLOC_1569_", "P8_Y5_PARENT_QLOC_2242_"),
    ("NEXT_1569_FIRST_INTERNAL_ZR_OR_TAU_R10_PROJECTION_ROW", "NEXT_2242_FIRST_INTERNAL_ZR_OR_TAU_R10_PROJECTION_ROW"),
    ("NEXT_1570_R10_CURVE_DIGITIZATION_OR_TAU_KERNEL_SOURCE_NORMALIZATION", "NEXT_2243_PARENT_FINITE_QUADRATIC_ROW_AND_SOURCE_TEST_BETA_SPLIT"),
    ("NEXT1569", "NEXT2242"),
    ("SRC1569", "SRC2242"),
    ("LSA1569", "LSA2242"),
    ("ZR1569", "ZR2242"),
    ("TAU1569", "TAU2242"),
    ("EXTBOUND1569", "EXTBOUND2242"),
    ("INT1569", "INT2242"),
    ("RUN1569", "RUN2242"),
    ("GATE1569", "GATE2242"),
    ("DEC1569", "DEC2242"),
    ("VAL1569", "VAL2242"),
]


GENERATED = [
    SOURCE_REGISTER,
    LOCAL_SOURCE_AUDIT,
    ZR_ATTEMPT,
    TAU_ATTEMPT,
    SOURCE_TEST_KERNEL_CONTRACT,
    EXTERNAL_R10_METADATA,
    INTERNAL_ROW_STATUS,
    INTERNAL_JOIN_READINESS,
    PROJECTION_TEMPLATE,
    RUNNER,
    CLAIM_GATE,
    DECISION,
    NEXT_TARGET,
    BRANCH_COPIES,
    VALIDATION,
]


def flags() -> dict[str, bool]:
    return {
        "numeric_value_present": False,
        "source_backed": False,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def resolve_project_path(path_text: str) -> Path:
    path_text = path_text.strip()
    if not path_text:
        return ROOT
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def rewrite_value(value: str) -> str:
    rewritten = value
    for old, new in OLD_TO_NEW:
        rewritten = rewritten.replace(old, new)
    return rewritten


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def validation_pass(path: Path) -> bool:
    if not path.exists():
        return False
    rows = read_csv(path)
    if not rows:
        return False
    id_key = "check_id" if "check_id" in rows[0] else "validation_id"
    result_key = "result" if "result" in rows[0] else "status"
    overall_rows = [row for row in rows if "overall" in row.get(id_key, "").lower() or "summary" in row.get(id_key, "").lower()]
    if overall_rows:
        return all(row.get(result_key, "").lower() == "pass" for row in overall_rows)
    return all(row.get(result_key, "").lower() == "pass" for row in rows)


def transform_old_csv(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_csv(path):
        new_row: dict[str, Any] = {"branch_id": BRANCH_ID}
        for key, value in row.items():
            if key == "same_parent_branch_id":
                continue
            new_row[key] = rewrite_value(value)
        rows.append(new_row)
    return rows


def localize_external_metadata() -> None:
    CURRENT_CROSSREF.parent.mkdir(parents=True, exist_ok=True)
    if not OLD_CROSSREF.exists():
        raise FileNotFoundError(OLD_CROSSREF)
    shutil.copyfile(OLD_CROSSREF, CURRENT_CROSSREF)


def crossref_anchor_present() -> bool:
    if not CURRENT_CROSSREF.exists():
        return False
    try:
        text = CURRENT_CROSSREF.read_text(encoding="utf-8")
        data = json.loads(text)
    except (OSError, json.JSONDecodeError):
        return False
    flattened = json.dumps(data)
    return "Combined Test of the Gravitational Inverse-Square Law" in flattened and "10.1103/PhysRevLett.126.211101" in flattened


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (key, path) in enumerate(SOURCE_FILES.items()):
        if key.startswith("2241"):
            role = "current R2FR handoff"
        elif key.startswith("1569"):
            role = "older first-internal-row checkpoint being imported"
        elif key.startswith("1033") or key.startswith("1035"):
            role = "tau_R10/K_X source-test projection grammar"
        else:
            role = "localized external R10 metadata"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": f"SRC2242_{index}_{key}",
                "source_path": rel(path),
                "path_exists": path.exists(),
                "validation_overall_pass": validation_pass(path) if key.endswith("validation") else "",
                "role": role,
                **flags(),
            }
        )
    return rows


def source_register_paths_exist() -> bool:
    return all(resolve_project_path(row["source_path"]).exists() for row in read_csv(SOURCE_REGISTER))


def source_test_kernel_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "branch_id": BRANCH_ID,
            "contract_id": "KERN2242_0_observable",
            "piece": "R10 Yukawa observable",
            "conditional_law": "V(r)=-G m_s m_t/r [1+alpha_R(lambda) exp(-r/lambda)]",
            "status": "OBSERVABLE_CONVENTION_IDENTIFIED",
            "missing_input": "digitized/source-backed alpha_bound(lambda) curve plus MTS alpha_R(lambda)",
            "why_it_matters": "sets the comparison target without creating a theory prediction",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "KERN2242_1_range",
            "piece": "finite R_AB range",
            "conditional_law": "lambda_R=sqrt(Z_R/M_R^2) only after Z_R and M_R^2 are parent-normalized and sign-healthy",
            "status": "MISSING_ZR_MR2",
            "missing_input": "Z_R, M_R^2, units, sign convention, and source anchor",
            "why_it_matters": "external lambda values do not define the MTS mode range",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "KERN2242_2_green_kernel",
            "piece": "static Green kernel",
            "conditional_law": "K_R^pt=1/(4 pi G_N Z_R) in canonical mass-normalized charge units; otherwise units must be declared",
            "status": "SYMBOLIC_CONDITIONAL",
            "missing_input": "parent charge convention, SI/hbar/c conversion, and Z_R",
            "why_it_matters": "prevents hiding normalization inside tau_R10",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "KERN2242_3_source_test_product",
            "piece": "source/test charge split",
            "conditional_law": "alpha_R10(lambda)=K_R^R10(lambda) beta_source(lambda) beta_test(lambda)+epsilon_tail(lambda)",
            "status": "REQUIRED_PRODUCT_FORM",
            "missing_input": "beta_source, beta_test, R10 profile/harmonic projection, and retained-tail envelope",
            "why_it_matters": "a two-body exchange is not a one-leg linear c_g score",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "KERN2242_4_universal_weyl_warning",
            "piece": "universal c_g branch",
            "conditional_law": "if both source and test legs are universal Weyl responses, alpha_R10 is proportional to c_g^2 unless one leg is already packed into Qbar",
            "status": "CG_SQUARED_WARNING",
            "missing_input": "proof of which leg Qbar_XH contains and whether c_g is source, test, or both",
            "why_it_matters": "blocks the old shorthand alpha ~ K Qbar tau_R10 c_g from being overclaimed",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "KERN2242_5_zero_branch",
            "piece": "operator-exclusion zero route",
            "conditional_law": "Z_R=0 only if the parent protection contract is signed and no representative Weyl/disformal/operator source can regenerate R_AB",
            "status": "FAILED_CURRENT_PARENT_PROOF",
            "missing_input": "primitive derivation of the 2240 protection contract or explicit closure adoption",
            "why_it_matters": "keeps theorem-zero separate from finite bound scoring",
            **flags(),
        },
    ]
    return rows


def internal_join_rows() -> list[dict[str, Any]]:
    targets = [
        ("JOIN2242_0_ZR", "Z_R", "kinetic residue or theorem-zero", "MISSING_THEOREM_ZERO_OR_NUMERIC_VALUE"),
        ("JOIN2242_1_MR2", "M_R^2", "mass/range Hessian", "MISSING_HESSIAN_OR_RANGE_VALUE"),
        ("JOIN2242_2_JR", "J_R", "source current coupling", "MISSING_SOURCE_CURRENT"),
        ("JOIN2242_3_BR", "B_R/Pi_R^n", "boundary/corner support", "MISSING_BOUNDARY_ZERO_OR_VALUE"),
        ("JOIN2242_4_beta_source", "beta_source(lambda)", "source-body charge leg", "MISSING_SOURCE_CHARGE"),
        ("JOIN2242_5_beta_test", "beta_test(lambda)", "test-body/readout charge leg", "MISSING_TEST_CHARGE"),
        ("JOIN2242_6_KR10", "K_R^R10(lambda)", "Green/profile/harmonic kernel", "SYMBOLIC_ONLY_NOT_NUMERIC"),
        ("JOIN2242_7_tau_R10", "tau_R10", "test projection shorthand", "MISSING_ARENA_PROJECTION"),
        ("JOIN2242_8_alpha_predicted", "alpha_R10(lambda)", "scoreable MTS prediction", "MISSING_SOURCE_NORMALIZED_ALPHA"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "join_id": join_id,
            "target": target,
            "role": role,
            "status": status,
            "ready_for_raw": False,
            "ready_for_accepted": False,
            "blocking_reason": "no parent-signed theorem-zero, no numeric source-backed row, or incomplete source/test projection",
            **flags(),
        }
        for join_id, target, role, status in targets
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2242_0_ZR",
            "decision": "first internal Z_R row",
            "result": "NOT_READY",
            "reason": "Z_R still needs theorem-zero from parent operator exclusion or a source-backed finite coefficient and range",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2242_1_tau",
            "decision": "tau_R10 projection",
            "result": "CONTRACT_REFINED_NOT_FILLED",
            "reason": "tau_R10 is now forced into source/test Yukawa product language, but beta_source, beta_test, Z_R, lambda_R, and R10 harmonic projection are missing",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2242_2_external_bound",
            "decision": "external R10 metadata",
            "result": "LOCAL_METADATA_ROW_READY_NONCLAIM",
            "reason": "Crossref metadata is localized under the current 2242 path; it remains metadata only, not a bound curve or MTS projection",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2242_3_next",
            "decision": "next target",
            "result": "NEXT_2243_PARENT_FINITE_QUADRATIC_ROW_AND_SOURCE_TEST_BETA_SPLIT",
            "reason": "the shortest honest route is to derive/source the parent finite R_AB quadratic row and beta_source/beta_test split before spending tokens digitizing external curves",
            **flags(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_id": "NEXT2242_0_2243",
            "next_target": "2243-Y5-R2FR-RAB-parent-finite-quadratic-row-and-source-test-beta-split.md",
            "script": "scripts/Y5_R2FR_RAB_parent_finite_quadratic_row_and_source_test_beta_split_2243.py",
            "objective": "derive or demote the parent finite R_AB quadratic action row that supplies Z_R, M_R^2/lambda_R, J_R, beta_source, beta_test, and the c_g versus c_g^2 coupling law",
            "do_not": "do not digitize external curves as a substitute for MTS-side coefficients; do not set tau_R10=1; do not score linear c_g without identifying the source leg; do not edit formalization-workbench",
            **flags(),
        }
    ]


def copy_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    copy_map = {
        "queue_external_metadata": EXTERNAL_R10_METADATA,
        "queue_internal_template": PROJECTION_TEMPLATE,
        "rab_docs_template": PROJECTION_TEMPLATE,
        "branch_wep": INTERNAL_JOIN_READINESS,
        "beta_docs": INTERNAL_JOIN_READINESS,
    }
    for copy_id, source in copy_map.items():
        target = COPY_TARGETS[copy_id]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": copy_id,
                "source_path": rel(source),
                "target_path": rel(target),
                "copied": target.exists(),
                "parse_ok": parse_csv(target),
                **flags(),
            }
        )
    return rows


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    keys = [
        "numeric_value_present",
        "source_backed",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
    ]
    for path in paths:
        for row in read_csv(path):
            for key in keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def no_internal_rows_ready() -> bool:
    rows = read_csv(INTERNAL_JOIN_READINESS) + read_csv(INTERNAL_ROW_STATUS)
    return bool(rows) and all(
        str(row.get("ready_for_raw", row.get("ready_for_accepted", "False"))).lower() != "true"
        and str(row.get("ready_for_accepted", "False")).lower() != "true"
        for row in rows
    )


def tau_product_law_present() -> bool:
    rows = read_csv(SOURCE_TEST_KERNEL_CONTRACT)
    text = " ".join(row.get("conditional_law", "") + " " + row.get("status", "") for row in rows)
    return "beta_source" in text and "beta_test" in text and "c_g^2" in text


def projection_template_nonclaim() -> bool:
    rows = read_csv(PROJECTION_TEMPLATE)
    text = " ".join(" ".join(row.values()) for row in rows)
    return "MISSING" in text and "DO_NOT_SCORE" in text


def claim_gates_closed() -> bool:
    rows = read_csv(CLAIM_GATE)
    return bool(rows) and all("BLOCKED" in row.get("status", "") or "NONCLAIM" in row.get("status", "") for row in rows)


def external_metadata_nonclaim() -> bool:
    rows = read_csv(EXTERNAL_R10_METADATA)
    text = " ".join(" ".join(row.values()) for row in rows)
    return bool(rows) and "MISSING_DIGITIZED_ALPHA_LAMBDA_CURVE" in text and "metadata" in text.lower()


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_2242_artifacts_absent() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(
        path.is_file()
        and "2242" in path.name
        and ".venv" not in path.relative_to(FORMALIZATION).parts
        for path in FORMALIZATION.rglob("*")
    )


def formalization_untouched_since_start() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(path.is_file() and path.stat().st_mtime >= START_TS for path in FORMALIZATION.rglob("*"))


def validation_rows(generated_paths: list[Path]) -> list[dict[str, Any]]:
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2242_00_sources_exist",
            "result": "PASS" if all(path.exists() for path in SOURCE_FILES.values()) and source_register_paths_exist() else "FAIL",
            "detail": "all direct and registered 2242 source paths exist",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2242_01_prior_validations",
            "result": "PASS"
            if validation_pass(SOURCE_FILES["2241_validation"])
            and validation_pass(SOURCE_FILES["1569_validation"])
            and validation_pass(SOURCE_FILES["1035_validation"])
            else "FAIL",
            "detail": "2241, 1569, and 1035 validations pass overall",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2242_02_crossref_localized",
            "result": "PASS" if crossref_anchor_present() else "FAIL",
            "detail": "R10 Crossref metadata is localized under the current 2242 path and anchored by DOI/title",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2242_03_ZR_not_ready",
            "result": "PASS" if any(row.get("status") == "NOT_READY" for row in read_csv(ZR_ATTEMPT)) else "FAIL",
            "detail": "Z_R theorem-zero/numeric row remains not ready",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2242_04_tau_product_law",
            "result": "PASS" if tau_product_law_present() else "FAIL",
            "detail": "tau_R10 is constrained by source/test product law and c_g-squared warning",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2242_05_no_internal_row",
            "result": "PASS" if no_internal_rows_ready() else "FAIL",
            "detail": "no internal Z_R/M_R^2/J_R/B_R/beta/tau row is ready for raw or accepted intake",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2242_06_external_metadata_nonclaim",
            "result": "PASS" if external_metadata_nonclaim() else "FAIL",
            "detail": "external R10 metadata is localized but remains nonclaim and not a digitized curve",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2242_07_template_nonclaim",
            "result": "PASS" if projection_template_nonclaim() else "FAIL",
            "detail": "projection templates contain MISSING markers and DO_NOT_SCORE policy",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2242_08_runner_blocks_claim",
            "result": "PASS" if any(row.get("current_status") == "BLOCKED_NO_CLAIM" for row in read_csv(RUNNER)) else "FAIL",
            "detail": "runner blocks R10/local-GR claim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2242_09_claim_gates",
            "result": "PASS" if claim_gates_closed() else "FAIL",
            "detail": "claim gates remain closed except nonclaim metadata localization",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2242_10_decision_next",
            "result": "PASS" if any(row.get("result") == "NEXT_2243_PARENT_FINITE_QUADRATIC_ROW_AND_SOURCE_TEST_BETA_SPLIT" for row in read_csv(DECISION)) else "FAIL",
            "detail": "decision selects parent finite quadratic row and source/test beta split next",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2242_11_next_target",
            "result": "PASS" if read_csv(NEXT_TARGET)[0]["next_target"].startswith("2243-Y5-R2FR-RAB-parent-finite-quadratic") else "FAIL",
            "detail": "next target is current-numbered parent finite quadratic row/beta split",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2242_12_csv_parse",
            "result": "PASS" if all(parse_csv(path) for path in generated_paths) else "FAIL",
            "detail": "all generated 2242 CSVs parse cleanly",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2242_13_claim_flags_false",
            "result": "PASS" if generated_flags_false(generated_paths) else "FAIL",
            "detail": "all generated prediction/claim flags remain false",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2242_14_branch_copies",
            "result": "PASS" if all(row["copied"] == "True" and row["parse_ok"] == "True" for row in read_csv(BRANCH_COPIES)) else "FAIL",
            "detail": "branch/quarantine nonclaim copies written",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2242_15_pycache_absent",
            "result": "PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent after run",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2242_16_formalization_no_2242",
            "result": "PASS" if formalization_2242_artifacts_absent() else "FAIL",
            "detail": "formalization-workbench has no non-venv 2242 artifacts",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2242_17_formalization_untouched",
            "result": "PASS" if formalization_untouched_since_start() else "FAIL",
            "detail": "formalization-workbench untouched during 2242 run",
        },
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2242_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2242 localizes R10 metadata under the current branch, refuses first internal Z_R/tau rows, sharpens tau_R10 into a source/test Yukawa kernel contract, and selects the parent finite quadratic row/beta split next",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_doc(
    source: list[dict[str, Any]],
    local_audit: list[dict[str, Any]],
    zr: list[dict[str, Any]],
    tau: list[dict[str, Any]],
    kernel: list[dict[str, Any]],
    external: list[dict[str, Any]],
    internal: list[dict[str, Any]],
    join: list[dict[str, Any]],
    template: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    claim: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 2242 - Y5/R2FR R_AB First Internal Z_R or tau_R10 Projection Row",
            "## Verdict\n"
            "- 2242 imports the old `1569` first-internal-row gate into the current R2FR chain after `2241` showed the primitive parent-contract route is not derived.\n"
            "- The first external R10 metadata source is now localized under the current `2242` path, but it is still not a digitized `alpha(lambda)` bound curve.\n"
            "- The first internal MTS row still cannot be filled: `Z_R`, `M_R^2`, `J_R`, `B_R`, `beta_source`, `beta_test`, and `tau_R10` lack theorem-zeroes or source-backed values.\n"
            "- The useful leap is structural: `tau_R10` is forced into a source/test Yukawa product law, and the old one-leg linear `c_g` shorthand is blocked unless the source leg is explicitly packed into `Qbar`.\n"
            "- No row was moved to raw or accepted; no `Z_R=0`, `q_R=0`, R10, PPN, WEP, clock, orbital, local GR, or Newton claim is made.",
            "## Source Register\n"
            + md_table(source, ["source_id", "source_path", "path_exists", "validation_overall_pass", "role"]),
            "## Local Source Audit\n"
            + md_table(local_audit, ["audit_id", "source_path", "source_exists", "anchor", "anchor_found", "source_role", "not_sufficient_for"]),
            "## Z_R Attempt\n"
            + md_table(zr, ["attempt_id", "target", "required_input", "status", "reason"]),
            "## tau_R10 Projection Attempt\n"
            + md_table(tau, ["projection_id", "projection_piece", "role", "status", "blocking_gap"]),
            "## Source/Test Kernel Contract\n"
            + md_table(kernel, ["contract_id", "piece", "conditional_law", "status", "missing_input", "why_it_matters"]),
            "## External R10 Bound Metadata Row\n"
            + md_table(external, ["row_id", "row_type", "arena", "quantity", "source_path", "doi", "metadata_status", "bound_curve_status", "why_not_scoreable"]),
            "## First Internal Row Status\n"
            + md_table(internal, ["status_id", "target", "current_evidence", "status", "ready_for_raw", "ready_for_accepted"]),
            "## Internal Join Readiness\n"
            + md_table(join, ["join_id", "target", "role", "status", "ready_for_raw", "ready_for_accepted", "blocking_reason"]),
            "## Projection Template\n"
            + md_table(template, ["row_id", "coefficient_symbol", "coefficient_value", "coefficient_units", "normalization_convention", "parent_action_block", "source_path", "source_anchor", "arena_projection", "placeholder_status"]),
            "## Runner\n"
            + md_table(runner, ["runner_id", "test", "current_status", "detail"]),
            "## Claim Gate\n"
            + md_table(claim, ["gate_id", "claim_gate", "status", "reason"]),
            "## Decision Ledger\n"
            + md_table(decision, ["decision_id", "decision", "result", "reason"]),
            "## Next Target\n"
            + md_table(next_target, ["next_id", "next_target", "script", "objective", "do_not"]),
            "## Branch Copies\n"
            + md_table(copies, ["copy_id", "source_path", "target_path", "copied", "parse_ok"]),
            "## Validation\n"
            + md_table(validation, ["check_id", "result", "detail"]),
            "## Working Interpretation\n\n"
            "This is progress, but not the glamorous kind: the R10 bridge has stopped being a foggy coupling word and has become a hard shopping list. "
            "A finite local `R_AB` branch must provide a parent-normalized quadratic row, a range, a source current, and separate source/test beta legs before any external R10 curve matters. "
            "That means the next best attack is not another public-looking bound plot; it is the parent finite-mode action row that either gives `Z_R, M_R^2, J_R, beta_source, beta_test` or proves they are absent.",
            "",
        ]
    )


def main() -> None:
    localize_external_metadata()

    source = source_rows()
    local_audit = transform_old_csv(OUT / "P8_Y5_PARENT_QLOC_1569_LOCAL_SOURCE_AUDIT.csv")
    zr = transform_old_csv(OUT / "P8_Y5_PARENT_QLOC_1569_ZR_THEOREM_OR_COEFFICIENT_ATTEMPT.csv")
    tau = transform_old_csv(OUT / "P8_Y5_PARENT_QLOC_1569_TAU_R10_PROJECTION_ATTEMPT.csv")
    kernel = source_test_kernel_rows()
    external = transform_old_csv(OUT / "P8_Y5_PARENT_QLOC_1569_EXTERNAL_R10_BOUND_METADATA_ROW.csv")
    internal = transform_old_csv(OUT / "P8_Y5_PARENT_QLOC_1569_FIRST_INTERNAL_ROW_STATUS.csv")
    join = internal_join_rows()
    template = transform_old_csv(RAB_DOCS / "ZR1569_TAU_R10_PROJECTION_ROW_TEMPLATE_NONCLAIM.csv")
    runner = transform_old_csv(OUT / "P8_Y5_PARENT_QLOC_1569_RUNNER_NONCLAIM.csv")
    claim = transform_old_csv(OUT / "P8_Y5_PARENT_QLOC_1569_CLAIM_GATE.csv")
    decision = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, source)
    write_csv(LOCAL_SOURCE_AUDIT, local_audit)
    write_csv(ZR_ATTEMPT, zr)
    write_csv(TAU_ATTEMPT, tau)
    write_csv(SOURCE_TEST_KERNEL_CONTRACT, kernel)
    write_csv(EXTERNAL_R10_METADATA, external)
    write_csv(INTERNAL_ROW_STATUS, internal)
    write_csv(INTERNAL_JOIN_READINESS, join)
    write_csv(PROJECTION_TEMPLATE, template)
    write_csv(RUNNER, runner)
    write_csv(CLAIM_GATE, claim)
    write_csv(DECISION, decision)
    write_csv(NEXT_TARGET, next_target)
    copies = copy_rows()
    write_csv(BRANCH_COPIES, copies)

    remove_pycache()
    generated_before_validation = [path for path in GENERATED if path != VALIDATION]
    validation = validation_rows(generated_before_validation)
    write_csv(VALIDATION, validation)
    remove_pycache()

    DOC.write_text(
        build_doc(
            source,
            local_audit,
            zr,
            tau,
            kernel,
            external,
            internal,
            join,
            template,
            runner,
            claim,
            decision,
            next_target,
            copies,
            validation,
        ),
        encoding="utf-8",
    )

    if not validation_pass(VALIDATION):
        raise SystemExit(f"2242 validation failed: {VALIDATION}")


if __name__ == "__main__":
    main()
