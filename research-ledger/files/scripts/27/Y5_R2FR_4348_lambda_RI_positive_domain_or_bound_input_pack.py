from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4348"
CLAIM_ID = "L-189"
BRANCH = "MTS_R2FR_Y5_LAMBDA_RI_POSITIVE_DOMAIN_OR_BOUND_INPUT_PACK_4348"
DECISION = "LAMBDA_RI_POSITIVE_DOMAIN_LAW_DERIVED_COMPONENT_INPUT_PACK_READY_NONCLAIM"
MARKER = "PPC4161_LAMBDA_RI_POSITIVE_DOMAIN_OR_BOUND_INPUT_PACK_4348"
PACKET_MARKER = "PPC4161_PACKET_LAMBDA_RI_POSITIVE_DOMAIN_OR_BOUND_INPUT_PACK_4348"
NEXT_TARGET = "4349-Y5-R2FR-ZRI-MRI-EtaRI-source-or-domain-spectrum-row.md"

FORMAL_PATH = FORMAL / "364-PPC4161-lambda-RI-positive-domain-or-bound-input-pack.md"
DOC_PATH = POST / "4348-Y5-R2FR-lambda-RI-positive-domain-or-bound-input-pack.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4348_VALIDATION.csv"
GENERATED_UTC = datetime.now(timezone.utc).isoformat(timespec="seconds")

SOURCES = [
    (
        "SRC4348_00_4347_next",
        FORMAL / "363-PPC4161-owner-tail-zero-signature-or-real-lambda-bound-runner.md",
        "4348-Y5-R2FR-lambda-RI-positive-domain-or-bound-input-pack.md",
        "4347 handoff selecting lambda_RI positive-domain row.",
    ),
    (
        "SRC4348_01_4344_operator",
        FORMAL / "360-PPC4161-adjoint-zero-and-boundary-kernel-proof-or-first-Kperp-score-row.md",
        "L_RI^dagger = -D_i(Z_RI D^i) + M_RI^2 + V_Ric - E_RI.",
        "RI adjoint operator form.",
    ),
    (
        "SRC4348_02_4344_lambda",
        FORMAL / "360-PPC4161-adjoint-zero-and-boundary-kernel-proof-or-first-Kperp-score-row.md",
        "lambda_RI := Z_RI,min lambda_1(D_RI) + M_RI,min^2 - Eta_RI > 0,",
        "4344 lambda_RI positivity formula.",
    ),
    (
        "SRC4348_03_4311_law",
        FORMAL / "327-PPC4161-lambda-floor-source-row-or-collar-residual-first-bound.md",
        "lambda_* := Z_min lambda_1(D_loc) + M2_min - Eta_H.",
        "General collar positivity law.",
    ),
    (
        "SRC4348_04_4311_routes",
        FORMAL / "327-PPC4161-lambda-floor-source-row-or-collar-residual-first-bound.md",
        "This gives three honest branches: a Poincare/Dirichlet gap, a mass-only zero-mode gap, or a mixed positive margin.",
        "Three positivity branches.",
    ),
    (
        "SRC4348_05_4302_gap",
        FORMAL / "318-PPC4161-m-lock-coercivity-gap-and-DvGamma-quadratic-input-pack.md",
        "lambda_m = Z_min lambda_1(D_loc) + M2_min - Eta_H.",
        "Analogous coercive gap precedent.",
    ),
    (
        "SRC4348_06_4310_no_concentration",
        FORMAL / "326-PPC4161-collar-no-concentration-signature-or-trace-bound-inputs.md",
        "lambda_* > 0,",
        "Positive gap controls collar amplitude.",
    ),
    (
        "SRC4348_07_4343_LRI",
        FORMAL / "359-PPC4161-parent-action-owner-for-KGamma-or-Kperp-sector-bound-runner.md",
        "L_RI A^nu=(Box delta^nu_sigma+Ric^nu_sigma)A^sigma",
        "RI covariant operator candidate.",
    ),
    (
        "SRC4348_08_208_domain",
        FORMAL / "208-PPC4161-parent-Xi-Hessian-signs-and-boundary-domain.md",
        "with `D_Xi>0` and `mu_Xi>0`, the scalar operator is positive on standard self-adjoint domains:",
        "Self-adjoint positive-domain precedent.",
    ),
    (
        "SRC4348_09_216_guard",
        FORMAL / "216-PPC4161-Kperp-boundary-zero-or-demotion.md",
        "elliptic/static proof != hyperbolic incoming-mode proof.",
        "Static-domain firewall.",
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


def theorem_rows() -> List[Dict[str, str]]:
    return [
        {
            "theorem_id": "LAM4348_THM_0_quadratic_form",
            "statement": "On a fixed static RI collar, the adjoint quadratic form has a lower bound by kinetic, mass and negative-correction pieces.",
            "formula": "a_RI[Lambda,Lambda] >= Z_RI,min ||D Lambda||^2 + (M_RI,min^2 - Eta_RI - B_RI,neg)||Lambda||^2",
            "result": "reduces adjoint no-kernel to a positive lower-bound problem",
            "status": "DERIVED_CONDITIONAL",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "LAM4348_THM_1_domain_gap",
            "statement": "If the domain removes the constant/gauge zero mode, a Poincare or spectral gap controls ||D Lambda|| by ||Lambda||.",
            "formula": "||D Lambda||^2 >= lambda_dom(D_RI)||Lambda||^2",
            "result": "lambda_RI,lower = Z_RI,min lambda_dom + M_RI,min^2 - Eta_RI - B_RI,neg",
            "status": "DERIVED_CONDITIONAL",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "LAM4348_THM_2_positive_gap",
            "statement": "A positive lower bound kills the homogeneous adjoint multiplier.",
            "formula": "lambda_RI,lower > 0 and L_RI^dagger Lambda=0 => Lambda=0",
            "result": "owner-tail Lambda leg vanishes",
            "status": "EXACT_IF_INPUTS_SIGNED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "LAM4348_THM_3_finite_inverse",
            "statement": "If the owner block is not exact-zero but lambda_RI,lower is positive, the finite inverse row is controlled.",
            "formula": "||Lambda|| <= ||R_Lambda||/lambda_RI,lower",
            "result": "feeds 4347 reduced absolute owner-tail bound",
            "status": "BOUND_FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": "False",
        },
    ]


def domain_branch_rows() -> List[Dict[str, str]]:
    return [
        {
            "branch_id": "DOM4348_0_dirichlet_anchored",
            "domain_branch": "Dirichlet/anchored residual collar",
            "domain_condition": "Lambda|partialD_RI=0 or residual representative anchored on the collar boundary",
            "lambda_dom_rule": "lambda_dom >= lambda_1^D(D_RI); for a unit interval/collar smoke lambda_1^D=pi^2/ell_RI^2",
            "positive_gap_condition": "Z_RI,min lambda_1^D + M_RI,min^2 > Eta_RI + B_RI,neg",
            "status": "BEST_THEOREM_ROUTE_IF_PARENT_BOUNDARY_SIGNED",
            "valid_for_claim": "False",
        },
        {
            "branch_id": "DOM4348_1_neumann_mass_gap",
            "domain_branch": "Neumann/no-flux with constant mode retained",
            "domain_condition": "normal flux is zero but the constant mode remains admissible",
            "lambda_dom_rule": "lambda_dom=0",
            "positive_gap_condition": "M_RI,min^2 > Eta_RI + B_RI,neg",
            "status": "VALID_ONLY_IF_MASS_GAP_SIGNED",
            "valid_for_claim": "False",
        },
        {
            "branch_id": "DOM4348_2_neumann_orthogonal",
            "domain_branch": "Neumann/no-flux with zero mode projected out",
            "domain_condition": "Lambda is orthogonal to kernel/constant/gauge modes by quotient or source constraint",
            "lambda_dom_rule": "lambda_dom=lambda_1^+(D_RI)>0",
            "positive_gap_condition": "Z_RI,min lambda_1^+ + M_RI,min^2 > Eta_RI + B_RI,neg",
            "status": "VALID_IF_ZERO_MODE_SELECTOR_SIGNED",
            "valid_for_claim": "False",
        },
        {
            "branch_id": "DOM4348_3_robin_routed",
            "domain_branch": "Robin/routed boundary",
            "domain_condition": "boundary form is self-adjoint and has lower bound B_Lambda >= -B_RI,neg ||Lambda||^2",
            "lambda_dom_rule": "lambda_dom=lambda_1^Robin(D_RI,beta) after boundary lower-bound accounting",
            "positive_gap_condition": "Z_RI,min lambda_1^Robin + M_RI,min^2 > Eta_RI + B_RI,neg",
            "status": "BOUND_ROUTE_IF_BOUNDARY_FORM_SOURCED",
            "valid_for_claim": "False",
        },
        {
            "branch_id": "DOM4348_4_exterior_weighted",
            "domain_branch": "exterior decay/weighted finite-energy branch",
            "domain_condition": "fixed exterior end with decay or weighted Hardy/Poincare inequality",
            "lambda_dom_rule": "lambda_dom=lambda_weighted>0 if a weighted inequality is parent-signed",
            "positive_gap_condition": "Z_RI,min lambda_weighted + M_RI,min^2 > Eta_RI + B_RI,neg",
            "status": "OPEN_WEIGHTED_GAP_ROUTE",
            "valid_for_claim": "False",
        },
        {
            "branch_id": "DOM4348_5_failure",
            "domain_branch": "unanchored zero-mode or negative correction dominance",
            "domain_condition": "zero mode remains and M_RI,min^2 <= Eta_RI+B_RI,neg, or component rows are placeholders",
            "lambda_dom_rule": "no positive lower bound",
            "positive_gap_condition": "fails",
            "status": "CLAIM_BLOCKED_USE_UNSCORED_LEDGER",
            "valid_for_claim": "False",
        },
    ]


def component_rows() -> List[Dict[str, str]]:
    return [
        {
            "component_id": "COMP4348_0_ZRI_min",
            "symbol": "Z_RI,min",
            "definition": "elliptic principal-symbol lower bound of L_RI^dagger on the static collar",
            "candidate_from_current_sources": "unit principal coefficient in the fixed weak-field Box/Ricci owner candidate",
            "required_for_claim": "parent adoption plus normalization/units proving Z_RI,min>0",
            "current_status": "CANDIDATE_SIGN_POSITIVE_PUBLIC_UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "component_id": "COMP4348_1_lambda_dom",
            "symbol": "lambda_dom(D_RI)",
            "definition": "first admissible domain eigenvalue after boundary/gauge/zero-mode choice",
            "candidate_from_current_sources": "Dirichlet smoke gives pi^2/ell_RI^2; physical ell_RI/domain not sourced",
            "required_for_claim": "fixed self-adjoint domain and collar geometry or theorem-level zero-mode selector",
            "current_status": "FORMULA_READY_PHYSICAL_DOMAIN_UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "component_id": "COMP4348_2_MRI_min2",
            "symbol": "M_RI,min^2",
            "definition": "nonnegative mass/Hessian floor in the adjoint owner operator",
            "candidate_from_current_sources": "flat KGamma owner candidate can use M_RI,min^2=0; mass-only route would need M_RI,min^2>0",
            "required_for_claim": "parent Hessian or operator lower-bound row in same normalization",
            "current_status": "ZERO_CANDIDATE_OR_MASS_GAP_UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "component_id": "COMP4348_3_EtaRI",
            "symbol": "Eta_RI",
            "definition": "upper bound on negative Ricci/correction/operator-drift terms",
            "candidate_from_current_sources": "flat/local smoke sets Eta_RI=0; curved physical bound missing",
            "required_for_claim": "absolute correction bound in the same collar norm",
            "current_status": "MISSING_CORRECTION_BOUND",
            "valid_for_claim": "False",
        },
        {
            "component_id": "COMP4348_4_Bneg",
            "symbol": "B_RI,neg",
            "definition": "negative part of the adjoint boundary form after routing/fixing",
            "candidate_from_current_sources": "zero on signed Dirichlet/decay/routed branch",
            "required_for_claim": "boundary certificate or finite lower-bound row",
            "current_status": "CONDITIONAL_ZERO_UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "component_id": "COMP4348_5_lambda_lower",
            "symbol": "lambda_RI,lower",
            "definition": "claim-usable lower bound for the RI adjoint operator",
            "candidate_from_current_sources": "Z_RI,min lambda_dom + M_RI,min^2 - Eta_RI - B_RI,neg",
            "required_for_claim": "all component rows real/source-backed and lambda_RI,lower>0",
            "current_status": "FORMULA_DERIVED_VALUE_UNSOURCED",
            "valid_for_claim": "False",
        },
    ]


def candidate_rows() -> List[Dict[str, str]]:
    return [
        {
            "candidate_id": "LC4348_0_flat_dirichlet_symbolic",
            "route": "flat static owner-candidate plus Dirichlet/anchored collar",
            "lambda_lower_symbolic": "lambda_RI,lower = pi^2/ell_RI^2",
            "conditions": "Z_RI,min=1, M_RI,min^2=0, Eta_RI=0, B_RI,neg=0, ell_RI finite, Dirichlet/anchored residual domain",
            "what_is_real_now": "formula and route only",
            "promotion_blocker": "physical ell_RI, boundary anchor and parent normalization not source-backed",
            "claim_valid": "False",
            "valid_for_claim": "False",
        },
        {
            "candidate_id": "LC4348_1_curved_dirichlet_bound",
            "route": "curved static collar with anchored residual domain",
            "lambda_lower_symbolic": "lambda_RI,lower = Z_RI,min lambda_1^D(D_RI)+M_RI,min^2-Eta_RI-B_RI,neg",
            "conditions": "lambda_1^D>0 and correction margin positive",
            "what_is_real_now": "theorem formula",
            "promotion_blocker": "Z_RI,min, lambda_1^D, M_RI,min^2, Eta_RI and B_RI,neg need rows",
            "claim_valid": "False",
            "valid_for_claim": "False",
        },
        {
            "candidate_id": "LC4348_2_mass_only_zero_mode",
            "route": "Neumann/no-flux with constant mode retained",
            "lambda_lower_symbolic": "lambda_RI,lower = M_RI,min^2-Eta_RI-B_RI,neg",
            "conditions": "M_RI,min^2 larger than all negative corrections",
            "what_is_real_now": "alternate formula",
            "promotion_blocker": "positive mass/Hessian floor not sourced",
            "claim_valid": "False",
            "valid_for_claim": "False",
        },
        {
            "candidate_id": "LC4348_3_zero_mode_projected",
            "route": "Neumann/no-flux with kernel projected out",
            "lambda_lower_symbolic": "lambda_RI,lower = Z_RI,min lambda_1^+(D_RI)+M_RI,min^2-Eta_RI-B_RI,neg",
            "conditions": "quotient/gauge/source rule removes zero mode before variation",
            "what_is_real_now": "route formula",
            "promotion_blocker": "zero-mode selector and lambda_1^+ row missing",
            "claim_valid": "False",
            "valid_for_claim": "False",
        },
    ]


def runner_rows() -> List[Dict[str, str]]:
    return [
        {
            "runner_id": "RUN4348_0_current",
            "branch_input": "current corpus through 4347",
            "action": "ADOPT_LAMBDA_RI_POSITIVE_DOMAIN_LAW_KEEP_CLAIM_FALSE",
            "output": "lambda_RI,lower formula and domain branches are explicit; component values remain open",
            "claim_policy": "no local-GR/PPN/R10/clock/orbital claim",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4348_1_zero_future",
            "branch_input": "component rows signed and lambda_RI,lower>0 plus boundary/no-incoming",
            "action": "ALLOW_LAMBDA_KILLS_LAMBDA_MULTIPLIER",
            "output": "Lambda=0 for owner-tail zero theorem",
            "claim_policy": "only this owner-tail leg closes; remaining gates still separate",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4348_2_bound_future",
            "branch_input": "positive lambda_RI,lower but residual forcing survives",
            "action": "RUN_OWNER_TAIL_FINITE_INVERSE_BOUND",
            "output": "||Lambda|| <= ||R_Lambda||/lambda_RI,lower",
            "claim_policy": "score only with real R_Lambda/projection/boundary/incoming rows",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4348_3_next_components",
            "branch_input": "current component pack",
            "action": "FILL_ZRI_MRI_ETARI_OR_DOMAIN_SPECTRUM_ROWS",
            "output": NEXT_TARGET,
            "claim_policy": "source component rows before any claim",
            "valid_for_claim": "False",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    return [
        {
            "firewall_id": "FW4348_0",
            "forbidden_shortcut": "Treating the flat Dirichlet smoke gap as the physical collar spectrum",
            "reason": "ell_RI, boundary anchoring, units and correction bounds must be source-backed.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4348_1",
            "forbidden_shortcut": "Using Neumann/no-flux while ignoring the constant zero mode",
            "reason": "Neumann branch needs a mass gap or a signed zero-mode projector.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4348_2",
            "forbidden_shortcut": "Letting Ricci/operator corrections be negative without Eta_RI",
            "reason": "negative corrections subtract from the gap and must be bounded.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4348_3",
            "forbidden_shortcut": "Using this static gap to erase hyperbolic incoming modes",
            "reason": "I_RI remains a separate owner-tail clause from 4347.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4348_0",
            "decision": DECISION,
            "reason": "lambda_RI is now a precise positive-domain law with domain branches and component rows; physical component values remain unsigned",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4348_0",
            "item": "lambda_RI law",
            "status": "POSITIVE_DOMAIN_LAW_DERIVED",
            "notes": "lambda_RI,lower = Z_RI,min lambda_dom + M_RI,min^2 - Eta_RI - B_RI,neg.",
        },
        {
            "status_id": "STAT4348_1",
            "item": "best branch",
            "status": "DIRICHLET_ANCHORED_ROUTE_SELECTED_FIRST",
            "notes": "flat candidate gives pi^2/ell_RI^2 if the residual boundary anchor is parent-signed.",
        },
        {
            "status_id": "STAT4348_2",
            "item": "claim status",
            "status": "COMPONENT_VALUES_UNSIGNED",
            "notes": "Z_RI, lambda_dom, M_RI^2, Eta_RI and B_RI,neg need source-backed rows.",
        },
        {
            "status_id": "STAT4348_3",
            "item": "next target",
            "status": "SOURCE_COMPONENT_ROWS",
            "notes": NEXT_TARGET,
        },
    ]


def next_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_target_id": "NT4348_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can Z_RI,min, M_RI,min^2, Eta_RI and the physical domain spectrum be source-backed enough to make lambda_RI,lower positive?",
            "preferred_route": "derive Z_RI,min=1 for the adopted RI principal block, sign an anchored Dirichlet/zero-mode domain, and prove Eta_RI+B_RI,neg below the spectral gap",
            "fallback_route": "keep lambda_RI as a finite nonclaim denominator row and source each component before owner-tail scoring",
            "valid_for_claim": "False",
        }
    ]


def build_tables() -> Dict[str, List[Dict[str, str]]]:
    return {
        "sources": source_rows(),
        "theorems": theorem_rows(),
        "domains": domain_branch_rows(),
        "components": component_rows(),
        "candidates": candidate_rows(),
        "runner": runner_rows(),
        "firewall": firewall_rows(),
        "decision": decision_rows(),
        "status": status_rows(),
        "next": next_rows(),
    }


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    formal = f"""# 364 PPC4161 lambda-RI positive domain or bound input pack

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint does not prove public local GR, Newton, R10, PPN, clock safety, orbital safety, WEP safety, Maxwell closure, source coupling closure, or a fundamental prediction of `G_N`.

## Result

4348 turns the `lambda_RI>0` phrase into an explicit theorem-or-input pack.

For the static RI adjoint branch:

```text
L_RI^dagger = -D_i(Z_RI D^i) + M_RI^2 + V_Ric - E_RI.
```

After bounding negative curvature/operator/boundary pieces:

```text
a_RI[Lambda,Lambda]
 >= Z_RI,min ||D Lambda||^2
  + (M_RI,min^2 - Eta_RI - B_RI,neg)||Lambda||^2.
```

If the domain supplies a Poincare/spectral gap:

```text
||D Lambda||^2 >= lambda_dom(D_RI)||Lambda||^2,
```

then:

```text
lambda_RI,lower
 := Z_RI,min lambda_dom(D_RI)
  + M_RI,min^2
  - Eta_RI
  - B_RI,neg.
```

The exact owner-tail adjoint leg closes when:

```text
lambda_RI,lower > 0
=> Lambda=0.
```

The best current route is the anchored/Dirichlet residual domain:

```text
lambda_RI,lower = pi^2/ell_RI^2
```

only in the flat/unit-normalized candidate with `Z_RI=1`, `M_RI^2=0`, `Eta_RI=0`, `B_RI,neg=0`, and a parent-signed finite collar length `ell_RI`. That is a useful symbolic route, not a physical claim.

## Source Register

{md_table(tables["sources"], ["source_id", "path", "path_exists", "needle_found", "line_number", "role", "valid_for_claim"])}

## Theorem Rows

{md_table(tables["theorems"], ["theorem_id", "statement", "formula", "result", "status", "valid_for_claim"])}

## Domain Branch Audit

{md_table(tables["domains"], ["branch_id", "domain_branch", "domain_condition", "lambda_dom_rule", "positive_gap_condition", "status", "valid_for_claim"])}

## Component Input Pack

{md_table(tables["components"], ["component_id", "symbol", "definition", "candidate_from_current_sources", "required_for_claim", "current_status", "valid_for_claim"])}

## Symbolic Candidate Rows

{md_table(tables["candidates"], ["candidate_id", "route", "lambda_lower_symbolic", "conditions", "what_is_real_now", "promotion_blocker", "claim_valid", "valid_for_claim"])}

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
    post = f"""# 4348 Y5-R2FR lambda-RI positive domain or bound input pack

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4348 derives the physical positive-gap contract:

```text
lambda_RI,lower =
  Z_RI,min lambda_dom(D_RI)
  + M_RI,min^2
  - Eta_RI
  - B_RI,neg.
```

If this lower bound is positive, the homogeneous adjoint multiplier is killed. If not, the owner-tail route keeps a finite denominator ledger and cannot claim local GR.

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
                    "4348 derives the physical positive-domain law for the RI adjoint gap. "
                    "On the static collar, a_RI[Lambda,Lambda] is bounded below by Z_RI,min||D Lambda||^2 plus M_RI,min^2 minus Eta_RI and the negative boundary form. "
                    "With a signed domain gap lambda_dom(D_RI), the claim-usable lower bound is lambda_RI,lower=Z_RI,min lambda_dom+M_RI,min^2-Eta_RI-B_RI,neg. "
                    "If lambda_RI,lower>0 then L_RI^dagger Lambda=0 implies Lambda=0; otherwise the owner-tail branch keeps a finite denominator row. "
                    "The flat Dirichlet symbolic route gives pi^2/ell_RI^2 only if the finite collar/domain and correction-zero assumptions are parent-signed. Current component values remain unsigned."
                ),
                "4348 source register, theorem rows, domain branch audit, component input pack, symbolic candidate rows, runner, firewall, decision, status, next-target and validation CSV.",
                "private_lambda_RI_positive_domain_law_nonclaim_component_rows_missing",
                "Source or derive Z_RI,min, physical lambda_dom(D_RI), M_RI,min^2, Eta_RI and B_RI,neg; then rerun the owner-tail zero/bound gate.",
                "Using flat Dirichlet smoke as physical spectrum; ignoring Neumann zero modes; dropping negative correction terms; using static gap to erase incoming modes.",
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

    add("VAL4348_sources_exist", "all source paths exist", all(row["path_exists"] == "True" for row in tables["sources"]), "source_register")
    add("VAL4348_needles_found", "all source anchors found", all(row["needle_found"] == "True" for row in tables["sources"]), "source_register")
    add("VAL4348_theorem_rows", "four theorem rows are present", len(tables["theorems"]) == 4, "theorems")
    add("VAL4348_lambda_formula", "lambda_RI lower-bound formula exists", any("lambda_RI,lower" in row["formula"] for row in tables["theorems"]), "theorems")
    add("VAL4348_domain_branches", "six domain branches are audited", len(tables["domains"]) == 6, "domains")
    add("VAL4348_neumann_guard", "Neumann zero-mode guard exists", any("constant mode" in row["domain_condition"] for row in tables["domains"]), "domains")
    add("VAL4348_components", "six component input rows are present", len(tables["components"]) == 6, "components")
    add("VAL4348_candidate_rows", "symbolic candidate rows are nonclaim", len(tables["candidates"]) == 4 and all(row["claim_valid"] == "False" for row in tables["candidates"]), "candidates")
    add("VAL4348_no_claim_flags", "all valid_for_claim flags remain false", all(row.get("valid_for_claim", "False") == "False" for table in tables.values() for row in table if "valid_for_claim" in row), "all_tables")
    add("VAL4348_next_target", "next target sources component rows", any(NEXT_TARGET in row["next_target"] for row in tables["next"]), "next")
    add("VAL4348_docs_exist", "formal and checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "docs")
    add("VAL4348_formal_marker", "formal marker exists", MARKER in read_text(FORMAL_PATH), "formal")
    add("VAL4348_post_marker", "post marker exists", MARKER in read_text(DOC_PATH), "post")
    add("VAL4348_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims")
    add("VAL4348_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "spine")
    add("VAL4348_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "packet")

    for key, path in paths.items():
        if key == "validation":
            continue
        try:
            with path.open(newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
            parsed = True
        except Exception:
            parsed = False
        add(f"VAL4348_csv_parse_{key}", f"{key} CSV parses", parsed, str(path))

    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4348_SOURCE_REGISTER.csv",
        "theorems": SOURCE_DIR / "P8_Y5_R2FR_4348_THEOREM_ROWS.csv",
        "domains": SOURCE_DIR / "P8_Y5_R2FR_4348_DOMAIN_BRANCH_AUDIT.csv",
        "components": SOURCE_DIR / "P8_Y5_R2FR_4348_COMPONENT_INPUT_PACK.csv",
        "candidates": SOURCE_DIR / "P8_Y5_R2FR_4348_SYMBOLIC_CANDIDATE_ROWS.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4348_RUNNER.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4348_CLAIM_FIREWALL.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4348_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4348_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4348_NEXT_TARGET.csv",
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
## PPC4161 4348 lambda-RI positive-domain law

Marker: `{MARKER}`

4348 derives the physical lower-bound contract for the RI adjoint gap:

```text
lambda_RI,lower =
  Z_RI,min lambda_dom(D_RI)
  + M_RI,min^2
  - Eta_RI
  - B_RI,neg.
```

If `lambda_RI,lower>0`, the homogeneous adjoint multiplier vanishes. The best route is an anchored/Dirichlet residual domain; the Neumann/no-flux route needs either a mass gap or a zero-mode projector. No claim fires until `Z_RI,min`, `lambda_dom`, `M_RI,min^2`, `Eta_RI`, and `B_RI,neg` are source-backed.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4348 packet lambda-RI positive-domain law

Marker: `{PACKET_MARKER}`

Packet update: the owner-tail gap is now a precise positive-domain contract, not a vague missing lambda. The packet must source `Z_RI,min`, `lambda_dom(D_RI)`, `M_RI,min^2`, `Eta_RI`, and `B_RI,neg` before using the owner-tail zero theorem or finite inverse score.
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
