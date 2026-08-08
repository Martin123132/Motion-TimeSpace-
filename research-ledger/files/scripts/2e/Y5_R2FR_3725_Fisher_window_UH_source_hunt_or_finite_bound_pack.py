from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3725"
BRANCH_ID = "MTS_R2FR_Y5_FISHER_WINDOW_UH_SOURCE_HUNT_OR_FINITE_BOUND_PACK_3725"
DOC = ROOT / "3725-Y5-R2FR-Fisher-window-UH-source-hunt-or-finite-bound-pack.md"

DOC_3724 = ROOT / "3724-Y5-R2FR-mean-branch-gap-floor-unit-map-owner.md"
NEXT_3724 = RESIDUALS / "P8_Y5_R2FR_3724_NEXT_TARGET.csv"
LAW_3724 = RESIDUALS / "P8_Y5_R2FR_3724_MEAN_GAP_LAW_ROWS.csv"
INPUT_3724 = RESIDUALS / "P8_Y5_R2FR_3724_REQUIRED_INPUT_ROWS.csv"
FISHER_3708 = RESIDUALS / "P8_Y5_R2FR_3708_FISHER_GAP_DERIVATION_ROWS.csv"
DOC_3253 = ROOT / "3253-Y5-R2FR-parent-ordinary-sector-action-signature-or-C_Tw-component-current-norm-intake-under-AX1090.md"
DOC_2281 = ROOT / "2281-Y5-R2FR-q-stiffness-parent-sector-or-no-go.md"


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


def line_hits(path: Path, terms: tuple[str, ...], limit: int = 4) -> list[str]:
    if not path.exists():
        return []
    hits: list[str] = []
    lower_terms = tuple(term.lower() for term in terms)
    for line_number, line in enumerate(read_text(path).splitlines(), 1):
        lower_line = line.lower()
        if any(term in lower_line for term in lower_terms):
            hits.append(f"L{line_number}:{line.strip()[:260]}")
        if len(hits) >= limit:
            break
    return hits


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("doc_3724", DOC_3724, "MEAN_GAP_LAW_DERIVED_FISHER_CEILING_AND_UNIT_MAP_REQUIRED", "3724 status"),
        ("next_3724", NEXT_3724, "theta_min, iota_min, iota_max, u_min", "3725 handoff"),
        ("law_3724", LAW_3724, "Theta_min/iota_max", "mean gap law"),
        ("input_3724", INPUT_3724, "MISSING_FISHER_CEILING", "required input rows"),
        ("fisher_3708", FISHER_3708, "I_AB^perp", "Fisher symbolic source"),
        ("doc_3253", DOC_3253, "lambda_max(G_J,G_Sigma)", "finite Gram/eigenvalue pattern"),
        ("doc_2281", DOC_2281, "lambda_min(L_q)", "coercive response bound pattern"),
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


def automated_hit_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("theta_min", ("Theta_H", "T_eff", "theta_min", "Theta_min")),
        ("iota_min", ("iota_H", "lambda_min", "I_H", "Fisher")),
        ("iota_max", ("iota_max", "lambda_max", "trace", "Gram")),
        ("U_H", ("U_H", "unit map", "same-basis", "operator units")),
        ("DeltaM_mean", ("DeltaM_mean", "DeltaM", "operator mismatch")),
        ("R_loss", ("R_loss", "R_domain", "R_source", "R_boundary")),
    ]
    files = [DOC_3724, LAW_3724, INPUT_3724, FISHER_3708, DOC_3253, DOC_2281]
    rows: list[dict[str, object]] = []
    for quantity, terms in specs:
        for path in files:
            hits = line_hits(path, terms)
            if hits:
                rows.append({
                    **base(ts),
                    "quantity": quantity,
                    "path": str(path),
                    "terms": ";".join(terms),
                    "hit_count": len(hits),
                    "snippets": " || ".join(hits),
                    "claim_allowed": False,
                })
    return rows


def adjudication_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        ("ADJ3725_0_theta_min", "Theta_min", "SYMBOLIC_ONLY", "3708/3724 give Theta_H/T_eff symbols but no parent-owned positive numeric/unit lower bound.", "derive scale from parent KL/Legendre action or keep finite row"),
        ("ADJ3725_1_iota_min", "iota_min", "FORMULA_ONLY", "3708 defines Fisher lower/eigenvalue language, but no coercivity proof for active score directions.", "derive Gram lower bound or retain missing invertibility row"),
        ("ADJ3725_2_iota_max", "iota_max", "MISSING_NEW_INPUT", "3724 shows this is mandatory for mean branch; corpus has lambda_max patterns in other sectors but no Fisher ceiling.", "derive score-norm ceiling Trace(I)<=Y2_max"),
        ("ADJ3725_3_UH", "U_H/u_min", "MISSING", "No same-basis unit map from Fisher Hessian to local m^-2 operator was found.", "construct U_H from field metric/residual projection or keep blocked"),
        ("ADJ3725_4_DeltaM_mean", "DeltaM_mean", "MISSING", "No source-owned mismatch between response-doublet M_Z and Theta_H I^{-1} exists.", "retain finite operator mismatch row"),
        ("ADJ3725_5_R_loss", "R_loss", "PARTIAL_SYMBOLIC", "Domain/source/boundary loss rows exist in neighbouring branches but no mean-branch combined bound is sourced.", "assemble R_loss from domain/source/boundary rows if available"),
        ("ADJ3725_6_verdict", "mean branch source pack", "NOT_CLAIM_READY", "No required input is currently source-owned enough to score Xi_loc.", "advance to finite score-Gram/U_H owner route"),
    ]
    return [
        {
            **base(ts),
            "adjudication_id": adjudication_id,
            "quantity": quantity,
            "status": status,
            "evidence_summary": evidence_summary,
            "next_action": next_action,
            "claim_allowed": False,
        }
        for adjudication_id, quantity, status, evidence_summary, next_action in rows
    ]


def gram_route_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "GRAM3725_0_score_gram",
            "I_AB=<Y_A,Y_B>_0",
            "Fisher matrix is a Gram matrix of score variables in the p_0 bath inner product.",
            "DERIVED_ROUTE",
        ),
        (
            "GRAM3725_1_ceiling_trace",
            "iota_max <= Tr(I)=sum_A ||Y_A||_0^2",
            "finite score norms give the Fisher ceiling required by the mean branch.",
            "DERIVED_BOUND",
        ),
        (
            "GRAM3725_2_ceiling_uniform",
            "If ||Y_A||_0 <= Y_max and dim K_act=N, then iota_max <= N Y_max^2",
            "coarse but sourceable ceiling when only per-component score bounds exist.",
            "DERIVED_BOUND",
        ),
        (
            "GRAM3725_3_floor_coercivity",
            "iota_min = inf_{||a||=1}<a^A Y_A,a^B Y_B>_0",
            "invertibility requires no active response direction has zero score.",
            "COERCIVITY_TARGET",
        ),
        (
            "GRAM3725_4_finite_matrix",
            "For finite active basis, compute eigenvalues of G_Y=(<Y_A,Y_B>_0)",
            "turns iota_min/iota_max into an eigenvalue problem rather than vibes.",
            "RUNNER_READY_CONCEPT",
        ),
    ]
    return [
        {
            **base(ts),
            "route_id": route_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "claim_allowed": False,
        }
        for route_id, formula, meaning, status in rows
    ]


def finite_pack_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        ("FP3725_0_theta_min", "Theta_min", "positive lower KL/Legendre scale", "MISSING_PARENT_SOURCE", "feeds numerator of Xi_loc"),
        ("FP3725_1_iota_min", "iota_min", "lambda_min(G_Y)", "MISSING_SCORE_GRAM", "needed for I^{-1} to exist"),
        ("FP3725_2_iota_max", "iota_max", "lambda_max(G_Y) or trace ceiling", "MISSING_SCORE_GRAM_OR_TRACE_BOUND", "controls mean-branch gap floor"),
        ("FP3725_3_u_min", "u_min", "smallest singular/coercivity value of U_H", "MISSING_UNIT_MAP", "maps abstract Hessian to local operator"),
        ("FP3725_4_DeltaM_mean", "||DeltaM_mean||", "operator mismatch norm", "MISSING_OPERATOR_MATCH_BOUND", "subtracts from gap"),
        ("FP3725_5_R_loss", "R_loss", "R_domain+R_source+R_boundary+even correction losses", "MISSING_COMBINED_LOSS_BOUND", "subtracts from gap"),
        ("FP3725_6_R_U", "R_U", "unit-map/projection remainder", "MISSING_UNIT_REMAINDER_BOUND", "subtracts after local conversion"),
        ("FP3725_7_Xi_loc", "Xi_loc", "u_min^2*(Theta_min/iota_max-DeltaM_mean-R_loss)-R_U", "BLOCKED_SYMBOLIC", "only scoreable when all upstream rows are finite"),
    ]
    return [
        {
            **base(ts),
            "pack_id": pack_id,
            "quantity": quantity,
            "definition": definition,
            "status": status,
            "local_impact": local_impact,
            "claim_allowed": False,
        }
        for pack_id, quantity, definition, status, local_impact in rows
    ]


def decision_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        ("DEC3725_0_no_claim", "NO_MEAN_BRANCH_INPUTS_SOURCE_OWNED", "The source hunt did not find claim-ready Theta/Fisher-window/U_H/correction inputs."),
        ("DEC3725_1_real_progress", "FINITE_GRAM_ROUTE_SELECTED", "iota_min and iota_max can be turned into a score-Gram eigenvalue problem, which is concrete and testable."),
        ("DEC3725_2_ceiling_priority", "IOTA_MAX_IS_NOW_FIRST_MEAN_BRANCH_TARGET", "Without iota_max the mean-branch lower gap cannot be computed even if iota_min exists."),
        ("DEC3725_3_next", "ADVANCE_TO_SCORE_GRAM_COHERCIVITY_RUNNER", "Next target should define the active score basis Y_A and produce a Gram/eigenvalue schema or theorem-zero demotion."),
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
        ("CG3725_0_score_basis", "BLOCKED", "active score variables Y_A and bath inner product are parent-owned"),
        ("CG3725_1_gram", "BLOCKED", "G_Y matrix or theorem bounds provide iota_min and iota_max"),
        ("CG3725_2_theta", "BLOCKED", "Theta_min source-owned with units"),
        ("CG3725_3_UH", "BLOCKED", "U_H and u_min source-owned with local units"),
        ("CG3725_4_losses", "BLOCKED", "DeltaM_mean, R_loss, and R_U finite or theorem-zero"),
        ("CG3725_5_Xi", "BLOCKED", "Xi_loc positive and scoreable"),
        ("CG3725_6_claim", "BLOCKED", "local screening claim allowed"),
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
        "status_id": "STATUS3725_0",
        "status": "SOURCE_HUNT_NO_CLAIM_FINITE_SCORE_GRAM_ROUTE_READY",
        "summary": "3725 finds no claim-ready mean-branch inputs, but converts the Fisher window into a concrete score-Gram eigenvalue route: iota_min/lambda_min and iota_max/lambda_max of G_Y.",
        "claim_allowed": False,
    }]


def next_target_rows(ts: str) -> list[dict[str, object]]:
    return [{
        **base(ts),
        "next_id": "NEXT3725_0",
        "target_doc": "3726-Y5-R2FR-score-Gram-coercivity-runner-or-symbolic-window-lock.md",
        "target_script": "scripts/Y5_R2FR_3726_score_Gram_coercivity_runner_or_symbolic_window_lock.py",
        "objective": "define the active score basis Y_A, bath inner product, finite Gram matrix schema, and eigenvalue window needed for iota_min/iota_max; otherwise lock the Fisher window as symbolic nonclaim rows",
        "success_gate": "score basis and Gram matrix are executable, or the Fisher window remains explicitly blocked with no local screening promotion",
        "claim_allowed": False,
    }]


def validation_rows(ts: str, paths: dict[str, Path]) -> list[dict[str, object]]:
    sources = parse_csv(paths["source_register"])
    csv_paths = [path for key, path in paths.items() if key not in {"doc", "validation"}]
    generated = [path for key, path in paths.items() if key != "validation"]
    formal_files = list(FORMALIZATION.rglob("*3725*")) if FORMALIZATION.exists() else []
    formal_files = [path for path in formal_files if path.is_file()]
    checks = [
        ("sources_exist", "sources exist", all(row["exists"] == "True" for row in sources)),
        ("needles_found", "source needles found", all(row["needle_found"] == "True" for row in sources)),
        ("outputs_exist", "outputs exist", all(path.exists() for path in generated)),
        ("csv_parse", "CSVs parse", all(len(parse_csv(path)) > 0 for path in csv_paths if path.exists())),
        ("hunt_rows", "automated hunt rows exist", len(parse_csv(paths["hits"])) > 0),
        ("adjudication", "adjudication includes no-claim verdict", "NOT_CLAIM_READY" in read_text(paths["adjudication"])),
        ("gram_route", "Gram route includes lambda max ceiling", all(token in read_text(paths["gram"]) for token in ["iota_max <= Tr(I)", "eigenvalues of G_Y"])),
        ("finite_pack", "finite pack includes all mean inputs", all(token in read_text(paths["finite_pack"]) for token in ["Theta_min", "iota_max", "u_min", "Xi_loc"])),
        ("claim_gates_blocked", "all claim gates blocked", all(row["gate_status"] == "BLOCKED" and row["claim_allowed"] == "False" for row in parse_csv(paths["claim_gates"]))),
        ("next_target_3726", "next target is 3726", "3726" in read_text(paths["next_target"])),
        ("doc_core_terms", "doc contains no-claim and Gram route", all(token in read_text(paths["doc"]) for token in ["no claim-ready", "score-Gram", "iota_max"])),
        ("no_formalization_leak", "no 3725 files in formalization-workbench", len(formal_files) == 0),
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
        "# 3725 — Fisher Window / U_H Source Hunt or Finite Bound Pack",
        "",
        "## Status",
        "- `SOURCE_HUNT_NO_CLAIM_FINITE_SCORE_GRAM_ROUTE_READY`",
        "- The hunt found no claim-ready `Theta_min`, `iota_min`, `iota_max`, `U_H`, or correction-loss row.",
        "- The useful advance is the score-Gram route: `I_AB=<Y_A,Y_B>_0`, so `iota_min=lambda_min(G_Y)` and `iota_max=lambda_max(G_Y)` or a trace ceiling.",
        "- This keeps the mean branch alive without smuggling a local screening pass.",
        "",
        "## Source Adjudication",
    ]
    for row in grouped["adjudication"]:
        lines.append(f"- `{row['adjudication_id']}` `{row['status']}` — {row['quantity']}: {row['evidence_summary']} Next: {row['next_action']}.")
    lines.extend(["", "## Score-Gram Route"])
    for row in grouped["gram"]:
        lines.append(f"- `{row['route_id']}` `{row['status']}`: `{row['formula']}` | {row['meaning']}")
    lines.extend(["", "## Finite Bound Pack"])
    for row in grouped["finite_pack"]:
        lines.append(f"- `{row['pack_id']}` `{row['quantity']}`: {row['definition']} | {row['status']} | impact: {row['local_impact']}")
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
        "## Automated Hit Rows",
        f"- See `{paths['hits']}`.",
        "",
        "## Next Target",
        "- `3726-Y5-R2FR-score-Gram-coercivity-runner-or-symbolic-window-lock.md`",
        "- Objective: define the score basis and Gram matrix schema, or lock the Fisher window as symbolic.",
        "",
        "## Validation",
        f"- See `{paths['validation']}`.",
    ])
    paths["doc"].write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ts = stamp()
    paths = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3725_SOURCE_REGISTER.csv",
        "hits": RESIDUALS / "P8_Y5_R2FR_3725_AUTOMATED_HIT_ROWS.csv",
        "adjudication": RESIDUALS / "P8_Y5_R2FR_3725_SOURCE_ADJUDICATION_ROWS.csv",
        "gram": RESIDUALS / "P8_Y5_R2FR_3725_SCORE_GRAM_ROUTE_ROWS.csv",
        "finite_pack": RESIDUALS / "P8_Y5_R2FR_3725_FINITE_BOUND_PACK_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3725_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3725_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3725_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3725_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3725_VALIDATION.csv",
        "doc": DOC,
    }
    grouped = {
        "source_register": source_register(ts),
        "hits": automated_hit_rows(ts),
        "adjudication": adjudication_rows(ts),
        "gram": gram_route_rows(ts),
        "finite_pack": finite_pack_rows(ts),
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
        raise SystemExit(f"3725 validation failed: {failures}")
    print("wrote 3725 checkpoint: no claim-ready inputs; score-Gram route staged")


if __name__ == "__main__":
    main()
