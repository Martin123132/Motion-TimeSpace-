#!/usr/bin/env python3
"""Checkpoint 237: local EH exterior action contract."""

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

CHECKPOINT_237_NAME = "local-EH-exterior-action-contract"
RUN_235 = RUNS_ROOT / "20260601-000052-projector-stress-variation-or-nohair-constraint-algebra"
RUN_236 = RUNS_ROOT / "20260601-000053-local-EH-operator-or-constraint-algebra-decision"

STATUS = "local_EH_exterior_action_contract_sharp_metric_only_gate_written_parent_reduction_not_derived_no_promotion"
CLAIM_CEILING = "EH_exterior_contract_only_no_parent_metric_reduction_or_PPN_promotion"
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


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_register_rows() -> list[dict[str, Any]]:
    paths = [
        (Path(__file__).resolve(), "checkpoint 237 runner"),
        (WORK_DIR / "177-parent-action-perturbation-local-GR-contract.md", "parent local-GR contract"),
        (WORK_DIR / "179-local-GR-PPN-silence-contract.md", "local PPN fence"),
        (WORK_DIR / "221-Noether-source-identity-or-compact-PPN-closure-map.md", "source identity template"),
        (WORK_DIR / "233-boundary-symplectic-metric-or-local-EH-operator.md", "EH/Lovelock gate"),
        (WORK_DIR / "234-boundary-metric-variation-and-Bianchi-ledger.md", "stress/Bianchi ledger"),
        (WORK_DIR / "235-projector-stress-variation-or-nohair-constraint-algebra.md", "safe branch conditions"),
        (WORK_DIR / "236-local-EH-operator-or-constraint-algebra-decision.md", "route decision"),
        (RUN_235 / "results" / "safe_branch_conditions.csv", "safe branch rows"),
        (RUN_236 / "status.json", "checkpoint 236 machine status"),
        (RUN_236 / "results" / "local_EH_exterior_contract.csv", "checkpoint 236 EH contract rows"),
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


def exterior_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause": "E0",
            "requirement": "define compact exterior region E outside the source/collar",
            "mathematical_form": "E={r>R_shell}; T_matter|E=0",
            "status": "definition",
            "promotion_gap": "",
        },
        {
            "clause": "E1",
            "requirement": "ordinary mass charge survives only as constant monopole",
            "mathematical_form": "Pi_M J -> M_eff; nabla M_eff=0",
            "status": "contract_not_parent_derived",
            "promotion_gap": "source normalization and conservation not derived",
        },
        {
            "clause": "E2",
            "requirement": "trace-free shell/memory stress vanishes in exterior",
            "mathematical_form": "T_TF|E=0; Pi_TF J=0",
            "status": "conditional_from_scalar_boundary",
            "promotion_gap": "scalar boundary variable set not fully parent-derived",
        },
        {
            "clause": "E3",
            "requirement": "direct matter/clock memory vertices absent",
            "mathematical_form": "Pi_matter=0",
            "status": "contract_not_parent_derived",
            "promotion_gap": "matter/clock action not derived",
        },
        {
            "clause": "E4",
            "requirement": "relative memory current exact and boundary-cancelled",
            "mathematical_form": "P_mem J_rel=d_rel A_rel; d_rel(P_mem J_rel)=0",
            "status": "topology_gate_plus_parent_gap",
            "promotion_gap": "P_mem and A_rel not parent-owned",
        },
        {
            "clause": "E5",
            "requirement": "projector stress vanishes or is included and cancels on shell",
            "mathematical_form": "T_projector|E=0 or nabla_mu T_total^{mu nu}=0 with T_projector included",
            "status": "structured_not_derived",
            "promotion_gap": "delta P_mem/delta g not computed from parent action",
        },
        {
            "clause": "E6",
            "requirement": "X/J_rel/V_def carry no exterior propagating hair",
            "mathematical_form": "no independent exterior scalar/vector/tensor profile",
            "status": "not_derived",
            "promotion_gap": "constraint algebra and boundary primitive open",
        },
        {
            "clause": "E7",
            "requirement": "remaining exterior action is metric-only, local, diffeo invariant, and two-derivative",
            "mathematical_form": "S_ext[g]=(16piG_eff)^-1 int_E sqrt(-g)(R-2Lambda_eff)+boundary",
            "status": "EH_target_contract",
            "promotion_gap": "not derived from MTS parent",
        },
        {
            "clause": "E8",
            "requirement": "local compact PPN branch drops Lambda-like term to negligible constant background",
            "mathematical_form": "G_mu_nu=0 to local PPN order around compact source",
            "status": "conditional_consequence",
            "promotion_gap": "depends on E1-E7",
        },
    ]


def derivation_chain_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "statement": "If E1-E6 hold, all non-metric MTS local exterior degrees are absent or reduced to M_eff/boundary terms.",
            "equation": "S_parent|E -> S_metric[g;G_eff,Lambda_eff,M_eff]",
            "status": "conditional",
        },
        {
            "step": 2,
            "statement": "If the remaining metric action is local, diffeomorphism invariant, and second order in four dimensions, the Lovelock-style gate selects EH plus Lambda.",
            "equation": "S_metric=(16piG_eff)^-1 int sqrt(-g)(R-2Lambda_eff)+boundary",
            "status": "conditional_theorem_gate",
        },
        {
            "step": 3,
            "statement": "Metric variation gives the exterior field equation.",
            "equation": "G_mu_nu+Lambda_eff g_mu_nu=0",
            "status": "conditional",
        },
        {
            "step": 4,
            "statement": "For Solar-System local PPN scales, Lambda_eff contributes only a negligible/constant background term.",
            "equation": "G_mu_nu=0 to local PPN order",
            "status": "conditional",
        },
        {
            "step": 5,
            "statement": "Static spherical asymptotically flat vacuum exterior is Schwarzschild with mass M_eff.",
            "equation": "g_00=-1+2U-2U^2+O(U^3)",
            "status": "conditional_consequence",
        },
        {
            "step": 6,
            "statement": "Therefore beta equals one only if the whole exterior contract is parent-derived.",
            "equation": "beta=1 iff E1-E8 are owned",
            "status": "not_promoted",
        },
    ]


def obstruction_rows() -> list[dict[str, Any]]:
    return [
        {
            "obstruction": "metric_only_reduction",
            "why_it_blocks": "EH gate cannot start if non-metric MTS fields have exterior dynamics",
            "current_status": "not derived",
            "next_needed": "prove E1-E6 from parent action",
        },
        {
            "obstruction": "two_derivative_operator",
            "why_it_blocks": "higher curvature or nonlocal terms alter PPN/EH conclusion",
            "current_status": "not derived",
            "next_needed": "derive derivative order of exterior parent action",
        },
        {
            "obstruction": "diffeomorphism_Bianchi_stress",
            "why_it_blocks": "projector/boundary stress can fake conservation if omitted",
            "current_status": "ledger only",
            "next_needed": "compute total stress variation",
        },
        {
            "obstruction": "M_eff_normalization",
            "why_it_blocks": "mass class must be conserved and not memory radial hair",
            "current_status": "contract only",
            "next_needed": "derive source normalization",
        },
        {
            "obstruction": "nohair_constraint",
            "why_it_blocks": "X/J_rel/V_def can spoil Schwarzschild even if q_loc is small",
            "current_status": "rank/bracket tests written, not solved",
            "next_needed": "constraint algebra or independent no-hair theorem",
        },
    ]


def coefficient_status_rows() -> list[dict[str, Any]]:
    previous = read_csv_rows(RUN_235 / "results" / "coefficient_status_after_235.csv")
    previous_by_residual = {row["residual"]: row for row in previous}
    updates = {
        "gamma_minus_1": (
            "EH_contract_requires_no_TF_exterior",
            "gamma safety flows from EH exterior only if T_TF/Pi_TF vanish",
            "derive E2 and metric-only exterior",
        ),
        "Phi_minus_Psi": (
            "EH_contract_requires_no_TF_exterior",
            "slip safety flows from EH exterior only if trace-free memory/shear is absent",
            "derive E2 and local EH action",
        ),
        "G_eff_over_G_minus_1": (
            "EH_contract_absorbs_monopole_as_Geff_Meff",
            "source effects allowed only as G_eff/M_eff normalization",
            "derive E1 and source normalization",
        ),
        "alpha_clock": (
            "EH_contract_requires_universal_metric_coupling",
            "clock safety not supplied by EH unless matter/clock coupling is universal",
            "derive E3 matter/clock action",
        ),
        "epsilon_matter": (
            "EH_contract_requires_universal_metric_coupling",
            "WEP safety not supplied by EH unless composition coupling is absent",
            "derive E3 matter action",
        ),
        "beta_minus_1": (
            "EH_contract_conditional_beta_one",
            "beta=1 follows from Schwarzschild only if E1-E8 are parent-derived",
            "derive metric-only EH exterior action",
        ),
    }
    rows: list[dict[str, Any]] = []
    for residual, prior in previous_by_residual.items():
        status, result, next_needed = updates[residual]
        rows.append(
            {
                "residual": residual,
                "checkpoint_235_status": prior["checkpoint_235_status"],
                "checkpoint_237_status": status,
                "coefficient_after_237": result,
                "parent_derived": "no",
                "promotion_allowed": "false",
                "next_needed": next_needed,
            }
        )
    return rows


def claim_gate_rows(source_rows: list[dict[str, Any]], coefficient_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = sum(row["exists"] != "yes" for row in source_rows)
    beta_contract = any(row["residual"] == "beta_minus_1" and row["checkpoint_237_status"] == "EH_contract_conditional_beta_one" for row in coefficient_rows)
    return [
        {
            "gate": "all cited local sources exist",
            "status": "pass" if missing_sources == 0 else "fail",
            "evidence": f"missing={missing_sources}",
            "claim_allowed": "internal checkpoint only",
        },
        {
            "gate": "EH exterior contract written",
            "status": "pass",
            "evidence": "E0-E8",
            "claim_allowed": "contract only",
        },
        {
            "gate": "Lovelock/EH conditional chain written",
            "status": "pass",
            "evidence": "metric-only diffeo-invariant second-order exterior -> EH+Lambda",
            "claim_allowed": "theorem gate only",
        },
        {
            "gate": "beta condition sharpened",
            "status": "pass" if beta_contract else "fail",
            "evidence": "beta=1 iff EH exterior contract is parent-owned",
            "claim_allowed": "conditional only",
        },
        {
            "gate": "metric-only exterior parent-derived",
            "status": "fail",
            "evidence": "E1-E7 remain parent gaps",
            "claim_allowed": "no local GR claim",
        },
        {
            "gate": "local EH operator derived",
            "status": "fail",
            "evidence": "contract written but not derived from MTS parent",
            "claim_allowed": "no PPN claim",
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
            "meaning": "The exterior GR limit is now sharply stated: MTS earns local EH only if all non-metric exterior sectors reduce to a conserved monopole or vanish/boundary-cancel, leaving a local metric-only diffeomorphism-invariant two-derivative action. Under that contract, EH+Lambda and Schwarzschild beta=1 follow. The parent corpus does not yet derive the contract, so this is not a local-GR or PPN promotion.",
            "main_gain": "the exact conditions for deriving GR outside a compact collar are now explicit",
            "main_failure": "metric-only exterior reduction and no-hair remain unproved",
            "next_target": "238-metric-only-exterior-reduction-or-nohair-theorem.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_237_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    contract = exterior_contract_rows()
    chain = derivation_chain_rows()
    obstructions = obstruction_rows()
    coefficients = coefficient_status_rows()
    gates = claim_gate_rows(source_rows, coefficients)
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "EH_exterior_contract_conditions.csv": (
            contract,
            ["clause", "requirement", "mathematical_form", "status", "promotion_gap"],
        ),
        "EH_derivation_chain.csv": (
            chain,
            ["step", "statement", "equation", "status"],
        ),
        "EH_obstruction_matrix.csv": (
            obstructions,
            ["obstruction", "why_it_blocks", "current_status", "next_needed"],
        ),
        "coefficient_status_after_237.csv": (
            coefficients,
            [
                "residual",
                "checkpoint_235_status",
                "checkpoint_237_status",
                "coefficient_after_237",
                "parent_derived",
                "promotion_allowed",
                "next_needed",
            ],
        ),
        "claim_gate_results.csv": (
            gates,
            ["gate", "status", "evidence", "claim_allowed"],
        ),
        "decision.csv": (
            decision,
            [
                "decision",
                "meaning",
                "main_gain",
                "main_failure",
                "next_target",
                "promotion_allowed",
                "claim_ceiling",
            ],
        ),
    }
    for filename, file_data in files.items():
        rows, fieldnames = file_data
        write_csv(results_dir / filename, rows, fieldnames)

    missing_sources = sum(row["exists"] != "yes" for row in source_rows)
    status_payload = {
        "status": decision[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(files.keys()),
        "missing_sources": missing_sources,
        "EH_exterior_contract_written": True,
        "Lovelock_EH_conditional_chain_written": True,
        "metric_only_exterior_parent_derived": False,
        "local_EH_operator_derived": False,
        "beta_second_order_parent_derived": False,
        "official_bounds_applied_as_pass_fail": False,
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
