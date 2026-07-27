from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3723"
BRANCH_ID = "MTS_R2FR_Y5_NATURAL_VS_MEAN_COORDINATE_OPERATOR_MATCH_OWNER_3723"
DOC = ROOT / "3723-Y5-R2FR-natural-vs-mean-coordinate-operator-match-owner.md"

DOC_3722 = ROOT / "3722-Y5-R2FR-KL-Legendre-effective-action-sign-owner-or-free-energy-demotion.md"
NEXT_3722 = RESIDUALS / "P8_Y5_R2FR_3722_NEXT_TARGET.csv"
COORD_3722 = RESIDUALS / "P8_Y5_R2FR_3722_COORDINATE_CHOICE_ROWS.csv"
OPM_3722 = RESIDUALS / "P8_Y5_R2FR_3722_OPERATOR_MATCH_ROWS.csv"
KLL_3722 = RESIDUALS / "P8_Y5_R2FR_3722_KL_LEGENDRE_THEOREM_ROWS.csv"
FISHER_3708 = RESIDUALS / "P8_Y5_R2FR_3708_FISHER_GAP_DERIVATION_ROWS.csv"
DOUBLET_517 = RESIDUALS / "P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv"
DOUBLET_CONTRACT_516 = RESIDUALS / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv"


def now() -> str:
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
        ("doc_3722", DOC_3722, "NATURAL_VS_MEAN_COORDINATE_IS_NOW_THE_MAIN_FORK", "3722 coordinate fork"),
        ("next_3722", NEXT_3722, "natural_vs_mean_coordinate", "3723 handoff"),
        ("coord_3722", COORD_3722, "Z=m=E_z[Y]-E_0[Y]", "mean coordinate branch"),
        ("opm_3722", OPM_3722, "Theta_H I^{-1}_AB", "operator branch rows"),
        ("kll_3722", KLL_3722, "W_star", "Legendre theorem rows"),
        ("fisher_3708", FISHER_3708, "p_z(xi|X_B,q)=p_0 exp", "natural-parameter Fisher source"),
        ("doublet_517", DOUBLET_517, "Z^A=(R_+^A-R_-^A)/2", "response-doublet residual coordinate"),
        ("doublet_contract_516", DOUBLET_CONTRACT_516, "Z^A=Y_loc^A", "physical residual lock requirement"),
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


def notation_reset_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        ("NOT3723_0_eta", "eta^A", "natural/exponential-family source parameter", "p_eta=p_0 exp[eta^A Y_A-W(eta)]"),
        ("NOT3723_1_m", "m_A", "mean/response coordinate", "m_A=E_eta[Y_A]-E_0[Y_A]=partial_A W(eta)"),
        ("NOT3723_2_Z", "Z^A", "response-doublet physical residual coordinate", "Z^A=(R_+^A-R_-^A)/2"),
        ("NOT3723_3_local_map", "Z=L_m m or Z=L_eta eta", "coordinate owner map", "must be parent-signed before choosing I or I^{-1}"),
    ]
    return [
        {
            **base(ts),
            "notation_id": notation_id,
            "symbol": symbol,
            "meaning": meaning,
            "definition": definition,
            "claim_allowed": False,
        }
        for notation_id, symbol, meaning, definition in rows
    ]


def evidence_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "EVID3723_0_3708_eta",
            "3708 uses p_z=p_0 exp[zY-W]",
            "This is natural-parameter form; rename that coordinate eta to avoid confusion.",
            "SUPPORTS_NATURAL_PARAMETER_FOR_3708_Z",
        ),
        (
            "EVID3723_1_517_Z",
            "517 defines Z=(R_+-R_-)/2 as a residual doublet coordinate",
            "This looks like a physical/mean residual amplitude, not a conjugate source multiplier.",
            "SUPPORTS_MEAN_DEFAULT_FOR_RESPONSE_Z",
        ),
        (
            "EVID3723_2_contract_lock",
            "516 requires Z^A=Y_loc^A through PPN/local order",
            "If Z is locked to local observable residuals, mean-coordinate interpretation is the less smuggly default.",
            "SUPPORTS_MEAN_DEFAULT_BUT_UNSIGNED",
        ),
        (
            "EVID3723_3_no_parent_choice",
            "No current row proves Z=eta rather than Z=m or Z=L eta",
            "Therefore no local screening claim can use either Hessian branch without a retained mismatch.",
            "CLAIM_BLOCKER",
        ),
    ]
    return [
        {
            **base(ts),
            "evidence_id": evidence_id,
            "source_observation": source_observation,
            "interpretation": interpretation,
            "status": status,
            "claim_allowed": False,
        }
        for evidence_id, source_observation, interpretation, status in rows
    ]


def coordinate_theorem_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "CTH3723_0_eta_to_m",
            "m_A=partial_A W(eta)=I_AB eta^B+O(eta^2)",
            "local mean and natural coordinates are related by the Fisher matrix",
            "DERIVED",
        ),
        (
            "CTH3723_1_natural_operator",
            "If Z=eta, then Psi=0.5 Theta_H I_AB Z^A Z^B+O(Z^3)",
            "M_Z=Theta_H I",
            "CONDITIONAL_BRANCH",
        ),
        (
            "CTH3723_2_mean_operator",
            "If Z=m, then Psi=Theta_H W_star(Z)=0.5 Theta_H (I^{-1})^{AB} Z_A Z_B+O(Z^3)",
            "M_Z=Theta_H I^{-1}",
            "CONDITIONAL_BRANCH_SELECTED_AS_DEFAULT",
        ),
        (
            "CTH3723_3_general_map",
            "If Z=L eta+O(eta^2), then M_Z=Theta_H L^{-T} I L^{-1}",
            "keeps arbitrary coordinate maps explicit",
            "DERIVED_BOUND_BRANCH",
        ),
        (
            "CTH3723_4_default_rule",
            "Because response-doublet Z is written as residual amplitude, default internal route is mean branch unless parent signs Z=eta",
            "this is a discipline rule, not a claim",
            "DEFAULT_SELECTION_NONCLAIM",
        ),
    ]
    return [
        {
            **base(ts),
            "theorem_id": theorem_id,
            "formula": formula,
            "result": result,
            "status": status,
            "claim_allowed": False,
        }
        for theorem_id, formula, result, status in rows
    ]


def operator_pack_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        ("PACK3723_0_default_mean", "M_Z,default", "Theta_H I^{-1} + DeltaM_mean", "local Hessian/operator units after U_H", "DEFAULT_NONCLAIM"),
        ("PACK3723_1_natural_alt", "M_Z,natural", "Theta_H I + DeltaM_nat", "only if Z=eta is parent-signed", "ALTERNATE_BRANCH_BLOCKED"),
        ("PACK3723_2_general", "M_Z,general", "Theta_H L^{-T} I L^{-1}+DeltaM_L", "if coordinate Jacobian L is sourced", "GENERAL_BOUND_BRANCH"),
        ("PACK3723_3_gap_default", "Xi_H,default", "lambda_min(Theta_H I^{-1})-||DeltaM_mean||-R_loss", "requires positive floor and unit map", "BOUND_FORM_NONCLAIM"),
        ("PACK3723_4_gap_guard", "no_claim_guard", "do not use lambda_min(Theta_H I) for response Z unless Z=eta", "prevents wrong-Hessian screening claim", "ACTIVE_GUARD"),
    ]
    return [
        {
            **base(ts),
            "pack_id": pack_id,
            "quantity": quantity,
            "formula": formula,
            "units_or_scope": units_or_scope,
            "status": status,
            "claim_allowed": False,
        }
        for pack_id, quantity, formula, units_or_scope, status in rows
    ]


def decision_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "DEC3723_0_notation_reset",
            "RENAME_3708_Z_TO_ETA_IN_THIS_BRANCH",
            "The exponential-family coordinate is natural parameter eta; response-doublet Z should not inherit that name silently.",
        ),
        (
            "DEC3723_1_default_mean",
            "MEAN_COORDINATE_DEFAULT_SELECTED_NONCLAIM",
            "Response-doublet Z is a residual amplitude, so the least-smuggly internal default is Z=m and M=Theta I^{-1}.",
        ),
        (
            "DEC3723_2_natural_not_rejected",
            "NATURAL_BRANCH_RETAINED_IF_PARENT_SIGNS_Z_EQUALS_ETA",
            "If later parent text proves Z is a conjugate bath-source parameter, switch to M=Theta I.",
        ),
        (
            "DEC3723_3_next",
            "ADVANCE_TO_MEAN_BRANCH_GAP_FLOOR_AND_UNIT_MAP_OWNER",
            "Next target should source-own I^{-1}, Theta_H, U_H, and DeltaM_mean or keep the default branch nonclaim.",
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
        ("CG3723_0_coordinate_type", "BLOCKED", "Z=m default or Z=eta alternative is parent-signed"),
        ("CG3723_1_I_inverse", "BLOCKED", "I is positive/invertible on active quotient-fibre subspace"),
        ("CG3723_2_theta", "BLOCKED", "Theta_H positive and unit-owned"),
        ("CG3723_3_UH", "BLOCKED", "U_H maps M_Z to local m^-2/operator units"),
        ("CG3723_4_DeltaM", "BLOCKED", "DeltaM_mean/natural/general is theorem-zero or bounded"),
        ("CG3723_5_boundary", "BLOCKED", "R_loss/F_loss/QK_loss are closed or finite"),
        ("CG3723_6_claim", "BLOCKED", "local gap/screening claim allowed"),
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
        "status_id": "STATUS3723_0",
        "status": "MEAN_COORDINATE_DEFAULT_SELECTED_NONCLAIM_NATURAL_BRANCH_RETAINED",
        "summary": "3723 resets notation: 3708 z becomes eta natural parameter, response-doublet Z defaults to mean/residual coordinate m, so the default operator is Theta_H I^{-1}, with Theta_H I retained only if Z=eta is parent-signed.",
        "claim_allowed": False,
    }]


def next_target_rows(ts: str) -> list[dict[str, object]]:
    return [{
        **base(ts),
        "next_id": "NEXT3723_0",
        "target_doc": "3724-Y5-R2FR-mean-branch-gap-floor-unit-map-owner.md",
        "target_script": "scripts/Y5_R2FR_3724_mean_branch_gap_floor_unit_map_owner.py",
        "objective": "try to source-own the mean-branch operator M_Z=Theta_H I^{-1}, including Fisher invertibility floor, Theta_H units, U_H local unit map, and DeltaM_mean correction bound",
        "success_gate": "I inverse, Theta_H, U_H, DeltaM_mean, and R_loss are parent-owned or retained as finite nonclaim rows",
        "claim_allowed": False,
    }]


def validation_rows(ts: str, paths: dict[str, Path]) -> list[dict[str, object]]:
    sources = parse_csv(paths["source_register"])
    csv_paths = [path for key, path in paths.items() if key not in {"doc", "validation"}]
    generated = [path for key, path in paths.items() if key != "validation"]
    formal_files = list(FORMALIZATION.rglob("*3723*")) if FORMALIZATION.exists() else []
    formal_files = [path for path in formal_files if path.is_file()]
    checks = [
        ("sources_exist", "sources exist", all(row["exists"] == "True" for row in sources)),
        ("needles_found", "source needles found", all(row["needle_found"] == "True" for row in sources)),
        ("outputs_exist", "outputs exist", all(path.exists() for path in generated)),
        ("csv_parse", "CSVs parse", all(len(parse_csv(path)) > 0 for path in csv_paths if path.exists())),
        ("notation_reset", "eta/m/Z notation rows exist", all(token in read_text(paths["notation"]) for token in ["eta^A", "m_A", "Z^A"])),
        ("mean_default", "mean branch default exists", all(token in read_text(paths["theorems"]) for token in ["M_Z=Theta_H I^{-1}", "DEFAULT_SELECTION_NONCLAIM"])),
        ("natural_guard", "natural branch retained only if signed", "only if Z=eta" in read_text(paths["pack"])),
        ("decisions", "decisions select mean default and retain natural alternative", all(token in read_text(paths["decisions"]) for token in ["MEAN_COORDINATE_DEFAULT_SELECTED_NONCLAIM", "NATURAL_BRANCH_RETAINED"])),
        ("claim_gates_blocked", "all claim gates blocked", all(row["gate_status"] == "BLOCKED" and row["claim_allowed"] == "False" for row in parse_csv(paths["claim_gates"]))),
        ("next_target_3724", "next target is 3724", "3724" in read_text(paths["next_target"])),
        ("doc_core_terms", "doc contains default operator result", all(token in read_text(paths["doc"]) for token in ["default operator is `Theta_H I^{-1}`", "3708 z becomes `eta`", "`Theta_H I` is retained only if `Z=eta`"])),
        ("no_formalization_leak", "no 3723 files in formalization-workbench", len(formal_files) == 0),
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
        "# 3723 — Natural vs Mean Coordinate Operator Match Owner",
        "",
        "## Status",
        "- `MEAN_COORDINATE_DEFAULT_SELECTED_NONCLAIM_NATURAL_BRANCH_RETAINED`",
        "- 3708 z becomes `eta` here: it is the natural/exponential-family parameter.",
        "- Response-doublet `Z=(R_+-R_-)/2` defaults to the mean/residual coordinate `m`, so the default operator is `Theta_H I^{-1}`.",
        "- `Theta_H I` is retained only if `Z=eta` is parent-signed.",
        "",
        "## Main Result",
        "- Natural-to-mean map: `m_A=partial_A W=I_AB eta^B+O(eta^2)`.",
        "- If `Z=eta`, then `M_Z=Theta_H I`.",
        "- If `Z=m`, then `M_Z=Theta_H I^{-1}`.",
        "- Current corpus leans to `Z=m` because response-doublet `Z` is written as a local residual amplitude, but this remains nonclaim until the parent signs the coordinate type.",
        "",
        "## Notation Reset",
    ]
    for row in grouped["notation"]:
        lines.append(f"- `{row['notation_id']}` `{row['symbol']}`: {row['meaning']} | {row['definition']}")
    lines.extend(["", "## Evidence"])
    for row in grouped["evidence"]:
        lines.append(f"- `{row['evidence_id']}` `{row['status']}`: {row['source_observation']} | {row['interpretation']}")
    lines.extend(["", "## Coordinate Theorems"])
    for row in grouped["theorems"]:
        lines.append(f"- `{row['theorem_id']}` `{row['status']}`: `{row['formula']}` | {row['result']}")
    lines.extend(["", "## Operator Pack"])
    for row in grouped["pack"]:
        lines.append(f"- `{row['pack_id']}` `{row['quantity']}`: `{row['formula']}` | {row['status']}")
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
        "- `3724-Y5-R2FR-mean-branch-gap-floor-unit-map-owner.md`",
        "- Objective: source-own or bound the mean-branch gap floor and unit map.",
        "",
        "## Validation",
        f"- See `{paths['validation']}`.",
    ])
    paths["doc"].write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ts = now()
    paths = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3723_SOURCE_REGISTER.csv",
        "notation": RESIDUALS / "P8_Y5_R2FR_3723_NOTATION_RESET_ROWS.csv",
        "evidence": RESIDUALS / "P8_Y5_R2FR_3723_COORDINATE_EVIDENCE_ROWS.csv",
        "theorems": RESIDUALS / "P8_Y5_R2FR_3723_COORDINATE_THEOREM_ROWS.csv",
        "pack": RESIDUALS / "P8_Y5_R2FR_3723_OPERATOR_PACK_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3723_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3723_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3723_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3723_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3723_VALIDATION.csv",
        "doc": DOC,
    }
    grouped = {
        "source_register": source_register(ts),
        "notation": notation_reset_rows(ts),
        "evidence": evidence_rows(ts),
        "theorems": coordinate_theorem_rows(ts),
        "pack": operator_pack_rows(ts),
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
        raise SystemExit(f"3723 validation failed: {failures}")
    print("wrote 3723 checkpoint: mean-coordinate default selected nonclaim; natural branch retained")


if __name__ == "__main__":
    main()
