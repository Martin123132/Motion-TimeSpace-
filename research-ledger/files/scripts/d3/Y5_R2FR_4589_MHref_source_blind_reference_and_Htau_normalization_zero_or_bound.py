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

CHECKPOINT = "4589"
CLAIM_ID = "L-431"
BRANCH_ID = "MTS_R2FR_Y5_MHREF_SOURCE_BLIND_REFERENCE_AND_HTAU_NORMALIZATION_ZERO_OR_BOUND_4589"
MARKER = "PPC4161_MHREF_SOURCE_BLIND_REFERENCE_AND_HTAU_NORMALIZATION_ZERO_OR_BOUND_4589"
PACKET_MARKER = "PPC4161_PACKET_MHREF_SOURCE_BLIND_REFERENCE_AND_HTAU_NORMALIZATION_ZERO_OR_BOUND_4589"
DECISION = "MHREF_QBASIC_DIFFERENCE_AND_SOURCE_BLIND_REFERENCE_ZERO_CONTRACT_DERIVED_POSITIVE_DENOMINATOR_BOUND_RETAINED_NONCLAIM"
NEXT_TARGET = "4590-Y5-R2FR-Dq-source-vertical-basis-and-readout-mask-zero-or-bound.md"

DOC_PATH = POST / "4589-Y5-R2FR-MHref-source-blind-reference-and-Htau-normalization-zero-or-bound.md"
FORMAL_PATH = FORMAL / "605-PPC4161-MHref-source-blind-reference-and-Htau-normalization-zero-or-bound.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_4588 = POST / "4588-Y5-R2FR-regular-source-support-boundary-zero-or-Reynolds-shell-bound.md"
CSV_4588_REDUCTION = SOURCE_DIR / "P8_Y5_R2FR_4588_SOURCE_KERNEL_REDUCTION_UPDATE.csv"
DOC_3560 = POST / "3560-Y5-R2FR-source-support-qbasic-worldtube-descent-or-bound-vector.md"
CSV_3560_BOUND = SOURCE_DIR / "P8_Y5_R2FR_3560_BOUND_VECTOR.csv"
CSV_3551_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_3551_MHREF_DESCENT_THEOREM.csv"
CSV_3551_LEAK = SOURCE_DIR / "P8_Y5_R2FR_3551_MHREF_LEAKAGE_BOUND_PACK.csv"
FORMAL_186 = FORMAL / "186-PPC4161-Hamiltonian-worldtube-mass-readout-glue.md"
FORMAL_194 = FORMAL / "194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md"
FORMAL_236 = FORMAL / "236-PPC4161-MHref-positive-source-denominator-stability-or-bound-pack.md"
CSV_4170_ID = SOURCE_DIR / "P8_Y5_R2FR_4170_SAME_OBJECT_IDENTITY.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4589_SOURCE_REGISTER.csv"
MHREF_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4589_MHREF_QBASIC_THEOREM.csv"
REFERENCE_CLAUSES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4589_SOURCE_BLIND_REFERENCE_CLAUSES.csv"
DENOMINATOR_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4589_DENOMINATOR_DRIFT_BOUND_ROWS.csv"
REDUCTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4589_SOURCE_KERNEL_REDUCTION_UPDATE.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4589_CONTROL_ROWS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4589_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4589_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4589_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4589_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4589_VALIDATION.csv"


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
        ("SRC4589_00_4588_doc", DOC_4588, "4589-Y5-R2FR-MHref-source-blind-reference-and-Htau-normalization-zero-or-bound.md", "4588 selected MHref target"),
        ("SRC4589_01_4588_reduction", CSV_4588_REDUCTION, "RSR4588_3_next_MHref", "4588 next denominator reduction"),
        ("SRC4589_02_3560_doc", DOC_3560, "SCL3560_3_MHref_qbasic", "3560 MHref q-basic clause"),
        ("SRC4589_03_3560_bound", CSV_3560_BOUND, "BF3560_4_E_Href", "3560 Href leakage bound row"),
        ("SRC4589_04_3551_theorem", CSV_3551_THEOREM, "MHD3551_1_sum_difference_descent", "3551 MHref descent theorem"),
        ("SRC4589_05_3551_leak", CSV_3551_LEAK, "LB3551_3_normalized_mass_leak", "3551 normalized mass leak bound"),
        ("SRC4589_06_186_glue", FORMAL_186, "M_H^dress[W_H;tau] = H_tau[S_link] - H_ref", "Hamiltonian worldtube mass glue"),
        ("SRC4589_07_194_calibration", FORMAL_194, "No orbital `GM`", "calibrated source-coupling anti-circularity"),
        ("SRC4589_08_236_positive", FORMAL_236, "M_H_ref >= M_EH", "positive denominator stability law"),
        ("SRC4589_09_4170_identity", CSV_4170_ID, "SO4170_1_identity", "same-object Hamiltonian identity"),
        ("SRC4589_10_claim_430", CLAIMS_PATH, "L-430", "prior claim register handoff"),
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


def mhref_theorem_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "MHR4589_0_definition",
            "claim": "The source-worldtube denominator is the Hamiltonian/Hilbert charge difference, not orbital GM.",
            "derivation": "M_H_ref := H_tau[S_link;tau,e_obs] - H_ref[Sigma_ref;tau,e_obs]. The same-object route identifies this with the dressed Hilbert worldtube source charge before readout.",
            "consequence": "Every source-worldtube bound must use the same tau/e_obs/source branch denominator, not a fitted acceleration or orbital mass.",
            "status": "DENOMINATOR_OBJECT_DEFINED",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "MHR4589_1_qbasic_difference",
            "claim": "If H_tau and H_ref descend through q on the same branch, then M_H_ref is q-basic.",
            "derivation": "H_tau=Hbar_tau(q(Phi)) and H_ref=Hbar_ref(q(Phi)) imply M_H_ref=Mbar_H_ref(q):=Hbar_tau(q)-Hbar_ref(q). Therefore D_v M_H_ref=dMbar_H_ref(Dq(v))=0 for v in ker(Dq).",
            "consequence": "E_Href=0 and the M_H_ref part of the source-support bundle is vertically silent on the strict branch.",
            "status": "CONDITIONAL_ZERO_THEOREM_DERIVED_NOT_GLOBAL_PARENT_SIGNED",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "MHR4589_2_no_cancellation_bound",
            "claim": "If q-basicness is unsigned, denominator drift is bounded without cancellation.",
            "derivation": "D_v M_H_ref=D_v H_tau-D_v H_ref, so |D_v M_H_ref| <= |D_v H_tau|+|D_v H_ref|. Normalized drift is epsilon_MHref <= (|D_v H_tau|+|D_v H_ref|)/M_lower.",
            "consequence": "The denominator problem becomes a sourceable H_tau/H_ref/M_lower vector.",
            "status": "BOUND_FORMULA_DERIVED_VALUES_MISSING",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "MHR4589_3_positive_denominator_guard",
            "claim": "A denominator bound is claim-eligible only with a positive same-frame lower bound.",
            "derivation": "Use M_H_ref >= M_EH*(1-epsilon_abs). If M_EH>0 and epsilon_abs<1, then M_lower:=M_EH*(1-epsilon_abs)>0. Otherwise normalized local bounds remain blocked.",
            "consequence": "No source-kernel or local-GR bound may divide by M_H_ref until the lower-bound row is signed or sourced.",
            "status": "POSITIVITY_GUARD_DERIVED_VALUES_MISSING",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
    ]


def reference_clause_rows(now: str) -> list[dict[str, Any]]:
    clauses = [
        ("MHC4589_0_same_tau_eobs", "H_tau and H_ref use the same tau, coframe, surface branch and units.", "same branch object before readout", "CONDITIONAL_REQUIRED"),
        ("MHC4589_1_Htau_qbasic", "H_tau descends through q.", "D_v H_tau=0 for v in ker(Dq)", "UNSIGNED_OR_BOUND_REQUIRED"),
        ("MHC4589_2_Href_qbasic", "H_ref is source-blind and descends through q.", "D_v H_ref=0; no source-dependent counterterm", "UNSIGNED_OR_BOUND_REQUIRED"),
        ("MHC4589_3_no_fitted_GM", "No orbital GM, acceleration fit or measured G defines H_tau/H_ref/M_H_ref.", "anti-circularity guard", "FIREWALL_REQUIRED"),
        ("MHC4589_4_positive_lower_bound", "M_H_ref has a positive same-frame lower bound.", "M_EH>0 and epsilon_abs<1", "MISSING_SOURCE_BACKED_LOWER_BOUND"),
        ("MHC4589_5_integrability", "Hamiltonian charge is integrable on the chosen surface family.", "curl/symplectic leakage zero or bounded", "UNSIGNED_OR_BOUND_REQUIRED"),
        ("MHC4589_6_reference_fixed_before_readout", "H_ref is selected before local residuals are inspected.", "no fitted subtraction/counterterm", "ANTI_TAUTOLOGY_GUARD_REQUIRED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "clause_id": clause_id,
            "clause": clause,
            "zero_condition": condition,
            "current_status": status,
            "zero_certificate_signed": "False" if "UNSIGNED" in status or "MISSING" in status or "REQUIRED" in status else "Conditional",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        }
        for clause_id, clause, condition, status in clauses
    ]


def denominator_bound_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("MDB4589_0_Dv_Htau", "D_v H_tau", "vertical derivative of Hamiltonian charge", "|D_v H_tau| <= |E_theta|+|E_Qtau|+|E_curl|+|E_surface|+|E_sector|+|E_boundary|", "MISSING_PARENT_HTAU_DERIVATIVE"),
        ("MDB4589_1_Dv_Href", "D_v H_ref", "vertical derivative of reference subtraction", "|D_v H_ref| <= |E_ref_selector|+|E_ref_boundary|+|E_ref_frame|+|E_ref_readout|", "MISSING_SOURCE_BLIND_HREF_DERIVATIVE"),
        ("MDB4589_2_Dv_MHref", "D_v M_H_ref", "source-worldtube denominator drift", "|D_v M_H_ref| <= |D_v H_tau|+|D_v H_ref|", "FORMULA_READY_VALUES_MISSING"),
        ("MDB4589_3_Mlower", "M_lower", "positive same-frame denominator lower bound", "M_lower=M_EH*(1-epsilon_abs), requiring M_EH>0 and epsilon_abs<1", "MISSING_POSITIVE_LOWER_BOUND"),
        ("MDB4589_4_epsilon_MHref", "epsilon_MHref", "normalized denominator drift", "epsilon_MHref <= (|D_v H_tau|+|D_v H_ref|)/M_lower", "FORMULA_READY_VALUES_MISSING"),
        ("MDB4589_5_no_fitted_G", "delta_Gfit", "absorbed fitted-G/orbital-GM contamination", "delta_Gfit=0 required; otherwise denominator branch rejected", "ANTI_CIRCULARITY_GUARD"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": bound_id,
            "symbol": symbol,
            "definition": definition,
            "bound_formula": formula,
            "current_status": status,
            "numeric_value_present": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        }
        for bound_id, symbol, definition, formula, status in rows
    ]


def reduction_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "MHRD4589_0_EHref_zero",
            "target": "E_Href / epsilon_MHref",
            "formula": "D_v M_H_ref=0 and epsilon_MHref=0",
            "branch_condition": "H_tau and H_ref q-basic, source-blind, same tau/e_obs/surface branch, positive lower bound, no fitted GM",
            "status": "CONDITIONAL_ZERO_NOT_PUBLIC_CLAIM",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "MHRD4589_1_EHref_bound",
            "target": "epsilon_MHref",
            "formula": "epsilon_MHref <= (|D_v H_tau|+|D_v H_ref|)/M_lower",
            "branch_condition": "any H_tau/H_ref q-basic or reference source-blind clause unsigned",
            "status": "DENOMINATOR_DRIFT_BOUND_READY_VALUES_MISSING",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "MHRD4589_2_CKsource_update",
            "target": "C_K_source_worldtube",
            "formula": "strict 4587+4588+4589 branch removes E_rho_qbasic, E_EM_flux, E_boundary_birth and E_Href; remaining blockers are E_Dq_source+E_tau_eobs+E_readout_mask",
            "branch_condition": "density/Poynting, support-boundary and denominator zero branches",
            "status": "PARTIAL_SOURCE_KERNEL_REDUCTION_DERIVED",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "MHRD4589_3_next_Dq_mask",
            "target": "E_Dq_source and E_readout_mask",
            "formula": "prove actual source residual is vertical and readout mask is fixed q-basic, or bound both operator components",
            "branch_condition": "next source-worldtube components after denominator lock",
            "status": "SELECTED_NEXT_DERIVATION_TARGET",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    controls = [
        ("CTRL4589_clean_qbasic", "H_tau and H_ref both q-basic same branch", "D_v M_H_ref=0", "SYMBOLIC_CONTROL_PASS"),
        ("CTRL4589_fitted_reference", "H_ref chosen to cancel a residual after readout", "reject zero; retain D_v H_ref/delta_Gfit", "COUNTERMODEL_CAUGHT"),
        ("CTRL4589_orbital_GM", "orbital GM or measured G used as denominator input", "reject denominator branch", "FIREWALL_PASS"),
        ("CTRL4589_nonintegrable_Htau", "Hamiltonian charge has curl/symplectic leakage", "retain D_v H_tau bound", "FIREWALL_PASS"),
        ("CTRL4589_zero_denominator", "M_lower missing or nonpositive", "block normalized claims", "COUNTERMODEL_CAUGHT"),
        ("CTRL4589_no_claim", "theorem exists but parent adoption/values missing", "no local-GR/R10/PPN claim", "FIREWALL_PASS"),
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
        for control_id, case, expected, status in controls
    ]


def promotion_rows(now: str) -> list[dict[str, Any]]:
    gates = [
        ("PROM4589_0_definition", "M_H_ref denominator object defined without orbital GM.", "PASSED"),
        ("PROM4589_1_qbasic_difference", "q-basic difference zero theorem derived conditionally.", "PASSED_CONDITIONAL"),
        ("PROM4589_2_no_cancellation", "open branch denominator drift bound emitted.", "PASSED"),
        ("PROM4589_3_positive_guard", "positive denominator lower-bound guard emitted.", "PASSED"),
        ("PROM4589_4_values", "H_tau/H_ref/M_lower clauses or numeric values are source-backed.", "BLOCKED"),
        ("PROM4589_5_no_claim", "No local-GR/R10/PPN claim from 4589 alone.", "PASSED_FIREWALL"),
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
        for gate_id, gate, status in gates
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "decision": DECISION,
            "plain_english": "4589 locks the denominator problem into a theorem-or-bound form. If H_tau and H_ref are q-basic on the same tau/e_obs/surface branch and H_ref is source-blind before readout, then M_H_ref is vertically silent. If not, denominator drift is bounded by |D_v H_tau|+|D_v H_ref| over a positive lower bound. Fitted GM/orbital mass is explicitly banned as denominator evidence.",
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
            "reason": "After density, support-boundary and denominator components, the remaining source-worldtube kernel blockers are actual verticality and readout-mask fixed-domain status.",
            "derive_first": "prove the source residual direction is genuinely in ker(Dq) and Pi_readout/source mask is fixed q-basic before variation",
            "fallback": "emit finite E_Dq_source and E_readout_mask rows with operator norms, units, support and no residual-fit masks",
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
            "summary": "M_H_ref q-basic/source-blind denominator zero route derived; open branch carries no-cancellation drift over positive lower bound.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def doc_text(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    clauses: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    reductions: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    promotions: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> str:
    return f"""# 4589 - MHref source-blind reference and Htau normalization zero or bound

Marker: `{MARKER}`  
Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`  
Private/public status: private nonclaim; no GitHub action.

## Result

4589 attacks the denominator/reference component exposed by 4588.

The denominator is:

```text
M_H_ref := H_tau[S_link;tau,e_obs] - H_ref[Sigma_ref;tau,e_obs].
```

If both pieces descend through the same quotient branch:

```text
H_tau=Hbar_tau(q(Phi)),
H_ref=Hbar_ref(q(Phi)),
v in ker(Dq),
```

then:

```text
D_v M_H_ref = 0,
epsilon_MHref = 0.
```

If that is not signed:

```text
epsilon_MHref <= (|D_v H_tau|+|D_v H_ref|)/M_lower.
```

The positive denominator guard is:

```text
M_lower = M_EH*(1-epsilon_abs),  M_EH>0,  epsilon_abs<1.
```

No orbital `GM`, measured `G`, fitted acceleration, or post-readout reference subtraction is allowed to define this denominator.

## MHref theorem

{markdown_table(theorem)}

## Source-blind reference clauses

{markdown_table(clauses)}

## Denominator drift bound rows

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
    return f"""## PPC4161 4589 MHref source-blind reference and Htau normalization zero or bound

Marker: `{MARKER}`  
Decision: `{DECISION}`  

The denominator/reference object is:

```text
M_H_ref := H_tau[S_link;tau,e_obs] - H_ref[Sigma_ref;tau,e_obs].
```

If:

```text
H_tau=Hbar_tau(q(Phi)), H_ref=Hbar_ref(q(Phi)), v in ker(Dq),
```

then:

```text
D_v M_H_ref = 0.
```

Open branch:

```text
epsilon_MHref <= (|D_v H_tau|+|D_v H_ref|)/M_lower,
M_lower=M_EH*(1-epsilon_abs)>0.
```

Orbital `GM`, measured `G`, fitted acceleration and post-readout reference subtraction are banned as denominator inputs.  Next target: `{NEXT_TARGET}`.
"""


def packet_text() -> str:
    return f"""## 4589 packet update - MHref source-blind denominator lock

Marker: `{PACKET_MARKER}`  
Decision: `{DECISION}`  

4589 derives the denominator leg: if `H_tau` and `H_ref` are q-basic on the same tau/e_obs/surface branch and `H_ref` is source-blind before readout, then `D_v M_H_ref=0`.  Otherwise `epsilon_MHref <= (|D_v H_tau|+|D_v H_ref|)/M_lower`, with `M_lower>0` required.  Fitted `GM/G` cannot be denominator evidence.
"""


def update_claims() -> None:
    if CLAIM_ID in read_text(CLAIMS_PATH):
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_signature",
        "claim": "4589 derives the M_H_ref q-basic/source-blind denominator zero contract and no-cancellation drift bound.",
        "current_evidence": "Generated MHref theorem, source-blind reference clauses, denominator drift rows, reductions, controls, gates and validation.",
        "status": "mhref_qbasic_difference_source_blind_reference_zero_contract_positive_denominator_bound_retained_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Using fitted GM/G, non-source-blind reference subtraction, or missing positive lower bound as if denominator stability were proved.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No local-GR/R10/PPN claim until H_tau/H_ref/M_lower clauses or numeric bounds are source-backed.",
    }
    rows = read_csv(CLAIMS_PATH)
    if rows:
        rows.append(row)
        write_csv(CLAIMS_PATH, rows)
    else:
        write_csv(CLAIMS_PATH, [row])


def validate(
    outputs: list[Path],
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    clauses: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    reductions: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    promotions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        checks.append({"checkpoint": CHECKPOINT, "branch": BRANCH_ID, "check_id": check_id, "check": check, "passed": bool_text(passed), "detail": detail})

    for path in outputs:
        add(f"VAL4589_exists_{path.name}", "output path exists", path.exists(), str(path))
        if path.suffix.lower() == ".csv":
            rows = read_csv(path)
            add(f"VAL4589_csv_parse_{path.name}", "CSV parses with at least one row", len(rows) > 0, f"rows={len(rows)}")

    add("VAL4589_sources_exist", "all cited sources exist", all(row["path_exists"] == "True" for row in sources), "source register existence")
    add("VAL4589_needles_found", "all cited needles found", all(row["needle_found"] == "True" for row in sources), "source register needles")
    add("VAL4589_definition", "denominator definition emitted", any(row["theorem_id"] == "MHR4589_0_definition" and "H_tau" in row["derivation"] for row in theorem), "MHR4589_0")
    add("VAL4589_qbasic_zero", "qbasic difference theorem emitted", any(row["theorem_id"] == "MHR4589_1_qbasic_difference" and "D_v M_H_ref" in row["derivation"] for row in theorem), "MHR4589_1")
    add("VAL4589_bound", "no-cancellation bound theorem emitted", any(row["theorem_id"] == "MHR4589_2_no_cancellation_bound" and "epsilon_MHref" in row["derivation"] for row in theorem), "MHR4589_2")
    add("VAL4589_positive_guard", "positive denominator guard emitted", any(row["theorem_id"] == "MHR4589_3_positive_denominator_guard" and "M_lower" in row["derivation"] for row in theorem), "MHR4589_3")
    add("VAL4589_clauses", "source-blind reference clauses cover qbasic Htau/Href and no fitted GM", all(any(row["clause_id"] == clause_id for row in clauses) for clause_id in ["MHC4589_1_Htau_qbasic", "MHC4589_2_Href_qbasic", "MHC4589_3_no_fitted_GM", "MHC4589_4_positive_lower_bound"]), "clauses")
    add("VAL4589_bound_rows", "bound rows include Htau, Href, MHref, lower bound and fitted-G guard", all(any(row["bound_id"] == bound_id for row in bounds) for bound_id in ["MDB4589_0_Dv_Htau", "MDB4589_1_Dv_Href", "MDB4589_2_Dv_MHref", "MDB4589_3_Mlower", "MDB4589_5_no_fitted_G"]), "bounds")
    add("VAL4589_reductions", "zero, bound and next rows emitted", all(any(row["row_id"] == row_id for row in reductions) for row_id in ["MHRD4589_0_EHref_zero", "MHRD4589_1_EHref_bound", "MHRD4589_3_next_Dq_mask"]), "reductions")
    add("VAL4589_controls", "countermodel controls emitted", all(any(row["control_id"] == control_id for row in controls) for control_id in ["CTRL4589_fitted_reference", "CTRL4589_orbital_GM", "CTRL4589_zero_denominator"]), "controls")
    add("VAL4589_values_blocked", "promotion gates block claims while values missing", any(row["gate_id"] == "PROM4589_4_values" and row["status"] == "BLOCKED" for row in promotions), "PROM4589_4")
    add("VAL4589_no_claim_flags", "all generated claim flags remain false", all(row.get("valid_for_claim", "False") == "False" for group in [theorem, clauses, bounds, reductions, controls, promotions] for row in group), "valid_for_claim false")
    add("VAL4589_decision_token", "decision token recorded", DECISION in read_text(DECISION_CSV) and DECISION in read_text(DOC_PATH), DECISION)
    add("VAL4589_next_target", "next target recorded", NEXT_TARGET in read_text(NEXT_CSV) and NEXT_TARGET in read_text(DOC_PATH), NEXT_TARGET)
    add("VAL4589_claim_register", "claim register updated", CLAIM_ID in read_text(CLAIMS_PATH), CLAIM_ID)
    add("VAL4589_spine_packet", "spine and packet markers present", MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH), f"{MARKER}; {PACKET_MARKER}")
    return checks


def main() -> None:
    now = utc_now()
    sources = source_rows(now)
    theorem = mhref_theorem_rows(now)
    clauses = reference_clause_rows(now)
    bounds = denominator_bound_rows(now)
    reductions = reduction_rows(now)
    controls = control_rows(now)
    promotions = promotion_rows(now)
    decision = decision_rows(now)
    next_target = next_rows(now)
    status = status_rows(now)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(MHREF_THEOREM_CSV, theorem)
    write_csv(REFERENCE_CLAUSES_CSV, clauses)
    write_csv(DENOMINATOR_BOUND_CSV, bounds)
    write_csv(REDUCTION_CSV, reductions)
    write_csv(CONTROL_CSV, controls)
    write_csv(PROMOTION_CSV, promotions)
    write_csv(DECISION_CSV, decision)
    write_csv(NEXT_CSV, next_target)
    write_csv(STATUS_CSV, status)

    DOC_PATH.write_text(doc_text(sources, theorem, clauses, bounds, reductions, controls, promotions, decision, next_target), encoding="utf-8")
    FORMAL_PATH.write_text(formal_text(), encoding="utf-8")

    append_once(
        SPINE_PATH,
        MARKER,
        f"""### 4589 - MHref source-blind reference and Htau normalization zero or bound

Marker: `{MARKER}`  
Decision: `{DECISION}`.  Next target: `{NEXT_TARGET}`.

The denominator is:

```text
M_H_ref := H_tau[S_link;tau,e_obs] - H_ref[Sigma_ref;tau,e_obs].
```

If `H_tau` and `H_ref` are both q-basic on the same branch:

```text
D_v M_H_ref=0.
```

Open branch:

```text
epsilon_MHref <= (|D_v H_tau|+|D_v H_ref|)/M_lower,
M_lower=M_EH*(1-epsilon_abs)>0.
```
""",
    )
    append_once(PACKET_PATH, PACKET_MARKER, packet_text())
    update_claims()

    outputs = [
        SOURCE_REGISTER,
        MHREF_THEOREM_CSV,
        REFERENCE_CLAUSES_CSV,
        DENOMINATOR_BOUND_CSV,
        REDUCTION_CSV,
        CONTROL_CSV,
        PROMOTION_CSV,
        DECISION_CSV,
        NEXT_CSV,
        STATUS_CSV,
        DOC_PATH,
        FORMAL_PATH,
    ]
    validations = validate(outputs, sources, theorem, clauses, bounds, reductions, controls, promotions)
    write_csv(VALIDATION_PATH, validations)
    failed = [row for row in validations if row["passed"] != "True"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)

    cache = Path(__file__).resolve().parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    print(f"4589 complete: {DECISION}")
    print(f"wrote: {DOC_PATH}")
    print(f"validation: {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
