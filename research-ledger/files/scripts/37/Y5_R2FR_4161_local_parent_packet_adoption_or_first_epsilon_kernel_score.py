from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4161-Y5-R2FR-local-parent-packet-adoption-or-first-epsilon-kernel-score.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_LOCAL_PARENT_PACKET_ADOPTION_4161"
CHECKPOINT_ID = "4161"
DECISION = "PRIVATE_LOCAL_PARENT_PACKET_ADOPTED_FOR_FIRST_ORDER_KERNEL_COLLAPSE_PUBLIC_CLAIM_BLOCKED"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4161_00_4160_doc": (
        ROOT / "4160-Y5-R2FR-PiM-fixedness-and-hidden-inner-charge-zero-or-bound.md",
        "Either adopt the selected local parent packet",
        "4160 handoff to local parent packet adoption or first score.",
    ),
    "SRC4161_01_4160_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4160_NEXT_TARGET.csv",
        "one action packet signs PiM fixedness",
        "4160 machine-readable next target.",
    ),
    "SRC4161_02_4160_collapse": (
        SOURCE_DIR / "P8_Y5_R2FR_4160_FIRST_ORDER_COLLAPSE_GATE.csv",
        "FIRST_ORDER_KERNEL_COLLAPSE_CONDITIONAL",
        "4160 conditional first-order kernel collapse.",
    ),
    "SRC4161_03_4056_packet": (
        SOURCE_DIR / "P8_Y5_R2FR_4056_LOCAL_PARENT_ACTION_PACKET.csv",
        "LAP4056_4_GK",
        "Candidate local parent action packet.",
    ),
    "SRC4161_04_4056_gate": (
        SOURCE_DIR / "P8_Y5_R2FR_4056_PACKET_ADOPTION_GATE.csv",
        "ADOPT4056_0_one_action",
        "4056 adoption gate.",
    ),
    "SRC4161_05_4056_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_4056_CONDITIONAL_LOCAL_GR_THEOREM.csv",
        "LGT4056_0_packet",
        "4056 conditional local GR theorem candidate.",
    ),
    "SRC4161_06_4048_contract": (
        SOURCE_DIR / "P8_Y5_R2FR_4048_PARENT_PACKET_CONTRACT.csv",
        "PPC4048_5_source_charge",
        "PPC4048 parent packet contract clauses.",
    ),
    "SRC4161_07_4048_audit": (
        SOURCE_DIR / "P8_Y5_R2FR_4048_ADOPTION_AUDIT.csv",
        "AUD4048_7_gamma_khat_qloc",
        "4048 adoption audit naming weak link and adoptable clauses.",
    ),
    "SRC4161_08_4048_sufficiency": (
        SOURCE_DIR / "P8_Y5_R2FR_4048_LOCAL_GR_SUFFICIENCY_THEOREM.csv",
        "SFT4048_1_Newton",
        "4048 Newton/PPN sufficiency theorem under adopted packet.",
    ),
    "SRC4161_09_4046_reset": (
        SOURCE_DIR / "P8_Y5_R2FR_4046_LOCAL_RESET_MEMORY_SIGNATURE.csv",
        "LRS4046_1_no_incoming",
        "Local reset/no-incoming memory signature.",
    ),
    "SRC4161_10_4055_dgk": (
        SOURCE_DIR / "P8_Y5_R2FR_4055_DGK_ZERO_CERTIFICATE.csv",
        "DGK4055_1_zero_if_adopted",
        "Gamma/Khat Hilbert-response adoption certificate.",
    ),
    "SRC4161_11_4038_poynting": (
        SOURCE_DIR / "P8_Y5_R2FR_4038_POYNTING_NO_FLUX_THEOREM.csv",
        "PNT4038_2_bound_fields_once",
        "Poynting/bound EM once-only branch.",
    ),
    "SRC4161_12_4043_domain": (
        SOURCE_DIR / "P8_Y5_R2FR_4043_SELECTED_BRANCH_ZERO_THEOREM.csv",
        "PZS4043_0_selected_signature",
        "Domain/projector selected branch.",
    ),
    "SRC4161_13_4160_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_4160_EPSILON_KERNEL_BOUND_ROWS.csv",
        "epsilon_kernel_4160",
        "4160 epsilon_kernel fallback rows.",
    ),
    "SRC4161_14_script": (
        SCRIPT_PATH,
        DECISION,
        "This generator records the 4161 private local packet adoption.",
    ),
}


def common() -> dict:
    return {
        "timestamp_utc": TIMESTAMP,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
    }


def write_csv(path: Path, rows: List[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def parse_csv(path: Path) -> List[dict]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def is_under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4161_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4161_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4161_PRIVATE_PACKET_ADOPTION": SOURCE_DIR / "P8_Y5_R2FR_4161_PRIVATE_PACKET_ADOPTION.csv",
        "P8_Y5_R2FR_4161_PACKET_CLAUSE_MAP": SOURCE_DIR / "P8_Y5_R2FR_4161_PACKET_CLAUSE_MAP.csv",
        "P8_Y5_R2FR_4161_FIRST_ORDER_KERNEL_COLLAPSE": SOURCE_DIR / "P8_Y5_R2FR_4161_FIRST_ORDER_KERNEL_COLLAPSE.csv",
        "P8_Y5_R2FR_4161_EPSILON_KERNEL_SCORECARD": SOURCE_DIR / "P8_Y5_R2FR_4161_EPSILON_KERNEL_SCORECARD.csv",
        "P8_Y5_R2FR_4161_CLAIM_FIREWALL": SOURCE_DIR / "P8_Y5_R2FR_4161_CLAIM_FIREWALL.csv",
        "P8_Y5_R2FR_4161_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4161_STATUS.csv",
        "P8_Y5_R2FR_4161_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4161_NEXT_TARGET.csv",
    }


def source_rows() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        exists = path.exists()
        text = read_text(path) if exists and path.is_file() else ""
        rows.append(
            {
                **common(),
                "source_id": source_id,
                "path": str(path),
                "needle": needle,
                "role": role,
                "exists": str(exists),
                "needle_found": str(bool(exists and needle in text)),
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def adoption_rows() -> List[dict]:
    return [
        {
            **common(),
            "adoption_id": "AD4161_0_scope",
            "adoption": "private local parent packet branch",
            "mathematical_statement": "Adopt LAP4056_0..7 / PPC4048_0..10 as one compact isolated <=2PN local parent-action branch for the first-order Newton/kernel proof only.",
            "effect": "the selected local branch becomes the working parent packet for the 4157-4160 kernel ladder",
            "status": "PRIVATE_BRANCH_ADOPTED_FOR_LOCAL_PROOF",
            "public_claim_allowed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "adoption_id": "AD4161_1_action",
            "adoption": "single local action packet",
            "mathematical_statement": "S_loc^{<=2PN}=S_EH[g_obs;kappa_*]+S_matter[psi,g_obs,theta]+S_EM[A,g_obs]+S_binding+S_GK+B_proper+S_top+S_vertical+S_reset",
            "effect": "prevents treating EH, matter, EM, boundary, projector and memory clauses as separate closure patches",
            "status": "ONE_PACKET_ADOPTED_PRIVATE",
            "public_claim_allowed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "adoption_id": "AD4161_2_nonclaim",
            "adoption": "claim firewall",
            "mathematical_statement": "private branch adoption != global MTS corpus adoption != public local-GR proof",
            "effect": "local proof branch may be used internally; public claim remains blocked until corpus mapping and empirical bound/readout gates pass",
            "status": "CLAIM_FIREWALL_ACTIVE",
            "public_claim_allowed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def clause_rows() -> List[dict]:
    return [
        {
            **common(),
            "clause_id": "CL4161_0_EH",
            "packet_clause": "EH observed metric",
            "adopted_condition": "S_EH[g_obs;kappa_*]+S_GHY[g_obs] with fixed local kappa_*",
            "kernel_effect": "delta L_ext=0 and fixed G_ref in the local branch",
            "residual_if_rejected": "epsilon_Pi_operator; epsilon_G_norm",
            "private_adopted": "True",
            "public_claim_allowed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "clause_id": "CL4161_1_matter",
            "packet_clause": "same-source matter",
            "adopted_condition": "S_matter descends through g_obs with fixed representation labels and no hidden source weights",
            "kernel_effect": "delta J_H_total=0 is meaningful and source weights cannot feed a_hom",
            "residual_if_rejected": "epsilon_delta_JH; epsilon_species_A",
            "private_adopted": "True",
            "public_claim_allowed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "clause_id": "CL4161_2_EM",
            "packet_clause": "unique EM owner",
            "adopted_condition": "S_EM[A,g_obs] uses one observed Hodge star and no hidden f(Z)F^2 multiplier",
            "kernel_effect": "minimal bound EM stress is counted once inside J_H_total; no extra Poynting source term",
            "residual_if_rejected": "epsilon_EM_extra_inner",
            "private_adopted": "True",
            "public_claim_allowed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "clause_id": "CL4161_3_source_charge",
            "packet_clause": "same source charge",
            "adopted_condition": "Pi_M^C J_H = J_M_top+dB_zero and M_H_ref=H_tau[S_outer]-H_ref before orbital readout",
            "kernel_effect": "inner Hilbert charge matching and outer reference lock can be used in the same proof branch",
            "residual_if_rejected": "epsilon_Pi_inner; epsilon_surface_mismatch",
            "private_adopted": "True",
            "public_claim_allowed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "clause_id": "CL4161_4_boundary_domain",
            "packet_clause": "boundary/domain support",
            "adopted_condition": "source-blind boundary/reference, q-basic fixed domain/projector, no wall flux, no support refit",
            "kernel_effect": "Phi_boundary=0, Phi_domain=0, delta B_ext=0, delta Sigma_ext=0",
            "residual_if_rejected": "epsilon_boundary_inner; epsilon_domain_inner",
            "private_adopted": "True",
            "public_claim_allowed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "clause_id": "CL4161_5_GK",
            "packet_clause": "Gamma/Khat/q_loc Hilbert response",
            "adopted_condition": "Khat=K_Gamma, Gamma_ren trace/background subtraction fixed, D_GK=0 under adoption",
            "kernel_effect": "q_loc bulk leakage is routed to Ward/Hilbert response instead of an independent inner source",
            "residual_if_rejected": "epsilon_symp_inner; Delta_K; q_loc residual",
            "private_adopted": "True",
            "public_claim_allowed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "clause_id": "CL4161_6_memory",
            "packet_clause": "local reset/no-incoming memory",
            "adopted_condition": "X_mem(t0)=0, J_open+B_lift=0, B_nonlocal_kernel=0 on the compact local collar",
            "kernel_effect": "Phi_incoming=0 for the local Newton/PPN collar without deleting FLRW/open memory sectors",
            "residual_if_rejected": "epsilon_incoming_mass; Delta_cZ",
            "private_adopted": "True",
            "public_claim_allowed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "clause_id": "CL4161_7_readout",
            "packet_clause": "readout firewall",
            "adopted_condition": "PPN, R10, clocks, orbital, EM and cosmology are post-variation readouts only",
            "kernel_effect": "delta readout=0 in Pi_M fixedness; measured GM cannot define the source charge",
            "residual_if_rejected": "epsilon_Pi_readout; GM_laundering_guard_violation",
            "private_adopted": "True",
            "public_claim_allowed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def collapse_rows() -> List[dict]:
    return [
        {
            **common(),
            "collapse_id": "FC4161_0_inputs",
            "statement": "packet signs 4160 inputs",
            "formula": "private packet adoption => delta Pi_M^C=0, Phi_hidden_inner=0, same S/tau/frame/units, outer reference fixed",
            "result": "4160_INPUTS_ZERO_UNDER_PRIVATE_PACKET",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "collapse_id": "FC4161_1_kernel",
            "statement": "first-order kernel collapse",
            "formula": "delta J_H_total=0 and private packet adoption => a_hom=0",
            "result": "FIRST_ORDER_AHOM_ZERO_PRIVATE_BRANCH",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "collapse_id": "FC4161_2_Newton",
            "statement": "conditional Newton source normalization",
            "formula": "a_hom=0 and fixed G_ref => mu_obs=G_ref M_H_ref up to higher-order/PPN/readout residuals",
            "result": "CONDITIONAL_NEWTON_SOURCE_NORMALIZATION_PRIVATE_BRANCH",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "collapse_id": "FC4161_3_limits",
            "statement": "scope limits",
            "formula": "private compact local <=2PN branch does not prove global MTS, cosmology, galaxy, radiative EM, or numerical G prediction",
            "result": "SCOPE_GUARD_ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def scorecard_rows() -> List[dict]:
    return [
        {
            **common(),
            "score_id": "SC4161_0_packet_score",
            "quantity": "epsilon_kernel_private_packet",
            "formula": "epsilon_kernel=0 under private adopted packet for same-source compact local first-order branch",
            "value": "0",
            "score_type": "symbolic_private_branch_zero",
            "score_ready": "False",
            "why_not_public": "private branch adoption is not global corpus adoption and not empirical numeric scoring",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "score_id": "SC4161_1_bound_fallback",
            "quantity": "epsilon_kernel_if_packet_rejected",
            "formula": "epsilon_kernel <= epsilon_Pi_inner + epsilon_hidden_inner + epsilon_surface_mismatch",
            "value": "MISSING_COMPONENT_VALUES",
            "score_type": "bound_formula_ready",
            "score_ready": "False",
            "why_not_public": "component values are not source-backed numeric bounds",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "score_id": "SC4161_2_required_numeric_path",
            "quantity": "first_executable_score_inputs",
            "formula": "epsilon_Pi_operator,boundary,domain,tau,frame,readout + epsilon_boundary,domain,symp,EM,incoming",
            "value": "SOURCE_BACKED_ROWS_REQUIRED",
            "score_type": "input_contract",
            "score_ready": "False",
            "why_not_public": "requires sourced zero certificates or numeric bounds for every non-adopted component",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def firewall_rows() -> List[dict]:
    return [
        {
            **common(),
            "firewall_id": "FW4161_0_private_not_public",
            "rule": "private local branch adoption is not a public claim",
            "meaning": "the packet can be used internally to continue derivations, but no GitHub/journal-facing local-GR claim follows from it alone",
            "status": "ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "firewall_id": "FW4161_1_no_global_overreach",
            "rule": "compact local branch does not erase FLRW/galaxy/memory/radiative sectors",
            "meaning": "the no-incoming/no-flux clauses are local collar clauses only",
            "status": "ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "firewall_id": "FW4161_2_empirical_needed",
            "rule": "public competitiveness needs empirical robustness passes",
            "meaning": "the local derivation branch must eventually meet PPN, clocks, orbital, R10, EM and cosmology tests",
            "status": "ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def status_rows() -> List[dict]:
    return [
        {
            **common(),
            "result": DECISION,
            "private_local_parent_packet_adopted": "True",
            "one_action_packet_adopted_private": "True",
            "first_order_ahom_zero_private_branch": "True",
            "conditional_Newton_source_normalization_private_branch": "True",
            "public_local_gr_claimed": "False",
            "global_MTS_claimed": "False",
            "numeric_epsilon_kernel_score_ready": "False",
            "fallback_bound_rows_retained": "True",
            "formalization_modified_by_4161": "False",
            "next_target": "4162-Y5-R2FR-private-packet-to-formal-spine-integration-or-epsilon-score-inputs.md",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> List[dict]:
    return [
        {
            **common(),
            "next_id": "NEXT4161_0",
            "target_doc": "4162-Y5-R2FR-private-packet-to-formal-spine-integration-or-epsilon-score-inputs.md",
            "target_script": "scripts/Y5_R2FR_4162_private_packet_to_formal_spine_integration_or_epsilon_score_inputs.py",
            "objective": "either integrate the private local packet into the formal unification spine as a clearly scoped local branch, or build source-backed epsilon_kernel input rows for any packet clause the corpus refuses to adopt",
            "success_gate": "formal spine names the private local parent packet, its scope, its nonclaim firewall and its required empirical readouts; otherwise numeric/source-backed epsilon_kernel inputs are emitted",
            "reason": "4161 adopts the private local branch and collapses first-order a_hom internally; the next work is formal integration discipline or executable scoring inputs.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def write_doc(outputs: Dict[str, Path]) -> None:
    text = f"""# 4161 - Local Parent Packet Adoption Or First Epsilon Kernel Score

Timestamp UTC: `{TIMESTAMP}`  
Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`

## Purpose
4160 reduced first-order source normalization to:

`epsilon_kernel <= epsilon_Pi_inner + epsilon_hidden_inner + epsilon_surface_mismatch`.

4161 takes the derivation route first: adopt the selected local parent packet as a **private compact local branch** for the kernel proof.

## Private Packet Adoption
Adopt, for the compact isolated local `<=2PN` branch only:

`S_loc^{{<=2PN}}=S_EH[g_obs;kappa_*]+S_matter[psi,g_obs,theta]+S_EM[A,g_obs]+S_binding+S_GK+B_proper+S_top+S_vertical+S_reset`.

This adoption is private/internal and scoped. It is not a public claim that all MTS sectors are now reduced to GR.

The adopted packet signs:

- fixed EH operator and fixed local `G_ref`;
- same-source matter Hilbert current;
- unique minimal EM owner, with bound EM stress counted once;
- same Hilbert/Hamiltonian source charge before orbital readout;
- source-blind boundary/reference and q-basic fixed domain/projector;
- `Khat=K_Gamma` Hilbert-response route for local `q_loc`;
- local reset/no-incoming memory for the compact collar only;
- readout-after-variation firewall.

## First-Order Kernel Result
Under the private packet:

`delta Pi_M^C=0`,

`Phi_hidden_inner=0`,

same `S/tau/frame/units` are fixed, and the outer reference is fixed.

Combining 4158, 4159 and 4160:

`delta J_H_total=0 and private packet adoption => a_hom=0`.

Therefore the first-order homogeneous Newton mass kernel collapses inside this private local branch:

`epsilon_kernel_private_packet=0`.

## What This Does And Does Not Mean
This is a real step forward: the local first-order source-normalization ladder now has a coherent parent-action branch rather than a pile of disconnected closure clauses.

But the firewall remains:

- this is not a public local-GR claim;
- this is not a global MTS/cosmology/galaxy/radiative-EM claim;
- this does not predict the numerical value of `G`;
- this still needs formal spine integration and empirical readout gates.

## Fallback If Packet Adoption Is Rejected
If any adopted clause is rejected, restore:

`epsilon_kernel <= epsilon_Pi_inner + epsilon_hidden_inner + epsilon_surface_mismatch`.

The first executable score then needs source-backed component rows for:

`epsilon_Pi_operator,boundary,domain,tau,frame,readout`

and

`epsilon_boundary,domain,symp,EM,incoming`.

## Verdict
4161 adopts the private local parent packet for the first-order kernel proof and conditionally collapses `a_hom`. Public/local-GR/global-MTS claims remain blocked by the claim firewall.

## Outputs
- `{outputs["P8_Y5_R2FR_4161_SOURCE_REGISTER"]}`
- `{outputs["P8_Y5_R2FR_4161_PRIVATE_PACKET_ADOPTION"]}`
- `{outputs["P8_Y5_R2FR_4161_PACKET_CLAUSE_MAP"]}`
- `{outputs["P8_Y5_R2FR_4161_FIRST_ORDER_KERNEL_COLLAPSE"]}`
- `{outputs["P8_Y5_R2FR_4161_EPSILON_KERNEL_SCORECARD"]}`
- `{outputs["P8_Y5_R2FR_4161_CLAIM_FIREWALL"]}`
- `{outputs["P8_Y5_R2FR_4161_STATUS"]}`
- `{outputs["P8_Y5_R2FR_4161_NEXT_TARGET"]}`

## Next Target
- `4162-Y5-R2FR-private-packet-to-formal-spine-integration-or-epsilon-score-inputs.md`
- Integrate this private local packet into the formal unification spine as a scoped local branch, or build source-backed score inputs for rejected clauses.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    write_csv(outputs["P8_Y5_R2FR_4161_SOURCE_REGISTER"], source_rows())
    write_csv(outputs["P8_Y5_R2FR_4161_PRIVATE_PACKET_ADOPTION"], adoption_rows())
    write_csv(outputs["P8_Y5_R2FR_4161_PACKET_CLAUSE_MAP"], clause_rows())
    write_csv(outputs["P8_Y5_R2FR_4161_FIRST_ORDER_KERNEL_COLLAPSE"], collapse_rows())
    write_csv(outputs["P8_Y5_R2FR_4161_EPSILON_KERNEL_SCORECARD"], scorecard_rows())
    write_csv(outputs["P8_Y5_R2FR_4161_CLAIM_FIREWALL"], firewall_rows())
    write_csv(outputs["P8_Y5_R2FR_4161_STATUS"], status_rows())
    write_csv(outputs["P8_Y5_R2FR_4161_NEXT_TARGET"], next_rows())
    write_doc(outputs)
    return outputs


def validate(outputs: Dict[str, Path]) -> List[dict]:
    checks: List[dict] = []

    def add(check_id: str, requirement: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                **common(),
                "check_id": check_id,
                "requirement": requirement,
                "passed": str(bool(passed)),
                "detail": detail,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )

    sources = source_rows()
    add(
        "VAL4161_0_sources",
        "all cited source paths exist and contain required needles",
        all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources),
        "; ".join(f"{row['source_id']} exists={row['exists']} needle={row['needle_found']}" for row in sources),
    )

    csv_ok = True
    csv_detail: List[str] = []
    for name, path in outputs.items():
        try:
            rows = parse_csv(path)
            csv_detail.append(f"{name}:{len(rows)}")
            csv_ok = csv_ok and bool(rows)
        except Exception as exc:
            csv_ok = False
            csv_detail.append(f"{name}:ERR {exc!r}")
    add("VAL4161_1_csv_parse", "all generated CSV outputs parse and are nonempty", csv_ok, ", ".join(csv_detail))

    doc_text = read_text(DOC_PATH) if DOC_PATH.exists() else ""
    doc_tokens = [
        DECISION,
        "S_loc^{<=2PN}",
        "delta J_H_total=0 and private packet adoption => a_hom=0",
        "epsilon_kernel_private_packet=0",
        "this is not a public local-GR claim",
        "4162-Y5-R2FR-private-packet-to-formal-spine-integration-or-epsilon-score-inputs.md",
    ]
    add("VAL4161_2_doc_tokens", "document records private packet adoption, kernel collapse, firewall and next target", all(token in doc_text for token in doc_tokens), "tokens checked")

    adoption_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4161_PRIVATE_PACKET_ADOPTION"]))
    adoption_tokens = ["PRIVATE_BRANCH_ADOPTED_FOR_LOCAL_PROOF", "ONE_PACKET_ADOPTED_PRIVATE", "CLAIM_FIREWALL_ACTIVE"]
    add("VAL4161_3_adoption", "adoption rows record private branch, one-packet adoption and firewall", all(token in adoption_text for token in adoption_tokens), "adoption tokens checked")

    clause_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4161_PACKET_CLAUSE_MAP"]))
    clause_tokens = ["EH observed metric", "same-source matter", "unique EM owner", "same source charge", "boundary/domain support", "Gamma/Khat/q_loc Hilbert response", "local reset/no-incoming memory", "readout firewall"]
    add("VAL4161_4_clauses", "clause map includes all adopted local packet sectors", all(token in clause_text for token in clause_tokens), "clause tokens checked")

    collapse_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4161_FIRST_ORDER_KERNEL_COLLAPSE"]))
    collapse_tokens = ["4160_INPUTS_ZERO_UNDER_PRIVATE_PACKET", "FIRST_ORDER_AHOM_ZERO_PRIVATE_BRANCH", "CONDITIONAL_NEWTON_SOURCE_NORMALIZATION_PRIVATE_BRANCH", "SCOPE_GUARD_ACTIVE"]
    add("VAL4161_5_collapse", "collapse rows record private first-order ahom zero and scope guard", all(token in collapse_text for token in collapse_tokens), "collapse tokens checked")

    score_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4161_EPSILON_KERNEL_SCORECARD"]))
    score_tokens = ["epsilon_kernel_private_packet", "symbolic_private_branch_zero", "epsilon_kernel_if_packet_rejected", "MISSING_COMPONENT_VALUES", "SOURCE_BACKED_ROWS_REQUIRED"]
    add("VAL4161_6_scorecard", "scorecard separates symbolic private zero from executable numeric score requirements", all(token in score_text for token in score_tokens), "score tokens checked")

    firewall_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4161_CLAIM_FIREWALL"]))
    firewall_tokens = ["private local branch adoption is not a public claim", "compact local branch does not erase FLRW/galaxy/memory/radiative sectors", "public competitiveness needs empirical robustness passes"]
    add("VAL4161_7_firewall", "firewall rows block public/global overclaim", all(token in firewall_text for token in firewall_tokens), "firewall tokens checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4161_STATUS"])
    status_ok = (
        len(status) == 1
        and status[0].get("result") == DECISION
        and status[0].get("private_local_parent_packet_adopted") == "True"
        and status[0].get("one_action_packet_adopted_private") == "True"
        and status[0].get("first_order_ahom_zero_private_branch") == "True"
        and status[0].get("conditional_Newton_source_normalization_private_branch") == "True"
        and status[0].get("public_local_gr_claimed") == "False"
        and status[0].get("global_MTS_claimed") == "False"
        and status[0].get("numeric_epsilon_kernel_score_ready") == "False"
    )
    add("VAL4161_8_status", "status records private adoption, first-order collapse and no public/global claim", status_ok, str(status))

    next_target = parse_csv(outputs["P8_Y5_R2FR_4161_NEXT_TARGET"])
    next_ok = len(next_target) == 1 and next_target[0].get("target_doc") == "4162-Y5-R2FR-private-packet-to-formal-spine-integration-or-epsilon-score-inputs.md"
    add("VAL4161_9_next", "next target is formal-spine integration or epsilon score inputs", next_ok, str(next_target))

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    no_public = all(row.get("public_claim_allowed", "False") in ("False", "") for row in all_rows)
    no_score = all(row.get("score_ready", "False") in ("False", "") for row in all_rows)
    add("VAL4161_10_no_claim", "all outputs remain nonclaim, no public claim and no executable score-ready row", no_claim and no_public and no_score, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(
            ("4161-Y5-R2FR" in item.name or "R2FR_4161" in item.name or "P8_Y5_R2FR_4161" in item.name)
            for item in FORMALIZATION.rglob("*")
        )
    add("VAL4161_11_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4161_12_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4161_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    print(f"wrote: {DOC_PATH}")
    for path in outputs.values():
        print(f"wrote: {path}")
    print(f"validation: {validation_path}")
    if failed:
        print("failed checks:")
        for row in failed:
            print(f"- {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("all validation checks passed")


if __name__ == "__main__":
    main()
