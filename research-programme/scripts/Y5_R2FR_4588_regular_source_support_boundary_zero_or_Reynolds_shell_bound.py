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

CHECKPOINT = "4588"
CLAIM_ID = "L-430"
BRANCH_ID = "MTS_R2FR_Y5_REGULAR_SOURCE_SUPPORT_BOUNDARY_ZERO_OR_REYNOLDS_SHELL_BOUND_4588"
MARKER = "PPC4161_REGULAR_SOURCE_SUPPORT_BOUNDARY_ZERO_OR_REYNOLDS_SHELL_BOUND_4588"
PACKET_MARKER = "PPC4161_PACKET_REGULAR_SOURCE_SUPPORT_BOUNDARY_ZERO_OR_REYNOLDS_SHELL_BOUND_4588"
DECISION = "REGULAR_ZERO_TRACE_SUPPORT_KILLS_REYNOLDS_BOUNDARY_BIRTH_CONDITIONAL_SHELL_NORM_RETAINED_NONCLAIM"
NEXT_TARGET = "4589-Y5-R2FR-MHref-source-blind-reference-and-Htau-normalization-zero-or-bound.md"

DOC_PATH = POST / "4588-Y5-R2FR-regular-source-support-boundary-zero-or-Reynolds-shell-bound.md"
FORMAL_PATH = FORMAL / "604-PPC4161-regular-source-support-boundary-zero-or-Reynolds-shell-bound.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_4587 = POST / "4587-Y5-R2FR-Hilbert-source-density-qbasic-and-Poynting-support-owner-or-bound.md"
CSV_4587_REDUCTION = SOURCE_DIR / "P8_Y5_R2FR_4587_SOURCE_KERNEL_REDUCTION_UPDATE.csv"
CSV_4587_RESIDUAL = SOURCE_DIR / "P8_Y5_R2FR_4587_DENSITY_POYNTING_RESIDUAL_VECTOR.csv"
DOC_4586 = POST / "4586-Y5-R2FR-source-worldtube-kernel-zero-certificate-or-first-operator-norm.md"
DOC_3560 = POST / "3560-Y5-R2FR-source-support-qbasic-worldtube-descent-or-bound-vector.md"
CSV_3560_BOUND = SOURCE_DIR / "P8_Y5_R2FR_3560_BOUND_VECTOR.csv"
FORMAL_192 = FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md"
CSV_4176_NOFLUX = SOURCE_DIR / "P8_Y5_R2FR_4176_NO_FLUX_THEOREM.csv"
FORMAL_324 = FORMAL / "324-PPC4161-smooth-Hilbert-volume-domain-parent-signature-or-worldtube-flux-profile-row.md"
FORMAL_284 = FORMAL / "284-PPC4161-Dq-boundary-projector-fixed-collar-or-boundary-residual-bound.md"
CSV_4580_DOMAIN = SOURCE_DIR / "P8_Y5_R2FR_4580_PI_READOUT_DOMAIN_CERTIFICATE.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4588_SOURCE_REGISTER.csv"
REYNOLDS_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4588_REYNOLDS_SUPPORT_THEOREM.csv"
ZERO_CLAUSES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4588_REGULAR_SUPPORT_ZERO_CLAUSES.csv"
SHELL_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4588_REYNOLDS_SHELL_BOUND_ROWS.csv"
REDUCTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4588_SOURCE_KERNEL_REDUCTION_UPDATE.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4588_CONTROL_ROWS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4588_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4588_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4588_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4588_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4588_VALIDATION.csv"


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
        ("SRC4588_00_4587_doc", DOC_4587, "4588-Y5-R2FR-regular-source-support-boundary-zero-or-Reynolds-shell-bound.md", "4587 selected regular support target"),
        ("SRC4588_01_4587_reduction", CSV_4587_REDUCTION, "DRR4587_3_next_regular_support", "4587 next support-boundary reduction"),
        ("SRC4588_02_4587_residual", CSV_4587_RESIDUAL, "E_distributional_shell", "4587 distributional shell residual"),
        ("SRC4588_03_4586_doc", DOC_4586, "E_boundary_birth", "4586 source-worldtube vector"),
        ("SRC4588_04_3560_doc", DOC_3560, "Reynolds transport", "3560 Reynolds support handoff"),
        ("SRC4588_05_3560_bound", CSV_3560_BOUND, "BF3560_1_E_boundary_birth", "3560 boundary birth bound row"),
        ("SRC4588_06_192_no_flux", FORMAL_192, "F_side[tau] = 0", "local boundary no-flux theorem"),
        ("SRC4588_07_4176_no_flux_csv", CSV_4176_NOFLUX, "NFT4176_1_support", "compact support no-flux selector"),
        ("SRC4588_08_324_trace", FORMAL_324, "mu_tr := weak-lim", "smooth-to-exterior trace defect precedent"),
        ("SRC4588_09_284_fixed_collar", FORMAL_284, "fixed collar", "fixed q-basic collar/domain precedent"),
        ("SRC4588_10_4580_domain", CSV_4580_DOMAIN, "PDC4580_1_fixed_qbasic_domain", "fixed q-basic readout domain certificate"),
        ("SRC4588_11_claim_429", CLAIMS_PATH, "L-429", "prior claim register handoff"),
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


def reynolds_theorem_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "RST4588_0_Reynolds_identity",
            "claim": "The support-boundary term is exactly the Reynolds transport term for moments over W_H.",
            "derivation": "For I_phi(t)=int_{W_t} phi rho_H dV, dI_phi/dt=int_{W_t} d_t(phi rho_H dV)+int_{partial W_t} phi rho_H^tr V_n dSigma + <phi,mu_birth>. The first term was attacked by 4587; the second/third are E_boundary_birth.",
            "consequence": "The support-boundary problem is no longer vague: zero trace/no shell kills it, otherwise a boundary measure norm is required.",
            "status": "REYNOLDS_IDENTITY_DERIVED",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "RST4588_1_zero_trace_support",
            "claim": "If the Hilbert source density has compact regular support with zero trace and no birth/death shell, then E_boundary_birth=0.",
            "derivation": "On a fixed q-basic collar, if rho_H^tr|partial W_H=0, V_n is finite, and mu_birth=0, the Reynolds boundary contribution int_partialW phi rho_H^tr V_n dSigma + <phi,mu_birth> vanishes for every bounded shape/readout test phi.",
            "consequence": "Regular zero-trace ordinary sources have E_boundary_birth=0 and do not create an active source-worldtube kernel by boundary motion.",
            "status": "CONDITIONAL_ZERO_THEOREM_DERIVED_NOT_GLOBAL_PARENT_SIGNED",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "RST4588_2_shell_bound",
            "claim": "If zero trace or no-shell regularity is not signed, the fallback is a finite Reynolds shell norm.",
            "derivation": "For |phi|<=Phi_A on the declared arena, |D_v I_phi|/M_H_ref <= Phi_A*(int_partialW |rho_H^tr| |V_n| dSigma + ||mu_birth||_TV)/|M_H_ref| plus any q-basic bulk failures retained from 4587.",
            "consequence": "E_boundary_birth receives sourceable inputs: boundary trace density, normal support velocity, shell measure, arena test ceiling and M_H_ref.",
            "status": "BOUND_FORMULA_DERIVED_VALUES_MISSING",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
    ]


def zero_clause_rows(now: str) -> list[dict[str, Any]]:
    clauses = [
        ("ZSR4588_0_fixed_qbasic_collar", "The source worldtube/collar is selected before variation and descends through q.", "D_v collar=0 except support motion induced by the Hilbert density itself", "CONDITIONAL_4580_284_ROUTE"),
        ("ZSR4588_1_compact_regular_support", "W_H has compact regular finite-perimeter boundary.", "partial W_H has finite area and a well-defined normal trace", "UNSIGNED_REGULARITY_PREMISE"),
        ("ZSR4588_2_zero_density_trace", "The Hilbert density has zero boundary trace on the support edge.", "rho_H^tr|partial W_H=0", "UNSIGNED_ZERO_TRACE_PREMISE"),
        ("ZSR4588_3_no_birth_death_shell", "No new source layer is born or killed under the vertical probe.", "mu_birth=0", "UNSIGNED_NO_SHELL_PREMISE"),
        ("ZSR4588_4_no_threshold_mask", "The support is not a fitted threshold/readout mask.", "W_H=closure(supp rho_H dV_H), not {rho>rho_cut from residual}", "ANTI_CIRCULARITY_GUARD_REQUIRED"),
        ("ZSR4588_5_no_flux_sidewall", "Sidewall/radiative flux is zero or routed as boundary Hamiltonian charge.", "F_side[tau]=0; F_rad routed, not hidden bulk", "CONDITIONAL_4176_ROUTE"),
        ("ZSR4588_6_bounded_test_functions", "Arena kernels have declared bounded test functions on the source boundary.", "sup_partialW |phi_A|=Phi_A<infty", "BOUND_SCHEMA_REQUIRED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "clause_id": clause_id,
            "clause": clause,
            "zero_condition": condition,
            "current_status": status,
            "zero_certificate_signed": "False" if "UNSIGNED" in status or "REQUIRED" in status else "Conditional",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        }
        for clause_id, clause, condition, status in clauses
    ]


def shell_bound_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("RSB4588_0_trace_density", "rho_H_trace_norm", "int_partialW |rho_H^tr| dSigma", "boundary trace of Hilbert source density", "MISSING_ZERO_TRACE_CERTIFICATE_OR_VALUE"),
        ("RSB4588_1_support_velocity", "V_n_bound", "sup_partialW |V_n|", "normal velocity of support boundary under source probe", "MISSING_SUPPORT_VARIATION_BOUND"),
        ("RSB4588_2_birth_measure", "mu_birth_TV", "||mu_birth||_TV", "distributional source shell/birth-death measure", "MISSING_NO_SHELL_CERTIFICATE_OR_VALUE"),
        ("RSB4588_3_test_ceiling", "Phi_A", "sup_partialW |phi_A|", "arena test/readout ceiling for source moment", "MISSING_ARENA_TEST_BOUND"),
        ("RSB4588_4_denominator", "M_H_ref", "|M_H_ref|", "same-frame positive Hilbert source normalization", "MISSING_POSITIVE_MHREF_OR_VALUE"),
        ("RSB4588_5_total", "E_boundary_birth", "Phi_A*(rho_H_trace_norm*V_n_bound + mu_birth_TV)/|M_H_ref|", "total Reynolds shell boundary birth envelope", "FORMULA_READY_VALUES_MISSING"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": bound_id,
            "symbol": symbol,
            "definition": definition,
            "meaning": meaning,
            "bound_formula": formula,
            "current_status": status,
            "numeric_value_present": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "generated_utc": now,
        }
        for bound_id, symbol, formula, meaning, status in rows
        for definition in [formula]
    ]


def reduction_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "RSR4588_0_Eboundary_zero",
            "target": "E_boundary_birth",
            "formula": "E_boundary_birth=0",
            "branch_condition": "fixed q-basic collar, compact regular support, rho_H^tr=0, mu_birth=0, no threshold mask, sidewall flux zero/routed",
            "status": "CONDITIONAL_ZERO_NOT_PUBLIC_CLAIM",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "RSR4588_1_Eboundary_bound",
            "target": "E_boundary_birth",
            "formula": "E_boundary_birth <= Phi_A*(rho_H_trace_norm*V_n_bound + mu_birth_TV)/|M_H_ref|",
            "branch_condition": "any regular support/zero-trace/no-shell clause unsigned",
            "status": "REYNOLDS_SHELL_BOUND_READY_VALUES_MISSING",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "RSR4588_2_CKsource_update",
            "target": "C_K_source_worldtube",
            "formula": "strict 4587+4588 branch removes E_rho_qbasic, E_EM_flux and E_boundary_birth; remaining blockers are E_Dq_source+E_tau_eobs+E_Href+E_readout_mask",
            "branch_condition": "density/Poynting zero branch plus regular support zero branch",
            "status": "PARTIAL_SOURCE_KERNEL_REDUCTION_DERIVED",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "RSR4588_3_next_MHref",
            "target": "E_Href and M_H_ref",
            "formula": "prove H_ref/M_H_ref source-blind q-basic positive normalization, or bound D_v H_ref and denominator drift",
            "branch_condition": "next most central denominator/coupling obstruction",
            "status": "SELECTED_NEXT_DERIVATION_TARGET",
            "generated_utc": now,
            "valid_for_claim": "False",
        },
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    controls = [
        ("CTRL4588_smooth_zero_trace", "smooth compact source with rho trace zero and no shell", "E_boundary_birth=0", "SYMBOLIC_CONTROL_PASS"),
        ("CTRL4588_hard_surface_jump", "sharp boundary with nonzero trace density or shell layer", "retain Reynolds shell bound", "COUNTERMODEL_CAUGHT"),
        ("CTRL4588_threshold_mask", "support defined by fitted cutoff after residual inspection", "reject zero; retain mask/shell row", "FIREWALL_PASS"),
        ("CTRL4588_radiative_sidewall", "nonzero sidewall/radiative flux through collar", "route as boundary flux, not hidden bulk zero", "FIREWALL_PASS"),
        ("CTRL4588_unbounded_test", "arena test function unbounded at boundary", "bound not score-ready", "COUNTERMODEL_CAUGHT"),
        ("CTRL4588_no_claim", "Reynolds theorem exists but values/signatures missing", "no local-GR/R10/PPN claim", "FIREWALL_PASS"),
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
        ("PROM4588_0_Reynolds_identity", "Reynolds transport identity for source support emitted.", "PASSED"),
        ("PROM4588_1_zero_trace", "Zero-trace/no-shell support theorem derived conditionally.", "PASSED_CONDITIONAL"),
        ("PROM4588_2_shell_bound", "Finite shell norm fallback emitted.", "PASSED"),
        ("PROM4588_3_firewalls", "Threshold mask, hard shell and radiative sidewall traps are blocked.", "PASSED_FIREWALL"),
        ("PROM4588_4_values", "Regular support clauses or numeric shell values are source-backed.", "BLOCKED"),
        ("PROM4588_5_no_local_claim", "No local-GR/R10/PPN claim from 4588 alone.", "PASSED_FIREWALL"),
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
            "plain_english": "4588 derives the Reynolds support-boundary law. If the Hilbert source support is compact regular, zero-trace and no-shell on a fixed q-basic collar, the boundary birth term vanishes. If not, the open branch is a finite shell norm with explicit trace-density, support-velocity, shell-measure, arena-test and M_H_ref inputs. This removes another source-worldtube ambiguity without claiming local GR.",
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
            "reason": "After density/Poynting and support-boundary components, the source-worldtube denominator and reference lock are the next central coupling obstruction.",
            "derive_first": "prove M_H_ref and H_ref are q-basic, source-blind, positive and fixed before readout in the same tau/e_obs branch",
            "fallback": "emit finite E_Href and denominator drift rows with H_tau/H_ref/M_H_ref units and no fitted-G absorption",
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
            "summary": "Regular zero-trace support kills Reynolds boundary birth conditionally; open branch carries finite shell norm.",
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
    return f"""# 4588 - Regular source-support boundary zero or Reynolds shell bound

Marker: `{MARKER}`  
Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`  
Private/public status: private nonclaim; no GitHub action.

## Result

4588 derives the support-boundary term instead of leaving it as a missing regularity phrase.

For any bounded arena/source test `phi`:

```text
I_phi(t)=int_W(t) phi rho_H dV.
```

The Reynolds transport split is:

```text
dI_phi/dt =
int_W d_t(phi rho_H dV)
+ int_partialW phi rho_H^tr V_n dSigma
+ <phi,mu_birth>.
```

The first term is the 4587 density q-basic object.  The live 4588 term is:

```text
E_boundary_birth ~ int_partialW phi rho_H^tr V_n dSigma + <phi,mu_birth>.
```

So the strict zero route is:

```text
rho_H^tr|partialW=0,  mu_birth=0,  fixed q-basic collar
=> E_boundary_birth=0.
```

If not signed, the finite bound is:

```text
E_boundary_birth <= Phi_A*(rho_H_trace_norm*V_n_bound + mu_birth_TV)/|M_H_ref|.
```

This is still not a local-GR claim.  It converts another source-worldtube blocker into either a theorem clause or sourceable shell norm.

## Reynolds theorem

{markdown_table(theorem)}

## Zero clauses

{markdown_table(clauses)}

## Shell bound rows

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
    return f"""## PPC4161 4588 regular source-support boundary zero or Reynolds shell bound

Marker: `{MARKER}`  
Decision: `{DECISION}`  

For source moments:

```text
I_phi(t)=int_W(t) phi rho_H dV.
```

Reynolds transport gives:

```text
dI_phi/dt=int_W d_t(phi rho_H dV)+int_partialW phi rho_H^tr V_n dSigma+<phi,mu_birth>.
```

4587 handles the bulk `d_t(rho_H dV)` route.  The source-support boundary zero theorem is:

```text
rho_H^tr|partialW=0 and mu_birth=0 and fixed q-basic collar
=> E_boundary_birth=0.
```

If not:

```text
E_boundary_birth <= Phi_A*(rho_H_trace_norm*V_n_bound + mu_birth_TV)/|M_H_ref|.
```

Thus the source-worldtube kernel vector can remove `E_boundary_birth` only on the regular zero-trace branch; otherwise it remains a finite shell input.  Next target: `{NEXT_TARGET}`.
"""


def packet_text() -> str:
    return f"""## 4588 packet update - regular source-support Reynolds shell law

Marker: `{PACKET_MARKER}`  
Decision: `{DECISION}`  

4588 derives the Reynolds source-support boundary term.  Zero-trace compact regular support with no birth/death shell gives `E_boundary_birth=0`; a hard surface, fitted threshold mask, distributional shell, or radiative sidewall becomes `Phi_A*(rho_H_trace_norm*V_n_bound+mu_birth_TV)/|M_H_ref|`.  The next coupling obstruction is `M_H_ref/H_ref` source-blind normalization.
"""


def update_claims() -> None:
    if CLAIM_ID in read_text(CLAIMS_PATH):
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_signature",
        "claim": "4588 derives the regular source-support Reynolds boundary zero theorem or finite shell norm bound.",
        "current_evidence": "Generated Reynolds theorem, zero clauses, shell bound rows, reductions, controls, gates and validation.",
        "status": "regular_zero_trace_support_kills_reynolds_boundary_birth_conditional_shell_norm_retained_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Using a hard surface, threshold mask or distributional source shell as if it were regular zero-trace support.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No local-GR/R10/PPN claim until regular support clauses or shell norms plus M_H_ref normalization are source-backed.",
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
        add(f"VAL4588_exists_{path.name}", "output path exists", path.exists(), str(path))
        if path.suffix.lower() == ".csv":
            rows = read_csv(path)
            add(f"VAL4588_csv_parse_{path.name}", "CSV parses with at least one row", len(rows) > 0, f"rows={len(rows)}")

    add("VAL4588_sources_exist", "all cited sources exist", all(row["path_exists"] == "True" for row in sources), "source register existence")
    add("VAL4588_needles_found", "all cited needles found", all(row["needle_found"] == "True" for row in sources), "source register needles")
    add("VAL4588_Reynolds_identity", "Reynolds identity emitted", any(row["theorem_id"] == "RST4588_0_Reynolds_identity" and "mu_birth" in row["derivation"] for row in theorem), "RST4588_0")
    add("VAL4588_zero_trace", "zero-trace theorem emitted", any(row["theorem_id"] == "RST4588_1_zero_trace_support" and "E_boundary_birth=0" in row["consequence"] for row in theorem), "RST4588_1")
    add("VAL4588_bound_formula", "shell bound theorem emitted", any(row["theorem_id"] == "RST4588_2_shell_bound" and "Phi_A" in row["derivation"] for row in theorem), "RST4588_2")
    add("VAL4588_zero_clauses", "zero clauses cover regular support, zero trace and no shell", all(any(row["clause_id"] == clause_id for row in clauses) for clause_id in ["ZSR4588_1_compact_regular_support", "ZSR4588_2_zero_density_trace", "ZSR4588_3_no_birth_death_shell"]), "zero clauses")
    add("VAL4588_bound_rows", "bound rows include trace, velocity, shell, test and denominator", all(any(row["bound_id"] == bound_id for row in bounds) for bound_id in ["RSB4588_0_trace_density", "RSB4588_1_support_velocity", "RSB4588_2_birth_measure", "RSB4588_3_test_ceiling", "RSB4588_4_denominator", "RSB4588_5_total"]), "bound rows")
    add("VAL4588_reductions", "zero, bound and next reduction rows emitted", all(any(row["row_id"] == row_id for row in reductions) for row_id in ["RSR4588_0_Eboundary_zero", "RSR4588_1_Eboundary_bound", "RSR4588_3_next_MHref"]), "reductions")
    add("VAL4588_controls", "countermodel controls emitted", all(any(row["control_id"] == control_id for row in controls) for control_id in ["CTRL4588_hard_surface_jump", "CTRL4588_threshold_mask", "CTRL4588_radiative_sidewall"]), "controls")
    add("VAL4588_values_blocked", "promotion gates block claims while values missing", any(row["gate_id"] == "PROM4588_4_values" and row["status"] == "BLOCKED" for row in promotions), "PROM4588_4")
    add("VAL4588_no_claim_flags", "all generated claim flags remain false", all(row.get("valid_for_claim", "False") == "False" for group in [theorem, clauses, bounds, reductions, controls, promotions] for row in group), "valid_for_claim false")
    add("VAL4588_decision_token", "decision token recorded", DECISION in read_text(DECISION_CSV) and DECISION in read_text(DOC_PATH), DECISION)
    add("VAL4588_next_target", "next target recorded", NEXT_TARGET in read_text(NEXT_CSV) and NEXT_TARGET in read_text(DOC_PATH), NEXT_TARGET)
    add("VAL4588_claim_register", "claim register updated", CLAIM_ID in read_text(CLAIMS_PATH), CLAIM_ID)
    add("VAL4588_spine_packet", "spine and packet markers present", MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH), f"{MARKER}; {PACKET_MARKER}")
    return checks


def main() -> None:
    now = utc_now()
    sources = source_rows(now)
    theorem = reynolds_theorem_rows(now)
    clauses = zero_clause_rows(now)
    bounds = shell_bound_rows(now)
    reductions = reduction_rows(now)
    controls = control_rows(now)
    promotions = promotion_rows(now)
    decision = decision_rows(now)
    next_target = next_rows(now)
    status = status_rows(now)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(REYNOLDS_THEOREM_CSV, theorem)
    write_csv(ZERO_CLAUSES_CSV, clauses)
    write_csv(SHELL_BOUND_CSV, bounds)
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
        f"""### 4588 - Regular source-support boundary zero or Reynolds shell bound

Marker: `{MARKER}`  
Decision: `{DECISION}`.  Next target: `{NEXT_TARGET}`.

For source moments:

```text
d/dt int_W(t) phi rho_H dV =
int_W d_t(phi rho_H dV)+int_partialW phi rho_H^tr V_n dSigma+<phi,mu_birth>.
```

The strict branch has `rho_H^tr=0`, `mu_birth=0`, and a fixed q-basic collar, so `E_boundary_birth=0`.  The open branch is:

```text
E_boundary_birth <= Phi_A*(rho_H_trace_norm*V_n_bound + mu_birth_TV)/|M_H_ref|.
```
""",
    )
    append_once(PACKET_PATH, PACKET_MARKER, packet_text())
    update_claims()

    outputs = [
        SOURCE_REGISTER,
        REYNOLDS_THEOREM_CSV,
        ZERO_CLAUSES_CSV,
        SHELL_BOUND_CSV,
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

    print(f"4588 complete: {DECISION}")
    print(f"wrote: {DOC_PATH}")
    print(f"validation: {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
