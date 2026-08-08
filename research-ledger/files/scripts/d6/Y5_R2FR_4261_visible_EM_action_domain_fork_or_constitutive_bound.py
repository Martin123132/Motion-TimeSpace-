from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4261"
CLAIM_ID = "L-102"
BRANCH = "MTS_R2FR_Y5_VISIBLE_EM_ACTION_DOMAIN_FORK_OR_CONSTITUTIVE_BOUND_4261"
DECISION = "VISIBLE_EM_ACTION_DOMAIN_SIGNED_INSIDE_4210_STANDARD_IMPORT_BRANCH_GLOBAL_MAXWELL_ALPHA_UNDERIVED_BOUND_FORK_RETAINED_NONCLAIM"
MARKER = "PPC4161_VISIBLE_EM_ACTION_DOMAIN_FORK_OR_CONSTITUTIVE_BOUND_4261"
PACKET_MARKER = "PPC4161_PACKET_VISIBLE_EM_ACTION_DOMAIN_FORK_OR_CONSTITUTIVE_BOUND_4261"
NEXT_TARGET = "4262-Y5-R2FR-visible-EM-readout-guard-or-charge-normalization-bound.md"

FORMAL_PATH = FORMAL / "277-PPC4161-visible-EM-action-domain-fork-or-constitutive-bound.md"
DOC_PATH = POST / "4261-Y5-R2FR-visible-EM-action-domain-fork-or-constitutive-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4261_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4261_00_4209_normalization_doc": SourceSpec(
        "SRC4261_00_4209_normalization_doc",
        FORMAL / "225-PPC4161-Maxwell-normalization-charge-current-owner.md",
        "The current safe route for local GR is calibrated visible EM",
        "Maxwell normalization and alpha/charge-current owner guard.",
    ),
    "SRC4261_01_4210_import_doc": SourceSpec(
        "SRC4261_01_4210_import_doc",
        FORMAL / "226-PPC4161-standard-visible-matter-import-contract.md",
        "S_Maxwell-Hodge[A,g_obs; alpha_EM_obs]",
        "Standard visible matter import action-domain contract.",
    ),
    "SRC4261_02_4210_import_csv": SourceSpec(
        "SRC4261_02_4210_import_csv",
        SOURCE_DIR / "P8_Y5_R2FR_4210_VISIBLE_MATTER_IMPORT_CONTRACT.csv",
        "VMI4210_1_action",
        "Machine-readable 4210 standard visible import contract.",
    ),
    "SRC4261_03_4218_visible_doc": SourceSpec(
        "SRC4261_03_4218_visible_doc",
        FORMAL / "234-PPC4161-visible-EM-material-curl-zero-or-residual-bound.md",
        "omega_visible_EM_residual = delta omega[DeltaS_MTS_visible] = 0",
        "Visible EM/material residual zero theorem under standard import.",
    ),
    "SRC4261_04_4218_theorem_csv": SourceSpec(
        "SRC4261_04_4218_theorem_csv",
        SOURCE_DIR / "P8_Y5_R2FR_4218_VISIBLE_EM_THEOREM.csv",
        "VEM4218_7_curl_zero",
        "Machine-readable conditional visible EM curl-zero theorem.",
    ),
    "SRC4261_05_4260_formal": SourceSpec(
        "SRC4261_05_4260_formal",
        FORMAL / "276-PPC4161-Delta-Hodge-EM-closure-or-bound.md",
        "Unsigned parent-action clauses",
        "4260 identified visible action-domain as the real Delta_Hodge_EM gap.",
    ),
    "SRC4261_06_4260_audit_csv": SourceSpec(
        "SRC4261_06_4260_audit_csv",
        SOURCE_DIR / "P8_Y5_R2FR_4260_HODGE_CLOSURE_AUDIT.csv",
        "HC4260_2_visible_action_domain",
        "Machine-readable 4260 Hodge action-domain clause audit.",
    ),
    "SRC4261_07_4260_subvector_csv": SourceSpec(
        "SRC4261_07_4260_subvector_csv",
        SOURCE_DIR / "P8_Y5_R2FR_4260_DELTA_HODGE_SUBVECTOR.csv",
        "Delta_chi_principal",
        "4260 retained Hodge subcomponent vector for the bound branch.",
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
    fieldnames: List[str] = []
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


def append_claim() -> None:
    path = FORMAL / "02-claims-register.csv"
    text = read_text(path)
    if CLAIM_ID in text:
        return
    with path.open(newline="", encoding="utf-8") as handle:
        fieldnames = next(csv.reader(handle))
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": (
            "4261 resolves the 4260 visible-EM action-domain gap by splitting it into branches. Inside the "
            "4210 standard-visible-import/local-GR branch, the Maxwell-Hodge action domain is conditionally "
            "signed because S_vis contains S_Maxwell-Hodge[A,g_obs;alpha_EM_obs] and DeltaS_MTS_visible is set "
            "to zero before variation. Global MTS derivation of Maxwell/QED/alpha remains underived, and any "
            "MTS-visible deformation reopens the Delta_Hodge_EM constitutive bound fork."
        ),
        "current_evidence": (
            "4261 source register, action-domain fork, Hodge subcomponent branch statuses, Delta_Hodge branch "
            "result, constitutive bound template, decision and firewall."
        ),
        "status": "private_visible_EM_action_domain_signed_only_in_4210_standard_import_branch_nonclaim",
        "next_test": "Close readout-regenerated Hodge/alpha response or charge-current normalization residuals.",
        "key_risk": "Confusing a calibrated local-GR visible-matter import branch with a global MTS derivation of electromagnetism or alpha_EM.",
    }
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writerow(row)


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for spec in SOURCE_SPECS.values():
        text = read_text(spec.path)
        rows.append(
            {
                **common(),
                "source_id": spec.source_id,
                "path": str(spec.path),
                "exists": str(spec.path.exists()),
                "required_text": spec.required_text,
                "required_text_found": str(spec.required_text in text),
                "role": spec.role,
                "valid_for_claim": "False",
            }
        )
    return rows


def action_domain_fork_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "ADF4261_0_standard_visible_import_branch",
            "4210_standard_visible_import_local_collar",
            "S_vis_standard contains S_Maxwell-Hodge[A,g_obs;alpha_EM_obs] and DeltaS_MTS_visible=0 before variation.",
            "SIGNED_FOR_PRIVATE_BASELINE_BRANCH",
            "visible EM action-domain clause is closed for the calibrated local-GR baseline branch",
            "does not derive global Maxwell/QED/alpha from MTS",
        ),
        (
            "ADF4261_1_global_parent_EM_derivation",
            "global_MTS_Maxwell_QED_alpha_derivation",
            "derive Maxwell-Hodge structure, charge-current normalization, QED/alpha and material constants from the parent MTS action.",
            "NOT_DERIVED",
            "cannot support a public EM-unification or alpha-prediction claim",
            "requires future parent coefficients and quantum/current ownership, not 4210 import",
        ),
        (
            "ADF4261_2_deformed_visible_sector",
            "MTS_visible_deformation_branch",
            "DeltaS_MTS_visible != 0 or any independent chi_EM, C_XF2, C_JQ, b_alpha, dlambda, marker, readout or Poynting side-channel appears.",
            "RETAINED_BOUND_FORK",
            "4260 constitutive vector and 4259 visible EM residual vector reopen",
            "must be bounded term by term with no cancellation",
        ),
        (
            "ADF4261_3_action_before_readout_guard",
            "variation_before_readout_guard",
            "theta_obs is q-basic/calibrated before variation; readout is not allowed to regenerate *_obs, alpha_EM or hidden EM metric dependence afterwards.",
            "CONDITION_REQUIRED",
            "keeps the standard import from becoming a hidden source-channel",
            "C_Hodge_readout remains the next live gate",
        ),
        (
            "ADF4261_4_boundary_flux_guard",
            "radiative_boundary_flux_guard",
            "live radiative Poynting flux is boundary-routed and not counted as a second local bulk source.",
            "CONDITION_REQUIRED",
            "preserves the 4259 Poynting once-only result",
            "Delta_orientation_flux and radiative boundary rows remain separate guards",
        ),
    ]
    return [
        {
            **common(),
            "fork_id": fork_id,
            "fork": fork,
            "action_domain_clause": clause,
            "status": status,
            "effect": effect,
            "limitation": limitation,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for fork_id, fork, clause, status, effect, limitation in raw
    ]


def subcomponent_action_domain_rows() -> List[Dict[str, str]]:
    source_rows_4260 = csv_rows(SOURCE_DIR / "P8_Y5_R2FR_4260_DELTA_HODGE_SUBVECTOR.csv")
    status_map = {
        "Delta_chi_principal": "ZERO_IN_4210_STANDARD_VISIBLE_IMPORT_BRANCH_ELSE_BOUND",
        "Delta_chi_skewon": "ZERO_IN_4210_STANDARD_VISIBLE_IMPORT_BRANCH_ELSE_BOUND",
        "L*dtheta_EM": "ZERO_IF_THETA_EM_Q_BASIC_AND_NO_ACTIVE_BULK_GRADIENT_ELSE_BOUND",
        "C_Hodge_hidden": "ZERO_IN_4210_STANDARD_VISIBLE_IMPORT_BRANCH_ELSE_BOUND",
        "C_Hodge_readout": "RETAINED_READOUT_GATE_NOT_CLOSED_BY_ACTION_DOMAIN_ALONE",
        "Delta_orientation_flux": "RETAINED_BOUNDARY_ORIENTATION_GATE",
    }
    rows: List[Dict[str, str]] = []
    for row in source_rows_4260:
        coefficient = row.get("coefficient", "")
        rows.append(
            {
                **common(),
                "component_id": row.get("component_id", ""),
                "coefficient": coefficient,
                "definition": row.get("definition", ""),
                "source_4260_status": row.get("status", ""),
                "branch_status": status_map.get(coefficient, "RETAINED_BOUND_GATE"),
                "standard_import_branch_value": "0_by_branch_definition_only" if "ZERO" in status_map.get(coefficient, "") else "not_closed_by_action_domain",
                "general_MTS_branch_value": "MISSING_SOURCE_BACKED_BOUND_OR_ZERO_PROOF",
                "feeds": "Delta_Hodge_EM",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def branch_result_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "BR4261_0_delta_hodge_action_domain_standard_branch",
            "In the 4210 standard-visible-import branch, the visible EM action-domain contribution to Delta_Hodge_EM is conditionally zero.",
            "CONDITIONAL_PRIVATE_BRANCH_ZERO_NOT_GLOBAL_CLAIM",
            "S_vis_standard includes Maxwell-Hodge on g_obs, DeltaS_MTS_visible=0 before variation, theta_obs q-basic/calibrated, no independent chi_EM.",
            "closes the 4260 action-domain clause only for the local-GR baseline branch",
        ),
        (
            "BR4261_1_delta_hodge_general_MTS_branch",
            "For a general MTS visible-sector deformation, Delta_Hodge_EM remains the 4260 no-cancellation bound vector.",
            "RETAINED_CONSTITUTIVE_BOUND_BRANCH",
            "any chi_EM/principal/skewon/axion/hidden/readout/orientation term must be sourced numerically or proved zero",
            "keeps the route honest if MTS predicts visible EM deviations",
        ),
        (
            "BR4261_2_alpha_and_charge_normalization",
            "The branch does not predict alpha_EM, charge/current normalization, mu0, Z_Q, source masses, or G_N.",
            "SCALE_AND_COUPLING_GATES_SEPARATE",
            "4210 imports calibrated visible constants; 4209 leaves b_alpha and g_J^2/lambda_A as separate gates",
            "prevents fake unification claims while allowing GR-style calibrated matter",
        ),
    ]
    return [
        {
            **common(),
            "result_id": result_id,
            "result": result,
            "status": status,
            "conditions": conditions,
            "effect": effect,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for result_id, result, status, conditions, effect in raw
    ]


def constitutive_bound_template_rows(subvector: List[Dict[str, str]]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for subrow in subvector:
        coefficient = subrow["coefficient"]
        rows.append(
            {
                **common(),
                "candidate_id": "DEFORMATION_BRANCH_TEMPLATE_ONLY",
                "coefficient": coefficient,
                "standard_import_branch_value": subrow["standard_import_branch_value"],
                "bound_needed_if_deformed": "MISSING_SOURCE_BACKED_NONNEGATIVE_BOUND_OR_THEOREM_ZERO",
                "units": "dimensionless_Hodge_operator_norm_or_normalized_component",
                "source_path": "MISSING_DEFORMATION_BOUND_SOURCE_PATH",
                "zero_proof_path": "MISSING_ZERO_PROOF_PATH_IF_ZERO",
                "valid_for_claim": "False",
            }
        )
    rows.append(
        {
            **common(),
            "candidate_id": "DEFORMATION_BRANCH_TEMPLATE_ONLY",
            "coefficient": "Delta_Hodge_EM_total",
            "standard_import_branch_value": "0_for_action_domain_part_only_under_4210_branch",
            "bound_needed_if_deformed": "SUM_ABS_OF_SUBCOMPONENTS",
            "units": "dimensionless_Hodge_operator_norm",
            "source_path": str(FORMAL_PATH),
            "zero_proof_path": "ALL_DEFORMATION_SUBCOMPONENTS_ZERO_OR_BOUNDED",
            "valid_for_claim": "False",
        }
    )
    return rows


def decision_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "DEC4261_0_branch_signed",
            "The visible EM action-domain clause is signed inside the 4210 standard-visible-import/local-GR branch.",
            "This is a real closure of the 4260 ambiguity, not a global EM derivation.",
            NEXT_TARGET,
        ),
        (
            "DEC4261_1_bound_fork_retained",
            "If MTS introduces any visible-sector deformation, the constitutive/residual bound fork immediately reopens.",
            "This lets the theory be tested instead of protected by words.",
            "Fill source-backed rows for the reopened coefficient or prove the deformation coefficient zero.",
        ),
        (
            "DEC4261_2_best_next_target",
            "The next live EM gate is readout-regenerated Hodge/alpha response or charge-current normalization.",
            "Action-domain import does not by itself close C_Hodge_readout, b_alpha, C_JQ or source-scale couplings.",
            NEXT_TARGET,
        ),
    ]
    return [
        {
            **common(),
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": "False",
        }
        for decision_id, decision, reason, next_action in raw
    ]


def firewall_rows() -> List[Dict[str, str]]:
    raw = [
        ("FW4261_0_import_overclaim", "using the 4210 calibrated visible import as a global MTS derivation of Maxwell/QED", "GLOBAL_PARENT_EM_DERIVATION_REQUIRED"),
        ("FW4261_1_alpha_overclaim", "claiming alpha_EM or charge normalization from a Maxwell-Hodge action convention", "CHARGE_CURRENT_SCALE_OWNER_REQUIRED"),
        ("FW4261_2_readout_smuggle", "allowing spectroscopy/readout to regenerate hidden Hodge or alpha dependence after variation", "C_HODGE_READOUT_GATE_REQUIRED"),
        ("FW4261_3_deformation_smuggle", "setting DeltaS_MTS_visible to zero after fitting rather than before variation", "ACTION_BRANCH_DECLARATION_REQUIRED"),
        ("FW4261_4_cancellation", "letting constitutive subcomponents cancel in the deformation branch", "SUM_ABS_NO_CANCELLATION_BOUND_REQUIRED"),
        ("FW4261_5_poynting_double_count", "counting Poynting as a second source after Maxwell-Hodge Hilbert stress", "POYNTING_ONCE_ONLY_ROUTE_REQUIRED"),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "forbidden_move": forbidden,
            "required_gate": gate,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, forbidden, gate in raw
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status_id": "STATUS4261_0",
            "summary": (
                "4261 turns the 4260 visible EM action-domain problem into a clean fork: standard calibrated "
                "visible matter closes the action-domain clause for the private local-GR baseline, while any "
                "MTS-visible deformation stays on the constitutive/residual bound route."
            ),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "objective": (
                "Attack C_Hodge_readout, b_alpha, C_JQ and charge-current normalization so the standard visible "
                "import branch cannot hide a readout-scale coupling leak."
            ),
            "avoid": "Do not try to get alpha_EM, G_N or source masses from the action-domain fork.",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""
# 277 - PPC4161 visible EM action-domain fork or constitutive bound

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Private nonclaim

4261 does not prove global Maxwell/QED, `alpha_EM`, charge quantization, `Dq_EM[Hperp]=0`, local GR, PPN, R10, clock safety, or a public EM-unification result.

It closes one narrower thing: the visible EM action-domain clause inside the existing 4210 standard-visible-import branch.

## Fork

The parent-visible local branch is written as:

```text
S_visible_parent
= S_vis_standard[g_obs,A,psi,theta_obs]
  + DeltaS_MTS_visible,

S_vis_standard
= S_matter[psi,g_obs,theta_obs]
 + S_Maxwell-Hodge[A,g_obs; alpha_EM_obs]
 + S_binding[psi,A,g_obs]
 + dB_impr.
```

In the 4210 private local-GR baseline branch:

```text
DeltaS_MTS_visible = 0 before variation,
theta_obs = {{m_A, charges, alpha_EM, hbar, c, material labels}} is q-basic/calibrated,
S_Maxwell-Hodge uses g_obs and *_obs.
```

Therefore the visible EM action-domain contribution to `Delta_Hodge_EM` is conditionally zero in that branch.

## What is not derived

This does not derive:

```text
global Maxwell equations from MTS,
QED,
absolute alpha_EM,
charge-current normalization,
mu0,
Z_Q,
G_N,
source masses.
```

Those remain coupling/scale gates.

## Deformation branch

If MTS adds:

```text
DeltaS_MTS_visible != 0,
chi_EM != chi(g_obs),
C_XF2,
C_JQ,
b_alpha,
dlnlambda,
material marker response,
readout-regenerated Hodge/alpha response,
extra bulk Poynting/source channel,
```

then the 4260 no-cancellation bound route reopens:

```text
||Delta_Hodge_EM||
<= ||Delta_chi_principal||
 + ||Delta_chi_skewon||
 + L||d theta_EM||
 + |C_Hodge_hidden|
 + |C_Hodge_readout|
 + |Delta_orientation_flux|.
```

No cancellation is allowed.

## Consequence

The previous 4260 blocker:

```text
visible EM action domain unsigned
```

is now:

```text
signed only inside the 4210 standard-visible-import branch;
retained as a bound/input problem in any MTS-visible deformation branch.
```

## Next target

`{NEXT_TARGET}` should attack the remaining readout/coupling leak: `C_Hodge_readout`, `b_alpha`, `C_JQ`, and charge-current normalization.
"""


def checkpoint_doc() -> str:
    return f"""
# 4261 - Y5 R2FR visible EM action-domain fork or constitutive bound

Packet marker: `{PACKET_MARKER}`

## Result

4261 signs the visible EM action-domain only in the calibrated 4210 standard-visible-import/local-GR branch.

That means:

```text
standard branch: Maxwell-Hodge action on g_obs is allowed;
general MTS-visible branch: Delta_Hodge_EM bound vector remains live.
```

## Claim status

Private nonclaim. This is a branch-control improvement, not a public derivation of electromagnetism.
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    fork = csv_rows(paths["fork"])
    subvector = csv_rows(paths["subvector"])
    branch_result = csv_rows(paths["branch_result"])
    template = csv_rows(paths["template"])
    rows = [
        ("VAL4261_0_sources_exist", all(row["exists"] == "True" for row in sources), "all source paths exist"),
        ("VAL4261_1_needles_found", all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL4261_2_standard_branch_signed",
            any(row["status"] == "SIGNED_FOR_PRIVATE_BASELINE_BRANCH" for row in fork),
            "standard visible import branch signed",
        ),
        (
            "VAL4261_3_global_derivation_not_claimed",
            any(row["status"] == "NOT_DERIVED" and "global" in row["fork"] for row in fork),
            "global Maxwell/QED/alpha derivation remains not derived",
        ),
        (
            "VAL4261_4_bound_fork_retained",
            any(row["status"] == "RETAINED_BOUND_FORK" for row in fork),
            "deformation branch bound fork retained",
        ),
        (
            "VAL4261_5_subcomponents_nonclaim",
            bool(subvector) and all(row["valid_for_claim"] == "False" for row in subvector),
            "all subcomponent branch statuses remain nonclaim",
        ),
        (
            "VAL4261_6_readout_still_live",
            any(row["coefficient"] == "C_Hodge_readout" and "RETAINED" in row["branch_status"] for row in subvector),
            "readout regenerated Hodge/alpha gate remains live",
        ),
        (
            "VAL4261_7_branch_result_split",
            any(row["status"] == "CONDITIONAL_PRIVATE_BRANCH_ZERO_NOT_GLOBAL_CLAIM" for row in branch_result)
            and any(row["status"] == "RETAINED_CONSTITUTIVE_BOUND_BRANCH" for row in branch_result),
            "Delta_Hodge branch split emitted",
        ),
        (
            "VAL4261_8_template_nonclaim",
            bool(template) and all(row["valid_for_claim"] == "False" for row in template),
            "constitutive bound template stays nonclaim",
        ),
        ("VAL4261_9_claim_row", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claim register row added"),
        ("VAL4261_10_formal_doc", MARKER in read_text(FORMAL_PATH), "formal marker present"),
        ("VAL4261_11_checkpoint_doc", PACKET_MARKER in read_text(DOC_PATH), "checkpoint marker present"),
    ]
    return [
        {
            **common(),
            "check_id": check_id,
            "description": description,
            "passed": str(bool(passed)),
            "evidence": "generated_artifacts",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, passed, description in rows
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    source_path = SOURCE_DIR / "P8_Y5_R2FR_4261_SOURCE_REGISTER.csv"
    fork_path = SOURCE_DIR / "P8_Y5_R2FR_4261_VISIBLE_EM_ACTION_DOMAIN_FORK.csv"
    subvector_path = SOURCE_DIR / "P8_Y5_R2FR_4261_HODGE_SUBCOMPONENT_ACTION_DOMAIN_STATUS.csv"
    branch_result_path = SOURCE_DIR / "P8_Y5_R2FR_4261_DELTA_HODGE_BRANCH_RESULT.csv"
    template_path = SOURCE_DIR / "P8_Y5_R2FR_4261_CONSTITUTIVE_BOUND_INPUT_TEMPLATE.csv"
    decision_path = SOURCE_DIR / "P8_Y5_R2FR_4261_DECISION.csv"
    firewall_path = SOURCE_DIR / "P8_Y5_R2FR_4261_CLAIM_FIREWALL.csv"
    status_path = SOURCE_DIR / "P8_Y5_R2FR_4261_STATUS.csv"
    next_path = SOURCE_DIR / "P8_Y5_R2FR_4261_NEXT_TARGET.csv"

    subvector = subcomponent_action_domain_rows()
    write_csv(source_path, source_rows())
    write_csv(fork_path, action_domain_fork_rows())
    write_csv(subvector_path, subvector)
    write_csv(branch_result_path, branch_result_rows())
    write_csv(template_path, constitutive_bound_template_rows(subvector))
    write_csv(decision_path, decision_rows())
    write_csv(firewall_path, firewall_rows())
    write_csv(status_path, status_rows())
    write_csv(next_path, next_target_rows())
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    append_claim()

    paths = {
        "sources": source_path,
        "fork": fork_path,
        "subvector": subvector_path,
        "branch_result": branch_result_path,
        "template": template_path,
    }
    validation = validation_rows(paths)
    write_csv(VALIDATION_PATH, validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote 9 csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(validation)} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")


if __name__ == "__main__":
    main()
