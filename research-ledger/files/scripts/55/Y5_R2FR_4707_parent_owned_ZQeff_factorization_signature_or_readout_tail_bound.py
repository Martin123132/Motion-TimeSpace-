from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4707"
CLAIM_ID = "L-549"
MARKER = "PPC4161_PARENT_OWNED_ZQEFF_FACTORIZATION_OR_READOUT_TAIL_BOUND_4707"
PACKET_MARKER = "PPC4161_PACKET_PARENT_OWNED_ZQEFF_FACTORIZATION_OR_READOUT_TAIL_BOUND_4707"
DECISION = "ZQEFF_FACTORIZATION_EXACT_IF_ALL_CLAUSES_SIGNED_READOUT_TAIL_BOUND_RETAINED_NONCLAIM"
NEXT_TARGET = "4708-Y5-R2FR-first-readout-tail-coefficient-zero-or-source-backed-bound.md"

DOC_PATH = POST / "4707-Y5-R2FR-parent-owned-ZQeff-factorization-signature-or-readout-tail-bound.md"
FORMAL_PATH = FORMAL / "723-PPC4161-parent-owned-ZQeff-factorization-signature-or-readout-tail-bound.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

DOC_3810 = POST / "3810-Y5-R2FR-parent-owned-ZQeff-readout-descent-contract-or-alpha-product-inputs.md"
DOC_3863 = POST / "3863-Y5-R2FR-Maxwell-normalization-charge-current-owner-or-EM-source-scale-bound.md"
DOC_1113 = POST / "1113-Y5-R10-parent-owned-readout-descent-contract-or-alpha-product-input-acquisition.md"
DOC_1219 = POST / "1219-Y5-R10-typed-visible-coefficient-functor-or-hidden-scalar-counterexample-lock.md"
DOC_4703 = POST / "4703-Y5-R2FR-no-extra-F2-operator-domain-or-lambdaA-source-row.md"
DOC_4704 = POST / "4704-Y5-R2FR-visible-operator-domain-image-proof-or-hidden-Hom-bound-row.md"

CSV_4706_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4706_NEXT_TARGET.csv"
CSV_4706_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4706_ZQEFF_KAPPA_DESCENT_THEOREM.csv"
CSV_4706_COUNTER = SOURCE_DIR / "P8_Y5_R2FR_4706_FINITE_BRANCH_COUNTERMODEL_ROWS.csv"
CSV_4706_CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_4706_PARENT_SIGNATURE_CONTRACT.csv"
CSV_4706_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4706_VALIDATION.csv"
CSV_4704_HOM = SOURCE_DIR / "P8_Y5_R2FR_4704_HIDDEN_HOM_BOUND_ROWS_NONCLAIM.csv"
CSV_4705_COMPOSITE = SOURCE_DIR / "P8_Y5_R2FR_4705_COMPOSITE_EM_RESIDUAL_LAW.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4707_SOURCE_REGISTER.csv"
SIGNATURE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4707_FACTORIZATION_SIGNATURE_AUDIT.csv"
ZERO_CONTRACT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4707_EXACT_ZERO_CONTRACT_ROWS.csv"
TAIL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4707_READOUT_TAIL_BOUND_ROWS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4707_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4707_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4707_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4707_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4707_VALIDATION.csv"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def line_of(path: Path, needle: str) -> int:
    for index, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return index
    return 0


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def table(rows: Iterable[dict[str, Any]]) -> str:
    rows = list(rows)
    if not rows:
        return ""
    headers = list(rows[0].keys())
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(header, "")).replace("|", "\\|").replace("\n", " ") for header in headers) + " |")
    return "\n".join(output)


def append_once(path: Path, marker: str, body: str) -> None:
    existing = text(path)
    if marker in existing:
        return
    path.write_text(existing.rstrip() + "\n\n" + body.strip() + "\n", encoding="utf-8")


def source_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4707_00_4706_next", CSV_4706_NEXT, "4707-Y5-R2FR-parent-owned-ZQeff-factorization-signature-or-readout-tail-bound.md", "4706 handoff"),
        ("SRC4707_01_4706_theorem", CSV_4706_THEOREM, "ZK4706_0_chain_rule_kappa_zero", "4706 kappa zero theorem"),
        ("SRC4707_02_4706_counter", CSV_4706_COUNTER, "CEX4706_1_readout_reentry", "4706 readout countermodel"),
        ("SRC4707_03_4706_contract", CSV_4706_CONTRACT, "SIG4706_3_radiative_readout_naturality", "4706 signature contract"),
        ("SRC4707_04_4706_validation", CSV_4706_VALIDATION, "VAL4706_OVERALL", "4706 validation passed"),
        ("SRC4707_05_3810_descent", DOC_3810, "ZRT3810_0_descent_readout_theorem", "3810 descent theorem"),
        ("SRC4707_06_3810_naturality", DOC_3810, "ZRT3810_2_radiative_naturality_extension", "3810 radiative/readout naturality"),
        ("SRC4707_07_3810_readout", DOC_3810, "POC3810_5_readout_closure", "3810 readout closure"),
        ("SRC4707_08_3863_owner", DOC_3863, "MNO3863_2_normalization_owner_theorem", "3863 EM source-scale owner theorem"),
        ("SRC4707_09_3863_bound", DOC_3863, "ESB3863_0_Z_drift", "3863 finite Z drift bound"),
        ("SRC4707_10_1113_parent_domain", DOC_1113, "POC1113_0_parent_domain", "1113 parent domain clause"),
        ("SRC4707_11_1113_maxwell_owner", DOC_1113, "POC1113_3_maxwell_owner", "1113 Maxwell owner clause"),
        ("SRC4707_12_1113_no_hidden", DOC_1113, "POC1113_4_no_hidden_visible_morphisms", "1113 no-hidden-visible clause"),
        ("SRC4707_13_1113_radiative", DOC_1113, "POC1113_6_radiative_closure", "1113 radiative closure clause"),
        ("SRC4707_14_1219_type_rule", DOC_1219, "NHA1219_0_type_rule", "1219 typed visible coefficient rule"),
        ("SRC4707_15_1219_verdict", DOC_1219, "TVC1219_6_verdict", "1219 not-derived verdict"),
        ("SRC4707_16_4703_no_extra", DOC_4703, "NEF4703_1_conditional_zero", "4703 no-extra-F2 conditional zero"),
        ("SRC4707_17_4704_image", DOC_4704, "VIP4704_0_exact_image_zero_theorem", "4704 image theorem"),
        ("SRC4707_18_4704_hom_bound", CSV_4704_HOM, "HOM4704_4_clock_readout_leg", "4704 readout-tail arena row"),
        ("SRC4707_19_4705_composite", CSV_4705_COMPOSITE, "LAW4705_3_composed_memory_F2_bound", "4705 composed finite law"),
    ]
    rows = []
    for source_id, path, needle, role in specs:
        line = line_of(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": line > 0,
                "source_line": line,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def signature_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "clause_id": "FSIG4707_0_parent_domain",
            "clause": "parent configuration/action domain excludes post-readout knobs from parent Euler-Lagrange equations",
            "best_evidence": "POC1113_0_parent_domain",
            "current_signature": "CONTRACT_WRITTEN_NOT_CORPUS_SIGNED",
            "effect_if_signed": "readout-selected forces are demoted to post-solution finite branches",
            "failure_tail": "E_parent_domain_tail",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "clause_id": "FSIG4707_1_ZQeff_factorization",
            "clause": "Z_Q_eff(Phi)=Zbar(q_obs(Phi),theta_rep,mu_rep) with Z_Q_eff positive",
            "best_evidence": "ZRT3810_0;POC1113_3;MNO3863_2",
            "current_signature": "EXACT_THEOREM_SHAPE_OWNER_UNSIGNED",
            "effect_if_signed": "D_v ln Z_Q_eff=0 and kappa_memF2=0 by chain rule",
            "failure_tail": "E_ZQ_factor_tail",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "clause_id": "FSIG4707_2_fixed_rep_readout",
            "clause": "D_v theta_rep = D_v mu_rep = 0 on the same memory vertical generator",
            "best_evidence": "ZRT3810_0;SIG4706_1",
            "current_signature": "UNSIGNED_CRITICAL",
            "effect_if_signed": "representation/readout standards cannot reintroduce hidden memory dependence",
            "failure_tail": "E_theta_mu_tail",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "clause_id": "FSIG4707_3_no_hidden_visible_F2",
            "clause": "visible EM coefficient functor has no hidden/material/readout target into Coeff(F_Q^2)",
            "best_evidence": "NHA1219_0;NEF4703_1;VIP4704_1",
            "current_signature": "EXACT_CONDITIONAL_NO_HOM_NOT_PARENT_SIGNED",
            "effect_if_signed": "Zbar(q)+epsilon*m_mem counterterm is ill-typed",
            "failure_tail": "E_F2_Hom_tail",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "clause_id": "FSIG4707_4_radiative_naturality",
            "clause": "RG, threshold, matching and effective-action maps preserve quotient factorization",
            "best_evidence": "ZRT3810_2;POC1113_6;NHA1219_3",
            "current_signature": "UNSIGNED_CRITICAL",
            "effect_if_signed": "D_v delta_lambda_rad=0",
            "failure_tail": "B_rad",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "clause_id": "FSIG4707_5_observed_readout_closure",
            "clause": "observed alpha, clocks, material response and apparatus maps factor through the same q_obs/Zbar branch after variation",
            "best_evidence": "POC3810_5;POC1113_6;HSC1219_3",
            "current_signature": "UNSIGNED_CRITICAL",
            "effect_if_signed": "D_v delta_lambda_readout=0 and observed clock/readout tails vanish on this branch",
            "failure_tail": "B_readout",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "clause_id": "FSIG4707_6_same_current_owner",
            "clause": "J_Q and T_EM are varied from the same q_obs-descended source action before readout",
            "best_evidence": "ZRT3810_1;POC3810_6;MNO3863_2",
            "current_signature": "EXACT_CONDITIONAL_SOURCE_OWNER_UNSIGNED",
            "effect_if_signed": "no source-only EM normalization or beta_F branch can be introduced after variation",
            "failure_tail": "E_same_current_tail",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "clause_id": "FSIG4707_7_arena_functors",
            "clause": "R10, PPN, clock and orbital observables are post-solution functors of the same branch with source-backed K/tau maps",
            "best_evidence": "POC1113_7;HOM4704 arena rows",
            "current_signature": "MISSING_ARENA_MAPS",
            "effect_if_signed": "one local EM coefficient bound can be transferred without mixing unrelated branches",
            "failure_tail": "E_arena_transfer_tail",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def zero_contract_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "zero_id": "ZERO4707_0_all_clause_factorization",
            "theorem": "If FSIG4707_0 through FSIG4707_7 all sign on one branch, then D_v ln Z_Q_eff = D_v ln alpha_read = 0 for v in ker(Dq_obs).",
            "proof": "Chain rule through Zbar(q_obs,theta_rep,mu_rep), fixed readout data, natural effective/readout functors and same-current variation.",
            "consequence": "kappa_memF2=0, beta_F=0, B_rad=0, B_readout=0 and the memory/F2 leg of the 4705 bound vanishes.",
            "current_status": "EXACT_CONDITIONAL_ZERO_NOT_PROMOTED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "zero_id": "ZERO4707_1_no_extra_F2_subcase",
            "theorem": "If no hidden/material/readout Hom into Coeff(F_Q^2) is parent-signed, then Z_Q_eff=Zbar(q_obs)+epsilon*m_mem is ill-typed.",
            "proof": "A nonconstant memory coefficient needs a visible coefficient target; removing that target removes the derivative rather than tuning it.",
            "consequence": "This closes the 4706 finite countermodel at tree level, subject to radiative/readout preservation.",
            "current_status": "EXACT_CONDITIONAL_NO_HOM_UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "zero_id": "ZERO4707_2_same_branch_transfer_guard",
            "theorem": "If same-current owner and arena functors sign, an alpha/readout zero may be transferred to R10, WEP, PPN, clocks and orbital rows only on that same branch.",
            "proof": "The observables must be functions of the same post-variation source action/readout branch; otherwise clock alpha closure and source-force closure are different claims.",
            "consequence": "Prevents a fake win by mixing a clock-only alpha theorem with unsourced force-sector couplings.",
            "current_status": "TRANSFER_GUARD_EXACT_ARENA_MAPS_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def tail_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "tail_id": "TAIL4707_0_ZQ_factor_tail",
            "symbol": "E_ZQ_factor_tail",
            "definition": "failure of Z_Q_eff to factor entirely through q_obs and fixed representation/readout data",
            "bound_formula": "|D_v ln Z_Q_eff| <= E_ZQ_factor_tail + E_theta_mu_tail + E_F2_Hom_tail + B_rad + B_readout",
            "feeds": "kappa_memF2; b_alpha; beta_F; C_memory_F2",
            "needed_input": "parent factorization certificate or source-backed derivative bound",
            "status": "FINITE_TAIL_ROW_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "tail_id": "TAIL4707_1_F2_Hom_tail",
            "symbol": "E_F2_Hom_tail",
            "definition": "hidden/material/readout Hom into Coeff(F_Q^2)",
            "bound_formula": "E_F2_Hom_tail <= H_XF2 unless no-Hom/no-extra-F2 signs",
            "feeds": "4704 H_XF2; 4705 composed memory/F2 bound",
            "needed_input": "no-Hom theorem or finite H_XF2/K_arena source row",
            "status": "FINITE_TAIL_ROW_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "tail_id": "TAIL4707_2_radiative_tail",
            "symbol": "B_rad",
            "definition": "loop, threshold, matching or effective-action regeneration of visible EM coefficient drift",
            "bound_formula": "B_rad := |D_v delta_lambda_rad|/Z_Q_eff_min",
            "feeds": "clock/WEP/R10/PPN/orbital EM coefficient rows",
            "needed_input": "radiative naturality proof or finite threshold/matching coefficient",
            "status": "FIRST_HIGH_VALUE_4708_TARGET",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "tail_id": "TAIL4707_3_readout_tail",
            "symbol": "B_readout",
            "definition": "spectroscopy, material, apparatus or post-variation readout re-entry of hidden/representative dependence",
            "bound_formula": "B_readout := |D_v delta_lambda_readout|/Z_Q_eff_min",
            "feeds": "observed alpha, clocks, WEP material response and R10 source/test products",
            "needed_input": "readout functor proof or finite readout coefficient/product value",
            "status": "FIRST_HIGH_VALUE_4708_TARGET",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "tail_id": "TAIL4707_4_same_current_tail",
            "symbol": "E_same_current_tail",
            "definition": "source-only current/stress normalization not owned by the same descended action",
            "bound_formula": "B_arena <= |K_arena_EM|*(E_ZQ_factor_tail+E_F2_Hom_tail+B_rad+B_readout+E_same_current_tail)",
            "feeds": "R10, PPN, WEP, orbital source-scale rows",
            "needed_input": "same-current owner certificate or arena-specific K/tau source row",
            "status": "FINITE_TAIL_ROW_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def promotion_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4707_0_exact_zero_promotion",
            "requires": "all factorization, no-Hom, radiative/readout and same-current clauses signed on one branch",
            "current_result": "BLOCKED_UNSIGNED_CLAUSES",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4707_1_finite_tail_scoring",
            "requires": "source-backed E_ZQ/E_F2Hom/B_rad/B_readout/E_same_current plus arena K/tau maps",
            "current_result": "BLOCKED_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_status_next(timestamp: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    decision = [
        {
            "checkpoint": CHECKPOINT,
            "branch": "MTS_R2FR_Y5_ZQEFF_FACTOR_SIGNATURE_4707",
            "decision": DECISION,
            "reason": "Existing evidence proves the theorem shape but not the parent signatures. Therefore the exact zero route is retained as conditional, while B_rad/B_readout and same-current tails become the first scoreable fallback.",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]
    status = [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "derived": "all-clause exact Z_Q_eff/readout zero contract and finite readout-tail bound decomposition",
            "not_derived": "parent-signed factorization, no-hidden visible coefficient grammar, radiative/readout naturality, same-current source owner, arena K/tau transfer maps",
            "claim_status": "PRIVATE_NONCLAIM",
            "local_GR_public_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]
    next_rows = [
        {
            "checkpoint": CHECKPOINT,
            "next_id": "NT4707_0",
            "target": NEXT_TARGET,
            "reason": "The largest immediately scoreable unsigned pieces are radiative and observed-readout tails; they decide whether bare Z_Q_eff descent survives clocks/material/R10.",
            "derive_first": "try to prove readout/radiative naturality for alpha/spectroscopy/material response on the same q_obs branch",
            "fallback": "source B_rad or B_readout as first finite coefficient product with units and arena map",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]
    return decision, status, next_rows


def write_documents(timestamp: str, data: dict[str, list[dict[str, Any]]]) -> None:
    DOC_PATH.write_text(
        f"""# 4707 - Parent-Owned ZQeff Factorization Signature Or Readout Tail Bound

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

Generated UTC: `{timestamp}`

## Result
4707 tries to sign the `Z_Q_eff` factorization route and rejects promotion from current evidence.

The exact theorem is still strong:

```text
Z_Q_eff = Zbar(q_obs, theta_rep, mu_rep)
with no hidden F2 Hom, natural radiative/readout maps,
and same-current source ownership
=> D_v ln Z_Q_eff = D_v ln alpha_read = 0.
```

But the parent signatures are not all present. The honest finite branch is:

```text
|D_v ln Z_Q_eff| <= E_ZQ_factor_tail + E_theta_mu_tail
                  + E_F2_Hom_tail + B_rad + B_readout.
```

and arena scoring requires:

```text
B_arena <= |K_arena_EM|*(E_ZQ_factor_tail + E_F2_Hom_tail
                         + B_rad + B_readout + E_same_current_tail).
```

So the next target is not another broad scalar audit. It is the first radiative/readout tail proof or finite coefficient row.

## Source Register
{table(data["sources"])}

## Factorization Signature Audit
{table(data["signature"])}

## Exact Zero Contract Rows
{table(data["zero"])}

## Readout Tail Bound Rows
{table(data["tail"])}

## Promotion Gates
{table(data["promotion"])}

## Decision
{table(data["decision"])}

## Status
{table(data["status"])}

## Next Target
{table(data["next"])}
""",
        encoding="utf-8",
    )
    FORMAL_PATH.write_text(
        f"""# 723 - PPC4161 Parent-Owned ZQeff Factorization Signature Or Readout Tail Bound

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

Generated UTC: `{timestamp}`

## Formal Insert
Exact branch:

```text
Z_Q_eff(Phi)=Zbar(q_obs(Phi),theta_rep,mu_rep),
D_v theta_rep = D_v mu_rep = 0,
NoHom(C_hid, Coeff(F_Q^2)),
Natural(EFT/readout),
SameCurrent(J_Q,T_EM)
=> D_v ln Z_Q_eff = D_v ln alpha_read = 0.
```

Finite branch:

```text
|D_v ln Z_Q_eff| <= E_ZQ_factor_tail + E_theta_mu_tail
                  + E_F2_Hom_tail + B_rad + B_readout.
```

Arena transfer:

```text
B_arena <= |K_arena_EM|*(E_ZQ_factor_tail + E_F2_Hom_tail
                         + B_rad + B_readout + E_same_current_tail).
```

No local-GR, Maxwell, alpha, R10, WEP, clock, PPN or orbital claim follows. The next derivation target is radiative/readout naturality or the first source-backed readout-tail coefficient.
""",
        encoding="utf-8",
    )


def update_registers(timestamp: str) -> None:
    claims = read_csv(CLAIMS_PATH) if CLAIMS_PATH.exists() else []
    fieldnames = list(claims[0].keys()) if claims else [
        "claim_id",
        "domain",
        "claim",
        "current_evidence",
        "status",
        "next_test",
        "key_risk",
        "sector",
        "evidence",
        "next_action",
        "risk",
        "title",
        "notes",
    ]
    claim_row = {field: "" for field in fieldnames}
    claim_row.update(
        {
            "claim_id": CLAIM_ID,
            "domain": "local_gr_empirical_interface",
            "claim": "4707 audits parent-owned Z_Q_eff factorization signatures and derives the readout-tail finite bound when signatures remain unsigned.",
            "current_evidence": "Generated source register, factorization signature audit, exact zero contract rows, readout-tail bounds, promotion gates, decision, status, next target and validation.",
            "status": "ZQeff_factorization_signature_unsigned_tail_bound_nonclaim",
            "next_test": NEXT_TARGET,
            "key_risk": "Promoting bare Z_Q_eff descent while readout/radiative or same-current source tails remain unsigned.",
            "sector": "local_gr",
            "evidence": str(DOC_PATH),
            "next_action": NEXT_TARGET,
            "title": "ZQeff factorization signature or readout tail bound",
            "notes": f"{MARKER}; {DECISION}; generated {timestamp}",
        }
    )
    existing = next((row for row in claims if row.get("claim_id") == CLAIM_ID), None)
    if existing is None:
        claims.append(claim_row)
    else:
        existing.update(claim_row)
    write_csv(CLAIMS_PATH, claims)

    append_once(
        SPINE_PATH,
        MARKER,
        f"""### {MARKER}

- Claim: `{CLAIM_ID}`.
- Status: private nonclaim.
- Movement: existing `Z_Q_eff` descent evidence is sorted into an exact all-clause zero theorem versus a finite readout-tail bound.
- Exact branch: `D_v ln Z_Q_eff = D_v ln alpha_read = 0` only if factorization, fixed readout data, no-Hom/no-extra-F2, radiative/readout naturality, same-current owner and arena maps sign on one branch.
- Finite branch: `|D_v ln Z_Q_eff| <= E_ZQ_factor_tail + E_theta_mu_tail + E_F2_Hom_tail + B_rad + B_readout`.
- Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""### {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet role: parent-owned `Z_Q_eff` factorization audit plus first finite readout-tail bound for local EM/source coupling.
- Validation: `{VALIDATION_CSV}`.
""",
    )
    RESUME_PATH.write_text(
        f"""# Current Local Resume Bookmark

Generated: 2026-07-07

Scope: local/private framework work only. No GitHub push, no public-stage update, no backup-repo operation.

## Latest Local Checkpoint

`4707-Y5-R2FR-parent-owned-ZQeff-factorization-signature-or-readout-tail-bound.md`

## What Changed

The `Z_Q_eff` route is now split cleanly:

```text
exact zero if all factorization/readout/current clauses sign
finite branch if any clause fails
```

The finite branch is:

```text
|D_v ln Z_Q_eff| <= E_ZQ_factor_tail + E_theta_mu_tail
                  + E_F2_Hom_tail + B_rad + B_readout.
```

## Current Best Next Target

`{NEXT_TARGET}`

## Do Not Do Next

- Do not loop back into scalar-functional audits.
- Do not claim local GR, Maxwell, alpha, R10, WEP, clock, PPN or orbital closure from these private checkpoints.
- Do not push to GitHub unless Martin explicitly asks for a GitHub update.
""",
        encoding="utf-8",
    )


def validation_rows(timestamp: str, data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "check_id": check_id,
                "passed": passed,
                "detail": detail,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )

    add("VAL4707_0_sources_exist", all(row["path_exists"] for row in data["sources"]), "all source-register paths exist")
    add("VAL4707_1_needles_found", all(row["needle_found"] for row in data["sources"]), "all source-register needles found")
    add("VAL4707_2_signature_rows", len(data["signature"]) >= 8, "factorization signature rows present")
    add("VAL4707_3_unsigned_not_promoted", all(row["claim_allowed"] is False for row in data["signature"]), "unsigned clauses not promoted")
    add("VAL4707_4_exact_contract", any("D_v ln Z_Q_eff" in row["theorem"] for row in data["zero"]), "exact zero contract present")
    add("VAL4707_5_tail_bound", any("B_rad + B_readout" in row["bound_formula"] for row in data["tail"]), "readout/radiative tail bound present")
    add("VAL4707_6_next_readout_tail", data["next"][0]["target"] == NEXT_TARGET, "next readout-tail target selected")
    add("VAL4707_7_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), f"claims register contains {CLAIM_ID}")
    add("VAL4707_8_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker")
    add("VAL4707_9_post_doc", DOC_PATH.exists() and MARKER in text(DOC_PATH), "post checkpoint exists with marker")
    add("VAL4707_10_spine_marker", MARKER in text(SPINE_PATH), "spine marker written")
    add("VAL4707_11_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written")
    add("VAL4707_12_resume_updated", NEXT_TARGET in text(RESUME_PATH), "resume bookmark updated")

    for csv_path in [
        SOURCE_REGISTER,
        SIGNATURE_CSV,
        ZERO_CONTRACT_CSV,
        TAIL_CSV,
        PROMOTION_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]:
        try:
            parsed = read_csv(csv_path)
            add(f"VAL4707_csv_{csv_path.stem}", len(parsed) > 0, f"{csv_path} parses with {len(parsed)} rows")
        except Exception as exc:
            add(f"VAL4707_csv_{csv_path.stem}", False, f"{csv_path} failed to parse: {exc}")

    claim_values: list[str] = []
    for rows_for_table in [
        data["signature"],
        data["zero"],
        data["tail"],
        data["promotion"],
        data["decision"],
        data["status"],
        data["next"],
    ]:
        for row in rows_for_table:
            for key in ("valid_for_claim", "claim_allowed", "local_GR_public_claim"):
                if key in row:
                    claim_values.append(str(row[key]).lower())
    add("VAL4707_13_no_claim_rows_true", all(value in {"false", ""} for value in claim_values), "generated rows keep claim flags false")

    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    add("VAL4707_14_pycache_absent", not pycache.exists(), "scripts __pycache__ absent")

    overall = all(str(row["passed"]) == "True" or row["passed"] is True for row in rows)
    add("VAL4707_OVERALL", overall, "PASS" if overall else "FAIL")
    return rows


def main() -> None:
    timestamp = now()
    decision, status, next_rows = decision_status_next(timestamp)
    data: dict[str, list[dict[str, Any]]] = {
        "sources": source_rows(timestamp),
        "signature": signature_rows(timestamp),
        "zero": zero_contract_rows(timestamp),
        "tail": tail_rows(timestamp),
        "promotion": promotion_rows(timestamp),
        "decision": decision,
        "status": status,
        "next": next_rows,
    }

    write_csv(SOURCE_REGISTER, data["sources"])
    write_csv(SIGNATURE_CSV, data["signature"])
    write_csv(ZERO_CONTRACT_CSV, data["zero"])
    write_csv(TAIL_CSV, data["tail"])
    write_csv(PROMOTION_CSV, data["promotion"])
    write_csv(DECISION_CSV, data["decision"])
    write_csv(STATUS_CSV, data["status"])
    write_csv(NEXT_CSV, data["next"])

    write_documents(timestamp, data)
    update_registers(timestamp)
    validation = validation_rows(timestamp, data)
    write_csv(VALIDATION_CSV, validation)

    print(f"{CHECKPOINT} complete: {DOC_PATH}")
    print(f"validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
