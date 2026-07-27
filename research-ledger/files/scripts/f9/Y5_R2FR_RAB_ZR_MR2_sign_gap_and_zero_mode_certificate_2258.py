from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

BRANCH_ID = "MTS_R2FR_PARENT_QLOC_RAB_SIGN_GAP_CERTIFICATE_2258"
DOC = ROOT / "2258-Y5-R2FR-RAB-ZR-MR2-sign-gap-and-zero-mode-certificate.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2258_00_2257_doc",
        "source_key": "2257_doc",
        "source_path": ROOT / "2257-Y5-R2FR-positive-RAB-working-branch-activation-vector.md",
        "needles": ["NEXT2257_0_primary", "OPR2257_0_ZR", "OPR2257_4_domain_gauge_quotient"],
        "role": "2257 selects Z_R/M_R^2 sign-gap and zero-mode certificate",
    },
    {
        "source_id": "SRC2258_01_2257_validation",
        "source_key": "2257_validation",
        "source_path": OUT / "P8_Y5_BRR545_2257_VALIDATION.csv",
        "needles": ["VAL2257_OVERALL", "PASS"],
        "role": "confirms 2257 passed before 2258 starts",
    },
    {
        "source_id": "SRC2258_02_2257_operator_rows",
        "source_key": "2257_operator_rows",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2257_OPERATOR_SIGN_GAP_ROWS.csv",
        "needles": ["OPR2257_0_ZR", "OPR2257_1_MR2", "OPR2257_4_domain_gauge_quotient"],
        "role": "current operator sign/gap row set",
    },
    {
        "source_id": "SRC2258_03_2248_doc",
        "source_key": "2248_nohair",
        "source_path": ROOT / "2248-Y5-R2FR-RAB-sourcefree-positive-RAB-nohair-identity-or-alpha3-prior-first-fill.md",
        "needles": ["NH2248_3_zero_theorem", "RNH2248_1_operator_sign_gap"],
        "role": "conditional no-hair identity and missing operator sign/gap premise",
    },
    {
        "source_id": "SRC2258_04_2095_doc",
        "source_key": "2095_doc",
        "source_path": ROOT / "2095-Y5-R2FR-ZR-MR2-operator-signature-source-row.md",
        "needles": ["OP2095_1_row_null_zero", "DEC2095_1_source_status", "VAL2095_OVERALL"],
        "role": "prior Z_R/M_R^2 operator signature source-row audit",
    },
    {
        "source_id": "SRC2258_05_2095_validation",
        "source_key": "2095_validation",
        "source_path": OUT / "P8_Y5_BRR545_2095_VALIDATION.csv",
        "needles": ["VAL2095_OVERALL", "PASS"],
        "role": "confirms prior Z_R/M_R^2 audit passed",
    },
    {
        "source_id": "SRC2258_06_2095_operator",
        "source_key": "2095_operator",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2095_OPERATOR_SIGNATURE_GATE.csv",
        "needles": ["OP2095_0_static_operator", "OP2095_1_row_null_zero", "OP2095_5_verdict"],
        "role": "machine-readable row-null/finite-operator fork",
    },
    {
        "source_id": "SRC2258_07_2095_scan",
        "source_key": "2095_scan",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2095_FINITE_SOURCE_SCAN_REVIEW.csv",
        "needles": ["SCAN2095_ZR", "SCAN2095_MR2", "NO_VALID_SOURCE_ROW_FOUND"],
        "role": "finite source scan reports no valid Z_R/M_R^2 source candidates",
    },
    {
        "source_id": "SRC2258_08_2095_inputs",
        "source_key": "2095_inputs",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2095_FINITE_OPERATOR_INPUT_ROWS.csv",
        "needles": ["ZRI2095_0_ZRR", "ZRI2095_2_MR2", "SOURCE_REQUIRED_NONCLAIM"],
        "role": "finite operator inputs still require source-backed parent rows",
    },
    {
        "source_id": "SRC2258_09_2170_doc",
        "source_key": "2170_doc",
        "source_path": ROOT / "2170-Y5-R2FR-QR-ZR-MR2-source-chain-first-fill-or-no-charge-return.md",
        "needles": ["FR2170_1_ZR_MR2", "DEC2170_4_next_route", "VAL2170_OVERALL"],
        "role": "anti-loop result: do not redo coefficient first-fill; move to category/compatibility owner",
    },
    {
        "source_id": "SRC2258_10_2170_validation",
        "source_key": "2170_validation",
        "source_path": OUT / "P8_Y5_BRR545_2170_VALIDATION.csv",
        "needles": ["VAL2170_OVERALL", "PASS"],
        "role": "confirms anti-loop import map passed",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2258_SOURCE_REGISTER.csv",
    "sign_gap": OUT / "P8_Y5_PARENT_QLOC_2258_SIGN_GAP_CERTIFICATE_AUDIT.csv",
    "zero_mode_domain": OUT / "P8_Y5_PARENT_QLOC_2258_ZERO_MODE_DOMAIN_AUDIT.csv",
    "anti_loop": OUT / "P8_Y5_PARENT_QLOC_2258_ANTI_LOOP_IMPORT_MAP.csv",
    "demotion_queue": OUT / "P8_Y5_PARENT_QLOC_2258_RESIDUAL_DEMOTION_QUEUE.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2258_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2258_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2258_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2258_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2258_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2258_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_sign_gap": QUEUE / "JR2258_RAB_SIGN_GAP_CERTIFICATE_AUDIT_NONCLAIM.csv",
    "queue_demotion": QUEUE / "JR2258_RAB_RESIDUAL_DEMOTION_QUEUE_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "RAB_sign_gap_nonclaim_2258.csv",
    "beta_docs": BETA_DOCS / "RAB_SIGN_GAP_2258_NONCLAIM.csv",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def validation_pass(path: Path) -> bool:
    if not path.exists():
        return False
    rows = read_csv(path)
    if not rows:
        return False
    id_key = "check_id" if "check_id" in rows[0] else "validation_id"
    result_key = "result" if "result" in rows[0] else "status"
    overall = [row for row in rows if "overall" in row.get(id_key, "").lower()]
    return all(row.get(result_key, "").lower() == "pass" for row in (overall or rows))


def false_flags() -> dict[str, bool]:
    return {
        "theorem_zero": False,
        "parent_signed": False,
        "numeric_value_present": False,
        "source_backed": False,
        "score_ready": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCES:
        path = source["source_path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": rel(path),
                "exists": exists,
                "needles": ";".join(source["needles"]),
                "needles_present": exists and all(needle in text for needle in source["needles"]),
                "validation_overall_pass": validation_pass(path) if "validation" in source["source_key"] else "",
                "role": source["role"],
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def src(*keys: str) -> str:
    by_key = {source["source_key"]: source["source_path"] for source in SOURCES}
    return ";".join(rel(by_key[key]) for key in keys)


def sign_gap_certificate_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "SG2258_0_ZR",
            "Z_R",
            "finite positive kinetic coefficient on the physical quotient",
            "FAIL_NOT_SOURCE_BACKED",
            "2095 scan reports no valid Z_R/Z_RR/Z_RY source rows; 2257 only restates the requirement.",
            src("2257_operator_rows", "2095_scan", "2095_operator"),
        ),
        (
            "SG2258_1_MR2",
            "M_R^2",
            "finite nonnegative/positive mass gap with same normalization as Z_R",
            "FAIL_NOT_SOURCE_BACKED",
            "2095 scan reports no valid M_R^2 source row and no lambda_R normalization.",
            src("2257_operator_rows", "2095_scan", "2095_inputs"),
        ),
        (
            "SG2258_2_Hessian_R",
            "Hessian_R",
            "second variation positive on allowed R_AB directions after quotienting gauge/kernel modes",
            "FAIL_PARENT_HESSIAN_UNSIGNED",
            "row-null Hessian condition is exact if factorised, but quotient factorisation is not parent-signed.",
            src("2095_doc", "2095_operator"),
        ),
        (
            "SG2258_3_cross_terms",
            "Z_RY/cross Hessian",
            "no surviving cross kinetic/mass channel can spoil positivity or create a hidden source",
            "FAIL_CROSS_TERMS_UNSIGNED",
            "2095 scalar projection guard forbids using scalar Z_R alone while Z_RY/cross terms are open.",
            src("2095_operator", "2095_inputs"),
        ),
        (
            "SG2258_4_row_null_zero",
            "row-null zero route",
            "J_u^A Z_AB^{mu nu}=0 for every parent direction, killing the finite R_AB operator before scoring",
            "FAIL_FACTORISATION_UNSIGNED",
            "exact route exists but current corpus does not prove quotient factorisation or nonprimitive R_AB status.",
            src("2095_doc", "2170_doc"),
        ),
        (
            "SG2258_5_verdict",
            "operator sign/gap certificate",
            "either theorem-zero row-null Hessian or finite positive Z_R/M_R^2 package",
            "SIGN_GAP_CERTIFICATE_NOT_CLOSED",
            "neither zero route nor finite source-backed positive route is available at claim level.",
            src("2257_doc", "2095_doc", "2170_doc"),
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "certificate_id": certificate_id,
            "object": object_name,
            "required_statement": required,
            "result": result,
            "reason": reason,
            "source_paths": source_paths,
            **false_flags(),
        }
        for certificate_id, object_name, required, result, reason, source_paths in entries
    ]


def zero_mode_domain_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "ZD2258_0_zero_modes",
            "zero_mode_rule",
            "constant, gauge, topological, and boundary kernels removed or projected out",
            "MISSING_ZERO_MODE_RULE",
            "2248 and 2257 require this, but no parent domain certificate supplies it.",
        ),
        (
            "ZD2258_1_self_adjoint",
            "self_adjoint_domain",
            "operator domain supports integration by parts without uncontrolled corner terms",
            "MISSING_SELF_ADJOINT_DOMAIN",
            "energy identity remains conditional until boundary/corner domain is fixed.",
        ),
        (
            "ZD2258_2_gauge_slice",
            "gauge_slice",
            "R_AB variations are measured on a fixed gauge/quotient slice rather than representative artifacts",
            "MISSING_GAUGE_QUOTIENT_SLICE",
            "positive Hessian cannot be read before the quotient representative is fixed.",
        ),
        (
            "ZD2258_3_local_exterior",
            "local_exterior_D",
            "source-free local domain D excludes bodies and fixes matching data to the exterior",
            "MISSING_LOCAL_DOMAIN_CONTRACT",
            "J_R and boundary clauses cannot be separated without the domain contract.",
        ),
        (
            "ZD2258_4_boundary_flux",
            "boundary_flux_sign",
            "Phi_boundary_local is zero or has sign-controlled finite contribution",
            "MISSING_BOUNDARY_FLUX_ZERO_OR_SIGN",
            "positive operator alone cannot kill boundary hair.",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "domain_id": domain_id,
            "object": object_name,
            "required_statement": required,
            "current_status": status,
            "reason": reason,
            "source_paths": src("2248_nohair", "2257_operator_rows"),
            **false_flags(),
        }
        for domain_id, object_name, required, status, reason in entries
    ]


def anti_loop_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "AL2258_0_2095",
            "2095 Z_R/M_R^2 operator signature audit",
            "imported",
            "already shows row-null zero route exact but unsigned, and finite Z_R/M_R^2 rows absent",
            "do not rerun finite source scan without new parent action input",
            src("2095_doc", "2095_validation", "2095_operator", "2095_scan"),
        ),
        (
            "AL2258_1_2170",
            "2170 Q_R/Z_R/M_R2 anti-loop map",
            "imported",
            "already reduces coefficient first-fill to compatibility-object/category-owner problem",
            "promote compatibility-object bridge rather than repeat coefficient bookkeeping",
            src("2170_doc", "2170_validation"),
        ),
        (
            "AL2258_2_2257",
            "2257 activation vector",
            "refined",
            "operator sign/gap remains the correct first gate, but prior audits show no claim-grade rows exist",
            "either prove non-dynamical compatibility object or demote positive branch to residual-only",
            src("2257_doc", "2257_validation"),
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "import_id": import_id,
            "source_checkpoint": checkpoint,
            "import_status": status,
            "imported_result": result,
            "anti_loop_rule": rule,
            "source_paths": source_paths,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for import_id, checkpoint, status, result, rule, source_paths in entries
    ]


def demotion_queue_rows() -> list[dict[str, Any]]:
    entries = [
        ("RD2258_0_ZR", "Z_R/Z_RR/Z_RY", "finite kinetic rows with source paths, units, and cross-term policy", "MISSING_SOURCE_BACKED_OPERATOR_INPUTS"),
        ("RD2258_1_MR2", "M_R^2/lambda_R", "finite mass gap/range row with same normalization as kinetic row", "MISSING_SOURCE_BACKED_MASS_RANGE"),
        ("RD2258_2_domain", "domain/zero-mode package", "explicit local domain, gauge slice, kernel removal, and boundary condition", "MISSING_DOMAIN_KERNEL_PACKAGE"),
        ("RD2258_3_JR", "J_R_res", "zero theorem or componentwise source bound for the local branch", "MISSING_SOURCE_VECTOR_ZERO_OR_BOUNDS"),
        ("RD2258_4_projection", "arena kernels", "q_loc, PPN, R10, clock, and orbital projection kernels for any retained residual", "MISSING_ARENA_PROJECTION_KERNELS"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "queue_id": queue_id,
            "object": object_name,
            "required_row": required,
            "current_status": status,
            "queue_policy": "residual-only if compatibility-object theorem fails",
            "source_paths": src("2257_doc", "2095_doc", "2170_doc"),
            **false_flags(),
        }
        for queue_id, object_name, required, status in entries
    ]


def refusal_rows() -> list[dict[str, Any]]:
    entries = [
        ("REF2258_0_sign_gap", "Z_R/M_R^2 sign-gap certificate closes", "BLOCKED", "SG2258_5_verdict=SIGN_GAP_CERTIFICATE_NOT_CLOSED"),
        ("REF2258_1_row_null", "row-null Hessian kills R_AB operator", "BLOCKED", "factorisation/nonprimitive compatibility proof unsigned"),
        ("REF2258_2_positive_nohair", "positive operator activates 2248 no-hair theorem", "BLOCKED", "Z_R/M_R^2/Hessian/domain/J_R/boundary premises not all signed"),
        ("REF2258_3_local_GR", "derived local GR/Newton recovery", "BLOCKED", "operator certificate and projection cleanup not closed"),
        ("REF2258_4_local_tests", "R10/PPN/clock/orbital scoring", "BLOCKED", "no source-backed finite rows or arena kernels"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "refusal_id": refusal_id,
            "attempted_claim": claim,
            "runner_result": result,
            "blocked_by": blocked_by,
            "score_eligible": False,
            **false_flags(),
        }
        for refusal_id, claim, result, blocked_by in entries
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    entries = [
        ("CG2258_0_ZR", "Z_R positive/source-backed", "no valid parent Z_R/Z_RR/Z_RY row found"),
        ("CG2258_1_MR2", "M_R^2 positive/source-backed", "no valid parent mass-gap row found"),
        ("CG2258_2_Hessian", "positive Hessian on quotient", "row-null/factorisation not parent-signed"),
        ("CG2258_3_zero_modes", "zero-mode/domain package", "gauge/domain/boundary kernels remain open"),
        ("CG2258_4_nohair", "2248 no-hair activation", "operator/source/boundary package not closed"),
        ("CG2258_5_local_GR_Newton", "derived local GR/Newton branch", "upstream certificate fails"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": claim_id,
            "claim": claim,
            "gate_pass": False,
            "reason": reason,
            **false_flags(),
        }
        for claim_id, claim, reason in entries
    ]


def decision_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "DEC2258_0_status",
            "SIGN_GAP_CERTIFICATE_NOT_CLOSED",
            "2258 attempted the exact gate selected by 2257 and found prior audits already rule out claim-grade Z_R/M_R^2 rows.",
            "keep positive branch nonclaim",
        ),
        (
            "DEC2258_1_no_loop",
            "DO_NOT_REPEAT_ZR_MR2_SOURCE_SCAN",
            "2095 and 2170 already did the coefficient first-fill/anti-loop work; repeating it without new parent input would be motion without progress.",
            "import anti-loop result",
        ),
        (
            "DEC2258_2_best_route",
            "COMPATIBILITY_OBJECT_BRIDGE_NEXT",
            "the only route that could still make this a GR derivation is proving R_AB/C_R is a parent compatibility/constraint object, not an independent local field.",
            "build 2259 compatibility-object bridge",
        ),
        (
            "DEC2258_3_fallback",
            "RESIDUAL_DEMOTION_QUEUE_READY",
            "if compatibility fails, all missing quantities become explicit finite residual rows with no local-GR claim.",
            "carry demotion queue",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            **false_flags(),
        }
        for decision_id, decision, reason, next_action in entries
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2258_0_primary",
            "next_target": "2259-Y5-R2FR-RAB-compatibility-object-bridge-or-residual-demotion.md",
            "script": "scripts/Y5_R2FR_RAB_compatibility_object_bridge_or_residual_demotion_2259.py",
            "objective": "try to prove R_AB/C_R is a non-dynamical parent compatibility/constraint object in the current local branch; if not, demote to explicit finite residual rows",
            "selection_status": "selected",
            "success_condition": "parent-signed compatibility-object theorem removes the independent local R_AB operator, or residual demotion is made explicit without local-GR claim",
            "forbidden_claims": "Z_R/M_R^2 positivity by placeholder; local-GR/Newton/R10/PPN pass; gamma-only shortcut; cancellation between residual channels",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2258_1_fallback",
            "next_target": "2259b-Y5-R2FR-RAB-finite-residual-source-pack-runner.md",
            "script": "scripts/Y5_R2FR_RAB_finite_residual_source_pack_runner_2259b.py",
            "objective": "if compatibility theorem fails, build source-ready residual rows for Z_R, M_R^2, J_R, boundary, B_Weyl/B_Ric, and arena projections",
            "selection_status": "held_fallback",
            "success_condition": "finite residual rows are source-backed, unit-normalized, and arena-projected, still with no GR claim",
            "forbidden_claims": "claim from unsourced rows; R10/PPN pass without kernels",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def copy_branch_rows() -> list[dict[str, Any]]:
    copies = [
        ("sign_gap", OUTPUTS["sign_gap"], COPY_TARGETS["queue_sign_gap"], "sign/gap certificate audit for R_AB branch"),
        ("demotion", OUTPUTS["demotion_queue"], COPY_TARGETS["queue_demotion"], "residual demotion queue if compatibility theorem fails"),
        ("branch_wep", OUTPUTS["claim_gates"], COPY_TARGETS["branch_wep"], "branch-locked local/WEP refusal gates"),
        ("beta_docs", OUTPUTS["decision"], COPY_TARGETS["beta_docs"], "portable sign/gap decision ledger"),
    ]
    rows = []
    for copy_id, source_path, target_path, reason in copies:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": f"BC2258_{copy_id}",
                "source_path": rel(source_path),
                "target_path": rel(target_path),
                "target_exists": target_path.exists(),
                "target_parses": parse_csv(target_path),
                "reason": reason,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def validation_rows(paths: list[Path]) -> list[dict[str, Any]]:
    source_rows = read_csv(OUTPUTS["source_register"])
    sign_gap = read_csv(OUTPUTS["sign_gap"])
    zero_mode_domain = read_csv(OUTPUTS["zero_mode_domain"])
    anti_loop = read_csv(OUTPUTS["anti_loop"])
    demotion_queue = read_csv(OUTPUTS["demotion_queue"])
    refusals = read_csv(OUTPUTS["refusal"])
    claims = read_csv(OUTPUTS["claim_gates"])
    decisions = read_csv(OUTPUTS["decision"])
    next_targets = read_csv(OUTPUTS["next_target"])
    copies = read_csv(OUTPUTS["branch_copies"])

    def check(check_id: str, passed: bool, detail: str) -> dict[str, Any]:
        return {"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail}

    csv_parse_ok = True
    for path in paths:
        try:
            parse_csv(path)
        except Exception:
            csv_parse_ok = False

    formalization_2258 = []
    if FORMALIZATION.exists():
        formalization_2258 = [path for path in FORMALIZATION.rglob("*2258*") if path.is_file()]

    sign_objects = {row["object"] for row in sign_gap}
    domain_objects = {row["object"] for row in zero_mode_domain}
    all_rows = [row for path in paths for row in read_csv(path)]

    rows = [
        check("VAL2258_0_sources_exist", all(row["exists"] == "True" for row in source_rows), "all cited source paths exist"),
        check("VAL2258_1_needles_present", all(row["needles_present"] == "True" for row in source_rows), "all cited source needles are present"),
        check("VAL2258_2_prior_validations", all(row["validation_overall_pass"] in ("", "True") for row in source_rows), "2095, 2170, and 2257 validations pass where checked"),
        check("VAL2258_3_sign_gap_coverage", {"Z_R", "M_R^2", "Hessian_R", "Z_RY/cross Hessian", "row-null zero route", "operator sign/gap certificate"}.issubset(sign_objects), "sign/gap audit covers finite and zero-route certificate clauses"),
        check("VAL2258_4_zero_mode_domain_coverage", {"zero_mode_rule", "self_adjoint_domain", "gauge_slice", "local_exterior_D", "boundary_flux_sign"}.issubset(domain_objects), "zero-mode/domain audit covers kernel, domain, gauge, local exterior, and boundary flux"),
        check("VAL2258_5_certificate_not_closed", any(row["certificate_id"] == "SG2258_5_verdict" and row["result"] == "SIGN_GAP_CERTIFICATE_NOT_CLOSED" for row in sign_gap), "certificate explicitly remains unclosed"),
        check("VAL2258_6_anti_loop_imported", len(anti_loop) == 3 and all("imported" in row["import_status"] or "refined" in row["import_status"] for row in anti_loop), "2095/2170 anti-loop evidence imported"),
        check("VAL2258_7_demotion_queue_retained", len(demotion_queue) == 5 and all(row["valid_for_claim"] == "False" for row in demotion_queue), "finite residual demotion queue retained as nonclaim"),
        check("VAL2258_8_runner_refuses", all(row["runner_result"] == "BLOCKED" for row in refusals), "refusal runner blocks all current claims"),
        check("VAL2258_9_claim_gates_blocked", all(row["gate_pass"] == "False" for row in claims), "claim gates are blocked"),
        check("VAL2258_10_decision_next", any(row["decision_id"] == "DEC2258_2_best_route" and row["decision"] == "COMPATIBILITY_OBJECT_BRIDGE_NEXT" for row in decisions), "decision selects compatibility-object bridge next"),
        check("VAL2258_11_next_selected", any(row["route_id"] == "NEXT2258_0_primary" and row["selection_status"] == "selected" for row in next_targets), "next target selected"),
        check("VAL2258_12_csv_parse", csv_parse_ok, "all generated 2258 CSVs parse"),
        check("VAL2258_13_no_claim_flags", all(row.get("valid_for_claim", "False") != "True" and row.get("claim_allowed", "False") != "True" and row.get("theorem_zero", "False") != "True" and row.get("parent_signed", "False") != "True" and row.get("score_ready", "False") != "True" and row.get("source_backed", "False") != "True" for row in all_rows), "no generated theorem/parent/source/score/claim flags are true"),
        check("VAL2258_14_branch_copies", all(row["target_exists"] == "True" and row["target_parses"] == "True" for row in copies), "branch/queue copies exist and parse"),
        check("VAL2258_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        check("VAL2258_16_formalization_no_2258", not formalization_2258, "formalization-workbench has no 2258 outputs"),
    ]
    rows.append(
        check(
            "VAL2258_OVERALL",
            all(row["result"] == "PASS" for row in rows),
            "2258 attempts the R_AB sign/gap and zero-mode certificate, imports prior anti-loop evidence, refuses closure, and selects the compatibility-object bridge next",
        )
    )
    return rows


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def build_doc(
    source_rows: list[dict[str, Any]],
    sign_gap: list[dict[str, Any]],
    zero_mode_domain: list[dict[str, Any]],
    anti_loop: list[dict[str, Any]],
    demotion_queue: list[dict[str, Any]],
    refusals: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_targets: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 2258 - Y5/R2FR R_AB Z_R/M_R^2 Sign-Gap And Zero-Mode Certificate",
            "## Verdict\n\n2258 tries the exact first gate selected by 2257 and refuses to fake it. The sign/gap certificate does **not** close: prior 2095 evidence already found no valid source rows for `Z_R`, `Z_RR`, `Z_RY`, or `M_R^2`, and the exact row-null Hessian zero route is still conditional on an unsigned quotient/factorisation theorem.\n\nThat is not a dead end; it is a routing decision. Repeating the coefficient hunt would be a loop. The next non-circular route is to try the compatibility-object bridge: prove `R_AB/C_R` is not an independent local field but a parent constraint/compatibility object. If that fails, we demote cleanly to explicit finite residual rows.",
            "## Source Register\n" + markdown_table(source_rows, ["source_id", "source_key", "source_path", "exists", "needles_present", "validation_overall_pass", "role"]),
            "## Sign/Gap Certificate Audit\n" + markdown_table(sign_gap, ["certificate_id", "object", "required_statement", "result", "reason", "valid_for_claim"]),
            "## Zero-Mode/Domain Audit\n" + markdown_table(zero_mode_domain, ["domain_id", "object", "required_statement", "current_status", "reason", "valid_for_claim"]),
            "## Anti-Loop Import Map\n" + markdown_table(anti_loop, ["import_id", "source_checkpoint", "import_status", "imported_result", "anti_loop_rule", "valid_for_claim"]),
            "## Residual Demotion Queue\n" + markdown_table(demotion_queue, ["queue_id", "object", "required_row", "current_status", "queue_policy", "valid_for_claim"]),
            "## Refusal Runner\n" + markdown_table(refusals, ["refusal_id", "attempted_claim", "runner_result", "blocked_by", "score_eligible", "valid_for_claim"]),
            "## Claim Gates\n" + markdown_table(claims, ["claim_id", "claim", "gate_pass", "reason", "valid_for_claim"]),
            "## Decision Ledger\n" + markdown_table(decisions, ["decision_id", "decision", "reason", "next_action", "valid_for_claim"]),
            "## Next Target\n" + markdown_table(next_targets, ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "## Branch Copies\n" + markdown_table(copies, ["copy_id", "source_path", "target_path", "target_exists", "target_parses", "reason"]),
            "## Validation\n" + markdown_table(validation, ["check_id", "result", "detail"]),
            "## Working Interpretation\n\nThis is the useful kind of bad news. The positive-operator/no-hair branch remains mathematically attractive, but the operator package is not claim-grade. The project should now take the leap that 2170 had already pointed toward: try to make `R_AB/C_R` a compatibility object of the parent geometry rather than a new fitted local field. If that proof lands, local GR recovery gets much cleaner. If it fails, we stop pretending and score residuals honestly.",
        ]
    ) + "\n"


def main() -> None:
    remove_pycache()

    source_rows = source_register_rows()
    sign_gap = sign_gap_certificate_rows()
    zero_mode_domain = zero_mode_domain_rows()
    anti_loop = anti_loop_rows()
    demotion_queue = demotion_queue_rows()
    refusals = refusal_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_target_rows()

    write_csv(OUTPUTS["source_register"], source_rows)
    write_csv(OUTPUTS["sign_gap"], sign_gap)
    write_csv(OUTPUTS["zero_mode_domain"], zero_mode_domain)
    write_csv(OUTPUTS["anti_loop"], anti_loop)
    write_csv(OUTPUTS["demotion_queue"], demotion_queue)
    write_csv(OUTPUTS["refusal"], refusals)
    write_csv(OUTPUTS["claim_gates"], claims)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next_target"], next_targets)

    copies = copy_branch_rows()
    write_csv(OUTPUTS["branch_copies"], copies)

    generated = [
        OUTPUTS["source_register"],
        OUTPUTS["sign_gap"],
        OUTPUTS["zero_mode_domain"],
        OUTPUTS["anti_loop"],
        OUTPUTS["demotion_queue"],
        OUTPUTS["refusal"],
        OUTPUTS["claim_gates"],
        OUTPUTS["decision"],
        OUTPUTS["next_target"],
        OUTPUTS["branch_copies"],
    ]

    validation = validation_rows(generated)
    write_csv(OUTPUTS["validation"], validation)
    remove_pycache()
    validation = validation_rows(generated)
    write_csv(OUTPUTS["validation"], validation)

    DOC.write_text(
        build_doc(source_rows, sign_gap, zero_mode_domain, anti_loop, demotion_queue, refusals, claims, decisions, next_targets, copies, validation),
        encoding="utf-8",
    )

    if not all(row["result"] == "PASS" for row in validation):
        raise SystemExit("2258 validation failed")

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
