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
DOC_PATH = ROOT / "4152-Y5-R2FR-topological-zero-form-kappa-superselection-or-coupling-drift-runner.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_TOPOLOGICAL_KAPPA_ZEROFORM_4152"
CHECKPOINT_ID = "4152"
DECISION = "TOPOLOGICAL_ZEROFORM_KAPPA_CONSTANCY_THEOREM_CONSTRUCTED_PARENT_ADOPTION_UNSIGNED_DRIFT_RESIDUAL_RUNNER_READY"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4152_00_4151_doc": (
        ROOT / "4151-Y5-R2FR-EH-only-source-normalization-lock-or-measured-GM-residual.md",
        "d kappa_*=0",
        "4151 handoff naming constant kappa as the root target.",
    ),
    "SRC4152_01_4151_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4151_NEXT_TARGET.csv",
        "topological zero-form",
        "Machine-readable 4151 next-target row.",
    ),
    "SRC4152_02_4080_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_4080_KAPPA_TOPOLOGICAL_THEOREM.csv",
        "KAP4080_0_constant_kappa",
        "Recent topological kappa theorem.",
    ),
    "SRC4152_03_3047_signature": (
        SOURCE_DIR / "P8_Y5_R2FR_3047_TOPOLOGICAL_KAPPA_SIGNATURE_ATTEMPT.csv",
        "LOCAL_CONSTANCY_DERIVED_IF_SECTOR_ADOPTED",
        "Earlier topological kappa signature audit.",
    ),
    "SRC4152_04_3050_spine": (
        SOURCE_DIR / "P8_Y5_R2FR_3050_PARENT_TOPOLOGICAL_KAPPA_SPINE_CANDIDATE.csv",
        "SPINE3050_1_action",
        "Parent action spine candidate with A_3 and kappa_eff.",
    ),
    "SRC4152_05_zeroform_clause": (
        SOURCE_DIR / "P8_CONSTANT_KAPPA_TOPOLOGICAL_ZEROFORM_CLAUSE.csv",
        "K508_1_variation_A3",
        "Topological zero-form clause with A3 variation.",
    ),
    "SRC4152_06_nohom": (
        SOURCE_DIR / "P8_Y5_R2FR_4017_KAPPA_VARIATION_AND_NOHOM_THEOREM.csv",
        "KVT4017_2_noHom_derivative_zero",
        "No-Hom/source-label derivative corollary.",
    ),
    "SRC4152_07_exchange_residual": (
        SOURCE_DIR / "P8_delta_kappa_source_exchange_residual.csv",
        "BK3048_0_bianchi_exchange_definition",
        "Bianchi/source exchange residual if kappa varies.",
    ),
    "SRC4152_08_calibration": (
        SOURCE_DIR / "P8_Y5_R2FR_4084_G_KAPPA_CALIBRATION_ROWS.csv",
        "GK4084_1_kappa_ref",
        "Calibration rows for G_ref/kappa_ref, nonclaim.",
    ),
    "SRC4152_09_script": (
        SCRIPT_PATH,
        "TOPOLOGICAL_ZEROFORM_KAPPA_CONSTANCY_THEOREM_CONSTRUCTED",
        "This generator records the 4152 topological kappa attempt.",
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
        "P8_Y5_R2FR_4152_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4152_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4152_TOPOLOGICAL_ZEROFORM_THEOREM": SOURCE_DIR / "P8_Y5_R2FR_4152_TOPOLOGICAL_ZEROFORM_THEOREM.csv",
        "P8_Y5_R2FR_4152_VARIATION_AUDIT": SOURCE_DIR / "P8_Y5_R2FR_4152_VARIATION_AUDIT.csv",
        "P8_Y5_R2FR_4152_ADOPTION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4152_ADOPTION_GATES.csv",
        "P8_Y5_R2FR_4152_COUPLING_DRIFT_RESIDUAL_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4152_COUPLING_DRIFT_RESIDUAL_ROWS.csv",
        "P8_Y5_R2FR_4152_DECISION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4152_DECISION_GATES.csv",
        "P8_Y5_R2FR_4152_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4152_STATUS.csv",
        "P8_Y5_R2FR_4152_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4152_NEXT_TARGET.csv",
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


def theorem_rows() -> List[dict]:
    return [
        {
            **common(),
            "theorem_id": "TZK4152_0_parent_module",
            "statement": "topological zero-form kappa module",
            "formula": "S_kappa_top=int_M kappa_eff dA_3",
            "derivation": "Introduce a metric-independent three-form A_3 and zero-form kappa_eff in a global/topological sector.",
            "result": "PARENT_MODULE_CONSTRUCTED",
            "current_parent_signed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "TZK4152_1_A3_variation",
            "statement": "A_3 variation gives local constancy",
            "formula": "delta_A3 S_kappa_top = boundary - int_M d kappa_eff wedge delta A_3",
            "derivation": "For admissible compact or fixed-boundary variations delta A_3, the Euler equation is d kappa_eff=0 on each connected local domain.",
            "result": "DKAPPA_ZERO_EXACT_IF_SECTOR_ADOPTED",
            "current_parent_signed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "TZK4152_2_metric_variation",
            "statement": "metric stress silence condition",
            "formula": "delta_g S_kappa_top=0 and nabla_mu(1/kappa_eff)=0 after d kappa_eff=0",
            "derivation": "The topological term is metric-independent. The EH coefficient has no scalar-tensor derivative terms after the A_3 equation sets d kappa_eff=0.",
            "result": "NO_SCALAR_TENSOR_DERIVATIVE_STRESS_CONDITIONAL",
            "current_parent_signed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "TZK4152_3_kappa_variation",
            "statement": "kappa variation is a companion flux equation, not a propagating scalar",
            "formula": "delta_kappa S gives dA_3 plus EH/source normalization companion term",
            "derivation": "The companion equation fixes a four-form/integration-constant relation. It is safe only if it does not introduce a local kinetic scalar, species label, or measured-mass boundary flux.",
            "result": "COMPANION_EQUATION_SAFE_ONLY_WITH_PARENT_CLAUSES",
            "current_parent_signed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "TZK4152_4_G_map",
            "statement": "constancy transfers to Newton coupling after convention map",
            "formula": "kappa_ref=8 pi G_ref/c^4 or equivalent EH convention; d kappa_ref=0 => dG_ref=0",
            "derivation": "The zero-gradient theorem fixes drift, not the absolute numerical value. The measured value remains calibration/global data unless an extra quantization/normalization law is derived.",
            "result": "DRIFT_ZERO_NOT_NUMERICAL_G_PREDICTION",
            "current_parent_signed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def variation_audit_rows() -> List[dict]:
    return [
        {
            **common(),
            "audit_id": "VA4152_0_boundary",
            "gate": "A_3 boundary variation fixed/topological",
            "formula": "int_partialM kappa_eff delta A_3 = 0",
            "current_status": "BOUNDARY_CLAUSE_REQUIRED",
            "failure_mode": "zero-gradient proof becomes a boundary closure assumption",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "audit_id": "VA4152_1_no_metric_stress",
            "gate": "topological sector has no local metric stress",
            "formula": "delta_g int kappa_eff dA_3=0",
            "current_status": "CONDITIONAL_METRIC_INDEPENDENT",
            "failure_mode": "constant-kappa mechanism pays for itself with new T_extra/Y6 stress",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "audit_id": "VA4152_2_no_local_scalar",
            "gate": "kappa_eff has no kinetic/local scalar branch",
            "formula": "no (partial kappa)^2, no V(kappa,x), no species/range/domain kappa labels",
            "current_status": "PARENT_CLAUSE_REQUIRED",
            "failure_mode": "scalar-kappa branch reopens Gdot/R10/source-charge rows",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "audit_id": "VA4152_3_noHom",
            "gate": "no homomorphism from source/domain/memory labels into kappa sector",
            "formula": "Hom(source/domain/memory/range,K_kappa)=0",
            "current_status": "CONDITIONAL_NOHOM_COROLLARY_NOT_PARENT_SIGNED",
            "failure_mode": "partial_A kappa or partial_lambda kappa survives",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "audit_id": "VA4152_4_Bianchi",
            "gate": "no hidden Bianchi exchange",
            "formula": "q_kappa^nu=kappa_eff^-1 P_loc[T_obs^{mu nu} nabla_mu kappa_eff]=0 when d kappa_eff=0",
            "current_status": "ZERO_IF_THEOREM_ADOPTED_ELSE_RETAIN",
            "failure_mode": "delta_kappa_source exchange residual remains active",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def adoption_gate_rows() -> List[dict]:
    return [
        {
            **common(),
            "gate_id": "AG4152_0_parent_action",
            "requirement": "parent action explicitly contains or derives the A_3/kappa sector",
            "formula": "S_parent includes S_EH[kappa_eff,g]+int kappa_eff dA_3",
            "current_status": "CANDIDATE_EXISTS_NOT_ACTIVE_PARENT_SIGNED",
            "if_passes": "d kappa_eff=0 becomes a theorem of the local branch",
            "if_fails": "constant kappa remains closure-level and drift rows stay live",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "AG4152_1_same_frame_source",
            "requirement": "matter/source action is same-frame and kappa-blind except through EH coefficient",
            "formula": "partial_A kappa_eff=partial_source kappa_eff=partial_frame kappa_eff=0",
            "current_status": "REQUIRED_NOT_PARENT_SIGNED_HERE",
            "if_passes": "source-charge and frame-split coupling drift rows close conditionally",
            "if_fails": "eta_source_AB and delta_frame_source remain active",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "AG4152_2_boundary_policy",
            "requirement": "A_3 boundary term is fixed/topological and carries no measured mass flux",
            "formula": "delta A_3|_partialM=0 or boundary term cancels without source readout",
            "current_status": "BOUNDARY_POLICY_REQUIRED",
            "if_passes": "zero-gradient proof is not a hidden boundary axiom",
            "if_fails": "boundary source-normalization residual remains active",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "AG4152_3_companion_equation",
            "requirement": "kappa variation companion equation does not add local scalar stress/source current",
            "formula": "delta_kappa S fixes dA_3/global flux, not a propagating kappa mode",
            "current_status": "COMPANION_OPEN",
            "if_passes": "topological kappa is a safe parent mechanism",
            "if_fails": "scalar-kappa/Y6 stress branch remains active",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "gate_id": "AG4152_4_G_value_policy",
            "requirement": "do not claim numerical G prediction",
            "formula": "dG_ref=0 is theorem target; G_ref value remains measured/global unless separately normalized",
            "current_status": "POLICY_PASSED",
            "if_passes": "GR-like local coupling stance remains honest",
            "if_fails": "false absolute-G overclaim",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def residual_rows() -> List[dict]:
    return [
        {
            **common(),
            "residual_id": "DR4152_0_dlnGdt",
            "quantity": "dln_Geff_dt",
            "formula": "dln_Geff_dt = +/- dln_kappa_eff_dt depending on EH convention",
            "zero_condition": "d kappa_eff=0 from adopted topological sector",
            "fallback_status": "RETAIN_IF_NOT_ADOPTED",
            "score_ready": "False",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            **common(),
            "residual_id": "DR4152_1_source_charge",
            "quantity": "eta_source_AB",
            "formula": "eta_source_AB ~= Delta_AB ln kappa_eff + Delta_AB ln M_H + Delta_AB ln(1+epsilon_mu)",
            "zero_condition": "no source/material homomorphism into kappa sector plus same-frame Hilbert mass",
            "fallback_status": "RETAIN_IF_NOHOM_UNSIGNED",
            "score_ready": "False",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            **common(),
            "residual_id": "DR4152_2_range",
            "quantity": "alpha(lambda)",
            "formula": "partial_lambda kappa_eff != 0 maps to finite-range source/coupling hair",
            "zero_condition": "partial_lambda kappa_eff=0 from topological/global sector",
            "fallback_status": "RETAIN_R10_CURVE_OR_ZERO_THEOREM_REQUIRED",
            "score_ready": "False",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            **common(),
            "residual_id": "DR4152_3_exchange",
            "quantity": "delta_kappa_source",
            "formula": "delta_kappa_source=kappa_eff^-1 P_loc[T_obs^{mu nu} nabla_mu kappa_eff]",
            "zero_condition": "d kappa_eff=0 and same-frame separately conserved matter source",
            "fallback_status": "RETAIN_QLOC_EXCHANGE_ROW",
            "score_ready": "False",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            **common(),
            "residual_id": "DR4152_4_frame_domain",
            "quantity": "delta_frame_source plus domain kappa drift",
            "formula": "partial_frame kappa_eff=partial_D kappa_eff=partial_boundary kappa_eff=0",
            "zero_condition": "kappa sector is disconnected from frame/domain/boundary labels",
            "fallback_status": "RETAIN_FRAME_DOMAIN_SOURCE_NORMALIZATION_ROWS",
            "score_ready": "False",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def decision_rows() -> List[dict]:
    return [
        {
            **common(),
            "decision_id": "DEC4152_0_derivation",
            "question": "does the topological zero-form module derive d kappa=0?",
            "answer": "yes, as an exact conditional parent-action theorem",
            "decision": "TOPOLOGICAL_DKAPPA_ZERO_THEOREM_CONSTRUCTED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "DEC4152_1_live_status",
            "question": "is the module already active-parent signed in the corpus?",
            "answer": "no",
            "decision": "PARENT_ADOPTION_UNSIGNED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "DEC4152_2_best_route",
            "question": "best route after this checkpoint",
            "answer": "stress-test/adopt the topological kappa sector inside the minimal parent action, or keep coupling drift residuals",
            "decision": "NEXT_PARENT_ACTION_STRESS_TEST",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "DEC4152_3_claim_ceiling",
            "question": "can Newton/local GR be promoted from this alone?",
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
            "topological_kappa_module_constructed": "True",
            "d_kappa_zero_derived_if_adopted": "True",
            "metric_stress_silence_conditional": "True",
            "companion_equation_safe_signed": "False",
            "matter_source_blindness_signed": "False",
            "boundary_policy_signed": "False",
            "parent_adoption_signed": "False",
            "absolute_G_predicted": "False",
            "coupling_drift_residual_rows_emitted": "True",
            "Newton_claimed": "False",
            "local_gr_claimed": "False",
            "next_target": "4153-Y5-R2FR-topological-kappa-parent-action-stress-test-or-adoption-packet.md",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> List[dict]:
    return [
        {
            **common(),
            "next_id": "NEXT4152_0",
            "target_doc": "4153-Y5-R2FR-topological-kappa-parent-action-stress-test-or-adoption-packet.md",
            "target_script": "scripts/Y5_R2FR_4153_topological_kappa_parent_action_stress_test_or_adoption_packet.py",
            "objective": "insert the topological kappa module into the minimal EH/source parent action and stress-test all variations: metric, A_3, kappa, matter, boundary, Bianchi, PPN beta, and Y6 stress; either create an explicit private adoption packet or demote it to a coupling-drift residual branch",
            "success_gate": "no local scalar mode, no new metric stress, no species/frame/range/domain kappa labels, fixed/topological A_3 boundary policy, same-frame matter source, and no hidden Bianchi exchange",
            "reason": "4152 derives the d kappa=0 mechanism conditionally; the next step is to see whether it can be safely adopted into the parent action without paying for constancy elsewhere.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def write_doc(outputs: Dict[str, Path]) -> None:
    text = f"""# 4152 - Topological Zero-Form Kappa Superselection Or Coupling-Drift Runner

Timestamp UTC: `{TIMESTAMP}`  
Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`

## Purpose
4151 proved the EH-only Newton source theorem conditionally. The remaining root question is whether `kappa_*`/`G_*` can be made constant by mechanism rather than by hand.

This checkpoint takes the best current shot: a topological zero-form / three-form module.

## Constructed Mechanism
Introduce a metric-independent three-form `A_3` and a zero-form coupling `kappa_eff`:

`S_kappa_top=int_M kappa_eff dA_3`.

Varying `A_3` gives

`delta_A3 S_kappa_top = boundary - int_M d kappa_eff wedge delta A_3`.

For compact or fixed/topological boundary variations, the Euler equation is

`d kappa_eff=0`.

So yes: this is an actual mechanism whose field equation makes the coupling locally constant on connected domains.

## Why This Is Not Yet A Live Claim
The theorem is exact only if the topological sector is part of the parent action and passes the safety gates:

- `A_3` boundary variation is fixed/topological, not a measured-mass flux;
- `delta_g S_kappa_top=0`;
- the `kappa_eff` companion equation fixes a four-form/global flux, not a propagating scalar;
- matter/source labels do not map into the `kappa` sector;
- frame, range, domain, memory, and boundary labels do not act on `kappa_eff`;
- no hidden Bianchi exchange remains.

Current corpus status: candidate mechanism exists, but active parent adoption is unsigned.

## What It Would Close If Adopted
If the parent action safely adopts this module, then

`d kappa_eff=0`

and therefore, after the EH convention map,

`dG_ref=0`.

That would close the pure coupling-drift part of Y5:

- `dln_Geff_dt`;
- `partial_r ln G_eff`;
- `partial_lambda ln G_eff`;
- `partial_A ln G_eff`;
- `delta_kappa_source`.

It would not by itself close `mu_extra`, Hilbert mass-flux closure, PPN beta source stability, or Y6 extra stress.

## Failure Branch
If the module is not adopted or fails a safety gate, the residual rows stay live:

`delta_kappa_source=kappa_eff^-1 P_loc[T_obs^{{mu nu}} nabla_mu kappa_eff]`.

The finite residual branch must then retain:

- `dln_Geff_dt`;
- `eta_source_AB`;
- `alpha(lambda)`;
- `delta_frame_source`;
- domain/boundary source-normalization rows.

## Current Verdict
| Gate | Result | Meaning |
|---|---|---|
| A3 variation | DERIVED IF ADOPTED | gives `d kappa_eff=0` |
| metric stress silence | CONDITIONAL | requires metric-independent topological sector |
| companion equation | UNSIGNED | must not reintroduce local scalar/source stress |
| matter/source blindness | UNSIGNED | no species/frame/range/domain labels may enter kappa |
| absolute G value | NOT PREDICTED | drift can be zero without deriving numerical G |
| Newton/local GR | NOT CLAIMED | only the coupling-drift mechanism is handled |

## Outputs
- `{outputs["P8_Y5_R2FR_4152_SOURCE_REGISTER"]}`
- `{outputs["P8_Y5_R2FR_4152_TOPOLOGICAL_ZEROFORM_THEOREM"]}`
- `{outputs["P8_Y5_R2FR_4152_VARIATION_AUDIT"]}`
- `{outputs["P8_Y5_R2FR_4152_ADOPTION_GATES"]}`
- `{outputs["P8_Y5_R2FR_4152_COUPLING_DRIFT_RESIDUAL_ROWS"]}`
- `{outputs["P8_Y5_R2FR_4152_DECISION_GATES"]}`
- `{outputs["P8_Y5_R2FR_4152_STATUS"]}`
- `{outputs["P8_Y5_R2FR_4152_NEXT_TARGET"]}`

## Next Target
- `4153-Y5-R2FR-topological-kappa-parent-action-stress-test-or-adoption-packet.md`
- Insert this module into the minimal EH/source parent action and stress-test every variation before deciding whether it is a legitimate private parent-action adoption or must remain a residual branch.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    write_csv(outputs["P8_Y5_R2FR_4152_SOURCE_REGISTER"], source_rows())
    write_csv(outputs["P8_Y5_R2FR_4152_TOPOLOGICAL_ZEROFORM_THEOREM"], theorem_rows())
    write_csv(outputs["P8_Y5_R2FR_4152_VARIATION_AUDIT"], variation_audit_rows())
    write_csv(outputs["P8_Y5_R2FR_4152_ADOPTION_GATES"], adoption_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4152_COUPLING_DRIFT_RESIDUAL_ROWS"], residual_rows())
    write_csv(outputs["P8_Y5_R2FR_4152_DECISION_GATES"], decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4152_STATUS"], status_rows())
    write_csv(outputs["P8_Y5_R2FR_4152_NEXT_TARGET"], next_rows())
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
        "VAL4152_0_sources",
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
    add("VAL4152_1_csv_parse", "all generated CSV outputs parse and are nonempty", csv_ok, ", ".join(csv_detail))

    doc_text = read_text(DOC_PATH) if DOC_PATH.exists() else ""
    doc_tokens = [
        DECISION,
        "S_kappa_top=int_M kappa_eff dA_3",
        "d kappa_eff=0",
        "delta_kappa_source=kappa_eff^-1 P_loc",
        "4153-Y5-R2FR-topological-kappa-parent-action-stress-test-or-adoption-packet.md",
    ]
    add("VAL4152_2_doc_tokens", "document records mechanism, constancy theorem, residual branch and next target", all(token in doc_text for token in doc_tokens), "tokens checked")

    theorem_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4152_TOPOLOGICAL_ZEROFORM_THEOREM"]))
    theorem_tokens = ["PARENT_MODULE_CONSTRUCTED", "DKAPPA_ZERO_EXACT_IF_SECTOR_ADOPTED", "NO_SCALAR_TENSOR_DERIVATIVE_STRESS_CONDITIONAL", "DRIFT_ZERO_NOT_NUMERICAL_G_PREDICTION"]
    add("VAL4152_3_theorem", "topological zero-form theorem derives d kappa zero conditionally and blocks absolute-G overclaim", all(token in theorem_text for token in theorem_tokens), "theorem tokens checked")

    audit_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4152_VARIATION_AUDIT"]))
    audit_tokens = ["BOUNDARY_CLAUSE_REQUIRED", "CONDITIONAL_METRIC_INDEPENDENT", "PARENT_CLAUSE_REQUIRED", "CONDITIONAL_NOHOM_COROLLARY_NOT_PARENT_SIGNED", "ZERO_IF_THEOREM_ADOPTED_ELSE_RETAIN"]
    add("VAL4152_4_audit", "variation audit records boundary, stress, scalar, no-Hom and Bianchi gates", all(token in audit_text for token in audit_tokens), "audit tokens checked")

    adoption_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4152_ADOPTION_GATES"]))
    adoption_tokens = ["CANDIDATE_EXISTS_NOT_ACTIVE_PARENT_SIGNED", "REQUIRED_NOT_PARENT_SIGNED_HERE", "BOUNDARY_POLICY_REQUIRED", "COMPANION_OPEN", "POLICY_PASSED"]
    add("VAL4152_5_adoption", "adoption gates distinguish constructed mechanism from active parent signature", all(token in adoption_text for token in adoption_tokens), "adoption tokens checked")

    residual_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4152_COUPLING_DRIFT_RESIDUAL_ROWS"]))
    residual_tokens = ["dln_Geff_dt", "eta_source_AB", "alpha(lambda)", "delta_kappa_source", "delta_frame_source"]
    add("VAL4152_6_residuals", "coupling drift residual rows cover time, source, range, exchange, frame/domain branches", all(token in residual_text for token in residual_tokens), "residual tokens checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4152_STATUS"])
    status_ok = (
        len(status) == 1
        and status[0].get("result") == DECISION
        and status[0].get("topological_kappa_module_constructed") == "True"
        and status[0].get("d_kappa_zero_derived_if_adopted") == "True"
        and status[0].get("parent_adoption_signed") == "False"
        and status[0].get("absolute_G_predicted") == "False"
        and status[0].get("coupling_drift_residual_rows_emitted") == "True"
        and status[0].get("Newton_claimed") == "False"
        and status[0].get("local_gr_claimed") == "False"
    )
    add("VAL4152_7_status", "status records constructed theorem, unsigned adoption, residual rows and no Newton/local-GR claim", status_ok, str(status))

    next_target = parse_csv(outputs["P8_Y5_R2FR_4152_NEXT_TARGET"])
    next_ok = len(next_target) == 1 and next_target[0].get("target_doc") == "4153-Y5-R2FR-topological-kappa-parent-action-stress-test-or-adoption-packet.md"
    add("VAL4152_8_next", "next target stress-tests parent action adoption packet", next_ok, str(next_target))

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    no_score = all(row.get("score_ready", "False") in ("False", "") for row in all_rows)
    add("VAL4152_9_no_claim", "all outputs remain nonclaim and not score-ready", no_claim and no_score, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(
            ("4152-Y5-R2FR" in item.name or "R2FR_4152" in item.name)
            for item in FORMALIZATION.rglob("*")
        )
    add("VAL4152_10_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4152_11_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4152_VALIDATION.csv"
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
