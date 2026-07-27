from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4347"
CLAIM_ID = "L-188"
BRANCH = "MTS_R2FR_Y5_OWNER_TAIL_ZERO_SIGNATURE_OR_REAL_LAMBDA_BOUND_RUNNER_4347"
DECISION = "OWNER_TAIL_ZERO_THEOREM_DERIVED_SIGNATURE_GAP_OPEN_REAL_BOUND_RUNNER_READY_NONCLAIM"
MARKER = "PPC4161_OWNER_TAIL_ZERO_SIGNATURE_OR_REAL_LAMBDA_BOUND_RUNNER_4347"
PACKET_MARKER = "PPC4161_PACKET_OWNER_TAIL_ZERO_SIGNATURE_OR_REAL_LAMBDA_BOUND_RUNNER_4347"
NEXT_TARGET = "4348-Y5-R2FR-lambda-RI-positive-domain-or-bound-input-pack.md"

FORMAL_PATH = FORMAL / "363-PPC4161-owner-tail-zero-signature-or-real-lambda-bound-runner.md"
DOC_PATH = POST / "4347-Y5-R2FR-owner-tail-zero-signature-or-real-lambda-bound-runner.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4347_VALIDATION.csv"
GENERATED_UTC = datetime.now(timezone.utc).isoformat(timespec="seconds")

ARENA_GATES = [
    ("delta_phi_fraction", "1.0e-5", "dimensionless", "59-local-ppn-branch-framework.md:112"),
    ("delta_gamma", "1.0e-5", "dimensionless", "59-local-ppn-branch-framework.md:113"),
    ("delta_beta", "1.0e-4", "dimensionless", "59-local-ppn-branch-framework.md:114"),
    ("alpha1", "1.0e-4", "dimensionless", "59-local-ppn-branch-framework.md:115"),
    ("alpha2", "1.0e-5", "dimensionless", "59-local-ppn-branch-framework.md:116"),
    ("eta_AB", "1.0e-13", "dimensionless", "59-local-ppn-branch-framework.md:117"),
    ("Gdot_over_G", "4.0e-14", "per_year", "59-local-ppn-branch-framework.md:118"),
    ("chi_local_leak_fraction", "1.0e-5", "dimensionless", "59-local-ppn-branch-framework.md:119"),
    ("clock_delta_z", "1.0e-16", "dimensionless", "59-local-ppn-branch-framework.md:120"),
]

SOURCES = [
    (
        "SRC4347_00_4346_next",
        FORMAL / "362-PPC4161-fill-real-owner-tail-Kperp-values-or-adopt-clean-sector.md",
        "4347-Y5-R2FR-owner-tail-zero-signature-or-real-lambda-bound-runner.md",
        "4346 handoff selecting owner-tail zero or real bound.",
    ),
    (
        "SRC4347_01_4343_action",
        FORMAL / "359-PPC4161-parent-action-owner-for-KGamma-or-Kperp-sector-bound-runner.md",
        "S_RI = int_U sqrt(-g) Lambda_nu",
        "Concrete multiplier owner action candidate.",
    ),
    (
        "SRC4347_02_4343_euler",
        FORMAL / "359-PPC4161-parent-action-owner-for-KGamma-or-Kperp-sector-bound-runner.md",
        "constraint = 0,",
        "Owner stress vanishes if constraint, Lambda and boundary vanish.",
    ),
    (
        "SRC4347_03_4344_adjoint",
        FORMAL / "360-PPC4161-adjoint-zero-and-boundary-kernel-proof-or-first-Kperp-score-row.md",
        "L_RI^dagger = -D_i(Z_RI D^i) + M_RI^2 + V_Ric - E_RI.",
        "Static adjoint collar operator.",
    ),
    (
        "SRC4347_04_4344_lambda",
        FORMAL / "360-PPC4161-adjoint-zero-and-boundary-kernel-proof-or-first-Kperp-score-row.md",
        "lambda_RI := Z_RI,min lambda_1(D_RI) + M_RI,min^2 - Eta_RI > 0,",
        "lambda_RI positivity condition.",
    ),
    (
        "SRC4347_05_4344_tail",
        FORMAL / "360-PPC4161-adjoint-zero-and-boundary-kernel-proof-or-first-Kperp-score-row.md",
        "Y_owner_a <= Pi_a^RI C_Lambda R_Lambda/lambda_RI",
        "Finite owner-tail score formula.",
    ),
    (
        "SRC4347_06_4344_boundary",
        FORMAL / "360-PPC4161-adjoint-zero-and-boundary-kernel-proof-or-first-Kperp-score-row.md",
        "B_Lambda=0 and B_RI=0 for the owner block",
        "Boundary-zero route.",
    ),
    (
        "SRC4347_07_216_hyperbolic_guard",
        FORMAL / "216-PPC4161-Kperp-boundary-zero-or-demotion.md",
        "elliptic/static proof != hyperbolic incoming-mode proof.",
        "Incoming-mode firewall.",
    ),
    (
        "SRC4347_08_138_hidden_stress",
        FORMAL / "138-metric-null-action-block-contract.md",
        "sqrt(-g),",
        "Covariance hidden-stress warning.",
    ),
    (
        "SRC4347_09_250_kperp_clean",
        FORMAL / "250-PPC4161-Kperp-EH-coframe-identity-proof-or-independent-tensor-source-row.md",
        "R_i^K = |W_i^K| N_T/D_T = 0",
        "Kperp is already privately routed out before owner-tail scoring.",
    ),
    (
        "SRC4347_10_327_gap",
        FORMAL / "327-PPC4161-lambda-floor-source-row-or-collar-residual-first-bound.md",
        "Poincare/Dirichlet collar gap",
        "Prior collar positivity precedent.",
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


def zero_signature_rows() -> List[Dict[str, str]]:
    return [
        {
            "clause_id": "OZ4347_0_parent_block",
            "clause": "S_RI is adopted as an auxiliary owner block in the selected local parent packet",
            "mathematical_role": "puts the KGamma right-inverse equation inside the variational system before scoring",
            "current_status": "CANDIDATE_DERIVED_PRIVATE_ADOPTION_UNSIGNED_PUBLIC",
            "zero_consequence": "constraint leg can vanish on shell",
            "if_unsigned": "owner route remains closure/candidate, not derivation",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "OZ4347_1_constraint",
            "clause": "C_RI^nu := L_RI A_Gamma^nu + nabla^nu Gamma_eff = 0",
            "mathematical_role": "delta Lambda equation of the multiplier owner block",
            "current_status": "EULER_EQUATION_DERIVED_IF_BLOCK_ADOPTED",
            "zero_consequence": "constraint-proportional metric stress is zero",
            "if_unsigned": "R_Lambda finite residual branch opens",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "OZ4347_2_adjoint_gap",
            "clause": "L_RI^dagger Lambda=0 has no admissible homogeneous mode",
            "mathematical_role": "coercive static collar energy identity",
            "current_status": "THEOREM_SHAPE_DERIVED_PHYSICAL_GAP_UNSIGNED",
            "zero_consequence": "Lambda=0",
            "if_unsigned": "C_Lambda R_Lambda/lambda_RI finite branch opens",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "OZ4347_3_boundary",
            "clause": "B_Lambda=0 and B_RI=0 by fixed Dirichlet/decay data or Hamiltonian/radiative routing",
            "mathematical_role": "prevents integration-by-parts boundary/corner stress from entering local metric response",
            "current_status": "CONDITIONAL_ROUTE_DERIVED_CERTIFICATE_UNSIGNED",
            "zero_consequence": "boundary owner-tail leg vanishes",
            "if_unsigned": "Pi_a^BRI B_RI row opens",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "OZ4347_4_no_incoming",
            "clause": "I_RI=0 for the stationary compact local branch",
            "mathematical_role": "separates static elliptic no-kernel proof from hyperbolic incoming memory",
            "current_status": "REQUIRED_SELECTOR_CLAUSE_UNSIGNED",
            "zero_consequence": "incoming homogeneous adjoint leg vanishes",
            "if_unsigned": "Pi_a^I I_RI row opens",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "OZ4347_5_Kperp_removed",
            "clause": "Kperp private clean sector from 4346 is active",
            "mathematical_role": "ensures owner-tail is scored alone, with no hidden Kperp cancellation",
            "current_status": "PRIVATE_SELECTOR_TRUE_PUBLIC_FALLBACK_RETAINED",
            "zero_consequence": "Y_a=Y_owner_a in the private selector",
            "if_unsigned": "public Kperp finite score row reopens",
            "valid_for_claim": "False",
        },
    ]


def derivation_rows() -> List[Dict[str, str]]:
    return [
        {
            "derivation_id": "DER4347_0_variation",
            "statement": "For S_RI=int sqrt(-g) Lambda_nu C_RI^nu, metric variation has constraint, multiplier-adjoint and boundary pieces.",
            "formula": "delta_g S_RI = constraint*C_g + Lambda*delta_g C_RI + B_RI",
            "result": "on C_RI=0, Lambda=0 and B_RI=0, T_RI^{mu nu}=0",
            "status": "DERIVED_CONDITIONAL",
            "valid_for_claim": "False",
        },
        {
            "derivation_id": "DER4347_1_adjoint_energy",
            "statement": "For the fixed static collar, the homogeneous adjoint equation is killed by a positive gap.",
            "formula": "0=<Lambda,L_RI^dagger Lambda> >= lambda_RI ||Lambda||^2",
            "result": "lambda_RI>0 implies Lambda=0",
            "status": "DERIVED_CONDITIONAL",
            "valid_for_claim": "False",
        },
        {
            "derivation_id": "DER4347_2_exact_zero",
            "statement": "The owner-tail score is exactly zero only if every leg of the owner-tail decomposition is zero.",
            "formula": "C_RI=0, Lambda=0, B_RI=0, I_RI=0 => Y_owner_a=0",
            "result": "local owner block is metric-null in the selected private branch",
            "status": "ZERO_THEOREM_DERIVED_SIGNATURE_UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "derivation_id": "DER4347_3_fallback_bound",
            "statement": "If the zero signature is not signed, the residual is a componentwise absolute bound, not a cancellation.",
            "formula": "|Y_a| <= |Pi_a^RI| C_Lambda |R_Lambda|/lambda_RI + |Pi_a^BRI||B_RI| + |Pi_a^I||I_RI|",
            "result": "reduced real-bound runner is now explicit",
            "status": "BOUND_RUNNER_READY_VALUES_MISSING",
            "valid_for_claim": "False",
        },
    ]


def fallback_input_rows() -> List[Dict[str, str]]:
    return [
        {
            "input_id": "FB4347_0_lambda_RI",
            "symbol": "lambda_RI",
            "bound_role": "positive denominator",
            "required_real_row": "Z_RI,min, lambda_1(D_RI), M_RI,min^2 and Eta_RI in the same static collar/domain",
            "current_status": "FORMULA_DERIVED_VALUE_UNSIGNED",
            "claim_blocker": "MISSING_PHYSICAL_GAP_ROW",
            "valid_for_claim": "False",
        },
        {
            "input_id": "FB4347_1_R_Lambda",
            "symbol": "R_Lambda",
            "bound_role": "adjoint residual forcing",
            "required_real_row": "zero theorem or sourced residual norm in same units as L_RI^dagger Lambda",
            "current_status": "ZERO_PREFERRED_VALUE_UNSIGNED",
            "claim_blocker": "MISSING_RESIDUAL_NORM",
            "valid_for_claim": "False",
        },
        {
            "input_id": "FB4347_2_B_RI",
            "symbol": "B_RI",
            "bound_role": "boundary/corner owner stress",
            "required_real_row": "fixed/routed boundary certificate or finite boundary norm",
            "current_status": "CONDITIONAL_ZERO_ROUTE_UNSIGNED",
            "claim_blocker": "MISSING_BOUNDARY_CERTIFICATE",
            "valid_for_claim": "False",
        },
        {
            "input_id": "FB4347_3_I_RI",
            "symbol": "I_RI",
            "bound_role": "incoming/hyperbolic homogeneous adjoint mode",
            "required_real_row": "stationary local selector/no-incoming certificate or finite incoming-mode norm",
            "current_status": "REQUIRED_SELECTOR_CLAUSE_UNSIGNED",
            "claim_blocker": "MISSING_NO_INCOMING_CERTIFICATE",
            "valid_for_claim": "False",
        },
        {
            "input_id": "FB4347_4_C_Lambda",
            "symbol": "C_Lambda",
            "bound_role": "adjoint inverse/constant in chosen norm",
            "required_real_row": "norm convention and inverse estimate, usually C_Lambda <= C_domain/lambda_RI",
            "current_status": "FORMULA_SHAPE_ONLY",
            "claim_blocker": "MISSING_NORM_CONSTANT",
            "valid_for_claim": "False",
        },
        {
            "input_id": "FB4347_5_projections",
            "symbol": "Pi_a^RI, Pi_a^BRI, Pi_a^I",
            "bound_role": "transfer to PPN/R10/clock/orbital/WEP arenas",
            "required_real_row": "arena-specific projection constants with units and source paths",
            "current_status": "MISSING_ARENA_PROJECTION_CONSTANTS",
            "claim_blocker": "MISSING_PROJECTIONS",
            "valid_for_claim": "False",
        },
    ]


def reduced_bound_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for observable, bound, units, source in ARENA_GATES:
        rows.append(
            {
                "score_id": f"OB4347_{observable}",
                "arena": observable,
                "arena_bound": bound,
                "units": units,
                "source": source,
                "Kperp_private": "0",
                "zero_branch": "Y_owner_a=0 if all OZ4347 clauses are signed",
                "fallback_bound": "|Pi_RI| C_Lambda |R_Lambda|/lambda_RI + |Pi_BRI||B_RI| + |Pi_I||I_RI| <= arena_bound",
                "status": "REAL_VALUES_MISSING_NONCLAIM",
                "claim_valid": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def runner_rows() -> List[Dict[str, str]]:
    return [
        {
            "runner_id": "RUN4347_0_zero_signature",
            "branch_input": "all OZ4347 clauses signed",
            "action": "DECLARE_OWNER_TAIL_ZERO_INSIDE_PRIVATE_SELECTOR",
            "output": "Y_owner_a=0 and private Kperp=0 for this channel",
            "claim_policy": "still no public local-GR claim until remaining source/readout gates close",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4347_1_bound_fallback",
            "branch_input": "one or more OZ4347 clauses unsigned",
            "action": "RUN_REDUCED_ABSOLUTE_OWNER_TAIL_BOUND_AFTER_REAL_ROWS",
            "output": "|Y_a| absolute-summed against arena gates with no Kperp cancellation",
            "claim_policy": "claim only after real numeric/source rows exist and pass",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4347_2_next_gap",
            "branch_input": "current corpus",
            "action": "ATTACK_LAMBDA_RI_POSITIVE_DOMAIN_FIRST",
            "output": NEXT_TARGET,
            "claim_policy": "positive gap is the highest leverage clause because it kills Lambda",
            "valid_for_claim": "False",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    return [
        {
            "firewall_id": "FW4347_0",
            "forbidden_shortcut": "Calling the owner block metric-null because the constraint is imposed",
            "reason": "delta_g S_RI also has Lambda and boundary/corner pieces; both must vanish.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4347_1",
            "forbidden_shortcut": "Using static elliptic adjoint zero to erase incoming modes",
            "reason": "I_RI is separate unless the local branch is parent-signed stationary/no-incoming.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4347_2",
            "forbidden_shortcut": "Letting owner-tail pieces cancel numerically",
            "reason": "fallback runner is componentwise absolute-summed.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4347_3",
            "forbidden_shortcut": "Treating private Kperp zero as public/global no-extra-TT-source",
            "reason": "4346 retained the public Kperp fallback.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4347_0",
            "decision": DECISION,
            "reason": "the exact owner-tail zero theorem is now written as a six-clause signature; current corpus does not yet sign the physical lambda/domain, boundary and no-incoming clauses",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4347_0",
            "item": "owner-tail theorem",
            "status": "EXACT_ZERO_SIGNATURE_DERIVED",
            "notes": "constraint=0, Lambda=0, B_RI=0 and I_RI=0 imply Y_owner=0.",
        },
        {
            "status_id": "STAT4347_1",
            "item": "real rows",
            "status": "PHYSICAL_VALUES_NOT_FILLED",
            "notes": "lambda_RI, R_Lambda, B_RI, I_RI, C_Lambda and projections remain nonnumeric.",
        },
        {
            "status_id": "STAT4347_2",
            "item": "bound runner",
            "status": "REDUCED_OWNER_TAIL_RUNNER_READY",
            "notes": "fallback uses absolute componentwise owner-tail score without Kperp cancellation.",
        },
        {
            "status_id": "STAT4347_3",
            "item": "next target",
            "status": "LAMBDA_RI_POSITIVE_DOMAIN_FIRST",
            "notes": NEXT_TARGET,
        },
    ]


def next_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_target_id": "NT4347_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can the physical static collar/domain sign lambda_RI>0, or must the owner-tail branch use a finite real denominator row?",
            "preferred_route": "derive Z_RI,min>0, lambda_1(D_RI)>0, M_RI,min^2-Eta_RI not too negative, fixed self-adjoint domain and no zero mode",
            "fallback_route": "source numeric/symbolic lower-bound rows for lambda_RI plus R_Lambda/B_RI/I_RI/projection rows and run the reduced bound",
            "valid_for_claim": "False",
        }
    ]


def build_tables() -> Dict[str, List[Dict[str, str]]]:
    return {
        "sources": source_rows(),
        "zero": zero_signature_rows(),
        "derivation": derivation_rows(),
        "inputs": fallback_input_rows(),
        "scores": reduced_bound_rows(),
        "runner": runner_rows(),
        "firewall": firewall_rows(),
        "decision": decision_rows(),
        "status": status_rows(),
        "next": next_rows(),
    }


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    formal = f"""# 363 PPC4161 owner-tail zero signature or real lambda bound runner

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint does not prove public local GR, Newton, R10, PPN, clock safety, orbital safety, WEP safety, Maxwell closure, source coupling closure, or a fundamental prediction of `G_N`.

## Result

4347 attacks the owner-tail branch directly.

With private `Kperp=0` from 4346, the remaining local score is:

```text
Y_a = Pi_a^RI C_Lambda R_Lambda/lambda_RI + Pi_a^BRI B_RI + Pi_a^I I_RI.
```

The zero theorem is now exact:

```text
S_RI = int sqrt(-g) Lambda_nu C_RI^nu
C_RI^nu = L_RI A_Gamma^nu + nabla^nu Gamma_eff

C_RI=0,
L_RI^dagger Lambda=0 with lambda_RI>0,
B_Lambda=B_RI=0,
I_RI=0
=> Lambda=0
=> T_RI^{{mu nu}}=0
=> Y_owner_a=0.
```

The key derivation is not "the constraint is zero, therefore no stress". The hidden-stress-safe statement is:

```text
delta_g S_RI = constraint*C_g + Lambda*delta_g C_RI + B_RI.
```

Only when `constraint=0`, `Lambda=0`, and `B_RI=0` does the owner action become metric-null. If any clause fails, the fallback is no-cancellation and absolute:

```text
|Y_a| <= |Pi_a^RI| C_Lambda |R_Lambda|/lambda_RI
       + |Pi_a^BRI||B_RI|
       + |Pi_a^I||I_RI|.
```

So the next real bottleneck is not writing another score shape. It is proving or sourcing the physical positive-gap/domain row for `lambda_RI`, then boundary and incoming-mode silence.

## Source Register

{md_table(tables["sources"], ["source_id", "path", "path_exists", "needle_found", "line_number", "role", "valid_for_claim"])}

## Zero-Signature Clauses

{md_table(tables["zero"], ["clause_id", "clause", "mathematical_role", "current_status", "zero_consequence", "if_unsigned", "valid_for_claim"])}

## Derivation Rows

{md_table(tables["derivation"], ["derivation_id", "statement", "formula", "result", "status", "valid_for_claim"])}

## Fallback Input Pack

{md_table(tables["inputs"], ["input_id", "symbol", "bound_role", "required_real_row", "current_status", "claim_blocker", "valid_for_claim"])}

## Reduced Bound Rows

{md_table(tables["scores"], ["score_id", "arena", "arena_bound", "units", "Kperp_private", "zero_branch", "fallback_bound", "status", "claim_valid", "valid_for_claim"])}

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
    post = f"""# 4347 Y5-R2FR owner-tail zero signature or real lambda bound runner

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4347 derives the exact owner-tail zero signature and keeps the real-bound fallback honest.

```text
constraint=0, Lambda=0, B_RI=0, I_RI=0 => Y_owner_a=0
|Y_a| <= |Pi_RI|C_Lambda|R_Lambda|/lambda_RI + |Pi_BRI||B_RI| + |Pi_I||I_RI|
```

This is progress, but not a claim: the physical positive-gap/domain row for `lambda_RI`, the boundary certificate, the no-incoming certificate and the projection constants are still required.

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
                    "4347 derives the exact owner-tail zero signature after the private Kperp clean-sector reduction. "
                    "For S_RI=int sqrt(-g) Lambda_nu C_RI^nu, metric variation splits into constraint, Lambda-adjoint and boundary/corner pieces. "
                    "Thus C_RI=0, L_RI^dagger Lambda=0 with lambda_RI>0, B_Lambda=B_RI=0 and I_RI=0 imply Lambda=0, T_RI=0 and Y_owner_a=0. "
                    "If any clause is unsigned, the reduced fallback is the no-cancellation bound |Y_a|<=|Pi_RI| C_Lambda |R_Lambda|/lambda_RI + |Pi_BRI||B_RI| + |Pi_I||I_RI|. "
                    "Current corpus still lacks physical lambda_RI/domain, boundary, no-incoming and projection rows, so all claims remain false."
                ),
                "4347 source register, zero-signature clauses, derivation rows, fallback input pack, reduced bound rows, runner, firewall, decision, status, next-target and validation CSV.",
                "private_owner_tail_zero_signature_derived_gap_domain_rows_missing_nonclaim",
                "Derive or source the physical lambda_RI positive-domain row, then boundary/no-incoming/projection rows, or run the reduced owner-tail bound.",
                "Calling constraint imposition metric-null by itself; erasing incoming modes with a static proof; allowing owner-tail cancellations; promoting private Kperp zero globally.",
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

    add("VAL4347_sources_exist", "all source paths exist", all(row["path_exists"] == "True" for row in tables["sources"]), "source_register")
    add("VAL4347_needles_found", "all source anchors found", all(row["needle_found"] == "True" for row in tables["sources"]), "source_register")
    add("VAL4347_zero_clauses", "six zero-signature clauses are present", len(tables["zero"]) == 6, "zero")
    add("VAL4347_derivation_count", "four derivation rows are present", len(tables["derivation"]) == 4, "derivation")
    add("VAL4347_exact_zero_formula", "exact zero theorem row exists", any(row["derivation_id"] == "DER4347_2_exact_zero" for row in tables["derivation"]), "derivation")
    add("VAL4347_fallback_absolute", "fallback bound is absolute/no-cancellation", any("abs" in row["action"].lower() or "ABSOLUTE" in row["action"] for row in tables["runner"]), "runner")
    add("VAL4347_inputs_open", "fallback input rows remain nonclaim", all(row["valid_for_claim"] == "False" for row in tables["inputs"]), "inputs")
    add("VAL4347_score_rows", "reduced score rows cover arenas", len(tables["scores"]) == len(ARENA_GATES), "scores")
    add("VAL4347_kperp_zero_in_scores", "all reduced rows carry private Kperp zero", all(row["Kperp_private"] == "0" for row in tables["scores"]), "scores")
    add("VAL4347_no_claim_flags", "all generated valid_for_claim flags are false", all(row.get("valid_for_claim", "False") == "False" for table in tables.values() for row in table if "valid_for_claim" in row), "all_tables")
    add("VAL4347_next_target", "next target attacks lambda_RI positive domain", any(NEXT_TARGET in row["next_target"] for row in tables["next"]), "next")
    add("VAL4347_docs_exist", "formal and checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "docs")
    add("VAL4347_formal_marker", "formal marker exists", MARKER in read_text(FORMAL_PATH), "formal")
    add("VAL4347_post_marker", "post marker exists", MARKER in read_text(DOC_PATH), "post")
    add("VAL4347_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims")
    add("VAL4347_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "spine")
    add("VAL4347_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "packet")

    for key, path in paths.items():
        if key == "validation":
            continue
        try:
            with path.open(newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
            parsed = True
        except Exception:
            parsed = False
        add(f"VAL4347_csv_parse_{key}", f"{key} CSV parses", parsed, str(path))

    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4347_SOURCE_REGISTER.csv",
        "zero": SOURCE_DIR / "P8_Y5_R2FR_4347_ZERO_SIGNATURE_CLAUSES.csv",
        "derivation": SOURCE_DIR / "P8_Y5_R2FR_4347_DERIVATION_ROWS.csv",
        "inputs": SOURCE_DIR / "P8_Y5_R2FR_4347_FALLBACK_INPUT_PACK.csv",
        "scores": SOURCE_DIR / "P8_Y5_R2FR_4347_REDUCED_BOUND_ROWS.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4347_RUNNER.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4347_CLAIM_FIREWALL.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4347_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4347_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4347_NEXT_TARGET.csv",
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
## PPC4161 4347 owner-tail zero signature

Marker: `{MARKER}`

4347 derives the exact owner-tail zero theorem after private `Kperp=0`:

```text
C_RI=0,
L_RI^dagger Lambda=0 with lambda_RI>0,
B_Lambda=B_RI=0,
I_RI=0
=> Lambda=0
=> T_RI=0
=> Y_owner_a=0.
```

If any clause remains unsigned, the branch uses the reduced absolute bound:

```text
|Y_a| <= |Pi_a^RI| C_Lambda |R_Lambda|/lambda_RI
       + |Pi_a^BRI||B_RI|
       + |Pi_a^I||I_RI|.
```

The next target is `{NEXT_TARGET}`: derive/source the physical positive-domain row for `lambda_RI` before trying to score local tests.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4347 packet owner-tail zero signature

Marker: `{PACKET_MARKER}`

Packet update: after the private Kperp clean-sector adoption, the owner-tail has an exact zero signature. The packet must now prove or source `lambda_RI>0`, `B_RI=0`, `I_RI=0`, and projection constants. Until then, the fallback is an absolute reduced owner-tail bound, not a local-GR claim.
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
