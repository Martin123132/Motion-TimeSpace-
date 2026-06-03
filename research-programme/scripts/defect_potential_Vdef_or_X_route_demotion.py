#!/usr/bin/env python3
"""Checkpoint 224: defect potential V_def attempt or X-route demotion."""

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

CHECKPOINT_224_NAME = "defect-potential-Vdef-or-X-route-demotion"
CHECKPOINT_223_RUN = RUNS_ROOT / "20260601-000040-X-constraint-algebra-and-Khat-Gamma-constitutive-owner"

STATUS = "Vdef_composite_candidate_partial_trace_flow_owned_X_route_demoted_to_closure_support"
CLAIM_CEILING = "Vdef_contract_only_X_source_identity_support_no_local_GR_promotion"
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
        (Path(__file__).resolve(), "checkpoint 224 V_def/X-route script"),
        (WORK_DIR / "138-coherent-volume-pressure-kernel-theorem.md", "coherent volume trace pressure theorem"),
        (WORK_DIR / "139-density-law-hazard-theorem-attempt.md", "hazard activation shape attempt"),
        (WORK_DIR / "140-boundary-charge-amplitude-decision-gate.md", "B_mem amplitude demotion gate"),
        (WORK_DIR / "141-consolidated-locked-memory-branch-contract.md", "locked memory branch claim ceiling"),
        (WORK_DIR / "210-GK-alphaK-parent-invariant-or-fixed-closure.md", "G_K composite invariant candidate"),
        (WORK_DIR / "211-GK-parent-metric-Ward-identity-attempt.md", "G_K parent metric partial owner status"),
        (WORK_DIR / "223-X-constraint-algebra-and-Khat-Gamma-constitutive-owner.md", "X/P constitutive owner checkpoint"),
        (CHECKPOINT_223_RUN / "status.json", "checkpoint 223 machine status"),
        (CHECKPOINT_223_RUN / "results" / "Khat_Gamma_constitutive_owner_tests.csv", "checkpoint 223 owner tests"),
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


def Vdef_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "C0_free_new_Vdef",
            "schematic": "declare V_def(Y,Z) so that partial V_def/partial Z=P",
            "owned_blocks": "none",
            "status": "rejected",
            "reason": "a newly named potential chosen to produce P is just the free-P problem in potential language",
        },
        {
            "candidate": "C1_trace_volume_memory",
            "schematic": "V_trace(N_D)=rho_Lambda+B_mem[1-exp(-I_M(N_D))]",
            "owned_blocks": "trace/volume pressure kernel and hazard shape conditional",
            "status": "partial_pass",
            "reason": "checkpoint 138 derives pressure from volume variation and checkpoint 139 derives survival shape conditionally; B_mem and domain owner remain closure/open",
        },
        {
            "candidate": "C2_flow_GK_quadratic_norm",
            "schematic": "V_flow=1/2 ||Xi_flow[Z_TF]||^2_DeWitt",
            "owned_blocks": "expansion dispersion/shear/vorticity partial",
            "status": "partial_pass",
            "reason": "ADM/DeWitt/Raychaudhuri gives partial kinematic ownership but not the full composite metric",
        },
        {
            "candidate": "C3_full_GK_composite_norm",
            "schematic": "V_GK=1/2 Xi_A M_AB Xi_B",
            "owned_blocks": "flow plus Weyl plus Q plus J_rel candidate",
            "status": "contract_only",
            "reason": "M_AB, cross terms, Weyl normalization, Q owner, and J_rel representative are not derived",
        },
        {
            "candidate": "C4_relative_boundary_Hodge_potential",
            "schematic": "V_rel=1/2 ||J_rel||^2_Hodge plus boundary primitive terms",
            "owned_blocks": "relative-current formal object",
            "status": "open",
            "reason": "closure can be imposed but local representative and boundary primitive selection are still missing",
        },
        {
            "candidate": "C5_combined_minimal_block_diagonal_Vdef",
            "schematic": "V_def=V_trace+V_flow+V_GK_sidecar+V_rel with no cross terms",
            "owned_blocks": "trace partial; flow partial; boundary/composite closure",
            "status": "best_contract_not_derivation",
            "reason": "it anchors P in existing blocks, but cross-term absence and full parent metric remain fixed closure",
        },
    ]


def response_deformation_rows() -> list[dict[str, Any]]:
    return [
        {
            "deformation": "Z_trace",
            "definition": "Z = (1/4) g^{mu nu} Z_mu_nu mapped to coherent volume N_D=(1/3)ln(V_D0/V_D)",
            "owned_status": "partial_pass",
            "maps_to": "Gamma_eff trace response",
            "gap": "domain D and local N_D=0 theorem not derived",
        },
        {
            "deformation": "Z_flow_TF",
            "definition": "trace-free flow deformation mapped to shear/expansion-dispersion/vorticity blocks",
            "owned_status": "partial_pass",
            "maps_to": "Khat flow block",
            "gap": "only kinematic block partially parent-owned",
        },
        {
            "deformation": "Z_Weyl",
            "definition": "curvature defect mapped to Weyl scalar norm W_D=(C_abcd C^abcd)^1/4",
            "owned_status": "natural_norm_not_parent_weighted",
            "maps_to": "Khat curvature block",
            "gap": "coefficient and stress variation not derived",
        },
        {
            "deformation": "Z_Q",
            "definition": "load anisotropy / determinant response block",
            "owned_status": "open",
            "maps_to": "Khat/load sidecar and trace exposure",
            "gap": "Q action/source law incomplete",
        },
        {
            "deformation": "Z_Jrel",
            "definition": "relative boundary current/exact primitive response",
            "owned_status": "open",
            "maps_to": "boundary contribution to P and J_eff",
            "gap": "local representative, exactness, and boundary primitive not derived",
        },
        {
            "deformation": "cross_terms",
            "definition": "mixed response between trace, flow, Weyl, Q, and J_rel blocks",
            "owned_status": "closure_zero",
            "maps_to": "off-diagonal M_AB",
            "gap": "zero cross terms are a minimal closure policy, not a Ward theorem",
        },
    ]


def derivation_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "statement": "Decompose response deformation Z_mu_nu into trace and trace-free/coherence-breaking blocks.",
            "result": "formal_decomposition",
            "gap": "parent definition of Z_mu_nu missing",
        },
        {
            "step": 2,
            "statement": "Use coherent volume variation for the trace potential V_trace(N_D).",
            "result": "Gamma_eff_trace_part_conditionally_owned",
            "gap": "B_mem, domain owner, and local N_D theorem missing",
        },
        {
            "step": 3,
            "statement": "Use ADM/DeWitt-style flow norm for the trace-free kinematic block.",
            "result": "Khat_flow_part_partially_owned",
            "gap": "not a full composite parent norm",
        },
        {
            "step": 4,
            "statement": "Attach Weyl, Q, and J_rel pieces through the checkpoint-210/211 G_K norm and relative boundary Hodge candidate.",
            "result": "candidate_composite_contract",
            "gap": "M_AB, cross terms, Q owner, and J_rel representative not derived",
        },
        {
            "step": 5,
            "statement": "Take P^{mu nu}=partial V_def/partial Z_mu_nu and split Gamma_eff=-trace(P)/4, Khat=P+Gamma_eff g.",
            "result": "P_contract_recovered",
            "gap": "only a contract unless V_def and Z_mu_nu are parent-derived",
        },
        {
            "step": 6,
            "statement": "Feed P[Y] into the X multiplier route.",
            "result": "X_route_demoted_to_closure_support",
            "gap": "not enough for local-GR promotion",
        },
    ]


def promotion_blocker_rows() -> list[dict[str, Any]]:
    return [
        {
            "blocker": "B1_parent_Z_definition",
            "required": "derive Z_mu_nu as a real response/deformation variable from MTS parent fields",
            "current_status": "missing",
            "effect": "without Z, V_def derivative is formal",
        },
        {
            "blocker": "B2_full_MAB",
            "required": "derive field-space metric M_AB and cross terms",
            "current_status": "missing",
            "effect": "G_K composite norm remains fixed closure",
        },
        {
            "blocker": "B3_boundary_primitive",
            "required": "derive compact-shell exact/pure-gauge A_rel and boundary stress",
            "current_status": "missing",
            "effect": "local J_rel leakage remains closure-bounded",
        },
        {
            "blocker": "B4_amplitude",
            "required": "derive B_mem=2/27 from normalized boundary charge",
            "current_status": "empirical_closure",
            "effect": "trace potential cannot be a full prediction",
        },
        {
            "blocker": "B5_constraint_algebra",
            "required": "close {C_X,C_X} on parent constraints",
            "current_status": "not_derived",
            "effect": "zero local X degrees remain conditional",
        },
        {
            "blocker": "B6_stress_variation",
            "required": "derive T_Vdef, T_X, T_boundary and prove Bianchi accounting",
            "current_status": "contract_only",
            "effect": "no local GR or field-theory promotion",
        },
    ]


def demotion_policy_rows() -> list[dict[str, Any]]:
    return [
        {
            "object": "X_source_identity_route",
            "new_status": "closure_support_theorem_target",
            "allowed_use": "organize q_loc source identity and leakage bounds",
            "forbidden_use": "claim derived local GR or PPN silence",
        },
        {
            "object": "V_def",
            "new_status": "composite_candidate_contract",
            "allowed_use": "track which blocks could own Gamma/Khat",
            "forbidden_use": "treat as parent action until Z_mu_nu and M_AB are derived",
        },
        {
            "object": "trace_volume_block",
            "new_status": "partial_conditional_owner",
            "allowed_use": "derive pressure kernel if N_D is real coherent volume",
            "forbidden_use": "derive B_mem or domain selector",
        },
        {
            "object": "flow_GK_block",
            "new_status": "partial_geometric_owner",
            "allowed_use": "motivate trace-free Khat flow response",
            "forbidden_use": "claim full composite norm or cross terms derived",
        },
        {
            "object": "relative_boundary_block",
            "new_status": "open_closure_bound",
            "allowed_use": "carry explicit local leakage budget",
            "forbidden_use": "erase PPN q_loc without exact representative",
        },
    ]


def claim_gate_rows(
    source_rows: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = sum(row["exists"] != "yes" for row in source_rows)
    partial_passes = sum(row["status"] == "partial_pass" for row in candidates)
    derived_failures = sum(row["current_status"] in {"missing", "not_derived", "empirical_closure", "contract_only"} for row in blockers)
    best_contracts = sum(row["status"] == "best_contract_not_derivation" for row in candidates)
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing_sources == 0 else "fail",
            "evidence": f"missing={missing_sources}",
            "claim_allowed": "internal checkpoint only",
        },
        {
            "gate": "free V_def rejected",
            "status": "pass",
            "evidence": "new potential by declaration is rejected",
            "claim_allowed": "guardrail",
        },
        {
            "gate": "trace block partially owned",
            "status": "conditional_pass" if partial_passes >= 1 else "fail",
            "evidence": "coherent-volume pressure and hazard shape conditional routes",
            "claim_allowed": "partial trace contract",
        },
        {
            "gate": "flow block partially owned",
            "status": "conditional_pass",
            "evidence": "ADM/DeWitt flow norm from checkpoint 211",
            "claim_allowed": "partial Khat contract",
        },
        {
            "gate": "combined V_def contract written",
            "status": "conditional_pass" if best_contracts == 1 else "fail",
            "evidence": f"best_contracts={best_contracts}",
            "claim_allowed": "contract only",
        },
        {
            "gate": "V_def parent-derived",
            "status": "fail",
            "evidence": f"derived_failures={derived_failures}; Z_mu_nu/M_AB/boundary/amplitude missing",
            "claim_allowed": "no theorem",
        },
        {
            "gate": "P=partial V_def/partial Z promoted",
            "status": "fail",
            "evidence": "P recovered only as a contract because V_def and Z are not parent-derived",
            "claim_allowed": "no local-GR promotion",
        },
        {
            "gate": "X route promoted",
            "status": "fail",
            "evidence": "X route demoted to closure support/theorem target",
            "claim_allowed": "support only",
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
            "meaning": "A composite V_def can be written using existing MTS blocks: coherent-volume trace pressure, additive-hazard trace density shape, partial ADM/DeWitt flow norm, and closure-level G_K/J_rel boundary pieces. This anchors P better than a free tensor, but it is not a parent derivation because Z_mu_nu, M_AB, cross terms, boundary primitive, amplitude, and stress variation remain unowned. Therefore the X-source-identity route is demoted to closure support/theorem target rather than promoted to local GR.",
            "main_gain": "V_def is decomposed into owned, partial, open, and closure blocks instead of being a magic potential",
            "main_failure": "no parent Z_mu_nu or full defect metric M_AB, so P is not derived",
            "route_status": "X_source_identity_closure_support",
            "next_target": "225-local-GR-route-ledger-and-empirical-pivot-gate.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_224_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    candidates = Vdef_candidate_rows()
    deformation_rows = response_deformation_rows()
    derivation_rows = derivation_attempt_rows()
    blockers = promotion_blocker_rows()
    demotion_rows = demotion_policy_rows()
    gates = claim_gate_rows(source_rows, candidates, blockers)
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "Vdef_candidate_ledger.csv": (
            candidates,
            ["candidate", "schematic", "owned_blocks", "status", "reason"],
        ),
        "response_deformation_Z_ledger.csv": (
            deformation_rows,
            ["deformation", "definition", "owned_status", "maps_to", "gap"],
        ),
        "derivation_attempt_chain.csv": (
            derivation_rows,
            ["step", "statement", "result", "gap"],
        ),
        "promotion_blockers.csv": (
            blockers,
            ["blocker", "required", "current_status", "effect"],
        ),
        "X_route_demotion_policy.csv": (
            demotion_rows,
            ["object", "new_status", "allowed_use", "forbidden_use"],
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
                "route_status",
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
    open_or_missing_blockers = sum(
        row["current_status"] in {"missing", "not_derived", "empirical_closure", "contract_only"}
        for row in blockers
    )
    status_payload = {
        "status": decision[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(files.keys()),
        "missing_sources": missing_sources,
        "free_Vdef_rejected": True,
        "trace_volume_block_partial": True,
        "flow_block_partial": True,
        "combined_Vdef_contract_written": True,
        "Vdef_parent_derived": False,
        "P_from_Vdef_promoted": False,
        "X_route_status": "closure_support_theorem_target",
        "open_or_missing_blockers": open_or_missing_blockers,
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
    payload = run(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
