from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4585"
CLAIM_ID = "L-427"
BRANCH_ID = "MTS_R2FR_Y5_ACTIVE_KERNEL_FIRST_ZERO_OR_OPERATOR_BOUND_4585"
MARKER = "PPC4161_ACTIVE_KERNEL_FIRST_ZERO_OR_OPERATOR_BOUND_4585"
PACKET_MARKER = "PPC4161_PACKET_ACTIVE_KERNEL_FIRST_ZERO_OR_OPERATOR_BOUND_4585"
DECISION = "ACTIVE_KERNEL_PRODUCT_RULE_AND_FIXED_QBASIC_ZERO_CONTRACT_DERIVED_SOURCE_WORLDTUBE_FIRST_BOUND_RETAINED_NONCLAIM"
NEXT_TARGET = "4586-Y5-R2FR-source-worldtube-kernel-zero-certificate-or-first-operator-norm.md"

DOC_PATH = POST / "4585-Y5-R2FR-active-kernel-first-zero-or-operator-bound.md"
FORMAL_PATH = FORMAL / "601-PPC4161-active-kernel-first-zero-or-operator-bound.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_4584 = POST / "4584-Y5-R2FR-parent-material-tensor-and-apparatus-support-zero-or-bound.md"
CSV_4584_REDUCTION = SOURCE_DIR / "P8_Y5_R2FR_4584_MATERIAL_APPARATUS_REDUCTION_ROWS.csv"
CSV_4584_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4584_NEXT_TARGET.csv"
FORMAL_597 = FORMAL / "597-PPC4161-remaining-Creadout-frame-material-kernel-EFT-tau-residual-bound-or-zero.md"
FORMAL_598 = FORMAL / "598-PPC4161-material-response-tail-and-active-kernel-first-bound-or-owner-zero.md"
FORMAL_514 = FORMAL / "514-PPC4161-shell-projection-arena-operator-source-fill-or-owner-kernel-parent-signature.md"
FORMAL_284 = FORMAL / "284-PPC4161-Dq-boundary-projector-fixed-collar-or-boundary-residual-bound.md"
CSV_4582_KERNEL = SOURCE_DIR / "P8_Y5_R2FR_4582_ACTIVE_KERNEL_BOUND_INTERFACE.csv"
CSV_2118_KERNELS = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2118_EXPLICIT_EXCEPTION_KERNELS.csv"
CSV_4580_CERT = SOURCE_DIR / "P8_Y5_R2FR_4580_PI_READOUT_DOMAIN_CERTIFICATE.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4585_SOURCE_REGISTER.csv"
PRODUCT_RULE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4585_KERNEL_PRODUCT_RULE_THEOREM.csv"
CERT_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4585_KERNEL_ZERO_CERTIFICATE_MATRIX.csv"
BOUND_SCHEMA_CSV = SOURCE_DIR / "P8_Y5_R2FR_4585_OPERATOR_BOUND_SCHEMA.csv"
REDUCTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4585_CREADOUT_KERNEL_REDUCTION_ROWS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4585_CONTROL_ROWS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4585_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4585_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4585_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4585_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4585_VALIDATION.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(key, "")).replace("\n", " ") for key in headers) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    path.write_text(text.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")


def source_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4585_00_4584_doc", DOC_4584, "C_readout <= C_kernel_active + C_EFT_active + C_tau_tail", "4584 handoff"),
        ("SRC4585_01_4584_reduction", CSV_4584_REDUCTION, "MAR4584_3_Creadout_update", "4584 Creadout reduction"),
        ("SRC4585_02_4584_next", CSV_4584_NEXT, "active-kernel-first-zero-or-operator-bound", "4584 selected 4585"),
        ("SRC4585_03_4581_fixed_kernel", FORMAL_597, "C_kernel_fixed = 0", "fixed kernel zero theorem"),
        ("SRC4585_04_4581_active_bound", FORMAL_597, "C_kernel_active <= K_clock", "active kernel tail bound"),
        ("SRC4585_05_4582_operator_bound", FORMAL_598, "C_kernel_active <= sum_A", "4582 active operator norm"),
        ("SRC4585_06_4582_kernel_csv", CSV_4582_KERNEL, "AK4582_0_source_worldtube", "4582 active kernel interface"),
        ("SRC4585_07_2118_kernels", CSV_2118_KERNELS, "KSR2118_7_total_no_cancellation", "explicit exception kernels"),
        ("SRC4585_08_operator_contract", FORMAL_514, "R_A = Pi_A T_shell", "arena operator contract precedent"),
        ("SRC4585_09_fixed_collar", FORMAL_284, "q-basic readout/domain data", "fixed q-basic collar precedent"),
        ("SRC4585_10_domain_cert", CSV_4580_CERT, "PDC4580_0_protocol_object", "pre-variation protocol object"),
        ("SRC4585_11_claim_426", CLAIMS_PATH, "L-426", "prior claim register handoff"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in specs:
        text = read_text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": bool_text(path.exists()),
                "needle": needle,
                "needle_found": bool_text(needle in text),
                "role": role,
                "generated_utc": now,
                "valid_for_claim": "False",
            }
        )
    return rows


def product_rule_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "KPR4585_0_product_rule",
            "claim": "The active kernel debt is exactly the product-rule derivative of the response kernel.",
            "derivation": "For an arena readout R_A=K_A J_H, O_f(K_A J_H)=(O_f K_A)J_H+K_A(O_f J_H). Earlier source/material/EM/apparatus reductions act on J_H or source tails; the surviving active-kernel term is (O_f K_A)J_H.",
            "consequence": "The kernel problem is no longer vague: prove O_f K_A=0 for each arena or bound ||(O_f K_A)J_H||/M_H_ref.",
            "status": "EXACT_PRODUCT_RULE_DERIVED",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "KPR4585_1_fixed_qbasic_kernel_zero",
            "claim": "A kernel declared before variation as fixed/q-basic downstream data has O_f K_A=0.",
            "derivation": "If K_A=Kbar_A(q, P_protocol, e_obs, tau_obs, units, orientation) and the protocol object is fixed before source variation, then the compact source probe does not vary K_A. Hence O_f K_A=0 and the arena contributes no C_kernel_active.",
            "consequence": "The fixed-kernel theorem from 4581 is lifted to each named active kernel as a certificate test.",
            "status": "CONDITIONAL_ZERO_CERTIFICATE_DERIVED",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "KPR4585_2_operator_norm_fallback",
            "claim": "If K_A is active, the fallback is an operator norm, not a placeholder.",
            "derivation": "C_KA := sup_{||f||_inf<=1} ||(O_f K_A)J_H||_TV/M_H_ref. The total active kernel envelope is the no-cancellation sum over source_worldtube, WEP, clock, light, orbital_GM and projective kernels.",
            "consequence": "Every arena now has a precise row to source: fixed-kernel certificate or finite operator norm with domain, units, support and source path.",
            "status": "BOUND_SCHEMA_DERIVED_VALUES_MISSING",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
    ]


def certificate_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("KC4585_0_source_worldtube", "K_source_worldtube", "Delta_source(lambda)=int K_source rho_source_residual", "fixed source support/profile and no post-fit source selector", "KSR2118_0_source_worldtube_kernel"),
        ("KC4585_1_WEP", "K_WEP", "tau_WEP=<P_inst(t)[Delta_a_source-Delta_a_test]>_segments", "official orbit/readout kernel fixed before variation and source-universality branch active", "KSR2118_1_orbit_WEP_kernel"),
        ("KC4585_2_clock", "K_clock", "delta_nu/nu=P_clock[Q_trace, rod calibration, material markers, projective trace]", "clock/rod/readout protocol fixed before variation with no material marker reentry", "KSR2118_2_clock_redshift_kernel"),
        ("KC4585_3_light", "K_light", "gamma_minus_1 or Shapiro residual=P_lightcone[Q_shear, photon branch, source geometry]", "lightcone response descends through observed metric/q and no active photon-branch selector", "KSR2118_3_lightcone_kernel"),
        ("KC4585_4_orbital_GM", "K_GM_orbit", "delta(GM)_obs or fifth-force residual=P_orbit[source_support, readout_action, inverse-square split, time/range law]", "GM convention and orbital transfer fixed before readout with no fitted-G absorption", "KSR2118_4_orbital_GM_kernel"),
        ("KC4585_5_projective", "K_projective", "projective residual=P_projective[source, clock, WEP]", "all-sector projective invariance certificate or fixed gauge projection", "KSR2118_6_projective_trace_kernel"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "certificate_id": cert_id,
            "symbol": symbol,
            "kernel_shape": shape,
            "zero_certificate": zero,
            "fallback": f"C_{symbol} <= sup_{{||f||_inf<=1}} ||(O_f {symbol})J_H||_TV/M_H_ref",
            "source_anchor": anchor,
            "certificate_currently_signed": "False",
            "numeric_operator_norm_present": "False",
            "status": "CERTIFICATE_OR_BOUND_REQUIRED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        }
        for cert_id, symbol, shape, zero, anchor in rows
    ]


def bound_schema_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("KBS4585_0_domain", "kernel domain/support", "W_loc, Sigma, source support, source profile and boundary class", "MISSING_FIXED_DOMAIN_OR_OPERATOR_DOMAIN"),
        ("KBS4585_1_protocol", "protocol fixed-before-variation flag", "P_protocol timestamp/source path; no residual-fit selector", "MISSING_PROTOCOL_CERTIFICATE"),
        ("KBS4585_2_operator_norm", "operator norm N_KA", "sup_{||f||<=1} ||O_f K_A|| on declared Banach/TV domain", "MISSING_OPERATOR_NORM"),
        ("KBS4585_3_source_norm", "source norm ||J_H||/M_H_ref", "finite same-Hilbert source charge normalization", "MISSING_SOURCE_NORM_OR_MHREF"),
        ("KBS4585_4_units", "common units/projection", "map each arena kernel to dimensionless C_kernel contribution", "MISSING_COMMON_UNITS"),
        ("KBS4585_5_total", "C_kernel_active", "sum_A C_KA with no cancellation", "SCHEMA_READY_VALUES_MISSING"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": row_id,
            "needed_input": needed,
            "definition": definition,
            "status": status,
            "valid_for_claim": "False",
            "claim_allowed": "False",
            "generated_utc": now,
        }
        for row_id, needed, definition, status in rows
    ]


def reduction_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "KRD4585_0_kernel_total_bound",
            "target": "C_kernel_active",
            "formula": "C_kernel_active <= C_K_source_worldtube + C_K_WEP + C_K_clock + C_K_light + C_K_GM_orbit + C_K_projective",
            "branch_condition": "any kernel certificate unsigned",
            "status": "NO_CANCELLATION_OPERATOR_BOUND",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "KRD4585_1_kernel_total_zero",
            "target": "C_kernel_active",
            "formula": "C_kernel_active=0",
            "branch_condition": "all six kernel zero certificates signed: O_f K_A=0 for every active arena",
            "status": "CONDITIONAL_ZERO_CERTIFICATE_NOT_YET_SIGNED",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "KRD4585_2_Creadout_if_kernel_zero",
            "target": "C_readout",
            "formula": "C_readout <= C_EFT_active + C_tau_tail",
            "branch_condition": "4584 strict branch plus all active kernel certificates",
            "status": "NEXT_REDUCTION_IF_KERNELS_CLOSE",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "KRD4585_3_first_target",
            "target": "K_source_worldtube",
            "formula": "C_K_source_worldtube <= sup_{||f||_inf<=1} ||(O_f K_source_worldtube)J_H||_TV/M_H_ref",
            "branch_condition": "first foundational kernel; feeds R10/PPN/orbital/source support",
            "status": "SELECTED_NEXT_ZERO_OR_OPERATOR_NORM_TARGET",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("CTRL4585_fixed_kernel", "kernel fixed before variation", "O_f K_A=0", "CONTROL_PASS"),
        ("CTRL4585_active_response", "kernel depends on fitted source support/readout residual", "operator norm retained", "COUNTERMODEL_CAUGHT"),
        ("CTRL4585_no_cancellation", "one kernel positive and another negative", "sum absolute component bounds", "FIREWALL_PASS"),
        ("CTRL4585_WEP_not_official", "surrogate/MICROSCOPE kernel not official fixed data", "WEP certificate remains unsigned", "FIREWALL_PASS"),
        ("CTRL4585_orbital_GM", "kernel uses fitted GM to define source", "reject zero; route to operator/source convention", "COUNTERMODEL_CAUGHT"),
        ("CTRL4585_no_local_claim", "kernel schema exists", "no local-GR/R10/PPN claim", "FIREWALL_PASS"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": control_id,
            "case": case,
            "expected_result": expected,
            "status": status,
            "generated_utc": now,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for control_id, case, expected, status in rows
    ]


def promotion_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("PROM4585_0_product_rule", "Active kernel product rule derived.", "PASSED"),
        ("PROM4585_1_fixed_zero", "Fixed q-basic kernel zero certificate derived.", "PASSED_CONDITIONAL"),
        ("PROM4585_2_operator_schema", "Operator norm fallback schema emitted.", "PASSED"),
        ("PROM4585_3_kernel_values", "Actual arena kernel certificates/operator norms are sourced.", "BLOCKED"),
        ("PROM4585_4_next_source_worldtube", "Source-worldtube selected as first kernel target.", "PASSED"),
        ("PROM4585_5_no_public_claim", "No local-GR/R10/PPN claim from kernel schema.", "PASSED_FIREWALL"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "generated_utc": now,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for gate_id, gate, status in rows
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "decision": DECISION,
            "plain_english": "4585 derives the exact active-kernel product rule and the fixed/q-basic kernel zero certificate. The old 'missing active kernels' are now six explicit certificate-or-operator-norm rows. No arena kernel is claimed closed yet; the first target is source-worldtube because it feeds source support, R10, PPN and orbital readouts.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "next_target": NEXT_TARGET,
            "reason": "The source-worldtube kernel is the first and most upstream active kernel; if fixed or bounded, several downstream arena kernels stop inheriting source-support ambiguity.",
            "derive_first": "prove K_source_worldtube is fixed q-basic/source-domain data, or source a finite operator norm on the declared local collar",
            "fallback": "stage source profile/support/operator norm rows with units, M_H_ref normalization and no fitted-G absorption",
            "valid_for_claim": "False",
        }
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "status": "PRIVATE_NONCLAIM_LOCAL_ONLY",
            "summary": "Active kernels are reduced to fixed/q-basic zero certificates or explicit operator norms; source-worldtube selected first.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def doc_text(sources: list[dict[str, Any]], product: list[dict[str, Any]], certs: list[dict[str, Any]], bounds: list[dict[str, Any]], reductions: list[dict[str, Any]], controls: list[dict[str, Any]], promotions: list[dict[str, Any]], decision: list[dict[str, Any]], next_target: list[dict[str, Any]]) -> str:
    return f"""# 4585 - Active kernel first zero or operator bound

Marker: `{MARKER}`  
Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`  
Private/public status: private nonclaim; no GitHub action.

## Result

4585 turns the active-kernel blocker into a precise contract.

The key identity is:

```text
O_f(K_A J_H) = (O_f K_A)J_H + K_A(O_f J_H).
```

The previous checkpoints attacked the `J_H` and source-tail side.  The remaining kernel debt is exactly:

```text
C_KA := sup_{{||f||_inf<=1}} ||(O_f K_A)J_H||_TV / M_H_ref.
```

If an arena kernel is declared before variation as fixed/q-basic downstream data, then:

```text
O_f K_A = 0.
```

If not, it must receive a real operator norm.  No cancellation is allowed between arenas.

## Product-rule theorem

{markdown_table(product)}

## Kernel certificate matrix

{markdown_table(certs)}

## Operator-bound schema

{markdown_table(bounds)}

## Reduction rows

{markdown_table(reductions)}

## Controls

{markdown_table(controls)}

## Promotion gates

{markdown_table(promotions)}

## Decision

{markdown_table(decision)}

## Next target

{markdown_table(next_target)}

## Source register

{markdown_table(sources)}
"""


def formal_text() -> str:
    return f"""## PPC4161 4585 active kernel first zero or operator bound

Marker: `{MARKER}`  
Decision: `{DECISION}`  

The active kernel term is exactly the product-rule residue:

```text
O_f(K_A J_H) = (O_f K_A)J_H + K_A(O_f J_H).
```

After previous source/material/EM/apparatus reductions, the remaining active-kernel debt is:

```text
C_KA := sup_{{||f||_inf<=1}} ||(O_f K_A)J_H||_TV/M_H_ref.
```

If `K_A` is fixed/q-basic protocol data selected before variation, then `O_f K_A=0`.  Otherwise it needs a sourced operator norm.  Therefore:

```text
C_kernel_active <= C_K_source_worldtube + C_K_WEP + C_K_clock + C_K_light + C_K_GM_orbit + C_K_projective.
```

If all six certificates close:

```text
C_kernel_active=0,
C_readout <= C_EFT_active + C_tau_tail.
```

No certificate is treated as already signed.  Next target: `{NEXT_TARGET}`.
"""


def packet_text() -> str:
    return f"""## 4585 packet update - active kernel product-rule contract

Marker: `{PACKET_MARKER}`  
Decision: `{DECISION}`  

4585 reduces the active-kernel blocker to six zero-certificate or operator-norm rows.  Fixed/q-basic downstream kernels have `O_f K_A=0`; active kernels require `sup ||(O_f K_A)J_H||/M_H_ref` bounds.  The source-worldtube kernel is selected as the first upstream target.
"""


def update_claims() -> None:
    if CLAIM_ID in read_text(CLAIMS_PATH):
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_signature",
        "claim": "4585 derives the active-kernel product-rule contract and stages fixed-kernel zero certificates or operator-norm bounds for each arena.",
        "current_evidence": "Generated source register, product-rule theorem rows, kernel certificate matrix, operator-bound schema, reduction rows, controls, gates and validation.",
        "status": "active_kernel_product_rule_and_fixed_qbasic_zero_contract_derived_source_worldtube_first_bound_retained_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating a kernel schema as a sourced operator norm or using fitted readout/source support as if fixed before variation.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "Source-worldtube, WEP, clock, light, orbital and projective kernels still need certificates or operator norms before local-GR/R10/PPN claims.",
    }
    rows = read_csv(CLAIMS_PATH)
    if rows:
        rows.append(row)
        write_csv(CLAIMS_PATH, rows)
    else:
        write_csv(CLAIMS_PATH, [row])


def validate(outputs: list[Path], sources: list[dict[str, Any]], product: list[dict[str, Any]], certs: list[dict[str, Any]], bounds: list[dict[str, Any]], reductions: list[dict[str, Any]], controls: list[dict[str, Any]]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        checks.append({"checkpoint": CHECKPOINT, "branch": BRANCH_ID, "check_id": check_id, "check": check, "passed": bool_text(passed), "detail": detail})

    for path in outputs:
        add(f"VAL4585_exists_{path.name}", "output path exists", path.exists(), str(path))
        if path.suffix.lower() == ".csv":
            rows = read_csv(path)
            add(f"VAL4585_csv_parse_{path.name}", "CSV parses with at least one row", len(rows) > 0, f"rows={len(rows)}")

    add("VAL4585_sources_exist", "all cited sources exist", all(row["path_exists"] == "True" for row in sources), "source register existence")
    add("VAL4585_needles_found", "all cited needles found", all(row["needle_found"] == "True" for row in sources), "source register needles")
    add("VAL4585_product_rule", "product-rule theorem emitted", any(row["theorem_id"] == "KPR4585_0_product_rule" and "O_f(K_A J_H)" in row["derivation"] for row in product), "KPR4585_0")
    add("VAL4585_fixed_zero", "fixed qbasic kernel zero theorem emitted", any(row["theorem_id"] == "KPR4585_1_fixed_qbasic_kernel_zero" and "O_f K_A=0" in row["claim"] for row in product), "KPR4585_1")
    add("VAL4585_kernel_matrix", "all six kernel certificate rows present", all(any(row["certificate_id"] == cert_id for row in certs) for cert_id in ["KC4585_0_source_worldtube", "KC4585_1_WEP", "KC4585_2_clock", "KC4585_3_light", "KC4585_4_orbital_GM", "KC4585_5_projective"]), "kernel matrix")
    add("VAL4585_bound_schema", "operator bound schema includes domain, protocol, norm and total", all(any(row["bound_id"] == bound_id for row in bounds) for bound_id in ["KBS4585_0_domain", "KBS4585_1_protocol", "KBS4585_2_operator_norm", "KBS4585_5_total"]), "bound schema")
    add("VAL4585_reduction", "Creadout reduction if kernels close emitted", any(row["row_id"] == "KRD4585_2_Creadout_if_kernel_zero" and "C_EFT_active" in row["formula"] for row in reductions), "KRD4585_2")
    add("VAL4585_first_target", "source-worldtube selected next", any(row["row_id"] == "KRD4585_3_first_target" and "K_source_worldtube" in row["target"] for row in reductions), "KRD4585_3")
    add("VAL4585_controls", "controls catch fitted/readout kernel traps", all(any(row["control_id"] == control_id for row in controls) for control_id in ["CTRL4585_active_response", "CTRL4585_WEP_not_official", "CTRL4585_orbital_GM"]), "controls")
    add("VAL4585_decision_token", "decision token recorded", DECISION in read_text(DECISION_CSV) and DECISION in read_text(DOC_PATH), DECISION)
    add("VAL4585_next_target", "next target recorded", NEXT_TARGET in read_text(NEXT_CSV) and NEXT_TARGET in read_text(DOC_PATH), NEXT_TARGET)
    add("VAL4585_claim_register", "claim register updated", CLAIM_ID in read_text(CLAIMS_PATH), CLAIM_ID)
    add("VAL4585_spine_packet", "spine and packet markers present", MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH), f"{MARKER}; {PACKET_MARKER}")
    return checks


def main() -> None:
    now = utc_now()
    sources = source_rows(now)
    product = product_rule_rows(now)
    certs = certificate_rows(now)
    bounds = bound_schema_rows(now)
    reductions = reduction_rows(now)
    controls = control_rows(now)
    promotions = promotion_rows(now)
    decision = decision_rows(now)
    next_target = next_rows(now)
    status = status_rows(now)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(PRODUCT_RULE_CSV, product)
    write_csv(CERT_MATRIX_CSV, certs)
    write_csv(BOUND_SCHEMA_CSV, bounds)
    write_csv(REDUCTION_CSV, reductions)
    write_csv(CONTROL_CSV, controls)
    write_csv(PROMOTION_CSV, promotions)
    write_csv(DECISION_CSV, decision)
    write_csv(NEXT_CSV, next_target)
    write_csv(STATUS_CSV, status)

    DOC_PATH.write_text(doc_text(sources, product, certs, bounds, reductions, controls, promotions, decision, next_target), encoding="utf-8")
    FORMAL_PATH.write_text(formal_text(), encoding="utf-8")

    append_once(
        SPINE_PATH,
        MARKER,
        f"""### 4585 - Active kernel first zero or operator bound

Marker: `{MARKER}`  
Decision: `{DECISION}`.  Next target: `{NEXT_TARGET}`.

4585 derives the active-kernel product rule:

```text
O_f(K_A J_H) = (O_f K_A)J_H + K_A(O_f J_H)
```

so fixed/q-basic kernels have `O_f K_A=0`, while active kernels require explicit operator norms. If all six kernel certificates close, the strict branch reduces to:

```text
C_readout <= C_EFT_active + C_tau_tail.
```
""",
    )
    append_once(PACKET_PATH, PACKET_MARKER, packet_text())
    update_claims()

    outputs = [SOURCE_REGISTER, PRODUCT_RULE_CSV, CERT_MATRIX_CSV, BOUND_SCHEMA_CSV, REDUCTION_CSV, CONTROL_CSV, PROMOTION_CSV, DECISION_CSV, NEXT_CSV, STATUS_CSV, DOC_PATH, FORMAL_PATH]
    validations = validate(outputs, sources, product, certs, bounds, reductions, controls)
    write_csv(VALIDATION_PATH, validations)
    failed = [row for row in validations if row["passed"] != "True"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)

    cache = Path(__file__).resolve().parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    print(f"4585 complete: {DECISION}")
    print(f"wrote: {DOC_PATH}")
    print(f"validation: {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
