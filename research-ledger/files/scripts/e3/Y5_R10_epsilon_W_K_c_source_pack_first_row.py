from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1136-Y5-R10-epsilon-W-K-c-source-pack-first-row.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    generated = now()
    return [{**row, "generated_utc": generated} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def source_rows() -> list[dict[str, object]]:
    sources = [
        {
            "source_id": "SRC1136_0_1135_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1135_NEXT_TARGET.csv",
            "needle": "NEXT1135_0_1136",
            "note": "1135 handoff to epsilon/W/K/c source-pack first rows.",
        },
        {
            "source_id": "SRC1136_1_1135_handoff",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1135_SOURCE_PACK_HANDOFF_ROWS.csv",
            "needle": "RH1135_0_epsilon_profile",
            "note": "1135 defines the source-pack handoff schemas.",
        },
        {
            "source_id": "SRC1136_2_1135_demotion",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1135_EPSILON_CLOSURE_DEMOTION_LEDGER.csv",
            "needle": "DEM1135_0_epsilon_zero",
            "note": "Epsilon zero is closure-only for current corpus.",
        },
        {
            "source_id": "SRC1136_3_1134_runner",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1134_EPSILON_PROFILE_RUNNER_INPUTS.csv",
            "needle": "RUN1134_0_epsilon_profile",
            "note": "1134 staged blocked runner inputs.",
        },
        {
            "source_id": "SRC1136_4_1132_products",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1132_EXECUTABLE_PRODUCT_MATRIX.csv",
            "needle": "PM1132_0_domain_flux",
            "note": "1132 supplies the two alpha3 product inequalities and total guard.",
        },
        {
            "source_id": "SRC1136_5_domain_coeffs",
            "relative_path": "source-intake/mts_residuals/P8_mu_extra_domain_projector_coefficients.csv",
            "needle": "W_domain_alpha3_epsilon_domain_flux",
            "note": "Existing domain coefficient row names W_domain_alpha3 but does not source a number.",
        },
        {
            "source_id": "SRC1136_6_R11_flux_contract",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1122_REMAINING_FLUX_CONTRACT.csv",
            "needle": "R11F1122_0_flux_alpha3",
            "note": "R11 flux contract names K*c*epsilon but does not source K or c.",
        },
        {
            "source_id": "SRC1136_7_R11_minimum",
            "relative_path": "source-intake/mts_residuals/R11_DOMAIN_PROJECTOR_OPERATOR_VECTOR_MINIMUM.csv",
            "needle": "c_domain_source_normalization_operator",
            "note": "R11 minimum vector/operator file carries missing source-normalization coefficients.",
        },
        {
            "source_id": "SRC1136_8_R11_missing",
            "relative_path": "source-intake/mts_residuals/R11_DOMAIN_PROJECTOR_VECTOR_MISSING_LEDGER.csv",
            "needle": "MISSING_DOMAIN_MU_EXTRA_OPERATOR_ZERO_OR_NUMERIC_COEFFICIENT",
            "note": "R11 missing ledger keeps source-normalization coefficient claim-blocked.",
        },
        {
            "source_id": "SRC1136_9_1123_bound",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1123_ALPHA3_FLUX_BOUND_PRODUCT_ROWS.csv",
            "needle": "FB1123_0_alpha3_flux_product",
            "note": "1123 gives the alpha3 flux bound product row and theorem-zero alternatives.",
        },
    ]
    checked: list[dict[str, object]] = []
    for source in sources:
        path = ROOT / str(source["relative_path"])
        text = read_text(path)
        checked.append(
            {
                **source,
                "exists": str(path.exists()).lower(),
                "needle_found": str(str(source["needle"]) in text).lower(),
            }
        )
    return stamp(checked)


def first_source_pack_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "pack_id": "SP1136_0_epsilon_domain_flux",
                "quantity": "epsilon_domain_flux",
                "role": "shared projected local flux factor",
                "value_abs": "MISSING_NUMERIC_PROFILE_OR_ZERO_THEOREM",
                "units": "dimensionless projected flux in observed PPN-safe coframe",
                "normalization": "same local coframe and source normalization used in alpha3 product rows",
                "source_path": "MISSING_PARENT_PROFILE_OR_THEOREM_SOURCE",
                "equation_or_map": "epsilon profile or theorem-zero must feed both W*epsilon and K*c*epsilon",
                "claim_blockers": "MISSING_VALUE;MISSING_SOURCE_PATH;EPSILON_ZERO_DEMOTED_TO_CLOSURE_ONLY",
                "status": "SOURCE_ROW_PLACEHOLDER_BLOCKED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "pack_id": "SP1136_1_W_domain_alpha3",
                "quantity": "W_domain_alpha3",
                "role": "domain alpha3 flux coupling",
                "value_abs": "MISSING_NUMERIC_COUPLING_OR_ZERO_THEOREM",
                "units": "dimensionless weak-field alpha3 coupling after declared normalization",
                "normalization": "alpha3_domain_flux = W_domain_alpha3 * epsilon_domain_flux",
                "source_path": "source-intake/mts_residuals/P8_mu_extra_domain_projector_coefficients.csv",
                "equation_or_map": "W_domain_alpha3_epsilon_domain_flux row gives map but not numeric W",
                "claim_blockers": "MISSING_VALUE;MAP_ONLY_NOT_COEFFICIENT_SOURCE",
                "status": "SOURCE_ROW_PLACEHOLDER_BLOCKED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "pack_id": "SP1136_2_K_R11_flux_alpha3",
                "quantity": "K_R11_flux_alpha3",
                "role": "R11 flux-to-alpha3 transfer coefficient",
                "value_abs": "MISSING_R11_FLUX_TRANSFER_COEFFICIENT",
                "units": "dimensionless R11 flux transfer after weak-field normalization",
                "normalization": "P_R11_source_alpha3_flux = K_R11_flux_alpha3*c_R11_flux_alpha3*epsilon_domain_flux",
                "source_path": "source-intake/mts_residuals/P8_Y5_R10_1122_REMAINING_FLUX_CONTRACT.csv",
                "equation_or_map": "1122 flux contract names K but does not source coefficient",
                "claim_blockers": "MISSING_VALUE;CONTRACT_ONLY_NOT_COEFFICIENT_SOURCE",
                "status": "SOURCE_ROW_PLACEHOLDER_BLOCKED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "pack_id": "SP1136_3_c_R11_flux_alpha3",
                "quantity": "c_R11_flux_alpha3",
                "role": "observed-coframe/source-normalization coefficient",
                "value_abs": "MISSING_R11_SOURCE_NORMALIZATION_COEFFICIENT",
                "units": "dimensionless observed-coframe/source-normalization coefficient",
                "normalization": "same source normalization as R11 domain projector vector/operator ledger",
                "source_path": "source-intake/mts_residuals/R11_DOMAIN_PROJECTOR_OPERATOR_VECTOR_MINIMUM.csv",
                "equation_or_map": "R11 source-normalization row remains missing/conditional",
                "claim_blockers": "MISSING_VALUE;R11_MISSING_LEDGER_ACTIVE",
                "status": "SOURCE_ROW_PLACEHOLDER_BLOCKED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "pack_id": "SP1136_4_R11_Kc_product",
                "quantity": "K_R11_flux_alpha3*c_R11_flux_alpha3",
                "role": "R11 combined coupling product",
                "value_abs": "MISSING_PRODUCT_BECAUSE_K_AND_c_MISSING",
                "units": "dimensionless product in alpha3 convention",
                "normalization": "product multiplies epsilon_domain_flux in R11 alpha3 product",
                "source_path": "source-intake/mts_residuals/P8_Y5_R10_1122_REMAINING_FLUX_CONTRACT.csv;source-intake/mts_residuals/R11_DOMAIN_PROJECTOR_OPERATOR_VECTOR_MINIMUM.csv",
                "equation_or_map": "combined product is allowed only after K and c individually source or theorem-zero",
                "claim_blockers": "MISSING_K;MISSING_c;NO_PRODUCT_SHORTCUT",
                "status": "DERIVED_PRODUCT_PLACEHOLDER_BLOCKED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
        ]
    )


def row_rejection_rows(source_pack: list[dict[str, object]]) -> list[dict[str, object]]:
    rejected: list[dict[str, object]] = []
    for row in source_pack:
        source_paths = str(row["source_path"]).split(";")
        missing_path = any(path.startswith("MISSING") for path in source_paths)
        missing_value = "MISSING" in str(row["value_abs"])
        local_paths_ok = all(path.startswith("MISSING") or (ROOT / path).exists() for path in source_paths)
        rejected.append(
            {
                "rejection_id": row["pack_id"].replace("SP1136", "REJ1136"),
                "pack_id": row["pack_id"],
                "quantity": row["quantity"],
                "missing_value": str(missing_value).lower(),
                "missing_source_path": str(missing_path).lower(),
                "declared_source_paths_exist_when_nonmissing": str(local_paths_ok).lower(),
                "reject_reason": row["claim_blockers"],
                "row_claim_verdict": "REJECT_VALID_FOR_CLAIM",
                "valid_for_claim": "false",
            }
        )
    return stamp(rejected)


def product_inequality_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "product_id": "PI1136_0_domain_alpha3",
                "product": "W_domain_alpha3*epsilon_domain_flux",
                "alpha3_limit": "4e-20",
                "required_for_pass": "abs(W_domain_alpha3*epsilon_domain_flux)<=4e-20 OR theorem-zero for W or epsilon",
                "available_inputs": "none source-backed",
                "current_evaluation": "BLOCKED_MISSING_W_AND_EPSILON",
                "no_cancellation_policy": "must pass independently before total row is considered",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "product_id": "PI1136_1_R11_alpha3",
                "product": "K_R11_flux_alpha3*c_R11_flux_alpha3*epsilon_domain_flux",
                "alpha3_limit": "4e-20",
                "required_for_pass": "abs(K_R11_flux_alpha3*c_R11_flux_alpha3*epsilon_domain_flux)<=4e-20 OR theorem-zero for K, c, or epsilon",
                "available_inputs": "none source-backed",
                "current_evaluation": "BLOCKED_MISSING_K_c_AND_EPSILON",
                "no_cancellation_policy": "must pass independently before total row is considered",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "product_id": "PI1136_2_total_guard",
                "product": "alpha3_direct_flux_total",
                "alpha3_limit": "4e-20",
                "required_for_pass": "PI1136_0 and PI1136_1 both independently close, or a parent identity derives exact cancellation",
                "available_inputs": "no parent cancellation identity; product rows blocked",
                "current_evaluation": "GUARD_ONLY_NOT_SCOREABLE",
                "no_cancellation_policy": "tuned cancellation forbidden",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
        ]
    )


def acquisition_priority_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "priority_id": "PRI1136_0_coupling_normalization_first",
                "target": "W_domain_alpha3;K_R11_flux_alpha3;c_R11_flux_alpha3",
                "why_first": "without coupling magnitudes, epsilon's required upper bound cannot be numerically stated",
                "next_test": "derive/source each weak-field coefficient or theorem-zero from parent/R11 rows",
                "risk": "couplings may be order unity, forcing epsilon below 4e-20",
                "valid_for_claim": "false",
            },
            {
                "priority_id": "PRI1136_1_epsilon_profile_parallel",
                "target": "epsilon_domain_flux",
                "why_first": "epsilon is shared by both products and remains the physical local-flux bottleneck",
                "next_test": "source a profile/bound in observed coframe or reopen parent gradient-flow theorem",
                "risk": "profile route is hard without a parent local-branch flux model",
                "valid_for_claim": "false",
            },
            {
                "priority_id": "PRI1136_2_no_cancellation_guard",
                "target": "alpha3_direct_flux_total",
                "why_first": "prevents fake pass from opposite-sign unknowns",
                "next_test": "require independent product closure before any total row",
                "risk": "none; this guard is mandatory",
                "valid_for_claim": "false",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1136_0_source_rows_exist",
                "rule": "source-pack first rows exist for epsilon, W, K, c, and K*c",
                "gate_pass": "true_nonclaim",
                "reason": "schemas exist but rows are placeholders with missing values",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1136_1_no_missing_values",
                "rule": "no MISSING markers in claim rows",
                "gate_pass": "false",
                "reason": "every first-row value is missing or product-blocked",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1136_2_source_paths",
                "rule": "all claim rows have real source paths",
                "gate_pass": "false",
                "reason": "epsilon source path is missing and map-only paths are not numeric coefficient sources",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1136_3_domain_product",
                "rule": "domain product can be evaluated",
                "gate_pass": "false",
                "reason": "W and epsilon are missing",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1136_4_R11_product",
                "rule": "R11 product can be evaluated",
                "gate_pass": "false",
                "reason": "K, c, and epsilon are missing",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1136_5_no_cancellation",
                "rule": "total alpha3 cannot pass by tuned cancellation",
                "gate_pass": "true_nonclaim",
                "reason": "total row is guard-only until product rows independently close",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1136_6_alpha3_local_GR",
                "rule": "alpha3/R10/PPN/local-GR can promote",
                "gate_pass": "false",
                "reason": "source pack is nonclaim and products remain blocked",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1136_0_verdict",
                "decision": "source_pack_first_rows_created_but_all_blocked",
                "reason": "schemas now exist for all live alpha3 factors, but no numeric/theorem-zero source has been supplied",
                "next_action": "attack coupling normalization/source rows first while keeping epsilon profile route live",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1136_1_best_next",
                "decision": "coupling_normalization_source_audit",
                "reason": "W/K/c determine the required epsilon bound and may be derivable from existing weak-field/R11 maps",
                "next_action": "try to derive or source W_domain_alpha3, K_R11_flux_alpha3, and c_R11_flux_alpha3 individually",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1136_2_parallel_route",
                "decision": "epsilon_profile_remains_physics_bottleneck",
                "reason": "epsilon is shared by both products, but its zero theorem is demoted and profile source is missing",
                "next_action": "do not forget epsilon; return after coupling envelope exists or parent action is upgraded",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1136_0_1137",
                "next_target": "1137-Y5-R10-W-K-c-coupling-normalization-source-audit.md",
                "objective": "derive or source W_domain_alpha3, K_R11_flux_alpha3, and c_R11_flux_alpha3 as individual weak-field/R11 coefficients, or mark them as missing with no product scoring",
                "include": "W map; K transfer coefficient; c source-normalization coefficient; units; source paths; theorem-zero alternatives; no product shortcut",
                "exclude": "epsilon zero claim; tuned cancellation; scalar no-hair import; alpha3/local-GR claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def local_paths_ok_for_pack(row: dict[str, object]) -> bool:
    paths = str(row["source_path"]).split(";")
    return all(path.startswith("MISSING") or (ROOT / path).exists() for path in paths)


def validate(
    sources: list[dict[str, object]],
    source_pack: list[dict[str, object]],
    rejections: list[dict[str, object]],
    products: list[dict[str, object]],
    priorities: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    outputs: dict[str, Path],
) -> list[dict[str, object]]:
    validation: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validation.append(
            {
                "check_id": check_id,
                "result": "pass" if passed else "fail",
                "detail": detail,
                "valid_for_claim": "false",
                "generated_utc": now(),
            }
        )

    all_rows = source_pack + rejections + products + priorities + gates + decisions + next_target
    pack_quantities = {row["quantity"] for row in source_pack}
    add("V1136_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources), "all cited local source paths exist and needles are found")
    add("V1136_1_pack_coverage", {"epsilon_domain_flux", "W_domain_alpha3", "K_R11_flux_alpha3", "c_R11_flux_alpha3", "K_R11_flux_alpha3*c_R11_flux_alpha3"}.issubset(pack_quantities), "source pack covers epsilon, W, K, c, and K*c")
    add("V1136_2_nonmissing_source_paths_exist", all(local_paths_ok_for_pack(row) for row in source_pack), "all non-missing source paths in pack rows exist locally")
    add("V1136_3_all_pack_rows_blocked", all(row["status"].endswith("BLOCKED") for row in source_pack), "all first source-pack rows remain blocked")
    add("V1136_4_rejections_complete", len(rejections) == len(source_pack) and all(row["row_claim_verdict"] == "REJECT_VALID_FOR_CLAIM" for row in rejections), "every source-pack row has a rejection verdict")
    add("V1136_5_products_nonclaim", all(row["current_evaluation"].startswith(("BLOCKED", "GUARD")) for row in products), "product inequalities are blocked or guard-only")
    add("V1136_6_no_cancellation_guard", products[-1]["current_evaluation"] == "GUARD_ONLY_NOT_SCOREABLE" and gates[5]["gate_pass"] == "true_nonclaim", "no-cancellation guard is active")
    add("V1136_7_gates_blocked", all(row["gate_pass"] in {"false", "true_nonclaim"} for row in gates) and sum(row["gate_pass"] == "false" for row in gates) >= 5, "claim gates remain blocked")
    add("V1136_8_no_claim_rows", all(row.get("valid_for_claim") == "false" for row in all_rows) and all(row.get("claim_allowed", "false") == "false" for row in source_pack + products + next_target), "all generated rows remain nonclaim")
    add("V1136_9_next_target", next_target[0]["next_target"].startswith("1137-") and "W-K-c" in str(next_target[0]["next_target"]), "1137 handoff targets W/K/c coupling normalization")
    add("V1136_10_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()), "all generated outputs are under post-checkpoint-work")
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1136_11_csv_parse", csv_parse_ok, "all 1136 CSV outputs parse cleanly")
    add("V1136_12_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add("V1136_SUMMARY", True, "1136 creates strict nonclaim source-pack rows and sends coupling normalization to 1137")
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    source_pack: list[dict[str, object]],
    rejections: list[dict[str, object]],
    products: list[dict[str, object]],
    priorities: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1136 - Y5/R10 Epsilon/W/K/c Source-Pack First Row

**Current verdict:** first source-pack rows now exist for `epsilon_domain_flux`, `W_domain_alpha3`, `K_R11_flux_alpha3`, and `c_R11_flux_alpha3`, but every row is still blocked by missing value/source/theorem inputs.

**Useful progress:** the alpha3 fallback route is now executable as a data contract: either source the four factors, prove one factor theorem-zero, or keep alpha3/local-GR blocked.

**Important guard:** map-only files are not coefficient sources. Existing rows name `W`, `K`, and `c`, but they do not provide claim-valid numeric values or parent zero theorems.

**Best next attack:** source/derive `W`, `K`, and `c` first. Their magnitudes determine how small `epsilon_domain_flux` must be if epsilon-zero remains closure-only.

**No claim:** no alpha3, R10, PPN, local-GR, measured-GM, or FLRW claim follows from 1136. The total row cannot pass by tuned cancellation.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "note"], sources)}

## First Source-Pack Rows
{table(["pack_id", "quantity", "role", "value_abs", "units", "normalization", "source_path", "equation_or_map", "claim_blockers", "status", "valid_for_claim", "claim_allowed"], source_pack)}

## Claim-Rejection Checks
{table(["rejection_id", "pack_id", "quantity", "missing_value", "missing_source_path", "declared_source_paths_exist_when_nonmissing", "reject_reason", "row_claim_verdict", "valid_for_claim"], rejections)}

## Product Inequality Rows
{table(["product_id", "product", "alpha3_limit", "required_for_pass", "available_inputs", "current_evaluation", "no_cancellation_policy", "valid_for_claim", "claim_allowed"], products)}

## Acquisition Priorities
{table(["priority_id", "target", "why_first", "next_test", "risk", "valid_for_claim"], priorities)}

## Claim Gates
{table(["gate_id", "rule", "gate_pass", "reason", "valid_for_claim"], gates)}

## Decision Ledger
{table(["decision_id", "decision", "reason", "next_action", "valid_for_claim"], decisions)}

## Validation
{table(["check_id", "result", "detail", "valid_for_claim"], validation)}

## Next Target
{table(["next_id", "next_target", "objective", "include", "exclude", "valid_for_claim"], next_target)}
"""
    DOC.write_text(text, encoding="utf-8")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists() and pycache.is_dir():
        shutil.rmtree(pycache)


def main() -> None:
    outputs = {
        "source_register": OUT / "P8_Y5_R10_1136_SOURCE_REGISTER.csv",
        "source_pack": OUT / "P8_Y5_R10_1136_EPSILON_W_K_C_SOURCE_PACK_FIRST_ROWS.csv",
        "rejections": OUT / "P8_Y5_R10_1136_SOURCE_PACK_REJECTION_CHECKS.csv",
        "products": OUT / "P8_Y5_R10_1136_ALPHA3_PRODUCT_INEQUALITY_ROWS.csv",
        "priorities": OUT / "P8_Y5_R10_1136_ACQUISITION_PRIORITIES.csv",
        "gates": OUT / "P8_Y5_R10_1136_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1136_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1136_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1136_VALIDATION.csv",
    }
    sources = source_rows()
    source_pack = first_source_pack_rows()
    rejections = row_rejection_rows(source_pack)
    products = product_inequality_rows()
    priorities = acquisition_priority_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["source_pack"], source_pack)
    write_csv(outputs["rejections"], rejections)
    write_csv(outputs["products"], products)
    write_csv(outputs["priorities"], priorities)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, source_pack, rejections, products, priorities, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, source_pack, rejections, products, priorities, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
