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

CHECKPOINT = "4201"
CLAIM_ID = "L-042"
BRANCH_ID = "MTS_R2FR_Y5_KPERP_FINITE_COEFFICIENT_VECTOR_4201"
DECISION = (
    "KPERP_FALLBACK_VECTOR_MAPPED_TO_PPN_INEQUALITIES_PARENT_LT_OR_NUMERIC_"
    "COEFFICIENTS_REQUIRED_NONCLAIM"
)
FORMAL_PATH = FORMAL / "217-PPC4161-Kperp-finite-coefficient-vector.md"
DOC_PATH = POST / "4201-Y5-R2FR-Kperp-finite-coefficient-vector-or-parent-tensor-operator-source.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_MARKER = "PPC4161_KPERP_FINITE_COEFFICIENT_VECTOR_4201"
PACKET_MARKER = "PPC4161_PACKET_KPERP_FINITE_COEFFICIENT_VECTOR_4201"
NEXT_TARGET = "4202-Y5-R2FR-parent-tensor-operator-LT-or-first-Kperp-coefficient-source-pack.md"

PPN_BOUNDS = [
    ("delta_phi_fraction", "dimensionless", 1.0e-5, "Newtonian potential fraction"),
    ("delta_gamma", "dimensionless", 1.0e-5, "spatial curvature / light propagation"),
    ("delta_beta", "dimensionless", 1.0e-4, "nonlinear potential response"),
    ("alpha1", "dimensionless", 1.0e-4, "preferred-frame vector response"),
    ("alpha2", "dimensionless", 1.0e-5, "preferred-frame tensor/vector response"),
    ("eta_AB", "dimensionless", 1.0e-13, "composition/equivalence-principle response"),
    ("Gdot_over_G", "yr^-1", 4.0e-14, "secular source-normalization drift"),
    ("chi_local_leak_fraction", "dimensionless", 1.0e-5, "forbidden local galaxy-transport leakage"),
    ("clock_delta_z", "dimensionless", 1.0e-16, "clock projection residual"),
]

SOURCES = {
    "SRC4201_00_4200_decision": (
        SOURCE_DIR / "P8_Y5_R2FR_4200_DECISION.csv",
        "fallback_bound_ready",
        "4200 decision row says finite Kperp fallback is active.",
    ),
    "SRC4201_01_4200_fallback": (
        SOURCE_DIR / "P8_Y5_R2FR_4200_FALLBACK_BOUND_VECTOR.csv",
        "KB4200_5_ppn_projection",
        "4200 fallback vector defines C_T, S_T, B_T, I_T, Z_T and W_i^K slots.",
    ),
    "SRC4201_02_4200_energy": (
        SOURCE_DIR / "P8_Y5_R2FR_4200_ENERGY_IDENTITY.csv",
        "||K_perp||_E <= C_T",
        "4200 finite norm inequality.",
    ),
    "SRC4201_03_59_ppn_bounds": (
        FORMAL / "59-local-ppn-branch-framework.md",
        "delta_gamma",
        "Local PPN observable contract and internal bounds.",
    ),
    "SRC4201_04_62_tensor_result": (
        FORMAL / "62-local-ppn-tensor-ansatz-first-results.md",
        "local_ppn_tensor_ansatz_open_amplitude_required",
        "Tensor ansatz result says amplitudes and PPN observables remain required.",
    ),
    "SRC4201_05_ppn_script": (
        FORMAL / "scripts" / "local_ppn_tensor_ansatz_gate.py",
        "BOUNDS = {",
        "Executable source of local PPN bound values.",
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


def parent_operator_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "LT4201_0_candidate_bulk_action",
            "S_Tbulk = 1/2 int sqrt(-g) [Z_T nabla K_perp nabla K_perp + M_T^2 K_perp^2] + int sqrt(-g) K_perp S_T",
            "would vary to L_T K_perp = S_T if K_perp is a parent field or controlled auxiliary",
            "candidate_contract_not_parent_adopted",
        ),
        (
            "LT4201_1_divergence_constraint",
            "partial_mu K_perp^{mu nu}=0 enforced by projector, constraint, or gauge-fixed transverse sector",
            "prevents double-counting the longitudinal A_loc current-owned part",
            "required_unsigned",
        ),
        (
            "LT4201_2_coercivity",
            "Z_T>0 and M_T^2>=0 with no negative boundary form",
            "gives C_T <= 1/c_T and makes 4200 energy proof quantitative",
            "required_unsigned",
        ),
        (
            "LT4201_3_boundary_domain",
            "Dirichlet/decay/routed Hamiltonian boundary plus no incoming modes",
            "sets B_T=0 and I_T=0 if parent selector owns the domain",
            "required_unsigned",
        ),
        (
            "LT4201_4_kernel_certificate",
            "P_ker K_perp=0 for TT/topological/gauge zero modes",
            "sets Z_T=0",
            "required_unsigned",
        ),
        (
            "LT4201_5_source_projection",
            "P_perp(source/current/sector leakage)=0 or finite sourced norm",
            "sets or bounds S_T",
            "required_unsigned",
        ),
    ]
    return [
        {
            **common(),
            "operator_id": operator_id,
            "mathematical_form": mathematical_form,
            "effect": effect,
            "current_status": current_status,
            "parent_signed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for operator_id, mathematical_form, effect, current_status in rows
    ]


def coefficient_schema_rows() -> List[Dict[str, str]]:
    base = [
        ("C_T", "coercivity/resolvent coefficient", "dimension depends on K norm", "positive finite value from L_T"),
        ("S_T", "transverse source-projection norm", "K-source norm", "zero theorem or finite source row"),
        ("B_T", "boundary obstruction norm", "K-boundary norm", "Z_B/no-flux theorem or finite boundary row"),
        ("I_T", "incoming homogeneous tensor memory norm", "K norm", "no-incoming certificate or finite wave row"),
        ("Z_T", "zero-mode projection norm", "K norm", "kernel certificate or finite zero-mode row"),
    ]
    weights = [(f"W_{observable}^K", f"projection weight from ||K_perp||_E to {observable}", units, "metric/clock/readout projection coefficient") for observable, units, _, _ in PPN_BOUNDS]
    rows = base + weights
    return [
        {
            **common(),
            "symbol": symbol,
            "definition": definition,
            "units": units,
            "required_source": required_source,
            "numeric_value": "MISSING",
            "source_path": "MISSING_PARENT_OR_NUMERIC_INPUT",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for symbol, definition, units, required_source in rows
    ]


def ppn_inequality_rows() -> List[Dict[str, str]]:
    rows = []
    for observable, units, bound, meaning in PPN_BOUNDS:
        weight = f"W_{observable}^K"
        rows.append(
            {
                **common(),
                "observable": observable,
                "bound_value": f"{bound:.12g}",
                "bound_units": units,
                "meaning": meaning,
                "inequality": f"|{weight}| * C_T * (|S_T|+|B_T|+|I_T|+|Z_T|) <= {bound:.12g} {units}",
                "unit_weight_ceiling_for_Knorm": f"{bound:.12g}",
                "required_weight": weight,
                "current_status": "not_scoreable_weight_or_norm_missing",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def smoke_rows() -> List[Dict[str, str]]:
    strictest_dimensionless = min(bound for _, units, bound, _ in PPN_BOUNDS if units == "dimensionless")
    return [
        {
            **common(),
            "case_id": "SMK4201_0_exact_zero_reference",
            "input_state": "C_T finite and S_T=B_T=I_T=Z_T=0",
            "result": "all Kperp PPN rows vanish",
            "score_status": "reference_only_parent_zero_not_signed",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "case_id": "SMK4201_1_current_state",
            "input_state": "C_T,S_T,B_T,I_T,Z_T,W_i^K missing",
            "result": "not scoreable",
            "score_status": "blocked_missing_coefficients",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "case_id": "SMK4201_2_unit_weight_dimensionless_ceiling",
            "input_state": "if all dimensionless W_i^K=1 and units are treated consistently",
            "result": f"need ||K_perp||_E <= {strictest_dimensionless:.12g}; clock_delta_z sets the strictest unit-weight dimensionless ceiling",
            "score_status": "useful_scale_not_claim",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "case_id": "SMK4201_3_symbolic_safe_branch",
            "input_state": "finite sourced coefficients satisfy every observable inequality row",
            "result": "Kperp finite branch would be PPN-safe without exact zero",
            "score_status": "future_scoreable_after_inputs",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision": DECISION,
            "parent_LT_signed": "False",
            "coefficient_vector_complete": "False",
            "ppn_inequality_map_complete": "True",
            "numeric_score_ready": "False",
            "current_route_status": "explicit_bound_contract_ready_inputs_missing",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def claim_firewall_rows() -> List[Dict[str, str]]:
    rows = [
        ("FW4201_0_no_unit_weight_claim", "Unit-weight ceilings are scale diagnostics, not claims about real projection weights."),
        ("FW4201_1_no_zero_from_schema", "A coefficient schema does not prove S_T, B_T, I_T or Z_T vanish."),
        ("FW4201_2_no_PPN_pass_without_weights", "Every PPN inequality needs W_i^K and Kperp norm components before scoring."),
        ("FW4201_3_no_parent_action_by_template", "A candidate quadratic S_K is a contract, not an adopted parent action."),
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
            "summary": "4201 maps the Kperp finite fallback to concrete PPN inequalities and coefficient/source slots; no numeric score is allowed until inputs are filled.",
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
            "why": "The Kperp bound is now scoreable in principle; next step must either parent-sign L_T or provide the first real coefficient/source pack.",
            "include": "Z_T/Z_B/C_T/S_T/B_T/I_T/W_i^K source paths, units, and one PPN inequality smoke row",
            "exclude": "unit-weight public claim, exact zero by no-flux wording, GitHub action",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def all_rows() -> Dict[str, List[Dict[str, str]]]:
    return {
        "P8_Y5_R2FR_4201_SOURCE_REGISTER.csv": source_rows(),
        "P8_Y5_R2FR_4201_PARENT_OPERATOR_CONTRACT.csv": parent_operator_rows(),
        "P8_Y5_R2FR_4201_COEFFICIENT_SCHEMA.csv": coefficient_schema_rows(),
        "P8_Y5_R2FR_4201_PPN_INEQUALITY_MAP.csv": ppn_inequality_rows(),
        "P8_Y5_R2FR_4201_SMOKE_ROWS.csv": smoke_rows(),
        "P8_Y5_R2FR_4201_DECISION.csv": decision_rows(),
        "P8_Y5_R2FR_4201_CLAIM_FIREWALL.csv": claim_firewall_rows(),
        "P8_Y5_R2FR_4201_STATUS.csv": status_rows(),
        "P8_Y5_R2FR_4201_NEXT_TARGET.csv": next_target_rows(),
    }


def write_docs() -> None:
    formal = f"""# 217 - PPC4161 Kperp Finite Coefficient Vector

Marker: `{SPINE_MARKER}`
Checkpoint: `{CHECKPOINT}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint does not prove `K_perp=0` and does not pass PPN. It makes the finite `K_perp` route scoreable in principle.

## Parent Operator Contract

A parent route would need:

```text
S_K = 1/2 int sqrt(-g) [Z_T nabla K_perp nabla K_perp + M_T^2 K_perp^2]
    + int sqrt(-g) K_perp S_T
```

with transverse constraint, positive coercivity, zero/routed boundary, no incoming tensor memory, and trivial kernel. This is a contract, not an adopted parent action.

## Finite Bound To Score

From 4200:

```text
||K_perp||_E <= C_T (|S_T| + |B_T| + |I_T| + |Z_T|).
```

Every local observable must satisfy:

```text
|W_i^K| C_T (|S_T|+|B_T|+|I_T|+|Z_T|) <= bound_i.
```

The strict unit-weight dimensionless ceiling is `1e-16` from `clock_delta_z`, but this is only a scale diagnostic until the real `W_i^K` and units are sourced.

## Verdict

4201 turns the vague instruction “bound Kperp” into a concrete coefficient vector:

```text
C_T, S_T, B_T, I_T, Z_T, W_i^K.
```

The current branch is not numerically score-ready. 4202 must either parent-sign `L_T` or fill the first real source pack for these coefficients.
"""
    checkpoint = f"""# 4201 - Y5 R2FR Kperp Finite Coefficient Vector Or Parent Tensor Operator Source

Decision: `{DECISION}`

4201 maps the 4200 fallback norm to the local PPN gates. The exact-zero theorem remains unsigned, but the finite route is now a clear inequality problem:

```text
|W_i^K| C_T (|S_T|+|B_T|+|I_T|+|Z_T|) <= bound_i.
```

No claim is allowed because all real coefficients are missing. The next work is not another abstract target: either derive the parent tensor operator `L_T`, or source the first actual coefficient pack for `C_T,S_T,B_T,I_T,Z_T,W_i^K`.
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
        f'{CLAIM_ID},local_gr,"The K_perp finite fallback is mapped to explicit PPN inequalities and a coefficient vector, '
        f'but parent L_T and numeric/source coefficient rows remain missing.","4201 source audit, parent operator contract, '
        f'coefficient schema, PPN inequality map, smoke rows, decision row and nonclaim firewall.",'
        f'private_Kperp_bound_contract_nonclaim_coefficients_missing,'
        f'"Parent-sign L_T/coercivity/kernel clauses or fill sourced C_T/S_T/B_T/I_T/Z_T/W_i^K rows.",'
        f'"Unit-weight ceilings or a quadratic action template could be mistaken for a scored PPN pass without real projection weights and source norms."'
    )
    if f"{CLAIM_ID}," not in read_text(CLAIMS_PATH):
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(claim_row + "\n")

    spine_block = f"""### PPC4161 Kperp Finite Coefficient Vector - 4201

Marker: `{SPINE_MARKER}`
Claim register row: `{CLAIM_ID}`

4201 maps the retained `Kperp` fallback into PPN inequalities:

```text
|W_i^K| C_T (|S_T|+|B_T|+|I_T|+|Z_T|) <= bound_i.
```

This makes the branch scoreable once coefficient/source rows exist. It is still nonclaim because `L_T`, `C_T`, obstruction norms, and PPN projection weights are missing."""
    append_once(SPINE_PATH, SPINE_MARKER, spine_block)

    packet_block = f"""## PPC4161 Packet Kperp Finite Coefficient Vector - 4201

Marker: `{PACKET_MARKER}`

Inside the private packet, `Kperp` has a finite coefficient vector:

```text
C_T, S_T, B_T, I_T, Z_T, W_i^K.
```

The packet remains nonclaim until those inputs are parent-derived or source-backed and every PPN inequality passes."""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)


def validate(rows_by_file: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    source = rows_by_file["P8_Y5_R2FR_4201_SOURCE_REGISTER.csv"]
    schema = rows_by_file["P8_Y5_R2FR_4201_COEFFICIENT_SCHEMA.csv"]
    ppn = rows_by_file["P8_Y5_R2FR_4201_PPN_INEQUALITY_MAP.csv"]
    smoke = rows_by_file["P8_Y5_R2FR_4201_SMOKE_ROWS.csv"]
    decision = rows_by_file["P8_Y5_R2FR_4201_DECISION.csv"]
    all_rows_flat = [row for rows in rows_by_file.values() for row in rows]
    symbols = {row["symbol"] for row in schema}
    checks = [
        ("VAL4201_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in source)),
        ("VAL4201_1_source_needles", "all source required text markers found", all(row["required_text_found"] == "True" for row in source)),
        ("VAL4201_2_schema_core", "schema includes C_T,S_T,B_T,I_T,Z_T", {"C_T", "S_T", "B_T", "I_T", "Z_T"}.issubset(symbols)),
        ("VAL4201_3_schema_weights", "schema includes one projection weight per PPN bound", len([s for s in symbols if s.startswith("W_") and s.endswith("^K")]) == len(PPN_BOUNDS)),
        ("VAL4201_4_ppn_rows", "PPN inequality map covers every bound", len(ppn) == len(PPN_BOUNDS)),
        ("VAL4201_5_clock_ceiling", "clock unit-weight ceiling is present", any(row["observable"] == "clock_delta_z" and row["unit_weight_ceiling_for_Knorm"] == "1e-16" for row in ppn)),
        ("VAL4201_6_smoke_blocked", "current smoke row remains blocked", any(row["case_id"] == "SMK4201_1_current_state" and row["score_status"] == "blocked_missing_coefficients" for row in smoke)),
        ("VAL4201_7_decision_nonclaim", "decision says numeric score not ready", decision[0]["numeric_score_ready"] == "False" and decision[0]["claim_allowed"] == "False"),
        ("VAL4201_8_no_claim_flags", "all generated claim flags remain false", all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_rows_flat)),
        ("VAL4201_9_docs_written", "formal and checkpoint docs written", FORMAL_PATH.exists() and DOC_PATH.exists()),
        ("VAL4201_10_claim_register", "claim register contains L-042", CLAIM_ID + "," in read_text(CLAIMS_PATH)),
        ("VAL4201_11_spine_marker", "spine marker present", SPINE_MARKER in read_text(SPINE_PATH)),
        ("VAL4201_12_packet_marker", "packet marker present", PACKET_MARKER in read_text(PACKET_PATH)),
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
    write_csv(SOURCE_DIR / "P8_Y5_BRR545_4201_VALIDATION.csv", validation)
    if not all(row["passed"] == "True" for row in validation):
        failed = [row for row in validation if row["passed"] != "True"]
        raise RuntimeError(f"4201 validation failed: {failed}")
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    write_all()
    print(DECISION)
    print(f"formal={FORMAL_PATH}")
    print(f"checkpoint={DOC_PATH}")
    print(f"validation={SOURCE_DIR / 'P8_Y5_BRR545_4201_VALIDATION.csv'}")
    print("rows=13 validation checks")


if __name__ == "__main__":
    main()
