from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3668"
BRANCH_ID = "MTS_R2FR_Y5_KH_KG_WEAK_FIELD_PROJECTION_ZERO_OR_TRANSFER_KERNEL_BOUND_3668"
DOC = ROOT / "3668-Y5-R2FR-kH-kG-weak-field-projection-zero-or-transfer-kernel-bound.md"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(ts: str) -> dict[str, object]:
    return {
        "timestamp_utc": ts,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> tuple[bool, int]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows)
    except Exception:
        return False, 0


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("handoff_3667", RESIDUALS / "P8_Y5_R2FR_3667_NEXT_TARGET.csv", "3668-Y5-R2FR-kH-kG-weak-field-projection-zero-or-transfer-kernel-bound.md", "3667 selected this target"),
        ("doc_3667", ROOT / "3667-Y5-R2FR-fEM-ZX-profile-normalization-proof-or-first-bound-row.md", "Cassini does not bound `f_EM` or `Z_X` separately", "3667 normalized-combination derivation"),
        ("combos_3667", RESIDUALS / "P8_Y5_R2FR_3667_NORMALIZED_GAMMA_COMBINATION_ROWS.csv", "NC3667_0_muH", "normalized mu_H/mu_G rows"),
        ("bounds_3667", RESIDUALS / "P8_Y5_R2FR_3667_FIRST_FINITE_GAMMA_BOUND_ROWS.csv", "FB3667_lambda_over_r_1", "finite scale-proxy bound rows"),
        ("status_3667", RESIDUALS / "P8_Y5_R2FR_3667_STATUS.csv", "NORMALIZED_GAMMA_COUPLINGS_DERIVED_FIRST_BOUND_ROW_NONCLAIM", "3667 status row"),
        ("doc_3656", ROOT / "3656-Y5-R2FR-first-MTS-local-GR-residual-component-acquisition.md", "S_TF_MTS", "weak-field gamma slip source functional"),
        ("gamma_3656", RESIDUALS / "P8_Y5_R2FR_3656_GAMMA_WEAK_FIELD_DERIVATION_ROWS.csv", "GD3656_2_tracefree_field_equation", "trace-free weak-field equation"),
        ("doc_3657", ROOT / "3657-Y5-R2FR-S_TF_MTS-zero-proof-or-gamma-coefficient-bound.md", "local isotropy/spherical symmetry alone does **not** prove", "STF zero proof and counterexample"),
        ("proof_3657", RESIDUALS / "P8_Y5_R2FR_3657_STF_ZERO_PROOF_ATTEMPT.csv", "ISOTROPY_ALONE_REJECTED", "radial gradient counterexample"),
        ("profile_3658", RESIDUALS / "P8_Y5_R2FR_3658_GAMMA_PROFILE_COEFFICIENT_ROWS.csv", "GPC3658_2_Yukawa_like_profile", "Hessian/gradient profile kernels"),
        ("doc_3658", ROOT / "3658-Y5-R2FR-no-gradient-STF-operator-condition-or-gamma-profile-coefficient.md", "gradient-square STF forces C=0", "radial no-gradient condition"),
        ("frame_leak_1027", ROOT / "1027-Y5-R10-qbarXT-source-zero-or-bounded-coupling-row.md", "Weyl/disformal", "frame/disformal counterexamples"),
        ("hessian_1025", ROOT / "1025-Y5-R10-parent-Hessian-ZX-MX2-range-or-alpha-source-row.md", "lambda_X=sqrt(Z_X/M_X^2)", "local X operator relation"),
    ]
    rows = []
    for source_id, path, needle, role in specs:
        body = read_text(path)
        rows.append(
            {
                **base(ts),
                "source_id": source_id,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in body,
                "role": role,
            }
        )
    return rows


def projection_derivation_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "derivation_id": "KHKG3668_0_STF_projection_form",
            "object": "weak-field STF profile projection",
            "statement": "Any surviving radial X profile contributes to gamma slip through a Hessian-STF term and/or a gradient-square-STF term.",
            "formula": "S_TF^X = k_H P_TF[partial_i partial_j X] + k_G P_TF[partial_i X partial_j X] + S_TF^other",
            "result": "PROJECTION_NORMAL_FORM_DERIVED",
            "claim_allowed": False,
        },
        {
            **base(ts),
            "derivation_id": "KHKG3668_1_linear_quadratic_split",
            "object": "profile-amplitude order",
            "statement": "For X=A_X exp(-r/lambda)/r, the k_H term is linear in A_X while the k_G term is quadratic in A_X.",
            "formula": "delta_gamma_EM = C_H(lambda) mu_H + C_G(lambda) mu_G + C_other; mu_H~f_EM/Z_X, mu_G~f_EM^2/Z_X^2",
            "result": "LINEAR_KH_AND_QUADRATIC_KG_SPLIT_DERIVED",
            "claim_allowed": False,
        },
        {
            **base(ts),
            "derivation_id": "KHKG3668_2_zero_condition",
            "object": "k_H/k_G zero theorem contract",
            "statement": "k_H and k_G vanish if the parent weak-field extra-sector response is trace-only/conformal in the observed frame and no derivative/disformal/boundary/readout STF channel survives.",
            "formula": "P_TF(delta E_ij^X)=0 and P_TF(delta T_ij^X)=0 and P_TF(B_ij+R_ij)=0 => k_H=k_G=0",
            "result": "CONDITIONAL_ZERO_THEOREM_DERIVED_PARENT_UNSIGNED",
            "claim_allowed": False,
        },
        {
            **base(ts),
            "derivation_id": "KHKG3668_3_current_verdict",
            "object": "current parent status",
            "statement": "Current files do not parent-sign trace-only response, no derivative anisotropy, no disformal channel, boundary silence, and readout silence together.",
            "formula": "zero route unsigned => retain finite coefficient/kernel rows",
            "result": "ZERO_NOT_CLOSED_BOUND_INTERFACE_REQUIRED",
            "claim_allowed": False,
        },
    ]


def zero_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("ZG3668_0_EH_TF", "EH trace-free equation owns the observed frame", "GZ3656_1_EH_TF_equation", "UNSIGNED", "without it, non-EH trace-free operators can source slip"),
        ("ZG3668_1_trace_only_extra", "extra local response is pure trace", "STF3657_3_strong_zero_condition", "UNSIGNED", "k_H survives if P_TF(delta E_ij^X) has Hessian-STF content"),
        ("ZG3668_2_no_gradient_stress", "no extra-sector anisotropic gradient stress", "STF3657_2_radial_gradient_counterexample", "UNSIGNED", "k_G survives if P_TF(partial_iX partial_jX) is present"),
        ("ZG3668_3_no_disformal_frame", "no Weyl/disformal representative frame leakage", "1027/1028 frame counterexamples", "UNSIGNED", "disformal/derivative frame can reopen STF response"),
        ("ZG3668_4_boundary_readout", "boundary and readout STF terms vanish", "GZ3656_3/GZ3656_4", "UNSIGNED", "k_H/k_G zero is insufficient if C_other_gamma survives"),
        ("ZG3668_5_total", "all k_H/k_G zero clauses hold together", "3668 combined gate", "NOT_SIGNED", "no gamma/local-GR pass"),
    ]
    return [
        {
            **base(ts),
            "gate_id": gate_id,
            "zero_clause": clause,
            "source_anchor": anchor,
            "current_status": status,
            "blocks_if_missing": blocks,
            "accepted_as_zero": False,
            "claim_allowed": False,
        }
        for gate_id, clause, anchor, status, blocks in specs
    ]


def kernel_coefficient_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "KCR3668_0_Kgamma_H",
            "K_gamma_H(lambda,b,path)",
            "transfer/readout factor mapping Hessian-STF local profile into observed Cassini gamma residual",
            "mu_H=|K_gamma_H k_H f_EM/Z_X|",
            "MISSING_TRANSFER_KERNEL",
            "derive Shapiro/path kernel or set conservative bounded transfer convention",
        ),
        (
            "KCR3668_1_Kgamma_G",
            "K_gamma_G(lambda,b,path)",
            "transfer/readout factor mapping gradient-square-STF local profile into observed Cassini gamma residual",
            "mu_G=|K_gamma_G k_G| f_EM^2/Z_X^2",
            "MISSING_TRANSFER_KERNEL",
            "derive Shapiro/path kernel or set conservative bounded transfer convention",
        ),
        (
            "KCR3668_2_kH",
            "k_H",
            "same-frame weak-field projection coefficient of P_TF[partial_i partial_j X]",
            "S_TF^X contains k_H P_TF[partial_i partial_j X]",
            "MISSING_PARENT_METRIC_RESPONSE",
            "prove no Hessian-STF operator or derive coefficient from parent metric response",
        ),
        (
            "KCR3668_3_kG",
            "k_G",
            "same-frame weak-field projection coefficient of P_TF[partial_i X partial_j X]",
            "S_TF^X contains k_G P_TF[partial_iX partial_jX]",
            "MISSING_PARENT_METRIC_RESPONSE",
            "prove no gradient-square/disformal stress or bound as second-order term",
        ),
        (
            "KCR3668_4_Cother",
            "C_other_gamma",
            "boundary/readout/source/non-EH residual floor outside the radial profile terms",
            "delta_gamma floor = |C_boundary|+|C_readout|+|C_source|+|C_nonEH_other|",
            "MISSING_COMPONENT_BOUNDS",
            "derive zero or source finite bound rows",
        ),
    ]
    return [
        {
            **base(ts),
            "row_id": row_id,
            "symbol": symbol,
            "definition": definition,
            "formula": formula,
            "current_status": status,
            "next_action": action,
            "score_ready": False,
            "claim_allowed": False,
        }
        for row_id, symbol, definition, formula, status, action in specs
    ]


def reduced_bound_rows(ts: str) -> list[dict[str, object]]:
    source_rows = load_csv(RESIDUALS / "P8_Y5_R2FR_3667_FIRST_FINITE_GAMMA_BOUND_ROWS.csv")
    rows = []
    for row in source_rows:
        rows.append(
            {
                **base(ts),
                "row_id": row["bound_id"].replace("FB3667", "RB3668"),
                "lambda_over_r_proxy": row["lambda_over_r_proxy"],
                "C_H_proxy": row["C_H_proxy"],
                "C_G_proxy": row["C_G_proxy"],
                "linear_branch_bound": f"mu_H <= {row['mu_H_max_if_muG_Cother_zero']} if mu_G=0 and C_other_gamma=0",
                "quadratic_branch_bound": f"mu_G <= {row['mu_G_max_if_muH_Cother_zero']} if mu_H=0 and C_other_gamma=0",
                "joint_bound_formula": row["joint_bound_formula"],
                "priority": "k_H_linear_first" if float(row["C_H_proxy"]) > 0.0 else "transfer_kernel_needed",
                "current_status": "REDUCED_NONCLAIM_BOUND_ROW_AWAITING_KH_KG_KGAMMA",
                "why_nonclaim": "uses 3667 solar-limb scale proxy and lacks parent k_H/k_G/K_gamma/C_other rows",
                "score_ready": False,
                "claim_allowed": False,
            }
        )
    return rows


def linear_quadratic_priority_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "priority_id": "PR3668_0_linear_kH",
            "target": "k_H Hessian-STF projection",
            "reason": "linear in A_X and therefore first-order in f_EM/Z_X; if nonzero, it dominates the earliest gamma leakage.",
            "decision": "NEXT_TARGET_PRIMARY",
            "claim_allowed": False,
        },
        {
            **base(ts),
            "priority_id": "PR3668_1_quadratic_kG",
            "target": "k_G gradient-square projection",
            "reason": "quadratic in A_X; can be demoted only under a sourced small-amplitude expansion or if parent stress/disformal terms vanish.",
            "decision": "RETAIN_SECOND_ORDER_GUARD",
            "claim_allowed": False,
        },
        {
            **base(ts),
            "priority_id": "PR3668_2_transfer_kernel",
            "target": "K_gamma transfer/readout kernel",
            "reason": "3667 solar-limb substitution is a scale proxy, not the Shapiro path kernel; any finite score needs the transfer map.",
            "decision": "PARALLEL_REQUIRED_FOR_SCORING",
            "claim_allowed": False,
        },
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("CG3668_0_zero_theorem", "k_H=k_G=0 theorem", "FAILED_UNSIGNED_PARENT_CLAUSES", "trace-only/no-gradient/no-disformal/boundary/readout silence not signed together"),
        ("CG3668_1_projection_normal_form", "weak-field projection normal form", "PASSED_DERIVATION", "S_TF^X splits into Hessian-STF and gradient-square-STF profile pieces"),
        ("CG3668_2_order_hierarchy", "linear/quadratic hierarchy", "PASSED_DERIVATION", "k_H is linear in profile amplitude; k_G is quadratic"),
        ("CG3668_3_bound_interface", "coefficient/kernel bound rows", "PASSED_NONCLAIM_INTERFACE", "K_gamma/k_H/k_G/Cother rows staged without values"),
        ("CG3668_4_gamma_claim", "Cassini gamma/local-GR claim", "ACTIVE_GUARD", "no numeric MTS gamma score or zero proof claimed"),
    ]
    return [
        {
            **base(ts),
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "reason": reason,
            "claim_allowed": False,
        }
        for gate_id, gate, status, reason in specs
    ]


def status_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "status": "KH_KG_ZERO_UNSIGNED_LINEAR_QUADRATIC_SPLIT_DERIVED_NONCLAIM",
            "summary": "3668 derives the k_H/k_G projection normal form and the linear-vs-quadratic hierarchy: k_H is the primary first-order gamma leakage, k_G is second-order but retained. The zero theorem remains unsigned, so finite kernel/coefficient rows are staged nonclaim.",
            "claim_ceiling": "no k_H/k_G zero, Cassini/gamma score, local-GR, PPN, WEP/R10, Newtonian, source-calibration, or EH-dominance pass is claimed",
            "useful_result": "The next target should attack k_H directly: no Hessian-STF/nonminimal/disformal metric-response owner, or a linear gamma-bound row.",
        }
    ]


def next_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3668_0",
            "target_doc": "3669-Y5-R2FR-kH-Hessian-STF-parent-owner-or-linear-gamma-bound-row.md",
            "target_script": "scripts/Y5_R2FR_3669_kH_Hessian_STF_parent_owner_or_linear_gamma_bound_row.py",
            "objective": "prove k_H=0 by excluding Hessian-STF/nonminimal/disformal metric response in the same observed frame, or stage the first linear mu_H gamma-bound row using the 3668 interface",
            "success_gate": "either the linear Hessian-STF channel is parent-zero, or mu_H has a clean nonclaim bound row with explicit transfer-kernel and coefficient blockers",
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    derivation: list[dict[str, object]],
    zero_gates: list[dict[str, object]],
    kernels: list[dict[str, object]],
    bounds: list[dict[str, object]],
    priorities: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3668 - kH kG weak-field projection zero or transfer-kernel bound",
        "",
        f"**Status:** {status[0]['summary']}",
        "",
        f"**Claim ceiling:** {status[0]['claim_ceiling']}.",
        "",
        "## Main result",
        "",
        "The weak-field profile channel now has the correct hierarchy:",
        "",
        "`S_TF^X = k_H P_TF[partial_i partial_j X] + k_G P_TF[partial_i X partial_j X] + S_TF^other`.",
        "",
        "For a Yukawa-like local profile, the `k_H` piece is linear in the profile amplitude while the `k_G` piece is quadratic. That makes `k_H` the first-order target for gamma/local-GR cleanup.",
        "",
        "A zero theorem exists only conditionally: the parent action must make the extra weak-field response trace-only in the same observed frame and must exclude derivative/disformal, boundary, and readout STF channels. Current files do not sign all those clauses together.",
        "",
        "## Projection derivation",
    ]
    for row in derivation:
        lines.append(f"- `{row['derivation_id']}`: {row['result']} - `{row['formula']}`")
    lines.extend(["", "## Zero gates"])
    for row in zero_gates:
        lines.append(f"- `{row['gate_id']}`: {row['current_status']} - {row['zero_clause']}")
    lines.extend(["", "## Kernel/coefficient rows"])
    for row in kernels:
        lines.append(f"- `{row['symbol']}`: {row['current_status']} - {row['next_action']}")
    lines.extend(["", "## Reduced bound interface"])
    for row in bounds:
        lines.append(f"- `{row['row_id']}`: {row['joint_bound_formula']} - {row['current_status']}")
    lines.extend(["", "## Priority decision"])
    for row in priorities:
        lines.append(f"- `{row['priority_id']}`: {row['decision']} - {row['target']}: {row['reason']}")
    lines.extend(["", "## Claim gates"])
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: {row['status']} - {row['gate']}")
    lines.extend(["", "## Next checkpoint", ""])
    lines.append(f"`{next_target[0]['target_doc']}` via `{next_target[0]['target_script']}`.")
    lines.extend(["", "## Sources"])
    for row in sources:
        lines.append(f"- `{row['source_id']}`: `{row['path']}` exists={row['exists']} needle_found={row['needle_found']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(
    ts: str,
    output_paths: list[Path],
    sources: list[dict[str, object]],
    derivation: list[dict[str, object]],
    zero_gates: list[dict[str, object]],
    kernels: list[dict[str, object]],
    bounds: list[dict[str, object]],
    priorities: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(validation_id: str, ok: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": ts,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "validation_id": validation_id,
                "result": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )

    csv_status = [parse_csv(path) for path in output_paths if path.suffix.lower() == ".csv"]
    generated = sources + derivation + zero_gates + kernels + bounds + priorities + gates + status + next_target
    doc_text = read_text(DOC)
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3668*", "3668-Y5-R2FR-*", "P8_Y5*3668*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))

    add("VAL3668_0_sources_exist", all(row["exists"] for row in sources), "every cited source exists")
    add("VAL3668_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found")
    add("VAL3668_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3668 outputs written")
    add("VAL3668_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    add("VAL3668_4_projection_form", any("S_TF^X" in row["formula"] and "k_H" in row["formula"] and "k_G" in row["formula"] for row in derivation), "kH/kG projection normal form present")
    add("VAL3668_5_order_split", any(row["result"] == "LINEAR_KH_AND_QUADRATIC_KG_SPLIT_DERIVED" for row in derivation), "linear/quadratic hierarchy derived")
    add("VAL3668_6_zero_not_accepted", not any(str(row["accepted_as_zero"]).lower() == "true" for row in zero_gates), "kH/kG zero theorem not accepted")
    add("VAL3668_7_kernel_rows", {"K_gamma_H(lambda,b,path)", "K_gamma_G(lambda,b,path)", "k_H", "k_G", "C_other_gamma"}.issubset({str(row["symbol"]) for row in kernels}), "kernel/coefficient blockers present")
    add("VAL3668_8_reduced_bounds", len(bounds) >= 5 and all("mu_H" in row["joint_bound_formula"] and "mu_G" in row["joint_bound_formula"] for row in bounds), "reduced bound rows inherited from 3667")
    add("VAL3668_9_priority", any(row["decision"] == "NEXT_TARGET_PRIMARY" and "k_H" in row["target"] for row in priorities), "kH selected as primary next target")
    add("VAL3668_10_all_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true" for row in generated), "all generated rows remain nonclaim")
    add("VAL3668_11_no_score_ready", not any(str(row.get("score_ready", "")).lower() == "true" for row in kernels + bounds), "kernel and bound rows are not score-ready")
    add("VAL3668_12_doc_written", "k_H" in doc_text and "k_G" in doc_text and "first-order target" in doc_text, "doc records hierarchy and next focus")
    add("VAL3668_13_no_formalization_leak", not leaks, "no 3668 checkpoint files in formalization-workbench")
    add("VAL3668_14_next_target", next_target[0]["target_doc"].startswith("3669-") and "kH-Hessian-STF" in next_target[0]["target_doc"], "3669 kH target selected")
    return rows


def main() -> int:
    ts = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(ts)
    derivation = projection_derivation_rows(ts)
    zero_gates = zero_gate_rows(ts)
    kernels = kernel_coefficient_rows(ts)
    bounds = reduced_bound_rows(ts)
    priorities = linear_quadratic_priority_rows(ts)
    gates = claim_gate_rows(ts)
    status = status_rows(ts)
    next_target = next_rows(ts)
    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3668_SOURCE_REGISTER.csv",
        "derivation": RESIDUALS / "P8_Y5_R2FR_3668_KH_KG_PROJECTION_DERIVATION_ROWS.csv",
        "zero_gates": RESIDUALS / "P8_Y5_R2FR_3668_KH_KG_ZERO_GATES.csv",
        "kernels": RESIDUALS / "P8_Y5_R2FR_3668_KERNEL_COEFFICIENT_ROWS.csv",
        "bounds": RESIDUALS / "P8_Y5_R2FR_3668_REDUCED_BOUND_INTERFACE_ROWS.csv",
        "priorities": RESIDUALS / "P8_Y5_R2FR_3668_LINEAR_QUADRATIC_PRIORITY_ROWS.csv",
        "gates": RESIDUALS / "P8_Y5_R2FR_3668_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3668_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3668_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3668_VALIDATION.csv",
    }
    write_csv(outputs["sources"], sources)
    write_csv(outputs["derivation"], derivation)
    write_csv(outputs["zero_gates"], zero_gates)
    write_csv(outputs["kernels"], kernels)
    write_csv(outputs["bounds"], bounds)
    write_csv(outputs["priorities"], priorities)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, derivation, zero_gates, kernels, bounds, priorities, gates, status, next_target)
    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, derivation, zero_gates, kernels, bounds, priorities, gates, status, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3668 validation failed: {failures}", file=sys.stderr)
        return 1
    print(f"wrote 3668 checkpoint with {len(validation)} validation checks; kH/kG hierarchy derived")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
