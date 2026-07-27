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

CHECKPOINT = "4262"
CLAIM_ID = "L-103"
BRANCH = "MTS_R2FR_Y5_VISIBLE_EM_READOUT_GUARD_OR_CHARGE_NORMALIZATION_BOUND_4262"
DECISION = "CALIBRATED_QBASIC_VISIBLE_CONSTANTS_KILL_EM_READOUT_COUPLING_LEAKS_IN_4210_BRANCH_DEFORMATION_BOUND_FORK_RETAINED_NONCLAIM"
MARKER = "PPC4161_VISIBLE_EM_READOUT_GUARD_OR_CHARGE_NORMALIZATION_BOUND_4262"
PACKET_MARKER = "PPC4161_PACKET_VISIBLE_EM_READOUT_GUARD_OR_CHARGE_NORMALIZATION_BOUND_4262"
NEXT_TARGET = "4263-Y5-R2FR-Dq-EM-closed-collar-adoption-or-radiative-boundary-row.md"

FORMAL_PATH = FORMAL / "278-PPC4161-visible-EM-readout-guard-or-charge-normalization-bound.md"
DOC_PATH = POST / "4262-Y5-R2FR-visible-EM-readout-guard-or-charge-normalization-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4262_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4262_00_4209_doc": SourceSpec(
        "SRC4262_00_4209_doc",
        FORMAL / "225-PPC4161-Maxwell-normalization-charge-current-owner.md",
        "b_alpha = D_X ln alpha_eff",
        "4209 charge/current normalization and alpha residual identity.",
    ),
    "SRC4262_01_4209_identities": SourceSpec(
        "SRC4262_01_4209_identities",
        SOURCE_DIR / "P8_Y5_R2FR_4209_NORMALIZATION_IDENTITIES.csv",
        "NI4209_4_vertical_residual",
        "Machine-readable b_alpha residual law.",
    ),
    "SRC4262_02_4209_contract": SourceSpec(
        "SRC4262_02_4209_contract",
        SOURCE_DIR / "P8_Y5_R2FR_4209_OWNER_CONTRACT.csv",
        "OC4209_6_visible_EM_import",
        "Machine-readable calibrated visible EM baseline allowance.",
    ),
    "SRC4262_03_4210_doc": SourceSpec(
        "SRC4262_03_4210_doc",
        FORMAL / "226-PPC4161-standard-visible-matter-import-contract.md",
        "calibrated/q-basic visible-sector readout constants",
        "4210 standard visible matter import and q-basic theta_obs clause.",
    ),
    "SRC4262_04_4210_csv": SourceSpec(
        "SRC4262_04_4210_csv",
        SOURCE_DIR / "P8_Y5_R2FR_4210_VISIBLE_MATTER_IMPORT_CONTRACT.csv",
        "VMI4210_2_constants",
        "Machine-readable q-basic calibrated constants clause.",
    ),
    "SRC4262_05_4218_doc": SourceSpec(
        "SRC4262_05_4218_doc",
        FORMAL / "234-PPC4161-visible-EM-material-curl-zero-or-residual-bound.md",
        "charge/current normalization and material labels are calibrated q-basic constants",
        "4218 visible EM/material residual zero theorem condition.",
    ),
    "SRC4262_06_4261_formal": SourceSpec(
        "SRC4262_06_4261_formal",
        FORMAL / "277-PPC4161-visible-EM-action-domain-fork-or-constitutive-bound.md",
        "readout-regenerated Hodge/alpha response",
        "4261 makes readout/coupling the next live EM leak.",
    ),
    "SRC4262_07_variation_before_readout": SourceSpec(
        "SRC4262_07_variation_before_readout",
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1816_VARIATION_BEFORE_READOUT_THEOREM.csv",
        "functional derivative is taken before readout maps",
        "Generic variation-before-readout theorem.",
    ),
    "SRC4262_08_readout_commutator": SourceSpec(
        "SRC4262_08_readout_commutator",
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1898_READOUT_VARIATION_COMMUTATOR_ZERO_ATTEMPT.csv",
        "pure postprocessing lemma",
        "Readout/variation commutator zero under pure postprocessing premise.",
    ),
    "SRC4262_09_conditional_readout": SourceSpec(
        "SRC4262_09_conditional_readout",
        SOURCE_DIR / "P8_Y5_READOUT_EREADOUT_CERTIFICATE_2637_CONDITIONAL_READOUT_LEMMA.csv",
        "CRL2637_1_no_source",
        "Conditional readout no-source lemma.",
    ),
    "SRC4262_10_4259_vector": SourceSpec(
        "SRC4262_10_4259_vector",
        SOURCE_DIR / "P8_Y5_R2FR_4259_EM_VISIBLE_RESIDUAL_VECTOR.csv",
        "R_balpha",
        "Current EM residual vector to reduce branchwise.",
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
            "4262 closes the EM readout/coupling leak only inside the 4210 calibrated q-basic visible-sector "
            "branch: if theta_obs, alpha_EM, charges, lambda_A, g_J, masses, clocks and material labels are "
            "fixed before variation and readout is pure postprocessing, then C_Hodge_readout, C_JQ, b_alpha, "
            "dlnlambda and material-marker derivatives vanish by branch typing. If any of those quantities "
            "enter the parent action, an effective action, or a source-current slot, the residual bound fork "
            "reopens. No alpha_EM or charge-scale prediction is claimed."
        ),
        "current_evidence": (
            "4262 source register, readout/coupling branch theorem, EM residual branch reduction, standard-branch "
            "Dq_EM candidate, deformation bound template, decision and firewall."
        ),
        "status": "private_calibrated_qbasic_EM_readout_coupling_silence_branch_nonclaim",
        "next_test": "Decide whether the closed-collar EM branch can be adopted into the Dq_EM component row, or fill the radiative/boundary flux row.",
        "key_risk": "Turning calibrated q-basic visible constants into a fake derivation of alpha_EM, charge normalization, or source coupling.",
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


def theorem_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "RCT4262_0_typed_constants",
            "q-basic calibrated visible constants",
            "In the 4210 branch theta_obs, alpha_EM, charge labels, masses, clocks and material labels are fixed action parameters before variation.",
            "BRANCH_PREMISE_SIGNED_FOR_4210",
            "D_X theta_obs = 0 in the calibrated branch; values are imported, not predicted.",
        ),
        (
            "RCT4262_1_alpha_ratio_silence",
            "EM alpha residual silence",
            "With lambda_A and g_J fixed before variation, b_alpha = D_X ln(g_J^2/lambda_A) = 0 branchwise.",
            "CONDITIONAL_ZERO_IN_CALIBRATED_BRANCH",
            "Does not determine the numerical alpha_EM value.",
        ),
        (
            "RCT4262_2_current_normalization_silence",
            "charge-current normalization silence",
            "If J_Q is defined by variation of the same visible matter action and charges are fixed representation/calibration labels, no source-only C_JQ slot exists.",
            "CONDITIONAL_ZERO_IN_CALIBRATED_BRANCH",
            "If a source-current multiplier enters before variation, it is a real residual.",
        ),
        (
            "RCT4262_3_readout_commutator_silence",
            "readout/variation commutator silence",
            "A pure postprocessing readout R_post:Sol(S_vis)->Obs cannot alter the Hilbert/Noether source or regenerate a Hodge/alpha coefficient.",
            "PURE_POSTPROCESSING_READOUT_SILENT_IF_TYPED",
            "Fails for effective actions, source-worldtube projectors, or readout maps with coefficient codomain.",
        ),
        (
            "RCT4262_4_hodge_readout_silence",
            "C_Hodge_readout branch silence",
            "If spectroscopy/clock/readout is absent from S_parent and S_eff before variation, C_Hodge_readout=0 in the standard branch.",
            "CONDITIONAL_ZERO_IN_CALIBRATED_BRANCH",
            "Loops/EFT/readout feedback must be bounded if introduced.",
        ),
        (
            "RCT4262_5_deformation_bound",
            "deformation branch no-cancellation law",
            "Any pre-variation EM scale/current/readout deformation is retained as abs(C_JQ)+abs(b_alpha)+abs(dlnlambda)+abs(C_Hodge_readout)+abs(b_marker)+abs(w_EM)+abs(C_XF2).",
            "RETAINED_BOUND_FORK",
            "No cancellation and no calibration-after-the-fact.",
        ),
    ]
    return [
        {
            **common(),
            "theorem_id": theorem_id,
            "name": name,
            "statement": statement,
            "status": status,
            "guard": guard,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for theorem_id, name, statement, status, guard in raw
    ]


def residual_reduction_rows() -> List[Dict[str, str]]:
    raw = [
        ("R_w_EM", "delta_w_EM", "0_by_4210_no_MTS_visible_deformation", "MISSING_SOURCE_BACKED_BOUND_IF_DEFORMED", "independent Maxwell stress/source multiplier"),
        ("R_XF2", "C_XF2", "0_by_4210_no_hidden_F2_operator", "MISSING_SOURCE_BACKED_BOUND_IF_DEFORMED", "hidden MTS coupling to F2 or F wedge F"),
        ("R_JQ", "C_JQ", "0_if_JQ_from_same_visible_action_and_charges_fixed_before_variation", "MISSING_CURRENT_OWNER_BOUND_IF_DEFORMED", "charge/current normalization source slot"),
        ("R_balpha", "b_alpha", "0_if_DX_lngJ_equals_0_and_DX_lnlambdaA_equals_0_in_calibrated_branch", "MISSING_ALPHA_SCALE_BOUND_IF_DEFORMED", "vertical drift of effective alpha"),
        ("R_dlambda", "dlnlambda_derivative", "0_if_lambda_A_fixed_before_variation", "MISSING_KINETIC_NORM_BOUND_IF_DEFORMED", "derivative interaction from varying Maxwell kinetic normalization"),
        ("R_marker", "b_A/b_marker", "0_if_theta_obs_material_labels_qbasic_before_variation", "MISSING_MARKER_BOUND_IF_DEFORMED", "material/clock/EM constants fail to descend q-basicly"),
        ("R_Hodge_readout", "C_Hodge_readout", "0_if_readout_is_pure_postprocessing_no_action_or_EFT_slot", "MISSING_READOUT_COMMUTATOR_BOUND_IF_DEFORMED", "readout regenerates effective Hodge or alpha response"),
        ("R_internal_exchange", "Delta_internal_exchange", "0_if_single_visible_action_owns_matter_EM_exchange", "MISSING_EXCHANGE_BOUND_IF_DEFORMED", "matter-EM exchange not owned by one visible action"),
        ("R_cPoynt_extra", "c_Poynt_extra", "0_if_Poynting_counted_once_through_Hilbert_stress", "MISSING_POYNTING_BOUND_IF_DEFORMED", "standalone Poynting source double count"),
        ("R_rad_Poynting", "Delta_rad_Poynting", "closed_collar_or_boundary_route_required_not_closed_by_4262", "MISSING_RADIATIVE_BOUNDARY_FLUX_ROW", "open radiative EM/Poynting flux through collar"),
        ("R_orientation_flux", "Delta_orientation_flux", "fixed_orientation_required_not_closed_by_4262", "MISSING_ORIENTATION_BOUNDARY_ROW", "orientation/time-orientation/boundary sign mismatch"),
    ]
    return [
        {
            **common(),
            "residual_id": residual_id,
            "coefficient": coefficient,
            "standard_import_branch_status": standard_status,
            "deformation_branch_requirement": deformation_requirement,
            "meaning": meaning,
            "feeds": "epsilon_EM_or_Delta_Hodge_EM",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for residual_id, coefficient, standard_status, deformation_requirement, meaning in raw
    ]


def dq_em_standard_branch_candidate_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "component": "Dq_EM",
            "candidate_value": "0",
            "candidate_status": "STANDARD_VISIBLE_IMPORT_CLOSED_COLLAR_CANDIDATE_ONLY",
            "required_conditions": (
                "4210 standard visible import; DeltaS_MTS_visible=0 before variation; theta_obs q-basic/calibrated; "
                "lambda_A and g_J fixed before variation; pure postprocessing readout; no source-current slot; "
                "single visible Hilbert source; Poynting once-only; closed EM collar or radiative flux boundary row."
            ),
            "not_copied_to_live_4254_reason": (
                "4262 closes readout/coupling leaks but leaves closed-collar radiative flux and orientation/boundary adoption "
                "as an explicit 4263 gate."
            ),
            "live_4254_action": "NO_OVERWRITE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def deformation_bound_template_rows() -> List[Dict[str, str]]:
    residuals = [
        ("C_JQ", "source-current multiplier or charge normalization drift", "Lorentz_force;source_charge;WEP;EM_stress_scale"),
        ("b_alpha", "D_X ln(g_J^2/lambda_A)", "clock;WEP;R10;alpha_drift;binding_energy"),
        ("dlnlambda_derivative", "derivative coupling from varying Maxwell kinetic normalization", "dispersion;current_leak;Poynting_anomaly"),
        ("C_Hodge_readout", "readout/spectroscopy loop regenerates Hodge or alpha response", "clock;R10;WEP;binding_response"),
        ("b_A/b_marker", "material/clock/EM constants fail q-basic descent", "composition;clock;spectroscopy;WEP"),
        ("delta_w_EM", "independent Maxwell stress/source multiplier", "WEP;clock;source_normalization"),
        ("C_XF2", "hidden MTS F2 or F wedge F operator", "alpha_EM;clock;WEP;R10;PPN"),
    ]
    rows = []
    for coefficient, definition, observable_links in residuals:
        rows.append(
            {
                **common(),
                "candidate_id": "DEFORMATION_BRANCH_TEMPLATE_ONLY",
                "coefficient": coefficient,
                "definition": definition,
                "observable_links": observable_links,
                "required_value": "MISSING_SOURCE_BACKED_NONNEGATIVE_BOUND_OR_THEOREM_ZERO",
                "units": "dimensionless_or_normalized_to_local_source_window",
                "source_path": "MISSING_DEFORMATION_BOUND_SOURCE_PATH",
                "zero_proof_path": "MISSING_ZERO_PROOF_PATH_IF_ZERO",
                "valid_for_claim": "False",
            }
        )
    rows.append(
        {
            **common(),
            "candidate_id": "DEFORMATION_BRANCH_TEMPLATE_ONLY",
            "coefficient": "epsilon_EM_readout_coupling_total",
            "definition": "sum_abs of all visible EM readout/coupling deformation coefficients",
            "observable_links": "clock;WEP;R10;PPN;EM_binding;source_normalization",
            "required_value": "SUM_ABS_NO_CANCELLATION",
            "units": "dimensionless_or_normalized_to_local_source_window",
            "source_path": str(FORMAL_PATH),
            "zero_proof_path": "ALL_SUBCOMPONENTS_ZERO_OR_BOUNDED",
            "valid_for_claim": "False",
        }
    )
    return rows


def decision_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "DEC4262_0_branch_closure",
            "The coupling/readout leak is closed only for the calibrated q-basic 4210 branch.",
            "This applies the exact postprocessing-readout theorem to the EM constants instead of merely listing them as missing.",
            NEXT_TARGET,
        ),
        (
            "DEC4262_1_no_alpha_claim",
            "No alpha_EM, charge scale, G_N, source mass, or QED derivation is claimed.",
            "GR itself imports matter constants; this local-GR branch may do the same without pretending to predict them.",
            "Keep parent scale-law search separate from local-GR safety.",
        ),
        (
            "DEC4262_2_deformation_tax",
            "If MTS predicts or deforms EM couplings, it must pay the bound tax term-by-term.",
            "A pre-variation coefficient is physics, not harmless readout.",
            "Fill source-backed bounds or prove the coefficient zero.",
        ),
        (
            "DEC4262_3_next_gate",
            "The remaining adoption gate for Dq_EM is closed-collar radiation/orientation handling.",
            "4262 makes a standard-branch Dq_EM candidate but does not overwrite the live 4254 row.",
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
        ("FW4262_0_alpha_fake", "using calibrated alpha_EM as if MTS derived its numerical value", "PARENT_SCALE_LAW_REQUIRED"),
        ("FW4262_1_charge_fake", "using fixed charge labels as if absolute charge/current normalization were derived", "CHARGE_CURRENT_OWNER_REQUIRED"),
        ("FW4262_2_readout_reentry", "letting readout, spectroscopy, clock or EFT maps enter before variation without a residual row", "READOUT_COMMUTATOR_BOUND_REQUIRED"),
        ("FW4262_3_after_fit_zero", "setting b_alpha or C_JQ to zero after fitting rather than before variation by branch typing", "PREVARIATION_BRANCH_DECLARATION_REQUIRED"),
        ("FW4262_4_boundary_skip", "adopting Dq_EM=0 without closed-collar radiative flux and orientation handling", "4263_BOUNDARY_GATE_REQUIRED"),
        ("FW4262_5_cancellation", "letting coupling/readout residuals cancel against each other", "SUM_ABS_NO_CANCELLATION_REQUIRED"),
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
            "status_id": "STATUS4262_0",
            "summary": (
                "4262 specializes the generic variation-before-readout theorem to EM: calibrated q-basic visible constants "
                "make C_Hodge_readout, C_JQ, b_alpha, dlnlambda and marker derivatives silent in the 4210 local branch, "
                "while any predictive/deformed EM coupling remains a retained bound problem."
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
                "Decide whether the 4262 standard-branch Dq_EM candidate can be adopted into the live component row by "
                "signing closed-collar radiative Poynting and orientation/boundary flux, or else fill a finite boundary bound."
            ),
            "avoid": "Do not overwrite live 4254 Dq_EM until the boundary/orientation gate is signed or bounded.",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""
# 278 - PPC4161 visible EM readout guard or charge-normalization bound

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Private nonclaim

4262 does not derive global electromagnetism, QED, `alpha_EM`, absolute charge normalization, source masses, `G_N`, PPN, R10, clock safety, or public local GR.

It does something narrower and useful: it applies the readout-before/after-variation discipline directly to the visible EM coupling leak.

## Branch theorem

In the 4210 standard visible branch:

```text
theta_obs = {{m_A, charges, alpha_EM, hbar, c, material labels}}
```

is fixed before variation as calibrated/q-basic visible-sector data.

The local EM source normalization identity is:

```text
alpha_eff proportional to g_J^2/lambda_A,
b_alpha = D_X ln alpha_eff
        = 2 D_X ln g_J - D_X ln lambda_A.
```

If `g_J`, `lambda_A`, charges, material labels, clocks and spectroscopy labels are fixed before variation, then:

```text
D_X theta_obs = 0,
D_X ln g_J = 0,
D_X ln lambda_A = 0,
b_alpha = 0,
C_JQ = 0,
dlnlambda_derivative = 0,
b_A/b_marker = 0.
```

If readout is pure postprocessing:

```text
R_post: Sol(S_vis_standard) -> Obs
```

with no argument slot in `S_parent` or `S_eff`, then:

```text
[delta_parent, R_post] source_coefficients = 0,
C_Hodge_readout = 0.
```

This is branch typing, not fitted cancellation.

## Deformation tax

If any of these enter before variation:

```text
g_J(Phi),
lambda_A(Phi),
alpha_EM(Phi),
charge/current multiplier C_JQ,
material marker b_A,
readout-regenerated Hodge/alpha map,
S_eff[R_read],
```

then they are physical residuals:

```text
epsilon_EM_readout_coupling_total
= |C_JQ|
 + |b_alpha|
 + |dlnlambda_derivative|
 + |C_Hodge_readout|
 + |b_A/b_marker|
 + |delta_w_EM|
 + |C_XF2|.
```

No cancellation is allowed.

## What is not claimed

This still does not predict:

```text
alpha_EM,
mu0,
Z_Q,
g_J,
lambda_A,
absolute charge scale,
G_N,
source masses.
```

It only says that the calibrated branch is locally safe from hidden EM readout/coupling leakage.

## Dq_EM status

4262 writes a standard-branch candidate:

```text
Dq_EM = 0
```

but does not copy it into the live 4254 component row. The live adoption gate still needs:

```text
closed-collar radiative Poynting flux,
fixed orientation/time-orientation boundary convention,
or a finite boundary flux bound.
```

## Next target

`{NEXT_TARGET}` should decide whether the standard-branch `Dq_EM` candidate is adoptable, or whether a radiative/boundary row must be filled.
"""


def checkpoint_doc() -> str:
    return f"""
# 4262 - Y5 R2FR visible EM readout guard or charge-normalization bound

Packet marker: `{PACKET_MARKER}`

## Result

4262 applies the variation-before-readout theorem to EM coupling:

```text
calibrated/q-basic visible constants before variation
=> b_alpha = C_JQ = dlnlambda = b_marker = C_Hodge_readout = 0
```

inside the 4210 standard visible branch.

If MTS makes those quantities parent-field-dependent, the deformation bound fork reopens.

## Claim status

Private nonclaim. This is local-branch safety, not a prediction of `alpha_EM` or charge scale.
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    theorems = csv_rows(paths["theorems"])
    residuals = csv_rows(paths["residuals"])
    dq_candidate = csv_rows(paths["dq_candidate"])
    template = csv_rows(paths["template"])
    rows = [
        ("VAL4262_0_sources_exist", all(row["exists"] == "True" for row in sources), "all source paths exist"),
        ("VAL4262_1_needles_found", all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL4262_2_branch_constants_theorem",
            any(row["theorem_id"] == "RCT4262_0_typed_constants" for row in theorems),
            "q-basic calibrated constants theorem emitted",
        ),
        (
            "VAL4262_3_alpha_current_readout_zero",
            all(
                any(row["coefficient"] == coeff and row["standard_import_branch_status"].startswith("0_") for row in residuals)
                for coeff in ["b_alpha", "C_JQ", "C_Hodge_readout", "dlnlambda_derivative", "b_A/b_marker"]
            ),
            "alpha/current/readout coupling leaks branch-zeroed under premises",
        ),
        (
            "VAL4262_4_boundary_not_silently_closed",
            any(row["coefficient"] == "Delta_rad_Poynting" and "not_closed_by_4262" in row["standard_import_branch_status"] for row in residuals)
            and any(row["coefficient"] == "Delta_orientation_flux" and "not_closed_by_4262" in row["standard_import_branch_status"] for row in residuals),
            "radiative/orientation boundary gate remains explicit",
        ),
        (
            "VAL4262_5_dq_candidate_not_live",
            bool(dq_candidate)
            and dq_candidate[0]["candidate_value"] == "0"
            and dq_candidate[0]["live_4254_action"] == "NO_OVERWRITE",
            "Dq_EM standard branch candidate emitted but not copied live",
        ),
        (
            "VAL4262_6_template_nonclaim",
            bool(template) and all(row["valid_for_claim"] == "False" for row in template),
            "deformation template stays nonclaim",
        ),
        (
            "VAL4262_7_no_public_claim",
            all(row["valid_for_claim"] == "False" for row in theorems + residuals + dq_candidate + template),
            "all generated rows remain private nonclaim",
        ),
        ("VAL4262_8_claim_row", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claim register row added"),
        ("VAL4262_9_formal_doc", MARKER in read_text(FORMAL_PATH), "formal marker present"),
        ("VAL4262_10_checkpoint_doc", PACKET_MARKER in read_text(DOC_PATH), "checkpoint marker present"),
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
    source_path = SOURCE_DIR / "P8_Y5_R2FR_4262_SOURCE_REGISTER.csv"
    theorem_path = SOURCE_DIR / "P8_Y5_R2FR_4262_READOUT_COUPLING_BRANCH_THEOREM.csv"
    residual_path = SOURCE_DIR / "P8_Y5_R2FR_4262_EM_COUPLING_RESIDUAL_REDUCTION.csv"
    dq_candidate_path = SOURCE_DIR / "P8_Y5_R2FR_4262_DQ_EM_STANDARD_BRANCH_CANDIDATE.csv"
    template_path = SOURCE_DIR / "P8_Y5_R2FR_4262_DEFORMATION_BOUND_TEMPLATE.csv"
    decision_path = SOURCE_DIR / "P8_Y5_R2FR_4262_DECISION.csv"
    firewall_path = SOURCE_DIR / "P8_Y5_R2FR_4262_CLAIM_FIREWALL.csv"
    status_path = SOURCE_DIR / "P8_Y5_R2FR_4262_STATUS.csv"
    next_path = SOURCE_DIR / "P8_Y5_R2FR_4262_NEXT_TARGET.csv"

    write_csv(source_path, source_rows())
    write_csv(theorem_path, theorem_rows())
    write_csv(residual_path, residual_reduction_rows())
    write_csv(dq_candidate_path, dq_em_standard_branch_candidate_rows())
    write_csv(template_path, deformation_bound_template_rows())
    write_csv(decision_path, decision_rows())
    write_csv(firewall_path, firewall_rows())
    write_csv(status_path, status_rows())
    write_csv(next_path, next_target_rows())
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    append_claim()

    paths = {
        "sources": source_path,
        "theorems": theorem_path,
        "residuals": residual_path,
        "dq_candidate": dq_candidate_path,
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
