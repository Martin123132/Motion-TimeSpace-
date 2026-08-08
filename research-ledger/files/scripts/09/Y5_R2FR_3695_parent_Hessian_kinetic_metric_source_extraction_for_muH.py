from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3695"
BRANCH_ID = "MTS_R2FR_Y5_PARENT_HESSIAN_KINETIC_METRIC_SOURCE_EXTRACTION_FOR_MUH_3695"
DOC = ROOT / "3695-Y5-R2FR-parent-Hessian-kinetic-metric-source-extraction-for-muH.md"


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
        ("handoff_3694", RESIDUALS / "P8_Y5_R2FR_3694_NEXT_TARGET.csv", "parent scalar/action Hessian"),
        ("gap_3694", RESIDUALS / "P8_Y5_R2FR_3694_PARENT_MASS_GAP_ROWS.csv", "M_eff,H"),
        ("operator_3693", RESIDUALS / "P8_Y5_R2FR_3693_HORIZONTAL_OPERATOR_ROWS.csv", "L_H"),
        ("fixed_point_124", FORMALIZATION / "124-fixed-point-extremality-origin.md", "m_AB Z_L^A Z_L^B"),
        ("leakage_invariant_125", FORMALIZATION / "125-local-leakage-vector-invariant.md", "G_AB = diag(w_A)"),
        ("scalar_evenness_126", FORMALIZATION / "126-scalar-evenness-origin.md", "s_L = G_AB Z_L^A Z_L^B"),
        ("signed_coordinates_127", FORMALIZATION / "127-signed-leakage-coordinate-map.md", "z_L^A -> -z_L^A"),
        ("metric_null_138", FORMALIZATION / "138-metric-null-action-block-contract.md", "S_parent"),
        ("clean_action_3686", ROOT / "3686-Y5-R2FR-GK-q_loc-action-existence-Helmholtz-or-RGK-action-bound-row.md", "S_GK^clean"),
        ("helmholtz_3687", ROOT / "3687-Y5-R2FR-clean-response-action-Helmholtz-matrix-or-DeltaK-bound-row.md", "M_AB=M_BA"),
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
                "role": "Hessian/kinetic metric extraction input",
            }
        )
    return rows


def extraction_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "HEX3695_0_signed_coordinates",
            "signed horizontal coordinates",
            "z^A are primitive signed leakage/response coordinates with reflection z^A -> -z^A",
            "Needed before scalar evenness can forbid linear local response terms.",
            "CANDIDATE_FROM_127_NOT_PARENT_SIGNED",
            "R_signed_z",
        ),
        (
            "HEX3695_1_kinetic_metric",
            "positive kinetic/leakage metric",
            "s_L := G_AB z^A z^B, G_AB=G_BA, G_H,IJ=H_I^A G_AB H_J^B",
            "This supplies the horizontal norm and the kinetic metric entering the mass-gap eigenvalue.",
            "CANDIDATE_FROM_125_126_NOT_PARENT_SIGNED",
            "R_GH_positive",
        ),
        (
            "HEX3695_2_even_scalar_potential",
            "even scalar response potential",
            "U_H(z,Y)=U_0(Y)+u_1(Y)s_L+u_2(Y)s_L^2+O(s_L^3)",
            "Parity/isotropy collapses the local potential to scalar powers of s_L.",
            "THEOREM_SHAPED_FROM_124_126_PARITY_UNSIGNED",
            "R_evenness",
        ),
        (
            "HEX3695_3_first_derivative",
            "fixed-point source silence",
            "partial_A U_H|_{z=0}=2u_1 G_AB z^B|_0=0",
            "The local fixed point has no linear horizontal force from the even parent potential itself.",
            "DERIVED_IF_EVEN_SCALAR_PARENT_SIGNED",
            "R_Jy_potential",
        ),
        (
            "HEX3695_4_Hessian",
            "Hessian extraction",
            "partial_A partial_B U_H|_0 = 2 u_1 G_AB",
            "This is the useful compression: the horizontal Hessian is not arbitrary once the even-scalar route is parent-owned.",
            "DERIVED_IF_EVEN_SCALAR_PARENT_SIGNED",
            "R_MH_parent",
        ),
        (
            "HEX3695_5_projected_Hessian",
            "projected horizontal Hessian",
            "M_H,IJ = 2 u_1 G_H,IJ + S_src,IJ + S_boundary,IJ + S_connection,IJ",
            "Source, boundary and connection Hessian pieces must be retained unless separately proven silent.",
            "PROJECTED_FORM_DERIVED_CORRECTIONS_UNSIGNED",
            "R_Meff",
        ),
        (
            "HEX3695_6_mass_gap",
            "symbolic mass gap",
            "mu_H^2 = 2u_1 + lambda_min(G_H^{-1/2} S_corr G_H^{-1/2}) - R_domain - R_source_slope",
            "For the minimal clean even branch with S_corr=0, mu_H^2=2u_1-R_domain-R_source_slope.",
            "SYMBOLIC_GAP_DERIVED_U1_VALUE_MISSING",
            "R_muH",
        ),
        (
            "HEX3695_7_verdict",
            "extraction verdict",
            "G_H and M_eff,H are symbolically extracted under the even-scalar parent route; parent signatures and u_1 remain missing",
            "This is progress over a free Yukawa mass: the problem reduces to parity/G positivity/u_1/source-correction ownership.",
            "SYMBOLIC_EXTRACTION_SUCCESS_CLAIM_BLOCKED",
            "R_parent_signature",
        ),
    ]
    return [
        {
            **base(timestamp),
            "extraction_id": extraction_id,
            "object": object_name,
            "formula": formula,
            "derivation": derivation,
            "status": status,
            "residual_if_failed": residual,
            "claim_allowed": False,
        }
        for extraction_id, object_name, formula, derivation, status, residual in specs
    ]


def closure_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "CLO3695_0_parity",
            "leakage-frame parity/reflection symmetry",
            "z^A -> -z^A forbids a_A z^A scalar terms",
            "If adopted without parent derivation, scalar evenness is a closure axiom.",
            "CLOSURE_IF_UNSIGNED",
        ),
        (
            "CLO3695_1_positive_G",
            "positive G_H",
            "G_H,IJ positive definite on the horizontal quotient block",
            "Required before lambda_min(G_H^-1 M_eff,H) is a physical mass gap.",
            "CLOSURE_IF_UNSIGNED",
        ),
        (
            "CLO3695_2_positive_u1",
            "positive curvature of local response potential",
            "u_1(local)>0 and 2u_1 > R_domain+R_source_slope",
            "This is the minimal local mass-gap condition.",
            "CLOSURE_OR_NUMERIC_INPUT_REQUIRED",
        ),
        (
            "CLO3695_3_source_corrections",
            "source/boundary/connection Hessian corrections",
            "S_corr := S_src+S_boundary+S_connection must be zero, positive, or bounded below",
            "A negative source-slope/correction can destroy the local gap.",
            "BOUND_REQUIRED",
        ),
        (
            "CLO3695_4_environment",
            "environmental split",
            "u_1(local) large while u_1(cosmic/galaxy) small enough to keep long-range response",
            "Unified viability needs this from parent source/support physics, not hand-tuning per arena.",
            "PARENT_DERIVATION_REQUIRED",
        ),
    ]
    return [
        {
            **base(timestamp),
            "closure_id": closure_id,
            "premise": premise,
            "formula": formula,
            "why_it_matters": why,
            "status": status,
            "claim_allowed": False,
        }
        for closure_id, premise, formula, why, status in specs
    ]


def symbolic_mu_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "MU3695_0_minimal_even_branch",
            "minimal clean branch",
            "mu_H^2 = 2u_1 - R_domain - R_source_slope",
            "local screening if mu_H^2>0 and ell_H=1/sqrt(mu_H^2) is below arena limits",
            "SYMBOLIC_ONLY",
        ),
        (
            "MU3695_1_corrected_branch",
            "corrected branch",
            "mu_H^2 = 2u_1 + lambda_min(G_H^{-1/2} S_corr G_H^{-1/2}) - R_domain - R_source_slope",
            "keeps source/boundary/connection corrections instead of hiding them",
            "SYMBOLIC_ONLY",
        ),
        (
            "MU3695_2_environmental_branch",
            "environmental branch",
            "u_1=u_1(rho_local, X_B, U_B, theta, J_phys)",
            "can separate local GR safety from galaxy/cosmology response only if the dependence is parent-derived",
            "SYMBOLIC_ONLY",
        ),
        (
            "MU3695_3_yukawa_interface",
            "Yukawa interface",
            "lambda_H = 1/sqrt(mu_H^2), alpha_A = K_A C_H ||J_y+B_y||/N_A",
            "passes to 3694 nonclaim arena runner until u_1 and projections are sourced",
            "NONCLAIM_RUNNER_READY",
        ),
    ]
    return [
        {
            **base(timestamp),
            "mu_id": mu_id,
            "branch": branch,
            "formula": formula,
            "use": use,
            "status": status,
            "claim_allowed": False,
            "score_ready": False,
        }
        for mu_id, branch, formula, use, status in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "DEC3695_0",
            "Symbolic extraction succeeds conditionally",
            "If the local horizontal response potential is an even scalar of s_L, the Hessian is 2u_1 G_H and the mass gap reduces to a scalar curvature u_1 plus corrections.",
            "ADOPT_CONDITIONAL_THEOREM",
        ),
        (
            "DEC3695_1",
            "No local claim",
            "The corpus still lacks parent-signed parity, positive G_H, u_1 value/origin, and correction bounds.",
            "CLAIM_BLOCKED",
        ),
        (
            "DEC3695_2",
            "Best next route",
            "Derive u_1 from the relaxation functional/fixed-point stability or mark it as a closure coefficient feeding the Yukawa runner.",
            "NEXT_U1_ORIGIN_TARGET",
        ),
    ]
    return [
        {**base(timestamp), "decision_id": decision_id, "decision": decision, "rationale": rationale, "status": status}
        for decision_id, decision, rationale, status in specs
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("CG3695_0_parity", "leakage-frame parity/reflection symmetry not parent signed", "BLOCKED"),
        ("CG3695_1_GH", "G_H positivity and units not parent signed", "BLOCKED"),
        ("CG3695_2_u1", "u_1 value/origin not derived or sourced", "BLOCKED"),
        ("CG3695_3_corrections", "S_corr, R_domain and R_source_slope not bounded", "BLOCKED"),
        ("CG3695_4_local_GR", "local GR requires arena residuals after lambda_H/alpha_A sourcing", "BLOCKED"),
        ("CG3695_5_public", "private checkpoint only; no public/GitHub claim", "BLOCKED"),
    ]
    return [
        {**base(timestamp), "gate_id": gate_id, "gate": gate, "status": status, "claim_allowed": False}
        for gate_id, gate, status in specs
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "status_id": "STATUS3695_0",
            "status": "CONDITIONAL_HESSIAN_EXTRACTION_SUCCEEDS_MUH_REDUCED_TO_U1_AND_CORRECTIONS",
            "summary": "Under the signed-coordinate/even-scalar route already staged in the corpus, the horizontal Hessian is M_H=2u_1 G_H plus explicit source/boundary/connection corrections. This reduces local screening from a free mass-gap assumption to the parent origin of u_1, G_H positivity and correction bounds.",
            "claim_allowed": False,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "next_id": "NEXT3695_0",
            "target_doc": "3696-Y5-R2FR-u1-origin-from-relaxation-functional-or-local-screening-closure.md",
            "target_script": "scripts/Y5_R2FR_3696_u1_origin_from_relaxation_functional_or_local_screening_closure.py",
            "objective": "derive the scalar curvature coefficient u_1 from the relaxation/fixed-point parent functional, or explicitly demote local mass-gap screening to a closure coefficient feeding the Yukawa runner",
            "success_gate": "u_1 is parent-derived/positive with units and environment dependence, or the route is labeled closure-only with nonclaim arena rows",
            "claim_allowed": False,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    extraction: list[dict[str, object]],
    closures: list[dict[str, object]],
    mu_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3695 - Parent Hessian kinetic metric source extraction for mu_H",
        "",
        "Private checkpoint. No GitHub action. No local-GR/Newton/R10/PPN/EM claim.",
        "",
        "## Status",
        f"- `{status[0]['status']}`",
        f"- {status[0]['summary']}",
        "",
        "## Main Result",
        "- This checkpoint extracts the useful theorem hidden inside the local fixed-point/evenness work.",
        "- If the horizontal local response variables are signed coordinates `z^A` and the parent scalar depends on them only through `s_L = G_AB z^A z^B`, then:",
        "  - `partial_A U_H|_0 = 0`;",
        "  - `partial_A partial_B U_H|_0 = 2 u_1 G_AB` for `U_H=U_0+u_1 s_L+u_2 s_L^2+...`;",
        "  - `M_H,IJ = 2 u_1 G_H,IJ + S_corr,IJ` after horizontal projection.",
        "- Therefore the clean mass-gap route is not an arbitrary `mu_H`; it is `mu_H^2 = 2u_1 + lambda_min(G_H^{-1/2}S_corrG_H^{-1/2}) - R_domain - R_source_slope`.",
        "",
        "## Interpretation",
        "- Good news: the problem compressed from a whole unknown Hessian to one scalar curvature `u_1` plus explicit correction terms.",
        "- Bad news, but honest: `u_1`, positive `G_H`, leakage-frame parity and correction bounds are not parent-signed yet.",
        "- So local screening is a conditional theorem route, not a claim.",
        "",
        "## Extraction Rows",
    ]
    for row in extraction:
        lines.append(f"- `{row['extraction_id']}`: {row['object']} | `{row['status']}` | {row['formula']}")
    lines.extend(["", "## Closure/Binder Rows"])
    for row in closures:
        lines.append(f"- `{row['closure_id']}`: {row['premise']} | `{row['status']}` | {row['formula']}")
    lines.extend(["", "## Symbolic mu_H Rows"])
    for row in mu_rows:
        lines.append(f"- `{row['mu_id']}`: {row['branch']} | `{row['status']}` | {row['formula']}")
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
    extraction: list[dict[str, object]],
    closures: list[dict[str, object]],
    mu_rows: list[dict[str, object]],
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
    no_leak = not any(FORMALIZATION.rglob("*3695*"))
    hessian_ok = any(row_data["extraction_id"] == "HEX3695_4_Hessian" and "2 u_1 G_AB" in row_data["formula"] for row_data in extraction)
    gap_ok = any(row_data["mu_id"] == "MU3695_0_minimal_even_branch" and "2u_1" in row_data["formula"] for row_data in mu_rows)
    closure_keys = {row_data["closure_id"] for row_data in closures}
    closure_ok = {"CLO3695_0_parity", "CLO3695_1_positive_G", "CLO3695_2_positive_u1", "CLO3695_3_source_corrections", "CLO3695_4_environment"}.issubset(closure_keys)
    gates_blocked = all(row_data["status"] == "BLOCKED" for row_data in claim_gates)
    nonclaim = all(
        not bool(row_data.get("valid_for_claim"))
        for table in [sources, extraction, closures, mu_rows, decisions, claim_gates, status, next_target]
        for row_data in table
    )
    next_ok = str(next_target[0]["target_doc"]).startswith("3696-") and "u1" in str(next_target[0]["target_doc"])
    doc_ok = all(needle in doc_text for needle in ["partial_A partial_B U_H|_0 = 2 u_1 G_AB", "mu_H^2 = 2u_1", "one scalar curvature `u_1`", "not parent-signed"])

    return [
        row("VAL3695_0_sources_exist", source_ok, "all input source files exist"),
        row("VAL3695_1_needles_found", needles_ok, "all source needles found"),
        row("VAL3695_2_outputs_exist", all(path.exists() for path in generated_paths), "all generated outputs exist"),
        row("VAL3695_3_csv_parse", parsed_ok, "; ".join(parse_details)),
        row("VAL3695_4_hessian_extraction", hessian_ok, "Hessian collapses to 2u_1 G_AB under even scalar route"),
        row("VAL3695_5_symbolic_gap", gap_ok, "minimal symbolic mu_H branch present"),
        row("VAL3695_6_closure_rows", closure_ok, "parity/G/u1/correction/environment rows present"),
        row("VAL3695_7_claim_gates_blocked", gates_blocked, "all claim gates remain blocked"),
        row("VAL3695_8_all_nonclaim", nonclaim, "all tables remain nonclaim"),
        row("VAL3695_9_next_target", next_ok, "3696 u1 origin target selected"),
        row("VAL3695_10_doc_written", doc_ok, "doc contains Hessian law, mass-gap compression and nonclaim status"),
        row("VAL3695_11_no_formalization_leak", no_leak, "no 3695 files under formalization-workbench"),
    ]


def main() -> int:
    timestamp = stamp()
    sources = source_register(timestamp)
    extraction = extraction_rows(timestamp)
    closures = closure_rows(timestamp)
    mu_rows = symbolic_mu_rows(timestamp)
    decisions = decision_rows(timestamp)
    claim_gates = claim_gate_rows(timestamp)
    status = status_rows(timestamp)
    next_target = next_rows(timestamp)

    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3695_SOURCE_REGISTER.csv",
        "extraction": RESIDUALS / "P8_Y5_R2FR_3695_HESSIAN_EXTRACTION_ROWS.csv",
        "closures": RESIDUALS / "P8_Y5_R2FR_3695_CLOSURE_BINDER_ROWS.csv",
        "mu": RESIDUALS / "P8_Y5_R2FR_3695_SYMBOLIC_MUH_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3695_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3695_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3695_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3695_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3695_VALIDATION.csv",
    }

    write_csv(outputs["sources"], sources)
    write_csv(outputs["extraction"], extraction)
    write_csv(outputs["closures"], closures)
    write_csv(outputs["mu"], mu_rows)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["claim_gates"], claim_gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, extraction, closures, mu_rows, decisions, claim_gates, status, next_target)

    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(timestamp, generated_paths, sources, extraction, closures, mu_rows, decisions, claim_gates, status, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3695 validation failed: {failures}", file=sys.stderr)
        return 1
    print("wrote 3695 checkpoint: Hessian extracted conditionally; mu_H reduced to u_1 plus corrections")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
