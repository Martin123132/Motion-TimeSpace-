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
SCRIPTS = POST / "scripts"
CORE = ROOT / "core-mts-framework"

CHECKPOINT = "4224"
CLAIM_ID = "L-065"
BRANCH = "MTS_R2FR_Y5_LAMBDA_GAMMA_CORE_SIGN_GATE_4224"
DECISION = "LAMBDA_NONNEGATIVE_CONDITIONALLY_DERIVED_FROM_PHI_FORMULAS_GAMMA_DAMPING_REQUIRES_BOUNDARY_OR_OPEN_SYSTEM_REPAIR_BINDING_ROW_REMAINS_UNFILLED_NONCLAIM"
MARKER = "PPC4161_LAMBDA_GAMMA_CORE_SIGN_GATE_4224"
PACKET_MARKER = "PPC4161_PACKET_LAMBDA_GAMMA_CORE_SIGN_GATE_4224"
NEXT_TARGET = "4225-Y5-R2FR-gamma-damping-open-system-action-or-boundary-repair.md"

FORMAL_PATH = FORMAL / "240-PPC4161-lambda-gamma-core-action-sign-and-binding-bound-source-row.md"
DOC_PATH = POST / "4224-Y5-R2FR-lambda-gamma-core-action-sign-and-binding-bound-source-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4224_VALIDATION.csv"


@dataclass(frozen=True)
class SourceSpec:
    source_id: str
    path: Path
    required_text: str
    role: str


SOURCE_SPECS: Dict[str, SourceSpec] = {
    "SRC4224_00_4223_next": SourceSpec(
        "SRC4224_00_4223_next",
        SOURCE_DIR / "P8_Y5_R2FR_4223_NEXT_TARGET.csv",
        "4224-Y5-R2FR-lambda-gamma-core-action-sign-and-binding-bound-source-row.md",
        "4223 selected lambda/gamma sign and binding source rows.",
    ),
    "SRC4224_01_4223_core": SourceSpec(
        "SRC4224_01_4223_core",
        SOURCE_DIR / "P8_Y5_R2FR_4223_CORE_ACTION_SIGN.csv",
        "CAS4223_4_lambda_sign",
        "4223 lambda/gamma core sign gate.",
    ),
    "SRC4224_02_fund_gamma": SourceSpec(
        "SRC4224_02_fund_gamma",
        CORE / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md",
        "γ = Φ_G",
        "Fundamental action source for gamma formula.",
    ),
    "SRC4224_03_fund_lambda": SourceSpec(
        "SRC4224_03_fund_lambda",
        CORE / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md",
        "λ = Φ_G³",
        "Fundamental action source for lambda formula.",
    ),
    "SRC4224_04_eff_action": SourceSpec(
        "SRC4224_04_eff_action",
        CORE / "field-theory" / "the-effective-field-theory-of-motion-timespace.md",
        "λ = Φ_G³",
        "Effective field source for lambda/gamma formula.",
    ),
    "SRC4224_05_red_team": SourceSpec(
        "SRC4224_05_red_team",
        FORMAL / "06-consistency-red-team.md",
        "Ordinary dissipative equations",
        "Existing critique of damping from a single-field conservative action.",
    ),
    "SRC4224_06_repair": SourceSpec(
        "SRC4224_06_repair",
        FORMAL / "10-core-consistency-repair.md",
        "open-system effective action",
        "Existing repair route for dissipative core dynamics.",
    ),
    "SRC4224_07_variable_gamma": SourceSpec(
        "SRC4224_07_variable_gamma",
        FORMAL / "04-variable-audit.csv",
        "gamma=Phi_G",
        "Variable audit records gamma formula and dimensional concerns.",
    ),
    "SRC4224_08_4223_formal": SourceSpec(
        "SRC4224_08_4223_formal",
        FORMAL / "239-PPC4161-binding-stabilizer-and-MTS-core-negative-energy-bound-or-parent-signature.md",
        "gamma boundary/bath-balanced",
        "4223 formal fork requiring gamma boundary or bath balance.",
    ),
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def common() -> Dict[str, str]:
    return {"timestamp_utc": now(), "branch_id": BRANCH, "checkpoint_id": CHECKPOINT}


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty csv: {path}")
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


def append_once(path: Path, marker: str, block: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = read_text(path)
    if marker in existing:
        return
    with path.open("a", encoding="utf-8") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + block.strip() + "\n")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source in SOURCE_SPECS.values():
        text = read_text(source.path)
        rows.append(
            {
                **common(),
                "source_id": source.source_id,
                "path": str(source.path),
                "exists": str(source.path.exists()),
                "required_text": source.required_text,
                "required_text_found": str(source.required_text in text),
                "role": source.role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def lambda_rows() -> List[Dict[str, str]]:
    data = [
        (
            "LGS4224_0_source_formulas",
            "source formulas",
            "gamma = Phi_G sqrt(c^5/(G hbar)); lambda = Phi_G^3 (c^3/G) gamma; n=4/3",
            "core action source files",
            "SOURCE_BACKED_FORMULA_SHAPE",
        ),
        (
            "LGS4224_1_substitution",
            "lambda substitution",
            "lambda = Phi_G^4 (c^3/G) sqrt(c^5/(G hbar))",
            "substitute gamma formula into lambda formula",
            "DERIVED_ALGEBRAIC_SUBSTITUTION",
        ),
        (
            "LGS4224_2_nonnegative",
            "lambda sign",
            "real Phi_G and c,G,hbar>0 => lambda>=0",
            "Phi_G^4 is nonnegative for real Phi_G; physical constants are positive.",
            "CONDITIONAL_LAMBDA_NONNEGATIVE_DERIVED",
        ),
        (
            "LGS4224_3_n_positive",
            "power sign",
            "n=4/3>0",
            "the potential denominator has positive exponent parameter in the source action.",
            "SOURCE_BACKED_POSITIVE_N",
        ),
        (
            "LGS4224_4_units_guard",
            "units guard",
            "lambda sign is not lambda units or magnitude",
            "The sign reduction does not repair dimensional consistency or predict a numeric value.",
            "UNITS_AUDIT_STILL_REQUIRED",
        ),
    ]
    return [
        {
            **common(),
            "lambda_id": lambda_id,
            "piece": piece,
            "formula": formula,
            "derivation": derivation,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for lambda_id, piece, formula, derivation, status in data
    ]


def gamma_fork_rows() -> List[Dict[str, str]]:
    data = [
        (
            "GFR4224_0_boundary_identity",
            "conservative boundary identity",
            "-gamma psi psi_dot = -(gamma/2) d_t(psi^2) for fixed gamma",
            "A fixed coefficient in a standard single-field action gives a boundary term.",
            "DERIVED_BOUNDARY_IDENTITY",
        ),
        (
            "GFR4224_1_no_damping_from_boundary",
            "Euler-Lagrange warning",
            "fixed-endpoint variation of the boundary term does not generate +gamma psi_dot bulk damping",
            "The written conservative action and the advertised damped equation cannot both be true without extra structure.",
            "CONSISTENCY_FORK_IDENTIFIED",
        ),
        (
            "GFR4224_2_conservative_route",
            "conservative route",
            "gamma term is boundary-routed and E_gamma_bath_or_open_abs=0 under fixed endpoint/no-flux conditions",
            "This repairs the energy sign but demotes gamma damping from the closed local core equation.",
            "CONDITIONAL_ROUTE_INPUTS_MISSING",
        ),
        (
            "GFR4224_3_open_system_route",
            "open-system route",
            "introduce bath/doubled/influence variables so total energy is conserved while psi subsystem damps",
            "This preserves damping but requires E_gamma_bath_or_open_abs or a theorem-zero bath balance.",
            "NEXT_DERIVATION_TARGET",
        ),
        (
            "GFR4224_4_binding_status",
            "binding row status",
            "beta_bind and E_stab_neg_abs remain missing",
            "4224 closes the lambda sign route but does not fill ordinary binding/stabilizer values.",
            "BINDING_SOURCE_ROW_STILL_MISSING",
        ),
    ]
    return [
        {
            **common(),
            "gamma_id": gamma_id,
            "piece": piece,
            "formula_or_statement": formula,
            "derivation": derivation,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for gamma_id, piece, formula, derivation, status in data
    ]


def updated_bound_rows() -> List[Dict[str, str]]:
    data = [
        (
            "UBR4224_0_core_lambda_removed",
            "E_MTS_core_neg_abs",
            "E_MTS_core_neg_abs <= E_gamma_bath_or_open_abs + E_signature_mismatch_abs",
            "lambda negative-potential term is removed if lambda>=0 derivation is accepted.",
            "BOUND_REDUCED_VALUES_MISSING",
        ),
        (
            "UBR4224_1_gamma_boundary_zero",
            "E_gamma_bath_or_open_abs",
            "0 if gamma is boundary-routed with fixed endpoints/no open flux",
            "conservative route",
            "THEOREM_ZERO_CONDITIONAL_INPUTS_MISSING",
        ),
        (
            "UBR4224_2_gamma_bath_bound",
            "E_gamma_bath_or_open_abs",
            "absolute bath/open-system energy leakage if damping is physical",
            "open-system route",
            "BOUND_ROW_REQUIRED_IF_DAMPING",
        ),
        (
            "UBR4224_3_signature_mismatch",
            "E_signature_mismatch_abs",
            "wrong-sign hidden metric/coarse-graining/signature mismatch energy",
            "parent metric/field-space signature row",
            "MISSING_PARENT_SIGNATURE_OR_BOUND",
        ),
        (
            "UBR4224_4_binding",
            "E_binding_stabilizer_neg_abs",
            "beta_bind E_visible_rest + E_stab_neg_abs",
            "ordinary binding/stabilizer row from 4223 remains",
            "MISSING_BINDING_SOURCE_VALUES",
        ),
    ]
    return [
        {
            **common(),
            "bound_id": bound_id,
            "quantity": quantity,
            "formula_or_condition": formula,
            "route": route,
            "status": status,
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for bound_id, quantity, formula, route, status in data
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "lambda_nonnegative_derived": "True",
            "lambda_negative_potential_removed": "True",
            "gamma_action_damping_fork_identified": "True",
            "gamma_mode_available": "False",
            "E_gamma_bound_available": "False",
            "binding_fraction_bound_available": "False",
            "M_EH_positive_available": "False",
            "local_GR_claim": "False",
            "remaining_gap": "gamma_boundary_or_open_system_bath_balance_and_binding_bound",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    data = [
        ("LGF4224_0_no_lambda_panic", "keep lambda negative-potential term after formula substitution", "blocked", "lambda is nonnegative if Phi_G is real and source formulas are accepted"),
        ("LGF4224_1_no_numeric_lambda_claim", "claim numeric lambda or correct units from sign algebra", "blocked", "sign algebra does not solve dimensional audit"),
        ("LGF4224_2_no_damping_from_boundary", "claim fixed gamma boundary term derives damping", "blocked", "boundary term does not produce bulk damping under ordinary variation"),
        ("LGF4224_3_no_bath_hiding", "use physical damping without bath/open flux row", "blocked", "open-system damping needs energy bookkeeping"),
        ("LGF4224_4_no_MEH_claim", "promote lambda sign to M_EH/local-GR pass", "blocked", "gamma, binding, signature mismatch and other epsilon_E rows remain"),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "forbidden_move": forbidden_move,
            "status": status,
            "reason": reason,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, forbidden_move, status, reason in data
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status_id": "LGS4224_STATUS",
            "decision": DECISION,
            "summary": "The lambda potential sign is conditionally closed by substituting the source formulas; the gamma damping/action fork remains the live core-energy obstruction.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "reason": "lambda sign no longer looks like the main blocker; the written gamma action must be repaired as boundary-only or as a genuine open-system/doubled/bath action.",
            "derive_first": "construct gamma bath balance or prove conservative boundary route is the intended local core action",
            "fill_second": "E_gamma_bath_or_open_abs and E_signature_mismatch_abs rows",
            "fallback": "if damping cannot be action-owned, demote damped core equation to phenomenological open-system closure in local-GR branch",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""# 240 - PPC4161 Lambda/Gamma Core Action Sign And Binding Bound Source Row

Marker: `{MARKER}`

Branch: `{BRANCH}`
Decision: `{DECISION}`

## Lambda sign

The source corpus gives:

```text
gamma = Phi_G sqrt(c^5/(G hbar)),
lambda = Phi_G^3 (c^3/G) gamma,
n = 4/3.
```

Substitution gives:

```text
lambda = Phi_G^4 (c^3/G) sqrt(c^5/(G hbar)).
```

So for real `Phi_G` and positive `c,G,hbar`:

```text
lambda >= 0.
```

This conditionally removes the negative-potential term from the `E_MTS_core_neg_abs` row.

## Gamma fork

For fixed `gamma`:

```text
-gamma psi psi_dot = -(gamma/2) d_t(psi^2).
```

That is a boundary term in an ordinary fixed-endpoint action. It does **not** generate physical damping by itself.

So MTS must choose one of two honest local-core routes:

1. **Conservative boundary route:** `gamma` is boundary-routed, contributes no bulk negative energy, and the local conservative core does not claim damping from this term.
2. **Open-system route:** damping is real, but it must come from bath/doubled/influence variables with explicit energy bookkeeping.

## Updated core bound

With the lambda sign reduction:

```text
E_MTS_core_neg_abs
<= E_gamma_bath_or_open_abs
 + E_signature_mismatch_abs.
```

Binding/stabilizer remains:

```text
E_binding_stabilizer_neg_abs
<= beta_bind E_visible_rest + E_stab_neg_abs.
```

## Next target

`{NEXT_TARGET}` should repair or own the gamma damping route. If not, the damped equation must be demoted to phenomenological open-system closure for the local-GR branch.
"""


def checkpoint_doc() -> str:
    return f"""# 4224 - Lambda/Gamma Core Action Sign And Binding Bound Source Row

**Status:** `{DECISION}`.

## What moved

`lambda` is no longer just "missing sign" in the same way:

```text
lambda = Phi_G^4 (c^3/G) sqrt(c^5/(G hbar)) >= 0
```

for real `Phi_G` and positive physical constants.

That removes the negative-potential term from the core-energy bound.

## What remains hard

The written `gamma psi psi_dot` action term is boundary-like for fixed `gamma`. It cannot simultaneously be the source of ordinary bulk damping unless the parent theory supplies an open-system/bath/doubled action.

Next: `{NEXT_TARGET}`.
"""


def update_registers() -> None:
    claim_row = (
        f'{CLAIM_ID},local_gr,'
        f'"The lambda part of the MTS-core negative-energy obstruction is conditionally closed by substituting the corpus formulas gamma=Phi_G sqrt(c^5/(G hbar)) and lambda=Phi_G^3(c^3/G)gamma, giving lambda=Phi_G^4(c^3/G)sqrt(c^5/(G hbar))>=0 for real Phi_G; the remaining core obstruction is the gamma damping fork, which must be boundary-routed or open-system/bath-owned.",'
        f'"4224 source audit, lambda sign derivation, gamma fork rows, updated core bound, decision and firewall.",'
        f'private_lambda_sign_reduction_gamma_fork_nonclaim,'
        f'"Construct gamma open-system/bath balance or conservative boundary repair.",'
        f'"This closes only the lambda sign part; it does not prove M_EH, M_H_ref, local GR, Newton or PPN."'
    )
    append_once(FORMAL / "02-claims-register.csv", CLAIM_ID, claim_row)

    spine_block = f"""
## 99. Lambda Sign Reduction And Gamma Damping Fork

Marker: `{MARKER}`

4224 substitutes the source formulas:

```text
lambda = Phi_G^4 (c^3/G) sqrt(c^5/(G hbar)) >= 0.
```

The core negative-energy bound sharpens to:

```text
E_MTS_core_neg_abs <= E_gamma_bath_or_open_abs + E_signature_mismatch_abs.
```

The live issue is now the gamma fork: boundary term if conservative, bath/open-system energy row if damping is physical.
"""
    append_once(FORMAL / "07-unification-spine.md", MARKER, spine_block)

    packet_block = f"""
## Packet Update - Lambda/Gamma Core Sign

Marker: `{PACKET_MARKER}`

The lambda potential-sign blocker is conditionally reduced. The packet remains private/nonclaim because gamma damping must be action-owned as boundary or open-system/bath exchange before the `M_EH` sign score can close.
"""
    append_once(FORMAL / "180-PPC4161-private-local-packet-integration.md", PACKET_MARKER, packet_block)


def validate(rows_by_file: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    sources = rows_by_file["P8_Y5_R2FR_4224_SOURCE_REGISTER.csv"]
    lambdas = rows_by_file["P8_Y5_R2FR_4224_LAMBDA_SIGN.csv"]
    gammas = rows_by_file["P8_Y5_R2FR_4224_GAMMA_FORK.csv"]
    bounds = rows_by_file["P8_Y5_R2FR_4224_UPDATED_BOUND_ROWS.csv"]
    decision = rows_by_file["P8_Y5_R2FR_4224_DECISION.csv"][0]
    firewalls = rows_by_file["P8_Y5_R2FR_4224_CLAIM_FIREWALL.csv"]
    next_rows = rows_by_file["P8_Y5_R2FR_4224_NEXT_TARGET.csv"]
    all_rows = [row for rows in rows_by_file.values() for row in rows]

    checks = [
        ("VAL4224_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in sources)),
        ("VAL4224_1_source_needles", "all required source text found", all(row["required_text_found"] == "True" for row in sources)),
        (
            "VAL4224_2_lambda_derivation",
            "lambda rows include source formulas, substitution and nonnegative sign",
            {"LGS4224_0_source_formulas", "LGS4224_1_substitution", "LGS4224_2_nonnegative"}.issubset({row["lambda_id"] for row in lambdas}),
        ),
        (
            "VAL4224_3_gamma_fork",
            "gamma rows include boundary identity, no-damping warning and open-system route",
            {"GFR4224_0_boundary_identity", "GFR4224_1_no_damping_from_boundary", "GFR4224_3_open_system_route"}.issubset({row["gamma_id"] for row in gammas}),
        ),
        (
            "VAL4224_4_updated_bounds",
            "updated bounds remove lambda negative term and retain gamma/signature/binding rows",
            {"UBR4224_0_core_lambda_removed", "UBR4224_1_gamma_boundary_zero", "UBR4224_2_gamma_bath_bound", "UBR4224_4_binding"}.issubset({row["bound_id"] for row in bounds}),
        ),
        (
            "VAL4224_5_decision_nonclaim",
            "decision derives lambda but keeps gamma and local-GR unavailable",
            decision["lambda_nonnegative_derived"] == "True" and decision["gamma_mode_available"] == "False" and decision["local_GR_claim"] == "False",
        ),
        (
            "VAL4224_6_firewall",
            "firewall blocks numeric lambda claim, boundary damping claim, bath hiding and MEH claim",
            {"LGF4224_1_no_numeric_lambda_claim", "LGF4224_2_no_damping_from_boundary", "LGF4224_3_no_bath_hiding", "LGF4224_4_no_MEH_claim"}.issubset({row["firewall_id"] for row in firewalls}),
        ),
        (
            "VAL4224_7_no_claim_flags",
            "all generated claim flags remain false",
            all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_rows),
        ),
        ("VAL4224_8_docs_written", "formal and checkpoint docs written", FORMAL_PATH.exists() and DOC_PATH.exists()),
        ("VAL4224_9_claim_register", "claim register contains L-065", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv")),
        ("VAL4224_10_spine_packet", "spine and packet contain 4224 markers", MARKER in read_text(FORMAL / "07-unification-spine.md") and PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md")),
        ("VAL4224_11_next_target", "next target selected", next_rows[0]["next_target"] == NEXT_TARGET),
        ("VAL4224_12_script_exists", "generator script exists", (SCRIPTS / "Y5_R2FR_4224_lambda_gamma_core_action_sign_and_binding_bound_source_row.py").exists()),
        ("VAL4224_13_status", "status records nonclaim reduction", rows_by_file["P8_Y5_R2FR_4224_STATUS.csv"][0]["decision"] == DECISION),
        (
            "VAL4224_14_binding_retained",
            "binding row remains retained and unfilled",
            any(row["bound_id"] == "UBR4224_4_binding" and row["status"] == "MISSING_BINDING_SOURCE_VALUES" for row in bounds),
        ),
    ]
    return [
        {**common(), "check_id": check_id, "description": description, "passed": str(bool(passed))}
        for check_id, description, passed in checks
    ]


def write_all() -> None:
    rows_by_file: Dict[str, List[Dict[str, str]]] = {
        "P8_Y5_R2FR_4224_SOURCE_REGISTER.csv": source_rows(),
        "P8_Y5_R2FR_4224_LAMBDA_SIGN.csv": lambda_rows(),
        "P8_Y5_R2FR_4224_GAMMA_FORK.csv": gamma_fork_rows(),
        "P8_Y5_R2FR_4224_UPDATED_BOUND_ROWS.csv": updated_bound_rows(),
        "P8_Y5_R2FR_4224_DECISION.csv": decision_rows(),
        "P8_Y5_R2FR_4224_CLAIM_FIREWALL.csv": firewall_rows(),
        "P8_Y5_R2FR_4224_STATUS.csv": status_rows(),
        "P8_Y5_R2FR_4224_NEXT_TARGET.csv": next_target_rows(),
    }
    for filename, rows in rows_by_file.items():
        write_csv(SOURCE_DIR / filename, rows)

    FORMAL_PATH.write_text(formal_doc(), encoding="utf-8")
    DOC_PATH.write_text(checkpoint_doc(), encoding="utf-8")
    update_registers()
    validation_rows = validate(rows_by_file)
    write_csv(VALIDATION_PATH, validation_rows)


def main() -> None:
    write_all()
    print(DECISION)
    print(f"formal={FORMAL_PATH}")
    print(f"checkpoint={DOC_PATH}")
    print(f"validation={VALIDATION_PATH}")
    print("rows=15 validation checks")


if __name__ == "__main__":
    main()
