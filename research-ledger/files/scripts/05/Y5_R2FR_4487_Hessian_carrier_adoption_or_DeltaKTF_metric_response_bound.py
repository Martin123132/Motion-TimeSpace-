from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from hessian_carrier_metric_response_gate import (  # noqa: E402
    adoption_fork_rows,
    claim_gate_rows,
    decision_ledger_rows,
    hessian_readout_rows,
    normalization_rows,
    ph_bound_rows,
    read_csv,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4487"
CLAIM_ID = "L-329"
MARKER = "PPC4161_HESSIAN_CARRIER_ADOPTION_OR_DELTAKTF_METRIC_RESPONSE_BOUND_4487"
PACKET_MARKER = "PPC4161_PACKET_HESSIAN_CARRIER_ADOPTION_OR_DELTAKTF_METRIC_RESPONSE_BOUND_4487"
DECISION = "HESSIAN_CARRIER_NOT_METRIC_NULL_ON_IDENTITY_READOUT_CHIH_NORMALIZATION_AND_PH_BOUND_ROUTE_DERIVED_NONCLAIM"
NEXT_TARGET = "4488-Y5-R2FR-PH-source-profile-row-or-parent-zero-transfer-upgrade.md"

FORMAL_PATH = FORMAL / "503-PPC4161-Hessian-carrier-adoption-or-DeltaKTF-metric-response-bound.md"
DOC_PATH = POST / "4487-Y5-R2FR-Hessian-carrier-adoption-or-DeltaKTF-metric-response-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4487_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4487_SOURCE_REGISTER.csv"
READOUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4487_HESSIAN_METRIC_READOUT.csv"
NORMALIZATION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4487_CHIH_PH_NORMALIZATION.csv"
ADOPTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4487_HESSIAN_ADOPTION_FORK.csv"
BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4487_PH_SLIP_BOUND_ROWS.csv"
DECISION_LEDGER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4487_DECISION_LEDGER.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4487_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4487_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4487_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4487_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "hessian_carrier_metric_response_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4487_Hessian_carrier_adoption_or_DeltaKTF_metric_response_bound.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

FORMAL_502 = FORMAL / "502-PPC4161-K2-source-derivative-inventory-sweep-or-first-M2K2-input-row.md"
NEXT_4486 = SOURCE_DIR / "P8_Y5_R2FR_4486_NEXT_TARGET.csv"
M2_4486 = SOURCE_DIR / "P8_Y5_R2FR_4486_FIRST_M2K2_INPUT_ROW.csv"
DTF_4486 = SOURCE_DIR / "P8_Y5_R2FR_4486_DELTAKTF_LEAKAGE_INPUT_ROW.csv"
DOC_3181 = POST / "3181-Y5-R2FR-exterior-Hessian-tidal-footprint-or-metric-null-bound-under-AX1090.md"
DER_3181 = SOURCE_DIR / "P8_Y5_R2FR_3181_EXTERIOR_HESSIAN_TIDAL_DERIVATION.csv"
MNG_3181 = SOURCE_DIR / "P8_Y5_R2FR_3181_METRIC_NULL_GATE.csv"
DOC_3182 = POST / "3182-Y5-R2FR-metric-readout-of-tracefree-Hessian-carrier-or-tidal-response-coefficient-under-AX1090.md"
READ_3182 = SOURCE_DIR / "P8_Y5_R2FR_3182_WEAK_FIELD_READOUT_DERIVATION.csv"
MNA_3182 = SOURCE_DIR / "P8_Y5_R2FR_3182_METRIC_NULL_AUDIT.csv"
DOC_3183 = POST / "3183-Y5-R2FR-Hessian-slip-amplitude-zero-theorem-or-J2-PPN-bound-under-AX1090.md"
SIGMA_3183 = SOURCE_DIR / "P8_Y5_R2FR_3183_SIGMA_NORMAL_FORM.csv"
J2_3183 = SOURCE_DIR / "P8_Y5_R2FR_3183_J2_SLIP_PRESSURE_BOUNDS.csv"
DOC_3184 = POST / "3184-Y5-R2FR-SigmaH-parent-owner-or-slip-bound-runner-under-AX1090.md"
OWNER_3184 = SOURCE_DIR / "P8_Y5_R2FR_3184_SIGMAH_PARENT_OWNER_LEDGER.csv"
RUN_3184 = SOURCE_DIR / "P8_Y5_R2FR_3184_SIGMAH_SLIP_BOUND_RUNNER.csv"
DOC_3185 = POST / "3185-Y5-R2FR-chiH-parent-variation-zero-or-order-estimate-under-AX1090.md"
CHI_3185 = SOURCE_DIR / "P8_Y5_R2FR_3185_CHIH_ORDER_DERIVATION.csv"
PV_3185 = SOURCE_DIR / "P8_Y5_R2FR_3185_PARENT_VARIATION_STATUS.csv"
DOC_3186 = POST / "3186-Y5-R2FR-source-owned-PH-amplitude-or-slip-transfer-bound-under-AX1090.md"
PH_3186 = SOURCE_DIR / "P8_Y5_R2FR_3186_PH_AMPLITUDE_MARGIN_RUNNER.csv"
GAPS_3186 = SOURCE_DIR / "P8_Y5_R2FR_3186_PH_SOURCE_OWNER_GAPS.csv"
DOC_3187 = POST / "3187-Y5-R2FR-kappaSTF-cExt-source-profile-estimator-or-parent-zero-under-AX1090.md"
EST_3187 = SOURCE_DIR / "P8_Y5_R2FR_3187_PROFILE_ESTIMATOR_DERIVATION.csv"
ZERO_3187 = SOURCE_DIR / "P8_Y5_R2FR_3187_PARENT_ZERO_AUDIT.csv"
CK2_3165 = SOURCE_DIR / "P8_Y5_R2FR_3165_K2_UNIT_RESIDUAL_COEFFICIENT.csv"


def text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for line_number, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return line_number
    return 0


def md(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def table(rows: Sequence[Mapping[str, object]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    output = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        output.append("| " + " | ".join(md(row.get(header, "")) for header in headers) + " |")
    return "\n".join(output)


def csv_lookup(path: Path, key: str, key_value: str, column: str) -> str:
    for row in read_csv(path):
        if row.get(key) == key_value:
            return row[column]
    raise KeyError(f"missing {key}={key_value} in {path}")


def numeric_inputs() -> Dict[str, float]:
    c_k2_unit = float(csv_lookup(CK2_3165, "unit_id", "KU3165_0_definition", "value"))
    return {"c_k2_unit": c_k2_unit, "chi_h": 2.0 * c_k2_unit / 25.0}


def source_specs() -> List[Dict[str, object]]:
    return [
        {"source_id": "SRC4487_00_next4486", "ref": NEXT_4486, "needle": "4487-Y5-R2FR-Hessian-carrier-adoption-or-DeltaKTF-metric-response-bound.md", "role": "4486 selected Hessian carrier adoption or DeltaKTF bound."},
        {"source_id": "SRC4487_01_formal502", "ref": FORMAL_502, "needle": "DeltaK_TF^{ij}", "role": "4486 precise leakage frontier."},
        {"source_id": "SRC4487_02_m2_4486", "ref": M2_4486, "needle": "M2I4486_0_projected_hessian_moment", "role": "4486 projected Hessian M2 input."},
        {"source_id": "SRC4487_03_dtf4486", "ref": DTF_4486, "needle": "DTF4486_0_definition", "role": "4486 DeltaKTF leakage row."},
        {"source_id": "SRC4487_04_doc3181", "ref": DOC_3181, "needle": "<K_L:K_L>_Omega = 336 C^2 r^-10", "role": "3181 exterior tensor footprint."},
        {"source_id": "SRC4487_05_der3181", "ref": DER_3181, "needle": "DER3181_4_angular_average", "role": "3181 machine footprint row."},
        {"source_id": "SRC4487_06_mng3181", "ref": MNG_3181, "needle": "MN3181_1_metric_readout", "role": "3181 metric-null gate."},
        {"source_id": "SRC4487_07_doc3182", "ref": DOC_3182, "needle": "Psi - Phi = 2 Sigma_H phi_ext", "role": "3182 weak-field slip response."},
        {"source_id": "SRC4487_08_read3182", "ref": READ_3182, "needle": "RO3182_4_operator_response_coefficient", "role": "3182 response coefficient row."},
        {"source_id": "SRC4487_09_mna3182", "ref": MNA_3182, "needle": "MN3182_0_identity_readout", "role": "3182 metric-null audit."},
        {"source_id": "SRC4487_10_doc3183", "ref": DOC_3183, "needle": "A_slip_surface = 2|Sigma_H|", "role": "3183 slip amplitude normal form."},
        {"source_id": "SRC4487_11_sigma3183", "ref": SIGMA_3183, "needle": "NF3183_3_candidate_factorization", "role": "3183 SigmaH factorization."},
        {"source_id": "SRC4487_12_j23183", "ref": J2_3183, "needle": "JP3183_CJ3170_2_Rozelot_half_range_proxy", "role": "3183 tight slip pressure row."},
        {"source_id": "SRC4487_13_doc3184", "ref": DOC_3184, "needle": "Sigma_H = chi_H P_H", "role": "3184 parent-normalization runner."},
        {"source_id": "SRC4487_14_owner3184", "ref": OWNER_3184, "needle": "OWN3184_1_chiH", "role": "3184 chiH owner ledger."},
        {"source_id": "SRC4487_15_run3184", "ref": RUN_3184, "needle": "RUN3184_BC3183_PR3180_CJ3170_2_Rozelot_half_range_proxy", "role": "3184 chiH pressure runner."},
        {"source_id": "SRC4487_16_doc3185", "ref": DOC_3185, "needle": "chi_H,natural = 2 C_K2_unit / 25", "role": "3185 chiH normalization derivation."},
        {"source_id": "SRC4487_17_chi3185", "ref": CHI_3185, "needle": "CHI3185_3_slip_amplitude_match", "role": "3185 machine chiH row."},
        {"source_id": "SRC4487_18_pv3185", "ref": PV_3185, "needle": "PV3185_3_next_live_object", "role": "3185 live P_H object."},
        {"source_id": "SRC4487_19_doc3186", "ref": DOC_3186, "needle": "the scary chi_H factor is explained", "role": "3186 PH amplitude fork."},
        {"source_id": "SRC4487_20_ph3186", "ref": PH_3186, "needle": "PH3186_CJ3170_2_Rozelot_half_range_proxy", "role": "3186 PH margin runner."},
        {"source_id": "SRC4487_21_gaps3186", "ref": GAPS_3186, "needle": "GAP3186_0_sK2", "role": "3186 source-owner gaps."},
        {"source_id": "SRC4487_22_doc3187", "ref": DOC_3187, "needle": "P_H = -(5/4) s_K2 kappa_STF I4_D2", "role": "3187 profile estimator."},
        {"source_id": "SRC4487_23_est3187", "ref": EST_3187, "needle": "EST3187_1_PH_signed_estimator", "role": "3187 machine profile estimator."},
        {"source_id": "SRC4487_24_zero3187", "ref": ZERO_3187, "needle": "ZERO3187_3_transition_cancellation", "role": "3187 zero/cancellation audit."},
        {"source_id": "SRC4487_25_ck2", "ref": CK2_3165, "needle": "KU3165_0_definition", "role": "C_K2_unit numeric owner."},
        {"source_id": "SRC4487_26_gate", "ref": GATE_PATH, "needle": "def hessian_readout_rows", "role": "4487 helper gate."},
        {"source_id": "SRC4487_27_generator", "ref": GENERATOR_PATH, "needle": 'CHECKPOINT = "4487"', "role": "4487 generator script."},
    ]


def source_rows() -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for spec in source_specs():
        source_path = Path(spec["ref"])
        needle = str(spec["needle"])
        line_number = line_of(source_path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": spec["source_id"],
                "source_kind": "local",
                "source_ref": str(source_path),
                "local_path_exists": source_path.exists(),
                "needle": needle,
                "needle_found": line_number > 0,
                "line_number": line_number,
                "role": spec["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "proof_result": "same-frame identity readout makes K_L a non-null public slip source; metric-null route fails unless Sigma_H=0 or parent improvement/solder theorem overrides it",
            "fallback_result": "finite route reduced to Sigma_H=chi_H P_H, chi_H=2*C_K2_unit/25, P_H=-(5/4)s_K2*kappa_STF*I4_D2 with nonclaim pressure rows",
            "claim_status": "private_nonclaim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "identity_readout_metric_null": "fails",
            "natural_chi_H": "2*C_K2_unit/25",
            "live_source_product": "P_H=s_K2*kappa_STF*c_ext=-(5/4)s_K2*kappa_STF*I4_D2",
            "local_GR_claim": False,
            "sharpest_open_clause": "source_owned_P_H_or_parent_zero_and_slip_transfer",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4487_0",
            "target": NEXT_TARGET,
            "objective": "Source-own P_H through I4_D2/N4_D2 and s_K2*kappa_STF, or prove a parent zero/improvement theorem; then upgrade the slip transfer from pressure proxy to arena-bound rows.",
            "derive_first": "derive parent source profile/coupling rows for P_H or exact Sigma_H=0",
            "fallback": "run source-profile prior grid and transfer-bound upgrade with all rows nonclaim",
            "risk": "treating order-one P_H smoke safety or pressure proxy as a public local-GR pass",
            "valid_for_claim": False,
        }
    ]


def append_section_once(path: Path, marker: str, title: str, body: str) -> None:
    current = text(path)
    if marker in current:
        return
    addition = f"\n\n## {title}\n\nMarker: `{marker}`  \n{body}\n"
    write_text(path, current.rstrip() + addition + "\n")


def update_claims_register() -> None:
    rows = read_csv(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    rows.append(
        {
            "claim_id": CLAIM_ID,
            "domain": "local_gr_newton_r10_scalar_source_coupling",
            "claim": "4487 shows that the Hessian carrier is not metric-null under same-frame identity readout; it sources public gravitational slip. The finite branch is reduced to Sigma_H=chi_H P_H with chi_H=2*C_K2_unit/25 and P_H=-(5/4)s_K2*kappa_STF*I4_D2, while local-GR/J2/PPN claims remain blocked.",
            "current_evidence": "4487 source register, Hessian readout rows, chiH/PH normalization rows, adoption fork, PH slip pressure rows, claim gates, decision/status/next CSVs and validation.",
            "status": "private_hessian_carrier_non_null_slip_response_and_PH_bound_route_nonclaim",
            "next_test": NEXT_TARGET,
            "key_risk": "using the pressure proxy or order-one PH smoke margin as a claim before source ownership, DeltaKTF leakage, and slip transfer are signed.",
            "sector": "local_gr_newton_r10_scalar_source_coupling",
            "evidence": str(FORMAL_PATH),
            "next_action": NEXT_TARGET,
            "risk": "K_L adoption, parent zero theorem, source-owned P_H, DeltaKTF leakage and arena transfer remain unsigned",
        }
    )
    write_csv(CLAIMS_PATH, rows)


def formal_body(
    sources: Sequence[Mapping[str, object]],
    readout_rows: Sequence[Mapping[str, object]],
    norm_rows: Sequence[Mapping[str, object]],
    fork_rows: Sequence[Mapping[str, object]],
    bound_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    tight_bound = bound_rows[-1]["P_H_bound_from_slip"]
    return f"""# 503 PPC4161 - Hessian Carrier Adoption Or DeltaKTF Metric Response Bound

Private checkpoint: `{CHECKPOINT}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Generated UTC: `{STAMP}`

## Result

4487 decides the Hessian carrier fork under the same-frame identity readout.

The old safe-looking fact still holds:

```text
D2[C r^-3] = 0.
```

But it is not enough. The full exterior Hessian has:

```text
<K_L:K_L>_Omega = 336 C^2 r^-10.
```

And the public weak-field metric reads it as slip:

```text
G_ij^(1) = partial_i partial_j(Psi-Phi),
K_L,ij = 2 partial_i partial_j phi_ext,
G_ij^(1)=Sigma_H K_L,ij
=> Psi-Phi = 2 Sigma_H r^-3 P2.
```

So on the identity-readout branch, `K_L` is **not metric-null**. The zero route must prove `Sigma_H=0`, a parent improvement/boundary silence theorem, or a nontrivial coframe/solder map.

The finite route is now clean:

```text
Sigma_H = chi_H P_H,
P_H := s_K2 kappa_STF c_ext,
chi_H = 2 C_K2_unit / 25 = {norm_rows[2]["value"]}.
```

The live source-profile estimator is:

```text
I4_D2 = -4 c_ext/5,
P_H = -(5/4) s_K2 kappa_STF I4_D2.
```

The tight current pressure row allows:

```text
|P_H| <= {tight_bound}.
```

This is not a public local-GR pass, but it is a genuine narrowing: the problem is now `P_H` source ownership plus slip/arena transfer, not a mysterious missing metric coefficient.

## Hessian Metric Readout

{table(readout_rows)}

## ChiH And PH Normalization

{table(norm_rows)}

## Hessian Adoption Fork

{table(fork_rows)}

## PH Slip Bound Rows

{table(bound_rows)}

## Decision Ledger

{table(ledger)}

## Claim Gates

{table(gates)}

## Status

{table(statuses)}

## Next Target

{table(next_targets)}

## Source Register

{table(sources)}

## Decision Row

{table(decisions)}
"""


def post_body(
    sources: Sequence[Mapping[str, object]],
    readout_rows: Sequence[Mapping[str, object]],
    norm_rows: Sequence[Mapping[str, object]],
    fork_rows: Sequence[Mapping[str, object]],
    bound_rows: Sequence[Mapping[str, object]],
    ledger: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4487 Y5/R2FR - Hessian Carrier Adoption Or DeltaKTF Metric Response Bound

Private post-checkpoint mirror for:

`{FORMAL_PATH}`

## What Actually Moved

4487 uses the old 3181-3187 algebra to decide the current Hessian fork. Under same-frame identity readout, `K_L` is not metric-null: it sources `Psi-Phi=2 Sigma_H r^-3 P2`. The scary `chi_H` is not arbitrary fine tuning; it is `2*C_K2_unit/25`. The next live object is the source product `P_H=-(5/4)s_K2*kappa_STF*I4_D2` plus a real slip transfer.

## Readout

{table(readout_rows)}

## Normalization

{table(norm_rows)}

## Fork And Bounds

{table(fork_rows)}

{table(bound_rows)}

## Gates And Decisions

{table(gates)}

{table(ledger)}

{table(decisions)}

## Status And Next Target

{table(statuses)}

{table(next_targets)}

## Sources

{table(sources)}
"""


def validate(
    sources: Sequence[Mapping[str, object]],
    readout_rows: Sequence[Mapping[str, object]],
    norm_rows: Sequence[Mapping[str, object]],
    fork_rows: Sequence[Mapping[str, object]],
    bound_rows: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
    csv_paths: Sequence[Path],
) -> List[Dict[str, object]]:
    validations: List[Dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append({"checkpoint": CHECKPOINT, "check_id": check_id, "passed": passed, "detail": detail, "valid_for_claim": False})

    add("VAL4487_0_sources_exist_and_needles_found", all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources), "every cited source path exists and its needle is found")
    add("VAL4487_1_metric_readout_written", any(row.get("readout_id") == "HMR4487_1_identity_metric_readout" for row in readout_rows), "same-frame metric readout row exists")
    add("VAL4487_2_metric_null_fails_conditionally", any(row.get("readout_id") == "HMR4487_2_metric_null_verdict" and "METRIC_NULL_FAILS" in str(row.get("status")) for row in readout_rows), "metric-null is not overclaimed")
    add("VAL4487_3_chiH_natural_written", any(row.get("norm_id") == "NORM4487_2_chiH_natural" and "2.875013085986371e-25" in str(row.get("value")) for row in norm_rows), "natural chiH row exists")
    add("VAL4487_4_profile_estimator_written", any(row.get("norm_id") == "NORM4487_3_profile_estimator" and "I4_D2" in str(row.get("formula")) for row in norm_rows), "P_H profile estimator exists")
    add("VAL4487_5_pressure_rows_imported", len(bound_rows) >= 3 and any(row.get("bound_name") == "solar_J2_half_range_proxy" for row in bound_rows), "P_H pressure rows exist")
    add("VAL4487_6_claim_gates_block_local_GR", all(str(row.get("claim_allowed")).lower() == "false" for row in gates), "claim gates block promotion")
    add(
        "VAL4487_7_no_generated_claim_rows",
        all(
            str(row.get("valid_for_claim")).lower() == "false"
            for group in [sources, readout_rows, norm_rows, fork_rows, bound_rows, gates, decisions, statuses, next_targets]
            for row in group
        ),
        "all generated rows remain private/nonclaim",
    )
    csv_ok = True
    csv_detail: List[str] = []
    for csv_path in csv_paths:
        try:
            parsed_rows = read_csv(csv_path)
            csv_detail.append(f"{csv_path.name}:{len(parsed_rows)}")
        except Exception as exc:  # pragma: no cover
            csv_ok = False
            csv_detail.append(f"{csv_path.name}:ERROR:{exc}")
    add("VAL4487_8_csvs_parse", csv_ok, "; ".join(csv_detail))
    add("VAL4487_9_docs_written", FORMAL_PATH.exists() and DOC_PATH.exists(), "formal and post checkpoint docs exist")
    add("VAL4487_10_claim_register_updated", any(row.get("claim_id") == CLAIM_ID for row in read_csv(CLAIMS_PATH)), "claims register contains L-329")
    add("VAL4487_11_spine_and_packet_updated", MARKER in text(SPINE_PATH) and PACKET_MARKER in text(PACKET_PATH), "spine and packet contain 4487 markers")
    add("VAL4487_12_next_target_selected", bool(next_targets) and next_targets[0].get("target") == NEXT_TARGET, NEXT_TARGET)
    add("VAL4487_13_pycache_removed", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generation")
    return validations


def main() -> None:
    inputs = numeric_inputs()
    sources = source_rows()
    readout_rows = hessian_readout_rows()
    norm_rows = normalization_rows(inputs["c_k2_unit"], inputs["chi_h"])
    fork_rows = adoption_fork_rows()
    bound_rows = ph_bound_rows(read_csv(PH_3186))
    ledger = decision_ledger_rows(NEXT_TARGET)
    gates = claim_gate_rows(sources, readout_rows, norm_rows, fork_rows, bound_rows)
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(READOUT_CSV, readout_rows)
    write_csv(NORMALIZATION_CSV, norm_rows)
    write_csv(ADOPTION_CSV, fork_rows)
    write_csv(BOUND_CSV, bound_rows)
    write_csv(DECISION_LEDGER_CSV, ledger)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)

    write_text(FORMAL_PATH, formal_body(sources, readout_rows, norm_rows, fork_rows, bound_rows, ledger, gates, decisions, statuses, next_targets))
    write_text(DOC_PATH, post_body(sources, readout_rows, norm_rows, fork_rows, bound_rows, ledger, gates, decisions, statuses, next_targets))
    update_claims_register()

    append_section_once(
        SPINE_PATH,
        MARKER,
        "4487 Hessian Carrier Metric Readout",
        "4487 decides the Hessian-carrier fork under same-frame identity readout: `D2[C r^-3]=0` does not mean metric silence, because the full carrier has `<K_L:K_L>_Omega=336 C^2 r^-10` and sources `Psi-Phi=2 Sigma_H r^-3 P2`. The finite branch reduces to `Sigma_H=chi_H P_H`, `chi_H=2 C_K2_unit/25`, and `P_H=-(5/4)s_K2 kappa_STF I4_D2`. Local-GR remains nonclaim until `P_H`, parent-zero/improvement, `DeltaK_TF`, and slip transfer are sourced.",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        "4487 Packet Integration",
        "The private packet now treats the Hessian carrier as a non-null slip source on the identity-readout branch, not as an automatically silent improvement. The apparent `chi_H` suppression is just the K2 metric normalization; the next concrete object is source-owned `P_H` or an exact parent-zero/improvement theorem.",
    )

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    csv_paths = [SOURCE_REGISTER, READOUT_CSV, NORMALIZATION_CSV, ADOPTION_CSV, BOUND_CSV, DECISION_LEDGER_CSV, CLAIM_GATES_CSV, DECISION_CSV, STATUS_CSV, NEXT_CSV]
    validations = validate(sources, readout_rows, norm_rows, fork_rows, bound_rows, gates, decisions, statuses, next_targets, csv_paths)
    write_csv(VALIDATION_PATH, validations)

    failed = [row for row in validations if str(row.get("passed")).lower() != "true"]
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Generated {CHECKPOINT}: {FORMAL_PATH}")
    print(f"Validation: {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
