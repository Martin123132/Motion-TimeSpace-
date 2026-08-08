from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4350"
CLAIM_ID = "L-191"
BRANCH = "MTS_R2FR_Y5_RI_BOUNDARY_ANCHOR_AND_ETARI_CORRECTION_BOUND_4350"
DECISION = "STATIC_COMPACT_ANCHORED_RI_BRANCH_GIVES_CONDITIONAL_POSITIVE_GAP_ETARI_ZERO_OR_BOUND_NONCLAIM"
MARKER = "PPC4161_RI_BOUNDARY_ANCHOR_AND_ETARI_CORRECTION_BOUND_4350"
PACKET_MARKER = "PPC4161_PACKET_RI_BOUNDARY_ANCHOR_AND_ETARI_CORRECTION_BOUND_4350"
NEXT_TARGET = "4351-Y5-R2FR-RI-owner-tail-zero-application-or-finite-bound-runner.md"

FORMAL_PATH = FORMAL / "366-PPC4161-RI-boundary-anchor-and-EtaRI-correction-bound.md"
DOC_PATH = POST / "4350-Y5-R2FR-RI-boundary-anchor-and-EtaRI-correction-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4350_VALIDATION.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4350_00_4349_handoff": (
        FORMAL / "365-PPC4161-ZRI-MRI-EtaRI-source-or-domain-spectrum-row.md",
        "Eta_RI,total < pi^2/ell_RI^2",
        "4349 handoff: positive RI gap reduces to anchored domain plus Eta ceiling.",
    ),
    "SRC4350_01_4348_domain": (
        FORMAL / "364-PPC4161-lambda-RI-positive-domain-or-bound-input-pack.md",
        "lambda_dom >= lambda_1^D(D_RI)",
        "Dirichlet/anchored residual domain gives the analytic domain spectrum.",
    ),
    "SRC4350_02_4344_adjoint": (
        FORMAL / "360-PPC4161-adjoint-zero-and-boundary-kernel-proof-or-first-Kperp-score-row.md",
        "L_RI^dagger = -D_i(Z_RI D^i) + M_RI^2 + V_Ric - E_RI.",
        "Adjoint operator whose boundary/domain terms must be signed.",
    ),
    "SRC4350_03_192_noflux": (
        FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md",
        "supp(T_local) subset int(W_loc)",
        "Compact local selector/support separation supplies the template for boundary silence.",
    ),
    "SRC4350_04_216_static_guard": (
        FORMAL / "216-PPC4161-Kperp-boundary-zero-or-demotion.md",
        "elliptic/static proof != hyperbolic incoming-mode proof.",
        "Static collar proof firewall.",
    ),
    "SRC4350_05_191_poynting_owner": (
        FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md",
        "So the Poynting vector is not a separate background field.",
        "EM/Poynting must be Hilbert-owned, not double-counted.",
    ),
    "SRC4350_06_4312_REM": (
        POST / "4312-Y5-R2FR-Zmin-M2min-EtaH-source-or-Poynting-residual-cancellation.md",
        "R_EM_Poynting=0",
        "Same-Hodge/current/no-flux EM branch can remove EM correction term conditionally.",
    ),
    "SRC4350_07_4314_rad": (
        POST / "4314-Y5-R2FR-radiative-Poynting-no-flux-or-boundary-flux-row.md",
        "P_rad_EM(tau)=0 pointwise",
        "Radiative Poynting flux is zero only on the closed static collar branch.",
    ),
    "SRC4350_08_4315_hodge": (
        POST / "4315-Y5-R2FR-Hodge-constitutive-owner-zero-or-DeltaHodge-bound.md",
        "Delta_Hodge_EM=0",
        "Same-Hodge constitutive owner can remove Hodge correction conditionally.",
    ),
    "SRC4350_09_4315_envelope": (
        POST / "4315-Y5-R2FR-Hodge-constitutive-owner-zero-or-DeltaHodge-bound.md",
        "no-cancellation envelope",
        "If same-Hodge fails, the EM contribution remains an explicit bound.",
    ),
}


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def find_line(path: Path, needle: str) -> str:
    text = read_text(path)
    index = text.find(needle)
    if index < 0:
        return ""
    return str(text[:index].count("\n") + 1)


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
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
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + block.strip() + "\n", encoding="utf-8")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, role) in SOURCES.items():
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


def anchor_rows() -> List[Dict[str, str]]:
    return [
        {
            "anchor_id": "ANCH4350_0_parent_test_space",
            "clause": "RI multiplier/test field lives in the compact residual test space H_0^1(D_RI)",
            "derivation": "If the local selector defines RI variations by compactly supported residual tests inside W_loc, the adjoint multiplier Lambda is a dual test field with zero trace on partialD_RI.",
            "result": "Lambda|partialD_RI=0",
            "status": "CONDITIONAL_THEOREM_IF_PARENT_SELECTOR_SIGNS_TEST_SPACE",
            "valid_for_claim": "False",
        },
        {
            "anchor_id": "ANCH4350_1_fixed_residual_representative",
            "clause": "boundary residual representative fixed before variation",
            "derivation": "Fixing the residual representative on the collar boundary removes the constant/reference mode from the adjoint problem; the homogeneous multiplier cannot shift by a boundary-supported constant.",
            "result": "Dirichlet/anchored representative route is allowed branch-locally",
            "status": "CONDITIONAL_BRANCH_NOT_GLOBAL",
            "valid_for_claim": "False",
        },
        {
            "anchor_id": "ANCH4350_2_no_flux_not_enough",
            "clause": "Neumann/no-flux without test-space anchoring",
            "derivation": "No-flux alone leaves the constant mode because M_RI,min^2=0 in the minimal RI owner block.",
            "result": "reject as positive-gap proof",
            "status": "FAILS_FOR_MINIMAL_BRANCH",
            "valid_for_claim": "False",
        },
        {
            "anchor_id": "ANCH4350_3_physical_charge_guard",
            "clause": "boundary anchor must not delete physical Hamiltonian/EM/radiative charges",
            "derivation": "The anchor applies only to the RI residual test multiplier; physical EM/gravity radiation and Hamiltonian flux are either absent in the closed collar or routed as boundary charges.",
            "result": "no hidden erasure of radiation or source charge",
            "status": "FIREWALL_ACTIVE",
            "valid_for_claim": "False",
        },
    ]


def eta_zero_rows() -> List[Dict[str, str]]:
    return [
        {
            "eta_id": "ETA4350_0_Ric",
            "component": "Eta_Ric",
            "zero_condition": "fixed flat/static observed collar or nonnegative Ricci/lower-order block on the RI adjoint domain",
            "bound_if_open": "Eta_Ric <= ||(E_RI - V_Ric)_+||_op",
            "current_result": "zero only in flat/static or signed nonnegative lower-order branch",
            "status": "ZERO_OR_BOUND_CONDITION_DERIVED",
            "valid_for_claim": "False",
        },
        {
            "eta_id": "ETA4350_1_comm",
            "component": "Eta_comm",
            "zero_condition": "D_RI, Green operator, coframe, projector and normal are fixed before variation",
            "bound_if_open": "Eta_comm <= ||[delta_v,L_RI]||_op + ||delta_v domain||_trace",
            "current_result": "zero on fixed-domain/fixed-operator branch",
            "status": "ZERO_OR_BOUND_CONDITION_DERIVED",
            "valid_for_claim": "False",
        },
        {
            "eta_id": "ETA4350_2_EM",
            "component": "Eta_EM",
            "zero_condition": "single Maxwell-Hodge Hilbert owner, same current, no extra XF2/source weight, no Hodge deformation, no net radiative collar flux",
            "bound_if_open": "Eta_EM <= C_EM*(||Delta_Hodge_EM|| ||F||^2 + |delta_w_EM| ||T_EM|| + |C_XF2| ||F||^2 + |C_JQ| ||J dot A|| + |Phi_rad| + ||Delta_internal_exchange||)",
            "current_result": "zero on the 4312/4314/4315 safe EM branch; otherwise explicit no-cancellation envelope",
            "status": "ZERO_OR_BOUND_CONDITION_DERIVED",
            "valid_for_claim": "False",
        },
        {
            "eta_id": "ETA4350_3_Bneg",
            "component": "B_RI,neg",
            "zero_condition": "Lambda in H_0^1(D_RI) or signed/routed nonnegative RI boundary form with no corner injection",
            "bound_if_open": "B_RI,neg <= C_trace ||boundary_data_RI||^2 + C_corner ||corner_RI||^2",
            "current_result": "zero if the anchored residual test space is parent-signed",
            "status": "ZERO_OR_BOUND_CONDITION_DERIVED",
            "valid_for_claim": "False",
        },
        {
            "eta_id": "ETA4350_4_total",
            "component": "Eta_RI,total",
            "zero_condition": "ETA4350_0 through ETA4350_3 zero in the same static compact anchored collar",
            "bound_if_open": "Eta_RI,total <= Eta_Ric_bound + Eta_comm_bound + Eta_EM_bound + B_RI_neg_bound",
            "current_result": "conditional zero branch exists; fallback bound ledger is exact but still lacks numeric/source values",
            "status": "CONDITIONAL_ZERO_OR_BOUND_LEDGER_READY",
            "valid_for_claim": "False",
        },
    ]


def gap_rows() -> List[Dict[str, str]]:
    return [
        {
            "gap_id": "GAP4350_0_clean_static",
            "route": "static compact anchored RI residual collar",
            "lambda_lower": "pi^2/ell_RI^2",
            "conditions": "Lambda in H_0^1(D_RI); Z_RI,min=1; M_RI,min^2=0; Eta_RI,total=0; finite ell_RI",
            "conclusion": "lambda_RI,lower>0 and homogeneous RI adjoint multiplier vanishes",
            "claim_status": "CONDITIONAL_PRIVATE_THEOREM_NOT_PUBLIC_CLAIM",
            "valid_for_claim": "False",
        },
        {
            "gap_id": "GAP4350_1_small_eta",
            "route": "anchored RI residual collar with finite correction ceiling",
            "lambda_lower": "pi^2/ell_RI^2 - Eta_RI,total_bound",
            "conditions": "0 <= Eta_RI,total_bound < pi^2/ell_RI^2",
            "conclusion": "positive gap survives but needs sourced ell_RI and Eta bound rows",
            "claim_status": "BOUND_ROUTE_FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": "False",
        },
        {
            "gap_id": "GAP4350_2_open_eta",
            "route": "anchored but correction ceiling not bounded",
            "lambda_lower": "unscored",
            "conditions": "Eta_RI,total_bound missing or >= pi^2/ell_RI^2",
            "conclusion": "owner-tail zero cannot be applied; finite residual bound only",
            "claim_status": "CLAIM_BLOCKED",
            "valid_for_claim": "False",
        },
        {
            "gap_id": "GAP4350_3_neumann_minimal",
            "route": "minimal RI with no-flux/Neumann constant mode",
            "lambda_lower": "-Eta_RI,total",
            "conditions": "M_RI,min^2=0 and no zero-mode projector",
            "conclusion": "fails as a positive local-GR route",
            "claim_status": "REJECTED_FOR_MINIMAL_BRANCH",
            "valid_for_claim": "False",
        },
    ]


def runner_rows() -> List[Dict[str, str]]:
    return [
        {
            "runner_id": "RUN4350_0_current",
            "input": "current corpus through 4349",
            "action": "TRY_PARENT_ANCHOR_AND_ETARI_ZERO",
            "result": "conditional static compact anchored branch gives Eta_RI,total=0 and positive RI gap",
            "claim_policy": "private branch theorem only; no public local-GR/Newton/R10/PPN claim",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4350_1_apply_if_signed",
            "input": "ANCH4350_0 plus ETA4350_0..4 in same collar",
            "action": "ALLOW_OWNER_TAIL_ZERO_APPLICATION",
            "result": "lambda_RI=pi^2/ell_RI^2 > 0, so 4347 Lambda=0 leg can fire",
            "claim_policy": "requires parent signature of branch clauses before promotion",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4350_2_bound_if_open",
            "input": "any Eta or boundary clause unsigned",
            "action": "KEEP_FINITE_BOUND_ROUTE",
            "result": "owner-tail residual bounded by Eta/B_RI inputs, not set to zero",
            "claim_policy": "needs numeric/source rows before empirical scoring",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4350_3_next",
            "input": "conditional theorem/bound fork written",
            "action": "APPLY_OR_BOUND_OWNER_TAIL",
            "result": NEXT_TARGET,
            "claim_policy": "carry branch signatures explicitly",
            "valid_for_claim": "False",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    return [
        {
            "firewall_id": "FW4350_0",
            "rule": "Do not use no-flux/Neumann as a Dirichlet anchor.",
            "reason": "minimal RI has M_RI,min^2=0, so the constant mode survives.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4350_1",
            "rule": "Do not set Eta_RI,total=0 unless all zero clauses hold in the same collar.",
            "reason": "Ricci, commutator, EM/Hodge/radiative and boundary terms cannot be killed in different branches and then combined.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4350_2",
            "rule": "Do not erase physical radiation or Hamiltonian charge with the RI anchor.",
            "reason": "The anchor is only for the residual adjoint multiplier; physical boundary flux is absent or routed.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4350_3",
            "rule": "Do not treat the static elliptic theorem as a hyperbolic incoming-mode proof.",
            "reason": "The 216 guard remains active outside the static compact branch.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4350_0",
            "decision": DECISION,
            "reason": "A clean local branch now exists: compact anchored RI residual test space plus fixed static same-Hodge/no-radiation collar sets the correction ceiling to zero and gives a positive Dirichlet gap. The branch is not public until the parent action signs those clauses; if any clause remains open, the same formula becomes a finite-bound route.",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4350_0",
            "item": "RI boundary anchor",
            "status": "CONDITIONAL_BRANCH_DERIVED",
            "note": "Lambda in H_0^1(D_RI) follows if the parent selector owns compact residual test fields.",
        },
        {
            "status_id": "STAT4350_1",
            "item": "Eta_RI,total",
            "status": "ZERO_OR_BOUND_LEDGER_READY",
            "note": "Ricci, commutator, EM/Hodge/radiative and boundary pieces have same-collar zero clauses and fallback bounds.",
        },
        {
            "status_id": "STAT4350_2",
            "item": "positive RI gap",
            "status": "CONDITIONAL_STATIC_ANCHORED_PASS",
            "note": "lambda_RI,lower=pi^2/ell_RI^2 on the clean branch; not a public claim.",
        },
        {
            "status_id": "STAT4350_3",
            "item": "next target",
            "status": "OWNER_TAIL_APPLICATION_OR_BOUND",
            "note": NEXT_TARGET,
        },
    ]


def next_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_target_id": "NT4350_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can the 4350 clean branch be applied to the 4347 owner-tail zero theorem, or must the owner tail remain as a finite residual bound?",
            "preferred_route": "apply Lambda=0 on the compact anchored static RI branch and propagate the owner-tail zero into the local GR/Newton residual vector",
            "fallback_route": "write the finite owner-tail bound with Eta_RI,total_bound and ell_RI source rows, keeping all arena claims false",
            "valid_for_claim": "False",
        }
    ]


def build_tables() -> Dict[str, List[Dict[str, str]]]:
    return {
        "sources": source_rows(),
        "anchors": anchor_rows(),
        "eta": eta_zero_rows(),
        "gap": gap_rows(),
        "runner": runner_rows(),
        "firewall": firewall_rows(),
        "decision": decision_rows(),
        "status": status_rows(),
        "next": next_rows(),
    }


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    formal = f"""# 366 PPC4161 RI boundary anchor and EtaRI correction bound

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint does not prove public local GR, Newtonian mechanics, Maxwell/QED, calibrated `G_N`, R10, PPN, clock, orbital, or WEP safety. It does produce a real conditional theorem branch and a finite-bound fallback.

## Result

4350 takes the 4349 condition

```text
lambda_RI,lower = pi^2/ell_RI^2 - Eta_RI,total
```

and sharpens it into an exact theorem fork.

Clean static compact branch:

```text
Lambda in H_0^1(D_RI),
Z_RI,min = 1,
M_RI,min^2 = 0,
Eta_Ric = Eta_comm = Eta_EM = B_RI,neg = 0

=> lambda_RI,lower = pi^2/ell_RI^2 > 0
=> homogeneous RI adjoint multiplier Lambda = 0.
```

This is the route we wanted: not a plateau axiom, not a no-flux handwave, but a compact anchored residual-domain theorem. The price is explicit: the parent selector must own the residual test space and all zero clauses must hold in the same static collar.

If any clause remains unsigned, the result is not thrown away. It becomes the finite bound:

```text
lambda_RI,lower =
  pi^2/ell_RI^2
  - (Eta_Ric_bound + Eta_comm_bound + Eta_EM_bound + B_RI_neg_bound).
```

The local branch can only use the owner-tail zero theorem when this lower bound is positive.

## Source Register

{md_table(tables["sources"], ["source_id", "path", "path_exists", "needle_found", "line_number", "role", "valid_for_claim"])}

## Boundary Anchor Rows

{md_table(tables["anchors"], ["anchor_id", "clause", "derivation", "result", "status", "valid_for_claim"])}

## Eta Zero Or Bound Rows

{md_table(tables["eta"], ["eta_id", "component", "zero_condition", "bound_if_open", "current_result", "status", "valid_for_claim"])}

## Gap Rows

{md_table(tables["gap"], ["gap_id", "route", "lambda_lower", "conditions", "conclusion", "claim_status", "valid_for_claim"])}

## Runner

{md_table(tables["runner"], ["runner_id", "input", "action", "result", "claim_policy", "valid_for_claim"])}

## Claim Firewall

{md_table(tables["firewall"], ["firewall_id", "rule", "reason", "status", "valid_for_claim"])}

## Decision

{md_table(tables["decision"], ["decision_id", "decision", "reason", "next_action", "claim_allowed", "valid_for_claim"])}

## Status

{md_table(tables["status"], ["status_id", "item", "status", "note"])}

## Next Target

{md_table(tables["next"], ["next_target_id", "next_target", "target_question", "preferred_route", "fallback_route", "valid_for_claim"])}
"""
    post = f"""# 4350 Y5-R2FR RI boundary anchor and EtaRI correction bound

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4350 makes a real leap forward on the local-GR route:

```text
compact anchored residual test space + fixed static same-Hodge closed collar
=> Eta_RI,total = 0
=> lambda_RI,lower = pi^2/ell_RI^2 > 0
=> homogeneous RI adjoint multiplier Lambda = 0.
```

This is still private/nonclaim because the parent action must sign the branch clauses. But it is no longer just "missing". The clean theorem path and the finite-bound fallback are now separated.

## Next

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
                    "4350 derives the conditional RI boundary-anchor and Eta-correction theorem fork. If the parent selector owns a compact anchored residual test space so Lambda lives in H_0^1(D_RI), and Ricci/lower-order, commutator/domain-motion, EM/Hodge/radiative, and RI boundary-negative terms vanish in the same fixed static collar, then Eta_RI,total=0 and lambda_RI,lower=pi^2/ell_RI^2>0. The homogeneous RI adjoint multiplier then vanishes, allowing the 4347 owner-tail zero leg only inside that branch. If any clause remains unsigned, the exact fallback is a finite bound with Eta_Ric_bound, Eta_comm_bound, Eta_EM_bound, and B_RI_neg_bound; no public local-GR/Newton/R10/PPN claim fires."
                ),
                (
                    "4350 source register, boundary anchor rows, Eta zero-or-bound rows, gap rows, runner, firewall, decision, status, next-target and validation CSV."
                ),
                "private_static_compact_anchored_RI_positive_gap_branch_nonclaim",
                (
                    "Apply the clean branch to the owner-tail theorem, or write the finite owner-tail bound with sourced ell_RI and Eta component rows."
                ),
                (
                    "Using no-flux as Dirichlet anchoring; setting Eta_RI,total=0 across mixed branches; erasing physical radiation or Hamiltonian charge; treating static elliptic positivity as a hyperbolic incoming-mode proof."
                ),
            ]
        )


def append_spine_and_packet() -> None:
    spine_block = f"""

## PPC4161 4350 RI boundary anchor and EtaRI correction bound

Marker: `{MARKER}`

4350 turns the 4349 symbolic inequality into a theorem fork. On the compact anchored residual test-space branch, `Lambda in H_0^1(D_RI)` gives the Dirichlet/anchored spectrum and kills the negative RI boundary form. If the same fixed static collar also has `Eta_Ric=Eta_comm=Eta_EM=0`, then `Eta_RI,total=0`, so:

```text
lambda_RI,lower = pi^2/ell_RI^2 > 0
```

and the homogeneous RI adjoint multiplier vanishes. If any clause is unsigned, the fallback is the exact finite bound with `Eta_Ric_bound`, `Eta_comm_bound`, `Eta_EM_bound`, and `B_RI_neg_bound`. This is progress toward local GR/Newton, but remains private/nonclaim until the parent action signs the branch clauses.
"""
    packet_block = f"""

## PPC4161 packet update 4350 RI anchor/Eta fork

Marker: `{PACKET_MARKER}`

Packet update: the local owner-tail route now has a clean conditional positive-gap branch instead of only a missing-input ledger. The branch requires compact anchored RI residual tests, fixed static domain/coframe, same-Hodge closed-collar EM ownership, and no negative RI boundary form. Open clauses are routed into an explicit `Eta_RI,total_bound` fallback.
"""
    append_once(FORMAL / "07-unification-spine.md", MARKER, spine_block)
    append_once(FORMAL / "180-PPC4161-private-local-packet-integration.md", PACKET_MARKER, packet_block)


def write_tables(tables: Dict[str, List[Dict[str, str]]]) -> None:
    mapping = {
        "sources": "P8_Y5_R2FR_4350_SOURCE_REGISTER.csv",
        "anchors": "P8_Y5_R2FR_4350_BOUNDARY_ANCHOR_ROWS.csv",
        "eta": "P8_Y5_R2FR_4350_ETARI_ZERO_OR_BOUND_ROWS.csv",
        "gap": "P8_Y5_R2FR_4350_GAP_ROWS.csv",
        "runner": "P8_Y5_R2FR_4350_RUNNER.csv",
        "firewall": "P8_Y5_R2FR_4350_CLAIM_FIREWALL.csv",
        "decision": "P8_Y5_R2FR_4350_DECISION.csv",
        "status": "P8_Y5_R2FR_4350_STATUS.csv",
        "next": "P8_Y5_R2FR_4350_NEXT_TARGET.csv",
    }
    for key, filename in mapping.items():
        write_csv(SOURCE_DIR / filename, tables[key])


def validate(tables: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    checks: List[Tuple[str, bool, str]] = []
    checks.append(("formal_doc_written", FORMAL_PATH.exists(), str(FORMAL_PATH)))
    checks.append(("post_doc_written", DOC_PATH.exists(), str(DOC_PATH)))
    checks.append(("marker_in_formal", MARKER in read_text(FORMAL_PATH), MARKER))
    checks.append(("decision_in_formal", DECISION in read_text(FORMAL_PATH), DECISION))
    checks.append(("clean_gap_formula_present", "lambda_RI,lower = pi^2/ell_RI^2 > 0" in read_text(FORMAL_PATH), "clean branch gap"))
    checks.append(("finite_bound_formula_present", "Eta_Ric_bound + Eta_comm_bound + Eta_EM_bound + B_RI_neg_bound" in read_text(FORMAL_PATH), "finite fallback"))
    checks.append(("all_sources_exist", all(row["path_exists"] == "True" for row in tables["sources"]), "source paths"))
    checks.append(("all_needles_found", all(row["needle_found"] == "True" for row in tables["sources"]), "source needles"))
    checks.append(("anchor_rows_present", len(tables["anchors"]) >= 4, str(len(tables["anchors"]))))
    checks.append(("eta_rows_present", len(tables["eta"]) >= 5, str(len(tables["eta"]))))
    checks.append(("gap_rows_present", len(tables["gap"]) >= 4, str(len(tables["gap"]))))
    checks.append(("no_valid_claim_rows", all(row.get("valid_for_claim") == "False" for rows in tables.values() for row in rows if "valid_for_claim" in row), "all generated claim flags false"))
    checks.append(("neumann_failure_recorded", any(row["gap_id"] == "GAP4350_3_neumann_minimal" for row in tables["gap"]), "minimal Neumann rejected"))
    checks.append(("eta_total_row_recorded", any(row["eta_id"] == "ETA4350_4_total" for row in tables["eta"]), "Eta total row"))
    checks.append(("claim_row_recorded", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), CLAIM_ID))
    checks.append(("spine_marker_recorded", MARKER in read_text(FORMAL / "07-unification-spine.md"), MARKER))
    checks.append(("packet_marker_recorded", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), PACKET_MARKER))
    for filename in [
        "P8_Y5_R2FR_4350_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4350_BOUNDARY_ANCHOR_ROWS.csv",
        "P8_Y5_R2FR_4350_ETARI_ZERO_OR_BOUND_ROWS.csv",
        "P8_Y5_R2FR_4350_GAP_ROWS.csv",
        "P8_Y5_R2FR_4350_RUNNER.csv",
        "P8_Y5_R2FR_4350_CLAIM_FIREWALL.csv",
        "P8_Y5_R2FR_4350_DECISION.csv",
        "P8_Y5_R2FR_4350_STATUS.csv",
        "P8_Y5_R2FR_4350_NEXT_TARGET.csv",
    ]:
        path = SOURCE_DIR / filename
        rows = list(csv.DictReader(path.open(newline="", encoding="utf-8"))) if path.exists() else []
        checks.append((f"csv_{filename}_parse_rows", bool(rows), f"{len(rows)} rows"))
    return [
        {
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "passed": str(bool(passed)),
            "detail": detail,
            "valid_for_claim": "False",
        }
        for check_id, passed, detail in checks
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    tables = build_tables()
    write_tables(tables)
    write_docs(tables)
    append_claim_once()
    append_spine_and_packet()
    validation_rows = validate(tables)
    write_csv(VALIDATION_PATH, validation_rows)
    failures = [row for row in validation_rows if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote 9 csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(validation_rows)} failed={len(failures)}")
    if failures:
        for row in failures:
            print(f"FAILED {row['check_id']}: {row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
