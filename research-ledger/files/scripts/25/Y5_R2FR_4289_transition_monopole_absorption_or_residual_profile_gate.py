from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4289"
CLAIM_ID = "L-130"
BRANCH = "MTS_R2FR_Y5_TRANSITION_MONOPOLE_ABSORPTION_OR_RESIDUAL_PROFILE_GATE_4289"
DECISION = "TRANSITION_SHELL_SPLIT_INTO_CALIBRATED_HILBERT_MONOPOLE_PLUS_RESIDUAL_VECTOR_NONCLAIM"
MARKER = "PPC4161_TRANSITION_MONOPOLE_ABSORPTION_OR_RESIDUAL_PROFILE_GATE_4289"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_MONOPOLE_ABSORPTION_OR_RESIDUAL_PROFILE_GATE_4289"
NEXT_TARGET = "4290-Y5-R2FR-transition-Hilbert-monopole-source-lock-or-first-residual-bound-row.md"

FORMAL_PATH = FORMAL / "305-PPC4161-transition-monopole-absorption-or-residual-profile-gate.md"
DOC_PATH = POST / "4289-Y5-R2FR-transition-monopole-absorption-or-residual-profile-gate.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4289_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
PI_B_COEFFICIENT = 0.167893843691
TRANSITION_PIB = 0.5000000000287336

SOURCES = {
    "SRC4289_00_4288_frontier": (
        FORMAL / "304-PPC4161-finite-margin-AJ-zero-domain-split-and-transition-frontier.md",
        "transition-shell cGamma/AJ leakage.",
        "4288 identifies the transition shell as the remaining cGamma/AJ frontier.",
    ),
    "SRC4289_01_4171_gauss_monopole": (
        FORMAL / "187-PPC4161-Poisson-Gauss-Newton-readout-from-Hamiltonian-source-charge.md",
        "For an exterior monopole/spherical source",
        "4171 gives the exterior monopole/Gauss readout from Hamiltonian source charge.",
    ),
    "SRC4289_02_4178_calibrated_coupling": (
        FORMAL / "194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md",
        "G_cal := c^4 kappa_eff/(8*pi).",
        "4178 permits one calibrated Newtonian coupling without claiming numeric G derivation.",
    ),
    "SRC4289_03_4170_worldtube": (
        FORMAL / "186-PPC4161-Hamiltonian-worldtube-mass-readout-glue.md",
        "No orbital `GM`, fitted acceleration, or measured Newton constant is used",
        "4170 supplies anti-circular Hamiltonian/worldtube mass-readout glue.",
    ),
    "SRC4289_04_4151_extra_monopole": (
        SOURCE_DIR / "P8_Y5_R2FR_4151_SOURCE_NORMALIZATION_PROOF.csv",
        "P4151_3_no_extra_monopole",
        "4151 says zero non-EH monopole is required but not parent-derived.",
    ),
    "SRC4289_05_4151_epsilon_mu": (
        SOURCE_DIR / "P8_Y5_R2FR_4151_MEASURED_GM_RESIDUAL_ROWS.csv",
        "epsilon_mu=mu_extra/(G_eff M_H)",
        "4151 defines the extra monopole residual epsilon_mu.",
    ),
    "SRC4289_06_4155_worldtube_lock": (
        SOURCE_DIR / "P8_Y5_R2FR_4155_WORLDTUBE_SOURCE_LOCK.csv",
        "M_H^dress[W;tau]=H_tau[S_outer]-H_tau[S_ref]",
        "4155 locks dressed source measure conditionally.",
    ),
    "SRC4289_07_3998_anti_backfill": (
        SOURCE_DIR / "P8_Y5_R2FR_3998_GM_ANTI_BACKFILL_CONTRACT.csv",
        "do not set M_H_ref=mu_obs/G0",
        "3998 forbids measured-GM backfill as a fake proof.",
    ),
    "SRC4289_08_4284_shell_fail": (
        FORMAL / "300-PPC4161-real-transition-shell-profile-calculator.md",
        "So the transition shell cannot be treated as a direct local metric source.",
        "4284 keeps direct transition projection failed.",
    ),
    "SRC4289_09_4286_firewall": (
        FORMAL / "302-PPC4161-transition-closure-local-sanity-and-cGamma-AJ-interface-runner.md",
        "The closure lock cannot be used as credit for them.",
        "4286 blocks closure credit for cGamma/AJ rows.",
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
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
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


def append_unique_block(path: Path, marker: str, heading: str, body: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    block = f"\n\n## {heading}\n\nMarker: `{marker}`\n\n{body}\n"
    write_text(path, text.rstrip() + block)


def append_claim() -> None:
    path = FORMAL / "02-claims-register.csv"
    text = read_text(path)
    if f"{CLAIM_ID}," in text:
        return
    row = (
        f'{CLAIM_ID},local_gr,'
        f'"4289 attempts the transition-shell parent-kernel route via a concrete monopole absorption theorem. It shows that a shell contribution which is part of the same pre-readout Hamiltonian/Hilbert worldtube monopole is not a separate local metric residual; it is absorbed into the calibrated source charge. The remaining transition danger is the residual vector: extra non-Hilbert monopole epsilon_mu, multipoles, time drift, range hair, frame/source species leakage, beta/PPN source terms, and any unsourced cGamma/AJ profile. The theorem is conditional because same-worldtube Hilbert inclusion and zero non-EH monopole are not parent-signed.",'
        f'"4289 source register, monopole theorem clauses, transition decomposition, residual vector schema, strong-window residual controls, decision and firewall.",'
        f'private_transition_monopole_absorption_split_residual_vector_nonclaim,'
        f'"Try to parent-sign the transition shell as same-worldtube Hilbert monopole with zero non-EH monopole, or source the first residual bound row for epsilon_mu, multipoles, time/range/frame hair, beta source, R_transport or R_Bgrad.",'
        f'"Using measured orbital GM to define the source, hiding non-Hilbert monopole in calibration, treating monopole absorption as full PPN, using closure credit, or ignoring multipole/range/time residuals."\n'
    )
    path.write_text(text.rstrip() + "\n" + row, encoding="utf-8")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
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


def theorem_clause_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "MTC4289_0_same_worldtube",
            "transition shell belongs to same pre-readout Hamiltonian/Hilbert worldtube source",
            "M_tr^H included in M_H^dress[W;tau] before orbital/PPN readout",
            "CONDITIONAL_NOT_PARENT_SIGNED",
            "otherwise absorption is denominator laundering",
        ),
        (
            "MTC4289_1_gauss_monopole",
            "exterior transition contribution is pure l=0 monopole",
            "Phi_tr=-G_cal M_tr^H/r plus constant in exterior leading term",
            "CONDITIONAL_THEOREM_ROUTE",
            "multipoles remain residuals",
        ),
        (
            "MTC4289_2_no_extra_nonEH_monopole",
            "mu_extra_tr=0 or epsilon_mu_tr is bounded",
            "epsilon_mu_tr=mu_extra_tr/(G_cal M_H^dress)",
            "NOT_PARENT_DERIVED",
            "extra monopole cannot be hidden inside calibration",
        ),
        (
            "MTC4289_3_anti_backfill",
            "source charge fixed before measured-GM/orbit use",
            "do not set M_H_ref=mu_obs/G0 and call it a derivation",
            "GUARD_AVAILABLE",
            "prevents circular Newton proof",
        ),
        (
            "MTC4289_4_no_second_order_hair",
            "time/range/frame/beta/source-species residuals are zero or bounded",
            "dlnM_dt, alpha(lambda), partial_r ln mu, delta_frame, delta_beta_source",
            "OPEN_RESIDUAL_VECTOR",
            "monopole absorption alone is not full local GR/PPN",
        ),
        (
            "MTC4289_5_verdict",
            "transition monopole absorption theorem",
            "same-worldtube Hilbert monopole plus zero residual vector would remove direct shell residual",
            "CONDITIONAL_NOT_PROMOTED",
            "next target is source-lock or first residual bound row",
        ),
    ]
    return [
        {
            **common(),
            "clause_id": clause_id,
            "clause": clause,
            "mathematical_form": form,
            "status": status,
            "residual_if_failed": residual,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for clause_id, clause, form, status, residual in raw
    ]


def transition_decomposition_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "TDS4289_0_same_Hilbert_monopole",
            "calibrated_Hilbert_monopole",
            "G_cal M_tr^H/r",
            "absorbed into M_H^dress if source worldtube is fixed before readout",
            "CONDITIONAL_ABSORBABLE",
        ),
        (
            "TDS4289_1_extra_monopole",
            "epsilon_mu_tr",
            "mu_extra_tr/(G_cal M_H^dress)",
            "source-normalization residual; cannot be calibrated away",
            "BOUND_OR_ZERO_REQUIRED",
        ),
        (
            "TDS4289_2_multipoles",
            "Q_l>=1_tr",
            "sum_l>=1 Q_lm/r^(l+1)",
            "anisotropic/local tidal residual, not GM calibration",
            "BOUND_OR_ZERO_REQUIRED",
        ),
        (
            "TDS4289_3_time_drift",
            "dln_Mtr_dt or dln_Geff_dt",
            "dln mu_obs/dt",
            "Gdot/clock/orbital timing residual",
            "BOUND_OR_ZERO_REQUIRED",
        ),
        (
            "TDS4289_4_range_hair",
            "alpha_tr(lambda)",
            "G_eff(r,lambda)=G_*[1+alpha(lambda) exp(-r/lambda)]",
            "R10/fifth-force residual",
            "BOUND_OR_ZERO_REQUIRED",
        ),
        (
            "TDS4289_5_frame_species",
            "delta_frame_source; eta_source_AB",
            "Delta_frame ln mu_obs; Delta_AB ln mu_obs",
            "WEP/frame/source-species residual",
            "BOUND_OR_ZERO_REQUIRED",
        ),
        (
            "TDS4289_6_beta_PPN_source",
            "delta_beta_source",
            "-1/(2N_U2)<L_00^-1 S_beta^source,U^2>",
            "second-order PPN residual after Newton monopole calibration",
            "BOUND_OR_ZERO_REQUIRED",
        ),
        (
            "TDS4289_7_cGamma_AJ_profile",
            "A_J_residual_tr",
            "|R_transport_to_local|+|R_Bgrad_to_local| after calibrated-monopole removal",
            "must satisfy 4287/4288 strong-window gate",
            "PROFILE_REQUIRED",
        ),
    ]
    return [
        {
            **common(),
            "term_id": term_id,
            "term": term,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for term_id, term, formula, meaning, status in raw
    ]


def residual_schema_rows() -> List[Dict[str, str]]:
    raw = [
        ("RS4289_0", "epsilon_mu_tr", "dimensionless", "MISSING_ZERO_THEOREM_OR_NUMERIC_BOUND", "measured-GM/source-normalization"),
        ("RS4289_1", "Q_l>=1_tr", "multipole units", "MISSING_MULTIPOLE_PROFILE", "PPN/tidal/orbital residual"),
        ("RS4289_2", "dln_mu_tr_dt", "time^-1", "MISSING_TIME_DRIFT_BOUND", "Gdot/clocks/orbits"),
        ("RS4289_3", "alpha_tr(lambda)", "dimensionless", "MISSING_RANGE_PROFILE", "R10/fifth-force"),
        ("RS4289_4", "delta_frame_source", "dimensionless", "MISSING_SAME_FRAME_SIGNATURE", "WEP/clocks"),
        ("RS4289_5", "delta_beta_source", "dimensionless", "MISSING_SECOND_ORDER_SOURCE_BOUND", "PPN beta"),
        ("RS4289_6", "R_transport_to_local", "normalized AJ", "MISSING_TRANSITION_PROFILE", "cGamma/AJ"),
        ("RS4289_7", "R_Bgrad_to_local", "normalized AJ", "MISSING_TRANSITION_PROFILE", "cGamma/AJ"),
    ]
    return [
        {
            **common(),
            "schema_id": schema_id,
            "quantity": quantity,
            "units": units,
            "status": status,
            "observable_link": observable,
            "numeric_value": "MISSING",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for schema_id, quantity, units, status, observable in raw
    ]


def aj_capacity(pi_b: float, tres_over_tau: float, c_gamma_abs: float) -> float:
    if c_gamma_abs <= 0.0:
        return float("inf")
    return PI_B_COEFFICIENT * pi_b * tres_over_tau / c_gamma_abs


def control_rows() -> List[Dict[str, str]]:
    controls = [
        (
            "CTRL4289_0_pure_hilbert_monopole",
            "pure same-worldtube Hilbert monopole",
            0.01,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            True,
            "PASS_IF_PARENT_SIGNED",
        ),
        (
            "CTRL4289_1_small_extra_monopole",
            "small non-Hilbert monopole residual",
            0.0,
            1.0e-5,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            True,
            "PASS_NUMERIC_CONTROL",
        ),
        (
            "CTRL4289_2_order_one_extra_monopole",
            "order-one non-Hilbert monopole residual",
            0.0,
            1.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            True,
            "FAIL_NUMERIC_CONTROL",
        ),
        (
            "CTRL4289_3_order_one_with_relaxation",
            "order-one residual at transition required relaxation",
            0.0,
            1.0,
            0.0,
            0.0,
            0.0,
            0.0,
            11.912289074553,
            True,
            "PASS_AT_THRESHOLD_CONTROL",
        ),
        (
            "CTRL4289_4_multipole_leak",
            "small monopole but live multipole",
            0.0,
            1.0e-5,
            0.1,
            0.0,
            0.0,
            0.0,
            1.0,
            True,
            "FAIL_MULTIPOLE_CONTROL",
        ),
        (
            "CTRL4289_5_missing_source_lock",
            "same-worldtube lock absent",
            0.01,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
            False,
            "UNSCOREABLE_PARENT_LOCK_MISSING",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for (
        control_id,
        description,
        hilbert_monopole_fraction,
        epsilon_mu,
        multipole_norm,
        time_norm,
        range_norm,
        beta_frame_norm,
        tres_over_tau,
        source_locked,
        expected,
    ) in controls:
        residual_AJ = abs(epsilon_mu) + abs(multipole_norm) + abs(time_norm) + abs(range_norm) + abs(beta_frame_norm)
        capacity = aj_capacity(TRANSITION_PIB, tres_over_tau, 1.0)
        score_ready = source_locked and expected != "UNSCOREABLE_PARENT_LOCK_MISSING"
        passes = score_ready and residual_AJ <= capacity and multipole_norm == 0.0 and time_norm == 0.0 and range_norm == 0.0 and beta_frame_norm == 0.0
        rows.append(
            {
                **common(),
                "control_id": control_id,
                "description": description,
                "hilbert_monopole_fraction": f"{hilbert_monopole_fraction:.12e}",
                "epsilon_mu_tr": f"{epsilon_mu:.12e}",
                "multipole_norm": f"{multipole_norm:.12e}",
                "time_norm": f"{time_norm:.12e}",
                "range_norm": f"{range_norm:.12e}",
                "beta_frame_norm": f"{beta_frame_norm:.12e}",
                "T_res_over_tau_L": f"{tres_over_tau:.12e}",
                "AJ_residual_proxy": f"{residual_AJ:.12e}",
                "AJ_capacity": f"{capacity:.12e}",
                "source_locked_before_readout": str(source_locked),
                "score_ready": str(score_ready),
                "passes_control": str(passes),
                "expected": expected,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision_id": "DEC4289_0",
            "selected_route": "HILBERT_MONOPOLE_SOURCE_LOCK_OR_FIRST_RESIDUAL_BOUND_ROW",
            "meaning": "Transition shell does not need pointwise deletion if it is a same-worldtube Hilbert monopole. What must be killed or bounded is the residual vector outside that monopole.",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    raw = [
        ("FW4289_0", "Do not use measured orbital GM to define the transition source mass."),
        ("FW4289_1", "Do not hide non-Hilbert monopole epsilon_mu inside calibrated G."),
        ("FW4289_2", "Do not treat l=0 monopole absorption as full PPN/local-GR."),
        ("FW4289_3", "Do not ignore multipole, time, range, frame, source-species, or beta residuals."),
        ("FW4289_4", "Do not use transition closure no-leak credit as cGamma/AJ evidence."),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "forbidden_move": forbidden_move,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, forbidden_move in raw
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status_id": "STATUS4289_0",
            "status": "TRANSITION_MONOPOLE_ROUTE_CONDITIONAL_RESIDUAL_VECTOR_DEFINED",
            "summary": "4289 turns the transition shell problem into a sharper split: same-worldtube Hilbert monopole is absorbable; all non-Hilbert/non-monopole/time/range/frame/PPN pieces remain live residual rows.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target_id": "NEXT4289_0",
            "target_file": NEXT_TARGET,
            "task": "Try to parent-sign the transition shell as a same-worldtube Hilbert monopole with zero non-Hilbert monopole; if not, fill the first residual bound row.",
            "priority": "highest_remaining_transition_frontier",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    capacity = aj_capacity(TRANSITION_PIB, 1.0, 1.0)
    return f"""
# 305 transition monopole absorption or residual profile gate

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Result

4289 tries a more physical transition-shell route.

The shell does **not** have to vanish pointwise if its exterior effect is only the same Hamiltonian/Hilbert monopole used to define the source before readout:

```text
M_H^dress -> M_H^dress + M_tr^H,
Phi_N = -G_cal (M_H^dress + M_tr^H)/r.
```

That piece is not an extra local residual. It is absorbed into the calibrated source charge in the same way ordinary binding/field energy contributes to active mass.

## The Actual Residual Vector

What cannot be hidden is:

```text
epsilon_mu_tr,
Q_l>=1_tr,
dln_mu_tr_dt,
alpha_tr(lambda),
delta_frame_source,
eta_source_AB,
delta_beta_source,
R_transport_to_local,
R_Bgrad_to_local.
```

So the transition-shell problem becomes:

```text
q_tr = q_tr^Hilbert-monopole + q_tr^residual.
```

Only `q_tr^Hilbert-monopole` is absorbable. The residual vector must be zero or bounded.

At the rough transition anchor `Pi_B={TRANSITION_PIB}` and `abs(c_Gamma)=1`, the 4287/4288 capacity at `T_res/tau_L=1` is:

```text
A_J,residual <= {capacity:.12e}.
```

## Verdict

This is progress, but not a public local-GR claim. The same-worldtube Hilbert inclusion and zero non-Hilbert monopole are not yet parent-signed.

Next target:

```text
prove transition shell is same-worldtube Hilbert monopole,
or fill first residual bound row.
```
"""


def checkpoint_doc() -> str:
    return f"""
# 4289 - transition monopole absorption or residual profile gate

Marker: `{MARKER}`

Decision: `{DECISION}`

4289 splits the transition shell into:

```text
q_tr = q_tr^Hilbert-monopole + q_tr^residual.
```

The same-worldtube Hilbert monopole can be absorbed into the calibrated source charge before readout. The residual vector cannot: `epsilon_mu_tr`, multipoles, time/range/frame/species hair, beta-source terms, and cGamma/AJ profile residuals must be zero or bounded.

No local-GR claim is promoted because same-worldtube source lock and zero non-Hilbert monopole are still not parent-signed.
"""


def generated_nonclaim_rows(paths: Dict[str, Path]) -> Iterable[Dict[str, str]]:
    for path in paths.values():
        for row in csv_rows(path):
            yield row


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    clauses = csv_rows(paths["theorem_clauses"])
    decomposition = csv_rows(paths["transition_decomposition"])
    schema = csv_rows(paths["residual_schema"])
    controls = csv_rows(paths["control_runner"])
    all_generated = list(generated_nonclaim_rows(paths))
    validations = [
        ("VAL4289_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited source paths exist"),
        ("VAL4289_1_needles_found", all(row["required_text_found"] == "True" for row in sources), "all cited source needles found"),
        (
            "VAL4289_2_theorem_not_promoted",
            any(row["clause_id"] == "MTC4289_5_verdict" and row["status"] == "CONDITIONAL_NOT_PROMOTED" for row in clauses),
            "monopole absorption theorem remains conditional nonclaim",
        ),
        (
            "VAL4289_3_nonEH_monopole_open",
            any(row["clause_id"] == "MTC4289_2_no_extra_nonEH_monopole" and row["status"] == "NOT_PARENT_DERIVED" for row in clauses),
            "non-Hilbert monopole zero is not parent-derived",
        ),
        (
            "VAL4289_4_decomposition_complete",
            {"calibrated_Hilbert_monopole", "epsilon_mu_tr", "Q_l>=1_tr", "alpha_tr(lambda)", "A_J_residual_tr"}.issubset({row["term"] for row in decomposition}),
            "transition decomposition includes absorbable monopole and residual terms",
        ),
        (
            "VAL4289_5_schema_missing_rows",
            {"epsilon_mu_tr", "Q_l>=1_tr", "dln_mu_tr_dt", "alpha_tr(lambda)", "R_transport_to_local", "R_Bgrad_to_local"}.issubset({row["quantity"] for row in schema})
            and all(row["score_ready"] == "False" for row in schema),
            "residual profile schema emitted as nonclaim missing rows",
        ),
        (
            "VAL4289_6_control_behaviour",
            any(row["control_id"] == "CTRL4289_0_pure_hilbert_monopole" and row["passes_control"] == "True" for row in controls)
            and any(row["control_id"] == "CTRL4289_2_order_one_extra_monopole" and row["passes_control"] == "False" for row in controls)
            and any(row["control_id"] == "CTRL4289_5_missing_source_lock" and row["score_ready"] == "False" for row in controls),
            "control rows distinguish absorbable monopole, failed extra monopole, and missing source lock",
        ),
        ("VAL4289_7_formal_doc", FORMAL_PATH.exists() and MARKER in read_text(FORMAL_PATH), "formal document written"),
        ("VAL4289_8_checkpoint_doc", DOC_PATH.exists() and DECISION in read_text(DOC_PATH), "post-checkpoint document written"),
        ("VAL4289_9_claim_row", f"{CLAIM_ID}," in read_text(FORMAL / "02-claims-register.csv"), "claim register row added"),
        (
            "VAL4289_10_no_claim_rows",
            all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_generated),
            "all generated rows remain private nonclaim rows",
        ),
    ]
    for name, path in paths.items():
        validations.append((f"VAL4289_csv_{name}", bool(csv_rows(path)), f"{path.name} parses with rows"))
    return [
        {
            **common(),
            "check_id": check_id,
            "description": description,
            "passed": str(passed),
            "evidence": "generated_artifacts",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, passed, description in validations
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4289_SOURCE_REGISTER.csv",
        "theorem_clauses": SOURCE_DIR / "P8_Y5_R2FR_4289_MONOPOLE_THEOREM_CLAUSES.csv",
        "transition_decomposition": SOURCE_DIR / "P8_Y5_R2FR_4289_TRANSITION_DECOMPOSITION.csv",
        "residual_schema": SOURCE_DIR / "P8_Y5_R2FR_4289_RESIDUAL_PROFILE_SCHEMA.csv",
        "control_runner": SOURCE_DIR / "P8_Y5_R2FR_4289_MONOPOLE_RESIDUAL_CONTROL_RUNNER.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4289_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4289_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4289_STATUS.csv",
        "next_target": SOURCE_DIR / "P8_Y5_R2FR_4289_NEXT_TARGET.csv",
    }
    write_csv(paths["sources"], source_rows())
    write_csv(paths["theorem_clauses"], theorem_clause_rows())
    write_csv(paths["transition_decomposition"], transition_decomposition_rows())
    write_csv(paths["residual_schema"], residual_schema_rows())
    write_csv(paths["control_runner"], control_rows())
    write_csv(paths["decision"], decision_rows())
    write_csv(paths["firewall"], firewall_rows())
    write_csv(paths["status"], status_rows())
    write_csv(paths["next_target"], next_target_rows())
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    append_claim()
    append_unique_block(
        FORMAL / "07-unification-spine.md",
        MARKER,
        "PPC4161 4289 transition monopole absorption split",
        "4289 makes the transition-shell frontier sharper. A same-worldtube Hamiltonian/Hilbert monopole contribution is absorbable into the calibrated source charge before readout, but only if the parent source lock is signed. The live residual vector is now explicit: extra non-Hilbert monopole `epsilon_mu_tr`, multipoles, time/range/frame/species hair, beta-source terms, and cGamma/AJ transition profile residuals.",
    )
    append_unique_block(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        "4289 packet transition monopole split",
        "Packet update: the transition shell need not be pointwise deleted if it is the same Hilbert monopole source. The remaining frontier is to parent-sign that source lock or bound the non-Hilbert/non-monopole residual vector.",
    )
    write_csv(VALIDATION_PATH, validation_rows(paths))
    failed = [row for row in csv_rows(VALIDATION_PATH) if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(paths)} csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(csv_rows(VALIDATION_PATH))} failed={len(failed)}")
    print(f"{CHECKPOINT}: transition AJ capacity at T_res/tau_L=1, |cGamma|=1 = {aj_capacity(TRANSITION_PIB, 1.0, 1.0):.12e}")
    print(f"{CHECKPOINT}: decision={DECISION}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['description']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
