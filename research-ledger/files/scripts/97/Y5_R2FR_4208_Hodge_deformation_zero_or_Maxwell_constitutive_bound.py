from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
SCRIPT_PATH = Path(__file__).resolve()

CHECKPOINT = "4208"
CLAIM_ID = "L-049"
BRANCH_ID = "MTS_R2FR_Y5_HODGE_DEFORMATION_GATE_4208"
DECISION = (
    "HODGE_DEFORMATION_ZERO_ROUTE_IMPORTED_CONSTITUTIVE_COUNTERMODEL_RETAINED_"
    "DELTA_HODGE_BOUND_LAW_WRITTEN_ACTION_DOMAIN_AND_CHARGE_SCALE_UNSIGNED_NONCLAIM"
)
FORMAL_PATH = FORMAL / "224-PPC4161-Hodge-deformation-zero-or-constitutive-bound.md"
DOC_PATH = POST / "4208-Y5-R2FR-MTS-Hodge-deformation-zero-or-Maxwell-constitutive-bound.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_MARKER = "PPC4161_HODGE_DEFORMATION_GATE_4208"
PACKET_MARKER = "PPC4161_PACKET_HODGE_DEFORMATION_GATE_4208"
NEXT_TARGET = "4209-Y5-R2FR-Maxwell-normalization-charge-current-owner-or-alpha-bound.md"

SOURCES = {
    "SRC4208_00_4207_decision": (
        SOURCE_DIR / "P8_Y5_R2FR_4207_DECISION.csv",
        "Hodge_deformation_gates_retained",
        "4207 handoff retaining Hodge deformation gates.",
    ),
    "SRC4208_01_223_formal": (
        FORMAL / "223-PPC4161-EM-Poynting-Hodge-source-owner-lock.md",
        "Delta_Hodge_EM",
        "Current formal Poynting/Hodge owner lock.",
    ),
    "SRC4208_02_190_selector": (
        FORMAL / "190-PPC4161-parent-action-selector-or-local-branch-quarantine.md",
        "Maxwell-Hodge/Poynting stress ownership;",
        "Local selector requires Maxwell-Hodge/Poynting source ownership.",
    ),
    "SRC4208_03_3503_owner": (
        SOURCE_DIR / "P8_Y5_R2FR_3503_OBSERVED_HODGE_MAXWELL_OWNER_THEOREM.csv",
        "EXACT_CONDITIONAL_IF_OBSERVED_HODGE_PARENT_OWNED",
        "Observed Hodge/Maxwell owner theorem.",
    ),
    "SRC4208_04_3504_uniqueness": (
        SOURCE_DIR / "P8_Y5_R2FR_3504_HODGE_UNIQUENESS_THEOREM.csv",
        "MATHEMATICAL_UNIQUENESS_LEMMA",
        "Hodge uniqueness and constitutive countermodel.",
    ),
    "SRC4208_05_3613_bound": (
        SOURCE_DIR / "P8_Y5_R2FR_3613_DELTA_HODGE_BOUND_LAW.csv",
        "Delta_Hodge_EM := *_EM - *_obs[e_obs(q)] or chi_EM - chi(g_obs)",
        "Delta-Hodge bound law.",
    ),
    "SRC4208_06_3862_zero": (
        SOURCE_DIR / "P8_Y5_R2FR_3862_EM_HODGE_ZERO_THEOREM.csv",
        "EXACT_CONDITIONAL_DELTA_HODGE_ZERO_THEOREM",
        "Strict EM Hodge zero theorem and caveats.",
    ),
    "SRC4208_07_flow_bound": (
        SOURCE_DIR / "P8_EM_Hodge_flow_rule_bound_or_zero.csv",
        "Delta_chi_principal",
        "Component bound vector for Hodge flow residuals.",
    ),
    "SRC4208_08_current_bound": (
        SOURCE_DIR / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv",
        "EMB3503_2_C_XF2",
        "Maxwell/Hodge/current owner bound vector.",
    ),
    "SRC4208_09_4175_variation": (
        SOURCE_DIR / "P8_Y5_R2FR_4175_MAXWELL_HODGE_ACTION_VARIATION.csv",
        "MH4175_2_Hilbert_stress",
        "Maxwell-Hodge action variation source rows.",
    ),
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def common() -> Dict[str, str]:
    return {"timestamp_utc": now(), "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_rows() -> List[Dict[str, str]]:
    rows = []
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


def zero_contract_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "HZ4208_0_observed_coframe",
            "e_obs and orientation descend through q",
            "g_obs=eta_ab e_obs^a e_obs^b and vol_obs are q-owned before EM variation",
            "needed_for_unique_Hodge_star",
            "conditional_from_3504",
        ),
        (
            "HZ4208_1_Hodge_uniqueness",
            "observed metric plus orientation fix *_obs",
            "alpha wedge *_obs beta = <alpha,beta>_g_obs vol_obs",
            "mathematical_lemma_not_parent_adoption",
            "derived_mathematical",
        ),
        (
            "HZ4208_2_visible_EM_action_domain",
            "EM action uses only F wedge *_obs F",
            "S_EM=-(4 mu0)^-1 int F wedge *_obs F, no independent chi_EM/background medium",
            "main_parent_action_domain_exclusion",
            "unsigned_current_corpus",
        ),
        (
            "HZ4208_3_constitutive_absence",
            "no independent principal/skewon/hidden/readout constitutive tensor",
            "chi_EM = chi(g_obs) after removing scale/topological pieces",
            "kills_Delta_Hodge_EM",
            "unsigned_current_corpus",
        ),
        (
            "HZ4208_4_axion_guard",
            "constant axion/topological term is separated; gradients are active",
            "theta_EM F wedge F is harmless only if d theta_EM=0 or boundary-routed",
            "prevents_topological_overclaim",
            "retained_gate",
        ),
        (
            "HZ4208_5_charge_scale_gate",
            "Z_Q, mu0, charge/current normalization and alpha_EM are separate scale owners",
            "4D Hodge on two-forms is conformally invariant, so light-cone/Hodge matching does not fix source scale",
            "prevents_fake_EM_unification",
            "next_target",
        ),
        (
            "HZ4208_6_readout_before_variation",
            "no post-solution readout map may regenerate Hodge/alpha dependence with theorem-zero credit",
            "readout Hodge tails become C_Hodge_readout or b_alpha rows",
            "protects_clock_spectroscopy_WEP",
            "retained_gate",
        ),
    ]
    return [
        {
            **common(),
            "contract_id": contract_id,
            "clause": clause,
            "formal_statement": formal_statement,
            "role": role,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for contract_id, clause, formal_statement, role, status in rows
    ]


def constitutive_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "CD4208_0_total",
            "Delta_Hodge_EM",
            "Delta_Hodge_EM := *_EM - *_obs[e_obs(q)] or chi_EM - chi(g_obs)",
            "aggregate Hodge/constitutive mismatch",
            "bound_or_zero_target",
        ),
        (
            "CD4208_1_principal",
            "Delta_chi_principal",
            "reciprocal principal part of chi_EM not reconstructed from g_obs",
            "changes light cone, anisotropy, birefringence, effective EM metric",
            "retained_component",
        ),
        (
            "CD4208_2_skewon",
            "Delta_chi_skewon",
            "skewon/nonreciprocal/dissipative constitutive component",
            "changes polarization, dispersion, Poynting loss and action conservation",
            "retained_component",
        ),
        (
            "CD4208_3_axion_gradient",
            "L*dtheta_EM",
            "gradient of theta_EM F wedge F term",
            "constant topological term separated; gradient acts as effective current/polarization rotation",
            "retained_component",
        ),
        (
            "CD4208_4_hidden_disformal",
            "C_Hodge_hidden",
            "hidden/motion/time field defines g_EM != g_obs or a medium-like Hodge star",
            "preferred-frame, clock and PPN side-channel",
            "retained_component",
        ),
        (
            "CD4208_5_readout",
            "C_Hodge_readout",
            "readout/spectroscopy/loop map regenerates effective EM Hodge or alpha response",
            "clock, WEP, binding-response side-channel",
            "retained_component",
        ),
        (
            "CD4208_6_conformal_scale",
            "Delta_conformal_scale",
            "EM cone/Hodge agrees but clock/source/charge scale remains unowned",
            "separate normalization and coupling gate",
            "retained_scale_gate",
        ),
        (
            "CD4208_7_orientation_flux",
            "Delta_orientation_flux",
            "orientation/time-orientation/boundary sign differs between EM flux and source charge",
            "Poynting sign and boundary charge convention hazard",
            "retained_component",
        ),
    ]
    return [
        {
            **common(),
            "component_id": component_id,
            "coefficient": coefficient,
            "definition": definition,
            "physical_effect": physical_effect,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for component_id, coefficient, definition, physical_effect, status in rows
    ]


def bound_law_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "BL4208_0_envelope",
            "Delta_Hodge_EM_envelope",
            "||Delta_Hodge_EM|| <= ||Delta_chi_principal|| + ||Delta_chi_skewon|| + L||dtheta_EM|| + |C_Hodge_hidden| + |C_Hodge_readout| + |Delta_orientation_flux|",
            "no-cancellation component envelope for the constitutive residual",
            "MISSING_NUMERIC_COMPONENTS",
        ),
        (
            "BL4208_1_observable_score",
            "score_i",
            "score_i^Hodge = |W_i^Hodge| ||Delta_Hodge_EM|| / tau_i <= 1",
            "generic arena comparator for light-cone, clocks, WEP, PPN, Poynting and source-charge rows",
            "SCHEMA_ONLY",
        ),
        (
            "BL4208_2_stress_perturbation",
            "Delta_T_EM",
            "||Delta T_EM|| <= C_F ||F||^2 ||Delta_Hodge_EM||",
            "maps constitutive mismatch into source stress/Hilbert mass error",
            "SYMBOLIC_BOUND",
        ),
        (
            "BL4208_3_current_perturbation",
            "Delta_J_eff",
            "d(Delta chi . F) acts as effective current unless parent-zero or bounded",
            "protects Maxwell equations and Lorentz-force exchange",
            "SYMBOLIC_BOUND",
        ),
        (
            "BL4208_4_scale_separation",
            "Z_Q/w_EM/alpha_EM",
            "conformal Hodge agreement does not score charge-current/source scale",
            "routes scale to 4209 instead of counting it as Delta_Hodge_EM zero",
            "SEPARATE_GATE",
        ),
    ]
    return [
        {
            **common(),
            "bound_id": bound_id,
            "quantity": quantity,
            "formula": formula,
            "meaning": meaning,
            "current_status": current_status,
            "numeric_value": "MISSING",
            "source_path": "MISSING_PARENT_OR_NUMERIC_INPUT",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for bound_id, quantity, formula, meaning, current_status in rows
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "Hodge_uniqueness_lemma_imported": "True",
            "conditional_Delta_Hodge_zero_route": "True",
            "visible_EM_action_domain_parent_signed": "False",
            "independent_constitutive_countermodel_retained": "True",
            "Delta_Hodge_bound_law_written": "True",
            "charge_current_scale_owned": "False",
            "global_parent_adoption": "False",
            "public_local_GR_claim": "False",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def claim_firewall_rows() -> List[Dict[str, str]]:
    rows = [
        ("FW4208_0_no_Hodge_equals_EM_claim", "Hodge uniqueness does not prove the parent EM action actually uses *_obs."),
        ("FW4208_1_no_constitutive_smuggle", "Gauge covariance permits independent chi_EM unless parent action-domain exclusion forbids it."),
        ("FW4208_2_no_conformal_overclaim", "In 4D, matching the Hodge star on two-forms does not fix clocks, charge normalization, source mass or G_N."),
        ("FW4208_3_no_EM_unification_claim", "This does not derive QED, charge quantization, alpha_EM, or the numerical EM coupling."),
        ("FW4208_4_no_cancellation_credit", "Constitutive components use an absolute envelope; no cancellation between unknown terms counts as evidence."),
        ("FW4208_5_no_public_local_GR", "The route is private-selector and bound-schema only until parent action-domain and scale gates are signed."),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "rule": rule,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, rule in rows
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "summary": "4208 imports the exact conditional Hodge-zero route into the live local-GR/EM gate and makes the countermodel explicit: if the parent permits independent chi_EM or charge-current scale freedom, Delta_Hodge_EM and normalization rows remain active.",
            "local_GR_claim": "False",
            "public_claim_allowed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "why": "Even if Delta_Hodge_EM is zero, Maxwell source strength still needs Z_Q, mu0, charge/current normalization and alpha_EM ownership.",
            "route_A": "derive parent charge/current normalization and unique Maxwell kinetic scale",
            "route_B": "prove no X F^2/current multiplier survives in compact local collars",
            "route_C": "if not, fill w_EM, C_XF2, C_JQ, b_alpha and alpha_EM bound rows",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def all_rows() -> Dict[str, List[Dict[str, str]]]:
    return {
        "P8_Y5_R2FR_4208_SOURCE_REGISTER.csv": source_rows(),
        "P8_Y5_R2FR_4208_HODGE_ZERO_CONTRACT.csv": zero_contract_rows(),
        "P8_Y5_R2FR_4208_CONSTITUTIVE_DECOMPOSITION.csv": constitutive_rows(),
        "P8_Y5_R2FR_4208_BOUND_LAW.csv": bound_law_rows(),
        "P8_Y5_R2FR_4208_DECISION.csv": decision_rows(),
        "P8_Y5_R2FR_4208_CLAIM_FIREWALL.csv": claim_firewall_rows(),
        "P8_Y5_R2FR_4208_STATUS.csv": status_rows(),
        "P8_Y5_R2FR_4208_NEXT_TARGET.csv": next_target_rows(),
    }


def write_docs() -> None:
    formal = f"""# 224 - PPC4161 Hodge Deformation Zero Or Constitutive Bound

Marker: `{SPINE_MARKER}`
Checkpoint: `{CHECKPOINT}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint imports the Hodge-zero theorem into the live 4207 EM/Poynting gate, but retains the independent constitutive countermodel.

## Exact Zero Route

Once the observed coframe, metric and orientation are fixed:

```text
g_obs = eta_ab e_obs^a e_obs^b,
alpha wedge *_obs beta = <alpha,beta>_g_obs vol_obs.
```

So the Hodge star is mathematically unique. Therefore:

```text
Delta_Hodge_EM = 0
```

if the parent-visible EM action uses only:

```text
S_EM = -(4 mu0)^-1 int F wedge *_obs F
```

and forbids independent `chi_EM`, hidden/disformal EM metrics, skewon/dissipative pieces, active axion gradients and readout-regenerated Hodge maps.

## Countermodel

Gauge covariance alone does not force the clean branch. A parent could instead allow:

```text
S_EM = -1/4 int F_ab chi_EM^{{abcd}} F_cd vol_obs,
chi_EM != chi(g_obs).
```

Then the residual is real:

```text
Delta_Hodge_EM := *_EM - *_obs[e_obs(q)]
              or chi_EM - chi(g_obs).
```

The no-cancellation envelope is:

```text
||Delta_Hodge_EM||
<= ||Delta_chi_principal||
 + ||Delta_chi_skewon||
 + L||d theta_EM||
 + |C_Hodge_hidden|
 + |C_Hodge_readout|
 + |Delta_orientation_flux|.
```

## Scale Guard

In four dimensions the Hodge star on two-forms is conformally invariant. So matching light cones or the Hodge star does not by itself fix:

```text
Z_Q, mu0, charge/current normalization, alpha_EM, source mass or G_N.
```

Those move to the next gate rather than being smuggled into a Hodge-zero claim.
"""
    checkpoint = f"""# 4208 - Y5 R2FR MTS Hodge Deformation Zero Or Maxwell Constitutive Bound

Decision: `{DECISION}`

4208 sharpens the EM branch:

```text
unique observed Hodge star + parent-visible Maxwell action
=> Delta_Hodge_EM = 0.
```

But the current corpus still has the countermodel:

```text
chi_EM != chi(g_obs)
```

unless the parent action-domain exclusion is signed. Therefore the constitutive bound law stays active and nonclaim.
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")
    DOC_PATH.write_text(checkpoint, encoding="utf-8")


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker not in text:
        with path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write("\n\n" + block.strip() + "\n")


def update_registers() -> None:
    claim_row = (
        f'{CLAIM_ID},em_local_gr,"The exact conditional Hodge-zero route is imported into the live local EM gate: observed coframe/metric/orientation uniquely fix *_obs, so Delta_Hodge_EM vanishes if the parent EM action uses only F wedge *_obs F; independent chi_EM/constitutive countermodels and charge-current scale gates remain active.",'
        f'"4208 source audit, Hodge zero contract, constitutive decomposition, bound law, decision row and firewall.",'
        f'private_Hodge_zero_route_nonclaim_constitutive_countermodel_retained,'
        f'"Parent-sign visible EM action-domain exclusion and Maxwell normalization/charge-current scale, or fill constitutive and alpha/charge bound rows.",'
        f'"Hodge uniqueness is mathematical; EM ownership still requires parent action-domain and scale ownership."'
    )
    if f"{CLAIM_ID}," not in read_text(CLAIMS_PATH):
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(claim_row + "\n")

    spine_block = f"""### PPC4161 Hodge Deformation Gate - 4208

Marker: `{SPINE_MARKER}`
Claim register row: `{CLAIM_ID}`

4208 imports the conditional Hodge-zero theorem:

```text
Delta_Hodge_EM = 0
```

if the parent-visible EM action uses only `F wedge *_obs F` with the observed coframe/metric/orientation and forbids independent `chi_EM`. The countermodel remains active:

```text
chi_EM != chi(g_obs)
```

so the constitutive bound envelope stays nonclaim until action-domain and charge-current scale ownership are signed."""
    append_once(SPINE_PATH, SPINE_MARKER, spine_block)

    packet_block = f"""## PPC4161 Packet Hodge Deformation Gate - 4208

Marker: `{PACKET_MARKER}`

The packet now separates the clean mathematical Hodge uniqueness lemma from the physical parent-action question. If MTS owns the visible Maxwell action domain, `Delta_Hodge_EM` closes. If not, independent constitutive coefficients must be bounded."""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)


def validate(rows_by_file: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    source = rows_by_file["P8_Y5_R2FR_4208_SOURCE_REGISTER.csv"]
    contract = rows_by_file["P8_Y5_R2FR_4208_HODGE_ZERO_CONTRACT.csv"]
    decomposition = rows_by_file["P8_Y5_R2FR_4208_CONSTITUTIVE_DECOMPOSITION.csv"]
    bound = rows_by_file["P8_Y5_R2FR_4208_BOUND_LAW.csv"]
    decision = rows_by_file["P8_Y5_R2FR_4208_DECISION.csv"]
    all_rows_flat = [row for rows in rows_by_file.values() for row in rows]
    checks = [
        ("VAL4208_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in source)),
        ("VAL4208_1_source_needles", "all source needles found", all(row["required_text_found"] == "True" for row in source)),
        ("VAL4208_2_contract_has_uniqueness", "Hodge zero contract includes observed coframe and uniqueness clauses", {"HZ4208_0_observed_coframe", "HZ4208_1_Hodge_uniqueness"}.issubset({row["contract_id"] for row in contract})),
        ("VAL4208_3_contract_has_action_domain", "contract includes visible EM action-domain exclusion", any(row["contract_id"] == "HZ4208_2_visible_EM_action_domain" and row["status"] == "unsigned_current_corpus" for row in contract)),
        ("VAL4208_4_decomposition_complete", "constitutive decomposition includes principal, skewon, axion, hidden, readout and scale gates", {"CD4208_1_principal", "CD4208_2_skewon", "CD4208_3_axion_gradient", "CD4208_4_hidden_disformal", "CD4208_5_readout", "CD4208_6_conformal_scale"}.issubset({row["component_id"] for row in decomposition})),
        ("VAL4208_5_bound_law", "bound law includes envelope and score rows", {"BL4208_0_envelope", "BL4208_1_observable_score"}.issubset({row["bound_id"] for row in bound})),
        ("VAL4208_6_missing_numeric", "bound law keeps numeric values missing/nonclaim", all(row["numeric_value"] == "MISSING" for row in bound)),
        ("VAL4208_7_decision_nonclaim", "decision keeps action domain unsigned and public claim false", decision[0]["visible_EM_action_domain_parent_signed"] == "False" and decision[0]["public_local_GR_claim"] == "False"),
        ("VAL4208_8_next_target_scale", "next target moves to Maxwell normalization/charge-current owner", "Maxwell-normalization" in decision[0]["next_target"]),
        ("VAL4208_9_no_claim_flags", "all generated claim flags remain false", all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_rows_flat)),
        ("VAL4208_10_docs_written", "formal and checkpoint docs written", FORMAL_PATH.exists() and DOC_PATH.exists()),
        ("VAL4208_11_claim_register", "claim register contains L-049", CLAIM_ID + "," in read_text(CLAIMS_PATH)),
        ("VAL4208_12_spine_marker", "spine marker present", SPINE_MARKER in read_text(SPINE_PATH)),
        ("VAL4208_13_packet_marker", "packet marker present", PACKET_MARKER in read_text(PACKET_PATH)),
    ]
    return [
        {
            **common(),
            "check_id": check_id,
            "check": check,
            "passed": str(bool(passed)),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, check, passed in checks
    ]


def write_all() -> None:
    rows_by_file = all_rows()
    write_docs()
    update_registers()
    for filename, rows in rows_by_file.items():
        write_csv(SOURCE_DIR / filename, rows)
    validation = validate(rows_by_file)
    write_csv(SOURCE_DIR / "P8_Y5_BRR545_4208_VALIDATION.csv", validation)
    if not all(row["passed"] == "True" for row in validation):
        failed = [row for row in validation if row["passed"] != "True"]
        raise RuntimeError(f"4208 validation failed: {failed}")
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    write_all()
    print(DECISION)
    print(f"formal={FORMAL_PATH}")
    print(f"checkpoint={DOC_PATH}")
    print(f"validation={SOURCE_DIR / 'P8_Y5_BRR545_4208_VALIDATION.csv'}")
    print("rows=14 validation checks")


if __name__ == "__main__":
    main()
