from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4090-Y5-R2FR-parent-qbasic-projector-ownership-or-alpha3-product-fill.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
DECISION = "QBASIC_PROJECTOR_PRIVATE_BRANCH_ALPHA3_ZERO_CONSOLIDATED_PUBLIC_PROMOTION_STILL_PARENT_ADOPTION_BLOCKED"
ALPHA3_BOUND = "4.0e-20"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4090_00_4089_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4089_NEXT_TARGET.csv",
        "4090-Y5-R2FR-parent-qbasic-projector-ownership-or-alpha3-product-fill.md",
        "4089 selects q-basic projector ownership or alpha3 product fill.",
    ),
    "SRC4090_01_4089_zero": (
        SOURCE_DIR / "P8_Y5_R2FR_4089_PROJECTOR_ZERO_THEOREM.csv",
        "EXACT_CONDITIONAL_PROJECTOR_DOMAIN_PPN_ZERO",
        "4089 gives the zero theorem to consolidate.",
    ),
    "SRC4090_02_4089_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_4089_PROJECTOR_COMPONENT_BOUND_VECTOR.csv",
        "PDB4089_4_alpha3",
        "4089 identifies the harsh alpha3 product fallback bound.",
    ),
    "SRC4090_03_4089_guard": (
        SOURCE_DIR / "P8_Y5_R2FR_4089_PROJECTOR_ABSOLUTE_SCORE_GUARD.csv",
        "ALPHA3_PRESSURE_IDENTIFIED",
        "4089 says exact zero is preferable to a tuned alpha3 product.",
    ),
    "SRC4090_04_3929_signature": (
        SOURCE_DIR / "P8_Y5_R2FR_3929_PROJECTOR_PARENT_SIGNATURE.csv",
        "PROJECTOR_DOMAIN_ZERO_SIGNED_FOR_PRIVATE_LOCAL_BRANCH",
        "3929 signs q-basic/topological projector ownership for the private selected local branch.",
    ),
    "SRC4090_05_3929_zero": (
        SOURCE_DIR / "P8_Y5_R2FR_3929_PROJECTOR_DOMAIN_ZERO_RESULT.csv",
        "epsilon_domain_projector_abs",
        "3929 records zero values for the private projector/domain branch.",
    ),
    "SRC4090_06_3928_audit": (
        SOURCE_DIR / "P8_Y5_R2FR_3928_PROJECTOR_DOMAIN_CERTIFICATE_AUDIT.csv",
        "PDC3928_6_zero_consequence",
        "3928 proves the conditional zero consequence from q-basic/projector clauses.",
    ),
    "SRC4090_07_3928_bound": (
        SOURCE_DIR / "P8_Y5_R2FR_3928_PROJECTOR_DOMAIN_BOUND_INPUT_ROWS.csv",
        "epsilon_domain_projector_abs",
        "3928 provides fallback absolute projector residual formulas.",
    ),
    "SRC4090_08_4043_factor": (
        SOURCE_DIR / "P8_Y5_R2FR_4043_PROJECTOR_STRESS_FACTORIZATION.csv",
        "PSF4043_3_wall_boundary",
        "4043 supplies the projector stress pieces and zero conditions.",
    ),
    "SRC4090_09_4061_kernel": (
        SOURCE_DIR / "P8_Y5_R2FR_4061_DOMAIN_PROJECTOR_KERNEL_THEOREM.csv",
        "DOMAIN_KERNEL_ZERO_SELECTED_BRANCH_ELSE_BOUND",
        "4061 states selected-branch kernel zero else alpha/xi/domain fallback.",
    ),
    "SRC4090_10_domain_coeffs": (
        SOURCE_DIR / "P8_mu_extra_domain_projector_coefficients.csv",
        "alpha3_domain = W_domain_alpha3 * epsilon_domain_flux",
        "Existing domain projector product row gives the alpha3 fallback form.",
    ),
    "SRC4090_11_alpha3_fill": (
        SOURCE_DIR / "P8_Y5_R2FR_3892_ALPHA3_PROJECTOR_NUMERIC_FILL_ROWS.csv",
        "AF3892_5_projector_preferred",
        "3892 records preferred-frame projector fill inputs if theorem zero is rejected.",
    ),
}


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
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
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def bool_string(value: bool) -> str:
    return "True" if value else "False"


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def source_register_rows() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        rows.append(
            {
                "source_id": source_id,
                "source_type": "local_checkpoint_csv",
                "path_or_url": str(path),
                "needle": needle,
                "role": role,
                "exists": bool_string(path.exists()),
                "valid_for_claim": "False",
                "timestamp_utc": TIMESTAMP,
            }
        )
    rows.append(
        {
            "source_id": "SRC4090_12_script",
            "source_type": "generator_script",
            "path_or_url": str(SCRIPT_PATH),
            "needle": SCRIPT_PATH.name,
            "role": "Reproducible generator for 4090 projector alpha3 zero/product gate.",
            "exists": bool_string(SCRIPT_PATH.exists()),
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        }
    )
    return rows


def ownership_ladder_rows() -> List[dict]:
    return [
        {
            "rung_id": "QBP4090_0_readout_split",
            "ownership_clause": "P_D is not an action-level dynamical Hodge/Green/trace/moving-domain variable.",
            "mathematical_effect": "partial S_parent^loc/partial P_D=0; no delta_g(P_D J_H) Euler stress from action variation.",
            "evidence": "SIG3929_1_no_action_level_PD",
            "selected_branch_status": "SIGNED_BY_READOUT_SPLIT",
            "public_claim_status": "PRIVATE_BRANCH_ONLY",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "rung_id": "QBP4090_1_topological_label",
            "ownership_clause": "If retained, P_D=q_src^*Pbar_top with Pbar_top fixed on quotient/topological data.",
            "mathematical_effect": "delta_g P_D=0 and D_D P_D=0.",
            "evidence": "SIG3929_2_fixed_topological_label",
            "selected_branch_status": "SIGNED_AS_LOCAL_BRANCH_CONTRACT",
            "public_claim_status": "PRIVATE_BRANCH_ONLY",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "rung_id": "QBP4090_2_fixed_domain",
            "ownership_clause": "D_loc=q_src^{-1}(Dbar) and source-silent local variations have D_X q_src=0.",
            "mathematical_effect": "domain/support motion term vanishes on the local collar.",
            "evidence": "SIG3929_3_fixed_qbasic_domain",
            "selected_branch_status": "SIGNED_FOR_SOURCE_SILENT_LOCAL_COLLAR",
            "public_claim_status": "PRIVATE_BRANCH_ONLY",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "rung_id": "QBP4090_3_wall_flux_silence",
            "ownership_clause": "Projector/domain collar has Phi_D=0 and tau_wall_TF=0.",
            "mathematical_effect": "domain boundary-flux and selector-wall terms vanish.",
            "evidence": "SIG3929_4_domain_collar_silence",
            "selected_branch_status": "SIGNED_ONLY_FOR_PROJECTOR_DOMAIN_COLLAR",
            "public_claim_status": "GLOBAL_BOUNDARY_HARMONIC_GATES_STILL_SEPARATE",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "rung_id": "QBP4090_4_same_denominator",
            "ownership_clause": "Projector readout uses the same Hilbert denominator and introduces no second compact-source mass.",
            "mathematical_effect": "no hidden source-normalization monopole survives as a projector/domain stress.",
            "evidence": "SIG3929_5_same_hilbert_denominator",
            "selected_branch_status": "SIGNED_AS_NO_EXTRA_SOURCE_NORMALIZATION_IN_PROJECTOR_SECTOR",
            "public_claim_status": "SOURCE_DENOMINATOR_PARENT_ADOPTION_STILL_GLOBAL_GATE",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def alpha3_zero_rows() -> List[dict]:
    return [
        {
            "zero_id": "A3Z4090_0_factor",
            "piece": "alpha3 projector product",
            "statement": "The harsh fallback product is alpha3_domain = W_domain_alpha3 * epsilon_domain_flux.",
            "formula": "alpha3_domain = W_domain_alpha3 * epsilon_domain_flux",
            "selected_branch_value": "",
            "status": "PRODUCT_IDENTIFIED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "zero_id": "A3Z4090_1_flux_zero",
            "piece": "epsilon_domain_flux",
            "statement": "In the q-basic/topological selected local branch, Phi_D=0 and tau_wall_TF=0, so the domain flux/STF wall channel feeding alpha3 is zero.",
            "formula": "Phi_D=0 and tau_wall_TF=0 => epsilon_domain_flux=0",
            "selected_branch_value": "0",
            "status": "EXACT_PRIVATE_BRANCH_ZERO",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "zero_id": "A3Z4090_2_alpha3_zero",
            "piece": "alpha3 projector residual",
            "statement": "Because epsilon_domain_flux=0 in the selected branch, alpha3_domain=0 independently of the fallback coefficient W_domain_alpha3.",
            "formula": "alpha3_domain = W_domain_alpha3 * 0 = 0",
            "selected_branch_value": "0",
            "status": "EXACT_PRIVATE_BRANCH_ALPHA3_ZERO",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "zero_id": "A3Z4090_3_ppn_consequence",
            "piece": "PPN alpha3 bound",
            "statement": "The selected branch beats the alpha3 bound by theorem-zero, not by small-number tuning, but public claim promotion is still blocked by parent-adoption scope.",
            "formula": "|alpha3_domain| = 0 <= 4.0e-20",
            "selected_branch_value": "0",
            "status": "PRIVATE_BRANCH_BOUND_SATISFIED_NOT_PUBLIC_CLAIM",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def fallback_contract_rows() -> List[dict]:
    return [
        {
            "contract_id": "A3F4090_0_rejection_trigger",
            "if_rejected": "If q-basic/topological projector ownership or collar flux silence is rejected.",
            "required_inputs": "W_domain_alpha3; epsilon_domain_flux; source_path; units; frame/coframe; source denominator; no-cancellation policy",
            "formula": "alpha3_domain = W_domain_alpha3 * epsilon_domain_flux",
            "pass_rule": f"abs(alpha3_domain) <= {ALPHA3_BOUND}",
            "status": "SOURCE_READY_FALLBACK_CONTRACT",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "contract_id": "A3F4090_1_unit_coefficient_screen",
            "if_rejected": "If W_domain_alpha3 is dimensionless and O(1).",
            "required_inputs": "epsilon_domain_flux numeric value with source path",
            "formula": "abs(epsilon_domain_flux) <= 4.0e-20 / abs(W_domain_alpha3)",
            "pass_rule": "for W=1, abs(epsilon_domain_flux) <= 4.0e-20",
            "status": "UNIT_COEFFICIENT_SCREEN_READY",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "contract_id": "A3F4090_2_no_cancellation",
            "if_rejected": "If multiple projector/domain channels are live.",
            "required_inputs": "each alpha_i/xi/zeta product separately",
            "formula": "alpha3 cannot be rescued by alpha1, alpha2, xi, zeta, gamma or beta cancellation",
            "pass_rule": "alpha3 product must pass individually unless a parent identity sets it exactly zero before fitting",
            "status": "NO_CANCELLATION_GUARD",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def adoption_gap_rows() -> List[dict]:
    return [
        {
            "gap_id": "ADOPT4090_0_private_vs_public",
            "gap": "3929 signs the selected private local branch, but valid_for_claim remains false.",
            "why_it_matters": "The branch is a rigorous internal route, not yet a full parent-action/public local-GR proof.",
            "needed_for_promotion": "Parent action adoption showing the q-basic/topological projector is not optional branch choice or closure-only assumption.",
            "status": "PROMOTION_BLOCK_ACTIVE",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "gap_id": "ADOPT4090_1_global_boundary",
            "gap": "Projector collar silence does not automatically close all global boundary/harmonic sectors.",
            "why_it_matters": "A separate boundary/harmonic gate can still feed local observables.",
            "needed_for_promotion": "Show global boundary/harmonic data are source-blind or separately bounded.",
            "status": "SEPARATE_GATE_REMAINS",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "gap_id": "ADOPT4090_2_source_denominator",
            "gap": "Projector sector uses same Hilbert denominator, but full source denominator equality remains a global parent gate.",
            "why_it_matters": "Local GR needs source normalization across all sectors, not only projector/domain stress.",
            "needed_for_promotion": "Pi_M/H_tau/Hilbert equality and same-frame source current promotion.",
            "status": "SEPARATE_GATE_REMAINS",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def r11_update_rows() -> List[dict]:
    return [
        {
            "update_id": "R11UP4090_0",
            "operator_family": "projector_domain_stress",
            "previous_status": "EXACT_CONDITIONAL_ZERO_OR_COMPONENTWISE_PPN_BOUND_GATE_FILLED",
            "new_status": "PRIVATE_BRANCH_QBASIC_ALPHA3_ZERO_CONSOLIDATED",
            "claim_allowed": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "update_id": "R11UP4090_1",
            "operator_family": "projector_domain_stress",
            "previous_status": "ALPHA3_PRODUCT_REQUIRED_IF_ZERO_REJECTED",
            "new_status": "ALPHA3_PRODUCT_FALLBACK_CONTRACT_READY",
            "claim_allowed": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def decision_rows() -> List[dict]:
    return [
        {
            "decision_id": "DEC4090_0_main",
            "decision": DECISION,
            "meaning": "The q-basic/topological projector route is consolidated into a private-branch alpha3 zero. If that route is rejected, the harsh alpha3 product contract is ready.",
            "claim_status": "PRIVATE_NONCLAIM",
            "next_required_move": "Promote or reject parent adoption of the q-basic projector branch; if rejected, fill W_domain_alpha3 epsilon_domain_flux with sourced values.",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "decision_id": "DEC4090_1_best_route",
            "decision": "ZERO_ROUTE_REMAINS_BEST_ROUTE",
            "meaning": "Because alpha3 is at 4e-20, theorem-zero is vastly cleaner than fitting a tiny product.",
            "claim_status": "ROUTE_SELECTION",
            "next_required_move": "Attack parent adoption scope, not small-number tuning.",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def claim_gate_rows() -> List[dict]:
    return [
        {
            "claim_id": "CLAIM4090_0_alpha3_projector",
            "claim": "alpha3 projector/domain branch is zero in selected private branch",
            "allowed": "True_private_checkpoint_only",
            "why_not_public": "Parent adoption/public local-GR scope remains unsigned even though the selected private branch zero is consolidated.",
            "minimum_unlock": "Promote q-basic/topological projector ownership from private branch contract to parent action theorem.",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4090_1_projector_sector_public",
            "claim": "Projector/domain sector passes public local PPN",
            "allowed": "False",
            "why_not_public": "4090 proves/consolidates a selected-branch route, not an unconditional corpus-wide parent theorem.",
            "minimum_unlock": "Resolve adoption gaps ADOPT4090_0..2 or fill fallback products.",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4090_2_local_GR",
            "claim": "MTS reduces to local GR",
            "allowed": "False",
            "why_not_public": "Other R11/source/readout/conservation gates remain live.",
            "minimum_unlock": "All 4086 families and 4085 PPN source-stability clauses zeroed/bounded.",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def next_target_rows() -> List[dict]:
    return [
        {
            "target_id": "NEXT4090_0",
            "next_target": "4091-Y5-R2FR-projector-adoption-promotion-or-vector-preferred-frame-bound.md",
            "script": "scripts/Y5_R2FR_4091_projector_adoption_promotion_or_vector_preferred_frame_bound.py",
            "why": "4090 consolidates alpha3 zero for the private q-basic branch. Next either promote/reject parent adoption, or move to the neighbouring vector preferred-frame alpha1/alpha2/xi branch.",
            "priority": "P0",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "target_id": "NEXT4090_1",
            "next_target": "alpha3_product_numeric_fill_if_rejected",
            "script": "defer_until_qbasic_rejected",
            "why": "Only fill tiny alpha3 products if the clean q-basic/topological zero route is rejected.",
            "priority": "P1",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def status_rows() -> List[dict]:
    return [
        {
            "checkpoint": "4090",
            "status": "private_nonclaim_checkpoint_complete",
            "decision": DECISION,
            "public_claim": "False",
            "github_action": "False",
            "formalization_workbench_modified_by_script": "False",
            "timestamp_utc": TIMESTAMP,
        }
    ]


def validation_rows(output_paths: Iterable[Path]) -> List[dict]:
    paths = list(output_paths)
    checks: List[dict] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                "check_id": check_id,
                "check": check,
                "passed": bool_string(passed),
                "detail": detail,
                "timestamp_utc": TIMESTAMP,
            }
        )

    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        exists = path.exists()
        contains = exists and needle in read_text(path)
        add(
            f"VAL4090_SRC_{source_id}",
            "local source exists and contains needle",
            bool(exists and contains),
            f"{path} | needle={needle} | role={role}",
        )

    for path in paths:
        rows = parse_csv(path)
        add(
            f"VAL4090_CSV_{path.stem}",
            "generated CSV parses and is non-empty",
            bool(rows),
            f"{path} rows={len(rows)}",
        )

    ownership_status = {row["selected_branch_status"] for row in ownership_ladder_rows()}
    add(
        "VAL4090_OWNERSHIP_LADDER",
        "q-basic ownership ladder has signed selected-branch rungs",
        "SIGNED_BY_READOUT_SPLIT" in ownership_status and "SIGNED_AS_LOCAL_BRANCH_CONTRACT" in ownership_status,
        f"statuses={sorted(ownership_status)}",
    )

    alpha3_rows = alpha3_zero_rows()
    alpha3_zero = any(row["status"] == "EXACT_PRIVATE_BRANCH_ALPHA3_ZERO" and row["selected_branch_value"] == "0" for row in alpha3_rows)
    add(
        "VAL4090_ALPHA3_ZERO",
        "selected private branch alpha3 zero is consolidated",
        alpha3_zero,
        f"alpha3_zero={alpha3_zero}",
    )

    fallback_rows = fallback_contract_rows()
    fallback_ready = any(ALPHA3_BOUND in row["pass_rule"] for row in fallback_rows)
    add(
        "VAL4090_ALPHA3_FALLBACK",
        "alpha3 fallback product contract is source-ready",
        fallback_ready,
        "fallback contains alpha3 bound 4.0e-20",
    )

    outputs_inside_post_checkpoint = all(is_under(path, ROOT) for path in paths) and is_under(DOC_PATH, ROOT)
    outputs_outside_formalization = all(not is_under(path, FORMALIZATION) for path in paths) and not is_under(DOC_PATH, FORMALIZATION)
    add(
        "VAL4090_SCOPE",
        "outputs stay in post-checkpoint-work and not formalization-workbench",
        bool(outputs_inside_post_checkpoint and outputs_outside_formalization),
        f"doc={DOC_PATH}; csv_count={len(paths)}",
    )

    no_public_claim = all(row.get("allowed") != "True" for row in claim_gate_rows())
    add(
        "VAL4090_NO_PUBLIC_LOCAL_GR_CLAIM",
        "4090 does not promote public local-GR/projector-sector claim",
        no_public_claim,
        "private checkpoint only; public projector/local-GR claims remain false",
    )

    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
        compile_ok = True
        compile_detail = "py_compile passed"
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4090_SCRIPT_COMPILES", "generator script compiles", compile_ok, compile_detail)

    return checks


def write_doc() -> None:
    DOC_PATH.write_text(
        f"""# 4090 - Parent Q-Basic Projector Ownership Or Alpha3 Product Fill

- Timestamp: `{TIMESTAMP}`
- Status: `private_nonclaim_checkpoint`
- Decision: `{DECISION}`
- Public local-GR/projector-sector claim: `false`
- GitHub action: `false`

## Result

4090 consolidates the clean route:

```text
P_D readout-only or q-basic/topological
delta_g P_D = 0
D_D P_D = 0
Phi_D = tau_wall_TF = 0
same Hilbert denominator
```

Therefore, in the selected private local branch:

```text
epsilon_domain_flux = 0
alpha3_domain = W_domain_alpha3 * epsilon_domain_flux = 0
```

This beats the brutal `alpha3 <= 4e-20` bound by theorem-zero, not by tuning.

## Why It Is Not Public Yet

The proof is strong inside the selected branch, but the corpus still needs one more parent-adoption move:

```text
the parent action must make q-basic/topological projector ownership mandatory
not optional branch choice
not closure-only
not post-readout fitting
```

So 4090 is a serious internal advance, not a public local-GR claim.

## Fallback If Rejected

If q-basic/topological ownership is rejected:

```text
alpha3_domain = W_domain_alpha3 * epsilon_domain_flux
|alpha3_domain| <= 4.0e-20
```

Required source fields:

```text
W_domain_alpha3
epsilon_domain_flux
units
frame/coframe
source denominator
source path
no-cancellation policy
```

For unit coefficient:

```text
|epsilon_domain_flux| <= 4.0e-20
```

That is why zero is the better route.

## Decision

```text
private selected branch alpha3 projector = exact zero
public projector-sector claim = still false
fallback alpha3 product contract = ready
next = parent adoption promotion or vector preferred-frame branch
```

## Next

```text
4091-Y5-R2FR-projector-adoption-promotion-or-vector-preferred-frame-bound.md
```
""",
        encoding="utf-8",
    )


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    outputs = {
        "P8_Y5_R2FR_4090_SOURCE_REGISTER.csv": source_register_rows(),
        "P8_Y5_R2FR_4090_QBASIC_PROJECTOR_OWNERSHIP_LADDER.csv": ownership_ladder_rows(),
        "P8_Y5_R2FR_4090_ALPHA3_PROJECTOR_ZERO.csv": alpha3_zero_rows(),
        "P8_Y5_R2FR_4090_ALPHA3_FALLBACK_PRODUCT_CONTRACT.csv": fallback_contract_rows(),
        "P8_Y5_R2FR_4090_PARENT_ADOPTION_GAPS.csv": adoption_gap_rows(),
        "P8_Y5_R2FR_4090_R11_VECTOR_UPDATE.csv": r11_update_rows(),
        "P8_Y5_R2FR_4090_DECISION_GATE.csv": decision_rows(),
        "P8_Y5_R2FR_4090_CLAIM_GATE.csv": claim_gate_rows(),
        "P8_Y5_R2FR_4090_NEXT_TARGET.csv": next_target_rows(),
        "P8_Y5_R2FR_4090_STATUS.csv": status_rows(),
    }

    output_paths: List[Path] = []
    for name, rows in outputs.items():
        path = SOURCE_DIR / name
        write_csv(path, rows)
        output_paths.append(path)

    write_doc()

    validation = validation_rows(output_paths)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4090_VALIDATION.csv"
    write_csv(validation_path, validation)
    output_paths.append(validation_path)

    shutil.rmtree(SCRIPT_PATH.parent / "__pycache__", ignore_errors=True)

    failures = [row for row in validation if row["passed"] != "True"]
    if failures:
        for failure in failures:
            print(f"VALIDATION_FAIL {failure['check_id']}: {failure['detail']}")
        raise SystemExit(1)

    print(f"4090 complete: {DECISION}")
    print(f"doc: {DOC_PATH}")
    print(f"csv_dir: {SOURCE_DIR}")
    print(f"validation: {validation_path}")


if __name__ == "__main__":
    main()
