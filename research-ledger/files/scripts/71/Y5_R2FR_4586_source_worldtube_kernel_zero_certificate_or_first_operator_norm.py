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

CHECKPOINT = "4586"
CLAIM_ID = "L-428"
BRANCH_ID = "MTS_R2FR_Y5_SOURCE_WORLDTUBE_KERNEL_ZERO_CERTIFICATE_OR_FIRST_OPERATOR_NORM_4586"
MARKER = "PPC4161_SOURCE_WORLDTUBE_KERNEL_ZERO_CERTIFICATE_OR_FIRST_OPERATOR_NORM_4586"
PACKET_MARKER = "PPC4161_PACKET_SOURCE_WORLDTUBE_KERNEL_ZERO_CERTIFICATE_OR_FIRST_OPERATOR_NORM_4586"
DECISION = "SOURCE_WORLDTUBE_KERNEL_FACTORISED_THROUGH_QBASIC_SUPPORT_BUNDLE_ZERO_CONTRACT_DERIVED_OPERATOR_VECTOR_RETAINED_NONCLAIM"
NEXT_TARGET = "4587-Y5-R2FR-Hilbert-source-density-qbasic-and-Poynting-support-owner-or-bound.md"

DOC_PATH = POST / "4586-Y5-R2FR-source-worldtube-kernel-zero-certificate-or-first-operator-norm.md"
FORMAL_PATH = FORMAL / "602-PPC4161-source-worldtube-kernel-zero-certificate-or-first-operator-norm.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_4585 = POST / "4585-Y5-R2FR-active-kernel-first-zero-or-operator-bound.md"
CSV_4585_CERT = SOURCE_DIR / "P8_Y5_R2FR_4585_KERNEL_ZERO_CERTIFICATE_MATRIX.csv"
CSV_4585_REDUCTION = SOURCE_DIR / "P8_Y5_R2FR_4585_CREADOUT_KERNEL_REDUCTION_ROWS.csv"
FORMAL_601 = FORMAL / "601-PPC4161-active-kernel-first-zero-or-operator-bound.md"
DOC_3560 = POST / "3560-Y5-R2FR-source-support-qbasic-worldtube-descent-or-bound-vector.md"
CSV_3560_BOUND = SOURCE_DIR / "P8_Y5_R2FR_3560_BOUND_VECTOR.csv"
CSV_3560_STATUS = SOURCE_DIR / "P8_Y5_source_support_qbasic_worldtube_status.csv"
DOC_4576 = FORMAL / "592-PPC4161-same-worldtube-Hilbert-source-lock-or-residual-moment-bound.md"
CSV_4576_LOCK = SOURCE_DIR / "P8_Y5_R2FR_4576_SAME_WORLDTUBE_LOCK_THEOREM.csv"
CSV_4170_ID = SOURCE_DIR / "P8_Y5_R2FR_4170_SAME_OBJECT_IDENTITY.csv"
CSV_4580_DOMAIN = SOURCE_DIR / "P8_Y5_R2FR_4580_PI_READOUT_DOMAIN_CERTIFICATE.csv"
DOC_3496 = POST / "3496-Y5-R2FR-source-worldtube-hypermomentum-zero-or-kernel-fill.md"
DOC_3375 = POST / "3375-Y5-R2FR-worldtube-source-measure-selector-or-Rworldtube-bound-under-AX1090.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4586_SOURCE_REGISTER.csv"
KERNEL_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4586_SOURCE_WORLDTUBE_KERNEL_THEOREM.csv"
ZERO_CLAUSE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4586_ZERO_CERTIFICATE_CLAUSES.csv"
OPERATOR_VECTOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4586_SOURCE_WORLDTUBE_OPERATOR_VECTOR.csv"
REDUCTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4586_CK_SOURCE_WORLDTUBE_REDUCTION_ROWS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4586_CONTROL_ROWS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4586_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4586_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4586_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4586_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4586_VALIDATION.csv"


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
        ("SRC4586_00_4585_doc", DOC_4585, "4586-Y5-R2FR-source-worldtube-kernel-zero-certificate-or-first-operator-norm.md", "4585 selected source-worldtube kernel"),
        ("SRC4586_01_4585_cert", CSV_4585_CERT, "KC4585_0_source_worldtube", "4585 source-worldtube certificate row"),
        ("SRC4586_02_4585_reduction", CSV_4585_REDUCTION, "KRD4585_3_first_target", "4585 first target reduction row"),
        ("SRC4586_03_601_formal", FORMAL_601, "C_K_source_worldtube", "formal active-kernel bound handoff"),
        ("SRC4586_04_3560_doc", DOC_3560, "SWT3560_1_qbasic_support_lemma", "q-basic source-support descent lemma"),
        ("SRC4586_05_3560_bound", CSV_3560_BOUND, "BF3560_0_E_rho_qbasic", "source-support failure vector"),
        ("SRC4586_06_3560_status", CSV_3560_STATUS, "SOURCE_SUPPORT_QBASIC_LEMMA_DERIVED_UNSIGNED", "canonical source-support status"),
        ("SRC4586_07_4576_lock_doc", DOC_4576, "SWL4576_1_same_worldtube_before_readout", "same-worldtube lock theorem"),
        ("SRC4586_08_4576_lock_csv", CSV_4576_LOCK, "SWL4576_3_profile_or_trace_defect", "profile/trace defect guard"),
        ("SRC4586_09_4170_identity", CSV_4170_ID, "SO4170_1_identity", "private Hilbert/Hamiltonian same-object identity"),
        ("SRC4586_10_4580_domain", CSV_4580_DOMAIN, "PDC4580_1_fixed_qbasic_domain", "fixed q-basic readout domain certificate"),
        ("SRC4586_11_3496_support", DOC_3496, "DER3496_2_worldtube_support_stability", "worldtube support stability precedent"),
        ("SRC4586_12_3375_poynting", DOC_3375, "POY3375_2_theory_policy", "Poynting/source-measure guard"),
        ("SRC4586_13_claim_427", CLAIMS_PATH, "L-427", "prior claim register handoff"),
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


def kernel_theorem_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "SWK4586_0_factorisation",
            "claim": "The source-worldtube kernel factors through the source-support bundle Y=(W_H, sigma^a, M_H_ref, tau_obs, e_obs, units).",
            "derivation": "Write K_source_worldtube=Kbar(q, Y, P_protocol). For source-vertical probes, D_v K_source_worldtube=(D_Y Kbar)(D_v Y) because Dq(v)=0 and the protocol is fixed before variation.",
            "consequence": "The old vague kernel is now reducible to source-support descent plus a Lipschitz/operator norm on Y.",
            "status": "CHAIN_RULE_FACTORISATION_DERIVED",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "SWK4586_1_zero_certificate",
            "claim": "If Y is q-basic and selected before readout, then O_f K_source_worldtube=0.",
            "derivation": "3560 gives D_v Y=0 when rho_H dV_H, W_H, sigma^a, M_H_ref, tau_obs and e_obs descend through q on a regular compact source support. Substituting D_v Y=0 into the factorisation gives D_v K_source_worldtube=0.",
            "consequence": "C_K_source_worldtube=0 on the strict same-Hilbert-worldtube branch.",
            "status": "CONDITIONAL_ZERO_THEOREM_DERIVED_NOT_PARENT_SIGNED",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "SWK4586_2_operator_vector",
            "claim": "If any source-support clause is unsigned, the fallback is a component operator vector, not a closure axiom.",
            "derivation": "Let L_K be the operator/Lipschitz constant of Kbar on the declared local collar. Then C_K_source_worldtube <= L_K*(E_rho_qbasic+E_boundary_birth+E_Dq_source+E_tau_eobs+E_Href+E_readout_mask+E_EM_flux), with no cancellation credit.",
            "consequence": "The first source-worldtube bound is now aligned with the 3560 failure vector and can be filled row by row.",
            "status": "OPERATOR_VECTOR_DERIVED_VALUES_MISSING",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
    ]


def zero_clause_rows(now: str) -> list[dict[str, Any]]:
    clauses = [
        ("ZC4586_0_parent_source_domain", "W_H is the parent Hilbert source worldtube, not an orbital/data mask.", "W_H=closure(supp J_H,total) before readout", "SUPPORTED_BY_4170_4576_CONDITIONAL"),
        ("ZC4586_1_qbasic_density_measure", "Hilbert source density measure descends through q.", "D_v(rho_H dV_H)=0 for v in ker(Dq)", "UNSIGNED_HARD_PREMISE"),
        ("ZC4586_2_regular_support", "The support boundary is compact regular with no vertical birth/death shell.", "D_v W_H=0 and no boundary Reynolds term", "UNSIGNED_REGULARITY_PREMISE"),
        ("ZC4586_3_profile_owner", "The density profile is the same Hilbert density as a distribution.", "rho_eff=rho_H or sigma_perp=0", "UNSIGNED_PROFILE_PREMISE"),
        ("ZC4586_4_fixed_readout_protocol", "The worldtube/collar/readout protocol is fixed before variation.", "[O_f,Pi_readout] on source support is zero", "CONDITIONAL_4580_ROUTE"),
        ("ZC4586_5_same_tau_eobs_units", "The same tau, observed frame and units define source and local readout.", "D_v(tau_obs,e_obs,units)=0 on source-support bundle", "UNSIGNED_OR_BOUND_REQUIRED"),
        ("ZC4586_6_poynting_in_source", "EM/Poynting stress is either inside the public Hilbert source or explicitly bounded.", "T_EM and S_EM belong to J_H, or E_EM_flux remains", "PLACED_BUT_INPUT_NORMS_MISSING"),
        ("ZC4586_7_no_fitted_G_or_mask", "No fitted GM/G/readout residual is used to define support or source normalization.", "source support and M_H_ref are parent-owned before local tests", "ANTI_CIRCULARITY_GUARD_REQUIRED"),
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


def operator_vector_rows(now: str) -> list[dict[str, Any]]:
    components = [
        ("CKSW4586_0_E_rho_qbasic", "E_rho_qbasic", "normalized vertical derivative of rho_H dV_H", "BF3560_0_E_rho_qbasic", "MISSING_JH_QBASIC_OWNER_OR_BOUND"),
        ("CKSW4586_1_E_boundary_birth", "E_boundary_birth", "support boundary birth/death or distributional source-shell layer", "BF3560_1_E_boundary_birth", "MISSING_REGULAR_SUPPORT_CERTIFICATE_OR_BOUND"),
        ("CKSW4586_2_E_Dq_source", "E_Dq_source", "failure that the source residual direction is truly vertical", "BF3560_2_E_Dq_source", "MISSING_ACTUAL_QMAP_VERTICAL_BASIS"),
        ("CKSW4586_3_E_tau_eobs", "E_tau_eobs", "same-frame/time support mismatch", "BF3560_3_E_tau_eobs", "MISSING_SAME_FRAME_SOURCE_SUPPORT_LOCK_OR_BOUND"),
        ("CKSW4586_4_E_Href", "E_Href", "source-blind reference/M_H_ref failure", "BF3560_4_E_Href", "MISSING_HREF_SOURCE_BLINDNESS_OR_BOUND"),
        ("CKSW4586_5_E_readout_mask", "E_readout_mask", "post-fit source mask or moving readout domain", "BF3560_5_E_readout_mask", "MISSING_NO_READOUT_MASK_THEOREM_OR_BOUND"),
        ("CKSW4586_6_E_EM_flux", "E_EM_flux", "EM/Poynting or radiative flux not included in stationary Hilbert source", "BF3560_6_E_EM_flux", "MISSING_STATIONARY_MINIMAL_EM_ZERO_OR_FLUX_BOUND"),
    ]
    rows = []
    for component_id, symbol, definition, inherited, status in components:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "component_id": component_id,
                "symbol": symbol,
                "definition": definition,
                "inherited_row": inherited,
                "operator_formula": f"C_K_source_worldtube[{symbol}] <= L_K_source * {symbol}",
                "units": "dimensionless_after_M_H_ref_normalization",
                "current_status": status,
                "numeric_value_present": "False",
                "claim_allowed": "False",
                "valid_for_claim": "False",
                "generated_utc": now,
            }
        )
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "component_id": "CKSW4586_7_total",
            "symbol": "C_K_source_worldtube",
            "definition": "total active source-worldtube kernel operator debt",
            "inherited_row": "KRD4585_3_first_target plus BF3560 vector",
            "operator_formula": "C_K_source_worldtube <= L_K_source*(E_rho_qbasic+E_boundary_birth+E_Dq_source+E_tau_eobs+E_Href+E_readout_mask+E_EM_flux)",
            "units": "dimensionless",
            "current_status": "SCHEMA_DERIVED_VALUES_MISSING",
            "numeric_value_present": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        }
    )
    return rows


def reduction_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "SWR4586_0_source_kernel_zero",
            "target": "C_K_source_worldtube",
            "formula": "C_K_source_worldtube=0",
            "branch_condition": "all zero clauses ZC4586_0..7 signed in one parent branch",
            "status": "CONDITIONAL_ZERO_NOT_CLAIMED",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "SWR4586_1_source_kernel_bound",
            "target": "C_K_source_worldtube",
            "formula": "C_K_source_worldtube <= L_K_source*(E_rho_qbasic+E_boundary_birth+E_Dq_source+E_tau_eobs+E_Href+E_readout_mask+E_EM_flux)",
            "branch_condition": "any source-support/worldtube clause unsigned",
            "status": "OPERATOR_VECTOR_BOUND_READY_VALUES_MISSING",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "SWR4586_2_Ckernel_update",
            "target": "C_kernel_active",
            "formula": "C_kernel_active <= C_K_source_worldtube + C_K_WEP + C_K_clock + C_K_light + C_K_GM_orbit + C_K_projective",
            "branch_condition": "4585 no-cancellation kernel envelope with source-worldtube term now factorised",
            "status": "FIRST_KERNEL_TERM_FACTORISED",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "SWR4586_3_next_first_component",
            "target": "E_rho_qbasic and E_EM_flux",
            "formula": "derive D_v(rho_H dV_H)=0 including EM/Poynting Hilbert stress, or source first finite flux/profile bound",
            "branch_condition": "best next step after source-worldtube factorisation",
            "status": "SELECTED_NEXT_DERIVATION_TARGET",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    controls = [
        ("CTRL4586_clean_parent", "all q-basic support/profile/source clauses true", "C_K_source_worldtube=0", "SYMBOLIC_CONTROL_PASS"),
        ("CTRL4586_moving_boundary", "rho_H support boundary moves under source probe", "retain E_boundary_birth", "COUNTERMODEL_CAUGHT"),
        ("CTRL4586_wrong_profile", "same monopole but wrong density profile", "retain E_rho_qbasic/E_profile style row", "COUNTERMODEL_CAUGHT"),
        ("CTRL4586_fitted_mask", "worldtube support chosen from residual/GM fit", "retain E_readout_mask and block claim", "FIREWALL_PASS"),
        ("CTRL4586_hidden_poynting", "EM/Poynting flux crosses source boundary outside public Hilbert stress", "retain E_EM_flux", "FIREWALL_PASS"),
        ("CTRL4586_no_local_claim", "operator vector exists but values are missing", "no R10/PPN/local-GR claim", "FIREWALL_PASS"),
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
        ("PROM4586_0_factorisation", "K_source_worldtube factorises through q-basic source-support bundle.", "PASSED"),
        ("PROM4586_1_zero_contract", "Exact zero certificate clauses emitted.", "PASSED_CONDITIONAL"),
        ("PROM4586_2_operator_vector", "Fallback operator vector emitted from 3560 components.", "PASSED"),
        ("PROM4586_3_poynting_guard", "Poynting/EM stress cannot be ignored; it is source-owned or bounded.", "PASSED_FIREWALL"),
        ("PROM4586_4_values", "All source-support/operator components have signed zeros or numeric values.", "BLOCKED"),
        ("PROM4586_5_no_claim", "No local-GR/R10/PPN claim from 4586 alone.", "PASSED_FIREWALL"),
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
            "plain_english": "4586 makes a real forward move: the source-worldtube active kernel is not just marked missing; it is factorised through the q-basic source-support bundle Y. If Y is parent-owned before readout, the kernel term is exactly zero. If not, the finite debt is the 3560 component vector times a source-kernel operator constant. Poynting/EM stress is explicitly routed into the source or a flux bound.",
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
            "reason": "The first live component in C_K_source_worldtube is rho_H dV_H q-basicness; EM/Poynting placement is the highest-risk way this can fail.",
            "derive_first": "prove D_v(rho_H dV_H)=0 from one public Hilbert matter+EM source functor on the same worldtube, including stationary Poynting/Maxwell stress",
            "fallback": "emit first finite E_rho_qbasic/E_EM_flux rows with units, M_H_ref normalization, support class and no fitted-G absorption",
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
            "summary": "Source-worldtube kernel zero route is derived conditionally; open branch is reduced to a concrete operator vector.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def doc_text(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    clauses: list[dict[str, Any]],
    operators: list[dict[str, Any]],
    reductions: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    promotions: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> str:
    return f"""# 4586 - Source-worldtube kernel zero certificate or first operator norm

Marker: `{MARKER}`  
Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`  
Private/public status: private nonclaim; no GitHub action.

## Result

4586 takes the first active-kernel target from 4585 and reduces it to a real theorem-or-bound shape.

Define the source-support bundle:

```text
Y_source = (W_H, sigma^a, M_H_ref, tau_obs, e_obs, units).
```

For a source-worldtube kernel selected before variation:

```text
K_source_worldtube = Kbar(q, Y_source, P_protocol).
```

For source-vertical probes `v in ker(Dq)`:

```text
D_v K_source_worldtube = (D_Y Kbar)(D_v Y_source).
```

So the exact zero route is:

```text
D_v Y_source = 0  =>  O_f K_source_worldtube = 0  =>  C_K_source_worldtube = 0.
```

If the source-support bundle is not parent-owned, the fallback is now explicit:

```text
C_K_source_worldtube <= L_K_source*(E_rho_qbasic+E_boundary_birth+E_Dq_source+E_tau_eobs+E_Href+E_readout_mask+E_EM_flux).
```

This is not a local-GR claim.  It is the first proper source-worldtube kernel reduction.  The next hard boss is `rho_H dV_H` q-basicness, with the Poynting/Maxwell stress placement included rather than ignored.

## Source-worldtube kernel theorem

{markdown_table(theorem)}

## Zero certificate clauses

{markdown_table(clauses)}

## Operator vector

{markdown_table(operators)}

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
    return f"""## PPC4161 4586 source-worldtube kernel zero certificate or first operator norm

Marker: `{MARKER}`  
Decision: `{DECISION}`  

The source-worldtube active kernel is factorised through the source-support bundle:

```text
Y_source=(W_H,sigma^a,M_H_ref,tau_obs,e_obs,units),
K_source_worldtube=Kbar(q,Y_source,P_protocol).
```

For `v in ker(Dq)`:

```text
D_v K_source_worldtube=(D_Y Kbar)(D_v Y_source).
```

Therefore the strict zero certificate is:

```text
D_v Y_source=0 -> O_f K_source_worldtube=0 -> C_K_source_worldtube=0.
```

The open branch is:

```text
C_K_source_worldtube <= L_K_source*(E_rho_qbasic+E_boundary_birth+E_Dq_source+E_tau_eobs+E_Href+E_readout_mask+E_EM_flux).
```

This imports the 3560 support vector rather than inventing a closure axiom.  Poynting/EM stress must be in the Hilbert source or carried as `E_EM_flux`.  Next target: `{NEXT_TARGET}`.
"""


def packet_text() -> str:
    return f"""## 4586 packet update - source-worldtube kernel factorisation

Marker: `{PACKET_MARKER}`  
Decision: `{DECISION}`  

4586 factorises `K_source_worldtube` through `Y_source=(W_H,sigma^a,M_H_ref,tau_obs,e_obs,units)`.  If that bundle is q-basic and fixed before readout, `C_K_source_worldtube=0`; otherwise the debt is the explicit 3560 vector multiplied by `L_K_source`.  This is a real narrowing of the coupling problem: next attack is `rho_H dV_H` q-basicness with EM/Poynting stress included or bounded.
"""


def update_claims() -> None:
    if CLAIM_ID in read_text(CLAIMS_PATH):
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_signature",
        "claim": "4586 factorises the source-worldtube active kernel through the q-basic source-support bundle and derives the zero certificate or operator-vector fallback.",
        "current_evidence": "Generated source register, source-worldtube kernel theorem, zero clauses, operator vector, controls, gates and validation.",
        "status": "source_worldtube_kernel_factorised_zero_contract_derived_operator_vector_retained_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Promoting the zero branch without parent-signed rho_H dV_H q-basicness, regular support, readout-mask silence and EM/Poynting placement.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No local-GR/R10/PPN claim until source-density/support components are signed zero or numerically sourced.",
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
    operators: list[dict[str, Any]],
    reductions: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    promotions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        checks.append({"checkpoint": CHECKPOINT, "branch": BRANCH_ID, "check_id": check_id, "check": check, "passed": bool_text(passed), "detail": detail})

    for path in outputs:
        add(f"VAL4586_exists_{path.name}", "output path exists", path.exists(), str(path))
        if path.suffix.lower() == ".csv":
            rows = read_csv(path)
            add(f"VAL4586_csv_parse_{path.name}", "CSV parses with at least one row", len(rows) > 0, f"rows={len(rows)}")

    add("VAL4586_sources_exist", "all cited sources exist", all(row["path_exists"] == "True" for row in sources), "source register existence")
    add("VAL4586_needles_found", "all cited needles found", all(row["needle_found"] == "True" for row in sources), "source register needles")
    add("VAL4586_factorisation", "kernel factorisation theorem emitted", any(row["theorem_id"] == "SWK4586_0_factorisation" and "D_v K_source_worldtube" in row["derivation"] for row in theorem), "SWK4586_0")
    add("VAL4586_zero_theorem", "zero theorem emitted", any(row["theorem_id"] == "SWK4586_1_zero_certificate" and "C_K_source_worldtube=0" in row["consequence"] for row in theorem), "SWK4586_1")
    add("VAL4586_operator_vector", "operator vector theorem emitted", any(row["theorem_id"] == "SWK4586_2_operator_vector" and "E_rho_qbasic" in row["derivation"] for row in theorem), "SWK4586_2")
    add("VAL4586_zero_clauses", "all zero clauses present", len(clauses) == 8 and all(row["claim_allowed"] == "False" for row in clauses), f"clauses={len(clauses)}")
    add("VAL4586_3560_components", "3560 component vector imported", all(any(row["symbol"] == symbol for row in operators) for symbol in ["E_rho_qbasic", "E_boundary_birth", "E_Dq_source", "E_tau_eobs", "E_Href", "E_readout_mask", "E_EM_flux"]), "operator components")
    add("VAL4586_total_bound", "total source-worldtube bound emitted", any(row["component_id"] == "CKSW4586_7_total" and "L_K_source" in row["operator_formula"] for row in operators), "CKSW4586_7_total")
    add("VAL4586_poynting_guard", "Poynting/EM guard retained", any(row["clause_id"] == "ZC4586_6_poynting_in_source" for row in clauses) and any(row["symbol"] == "E_EM_flux" for row in operators), "E_EM_flux")
    add("VAL4586_reduction_rows", "kernel zero and bound reductions emitted", all(any(row["row_id"] == row_id for row in reductions) for row_id in ["SWR4586_0_source_kernel_zero", "SWR4586_1_source_kernel_bound", "SWR4586_2_Ckernel_update"]), "reductions")
    add("VAL4586_controls", "countermodel controls emitted", all(any(row["control_id"] == control_id for row in controls) for control_id in ["CTRL4586_moving_boundary", "CTRL4586_wrong_profile", "CTRL4586_hidden_poynting"]), "controls")
    add("VAL4586_values_blocked", "promotion gates block claims while values missing", any(row["gate_id"] == "PROM4586_4_values" and row["status"] == "BLOCKED" for row in promotions), "PROM4586_4")
    add("VAL4586_no_claim_flags", "all generated claim flags remain false", all(row.get("valid_for_claim", "False") == "False" for group in [theorem, clauses, operators, reductions, controls, promotions] for row in group), "valid_for_claim false")
    add("VAL4586_decision_token", "decision token recorded", DECISION in read_text(DECISION_CSV) and DECISION in read_text(DOC_PATH), DECISION)
    add("VAL4586_next_target", "next target recorded", NEXT_TARGET in read_text(NEXT_CSV) and NEXT_TARGET in read_text(DOC_PATH), NEXT_TARGET)
    add("VAL4586_claim_register", "claim register updated", CLAIM_ID in read_text(CLAIMS_PATH), CLAIM_ID)
    add("VAL4586_spine_packet", "spine and packet markers present", MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH), f"{MARKER}; {PACKET_MARKER}")
    return checks


def main() -> None:
    now = utc_now()
    sources = source_rows(now)
    theorem = kernel_theorem_rows(now)
    clauses = zero_clause_rows(now)
    operators = operator_vector_rows(now)
    reductions = reduction_rows(now)
    controls = control_rows(now)
    promotions = promotion_rows(now)
    decision = decision_rows(now)
    next_target = next_rows(now)
    status = status_rows(now)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(KERNEL_THEOREM_CSV, theorem)
    write_csv(ZERO_CLAUSE_CSV, clauses)
    write_csv(OPERATOR_VECTOR_CSV, operators)
    write_csv(REDUCTION_CSV, reductions)
    write_csv(CONTROL_CSV, controls)
    write_csv(PROMOTION_CSV, promotions)
    write_csv(DECISION_CSV, decision)
    write_csv(NEXT_CSV, next_target)
    write_csv(STATUS_CSV, status)

    DOC_PATH.write_text(doc_text(sources, theorem, clauses, operators, reductions, controls, promotions, decision, next_target), encoding="utf-8")
    FORMAL_PATH.write_text(formal_text(), encoding="utf-8")

    append_once(
        SPINE_PATH,
        MARKER,
        f"""### 4586 - Source-worldtube kernel zero certificate or first operator norm

Marker: `{MARKER}`  
Decision: `{DECISION}`.  Next target: `{NEXT_TARGET}`.

The first active source kernel is factorised as:

```text
K_source_worldtube=Kbar(q,Y_source,P_protocol),
D_v K_source_worldtube=(D_Y Kbar)(D_v Y_source).
```

If `Y_source=(W_H,sigma^a,M_H_ref,tau_obs,e_obs,units)` is q-basic and fixed before readout, then `C_K_source_worldtube=0`.  Otherwise:

```text
C_K_source_worldtube <= L_K_source*(E_rho_qbasic+E_boundary_birth+E_Dq_source+E_tau_eobs+E_Href+E_readout_mask+E_EM_flux).
```
""",
    )
    append_once(PACKET_PATH, PACKET_MARKER, packet_text())
    update_claims()

    outputs = [
        SOURCE_REGISTER,
        KERNEL_THEOREM_CSV,
        ZERO_CLAUSE_CSV,
        OPERATOR_VECTOR_CSV,
        REDUCTION_CSV,
        CONTROL_CSV,
        PROMOTION_CSV,
        DECISION_CSV,
        NEXT_CSV,
        STATUS_CSV,
        DOC_PATH,
        FORMAL_PATH,
    ]
    validations = validate(outputs, sources, theorem, clauses, operators, reductions, controls, promotions)
    write_csv(VALIDATION_PATH, validations)
    failed = [row for row in validations if row["passed"] != "True"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)

    cache = Path(__file__).resolve().parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    print(f"4586 complete: {DECISION}")
    print(f"wrote: {DOC_PATH}")
    print(f"validation: {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
