from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3724"
BRANCH_ID = "MTS_R2FR_Y5_MEAN_BRANCH_GAP_FLOOR_UNIT_MAP_OWNER_3724"
DOC = ROOT / "3724-Y5-R2FR-mean-branch-gap-floor-unit-map-owner.md"

DOC_3723 = ROOT / "3723-Y5-R2FR-natural-vs-mean-coordinate-operator-match-owner.md"
NEXT_3723 = RESIDUALS / "P8_Y5_R2FR_3723_NEXT_TARGET.csv"
PACK_3723 = RESIDUALS / "P8_Y5_R2FR_3723_OPERATOR_PACK_ROWS.csv"
GATES_3723 = RESIDUALS / "P8_Y5_R2FR_3723_CLAIM_GATES.csv"
KLL_3722 = RESIDUALS / "P8_Y5_R2FR_3722_KL_LEGENDRE_THEOREM_ROWS.csv"
FISHER_3708 = RESIDUALS / "P8_Y5_R2FR_3708_FISHER_GAP_DERIVATION_ROWS.csv"


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
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("doc_3723", DOC_3723, "MEAN_COORDINATE_DEFAULT_SELECTED_NONCLAIM_NATURAL_BRANCH_RETAINED", "3723 status"),
        ("next_3723", NEXT_3723, "mean-branch operator M_Z=Theta_H I^{-1}", "3724 handoff"),
        ("pack_3723", PACK_3723, "lambda_min(Theta_H I^{-1})", "default mean gap row"),
        ("gates_3723", GATES_3723, "I is positive/invertible", "prior inverse gate"),
        ("kll_3722", KLL_3722, "W_star", "Legendre/mean Hessian theorem"),
        ("fisher_3708", FISHER_3708, "iota_H=lambda_min", "older Fisher gap notation"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append({
            **base(ts),
            "source_id": source_id,
            "path": str(path),
            "exists": exists,
            "needle": needle,
            "needle_found": needle in text,
            "role": role,
        })
    return rows


def mean_gap_law_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "MGL3724_0_active_subspace",
            "Work on active fibre subspace K_act after exact nulls/gauge directions are quotiented.",
            "required before I^{-1} exists",
            "DOMAIN_CLAUSE",
        ),
        (
            "MGL3724_1_fisher_window",
            "0 < iota_min <= lambda_min(I_H|K_act) and lambda_max(I_H|K_act) <= iota_max < infinity",
            "iota_min gives invertibility; iota_max gives a lower floor for I^{-1}",
            "DERIVED_REQUIREMENT",
        ),
        (
            "MGL3724_2_inverse_floor",
            "lambda_min(I_H^{-1}|K_act)=1/lambda_max(I_H|K_act) >= 1/iota_max",
            "mean branch needs Fisher ceiling, not only Fisher floor",
            "DERIVED_EXACT",
        ),
        (
            "MGL3724_3_core_gap",
            "lambda_min(Theta_H I_H^{-1}) >= Theta_min/iota_max if Theta_H>=Theta_min>0",
            "core mean-branch gap floor",
            "DERIVED_BOUND",
        ),
        (
            "MGL3724_4_correction_gap",
            "lambda_min(M_Z,total) >= Theta_min/iota_max - ||DeltaM_mean|| - R_loss",
            "Weyl-safe correction bound before unit conversion",
            "DERIVED_BOUND",
        ),
        (
            "MGL3724_5_local_unit_gap",
            "Xi_loc >= u_min^2*(Theta_min/iota_max - ||DeltaM_mean|| - R_loss) - R_U",
            "local m^-2/operator gap after U_H with coercivity u_min and unit-map remainder R_U",
            "DERIVED_BOUND",
        ),
    ]
    return [
        {
            **base(ts),
            "law_id": law_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "claim_allowed": False,
        }
        for law_id, formula, meaning, status in rows
    ]


def input_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        ("IN3724_0_theta_min", "Theta_min", "lower bound of positive KL/Legendre scale", "action/operator scale", "MISSING_PARENT_VALUE"),
        ("IN3724_1_iota_min", "iota_min", "positive lower Fisher eigenvalue on K_act", "score^2 units", "MISSING_INVERTIBILITY_FLOOR"),
        ("IN3724_2_iota_max", "iota_max", "finite upper Fisher eigenvalue on K_act", "score^2 units", "MISSING_FISHER_CEILING"),
        ("IN3724_3_UH_umin", "u_min", "coercivity/smallest singular value of U_H local unit map", "basis-to-local operator conversion", "MISSING_UNIT_MAP_COERCIVITY"),
        ("IN3724_4_DeltaM_mean", "||DeltaM_mean||", "operator mismatch between response doublet M_Z and Theta_H I^{-1}", "same basis as M_Z", "MISSING_MISMATCH_BOUND"),
        ("IN3724_5_R_loss", "R_loss", "domain/source/boundary/even-correction loss", "same basis as M_Z", "MISSING_CORRECTION_BOUND"),
        ("IN3724_6_R_U", "R_U", "unit-map remainder from non-isometric/projection conversion", "local operator units", "MISSING_UNIT_REMAINDER"),
        ("IN3724_7_Xi_loc", "Xi_loc", "u_min^2*(Theta_min/iota_max-||DeltaM_mean||-R_loss)-R_U", "m^-2/local operator units", "SYMBOLIC_DERIVED_NOT_NUMERIC"),
    ]
    return [
        {
            **base(ts),
            "input_id": input_id,
            "quantity": quantity,
            "definition": definition,
            "units_or_basis": units_or_basis,
            "status": status,
            "claim_allowed": False,
        }
        for input_id, quantity, definition, units_or_basis, status in rows
    ]


def correction_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        ("COR3724_0_DeltaM_mean", "DeltaM_mean", "M_Z,total - Theta_H I^{-1}", "operator mismatch; must be zero or bounded"),
        ("COR3724_1_R_domain", "R_domain", "loss from finite local domain and gauge/null quotient", "can reduce gap or spoil invertibility"),
        ("COR3724_2_R_source", "R_source", "source-current or slope loss in active local branch", "prevents treating bath stiffness as source-free"),
        ("COR3724_3_R_boundary", "R_boundary", "boundary/symplectic/local collar remainder", "same boundary debt as earlier F_loss/QK_loss"),
        ("COR3724_4_R_U", "R_U", "unit-map/projection remainder", "converts abstract Hessian to observed local operator"),
    ]
    return [
        {
            **base(ts),
            "correction_id": correction_id,
            "quantity": quantity,
            "definition": definition,
            "impact": impact,
            "status": "FINITE_ROW_REQUIRED_UNLESS_THEOREM_ZERO",
            "claim_allowed": False,
        }
        for correction_id, quantity, definition, impact in rows
    ]


def decision_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "DEC3724_0_ceiling_needed",
            "FISHER_CEILING_ADDED_TO_MEAN_BRANCH",
            "For M=Theta I^{-1}, the smallest local gap is controlled by lambda_max(I), so iota_max is mandatory.",
        ),
        (
            "DEC3724_1_floor_still_needed",
            "FISHER_FLOOR_STILL_REQUIRED_FOR_INVERTIBILITY",
            "iota_min remains required so I^{-1} exists on the active subspace, but it is not the mean-branch gap floor.",
        ),
        (
            "DEC3724_2_unit_map_is_live",
            "UNIT_MAP_COERCIVITY_IS_A_REAL_GATE",
            "Even a positive abstract Hessian is not a local R10/PPN operator until U_H and its units are owned.",
        ),
        (
            "DEC3724_3_next",
            "ADVANCE_TO_FISHER_WINDOW_AND_UH_SOURCE_HUNT",
            "Next target should try to source-own theta_min, iota_min, iota_max, U_H, and correction losses from the parent corpus.",
        ),
    ]
    return [
        {
            **base(ts),
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "claim_allowed": False,
        }
        for decision_id, decision, rationale in rows
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    gates = [
        ("CG3724_0_Kact", "BLOCKED", "active fibre subspace K_act is parent-defined after null/gauge quotient"),
        ("CG3724_1_I_window", "BLOCKED", "0<iota_min and finite iota_max are parent-owned"),
        ("CG3724_2_theta", "BLOCKED", "Theta_min positive with units"),
        ("CG3724_3_UH", "BLOCKED", "U_H local unit map has coercivity u_min and units"),
        ("CG3724_4_corrections", "BLOCKED", "DeltaM_mean, R_loss, and R_U are zero or finite sourced"),
        ("CG3724_5_Xi_positive", "BLOCKED", "Xi_loc>0 in m^-2/local operator units"),
        ("CG3724_6_claim", "BLOCKED", "mean-branch local screening claim allowed"),
    ]
    return [
        {
            **base(ts),
            "gate_id": gate_id,
            "gate_status": gate_status,
            "required_before_claim": required_before_claim,
            "claim_allowed": False,
        }
        for gate_id, gate_status, required_before_claim in gates
    ]


def status_rows(ts: str) -> list[dict[str, object]]:
    return [{
        **base(ts),
        "status_id": "STATUS3724_0",
        "status": "MEAN_GAP_LAW_DERIVED_FISHER_CEILING_AND_UNIT_MAP_REQUIRED",
        "summary": "3724 derives the corrected mean-branch local gap bound Xi_loc >= u_min^2*(Theta_min/iota_max-||DeltaM_mean||-R_loss)-R_U. This adds a Fisher ceiling iota_max and a U_H coercivity gate.",
        "claim_allowed": False,
    }]


def next_target_rows(ts: str) -> list[dict[str, object]]:
    return [{
        **base(ts),
        "next_id": "NEXT3724_0",
        "target_doc": "3725-Y5-R2FR-Fisher-window-UH-source-hunt-or-finite-bound-pack.md",
        "target_script": "scripts/Y5_R2FR_3725_Fisher_window_UH_source_hunt_or_finite_bound_pack.py",
        "objective": "search and source-own the Fisher eigenvalue window, Theta_H units, U_H local unit map, and correction losses; otherwise retain them as finite nonclaim coefficient rows",
        "success_gate": "theta_min, iota_min, iota_max, u_min, DeltaM_mean, R_loss, and R_U have source paths or remain explicit blocked rows",
        "claim_allowed": False,
    }]


def validation_rows(ts: str, paths: dict[str, Path]) -> list[dict[str, object]]:
    sources = parse_csv(paths["source_register"])
    csv_paths = [path for key, path in paths.items() if key not in {"doc", "validation"}]
    generated = [path for key, path in paths.items() if key != "validation"]
    formal_files = list(FORMALIZATION.rglob("*3724*")) if FORMALIZATION.exists() else []
    formal_files = [path for path in formal_files if path.is_file()]
    checks = [
        ("sources_exist", "sources exist", all(row["exists"] == "True" for row in sources)),
        ("needles_found", "source needles found", all(row["needle_found"] == "True" for row in sources)),
        ("outputs_exist", "outputs exist", all(path.exists() for path in generated)),
        ("csv_parse", "CSVs parse", all(len(parse_csv(path)) > 0 for path in csv_paths if path.exists())),
        ("inverse_floor", "inverse floor uses iota_max", "lambda_min(I_H^{-1}|K_act)=1/lambda_max" in read_text(paths["laws"])),
        ("local_gap", "local gap includes U_H and corrections", all(token in read_text(paths["laws"]) for token in ["u_min^2", "Theta_min/iota_max", "R_U"])),
        ("inputs", "input rows include iota_max and u_min", all(token in read_text(paths["inputs"]) for token in ["iota_max", "u_min", "Xi_loc"])),
        ("decisions", "decisions call out Fisher ceiling", "FISHER_CEILING_ADDED_TO_MEAN_BRANCH" in read_text(paths["decisions"])),
        ("claim_gates_blocked", "all claim gates blocked", all(row["gate_status"] == "BLOCKED" and row["claim_allowed"] == "False" for row in parse_csv(paths["claim_gates"]))),
        ("next_target_3725", "next target is 3725", "3725" in read_text(paths["next_target"])),
        ("doc_core_terms", "doc contains corrected mean bound", all(token in read_text(paths["doc"]) for token in ["Theta_min/iota_max", "Fisher ceiling", "Xi_loc"])),
        ("no_formalization_leak", "no 3724 files in formalization-workbench", len(formal_files) == 0),
    ]
    return [
        {
            **base(ts),
            "validation_id": validation_id,
            "description": description,
            "result": "PASS" if result else "FAIL",
            "details": "",
        }
        for validation_id, description, result in checks
    ]


def write_doc(paths: dict[str, Path], grouped: dict[str, list[dict[str, object]]]) -> None:
    lines = [
        "# 3724 — Mean-Branch Gap Floor and Unit Map Owner",
        "",
        "## Status",
        "- `MEAN_GAP_LAW_DERIVED_FISHER_CEILING_AND_UNIT_MAP_REQUIRED`",
        "- Corrected mean-branch bound: `Xi_loc >= u_min^2*(Theta_min/iota_max-||DeltaM_mean||-R_loss)-R_U`.",
        "- New discipline point: the mean branch needs a Fisher ceiling `iota_max`; `iota_min` gives invertibility but not the lower gap floor.",
        "- No local screening claim follows until `Theta_H`, the Fisher eigenvalue window, `U_H`, and correction losses are parent-owned or bounded.",
        "",
        "## Main Result",
        "- For `M_Z=Theta_H I_H^{-1}`, `lambda_min(I_H^{-1})=1/lambda_max(I_H)`.",
        "- Therefore the abstract mean gap is bounded by `Theta_min/iota_max`, not by `Theta_min/iota_min`.",
        "- The local operator gap additionally needs unit-map coercivity: `U_H` contributes `u_min^2` and remainder `R_U`.",
        "",
        "## Mean Gap Laws",
    ]
    for row in grouped["laws"]:
        lines.append(f"- `{row['law_id']}` `{row['status']}`: `{row['formula']}` | {row['meaning']}")
    lines.extend(["", "## Required Inputs"])
    for row in grouped["inputs"]:
        lines.append(f"- `{row['input_id']}` `{row['quantity']}`: {row['definition']} | {row['units_or_basis']} | {row['status']}")
    lines.extend(["", "## Correction Rows"])
    for row in grouped["corrections"]:
        lines.append(f"- `{row['correction_id']}` `{row['quantity']}`: {row['definition']} | {row['impact']}")
    lines.extend(["", "## Decisions"])
    for row in grouped["decisions"]:
        lines.append(f"- `{row['decision_id']}` `{row['decision']}` | {row['rationale']}")
    lines.extend(["", "## Claim Gates"])
    for row in grouped["claim_gates"]:
        lines.append(f"- `{row['gate_id']}` `{row['gate_status']}` | {row['required_before_claim']}")
    lines.extend(["", "## Source Register"])
    for row in grouped["source_register"]:
        lines.append(f"- `{row['source_id']}`: exists={row['exists']} needle_found={row['needle_found']} path=`{row['path']}`")
    lines.extend([
        "",
        "## Next Target",
        "- `3725-Y5-R2FR-Fisher-window-UH-source-hunt-or-finite-bound-pack.md`",
        "- Objective: source-own or explicitly retain `theta_min`, `iota_min`, `iota_max`, `u_min`, `DeltaM_mean`, `R_loss`, and `R_U`.",
        "",
        "## Validation",
        f"- See `{paths['validation']}`.",
    ])
    paths["doc"].write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ts = stamp()
    paths = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3724_SOURCE_REGISTER.csv",
        "laws": RESIDUALS / "P8_Y5_R2FR_3724_MEAN_GAP_LAW_ROWS.csv",
        "inputs": RESIDUALS / "P8_Y5_R2FR_3724_REQUIRED_INPUT_ROWS.csv",
        "corrections": RESIDUALS / "P8_Y5_R2FR_3724_CORRECTION_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3724_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3724_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3724_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3724_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3724_VALIDATION.csv",
        "doc": DOC,
    }
    grouped = {
        "source_register": source_register(ts),
        "laws": mean_gap_law_rows(ts),
        "inputs": input_rows(ts),
        "corrections": correction_rows(ts),
        "decisions": decision_rows(ts),
        "claim_gates": claim_gate_rows(ts),
        "status": status_rows(ts),
        "next_target": next_target_rows(ts),
    }
    for key, rows in grouped.items():
        write_csv(paths[key], rows)
    write_doc(paths, grouped)
    write_csv(paths["validation"], validation_rows(ts, paths))
    failures = [row for row in parse_csv(paths["validation"]) if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3724 validation failed: {failures}")
    print("wrote 3724 checkpoint: corrected mean-branch gap bound with Fisher ceiling and U_H gate")


if __name__ == "__main__":
    main()
