from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3722"
BRANCH_ID = "MTS_R2FR_Y5_KL_LEGENDRE_EFFECTIVE_ACTION_SIGN_OWNER_OR_FREE_ENERGY_DEMOTION_3722"
DOC = ROOT / "3722-Y5-R2FR-KL-Legendre-effective-action-sign-owner-or-free-energy-demotion.md"

DOC_3721 = ROOT / "3721-Y5-R2FR-response-doublet-to-Gibbs-bath-parity-map-or-demotion.md"
NEXT_3721 = RESIDUALS / "P8_Y5_R2FR_3721_NEXT_TARGET.csv"
THEOREM_3721 = RESIDUALS / "P8_Y5_R2FR_3721_BRIDGE_THEOREM_ROWS.csv"
AUDIT_3721 = RESIDUALS / "P8_Y5_R2FR_3721_CURRENT_BRIDGE_AUDIT_ROWS.csv"
COEFF_3721 = RESIDUALS / "P8_Y5_R2FR_3721_RETAINED_COEFFICIENT_ROWS.csv"
FISHER_3708 = RESIDUALS / "P8_Y5_R2FR_3708_FISHER_GAP_DERIVATION_ROWS.csv"
DOUBLET_517 = RESIDUALS / "P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv"


def utc_stamp() -> str:
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
        ("doc_3721", DOC_3721, "CONDITIONAL_BRIDGE_THEOREM_BUILT_RAW_FREE_ENERGY_GUARD_ADDED", "3721 status"),
        ("next_3721", NEXT_3721, "positive Hessian sign", "3722 handoff"),
        ("theorem_3721", THEOREM_3721, "Raw partition free energy", "raw free-energy guard"),
        ("audit_3721", AUDIT_3721, "AUD3721_3_action_hessian", "operator equality unsigned"),
        ("coeff_3721", COEFF_3721, "DeltaM_map", "retained operator mismatch"),
        ("fisher_3708", FISHER_3708, "Delta F_cg=T_eff D_KL", "KL/free-energy route"),
        ("doublet_517", DOUBLET_517, "Gamma_eff = Gamma0 + 1/2 M_AB", "response-doublet quadratic action"),
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


def kl_legendre_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "KLL3722_0_exponential_family",
            "p_z=p_0 exp[z^A Y_A-W(z)] with W(z)=log E_0 exp[z^A Y_A]",
            "normalization makes W the cumulant generator",
            "THEOREM_TEMPLATE",
        ),
        (
            "KLL3722_1_zero_score",
            "If E_0[Y_A]=0, then partial_A W|0=0 and I_AB=partial_A partial_B W|0=E_0[Y_A Y_B]",
            "Fisher matrix is positive semidefinite",
            "DERIVED",
        ),
        (
            "KLL3722_2_natural_KL",
            "D_KL(p_z||p_0)=z^A partial_A W-W=0.5 I_AB z^A z^B+O(z^3)",
            "natural-parameter coordinate has Hessian I_AB",
            "DERIVED",
        ),
        (
            "KLL3722_3_mean_legendre",
            "m_A:=partial_A W; W_star(m)=sup_z[z^A m_A-W(z)]",
            "mean-response coordinate has Hessian partial_m partial_m W_star|0=I^{-1} on identifiable subspace",
            "DERIVED_IF_I_INVERTIBLE",
        ),
        (
            "KLL3722_4_positive_action",
            "Psi_KL=Theta_H D_KL or Theta_H W_star is positive if Theta_H>0 and I has a positive floor",
            "this is the legitimate sign-owner route",
            "DERIVED_CONDITIONAL",
        ),
        (
            "KLL3722_5_parent_owner_clause",
            "Parent action must contain the information-projection/Legendre penalty as an effective action term, not merely a raw partition function",
            "prevents importing entropy sign by notation",
            "REQUIRED_BEFORE_CLAIM",
        ),
    ]
    return [
        {
            **base(ts),
            "theorem_id": theorem_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "claim_allowed": False,
        }
        for theorem_id, formula, meaning, status in rows
    ]


def raw_free_energy_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "RAW3722_0_raw_partition",
            "F_raw(z)=-Theta log integral exp[-A(z,xi)/Theta] dmu",
            "not equivalent to Theta D_KL unless the variational/Legendre construction is supplied",
            "NOT_A_GAP_SOURCE_BY_ITSELF",
        ),
        (
            "RAW3722_1_hessian",
            "partial_AB F_raw=<A_AB>-(1/Theta)Cov(A_A,A_B)",
            "covariance term has the sign opposite to a naive positive stiffness",
            "SIGN_INDEFINITE",
        ),
        (
            "RAW3722_2_dominance_condition",
            "<A_AB> must dominate (1/Theta)Cov(A_A,A_B) for raw F to be convex",
            "this would be a separate parent theorem, not automatic Fisher positivity",
            "MISSING_DOMINANCE_THEOREM",
        ),
        (
            "RAW3722_3_demote_if_no_owner",
            "If parent only owns raw F_raw and not Psi_KL/Legendre convexity, keep M_AB independent",
            "prevents false local screening gap",
            "DEMOTION_RULE",
        ),
    ]
    return [
        {
            **base(ts),
            "raw_id": raw_id,
            "formula": formula,
            "risk_or_meaning": risk_or_meaning,
            "status": status,
            "claim_allowed": False,
        }
        for raw_id, formula, risk_or_meaning, status in rows
    ]


def coordinate_choice_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "COORD3722_0_natural_branch",
            "Z=z natural parameter",
            "M_AB should match Theta_H I_AB plus DeltaM_map",
            "best if response doublet changes the bath weights/sources directly",
            "UNSIGNED_BRANCH",
        ),
        (
            "COORD3722_1_mean_branch",
            "Z=m=E_z[Y]-E_0[Y] mean response",
            "M_AB should match Theta_H (I^{-1})_AB plus DeltaM_map",
            "best if response doublet is the observed/mean residual amplitude",
            "UNSIGNED_BRANCH",
        ),
        (
            "COORD3722_2_mixed_branch",
            "Z=L z + O(z^2)",
            "M_Z=Theta_H L^{-T} I L^{-1} plus correction terms",
            "most general local coordinate map; needs Jacobian L and units",
            "FINITE_MAP_ROW_REQUIRED",
        ),
        (
            "COORD3722_3_no_choice_no_claim",
            "coordinate type unresolved",
            "both M=Theta I and M=Theta I^{-1} are unsafe as claims",
            "forces M_AB to remain independent nonclaim coefficient",
            "ACTIVE_GUARD",
        ),
    ]
    return [
        {
            **base(ts),
            "coordinate_id": coordinate_id,
            "branch": branch,
            "operator_match": operator_match,
            "when_plausible": when_plausible,
            "status": status,
            "claim_allowed": False,
        }
        for coordinate_id, branch, operator_match, when_plausible, status in rows
    ]


def operator_match_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        ("OPM3722_0_natural_bound", "natural", "DeltaM_nat:=M_AB-Theta_H I_AB", "Xi_H >= lambda_min(Theta_H I)-||DeltaM_nat||-R_loss"),
        ("OPM3722_1_mean_bound", "mean", "DeltaM_mean:=M_AB-Theta_H I^{-1}_AB", "Xi_H >= lambda_min(Theta_H I^{-1})-||DeltaM_mean||-R_loss"),
        ("OPM3722_2_general_jacobian", "mixed", "DeltaM_L:=M_Z-Theta_H L^{-T} I L^{-1}", "Xi_H >= lambda_min(Theta_H L^{-T} I L^{-1})-||DeltaM_L||-R_loss"),
        ("OPM3722_3_response_gap", "independent", "M_AB remains parent response-doublet coefficient", "Xi_H >= lambda_min(M_AB)-R_loss if M_AB positive is separately proved"),
    ]
    return [
        {
            **base(ts),
            "operator_id": operator_id,
            "branch": branch,
            "mismatch": mismatch,
            "gap_bound": gap_bound,
            "status": "BOUND_FORM_NONCLAIM",
            "claim_allowed": False,
        }
        for operator_id, branch, mismatch, gap_bound in rows
    ]


def demotion_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "DEM3722_0_KL_owner_missing",
            "Parent variational principle does not explicitly own Psi_KL or W_star",
            "Do not use Fisher positivity as local screening evidence; retain M_AB.",
        ),
        (
            "DEM3722_1_coordinate_missing",
            "Natural vs mean coordinate not selected",
            "Do not choose M=Theta I or M=Theta I^{-1}; retain coordinate-map residual DeltaM_L.",
        ),
        (
            "DEM3722_2_units_missing",
            "Theta_H, I_H, G_H/U_H units not locked",
            "Do not compare Xi_H to R10/PPN/clock/orbit scales.",
        ),
        (
            "DEM3722_3_boundary_missing",
            "J_Z/B_Z and boundary corrections not theorem-zero",
            "Keep F_loss/QK_loss/R_loss active.",
        ),
    ]
    return [
        {
            **base(ts),
            "demotion_id": demotion_id,
            "trigger": trigger,
            "action": action,
            "status": "NONCLAIM_DEMOTION_RULE",
            "claim_allowed": False,
        }
        for demotion_id, trigger, action in rows
    ]


def decision_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "DEC3722_0_sign_route",
            "KL_LEGENDRE_SIGN_ROUTE_IS_VALID_CONDITIONAL",
            "The positive sign is mathematically clean for Theta_H D_KL or the Legendre dual, assuming Theta_H>0 and identifiable Fisher directions.",
        ),
        (
            "DEC3722_1_raw_route",
            "RAW_FREE_ENERGY_ROUTE_DEMOTED",
            "Raw -Theta log Z is sign-indefinite unless a separate convexity/dominance theorem is supplied.",
        ),
        (
            "DEC3722_2_coordinate_fork",
            "NATURAL_VS_MEAN_COORDINATE_IS_NOW_THE_MAIN_FORK",
            "Response-doublet Z may be a natural bath-source coordinate or a mean residual coordinate, changing M from Theta I to Theta I^{-1}.",
        ),
        (
            "DEC3722_3_next",
            "ADVANCE_TO_COORDINATE_TYPE_AND_OPERATOR_MATCH_OWNER",
            "Next target should decide whether Z is natural, mean, or mixed, then write the correct M_AB match and retained mismatch row.",
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
        ("CG3722_0_KL_owner", "BLOCKED", "parent action owns Psi_KL=Theta_H D_KL or W_star"),
        ("CG3722_1_theta", "BLOCKED", "Theta_H positive and unit-normalized"),
        ("CG3722_2_coordinate", "BLOCKED", "Z coordinate type is natural, mean, or mixed with Jacobian"),
        ("CG3722_3_operator", "BLOCKED", "M_AB match uses the correct I/I^{-1}/Jacobian branch"),
        ("CG3722_4_identifiability", "BLOCKED", "Fisher floor positive on active local subspace"),
        ("CG3722_5_boundary", "BLOCKED", "boundary/source correction budget closed or finite"),
        ("CG3722_6_claim", "BLOCKED", "local gap/screening claim allowed"),
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
        "status_id": "STATUS3722_0",
        "status": "KL_LEGENDRE_SIGN_DERIVED_RAW_FREE_ENERGY_DEMOTED_COORDINATE_FORK_OPEN",
        "summary": "3722 derives the positive KL/Legendre sign route, demotes raw -Theta log Z as sign-indefinite, and exposes natural-vs-mean coordinate choice as the next operator-match fork.",
        "claim_allowed": False,
    }]


def next_target_rows(ts: str) -> list[dict[str, object]]:
    return [{
        **base(ts),
        "next_id": "NEXT3722_0",
        "target_doc": "3723-Y5-R2FR-natural-vs-mean-coordinate-operator-match-owner.md",
        "target_script": "scripts/Y5_R2FR_3723_natural_vs_mean_coordinate_operator_match_owner.py",
        "objective": "decide whether the response-doublet coordinate Z is a natural bath parameter, a mean residual coordinate, or a mixed coordinate map, then derive the correct M_AB match or retain DeltaM_L as a nonclaim coefficient",
        "success_gate": "coordinate type, Jacobian, Theta/I or I^{-1} operator match, units, and retained mismatch are explicitly owned or blocked",
        "claim_allowed": False,
    }]


def validation_rows(ts: str, paths: dict[str, Path]) -> list[dict[str, object]]:
    sources = parse_csv(paths["source_register"])
    csv_paths = [path for key, path in paths.items() if key not in {"doc", "validation"}]
    generated = [path for key, path in paths.items() if key != "validation"]
    formal_files = list(FORMALIZATION.rglob("*3722*")) if FORMALIZATION.exists() else []
    formal_files = [path for path in formal_files if path.is_file()]
    checks = [
        ("sources_exist", "sources exist", all(row["exists"] == "True" for row in sources)),
        ("needles_found", "source needles found", all(row["needle_found"] == "True" for row in sources)),
        ("outputs_exist", "outputs exist", all(path.exists() for path in generated)),
        ("csv_parse", "CSVs parse and are nonempty", all(len(parse_csv(path)) > 0 for path in csv_paths if path.exists())),
        ("kl_theorems", "KL rows include natural and Legendre Hessians", all(token in read_text(paths["kl"]) for token in ["D_KL", "W_star", "I^{-1}"])),
        ("raw_demoted", "raw free energy sign-indefinite guard exists", all(token in read_text(paths["raw"]) for token in ["SIGN_INDEFINITE", "DEMOTION_RULE"])),
        ("coordinate_fork", "natural and mean branches both present", all(token in read_text(paths["coordinates"]) for token in ["Z=z natural", "Z=m=E_z"])),
        ("operator_bounds", "operator bounds include I and I^{-1}", all(token in read_text(paths["operators"]) for token in ["Theta_H I_AB", "Theta_H I^{-1}_AB"])),
        ("claim_gates_blocked", "all claim gates blocked", all(row["gate_status"] == "BLOCKED" and row["claim_allowed"] == "False" for row in parse_csv(paths["claim_gates"]))),
        ("next_target_3723", "next target is 3723", "3723" in read_text(paths["next_target"])),
        ("doc_core_terms", "doc includes sign and coordinate fork", all(token in read_text(paths["doc"]) for token in ["Raw `-Theta log Z`", "M=Theta I", "M=Theta I^{-1}"])),
        ("no_formalization_leak", "no 3722 files written to formalization-workbench", len(formal_files) == 0),
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
        "# 3722 — KL/Legendre Effective Action Sign Owner or Free-Energy Demotion",
        "",
        "## Status",
        "- `KL_LEGENDRE_SIGN_DERIVED_RAW_FREE_ENERGY_DEMOTED_COORDINATE_FORK_OPEN`",
        "- Positive sign is valid for `Psi_KL=Theta_H D_KL` or the Legendre dual, if the parent action owns that effective action and `Theta_H>0`.",
        "- Raw `-Theta log Z` is demoted as a gap source unless a separate convexity theorem is supplied.",
        "- New fork: if `Z` is a natural bath coordinate then `M=Theta I`; if `Z` is a mean/response coordinate then `M=Theta I^{-1}`.",
        "",
        "## Main Result",
        "- Exponential-family route: `D_KL(p_z||p_0)=0.5 I_AB z^A z^B+O(z^3)` gives a positive Hessian in natural coordinates.",
        "- Legendre route: `W_star(m)=sup_z(z*m-W)` gives Hessian `I^{-1}` in mean coordinates.",
        "- Raw free-energy route: `partial_AB F_raw=<A_AB>-(1/Theta)Cov(A_A,A_B)`, so it is not automatically a stable local gap.",
        "- Therefore the local operator match cannot be claimed until the theory chooses natural, mean, or mixed coordinate geometry.",
        "",
        "## KL/Legendre Theorems",
    ]
    for row in grouped["kl"]:
        lines.append(f"- `{row['theorem_id']}` `{row['status']}`: `{row['formula']}` | {row['meaning']}")
    lines.extend(["", "## Raw Free-Energy Audit"])
    for row in grouped["raw"]:
        lines.append(f"- `{row['raw_id']}` `{row['status']}`: `{row['formula']}` | {row['risk_or_meaning']}")
    lines.extend(["", "## Coordinate Choice"])
    for row in grouped["coordinates"]:
        lines.append(f"- `{row['coordinate_id']}` `{row['status']}`: {row['branch']} -> {row['operator_match']} | {row['when_plausible']}")
    lines.extend(["", "## Operator Matches"])
    for row in grouped["operators"]:
        lines.append(f"- `{row['operator_id']}` `{row['branch']}`: {row['mismatch']} | {row['gap_bound']}")
    lines.extend(["", "## Demotion Rules"])
    for row in grouped["demotions"]:
        lines.append(f"- `{row['demotion_id']}` `{row['status']}`: {row['trigger']} -> {row['action']}")
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
        "- `3723-Y5-R2FR-natural-vs-mean-coordinate-operator-match-owner.md`",
        "- Objective: choose or bound the coordinate type before using the Fisher gap in local screening.",
        "",
        "## Validation",
        f"- See `{paths['validation']}`.",
    ])
    paths["doc"].write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ts = utc_stamp()
    paths = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3722_SOURCE_REGISTER.csv",
        "kl": RESIDUALS / "P8_Y5_R2FR_3722_KL_LEGENDRE_THEOREM_ROWS.csv",
        "raw": RESIDUALS / "P8_Y5_R2FR_3722_RAW_FREE_ENERGY_SIGN_AUDIT_ROWS.csv",
        "coordinates": RESIDUALS / "P8_Y5_R2FR_3722_COORDINATE_CHOICE_ROWS.csv",
        "operators": RESIDUALS / "P8_Y5_R2FR_3722_OPERATOR_MATCH_ROWS.csv",
        "demotions": RESIDUALS / "P8_Y5_R2FR_3722_DEMOTION_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3722_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3722_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3722_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3722_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3722_VALIDATION.csv",
        "doc": DOC,
    }
    grouped = {
        "source_register": source_register(ts),
        "kl": kl_legendre_rows(ts),
        "raw": raw_free_energy_rows(ts),
        "coordinates": coordinate_choice_rows(ts),
        "operators": operator_match_rows(ts),
        "demotions": demotion_rows(ts),
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
        raise SystemExit(f"3722 validation failed: {failures}")
    print("wrote 3722 checkpoint: KL/Legendre sign derived; raw free energy demoted; coordinate fork opened")


if __name__ == "__main__":
    main()
