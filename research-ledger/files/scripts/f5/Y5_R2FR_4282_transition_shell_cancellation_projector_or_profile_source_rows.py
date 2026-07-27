from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4282"
CLAIM_ID = "L-123"
BRANCH = "MTS_R2FR_Y5_TRANSITION_SHELL_CANCELLATION_PROJECTOR_OR_PROFILE_SOURCE_ROWS_4282"
DECISION = "BULK_KHAT_PROJECTOR_CANCELLATION_REJECTED_CONSERVATION_OWNERSHIP_CONTRACT_ONLY_BOUNDARY_TOPOLOGICAL_OR_PROFILE_NEXT_NONCLAIM"
MARKER = "PPC4161_TRANSITION_SHELL_CANCELLATION_PROJECTOR_OR_PROFILE_SOURCE_ROWS_4282"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_SHELL_CANCELLATION_PROJECTOR_OR_PROFILE_SOURCE_ROWS_4282"
NEXT_TARGET = "4283-Y5-R2FR-transition-boundary-topological-superpotential-or-shell-profile-runner.md"

FORMAL_PATH = FORMAL / "298-PPC4161-transition-shell-cancellation-projector-theorem-or-profile-source-rows.md"
DOC_PATH = POST / "4282-Y5-R2FR-transition-shell-cancellation-projector-theorem-or-profile-source-rows.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4282_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
REQUIRED_SUPPRESSION = "4.3819265819966744e-17"
CONTRACT_SUPPRESSION = "4.212667126774669e-17"
AJ_STRONG_WINDOW = "0.1678939074330212*(mu_Xi T_res)/|c_Gamma|"

SOURCES = {
    "SRC4282_00_4281_gate": (
        FORMAL / "297-PPC4161-cGamma-transport-Bgrad-routing-zero-or-profile-source-pack.md",
        "finite-margin zero theorem cannot be extended through the transition shell",
        "4281 says local support zero works only away from transition support.",
    ),
    "SRC4282_01_133_exact_theorem": (
        FORMAL / "133-exact-transition-cancellation-or-projector-theorem.md",
        "exact_transition_cancellation_projector_not_derived_quarantine_only",
        "133 rejects current exact Khat/projector closure and leaves quarantine.",
    ),
    "SRC4282_02_134_conservation": (
        FORMAL / "134-conservation-owned-quarantine-equations.md",
        "q_tr^nu + nabla_mu K_own^{mu nu} = 0.",
        "134 gives algebraically clean conservation ownership but not a parent derivation.",
    ),
    "SRC4282_03_135_projector_origin": (
        FORMAL / "135-quarantine-projector-parent-origin.md",
        "R_loc^nu_alpha q_tr^alpha = 0.",
        "135 identifies the response-kernel theorem form and says it is not derived.",
    ),
    "SRC4282_04_137_source_lift": (
        FORMAL / "137-transition-source-lift-action-block.md",
        "Sigma_metric[q_tr] = 0",
        "137 states the metric-null source-lift/action-block requirement.",
    ),
    "SRC4282_05_138_contract": (
        FORMAL / "138-metric-null-action-block-contract.md",
        "metric_null_action_block_contract_defined_not_derived_route_contract_only",
        "138 writes the C0-C9 metric-null action contract and marks it contract-only.",
    ),
    "SRC4282_06_142_solder": (
        FORMAL / "142-owner-spacetime-solder-map-theorem.md",
        "bulk hybrid route fails; only boundary/topological backup remains",
        "142 rejects bulk owner-solder derivation while leaving boundary/topological backup open.",
    ),
    "SRC4282_07_144_closure": (
        FORMAL / "144-local-transition-closure-contract.md",
        "normalized local transition response <= 4.212667126774669e-17.",
        "144 records the closure-only local transition contract and response threshold.",
    ),
    "SRC4282_08_92_numeric": (
        FORMAL / "92-solar-transition-current-ppn-gate.md",
        "required_q_suppression_factor = 4.3819265819966744e-17",
        "92 supplies the hard transition-shell suppression factor.",
    ),
    "SRC4282_09_projector_redteam": (
        FORMAL / "06-consistency-red-team.md",
        "Solar transition shell -> q_loc branch -> PPN_required.",
        "06 forbids routing Solar transition shells away by sector label.",
    ),
}


def common() -> Dict[str, str]:
    return {
        "checkpoint": CHECKPOINT,
        "branch": BRANCH,
        "generated_utc": STAMP,
        "decision": DECISION,
    }


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def append_unique_block(path: Path, marker: str, heading: str, body: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    block = f"\n\n## {heading}\n\nMarker: `{marker}`\n\n{body}\n"
    write_text(path, text.rstrip() + block)


def append_claim() -> None:
    path = FORMAL / "02-claims-register.csv"
    text = read_text(path)
    if f"{CLAIM_ID}," in text:
        return
    row = (
        f'{CLAIM_ID},local_gr,'
        f'"4282 attacks the remaining transition-shell obstruction directly. It rejects the current bulk Khat cancellation, sector/projector routing, and conservation-only ownership as derived local-GR proofs. The result is a sharper fork: either derive a boundary/topological/superpotential owner that gives zero bulk local metric response, or run a real finite shell-profile comparator against the hard transition suppression threshold.",'
        f'"4282 source register, Khat cancellation audit, projector-kernel audit, conservation-ownership audit, metric-null contract rows, shell profile source rows, decision and firewall.",'
        f'private_transition_bulk_zero_rejected_boundary_topological_or_profile_next_nonclaim,'
        f'"Try the boundary/topological superpotential route, or fill real q_tr/Sigma_metric/R_transport/R_Bgrad shell profiles and test against the transition threshold.",'
        f'"Claiming conservation ownership alone makes the shell invisible, using sector labels as projectors, or using Khat=Gamma*g as cancellation while reintroducing metric stress."\n'
    )
    path.write_text(text.rstrip() + "\n" + row, encoding="utf-8")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, role) in SOURCES.items():
        text = read_text(path)
        rows.append(
            {
                **common(),
                "source_id": source_id,
                "path": str(path),
                "exists": str(path.exists()),
                "required_text": needle,
                "required_text_found": str(needle in text),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def khat_audit_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "KH4282_0_required_identity",
            "nabla_mu K_hat^{mu nu} = nabla^nu Gamma_eff on transition support",
            "Necessary and sufficient pointwise cancellation of q_tr^nu in the local transition channel.",
            "REQUIRED_IDENTITY_DEFINED",
        ),
        (
            "KH4282_1_no_parent_identity",
            "current corpus has no parent equation fixing div K_hat to grad Gamma_eff",
            "133 and 137 both mark exact Khat/source-lift cancellation as not derived.",
            "BULK_KHAT_CANCELLATION_NOT_DERIVED",
        ),
        (
            "KH4282_2_trace_shortcut_rejected",
            "K_hat^{mu nu}=Gamma_eff g^{mu nu} would cancel q_tr but is not the tracefree residual split and reintroduces local metric stress.",
            "This is cancellation by moving the source into the metric tensor, not a safe theorem.",
            "TRACE_REINTRODUCTION_SHORTCUT_REJECTED",
        ),
        (
            "KH4282_3_inverse_divergence_rejected",
            "K_hat = Div^{-1}(grad Gamma_eff) is a formal PDE solve with boundary data, not a parent local identity.",
            "Without action/Noether ownership it is a fitted nonlocal compensator.",
            "INVERSE_DIVERGENCE_COMPENSATOR_REJECTED_AS_THEOREM",
        ),
    ]
    return [
        {
            **common(),
            "audit_id": audit_id,
            "mathematical_clause": clause,
            "meaning": meaning,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for audit_id, clause, meaning, status in raw
    ]


def projector_audit_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "PK4282_0_sector_projector_fail",
            "P_loc=1, P_gal=0, P_cos=0 on Solar/vacuum transition shell",
            "The shell cannot be hidden in galaxy/cosmology routing.",
            "SECTOR_ROUTING_FORBIDDEN",
        ),
        (
            "PK4282_1_response_kernel_target",
            "R_loc q_tr = 0",
            "Correct theorem form: transition current must lie in kernel of the local metric/PPN response operator.",
            "RESPONSE_KERNEL_THEOREM_TARGET",
        ),
        (
            "PK4282_2_kernel_not_derived",
            "R_loc is not derived from a parent action/coarse-graining map and q_tr in Ker(R_loc) is not proved.",
            "135 identifies the target but does not close it.",
            "PROJECTOR_KERNEL_NOT_DERIVED",
        ),
        (
            "PK4282_3_finite_margin_not_shell",
            "support-separated W_loc zero does not apply when W_loc intersects supp(grad Pi_B, grad B_env, I_Bgrad)",
            "4281 exact zero is useful but cannot cross the shell.",
            "FINITE_MARGIN_THEOREM_DOES_NOT_CLOSE_SHELL",
        ),
    ]
    return [
        {
            **common(),
            "audit_id": audit_id,
            "mathematical_clause": clause,
            "meaning": meaning,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for audit_id, clause, meaning, status in raw
    ]


def conservation_audit_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "CO4282_0_owner_identity",
            "q_tr^nu + nabla_mu K_own^{mu nu} = 0",
            "This is algebraically clean current ownership.",
            "CONSERVATION_OWNERSHIP_ALGEBRA_PASSES",
        ),
        (
            "CO4282_1_not_metric_null",
            "nabla_mu K_own^{mu nu}=-q_tr^nu does not imply delta S_owner/delta g_loc=0",
            "A tensor can own the current and still gravitate locally.",
            "CONSERVATION_ALONE_NOT_LOCAL_GR_PROOF",
        ),
        (
            "CO4282_2_action_block_missing",
            "Sigma_metric[q_tr]=0 and owner metric-nullity are not parent-derived",
            "137/138 mark source-lift/action-block orthogonality as a contract, not a theorem.",
            "METRIC_NULL_ACTION_BLOCK_NOT_DERIVED",
        ),
        (
            "CO4282_3_bulk_solder_fail",
            "owner-current primitive needs a spacetime solder map; metric/tetrad solder reintroduces Sigma_metric",
            "142 rejects the bulk hybrid derivation.",
            "BULK_OWNER_SOLDER_ROUTE_FAILS",
        ),
    ]
    return [
        {
            **common(),
            "audit_id": audit_id,
            "mathematical_clause": clause,
            "meaning": meaning,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for audit_id, clause, meaning, status in raw
    ]


def metric_null_contract_rows() -> List[Dict[str, str]]:
    raw = [
        ("MN4282_0", "Sigma_metric[q_tr]=0", "required for local metric-null transition exchange", "UNSIGNED_CONTRACT"),
        ("MN4282_1", "delta S_tr/delta g_loc = 0 while ordinary S_matter still couples to g_loc", "prevents saving transition branch by switching off GR matter response", "UNSIGNED_CONTRACT"),
        ("MN4282_2", "delta S_owner/delta g_loc = 0 or PPN-null", "owner fields must not reintroduce the same shell source", "UNSIGNED_CONTRACT"),
        ("MN4282_3", "q_tr + div K_own = 0", "transition current remains visible and conserved", "ALGEBRAICALLY_AVAILABLE_NOT_PARENT_DERIVED"),
        ("MN4282_4", "boundary/topological/superpotential owner with zero bulk local response", "only still-open theorem class after bulk route failure", "NEXT_THEOREM_CLASS_OPEN"),
    ]
    return [
        {
            **common(),
            "contract_id": contract_id,
            "required_clause": clause,
            "meaning": meaning,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for contract_id, clause, meaning, status in raw
    ]


def profile_source_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "PR4282_0_threshold_92",
            "required_q_suppression_factor",
            REQUIRED_SUPPRESSION,
            "dimensionless",
            str(FORMAL / "92-solar-transition-current-ppn-gate.md"),
            "SOURCE_BACKED_THRESHOLD",
        ),
        (
            "PR4282_1_threshold_144",
            "normalized_local_transition_response_limit",
            CONTRACT_SUPPRESSION,
            "dimensionless",
            str(FORMAL / "144-local-transition-closure-contract.md"),
            "SOURCE_BACKED_THRESHOLD",
        ),
        (
            "PR4282_2_qtr_profile",
            "q_tr_shell_norm",
            "MISSING_REAL_PROFILE",
            "same normalization as transition threshold",
            "MISSING_SOURCE_PATH",
            "PROFILE_REQUIRED",
        ),
        (
            "PR4282_3_sigma_metric",
            "Sigma_metric[q_tr]_shell_norm",
            "MISSING_REAL_PROFILE",
            "local metric response units",
            "MISSING_SOURCE_PATH",
            "PROFILE_REQUIRED",
        ),
        (
            "PR4282_4_AJ_shell",
            "R_transport_to_local+R_Bgrad_to_local",
            f"must satisfy <= {AJ_STRONG_WINDOW}",
            "AJ private units",
            "MISSING_SOURCE_PATH",
            "PROFILE_REQUIRED",
        ),
        (
            "PR4282_5_superpotential",
            "boundary_topological_superpotential_U",
            "MISSING_PARENT_THEOREM_OR_PROFILE",
            "boundary/current units",
            "MISSING_SOURCE_PATH",
            "THEOREM_OR_PROFILE_REQUIRED",
        ),
    ]
    return [
        {
            **common(),
            "profile_id": profile_id,
            "quantity": quantity,
            "value_or_requirement": value,
            "units": units,
            "source_path": source_path,
            "status": status,
            "score_ready": str(status == "SOURCE_BACKED_THRESHOLD"),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for profile_id, quantity, value, units, source_path, status in raw
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision_id": "DEC4282_0",
            "selected_route": "BOUNDARY_TOPOLOGICAL_SUPERPOTENTIAL_OR_PROFILE_RUNNER",
            "meaning": "Bulk Khat cancellation, sector projector routing, and conservation-only ownership are rejected as derived local-GR proofs; only boundary/topological zero-response theorem or finite shell-profile scoring remains.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    raw = [
        ("FW4282_0", "Do not claim q_tr is locally invisible merely because q_tr+div K_own=0."),
        ("FW4282_1", "Do not use P_gal/P_cos sector labels to hide a Solar/vacuum transition shell with P_loc=1."),
        ("FW4282_2", "Do not use K_hat=Gamma_eff*g as cancellation because it reintroduces trace/local metric stress."),
        ("FW4282_3", "Do not treat inverse-divergence Khat solves as parent identities without action/source/boundary ownership."),
        ("FW4282_4", "Do not treat threshold rows as passes until real q_tr/Sigma_metric/AJ profiles are sourced."),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "forbidden_move": forbidden_move,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, forbidden_move in raw
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status_id": "STATUS4282_0",
            "status": "TRANSITION_SHELL_BULK_ZERO_REJECTED_BOUNDARY_TOPOLOGICAL_OR_PROFILE_NEXT",
            "summary": "The local transition obstruction is now narrowed to boundary/topological superpotential theorem or explicit shell-profile scoring.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target_id": "NEXT4282_0",
            "target_file": NEXT_TARGET,
            "task": "Try boundary/topological superpotential ownership for q_tr with zero bulk local metric response; if it fails, build the finite shell-profile runner against the sourced transition thresholds.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""
# 298 Transition-Shell Cancellation/Projector Theorem Or Profile Source Rows

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Result

4282 attacks the transition shell directly.

The dangerous shell current is:

```text
q_tr^nu = nabla^nu Gamma_eff - nabla_mu K_hat^{{mu nu}}.
```

The exact pointwise cancellation route would require:

```text
nabla_mu K_hat^{{mu nu}} = nabla^nu Gamma_eff
```

on the transition support. Current parent material does not sign that identity.

Two fake closures are rejected:

```text
K_hat^{{mu nu}} = Gamma_eff g^{{mu nu}}
```

because that reintroduces trace/local metric stress, and:

```text
K_hat = Div^-1(grad Gamma_eff)
```

because that is a boundary-dependent compensator, not a parent identity.

## Projector Route

For the Solar/vacuum transition shell:

```text
P_loc = 1,
P_gal = 0,
P_cos = 0.
```

So sector routing is forbidden. The only real projector theorem has to be:

```text
R_loc q_tr = 0,
```

where `R_loc` is the local metric/PPN response operator. The current corpus identifies this kernel theorem but does not derive `R_loc` or prove `q_tr in Ker(R_loc)`.

## Conservation Ownership

The clean accounting identity is:

```text
q_tr^nu + nabla_mu K_own^{{mu nu}} = 0.
```

This is necessary and useful. It is not sufficient for local GR, because an owner tensor can conserve the current and still gravitate locally.

The missing metric-null action/source-lift clause is:

```text
Sigma_metric[q_tr] = 0
```

or a PPN-null equivalent. The bulk owner/solder route fails because any metric/tetrad solder reintroduces local metric dependence.

## Remaining Honest Fork

The live fork is now:

```text
boundary/topological/superpotential owner with zero bulk local response
```

or:

```text
finite shell-profile runner.
```

The finite runner must compare real shell profiles against the sourced thresholds:

```text
required_q_suppression_factor = {REQUIRED_SUPPRESSION}
normalized_local_transition_response <= {CONTRACT_SUPPRESSION}.
```

For the cGamma AJ branch it must also test:

```text
|R_transport_to_local| + |R_Bgrad_to_local|
<= {AJ_STRONG_WINDOW}.
```

## Interpretation

This is progress, but not victory:

```text
bulk cancellation: rejected under current corpus;
sector projector: rejected;
conservation-only ownership: contract-only;
boundary/topological theorem: still open;
profile runner: now source-ready but not filled.
```

No public local-GR claim is made.

## Next Target

`{NEXT_TARGET}` should try the boundary/topological superpotential route first. If it fails, build the shell-profile runner.
"""


def checkpoint_doc() -> str:
    return f"""
# 4282 - transition-shell cancellation/projector theorem or profile source rows

Marker: `{MARKER}`

Decision: `{DECISION}`

4282 rejects the current bulk zero shortcuts:

```text
bulk Khat cancellation not parent-derived;
sector projector routing forbidden for Solar/vacuum transition shell;
conservation ownership alone is not metric-null.
```

The remaining honest route is:

```text
boundary/topological superpotential theorem
```

or:

```text
finite shell-profile runner against sourced transition thresholds.
```
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    khat = csv_rows(paths["khat"])
    projectors = csv_rows(paths["projectors"])
    conservation = csv_rows(paths["conservation"])
    contract = csv_rows(paths["contract"])
    profiles = csv_rows(paths["profiles"])
    generated_rows: Iterable[Dict[str, str]] = (
        sources
        + khat
        + projectors
        + conservation
        + contract
        + profiles
        + csv_rows(paths["decision"])
        + csv_rows(paths["firewall"])
        + csv_rows(paths["status"])
        + csv_rows(paths["next_target"])
    )
    validations = [
        ("VAL4282_0_sources_exist", all(row["exists"] == "True" for row in sources), "all source paths exist"),
        ("VAL4282_1_needles_found", all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL4282_2_khat_rejected",
            any(row["status"] == "BULK_KHAT_CANCELLATION_NOT_DERIVED" for row in khat)
            and any(row["status"] == "TRACE_REINTRODUCTION_SHORTCUT_REJECTED" for row in khat),
            "bulk Khat zero shortcuts rejected",
        ),
        (
            "VAL4282_3_projector_kernel",
            any(row["status"] == "RESPONSE_KERNEL_THEOREM_TARGET" for row in projectors)
            and any(row["status"] == "PROJECTOR_KERNEL_NOT_DERIVED" for row in projectors),
            "response-kernel target identified but unsigned",
        ),
        (
            "VAL4282_4_conservation_not_enough",
            any(row["status"] == "CONSERVATION_OWNERSHIP_ALGEBRA_PASSES" for row in conservation)
            and any(row["status"] == "CONSERVATION_ALONE_NOT_LOCAL_GR_PROOF" for row in conservation),
            "conservation ownership separated from metric nullity",
        ),
        (
            "VAL4282_5_boundary_route_open",
            any(row["status"] == "NEXT_THEOREM_CLASS_OPEN" for row in contract),
            "boundary/topological superpotential route remains open",
        ),
        (
            "VAL4282_6_thresholds_sourced",
            {"required_q_suppression_factor", "normalized_local_transition_response_limit"}.issubset(
                {row["quantity"] for row in profiles if row["status"] == "SOURCE_BACKED_THRESHOLD"}
            ),
            "finite profile thresholds are source-backed",
        ),
        (
            "VAL4282_7_profile_rows_blocked",
            any(row["status"] == "PROFILE_REQUIRED" and "MISSING" in row["value_or_requirement"] for row in profiles),
            "real profile rows remain blocked until sourced",
        ),
        ("VAL4282_8_formal_doc", FORMAL_PATH.exists() and MARKER in read_text(FORMAL_PATH), "formal doc written"),
        ("VAL4282_9_checkpoint_doc", DOC_PATH.exists() and DECISION in read_text(DOC_PATH), "checkpoint doc written"),
        ("VAL4282_10_claim_row", f"{CLAIM_ID}," in read_text(FORMAL / "02-claims-register.csv"), "claim register row added"),
        (
            "VAL4282_11_no_claim_rows",
            all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in generated_rows),
            "all generated rows remain nonclaim",
        ),
    ]
    for name, path in paths.items():
        validations.append((f"VAL4282_csv_{name}", bool(csv_rows(path)), f"{path.name} parses"))
    return [
        {
            **common(),
            "check_id": check_id,
            "description": description,
            "passed": str(passed),
            "evidence": "generated_artifacts",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, passed, description in validations
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4282_SOURCE_REGISTER.csv",
        "khat": SOURCE_DIR / "P8_Y5_R2FR_4282_EXACT_KHAT_CANCELLATION_AUDIT.csv",
        "projectors": SOURCE_DIR / "P8_Y5_R2FR_4282_PROJECTOR_KERNEL_AUDIT.csv",
        "conservation": SOURCE_DIR / "P8_Y5_R2FR_4282_CONSERVATION_OWNERSHIP_AUDIT.csv",
        "contract": SOURCE_DIR / "P8_Y5_R2FR_4282_METRIC_NULL_ACTION_CONTRACT.csv",
        "profiles": SOURCE_DIR / "P8_Y5_R2FR_4282_SHELL_PROFILE_SOURCE_ROWS.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4282_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4282_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4282_STATUS.csv",
        "next_target": SOURCE_DIR / "P8_Y5_R2FR_4282_NEXT_TARGET.csv",
    }
    write_csv(paths["sources"], source_rows())
    write_csv(paths["khat"], khat_audit_rows())
    write_csv(paths["projectors"], projector_audit_rows())
    write_csv(paths["conservation"], conservation_audit_rows())
    write_csv(paths["contract"], metric_null_contract_rows())
    write_csv(paths["profiles"], profile_source_rows())
    write_csv(paths["decision"], decision_rows())
    write_csv(paths["firewall"], firewall_rows())
    write_csv(paths["status"], status_rows())
    write_csv(paths["next_target"], next_target_rows())
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    append_claim()
    append_unique_block(
        FORMAL / "07-unification-spine.md",
        MARKER,
        "PPC4161 4282 transition-shell fork narrowed",
        "4282 rejects bulk Khat cancellation, sector-projector routing, and conservation-only ownership as derived transition-shell local-GR proofs. The local shell obstruction is now narrowed to a boundary/topological superpotential theorem or a real finite shell-profile runner against sourced transition thresholds.",
    )
    append_unique_block(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        "4282 packet transition-shell obstruction",
        "Packet update: finite-margin collars remain safe, but the shell itself is not closed by bulk Khat, projectors, or conservation-only ownership. Boundary/topological superpotential or source-backed shell profiles are next.",
    )
    write_csv(VALIDATION_PATH, validation_rows(paths))
    failed = [row for row in csv_rows(VALIDATION_PATH) if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(paths)} csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(csv_rows(VALIDATION_PATH))} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['description']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
