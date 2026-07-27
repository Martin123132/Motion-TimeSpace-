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
DOC_PATH = ROOT / "4153-Y5-R2FR-topological-kappa-parent-action-stress-test-or-adoption-packet.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_TOPOLOGICAL_KAPPA_PARENT_STRESS_TEST_4153"
CHECKPOINT_ID = "4153"
DECISION = "TOPOLOGICAL_KAPPA_PARENT_ACTION_STRESS_TEST_PASSED_CONDITIONALLY_ADOPTION_PACKET_UNSIGNED_MU_EXTRA_NEXT"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4153_00_4152_doc": (
        ROOT / "4152-Y5-R2FR-topological-zero-form-kappa-superselection-or-coupling-drift-runner.md",
        "Insert this module into the minimal EH/source parent action",
        "4152 handoff to parent action stress test.",
    ),
    "SRC4153_01_4152_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4152_NEXT_TARGET.csv",
        "stress-test all variations",
        "Machine-readable 4152 next-target row.",
    ),
    "SRC4153_02_4152_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_4152_TOPOLOGICAL_ZEROFORM_THEOREM.csv",
        "DKAPPA_ZERO_EXACT_IF_SECTOR_ADOPTED",
        "4152 topological zero-form theorem.",
    ),
    "SRC4153_03_4152_audit": (
        SOURCE_DIR / "P8_Y5_R2FR_4152_VARIATION_AUDIT.csv",
        "PARENT_CLAUSE_REQUIRED",
        "4152 variation audit and open companion gate.",
    ),
    "SRC4153_04_4151_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_4151_EH_ONLY_NEWTON_THEOREM.csv",
        "NEWTON_SOURCE_THEOREM_DERIVED",
        "4151 EH-only Newton source theorem.",
    ),
    "SRC4153_05_3050_spine": (
        SOURCE_DIR / "P8_Y5_R2FR_3050_PARENT_TOPOLOGICAL_KAPPA_SPINE_CANDIDATE.csv",
        "SPINE3050_1_action",
        "Earlier parent action spine candidate.",
    ),
    "SRC4153_06_1088_matter": (
        ROOT / "1088-Y5-R10-minimal-parent-ordinary-matter-signature-clause-or-finite-coefficient-intake.md",
        "MOMS1088_0_action_form",
        "Minimal ordinary-matter parent signature clause.",
    ),
    "SRC4153_07_4080_kappa": (
        SOURCE_DIR / "P8_Y5_R2FR_4080_KAPPA_TOPOLOGICAL_THEOREM.csv",
        "KAP4080_0_constant_kappa",
        "Earlier exact conditional topological kappa theorem.",
    ),
    "SRC4153_08_4017_nohom": (
        SOURCE_DIR / "P8_Y5_R2FR_4017_KAPPA_VARIATION_AND_NOHOM_THEOREM.csv",
        "KVT4017_4_not_enough_for_local_GR",
        "No-Hom/anti-overclaim guard.",
    ),
    "SRC4153_09_script": (
        SCRIPT_PATH,
        "TOPOLOGICAL_KAPPA_PARENT_ACTION_STRESS_TEST_PASSED_CONDITIONALLY",
        "This generator records the 4153 topological kappa parent action stress test.",
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
        "P8_Y5_R2FR_4153_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4153_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4153_PARENT_ACTION_PACKET": SOURCE_DIR / "P8_Y5_R2FR_4153_PARENT_ACTION_PACKET.csv",
        "P8_Y5_R2FR_4153_VARIATION_STRESS_TEST": SOURCE_DIR / "P8_Y5_R2FR_4153_VARIATION_STRESS_TEST.csv",
        "P8_Y5_R2FR_4153_ADOPTION_PACKET_GATES": SOURCE_DIR / "P8_Y5_R2FR_4153_ADOPTION_PACKET_GATES.csv",
        "P8_Y5_R2FR_4153_NEWTON_LOCAL_GR_IMPACT": SOURCE_DIR / "P8_Y5_R2FR_4153_NEWTON_LOCAL_GR_IMPACT.csv",
        "P8_Y5_R2FR_4153_RESIDUALS_IF_REJECTED": SOURCE_DIR / "P8_Y5_R2FR_4153_RESIDUALS_IF_REJECTED.csv",
        "P8_Y5_R2FR_4153_DECISION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4153_DECISION_GATES.csv",
        "P8_Y5_R2FR_4153_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4153_STATUS.csv",
        "P8_Y5_R2FR_4153_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4153_NEXT_TARGET.csv",
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


def parent_action_packet_rows() -> List[dict]:
    return [
        {
            **common(),
            "packet_id": "PAP4153_0_total_action",
            "object": "candidate local parent action",
            "formula": "S_parent = (1/(2 kappa)) int_M eps_g R[g] + int_M kappa dA_3 + S_matter[psi,g_obs,theta] + S_boundary + S_rest",
            "role": "minimal local EH/source/kappa parent action stress-test packet",
            "adoption_status": "PRIVATE_PACKET_READY_UNSIGNED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "packet_id": "PAP4153_1_kappa_sector",
            "object": "topological kappa sector",
            "formula": "S_kappa_top = int_M kappa dA_3",
            "role": "A_3 variation enforces d kappa=0 without a kinetic scalar",
            "adoption_status": "SAFE_IF_BOUNDARY_AND_COMPANION_GATES_PASS",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "packet_id": "PAP4153_2_matter_signature",
            "object": "ordinary matter signature",
            "formula": "S_matter=sum_A S_A[Psi_A; g_obs, A_obs, theta_A], with partial_A kappa=partial_theta kappa=0",
            "role": "prevents source-label, material, frame, or clock constants from carrying hidden kappa dependence",
            "adoption_status": "REQUIRES_MOMS1088_SIGNATURE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "packet_id": "PAP4153_3_boundary_policy",
            "object": "boundary policy",
            "formula": "delta A_3|_partialM=0 or topological boundary term cancels; S_GHY uses same constant kappa after d kappa=0",
            "role": "keeps the zero-gradient proof from becoming hidden boundary/source-normalization closure",
            "adoption_status": "BOUNDARY_POLICY_REQUIRED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "packet_id": "PAP4153_4_rest_sector",
            "object": "all non-EH/rest sectors",
            "formula": "S_rest must have zero local monopole, zero PPN projection, or explicit residual rows",
            "role": "prevents the kappa win from being over-promoted to full Newton/local-GR recovery",
            "adoption_status": "MU_EXTRA_AND_Y6_STILL_OPEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def variation_stress_rows() -> List[dict]:
    return [
        {
            **common(),
            "test_id": "VST4153_0_A3",
            "variation": "delta_A3",
            "formula": "delta_A3 S = boundary - int_M d kappa wedge delta A_3",
            "result": "d kappa=0 on connected local domains",
            "stress_test_verdict": "PASS_CONDITIONAL_ON_BOUNDARY_POLICY",
            "residual_if_failed": "dln_Geff_dt; delta_kappa_source",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "test_id": "VST4153_1_metric",
            "variation": "delta_g",
            "formula": "delta_g[(1/(2 kappa)) int eps R] -> kappa^-1 G_mn + (nabla_m nabla_n-g_mn Box)kappa^-1",
            "result": "after d kappa=0, derivative scalar-tensor stress vanishes; int kappa dA_3 is metric-independent",
            "stress_test_verdict": "PASS_IF_DKAPPA_ZERO_AND_TOPOLOGICAL_TERM_METRIC_INDEPENDENT",
            "residual_if_failed": "Y6 T_extra; scalar-tensor PPN rows",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "test_id": "VST4153_2_kappa",
            "variation": "delta_kappa",
            "formula": "delta_kappa S = int_M delta kappa [dA_3 - (1/(2 kappa^2)) eps_g R] + delta_kappa S_matter + delta_kappa S_rest",
            "result": "companion equation sets dA_3=(1/(2 kappa^2))eps_g R only if matter/rest are kappa-blind; no local scalar propagation appears",
            "stress_test_verdict": "PASS_CONDITIONAL_COMPANION_NOT_PARENT_SIGNED",
            "residual_if_failed": "scalar-kappa source current; measured-mass flux; Y6 stress",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "test_id": "VST4153_3_matter",
            "variation": "delta_psi_and_delta_source_labels",
            "formula": "delta_kappa S_matter=0 and partial_A kappa=partial_source kappa=partial_frame kappa=0",
            "result": "no species/source/frame coupling drift if MOMS1088-style matter signature is adopted",
            "stress_test_verdict": "PASS_ONLY_IF_MATTER_SIGNATURE_SIGNED",
            "residual_if_failed": "eta_source_AB; delta_frame_source; qbar_constants",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "test_id": "VST4153_4_boundary",
            "variation": "boundary_variations",
            "formula": "delta S_boundary cancels EH boundary variation with constant kappa; int_partialM kappa delta A_3=0",
            "result": "boundary does not become a source-normalization channel if fixed/topological boundary policy is part of packet",
            "stress_test_verdict": "PASS_CONDITIONAL_BOUNDARY_UNSIGNED",
            "residual_if_failed": "boundary mu_extra; alpha3; radial/source hair",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "test_id": "VST4153_5_Bianchi",
            "variation": "Bianchi/Ward consistency",
            "formula": "q_kappa^nu=kappa^-1 P_loc[T_obs^{mu nu} nabla_mu kappa]=0 after d kappa=0",
            "result": "hidden exchange term vanishes if same-frame source and d kappa=0 both hold",
            "stress_test_verdict": "PASS_IF_DKAPPA_AND_SAME_FRAME_SOURCE",
            "residual_if_failed": "delta_kappa_source exchange row",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "test_id": "VST4153_6_PPN",
            "variation": "Newton/PPN projection",
            "formula": "dG_ref=0 closes pure coupling drift; beta still needs S_beta^source=0 and mu_extra=0",
            "result": "topological kappa adoption helps Y5 but does not by itself prove local GR",
            "stress_test_verdict": "ANTI_OVERCLAIM_PASS",
            "residual_if_failed": "delta_beta_source; mu_extra; Y6 T_extra",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def adoption_gate_rows() -> List[dict]:
    return [
        {
            **common(),
            "gate_id": "APG4153_0_action_packet",
            "gate": "candidate action packet is explicit",
            "pass_condition": "S_parent line includes EH, topological kappa, same-frame matter, boundary, and rest sectors",
            "current_result": "PASS_PACKET_WRITTEN",
            "adoption_credit": "private_candidate_only",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "APG4153_1_variations",
            "gate": "all local variations have a safe route",
            "pass_condition": "delta_A3, delta_g, delta_kappa, matter, boundary, Bianchi, and PPN tests produce no uncontrolled source if clauses hold",
            "current_result": "PASS_CONDITIONAL",
            "adoption_credit": "stress_test_passed_conditionally",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "APG4153_2_companion",
            "gate": "kappa companion equation is not a new scalar-force law",
            "pass_condition": "dA_3=(1/(2 kappa^2))eps R is global/topological and matter/rest are kappa-blind",
            "current_result": "UNSIGNED",
            "adoption_credit": "blocks_live_adoption",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "APG4153_3_matter_signature",
            "gate": "ordinary matter signature is parent-signed",
            "pass_condition": "MOMS1088 no species weights, no variable constants, no shadow frame, variation-before-readout",
            "current_result": "UNSIGNED",
            "adoption_credit": "blocks_source_charge_silence",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "APG4153_4_boundary",
            "gate": "A_3 and EH boundary policy is parent-signed",
            "pass_condition": "fixed/topological A_3 boundary and constant-kappa GHY term carry no measured mass flux",
            "current_result": "UNSIGNED",
            "adoption_credit": "blocks_boundary_source_normalization_silence",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "APG4153_5_claim",
            "gate": "Newton/local-GR promotion",
            "pass_condition": "topological kappa plus mu_extra=0, Hilbert mass flux, beta closure, Y6 stress silence",
            "current_result": "FAIL_CURRENT_CLAIM",
            "adoption_credit": "no_public_or_live_claim",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def impact_rows() -> List[dict]:
    return [
        {
            **common(),
            "impact_id": "IMP4153_0_coupling",
            "component": "pure coupling drift",
            "if_adopted": "dG_ref=0 and delta_kappa_source=0",
            "still_needed": "same-frame source and no-Hom matter signature",
            "status": "CLOSES_CONDITIONALLY",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "impact_id": "IMP4153_1_Newton",
            "component": "Newton source normalization",
            "if_adopted": "constant G_* part of mu_obs=G_* M_H+mu_extra is safe",
            "still_needed": "mu_extra=0 and closed Hilbert mass flux",
            "status": "PARTIAL_PROGRESS_NOT_NEWTON_PASS",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "impact_id": "IMP4153_2_PPN_beta",
            "component": "PPN beta source closure",
            "if_adopted": "kappa derivative terms vanish from beta source",
            "still_needed": "S_beta^source=0 for mu_extra/rest sectors",
            "status": "BETA_STILL_OPEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "impact_id": "IMP4153_3_Y6",
            "component": "extra stress",
            "if_adopted": "topological kappa sector contributes no metric stress",
            "still_needed": "all other S_rest/projector/domain stresses topological/invisible/bounded",
            "status": "KAPPA_Y6_SAFE_CONDITIONAL_OTHER_Y6_OPEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "impact_id": "IMP4153_4_EM_Maxwell",
            "component": "EM/Maxwell coupling consistency",
            "if_adopted": "gravitational source coupling no longer drifts into EM tests via kappa",
            "still_needed": "Maxwell action/Hodge/current ownership and alpha_EM constant-superselection remain separate",
            "status": "NO_EM_CLAIM",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def residual_rows() -> List[dict]:
    return [
        {
            **common(),
            "residual_id": "RR4153_0_reject_topological",
            "trigger": "topological kappa packet rejected or not adopted",
            "active_residuals": "dln_Geff_dt; delta_kappa_source; alpha(lambda); eta_source_AB; delta_frame_source",
            "runner_status": "RETAIN_COUPLING_DRIFT_RUNNER",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "residual_id": "RR4153_1_companion_fails",
            "trigger": "delta_kappa companion equation creates local scalar/source stress",
            "active_residuals": "scalar_kappa; Y6_T_extra; delta_beta_source",
            "runner_status": "DEMOTE_TO_SCALAR_KAPPA_BRANCH",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "residual_id": "RR4153_2_matter_fails",
            "trigger": "matter/source labels couple to kappa or ordinary matter signature remains unsigned",
            "active_residuals": "eta_source_AB; qbar_constants; delta_frame_source",
            "runner_status": "RETAIN_MATTER_SIGNATURE_OR_FINITE_DD_INTAKE",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "residual_id": "RR4153_3_boundary_fails",
            "trigger": "A_3 or EH boundary term carries source-normalization flux",
            "active_residuals": "boundary_mu_extra; alpha3; radial_source_hair",
            "runner_status": "RETAIN_BOUNDARY_SOURCE_NORMALIZATION_ROWS",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[dict]:
    return [
        {
            **common(),
            "decision_id": "DEC4153_0_packet",
            "question": "is there a coherent private parent-action packet for constant kappa?",
            "answer": "yes, conditionally",
            "decision": "ADOPTION_PACKET_READY_UNSIGNED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "DEC4153_1_stress_test",
            "question": "does the packet pass metric/A3/kappa/matter/boundary/Bianchi stress tests?",
            "answer": "it passes as a conditional packet, but companion, matter, and boundary gates are unsigned",
            "decision": "STRESS_TEST_PASSED_CONDITIONALLY_NOT_LIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "DEC4153_2_next",
            "question": "what is the next most valuable target?",
            "answer": "attack mu_extra=0 and closed Hilbert mass flux, because pure coupling drift now has a candidate mechanism",
            "decision": "NEXT_MU_EXTRA_HILBERT_FLUX_LOCK",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "DEC4153_3_claim",
            "question": "can this be treated as a local GR/Newton claim?",
            "answer": "no",
            "decision": "NO_NEWTON_LOCAL_GR_CLAIM",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def status_rows() -> List[dict]:
    return [
        {
            **common(),
            "result": DECISION,
            "parent_action_packet_written": "True",
            "A3_variation_dkappa_zero": "True",
            "metric_stress_test_passed_conditionally": "True",
            "kappa_companion_safe_signed": "False",
            "matter_signature_signed": "False",
            "boundary_policy_signed": "False",
            "coupling_drift_closed_if_adopted": "True",
            "mu_extra_zero_signed": "False",
            "Hilbert_mass_flux_signed": "False",
            "PPN_beta_closed": "False",
            "Newton_claimed": "False",
            "local_gr_claimed": "False",
            "next_target": "4154-Y5-R2FR-mu-extra-zero-and-Hilbert-mass-flux-lock-or-source-normalization-runner.md",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> List[dict]:
    return [
        {
            **common(),
            "next_id": "NEXT4153_0",
            "target_doc": "4154-Y5-R2FR-mu-extra-zero-and-Hilbert-mass-flux-lock-or-source-normalization-runner.md",
            "target_script": "scripts/Y5_R2FR_4154_mu_extra_zero_and_Hilbert_mass_flux_lock_or_source_normalization_runner.py",
            "objective": "with pure kappa drift now conditionally mechanism-owned, attack the remaining Newton source blocker: prove mu_extra=0 and closed Hilbert mass flux for the same-frame source branch, or turn the source-normalization residual vector into a finite runner",
            "success_gate": "all non-EH/rest monopoles vanish or are topological/bounded, Pi_M/Hilbert mass flux is closed, no boundary/domain/projector measured-mass flux survives, and beta source closure is either theorem-zero or explicitly bounded",
            "reason": "4153 moves kappa from magic constant toward a conditional parent mechanism; Newton still fails unless mu_extra and mass flux close.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def write_doc(outputs: Dict[str, Path]) -> None:
    text = f"""# 4153 - Topological Kappa Parent Action Stress Test Or Adoption Packet

Timestamp UTC: `{TIMESTAMP}`  
Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`

## Purpose
4152 constructed a real mechanism for constant coupling:

`S_kappa_top=int_M kappa dA_3`.

4153 stress-tests whether that mechanism can be inserted into the parent action without paying for `dG=0` through a new scalar force, boundary source, or Y6 stress.

## Candidate Parent Packet
The private candidate packet is:

`S_parent = (1/(2 kappa)) int_M eps_g R[g] + int_M kappa dA_3 + S_matter[psi,g_obs,theta] + S_boundary + S_rest`.

This is not public-facing and not a claim. It is a stress-test packet.

## Variation Results
### `A_3` variation
`delta_A3 S = boundary - int_M d kappa wedge delta A_3`.

With fixed/topological boundary variation:

`d kappa=0`.

### Metric variation
The EH term gives

`kappa^-1 G_mn + (nabla_m nabla_n-g_mn Box)kappa^-1`.

After `d kappa=0`, the derivative scalar-tensor terms vanish. The topological term `int kappa dA_3` is metric-independent, so it adds no local metric stress.

### `kappa` variation
This is the important stress test:

`delta_kappa S = int_M delta kappa [dA_3 - (1/(2 kappa^2)) eps_g R] + delta_kappa S_matter + delta_kappa S_rest`.

So the companion equation is:

`dA_3=(1/(2 kappa^2))eps_g R`

only if matter/rest sectors are `kappa`-blind. This does not propagate a scalar by itself, but it must be treated as a global/topological flux equation rather than a new source-current law.

## Conditional Adoption Verdict
The packet passes the internal mathematical stress test if all clauses are adopted:

- fixed/topological `A_3` boundary policy;
- metric-independent topological sector;
- no local kinetic/propagating `kappa` scalar;
- matter/source/frame/range/domain labels do not map into `kappa`;
- no hidden Bianchi exchange;
- `S_rest` either has zero local monopole/PPN projection or stays as residual rows.

But these clauses are not parent-signed in the current corpus. Therefore this is an adoption packet, not a live theorem claim.

## What This Actually Buys
If later adopted safely, this closes pure coupling drift:

- `dln_Geff_dt=0`;
- `delta_kappa_source=0`;
- `partial_lambda G_eff=0`;
- `partial_A G_eff=0`;
- `partial_frame G_eff=0`.

It does **not** close:

- `mu_extra`;
- closed Hilbert mass flux;
- `delta_beta_source`;
- Y6 extra stress;
- Maxwell/EM current ownership.

## Current Verdict
| Gate | Result | Meaning |
|---|---|---|
| parent packet | WRITTEN | explicit private candidate action |
| `A_3` variation | PASSES CONDITIONALLY | derives `d kappa=0` |
| metric stress | PASSES CONDITIONALLY | no new stress if topological/metric-independent |
| `kappa` companion | UNSIGNED | must stay global/topological, not scalar-force |
| matter signature | UNSIGNED | needs MOMS1088/no source labels |
| boundary policy | UNSIGNED | no measured mass/source flux from `A_3` boundary |
| local GR/Newton | NOT CLAIMED | `mu_extra`, mass flux, beta, Y6 still open |

## Outputs
- `{outputs["P8_Y5_R2FR_4153_SOURCE_REGISTER"]}`
- `{outputs["P8_Y5_R2FR_4153_PARENT_ACTION_PACKET"]}`
- `{outputs["P8_Y5_R2FR_4153_VARIATION_STRESS_TEST"]}`
- `{outputs["P8_Y5_R2FR_4153_ADOPTION_PACKET_GATES"]}`
- `{outputs["P8_Y5_R2FR_4153_NEWTON_LOCAL_GR_IMPACT"]}`
- `{outputs["P8_Y5_R2FR_4153_RESIDUALS_IF_REJECTED"]}`
- `{outputs["P8_Y5_R2FR_4153_DECISION_GATES"]}`
- `{outputs["P8_Y5_R2FR_4153_STATUS"]}`
- `{outputs["P8_Y5_R2FR_4153_NEXT_TARGET"]}`

## Next Target
- `4154-Y5-R2FR-mu-extra-zero-and-Hilbert-mass-flux-lock-or-source-normalization-runner.md`
- Pure coupling drift now has a candidate mechanism. The next Newton blocker is `mu_extra=0` plus closed Hilbert mass flux.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    write_csv(outputs["P8_Y5_R2FR_4153_SOURCE_REGISTER"], source_rows())
    write_csv(outputs["P8_Y5_R2FR_4153_PARENT_ACTION_PACKET"], parent_action_packet_rows())
    write_csv(outputs["P8_Y5_R2FR_4153_VARIATION_STRESS_TEST"], variation_stress_rows())
    write_csv(outputs["P8_Y5_R2FR_4153_ADOPTION_PACKET_GATES"], adoption_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4153_NEWTON_LOCAL_GR_IMPACT"], impact_rows())
    write_csv(outputs["P8_Y5_R2FR_4153_RESIDUALS_IF_REJECTED"], residual_rows())
    write_csv(outputs["P8_Y5_R2FR_4153_DECISION_GATES"], decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4153_STATUS"], status_rows())
    write_csv(outputs["P8_Y5_R2FR_4153_NEXT_TARGET"], next_rows())
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
        "VAL4153_0_sources",
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
    add("VAL4153_1_csv_parse", "all generated CSV outputs parse and are nonempty", csv_ok, ", ".join(csv_detail))

    doc_text = read_text(DOC_PATH) if DOC_PATH.exists() else ""
    doc_tokens = [
        DECISION,
        "S_parent = (1/(2 kappa))",
        "d kappa=0",
        "dA_3=(1/(2 kappa^2))eps_g R",
        "mu_extra",
        "4154-Y5-R2FR-mu-extra-zero-and-Hilbert-mass-flux-lock-or-source-normalization-runner.md",
    ]
    add("VAL4153_2_doc_tokens", "document records parent packet, variation tests, companion equation, remaining blockers and next target", all(token in doc_text for token in doc_tokens), "tokens checked")

    packet_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4153_PARENT_ACTION_PACKET"]))
    packet_tokens = ["PRIVATE_PACKET_READY_UNSIGNED", "SAFE_IF_BOUNDARY_AND_COMPANION_GATES_PASS", "REQUIRES_MOMS1088_SIGNATURE", "MU_EXTRA_AND_Y6_STILL_OPEN"]
    add("VAL4153_3_packet", "parent action packet is explicit and unsigned", all(token in packet_text for token in packet_tokens), "packet tokens checked")

    variation_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4153_VARIATION_STRESS_TEST"]))
    variation_tokens = ["PASS_CONDITIONAL_ON_BOUNDARY_POLICY", "PASS_IF_DKAPPA_ZERO_AND_TOPOLOGICAL_TERM_METRIC_INDEPENDENT", "PASS_CONDITIONAL_COMPANION_NOT_PARENT_SIGNED", "PASS_ONLY_IF_MATTER_SIGNATURE_SIGNED", "ANTI_OVERCLAIM_PASS"]
    add("VAL4153_4_variations", "variation stress test covers A3, metric, kappa, matter, boundary, Bianchi and PPN", all(token in variation_text for token in variation_tokens), "variation tokens checked")

    adoption_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4153_ADOPTION_PACKET_GATES"]))
    adoption_tokens = ["PASS_PACKET_WRITTEN", "PASS_CONDITIONAL", "UNSIGNED", "FAIL_CURRENT_CLAIM"]
    add("VAL4153_5_adoption", "adoption gates show conditional packet but no live claim", all(token in adoption_text for token in adoption_tokens), "adoption tokens checked")

    impact_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4153_NEWTON_LOCAL_GR_IMPACT"]))
    impact_tokens = ["CLOSES_CONDITIONALLY", "PARTIAL_PROGRESS_NOT_NEWTON_PASS", "BETA_STILL_OPEN", "KAPPA_Y6_SAFE_CONDITIONAL_OTHER_Y6_OPEN", "NO_EM_CLAIM"]
    add("VAL4153_6_impact", "impact rows distinguish coupling progress from Newton, beta, Y6 and EM claims", all(token in impact_text for token in impact_tokens), "impact tokens checked")

    residual_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4153_RESIDUALS_IF_REJECTED"]))
    residual_tokens = ["RETAIN_COUPLING_DRIFT_RUNNER", "DEMOTE_TO_SCALAR_KAPPA_BRANCH", "RETAIN_MATTER_SIGNATURE_OR_FINITE_DD_INTAKE", "RETAIN_BOUNDARY_SOURCE_NORMALIZATION_ROWS"]
    add("VAL4153_7_residuals", "rejection residual rows preserve nonclaim fallback branches", all(token in residual_text for token in residual_tokens), "residual tokens checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4153_STATUS"])
    status_ok = (
        len(status) == 1
        and status[0].get("result") == DECISION
        and status[0].get("parent_action_packet_written") == "True"
        and status[0].get("A3_variation_dkappa_zero") == "True"
        and status[0].get("metric_stress_test_passed_conditionally") == "True"
        and status[0].get("kappa_companion_safe_signed") == "False"
        and status[0].get("matter_signature_signed") == "False"
        and status[0].get("boundary_policy_signed") == "False"
        and status[0].get("coupling_drift_closed_if_adopted") == "True"
        and status[0].get("mu_extra_zero_signed") == "False"
        and status[0].get("Newton_claimed") == "False"
        and status[0].get("local_gr_claimed") == "False"
    )
    add("VAL4153_8_status", "status records conditional stress-test pass, unsigned gates and no Newton/local-GR claim", status_ok, str(status))

    next_target = parse_csv(outputs["P8_Y5_R2FR_4153_NEXT_TARGET"])
    next_ok = len(next_target) == 1 and next_target[0].get("target_doc") == "4154-Y5-R2FR-mu-extra-zero-and-Hilbert-mass-flux-lock-or-source-normalization-runner.md"
    add("VAL4153_9_next", "next target attacks mu_extra zero and Hilbert mass flux", next_ok, str(next_target))

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    no_score = all(row.get("score_ready", "False") in ("False", "") for row in all_rows)
    add("VAL4153_10_no_claim", "all outputs remain nonclaim and not score-ready", no_claim and no_score, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(
            ("4153-Y5-R2FR" in item.name or "R2FR_4153" in item.name)
            for item in FORMALIZATION.rglob("*")
        )
    add("VAL4153_11_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4153_12_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4153_VALIDATION.csv"
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
