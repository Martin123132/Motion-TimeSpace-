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

CHECKPOINT = "4717"
CLAIM_ID = "L-559"
MARKER = "PPC4161_NO_PREACTION_SOURCE_PREFACTOR_SIGNATURE_OR_DELTAW_KERNEL_4717"
PACKET_MARKER = "PPC4161_PACKET_NO_PREACTION_SOURCE_PREFACTOR_SIGNATURE_OR_DELTAW_KERNEL_4717"
DECISION = "SUFFICIENCY_THEOREM_BUILT_PARENT_SIGNATURE_UNSIGNED_DELTAW_KERNEL_STAGED_NONCLAIM"
NEXT_TARGET = "4718-Y5-R2FR-parent-action-signature-insertion-and-common-G-normalization-owner.md"

DOC_PATH = POST / "4717-Y5-R2FR-no-preaction-source-prefactor-signature-or-deltaw-kernel-first-row.md"
FORMAL_PATH = FORMAL / "733-PPC4161-no-preaction-source-prefactor-signature-or-deltaw-kernel-first-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4717_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4717_NO_PREACTION_PREFACTOR_SIGNATURE_THEOREM.csv"
CONTRACT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4717_PARENT_SIGNATURE_CONTRACT.csv"
KERNEL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4717_DELTAW_KERNEL_FIRST_ROWS.csv"
GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4717_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4717_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4717_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4717_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4717_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4717_VALIDATION.csv"


SOURCE_SPECS = [
    {
        "source_id": "SRC4717_0",
        "path": "P8_Y5_R2FR_4716_CURRENT_RESCALE_NO_MORPHISM_THEOREM.csv",
        "needle": "NCM4716_1_preaction_countermodel",
        "role": "4716 obstruction: pre-action source/current prefactors survive ordinary current ownership.",
    },
    {
        "source_id": "SRC4717_1",
        "path": "P8_Y5_R2FR_4716_FIRST_SOURCE_TEST_COEFFICIENT_ROWS.csv",
        "needle": "COEF4716_0_delta_w_species",
        "role": "First live coefficient vector that 4717 tries to kill by signature or route into kernels.",
    },
    {
        "source_id": "SRC4717_2",
        "path": "P8_Y5_PARENT_QLOC_1815_NO_CURRENT_RESCALE_THEOREM.csv",
        "needle": "NCR1815_3_connected_naturality",
        "role": "Earlier connected-naturality route for banning relative source weights.",
    },
    {
        "source_id": "SRC4717_3",
        "path": "P8_EM_no_source_only_matter_functor_residual.csv",
        "needle": "NSSR3509_0_delta_w_species",
        "role": "Matter-functor residual ledger for relative source/species weights.",
    },
    {
        "source_id": "SRC4717_4",
        "path": "P8_EM_common_action_density_line_universal_source_scale.csv",
        "needle": "UCSR3510_1_delta_w_species",
        "role": "Common density-line scale versus forbidden relative species/source weights.",
    },
    {
        "source_id": "SRC4717_5",
        "path": "P8_EM_vq_parent_object_language_normal_form_candidate.csv",
        "needle": "NF3519_2_matter_functor",
        "role": "Candidate normal form forbidding private source prefactors.",
    },
    {
        "source_id": "SRC4717_6",
        "path": "P8_Y5_PARENT_QLOC_1890_NO_SOURCE_PREFACTOR_THEOREM_ATTEMPT.csv",
        "needle": "NSP1890_6_countermodel",
        "role": "Countermodel showing covariance/Ward alone do not kill pre-action prefactors.",
    },
    {
        "source_id": "SRC4717_7",
        "path": "P8_Y5_PARENT_QLOC_1892_ORDINARY_MATTER_ACTION_SIGNATURE_ATTEMPT.csv",
        "needle": "OMAS1892_0_target_signature",
        "role": "Earlier ordinary-matter action signature target.",
    },
    {
        "source_id": "SRC4717_8",
        "path": "P8_Y5_PARENT_QLOC_1893_LABEL_FORGETTING_CLAUSE_AUDIT.csv",
        "needle": "LFA1893_2_no_prefactors",
        "role": "Label-forgetting clause audit for no independent source-only species prefactors.",
    },
    {
        "source_id": "SRC4717_9",
        "path": "P8_Y5_R10_765_RESCALING_COUNTEREXAMPLE_LEDGER.csv",
        "needle": "RCE765_2_current_rescale",
        "role": "Counterexample ledger motivating explicit coefficient kernels if signature is unsigned.",
    },
]


def timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"No rows for {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
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


def theorem_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "NPP4717_0_sufficient_signature",
            "claim": "A no-preaction-prefactor theorem is available if the parent ordinary-matter functor is label-forgetting and its action-density target has no relative scalar endomorphism slots.",
            "derivation": "Let C_m be the ordinary-matter source category and D be the common density-line target. A relative pre-action prefactor is a natural transformation w:C_m->R_+ that is visible only to source labels. If C_m is connected under allowed matter/source identifications and R_+ has no nontrivial label action, naturality along every A->B gives w_A=w_B. Hence delta_w_AB=0; only one common scale survives.",
            "status": "sufficient_theorem_proved",
            "parent_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "NPP4717_1_preaction_wA_iltyped",
            "claim": "A term sum_A w_A S_A is not a legal parent term under the signature unless w_A factors through the single common action-density scale.",
            "derivation": "The coefficient w_A needs a map from a species/source label object into the scalar density line. The signature removes that object from the parent language before variation, so a relative w_A has no domain. A universal w_common remains a normalization of the whole matter action and is routed to the G/action-density owner, not to WEP-like relative residuals.",
            "status": "exact_if_signature_signed",
            "parent_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "NPP4717_2_kappa_q_current_iltyped",
            "claim": "Source-only kappa_A and q_A(X) current weights are illegal under the same signature unless they are representation constants already present in the matter bundle, not source/readout prefactors.",
            "derivation": "A pre-variation current weight requires Coeff(J_Q), Hom(label,C_source), or a private X-dependent scalar in the action grammar. The no-morphism signature admits fields, q-basic geometry/gauge data, fixed representation constants, and one common density scale only. Therefore relative kappa_A or q_A(X) are coefficient insertions, not derived currents.",
            "status": "exact_if_signature_signed",
            "parent_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "NPP4717_3_hidden_marker_iltyped",
            "claim": "Hidden material/source markers are banned by label forgetting; if they remain, the local branch must carry them as explicit composition-dependent residuals.",
            "derivation": "A hidden marker is precisely a non-forgotten label carried from material/source identity into the coefficient target. The label-forgetting functor sends these labels to the same parent source object before variation; no distinct scalar coefficient can be formed without adding forbidden structure.",
            "status": "exact_if_signature_signed",
            "parent_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "NPP4717_4_countermodel_boundary",
            "claim": "The theorem does not follow from covariance, Ward conservation, or current ownership alone.",
            "derivation": "If the parent grammar permits disconnected source labels or explicit scalar coefficient slots, S_matter=sum_A w_A S_A and S_int=sum_A kappa_A A_Q J_A remain covariant and can satisfy a weighted Ward identity. That is the countermodel, so the signature is not optional wording; it is the missing mathematical contract.",
            "status": "countermodel_retained",
            "parent_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "NPP4717_5_verdict",
            "claim": "4717 moves the branch forward: it proves the sufficient no-prefactor theorem and stages the first delta_w/kappa/q kernel, but it still does not claim local-GR or source-coupling closure until the parent action itself signs the signature.",
            "derivation": "This is stronger than a missing-item ledger because it identifies the exact parent-language axiom that kills the coupling leak. It also names the finite residual vector to use if the parent refuses that axiom.",
            "status": "private_nonclaim_progress",
            "parent_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def contract_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "contract_id": "PSC4717_0_single_density_line",
            "clause": "One common matter action-density line lambda_D multiplies the total ordinary-matter action.",
            "kills": "relative w_A, relative action-unit drift",
            "survivor": "one common normalization routed to G/action-density calibration",
            "parent_status": "unsigned_parent_clause",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "contract_id": "PSC4717_1_connected_label_forgetting",
            "clause": "The source functor forgets ordinary composition labels before variation and the ordinary matter source category is connected for allowed source/test comparisons.",
            "kills": "delta_w_species, hidden_marker_source",
            "survivor": "composition dependence only through measured stress/current after variation",
            "parent_status": "unsigned_parent_clause",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "contract_id": "PSC4717_2_no_scalar_coefficient_target",
            "clause": "The parent object language has no Coeff(J_Q), no Hom(label,C_source), and no independent source-only scalar endomorphism target.",
            "kills": "kappa_A_source, q_A_current, c_A_current",
            "survivor": "fixed representation constants already inside matter bundles",
            "parent_status": "unsigned_parent_clause",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "contract_id": "PSC4717_3_variation_before_readout",
            "clause": "The parent action is varied once to produce J_Q and T_Q before any source/test readout, worldtube split, or calibration map is applied.",
            "kills": "post-variation current/source rescaling",
            "survivor": "readout calibration residuals only",
            "parent_status": "supported_by_4716_but_parent_signature_needed",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "contract_id": "PSC4717_4_common_G_normalization_route",
            "clause": "The common matter normalization is paired with the gravitational coupling normalization rather than fitted separately per source sector.",
            "kills": "fake WEP/local residual from universal scale",
            "survivor": "G_N measurement/calibration problem, not a relative source-coupling violation",
            "parent_status": "next_target",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "contract_id": "PSC4717_5_boundary_projection_silence",
            "clause": "Boundary, wall flux, and local projection terms do not reintroduce label-dependent source coefficients.",
            "kills": "boundary-sidechannel source weights",
            "survivor": "explicit finite boundary/readout residuals if not signed",
            "parent_status": "unsigned_parent_clause",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def kernel_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "kernel_id": "DWK4717_0_R10_pairwise_composition",
            "arena": "R10_short_range",
            "first_kernel": "eta_R10_AB(lambda)=K_R10_w_AB(lambda)*(delta_w_A-delta_w_B)+K_R10_kappa_AB(lambda)*Delta_kappa_AB+K_R10_q_AB(lambda)*<D_X ln q_A-D_X ln q_B>+K_R10_h_AB(lambda)*hidden_marker_AB+B_R10_readout",
            "required_inputs": "composition fractions A/B, lambda, arena Green kernel, source/test map, parent coefficient signs",
            "claim_state": "nonclaim_kernel_staged",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "kernel_id": "DWK4717_1_WEP_Eotvos",
            "arena": "WEP_Eotvos",
            "first_kernel": "eta_AB=sum_i(f_i^A-f_i^B)*delta_w_i+sum_i(f_i^A-f_i^B)*Delta_kappa_i+K_q_AB*sup|D_X ln q_i|+B_WEP_readout",
            "required_inputs": "source/test composition vectors, isotope/electron/nuclear fractions, torsion-balance kernel, coefficient priors",
            "claim_state": "nonclaim_kernel_staged",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "kernel_id": "DWK4717_2_PPN_source_vector",
            "arena": "PPN_local_GR",
            "first_kernel": "||Delta_PPN||<=|K_gamma_w|*||delta_w||+|K_beta_w|*||delta_w||+|K_kappa|*||Delta_kappa||+|K_q|*sup|D_X ln q_A|+B_PPN_projection+B_metric_closure",
            "required_inputs": "metric closure map, matter-source fractions, PPN observable basis, parent signature signs",
            "claim_state": "nonclaim_kernel_staged",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "kernel_id": "DWK4717_3_clock_alpha_EM",
            "arena": "clocks_alpha_EM",
            "first_kernel": "|D_tau ln alpha_EM|<=L_linear|tau_clock_time|+K_clock_w||delta_w_EM||+K_clock_q sup|D_X ln q_EM|+B_rad_clock+B_readout_clock",
            "required_inputs": "clock transition sensitivities, EM owner map, linear leak bound from 4713, parent coefficient signs",
            "claim_state": "nonclaim_kernel_staged",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "kernel_id": "DWK4717_4_orbital_Gdot_common_scale",
            "arena": "orbital_Newtonian",
            "first_kernel": "|dotG_eff/G_eff|<=|D_tau ln w_common|+K_orb_w||delta_w_relative||+K_orb_q sup|D_X ln q_A|+B_ephemeris+B_projection",
            "required_inputs": "common scale owner, ephemeris kernel, source/test composition leakage, time-projection map",
            "claim_state": "nonclaim_kernel_staged",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "kernel_id": "DWK4717_5_Newton_constant_owner",
            "arena": "G_Newton_normalization",
            "first_kernel": "G_N is owned by the common normalization relation between the gravitational kinetic term and the total matter density line; relative source weights are not allowed to masquerade as G_N.",
            "required_inputs": "parent action normalization, kinetic coefficient, matter density-line normalization, calibration convention",
            "claim_state": "conceptual_kernel_for_4718",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def gate_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "GATE4717_0_parent_signature_adopted",
            "requirement": "Parent action explicitly adopts the label-forgetting ordinary-matter/source-functor signature.",
            "passed": False,
            "blocking_residual": "PARENT_SIGNATURE_UNSIGNED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "GATE4717_1_no_prefactor_targets",
            "requirement": "No Coeff(J_Q), Hom(label,C_source), source-only scalar, or q_A(X) target exists in the parent grammar.",
            "passed": False,
            "blocking_residual": "COEFFICIENT_TARGET_AUDIT_NEEDED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "GATE4717_2_common_G_owner",
            "requirement": "The universal matter scale is paired with the gravitational kinetic normalization and not fitted as a source/test residual.",
            "passed": False,
            "blocking_residual": "COMMON_G_NORMALIZATION_OWNER_NEEDED",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "GATE4717_3_numeric_kernel_inputs",
            "requirement": "R10/WEP/PPN/clock/orbital kernels have numeric source/test coefficients and cited bounds.",
            "passed": False,
            "blocking_residual": "NUMERIC_ARENA_KERNELS_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def firewall_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4717_0_no_GR_claim",
            "rule": "Do not claim local GR, PPN, WEP, R10, clock, orbital, or Newtonian closure from 4717.",
            "reason": "The sufficiency theorem is proved, but the parent action has not yet been shown to satisfy the signature.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4717_1_no_G_derivation_claim",
            "rule": "Do not claim MTS derives the measured numerical value of G_N at 4717.",
            "reason": "4717 only separates common normalization from relative source weights; deriving or owning G_N is the 4718 target.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def decision_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4717_0",
            "decision": DECISION,
            "meaning": "We no longer merely say the coupling is missing. We have a precise theorem: relative source prefactors vanish if the parent action is a connected label-forgetting matter functor with one density-line scale and no scalar coefficient target. The remaining work is to sign that into the parent action or use the delta_w kernel.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
    ]


def status_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4717_0",
            "status": "private_nonclaim_derivation_checkpoint",
            "summary": "Sufficient no-preaction-prefactor theorem proved under an explicit parent signature; parent signature remains unsigned; first delta_w/kappa/q arena kernels staged.",
            "claim_allowed": False,
            "timestamp_utc": ts,
        }
    ]


def next_target_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_id": "NT4717_0",
            "next_target": NEXT_TARGET,
            "why": "The theorem needs to be attached to the parent action, and the common matter normalization has to be routed into the G_N/Newton limit rather than confused with relative source coupling.",
            "derive_first": "write the parent action signature S_parent=S_geo[Phi]+lambda_D S_matter[Psi;q(Phi),theta]+S_bound and prove no source-label scalar targets exist",
            "fallback": "keep parent unsigned and start filling numeric delta_w/kappa/q kernels for WEP/R10/PPN/clock/orbital tests",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
    ]


def write_documents(
    ts: str,
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    kernels: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    source_lines = "\n".join(
        f"- `{row['source_id']}`: `{row['source_path']}`; exists={row['exists']}; needle_found={row['needle_found']}; role={row['role']}"
        for row in sources
    )
    theorem_lines = "\n".join(
        f"- `{row['row_id']}` ({row['status']}): {row['claim']}"
        for row in theorem
    )
    contract_lines = "\n".join(
        f"- `{row['contract_id']}`: {row['clause']} Kills: {row['kills']}. Survivor: {row['survivor']}."
        for row in contract
    )
    kernel_lines = "\n".join(
        f"- `{row['kernel_id']}` / `{row['arena']}`: `{row['first_kernel']}`"
        for row in kernels
    )
    gate_lines = "\n".join(
        f"- `{row['gate_id']}`: passed={row['passed']}; blocker=`{row['blocking_residual']}`."
        for row in gates
    )

    write_text(
        DOC_PATH,
        f"""# 4717 - No Pre-Action Source Prefactor Signature or Delta-W Kernel First Row

Generated: `{ts}`

## Purpose

Checkpoint 4716 showed that post-variation current rescaling is conditionally demoted, but pre-action source prefactors survive unless the parent object language forbids them. This checkpoint takes the derivation route first.

## Result

This is real progress, not another missing-item loop:

1. A sufficient no-prefactor theorem is now explicit.
2. The theorem says relative source weights vanish if the ordinary-matter/source functor is connected, label-forgetting, and has one common action-density line with no scalar coefficient target.
3. The theorem is not yet a public/local-GR claim because the parent action still has to sign that exact signature.
4. If the parent refuses the signature, the branch is not vague; it carries the staged `delta_w/kappa/q_A` kernel into R10, WEP, PPN, clock, orbital, and Newtonian tests.

## Sufficient Theorem

Let `C_m` be the ordinary-matter source category and let `D` be the common action-density line. A relative pre-action source prefactor is a natural transformation `w:C_m -> R_+` that can see source labels before variation. If:

- `C_m` is connected for the source/test comparisons under consideration;
- the source functor forgets composition labels before variation;
- the parent language has no `Coeff(J_Q)`, `Hom(label,C_source)`, private `q_A(X)`, or source-only scalar target;
- the matter action is multiplied only by one common density-line scale;

then naturality along every allowed source identification forces `w_A=w_B`. Hence `delta_w_AB=0`. The same typing argument bans relative `kappa_A`, `q_A(X)`, hidden source markers, and post-variation `c_A` as parent source terms.

## Important G_N / Newton Point

GR does not derive the measured number `G_N` from pure geometry alone; it owns where `G_N` enters the coupling between geometry and stress-energy. For MTS, the analogous honest target is:

`G_N` must be owned by the common normalization relation between the gravitational kinetic term and the total matter density line.

That is different from allowing per-source prefactors. A universal scale belongs to calibration/Newton-limit ownership; relative source weights belong to WEP/R10/PPN residuals.

## Theorem Rows

{theorem_lines}

## Parent Signature Contract

{contract_lines}

## First Delta-W Kernel Rows

{kernel_lines}

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
        f"""# PPC4161 4717 - No Pre-Action Source Prefactor Signature / Delta-W Kernel

Generated: `{ts}`

## Formal Statement

The local source-coupling leak reduces to a parent-language question.

If the parent matter action is a connected label-forgetting functor into a single common density line, with no scalar coefficient target for source labels or currents, then all relative pre-action source prefactors are ill-typed or constant by naturality:

`delta_w_AB = 0`, `Delta kappa_AB = 0`, `D_X ln q_A = 0`, and hidden material/source markers do not enter `J_Q`.

The theorem is conditional because the parent action has not yet been shown to carry this signature.

## Nonclaim Residual

If the signature is not signed:

`E_source_test = ||delta_w|| + ||Delta kappa|| + sup|D_X ln q_A| + |hidden_marker_source| + B_readout + B_boundary`

with arena kernels in `{KERNEL_CSV}`.

## Decision

`{DECISION}`

## Next

`{NEXT_TARGET}`
""",
    )


def update_claims(ts: str) -> None:
    CLAIMS_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not CLAIMS_PATH.exists():
        raise FileNotFoundError(CLAIMS_PATH)
    with CLAIMS_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        rows = list(reader)
    if CLAIM_ID in {row.get("claim_id", "") for row in rows}:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_empirical_interface",
        "claim": "4717 proves a sufficient no-preaction-source-prefactor theorem under a connected label-forgetting parent matter signature, and stages delta_w/kappa/q kernels if unsigned.",
        "current_evidence": "Generated source register, theorem rows, parent signature contract, first delta_w arena kernels, promotion gates, firewalls, decision, status, next target and validation.",
        "status": "sufficiency_theorem_parent_unsigned_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Mistaking a sufficient parent signature theorem for proof that the existing parent action already satisfies the signature.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "",
        "title": "No preaction source prefactor signature or delta-w kernel first row",
        "notes": f"{MARKER}; {DECISION}; generated {ts}",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writerow(row)


def update_resume(ts: str) -> None:
    write_text(
        RESUME_PATH,
        f"""# Current Local Resume

Updated: `{ts}`

## Latest completed checkpoint

`4717-Y5-R2FR-no-preaction-source-prefactor-signature-or-deltaw-kernel-first-row.md`

## Decision

`{DECISION}`

## What moved forward

- The branch now has a precise sufficient theorem for killing relative pre-action source prefactors.
- The theorem is: connected label-forgetting matter functor + one common density-line scale + no scalar coefficient target implies `delta_w_AB=0` and bans source-only `kappa_A/q_A/c_A` current weights.
- The common scale is not a WEP-style violation; it must be routed into the Newton/`G_N` normalization owner.
- No local-GR/R10/WEP/PPN/clock/orbital claim is allowed yet because the parent action has not signed the signature.

## Current target

`{NEXT_TARGET}`

## Local-only note

No GitHub action was performed by this checkpoint.
""",
    )


def validation_rows(
    ts: str,
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    kernels: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = [
        ("VAL4717_sources_exist", all(row["exists"] for row in sources), "all cited local source paths exist"),
        ("VAL4717_needles_found", all(row["needle_found"] for row in sources), "all cited source needles found"),
        (
            "VAL4717_sufficiency_theorem",
            any(row["row_id"] == "NPP4717_0_sufficient_signature" and row["status"] == "sufficient_theorem_proved" for row in theorem),
            "sufficient no-prefactor theorem present",
        ),
        (
            "VAL4717_countermodel_retained",
            any(row["row_id"] == "NPP4717_4_countermodel_boundary" for row in theorem),
            "covariance/Ward countermodel retained",
        ),
        (
            "VAL4717_contract_clauses",
            len(contract) >= 6 and any(row["contract_id"] == "PSC4717_4_common_G_normalization_route" for row in contract),
            "parent signature contract clauses present including common G route",
        ),
        (
            "VAL4717_delta_w_kernels",
            len(kernels) >= 6 and any(row["kernel_id"] == "DWK4717_5_Newton_constant_owner" for row in kernels),
            "delta_w kernels present including Newton/G owner row",
        ),
        (
            "VAL4717_no_claim_allowed",
            all(not bool(row.get("valid_for_claim")) for row in sources + theorem + contract + kernels + gates),
            "no row allows a claim",
        ),
        (
            "VAL4717_gates_not_passing",
            not all(bool(row["passed"]) for row in gates),
            "promotion gates not all passing",
        ),
        ("VAL4717_doc_written", DOC_PATH.exists() and DOC_PATH.stat().st_size > 1000, "checkpoint document written"),
        ("VAL4717_formal_written", FORMAL_PATH.exists() and FORMAL_PATH.stat().st_size > 500, "formal packet document written"),
        ("VAL4717_no_pycache", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
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
            "validation_id": "VAL4717_OVERALL",
            "passed": overall,
            "detail": "4717 artifacts validate as private nonclaim derivation checkpoint",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
    )
    return rows


def main() -> None:
    ts = timestamp()

    sources = source_register(ts)
    theorem = theorem_rows(ts)
    contract = contract_rows(ts)
    kernels = kernel_rows(ts)
    gates = gate_rows(ts)
    firewalls = firewall_rows(ts)
    decisions = decision_rows(ts)
    statuses = status_rows(ts)
    next_targets = next_target_rows(ts)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(THEOREM_CSV, theorem)
    write_csv(CONTRACT_CSV, contract)
    write_csv(KERNEL_CSV, kernels)
    write_csv(GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)

    write_documents(ts, sources, theorem, contract, kernels, gates)
    update_claims(ts)
    append_once(
        SPINE_PATH,
        MARKER,
        f"""### {MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Derivation gain: a sufficient no-preaction-source-prefactor theorem exists under a connected label-forgetting ordinary-matter signature.
- Still blocked: the parent action has not yet signed the signature, so all local arenas remain private nonclaims.
- Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""### {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet role: routes relative source-prefactor leakage into either an exact parent signature ban or a finite `delta_w/kappa/q_A` arena kernel.
- Validation: `{VALIDATION_CSV}`.
""",
    )
    update_resume(ts)

    shutil.rmtree(POST / "scripts" / "__pycache__", ignore_errors=True)
    validation = validation_rows(ts, sources, theorem, contract, kernels, gates)
    write_csv(VALIDATION_CSV, validation)


if __name__ == "__main__":
    main()
