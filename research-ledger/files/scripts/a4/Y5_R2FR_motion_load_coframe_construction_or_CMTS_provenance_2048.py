from __future__ import annotations

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


DOC = ROOT / "2048-Y5-R2FR-motion-load-coframe-construction-or-CMTS-provenance.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()


def formalization_has_2048_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        patterns = (
            "*2048-Y5-R2FR*",
            "*P8_Y5_PARENT_QLOC_2048*",
            "*Y5_R2FR_motion_load_coframe_construction_or_CMTS_provenance_2048*",
        )
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def scripts_pycache_exists() -> bool:
    return (SCRIPT_PATH.parent / "__pycache__").exists()


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2048_00_2047_doc",
            ROOT / "2047-Y5-R2FR-parent-observed-geometry-slot-signature-or-CMTS-first-coefficient.md",
            ["NEXT2047_0_2048", "CMTS2047_VERDICT", "VAL2047_OVERALL"],
            "2047 selected primitive motion-load coframe construction or C_MTS provenance.",
        ),
        (
            "SRC2048_01_motion_load_contract",
            ROOT / "01-motion-load-route-contract.md",
            ["c^2 = v_space^2", "S_p(r)", "p = 1"],
            "motion-load primitive scaffold and promotion criteria.",
        ),
        (
            "SRC2048_02_local_GR_reduction",
            ROOT / "02-motion-load-local-GR-reduction.md",
            ["motion_load_local_GR_reduction_conditional_not_promoted", "gamma = p", "beta completion = conditional"],
            "conditional local-GR weak-field reduction source.",
        ),
        (
            "SRC2048_03_phase_volume",
            ROOT / "08-phase-volume-reciprocity-origin.md",
            ["T sqrt(S) = 1", "generic volume principles are rejected", "phase-volume balance motivates the route"],
            "phase-volume radial-cell motivation and generic-volume rejection.",
        ),
        (
            "SRC2048_04_hamiltonian_cell",
            ROOT / "09-hamiltonian-radial-cell-derivation.md",
            ["generic symplectic or Liouville phase-volume preservation does not derive p=1", "J_tr = T sqrt(S)", "radial observer cell"],
            "Hamiltonian/Liouville obstruction source.",
        ),
        (
            "SRC2048_05_observer_contract",
            ROOT / "10-observer-map-symplectic-contract.md",
            ["theta_0 = T c dt", "R_AB = ln(T^2 S)", "That is the exact missing theorem"],
            "observer coframe and radial-cell contract source.",
        ),
        (
            "SRC2048_06_1859_noGR",
            ROOT / "1859-Y5-R2FR-motion-load-phase-volume-parent-origin-no-GR-import-derivation.md",
            ["MPD1859_6_best_surviving_route", "FRS1859_2_parent_Euler_difference", "VAL1859_OVERALL"],
            "later no-GR-import derivation audit selecting parent Euler/source-map route.",
        ),
        (
            "SRC2048_07_2047_cmts",
            OUT / "P8_Y5_PARENT_QLOC_2047_CMTS_FIRST_COEFFICIENT_CHAIN.csv",
            ["CMTS2047_0_C_tensor", "CMTS2047_VERDICT"],
            "C_MTS fallback coefficient chain from 2047.",
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


def coframe_construction_rows() -> list[dict[str, object]]:
    data = [
        (
            "MLC2048_0_clock_load",
            "clock-load lapse",
            "T^2(r)=1-L(r), L(r)=2GM/(r c^2), from d tau/dt=v_clock/c=sqrt(1-L) in the static load branch.",
            "PRIMITIVE_CLOCK_SIDE_DEFINED",
            "dimensionless T; dimensionless L",
            "Newtonian load side is defined, but source GM ownership remains separate",
        ),
        (
            "MLC2048_1_routing_scale",
            "radial routing scale",
            "S_p(r)=(1-L)^(-p), so theta^1=sqrt(S_p) dr and gamma=p at first post-Newtonian order.",
            "ROUTING_FAMILY_DEFINED",
            "dimensionless S; p dimensionless",
            "p is not fixed unless R_AB=0 or equivalent parent law is derived",
        ),
        (
            "MLC2048_2_observed_coframe",
            "motion-load observed coframe",
            "theta^0=T c dt; theta^1=sqrt(S) dr; theta^2=r dtheta; theta^3=r sin(theta) dphi.",
            "LOCAL_COFRAME_CONSTRUCTED",
            "orthonormal coframe units",
            "static spherical branch only; not yet a universal parent matter/readout coframe",
        ),
        (
            "MLC2048_3_observed_metric",
            "metric from coframe",
            "g_obs=-(theta^0)^2+(theta^1)^2+(theta^2)^2+(theta^3)^2 = -T^2 c^2 dt^2 + S dr^2 + r^2 dOmega^2.",
            "LOCAL_METRIC_CONSTRUCTED",
            "metric line element",
            "not a parent field equation yet",
        ),
        (
            "MLC2048_4_LC_spin_connection",
            "torsion-free coframe connection",
            "Cartan: dtheta^a + omega^a_b wedge theta^b=0 gives omega^0_1=(T'/(T sqrt(S)))theta^0, omega^2_1=(1/(r sqrt(S)))theta^2, omega^3_1=(1/(r sqrt(S)))theta^3, omega^3_2=(cot(theta)/r)theta^3 plus antisymmetry.",
            "LC_CONNECTION_CONSTRUCTED_FROM_COFRAME",
            "inverse length",
            "requires the ordinary spin connection to be this LC object, not an independent torsionful slot",
        ),
        (
            "MLC2048_5_torsion_zero_by_construction",
            "torsion status in coframe branch",
            "Torsion two-forms T^a=dtheta^a+omega^a_b wedge theta^b vanish identically for the constructed LC connection.",
            "EXACT_WITHIN_CONSTRUCTED_LC_BRANCH",
            "zero",
            "does not prove the parent forbids a separate C_MTS branch",
        ),
        (
            "MLC2048_6_radial_cell_condition",
            "reciprocal observer cell",
            "J_q=T sqrt(S); R_AB=ln(T^2 S)=2 ln(J_q); R_AB=0 iff T^2 S=1 iff p=1 for S_p=(1-L)^(-p).",
            "EXACT_CONDITIONAL_GR_LANE",
            "dimensionless",
            "R_AB=0 parent origin is still missing",
        ),
        (
            "MLC2048_7_ppn_lane",
            "weak-field PPN lane",
            "gamma=p; if R_AB=0 then p=1 and gamma=1. Beta=1 follows only under the exact Schwarzschild-like reciprocal completion and valid PPN coordinate construction.",
            "PPN_CONDITIONAL_NOT_PROMOTED",
            "dimensionless PPN parameters",
            "beta completion and parent field equation are not derived here",
        ),
        (
            "MLC2048_8_verdict",
            "motion-load coframe result",
            "The primitive route constructs e_obs, g_obs and omega_LC[e_obs] locally; it does not yet derive the parent law R_AB=0 or universal matter/readout use of this coframe.",
            "COFRAME_CONSTRUCTED_PARENT_ORIGIN_MISSING",
            "useful bridge to 2047",
            "no local-GR/Newton promotion",
        ),
    ]
    rows = []
    for row_id, object_name, formula, status, units, blocker in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "object": object_name,
                "formula": formula,
                "status": status,
                "units": units,
                "blocker": blocker,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def parent_origin_audit_rows() -> list[dict[str, object]]:
    data = [
        (
            "POA2048_0_observed_geometry_slot",
            "2047 OGS clauses",
            "The constructed coframe supplies the object requested by OGS2047, but not the parent action signature that all ordinary sectors must use it.",
            "OBJECT_SUPPLIED_SIGNATURE_NOT_SIGNED",
            "ordinary matter/source/readout action-domain proof",
        ),
        (
            "POA2048_1_reciprocal_constraint",
            "R_AB=0",
            "The radial cell condition exactly selects p=1, but 08/09/10/1859 show direct phase-volume, Liouville, null and current shortcuts do not derive it.",
            "PARENT_ORIGIN_MISSING",
            "MTS-owned Euler difference or no-charge source/boundary theorem",
        ),
        (
            "POA2048_2_connection_fork",
            "Gamma_MTS",
            "If the coframe branch is parent-selected, Gamma_MTS=LC[g_obs] and C_MTS=0. If an independent connection remains, CMTS2047 rows must be sourced.",
            "FORK_REDUCED_NOT_CLOSED",
            "parent branch selection or C_MTS coefficient provenance",
        ),
        (
            "POA2048_3_no_GR_import",
            "no Schwarzschild import",
            "Using T^2=1-L and S=1/(1-L) is allowed only as a conditional reciprocal completion, not as proof imported from Einstein vacuum equations.",
            "NO_IMPORT_GUARD_RETAINED",
            "derive R_AB=0 from MTS parent equations",
        ),
        (
            "POA2048_4_best_surviving_route",
            "parent Euler/source-map route",
            "1859 selects E_time-E_radial/source-map/boundary/no-charge certificates as the strongest noncircular derivation path for R_AB=0.",
            "SELECT_PRIMARY_NEXT_PROOF_CHAIN",
            "construct MTS time/radial Euler equations or retain finite R_AB residual",
        ),
        (
            "POA2048_5_verdict",
            "parent-origin audit",
            "2048 upgrades the LC route from abstract signature to concrete local coframe, but the decisive theorem is still parent-owned R_AB=0 plus universal coframe coupling.",
            "COFRAME_BRIDGE_PROGRESS_NO_PROMOTION",
            "derive Euler difference next",
        ),
    ]
    rows = []
    for row_id, gate, evidence, status, needed in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "gate": gate,
                "evidence": evidence,
                "status": status,
                "needed_next": needed,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def cmts_decision_rows() -> list[dict[str, object]]:
    data = [
        (
            "CDEC2048_0_coframe_LC_branch",
            "C_MTS=0 within constructed coframe branch",
            "If Gamma_MTS is defined as omega_LC[e_obs] from MLC2048_4, then the affine residual C_MTS vanishes by definition.",
            "CONDITIONAL_ZERO_BRANCH",
            "requires parent selection of the coframe LC branch",
        ),
        (
            "CDEC2048_1_independent_connection_branch",
            "retain C_MTS if any independent connection remains",
            "Any torsionful/nonmetric connection not equal to LC[e_obs] must be projected into CMTS2047 coefficient rows.",
            "FINITE_RESIDUAL_BACKSTOP",
            "requires C_MTS components, coupling, frame map and source bounds",
        ),
        (
            "CDEC2048_2_runner_policy",
            "no mixed shortcut",
            "Do not use the coframe construction to claim LC while also using independent C_MTS effects as hidden phenomenology.",
            "BRANCH_EXCLUSIVITY_REQUIRED",
            "select LC-zero or score C_MTS explicitly",
        ),
    ]
    rows = []
    for row_id, decision, rule, status, required in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "decision": decision,
                "rule": rule,
                "status": status,
                "required_before_claim": required,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def runner_rows() -> list[dict[str, object]]:
    data = [
        (
            "RUN2048_0_construct_coframe",
            "MLC2048_2_observed_coframe",
            "ACCEPTED_AS_LOCAL_CONSTRUCTION",
            "e_obs/g_obs/omega_LC are explicitly defined for the static motion-load branch",
            "false",
        ),
        (
            "RUN2048_1_claim_parent_signature",
            "POA2048_0_observed_geometry_slot",
            "REJECTED_SIGNATURE_NOT_PARENT_SIGNED",
            "constructed object is not the same as proof every ordinary sector must use it",
            "false",
        ),
        (
            "RUN2048_2_claim_RAB_zero",
            "MLC2048_6_radial_cell_condition",
            "REJECTED_PARENT_ORIGIN_MISSING",
            "R_AB=0 selects GR lane but remains a missing parent law",
            "false",
        ),
        (
            "RUN2048_3_claim_local_GR",
            "MLC2048_7_ppn_lane",
            "REJECTED_BETA_EULER_SOURCE_GATES_OPEN",
            "gamma=1 conditional is not full GR/Newton derivation",
            "false",
        ),
        (
            "RUN2048_VERDICT",
            "all_2048_rows",
            "COFRAME_BRIDGE_BUILT_NONCLAIM",
            "2048 makes the LC route concrete and selects parent Euler difference as the next derivation target",
            "false",
        ),
    ]
    rows = []
    for run_id, input_id, verdict, reason, claim_allowed in data:
        row = base_row()
        row.update(
            {
                "run_id": run_id,
                "input_id": input_id,
                "verdict": verdict,
                "reason": reason,
                "claim_allowed": claim_allowed == "true",
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("GATE2048_0_coframe_defined", "motion-load coframe is locally defined", "PASS_NONCLAIM", "static branch e_obs/g_obs/omega_LC constructed"),
        ("GATE2048_1_parent_signature", "all ordinary sectors must use this coframe", "FAIL_BLOCKED", "action-domain signature remains unsigned"),
        ("GATE2048_2_RAB_zero", "R_AB=0 derived", "FAIL_BLOCKED", "radial-cell parent origin missing"),
        ("GATE2048_3_Gamma_LC", "Gamma_MTS=LC[g_obs] claimed", "FAIL_BLOCKED", "LC branch is constructed but not parent-selected"),
        ("GATE2048_4_PPN_GR", "PPN gamma=beta=1 and local GR/Newton derived", "FAIL_BLOCKED", "gamma lane conditional; beta/Euler/source/conservation gates open"),
        ("GATE2048_5_CMTS_score", "C_MTS fallback scoreable", "FAIL_BLOCKED", "fallback rows inherited from 2047 remain unfilled"),
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
            "DEC2048_0_real_progress",
            "The abstract observed-geometry slot is now a concrete motion-load coframe in the static branch.",
            "This directly improves the 2047 LC route: `omega_LC[e_obs]` is no longer only a slogan.",
        ),
        (
            "DEC2048_1_main_missing_theorem",
            "The hard theorem is now `R_AB=0`, not the existence of a coframe.",
            "`T sqrt(S)=1` is exactly the GR lane; deriving it from MTS parent dynamics is the next bottleneck.",
        ),
        (
            "DEC2048_2_best_route",
            "Use the 1859 parent Euler/source-map equation-difference route next.",
            "It is less axiom-like than radial-cell closure and avoids importing Schwarzschild or Einstein vacuum equations.",
        ),
        (
            "DEC2048_3_backstop",
            "If the Euler difference cannot be derived, retain finite `R_AB` and `C_MTS` residuals.",
            "That keeps the theory testable without pretending the GR reduction has been earned.",
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
            "target_id": "NEXT2048_0_2049",
            "target_doc": "2049-Y5-R2FR-motion-load-parent-Euler-difference-or-RAB-finite-residual.md",
            "objective": "try to derive an MTS-owned time/radial parent Euler difference D_R[MTS]=partial_r C_R-S_R=0 for the motion-load coframe; prove S_R=0 and no radial-cell charge in the local branch, or stage finite R_AB residual rows",
            "must_include": "E_time; E_radial; C_R=ln(T^2S); source map S_R; boundary/no-charge rule; no-GR-import guard; beta/gamma consequence; finite R_AB fallback",
            "excluded": "using Einstein vacuum equations; imposing T^2S=1 as closure; claiming local GR from gamma alone; inventing residual values; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    coframe_rows: list[dict[str, object]],
    parent_rows: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2048_0_source_weight_motion_load_coframe",
            SOURCE_WEIGHT_DOCS / "AFRAME_MOTION_LOAD_COFRAME_2048_NONCLAIM.csv",
            coframe_rows,
        ),
        (
            "COPY2048_1_wep_parent_origin_audit",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2048_PARENT_ORIGIN_AUDIT_NONCLAIM.csv",
            parent_rows,
        ),
        (
            "COPY2048_2_rab_next",
            QUEUE / "JR2048_PARENT_EULER_DIFFERENCE_NEXT_NONCLAIM.csv",
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
    coframe_rows: list[dict[str, object]],
    parent_rows: list[dict[str, object]],
    cmts_rows: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources)
    coframe_verdict = next(row for row in coframe_rows if row["row_id"] == "MLC2048_8_verdict")
    parent_verdict = next(row for row in parent_rows if row["row_id"] == "POA2048_5_verdict")
    cmts_policy = next(row for row in cmts_rows if row["row_id"] == "CDEC2048_2_runner_policy")
    runner_verdict = next(row for row in runner if row["run_id"] == "RUN2048_VERDICT")
    coframe_gate = next(row for row in gates if row["row_id"] == "GATE2048_0_coframe_defined")
    gr_gate = next(row for row in gates if row["row_id"] == "GATE2048_4_PPN_GR")
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2048_00_local_sources_exist", source_ok, "all cited local source paths and needles exist"))
    checks.append(("VAL2048_01_csv_parse", all(csv_rows_parse(path) for path in csv_paths), "all generated CSV files parse cleanly"))
    checks.append(("VAL2048_02_coframe_constructed_nonclaim", coframe_verdict["status"] == "COFRAME_CONSTRUCTED_PARENT_ORIGIN_MISSING", "motion-load coframe is constructed but nonclaim"))
    checks.append(("VAL2048_03_parent_origin_missing", parent_verdict["status"] == "COFRAME_BRIDGE_PROGRESS_NO_PROMOTION", "parent origin audit blocks promotion"))
    checks.append(("VAL2048_04_cmts_policy_retained", cmts_policy["status"] == "BRANCH_EXCLUSIVITY_REQUIRED", "C_MTS fallback retained only as explicit branch"))
    checks.append(("VAL2048_05_runner_rejects_claims", runner_verdict["verdict"] == "COFRAME_BRIDGE_BUILT_NONCLAIM", "runner rejects parent/local-GR claims"))
    checks.append(("VAL2048_06_coframe_gate_pass_only_nonclaim", coframe_gate["status"] == "PASS_NONCLAIM", "only the coframe-definition gate passes, nonclaim"))
    checks.append(("VAL2048_07_GR_gate_blocked", gr_gate["status"] == "FAIL_BLOCKED", "local-GR/PPN gate remains blocked"))
    checks.append(("VAL2048_08_next_selected", next_rows_[0]["target_id"] == "NEXT2048_0_2049", "2049 parent Euler difference target selected"))
    checks.append(("VAL2048_09_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2048_10_no_formalization_2048_artifacts", not formalization_has_2048_artifacts(), "no 2048 artifacts were written under formalization-workbench"))
    checks.append(("VAL2048_11_no_pycache", not scripts_pycache_exists(), "scripts __pycache__ removed"))
    overall_ok = all(ok for _, ok, _ in checks)
    checks.append(("VAL2048_OVERALL", overall_ok, "2048 builds the motion-load coframe/LC bridge and selects parent Euler difference as next proof target"))
    rows = []
    for check_id, ok, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    coframe_rows: list[dict[str, object]],
    parent_rows: list[dict[str, object]],
    cmts_rows: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2048 Y5 R2FR Motion-Load Coframe Construction Or C_MTS Provenance",
        "",
        "## Current Verdict",
        "",
        "2048 makes a real forward move: the motion-load route can construct a local observed coframe, metric, and Levi-Civita spin connection in the static branch. The coframe is `theta^0=T c dt`, `theta^1=sqrt(S) dr`, `theta^2=r dtheta`, `theta^3=r sin(theta)dphi`; its LC connection has zero torsion by Cartan's first structure equation.",
        "",
        "This helps the 2047 connection problem, because `Gamma_MTS=LC[g_obs]` is now a concrete branch rather than just a slogan. But it still does not prove local GR: the parent theory must derive `R_AB=ln(T^2S)=0`, i.e. `T sqrt(S)=1`, and prove all ordinary matter/source/readout sectors use this coframe. No local-GR, Newton, WEP, clock, orbital, PPN, R10, torsion, GitHub, or public claim is made.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_kind", "source_path", "status", "note", "valid_for_claim"]),
        "## Motion-Load Coframe Construction",
        md_table(coframe_rows, ["row_id", "object", "formula", "status", "units", "blocker", "claim_allowed"]),
        "## Parent-Origin Audit",
        md_table(parent_rows, ["row_id", "gate", "evidence", "status", "needed_next", "claim_allowed"]),
        "## C_MTS Branch Decision",
        md_table(cmts_rows, ["row_id", "decision", "rule", "status", "required_before_claim", "claim_allowed"]),
        "## Runner Refusals",
        md_table(runner, ["run_id", "input_id", "verdict", "reason", "claim_allowed"]),
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
    coframe_rows = coframe_construction_rows()
    parent_rows = parent_origin_audit_rows()
    cmts_rows = cmts_decision_rows()
    runner = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2048_SOURCE_REGISTER.csv",
        "coframe": OUT / "P8_Y5_PARENT_QLOC_2048_MOTION_LOAD_COFRAME_CONSTRUCTION.csv",
        "parent": OUT / "P8_Y5_PARENT_QLOC_2048_PARENT_ORIGIN_AUDIT.csv",
        "cmts": OUT / "P8_Y5_PARENT_QLOC_2048_CMTS_BRANCH_DECISION.csv",
        "runner": OUT / "P8_Y5_PARENT_QLOC_2048_RUNNER_REFUSALS.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2048_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2048_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2048_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2048_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2048_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["coframe"], coframe_rows)
    write_csv(paths["parent"], parent_rows)
    write_csv(paths["cmts"], cmts_rows)
    write_csv(paths["runner"], runner)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(coframe_rows, parent_rows, next_rows_)
    write_csv(paths["branch"], copies)
    remove_pycache()
    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [Path(row["path"]) for row in copies]
    validation = validation_rows(sources, coframe_rows, parent_rows, cmts_rows, runner, gates, next_rows_, csv_paths_without_validation)
    write_csv(paths["validation"], validation)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in copies]
    remove_pycache()
    validation = validation_rows(sources, coframe_rows, parent_rows, cmts_rows, runner, gates, next_rows_, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, coframe_rows, parent_rows, cmts_rows, runner, gates, decisions, next_rows_, copies, validation)
    remove_pycache()


if __name__ == "__main__":
    main()
