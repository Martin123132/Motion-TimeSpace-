from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
DOC = ROOT / "2007-Y5-R2FR-full-tetrad-completion-from-radial-seed-or-residual-interface.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row() -> dict[str, object]:
    return {
        "branch_id": BRANCH_ID,
        "valid_for_claim": "false",
        "claim_allowed": "false",
        "generated_utc": stamp(),
    }


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_rows_parse(path: Path) -> bool:
    try:
        read_csv(path)
    except csv.Error:
        return False
    return True


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def count_formalization_modified_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED
    )


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2007_00_2006_handoff",
            "2006-Y5-R2FR-parent-EqPhi-coframe-readout-map-or-owned-coframe-closure-demotion.md",
            ["NEXT2006_0_2007", "RSEED2006_2_full_spatial_triads", "VAL2006_OVERALL"],
            "2006 selected full tetrad completion from the clock/radial seed.",
        ),
        (
            "SRC2007_01_radial_cell",
            "09-hamiltonian-radial-cell-derivation.md",
            ["defined clock-load coframe", "defined radial routing coframe", "separate radial cell gives p=1 exactly"],
            "clock-load and radial-routing seed.",
        ),
        (
            "SRC2007_02_observer_contract",
            "10-observer-map-symplectic-contract.md",
            ["The local observer coframe must be defined before any PPN claim", "all matter sectors couple to the same observer coframe", "contract not satisfied"],
            "observer coframe and PPN completion contract.",
        ),
        (
            "SRC2007_03_788_nonholonomic",
            "788-Y5-R10-nonholonomic-coframe-or-moment-closure-parent-action.md",
            ["NHC788_1_nonholonomic_ansatz", "NHC788_4_ownership_warning", "PAC788_0_palatini_tetrad_contract"],
            "nonholonomic coframe route and ownership warning.",
        ),
        (
            "SRC2007_04_789_palatini",
            "789-Y5-R10-palatini-tetrad-GR-limit-with-MTS-exchange-contract.md",
            ["PTG789_0_field_content", "PTG789_4_GR_recovery", "NPR789_4_frame"],
            "Palatini/tetrad local-GR contract and residual list.",
        ),
        (
            "SRC2007_05_785_stack",
            "785-Y5-R10-psi-metric-coframe-connection-contract-or-bg-residual-lock.md",
            ["PMC785_2_local_coframe_existence", "CDS785_0_tetrad_domain", "BGL785_3_matter_blindness_trigger"],
            "conditional local coframe existence and matter-blindness blocker.",
        ),
        (
            "SRC2007_06_943_contract",
            "943-Y5-R10-single-observed-coframe-matter-coupling-contract-or-frame-residual-source-pack.md",
            ["CFC943_2_matter_functor", "DER943_5_shadow_counterexample", "ARENA943_3_clocks"],
            "matter functor, shadow-frame counterexamples, and local arenas.",
        ),
        (
            "SRC2007_07_944_descent",
            "944-Y5-R10-quotient-observed-coframe-descent-proof-or-frame-leak-source-bounds.md",
            ["QDG944_2_observed_coframe_functor", "P944_5_counterexample_common_frame", "FLB944_7_epsilon_frame_leak"],
            "quotient descent theorem and frame-leak fallback.",
        ),
        (
            "SRC2007_08_1738_kernel",
            "1738-Y5-R2FR-observed-coframe-kernel-zero-or-first-finite-DObs-e-row.md",
            ["DOK1738_0_chain_rule_kernel", "DOK1738_1_same_coframe_not_enough", "DOE1738_4_total_coframe_kernel_envelope"],
            "coframe kernel zero theorem and DObs_e finite envelope.",
        ),
        (
            "SRC2007_09_1880_no_shadow",
            "1880-Y5-R2FR-terminal-public-coframe-no-shadow-frame-or-bg-bound-projection.md",
            ["TPC1880_0_terminal_object", "ZTH1880_0_exact_conditional", "BIN1880_0_coefficients"],
            "terminal public coframe/no-shadow theorem and response-kernel fallback.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, relative_path, needles, note in specs:
        path = source_path(relative_path)
        exists = path.exists()
        text = read_text(path) if exists else ""
        missing = [needle for needle in needles if needle not in text]
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "needed_for": "2007 full tetrad completion from radial seed or residual interface",
                "needles": ";".join(needles),
                "exists": str(exists),
                "anchor_found": str(exists and not missing),
                "missing_needles": ";".join(missing),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "note": note,
            }
        )
        rows.append(row)
    return rows


def tetrad_completion_rows() -> list[dict[str, object]]:
    specs = [
        (
            "TET2007_0_time_leg",
            "e_obs^0",
            "clock-load one-form from the local observer/radial-cell branch",
            "SUPPORTED_SEED_NOT_NORMALIZED",
            "normalization and universality remain parent-unsigned",
        ),
        (
            "TET2007_1_radial_leg",
            "e_obs^1",
            "radial-routing one-form selected by the separate radial observer cell",
            "SUPPORTED_SEED_NOT_PARENT_DERIVED",
            "radial cell conservation remains a closure condition rather than a parent theorem",
        ),
        (
            "TET2007_2_exact_gradient_route",
            "e^a=dX^a",
            "four exact scalar gradients cannot carry generic curved/tidal coframe with anholonomy",
            "REJECTED_FOR_FULL_GR",
            "flat-pullback trap from 788; not a serious full tetrad completion",
        ),
        (
            "TET2007_3_nonholonomic_completion",
            "e^a=dX^a+A^a",
            "add a frame-deformation/nonholonomic one-form A^a so de^a can be nonzero and curvature can be carried",
            "VIABLE_CONDITIONAL_CONTRACT",
            "A^a dynamics and MTS parent origin are not derived",
        ),
        (
            "TET2007_4_transverse_legs",
            "e_obs^2,e_obs^3",
            "two transverse ruler/angle one-forms complete the local tetrad and support generic PPN/light-cone tests",
            "MISSING_PARENT_DERIVATION",
            "no inspected source derives transverse legs from MTS flow/cell data",
        ),
        (
            "TET2007_5_nonzero_determinant",
            "det(e_obs)",
            "full four-leg coframe must be nondegenerate with Lorentzian orientation and time orientation",
            "MISSING_DOMAIN_PROOF",
            "clock/radial seed alone cannot prove det(e_obs)!=0",
        ),
        (
            "TET2007_6_lorentz_gauge",
            "e_obs ~ Lambda(x)e_obs",
            "pure local Lorentz rotations should be gauge and not physical frame leakage",
            "CONDITIONAL_GAUGE_RULE",
            "matter representation/gauge invariance and no-spurion proof remain unsigned",
        ),
        (
            "TET2007_7_matter_functor",
            "S_matter[e_obs,omega_LC[e_obs],A_owned,theta]",
            "ordinary matter must use only the completed coframe, induced connection, owned gauge fields, and constants",
            "CONTRACT_AVAILABLE_UNSIGNED",
            "shadow Weyl/disformal/species marker counterexamples remain legal until excluded",
        ),
        (
            "TET2007_8_completion_verdict",
            "full e_obs tetrad",
            "the radial seed plus nonholonomic contract is promising, but the full tetrad is not derived from current MTS parent equations",
            "FULL_TETRAD_NOT_DERIVED_CURRENT_CORPUS",
            "activate residual interface and target A^a parent dynamics next",
        ),
    ]
    rows: list[dict[str, object]] = []
    for tetrad_id, element, requirement, status, blocker in specs:
        row = base_row()
        row.update(
            {
                "tetrad_id": tetrad_id,
                "element": element,
                "requirement_or_result": requirement,
                "status": status,
                "blocker": blocker,
                "parent_signed": "false",
            }
        )
        rows.append(row)
    return rows


def nonholonomic_contract_rows() -> list[dict[str, object]]:
    specs = [
        (
            "NHC2007_0_candidate",
            "e^a = dX^a + A^a_MTS",
            "A^a_MTS is a parent-owned frame-deformation one-form built from motion/time/space flow, cell, or memory data",
            "BEST_CONSTRUCTIVE_ROUTE",
            "keeps curvature without pretending exact scalar gradients are enough",
            "MISSING_ACTION_AND_GAUGE_LAW",
        ),
        (
            "NHC2007_1_anholonomy",
            "C^a = de^a",
            "nonzero anholonomy is allowed as frame curvature data, but torsion must still be zero, sourced, or bounded after connection variation",
            "CONDITIONAL_GEOMETRY_OK",
            "separates coframe anholonomy from physical torsion",
            "MISSING_CONNECTION_EQUATION",
        ),
        (
            "NHC2007_2_action",
            "S_A = integral det(e) L_A(A^a_MTS,dA^a_MTS,Xi_MTS)",
            "parent must supply dynamics or constraints for A^a_MTS, not just name it",
            "NOT_DERIVED",
            "prevents arbitrary tetrad insertion",
            "MISSING_PARENT_LAGRANGIAN",
        ),
        (
            "NHC2007_3_rank",
            "rank(delta e^a_mu / delta parent fields)=16 modulo gauges",
            "coframe variations must be rich enough for local metric/tetrad dynamics",
            "MISSING_RANK_CERTIFICATE",
            "avoids scalar-only rank trap",
            "MISSING_MULTIFIELD_RANK_PROOF",
        ),
        (
            "NHC2007_4_local_GR_contract",
            "Palatini/tetrad limit",
            "if A^a_MTS is owned and residual MTS stress/exchange vanishes, 789 gives the GR/Newton contract",
            "EXACT_CONDITIONAL_BRIDGE",
            "keeps the path to GR clear",
            "MISSING_RESIDUAL_SUPPRESSION_AND_EH_GATE",
        ),
    ]
    rows: list[dict[str, object]] = []
    for contract_id, object_name, clause, status, value, missing in specs:
        row = base_row()
        row.update(
            {
                "contract_id": contract_id,
                "object": object_name,
                "clause": clause,
                "status": status,
                "value": value,
                "missing_before_claim": missing,
            }
        )
        rows.append(row)
    return rows


def residual_interface_rows() -> list[dict[str, object]]:
    specs = [
        ("RES2007_0_transverse_frame", "epsilon_perp", "failure to derive e_obs^2,e_obs^3 from parent MTS data", "PPN light-bending; preferred-frame; orbital light-time", "MISSING_NUMERIC_OR_THEOREM_ZERO"),
        ("RES2007_1_determinant_domain", "epsilon_det", "nonzero determinant/Lorentzian-domain failure", "metric-domain and local tetrad validity", "MISSING_DOMAIN_BOUND"),
        ("RES2007_2_common_frame", "b_g_or_c_g", "universal Weyl/common-frame derivative of completed coframe", "R10; PPN; clocks; WEP common-mode/source leg", "MISSING_PARENT_ZERO_OR_NUMERIC_BOUND"),
        ("RES2007_3_disformal_frame", "b_dis", "disformal/preferred-frame component of matter-visible tetrad/metric", "preferred-frame PPN; clock; orbital", "MISSING_DISFORMAL_ZERO_OR_BOUND"),
        ("RES2007_4_matter_functor", "epsilon_matter_frame", "direct Phi_MTS, species marker, mass, or readout dependence outside e_obs", "WEP; clock; source normalization", "MISSING_MATTER_DESCENT_OR_BOUND"),
        ("RES2007_5_connection", "epsilon_P4", "independent connection/torsion/nonmetricity if tetrad route not canonicalized", "spin/precession; PPN; source-side GR", "MISSING_P4_BOUND_OR_NO_GAMMA_CANONICALIZATION"),
        ("RES2007_6_R11_operator", "Xi_R11", "higher-curvature/nonlocal/extra-sector local exterior operator", "Newton/Poisson; PPN gamma/beta", "MISSING_R11_EXECUTABLE_ROW"),
        ("RES2007_7_total_envelope", "epsilon_tetrad_abs", "absolute sum envelope for all tetrad/frame/operator residuals", "all local arenas", "MISSING_COMPONENT_INPUTS"),
    ]
    rows: list[dict[str, object]] = []
    for residual_id, symbol, meaning, arenas, status in specs:
        row = base_row()
        row.update(
            {
                "residual_id": residual_id,
                "symbol": symbol,
                "meaning": meaning,
                "test_arenas": arenas,
                "status": status,
                "numeric_value": "MISSING",
                "units": "MISSING",
                "source_path": "MISSING",
                "valid_for_claim": "false",
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    specs = [
        ("CG2007_0_radial_seed", "clock/radial seed exists", "PASS_NONCLAIM", "partial support only"),
        ("CG2007_1_exact_gradient", "exact-gradient tetrad derives full GR geometry", "FAIL_REJECTED", "flat-pullback/anholonomy trap"),
        ("CG2007_2_nonholonomic_contract", "nonholonomic tetrad completion contract exists", "PASS_NONCLAIM", "viable route but not parent-derived"),
        ("CG2007_3_full_tetrad_parent_signed", "full nondegenerate Lorentz tetrad derived from MTS", "FAIL_BLOCKED", "transverse legs, determinant, gauge, matter functor, and A^a dynamics unsigned"),
        ("CG2007_4_residual_interface_score", "residual interface score-ready", "FAIL_BLOCKED", "numeric coefficients, units, projections, and source paths missing"),
        ("CG2007_5_local_GR_Newton", "local GR/Newton derived", "FAIL_BLOCKED", "full tetrad, EH/R11, residual suppression, and GM transfer remain open"),
        ("CG2007_6_public_claim", "public local-GR claim allowed", "FAIL_BLOCKED", "private nonclaim derivation checkpoint"),
    ]
    rows: list[dict[str, object]] = []
    for gate_id, gate, status, reason in specs:
        row = base_row()
        row.update(
            {
                "gate_id": gate_id,
                "gate": gate,
                "status": status,
                "reason": reason,
                "passed_for_claim": "false",
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    specs = [
        (
            "DEC2007_0_result",
            "FULL_TETRAD_NOT_DERIVED_BUT_NONHOLONOMIC_ROUTE_SELECTED",
            "The radial seed is real but only two-legged; exact gradients fail; the serious route is parent-owned nonholonomic frame deformation A^a_MTS.",
            "derive A^a_MTS action/rank/gauge law next or begin residual response rows",
        ),
        (
            "DEC2007_1_not_a_retreat",
            "CLOSURE_BRANCH_NOW_HAS_A_SHARP_PARENT_ACTION_TARGET",
            "ACT1963 is not dead; it needs A^a_MTS ownership and full tetrad completion before canonicalization.",
            "keep no-Gamma theorem as conditional, do not promote it globally",
        ),
        (
            "DEC2007_2_data_path",
            "RESIDUAL_INTERFACE_READY_BUT_NOT_SCORE_READY",
            "If derivation stalls, the local test path is no longer vague: transverse, determinant, common/disformal frame, matter functor, P4, and R11 rows must be sourced.",
            "source response kernels only after parent zero attempts fail",
        ),
    ]
    rows: list[dict[str, object]] = []
    for decision_id, verdict, rationale, next_action in specs:
        row = base_row()
        row.update(
            {
                "decision_id": decision_id,
                "verdict": verdict,
                "rationale": rationale,
                "next_action": next_action,
            }
        )
        rows.append(row)
    return rows


def next_target_rows() -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "target_id": "NEXT2007_0_2008",
            "selected": "true",
            "next_doc": "2008-Y5-R2FR-parent-nonholonomic-frame-deformation-action-or-tetrad-residual-runner.md",
            "next_script": "scripts/Y5_R2FR_parent_nonholonomic_frame_deformation_action_or_tetrad_residual_runner_2008.py",
            "objective": "try to derive a parent action/gauge/rank law for the nonholonomic frame-deformation one-form A^a_MTS that completes the tetrad; if not, turn the 2007 residual interface into first executable local response rows",
            "include": "A^a_MTS one-form; anholonomy; local Lorentz gauge; determinant/rank certificate; matter functor; Palatini/tetrad contract; residual response rows",
            "exclude": "exact-gradient tetrad as full GR proof; declaring independent tetrad without label; local-GR claim; GitHub; formalization-workbench edits",
        }
    )
    return [row]


def branch_copy_rows(paths: list[Path], notes: list[str]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for idx, (path, note) in enumerate(zip(paths, notes, strict=True)):
        row = base_row()
        row.update(
            {
                "copy_id": f"COPY2007_{idx}",
                "copy_path": str(path),
                "exists": str(path.exists()),
                "note": note,
            }
        )
        rows.append(row)
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    tetrad_rows: list[dict[str, object]],
    contracts: list[dict[str, object]],
    residuals: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    output_paths: list[Path],
    branch_paths: list[Path],
) -> list[dict[str, object]]:
    checks = [
        ("VAL2007_00_sources", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources), "all cited source paths exist and needles are found"),
        ("VAL2007_01_exact_gradient_rejected", any(row["status"] == "REJECTED_FOR_FULL_GR" for row in tetrad_rows), "exact-gradient route rejected as full GR derivation"),
        ("VAL2007_02_nonholonomic_selected", any(row["status"] == "VIABLE_CONDITIONAL_CONTRACT" for row in tetrad_rows) and any(row["status"] == "BEST_CONSTRUCTIVE_ROUTE" for row in contracts), "nonholonomic completion route selected as conditional"),
        ("VAL2007_03_full_tetrad_not_signed", any(row["status"] == "FULL_TETRAD_NOT_DERIVED_CURRENT_CORPUS" for row in tetrad_rows) and all(row["parent_signed"] == "false" for row in tetrad_rows), "full tetrad not falsely promoted"),
        ("VAL2007_04_residuals_nonclaim", all(row["valid_for_claim"] == "false" and row["numeric_value"] == "MISSING" for row in residuals), "residual interface rows remain nonclaim placeholders"),
        ("VAL2007_05_claim_gates_blocked", all(row["passed_for_claim"] == "false" for row in claim_gates), "all claim gates remain blocked"),
        ("VAL2007_06_csv_parse", all(path.exists() and csv_rows_parse(path) for path in output_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2007_07_branch_copies", all(path.exists() for path in branch_paths), "branch-copy CSVs exist"),
        ("VAL2007_08_no_formalization_edits", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains 0 for this run"),
        ("VAL2007_09_output_scope", all(ROOT in [path, *path.parents] for path in [*output_paths, *branch_paths, DOC]), "all outputs are under post-checkpoint-work"),
    ]
    rows: list[dict[str, object]] = []
    for check_id, passed, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail})
        rows.append(row)
    overall = all(row["status"] == "PASS" for row in rows)
    row = base_row()
    row.update(
        {
            "check_id": "VAL2007_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "2007 full tetrad completion from radial seed or residual interface",
        }
    )
    rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    tetrad_rows: list[dict[str, object]],
    contracts: list[dict[str, object]],
    residuals: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    branch_copies: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 2007 Y5 R2FR: Full Tetrad Completion From Radial Seed Or Residual Interface

Private checkpoint. This tries to upgrade the 2006 clock/radial coframe seed into a full four-leg Lorentz coframe.

## Current Verdict

The full tetrad is not derived yet. The clock-load leg and radial-routing leg are genuine support, but a two-leg radial seed is not a four-leg local spacetime frame. The exact-gradient route is rejected because it cannot carry generic anholonomy/curvature. The best constructive route is a parent-owned nonholonomic frame-deformation one-form `A^a_MTS` such that `e^a=dX^a+A^a_MTS`.

That route is viable but still conditional: the parent action, gauge law, rank/nonzero-determinant certificate, universal matter functor, and residual suppression are missing. Therefore the tetrad branch stays private/nonclaim, and the residual interface is made explicit for local testing if the derivation fails.

No local-GR/Newton/WEP claim is promoted.

## Source Register
{md_table(sources, ["source_id", "source_path", "status", "needles", "note"])}

## Tetrad Completion Attempt
{md_table(tetrad_rows, ["tetrad_id", "element", "status", "blocker", "parent_signed"])}

## Nonholonomic Frame-Deformation Contract
{md_table(contracts, ["contract_id", "object", "status", "value", "missing_before_claim"])}

## Residual Interface
{md_table(residuals, ["residual_id", "symbol", "meaning", "test_arenas", "status", "valid_for_claim"])}

## Claim Gates
{md_table(claim_gates, ["gate_id", "gate", "status", "reason", "passed_for_claim"])}

## Decision Ledger
{md_table(decisions, ["decision_id", "verdict", "rationale", "next_action"])}

## Branch Copies
{md_table(branch_copies, ["copy_id", "copy_path", "exists", "note"])}

## Next Target
{md_table(next_target, ["target_id", "next_doc", "objective", "include", "exclude"])}

## Validation
{md_table(validation, ["check_id", "status", "detail"])}
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    tetrad_rows = tetrad_completion_rows()
    contracts = nonholonomic_contract_rows()
    residuals = residual_interface_rows()
    claim_gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    output_map = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2007_SOURCE_REGISTER.csv",
        "tetrad": OUT / "P8_Y5_PARENT_QLOC_2007_TETRAD_COMPLETION_ATTEMPT.csv",
        "contracts": OUT / "P8_Y5_PARENT_QLOC_2007_NONHOLONOMIC_CONTRACT.csv",
        "residuals": OUT / "P8_Y5_PARENT_QLOC_2007_RESIDUAL_INTERFACE.csv",
        "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2007_CLAIM_GATE.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2007_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_PARENT_QLOC_2007_NEXT_TARGET.csv",
    }
    write_csv(output_map["sources"], sources)
    write_csv(output_map["tetrad"], tetrad_rows)
    write_csv(output_map["contracts"], contracts)
    write_csv(output_map["residuals"], residuals)
    write_csv(output_map["claim_gates"], claim_gates)
    write_csv(output_map["decisions"], decisions)
    write_csv(output_map["next_target"], next_target)

    branch_paths = [
        SOURCE_WEIGHT_DOCS / "FULL_TETRAD_COMPLETION_2007_NONCLAIM.csv",
        BRANCH_WEP / "P8_Y5_PARENT_QLOC_2007_TETRAD_STATUS_NONCLAIM.csv",
        QUEUE / "JR2007_TETRAD_RESIDUAL_INTERFACE_QUEUE.csv",
    ]
    branch_paths[0].parent.mkdir(parents=True, exist_ok=True)
    branch_paths[1].parent.mkdir(parents=True, exist_ok=True)
    branch_paths[2].parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(output_map["tetrad"], branch_paths[0])
    shutil.copyfile(output_map["contracts"], branch_paths[1])
    shutil.copyfile(output_map["residuals"], branch_paths[2])

    branch_copies = branch_copy_rows(
        branch_paths,
        [
            "full tetrad completion nonclaim copy",
            "tetrad/nonholonomic contract status nonclaim copy",
            "tetrad residual interface queue",
        ],
    )
    branch_copy_path = OUT / "P8_Y5_PARENT_QLOC_2007_BRANCH_COPIES.csv"
    write_csv(branch_copy_path, branch_copies)

    output_paths = [*output_map.values(), branch_copy_path]
    validation = validation_rows(sources, tetrad_rows, contracts, residuals, claim_gates, output_paths, branch_paths)
    validation_path = OUT / "P8_Y5_BRR545_2007_VALIDATION.csv"
    write_csv(validation_path, validation)
    output_paths.append(validation_path)

    write_doc(sources, tetrad_rows, contracts, residuals, claim_gates, decisions, branch_copies, next_target, validation)
    remove_pycache()

    overall = [row for row in validation if row["check_id"] == "VAL2007_OVERALL"][0]["status"]
    print(f"VAL2007_OVERALL={overall}")
    print(str(DOC))
    for path in output_paths:
        print(str(path))
    for path in branch_paths:
        print(str(path))


if __name__ == "__main__":
    main()
