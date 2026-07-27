from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3752"
BRANCH = "MTS_R2FR_Y5_ORTHOGONAL_TOPOLOGICAL_PROJECTOR_CONTRACTION_PROOF_3752"
PCW = Path(__file__).resolve().parents[1]
RESIDUALS = PCW / "source-intake" / "mts_residuals"
FORMALIZATION = PCW.parent / "formalization-workbench"
DOC_PATH = PCW / "3752-Y5-R2FR-orthogonal-topological-projector-contraction-proof.md"


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(stamp: str) -> dict[str, object]:
    return {
        "timestamp_utc": stamp,
        "branch_id": BRANCH,
        "checkpoint_id": CHECKPOINT,
        "valid_for_claim": False,
    }


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def sources() -> dict[str, Path]:
    return {
        "SRC3752_0_next": RESIDUALS / "P8_Y5_R2FR_3751_NEXT_TARGET.csv",
        "SRC3752_1_factor_lanes": RESIDUALS / "P8_Y5_R2FR_3751_HOP_FACTOR_LANES.csv",
        "SRC3752_2_zero_route": RESIDUALS / "P8_Y5_R2FR_3751_ZERO_ROUTE_CLAUSES.csv",
        "SRC3752_3_projector_variation_contract": RESIDUALS / "P8_PiM_projector_variation_stress_CONTRACT.csv",
        "SRC3752_4_topological_naturality": RESIDUALS / "P8_Y5_R2FR_3498_PROJECTOR_NATURALITY_THEOREM.csv",
        "SRC3752_5_gamma_naturality": RESIDUALS / "P8_Y5_R2FR_3572_PROJECTOR_NATURALITY_PROOF.csv",
        "SRC3752_6_parallel_zero": RESIDUALS / "P8_Y5_R2FR_3747_PARALLEL_PROJECTOR_ZERO_THEOREM.csv",
        "SRC3752_7_domain_bounds": RESIDUALS / "P8_Y5_R2FR_3431_DOMAIN_PROJECTOR_OPERATOR_BOUND_PACK.csv",
        "SRC3752_8_leak_formulas": RESIDUALS / "P8_Y5_R2FR_3748_PROJECTOR_LEAK_BOUND_FORMULAS.csv",
        "SRC3752_9_cap": RESIDUALS / "P8_Y5_R2FR_3750_HIDDEN_OPERATOR_NORM_CAPS.csv",
    }


def source_register(stamp: str) -> list[dict[str, object]]:
    purpose = {
        "SRC3752_0_next": "imports 3752 objective",
        "SRC3752_1_factor_lanes": "imports active metric projector gap",
        "SRC3752_2_zero_route": "imports topological/orthogonal route clauses",
        "SRC3752_3_projector_variation_contract": "imports exact projector variation/stress contract",
        "SRC3752_4_topological_naturality": "imports topological projector condition",
        "SRC3752_5_gamma_naturality": "imports already-closed independent-Gamma projector branch",
        "SRC3752_6_parallel_zero": "imports parent parallel split theorem requirements",
        "SRC3752_7_domain_bounds": "imports fallback metric/domain/boundary bound rows",
        "SRC3752_8_leak_formulas": "imports no-cancellation leakage formulas",
        "SRC3752_9_cap": "imports 3750 global hidden-operator cap",
    }
    return [
        {
            **base(stamp),
            "source_id": key,
            "source_path": str(path),
            "purpose": purpose[key],
            "exists": path.exists(),
            "claim_allowed": False,
        }
        for key, path in sources().items()
    ]


def global_cap() -> float:
    rows = read_csv(sources()["SRC3752_9_cap"])
    for row in rows:
        if row.get("cap_id") == "CAP3750_GLOBAL_MIN":
            return float(row["H_op_max_to_pass_placeholder_tol"])
    raise RuntimeError("CAP3750_GLOBAL_MIN not found")


def theorem_rows(stamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "THM3752_0_setup",
            "Parent Hilbert bundle split",
            "Let E=E_L direct-sum E_M over a local domain D with a parent positive inner product <.,.>_P and closed E_M.",
            "definition",
            "sets the norm in which a contraction statement has meaning",
            "P8_Y5_R2FR_3747_PARALLEL_PROJECTOR_ZERO_THEOREM.csv",
        ),
        (
            "THM3752_1_orthogonal_projector",
            "Orthogonal projection hypotheses",
            "If Pi_M^2=Pi_M and Pi_M^dagger=Pi_M in <.,.>_P, then E_M is orthogonally complemented by ker Pi_M.",
            "hypothesis",
            "rules out an oblique projector with arbitrarily large norm",
            "P8_Y5_R2FR_3751_ZERO_ROUTE_CLAUSES.csv",
        ),
        (
            "THM3752_2_contraction",
            "Contraction proof",
            "For any x, x=Pi_M x+(1-Pi_M)x and the two terms are parent-orthogonal, so ||x||_P^2=||Pi_M x||_P^2+||(1-Pi_M)x||_P^2 >= ||Pi_M x||_P^2.",
            "exact_theorem",
            "therefore ||Pi_M||_{P->P}<=1, with equality unless Pi_M=0",
            "P8_Y5_R2FR_3751_HOP_FACTOR_LANES.csv",
        ),
        (
            "THM3752_3_metric_silence",
            "Metric-independent topological projector",
            "If Pi_M=Pi_top is fixed by parent topology/relative charge before local metric variation, then delta_g Pi_M=0 because neither the charge functional nor representative changes under delta_g.",
            "exact_conditional_theorem",
            "kills bulk projector metric stress only in the parent-owned topological branch",
            "P8_PiM_projector_variation_stress_CONTRACT.csv",
        ),
        (
            "THM3752_4_topological_rank_one_norm",
            "Topological rank-one bound",
            "For Pi_top J=omega_M ell_M(J), ||Pi_top|| <= ||omega_M||_P ||ell_M||_{P,*}; it is contractive if the parent normalizes both dual factors to one.",
            "exact_bound",
            "topological silence does not automatically give contraction unless the parent norm fixes the dual normalization",
            "P8_Y5_R2FR_3498_PROJECTOR_NATURALITY_THEOREM.csv",
        ),
        (
            "THM3752_5_hodge_caveat",
            "Hodge or DeWitt orthogonality caveat",
            "If Pi_M is orthogonal only with respect to a metric-dependent Hodge/DeWitt/e_obs inner product, contraction may hold instantaneously but delta_g Pi_M is generally nonzero.",
            "counterbranch",
            "orthogonal is not the same as metric-stress silent",
            "P8_PiM_projector_variation_stress_CONTRACT.csv",
        ),
        (
            "THM3752_6_local_leak_consequence",
            "Local leak consequence",
            "If THM3752_2 plus THM3752_3 and the 3747 parallel split are parent-signed, then ||E_M^nabla||<=1 and the delta_g projector term is zero; otherwise metric-stress bounds remain active.",
            "conditional_reduction",
            "advances H_op by reducing one factor without claiming full local GR",
            "P8_Y5_R2FR_3748_PROJECTOR_LEAK_BOUND_FORMULAS.csv",
        ),
    ]
    return [
        {
            **base(stamp),
            "theorem_id": theorem_id,
            "claim_piece": claim_piece,
            "statement_or_derivation": statement,
            "status": status,
            "impact": impact,
            "source_file": str(RESIDUALS / source_file),
            "claim_allowed": False,
        }
        for theorem_id, claim_piece, statement, status, impact, source_file in rows
    ]


def branch_matrix(stamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "BR3752_0_parent_topological_orthogonal",
            "Pi_M parent-owned, metric-independent, orthogonal/dual-normalized",
            "||Pi_M||<=1 and delta_g Pi_M=0",
            "BEST_ROUTE_CONDITIONAL",
            "requires parent topology/norm signature; no fitted readout masks",
        ),
        (
            "BR3752_1_parent_topological_oblique",
            "Pi_M parent-owned and metric-independent but not orthogonal/dual-normalized",
            "delta_g Pi_M=0 but ||Pi_M||<=||omega_M||||ell_M||",
            "BOUND_ROUTE",
            "must bound topological dual norm product",
        ),
        (
            "BR3752_2_hodge_orthogonal",
            "Pi_M orthogonal under Hodge/DeWitt/e_obs metric-dependent inner product",
            "||Pi_M||<=1 in that metric but delta_g Pi_M remains live",
            "METRIC_STRESS_ROUTE",
            "must use spectral/projector derivative bound",
        ),
        (
            "BR3752_3_affine_transport_or_mask",
            "Pi_M uses Gamma_ind transport, fitted masks, collars, or empirical selectors before variation",
            "neither contraction nor metric silence is claimable",
            "REJECT_OR_BOUND",
            "falls back to explicit operator source rows",
        ),
    ]
    return [
        {
            **base(stamp),
            "branch_case_id": branch_case_id,
            "projector_branch": projector_branch,
            "mathematical_result": result,
            "status": status,
            "required_next_input": required,
            "claim_allowed": False,
        }
        for branch_case_id, projector_branch, result, status, required in rows
    ]


def fallback_bound_rows(stamp: str, cap: float) -> list[dict[str, object]]:
    rows = [
        (
            "FB3752_0_metric_projector_stress",
            "epsilon_Pi_g",
            "epsilon_Pi_g <= C_pair * ||delta_g Pi_M||_op * ||J_H||_* / M_H_ref",
            "C_pair, ||delta_g Pi_M||_op, ||J_H||_*, M_H_ref",
            "SOURCE_VALUES_MISSING",
        ),
        (
            "FB3752_1_spectral_projector_derivative",
            "||delta_g Pi_M||_op",
            "if Pi_M is a spectral projector of A_P(g), ||delta_g Pi_M||_op <= C_spec * ||delta_g A_P||_op / gap_P",
            "C_spec, ||delta_g A_P||_op, spectral gap gap_P",
            "DERIVED_BOUND_VALUES_MISSING",
        ),
        (
            "FB3752_2_topological_oblique_norm",
            "||Pi_top||",
            "||Pi_top|| <= ||omega_M||_P ||ell_M||_{P,*}",
            "parent normalization of omega_M and ell_M",
            "DERIVED_BOUND_VALUES_MISSING",
        ),
        (
            "FB3752_3_domain_motion",
            "epsilon_Pi_D",
            "epsilon_Pi_D <= C_Pi_D * ||D_D Pi_M||_op * ||delta D|| * ||J_H||_* / M_H_ref",
            "domain derivative norm, support motion amplitude, source norm, M_H_ref",
            "SOURCE_VALUES_MISSING",
        ),
        (
            "FB3752_4_boundary_flux",
            "epsilon_boundary",
            "epsilon_boundary <= |Phi_D| / M_H_ref",
            "no-flux theorem or measured/sourced boundary flux integral",
            "SOURCE_VALUES_MISSING",
        ),
        (
            "FB3752_5_total_absolute",
            "epsilon_projector_abs",
            "epsilon_projector_abs <= |epsilon_Pi_g|+|epsilon_Pi_D|+|epsilon_boundary|+|epsilon_transition|",
            "all sub-bounds, no-cancellation policy",
            "ABSOLUTE_SUM_GUARD",
        ),
        (
            "FB3752_6_cap_interface",
            "H_op_remaining",
            f"fallback product must remain below {cap:.12e} after inserting finite projector-stress factors",
            "finite factors from FB3752_0..FB3752_5",
            "NONCLAIM_CAP_INTERFACE",
        ),
    ]
    return [
        {
            **base(stamp),
            "bound_id": bound_id,
            "quantity": quantity,
            "bound_formula": formula,
            "needed_inputs": needed,
            "status": status,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for bound_id, quantity, formula, needed, status in rows
    ]


def reduced_hop_rows(stamp: str, cap: float) -> list[dict[str, object]]:
    rows = [
        (
            "RHOP3752_0_if_parent_signed",
            "C_pair * 1 * 1 * PPN_response_norm",
            f"PPN_response_norm <= {cap:.12e}",
            "uses contraction ||Pi_M||<=1 and unit Frechet variation",
            "CONDITIONAL_NOT_CLAIM",
        ),
        (
            "RHOP3752_1_if_top_oblique",
            "C_pair * ||omega_M||||ell_M|| * 1 * PPN_response_norm",
            f"C_pair*||omega_M||||ell_M||*PPN_response_norm <= {cap:.12e}",
            "topological silence but non-orthogonal normalization must be bounded",
            "BOUND_ROUTE",
        ),
        (
            "RHOP3752_2_if_hodge_metric",
            "C_pair * (1 + C_spec||delta_g A_P||/gap_P) * PPN_response_norm",
            f"full product must be <= {cap:.12e}",
            "orthogonal alone does not remove metric-stress derivative",
            "ACTIVE_STRESS_ROUTE",
        ),
    ]
    return [
        {
            **base(stamp),
            "reduction_id": reduction_id,
            "reduced_product": product,
            "required_inequality": inequality,
            "assumption": assumption,
            "status": status,
            "claim_allowed": False,
        }
        for reduction_id, product, inequality, assumption, status in rows
    ]


def claim_gates(stamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    all_sources = all(bool(row["exists"]) for row in grouped["sources"])
    exact_contraction = any(row["theorem_id"] == "THM3752_2_contraction" and row["status"] == "exact_theorem" for row in grouped["theorems"])
    hodge_caveat = any(row["theorem_id"] == "THM3752_5_hodge_caveat" for row in grouped["theorems"])
    fallback = len(grouped["fallback_bounds"]) == 7
    gates = [
        ("CG3752_0_sources", "all 3752 source paths exist", all_sources, "path hygiene"),
        ("CG3752_1_contraction_theorem", "orthogonal projector contraction derived", exact_contraction, "||Pi_M||<=1 proof recorded"),
        ("CG3752_2_metric_silence_conditional", "metric silence theorem recorded", True, "requires parent-owned topological branch"),
        ("CG3752_3_hodge_caveat", "Hodge/DeWitt caveat retained", hodge_caveat, "prevents false local-GR closure"),
        ("CG3752_4_fallback_bounds", "metric-stress fallback bounds emitted", fallback, "if topology route fails"),
        ("CG3752_5_parent_signature", "parent topology/norm signature is sourced", False, "still not signed by parent action"),
        ("CG3752_6_parallel_split", "parallel split A_ML=A_LM=0 is sourced", False, "3747 remains conditional"),
        ("CG3752_7_local_claim", "local GR/Newton/PPN claim allowed", False, "3752 is proof progress plus bound interface only"),
    ]
    return [
        {
            **base(stamp),
            "gate_id": gate_id,
            "gate": gate,
            "passed": passed,
            "details": details,
            "claim_allowed": False,
        }
        for gate_id, gate, passed, details in gates
    ]


def decision_rows(stamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "DEC3752_0_progress",
            "ORTHOGONAL_CONTRACTION_DERIVED",
            "The projector norm part is no longer a vague missing coefficient: if Pi_M is parent-orthogonal, ||Pi_M||<=1 follows exactly.",
        ),
        (
            "DEC3752_1_key_warning",
            "ORTHOGONAL_NOT_ENOUGH_FOR_METRIC_SILENCE",
            "If the projector is Hodge/DeWitt metric-built, delta_g Pi_M remains active even though the instantaneous norm is contractive.",
        ),
        (
            "DEC3752_2_best_route",
            "PARENT_TOPOLOGICAL_DUAL_NORMALIZED_PROJECTOR",
            "The least-scrutiny route is to make Pi_M a parent-owned topological/relative-charge projector with fixed dual normalization.",
        ),
        (
            "DEC3752_3_fallback",
            "SPECTRAL_PROJECTOR_DERIVATIVE_BOUND",
            "If metric-built projection is unavoidable, use the spectral-gap derivative bound and feed it into the absolute PPN/source residual vector.",
        ),
    ]
    return [
        {
            **base(stamp),
            "decision_id": decision_id,
            "decision": decision,
            "meaning": meaning,
            "claim_allowed": False,
        }
        for decision_id, decision, meaning in rows
    ]


def next_target(stamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(stamp),
            "next_id": "NEXT3752_0",
            "target_doc": "3753-Y5-R2FR-parent-topological-charge-projector-action-signature.md",
            "target_script": "scripts/Y5_R2FR_3753_parent_topological_charge_projector_action_signature.py",
            "objective": "write the exact parent-action signature that makes Pi_M a metric-independent, dual-normalized topological charge projector before variation, or route to the spectral-gap metric-stress bound",
            "why_this_next": "3752 proves the theorem under precise hypotheses; 3753 must try to source those hypotheses from the parent action rather than leave them as clauses",
            "claim_allowed": False,
        }
    ]


def status_rows(stamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(stamp),
            "status_id": "STATUS3752_0",
            "status": "ORTHOGONAL_CONTRACTION_PROVED_METRIC_SILENCE_CONDITIONAL",
            "summary": "3752 proves the contraction theorem for a parent-orthogonal projector and separates it from metric-stress silence; the clean route now requires a parent topological charge-projector action signature.",
            "claim_allowed": False,
        }
    ]


def validate(stamp: str, paths: dict[str, Path], grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    checks = [
        ("sources_exist", "all source paths exist", all(Path(str(row["source_path"])).exists() for row in grouped["sources"])),
        ("csv_parse", "all generated CSVs parse", all(len(read_csv(path)) > 0 for key, path in paths.items() if key not in {"doc", "validation"})),
        ("contraction_theorem", "exact contraction theorem emitted", any(row["theorem_id"] == "THM3752_2_contraction" and row["status"] == "exact_theorem" for row in grouped["theorems"])),
        ("metric_silence_condition", "metric silence kept conditional", any(row["theorem_id"] == "THM3752_3_metric_silence" and row["status"] == "exact_conditional_theorem" for row in grouped["theorems"])),
        ("hodge_counterbranch", "Hodge metric-stress caveat retained", any(row["theorem_id"] == "THM3752_5_hodge_caveat" and row["status"] == "counterbranch" for row in grouped["theorems"])),
        ("fallback_bounds", "fallback bound rows emitted", len(grouped["fallback_bounds"]) == 7),
        ("local_claim_blocked", "local claim gate remains false", any(row["gate_id"] == "CG3752_7_local_claim" and row["passed"] is False for row in grouped["claim_gates"])),
        ("next_target", "3753 target emitted", grouped["next_target"][0]["target_doc"] == "3753-Y5-R2FR-parent-topological-charge-projector-action-signature.md"),
        ("no_formalization_leak", "no 3752 files written to formalization-workbench", not FORMALIZATION.exists() or not list(FORMALIZATION.rglob("*3752*"))),
    ]
    return [
        {
            **base(stamp),
            "validation_id": validation_id,
            "description": description,
            "result": "PASS" if passed else "FAIL",
            "details": "",
        }
        for validation_id, description, passed in checks
    ]


def render_doc(grouped: dict[str, list[dict[str, object]]], cap: float) -> str:
    lines = [
        "# 3752 — Orthogonal/Topological Projector Contraction Proof",
        "",
        "## Status",
        "",
        "`ORTHOGONAL_CONTRACTION_PROVED_METRIC_SILENCE_CONDITIONAL`.",
        "",
        "This checkpoint proves one piece rather than circling it: a parent-orthogonal projector is contractive. It also blocks the tempting mistake: Hodge/DeWitt orthogonality does not by itself make the projector metric-stress silent.",
        "",
        "## Theorem Core",
    ]
    for row in grouped["theorems"]:
        lines.append(f"- `{row['theorem_id']}` `{row['status']}`: {row['claim_piece']} — {row['impact']}")
    lines.extend(["", "## Branch Matrix"])
    for row in grouped["branches"]:
        lines.append(f"- `{row['branch_case_id']}` `{row['status']}`: {row['projector_branch']} -> {row['mathematical_result']}")
    lines.extend(["", "## Reduced H_op Interface", f"- Imported cap: `H_op <= {cap:.12e}`."])
    for row in grouped["reduced_hop"]:
        lines.append(f"- `{row['reduction_id']}` `{row['status']}`: `{row['reduced_product']}` requires `{row['required_inequality']}`.")
    lines.extend(["", "## Fallback Bounds"])
    for row in grouped["fallback_bounds"]:
        lines.append(f"- `{row['bound_id']}` `{row['status']}`: `{row['bound_formula']}`")
    lines.extend(["", "## Decisions"])
    for row in grouped["decisions"]:
        lines.append(f"- `{row['decision_id']}` `{row['decision']}`: {row['meaning']}")
    lines.extend(["", "## Claim Gates"])
    for row in grouped["claim_gates"]:
        lines.append(f"- `{row['gate_id']}` pass=`{row['passed']}`: {row['gate']} — {row['details']}")
    lines.extend(["", "## Next Target"])
    for row in grouped["next_target"]:
        lines.append(f"- `{row['target_doc']}`: {row['objective']}")
    lines.extend(["", "## Source Register"])
    for row in grouped["sources"]:
        lines.append(f"- `{row['source_id']}` exists=`{row['exists']}`: `{row['source_path']}`")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    stamp = timestamp()
    cap = global_cap()
    paths = {
        "doc": DOC_PATH,
        "sources": RESIDUALS / "P8_Y5_R2FR_3752_SOURCE_REGISTER.csv",
        "theorems": RESIDUALS / "P8_Y5_R2FR_3752_ORTHOGONAL_TOPOLOGICAL_THEOREM_ROWS.csv",
        "branches": RESIDUALS / "P8_Y5_R2FR_3752_PROJECTOR_BRANCH_MATRIX.csv",
        "fallback_bounds": RESIDUALS / "P8_Y5_R2FR_3752_METRIC_STRESS_FALLBACK_BOUNDS.csv",
        "reduced_hop": RESIDUALS / "P8_Y5_R2FR_3752_REDUCED_HOP_INTERFACE.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3752_CLAIM_GATES.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3752_DECISION_ROWS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3752_NEXT_TARGET.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3752_STATUS.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3752_VALIDATION.csv",
    }
    grouped: dict[str, list[dict[str, object]]] = {
        "sources": source_register(stamp),
        "theorems": theorem_rows(stamp),
        "branches": branch_matrix(stamp),
        "fallback_bounds": fallback_bound_rows(stamp, cap),
        "reduced_hop": reduced_hop_rows(stamp, cap),
        "decisions": decision_rows(stamp),
        "next_target": next_target(stamp),
        "status": status_rows(stamp),
    }
    grouped["claim_gates"] = claim_gates(stamp, grouped)
    for key, rows in grouped.items():
        write_csv(paths[key], rows)
    DOC_PATH.write_text(render_doc(grouped, cap), encoding="utf-8")
    grouped["validation"] = validate(stamp, paths, grouped)
    write_csv(paths["validation"], grouped["validation"])
    failures = [row for row in grouped["validation"] if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3752 validation failed: {failures}")
    cache = Path(__file__).resolve().parent / "__pycache__"
    if cache.exists() and str(cache.resolve()).startswith(str(PCW.resolve())):
        shutil.rmtree(cache)
    print("wrote 3752 checkpoint: orthogonal contraction proved; metric silence remains conditional")


if __name__ == "__main__":
    main()
