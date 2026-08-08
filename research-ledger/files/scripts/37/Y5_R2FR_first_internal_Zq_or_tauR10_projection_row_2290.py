from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_DOCS = ROOT / "source-intake" / "rab-sector" / "docs"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
EXTERNAL_2242 = ROOT / "source-intake" / "rab-sector" / "external" / "r10" / "2242" / "crossref_10.1103_PhysRevLett.126.211101.json"
EXTERNAL_2290 = ROOT / "source-intake" / "rab-sector" / "external" / "r10" / "2290" / "crossref_10.1103_PhysRevLett.126.211101.json"

BRANCH_ID = "MTS_R2FR_FIRST_INTERNAL_ZQ_OR_TAUR10_PROJECTION_ROW_2290"
START_TS = datetime.now(timezone.utc).timestamp()
DOC = ROOT / "2290-Y5-R2FR-first-internal-Zq-or-tauR10-projection-row.md"


def source_specs() -> list[dict[str, Any]]:
    return [
        {
            "source_id": "SRC2290_00_2289_doc",
            "source_key": "2289_handoff",
            "source_path": ROOT / "2289-Y5-R2FR-parent-protection-contract-derivation-from-MTS-primitives-or-first-live-Zq-row.md",
            "needles": ["NEXT_2290_FIRST_INTERNAL_ZQ_OR_TAUR10_PROJECTION_ROW", "internal Z_q theorem/value", "tau_R10"],
            "role": "current handoff selecting first internal Zq or tau_R10 row",
        },
        {
            "source_id": "SRC2290_01_2289_validation",
            "source_key": "2289_validation",
            "source_path": OUT / "P8_Y5_BRR545_2289_VALIDATION.csv",
            "needles": ["VAL2289_OVERALL", "PASS"],
            "role": "confirms 2289 passed before 2290",
        },
        {
            "source_id": "SRC2290_02_2289_external",
            "source_key": "2289_external_bound",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_2289_FIRST_EXTERNAL_BOUND_SOURCE_ROW.csv",
            "needles": ["BOUND2289_R10_EOTWASH_PRL_2021", "external_arena_bound_only", "SOURCE_URL_IDENTIFIED_NEEDS_LOCAL_DIGITIZATION_OR_TABLE"],
            "role": "external R10 comparator row",
        },
        {
            "source_id": "SRC2290_03_2289_internal",
            "source_key": "2289_internal_status",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_2289_FIRST_INTERNAL_COEFFICIENT_ROW_STATUS.csv",
            "needles": ["COEFF2289_0_Zq", "COEFF2289_4_tau_R10", "NO_INTERNAL_ROW_READY"],
            "role": "current internal coefficient/projection missing status",
        },
        {
            "source_id": "SRC2290_04_2242_doc",
            "source_key": "2242_first_row_checkpoint",
            "source_path": ROOT / "2242-Y5-R2FR-RAB-first-internal-ZR-or-tauR10-projection-row.md",
            "needles": ["source/test Yukawa product law", "one-leg linear `c_g`", "2243-Y5-R2FR"],
            "role": "previous same-fork source/test projection checkpoint",
        },
        {
            "source_id": "SRC2290_05_2242_validation",
            "source_key": "2242_validation",
            "source_path": OUT / "P8_Y5_BRR545_2242_VALIDATION.csv",
            "needles": ["VAL2242_OVERALL", "PASS"],
            "role": "confirms 2242 passed as nonclaim",
        },
        {
            "source_id": "SRC2290_06_2242_zr",
            "source_key": "2242_zr_attempt",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_2242_ZR_THEOREM_OR_COEFFICIENT_ATTEMPT.csv",
            "needles": ["ZR2242_0_theorem_zero", "MISSING_INTERNAL_COEFFICIENT", "NOT_READY"],
            "role": "Z_R theorem/numeric coefficient still not ready",
        },
        {
            "source_id": "SRC2290_07_2242_tau",
            "source_key": "2242_tau_attempt",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_2242_TAU_R10_PROJECTION_ATTEMPT.csv",
            "needles": ["TAU2242_0_external_form", "TAU2242_3_projection_kernel", "KERNEL_CONTRACT_WRITTEN_NOT_FILLED"],
            "role": "tau_R10 projection shape exists but is not filled",
        },
        {
            "source_id": "SRC2290_08_2242_kernel",
            "source_key": "2242_kernel_contract",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_2242_SOURCE_TEST_KERNEL_CONTRACT.csv",
            "needles": ["KERN2242_3_source_test_product", "KERN2242_4_universal_weyl_warning", "CG_SQUARED_WARNING"],
            "role": "source/test product law and c_g^2 warning",
        },
        {
            "source_id": "SRC2290_09_2242_join",
            "source_key": "2242_join_readiness",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_2242_INTERNAL_JOIN_READINESS.csv",
            "needles": ["JOIN2242_4_beta_source", "JOIN2242_7_tau_R10", "JOIN2242_8_alpha_predicted"],
            "role": "internal join readiness blockers",
        },
        {
            "source_id": "SRC2290_10_1033_tau",
            "source_key": "1033_tau_audit",
            "source_path": OUT / "P8_Y5_R10_1033_TAU_R10_DERIVATION_AUDIT.csv",
            "needles": ["TAUR1033_1_factorization", "TAUR1033_5_universal_cg_limit", "UNITY_SHORTCUT_REJECTED"],
            "role": "tau_R10 source/test/Green projection grammar",
        },
        {
            "source_id": "SRC2290_11_1035_split",
            "source_key": "1035_source_test_split",
            "source_path": OUT / "P8_Y5_R10_1035_SOURCE_TEST_CHARGE_SPLIT.csv",
            "needles": ["BETA1035_0_product_law", "BETA1035_1_universal_weyl", "CONDITIONAL_CG_SQUARED_WARNING"],
            "role": "two-body source/test charge split",
        },
        {
            "source_id": "SRC2290_12_1035_factorization",
            "source_key": "1035_KX_factorization",
            "source_path": OUT / "P8_Y5_R10_1035_KX_FACTORIZATION_ROWS.csv",
            "needles": ["KXF1035_0_KX_point", "KXF1035_4_total", "NOT_NUMERIC_CURRENT_CORPUS"],
            "role": "K_X factorization requirements",
        },
        {
            "source_id": "SRC2290_13_1035_validation",
            "source_key": "1035_validation",
            "source_path": OUT / "P8_Y5_BRR545_1035_VALIDATION.csv",
            "needles": ["V1035_SUMMARY", "pass"],
            "role": "confirms 1035 kernel checkpoint passed",
        },
        {
            "source_id": "SRC2290_14_crossref_metadata",
            "source_key": "2290_crossref_metadata",
            "source_path": EXTERNAL_2290,
            "needles": ["Combined Test of the Gravitational Inverse-Square Law at the Centimeter Range", "10.1103", "PhysRevLett.126.211101"],
            "role": "localized external R10 metadata copied forward from 2242",
        },
    ]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2290_SOURCE_REGISTER.csv",
    "local_source_audit": OUT / "P8_Y5_PARENT_QLOC_2290_LOCAL_SOURCE_AUDIT.csv",
    "zq_attempt": OUT / "P8_Y5_PARENT_QLOC_2290_ZQ_THEOREM_OR_COEFFICIENT_ATTEMPT.csv",
    "tau_attempt": OUT / "P8_Y5_PARENT_QLOC_2290_TAU_R10_PROJECTION_ATTEMPT.csv",
    "kernel_contract": OUT / "P8_Y5_PARENT_QLOC_2290_SOURCE_TEST_KERNEL_CONTRACT.csv",
    "external_metadata": OUT / "P8_Y5_PARENT_QLOC_2290_EXTERNAL_R10_BOUND_METADATA_ROW.csv",
    "internal_status": OUT / "P8_Y5_PARENT_QLOC_2290_FIRST_INTERNAL_ROW_STATUS.csv",
    "join_readiness": OUT / "P8_Y5_PARENT_QLOC_2290_INTERNAL_JOIN_READINESS.csv",
    "projection_template": OUT / "P8_Y5_PARENT_QLOC_2290_PROJECTION_TEMPLATE_NONCLAIM.csv",
    "runner": OUT / "P8_Y5_PARENT_QLOC_2290_RUNNER_NONCLAIM.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2290_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2290_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2290_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2290_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2290_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_external_metadata": (OUTPUTS["external_metadata"], QUEUE / "ZQ2290_EXTERNAL_R10_BOUND_METADATA_ROW_NONCLAIM.csv"),
    "queue_internal_template": (OUTPUTS["projection_template"], QUEUE / "ZQ2290_FIRST_INTERNAL_ZQ_OR_TAUR10_TEMPLATE_NONCLAIM.csv"),
    "rab_docs_template": (OUTPUTS["projection_template"], RAB_DOCS / "ZQ2290_TAU_R10_PROJECTION_ROW_TEMPLATE_NONCLAIM.csv"),
    "branch_wep": (OUTPUTS["join_readiness"], MICROSCOPE / "first_internal_Zq_or_tauR10_projection_nonclaim_2290.csv"),
    "beta_docs": (OUTPUTS["join_readiness"], BETA_DOCS / "FIRST_INTERNAL_ZQ_OR_TAUR10_PROJECTION_2290_NONCLAIM.csv"),
}


def stringify(value: Any) -> str:
    if isinstance(value, bool):
        return "True" if value else "False"
    return str(value)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow({key: stringify(value) for key, value in row.items()})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def validation_pass(path: Path) -> bool:
    if not path.exists() or not csv_parses(path):
        return False
    rows = read_csv(path)
    if not rows:
        return False
    id_key = "check_id" if "check_id" in rows[0] else "validation_id"
    result_key = "result" if "result" in rows[0] else "status"
    overall_rows = [row for row in rows if "overall" in row.get(id_key, "").lower()]
    if overall_rows:
        return all(row.get(result_key, "").upper() == "PASS" for row in overall_rows)
    return all(row.get(result_key, "").upper() == "PASS" for row in rows)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def ignored_environment_path(path: Path) -> bool:
    ignored_parts = {".venv", ".venv-score", "__pycache__", "site-packages", ".git"}
    return any(part in ignored_parts for part in path.parts)


def formalization_has_2290_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    for candidate in FORMALIZATION.rglob("*2290*"):
        if candidate.is_file() and not ignored_environment_path(candidate.relative_to(FORMALIZATION)):
            return True
    return False


def formalization_touched_since_start() -> bool:
    if not FORMALIZATION.exists():
        return False
    for candidate in FORMALIZATION.rglob("*"):
        if candidate.is_file() and not ignored_environment_path(candidate.relative_to(FORMALIZATION)):
            if candidate.stat().st_mtime >= START_TS:
                return True
    return False


def table(headers: list[str], rows: list[dict[str, Any]]) -> str:
    def cell(value: Any) -> str:
        return stringify(value).replace("\n", " ").replace("|", "\\|")

    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def localize_external_metadata() -> None:
    EXTERNAL_2290.parent.mkdir(parents=True, exist_ok=True)
    if EXTERNAL_2242.exists():
        shutil.copyfile(EXTERNAL_2242, EXTERNAL_2290)
    elif not EXTERNAL_2290.exists():
        raise FileNotFoundError(f"missing external metadata source: {EXTERNAL_2242}")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in source_specs():
        source_path = Path(source["source_path"])
        source_text = read_text(source_path)
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": source_path,
                "exists": source_path.exists(),
                "needles": "; ".join(needles),
                "needles_present": all(needle in source_text for needle in needles),
                "role": source["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def local_source_audit_rows() -> list[dict[str, Any]]:
    metadata_text = read_text(EXTERNAL_2290)
    return [
        {
            "audit_id": "LSA2290_0_crossref_metadata",
            "source_path": EXTERNAL_2290,
            "source_exists": EXTERNAL_2290.exists(),
            "anchor": "Combined Test of the Gravitational Inverse-Square Law at the Centimeter Range",
            "anchor_found": "Combined Test of the Gravitational Inverse-Square Law at the Centimeter Range" in metadata_text,
            "source_role": "external R10 metadata/provenance only",
            "not_sufficient_for": "digitized alpha(lambda) curve; MTS Z_q/M_q^2/j_q/B_R/tau coefficient; accepted score row",
            "valid_for_claim": False,
        },
        {
            "audit_id": "LSA2290_1_aps_fulltext",
            "source_path": "https://link.aps.org/doi/10.1103/PhysRevLett.126.211101",
            "source_exists": False,
            "anchor": "APS full text or table not localized in 2290",
            "anchor_found": False,
            "source_role": "primary DOI page; not locally cached as curve/table",
            "not_sufficient_for": "local source-backed digitization until accessible PDF/fulltext/table is acquired",
            "valid_for_claim": False,
        },
    ]


def zq_attempt_rows() -> list[dict[str, Any]]:
    entries = [
        ("ZQ2290_0_theorem_zero", "Z_q=0 from parent operator exclusion", "signed parent protection contract and primitive derivation success", "FAILED_CURRENT_PARENT_PROOF", "1237/2289 say sorted grammar/ParentGenerate exhaustion is closure-only"),
        ("ZQ2290_1_numeric_coefficient", "finite Z_q value", "parent-normalized coefficient, units, source path, and source anchor", "MISSING_INTERNAL_COEFFICIENT", "no local source-backed MTS Z_q row exists"),
        ("ZQ2290_2_mass_gap", "M_q^2 or lambda_q=sqrt(Z_q/M_q^2)", "Hessian/range source in same normalization as Z_q", "MISSING_INTERNAL_RANGE", "external R10 alpha(lambda) bound does not supply MTS lambda_q"),
        ("ZQ2290_3_verdict", "first internal Z_q row", "theorem-zero or finite coefficient", "NOT_READY", "keep finite residual branch open but unscored"),
    ]
    return [
        {
            "attempt_id": attempt_id,
            "target": target,
            "required_input": required,
            "status": status,
            "reason": reason,
            "score_ready": False,
            "valid_for_claim": False,
        }
        for attempt_id, target, required, status, reason in entries
    ]


def tau_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "projection_id": "TAU2290_0_external_form",
            "projection_piece": "R10 tests constrain alpha(lambda) in V=-Gm_s m_t/r[1+alpha exp(-r/lambda)]",
            "role": "external comparison form",
            "status": "FORMAL_EXTERNAL_FORM_ONLY",
            "blocking_gap": "metadata localized; full digitized curve/table still needed",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "projection_id": "TAU2290_1_internal_range",
            "projection_piece": "lambda_q=sqrt(Z_q/M_q^2) or equivalent parent range",
            "role": "finite q/R_AB mode range",
            "status": "MISSING_ZQ_MQ2",
            "blocking_gap": "cannot assign lambda_q from external bound alone",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "projection_id": "TAU2290_2_internal_amplitude",
            "projection_piece": "alpha_MTS(lambda)=K_q^R10(lambda) beta_source(lambda) beta_test(lambda)+epsilon_tail(lambda)",
            "role": "scoreable MTS prediction form",
            "status": "MISSING_SOURCE_TEST_NORMALIZATION",
            "blocking_gap": "beta_source, beta_test, Z_q/M_q^2 and geometric profile kernel are not derived",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "projection_id": "TAU2290_3_projection_kernel",
            "projection_piece": "tau_R10 is a shorthand only after source/test legs and K_q^R10 are explicitly packed",
            "role": "bridge from theory coefficients to R10 alpha(lambda)",
            "status": "KERNEL_CONTRACT_REFINED_NOT_FILLED",
            "blocking_gap": "no numeric/theorem-zero kernel and no accepted internal row",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "projection_id": "TAU2290_4_verdict",
            "projection_piece": "first tau_R10 row",
            "role": "projection kernel plus local source path/anchor/units",
            "status": "NOT_READY",
            "blocking_gap": "do not move to raw/accepted",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def kernel_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "KERN2290_0_observable",
            "piece": "R10 Yukawa observable",
            "conditional_law": "V(r)=-G m_s m_t/r [1+alpha_q(lambda) exp(-r/lambda)]",
            "status": "OBSERVABLE_CONVENTION_IDENTIFIED",
            "missing_input": "digitized/source-backed alpha_bound(lambda) curve plus MTS alpha_q(lambda)",
            "why_it_matters": "sets comparison target without creating a theory prediction",
            "valid_for_claim": False,
        },
        {
            "contract_id": "KERN2290_1_range",
            "piece": "finite q/R_AB range",
            "conditional_law": "lambda_q=sqrt(Z_q/M_q^2) only after Z_q and M_q^2 are parent-normalized and sign-healthy",
            "status": "MISSING_ZQ_MQ2",
            "missing_input": "Z_q, M_q^2, units, sign convention, and source anchor",
            "why_it_matters": "external lambda values do not define the MTS mode range",
            "valid_for_claim": False,
        },
        {
            "contract_id": "KERN2290_2_green_kernel",
            "piece": "static Green kernel",
            "conditional_law": "K_q^pt=1/(4 pi G_N Z_q) only in canonical mass-normalized charge units; otherwise units must be declared",
            "status": "SYMBOLIC_CONDITIONAL",
            "missing_input": "parent charge convention, SI/hbar/c conversion, and Z_q",
            "why_it_matters": "prevents hiding normalization inside tau_R10",
            "valid_for_claim": False,
        },
        {
            "contract_id": "KERN2290_3_source_test_product",
            "piece": "source/test charge split",
            "conditional_law": "alpha_R10(lambda)=K_q^R10(lambda) beta_source(lambda) beta_test(lambda)+epsilon_tail(lambda)",
            "status": "REQUIRED_PRODUCT_FORM",
            "missing_input": "beta_source, beta_test, R10 profile/harmonic projection, and retained-tail envelope",
            "why_it_matters": "a two-body exchange is not a one-leg linear c_g score",
            "valid_for_claim": False,
        },
        {
            "contract_id": "KERN2290_4_universal_weyl_warning",
            "piece": "universal c_g branch",
            "conditional_law": "if source and test both respond universally, alpha_R10 is proportional to c_g^2 unless one leg is already packed into Qbar",
            "status": "CG_SQUARED_WARNING",
            "missing_input": "proof of which leg Qbar contains and whether c_g is source, test, or both",
            "why_it_matters": "blocks old shorthand alpha ~ K Qbar tau_R10 c_g from being overclaimed",
            "valid_for_claim": False,
        },
        {
            "contract_id": "KERN2290_5_zero_branch",
            "piece": "operator-exclusion zero route",
            "conditional_law": "Z_q=0 only if the parent protection contract is signed and no readout/source/operator channel regenerates q",
            "status": "FAILED_CURRENT_PARENT_PROOF",
            "missing_input": "primitive derivation of the protection contract or explicit closure adoption",
            "why_it_matters": "keeps theorem-zero separate from finite bound scoring",
            "valid_for_claim": False,
        },
    ]


def external_metadata_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "EXTBOUND2290_R10_CROSSREF_PRL126_211101",
            "row_type": "external_metadata_localized_nonclaim",
            "arena": "R10",
            "quantity": "alpha(lambda) Yukawa bound source metadata",
            "source_path": EXTERNAL_2290,
            "doi": "10.1103/PhysRevLett.126.211101",
            "metadata_status": "LOCAL_CROSSREF_METADATA_PRESENT",
            "bound_curve_status": "MISSING_DIGITIZED_ALPHA_LAMBDA_CURVE",
            "why_not_scoreable": "external metadata is not a digitized bound curve and not an MTS tau_R10 projection",
            "source_backed": False,
            "score_ready": False,
            "valid_for_claim": False,
        }
    ]


def first_internal_status_rows() -> list[dict[str, Any]]:
    entries = [
        ("INT2290_0_Zq", "Z_q", "no theorem-zero; no source-backed coefficient", "BLOCKED"),
        ("INT2290_1_Mq2", "M_q^2", "no parent Hessian/range source", "BLOCKED"),
        ("INT2290_2_jq", "j_q/J_q", "matter descent/source-current row missing", "BLOCKED"),
        ("INT2290_3_boundary", "B_R/Pi_q/Q_R", "boundary/corner zero or finite bound missing", "BLOCKED"),
        ("INT2290_4_tau_R10", "tau_R10", "projection kernel not filled; external metadata localized only", "BLOCKED"),
        ("INT2290_5_verdict", "first internal accepted/raw row", "not ready; no row moved to raw or accepted", "NO_INTERNAL_ROW_READY"),
    ]
    return [
        {
            "status_id": status_id,
            "target": target,
            "current_evidence": evidence,
            "status": status,
            "ready_for_raw": False,
            "ready_for_accepted": False,
            "score_ready": False,
            "valid_for_claim": False,
        }
        for status_id, target, evidence, status in entries
    ]


def join_readiness_rows() -> list[dict[str, Any]]:
    entries = [
        ("JOIN2290_0_Zq", "Z_q", "kinetic residue or theorem-zero", "MISSING_THEOREM_ZERO_OR_NUMERIC_VALUE"),
        ("JOIN2290_1_Mq2", "M_q^2", "mass/range Hessian", "MISSING_HESSIAN_OR_RANGE_VALUE"),
        ("JOIN2290_2_jq", "j_q/J_q", "source current coupling", "MISSING_SOURCE_CURRENT"),
        ("JOIN2290_3_boundary", "B_R/Pi_q/Q_R", "boundary/corner support", "MISSING_BOUNDARY_ZERO_OR_VALUE"),
        ("JOIN2290_4_beta_source", "beta_source(lambda)", "source-body charge leg", "MISSING_SOURCE_CHARGE"),
        ("JOIN2290_5_beta_test", "beta_test(lambda)", "test-body/readout charge leg", "MISSING_TEST_CHARGE"),
        ("JOIN2290_6_KR10", "K_q^R10(lambda)", "Green/profile/harmonic kernel", "SYMBOLIC_ONLY_NOT_NUMERIC"),
        ("JOIN2290_7_tau_R10", "tau_R10", "projection shorthand", "MISSING_ARENA_PROJECTION"),
        ("JOIN2290_8_alpha_predicted", "alpha_R10(lambda)", "scoreable MTS prediction", "MISSING_SOURCE_NORMALIZED_ALPHA"),
    ]
    return [
        {
            "join_id": join_id,
            "target": target,
            "role": role,
            "status": status,
            "ready_for_raw": False,
            "ready_for_accepted": False,
            "blocking_reason": "no parent-signed theorem-zero, no numeric source-backed row, or incomplete source/test projection",
            "valid_for_claim": False,
        }
        for join_id, target, role, status in entries
    ]


def projection_template_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "ZQ2290_TEMPLATE_TAU_R10",
            "coefficient_symbol": "tau_R10",
            "coefficient_value": "MISSING_TRANSFER_KERNEL",
            "coefficient_units": "MISSING_DIMENSIONLESS_OR_KERNEL_UNITS",
            "normalization_convention": "MISSING_Q_TO_ALPHA_NORMALIZATION",
            "parent_action_block": "MISSING_R10_PROJECTION_BLOCK",
            "source_path": EXTERNAL_2290,
            "source_anchor": "Combined Test of the Gravitational Inverse-Square Law at the Centimeter Range",
            "arena_projection": "R10",
            "placeholder_status": "MISSING_DO_NOT_SCORE",
            "valid_for_claim": False,
        },
        {
            "row_id": "ZQ2290_TEMPLATE_ZQ",
            "coefficient_symbol": "Z_q",
            "coefficient_value": "MISSING_THEOREM_ZERO_OR_NUMERIC_VALUE",
            "coefficient_units": "MISSING_PARENT_UNITS",
            "normalization_convention": "MISSING_Q_NORMALIZATION",
            "parent_action_block": "MISSING_OPERATOR_EXCLUSION_OR_COEFFICIENT_SOURCE",
            "source_path": "MISSING_INTERNAL_SOURCE_PATH",
            "source_anchor": "MISSING_INTERNAL_SOURCE_ANCHOR",
            "arena_projection": "R10;PPN;clock;orbital",
            "placeholder_status": "MISSING_DO_NOT_SCORE",
            "valid_for_claim": False,
        },
        {
            "row_id": "ZQ2290_TEMPLATE_MQ2",
            "coefficient_symbol": "M_q^2",
            "coefficient_value": "MISSING_HESSIAN_OR_RANGE_VALUE",
            "coefficient_units": "MISSING_PARENT_UNITS",
            "normalization_convention": "MISSING_Q_NORMALIZATION",
            "parent_action_block": "MISSING_PARENT_HESSIAN_BLOCK",
            "source_path": "MISSING_INTERNAL_SOURCE_PATH",
            "source_anchor": "MISSING_INTERNAL_SOURCE_ANCHOR",
            "arena_projection": "R10;PPN;clock;orbital",
            "placeholder_status": "MISSING_DO_NOT_SCORE",
            "valid_for_claim": False,
        },
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {"runner_id": "RUN2290_0_sources", "test": "load 2289/2242/1033/1035 and local R10 metadata", "current_status": "PASS", "detail": "all source register needles found", "score_ready": False, "valid_for_claim": False},
        {"runner_id": "RUN2290_1_Zq", "test": "first internal Z_q theorem/numeric row", "current_status": "FAILED_CURRENT_PARENT_PROOF", "detail": "no theorem-zero and no numeric parent coefficient", "score_ready": False, "valid_for_claim": False},
        {"runner_id": "RUN2290_2_tau_R10", "test": "first tau_R10 projection row", "current_status": "KERNEL_CONTRACT_REFINED_NOT_FILLED", "detail": "source/test product law is explicit, but internal source normalization and range are missing", "score_ready": False, "valid_for_claim": False},
        {"runner_id": "RUN2290_3_external_bound", "test": "external R10 metadata row", "current_status": "PASS_NONCLAIM_METADATA_LOCALIZED", "detail": "Crossref DOI metadata is local; digitized curve/table still missing", "score_ready": False, "valid_for_claim": False},
        {"runner_id": "RUN2290_4_raw_accepted", "test": "raw/accepted finite rows", "current_status": "NO_LIVE_SCORE_ROWS", "detail": "raw_rows=0; accepted_rows=0", "score_ready": False, "valid_for_claim": False},
        {"runner_id": "RUN2290_5_claim", "test": "R10/local GR claim", "current_status": "BLOCKED_NO_CLAIM", "detail": "external bound is not an MTS prediction and internal projection is missing", "score_ready": False, "valid_for_claim": False},
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {"gate_id": "GATE2290_0_Zq", "claim_gate": "Z_q theorem-zero or finite coefficient", "status": "BLOCKED_NO_CLAIM", "reason": "no parent theorem and no source-backed coefficient", "valid_for_claim": False, "claim_allowed": False},
        {"gate_id": "GATE2290_1_tau_R10", "claim_gate": "tau_R10 projection kernel", "status": "BLOCKED_NO_CLAIM", "reason": "projection formula lacks internal source/test normalization", "valid_for_claim": False, "claim_allowed": False},
        {"gate_id": "GATE2290_2_external_bound", "claim_gate": "external R10 bound metadata", "status": "PASS_SOURCE_QUEUE_NONCLAIM", "reason": "metadata localized but no bound curve and no MTS prediction", "valid_for_claim": False, "claim_allowed": False},
        {"gate_id": "GATE2290_3_raw_accepted", "claim_gate": "raw/accepted finite row", "status": "BLOCKED_NO_CLAIM", "reason": "no internal row moved to raw/accepted", "valid_for_claim": False, "claim_allowed": False},
        {"gate_id": "GATE2290_4_local_GR", "claim_gate": "derived local GR/Newton/R10 safety", "status": "BLOCKED_NO_CLAIM", "reason": "theory side remains missing", "valid_for_claim": False, "claim_allowed": False},
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {"decision_id": "DEC2290_0_Zq", "decision": "first internal Z_q row", "result": "NOT_READY", "reason": "Z_q still needs theorem-zero from parent operator exclusion or a source-backed finite coefficient and range", "next_action": "derive/source finite quadratic q row", "valid_for_claim": False},
        {"decision_id": "DEC2290_1_tau", "decision": "tau_R10 projection", "result": "CONTRACT_REFINED_NOT_FILLED", "reason": "tau_R10 is forced into source/test Yukawa product language, but beta_source, beta_test, Z_q, lambda_q, and R10 harmonic projection are missing", "next_action": "derive/source beta_source and beta_test split before scoring", "valid_for_claim": False},
        {"decision_id": "DEC2290_2_external_bound", "decision": "external R10 metadata", "result": "LOCAL_METADATA_ROW_READY_NONCLAIM", "reason": "Crossref metadata is localized under the 2290 path; it remains metadata only, not a bound curve or MTS projection", "next_action": "digitize curve later only after MTS-side coefficients/projection exist", "valid_for_claim": False},
        {"decision_id": "DEC2290_3_next", "decision": "next target", "result": "NEXT_2291_PARENT_FINITE_QUADRATIC_ROW_AND_SOURCE_TEST_BETA_SPLIT", "reason": "the shortest honest route is to derive/source the parent finite q quadratic row and beta_source/beta_test split before spending tokens digitizing external curves", "next_action": "2291-Y5-R2FR-parent-finite-quadratic-row-and-source-test-beta-split.md", "valid_for_claim": False},
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2290_0_primary",
            "next_target": "2291-Y5-R2FR-parent-finite-quadratic-row-and-source-test-beta-split.md",
            "script": "scripts/Y5_R2FR_parent_finite_quadratic_row_and_source_test_beta_split_2291.py",
            "objective": "derive or demote the parent finite q/R_AB quadratic action row that supplies Z_q, M_q^2/lambda_q, j_q, beta_source, beta_test, and the c_g versus c_g^2 coupling law",
            "do_not": "do not digitize external curves as a substitute for MTS-side coefficients; do not set tau_R10=1; do not score linear c_g without identifying the source leg; do not edit formalization-workbench",
            "valid_for_claim": False,
        }
    ]


def generated_claim_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    guarded_keys = {
        "source_backed",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "ready_for_raw",
        "ready_for_accepted",
    }
    for path in paths:
        for row in read_csv(path):
            for key, value in row.items():
                if key in guarded_keys and value.strip().lower() not in false_values:
                    return False
    return True


def projection_templates_have_missing_markers(rows: list[dict[str, Any]]) -> bool:
    return all("MISSING" in " ".join(str(value) for value in row.values()) and row["placeholder_status"] == "MISSING_DO_NOT_SCORE" for row in rows)


def copy_branch_files() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for copy_id, (source_path, target_path) in COPY_TARGETS.items():
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        rows.append(
            {
                "copy_id": copy_id,
                "source_path": source_path,
                "target_path": target_path,
                "target_exists": target_path.exists(),
                "target_parses": csv_parses(target_path),
                "reason": "branch copy for 2290 first internal Zq/tauR10 projection checkpoint",
            }
        )
    return rows


def validation_rows(all_generated_before_validation: list[Path], branch_copy_rows: list[dict[str, Any]], projection_templates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_rows = read_csv(OUTPUTS["source_register"])
    source_audit_rows = read_csv(OUTPUTS["local_source_audit"])
    zq_rows = read_csv(OUTPUTS["zq_attempt"])
    tau_rows = read_csv(OUTPUTS["tau_attempt"])
    kernel_rows = read_csv(OUTPUTS["kernel_contract"])
    external_rows = read_csv(OUTPUTS["external_metadata"])
    internal_rows = read_csv(OUTPUTS["internal_status"])
    join_rows = read_csv(OUTPUTS["join_readiness"])
    runner_rows_local = read_csv(OUTPUTS["runner"])
    claim_rows = read_csv(OUTPUTS["claim_gates"])
    decision_rows_local = read_csv(OUTPUTS["decision"])
    next_rows = read_csv(OUTPUTS["next_target"])

    checks = [
        ("VAL2290_0_sources_exist", all(row["exists"] == "True" for row in source_rows), "all cited source paths exist"),
        ("VAL2290_1_needles_present", all(row["needles_present"] == "True" for row in source_rows), "all cited source needles are present"),
        (
            "VAL2290_2_prior_validations",
            validation_pass(OUT / "P8_Y5_BRR545_2289_VALIDATION.csv")
            and validation_pass(OUT / "P8_Y5_BRR545_2242_VALIDATION.csv")
            and validation_pass(OUT / "P8_Y5_BRR545_1035_VALIDATION.csv"),
            "2289, 2242, and 1035 validation files pass overall",
        ),
        (
            "VAL2290_3_crossref_localized",
            any(row["audit_id"] == "LSA2290_0_crossref_metadata" and row["source_exists"] == "True" and row["anchor_found"] == "True" for row in source_audit_rows),
            "R10 Crossref metadata is localized under the 2290 path and anchored by title",
        ),
        (
            "VAL2290_4_Zq_not_ready",
            any(row["attempt_id"] == "ZQ2290_3_verdict" and row["status"] == "NOT_READY" for row in zq_rows)
            and all(row["score_ready"] == "False" for row in zq_rows),
            "Z_q theorem-zero/numeric row remains not ready",
        ),
        (
            "VAL2290_5_tau_product_law",
            any(row["status"] == "KERNEL_CONTRACT_REFINED_NOT_FILLED" for row in tau_rows)
            and any(row["status"] == "CG_SQUARED_WARNING" for row in kernel_rows)
            and any(row["status"] == "REQUIRED_PRODUCT_FORM" for row in kernel_rows),
            "tau_R10 is constrained by source/test product law and c_g-squared warning",
        ),
        (
            "VAL2290_6_no_internal_row",
            any(row["status"] == "NO_INTERNAL_ROW_READY" for row in internal_rows)
            and all(row["ready_for_raw"] == "False" and row["ready_for_accepted"] == "False" for row in internal_rows),
            "no internal Z_q/M_q^2/j_q/B_R/beta/tau row is ready for raw or accepted intake",
        ),
        (
            "VAL2290_7_external_metadata_nonclaim",
            any(row["bound_curve_status"] == "MISSING_DIGITIZED_ALPHA_LAMBDA_CURVE" and row["score_ready"] == "False" for row in external_rows),
            "external R10 metadata is localized but remains nonclaim and not a digitized curve",
        ),
        (
            "VAL2290_8_template_nonclaim",
            projection_templates_have_missing_markers(projection_templates),
            "projection templates contain MISSING markers and DO_NOT_SCORE policy",
        ),
        (
            "VAL2290_9_join_blocks_alpha",
            any(row["join_id"] == "JOIN2290_8_alpha_predicted" and row["status"] == "MISSING_SOURCE_NORMALIZED_ALPHA" for row in join_rows),
            "join readiness blocks alpha prediction until theory-side factors exist",
        ),
        (
            "VAL2290_10_runner_blocks_claim",
            any(row["current_status"] == "BLOCKED_NO_CLAIM" for row in runner_rows_local)
            and any(row["current_status"] == "KERNEL_CONTRACT_REFINED_NOT_FILLED" for row in runner_rows_local),
            "runner blocks R10/local-GR claim",
        ),
        (
            "VAL2290_11_claim_gates",
            any(row["claim_gate"] == "derived local GR/Newton/R10 safety" and row["status"] == "BLOCKED_NO_CLAIM" for row in claim_rows)
            and all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in claim_rows),
            "claim gates remain closed except nonclaim metadata localization",
        ),
        (
            "VAL2290_12_decision_next",
            any(row["result"] == "NEXT_2291_PARENT_FINITE_QUADRATIC_ROW_AND_SOURCE_TEST_BETA_SPLIT" for row in decision_rows_local)
            and any(row["next_target"] == "2291-Y5-R2FR-parent-finite-quadratic-row-and-source-test-beta-split.md" for row in next_rows),
            "decision selects parent finite quadratic row and source/test beta split next",
        ),
        ("VAL2290_13_csv_parse", all(csv_parses(path) for path in all_generated_before_validation), "all generated 2290 CSVs parse before validation file"),
        ("VAL2290_14_no_claim_flags", generated_claim_flags_false(all_generated_before_validation), "all generated prediction/claim flags remain false"),
        ("VAL2290_15_branch_copies", all(row["target_exists"] and row["target_parses"] for row in branch_copy_rows), "branch/queue copies exist and parse"),
        ("VAL2290_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL2290_17_formalization_no_2290", not formalization_has_2290_artifacts(), "formalization-workbench has no non-venv 2290 artifacts"),
        ("VAL2290_18_formalization_untouched", not formalization_touched_since_start(), "formalization-workbench untouched during 2290 run"),
    ]
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]
    overall_pass = all(row["result"] == "PASS" for row in rows)
    rows.append(
        {
            "check_id": "VAL2290_OVERALL",
            "result": "PASS" if overall_pass else "FAIL",
            "detail": "2290 localizes external R10 metadata, refuses first internal Zq/tau_R10 row, refines the source/test product law, and selects finite quadratic row plus beta split next",
        }
    )
    return rows


def write_markdown(
    sources: list[dict[str, Any]],
    source_audit: list[dict[str, Any]],
    zq_attempt: list[dict[str, Any]],
    tau_attempt: list[dict[str, Any]],
    kernel_contract: list[dict[str, Any]],
    external_metadata: list[dict[str, Any]],
    internal_status: list[dict[str, Any]],
    join_readiness: list[dict[str, Any]],
    projection_template: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    claim_gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    branch_copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    content = f"""# 2290 - Y5/R2FR First Internal Zq or tau_R10 Projection Row

## Verdict

2290 does not fill a scoreable internal row yet, but it does tighten the rules for what a real row must be.

`Z_q` still has no theorem-zero and no source-backed finite coefficient. `tau_R10` is also not a free dial: it is a source/test Yukawa product bridge. The scoreable form must look like `alpha_R10(lambda)=K_q^R10(lambda) beta_source(lambda) beta_test(lambda)+epsilon_tail(lambda)`, not a one-leg linear `c_g` shortcut.

The external R10 metadata is localized under the 2290 path, but it is still only metadata: no digitized `alpha(lambda)` curve, no MTS-side `Z_q/M_q^2/j_q/B_R`, and no accepted projection kernel. Therefore no R10/local-GR claim is made.

## Source Register
{table(["source_id", "source_key", "source_path", "exists", "needles_present", "role", "valid_for_claim"], sources)}

## Local Source Audit
{table(["audit_id", "source_path", "source_exists", "anchor", "anchor_found", "source_role", "not_sufficient_for", "valid_for_claim"], source_audit)}

## Zq Theorem Or Coefficient Attempt
{table(["attempt_id", "target", "required_input", "status", "reason", "score_ready", "valid_for_claim"], zq_attempt)}

## tau_R10 Projection Attempt
{table(["projection_id", "projection_piece", "role", "status", "blocking_gap", "score_ready", "valid_for_claim"], tau_attempt)}

## Source/Test Kernel Contract
{table(["contract_id", "piece", "conditional_law", "status", "missing_input", "why_it_matters", "valid_for_claim"], kernel_contract)}

## External R10 Bound Metadata Row
{table(["row_id", "row_type", "arena", "quantity", "source_path", "doi", "metadata_status", "bound_curve_status", "why_not_scoreable", "source_backed", "score_ready", "valid_for_claim"], external_metadata)}

## First Internal Row Status
{table(["status_id", "target", "current_evidence", "status", "ready_for_raw", "ready_for_accepted", "score_ready", "valid_for_claim"], internal_status)}

## Internal Join Readiness
{table(["join_id", "target", "role", "status", "ready_for_raw", "ready_for_accepted", "blocking_reason", "valid_for_claim"], join_readiness)}

## Projection Template
{table(["row_id", "coefficient_symbol", "coefficient_value", "coefficient_units", "normalization_convention", "parent_action_block", "source_path", "source_anchor", "arena_projection", "placeholder_status", "valid_for_claim"], projection_template)}

## Runner
{table(["runner_id", "test", "current_status", "detail", "score_ready", "valid_for_claim"], runner)}

## Claim Gates
{table(["gate_id", "claim_gate", "status", "reason", "valid_for_claim", "claim_allowed"], claim_gates)}

## Decision Ledger
{table(["decision_id", "decision", "result", "reason", "next_action", "valid_for_claim"], decisions)}

## Next Target
{table(["next_id", "next_target", "script", "objective", "do_not", "valid_for_claim"], next_target)}

## Branch Copies
{table(["copy_id", "source_path", "target_path", "target_exists", "target_parses", "reason"], branch_copies)}

## Validation
{table(["check_id", "result", "detail"], validation)}

## Working Interpretation

This is a good ugly result. We still do not have the internal coefficient, but we have killed a dangerous shortcut: R10 is a two-body source/test exchange, so coupling strength is generally product-like. Before we spend time digitizing external curves, the theory side needs a finite quadratic q-row and a beta_source/beta_test split. That is the next clean target.
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    remove_pycache()
    localize_external_metadata()

    sources = source_register_rows()
    source_audit = local_source_audit_rows()
    zq_attempt = zq_attempt_rows()
    tau_attempt = tau_attempt_rows()
    kernel_contract = kernel_contract_rows()
    external_metadata = external_metadata_rows()
    internal_status = first_internal_status_rows()
    join_readiness = join_readiness_rows()
    projection_template = projection_template_rows()
    runner = runner_rows()
    claim_gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["local_source_audit"], source_audit)
    write_csv(OUTPUTS["zq_attempt"], zq_attempt)
    write_csv(OUTPUTS["tau_attempt"], tau_attempt)
    write_csv(OUTPUTS["kernel_contract"], kernel_contract)
    write_csv(OUTPUTS["external_metadata"], external_metadata)
    write_csv(OUTPUTS["internal_status"], internal_status)
    write_csv(OUTPUTS["join_readiness"], join_readiness)
    write_csv(OUTPUTS["projection_template"], projection_template)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["claim_gates"], claim_gates)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next_target"], next_target)

    branch_copies = copy_branch_files()
    write_csv(OUTPUTS["branch_copies"], branch_copies)

    generated_before_validation = [
        OUTPUTS["source_register"],
        OUTPUTS["local_source_audit"],
        OUTPUTS["zq_attempt"],
        OUTPUTS["tau_attempt"],
        OUTPUTS["kernel_contract"],
        OUTPUTS["external_metadata"],
        OUTPUTS["internal_status"],
        OUTPUTS["join_readiness"],
        OUTPUTS["projection_template"],
        OUTPUTS["runner"],
        OUTPUTS["claim_gates"],
        OUTPUTS["decision"],
        OUTPUTS["next_target"],
        OUTPUTS["branch_copies"],
    ]
    remove_pycache()
    validation = validation_rows(generated_before_validation, branch_copies, projection_template)
    write_csv(OUTPUTS["validation"], validation)
    write_markdown(
        sources,
        source_audit,
        zq_attempt,
        tau_attempt,
        kernel_contract,
        external_metadata,
        internal_status,
        join_readiness,
        projection_template,
        runner,
        claim_gates,
        decisions,
        next_target,
        branch_copies,
        validation,
    )
    remove_pycache()

    failed = [row for row in validation if row["result"] != "PASS"]
    if failed:
        failed_ids = ", ".join(row["check_id"] for row in failed)
        raise SystemExit(f"2290 validation failed: {failed_ids}")
    print(f"Wrote {DOC}")
    print(f"Wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
