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
DOC = ROOT / "2006-Y5-R2FR-parent-EqPhi-coframe-readout-map-or-owned-coframe-closure-demotion.md"
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
            "SRC2006_00_2005_handoff",
            "2005-Y5-R2FR-parent-action-clause-extraction-for-local-GR-signature.md",
            ["NEXT2005_0_2006", "e_obs=E[q(Phi_MTS)]", "VAL2005_OVERALL"],
            "2005 selected the parent coframe-readout map as the next non-circling target.",
        ),
        (
            "SRC2006_01_1964_legitimacy",
            "1964-Y5-R2FR-owned-coframe-legitimacy-and-EH-second-order-gate.md",
            ["LEG1964_3_MTS_readout_contract", "LEG1964_5_legitimacy_verdict", "EH2_1964_2_central_blocker"],
            "1964 says the coframe is source-supported but missing E[q(Phi_MTS)].",
        ),
        (
            "SRC2006_02_1963_action",
            "1963-Y5-R2FR-minimal-owned-coframe-parent-action-or-P4-hypermomentum-row.md",
            ["ACT1963_1_variable_list", "NGT1963_0_theorem", "NGT1963_2_q_vertical_silence"],
            "1963 action skeleton and no-Gamma theorem inside the owned-coframe branch.",
        ),
        (
            "SRC2006_03_observer_contract",
            "10-observer-map-symplectic-contract.md",
            ["The local observer coframe must be defined before any PPN claim", "all matter sectors couple to the same observer coframe"],
            "observer coframe and universal matter coframe requirement.",
        ),
        (
            "SRC2006_04_radial_cell",
            "09-hamiltonian-radial-cell-derivation.md",
            ["defined clock-load coframe", "defined radial routing coframe", "Hamiltonian law derives separate radial cell"],
            "radial clock/routing coframe seed and its non-derived parent origin.",
        ),
        (
            "SRC2006_05_943_coframe",
            "943-Y5-R10-single-observed-coframe-matter-coupling-contract-or-frame-residual-source-pack.md",
            ["e_obs(Phi) = Obs_e(q(Phi))", "CFC943_2_matter_functor", "DER943_6_verdict"],
            "quotient observed-coframe descent and matter-functor contract.",
        ),
        (
            "SRC2006_06_944_descent",
            "944-Y5-R10-quotient-observed-coframe-descent-proof-or-frame-leak-source-bounds.md",
            ["QDG944_2_observed_coframe_functor", "P944_1_chain_rule_coframe", "P944_7_verdict"],
            "valid chain-rule descent theorem but missing parent q/Obs_e.",
        ),
        (
            "SRC2006_07_945_q_candidate",
            "945-Y5-R10-parent-q-map-Obs-e-functor-construction-or-first-frame-leak-bound-pack.md",
            ["QMAP945_2_observed_functor", "QMAP945_4_presymplectic_ownership", "DEC945_0_candidate_q"],
            "candidate q/Obs_e construction and projection-by-declaration warning.",
        ),
        (
            "SRC2006_08_785_stack",
            "785-Y5-R10-psi-metric-coframe-connection-contract-or-bg-residual-lock.md",
            ["PMC785_2_local_coframe_existence", "PMC785_5_matter_metric_only_coupling", "PMC785_6_parent_action_metric_ownership"],
            "metric/coframe/connection stack conditional and parent-action ownership blocker.",
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
                "needed_for": "2006 parent E[q(Phi)] coframe readout map or closure demotion",
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


def coframe_map_attempt_rows() -> list[dict[str, object]]:
    specs = [
        (
            "EQP2006_0_parent_object",
            "Phi_MTS",
            "parent motion/time/space data containing clock-load, routing, observer-cell, local geometry, matter, gauge, boundary, and residual-sector variables",
            "FIELD_INVENTORY_SUPPORTED_NOT_ACTION_COMPLETE",
            "current documents identify required ingredients but not a full variational parent object",
            "false",
        ),
        (
            "EQP2006_1_quotient_map",
            "q: Phi_MTS -> Q_readout",
            "Q_readout must be fixed before matter coupling and contain only operational local readout data, not arbitrary representative fields",
            "CANDIDATE_REQUIRED_NOT_PARENT_SIGNED",
            "945 can write q_candidate, but kernel/null ownership is missing",
            "false",
        ),
        (
            "EQP2006_2_clock_leg",
            "e_obs^0 = N_tau(q) tau_clock",
            "clock-load one-form supplies the time leg of the operational coframe",
            "RADIAL_CLOCK_SEED_SUPPORTED",
            "09/10 support clock coframe language, but not full parent normalization or universal clock-sector proof",
            "false",
        ),
        (
            "EQP2006_3_radial_leg",
            "e_obs^1 = N_r(q) rho_radial",
            "radial routing one-form supplies the radial spatial leg in the local exterior/radial-cell branch",
            "RADIAL_ROUTING_SEED_SUPPORTED",
            "radial branch support does not produce a full 3D spatial triad",
            "false",
        ),
        (
            "EQP2006_4_transverse_legs",
            "e_obs^2,e_obs^3 = E_perp^A(q)",
            "two transverse ruler/angle legs complete the tetrad and protect nondegenerate four-volume",
            "MISSING_FULL_TETRAD_COMPLETION",
            "current inspected sources do not derive the transverse anholonomic coframe from MTS parent variables",
            "false",
        ),
        (
            "EQP2006_5_nonintegrable_coframe",
            "de_obs^a may be nonzero",
            "the coframe cannot be reduced to four exact scalar gradients; anholonomy is needed for generic curved/tidal frames",
            "REQUIREMENT_RECORDED_FROM_1964",
            "need a frame-deformation/one-form parent field or equivalent rank-surjective map",
            "false",
        ),
        (
            "EQP2006_6_lorentz_gauge",
            "e_obs ~ Lambda(x)e_obs",
            "local Lorentz rotations are gauge representatives, not matter-visible extra couplings",
            "GAUGE_REQUIREMENT_IDENTIFIED",
            "gauge blindness/matter representation proof remains conditional",
            "false",
        ),
        (
            "EQP2006_7_universal_functor",
            "S_matter = sum_A S_A[Psi_A,e_obs,omega_LC[e_obs],A_owned,theta_A]",
            "all ordinary matter uses the same descended coframe and induced connection",
            "CONTRACT_AVAILABLE_NOT_PARENT_SIGNED",
            "943/1963 write the functor, but constants, masses, boundary tails, and readout order remain unsigned",
            "false",
        ),
        (
            "EQP2006_8_readout_map_verdict",
            "e_obs = E[q(Phi_MTS)]",
            "a partial radial/clock seed exists, but the full nondegenerate tetrad map is not derived from the current corpus",
            "PARTIAL_DERIVATION_NOT_FULL_PARENT_SIGNATURE",
            "ACT1963 cannot be canonicalized yet; it remains an explicit closure branch until full tetrad completion is proved",
            "false",
        ),
    ]
    rows: list[dict[str, object]] = []
    for map_id, object_name, construction, status, blocker, parent_signed in specs:
        row = base_row()
        row.update(
            {
                "map_id": map_id,
                "object": object_name,
                "construction_or_requirement": construction,
                "status": status,
                "blocker": blocker,
                "parent_signed": parent_signed,
            }
        )
        rows.append(row)
    return rows


def radial_seed_rows() -> list[dict[str, object]]:
    specs = [
        (
            "RSEED2006_0_clock_load",
            "e^0 clock/load leg",
            "09 and 10 require a clock-load coframe before local PPN/Newton claims",
            "SUPPORTED_SEED",
            "normalization, universality, and parent action ownership not complete",
        ),
        (
            "RSEED2006_1_radial_routing",
            "e^1 radial routing leg",
            "09 identifies radial routing coframe and separate radial observer-cell conservation as the GR lane",
            "SUPPORTED_SEED",
            "radial cell origin still not parent-derived",
        ),
        (
            "RSEED2006_2_full_spatial_triads",
            "e^1,e^2,e^3 spatial ruler triad",
            "full tetrad needs two transverse one-forms beyond the radial leg",
            "MISSING_COMPLETION",
            "no source signs transverse ruler/angle coframe from MTS variables",
        ),
        (
            "RSEED2006_3_local_volume",
            "det(e_obs) != 0",
            "full local matter/metric branch needs nondegenerate four-volume and Lorentz signature",
            "MISSING_PROOF",
            "radial two-leg seed cannot prove full determinant nonzero",
        ),
        (
            "RSEED2006_4_status",
            "radial seed value",
            "seed is real and useful for spherical/PPN scaffolding but not enough for fundamental field theory",
            "PARTIAL_ONLY",
            "needs full tetrad completion or labelled closure",
        ),
    ]
    rows: list[dict[str, object]] = []
    for seed_id, element, evidence, status, remaining_gap in specs:
        row = base_row()
        row.update(
            {
                "seed_id": seed_id,
                "element": element,
                "evidence": evidence,
                "status": status,
                "remaining_gap": remaining_gap,
            }
        )
        rows.append(row)
    return rows


def full_tetrad_gap_rows() -> list[dict[str, object]]:
    specs = [
        ("TGAP2006_0_parent_E_map", "derive E[q(Phi_MTS)] without inserting e_obs by declaration", "MISSING", "prevents projection-by-declaration"),
        ("TGAP2006_1_transverse_triad", "derive two transverse anholonomic ruler/angle one-forms", "MISSING", "prevents full 4D coframe claim"),
        ("TGAP2006_2_nonzero_det", "prove det(e_obs) bounded away from zero on local branch", "MISSING", "prevents local Lorentzian metric domain"),
        ("TGAP2006_3_lorentz_gauge_blindness", "prove local Lorentz frame choices are gauge for all matter/readout sectors", "UNSIGNED", "prevents tetrad representative couplings"),
        ("TGAP2006_4_universal_matter_functor", "prove all ordinary matter sees only e_obs, omega_LC[e_obs], owned gauge fields, and constants", "UNSIGNED", "prevents hidden source/WEP currents"),
        ("TGAP2006_5_boundary_no_tail", "prove vertical/readout variations have no compact local boundary/source tail", "UNSIGNED", "prevents non-Hilbert readout source leakage"),
        ("TGAP2006_6_EH_second_order", "prove surviving local exterior operator is second-order EH or residuals executable", "OPEN_NEXT_FORK", "prevents GR/Newton source equation claim"),
    ]
    rows: list[dict[str, object]] = []
    for gap_id, requirement, status, consequence in specs:
        row = base_row()
        row.update(
            {
                "gap_id": gap_id,
                "requirement": requirement,
                "status": status,
                "consequence": consequence,
                "blocks_local_GR_claim": "true",
            }
        )
        rows.append(row)
    return rows


def closure_demotion_rows() -> list[dict[str, object]]:
    specs = [
        (
            "CLOS2006_0_ACT1963_status",
            "ACT1963 owned-coframe action skeleton",
            "DOWNGRADE_TO_EXPLICIT_CLOSURE_BRANCH",
            "full E[q(Phi_MTS)] coframe map is partial only",
            "can be used as a private theorem sandbox, not as a derived parent action",
        ),
        (
            "CLOS2006_1_noGamma_status",
            "NGT1963 no-independent-Gamma theorem",
            "VALID_INSIDE_CLOSURE_BRANCH",
            "the theorem is mathematically valid if the branch is assumed",
            "does not globally kill P4 unless ACT1963 is canonicalized",
        ),
        (
            "CLOS2006_2_frame_residuals",
            "frame/coframe leakage",
            "RETAIN_RESIDUAL_INTERFACE",
            "full tetrad and universal matter descent remain unsigned",
            "keep c_g, b_dis, b_A, q_nonH, readout_marker rows active",
        ),
        (
            "CLOS2006_3_R11_P4_residuals",
            "R11/P4/source residual branch",
            "ACTIVE_FALLBACK",
            "local exterior operator and connection alternatives are not fully derived",
            "route tests through executable residual rows unless the next derivation closes gaps",
        ),
        (
            "CLOS2006_4_public_language",
            "claim wording",
            "PRIVATE_NONCLAIM_ONLY",
            "closure branch is not embarrassing, but it is not a public GR derivation",
            "say 'conditional owned-coframe closure branch', not 'MTS derives GR'",
        ),
    ]
    rows: list[dict[str, object]] = []
    for closure_id, object_name, status, reason, allowed_use in specs:
        row = base_row()
        row.update(
            {
                "closure_id": closure_id,
                "object": object_name,
                "status": status,
                "reason": reason,
                "allowed_use": allowed_use,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    specs = [
        ("CG2006_0_radial_seed", "clock/radial coframe seed exists", "PASS_NONCLAIM", "useful partial support only"),
        ("CG2006_1_full_EqPhi_map", "full e_obs=E[q(Phi_MTS)] parent map derived", "FAIL_BLOCKED", "transverse tetrad, nondegeneracy, Lorentz gauge, and matter functor remain unsigned"),
        ("CG2006_2_ACT1963_canonical", "ACT1963 owned-coframe branch canonicalized as MTS parent action", "FAIL_BLOCKED", "coframe map is partial and closure-demoted"),
        ("CG2006_3_noGamma_global", "P4/hypermomentum killed globally", "FAIL_BLOCKED", "no-Gamma theorem is valid only inside closure branch"),
        ("CG2006_4_local_GR_Newton", "local GR/Newton derived", "FAIL_BLOCKED", "EH second-order/no-extra-sector and GM transfer remain open"),
        ("CG2006_5_public_claim", "public local-GR claim allowed", "FAIL_BLOCKED", "private nonclaim checkpoint"),
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
            "DEC2006_0_derivation_result",
            "PARTIAL_COFRAME_READOUT_DERIVED_FULL_TETRAD_NOT_DERIVED",
            "The clock-load and radial-routing legs are genuinely supported, but the full nondegenerate tetrad map is not in the current corpus.",
            "do not canonicalize ACT1963 yet",
        ),
        (
            "DEC2006_1_demote_cleanly",
            "ACT1963_DEMOTED_TO_EXPLICIT_CLOSURE_BRANCH",
            "The owned-coframe branch remains valuable because no-Gamma follows inside it, but it is now labelled as closure until E[q(Phi_MTS)] is completed.",
            "retain frame/P4/R11/source residual rows outside the closure",
        ),
        (
            "DEC2006_2_next_best",
            "FULL_TETRAD_COMPLETION_BEFORE_R11_IF_DERIVATION_FIRST",
            "The most direct derivation path is to upgrade the radial seed into a four-leg coframe; if that fails, R11/P4 residual acquisition becomes unavoidable.",
            "target transverse triad, determinant, Lorentz gauge, and matter-functor signatures",
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
            "target_id": "NEXT2006_0_2007",
            "selected": "true",
            "next_doc": "2007-Y5-R2FR-full-tetrad-completion-from-radial-seed-or-residual-interface.md",
            "next_script": "scripts/Y5_R2FR_full_tetrad_completion_from_radial_seed_or_residual_interface_2007.py",
            "objective": "try to complete the radial clock/routing coframe seed into a full nondegenerate Lorentz coframe with transverse ruler legs and universal matter functor; if this fails, start executable residual interfaces for frame/P4/R11 tests",
            "include": "clock-load leg; radial-routing leg; transverse triad; nonzero determinant; local Lorentz gauge; matter functor; no-Gamma theorem; frame/P4 residual fallback",
            "exclude": "declaring e_obs by projection alone; hiding disformal/species markers; claiming local GR; GitHub; formalization-workbench edits",
        }
    )
    return [row]


def branch_copy_rows(paths: list[Path], notes: list[str]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for idx, (path, note) in enumerate(zip(paths, notes, strict=True)):
        row = base_row()
        row.update(
            {
                "copy_id": f"COPY2006_{idx}",
                "copy_path": str(path),
                "exists": str(path.exists()),
                "note": note,
            }
        )
        rows.append(row)
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    map_rows: list[dict[str, object]],
    gaps: list[dict[str, object]],
    closures: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    output_paths: list[Path],
    branch_paths: list[Path],
) -> list[dict[str, object]]:
    full_map_signed = any(
        row.get("map_id") == "EQP2006_8_readout_map_verdict"
        and str(row.get("parent_signed", "")).lower() == "true"
        for row in map_rows
    )
    checks = [
        ("VAL2006_00_sources", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources), "all cited source paths exist and needles are found"),
        ("VAL2006_01_radial_seed_only", any(row["status"] == "RADIAL_CLOCK_SEED_SUPPORTED" for row in map_rows) and any(row["status"] == "RADIAL_ROUTING_SEED_SUPPORTED" for row in map_rows), "clock/radial coframe seed recorded"),
        ("VAL2006_02_full_map_not_promoted", not full_map_signed, "full E[q(Phi_MTS)] map not falsely promoted"),
        ("VAL2006_03_tetrad_gaps_block", all(row["blocks_local_GR_claim"] == "true" for row in gaps), "all tetrad/completion gaps block local-GR claim"),
        ("VAL2006_04_closure_demoted", any(row["status"] == "DOWNGRADE_TO_EXPLICIT_CLOSURE_BRANCH" for row in closures), "ACT1963 is explicitly closure-demoted"),
        ("VAL2006_05_claim_gates_blocked", all(row["passed_for_claim"] == "false" for row in claim_gates), "all claim gates remain blocked"),
        ("VAL2006_06_csv_parse", all(path.exists() and csv_rows_parse(path) for path in output_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2006_07_branch_copies", all(path.exists() for path in branch_paths), "branch-copy CSVs exist"),
        ("VAL2006_08_no_formalization_edits", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains 0 for this run"),
        ("VAL2006_09_output_scope", all(ROOT in [path, *path.parents] for path in [*output_paths, *branch_paths, DOC]), "all outputs are under post-checkpoint-work"),
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
            "check_id": "VAL2006_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "2006 parent E[q(Phi)] coframe readout map or owned-coframe closure demotion",
        }
    )
    rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    map_rows: list[dict[str, object]],
    radial_seed: list[dict[str, object]],
    gaps: list[dict[str, object]],
    closures: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    branch_copies: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 2006 Y5 R2FR: Parent E[q(Phi)] Coframe Readout Map Or Owned-Coframe Closure Demotion

Private checkpoint. This attempts the constructive derivation requested by 2005: make the owned coframe a real MTS readout map rather than a GR-shaped insertion.

## Current Verdict

2006 gets a partial win, not a full proof. The corpus genuinely supports a clock-load coframe leg and a radial-routing coframe leg, so the owned-coframe branch is not arbitrary decoration. But the full parent map `e_obs=E[q(Phi_MTS)]` is not derived: the transverse tetrad legs, nonzero determinant, local Lorentz gauge blindness, universal matter functor, and boundary/no-tail certificate remain unsigned.

Therefore ACT1963 is demoted to an explicit closure branch. Inside that closure branch the no-independent-Gamma theorem remains valid, but outside it the frame/P4/R11/source residual interfaces stay active. No local-GR/Newton/WEP claim is promoted.

## Source Register
{md_table(sources, ["source_id", "source_path", "status", "needles", "note"])}

## Coframe Map Attempt
{md_table(map_rows, ["map_id", "object", "status", "blocker", "parent_signed"])}

## Radial Seed Ledger
{md_table(radial_seed, ["seed_id", "element", "status", "remaining_gap"])}

## Full Tetrad Completion Gaps
{md_table(gaps, ["gap_id", "requirement", "status", "consequence", "blocks_local_GR_claim"])}

## Closure Demotion Ledger
{md_table(closures, ["closure_id", "object", "status", "reason", "allowed_use"])}

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
    map_rows = coframe_map_attempt_rows()
    radial_seed = radial_seed_rows()
    gaps = full_tetrad_gap_rows()
    closures = closure_demotion_rows()
    claim_gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    output_map = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2006_SOURCE_REGISTER.csv",
        "map": OUT / "P8_Y5_PARENT_QLOC_2006_COFRAME_MAP_ATTEMPT.csv",
        "radial": OUT / "P8_Y5_PARENT_QLOC_2006_RADIAL_SEED_LEDGER.csv",
        "gaps": OUT / "P8_Y5_PARENT_QLOC_2006_FULL_TETRAD_COMPLETION_GAP.csv",
        "closures": OUT / "P8_Y5_PARENT_QLOC_2006_CLOSURE_DEMOTION_LEDGER.csv",
        "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2006_CLAIM_GATE.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2006_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_PARENT_QLOC_2006_NEXT_TARGET.csv",
    }
    write_csv(output_map["sources"], sources)
    write_csv(output_map["map"], map_rows)
    write_csv(output_map["radial"], radial_seed)
    write_csv(output_map["gaps"], gaps)
    write_csv(output_map["closures"], closures)
    write_csv(output_map["claim_gates"], claim_gates)
    write_csv(output_map["decisions"], decisions)
    write_csv(output_map["next_target"], next_target)

    branch_paths = [
        SOURCE_WEIGHT_DOCS / "PARENT_EQPHI_COFRAME_READOUT_MAP_2006_NONCLAIM.csv",
        BRANCH_WEP / "P8_Y5_PARENT_QLOC_2006_OWNED_COFRAME_STATUS_NONCLAIM.csv",
        QUEUE / "JR2006_FULL_TETRAD_OR_RESIDUAL_QUEUE.csv",
    ]
    branch_paths[0].parent.mkdir(parents=True, exist_ok=True)
    branch_paths[1].parent.mkdir(parents=True, exist_ok=True)
    branch_paths[2].parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(output_map["map"], branch_paths[0])
    shutil.copyfile(output_map["closures"], branch_paths[1])
    shutil.copyfile(output_map["gaps"], branch_paths[2])

    branch_copies = branch_copy_rows(
        branch_paths,
        [
            "parent E[q(Phi)] coframe readout map nonclaim copy",
            "owned-coframe closure status nonclaim copy",
            "full tetrad or residual queue",
        ],
    )
    branch_copy_path = OUT / "P8_Y5_PARENT_QLOC_2006_BRANCH_COPIES.csv"
    write_csv(branch_copy_path, branch_copies)

    output_paths = [*output_map.values(), branch_copy_path]
    validation = validation_rows(sources, map_rows, gaps, closures, claim_gates, output_paths, branch_paths)
    validation_path = OUT / "P8_Y5_BRR545_2006_VALIDATION.csv"
    write_csv(validation_path, validation)
    output_paths.append(validation_path)

    write_doc(sources, map_rows, radial_seed, gaps, closures, claim_gates, decisions, branch_copies, next_target, validation)
    remove_pycache()

    overall = [row for row in validation if row["check_id"] == "VAL2006_OVERALL"][0]["status"]
    print(f"VAL2006_OVERALL={overall}")
    print(str(DOC))
    for path in output_paths:
        print(str(path))
    for path in branch_paths:
        print(str(path))


if __name__ == "__main__":
    main()
