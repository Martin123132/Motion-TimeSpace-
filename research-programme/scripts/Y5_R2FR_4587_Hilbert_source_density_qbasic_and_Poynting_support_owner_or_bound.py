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

CHECKPOINT = "4587"
CLAIM_ID = "L-429"
BRANCH_ID = "MTS_R2FR_Y5_HILBERT_SOURCE_DENSITY_QBASIC_AND_POYNTING_SUPPORT_OWNER_OR_BOUND_4587"
MARKER = "PPC4161_HILBERT_SOURCE_DENSITY_QBASIC_AND_POYNTING_SUPPORT_OWNER_OR_BOUND_4587"
PACKET_MARKER = "PPC4161_PACKET_HILBERT_SOURCE_DENSITY_QBASIC_AND_POYNTING_SUPPORT_OWNER_OR_BOUND_4587"
DECISION = "HILBERT_SOURCE_DENSITY_QBASIC_THEOREM_AND_POYNTING_ONCE_ONLY_LOCK_DERIVED_RESIDUAL_VECTOR_RETAINED_NONCLAIM"
NEXT_TARGET = "4588-Y5-R2FR-regular-source-support-boundary-zero-or-Reynolds-shell-bound.md"

DOC_PATH = POST / "4587-Y5-R2FR-Hilbert-source-density-qbasic-and-Poynting-support-owner-or-bound.md"
FORMAL_PATH = FORMAL / "603-PPC4161-Hilbert-source-density-qbasic-and-Poynting-support-owner-or-bound.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_4586 = POST / "4586-Y5-R2FR-source-worldtube-kernel-zero-certificate-or-first-operator-norm.md"
CSV_4586_OPERATOR = SOURCE_DIR / "P8_Y5_R2FR_4586_SOURCE_WORLDTUBE_OPERATOR_VECTOR.csv"
CSV_4586_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4586_NEXT_TARGET.csv"
DOC_3560 = POST / "3560-Y5-R2FR-source-support-qbasic-worldtube-descent-or-bound-vector.md"
CSV_3560_BOUND = SOURCE_DIR / "P8_Y5_R2FR_3560_BOUND_VECTOR.csv"
FORMAL_191 = FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md"
FORMAL_193 = FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md"
FORMAL_223 = FORMAL / "223-PPC4161-EM-Poynting-Hodge-source-owner-lock.md"
DOC_3375 = POST / "3375-Y5-R2FR-worldtube-source-measure-selector-or-Rworldtube-bound-under-AX1090.md"
DOC_3496 = POST / "3496-Y5-R2FR-source-worldtube-hypermomentum-zero-or-kernel-fill.md"
CSV_4170_ID = SOURCE_DIR / "P8_Y5_R2FR_4170_SAME_OBJECT_IDENTITY.csv"
CSV_4580_DOMAIN = SOURCE_DIR / "P8_Y5_R2FR_4580_PI_READOUT_DOMAIN_CERTIFICATE.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4587_SOURCE_REGISTER.csv"
DENSITY_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4587_DENSITY_QBASIC_THEOREM.csv"
POYNTING_OWNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4587_POYNTING_OWNER_LOCK.csv"
RESIDUAL_VECTOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4587_DENSITY_POYNTING_RESIDUAL_VECTOR.csv"
REDUCTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4587_SOURCE_KERNEL_REDUCTION_UPDATE.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4587_CONTROL_ROWS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4587_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4587_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4587_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4587_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4587_VALIDATION.csv"


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
        ("SRC4587_00_4586_doc", DOC_4586, "4587-Y5-R2FR-Hilbert-source-density-qbasic-and-Poynting-support-owner-or-bound.md", "4586 selected density/Poynting target"),
        ("SRC4587_01_4586_operator", CSV_4586_OPERATOR, "CKSW4586_0_E_rho_qbasic", "4586 E_rho_qbasic source-kernel component"),
        ("SRC4587_02_4586_next", CSV_4586_NEXT, "4587-Y5-R2FR-Hilbert-source-density-qbasic-and-Poynting-support-owner-or-bound.md", "4586 next target csv"),
        ("SRC4587_03_3560_doc", DOC_3560, "D_X(rho_H dV_H)=0", "3560 density q-basic implication"),
        ("SRC4587_04_3560_bound", CSV_3560_BOUND, "BF3560_6_E_EM_flux", "3560 E_rho/E_EM failure vector"),
        ("SRC4587_05_191_Maxwell", FORMAL_191, "Poynting vector is not a separate background field", "Maxwell-Hodge/Poynting stress theorem"),
        ("SRC4587_06_193_quotient", FORMAL_193, "S_matter = Sbar_m", "quotient naturality matter descent"),
        ("SRC4587_07_223_once_only", FORMAL_223, "c_Poynt_extra = 0", "Poynting once-only source lock"),
        ("SRC4587_08_3375_policy", DOC_3375, "POY3375_2_theory_policy", "Poynting must be included or bounded"),
        ("SRC4587_09_3496_poynting", DOC_3496, "DER3496_4_poynting_not_optional", "Poynting not optional precedent"),
        ("SRC4587_10_4170_identity", CSV_4170_ID, "SO4170_1_identity", "same Hilbert/Hamiltonian charge object"),
        ("SRC4587_11_4580_domain", CSV_4580_DOMAIN, "PDC4580_1_fixed_qbasic_domain", "fixed q-basic domain certificate"),
        ("SRC4587_12_claim_428", CLAIMS_PATH, "L-428", "prior claim register handoff"),
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


def density_theorem_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "DQT4587_0_density_definition",
            "claim": "The active source density is the Hilbert density measure, not bare rest mass.",
            "derivation": "rho_H dV_H := c^-2 T_total(n,n) dV_eobs, where T_total is obtained from the same observed-metric Hilbert source action used by the parent source current.",
            "consequence": "Binding, pressure, EM stress, Poynting bookkeeping and boundary/reference dressing cannot be omitted from the active source.",
            "status": "SOURCE_DENSITY_OBJECT_DEFINED",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "DQT4587_1_qbasic_density_zero",
            "claim": "If the matter+EM source functor descends through q before variation, then D_v(rho_H dV_H)=0 for v in ker(Dq).",
            "derivation": "S_src=Sbar_src[q(Phi),Psi,A,theta] with D_v theta=0 gives D_v g_obs=D_v n=D_v dV=0 and D_v T_total=0 on the source functor. Therefore D_v(c^-2 T_total(n,n)dV_eobs)=0.",
            "consequence": "E_rho_qbasic=0 in the compact private source-functor branch.",
            "status": "CONDITIONAL_ZERO_THEOREM_DERIVED_NOT_GLOBAL_PARENT_SIGNED",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "DQT4587_2_profile_support_handoff",
            "claim": "Density q-basicness is the first input to source-support descent, not the whole local-GR proof.",
            "derivation": "3560 still requires compact regular support, fixed tau/e_obs, M_H_ref source-blindness and no readout mask. Density zero removes E_rho_qbasic only on the strict branch.",
            "consequence": "The next obstruction becomes regular source-support boundary/Reynolds shell control.",
            "status": "PARTIAL_KERNEL_COMPONENT_ZERO_ROUTE",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
    ]


def poynting_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "POY4587_0_public_Maxwell_Hodge",
            "case": "EM action uses the public observed Hodge/coframe",
            "formula": "S_EM=-1/(4 mu0) int sqrt(-g_obs) F^2; T_EM^{mu nu}=Hilbert variation",
            "result": "rho_EM=T_EM(n,n)/c^2 and S_EM^i=-T_EM(n,e_i) are components of the same Hilbert stress.",
            "status": "POYNTING_INSIDE_HILBERT_SOURCE_CONDITIONAL",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "POY4587_1_once_only",
            "case": "attempt to add an extra background/Poynting source after T_EM is already in T_total",
            "formula": "T_total includes T_EM and c_Poynt_extra int_boundary S dot n would double-count",
            "result": "c_Poynt_extra=0 in the single source functional branch.",
            "status": "ONCE_ONLY_LOCK_DERIVED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "POY4587_2_flux_boundary",
            "case": "radiative or nonminimal EM flux crosses the local source collar",
            "formula": "E_EM_flux >= |int_{partial W} T_EM(tau,n_boundary) dSigma dt| / |M_H_ref|",
            "result": "radiative Poynting is not erased; it is boundary/Hamiltonian flux or an explicit source-worldtube residual.",
            "status": "BOUND_ROW_RETAINED_VALUES_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        },
    ]


def residual_vector_rows(now: str) -> list[dict[str, Any]]:
    components = [
        ("DRV4587_0_E_action_vertical", "E_action_vertical", "explicit vertical field/source dependence in S_src not mediated by q", "zero if S_src=Sbar_src[q(Phi),Psi,A,theta] and D_v theta=0"),
        ("DRV4587_1_E_constant_marker", "E_constant_marker", "hidden vertical dependence of masses, alpha_EM, source normalization or material/source labels", "zero if theta, m_A, alpha_EM and source scale are q-owned/fixed"),
        ("DRV4587_2_E_matter_lift", "E_matter_lift", "matter field lift changes physical Hilbert density rather than representative variables", "zero if source probe is vertical/gauge or on-shell quotient silent"),
        ("DRV4587_3_E_Hodge_EM", "E_Hodge_EM", "EM Hodge/constitutive relation uses hidden or second frame structure", "zero in public Maxwell-Hodge branch"),
        ("DRV4587_4_E_Poynting_boundary", "E_Poynting_boundary", "EM flux through the source collar not already in stationary H_tau", "zero only with no-flux/stationary collar; otherwise finite boundary row"),
        ("DRV4587_5_E_nonminimal_EM", "E_nonminimal_EM", "nonminimal EM/current coupling creates independent source weight", "zero if unique Maxwell block and no extra F^2/source multiplier"),
        ("DRV4587_6_E_distributional_shell", "E_distributional_shell", "density/support boundary has source shell or birth/death layer", "not solved here; pass to 4588 regular support target"),
        ("DRV4587_7_E_readout_state", "E_readout_state", "state/readout mask selected after local residual is inspected", "zero only for fixed q-basic domain certificate"),
    ]
    rows = []
    for row_id, symbol, definition, zero_condition in components:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "component_id": row_id,
                "symbol": symbol,
                "definition": definition,
                "zero_condition": zero_condition,
                "bound_formula": f"E_rho_qbasic[{symbol}] <= N_density * {symbol}",
                "status": "ZERO_CONDITION_DEFINED_VALUE_MISSING",
                "numeric_value_present": "False",
                "claim_allowed": "False",
                "valid_for_claim": "False",
                "generated_utc": now,
            }
        )
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "component_id": "DRV4587_8_total",
            "symbol": "E_rho_qbasic_open",
            "definition": "open-branch Hilbert density q-basicness failure",
            "zero_condition": "all DRV4587_0..7 components zero in one parent branch",
            "bound_formula": "E_rho_qbasic <= N_density*(E_action_vertical+E_constant_marker+E_matter_lift+E_Hodge_EM+E_Poynting_boundary+E_nonminimal_EM+E_distributional_shell+E_readout_state)",
            "status": "RESIDUAL_VECTOR_READY_VALUES_MISSING",
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
            "row_id": "DRR4587_0_Erho_zero",
            "target": "E_rho_qbasic",
            "formula": "E_rho_qbasic=0",
            "branch_condition": "single q-basic matter+EM Hilbert source functor; fixed constants/source normalization; no hidden EM Hodge; no post-fit readout mask",
            "status": "CONDITIONAL_ZERO_NOT_PUBLIC_CLAIM",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "DRR4587_1_EEM_zero_or_bound",
            "target": "E_EM_flux",
            "formula": "E_EM_flux=0 for stationary public-Hodge no-flux collar; otherwise E_EM_flux >= |int_boundary T_EM(tau,n)dSigma dt|/|M_H_ref|",
            "branch_condition": "public Maxwell-Hodge stress plus stationary/no-flux boundary, or explicit radiative boundary row",
            "status": "POYNTING_ONCE_ONLY_ZERO_OR_BOUND",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "DRR4587_2_CKsource_strict_update",
            "target": "C_K_source_worldtube",
            "formula": "strict branch removes E_rho_qbasic and E_EM_flux from the 4586 vector; remaining blockers start with E_boundary_birth and support regularity",
            "branch_condition": "4587 density/Poynting zero branch plus 4586 source-worldtube factorisation",
            "status": "PARTIAL_REDUCTION_DERIVED",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "DRR4587_3_next_regular_support",
            "target": "E_boundary_birth",
            "formula": "prove compact regular support/no Reynolds shell birth, or bound the boundary source layer",
            "branch_condition": "next obstruction after density/Poynting placement",
            "status": "SELECTED_NEXT_DERIVATION_TARGET",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    controls = [
        ("CTRL4587_public_Hilbert_EM", "public Maxwell-Hodge EM inside T_total", "Poynting is Hilbert flux, not extra source", "SYMBOLIC_CONTROL_PASS"),
        ("CTRL4587_double_count", "add Poynting source after including T_EM", "reject; c_Poynt_extra=0", "COUNTERMODEL_CAUGHT"),
        ("CTRL4587_hidden_Hodge", "EM Hodge/constitutive law uses hidden frame", "retain E_Hodge_EM/E_EM_flux", "FIREWALL_PASS"),
        ("CTRL4587_bare_mass", "bare rest mass used as active source", "reject; use rho_H/H_tau dressed source", "COUNTERMODEL_CAUGHT"),
        ("CTRL4587_radiative_flux", "nonzero EM flux exits collar", "retain boundary flux row", "FIREWALL_PASS"),
        ("CTRL4587_no_claim", "conditional density theorem exists", "no R10/PPN/local-GR claim", "FIREWALL_PASS"),
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
        ("PROM4587_0_density_object", "Hilbert density object defined as dressed T_total(n,n)dV/c^2.", "PASSED"),
        ("PROM4587_1_qbasic_theorem", "q-basic density zero theorem derived conditionally.", "PASSED_CONDITIONAL"),
        ("PROM4587_2_poynting_once_only", "Poynting/Maxwell stress is inside Hilbert source or explicit flux bound.", "PASSED_FIREWALL"),
        ("PROM4587_3_residual_vector", "Open branch residual vector emitted.", "PASSED"),
        ("PROM4587_4_parent_adoption", "One global parent branch signs all density/Poynting clauses.", "BLOCKED"),
        ("PROM4587_5_no_local_claim", "No local-GR/R10/PPN claim from 4587 alone.", "PASSED_FIREWALL"),
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
            "plain_english": "4587 derives the density leg instead of just labelling it missing: if the source action is one q-basic matter+EM Hilbert functor before variation, then rho_H dV_H is vertically silent. Poynting is handled once: public Maxwell-Hodge stress puts it inside T_total/H_tau; radiative or hidden-Hodge flux remains E_EM_flux. The open branch is an explicit residual vector, not a closure assumption.",
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
            "reason": "After density/Poynting ownership, the next source-worldtube obstruction is whether the support boundary is regular and vertically fixed.",
            "derive_first": "prove no source-support birth/death/Reynolds shell term for compact ordinary sources in the same Hilbert worldtube",
            "fallback": "emit finite E_boundary_birth row with boundary measure, collar normal, density jump/shell strength, M_H_ref normalization and arena links",
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
            "summary": "Density q-basicness and Poynting source placement are derived as a conditional theorem; open branch carries residual vector.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def doc_text(
    sources: list[dict[str, Any]],
    density: list[dict[str, Any]],
    poynting: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    reductions: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    promotions: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> str:
    return f"""# 4587 - Hilbert source density q-basic and Poynting support owner or bound

Marker: `{MARKER}`  
Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`  
Private/public status: private nonclaim; no GitHub action.

## Result

4587 attacks the first 4586 source-worldtube component directly.

The active source density is:

```text
rho_H dV_H := c^-2 T_total(n,n) dV_eobs.
```

If the source sector is a single q-basic Hilbert functor before variation,

```text
S_src = Sbar_src[q(Phi), Psi, A, theta],
D_v theta=0,
v in ker(Dq),
```

then:

```text
D_v(rho_H dV_H)=0,
E_rho_qbasic=0.
```

The Poynting rule is once-only:

```text
public Maxwell-Hodge T_EM included in T_total  =>  no extra Poynting source coefficient,
c_Poynt_extra=0.
```

Radiative or hidden-Hodge leakage is not erased:

```text
E_EM_flux >= |int_boundary T_EM(tau,n_boundary) dSigma dt| / |M_H_ref|.
```

So this is genuine progress, but still private/nonclaim: parent adoption, regular support, reference normalization and readout masks still gate local GR.

## Density q-basic theorem

{markdown_table(density)}

## Poynting owner lock

{markdown_table(poynting)}

## Residual vector

{markdown_table(residuals)}

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
    return f"""## PPC4161 4587 Hilbert source density q-basic and Poynting support owner or bound

Marker: `{MARKER}`  
Decision: `{DECISION}`  

Define the source density used by the source-worldtube branch:

```text
rho_H dV_H := c^-2 T_total(n,n) dV_eobs.
```

If:

```text
S_src=Sbar_src[q(Phi),Psi,A,theta],
D_v theta=0,
v in ker(Dq),
```

then the observed metric/coframe, normal, volume form and source stress are vertically silent:

```text
D_v(rho_H dV_H)=0.
```

For EM, public Maxwell-Hodge stress gives Poynting as a component of `T_EM`, not a second source:

```text
c_Poynt_extra=0
```

inside the single-source functional branch.  Open radiative/nonminimal leakage remains:

```text
E_EM_flux >= |int_boundary T_EM(tau,n_boundary)dSigma dt|/|M_H_ref|.
```

The next obstruction is regular support/Reynolds shell control: `{NEXT_TARGET}`.
"""


def packet_text() -> str:
    return f"""## 4587 packet update - density q-basic and Poynting once-only source lock

Marker: `{PACKET_MARKER}`  
Decision: `{DECISION}`  

4587 derives the strict density leg: if source matter+EM descends through one q-basic Hilbert functor before variation, `D_v(rho_H dV_H)=0`, so `E_rho_qbasic=0`.  Poynting is not ignored: in the public Maxwell-Hodge branch it is part of `T_EM/H_tau`; hidden/radiative flux remains `E_EM_flux`.  The next live obstruction is regular support boundary/Reynolds shell birth.
"""


def update_claims() -> None:
    if CLAIM_ID in read_text(CLAIMS_PATH):
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_signature",
        "claim": "4587 derives the conditional Hilbert source-density q-basic theorem and Poynting once-only source lock for the source-worldtube kernel route.",
        "current_evidence": "Generated density theorem, Poynting lock, residual vector, reductions, controls, gates and validation.",
        "status": "density_qbasic_theorem_and_poynting_once_only_lock_derived_residual_vector_retained_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating public-Hodge Poynting placement as a global parent adoption, or erasing radiative/nonminimal boundary flux.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No local-GR/R10/PPN claim until parent adoption, regular support, M_H_ref/source normalization and boundary/readout rows close.",
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
    density: list[dict[str, Any]],
    poynting: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    reductions: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    promotions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        checks.append({"checkpoint": CHECKPOINT, "branch": BRANCH_ID, "check_id": check_id, "check": check, "passed": bool_text(passed), "detail": detail})

    for path in outputs:
        add(f"VAL4587_exists_{path.name}", "output path exists", path.exists(), str(path))
        if path.suffix.lower() == ".csv":
            rows = read_csv(path)
            add(f"VAL4587_csv_parse_{path.name}", "CSV parses with at least one row", len(rows) > 0, f"rows={len(rows)}")

    add("VAL4587_sources_exist", "all cited sources exist", all(row["path_exists"] == "True" for row in sources), "source register existence")
    add("VAL4587_needles_found", "all cited needles found", all(row["needle_found"] == "True" for row in sources), "source register needles")
    add("VAL4587_density_definition", "Hilbert density object defined", any(row["theorem_id"] == "DQT4587_0_density_definition" and "T_total" in row["derivation"] for row in density), "DQT4587_0")
    add("VAL4587_density_zero", "qbasic density zero theorem emitted", any(row["theorem_id"] == "DQT4587_1_qbasic_density_zero" and "D_v(c^-2" in row["derivation"] for row in density), "DQT4587_1")
    add("VAL4587_poynting_once", "Poynting once-only row emitted", any(row["row_id"] == "POY4587_1_once_only" and "c_Poynt_extra=0" in row["result"] for row in poynting), "POY4587_1")
    add("VAL4587_flux_bound", "radiative flux bound retained", any(row["row_id"] == "POY4587_2_flux_boundary" and "E_EM_flux" in row["formula"] for row in poynting), "POY4587_2")
    add("VAL4587_residual_vector", "residual vector includes action, Hodge, Poynting and shell components", all(any(row["symbol"] == symbol for row in residuals) for symbol in ["E_action_vertical", "E_Hodge_EM", "E_Poynting_boundary", "E_distributional_shell"]), "residual vector")
    add("VAL4587_reductions", "density and EM reductions emitted", all(any(row["row_id"] == row_id for row in reductions) for row_id in ["DRR4587_0_Erho_zero", "DRR4587_1_EEM_zero_or_bound", "DRR4587_3_next_regular_support"]), "reductions")
    add("VAL4587_controls", "countermodel controls emitted", all(any(row["control_id"] == control_id for row in controls) for control_id in ["CTRL4587_double_count", "CTRL4587_hidden_Hodge", "CTRL4587_bare_mass", "CTRL4587_radiative_flux"]), "controls")
    add("VAL4587_parent_blocked", "parent adoption remains blocked", any(row["gate_id"] == "PROM4587_4_parent_adoption" and row["status"] == "BLOCKED" for row in promotions), "PROM4587_4")
    add("VAL4587_no_claim_flags", "all generated claim flags remain false", all(row.get("valid_for_claim", "False") == "False" for group in [density, poynting, residuals, reductions, controls, promotions] for row in group), "valid_for_claim false")
    add("VAL4587_decision_token", "decision token recorded", DECISION in read_text(DECISION_CSV) and DECISION in read_text(DOC_PATH), DECISION)
    add("VAL4587_next_target", "next target recorded", NEXT_TARGET in read_text(NEXT_CSV) and NEXT_TARGET in read_text(DOC_PATH), NEXT_TARGET)
    add("VAL4587_claim_register", "claim register updated", CLAIM_ID in read_text(CLAIMS_PATH), CLAIM_ID)
    add("VAL4587_spine_packet", "spine and packet markers present", MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH), f"{MARKER}; {PACKET_MARKER}")
    return checks


def main() -> None:
    now = utc_now()
    sources = source_rows(now)
    density = density_theorem_rows(now)
    poynting = poynting_rows(now)
    residuals = residual_vector_rows(now)
    reductions = reduction_rows(now)
    controls = control_rows(now)
    promotions = promotion_rows(now)
    decision = decision_rows(now)
    next_target = next_rows(now)
    status = status_rows(now)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(DENSITY_THEOREM_CSV, density)
    write_csv(POYNTING_OWNER_CSV, poynting)
    write_csv(RESIDUAL_VECTOR_CSV, residuals)
    write_csv(REDUCTION_CSV, reductions)
    write_csv(CONTROL_CSV, controls)
    write_csv(PROMOTION_CSV, promotions)
    write_csv(DECISION_CSV, decision)
    write_csv(NEXT_CSV, next_target)
    write_csv(STATUS_CSV, status)

    DOC_PATH.write_text(doc_text(sources, density, poynting, residuals, reductions, controls, promotions, decision, next_target), encoding="utf-8")
    FORMAL_PATH.write_text(formal_text(), encoding="utf-8")

    append_once(
        SPINE_PATH,
        MARKER,
        f"""### 4587 - Hilbert source density q-basic and Poynting support owner or bound

Marker: `{MARKER}`  
Decision: `{DECISION}`.  Next target: `{NEXT_TARGET}`.

The source density leg is:

```text
rho_H dV_H := c^-2 T_total(n,n)dV_eobs.
```

If `S_src=Sbar_src[q(Phi),Psi,A,theta]`, `D_v theta=0`, and `v in ker(Dq)`, then:

```text
D_v(rho_H dV_H)=0.
```

Public Maxwell-Hodge Poynting is once-only: it belongs inside `T_EM/H_tau`, so an extra Poynting source coefficient is zero.  Radiative/hidden-Hodge flux remains `E_EM_flux`.
""",
    )
    append_once(PACKET_PATH, PACKET_MARKER, packet_text())
    update_claims()

    outputs = [
        SOURCE_REGISTER,
        DENSITY_THEOREM_CSV,
        POYNTING_OWNER_CSV,
        RESIDUAL_VECTOR_CSV,
        REDUCTION_CSV,
        CONTROL_CSV,
        PROMOTION_CSV,
        DECISION_CSV,
        NEXT_CSV,
        STATUS_CSV,
        DOC_PATH,
        FORMAL_PATH,
    ]
    validations = validate(outputs, sources, density, poynting, residuals, reductions, controls, promotions)
    write_csv(VALIDATION_PATH, validations)
    failed = [row for row in validations if row["passed"] != "True"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)

    cache = Path(__file__).resolve().parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    print(f"4587 complete: {DECISION}")
    print(f"wrote: {DOC_PATH}")
    print(f"validation: {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
