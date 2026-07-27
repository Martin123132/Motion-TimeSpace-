from __future__ import annotations

import csv
from pathlib import Path

from Y5_R2FR_Dq_vX_observed_metric_zero_or_finite_DObs_leak_row_2025 import (
    BRANCH_WEP,
    OUT,
    QUEUE,
    ROOT,
    SOURCE_WEIGHT_DOCS,
    base_row,
    count_formalization_modified,
    csv_rows_parse,
    md_table,
    read_text,
    remove_pycache,
    write_csv,
)


DOC = ROOT / "2046-Y5-R2FR-GammaMTS-affine-torsion-definition-or-LC-zero-theorem.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
HBARC_GEV_M = "1.973269804e-16"


def formalization_has_2046_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        artifact_patterns = (
            "*2046-Y5-R2FR*",
            "*P8_Y5_PARENT_QLOC_2046*",
            "*Y5_R2FR_GammaMTS_affine_torsion_definition_or_LC_zero_theorem_2046*",
        )
        return any(path.is_file() for pattern in artifact_patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def scripts_pycache_exists() -> bool:
    return (SCRIPT_PATH.parent / "__pycache__").exists()


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    try:
        with path.open("r", newline="", encoding="utf-8", errors="replace") as handle:
            return list(csv.DictReader(handle))
    except Exception:
        return []


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2046_00_2045_doc",
            ROOT / "2045-Y5-R2FR-MTS-axial-torsion-component-map-or-P4-bound-runner.md",
            ["NEXT2045_0_2046", "REQ2045_0_Gamma_MTS", "VAL2045_OVERALL"],
            "2045 handoff: define or kill Gamma_MTS before any axial torsion bound can score.",
        ),
        (
            "SRC2046_01_2045_next",
            OUT / "P8_Y5_PARENT_QLOC_2045_NEXT_TARGET.csv",
            ["NEXT2045_0_2046", "Gamma_MTS owner"],
            "machine-readable 2046 target.",
        ),
        (
            "SRC2046_02_2045_requirements",
            OUT / "P8_Y5_PARENT_QLOC_2045_MTS_VARIABLE_REQUIREMENTS.csv",
            ["REQ2045_0_Gamma_MTS", "REQ2045_1_T_MTS", "MISSING_PARENT_INPUT"],
            "Gamma_MTS and T_MTS requirement rows.",
        ),
        (
            "SRC2046_03_2045_map",
            OUT / "P8_Y5_PARENT_QLOC_2045_CONDITIONAL_COMPONENT_MAP.csv",
            ["MAP2045_0_affine_torsion", "MAP2045_7_verdict"],
            "conditional axial torsion map that remains blocked until Gamma_MTS exists.",
        ),
        (
            "SRC2046_04_2042_lc_theorem",
            ROOT / "2042-Y5-R2FR-Levi-Civita-no-hypermomentum-parent-clause-or-P4-connection-row.md",
            ["NH2042_1_no_gamma_slot", "PAL2042_3_lc_result", "VAL2042_OVERALL"],
            "no-hypermomentum and Palatini/LC theorem source.",
        ),
        (
            "SRC2046_05_2043_gamma_owner",
            ROOT / "2043-Y5-R2FR-parent-Gamma-slot-owner-or-first-P4-connection-bound-row.md",
            ["GSO2043_0_target", "SPG2043_0_spin_guard", "VAL2043_OVERALL"],
            "parent Gamma-slot owner and spin/projective guard source.",
        ),
        (
            "SRC2046_06_2044_p4_source",
            ROOT / "2044-Y5-R2FR-sector-Gamma-slot-audit-or-first-numeric-P4-source.md",
            ["P4SRC2044_0_KRT2008_axial_torsion_anchor", "MAP2044_0_component_basis", "VAL2044_OVERALL"],
            "first torsion bound source anchor and component-basis blocker.",
        ),
        (
            "SRC2046_07_1339_left_hand",
            ROOT / "1339-Y5-R10-RAB-source-closure-to-EH-left-hand-local-GR-reduction-gate.md",
            ["EHGate1339_3_Levi_Civita", "LOV1339_0_conditional_EH_selection"],
            "left-hand EH route requiring Levi-Civita as one premise.",
        ),
        (
            "SRC2046_08_1340_R11_interface",
            ROOT / "1340-Y5-R10-RAB-EH-core-selection-or-first-executable-R11-residual-interface.md",
            ["EH1340_3_connection_obstruction", "R11SCHEMA1340_2_connection", "VAL1340_11_overall"],
            "strict R11 connection residual interface.",
        ),
    ]
    rows = []
    for source_id, path, needles, note in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        ok = exists and all(needle in text for needle in needles)
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_kind": "local",
                "source_path": str(path),
                "status": "EXISTS_NEEDLES_CONFIRMED" if ok else "MISSING_OR_NEEDLE_FAIL",
                "needles": ";".join(needles),
                "note": note,
            }
        )
        rows.append(row)
    return rows


def lc_zero_theorem_rows() -> list[dict[str, object]]:
    data = [
        (
            "LCZ2046_0_choice",
            "metric/coframe-only observed branch",
            "Choose the parent ordinary local branch so the observed geometry is carried by e_obs or g_obs, and any spin connection is omega_LC[e_obs].",
            "PARENT_SIGNATURE_REQUIRED",
            "would remove independent affine Gamma_MTS as a physical local field",
            "current corpus has contracts but no final parent action signature",
        ),
        (
            "LCZ2046_1_no_independent_Gamma",
            "Gamma_MTS has no independent slot",
            "If S_parent^local = Sbar[g_obs(e_obs), Psi, A_Q, theta] plus omega_LC[e_obs] for spinors, then delta S_ord / delta Gamma_MTS = 0 by absence of the argument.",
            "EXACT_CONDITIONAL_THEOREM",
            "hypermomentum Delta_lambda^{mu nu}=0 without tuning",
            "ordinary matter/source/clock/light/orbit slots are not all parent-signed",
        ),
        (
            "LCZ2046_2_definition",
            "define Gamma_MTS by LC only",
            "Gamma_MTS^lambda_{mu nu} := {lambda}_{mu nu}[g_obs]; no additional affine residual C_MTS is present in the local readout branch.",
            "EXACT_IF_LCZ2046_0_SIGNED",
            "the connection is universal and metric compatible",
            "LCZ2046_0 signature missing",
        ),
        (
            "LCZ2046_3_torsion_zero",
            "torsion vanishes",
            "T_MTS^lambda_{mu nu} = 2 Gamma_MTS^lambda_{[mu nu]} = 0 because the Levi-Civita connection is symmetric in the lower indices.",
            "EXACT_CONDITIONAL_ZERO",
            "axial torsion A_MTS^mu and c_A S_mu vanish in the local branch",
            "cannot promote until Gamma_MTS=LC[g_obs] is parent-signed",
        ),
        (
            "LCZ2046_4_nonmetricity_zero",
            "nonmetricity vanishes",
            "Q_MTS,rho mu nu := -nabla^Gamma_MTS_rho g_obs,mu nu = 0 for Gamma_MTS=LC[g_obs].",
            "EXACT_CONDITIONAL_ZERO",
            "Weyl/shear nonmetricity P4 rows vanish in the same branch",
            "cannot promote until Gamma_MTS=LC[g_obs] is parent-signed",
        ),
        (
            "LCZ2046_5_projective_silence",
            "no projective trace",
            "If there is no independent Gamma variable, the Palatini projective ambiguity never becomes a physical readout coefficient.",
            "EXACT_CONDITIONAL_ZERO",
            "trace/projective P4 row is killed by ontology rather than by a fitted small value",
            "if a Palatini independent Gamma is retained, projective silence still needs its own clause",
        ),
        (
            "LCZ2046_6_local_GR_impact",
            "connection gate impact",
            "LCZ2046_0 through LCZ2046_5 would close the torsion/nonmetricity connection family for the local exterior branch, but not the whole GR reduction alone.",
            "CONDITIONAL_STRONG_GATE",
            "turns one major local-GR obstruction into an exact zero theorem",
            "EH/no-extra/second-order/source-GM/PPN gates still need their own closure",
        ),
        (
            "LCZ2046_7_verdict",
            "LC-zero theorem status",
            "The local connection can be killed cleanly if the parent chooses metric/coframe-only observed geometry; current MTS has not signed that choice.",
            "THEOREM_AVAILABLE_NOT_PARENT_DERIVED",
            "this is the clean route and should be preferred if compatible with the corpus",
            "missing parent observed-geometry slot signature",
        ),
    ]
    rows = []
    for row_id, branch_piece, statement, status, if_closed, blocker in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "branch_piece": branch_piece,
                "statement": statement,
                "status": status,
                "if_closed": if_closed,
                "blocker": blocker,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def affine_residual_rows() -> list[dict[str, object]]:
    data = [
        (
            "AFF2046_0_residual_definition",
            "affine residual tensor",
            "If the parent retains an independent local affine branch, define C_MTS^lambda_{mu nu} := Gamma_MTS^lambda_{mu nu} - {lambda}_{mu nu}[g_obs].",
            "DEFINITION_READY_IF_GAMMA_EXISTS",
            "dimension L^-1 in geometric units",
            "MISSING_PARENT_GAMMA_MTS_FIELD",
        ),
        (
            "AFF2046_1_torsion_from_residual",
            "torsion tensor",
            "T_MTS^lambda_{mu nu} = 2 C_MTS^lambda_{[mu nu]} because LC[g_obs] has zero torsion.",
            "EXACT_COMPONENT_FORMULA",
            "dimension L^-1",
            "MISSING_C_MTS_COMPONENTS_AND_SIGN_CONVENTION",
        ),
        (
            "AFF2046_2_nonmetricity_from_residual",
            "nonmetricity tensor",
            "With Q_rho mu nu := -nabla^Gamma_rho g_mu nu, Q_MTS,rho mu nu = C_MTS^sigma_{rho mu} g_sigma nu + C_MTS^sigma_{rho nu} g_mu sigma under this sign convention.",
            "EXACT_COMPONENT_FORMULA_WITH_DECLARED_CONVENTION",
            "dimension L^-1",
            "MISSING_C_MTS_COMPONENTS_AND_Q_SIGN_CONVENTION",
        ),
        (
            "AFF2046_3_axial_projection",
            "axial torsion vector",
            "A_MTS^mu := (1/6) epsilon^{alpha beta gamma mu} T_MTS,alpha beta gamma = (1/3) epsilon^{alpha beta gamma mu} C_MTS,alpha[beta gamma].",
            "EXACT_COMPONENT_FORMULA_WITH_ORIENTATION",
            "feeds the 2045 KRT axial map",
            "MISSING_ORIENTATION_FRAME_AND_COMPONENT_LABEL",
        ),
        (
            "AFF2046_4_units",
            "natural-unit conversion",
            f"If A_MTS is computed in m^-1, the corresponding natural energy scale is A_GeV = {HBARC_GEV_M} * A_m^-1 before convention factors xi_A and C_basis.",
            "UNIT_BRIDGE_READY",
            "lets a future runner compare against GeV torsion-component bounds",
            "MISSING_A_MTS_VALUE_AND_COUPLING_FACTOR",
        ),
        (
            "AFF2046_5_spin_coupling",
            "observable spin kernel",
            "b_eff^mu = xi_A A_MTS^mu plus any convention-required vector/tensor torsion mixing; xi_A must be sourced from the chosen matter coupling.",
            "COUPLING_REQUIRED_NOT_FILLED",
            "would make the KRT bound scoreable",
            "MISSING_XI_A_AND_MIXING_MATRIX",
        ),
        (
            "AFF2046_6_no_cancellation_envelope",
            "absolute residual envelope",
            "Score only abs(xi_A C_basis A_MTS_component) <= bound_component with no cancellation against unmapped torsion/nonmetricity components.",
            "RUNNER_RULE_READY",
            "prevents hiding a live connection behind cancellations",
            "MISSING_NUMERIC_COMPONENTS",
        ),
        (
            "AFF2046_7_verdict",
            "affine-residual branch status",
            "The fallback is now tensor-defined, but non-numeric: it needs C_MTS components, xi_A, frame map, and a component-specific bound table before scoring.",
            "DEFINED_FALLBACK_NOT_SCOREABLE",
            "no more vague c_T/c_Q placeholder if the branch is chosen",
            "MISSING_PARENT_C_MTS_AND_COUPLING_INPUTS",
        ),
    ]
    rows = []
    for row_id, object_name, formula, status, units_or_use, blocker in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "object": object_name,
                "formula": formula,
                "status": status,
                "units_or_use": units_or_use,
                "blocker": blocker,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def decision_runner_rows() -> list[dict[str, object]]:
    data = [
        (
            "RUN2046_0_metric_coframe_branch",
            "LCZ2046_0_choice",
            "requires parent signature: local observed geometry has no independent affine Gamma_MTS slot",
            "NOT_ACCEPTED_CURRENT_CORPUS",
            "would set Gamma_MTS=LC[g_obs], T=0, Q=0, A_MTS=0",
            "MISSING_PARENT_OBSERVED_GEOMETRY_SLOT_SIGNATURE",
        ),
        (
            "RUN2046_1_palatini_branch",
            "PAL2042_3_lc_result",
            "requires Palatini-EH-only connection action, zero hypermomentum, and projective silence",
            "NOT_ACCEPTED_CURRENT_CORPUS",
            "would also force Gamma=LC(g_obs) modulo gauge",
            "MISSING_EH_ONLY_CONNECTION_ACTION_OR_PROJECTIVE_SILENCE",
        ),
        (
            "RUN2046_2_affine_residual_branch",
            "AFF2046_0_residual_definition",
            "requires parent C_MTS field, coefficients, units, source maps, and observable kernels",
            "DEFINED_BUT_NOT_SCOREABLE",
            "keeps torsion/nonmetricity as explicit P4 residuals",
            "MISSING_C_MTS_XI_A_FRAME_BOUND_INPUTS",
        ),
        (
            "RUN2046_VERDICT",
            "all_connection_branches",
            "the theory must now choose/sign metric-coframe LC zero or provide affine residual coefficients",
            "CONNECTION_FORK_EXPOSED_NONCLAIM",
            "this is the actual coupling fork, not another data loop",
            "PARENT_SIGNATURE_OR_NUMERIC_RESIDUAL_INPUTS_REQUIRED",
        ),
    ]
    rows = []
    for run_id, input_id, premise, status, outcome_if_closed, missing in data:
        row = base_row()
        row.update(
            {
                "run_id": run_id,
                "input_id": input_id,
                "premise": premise,
                "runner_status": status,
                "outcome_if_closed": outcome_if_closed,
                "missing": missing,
                "score_attempted": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        (
            "GATE2046_0_connection_owner",
            "Gamma_MTS owner selected",
            "FAIL_BLOCKED",
            "metric/coframe-only LC zero branch and affine-residual branch are both explicit, but neither is parent-selected",
        ),
        (
            "GATE2046_1_torsion_zero",
            "T_MTS=0 can be claimed",
            "FAIL_BLOCKED",
            "exact if Gamma_MTS=LC[g_obs], but that parent signature is missing",
        ),
        (
            "GATE2046_2_affine_residual_score",
            "C_MTS residual can be bounded",
            "FAIL_BLOCKED",
            "component values, coupling matrix, units, frame map, and bound rows are missing",
        ),
        (
            "GATE2046_3_KRT_torsion_score",
            "KRT torsion anchor can score MTS",
            "FAIL_BLOCKED",
            "2045 KRT map still waits on Gamma_MTS/C_MTS and xi_A",
        ),
        (
            "GATE2046_4_EH_Lovelock_route",
            "EH/Newton left-hand route can use Levi-Civita premise",
            "FAIL_BLOCKED",
            "LC theorem exists but is not parent-derived, so EH reduction remains conditional",
        ),
        (
            "GATE2046_5_local_GR_Newton",
            "derived local GR/Newton branch",
            "FAIL_BLOCKED",
            "connection fork is exposed, not closed; other EH/source/PPN gates remain open",
        ),
        (
            "GATE2046_6_public_claim",
            "public torsion/local-GR claim",
            "FAIL_BLOCKED",
            "private nonclaim checkpoint only",
        ),
    ]
    rows = []
    for row_id, gate, status, detail in data:
        row = base_row()
        row.update({"row_id": row_id, "gate": gate, "status": status, "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    data = [
        (
            "DEC2046_0_not_circling",
            "This checkpoint is a fork, not another pass around the same object.",
            "Either the local observed branch is metric/coframe-only and torsion dies exactly, or MTS must own an affine residual tensor C_MTS and pay every bound.",
        ),
        (
            "DEC2046_1_best_route",
            "Prefer the LC-zero route if the parent corpus can support it.",
            "It is cleaner than fitting c_A small: no independent Gamma slot gives Delta=0, Gamma=LC, T=0, Q=0 by structure.",
        ),
        (
            "DEC2046_2_fallback_route",
            "If MTS really needs an independent connection, it must be tensor-explicit.",
            "The fallback is C_MTS=Gamma_MTS-LC[g_obs], with torsion/nonmetricity projections, units, frame maps, and no-cancellation bounds.",
        ),
        (
            "DEC2046_3_honest_status",
            "We are closer because the missing coupling has been isolated to a binary parent-action choice.",
            "This does not prove local GR yet, but it removes the fog around the connection/coupling problem.",
        ),
    ]
    rows = []
    for row_id, decision, rationale in data:
        row = base_row()
        row.update({"row_id": row_id, "decision": decision, "rationale": rationale, "claim_allowed": False})
        rows.append(row)
    return rows


def next_target_rows() -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "target_id": "NEXT2046_0_2047",
            "target_doc": "2047-Y5-R2FR-parent-observed-geometry-slot-signature-or-CMTS-first-coefficient.md",
            "objective": "attempt to parent-sign the metric/coframe-only observed geometry slot so Gamma_MTS=LC[g_obs] and torsion/nonmetricity vanish; if that fails, fill the first C_MTS coefficient row with units and source map",
            "must_include": "parent action argument list; e_obs/g_obs ownership; spin connection omega_LC[e_obs]; source/clock/light/orbit no-Gamma clauses; explicit rejection or adoption of C_MTS; first coefficient row if adopted",
            "excluded": "claiming LC from GR notation; using KRT bound without xi_A; inventing C_MTS values; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    lc_rows: list[dict[str, object]],
    affine_rows: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2046_0_source_weight_lc_zero",
            SOURCE_WEIGHT_DOCS / "AFRAME_GAMMA_MTS_LC_ZERO_THEOREM_2046_NONCLAIM.csv",
            lc_rows,
        ),
        (
            "COPY2046_1_wep_affine_residual",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2046_AFFINE_RESIDUAL_RUNNER_INPUTS_NONCLAIM.csv",
            affine_rows,
        ),
        (
            "COPY2046_2_rab_next",
            QUEUE / "JR2046_PARENT_GEOMETRY_SLOT_SIGNATURE_NEXT_NONCLAIM.csv",
            next_rows_,
        ),
    ]
    rows = []
    for copy_id, path, data in copies:
        write_csv(path, data)
        row = base_row()
        row.update({"copy_id": copy_id, "path": str(path), "rows": len(data), "status": "WRITTEN_NONCLAIM_COPY"})
        rows.append(row)
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    lc_rows: list[dict[str, object]],
    affine_rows: list[dict[str, object]],
    runner_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    local_sources_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources)
    lc_verdict = next(row for row in lc_rows if row["row_id"] == "LCZ2046_7_verdict")
    affine_verdict = next(row for row in affine_rows if row["row_id"] == "AFF2046_7_verdict")
    runner_verdict = next(row for row in runner_rows if row["run_id"] == "RUN2046_VERDICT")
    connection_gate = next(row for row in gates if row["row_id"] == "GATE2046_0_connection_owner")
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2046_00_local_sources_exist", local_sources_ok, "all cited local source paths and needles exist"))
    checks.append(("VAL2046_01_csv_parse", all(csv_rows_parse(path) for path in csv_paths), "all generated CSV files parse cleanly"))
    checks.append(("VAL2046_02_lc_zero_not_promoted", lc_verdict["status"] == "THEOREM_AVAILABLE_NOT_PARENT_DERIVED", "LC-zero theorem is exact conditional but not promoted"))
    checks.append(("VAL2046_03_affine_fallback_defined", affine_verdict["status"] == "DEFINED_FALLBACK_NOT_SCOREABLE", "affine residual fallback is tensor-defined but not scoreable"))
    checks.append(("VAL2046_04_runner_exposes_fork", runner_verdict["runner_status"] == "CONNECTION_FORK_EXPOSED_NONCLAIM", "runner exposes metric/coframe-zero vs affine-residual fork"))
    checks.append(("VAL2046_05_claim_gates_closed", connection_gate["status"] == "FAIL_BLOCKED", "connection owner claim gate remains closed"))
    checks.append(("VAL2046_06_next_selected", next_rows_[0]["target_id"] == "NEXT2046_0_2047", "2047 parent observed-geometry slot target selected"))
    checks.append(("VAL2046_07_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2046_08_no_formalization_2046_artifacts", not formalization_has_2046_artifacts(), "no 2046 artifacts were written under formalization-workbench"))
    checks.append(("VAL2046_09_no_pycache", not scripts_pycache_exists(), "scripts __pycache__ removed"))
    overall_ok = all(ok for _, ok, _ in checks)
    checks.append(("VAL2046_OVERALL", overall_ok, "2046 exposes the GammaMTS fork: exact LC-zero theorem if parent-signed, explicit C_MTS residual if not"))
    rows = []
    for check_id, ok, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    lc_rows: list[dict[str, object]],
    affine_rows: list[dict[str, object]],
    runner_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2046 Y5 R2FR GammaMTS Affine Torsion Definition Or LC Zero Theorem",
        "",
        "## Current Verdict",
        "",
        "2046 is the connection fork. The clean route is now precise: if the parent observed local branch is metric/coframe-only, then `Gamma_MTS := LC[g_obs]`, `T_MTS=0`, `Q_MTS=0`, and the axial torsion coefficient vanishes without fitting. That is an exact conditional theorem, not yet a claim, because the parent action has not signed the observed-geometry slot across matter, spin, source, clocks, light and orbital readout.",
        "",
        "The fallback route is also now precise: if MTS keeps an independent affine connection, it must expose `C_MTS^lambda_{mu nu}=Gamma_MTS^lambda_{mu nu}-LC[g_obs]^lambda_{mu nu}`. Torsion, nonmetricity, axial projection, units, coupling, frame map and no-cancellation bounds then become mandatory. No local-GR, Newton, WEP, clock, orbital, PPN, R10, torsion, GitHub, or public claim is made.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_kind", "source_path", "status", "note", "valid_for_claim"]),
        "## LC-Zero Theorem Branch",
        md_table(lc_rows, ["row_id", "branch_piece", "statement", "status", "if_closed", "blocker", "claim_allowed"]),
        "## Affine Residual Fallback",
        md_table(affine_rows, ["row_id", "object", "formula", "status", "units_or_use", "blocker", "claim_allowed"]),
        "## Connection Decision Runner",
        md_table(runner_rows, ["run_id", "input_id", "premise", "runner_status", "outcome_if_closed", "missing", "score_attempted", "claim_allowed"]),
        "## Claim Gate",
        md_table(gates, ["row_id", "gate", "status", "detail", "claim_allowed"]),
        "## Decision Ledger",
        md_table(decisions, ["row_id", "decision", "rationale", "claim_allowed"]),
        "## Next Target",
        md_table(next_rows_, ["target_id", "target_doc", "objective", "must_include", "excluded", "claim_allowed"]),
        "## Branch Copies",
        md_table(copies, ["copy_id", "path", "rows", "status", "valid_for_claim"]),
        "## Validation",
        md_table(validation, ["check_id", "status", "detail", "claim_allowed"]),
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    lc_rows = lc_zero_theorem_rows()
    affine_rows = affine_residual_rows()
    runner_rows = decision_runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2046_SOURCE_REGISTER.csv",
        "lc": OUT / "P8_Y5_PARENT_QLOC_2046_LC_ZERO_THEOREM_BRANCH.csv",
        "affine": OUT / "P8_Y5_PARENT_QLOC_2046_AFFINE_RESIDUAL_DEFINITION.csv",
        "runner": OUT / "P8_Y5_PARENT_QLOC_2046_CONNECTION_DECISION_RUNNER.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2046_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2046_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2046_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2046_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2046_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["lc"], lc_rows)
    write_csv(paths["affine"], affine_rows)
    write_csv(paths["runner"], runner_rows)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(lc_rows, affine_rows, next_rows_)
    write_csv(paths["branch"], copies)
    remove_pycache()
    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [Path(row["path"]) for row in copies]
    validation = validation_rows(sources, lc_rows, affine_rows, runner_rows, gates, next_rows_, csv_paths_without_validation)
    write_csv(paths["validation"], validation)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in copies]
    remove_pycache()
    validation = validation_rows(sources, lc_rows, affine_rows, runner_rows, gates, next_rows_, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, lc_rows, affine_rows, runner_rows, gates, decisions, next_rows_, copies, validation)
    remove_pycache()


if __name__ == "__main__":
    main()
