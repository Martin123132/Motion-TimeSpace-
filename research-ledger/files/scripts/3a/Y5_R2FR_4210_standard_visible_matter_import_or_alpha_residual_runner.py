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

CHECKPOINT = "4210"
CLAIM_ID = "L-051"
BRANCH_ID = "MTS_R2FR_Y5_VISIBLE_MATTER_IMPORT_4210"
DECISION = (
    "STANDARD_VISIBLE_MATTER_IMPORT_CONTRACT_WRITTEN_LOCAL_GR_CAN_USE_CALIBRATED_MATTER_"
    "MTS_ALPHA_PREDICTION_DEFERRED_ALPHA_F2_CURRENT_RESIDUAL_RUNNER_SCHEMA_READY_NONCLAIM"
)
FORMAL_PATH = FORMAL / "226-PPC4161-standard-visible-matter-import-contract.md"
DOC_PATH = POST / "4210-Y5-R2FR-standard-visible-matter-import-contract-or-alpha-residual-bound-runner.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_MARKER = "PPC4161_STANDARD_VISIBLE_MATTER_IMPORT_4210"
PACKET_MARKER = "PPC4161_PACKET_STANDARD_VISIBLE_MATTER_IMPORT_4210"
NEXT_TARGET = "4211-Y5-R2FR-Htau-MHsource-parent-charge-owner-or-visible-matter-residual-scorecard.md"

SOURCES = {
    "SRC4210_00_4209_decision": (
        SOURCE_DIR / "P8_Y5_R2FR_4209_DECISION.csv",
        "visible_EM_calibration_allowed",
        "4209 decision allowing calibrated visible EM baseline.",
    ),
    "SRC4210_01_4209_residuals": (
        SOURCE_DIR / "P8_Y5_R2FR_4209_RESIDUAL_BOUND_ROWS.csv",
        "RB4209_3_b_alpha",
        "4209 retained alpha/current/F2 residual rows.",
    ),
    "SRC4210_02_225_formal": (
        FORMAL / "225-PPC4161-Maxwell-normalization-charge-current-owner.md",
        "standard visible EM is imported with calibrated alpha_EM",
        "4209 formal import baseline.",
    ),
    "SRC4210_03_185_source": (
        FORMAL / "185-PPC4161-Hilbert-source-measure-descent-and-delta-ZH-closure.md",
        "S_src = S_matter[psi,g_obs,theta]",
        "Hilbert source-measure descent source action.",
    ),
    "SRC4210_04_188_ppn": (
        FORMAL / "188-PPC4161-full-PPN-readout-vector.md",
        "R_PPN =",
        "Full private PPN readout vector.",
    ),
    "SRC4210_05_189_validation": (
        FORMAL / "189-PPC4161-local-empirical-validation-pack.md",
        "source-backed comparator pack",
        "Local comparator pack caveat.",
    ),
    "SRC4210_06_190_quarantine": (
        FORMAL / "190-PPC4161-parent-action-selector-or-local-branch-quarantine.md",
        "S_parent|loc =",
        "Parent selector/quarantine action form.",
    ),
    "SRC4210_07_194_Gcal": (
        FORMAL / "194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md",
        "numeric(G_cal) = empirical calibration",
        "GR-like calibrated Newton coupling precedent.",
    ),
    "SRC4210_08_191_poynting": (
        FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md",
        "S_i = -T_EM(n,e_i) = (E cross B)_i.",
        "EM/Poynting Hilbert stress owner.",
    ),
    "SRC4210_09_224_hodge": (
        FORMAL / "224-PPC4161-Hodge-deformation-zero-or-constitutive-bound.md",
        "Z_Q, mu0, charge/current normalization, alpha_EM",
        "Hodge gate scale guard.",
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


def import_contract_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "VMI4210_0_scope",
            "compact ordinary-matter local collar through <=2PN",
            "standard visible matter import applies only to local GR/Newton/PPN safety branch",
            "does_not_define_global_MTS_or_cosmology",
        ),
        (
            "VMI4210_1_action",
            "S_vis = S_matter[psi,g_obs,theta_obs] + S_Maxwell-Hodge[A,g_obs;alpha_EM_obs] + S_binding + dB_impr",
            "ordinary visible matter uses one observed metric/coframe and calibrated matter constants",
            "baseline_import_contract",
        ),
        (
            "VMI4210_2_constants",
            "theta_obs = {m_A, charges, alpha_EM, hbar, c, material labels} are calibrated/q-basic readout constants",
            "calibrated constants are not MTS predictions and must not carry hidden X/q dependence",
            "calibrated_not_predicted",
        ),
        (
            "VMI4210_3_Hilbert_source",
            "T_H = -2/sqrt(-g_obs) delta S_vis/delta g_obs",
            "all visible matter, EM, binding and improvement terms enter the same Hilbert source once",
            "source_owner_requirement",
        ),
        (
            "VMI4210_4_no_MTS_deviation",
            "Delta S_MTS-visible = 0 in the baseline branch",
            "no extra F2, current, marker, disformal, memory or Poynting source side-channel is silently added",
            "baseline_firewall",
        ),
        (
            "VMI4210_5_reactivation",
            "if MTS adds any visible-sector deformation, it becomes a retained residual row",
            "w_EM, C_XF2, C_JQ, b_alpha, b_A/b_marker, Delta_Hodge_EM, Delta_rad_Poynting reopen",
            "bound_runner_handoff",
        ),
        (
            "VMI4210_6_local_GR_status",
            "standard visible matter import is compatible with local GR reduction",
            "same methodological status as GR using calibrated matter constants and calibrated G_N",
            "methodology_lock",
        ),
    ]
    return [
        {
            **common(),
            "contract_id": contract_id,
            "clause": clause,
            "effect": effect,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for contract_id, clause, effect, status in rows
    ]


def residual_envelope_rows() -> List[Dict[str, str]]:
    rows = [
        ("ARE4210_0_wEM", "w_EM", "independent Maxwell stress multiplier", "WEP;clock;source_normalization;EM_binding", "abs(delta_w_EM)"),
        ("ARE4210_1_CXF2", "C_XF2", "hidden/motion/time field coupling to F^2 or F wedge F", "alpha_EM;clock;WEP;R10;PPN", "abs(C_XF2 * projection_XF2)"),
        ("ARE4210_2_CJQ", "C_JQ", "charge/current normalization not fixed by same parent object", "Lorentz_force;source_charge;WEP;EM_stress_scale", "abs(C_JQ * projection_JQ)"),
        ("ARE4210_3_balpha", "b_alpha", "D_X ln(g_J^2/lambda_A)", "clock;WEP;R10;alpha_EM_drift;binding_energy", "abs(b_alpha * sensitivity_alpha)"),
        ("ARE4210_4_dlambda", "dlnlambda_derivative", "derivative interaction from varying Maxwell kinetic normalization", "dispersion;current_leak;Poynting_anomaly", "abs(dlnlambda_derivative * scale_length)"),
        ("ARE4210_5_marker", "b_A/b_marker", "material, clock or EM constants do not descend through q", "composition;clock;spectroscopy;WEP", "abs(sum_A sensitivity_A b_A)"),
        ("ARE4210_6_Hodge", "Delta_Hodge_EM", "EM constitutive/Hodge mismatch", "light_cone;birefringence;Poynting;PPN", "||Delta_Hodge_EM||"),
        ("ARE4210_7_rad", "Delta_rad_Poynting", "open radiative/background EM flux through local collar", "Gdot;clock_drift;source_mass_drift", "abs(Phi_EM_rad)/(M_H c^2/time_window)"),
    ]
    return [
        {
            **common(),
            "component_id": component_id,
            "coefficient": coefficient,
            "definition": definition,
            "observable_links": observable_links,
            "absolute_component": absolute_component,
            "numeric_value": "MISSING",
            "source_path": "MISSING_PARENT_OR_NUMERIC_INPUT",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for component_id, coefficient, definition, observable_links, absolute_component in rows
    ]


def runner_schema_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "ARS4210_0_total_envelope",
            "epsilon_visible_EM_total",
            "sum_abs_components",
            "sum of ARE4210 absolute components with no cancellation credit",
            "all component values, units, source paths, sensitivity maps",
        ),
        (
            "ARS4210_1_clock",
            "delta_ln_nu_clock",
            "epsilon_visible_EM_total <= tau_clock",
            "clock/spectroscopy drift from alpha/material marker/current residuals",
            "clock sensitivities, tau_clock, units, source path",
        ),
        (
            "ARS4210_2_WEP",
            "eta_AB_EM",
            "epsilon_visible_EM_total <= tau_WEP",
            "composition-dependent EM binding/source response",
            "material pair, sensitivities, tau_WEP, source path",
        ),
        (
            "ARS4210_3_R10",
            "alpha_R10_EM(lambda)",
            "alpha_pred(lambda) <= alpha_bound(lambda)",
            "finite-range or marker-mediated EM/source response",
            "lambda, profile convention, projection factors, digitized bound curve",
        ),
        (
            "ARS4210_4_PPN",
            "delta_PPN_EM",
            "epsilon_visible_EM_total <= tau_PPN",
            "preferred-frame/source stress/readout residual from EM sector",
            "PPN projection weights and bounds",
        ),
        (
            "ARS4210_5_source_mass",
            "delta_MH_EM/M_H",
            "epsilon_visible_EM_total <= tau_source",
            "Hamiltonian source-mass drift from visible-sector side-channels",
            "M_H_ref, H_tau owner, source normalization, boundary flux",
        ),
    ]
    return [
        {
            **common(),
            "schema_id": schema_id,
            "observable": observable,
            "score_formula": score_formula,
            "purpose": purpose,
            "required_inputs": required_inputs,
            "numeric_score": "MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for schema_id, observable, score_formula, purpose, required_inputs in rows
    ]


def route_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "VR4210_0_baseline",
            "standard visible matter baseline",
            "use calibrated Standard-Model/Maxwell matter constants as q-basic readout constants",
            "recommended_for_local_GR_branch",
        ),
        (
            "VR4210_1_prediction",
            "MTS predicts alpha_EM or matter constants",
            "requires separate parent scale law/charge-current owner and is not needed for local GR reduction",
            "deferred_speculative_extension",
        ),
        (
            "VR4210_2_deviation",
            "MTS deforms visible matter",
            "score residual envelope before any claim",
            "fallback_bound_route",
        ),
        (
            "VR4210_3_forbidden",
            "use calibrated constants but present them as MTS predictions",
            "overclaim and notation laundering",
            "rejected",
        ),
    ]
    return [
        {
            **common(),
            "route_id": route_id,
            "route": route,
            "effect": effect,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for route_id, route, effect, status in rows
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "standard_visible_matter_import_contract": "True",
            "calibrated_constants_allowed": "True",
            "MTS_alpha_prediction_claim": "False",
            "visible_sector_residual_envelope_written": "True",
            "alpha_residual_runner_schema_ready": "True",
            "global_parent_adoption": "False",
            "public_local_GR_claim": "False",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def claim_firewall_rows() -> List[Dict[str, str]]:
    rows = [
        ("FW4210_0_no_alpha_prediction", "Calibrated alpha_EM and matter constants are not MTS predictions."),
        ("FW4210_1_no_hidden_MTS_visible_deformation", "Any MTS-specific F2/current/Hodge/material/radiative deformation must enter the residual envelope."),
        ("FW4210_2_no_double_source", "Visible EM/binding energy is counted once in Hilbert source stress, not again as a correction."),
        ("FW4210_3_no_public_local_GR", "The import contract supports a private local branch; it does not prove global parent adoption or public local GR."),
        ("FW4210_4_no_cancellation", "Unknown visible-sector residuals cannot cancel each other to make a pass."),
        ("FW4210_5_no_raw_empirical_claim", "Runner schema is not a raw-data pass or claim-grade empirical result until all rows are sourced."),
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
            "summary": "4210 writes the standard visible matter import contract: local GR may use calibrated visible matter constants as q-basic readout constants, while any MTS-specific alpha/F2/current/Hodge/material/radiative deviation is routed into an absolute residual envelope and bound-runner schema.",
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
            "why": "With visible matter calibrated rather than predicted, the next pressure point returns to the source charge: H_tau/M_H must be parent-owned or the residual scorecard remains only a schema.",
            "route_A": "attack H_tau/M_Hdress parent charge owner with the standard visible matter contract included",
            "route_B": "build first visible-sector residual scorecard row if source charge remains unsigned",
            "route_C": "keep alpha prediction quarantined until a parent scale law exists",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def all_rows() -> Dict[str, List[Dict[str, str]]]:
    return {
        "P8_Y5_R2FR_4210_SOURCE_REGISTER.csv": source_rows(),
        "P8_Y5_R2FR_4210_VISIBLE_MATTER_IMPORT_CONTRACT.csv": import_contract_rows(),
        "P8_Y5_R2FR_4210_ALPHA_RESIDUAL_ENVELOPE.csv": residual_envelope_rows(),
        "P8_Y5_R2FR_4210_ALPHA_RESIDUAL_RUNNER_SCHEMA.csv": runner_schema_rows(),
        "P8_Y5_R2FR_4210_ROUTE_MATRIX.csv": route_rows(),
        "P8_Y5_R2FR_4210_DECISION.csv": decision_rows(),
        "P8_Y5_R2FR_4210_CLAIM_FIREWALL.csv": claim_firewall_rows(),
        "P8_Y5_R2FR_4210_STATUS.csv": status_rows(),
        "P8_Y5_R2FR_4210_NEXT_TARGET.csv": next_target_rows(),
    }


def write_docs() -> None:
    formal = f"""# 226 - PPC4161 Standard Visible Matter Import Contract

Marker: `{SPINE_MARKER}`
Checkpoint: `{CHECKPOINT}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint separates local-GR reduction from speculative prediction of visible matter constants.

## Contract

In the compact ordinary-matter local branch, use:

```text
S_vis =
S_matter[psi,g_obs,theta_obs]
+ S_Maxwell-Hodge[A,g_obs; alpha_EM_obs]
+ S_binding[psi,A,g_obs]
+ dB_impr.
```

Here:

```text
theta_obs = {{m_A, charges, alpha_EM, hbar, c, material labels}}
```

are calibrated/q-basic visible-sector readout constants. They are not MTS predictions.

The Hilbert source is:

```text
T_H = -2/sqrt(-g_obs) delta S_vis/delta g_obs.
```

## Why This Is Legitimate

GR reduces to Newton/PPN using calibrated matter constants and calibrated `G_N`; it does not predict the electron mass, charge, or fine-structure constant. MTS local-GR reduction should meet the same structural burden:

```text
same observed metric,
same Hilbert source,
one calibrated G_N,
one calibrated visible matter sector,
no hidden MTS residuals in the local branch.
```

## Residual Envelope

Any MTS-specific visible-sector deviation reopens an explicit row:

```text
epsilon_visible_EM_total =
|delta_w_EM|
+ |C_XF2 projection_XF2|
+ |C_JQ projection_JQ|
+ |b_alpha sensitivity_alpha|
+ |dlnlambda derivative scale|
+ |sum_A sensitivity_A b_A|
+ ||Delta_Hodge_EM||
+ |Phi_EM_rad|/(M_H c^2/window).
```

No cancellation between unknown terms is allowed.

## Current Verdict

The local-GR branch can proceed with calibrated visible matter. Prediction of `alpha_EM` remains quarantined until a parent scale law exists.
"""
    checkpoint = f"""# 4210 - Y5 R2FR Standard Visible Matter Import Contract Or Alpha Residual Bound Runner

Decision: `{DECISION}`

4210 makes the visible matter route explicit:

```text
calibrated visible matter constants are allowed;
MTS alpha_EM prediction is not claimed;
MTS-specific visible-sector deviations must be bounded.
```

The residual runner schema is ready, but not claim-grade:

```text
epsilon_visible_EM_total = sum absolute visible-sector residual components.
```
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
        f'{CLAIM_ID},em_local_gr,"The standard visible matter import contract is written: local GR can use calibrated visible matter constants as q-basic readout constants while MTS alpha prediction is deferred; any MTS-specific alpha/F2/current/Hodge/material/radiative deviation is routed to an absolute residual envelope and runner schema.",'
        f'"4210 source audit, visible matter import contract, alpha residual envelope, runner schema, route matrix, decision row and firewall.",'
        f'private_visible_matter_import_nonclaim_alpha_prediction_deferred,'
        f'"Attack H_tau/M_Hdress parent source charge with visible matter contract included, or fill first visible-sector residual scorecard row.",'
        f'"This keeps the local-GR route competitive without pretending to derive Standard Model constants."'
    )
    if f"{CLAIM_ID}," not in read_text(CLAIMS_PATH):
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(claim_row + "\n")

    spine_block = f"""### PPC4161 Standard Visible Matter Import - 4210

Marker: `{SPINE_MARKER}`
Claim register row: `{CLAIM_ID}`

4210 allows the local-GR branch to import calibrated visible matter constants in the same disciplined way GR does:

```text
S_vis = S_matter + S_Maxwell-Hodge + S_binding + dB_impr.
```

MTS does not claim `alpha_EM` or Standard Model constants here. Any MTS-specific visible-sector deviation enters:

```text
epsilon_visible_EM_total = sum_abs(w_EM, C_XF2, C_JQ, b_alpha, b_A, Delta_Hodge_EM, Delta_rad_Poynting).
```"""
    append_once(SPINE_PATH, SPINE_MARKER, spine_block)

    packet_block = f"""## PPC4161 Packet Standard Visible Matter Import - 4210

Marker: `{PACKET_MARKER}`

The packet now has a clean local matter stance: calibrated visible matter is allowed; MTS-specific visible-sector deviations are bounded; alpha prediction stays quarantined."""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)


def validate(rows_by_file: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    source = rows_by_file["P8_Y5_R2FR_4210_SOURCE_REGISTER.csv"]
    contract = rows_by_file["P8_Y5_R2FR_4210_VISIBLE_MATTER_IMPORT_CONTRACT.csv"]
    envelope = rows_by_file["P8_Y5_R2FR_4210_ALPHA_RESIDUAL_ENVELOPE.csv"]
    schema = rows_by_file["P8_Y5_R2FR_4210_ALPHA_RESIDUAL_RUNNER_SCHEMA.csv"]
    routes = rows_by_file["P8_Y5_R2FR_4210_ROUTE_MATRIX.csv"]
    decision = rows_by_file["P8_Y5_R2FR_4210_DECISION.csv"]
    all_rows_flat = [row for rows in rows_by_file.values() for row in rows]
    checks = [
        ("VAL4210_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in source)),
        ("VAL4210_1_source_needles", "all source needles found", all(row["required_text_found"] == "True" for row in source)),
        ("VAL4210_2_contract_action", "visible matter action contract written", any(row["contract_id"] == "VMI4210_1_action" for row in contract)),
        ("VAL4210_3_constants_calibrated", "calibrated constants are explicitly not MTS predictions", any(row["contract_id"] == "VMI4210_2_constants" and row["status"] == "calibrated_not_predicted" for row in contract)),
        ("VAL4210_4_reactivation", "reactivation clause routes deviations to residual rows", any(row["contract_id"] == "VMI4210_5_reactivation" for row in contract)),
        ("VAL4210_5_envelope_components", "residual envelope includes F2, current, alpha, marker, Hodge and radiation components", {"C_XF2", "C_JQ", "b_alpha", "b_A/b_marker", "Delta_Hodge_EM", "Delta_rad_Poynting"}.issubset({row["coefficient"] for row in envelope})),
        ("VAL4210_6_envelope_missing", "envelope values remain missing/nonclaim", all(row["numeric_value"] == "MISSING" for row in envelope)),
        ("VAL4210_7_runner_schema", "runner schema covers clock, WEP, R10, PPN and source mass", {"delta_ln_nu_clock", "eta_AB_EM", "alpha_R10_EM(lambda)", "delta_PPN_EM", "delta_MH_EM/M_H"}.issubset({row["observable"] for row in schema})),
        ("VAL4210_8_route_matrix", "route matrix includes baseline, prediction, deviation and forbidden shortcut", {"VR4210_0_baseline", "VR4210_1_prediction", "VR4210_2_deviation", "VR4210_3_forbidden"}.issubset({row["route_id"] for row in routes})),
        ("VAL4210_9_decision_nonclaim", "decision keeps alpha prediction and public local GR false", decision[0]["MTS_alpha_prediction_claim"] == "False" and decision[0]["public_local_GR_claim"] == "False"),
        ("VAL4210_10_no_claim_flags", "all generated claim flags remain false", all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_rows_flat)),
        ("VAL4210_11_docs_written", "formal and checkpoint docs written", FORMAL_PATH.exists() and DOC_PATH.exists()),
        ("VAL4210_12_claim_register", "claim register contains L-051", CLAIM_ID + "," in read_text(CLAIMS_PATH)),
        ("VAL4210_13_spine_marker", "spine marker present", SPINE_MARKER in read_text(SPINE_PATH)),
        ("VAL4210_14_packet_marker", "packet marker present", PACKET_MARKER in read_text(PACKET_PATH)),
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
    write_csv(SOURCE_DIR / "P8_Y5_BRR545_4210_VALIDATION.csv", validation)
    if not all(row["passed"] == "True" for row in validation):
        failed = [row for row in validation if row["passed"] != "True"]
        raise RuntimeError(f"4210 validation failed: {failed}")
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    write_all()
    print(DECISION)
    print(f"formal={FORMAL_PATH}")
    print(f"checkpoint={DOC_PATH}")
    print(f"validation={SOURCE_DIR / 'P8_Y5_BRR545_4210_VALIDATION.csv'}")
    print("rows=15 validation checks")


if __name__ == "__main__":
    main()
