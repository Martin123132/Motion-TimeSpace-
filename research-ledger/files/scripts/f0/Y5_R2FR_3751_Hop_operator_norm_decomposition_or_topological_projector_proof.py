from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3751"
BRANCH = "MTS_R2FR_Y5_HOP_OPERATOR_NORM_DECOMPOSITION_OR_TOPOLOGICAL_PROJECTOR_PROOF_3751"
PCW = Path(__file__).resolve().parents[1]
RESIDUALS = PCW / "source-intake" / "mts_residuals"
FORMALIZATION = PCW.parent / "formalization-workbench"
DOC_PATH = PCW / "3751-Y5-R2FR-Hop-operator-norm-decomposition-or-topological-projector-proof.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(timestamp: str) -> dict[str, object]:
    return {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH,
        "checkpoint_id": CHECKPOINT,
        "valid_for_claim": False,
    }


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def source_paths() -> dict[str, Path]:
    return {
        "SRC3751_0_3750_cap": RESIDUALS / "P8_Y5_R2FR_3750_HIDDEN_OPERATOR_NORM_CAPS.csv",
        "SRC3751_1_3750_contract": RESIDUALS / "P8_Y5_R2FR_3750_BOUND_CONTRACT_ROWS.csv",
        "SRC3751_2_3748_formula": RESIDUALS / "P8_Y5_R2FR_3748_PROJECTOR_LEAK_BOUND_FORMULAS.csv",
        "SRC3751_3_3749_results": RESIDUALS / "P8_Y5_R2FR_3749_FERMI_DOMAIN_RESULTS.csv",
        "SRC3751_4_3747_zero_theorem": RESIDUALS / "P8_Y5_R2FR_3747_PARALLEL_PROJECTOR_ZERO_THEOREM.csv",
        "SRC3751_5_3572_naturality": RESIDUALS / "P8_Y5_R2FR_3572_PROJECTOR_NATURALITY_PROOF.csv",
        "SRC3751_6_3572_kprojector": RESIDUALS / "P8_Y5_R2FR_3572_KPROJECTOR_OPERATOR_NORM_ROWS.csv",
        "SRC3751_7_3498_naturality": RESIDUALS / "P8_Y5_R2FR_3498_PROJECTOR_NATURALITY_THEOREM.csv",
        "SRC3751_8_3431_domain_bound": RESIDUALS / "P8_Y5_R2FR_3431_DOMAIN_PROJECTOR_OPERATOR_BOUND_PACK.csv",
        "SRC3751_9_3492_ppn_products": RESIDUALS / "P8_Y5_R2FR_3492_PPN_PRODUCT_BOUNDS.csv",
    }


def source_register(timestamp: str) -> list[dict[str, object]]:
    purposes = {
        "SRC3751_0_3750_cap": "imports global H_op cap from worst 3749 smoke scenario",
        "SRC3751_1_3750_contract": "imports H_op factor definition",
        "SRC3751_2_3748_formula": "imports projector leak factor formulas",
        "SRC3751_3_3749_results": "imports Fermi-domain smoke epsilon rows",
        "SRC3751_4_3747_zero_theorem": "imports parent parallel projector zero route",
        "SRC3751_5_3572_naturality": "imports q/e_obs/tau Gamma-naturality result",
        "SRC3751_6_3572_kprojector": "imports operator norm rows still missing values",
        "SRC3751_7_3498_naturality": "imports topological projector conditional route",
        "SRC3751_8_3431_domain_bound": "imports domain-projector metric/boundary stress split",
        "SRC3751_9_3492_ppn_products": "imports PPN product-bound templates",
    }
    return [
        {
            **base(timestamp),
            "source_id": source_id,
            "source_path": str(path),
            "purpose": purposes[source_id],
            "exists": path.exists(),
            "claim_allowed": False,
        }
        for source_id, path in source_paths().items()
    ]


def global_cap() -> float:
    caps = read_csv(source_paths()["SRC3751_0_3750_cap"])
    global_rows = [row for row in caps if row.get("cap_id") == "CAP3750_GLOBAL_MIN"]
    if not global_rows:
        raise RuntimeError("CAP3750_GLOBAL_MIN missing")
    return float(global_rows[0]["H_op_max_to_pass_placeholder_tol"])


def decomposition_rows(timestamp: str, cap: float) -> list[dict[str, object]]:
    rows = [
        (
            "HOP3751_0_product",
            "H_op",
            "C_pair * ||E_M^nabla||_D * ||deltaPhi_L||_D * PPN_response_norm",
            "whole hidden gain multiplying the 3749 unit-norm Fermi leakage",
            "DEFINED_CAP_TARGET",
            f"must be <= {cap:.12e} for every 3749 smoke scenario",
            "P8_Y5_R2FR_3750_BOUND_CONTRACT_ROWS.csv",
        ),
        (
            "HOP3751_1_pairing",
            "C_pair",
            "dual pairing/normalization constant taking source leakage into residual units",
            "finite by construction only after parent inner product and source norm are fixed",
            "FINITE_BOUND_MISSING",
            "derive from parent bilinear form or set by explicit normalization convention",
            "P8_Y5_R2FR_3748_PROJECTOR_LEAK_BOUND_FORMULAS.csv",
        ),
        (
            "HOP3751_2_memory_norm",
            "||E_M^nabla||_D",
            "norm of the memory/projector current response over the local Fermi domain",
            "zero/contractive only if parent projector is topological/orthogonal and connection-preserved",
            "ZERO_OR_CONTRACTION_UNSIGNED",
            "prove ||P_M||<=1 plus block-diagonal connection, or source a finite operator norm",
            "P8_Y5_R2FR_3572_KPROJECTOR_OPERATOR_NORM_ROWS.csv",
        ),
        (
            "HOP3751_3_variation_norm",
            "||deltaPhi_L||_D",
            "size of the local variation used to define the residual operator",
            "can be one only after the test is explicitly written as a unit Frechet/operator norm",
            "NORMALIZATION_ROUTE_UNSIGNED",
            "turn local PPN residual into a unit-variation operator norm, not an arbitrary field amplitude",
            "P8_Y5_R2FR_3750_BOUND_CONTRACT_ROWS.csv",
        ),
        (
            "HOP3751_4_ppn_response",
            "PPN_response_norm",
            "map from normalized leakage scalar/vector into gamma, beta, Newton, WEP, clock, and orbital residuals",
            "schemas and product bounds exist; source-backed response coefficients are still missing",
            "RESPONSE_KERNEL_MISSING",
            "fill K_gamma, K_beta, K_Newton, K_WEP, K_clock, K_orbital or prove silence",
            "P8_Y5_R2FR_3492_PPN_PRODUCT_BOUNDS.csv",
        ),
        (
            "HOP3751_5_gamma_natural_projector",
            "delta_Gamma_ind Pi_M",
            "independent-connection variation of the memory projector",
            "3572 gives an exact zero inside the q/e_obs/tau-natural LC branch",
            "PARTIAL_ZERO_AVAILABLE",
            "usable only for Gamma-source hypermomentum; does not close metric stress or PPN",
            "P8_Y5_R2FR_3572_PROJECTOR_NATURALITY_PROOF.csv",
        ),
        (
            "HOP3751_6_metric_projector_stress",
            "delta_g Pi_M",
            "metric/coframe/domain variation of the memory projector",
            "not killed by Gamma-naturality; must be topological, orthogonal-contractive, or bounded",
            "ACTIVE_LOCAL_GR_GAP",
            "this is the current hard local-GR gap",
            "P8_Y5_R2FR_3431_DOMAIN_PROJECTOR_OPERATOR_BOUND_PACK.csv",
        ),
        (
            "HOP3751_7_boundary_transition",
            "epsilon_boundary + epsilon_transition",
            "domain boundary flux and finite transition-width leakage",
            "not included as a proven zero in 3750 cap; absolute no-cancellation policy keeps it live",
            "ACTIVE_CLOSURE_GAP",
            "prove no-flux/fixed topology or include as separate bound row",
            "P8_Y5_R2FR_3748_PROJECTOR_LEAK_BOUND_FORMULAS.csv",
        ),
    ]
    return [
        {
            **base(timestamp),
            "factor_id": factor_id,
            "symbol": symbol,
            "definition": definition,
            "current_read": current_read,
            "status": status,
            "next_derivation_or_bound": next_step,
            "source_file": str(RESIDUALS / source_file),
            "claim_allowed": False,
        }
        for factor_id, symbol, definition, current_read, status, next_step, source_file in rows
    ]


def cap_allocation_rows(timestamp: str, cap: float) -> list[dict[str, object]]:
    assumptions = [
        ("ALLOC3751_0_unit_factors", 1.0, 1.0, 1.0, "if C_pair, memory norm, and variation norm are unit/contractive"),
        ("ALLOC3751_1_ten_each", 10.0, 10.0, 10.0, "if the three non-response factors each cost one order of magnitude"),
        ("ALLOC3751_2_thousand_each", 1.0e3, 1.0e3, 1.0e3, "if each non-response factor is large but finite at 1e3"),
        ("ALLOC3751_3_million_pair_only", 1.0e6, 1.0, 1.0, "if source pairing alone is a million-scale conversion"),
        ("ALLOC3751_4_million_memory_only", 1.0, 1.0e6, 1.0, "if memory-current operator norm alone is million-scale"),
    ]
    rows: list[dict[str, object]] = []
    for allocation_id, c_pair, e_norm, variation_norm, assumption in assumptions:
        divisor = c_pair * e_norm * variation_norm
        rows.append(
            {
                **base(timestamp),
                "allocation_id": allocation_id,
                "C_pair_assumed": f"{c_pair:.12e}",
                "E_M_nabla_norm_assumed": f"{e_norm:.12e}",
                "deltaPhi_L_norm_assumed": f"{variation_norm:.12e}",
                "PPN_response_norm_max": f"{cap / divisor:.12e}",
                "assumption": assumption,
                "interpretation": "large remaining headroom" if cap / divisor >= 1.0e3 else "tight headroom",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def sensitivity_rows(timestamp: str, cap: float) -> list[dict[str, object]]:
    bundles = [
        ("BUNDLE3751_0_unit", 1.0, 1.0, 1.0, 1.0),
        ("BUNDLE3751_1_conservative", 10.0, 10.0, 10.0, 1.0e3),
        ("BUNDLE3751_2_large_response", 1.0, 1.0, 1.0, 1.0e12),
        ("BUNDLE3751_3_cap_edge", 1.0, 1.0, 1.0, cap),
        ("BUNDLE3751_4_first_fail", 1.0, 1.0, 1.0, 1.0e13),
    ]
    rows: list[dict[str, object]] = []
    for bundle_id, c_pair, e_norm, variation_norm, response_norm in bundles:
        product = c_pair * e_norm * variation_norm * response_norm
        fraction = product / cap
        rows.append(
            {
                **base(timestamp),
                "bundle_id": bundle_id,
                "C_pair": f"{c_pair:.12e}",
                "E_M_nabla_norm": f"{e_norm:.12e}",
                "deltaPhi_L_norm": f"{variation_norm:.12e}",
                "PPN_response_norm": f"{response_norm:.12e}",
                "H_op_product": f"{product:.12e}",
                "fraction_of_3750_cap": f"{fraction:.12e}",
                "passes_3750_placeholder_cap": product <= cap * (1.0 + 1.0e-12),
                "interpretation": "passes nonclaim smoke cap" if product <= cap * (1.0 + 1.0e-12) else "fails nonclaim smoke cap",
                "claim_allowed": False,
            }
        )
    return rows


def zero_route_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "ZR3751_0_parent_split",
            "E = E_L direct-sum E_M is parent-owned, not a fitted readout partition",
            "P_M P_L=0 structurally",
            "3747/3748",
            "UNSIGNED_PARENT_ASSUMPTION",
        ),
        (
            "ZR3751_1_parallel_connection",
            "parent connection preserves E_L and E_M so A_ML=A_LM=0",
            "[nabla,P_M]P_L deltaPhi=0",
            "3747/3748",
            "UNSIGNED_HARD_CLAUSE",
        ),
        (
            "ZR3751_2_q_eobs_tau_naturality",
            "Pi_M has only q/e_obs/tau/H_ref/topology slots and no Gamma_ind slot",
            "delta_Gamma_ind Pi_M=0 by chain rule",
            "3498/3572",
            "EXACT_INSIDE_BRANCH_NOT_FULL_PPN",
        ),
        (
            "ZR3751_3_topological_or_orthogonal_projector",
            "Pi_M is metric-independent topological or orthogonal contractive in the parent norm",
            "delta_g Pi_M=0 or ||Pi_M||<=1 without fit freedom",
            "3498/3572/3431",
            "BEST_DERIVATION_ROUTE_UNSIGNED",
        ),
        (
            "ZR3751_4_boundary_silence",
            "fixed relative chain/no-flux boundary and no transition collar tuned by local fields",
            "epsilon_boundary=epsilon_transition=0",
            "3431/3748",
            "MISSING_BOUNDARY_THEOREM",
        ),
        (
            "ZR3751_5_verdict",
            "all zero clauses signed together",
            "H_op becomes irrelevant for the projector leak branch",
            "3751 synthesis",
            "NOT_CLAIMED_ROUTE_IDENTIFIED",
        ),
    ]
    return [
        {
            **base(timestamp),
            "clause_id": clause_id,
            "condition": condition,
            "result_if_signed": result,
            "source_anchor": anchor,
            "status": status,
            "claim_allowed": False,
        }
        for clause_id, condition, result, anchor, status in rows
    ]


def claim_gates(timestamp: str, source_rows: list[dict[str, object]], factor_rows: list[dict[str, object]], sensitivity: list[dict[str, object]]) -> list[dict[str, object]]:
    all_sources_exist = all(str(row["exists"]) == "True" or row["exists"] is True for row in source_rows)
    factor_status_text = " ".join(str(row["status"]) for row in factor_rows)
    pass_unit = any(row["bundle_id"] == "BUNDLE3751_0_unit" and str(row["passes_3750_placeholder_cap"]) == "True" for row in sensitivity)
    fail_first = any(row["bundle_id"] == "BUNDLE3751_4_first_fail" and str(row["passes_3750_placeholder_cap"]) == "False" for row in sensitivity)
    gates = [
        ("CG3751_0_sources", "all 3751 cited local source paths exist", all_sources_exist, "path hygiene"),
        ("CG3751_1_decomposition", "H_op decomposed into named factor lanes", len(factor_rows) == 8, "not a black box now"),
        ("CG3751_2_cap_allocation", "global 3750 cap imported and allocated", True, "cap is numeric but nonclaim"),
        ("CG3751_3_sensitivity", "unit bundle passes and 1e13 bundle fails", pass_unit and fail_first, "brackets useful factor scale"),
        ("CG3751_4_parent_zero", "full topological/parallel zero proof achieved", False, "clauses remain unsigned"),
        ("CG3751_5_source_backed_factors", "all H_op factors source-backed", "MISSING" not in factor_status_text and "UNSIGNED" not in factor_status_text, "intentionally expected false"),
        ("CG3751_6_local_claim", "local GR/Newton/PPN pass claim allowed", False, "no local claim from 3751"),
    ]
    return [
        {
            **base(timestamp),
            "gate_id": gate_id,
            "gate": gate,
            "passed": passed,
            "details": details,
            "claim_allowed": False,
        }
        for gate_id, gate, passed, details in gates
    ]


def decision_rows(timestamp: str, cap: float) -> list[dict[str, object]]:
    rows = [
        (
            "DEC3751_0_result",
            "H_OP_DECOMPOSED_NOT_CLAIMED",
            f"3751 turns the hidden product into factor lanes and keeps the cap H_op <= {cap:.12e}.",
        ),
        (
            "DEC3751_1_real_progress",
            "GAMMA_PROJECTOR_ZERO_SEPARATED_FROM_METRIC_STRESS",
            "The q/e_obs/tau branch can kill delta_Gamma_ind Pi_M, but metric projector stress remains the local-GR gap.",
        ),
        (
            "DEC3751_2_best_route",
            "PROVE_ORTHOGONAL_TOPOLOGICAL_PROJECTOR_CONTRACTION",
            "The least-scrutiny route is theorem-first: make Pi_M parent-owned, topological/orthogonal, and contractive so the large cap does not need a fitted operator.",
        ),
        (
            "DEC3751_3_bound_route",
            "BOUND_REMAINING_RESPONSE_KERNEL",
            "If zero proof stalls, source K_gamma, K_beta, K_Newton, WEP, clock, and orbital response coefficients as an absolute vector.",
        ),
    ]
    return [
        {
            **base(timestamp),
            "decision_id": decision_id,
            "decision": decision,
            "meaning": meaning,
            "claim_allowed": False,
        }
        for decision_id, decision, meaning in rows
    ]


def next_target_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "next_id": "NEXT3751_0",
            "target_doc": "3752-Y5-R2FR-orthogonal-topological-projector-contraction-proof.md",
            "target_script": "scripts/Y5_R2FR_3752_orthogonal_topological_projector_contraction_proof.py",
            "objective": "prove ||Pi_M||<=1 and delta_g Pi_M=0 from a parent-owned topological/orthogonal projector, or fall back to explicit metric-stress operator bounds",
            "why_this_next": "this attacks the actual active local-GR gap rather than repeating the broad missing-coupling complaint",
            "claim_allowed": False,
        }
    ]


def status_rows(timestamp: str, cap: float) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "status_id": "STATUS3751_0",
            "status": "HOP_DECOMPOSED_TO_FACTOR_LANES_PARENT_TOPOLOGICAL_ROUTE_IDENTIFIED",
            "summary": f"3751 decomposes H_op and shows the clean route is not another fit: prove a parent-owned topological/orthogonal projector contraction, while the fallback requires finite response-kernel bounds below {cap:.12e}.",
            "claim_allowed": False,
        }
    ]


def validation_rows(timestamp: str, paths: dict[str, Path], grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    checks = [
        ("source_paths", "every 3751 source path exists", all(Path(str(row["source_path"])).exists() for row in grouped["source_register"])),
        ("csv_parse", "all generated CSV outputs parse", all(len(read_csv(path)) > 0 for key, path in paths.items() if key not in {"doc", "validation"})),
        ("global_cap", "global cap is positive finite", math.isfinite(global_cap()) and global_cap() > 0),
        ("factor_count", "decomposition has eight factor rows", len(grouped["factors"]) == 8),
        ("active_gap", "metric projector stress remains active", any(row["factor_id"] == "HOP3751_6_metric_projector_stress" and row["status"] == "ACTIVE_LOCAL_GR_GAP" for row in grouped["factors"])),
        ("zero_route_nonclaim", "zero route verdict remains not claimed", any(row["clause_id"] == "ZR3751_5_verdict" and row["status"] == "NOT_CLAIMED_ROUTE_IDENTIFIED" for row in grouped["zero_route"])),
        ("allocation_rows", "cap allocation rows emitted", len(grouped["allocations"]) == 5),
        ("sensitivity_bracket", "unit bundle passes and first-fail bundle fails", any(row["bundle_id"] == "BUNDLE3751_0_unit" and row["passes_3750_placeholder_cap"] is True for row in grouped["sensitivity"]) and any(row["bundle_id"] == "BUNDLE3751_4_first_fail" and row["passes_3750_placeholder_cap"] is False for row in grouped["sensitivity"])),
        ("claim_gates_block", "local claim gate is blocked", any(row["gate_id"] == "CG3751_6_local_claim" and row["passed"] is False for row in grouped["claim_gates"])),
        ("no_formalization_leak", "no 3751 files written to formalization-workbench", not FORMALIZATION.exists() or not list(FORMALIZATION.rglob("*3751*"))),
    ]
    return [
        {
            **base(timestamp),
            "validation_id": validation_id,
            "description": description,
            "result": "PASS" if passed else "FAIL",
            "details": "",
        }
        for validation_id, description, passed in checks
    ]


def render_doc(grouped: dict[str, list[dict[str, object]]], cap: float) -> str:
    lines = [
        "# 3751 — H_op Operator-Norm Decomposition Or Topological Projector Proof",
        "",
        "## Status",
        "",
        "`HOP_DECOMPOSED_TO_FACTOR_LANES_PARENT_TOPOLOGICAL_ROUTE_IDENTIFIED`.",
        "",
        "This checkpoint does not claim local GR/Newton/PPN closure. It does the thing that was missing from 3750: it stops treating the hidden operator as one foggy monster and splits it into proof/bound lanes.",
        "",
        "## Core Result",
        "",
        f"- Imported 3750 global nonclaim cap: `H_op <= {cap:.12e}`.",
        "- Decomposition: `H_op = C_pair * ||E_M^nabla||_D * ||deltaPhi_L||_D * PPN_response_norm`.",
        "- `delta_Gamma_ind Pi_M = 0` is available inside the q/e_obs/tau-natural LC branch, but this is not full metric-stress silence.",
        "- The hard local-GR gap is now sharper: `delta_g Pi_M`, boundary flux, transition collars, and the PPN response vector.",
        "",
        "## Factor Lanes",
    ]
    for row in grouped["factors"]:
        lines.append(f"- `{row['factor_id']}` `{row['status']}`: `{row['symbol']}` — {row['next_derivation_or_bound']}")
    lines.extend(["", "## Cap Allocation"])
    for row in grouped["allocations"]:
        lines.append(
            f"- `{row['allocation_id']}` gives `PPN_response_norm_max={row['PPN_response_norm_max']}` under {row['assumption']}."
        )
    lines.extend(["", "## Sensitivity Bundles"])
    for row in grouped["sensitivity"]:
        lines.append(
            f"- `{row['bundle_id']}` `H_op={row['H_op_product']}` fraction `{row['fraction_of_3750_cap']}` pass=`{row['passes_3750_placeholder_cap']}`."
        )
    lines.extend(["", "## Zero-Proof Route"])
    for row in grouped["zero_route"]:
        lines.append(f"- `{row['clause_id']}` `{row['status']}`: {row['condition']} -> {row['result_if_signed']}")
    lines.extend(["", "## Decision"])
    for row in grouped["decisions"]:
        lines.append(f"- `{row['decision_id']}` `{row['decision']}`: {row['meaning']}")
    lines.extend(["", "## Claim Gates"])
    for row in grouped["claim_gates"]:
        lines.append(f"- `{row['gate_id']}` pass=`{row['passed']}`: {row['gate']} — {row['details']}")
    lines.extend(["", "## Next Target"])
    for row in grouped["next_target"]:
        lines.append(f"- `{row['target_doc']}`: {row['objective']}")
    lines.extend(["", "## Source Files"])
    for row in grouped["source_register"]:
        lines.append(f"- `{row['source_id']}` exists=`{row['exists']}`: `{row['source_path']}`")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    timestamp = now()
    cap = global_cap()
    paths = {
        "doc": DOC_PATH,
        "source_register": RESIDUALS / "P8_Y5_R2FR_3751_SOURCE_REGISTER.csv",
        "factors": RESIDUALS / "P8_Y5_R2FR_3751_HOP_FACTOR_LANES.csv",
        "allocations": RESIDUALS / "P8_Y5_R2FR_3751_CAP_ALLOCATION_ROWS.csv",
        "sensitivity": RESIDUALS / "P8_Y5_R2FR_3751_FACTOR_SENSITIVITY_BUNDLES.csv",
        "zero_route": RESIDUALS / "P8_Y5_R2FR_3751_ZERO_ROUTE_CLAUSES.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3751_CLAIM_GATES.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3751_DECISION_ROWS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3751_NEXT_TARGET.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3751_STATUS.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3751_VALIDATION.csv",
    }
    grouped: dict[str, list[dict[str, object]]] = {}
    grouped["source_register"] = source_register(timestamp)
    grouped["factors"] = decomposition_rows(timestamp, cap)
    grouped["allocations"] = cap_allocation_rows(timestamp, cap)
    grouped["sensitivity"] = sensitivity_rows(timestamp, cap)
    grouped["zero_route"] = zero_route_rows(timestamp)
    grouped["decisions"] = decision_rows(timestamp, cap)
    grouped["next_target"] = next_target_rows(timestamp)
    grouped["status"] = status_rows(timestamp, cap)
    grouped["claim_gates"] = claim_gates(timestamp, grouped["source_register"], grouped["factors"], grouped["sensitivity"])
    for key, rows in grouped.items():
        write_csv(paths[key], rows)
    DOC_PATH.write_text(render_doc(grouped, cap), encoding="utf-8")
    grouped["validation"] = validation_rows(timestamp, paths, grouped)
    write_csv(paths["validation"], grouped["validation"])
    failures = [row for row in grouped["validation"] if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3751 validation failed: {failures}")
    cache = Path(__file__).resolve().parent / "__pycache__"
    if cache.exists() and str(cache.resolve()).startswith(str(PCW.resolve())):
        shutil.rmtree(cache)
    print("wrote 3751 checkpoint: H_op decomposed; topological/orthogonal projector route identified")


if __name__ == "__main__":
    main()
