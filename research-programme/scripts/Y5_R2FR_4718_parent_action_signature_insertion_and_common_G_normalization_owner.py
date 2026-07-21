from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4718"
CLAIM_ID = "L-560"
MARKER = "PPC4161_PARENT_ACTION_SIGNATURE_AND_COMMON_G_NORMALIZATION_OWNER_4718"
PACKET_MARKER = "PPC4161_PACKET_PARENT_ACTION_SIGNATURE_AND_COMMON_G_NORMALIZATION_OWNER_4718"
DECISION = "PARENT_ACTION_SIGNATURE_CANDIDATE_INSERTED_G_OWNER_LAW_DERIVED_PARENT_COEFFICIENTS_UNSIGNED_NONCLAIM"
NEXT_TARGET = "4719-Y5-R2FR-local-linearized-GR-limit-and-Poisson-equation-residual-bound.md"

DOC_PATH = POST / "4718-Y5-R2FR-parent-action-signature-insertion-and-common-G-normalization-owner.md"
FORMAL_PATH = FORMAL / "734-PPC4161-parent-action-signature-insertion-and-common-G-normalization-owner.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4718_SOURCE_REGISTER.csv"
ACTION_SIGNATURE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4718_PARENT_ACTION_SIGNATURE_ROWS.csv"
G_OWNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4718_COMMON_G_NORMALIZATION_OWNER_ROWS.csv"
LOCAL_RESIDUAL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4718_LOCAL_GR_NEWTON_RESIDUAL_ROWS.csv"
GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4718_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4718_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4718_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4718_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4718_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4718_VALIDATION.csv"


SOURCE_SPECS = [
    {
        "source_id": "SRC4718_0",
        "path": "P8_Y5_R2FR_4717_PARENT_SIGNATURE_CONTRACT.csv",
        "needle": "PSC4717_4_common_G_normalization_route",
        "role": "4717 contract row that separated common G normalization from relative source prefactors.",
    },
    {
        "source_id": "SRC4718_1",
        "path": "P8_Y5_R2FR_4717_NO_PREACTION_PREFACTOR_SIGNATURE_THEOREM.csv",
        "needle": "NPP4717_0_sufficient_signature",
        "role": "Sufficient no-preaction-source-prefactor theorem.",
    },
    {
        "source_id": "SRC4718_2",
        "path": "P8_Y5_R2FR_4717_DELTAW_KERNEL_FIRST_ROWS.csv",
        "needle": "DWK4717_5_Newton_constant_owner",
        "role": "Newton/G owner kernel row staged by 4717.",
    },
    {
        "source_id": "SRC4718_3",
        "path": "P8_Y5_R2FR_4716_CURRENT_RESCALE_NO_MORPHISM_THEOREM.csv",
        "needle": "NCM4716_0_postvariation_rescale",
        "role": "Variation-before-readout route for post-variation current/source rescale demotion.",
    },
    {
        "source_id": "SRC4718_4",
        "path": "P8_Y5_R2FR_4715_SAME_CURRENT_CHARGE_LATTICE_THEOREM.csv",
        "needle": "SCC4715_2_no_current_rescale_subtheorem",
        "role": "Same-current theorem that fixes source current identity after variation.",
    },
    {
        "source_id": "SRC4718_5",
        "path": "P8_Y5_PARENT_QLOC_1892_ORDINARY_MATTER_ACTION_SIGNATURE_ATTEMPT.csv",
        "needle": "OMAS1892_0_target_signature",
        "role": "Earlier ordinary-matter action signature target.",
    },
    {
        "source_id": "SRC4718_6",
        "path": "P8_Y5_PARENT_QLOC_1892_SIGNATURE_CLAUSE_MATRIX.csv",
        "needle": "OMC1892_4_source_functor_label_forgetting",
        "role": "Source-functor label-forgetting clause.",
    },
    {
        "source_id": "SRC4718_7",
        "path": "P8_EM_common_action_density_line_universal_source_scale.csv",
        "needle": "UCSR3510_0_zeta_w_common",
        "role": "Common action-density line / universal source scale split.",
    },
    {
        "source_id": "SRC4718_8",
        "path": "P8_EM_quotient_action_derives_q_normal_form_status.csv",
        "needle": "STAT3520_3_prefactor",
        "role": "Prefactor obstruction surviving quotient/basicness alone.",
    },
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"No rows supplied for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def append_once(path: Path, marker: str, block: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = read_text(path) if path.exists() else ""
    if marker in existing:
        return
    separator = "\n\n" if existing and not existing.endswith("\n\n") else ""
    path.write_text(existing + separator + block.rstrip() + "\n", encoding="utf-8", newline="\n")


def source_register(ts: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = SOURCE_DIR / spec["path"]
        text = read_text(path) if path.exists() else ""
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": spec["source_id"],
                "source_path": str(path),
                "exists": path.exists(),
                "needle": spec["needle"],
                "needle_found": spec["needle"] in text,
                "role": spec["role"],
                "valid_for_claim": False,
                "timestamp_utc": ts,
            }
        )
    return rows


def action_signature_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "PAS4718_0_candidate_parent_action",
            "statement": "Use the parent signature S_parent=S_geo[Phi]+S_MTS_aux[Phi]+lambda_D S_matter[Psi;e_obs(q(Phi)),omega(e_obs),A_Q(q(Phi)),theta_rep]+S_boundary.",
            "role": "This inserts the 4717 no-prefactor signature into a concrete action form while keeping one common matter density-line scale.",
            "derived_consequence": "No sum_A w_A S_A, no kappa_A A_Q J_A, no q_A(X) A_Q J_A, and no source-label scalar target appear before variation.",
            "parent_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "PAS4718_1_variation_before_readout",
            "statement": "Vary the action before source/test readout: delta S_parent/delta g_eff^{mu nu}=0 and delta S_parent/delta A_Q=0 define T_Q and J_Q once.",
            "role": "Post-variation calibration maps can change units/readout labels, but cannot become parent source couplings.",
            "derived_consequence": "The same-current theorem and 4716 post-variation rescale demotion attach to the action signature.",
            "parent_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "PAS4718_2_metric_sector_EH_target",
            "statement": "For a local GR/Newton limit, the q-basic metric sector must reduce to an Einstein-Hilbert kinetic term (M_EH^2/2) int sqrt(-g_eff) R[g_eff] plus residuals.",
            "role": "This is the exact target needed to connect MTS to GR rather than only to a phenomenological force law.",
            "derived_consequence": "Once this target is signed, the coupling equation is M_EH^2 G_{mu nu}=lambda_D T_{mu nu}+R_{mu nu}^{local}.",
            "parent_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "PAS4718_3_common_scale_not_relative_prefactor",
            "statement": "lambda_D is one common matter scale and is paired with M_EH^2; it is not an allowed composition-dependent source/test coefficient.",
            "role": "This answers the coupling worry cleanly: universal normalization belongs to G_N ownership, while relative source weights are WEP/R10/PPN residuals.",
            "derived_consequence": "delta_w_AB=0 if the signature is signed; common G calibration remains as a separate parent coefficient question.",
            "parent_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "PAS4718_4_verdict",
            "statement": "4718 derives the common G owner law from the candidate action signature but does not claim that MTS has already derived the numeric value of G_N.",
            "role": "This moves the work toward local GR/Newton in the right order: action signature, field equation, Newton limit, then tests.",
            "derived_consequence": "Next target is the local linearized GR and Poisson residual bound.",
            "parent_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def g_owner_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "law_id": "GNL4718_0_Einstein_coupling_law",
            "law": "If S_geo contains (M_EH^2/2) int sqrt(-g_eff) R and S_matter is multiplied by lambda_D, variation gives M_EH^2 G_{mu nu}=lambda_D T_{mu nu}+R_{mu nu}^{local}.",
            "consequence": "The effective local Newton coupling is G_eff=lambda_D/(8*pi*M_EH^2) when residuals vanish in the GR limit.",
            "claim_state": "derived_conditionally_from_signature",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "law_id": "GNL4718_1_Newton_Poisson_limit",
            "law": "In the weak-field, static, slow-motion limit g_00=-(1+2 Phi_N), the previous row yields nabla^2 Phi_N=4*pi*G_eff*rho+R_N.",
            "consequence": "The Newton limit is now a concrete residual target, not a slogan: R_N must be bounded by EH-closure, stress-owner, projection, boundary and readout terms.",
            "claim_state": "next_derivation_target",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "law_id": "GNL4718_2_numeric_G_status",
            "law": "The framework can own where G_N comes from before it derives the measured number: G_N is the ratio of common matter normalization lambda_D to metric kinetic normalization M_EH^2.",
            "consequence": "If lambda_D and M_EH^2 are independently derived by the deeper MTS parent, G_N is derived; otherwise G_N remains a calibration constant just as in GR.",
            "claim_state": "honest_nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "law_id": "GNL4718_3_relative_prefactor_separation",
            "law": "A universal rescaling of all matter stress shifts G_eff; a relative rescaling between source sectors violates the 4717 signature and feeds WEP/R10/PPN kernels.",
            "consequence": "This prevents using G_N calibration to hide composition-dependent coupling errors.",
            "claim_state": "firewall",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def local_residual_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "residual_id": "RLG4718_0_local_field_equation",
            "residual": "R_local^{mu nu}=R_EH_closure^{mu nu}+R_metric_projection^{mu nu}+R_stress_owner^{mu nu}+R_source_prefactor^{mu nu}+R_boundary^{mu nu}+R_readout^{mu nu}",
            "zero_condition": "EH kinetic target signed, q-basic metric projection controlled, same T_Q owner, 4717 source signature signed, boundary/projection silence.",
            "next_measure": "derive norm bound for ||R_local|| in 4719",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "residual_id": "RLG4718_1_Newton_residual",
            "residual": "R_N=K_EH R_EH_closure+K_T R_stress_owner+K_w||delta_w||+K_proj R_projection+K_bound R_boundary+K_readout R_readout",
            "zero_condition": "all local residual terms vanish or are below solar-system/Newtonian sensitivity.",
            "next_measure": "turn into Poisson/PPN acceptance gate in 4719",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "residual_id": "RLG4718_2_common_vs_relative_coupling",
            "residual": "G_eff drift belongs to D_tau ln(lambda_D/M_EH^2); relative source coupling belongs to delta_w/kappa/q kernels.",
            "zero_condition": "constant common normalization and signed no-relative-prefactor theorem.",
            "next_measure": "separate Gdot/orbital bound from WEP/R10 composition bounds",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def gate_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "GATE4718_0_parent_action_exists",
            "requirement": "A parent MTS action with the 4718 signature is explicitly written and accepted as the working parent.",
            "passed": False,
            "blocker": "PARENT_ACTION_SIGNATURE_UNSIGNED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "GATE4718_1_EH_kinetic_reduction",
            "requirement": "The q-basic metric sector reduces to (M_EH^2/2) int sqrt(-g) R plus bounded residuals.",
            "passed": False,
            "blocker": "EH_CLOSURE_NOT_DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "GATE4718_2_common_coefficients_owned",
            "requirement": "lambda_D and M_EH^2 are either derived from MTS primitives or explicitly declared calibration constants.",
            "passed": False,
            "blocker": "COMMON_COEFFICIENT_OWNER_NEEDED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "GATE4718_3_Newton_residual_bounded",
            "requirement": "R_N is bounded tightly enough to recover Newtonian mechanics in the appropriate local limit.",
            "passed": False,
            "blocker": "POISSON_RESIDUAL_BOUND_NEEDED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def firewall_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4718_0_no_numeric_G_claim",
            "rule": "Do not claim MTS has derived the measured numerical value of G_N from 4718.",
            "reason": "4718 derives the owner relation G_eff=lambda_D/(8*pi*M_EH^2), not the primitive values of lambda_D and M_EH^2.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4718_1_no_local_GR_claim",
            "rule": "Do not claim local GR/Newton closure until EH reduction and Poisson/PPN residuals are bounded.",
            "reason": "The field-equation bridge is staged but not yet closed.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def decision_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4718_0",
            "decision": DECISION,
            "meaning": "The coupling problem is now split correctly: relative source prefactors are banned by the 4717 signature if signed; the universal normalization becomes G_eff=lambda_D/(8*pi*M_EH^2) if the metric sector has an EH limit.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
    ]


def status_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4718_0",
            "status": "private_nonclaim_bridge_checkpoint",
            "summary": "Candidate parent action signature inserted; common G owner law derived conditionally; local GR/Newton residual target defined.",
            "claim_allowed": False,
            "timestamp_utc": ts,
        }
    ]


def next_target_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_id": "NT4718_0",
            "next_target": NEXT_TARGET,
            "why": "Now that the coupling law has a clean owner, the next honest step is to derive the local linearized GR limit and Poisson equation residual bound.",
            "derive_first": "expand g_eff=eta+h, show EH target gives linearized Einstein/Poisson equation, and route every non-EH term into R_N/R_PPN",
            "fallback": "if EH reduction cannot be derived, demote local-GR route to explicit closure with measured G_eff and finite residual gates",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
    ]


def write_docs(
    ts: str,
    sources: list[dict[str, Any]],
    action: list[dict[str, Any]],
    g_rows: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    source_lines = "\n".join(
        f"- `{r['source_id']}`: `{r['source_path']}`; exists={r['exists']}; needle_found={r['needle_found']}; role={r['role']}"
        for r in sources
    )
    action_lines = "\n".join(f"- `{r['row_id']}`: {r['statement']} Consequence: {r['derived_consequence']}" for r in action)
    g_lines = "\n".join(f"- `{r['law_id']}`: `{r['law']}` Consequence: {r['consequence']}" for r in g_rows)
    residual_lines = "\n".join(f"- `{r['residual_id']}`: `{r['residual']}` Zero condition: {r['zero_condition']}" for r in residuals)
    gate_lines = "\n".join(f"- `{r['gate_id']}`: passed={r['passed']}; blocker=`{r['blocker']}`." for r in gates)

    write_text(
        DOC_PATH,
        f"""# 4718 - Parent Action Signature Insertion and Common G Normalization Owner

Generated: `{ts}`

## Purpose

This checkpoint turns the coupling worry into an action-level bridge. The question is no longer “is the coupling missing?” but:

1. does the parent action have the no-prefactor matter signature from 4717?
2. does the local metric sector reduce to an Einstein-Hilbert kinetic term?
3. are the common matter and metric normalizations owned or honestly calibrated?

## Candidate Parent Signature

`S_parent = S_geo[Phi] + S_MTS_aux[Phi] + lambda_D S_matter[Psi; e_obs(q(Phi)), omega(e_obs), A_Q(q(Phi)), theta_rep] + S_boundary`

This is deliberately narrow. It allows one common matter density-line scale `lambda_D`, but it does not allow `sum_A w_A S_A`, `kappa_A A_Q J_A`, private `q_A(X)`, hidden source markers, or post-variation source rescaling as parent couplings.

## Derived Common G Owner Law

If the local metric sector reduces to:

`S_geo -> (M_EH^2/2) int sqrt(-g_eff) R[g_eff]`

and the matter part is multiplied by `lambda_D`, variation gives:

`M_EH^2 G_mu_nu = lambda_D T_mu_nu + R_mu_nu^local`

so the effective Newton coupling is:

`G_eff = lambda_D / (8*pi*M_EH^2)`

This is the honest GR-style result. It derives where `G` lives. It does not yet derive the measured number unless MTS derives `lambda_D` and `M_EH^2` from deeper primitives.

## Why This Helps

Universal normalization and relative source coupling are now separated:

- universal scale: `G_eff=lambda_D/(8*pi*M_EH^2)`;
- relative source prefactors: `delta_w`, `Delta kappa`, `D_X ln q_A`, hidden markers;
- local-GR/Newton target: bound `R_mu_nu^local` and `R_N`.

That is the correct way to connect MTS to GR/Newton without pretending GR itself derives its coupling constant.

## Action Rows

{action_lines}

## G Owner Rows

{g_lines}

## Local Residual Rows

{residual_lines}

## Gates

{gate_lines}

## Source Register

{source_lines}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
""",
    )

    write_text(
        FORMAL_PATH,
        f"""# PPC4161 4718 - Parent Action Signature and Common G Normalization Owner

Generated: `{ts}`

## Formal Bridge

Assume the local metric sector of the parent action has an Einstein-Hilbert limit:

`S_geo = (M_EH^2/2) int sqrt(-g_eff) R[g_eff] + S_res`

and ordinary matter enters through one common density-line scale:

`S_m = lambda_D S_matter[Psi;g_eff,A_Q,theta]`.

Then variation before readout yields:

`M_EH^2 G_mu_nu = lambda_D T_mu_nu + R_mu_nu^local`.

Comparison with `G_mu_nu = 8*pi*G_N T_mu_nu` gives:

`G_eff = lambda_D/(8*pi*M_EH^2)`.

## Nonclaim Boundary

This does not yet prove local GR or derive the numerical value of `G_N`; it supplies the owner relation that 4719 must use in the linearized/Poisson residual bound.

## Decision

`{DECISION}`

## Next

`{NEXT_TARGET}`
""",
    )


def update_claims(ts: str) -> None:
    with CLAIMS_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        rows = list(reader)
    if CLAIM_ID in {row.get("claim_id", "") for row in rows}:
        return
    new_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_newton_bridge",
        "claim": "4718 inserts a candidate parent action signature and derives the common G owner relation G_eff=lambda_D/(8*pi*M_EH^2) conditionally on an EH local metric limit.",
        "current_evidence": "Generated source register, action signature rows, common G owner rows, local GR/Newton residual rows, gates, firewalls, decision, status, next target and validation.",
        "status": "conditional_bridge_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Confusing ownership of the coupling relation with derivation of the numerical measured value of G_N or closure of local GR.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "",
        "title": "Parent action signature and common G normalization owner",
        "notes": f"{MARKER}; {DECISION}; generated {ts}",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        csv.DictWriter(handle, fieldnames=fieldnames).writerow(new_row)


def update_resume(ts: str) -> None:
    write_text(
        RESUME_PATH,
        f"""# Current Local Resume

Updated: `{ts}`

## Latest completed checkpoint

`4718-Y5-R2FR-parent-action-signature-insertion-and-common-G-normalization-owner.md`

## Decision

`{DECISION}`

## What moved forward

- The source-coupling branch now has an action-level candidate signature.
- Relative source prefactors are separated from universal normalization.
- The common Newton/GR coupling owner law is conditionally derived:

`G_eff = lambda_D / (8*pi*M_EH^2)`

- This is not yet a numerical derivation of `G_N`; it is the correct bridge law that 4719 must push into the local linearized GR/Newton limit.

## Current target

`{NEXT_TARGET}`

## Local-only note

No GitHub action was performed by this checkpoint.
""",
    )


def validation_rows(
    ts: str,
    sources: list[dict[str, Any]],
    action: list[dict[str, Any]],
    g_rows: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = [
        ("VAL4718_sources_exist", all(r["exists"] for r in sources), "all cited local source paths exist"),
        ("VAL4718_needles_found", all(r["needle_found"] for r in sources), "all cited source needles found"),
        ("VAL4718_action_signature", any(r["row_id"] == "PAS4718_0_candidate_parent_action" for r in action), "candidate parent action row present"),
        ("VAL4718_EH_target", any(r["row_id"] == "PAS4718_2_metric_sector_EH_target" for r in action), "EH kinetic target row present"),
        ("VAL4718_G_owner_law", any(r["law_id"] == "GNL4718_0_Einstein_coupling_law" and "lambda_D/(8*pi*M_EH^2)" in r["consequence"] for r in g_rows), "G owner law present"),
        ("VAL4718_Newton_limit", any(r["law_id"] == "GNL4718_1_Newton_Poisson_limit" for r in g_rows), "Newton/Poisson limit row present"),
        ("VAL4718_residual_vector", len(residuals) >= 3 and any(r["residual_id"] == "RLG4718_1_Newton_residual" for r in residuals), "local residual vector rows present"),
        ("VAL4718_no_claim_allowed", all(not bool(r.get("valid_for_claim")) for r in sources + action + g_rows + residuals + gates), "no row allows a claim"),
        ("VAL4718_gates_not_passing", not all(bool(r["passed"]) for r in gates), "promotion gates not all passing"),
        ("VAL4718_doc_written", DOC_PATH.exists() and DOC_PATH.stat().st_size > 1000, "checkpoint document written"),
        ("VAL4718_formal_written", FORMAL_PATH.exists() and FORMAL_PATH.stat().st_size > 500, "formal packet document written"),
        ("VAL4718_no_pycache", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "validation_id": check_id,
            "passed": passed,
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "validation_id": "VAL4718_OVERALL",
            "passed": overall,
            "detail": "4718 artifacts validate as private nonclaim GR/Newton bridge checkpoint",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
    )
    return rows


def main() -> None:
    ts = now()

    sources = source_register(ts)
    action = action_signature_rows(ts)
    g_rows = g_owner_rows(ts)
    residuals = local_residual_rows(ts)
    gates = gate_rows(ts)
    firewalls = firewall_rows(ts)
    decisions = decision_rows(ts)
    statuses = status_rows(ts)
    next_targets = next_target_rows(ts)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(ACTION_SIGNATURE_CSV, action)
    write_csv(G_OWNER_CSV, g_rows)
    write_csv(LOCAL_RESIDUAL_CSV, residuals)
    write_csv(GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)

    write_docs(ts, sources, action, g_rows, residuals, gates)
    update_claims(ts)
    append_once(
        SPINE_PATH,
        MARKER,
        f"""### {MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Derivation gain: common source coupling is now owned by `G_eff=lambda_D/(8*pi*M_EH^2)` if the local metric sector has an EH limit.
- Still blocked: parent action signature, EH kinetic reduction, and Poisson/PPN residual bounds remain unsigned.
- Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""### {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet role: connects the no-prefactor source signature to a GR/Newton coupling owner law and stages the local field-equation residual vector.
- Validation: `{VALIDATION_CSV}`.
""",
    )
    update_resume(ts)

    shutil.rmtree(POST / "scripts" / "__pycache__", ignore_errors=True)
    write_csv(VALIDATION_CSV, validation_rows(ts, sources, action, g_rows, residuals, gates))


if __name__ == "__main__":
    main()
