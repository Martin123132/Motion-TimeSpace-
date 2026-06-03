from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "domain_projector_alpha3_noleak_attempt_written_topological_no_bulk_stress_partial_R11_link_required_no_Newton_or_local_GR_pass"
CLAIM_CEILING = "domain_projector_alpha3_no_leak_or_R11_link_only_no_domain_channel_pass_no_mu_extra_zero_PPN_Newton_or_local_GR_pass"
NEXT_TARGET = "473-R11-domain-projector-operator-vector-minimum-fill.md"

DOC_PATH = Path("472-domain-projector-alpha3-no-leak-or-R11-link.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_DOMAIN_ALPHA3_SOURCE_REGISTER.csv")
NOLEAK_ATTEMPT_PATH = Path("source-intake/mts_residuals/P8_DOMAIN_ALPHA3_NOLEAK_THEOREM_ATTEMPT.csv")
PREMISE_PATH = Path("source-intake/mts_residuals/P8_DOMAIN_ALPHA3_PREMISE_OWNERSHIP.csv")
R11_LINK_PATH = Path("source-intake/mts_residuals/P8_DOMAIN_ALPHA3_R11_LINK.csv")
DOMAIN_COEFFICIENTS_PATH = Path("source-intake/mts_residuals/P8_mu_extra_domain_projector_coefficients.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_DOMAIN_ALPHA3_DECISION.csv")

SCORECARD_PATH = Path("source-intake/mts_residuals/P8_MU_EXTRA_LOCAL_BOUND_SCORECARD.csv")
REQUIRED_INPUTS_PATH = Path("source-intake/mts_residuals/P8_MU_EXTRA_SCORECARD_REQUIRED_INPUTS.csv")
ALPHA3_SKELETON_PATH = Path("source-intake/mts_residuals/P8_MU_EXTRA_ALPHA3_FILL_INPUT_SKELETON.csv")


SOURCE_REGISTER = [
    {
        "path": "143-domain-selector-variational-action-attempt.md",
        "role": "domain selector and wall-stress risks; selector not derived",
    },
    {
        "path": "207-domain-projector-action-and-Bianchi-identity.md",
        "role": "formal projector action and Bianchi accounting conditional on retaining stresses",
    },
    {
        "path": "235-projector-stress-variation-or-nohair-constraint-algebra.md",
        "role": "projector variation/stress no-cheat conditions",
    },
    {
        "path": "242-strict-local-coframe-branch-or-domain-projector-action.md",
        "role": "local branch warns domain projector is not enough without response/stress derivation",
    },
    {
        "path": "309-MTS-boundary-projector-contract-attempt.md",
        "role": "P_MTS,D projector contract with Ward-safe stress and parent gaps",
    },
    {
        "path": "347-local-GR-parent-reduction-theorem-attempt.md",
        "role": "local GR reduction requires projector stress owned/silenced and no vector hair",
    },
    {
        "path": "348-N5-projector-stress-conservation-theorem.md",
        "role": "metric-independent topological projector gives no local bulk projector stress conditionally",
    },
    {
        "path": "356-parent-action-ward-identity-and-projector-variation.md",
        "role": "parent Ward force ledger includes F_P and F_domain channels",
    },
    {
        "path": "429-Ward-Bianchi-exchange-owner-for-Poisson-source.md",
        "role": "domain/projector channels affect R5/R6/R7/R8/R11 and are retained",
    },
    {
        "path": "471-boundary-scalar-action-owner-or-domain-alpha3-no-leak.md",
        "role": "moves tied alpha3 pressure row from boundary closure to domain no-leak attempt",
    },
    {
        "path": str(SCORECARD_PATH),
        "role": "machine-readable domain_projector_mass scorecard rows",
    },
    {
        "path": str(REQUIRED_INPUTS_PATH),
        "role": "required domain coefficient and R11 inputs",
    },
    {
        "path": str(ALPHA3_SKELETON_PATH),
        "role": "domain alpha3 bound-product skeleton",
    },
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with (ROOT / path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    columns = list(rows[0].keys())
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    columns = list(rows[0].keys())
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, str]]:
    return [
        {
            "source_file": item["path"],
            "exists": str((ROOT / item["path"]).exists()),
            "role": item["role"],
        }
        for item in SOURCE_REGISTER
    ]


def domain_scorecard_rows() -> list[dict[str, str]]:
    rows = [row for row in read_csv(SCORECARD_PATH) if row["epsilon_channel"] == "domain_projector_mass"]
    if len(rows) != 5:
        raise ValueError(f"expected 5 domain scorecard rows, found {len(rows)}")
    return rows


def build_noleak_attempt() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "N0_target_projection",
            "claim": "domain alpha3 is the preferred-momentum flux/vector projection of projector/domain stress",
            "mathematical_form": "alpha3_domain = W_domain_alpha3 * epsilon_domain_flux",
            "result": "definition_pass",
            "evidence": "469 alpha3 skeleton and 468 domain scorecard row",
            "gap_if_failed": "epsilon_domain_projector is only a label, not a prediction",
            "effect_on_alpha3": "sets exact score target",
        },
        {
            "step_id": "N1_topological_projector_no_bulk_stress",
            "claim": "metric-independent topological/relative-chain P_D has no local bulk projector stress",
            "mathematical_form": "delta_g S_projector|bulk = 0 so T_projector^{mu nu}|bulk = 0",
            "result": "conditional_pass_from_348",
            "evidence": "348 proves this for metric-free wedge/chain projector, not Hodge/orthogonal projector",
            "gap_if_failed": "metric-dependent projector stress becomes physical and must be retained",
            "effect_on_alpha3": "removes bulk projector-stress contribution if parent-owned",
        },
        {
            "step_id": "N2_projector_parent_ownership",
            "claim": "the parent action derives the metric-independent topological P_D used locally",
            "mathematical_form": "S_parent -> P_D relative-chain/cohomology projector, diffeo-covariant and not external",
            "result": "fail_current_corpus",
            "evidence": "348 and 309 both state parent ownership/selection is not derived",
            "gap_if_failed": "projector can be an external filter or closure device",
            "effect_on_alpha3": "blocks theorem-level no-leak",
        },
        {
            "step_id": "N3_domain_selector_no_vector",
            "claim": "domain selection introduces no local vector, normal flow, velocity, marker, or preferred frame",
            "mathematical_form": "u_D^i = 0, D_i chi_D = 0, delta sigma_D^i = 0 in compact stationary branch",
            "result": "not_derived",
            "evidence": "143 and 356 keep S_domain/F_domain open; 429 lists covariant_domain_vector counterexample",
            "gap_if_failed": "covariant domain vector can satisfy Ward identity while producing alpha1/alpha2/alpha3/xi",
            "effect_on_alpha3": "directly blocks alpha3 pass",
        },
        {
            "step_id": "N4_local_trivial_representative",
            "claim": "compact stationary local branch has trivial/exact domain representative and no coherent FLRW/domain memory class locally",
            "mathematical_form": "[J_D]_local = 0 or P_D J_D is homogeneous scalar singlet",
            "result": "conditional_not_parent_derived",
            "evidence": "309 says exact/no-flux local relative currents are conditional; 242 selects strict local coframe branch as contract",
            "gap_if_failed": "nontrivial domain class can carry local preferred-location/anisotropy residuals",
            "effect_on_alpha3": "needed for no local domain flux",
        },
        {
            "step_id": "N5_R11_operator_silence",
            "claim": "any retained domain/projector operator coefficients vanish or are supplied in an executable R11 vector",
            "mathematical_form": "c_domain_operator_vector = 0 or R11_nonEH_operator_vector_executable.csv supplies coefficients/maps",
            "result": "missing_R11_vector",
            "evidence": "468 requires R11 vector for the domain channel",
            "gap_if_failed": "non-EH/source-normalization operators can generate preferred-frame and operator-ledger rows",
            "effect_on_alpha3": "must link to R11 before scorecard pass",
        },
        {
            "step_id": "N6_Ward_ownership_not_absence",
            "claim": "Ward/Bianchi ownership proves domain/projector flux is absent",
            "mathematical_form": "F_P^nu + F_domain^nu is owned, therefore zero",
            "result": "fail_as_shortcut",
            "evidence": "429 explicitly says Ward ownership is necessary footwork, not a knockout",
            "gap_if_failed": "owned covariant domain vector remains a valid counterexample",
            "effect_on_alpha3": "prevents fake local-GR promotion",
        },
        {
            "step_id": "N7_no_leak_verdict",
            "claim": "domain alpha3 is theorem-zero in the current corpus",
            "mathematical_form": "W_domain_alpha3 = 0 follows from N1-N6",
            "result": "fail_current_corpus",
            "evidence": "N1 is conditional, N2-N5 are missing, N6 blocks shortcut",
            "gap_if_failed": "R11/domain coefficient artifact required",
            "effect_on_alpha3": "domain alpha3 remains retained and not scoreable",
        },
    ]


def build_premise_ownership() -> list[dict[str, Any]]:
    return [
        {
            "premise_id": "P0_metric_independent_topological_projector",
            "needed_for_zero": "P_D has no local bulk metric variation",
            "current_evidence": "348 conditional theorem",
            "owner_status": "conditional_not_parent_owned",
            "blocks_claim": "true",
            "repair_route": "derive P_D from parent relative-chain/cohomology variables rather than choose a filter",
        },
        {
            "premise_id": "P1_not_Hodge_or_external_projector",
            "needed_for_zero": "projector is not metric-dependent and not inserted after solving",
            "current_evidence": "348/356 reject Hodge/orthogonal and external projectors",
            "owner_status": "policy_pass_not_positive_derivation",
            "blocks_claim": "true",
            "repair_route": "write explicit allowed projector construction",
        },
        {
            "premise_id": "P2_domain_selector_no_vector",
            "needed_for_zero": "domain selector carries no preferred local vector/frame/normal flow",
            "current_evidence": "143 selector not derived; 429 covariant_domain_vector counterexample",
            "owner_status": "not_derived",
            "blocks_claim": "true",
            "repair_route": "derive stationary scalar domain selector or retain vector coefficient",
        },
        {
            "premise_id": "P3_local_trivial_representative",
            "needed_for_zero": "local compact branch has exact/trivial domain class and no coherent active domain memory",
            "current_evidence": "309 exact/no-flux local currents are conditional",
            "owner_status": "conditional",
            "blocks_claim": "true",
            "repair_route": "prove local representative theorem from parent action",
        },
        {
            "premise_id": "P4_Bianchi_stress_retained",
            "needed_for_zero": "all projector/domain/boundary stresses are varied, retained, or theorem-zero",
            "current_evidence": "207/235/356 insist no dropped stress",
            "owner_status": "structural_policy_only",
            "blocks_claim": "true",
            "repair_route": "supply stress ledger or zero theorem for every retained term",
        },
        {
            "premise_id": "P5_R11_operator_vector",
            "needed_for_zero": "retained operator/domain coefficients are executable and zero/bounded",
            "current_evidence": "468 required R11_nonEH_operator_vector_executable.csv for domain",
            "owner_status": "missing",
            "blocks_claim": "true",
            "repair_route": "build R11 domain operator vector minimum artifact",
        },
    ]


def build_r11_link() -> list[dict[str, Any]]:
    return [
        {
            "link_id": "L0_alpha1_vector",
            "domain_row": "R5_alpha1",
            "observable": "alpha1",
            "required_artifact": "P8_mu_extra_domain_projector_coefficients.csv;R11_nonEH_operator_vector_executable.csv",
            "coefficient_needed": "W_domain_alpha1 * epsilon_domain_vector",
            "acceptance": "numeric/theorem-zero vector coefficient; no local domain frame",
            "current_status": "missing",
        },
        {
            "link_id": "L1_alpha2_vector",
            "domain_row": "R6_alpha2",
            "observable": "alpha2",
            "required_artifact": "P8_mu_extra_domain_projector_coefficients.csv;R11_nonEH_operator_vector_executable.csv",
            "coefficient_needed": "W_domain_alpha2 * epsilon_domain_vector",
            "acceptance": "numeric/theorem-zero vector coefficient; no local domain frame",
            "current_status": "missing",
        },
        {
            "link_id": "L2_alpha3_flux",
            "domain_row": "R7_alpha3",
            "observable": "alpha3",
            "required_artifact": "P8_mu_extra_domain_projector_coefficients.csv;R11_nonEH_operator_vector_executable.csv",
            "coefficient_needed": "W_domain_alpha3 * epsilon_domain_flux",
            "acceptance": "abs(product) <= 4e-20 or theorem-zero no-leak",
            "current_status": "missing_highest_pressure",
        },
        {
            "link_id": "L3_xi_anisotropy",
            "domain_row": "R8_xi",
            "observable": "xi",
            "required_artifact": "P8_mu_extra_domain_projector_coefficients.csv;R11_nonEH_operator_vector_executable.csv",
            "coefficient_needed": "W_domain_xi * epsilon_domain_anisotropy",
            "acceptance": "numeric/theorem-zero anisotropy coefficient",
            "current_status": "missing",
        },
        {
            "link_id": "L4_R11_operator",
            "domain_row": "R11_EH_operator_ledger",
            "observable": "non_EH_operator_coefficients",
            "required_artifact": "R11_nonEH_operator_vector_executable.csv",
            "coefficient_needed": "c_source_normalization_operator[domain_projector_mass]",
            "acceptance": "operator row has source path, units, normalization, weak-field map, and no MISSING fields",
            "current_status": "missing",
        },
    ]


def build_domain_coefficients() -> list[dict[str, Any]]:
    return [
        {
            "channel": "domain_projector_mass",
            "target_row": "R5_alpha1",
            "observable": "alpha1",
            "coefficient_symbol": "W_domain_alpha1_epsilon_domain_vector",
            "map": "alpha1_domain = W_domain_alpha1 * epsilon_domain_vector",
            "value_or_theorem": "MISSING_NUMERIC_OR_DERIVED_ZERO",
            "premise_status": "domain_selector_no_vector_not_derived",
            "target_bound": "source-locked row bound from scorecard",
            "score_status": "not_scoreable",
            "valid_for_claim": "false",
            "source": str(DOC_PATH),
        },
        {
            "channel": "domain_projector_mass",
            "target_row": "R6_alpha2",
            "observable": "alpha2",
            "coefficient_symbol": "W_domain_alpha2_epsilon_domain_vector",
            "map": "alpha2_domain = W_domain_alpha2 * epsilon_domain_vector",
            "value_or_theorem": "MISSING_NUMERIC_OR_DERIVED_ZERO",
            "premise_status": "domain_selector_no_vector_not_derived",
            "target_bound": "source-locked row bound from scorecard",
            "score_status": "not_scoreable",
            "valid_for_claim": "false",
            "source": str(DOC_PATH),
        },
        {
            "channel": "domain_projector_mass",
            "target_row": "R7_alpha3",
            "observable": "alpha3",
            "coefficient_symbol": "W_domain_alpha3_epsilon_domain_flux",
            "map": "alpha3_domain = W_domain_alpha3 * epsilon_domain_flux",
            "value_or_theorem": "0_IF_PARENT_OWNS_TOPOLOGICAL_PROJECTOR_AND_NO_SELECTOR_VECTOR_AND_R11_SILENCE_ELSE_MISSING_NUMERIC_PRODUCT",
            "premise_status": "partial_no_bulk_stress_theorem_R11_and_selector_gaps_open",
            "target_bound": "4e-20 dimensionless",
            "score_status": "conditional_not_scoreable",
            "valid_for_claim": "false",
            "source": str(DOC_PATH),
        },
        {
            "channel": "domain_projector_mass",
            "target_row": "R8_xi",
            "observable": "xi",
            "coefficient_symbol": "W_domain_xi_epsilon_domain_anisotropy",
            "map": "xi_domain = W_domain_xi * epsilon_domain_anisotropy",
            "value_or_theorem": "MISSING_NUMERIC_OR_DERIVED_ZERO",
            "premise_status": "domain_anisotropy_not_derived_zero",
            "target_bound": "source-locked row bound from scorecard",
            "score_status": "not_scoreable",
            "valid_for_claim": "false",
            "source": str(DOC_PATH),
        },
        {
            "channel": "domain_projector_mass",
            "target_row": "R11_EH_operator_ledger",
            "observable": "non_EH_operator_coefficients",
            "coefficient_symbol": "c_domain_source_normalization_operator",
            "map": "R11 includes domain_projector_mass operator coefficients and weak-field maps",
            "value_or_theorem": "MISSING_R11_OPERATOR_VECTOR_OR_DERIVED_EH_ONLY_ZERO",
            "premise_status": "R11_link_required",
            "target_bound": "operator-vector executable, no scalar bound",
            "score_status": "not_scoreable",
            "valid_for_claim": "false",
            "source": str(DOC_PATH),
        },
    ]


def build_decision() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D0_partial_theorem",
            "status": "conditional_pass",
            "meaning": "metric-independent topological projector has no local bulk projector stress if parent-owned",
            "next_action": "do not confuse no-bulk-stress with full domain alpha3 no-leak",
        },
        {
            "decision_id": "D1_domain_alpha3",
            "status": "not_derived",
            "meaning": "selector/vector/local representative/R11 gaps can still generate preferred-frame flux",
            "next_action": "keep domain alpha3 not scoreable",
        },
        {
            "decision_id": "D2_R11_link",
            "status": "required",
            "meaning": "domain_projector_mass touches R5/R6/R7/R8/R11, so R11 operator vector is mandatory unless a stronger theorem-zero is derived",
            "next_action": NEXT_TARGET,
        },
        {
            "decision_id": "D3_mu_extra_status",
            "status": "not_promoted",
            "meaning": "boundary alpha3 is closure-only and domain alpha3 is open",
            "next_action": "no total alpha3 score or local-GR claim",
        },
        {
            "decision_id": "D4_claim_ceiling",
            "status": "enforced",
            "meaning": "no domain channel, mu_extra zero, PPN, Newton, or local-GR pass",
            "next_action": "continue with R11 minimum vector",
        },
    ]


def build_doc(run_dir: Path) -> str:
    source_rows = read_csv(SOURCE_REGISTER_PATH)
    domain_rows = domain_scorecard_rows()
    noleak_rows = read_csv(NOLEAK_ATTEMPT_PATH)
    premise_rows = read_csv(PREMISE_PATH)
    r11_rows = read_csv(R11_LINK_PATH)
    coefficient_rows = read_csv(DOMAIN_COEFFICIENTS_PATH)
    decision_rows = read_csv(DECISION_PATH)
    return f"""# 472 - Domain Projector `alpha3` No-Leak Or R11 Link

Private local-GR/Newton/PPN source-normalization checkpoint. This is not a public PPN pass, Newtonian-limit pass, local-GR derivation, measured-GM derivation, cosmology result, EM result, or unified-field claim.

## 1. Purpose

Checkpoint `471` left the tied highest-pressure row open on the domain side:

```text
domain_projector_mass -> R7_alpha3 <= 4e-20.
```

This checkpoint asks:

```text
Can the domain/projector contribution to alpha3 be theorem-zero,
or must it be linked to the R11 executable operator vector?
```

Short answer:

```text
Partial theorem yes: metric-independent topological projector gives no local bulk projector stress.
Full alpha3 no-leak no: selector/vector/R11 gaps remain.
```

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/domain_projector_alpha3_no_leak_or_R11_link.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{md_table(source_rows)}

## 4. Domain Scorecard Rows

{md_table(domain_rows)}

The domain channel is not just `alpha3`; it touches:

```text
R5 alpha1,
R6 alpha2,
R7 alpha3,
R8 xi,
R11 operator ledger.
```

That is why a scalar alpha3-only argument cannot close the channel.

## 5. No-Leak Attempt

{md_table(noleak_rows)}

The useful partial theorem is:

```text
metric-independent topological/relative-chain P_D
  -> delta_g S_projector|bulk = 0
  -> T_projector|bulk = 0.
```

But alpha3 also cares about:

```text
domain selector vector,
domain representative,
normal momentum flux,
and retained non-EH/source-normalization operator coefficients.
```

Those are not currently parent-zeroed.

## 6. Premise Ownership

{md_table(premise_rows)}

The domain no-leak theorem would need:

```text
P_D parent-owned as metric-independent topological data,
no Hodge/external projector,
no domain selector vector or preferred frame,
local trivial/exact representative,
all projector/domain stresses varied or theorem-zero,
and R11 operator coefficients zero or executable.
```

Current corpus:

```text
not enough for a theorem-level alpha3 pass.
```

## 7. R11 Link

{md_table(r11_rows)}

Domain coefficient artifact:

{md_table(coefficient_rows)}

The highest-pressure executable condition remains:

```text
abs(W_domain_alpha3 epsilon_domain_flux) <= 4e-20
```

or a theorem-zero that closes the selector/vector/R11 gaps.

## 8. Decision

{md_table(decision_rows)}

Plain-English status:

```text
The projector stress problem has a good partial route.
The domain alpha3 problem is bigger: it needs no domain vector and R11 silence.
So the domain row is not dead, but it is not passed.
```

Boxing-score version:

```text
We slipped one jab: no bulk stress if P_D is topological.
But the opponent still has a right hand: selector/vector leakage plus R11.
```

## 9. Claim Ceiling

Allowed:

```text
If P_D is parent-owned, metric-independent, and topological, local bulk projector stress is zero.
```

Allowed:

```text
Domain alpha3 still requires no selector vector, local trivial representative, and R11 operator silence or executable coefficients.
```

Forbidden:

```text
MTS parent-derives domain alpha3 = 0.
```

Forbidden:

```text
MTS passes PPN alpha3, mu_extra zero, Newton, or local GR.
```

## 10. Next Queue

| Rank | Target | Why |
| ---: | --- | --- |
| 1 | `473-R11-domain-projector-operator-vector-minimum-fill.md` | domain channel cannot score while R11/operator vector is missing |
| 2 | `474-domain-selector-no-vector-theorem-or-coefficient.md` | alpha3 no-leak needs no local selector vector/domain frame |
| 3 | `475-alpha3-bound-product-evaluator.md` | only useful after boundary/domain theorem premises or numeric products exist |
"""


def write_run(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-domain-projector-alpha3-no-leak-or-R11-link"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    write_csv(SOURCE_REGISTER_PATH, source_register_rows())
    write_csv(NOLEAK_ATTEMPT_PATH, build_noleak_attempt())
    write_csv(PREMISE_PATH, build_premise_ownership())
    write_csv(R11_LINK_PATH, build_r11_link())
    write_csv(DOMAIN_COEFFICIENTS_PATH, build_domain_coefficients())
    write_csv(DECISION_PATH, build_decision())

    for path in [
        SOURCE_REGISTER_PATH,
        NOLEAK_ATTEMPT_PATH,
        PREMISE_PATH,
        R11_LINK_PATH,
        DOMAIN_COEFFICIENTS_PATH,
        DECISION_PATH,
    ]:
        write_csv(Path(results_dir.relative_to(ROOT)) / path.name.lower(), read_csv(path))

    (ROOT / DOC_PATH).write_text(build_doc(run_dir), encoding="utf-8")

    source_rows = read_csv(SOURCE_REGISTER_PATH)
    noleak_rows = read_csv(NOLEAK_ATTEMPT_PATH)
    premise_rows = read_csv(PREMISE_PATH)
    r11_rows = read_csv(R11_LINK_PATH)
    coefficient_rows = read_csv(DOMAIN_COEFFICIENTS_PATH)
    decision_rows = read_csv(DECISION_PATH)
    status = {
        "timestamp": timestamp,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "noleak_attempt": str(ROOT / NOLEAK_ATTEMPT_PATH),
        "premise_ownership": str(ROOT / PREMISE_PATH),
        "R11_link": str(ROOT / R11_LINK_PATH),
        "domain_coefficients": str(ROOT / DOMAIN_COEFFICIENTS_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "source_rows": len(source_rows),
        "source_paths_missing": sum(1 for row in source_rows if row["exists"] != "True"),
        "domain_scorecard_rows_loaded": len(domain_scorecard_rows()),
        "noleak_attempt_rows": len(noleak_rows),
        "premise_rows": len(premise_rows),
        "R11_link_rows": len(r11_rows),
        "domain_coefficient_rows": len(coefficient_rows),
        "decision_rows": len(decision_rows),
        "topological_projector_no_bulk_stress_partial": True,
        "domain_projector_parent_owned": False,
        "domain_selector_no_vector_derived": False,
        "R11_domain_vector_supplied": False,
        "domain_alpha3_score_ready": False,
        "domain_alpha3_promoted": False,
        "domain_channel_promoted": False,
        "mu_extra_zero_promoted": False,
        "Newtonian_reduction_promoted": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    return status


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()
    print(json.dumps(write_run(args.timestamp), indent=2))


if __name__ == "__main__":
    main()
