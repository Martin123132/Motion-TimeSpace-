from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3696"
BRANCH_ID = "MTS_R2FR_Y5_U1_ORIGIN_FROM_RELAXATION_FUNCTIONAL_OR_LOCAL_SCREENING_CLOSURE_3696"
DOC = ROOT / "3696-Y5-R2FR-u1-origin-from-relaxation-functional-or-local-screening-closure.md"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(timestamp: str) -> dict[str, object]:
    return {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("handoff_3695", RESIDUALS / "P8_Y5_R2FR_3695_NEXT_TARGET.csv", "u_1"),
        ("hessian_3695", RESIDUALS / "P8_Y5_R2FR_3695_HESSIAN_EXTRACTION_ROWS.csv", "2 u_1 G_AB"),
        ("mu_3695", RESIDUALS / "P8_Y5_R2FR_3695_SYMBOLIC_MUH_ROWS.csv", "mu_H^2 = 2u_1"),
        ("equations_register", FORMALIZATION / "05-equation-register.md", "F_2 = a_F lambda_R"),
        ("variable_audit_Rlock", FORMALIZATION / "04-variable-audit.csv", "R=R_L+0.5 lambda_R"),
        ("scalar_evenness_126", FORMALIZATION / "126-scalar-evenness-origin.md", "scalar evenness is theorem-shaped"),
        ("signed_map_127", FORMALIZATION / "127-signed-leakage-coordinate-map.md", "a_A z_L^A"),
        ("leakage_invariant_125", FORMALIZATION / "125-local-leakage-vector-invariant.md", "s_L = D_L^2"),
    ]
    rows = []
    for source_id, path, needle in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                **base(timestamp),
                "source_id": source_id,
                "path": str(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": "u1-origin/no-go input",
            }
        )
    return rows


def u1_origin_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "UOR3696_0_Rlock_memory",
            "scalar memory relaxation lock",
            "R(m;X_B)=R_L+0.5 lambda_R(m-m_L)^2+O((m-m_L)^3), F=F_L+a_F[R-R_L]",
            "This existing route explains F1=0 and F2=a_F lambda_R for the trace projection.",
            "SOURCE_CONFIRMED_CONDITIONAL",
            "R_Rlock_parent",
        ),
        (
            "UOR3696_1_chain_Hessian",
            "R-lock contribution to z-Hessian",
            "partial_A partial_B U_R|_0 = a_R[lambda_R m_A m_B + R_m m_AB]|_0 = a_R lambda_R m_A m_B",
            "At the fixed point R_m=0, so only the first derivative m_A:=partial_A m|_0 can give a quadratic z mass.",
            "DERIVED_CHAIN_RULE",
            "R_mA_map",
        ),
        (
            "UOR3696_2_even_m_no_gap",
            "even scalar memory map",
            "if m(z)=m_L+c_1 s_L+O(s_L^2), then m_A=0 and R(m(z))-R_L=0.5 lambda_R c_1^2 s_L^2+O(s_L^3)",
            "The scalar R-lock is quartic in z and gives no quadratic horizontal mass gap: u_1^R=0.",
            "NO_GO_FOR_U1_FROM_EVEN_SCALAR_RLOCK",
            "R_u1_Rlock_zero",
        ),
        (
            "UOR3696_3_linear_m_route",
            "linear memory map route",
            "if m(z)=m_L+b_A z^A+O(z^2), then M_AB^R=a_R lambda_R b_A b_B",
            "This can produce a mass term, but it breaks the scalar-evenness/parity route unless b_A z^A is vertical, gauge-hidden, or otherwise unobservable.",
            "POSSIBLE_BUT_DANGEROUS_RANK_AND_PARITY_ROUTE",
            "R_linear_memory_leak",
        ),
        (
            "UOR3696_4_direct_leakage_penalty",
            "direct horizontal leakage penalty",
            "U_Z(z;X_B)=u_1(X_B,local_state)s_L+O(s_L^2)",
            "This is the clean full-rank route to M_H=2u_1G_H. It is not derived by the scalar R-lock; it must be a parent action/coarse-graining/entropy penalty.",
            "BEST_ROUTE_NOT_PARENT_DERIVED",
            "R_UZ_parent",
        ),
        (
            "UOR3696_5_verdict",
            "u1 origin verdict",
            "current R(m;X_B) lock does not by itself derive u_1>0 for the horizontal mass gap under the same evenness assumptions that protect local PPN",
            "Local screening therefore needs either a direct parent leakage penalty, a safe linear-memory map, or explicit closure/Yukawa phenomenology.",
            "U1_NOT_DERIVED_DIRECT_LEAKAGE_PENALTY_REQUIRED",
            "R_u1_origin",
        ),
    ]
    return [
        {
            **base(timestamp),
            "origin_id": origin_id,
            "route": route,
            "formula": formula,
            "derivation": derivation,
            "status": status,
            "residual_if_failed": residual,
            "claim_allowed": False,
        }
        for origin_id, route, formula, derivation, status, residual in specs
    ]


def direct_penalty_contract_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "DPC3696_0_action_term",
            "parent leakage penalty",
            "S_leak = -int sqrt(-g) u_1(X_B,rho,theta,J_phys) G_AB z^A z^B + O(z^4)",
            "Must be present before local screening can be derived rather than fitted.",
            "CONTRACT_REQUIRED",
        ),
        (
            "DPC3696_1_symmetry",
            "leakage-frame parity",
            "S_leak[z]=S_leak[-z]",
            "Forbids dangerous linear source terms while allowing quadratic mass.",
            "CONTRACT_REQUIRED",
        ),
        (
            "DPC3696_2_positivity",
            "positive local curvature",
            "u_1(local)>0 and G_H>0",
            "Gives mu_H^2=2u_1-corrections on the clean branch.",
            "CONTRACT_REQUIRED",
        ),
        (
            "DPC3696_3_environment",
            "local/cosmic separation",
            "u_1(local) large enough for local tests while u_1(gal/cos) does not erase intended long-range response",
            "Prevents solving Solar physics by killing the galaxy/cosmology pillars.",
            "CONTRACT_REQUIRED",
        ),
        (
            "DPC3696_4_source_silence",
            "ordinary-sector safety",
            "partial_z S_matter=0 and no hidden z-dependent masses/charges except quotient-owned terms",
            "Prevents the new leakage penalty from reintroducing WEP/clock/EM failures.",
            "CONTRACT_REQUIRED",
        ),
    ]
    return [
        {
            **base(timestamp),
            "contract_id": contract_id,
            "clause": clause,
            "formula": formula,
            "why_it_matters": why,
            "status": status,
            "claim_allowed": False,
        }
        for contract_id, clause, formula, why, status in specs
    ]


def route_score_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "RS3696_0_scalar_Rlock",
            "scalar R-lock only",
            "u_1^R=0 if m-m_L=O(s_L)",
            "keeps F1=0 but does not supply a quadratic local mass gap",
            "REJECT_AS_SOLE_MASS_GAP_ORIGIN",
        ),
        (
            "RS3696_1_linear_memory",
            "linear memory map",
            "M_AB=a_R lambda_R b_A b_B",
            "can give rank-limited mass but threatens parity/source leakage and may not gap all horizontal modes",
            "HIGH_SCRUTINY_ROUTE",
        ),
        (
            "RS3696_2_direct_penalty",
            "direct leakage penalty",
            "M_AB=2u_1G_AB",
            "cleanest route if parent action/coarse-graining derives u_1 and ordinary-sector silence",
            "BEST_NEXT_ROUTE",
        ),
        (
            "RS3696_3_closure",
            "closure/Yukawa branch",
            "u_1 declared or fitted, lambda_H=1/sqrt(2u_1-corrections)",
            "usable only as nonclaim phenomenology until parent origin is supplied",
            "FALLBACK_NONCLAIM",
        ),
    ]
    return [
        {
            **base(timestamp),
            "route_id": route_id,
            "route": route,
            "mass_formula": mass_formula,
            "assessment": assessment,
            "status": status,
            "claim_allowed": False,
        }
        for route_id, route, mass_formula, assessment, status in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "DEC3696_0",
            "Scalar R-lock no-go",
            "The same evenness that protects local PPN makes scalar R(m) quartic in z, so it cannot alone produce u_1.",
            "NO_GO_ADOPTED",
        ),
        (
            "DEC3696_1",
            "Direct penalty is the clean target",
            "The next derivation should seek a parent/coarse-grained entropy or Onsager penalty proportional to s_L.",
            "NEXT_ROUTE_SELECTED",
        ),
        (
            "DEC3696_2",
            "No claim",
            "u_1 remains unsigned; local screening remains conditional or closure-only.",
            "CLAIM_BLOCKED",
        ),
    ]
    return [
        {**base(timestamp), "decision_id": decision_id, "decision": decision, "rationale": rationale, "status": status}
        for decision_id, decision, rationale, status in specs
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("CG3696_0_u1", "u_1 not derived from scalar R-lock under evenness", "BLOCKED"),
        ("CG3696_1_penalty", "direct leakage penalty not parent-signed", "BLOCKED"),
        ("CG3696_2_source_silence", "ordinary matter/EM/source silence under z not proved", "BLOCKED"),
        ("CG3696_3_environment", "local/cosmic/galaxy u_1 separation not derived", "BLOCKED"),
        ("CG3696_4_local_GR", "local GR screening still awaits sourced u_1 and arena projections", "BLOCKED"),
        ("CG3696_5_public", "private checkpoint only; no public/GitHub claim", "BLOCKED"),
    ]
    return [
        {**base(timestamp), "gate_id": gate_id, "gate": gate, "status": status, "claim_allowed": False}
        for gate_id, gate, status in specs
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "status_id": "STATUS3696_0",
            "status": "SCALAR_RLOCK_DOES_NOT_DERIVE_U1_UNDER_EVENNESS_DIRECT_LEAKAGE_PENALTY_REQUIRED",
            "summary": "The R(m;X_B) lock still helps the trace branch by giving F1=0, but under scalar-even leakage variables it contributes only quartic z stiffness and no quadratic horizontal mass gap. A separate parent-derived leakage penalty U_Z=u_1 s_L, or a risky linear-memory route, is required for local screening.",
            "claim_allowed": False,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "next_id": "NEXT3696_0",
            "target_doc": "3697-Y5-R2FR-direct-leakage-penalty-from-coarse-graining-Onsager-or-closure.md",
            "target_script": "scripts/Y5_R2FR_3697_direct_leakage_penalty_from_coarse_graining_Onsager_or_closure.py",
            "objective": "try to derive the direct quadratic leakage penalty U_Z=u_1 s_L from coarse-graining entropy, Onsager dissipation, or parent variational stability; if not, mark u_1 as closure-only and pass it to the nonclaim Yukawa runner",
            "success_gate": "u_1 is parent-derived with positivity, units, environment dependence and ordinary-sector silence, or local mass-gap screening is explicitly closure-only",
            "claim_allowed": False,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    origin: list[dict[str, object]],
    contracts: list[dict[str, object]],
    routes: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3696 - u1 origin from relaxation functional or local screening closure",
        "",
        "Private checkpoint. No GitHub action. No local-GR/Newton/R10/PPN/EM claim.",
        "",
        "## Status",
        f"- `{status[0]['status']}`",
        f"- {status[0]['summary']}",
        "",
        "## Main Result",
        "- The scalar relaxation lock `R(m;X_B)` still matters: it can lock `F1=0` and give `F2=a_F lambda_R`.",
        "- But under the same scalar-evenness route used for local safety, `m(z)-m_L=O(s_L)` with `s_L=G_AB z^A z^B`.",
        "- Then `R(m(z))-R_L = 0.5 lambda_R O(s_L^2)`, which is quartic in `z`, so it gives `u_1^R=0`.",
        "- Therefore scalar R-lock alone does **not** derive the quadratic horizontal mass gap.",
        "",
        "## Route Split",
        "- Safe/even route: protects local trace/source behavior but does not generate `u_1`.",
        "- Linear-memory route: can generate `M_AB=a_R lambda_R b_A b_B`, but threatens parity and only gaps the directions spanned by `b_A`.",
        "- Direct penalty route: `U_Z=u_1 s_L+O(s_L^2)` gives `M_AB=2u_1G_AB`; this is the clean target, but must be parent-derived.",
        "",
        "## Direct Penalty Contract",
        "- Needed term: `S_leak = -int sqrt(-g) u_1(X_B,rho,theta,J_phys) G_AB z^A z^B + O(z^4)`.",
        "- Required gates: parity, positive `G_H`, positive local `u_1`, bounded corrections, environment dependence, and ordinary-sector silence.",
        "",
        "## u1 Origin Rows",
    ]
    for row in origin:
        lines.append(f"- `{row['origin_id']}`: {row['route']} | `{row['status']}` | {row['formula']}")
    lines.extend(["", "## Direct Penalty Contract Rows"])
    for row in contracts:
        lines.append(f"- `{row['contract_id']}`: {row['clause']} | `{row['status']}` | {row['formula']}")
    lines.extend(["", "## Route Scores"])
    for row in routes:
        lines.append(f"- `{row['route_id']}`: {row['route']} | `{row['status']}` | {row['mass_formula']}")
    lines.extend(["", "## Decisions"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: `{row['status']}` - {row['rationale']}")
    lines.extend(["", "## Claim Gates"])
    for row in claim_gates:
        lines.append(f"- `{row['gate_id']}`: `{row['status']}` - {row['gate']}")
    lines.extend(["", "## Source Register"])
    for row in sources:
        lines.append(f"- `{row['source_id']}`: exists={row['exists']}, needle_found={row['needle_found']}, path=`{row['path']}`")
    lines.extend(["", "## Next Target"])
    lines.append(f"- `{next_target[0]['target_doc']}`")
    lines.append(f"- Objective: {next_target[0]['objective']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(
    timestamp: str,
    generated_paths: list[Path],
    sources: list[dict[str, object]],
    origin: list[dict[str, object]],
    contracts: list[dict[str, object]],
    routes: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    def row(check_id: str, result: bool, detail: str) -> dict[str, object]:
        return {**base(timestamp), "check_id": check_id, "result": "PASS" if result else "FAIL", "detail": detail}

    parsed_ok = True
    parse_details = []
    for path in generated_paths:
        if path.suffix.lower() == ".csv":
            try:
                parse_csv(path)
                parse_details.append(f"{path.name}:ok")
            except Exception as exc:  # noqa: BLE001
                parsed_ok = False
                parse_details.append(f"{path.name}:{exc}")

    doc_text = read_text(DOC) if DOC.exists() else ""
    source_ok = all(bool(source["exists"]) for source in sources)
    needles_ok = all(bool(source["needle_found"]) for source in sources)
    no_leak = not any(FORMALIZATION.rglob("*3696*"))
    nogo_ok = any(row_data["origin_id"] == "UOR3696_2_even_m_no_gap" and row_data["status"] == "NO_GO_FOR_U1_FROM_EVEN_SCALAR_RLOCK" for row_data in origin)
    direct_ok = any(row_data["origin_id"] == "UOR3696_4_direct_leakage_penalty" and "u_1" in row_data["formula"] for row_data in origin)
    route_ok = any(row_data["route_id"] == "RS3696_2_direct_penalty" and row_data["status"] == "BEST_NEXT_ROUTE" for row_data in routes)
    contract_ok = {row_data["contract_id"] for row_data in contracts} == {"DPC3696_0_action_term", "DPC3696_1_symmetry", "DPC3696_2_positivity", "DPC3696_3_environment", "DPC3696_4_source_silence"}
    gates_blocked = all(row_data["status"] == "BLOCKED" for row_data in claim_gates)
    nonclaim = all(
        not bool(row_data.get("valid_for_claim"))
        for table in [sources, origin, contracts, routes, decisions, claim_gates, status, next_target]
        for row_data in table
    )
    next_ok = str(next_target[0]["target_doc"]).startswith("3697-") and "leakage-penalty" in str(next_target[0]["target_doc"])
    doc_ok = all(needle in doc_text for needle in ["u_1^R=0", "scalar R-lock alone", "U_Z=u_1 s_L", "Direct Penalty Contract"])

    return [
        row("VAL3696_0_sources_exist", source_ok, "all input source files exist"),
        row("VAL3696_1_needles_found", needles_ok, "all source needles found"),
        row("VAL3696_2_outputs_exist", all(path.exists() for path in generated_paths), "all generated outputs exist"),
        row("VAL3696_3_csv_parse", parsed_ok, "; ".join(parse_details)),
        row("VAL3696_4_even_Rlock_nogo", nogo_ok, "scalar even R-lock no-go row present"),
        row("VAL3696_5_direct_penalty_route", direct_ok and route_ok, "direct leakage penalty selected as best route"),
        row("VAL3696_6_contract_rows", contract_ok, "direct penalty contract complete"),
        row("VAL3696_7_claim_gates_blocked", gates_blocked, "all claim gates remain blocked"),
        row("VAL3696_8_all_nonclaim", nonclaim, "all tables remain nonclaim"),
        row("VAL3696_9_next_target", next_ok, "3697 direct leakage penalty target selected"),
        row("VAL3696_10_doc_written", doc_ok, "doc contains no-go and direct penalty route"),
        row("VAL3696_11_no_formalization_leak", no_leak, "no 3696 files under formalization-workbench"),
    ]


def main() -> int:
    timestamp = stamp()
    sources = source_register(timestamp)
    origin = u1_origin_rows(timestamp)
    contracts = direct_penalty_contract_rows(timestamp)
    routes = route_score_rows(timestamp)
    decisions = decision_rows(timestamp)
    claim_gates = claim_gate_rows(timestamp)
    status = status_rows(timestamp)
    next_target = next_rows(timestamp)

    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3696_SOURCE_REGISTER.csv",
        "origin": RESIDUALS / "P8_Y5_R2FR_3696_U1_ORIGIN_ROWS.csv",
        "contracts": RESIDUALS / "P8_Y5_R2FR_3696_DIRECT_PENALTY_CONTRACT_ROWS.csv",
        "routes": RESIDUALS / "P8_Y5_R2FR_3696_ROUTE_SCORE_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3696_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3696_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3696_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3696_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3696_VALIDATION.csv",
    }

    write_csv(outputs["sources"], sources)
    write_csv(outputs["origin"], origin)
    write_csv(outputs["contracts"], contracts)
    write_csv(outputs["routes"], routes)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["claim_gates"], claim_gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, origin, contracts, routes, decisions, claim_gates, status, next_target)

    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(timestamp, generated_paths, sources, origin, contracts, routes, decisions, claim_gates, status, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3696 validation failed: {failures}", file=sys.stderr)
        return 1
    print("wrote 3696 checkpoint: scalar R-lock no-go for u1; direct leakage penalty route selected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
