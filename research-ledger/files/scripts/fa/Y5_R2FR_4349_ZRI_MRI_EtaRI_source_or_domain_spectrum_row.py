from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4349"
CLAIM_ID = "L-190"
BRANCH = "MTS_R2FR_Y5_ZRI_MRI_ETARI_SOURCE_OR_DOMAIN_SPECTRUM_ROW_4349"
DECISION = "ZRI_PRINCIPAL_SIGN_AND_MINIMAL_MRI_ZERO_DERIVED_DOMAIN_SPECTRUM_SYMBOLIC_ETARI_BOUND_OPEN_NONCLAIM"
MARKER = "PPC4161_ZRI_MRI_ETARI_SOURCE_OR_DOMAIN_SPECTRUM_ROW_4349"
PACKET_MARKER = "PPC4161_PACKET_ZRI_MRI_ETARI_SOURCE_OR_DOMAIN_SPECTRUM_ROW_4349"
NEXT_TARGET = "4350-Y5-R2FR-RI-boundary-anchor-and-EtaRI-correction-bound.md"

FORMAL_PATH = FORMAL / "365-PPC4161-ZRI-MRI-EtaRI-source-or-domain-spectrum-row.md"
DOC_PATH = POST / "4349-Y5-R2FR-ZRI-MRI-EtaRI-source-or-domain-spectrum-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4349_VALIDATION.csv"
GENERATED_UTC = datetime.now(timezone.utc).isoformat(timespec="seconds")

SOURCES = [
    (
        "SRC4349_00_4348_next",
        FORMAL / "364-PPC4161-lambda-RI-positive-domain-or-bound-input-pack.md",
        "4349-Y5-R2FR-ZRI-MRI-EtaRI-source-or-domain-spectrum-row.md",
        "4348 handoff selecting component rows.",
    ),
    (
        "SRC4349_01_4343_flat",
        FORMAL / "359-PPC4161-parent-action-owner-for-KGamma-or-Kperp-sector-bound-runner.md",
        "S_RI^flat=int_U Lambda_nu [Box A_Gamma^nu + partial^nu Gamma_eff]",
        "Flat RI owner block fixes unit second-order principal coefficient.",
    ),
    (
        "SRC4349_02_4343_curved",
        FORMAL / "359-PPC4161-parent-action-owner-for-KGamma-or-Kperp-sector-bound-runner.md",
        "L_RI A^nu=(Box delta^nu_sigma+Ric^nu_sigma)A^sigma",
        "Curved RI operator has Box principal block plus Ricci lower-order correction.",
    ),
    (
        "SRC4349_03_4344_operator",
        FORMAL / "360-PPC4161-adjoint-zero-and-boundary-kernel-proof-or-first-Kperp-score-row.md",
        "L_RI^dagger = -D_i(Z_RI D^i) + M_RI^2 + V_Ric - E_RI.",
        "Adjoint operator form.",
    ),
    (
        "SRC4349_04_4348_lambda",
        FORMAL / "364-PPC4161-lambda-RI-positive-domain-or-bound-input-pack.md",
        "lambda_RI,lower",
        "Claim-usable lower-bound law.",
    ),
    (
        "SRC4349_05_4348_dirichlet",
        FORMAL / "364-PPC4161-lambda-RI-positive-domain-or-bound-input-pack.md",
        "lambda_dom >= lambda_1^D(D_RI); for a unit interval/collar smoke lambda_1^D=pi^2/ell_RI^2",
        "Dirichlet/anchored domain spectrum rule.",
    ),
    (
        "SRC4349_06_4348_neumann",
        FORMAL / "364-PPC4161-lambda-RI-positive-domain-or-bound-input-pack.md",
        "normal flux is zero but the constant mode remains admissible",
        "Neumann zero-mode guard.",
    ),
    (
        "SRC4349_07_1529_zero_mode",
        POST / "1529-Y5-parent-boundary-no-flux-zero-mode-certificate-or-lambda-phi-bound-inputs.md",
        "Neumann/no-flux requires mean(lambda_phi)=0 or a fixed reference value",
        "Older boundary/zero-mode certificate warning.",
    ),
    (
        "SRC4349_08_4315_eta",
        FORMAL / "07-unification-spine.md",
        "feeding `R_EM_Poynting`, `Eta_H`, and `S_U`",
        "EM/Hodge residual precedent for correction terms feeding Eta-like rows.",
    ),
    (
        "SRC4349_09_216_static_guard",
        FORMAL / "216-PPC4161-Kperp-boundary-zero-or-demotion.md",
        "elliptic/static proof != hyperbolic incoming-mode proof.",
        "Static proof firewall remains active.",
    ),
]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        return ""


def find_line(path: Path, needle: str) -> str:
    text = read_text(path)
    index = text.find(needle)
    if index < 0:
        return ""
    return str(text[:index].count("\n") + 1)


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: str(row.get(key, "")) for key in fields})


def md_cell(value: object) -> str:
    return str(value).replace("|", r"\|").replace("\n", "<br>")


def md_table(rows: List[Dict[str, str]], fields: List[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + block.strip() + "\n", encoding="utf-8")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, path, needle, role in SOURCES:
        line_number = find_line(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(bool(line_number)),
                "line_number": line_number,
                "role": role,
                "valid_for_claim": "False",
            }
        )
    return rows


def principal_rows() -> List[Dict[str, str]]:
    return [
        {
            "principal_id": "ZRI4349_0_flat_principal",
            "quantity": "Z_RI,min",
            "derived_value": "1",
            "derivation": "In the fixed flat RI owner block L_RI=Box, the static elliptic adjoint has principal part -Delta with unit coefficient.",
            "source": "359-PPC4161-parent-action-owner-for-KGamma-or-Kperp-sector-bound-runner.md",
            "scope": "fixed flat/static local candidate with chosen units",
            "public_parent_status": "PRIVATE_CANDIDATE_NOT_PUBLIC_PARENT_ADOPTED",
            "claim_valid": "False",
            "valid_for_claim": "False",
        },
        {
            "principal_id": "ZRI4349_1_curved_principal",
            "quantity": "Z_RI,min",
            "derived_value": "1 + O(metric_principal_deformation)",
            "derivation": "L_RI=(Box delta+Ric) keeps Box as the principal symbol; Ricci is lower-order. Principal deformation is zero only in the fixed observed coframe/static normalization.",
            "source": "359-PPC4161-parent-action-owner-for-KGamma-or-Kperp-sector-bound-runner.md",
            "scope": "curved static collar with fixed metric principal block",
            "public_parent_status": "NEEDS_FIXED_COFRAME_AND_OPERATOR_NORMALIZATION",
            "claim_valid": "False",
            "valid_for_claim": "False",
        },
        {
            "principal_id": "ZRI4349_2_claim_gate",
            "quantity": "Z_RI,min_claim",
            "derived_value": "MISSING_PARENT_ADOPTION_AND_UNITS",
            "derivation": "A claim row must cite the adopted parent operator, metric/coframe normalization, field norm and allowed domain before using Z_RI,min=1.",
            "source": "364-PPC4161-lambda-RI-positive-domain-or-bound-input-pack.md",
            "scope": "claim gate",
            "public_parent_status": "BLOCKED",
            "claim_valid": "False",
            "valid_for_claim": "False",
        },
    ]


def mass_rows() -> List[Dict[str, str]]:
    return [
        {
            "mass_id": "MRI4349_0_minimal_operator",
            "quantity": "M_RI,min^2",
            "derived_value": "0",
            "derivation": "The explicit flat and Ricci-corrected RI owner candidates contain no independent positive mass/Hessian term; the Ricci term is lower-order correction, not a guaranteed mass floor.",
            "scope": "minimal RI owner candidate",
            "effect": "mass-only zero-mode route is unavailable in the minimal branch",
            "claim_valid": "False",
            "valid_for_claim": "False",
        },
        {
            "mass_id": "MRI4349_1_mass_gap_extension",
            "quantity": "M_RI,min^2",
            "derived_value": "MISSING_IF_NONMINIMAL_EXTENSION",
            "derivation": "A positive mass floor would need an explicit parent Hessian/potential term in S_RI, not an after-the-fact regularizer.",
            "scope": "possible nonminimal extension",
            "effect": "could rescue Neumann constant mode only if parent-derived",
            "claim_valid": "False",
            "valid_for_claim": "False",
        },
    ]


def domain_rows() -> List[Dict[str, str]]:
    return [
        {
            "domain_id": "DOMSPEC4349_0_anchored_dirichlet",
            "quantity": "lambda_dom",
            "symbolic_value": "pi^2/ell_RI^2",
            "conditions": "Lambda|partialD_RI=0 or residual representative anchored; finite collar length ell_RI; fixed self-adjoint domain",
            "what_is_filled": "analytic spectrum law",
            "what_remains": "parent-owned boundary anchor and physical ell_RI/geometry",
            "valid_for_claim": "False",
        },
        {
            "domain_id": "DOMSPEC4349_1_neumann_constant",
            "quantity": "lambda_dom",
            "symbolic_value": "0",
            "conditions": "no-flux boundary with constant mode retained",
            "what_is_filled": "zero-mode danger explicitly fixed",
            "what_remains": "needs M_RI,min^2 > Eta_RI+B_RI,neg; minimal branch has M_RI,min^2=0",
            "valid_for_claim": "False",
        },
        {
            "domain_id": "DOMSPEC4349_2_neumann_projected",
            "quantity": "lambda_dom",
            "symbolic_value": "lambda_1^+(D_RI)",
            "conditions": "constant/gauge kernel projected out by quotient/source/reference before variation",
            "what_is_filled": "theorem route",
            "what_remains": "zero-mode projector/source-reference certificate",
            "valid_for_claim": "False",
        },
        {
            "domain_id": "DOMSPEC4349_3_weighted_exterior",
            "quantity": "lambda_dom",
            "symbolic_value": "lambda_weighted",
            "conditions": "finite-energy exterior decay plus Hardy/Poincare inequality",
            "what_is_filled": "fallback route label",
            "what_remains": "weighted inequality and exterior-end source",
            "valid_for_claim": "False",
        },
    ]


def eta_rows() -> List[Dict[str, str]]:
    return [
        {
            "eta_id": "ETA4349_0_curvature_lower_order",
            "component": "Ricci/lower-order correction",
            "bound_symbol": "Eta_Ric",
            "definition": "operator norm of the negative part of V_Ric-E_RI on the selected RI collar",
            "zero_route": "flat fixed local branch or Ricci/lower-order term nonnegative in the chosen sector",
            "bound_route": "Eta_Ric <= ||(E_RI - V_Ric)_+||_op",
            "status": "BOUND_FORMULA_READY_VALUE_MISSING",
            "valid_for_claim": "False",
        },
        {
            "eta_id": "ETA4349_1_commutator_domain",
            "component": "operator/domain commutator",
            "bound_symbol": "Eta_comm",
            "definition": "negative contribution from moving collar, non-fixed Green operator, or D_v/domain commutators",
            "zero_route": "fixed domain and Green data before variation",
            "bound_route": "source absolute commutator norm",
            "status": "ZERO_OR_BOUND_OPEN",
            "valid_for_claim": "False",
        },
        {
            "eta_id": "ETA4349_2_EM_Poynting_Hodge",
            "component": "EM/Poynting/Hodge residual feeding correction budget",
            "bound_symbol": "Eta_EM",
            "definition": "same-collar constitutive/Hodge or radiative residual that can enter lower-order correction budget",
            "zero_route": "same-Hodge Maxwell/Hilbert branch with no independent constitutive term",
            "bound_route": "Delta_Hodge/constitutive no-cancellation envelope",
            "status": "ROUTE_AVAILABLE_VALUE_MISSING",
            "valid_for_claim": "False",
        },
        {
            "eta_id": "ETA4349_3_boundary_negative",
            "component": "negative boundary form",
            "bound_symbol": "B_RI,neg",
            "definition": "negative part of the adjoint boundary/corner quadratic form",
            "zero_route": "signed Dirichlet/decay/routed Hamiltonian boundary",
            "bound_route": "B_RI,neg <= C_trace ||boundary_data||",
            "status": "BOUNDARY_CERTIFICATE_MISSING",
            "valid_for_claim": "False",
        },
        {
            "eta_id": "ETA4349_4_total",
            "component": "total correction ceiling",
            "bound_symbol": "Eta_RI,total",
            "definition": "Eta_RI,total = Eta_Ric + Eta_comm + Eta_EM + B_RI,neg",
            "zero_route": "all components theorem-zero in same fixed static collar",
            "bound_route": "absolute sum, no cancellation",
            "status": "FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": "False",
        },
    ]


def lambda_rows() -> List[Dict[str, str]]:
    return [
        {
            "lambda_id": "LAM4349_0_minimal_anchored_symbolic",
            "route": "minimal RI + anchored Dirichlet",
            "lambda_lower": "pi^2/ell_RI^2 - Eta_RI,total",
            "closure_condition": "Eta_RI,total < pi^2/ell_RI^2",
            "filled_now": "Z_RI,min=1 in the normalized candidate; M_RI,min^2=0; lambda_dom symbolic",
            "still_missing": "parent boundary anchor, ell_RI/geometry, Eta_RI,total values",
            "claim_valid": "False",
            "valid_for_claim": "False",
        },
        {
            "lambda_id": "LAM4349_1_minimal_flat_smoke",
            "route": "minimal flat unit interval smoke",
            "lambda_lower": "pi^2",
            "closure_condition": "ell_RI=1, Eta_RI,total=0, boundary anchor signed",
            "filled_now": "analytic normalization only",
            "still_missing": "not physical until ell_RI/domain/boundary/corrections are source-backed",
            "claim_valid": "False",
            "valid_for_claim": "False",
        },
        {
            "lambda_id": "LAM4349_2_neumann_minimal_failure",
            "route": "minimal RI + Neumann constant mode",
            "lambda_lower": "-Eta_RI,total",
            "closure_condition": "fails unless Eta_RI,total<0, impossible for nonnegative ceiling",
            "filled_now": "minimal mass-only route rejected",
            "still_missing": "positive mass floor or zero-mode projector",
            "claim_valid": "False",
            "valid_for_claim": "False",
        },
        {
            "lambda_id": "LAM4349_3_neumann_projected",
            "route": "minimal RI + Neumann zero-mode projected",
            "lambda_lower": "lambda_1^+(D_RI)-Eta_RI,total",
            "closure_condition": "Eta_RI,total < lambda_1^+(D_RI)",
            "filled_now": "formula route",
            "still_missing": "zero-mode projector and lambda_1^+ row",
            "claim_valid": "False",
            "valid_for_claim": "False",
        },
    ]


def runner_rows() -> List[Dict[str, str]]:
    return [
        {
            "runner_id": "RUN4349_0_current",
            "branch_input": "current corpus through 4348",
            "action": "FILL_SYMBOLIC_ZRI_MRI_DOMAIN_ROWS_KEEP_CLAIM_FALSE",
            "output": "Z_RI,min=1 candidate; M_RI,min^2=0 minimal; lambda_dom laws; Eta decomposition",
            "claim_policy": "no local-GR/PPN/R10/clock/orbital claim",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4349_1_best_zero_future",
            "branch_input": "anchored Dirichlet residual domain plus Eta_RI,total < pi^2/ell_RI^2",
            "action": "ALLOW_LAMBDA_RI_POSITIVE_FOR_OWNER_TAIL_ZERO",
            "output": "Lambda=0 leg can fire in 4347 owner-tail theorem",
            "claim_policy": "only after parent boundary/domain/correction rows are signed",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4349_2_neumann_warning",
            "branch_input": "minimal RI with Neumann constant mode",
            "action": "REJECT_MASS_ONLY_ROUTE_IN_MINIMAL_BRANCH",
            "output": "constant zero mode survives unless mass gap or projector is added",
            "claim_policy": "do not use no-flux alone as lambda proof",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4349_3_next",
            "branch_input": "symbolic component rows filled",
            "action": "SOURCE_BOUNDARY_ANCHOR_AND_ETARI_BOUND",
            "output": NEXT_TARGET,
            "claim_policy": "claim remains blocked until Eta and boundary/domain rows are real",
            "valid_for_claim": "False",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    return [
        {
            "firewall_id": "FW4349_0",
            "forbidden_shortcut": "Promoting Z_RI,min=1 candidate to public parent fact",
            "reason": "the RI owner block is still a private/candidate parent extension, and units/domain must be fixed.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4349_1",
            "forbidden_shortcut": "Using no-flux/Neumann as a positive gap",
            "reason": "minimal RI has M_RI,min^2=0, so a constant zero mode survives unless projected out.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4349_2",
            "forbidden_shortcut": "Setting Eta_RI=0 in curved/local physical branch by wish",
            "reason": "Ricci, commutator, EM/Hodge and boundary negative components need theorem-zero or absolute bounds.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4349_3",
            "forbidden_shortcut": "Cancelling Eta components against each other",
            "reason": "Eta_RI,total is an absolute ceiling, not a tuned signed sum.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4349_0",
            "decision": DECISION,
            "reason": "the current RI owner candidate does fill the principal sign and minimal mass status symbolically, but physical positivity still depends on domain anchor and Eta/Bneg bounds",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4349_0",
            "item": "Z_RI,min",
            "status": "CANDIDATE_DERIVED_AS_1",
            "notes": "unit principal sign follows from the flat/static RI Box operator, pending parent adoption and units.",
        },
        {
            "status_id": "STAT4349_1",
            "item": "M_RI,min^2",
            "status": "MINIMAL_BRANCH_ZERO",
            "notes": "no mass-only zero-mode rescue in the explicit minimal RI owner block.",
        },
        {
            "status_id": "STAT4349_2",
            "item": "domain/Eta",
            "status": "SYMBOLIC_DOMAIN_AND_ETA_BOUND_OPEN",
            "notes": "best condition is Eta_RI,total < pi^2/ell_RI^2 on anchored residual domain.",
        },
        {
            "status_id": "STAT4349_3",
            "item": "next target",
            "status": "BOUNDARY_ANCHOR_AND_ETARI_BOUND",
            "notes": NEXT_TARGET,
        },
    ]


def next_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_target_id": "NT4349_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can the anchored residual boundary/domain and Eta_RI,total correction ceiling be proved small enough to make the minimal RI gap positive?",
            "preferred_route": "parent-sign Dirichlet/anchored residual domain and prove Eta_Ric=Eta_comm=Eta_EM=B_RI,neg=0 in the same static collar",
            "fallback_route": "source absolute bounds for Eta_RI,total and ell_RI, then keep owner-tail finite-bound runner nonclaim",
            "valid_for_claim": "False",
        }
    ]


def build_tables() -> Dict[str, List[Dict[str, str]]]:
    return {
        "sources": source_rows(),
        "principal": principal_rows(),
        "mass": mass_rows(),
        "domain": domain_rows(),
        "eta": eta_rows(),
        "lambda": lambda_rows(),
        "runner": runner_rows(),
        "firewall": firewall_rows(),
        "decision": decision_rows(),
        "status": status_rows(),
        "next": next_rows(),
    }


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    formal = f"""# 365 PPC4161 ZRI MRI EtaRI source or domain spectrum row

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint does not prove public local GR, Newton, R10, PPN, clock safety, orbital safety, WEP safety, Maxwell closure, source coupling closure, or a fundamental prediction of `G_N`.

## Result

4349 fills the first real symbolic component rows for the `lambda_RI` gate.

From the fixed flat RI owner candidate:

```text
S_RI^flat = int Lambda_nu [Box A_Gamma^nu + partial^nu Gamma_eff],
```

the static adjoint principal block is the unit elliptic operator:

```text
Z_RI,min = 1
```

inside the selected normalization. The curved candidate

```text
L_RI A^nu = (Box delta^nu_sigma + Ric^nu_sigma) A^sigma
```

keeps the same `Box` principal symbol; the Ricci term is lower-order and belongs in the correction ceiling, not in the principal sign.

The explicit minimal RI owner block has no independent positive mass/Hessian term:

```text
M_RI,min^2 = 0
```

so the mass-only Neumann route is not available unless a new parent-derived mass term is added.

The best current symbolic positive-gap route is therefore:

```text
lambda_RI,lower = pi^2/ell_RI^2 - Eta_RI,total
Eta_RI,total = Eta_Ric + Eta_comm + Eta_EM + B_RI,neg.
```

This is progress: the remaining problem is now sharply stated as a boundary/domain and correction-bound problem:

```text
Eta_RI,total < pi^2/ell_RI^2.
```

No claim fires, because `ell_RI`, the anchored residual boundary/domain, and the `Eta_RI,total` components are not parent-signed.

## Source Register

{md_table(tables["sources"], ["source_id", "path", "path_exists", "needle_found", "line_number", "role", "valid_for_claim"])}

## Principal Rows

{md_table(tables["principal"], ["principal_id", "quantity", "derived_value", "derivation", "source", "scope", "public_parent_status", "claim_valid", "valid_for_claim"])}

## Mass Rows

{md_table(tables["mass"], ["mass_id", "quantity", "derived_value", "derivation", "scope", "effect", "claim_valid", "valid_for_claim"])}

## Domain Spectrum Rows

{md_table(tables["domain"], ["domain_id", "quantity", "symbolic_value", "conditions", "what_is_filled", "what_remains", "valid_for_claim"])}

## Eta Decomposition Rows

{md_table(tables["eta"], ["eta_id", "component", "bound_symbol", "definition", "zero_route", "bound_route", "status", "valid_for_claim"])}

## Lambda Candidate Rows

{md_table(tables["lambda"], ["lambda_id", "route", "lambda_lower", "closure_condition", "filled_now", "still_missing", "claim_valid", "valid_for_claim"])}

## Runner

{md_table(tables["runner"], ["runner_id", "branch_input", "action", "output", "claim_policy", "valid_for_claim"])}

## Claim Firewall

{md_table(tables["firewall"], ["firewall_id", "forbidden_shortcut", "reason", "status", "valid_for_claim"])}

## Decision

{md_table(tables["decision"], ["decision_id", "decision", "reason", "next_action", "claim_allowed", "valid_for_claim"])}

## Status

{md_table(tables["status"], ["status_id", "item", "status", "notes"])}

## Next Target

{md_table(tables["next"], ["next_target_id", "next_target", "target_question", "preferred_route", "fallback_route", "valid_for_claim"])}
"""
    post = f"""# 4349 Y5-R2FR ZRI MRI EtaRI source or domain spectrum row

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4349 fills what can honestly be filled:

```text
Z_RI,min = 1                     # normalized RI principal block, private/candidate
M_RI,min^2 = 0                   # minimal RI owner has no mass gap
lambda_RI,lower = pi^2/ell_RI^2 - Eta_RI,total
Eta_RI,total = Eta_Ric + Eta_comm + Eta_EM + B_RI,neg
```

So the next target is not another lambda formula. It is proving or bounding:

```text
Eta_RI,total < pi^2/ell_RI^2
```

on a parent-signed anchored residual domain.

## Handoff

{md_table(tables["next"], ["next_target", "target_question", "preferred_route", "fallback_route"])}
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")
    DOC_PATH.write_text(post, encoding="utf-8")


def append_claim_once() -> None:
    path = FORMAL / "02-claims-register.csv"
    existing = read_text(path)
    if CLAIM_ID in existing:
        return
    with path.open("a", newline="", encoding="utf-8") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        writer = csv.writer(handle)
        writer.writerow(
            [
                CLAIM_ID,
                "local_gr",
                (
                    "4349 fills the first symbolic component rows for the RI adjoint gap. "
                    "The fixed flat RI owner candidate has unit static elliptic principal coefficient, so Z_RI,min=1 inside the selected private normalization; the curved Ricci-corrected branch keeps Box as the principal symbol and treats Ricci as a lower-order correction. "
                    "The explicit minimal RI owner block has no independent positive mass/Hessian floor, so M_RI,min^2=0 and the mass-only Neumann route is unavailable unless a new parent-derived mass term is added. "
                    "The best symbolic positive-gap route is therefore lambda_RI,lower=pi^2/ell_RI^2-Eta_RI,total on an anchored residual domain, with Eta_RI,total=Eta_Ric+Eta_comm+Eta_EM+B_RI,neg. "
                    "Current claims remain false because parent boundary anchoring, ell_RI/geometry, and Eta component bounds are not source-backed."
                ),
                "4349 source register, principal rows, mass rows, domain spectrum rows, Eta decomposition rows, lambda candidate rows, runner, firewall, decision, status, next-target and validation CSV.",
                "private_ZRI_principal_sign_minimal_MRI_zero_lambda_symbolic_nonclaim",
                "Prove parent anchored residual domain and Eta_RI,total < pi^2/ell_RI^2, or source absolute bounds and run owner-tail finite-bound row.",
                "Promoting Z_RI=1 to public parent fact; using Neumann no-flux as a positive gap; setting Eta_RI=0 by wish; cancelling Eta components.",
            ]
        )


def validation_rows(paths: Dict[str, Path], tables: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []

    def add(check_id: str, description: str, passed: bool, evidence: str) -> None:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "branch": BRANCH,
                "generated_utc": GENERATED_UTC,
                "decision": DECISION,
                "claim_allowed": "False",
                "valid_for_claim": "False",
                "check_id": check_id,
                "description": description,
                "passed": str(bool(passed)),
                "evidence": evidence,
            }
        )

    add("VAL4349_sources_exist", "all source paths exist", all(row["path_exists"] == "True" for row in tables["sources"]), "source_register")
    add("VAL4349_needles_found", "all source anchors found", all(row["needle_found"] == "True" for row in tables["sources"]), "source_register")
    add("VAL4349_ZRI_candidate", "Z_RI candidate value is filled as 1", any(row["quantity"] == "Z_RI,min" and row["derived_value"] == "1" for row in tables["principal"]), "principal")
    add("VAL4349_MRI_zero", "minimal M_RI mass row is zero", any(row["quantity"] == "M_RI,min^2" and row["derived_value"] == "0" for row in tables["mass"]), "mass")
    add("VAL4349_domain_dirichlet", "Dirichlet symbolic spectrum row exists", any("pi^2/ell_RI^2" in row["symbolic_value"] for row in tables["domain"]), "domain")
    add("VAL4349_eta_total", "Eta total absolute decomposition exists", any(row["bound_symbol"] == "Eta_RI,total" for row in tables["eta"]), "eta")
    add("VAL4349_minimal_neumann_rejected", "minimal Neumann constant-mode route is rejected", any(row["lambda_id"] == "LAM4349_2_neumann_minimal_failure" for row in tables["lambda"]), "lambda")
    add("VAL4349_no_claim_flags", "all valid_for_claim flags remain false", all(row.get("valid_for_claim", "False") == "False" for table in tables.values() for row in table if "valid_for_claim" in row), "all_tables")
    add("VAL4349_next_target", "next target attacks boundary anchor and Eta bound", any(NEXT_TARGET in row["next_target"] for row in tables["next"]), "next")
    add("VAL4349_docs_exist", "formal and checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "docs")
    add("VAL4349_formal_marker", "formal marker exists", MARKER in read_text(FORMAL_PATH), "formal")
    add("VAL4349_post_marker", "post marker exists", MARKER in read_text(DOC_PATH), "post")
    add("VAL4349_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims")
    add("VAL4349_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "spine")
    add("VAL4349_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "packet")

    for key, path in paths.items():
        if key == "validation":
            continue
        try:
            with path.open(newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
            parsed = True
        except Exception:
            parsed = False
        add(f"VAL4349_csv_parse_{key}", f"{key} CSV parses", parsed, str(path))

    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4349_SOURCE_REGISTER.csv",
        "principal": SOURCE_DIR / "P8_Y5_R2FR_4349_ZRI_PRINCIPAL_ROWS.csv",
        "mass": SOURCE_DIR / "P8_Y5_R2FR_4349_MRI_MASS_ROWS.csv",
        "domain": SOURCE_DIR / "P8_Y5_R2FR_4349_DOMAIN_SPECTRUM_ROWS.csv",
        "eta": SOURCE_DIR / "P8_Y5_R2FR_4349_ETARI_DECOMPOSITION_ROWS.csv",
        "lambda": SOURCE_DIR / "P8_Y5_R2FR_4349_LAMBDA_CANDIDATE_ROWS.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4349_RUNNER.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4349_CLAIM_FIREWALL.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4349_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4349_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4349_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = build_tables()
    for key, table_rows in tables.items():
        write_csv(paths[key], table_rows)
    write_docs(tables)
    append_claim_once()
    append_once(
        FORMAL / "07-unification-spine.md",
        MARKER,
        f"""
## PPC4161 4349 RI principal sign and minimal mass row

Marker: `{MARKER}`

4349 fills the first symbolic component rows for the owner-tail `lambda_RI` gate:

```text
Z_RI,min = 1
M_RI,min^2 = 0
lambda_RI,lower = pi^2/ell_RI^2 - Eta_RI,total
Eta_RI,total = Eta_Ric + Eta_comm + Eta_EM + B_RI,neg.
```

This narrows the live branch: the minimal RI owner route needs an anchored residual domain and `Eta_RI,total < pi^2/ell_RI^2`. Neumann/no-flux alone fails in the minimal branch because the constant zero mode survives without a mass gap or projector.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4349 packet RI principal sign and minimal mass row

Marker: `{PACKET_MARKER}`

Packet update: the owner-tail gap no longer lacks every component. The private RI candidate supplies a unit principal sign and a minimal zero mass floor. The remaining local-GR pressure is now boundary/domain ownership plus the absolute correction ceiling `Eta_RI,total`.
""",
    )
    validation = validation_rows(paths, tables)
    write_csv(paths["validation"], validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(tables)} csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(validation)} failed={len(failed)}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['description']} :: {row['evidence']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
