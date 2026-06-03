#!/usr/bin/env python3
"""Checkpoint 244: M_eff monopole source normalization or radial memory hair."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

CHECKPOINT_244_NAME = "Meff-monopole-source-normalization-or-radial-memory-hair"
RUN_243 = RUNS_ROOT / "20260601-000060-local-representative-selection-action-or-no-shear-gate"

STATUS = "N1_Meff_monopole_conservation_gate_derived_conditionally_radial_memory_hair_parent_source_identity_open_no_promotion"
CLAIM_CEILING = "N1_Meff_conditional_flux_gate_no_Geff_or_PPN_promotion"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_register_rows() -> list[dict[str, Any]]:
    paths = [
        (Path(__file__).resolve(), "checkpoint 244 runner"),
        (WORK_DIR / "230-exterior-vacuum-Einstein-branch-or-Jrel-representative.md", "mass/J_rel separation and beta route"),
        (WORK_DIR / "231-Jrel-cohomology-projector-or-local-EH-limit.md", "absolute H2 mass class and relative exactness"),
        (WORK_DIR / "232-parent-Pmem-projector-or-source-identity-variation.md", "Pi_M/P_mem decomposition"),
        (WORK_DIR / "233-boundary-symplectic-metric-or-local-EH-operator.md", "boundary Hodge/DeWitt metric candidate"),
        (WORK_DIR / "243-local-representative-selection-action-or-no-shear-gate.md", "N2 no-shear and local gate status"),
        (RUN_243 / "status.json", "checkpoint 243 machine status"),
        (RUN_243 / "results" / "coefficient_status_after_243.csv", "coefficient status before N1"),
    ]
    rows: list[dict[str, Any]] = []
    for path, role in paths:
        exists = path.exists()
        rows.append(
            {
                "source": path.name,
                "path": str(path),
                "exists": "yes" if exists else "no",
                "sha256": sha256_file(path) if exists and path.is_file() else "",
                "role": role,
                "issue": "" if exists else "missing",
            }
        )
    return rows


def monopole_flux_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "name": "compact_exterior_shell",
            "condition": "Sigma_ext ~= S^2 x I outside compact source",
            "equation": "H^2(Sigma_ext)=R, H^2(Sigma_ext,partial Sigma_ext)=0",
            "result": "one absolute harmonic flux class exists and must not be erased",
        },
        {
            "step": 2,
            "name": "mass_projector",
            "condition": "Pi_M extracts the absolute S^2 harmonic flux",
            "equation": "M_eff(r) := (1/4pi G) int_{S^2_r} Pi_M J",
            "result": "ordinary enclosed mass is stored as M_eff rather than J_rel",
        },
        {
            "step": 3,
            "name": "vacuum_flux_closure",
            "condition": "no ordinary matter source and no memory leakage in exterior annulus",
            "equation": "d(Pi_M J)=0 on Sigma_ext",
            "result": "M_eff(r2)-M_eff(r1)=int_{S^2x[r1,r2]} d(Pi_M J)=0",
        },
        {
            "step": 4,
            "name": "monopole_solution",
            "condition": "stationary compact exterior with only conserved M_eff",
            "equation": "U(r)=G M_eff/r + const + O(r^-2 multipoles)",
            "result": "source normalization is a conserved monopole, not a radial profile",
        },
        {
            "step": 5,
            "name": "radial_memory_hair_test",
            "condition": "any M_eff(r) with dM_eff/dr != 0",
            "equation": "delta G_eff(r)/G ~ delta M_eff(r)/M_eff",
            "result": "radial memory hair would re-open G_eff and beta gates",
        },
        {
            "step": 6,
            "name": "promotion_limit",
            "condition": "parent must derive Pi_M and d(Pi_M J)=0",
            "equation": "delta S_parent -> mass flux closure and no leakage",
            "result": "N1 is a conditional flux theorem, not a parent-derived pass",
        },
    ]


def radial_hair_exclusion_rows() -> list[dict[str, Any]]:
    return [
        {
            "hair_channel": "absolute_monopole_variation",
            "mathematical_form": "dM_eff/dr != 0",
            "excluded_if": "d(Pi_M J)=0 in exterior annulus",
            "current_status": "conditional_gate",
            "remaining_gap": "parent source identity and Pi_M closure",
        },
        {
            "hair_channel": "l>=2_trace_free_shear",
            "mathematical_form": "K_TF_AB or tangential memory shear",
            "excluded_if": "N2 scalar-only boundary stress holds",
            "current_status": "conditional_gate_from_243",
            "remaining_gap": "parent scalar-boundary variable set",
        },
        {
            "hair_channel": "relative_memory_exact_sector",
            "mathematical_form": "P_mem J_rel not exact or nonzero boundary primitive",
            "excluded_if": "N4 exact relative memory and pure-gauge A_rel",
            "current_status": "open",
            "remaining_gap": "parent P_mem/source identity/A_rel representative",
        },
        {
            "hair_channel": "direct_matter_clock_source",
            "mathematical_form": "Pi_matter J != 0",
            "excluded_if": "N3 strict universal coframe",
            "current_status": "conditional_gate_from_240_242",
            "remaining_gap": "parent R_loc selection",
        },
        {
            "hair_channel": "auxiliary_X_Vdef_radial_hair",
            "mathematical_form": "X/J_rel/V_def propagating exterior mode",
            "excluded_if": "N6 auxiliary no-hair",
            "current_status": "open",
            "remaining_gap": "constraint algebra/no-hair theorem",
        },
        {
            "hair_channel": "projector_stress_leakage",
            "mathematical_form": "nabla_mu T_projector^{mu nu} != cancelled",
            "excluded_if": "N5 projector-stress Bianchi cancellation",
            "current_status": "open",
            "remaining_gap": "variation of Pi_M/P_mem boundary metric",
        },
    ]


def source_normalization_rows() -> list[dict[str, Any]]:
    return [
        {
            "observable_channel": "G_eff_over_G_minus_1",
            "N1_readout": "conditionally_zero_for_radial_profile",
            "equation": "G_eff(r) M_bare -> G M_eff with dM_eff/dr=0",
            "what_is_owned": "radial source profile removed if flux closure holds",
            "what_is_not_owned": "absolute calibration of M_eff from parent matter/boundary action",
        },
        {
            "observable_channel": "beta_minus_1",
            "N1_readout": "helpful_not_sufficient",
            "equation": "conserved M_eff is needed for Schwarzschild exterior",
            "what_is_owned": "one beta blocker is removed conditionally",
            "what_is_not_owned": "metric-only EH operator and no auxiliary hair",
        },
        {
            "observable_channel": "gamma_minus_1/Phi_minus_Psi",
            "N1_readout": "unchanged",
            "equation": "no-shear N2 handles trace-free slip",
            "what_is_owned": "not addressed by N1",
            "what_is_not_owned": "parent scalar-boundary no-shear theorem",
        },
        {
            "observable_channel": "epsilon_matter/alpha_clock",
            "N1_readout": "unchanged",
            "equation": "strict matter coframe handles direct vertices",
            "what_is_owned": "not addressed by N1",
            "what_is_not_owned": "parent R_loc selection",
        },
    ]


def coefficient_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual": "G_eff_over_G_minus_1",
            "status_after_244": "conditionally_monopole_only_if_N1_holds",
            "coefficient_status": "radial c_Geff(r) hair removed if d(Pi_M J)=0",
            "remaining_gap": "parent Pi_M flux closure and absolute source normalization",
        },
        {
            "residual": "beta_minus_1",
            "status_after_244": "still_open_but_N1_piece_conditionally_required",
            "coefficient_status": "conserved M_eff is necessary for Schwarzschild beta=1",
            "remaining_gap": "N4/N5/N6 and metric-only EH exterior",
        },
        {
            "residual": "gamma_minus_1",
            "status_after_244": "unchanged_conditionally_zero_if_N2_holds",
            "coefficient_status": "c_gamma=0 under scalar-boundary/no-shear theorem",
            "remaining_gap": "parent scalar-only boundary variable set",
        },
        {
            "residual": "Phi_minus_Psi",
            "status_after_244": "unchanged_conditionally_zero_if_N2_holds",
            "coefficient_status": "c_slip=0 under tau_TF_AB=0 and compact matching",
            "remaining_gap": "forbid tangential shear/J_rel_A from parent action",
        },
        {
            "residual": "epsilon_matter",
            "status_after_244": "unchanged_conditionally_zero_from_N3",
            "coefficient_status": "c_matter_direct=0 under strict matter coframe",
            "remaining_gap": "parent selection of strict coframe/R_loc",
        },
        {
            "residual": "alpha_clock",
            "status_after_244": "unchanged_direct_vertex_conditionally_zero",
            "coefficient_status": "c_clock_direct=0 under strict matter coframe",
            "remaining_gap": "metric clock redshift/C representative still open",
        },
    ]


def local_gate_priority_rows() -> list[dict[str, Any]]:
    return [
        {
            "rank_after_244": 1,
            "target": "Pi_M_flux_closure_parent_owner",
            "status": "open_parent_theorem",
            "why": "N1 requires d(Pi_M J)=0, not just a named mass projector",
            "next_action": "derive Pi_M from boundary symplectic metric/source identity",
        },
        {
            "rank_after_244": 2,
            "target": "N4_exact_relative_memory",
            "status": "open",
            "why": "after M_eff is separated, relative memory must be exact/pure gauge",
            "next_action": "derive P_mem J_rel=dA_rel and boundary primitive selection",
        },
        {
            "rank_after_244": 3,
            "target": "N5_projector_stress",
            "status": "open",
            "why": "Pi_M/P_mem variations must not hide source leakage",
            "next_action": "compute projector stress or prove Bianchi cancellation",
        },
        {
            "rank_after_244": 4,
            "target": "N6_auxiliary_nohair",
            "status": "open",
            "why": "X/J_rel/V_def cannot carry radial exterior hair",
            "next_action": "derive constraint algebra/no-propagating exterior modes",
        },
        {
            "rank_after_244": 5,
            "target": "local_EH_exterior",
            "status": "open",
            "why": "only after N1/N4/N5/N6 can beta route close",
            "next_action": "derive metric-only exterior operator",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    missing_sources = sum(row["exists"] != "yes" for row in source_register_rows())
    return [
        {
            "gate": "all cited local sources exist",
            "status": "pass" if missing_sources == 0 else "fail",
            "evidence": f"missing={missing_sources}",
            "claim_allowed": "internal checkpoint only",
        },
        {
            "gate": "absolute H2 mass class preserved",
            "status": "pass",
            "evidence": "H^2(S^2xI)=R assigned to Pi_M/M_eff",
            "claim_allowed": "topology bookkeeping only",
        },
        {
            "gate": "M_eff conserved in exterior",
            "status": "conditional_pass",
            "evidence": "d(Pi_M J)=0 -> M_eff(r2)=M_eff(r1)",
            "claim_allowed": "conditional N1 theorem",
        },
        {
            "gate": "radial memory hair excluded by parent action",
            "status": "fail",
            "evidence": "Pi_M flux closure/source identity not parent-derived",
            "claim_allowed": "no",
        },
        {
            "gate": "G_eff/local source normalization public pass claimed",
            "status": "fail",
            "evidence": "absolute M_eff calibration and no-hair chain still open",
            "claim_allowed": "no",
        },
        {
            "gate": "local GR or PPN promoted",
            "status": "fail",
            "evidence": CLAIM_CEILING,
            "claim_allowed": "no",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "meaning": "N1_Meff now has a sharp conditional flux theorem: on the compact exterior shell, the absolute H2 class is the ordinary mass/Gauss flux and must be preserved as M_eff. If Pi_M extracts that class and d(Pi_M J)=0 in the exterior annulus, M_eff is radially conserved and the local source is monopole-only. Radial memory hair is precisely failure of that flux closure or leakage into relative/projector/auxiliary sectors. The parent still has to derive Pi_M and the source identity.",
            "main_gain": "G_eff/source normalization is no longer a vague fitted closure; it is reduced to Pi_M flux closure plus no radial hair",
            "main_failure": "Pi_M flux closure, absolute M_eff calibration, and projector/Bianchi ownership remain parent gaps",
            "next_target": "245-exact-relative-memory-or-projector-stress-bianchi.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_244_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    theorem_rows = monopole_flux_theorem_rows()
    hair_rows = radial_hair_exclusion_rows()
    normalization_rows = source_normalization_rows()
    coefficient_rows = coefficient_status_rows()
    priority_rows = local_gate_priority_rows()
    gates = claim_gate_rows()
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "monopole_flux_theorem_chain.csv": (
            theorem_rows,
            ["step", "name", "condition", "equation", "result"],
        ),
        "radial_memory_hair_exclusion.csv": (
            hair_rows,
            ["hair_channel", "mathematical_form", "excluded_if", "current_status", "remaining_gap"],
        ),
        "source_normalization_readout.csv": (
            normalization_rows,
            ["observable_channel", "N1_readout", "equation", "what_is_owned", "what_is_not_owned"],
        ),
        "coefficient_status_after_244.csv": (
            coefficient_rows,
            ["residual", "status_after_244", "coefficient_status", "remaining_gap"],
        ),
        "local_gate_priority_after_244.csv": (
            priority_rows,
            ["rank_after_244", "target", "status", "why", "next_action"],
        ),
        "claim_gate_results.csv": (
            gates,
            ["gate", "status", "evidence", "claim_allowed"],
        ),
        "decision.csv": (
            decision,
            ["decision", "meaning", "main_gain", "main_failure", "next_target", "promotion_allowed", "claim_ceiling"],
        ),
    }
    for filename, file_data in files.items():
        rows, fieldnames = file_data
        write_csv(results_dir / filename, rows, fieldnames)

    status_payload = {
        "status": decision[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(files.keys()),
        "missing_sources": sum(row["exists"] != "yes" for row in source_rows),
        "N1_Meff_flux_gate_conditionally_locked": True,
        "Pi_M_flux_closure_parent_derived": False,
        "radial_memory_hair_parent_excluded": False,
        "G_eff_public_pass_claimed": False,
        "local_GR_promoted": False,
        "PPN_promoted": False,
        "promotion_allowed": False,
        "next_target": decision[0]["next_target"],
    }
    write_json(run_dir / "status.json", status_payload)
    (run_dir / "DONE.txt").write_text(status_payload["status"] + "\n", encoding="utf-8")
    return status_payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timestamp", default=None, help="Optional run timestamp prefix.")
    args = parser.parse_args()
    print(json.dumps(run(args.timestamp), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
