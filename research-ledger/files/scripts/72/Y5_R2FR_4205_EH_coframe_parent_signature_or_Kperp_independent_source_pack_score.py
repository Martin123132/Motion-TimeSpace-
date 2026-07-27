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

CHECKPOINT = "4205"
CLAIM_ID = "L-046"
BRANCH_ID = "MTS_R2FR_Y5_EH_COFRAME_OR_KPERP_SCORE_4205"
DECISION = (
    "EH_COFRAME_PARENT_SIGNATURE_GATE_REDUCED_TO_SIX_CLAUSES_"
    "INDEPENDENT_KPERP_SCORE_FUNCTION_DERIVED_NUMERIC_SOURCES_MISSING_NONCLAIM"
)
FORMAL_PATH = FORMAL / "221-PPC4161-EH-coframe-parent-signature-or-Kperp-score.md"
DOC_PATH = POST / "4205-Y5-R2FR-EH-coframe-parent-signature-or-Kperp-independent-source-pack-score.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_MARKER = "PPC4161_EH_COFRAME_OR_KPERP_SCORE_4205"
PACKET_MARKER = "PPC4161_PACKET_EH_COFRAME_OR_KPERP_SCORE_4205"
NEXT_TARGET = "4206-Y5-R2FR-source-coupling-GN-normalization-or-independent-Kperp-score-inputs.md"

SOURCES = {
    "SRC4205_00_4204_decision": (
        SOURCE_DIR / "P8_Y5_R2FR_4204_DECISION.csv",
        "KPERP_SECTOR_PLACEMENT_THEOREM_WRITTEN",
        "4204 says Kperp must be sector-placed before scoring.",
    ),
    "SRC4205_01_4204_pack": (
        SOURCE_DIR / "P8_Y5_R2FR_4204_INDEPENDENT_SOURCE_PACK.csv",
        "no_double_count_certificate",
        "4204 independent tensor source pack fields.",
    ),
    "SRC4205_02_4203_no_pole": (
        FORMAL / "219-PPC4161-no-physical-Kperp-pole-theorem.md",
        "Delta K_perp = 0",
        "4203 static GR TT no-pole theorem.",
    ),
    "SRC4205_03_197_EH": (
        FORMAL / "197-PPC4161-EH-local-metric-principal-block-origin-gate.md",
        "S_EC[e,omega;kappa_eff] -> S_EH[g_obs;kappa_eff] + boundary",
        "Conditional EH/Palatini local metric principal block.",
    ),
    "SRC4205_04_193_quotient": (
        FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md",
        "S_matter = Sbar_m[psi, g_obs(q), A(q), theta(q)]",
        "Matter/readout quotient descent before variation.",
    ),
    "SRC4205_05_201_residuals": (
        FORMAL / "201-PPC4161-extra-invariant-residual-coefficient-map.md",
        "c_T         torsion-square residual",
        "Residual map keeps c_T/source-coupling gaps explicit.",
    ),
    "SRC4205_06_4202_pack": (
        SOURCE_DIR / "P8_Y5_R2FR_4202_FIRST_SOURCE_PACK.csv",
        "Z_T",
        "4202 source pack inputs for independent Kperp scoring.",
    ),
    "SRC4205_07_4202_thresholds": (
        SOURCE_DIR / "P8_Y5_R2FR_4202_PPN_THRESHOLD_MAP.csv",
        "delta_gamma",
        "4202 PPN/clock/local threshold map.",
    ),
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def common() -> Dict[str, str]:
    return {"timestamp_utc": now(), "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def read_csv(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


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


def signature_clause_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "SIG4205_0_same_coframe",
            "same observed coframe",
            "all matter, EM, clocks, rods and PPN readouts use one nondegenerate e_obs(q)",
            "without this, local GR cannot inherit one metric or one inertial frame",
            "conditional_not_parent_signed",
        ),
        (
            "SIG4205_1_EH_principal_block",
            "EH/Palatini spin-2 principal block",
            "the leading local two-derivative spin-2 sector is S_EH[g_obs;kappa_eff] plus boundary",
            "moves K_metric_TT to ordinary GR geometry rather than extra source",
            "conditional_not_parent_signed",
        ),
        (
            "SIG4205_2_no_independent_TT_source",
            "no independent TT source",
            "P_TT(delta S_extra/delta g_obs)=0 after quotient and boundary routing",
            "kills K_extra_source instead of merely calling it GR",
            "unsigned",
        ),
        (
            "SIG4205_3_quotient_vertical_silence",
            "vertical quotient silence",
            "Dq[v]=0 and O_loc=Obar_loc o q imply DO_loc[v]=0",
            "sets W_i^K=0 for vertical/gauge representatives only",
            "conditional_selector",
        ),
        (
            "SIG4205_4_boundary_radiation_routing",
            "boundary/radiation routing",
            "B_T=I_T=Z_Tmode=0 in stationary compact local PPN, while waves route to flux",
            "prevents hiding radiation as a static inverse-square residual",
            "conditional_private_selector",
        ),
        (
            "SIG4205_5_source_coupling_normalization",
            "source coupling normalization",
            "kappa_eff is the same coupling in geometry and matter, with kappa_eff=8*pi*G_N/c^4 after calibration",
            "this is the Newton/GR coupling bridge; current corpus has the slot, not the derivation",
            "unsigned_numeric_or_parent_derivation",
        ),
    ]
    return [
        {
            **common(),
            "clause_id": clause_id,
            "clause": clause,
            "required_statement": required_statement,
            "why_it_matters": why_it_matters,
            "current_status": current_status,
            "parent_signed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for clause_id, clause, required_statement, why_it_matters, current_status in rows
    ]


def fork_theorem_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "TH4205_0_signature_gate",
            "EH/coframe signature route",
            "if all SIG4205 clauses are parent-signed, then K_extra_source=0 and local Kperp is GR TT/vertical/boundary-radiative",
            "route to 4203 no-pole theorem and quotient zero weights",
            "conditional_theorem",
        ),
        (
            "TH4205_1_score_route",
            "independent source route",
            "if any signature clause fails, score K_extra_source with R_i^K <= |W_i^K| N_T / D_T",
            "no more unscored Kperp branch is allowed",
            "active_fallback",
        ),
        (
            "TH4205_2_numerator",
            "source numerator",
            "N_T = |S_T| + |B_T| + |I_T| + |Z_Tmode|",
            "collects source, boundary, incoming wave and kernel obstructions",
            "derived_from_4202",
        ),
        (
            "TH4205_3_denominator",
            "coercive denominator",
            "D_T = Z_T*lambda_D + M_T2",
            "must be positive before a finite independent Kperp bound exists",
            "derived_from_4202",
        ),
        (
            "TH4205_4_observable_score",
            "arena score",
            "score_i = |W_i^K| N_T / (D_T tau_i) <= 1",
            "turns local PPN/clock/WEP/orbital checks into one comparable gate",
            "new_4205_score_function",
        ),
        (
            "TH4205_5_no_middle_route",
            "no middle route",
            "either parent-sign zero/GR identity or provide numeric sourced score inputs",
            "prevents circling the same missing Kperp branch without a pass/fail gate",
            "derived_project_management_gate",
        ),
    ]
    return [
        {
            **common(),
            "theorem_id": theorem_id,
            "step": step,
            "formula": formula,
            "effect": effect,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for theorem_id, step, formula, effect, status in rows
    ]


def score_input_rows() -> List[Dict[str, str]]:
    rows = [
        ("Z_T", "coercive kinetic coefficient", "coefficient of |D K_perp|^2 in parent second variation", "MISSING_PARENT_KINETIC_RESIDUE"),
        ("lambda_D", "first positive tensor-domain eigenvalue", "local domain/spectral certificate after kernel projection", "MISSING_DOMAIN_AND_KERNEL_CERTIFICATE"),
        ("M_T2", "mass/stiffness gap", "coefficient of |K_perp|^2 in parent Hessian", "MISSING_PARENT_MASS_GAP_OR_NO_POLE"),
        ("S_T", "independent TT source norm", "P_TT source/current/sector leakage norm", "MISSING_SOURCE_ZERO_OR_NORM"),
        ("B_T", "bad boundary obstruction norm", "unrouted surface data not assigned to Hamiltonian/radiation flux", "MISSING_BOUNDARY_ZERO_OR_NORM"),
        ("I_T", "incoming tensor wave norm", "nonstationary homogeneous input in local branch", "MISSING_NO_INCOMING_OR_WAVE_NORM"),
        ("Z_Tmode", "zero-mode projection norm", "projection onto ker L_T after boundary conditions", "MISSING_KERNEL_CERTIFICATE"),
        ("W_i^K", "observable projection weights", "Jacobian from Kperp norm to each local arena residual", "MISSING_OBSERVABLE_PROJECTION_WEIGHTS"),
        ("tau_i", "arena threshold", "PPN/WEP/clock/orbital/R10 bound row", "PARTIAL_FROM_4202_PLACEHOLDER_THRESHOLDS"),
        ("sector_certificate", "no-double-count certificate", "proof this row is not ordinary EH TT or vertical/boundary data", "MISSING_PARENT_SECTOR_CERTIFICATE"),
    ]
    return [
        {
            **common(),
            "symbol": symbol,
            "definition": definition,
            "required_source_or_derivation": required_source_or_derivation,
            "current_status": current_status,
            "numeric_value": "MISSING",
            "source_path": "MISSING_PARENT_OR_NUMERIC_INPUT",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for symbol, definition, required_source_or_derivation, current_status in rows
    ]


def score_gate_rows() -> List[Dict[str, str]]:
    thresholds = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4202_PPN_THRESHOLD_MAP.csv")
    rows = []
    for row in thresholds:
        observable = row.get("observable", "MISSING_OBSERVABLE")
        tau = row.get("bound_value", "MISSING")
        units = row.get("bound_units", "MISSING")
        rows.append(
            {
                **common(),
                "observable": observable,
                "tau_i": tau,
                "tau_units": units,
                "residual_bound": f"R_{observable}^K <= |W_{observable}^K|*(|S_T|+|B_T|+|I_T|+|Z_Tmode|)/(Z_T*lambda_D+M_T2)",
                "pass_gate": f"|W_{observable}^K|*(|S_T|+|B_T|+|I_T|+|Z_Tmode|) <= {tau}*(Z_T*lambda_D+M_T2)",
                "current_status": "not_scoreable_parent_coefficients_or_W_missing",
                "numeric_score_i": "MISSING",
                "source_path": str(SOURCE_DIR / "P8_Y5_R2FR_4202_PPN_THRESHOLD_MAP.csv"),
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "six_clause_EH_coframe_gate_written": "True",
            "independent_Kperp_score_function_written": "True",
            "EH_coframe_parent_signed": "False",
            "Kperp_score_numeric": "False",
            "source_coupling_GN_normalized": "False",
            "local_GR_claim": "False",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def claim_firewall_rows() -> List[Dict[str, str]]:
    rows = [
        ("FW4205_0_no_EH_without_signature", "Do not call Kperp GR TT unless the EH/coframe identity and coupling clauses are parent-signed."),
        ("FW4205_1_no_score_without_coefficients", "Do not claim local pass from the score formula until every coefficient, weight and threshold is sourced."),
        ("FW4205_2_no_coupling_skip", "Newton/GR reduction needs kappa_eff/G_N normalization, not just an EH-looking operator."),
        ("FW4205_3_no_double_count", "A Kperp row cannot be both already counted as geometry and scored as an extra source."),
        ("FW4205_4_no_static_wave_smuggle", "Incoming or radiative tensor modes must be routed as flux/boundary, not static PPN silence."),
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
            "summary": "4205 reduces the Kperp local-GR fork to a six-clause EH/coframe/coupling signature gate or a single independent-source score inequality for every local arena.",
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
            "why": "The only serious remaining fork is now coupling and source ownership: either derive kappa_eff/G_N and zero independent Kperp source, or populate the score inputs.",
            "route_A": "derive source-coupling normalization kappa_eff -> G_N from parent matter variation",
            "route_B": "prove P_TT(delta S_extra)=0 and boundary/incoming/kernel obstructions vanish",
            "route_C": "source numeric Z_T, lambda_D, M_T2, W_i^K and obstruction norms for score_i",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def all_rows() -> Dict[str, List[Dict[str, str]]]:
    return {
        "P8_Y5_R2FR_4205_SOURCE_REGISTER.csv": source_rows(),
        "P8_Y5_R2FR_4205_EH_COFRAME_SIGNATURE_GATE.csv": signature_clause_rows(),
        "P8_Y5_R2FR_4205_FORK_THEOREM.csv": fork_theorem_rows(),
        "P8_Y5_R2FR_4205_SCORE_INPUTS.csv": score_input_rows(),
        "P8_Y5_R2FR_4205_SCORE_GATES.csv": score_gate_rows(),
        "P8_Y5_R2FR_4205_DECISION.csv": decision_rows(),
        "P8_Y5_R2FR_4205_CLAIM_FIREWALL.csv": claim_firewall_rows(),
        "P8_Y5_R2FR_4205_STATUS.csv": status_rows(),
        "P8_Y5_R2FR_4205_NEXT_TARGET.csv": next_target_rows(),
    }


def write_docs() -> None:
    formal = f"""# 221 - PPC4161 EH Coframe Parent Signature Or Kperp Score

Marker: `{SPINE_MARKER}`
Checkpoint: `{CHECKPOINT}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint turns the `K_perp` ambiguity into a hard fork:

```text
parent-sign EH/coframe/coupling identity
```

or

```text
score an independent Kperp source against every local arena.
```

## Six-Clause EH/Coframe Gate

The GR/static branch is allowed only if all six clauses are parent-owned:

```text
same observed coframe for matter, EM, clocks and rods;
EH/Palatini spin-2 principal block;
no independent TT source projection;
vertical quotient silence;
boundary/radiation routing;
kappa_eff = 8*pi*G_N/c^4 after source calibration.
```

If those clauses hold, `K_perp` is ordinary GR TT, vertical, or boundary/radiative, and the 4203 no-pole theorem closes the stationary compact local branch.

## Independent-Source Score

If any clause fails, the extra branch must be scored:

```text
N_T = |S_T| + |B_T| + |I_T| + |Z_Tmode|
D_T = Z_T*lambda_D + M_T2
R_i^K <= |W_i^K| N_T / D_T
score_i = |W_i^K| N_T / (D_T tau_i) <= 1.
```

The current corpus has the formula and threshold interface, but not the parent-owned numeric/source inputs.

## Current Verdict

This is a leap forward in structure, not a pass. The local branch now has no soft middle: either derive the parent EH/coframe/source-coupling identity, or provide a numeric sourced independent-source score pack.
"""
    checkpoint = f"""# 4205 - Y5 R2FR EH Coframe Parent Signature Or Kperp Independent Source Pack Score

Decision: `{DECISION}`

4205 sharpens the 4204 fork into a pass/fail contract.

The derivation route requires a six-clause parent signature:

```text
same coframe + EH principal block + no independent TT source
+ quotient vertical silence + boundary/radiation routing + kappa_eff/G_N normalization.
```

The fallback route is no longer a vague source pack. It has the score:

```text
score_i = |W_i^K| (|S_T|+|B_T|+|I_T|+|Z_Tmode|)
          / ((Z_T*lambda_D+M_T2) tau_i).
```

Current status remains nonclaim because the signature clauses and score coefficients are not parent-sourced yet.
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
        f'{CLAIM_ID},local_gr,"The EH/coframe parent-signature gate is reduced to six clauses, and the independent Kperp source branch is reduced to a single score inequality per local arena.",'
        f'"4205 source audit, EH/coframe signature clauses, fork theorem, score input rows, score gates, decision row and firewall.",'
        f'private_EH_coframe_or_Kperp_score_nonclaim_coefficients_missing,'
        f'"Derive kappa_eff/G_N and no independent TT source, or source numeric Z_T, lambda_D, M_T2, N_T and W_i^K.",'
        f'"This removes the soft middle route: Kperp must be parent-identified as GR/vertical/boundary or independently scored."'
    )
    if f"{CLAIM_ID}," not in read_text(CLAIMS_PATH):
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(claim_row + "\n")

    spine_block = f"""### PPC4161 EH Coframe Or Kperp Score - 4205

Marker: `{SPINE_MARKER}`
Claim register row: `{CLAIM_ID}`

4205 turns the local `Kperp` fork into a strict contract. Either the parent signs same-coframe/EH/no-independent-TT/quotient/boundary/source-coupling clauses, or every independent tensor contribution must satisfy:

```text
score_i = |W_i^K| (|S_T|+|B_T|+|I_T|+|Z_Tmode|) / ((Z_T*lambda_D+M_T2) tau_i) <= 1.
```

Current status remains nonclaim because the source-coupling normalization and numeric score inputs are not parent-owned."""
    append_once(SPINE_PATH, SPINE_MARKER, spine_block)

    packet_block = f"""## PPC4161 Packet EH Coframe Or Kperp Score - 4205

Marker: `{PACKET_MARKER}`

The local branch now has no fog-bank option. It is either parent-signed GR/vertical/boundary data, or it is an independent source with a score against every local arena."""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)


def validate(rows_by_file: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    source = rows_by_file["P8_Y5_R2FR_4205_SOURCE_REGISTER.csv"]
    clauses = rows_by_file["P8_Y5_R2FR_4205_EH_COFRAME_SIGNATURE_GATE.csv"]
    theorem = rows_by_file["P8_Y5_R2FR_4205_FORK_THEOREM.csv"]
    inputs = rows_by_file["P8_Y5_R2FR_4205_SCORE_INPUTS.csv"]
    gates = rows_by_file["P8_Y5_R2FR_4205_SCORE_GATES.csv"]
    decision = rows_by_file["P8_Y5_R2FR_4205_DECISION.csv"]
    all_rows_flat = [row for rows in rows_by_file.values() for row in rows]
    tau_positive = all(float(row["tau_i"]) > 0 for row in gates if row["tau_i"] != "MISSING")
    checks = [
        ("VAL4205_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in source)),
        ("VAL4205_1_source_needles", "all source needles found", all(row["required_text_found"] == "True" for row in source)),
        ("VAL4205_2_six_clauses", "six EH/coframe/coupling clauses written", len(clauses) == 6),
        ("VAL4205_3_coupling_clause", "source coupling normalization clause present", any(row["clause_id"] == "SIG4205_5_source_coupling_normalization" for row in clauses)),
        ("VAL4205_4_fork_theorem", "fork theorem includes signature and score routes", any(row["theorem_id"] == "TH4205_0_signature_gate" for row in theorem) and any(row["theorem_id"] == "TH4205_1_score_route" for row in theorem)),
        ("VAL4205_5_score_formula", "score formula includes numerator, denominator and score gate", {"TH4205_2_numerator", "TH4205_3_denominator", "TH4205_4_observable_score"}.issubset({row["theorem_id"] for row in theorem})),
        ("VAL4205_6_score_inputs_missing", "score inputs remain explicitly missing/nonclaim", all(row["numeric_value"] == "MISSING" for row in inputs)),
        ("VAL4205_7_score_gates_from_4202", "score gates generated from 4202 thresholds", len(gates) >= 8 and tau_positive),
        ("VAL4205_8_decision_nonclaim", "decision keeps EH unsigned and score nonnumeric", decision[0]["EH_coframe_parent_signed"] == "False" and decision[0]["Kperp_score_numeric"] == "False"),
        ("VAL4205_9_no_claim_flags", "all generated claim flags remain false", all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_rows_flat)),
        ("VAL4205_10_docs_written", "formal and checkpoint docs written", FORMAL_PATH.exists() and DOC_PATH.exists()),
        ("VAL4205_11_claim_register", "claim register contains L-046", CLAIM_ID + "," in read_text(CLAIMS_PATH)),
        ("VAL4205_12_spine_marker", "spine marker present", SPINE_MARKER in read_text(SPINE_PATH)),
        ("VAL4205_13_packet_marker", "packet marker present", PACKET_MARKER in read_text(PACKET_PATH)),
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
    write_csv(SOURCE_DIR / "P8_Y5_BRR545_4205_VALIDATION.csv", validation)
    if not all(row["passed"] == "True" for row in validation):
        failed = [row for row in validation if row["passed"] != "True"]
        raise RuntimeError(f"4205 validation failed: {failed}")
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    write_all()
    print(DECISION)
    print(f"formal={FORMAL_PATH}")
    print(f"checkpoint={DOC_PATH}")
    print(f"validation={SOURCE_DIR / 'P8_Y5_BRR545_4205_VALIDATION.csv'}")
    print("rows=14 validation checks")


if __name__ == "__main__":
    main()
