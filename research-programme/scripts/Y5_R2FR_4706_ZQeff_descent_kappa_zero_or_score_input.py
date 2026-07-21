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

CHECKPOINT = "4706"
CLAIM_ID = "L-548"
MARKER = "PPC4161_ZQEFF_DESCENT_KAPPA_ZERO_OR_SCORE_INPUT_4706"
PACKET_MARKER = "PPC4161_PACKET_ZQEFF_DESCENT_KAPPA_ZERO_OR_SCORE_INPUT_4706"
DECISION = "KAPPA_MEMF2_REDUCED_TO_ZQEFF_QUOTIENT_DESCENT_OR_FINITE_SCORE_INPUT_NONCLAIM"
NEXT_TARGET = "4707-Y5-R2FR-parent-owned-ZQeff-factorization-signature-or-readout-tail-bound.md"

DOC_PATH = POST / "4706-Y5-R2FR-composite-EM-local-residual-score-or-first-source-backed-input.md"
FORMAL_PATH = FORMAL / "722-PPC4161-ZQeff-quotient-descent-kappa-zero-or-source-backed-score.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

CSV_4705_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4705_NEXT_TARGET.csv"
CSV_4705_COMPOSITE = SOURCE_DIR / "P8_Y5_R2FR_4705_COMPOSITE_EM_RESIDUAL_LAW.csv"
CSV_4705_CHANNELS = SOURCE_DIR / "P8_Y5_R2FR_4705_SOURCE_CHANNEL_SELECTION_ROWS.csv"
CSV_4705_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4705_VALIDATION.csv"
CSV_4620_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4620_KAPPA_MEMF2_ZERO_ROUTES.csv"
CSV_4620_NUMERIC = SOURCE_DIR / "P8_Y5_R2FR_4620_KAPPA_MEMF2_FIRST_NUMERIC_ROW_NONCLAIM.csv"
CSV_4623_SELECTION = SOURCE_DIR / "P8_Y5_R2FR_4623_PARENT_SELECTION_THEOREMS.csv"
CSV_4623_BETA = SOURCE_DIR / "P8_Y5_R2FR_4623_BETA_OWNERSHIP_MATRIX.csv"
CSV_4704_BLOCKERS = SOURCE_DIR / "P8_Y5_R2FR_4704_CLAIM_BLOCKERS.csv"
DOC_3810 = POST / "3810-Y5-R2FR-parent-owned-ZQeff-readout-descent-contract-or-alpha-product-inputs.md"
DOC_3863 = POST / "3863-Y5-R2FR-Maxwell-normalization-charge-current-owner-or-EM-source-scale-bound.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4706_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4706_ZQEFF_KAPPA_DESCENT_THEOREM.csv"
COUNTERMODEL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4706_FINITE_BRANCH_COUNTERMODEL_ROWS.csv"
HUNT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4706_SOURCE_BACKED_INPUT_HUNT_VERDICT.csv"
CONTRACT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4706_PARENT_SIGNATURE_CONTRACT.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4706_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4706_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4706_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4706_VALIDATION.csv"


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
        ("SRC4706_00_4705_next", CSV_4705_NEXT, "4706-Y5-R2FR-composite-EM-local-residual-score-or-first-source-backed-input.md", "4705 selected score/zero input target"),
        ("SRC4706_01_4705_composite", CSV_4705_COMPOSITE, "LAW4705_3_composed_memory_F2_bound", "4705 composite memory/F2 bound"),
        ("SRC4706_02_4705_channels", CSV_4705_CHANNELS, "CHAN4705_1_EM_scalar", "4705 beta_F/kappa channel"),
        ("SRC4706_03_4705_validation", CSV_4705_VALIDATION, "VAL4705_OVERALL", "4705 validation passed"),
        ("SRC4706_04_4620_zero", CSV_4620_ZERO, "KZ4620_0_typed_domain_zero", "4620 kappa zero routes"),
        ("SRC4706_05_4620_numeric", CSV_4620_NUMERIC, "KNUM4620_0_first_numeric_template", "4620 finite numeric template"),
        ("SRC4706_06_4623_selection", CSV_4623_SELECTION, "PSEL4623_2_betaF_kappa_link", "4623 beta_F/kappa link"),
        ("SRC4706_07_4623_beta", CSV_4623_BETA, "BOWN4623_2_beta_F", "4623 beta_F owner row"),
        ("SRC4706_08_3810_descent", DOC_3810, "ZRT3810_0_descent_readout_theorem", "3810 Z_Q_eff descent theorem"),
        ("SRC4706_09_3810_radiative", DOC_3810, "ZRT3810_2_radiative_naturality_extension", "3810 radiative/readout naturality extension"),
        ("SRC4706_10_3810_readout", DOC_3810, "POC3810_5_readout_closure", "3810 readout closure contract"),
        ("SRC4706_11_3863_owner", DOC_3863, "MNO3863_2_normalization_owner_theorem", "3863 Maxwell normalization/source-scale owner theorem"),
        ("SRC4706_12_3863_bound", DOC_3863, "ESB3863_0_Z_drift", "3863 finite Z drift bound"),
        ("SRC4706_13_4704_readout", CSV_4704_BLOCKERS, "BLK4704_2_radiative_readout_stability", "4704 readout/radiative blocker"),
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


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "ZK4706_0_chain_rule_kappa_zero",
            "claim_piece": "kappa_memF2 zero from quotient descent",
            "formal_statement": "Let v_m be the memory vertical generator with Dq_obs[v_m]=0. If Z_Q_eff(Phi)=Zbar(q_obs(Phi),theta_rep,mu_rep) and theta_rep,mu_rep are fixed on v_m, then kappa_memF2 := D_v_m Z_Q_eff = DZbar[Dq_obs(v_m),Dtheta(v_m),Dmu(v_m)] = 0.",
            "proof": "This is the 3810 chain-rule theorem applied to the memory/F2 coefficient named by 4620. No cancellation or fitting is used.",
            "consequence": "C_memory_F2=0 for the Maxwell kinetic memory leg, and beta_F=0 through the 4623 beta_F=+/-kappa_memF2/4 owner relation.",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "ZK4706_1_radiative_readout_extension",
            "claim_piece": "readout/radiative tail zero from natural quotient maps",
            "formal_statement": "If RG/matching/spectroscopy/readout maps are natural quotient functors on q_obs and fixed representation/readout data, then D_v_m delta_lambda_rad = D_v_m delta_lambda_readout = 0.",
            "proof": "A natural functor fed only quotient data cannot create dependence on a hidden representative coordinate; non-natural thresholds/readouts remain finite residuals.",
            "consequence": "The 4704 B_rad and B_readout terms close only on this same quotient-natural branch.",
            "current_status": "EXACT_CONDITIONAL_EFT_READOUT_EXTENSION_UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "ZK4706_2_same_current_source_scale_extension",
            "claim_piece": "source-only alpha/kappa leakage forbidden by same-current owner",
            "formal_statement": "If charged matter, EM, binding, apparatus and boundary bookkeeping are varied in one q_obs-descended source action using the same A_Q/coframe branch, then no separate source-only kappa_memF2 or beta_F can be introduced after variation.",
            "proof": "A single descended action has one Maxwell kinetic owner and one current/stress variation. A separate source-only coefficient is a different branch, not a consequence of the same parent action.",
            "consequence": "WEP/R10/clock source products cannot borrow a clock-only alpha closure unless same-current ownership is signed.",
            "current_status": "EXACT_CONDITIONAL_SOURCE_OWNER_EXTENSION_UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def countermodel_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "counter_id": "CEX4706_0_hidden_F2_coefficient",
            "countermodel": "Z_Q_eff = Zbar(q_obs) + epsilon*m_mem",
            "why_legal_if_unsigned": "If m_mem is a legal coefficient argument and Coeff(F_Q^2) is a visible target, covariance and U(1) gauge invariance do not forbid this term.",
            "finite_effect": "kappa_memF2=epsilon and C_memory_F2 survives in the 4705 composed bound.",
            "blocked_by": "parent-owned Z_Q_eff quotient factorization; no-Hom/no-extra-F2 operator domain; branch extremum",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "counter_id": "CEX4706_1_readout_reentry",
            "countermodel": "alpha_read = Abar(q_obs,Zbar) + epsilon_readout*m_mem",
            "why_legal_if_unsigned": "A bare action descent does not automatically prove apparatus/spectroscopy/material readout descent.",
            "finite_effect": "delta_lambda_readout remains in |s_XF2| <= H_XF2 + B_rad + B_readout.",
            "blocked_by": "readout functor factorization and radiative naturality on the same branch",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def hunt_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "hunt_id": "HUNT4706_0_kappa_numeric",
            "target": "kappa_memF2 or epsilon_memF2",
            "local_result": "only nonclaim templates and symbolic rows found in current corpus search",
            "best_action": "try quotient-descent zero certificate before fabricating a numeric value",
            "claim_grade_input_found": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "hunt_id": "HUNT4706_1_Zmem_M2mem",
            "target": "Z_mem_min and M2_mem_min",
            "local_result": "operator scaffold and positive-operator theorem exist, but units/signs/branch Hessian values are not claim-grade",
            "best_action": "source parent Hessian signature or retain finite amplitude denominator",
            "claim_grade_input_found": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "hunt_id": "HUNT4706_2_arena_K_tau",
            "target": "K_R10_EM, K_PPN_EM, K_clock_alpha, K_orb_EM and tau projections",
            "local_result": "arena rows are strict schemas; no source-backed projection coefficient was promoted here",
            "best_action": "only score after theorem-zero fails and one arena projection is sourced",
            "claim_grade_input_found": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def contract_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "clause_id": "SIG4706_0_qobs_factorization",
            "clause": "Z_Q_eff(Phi)=Zbar(q_obs(Phi),theta_rep,mu_rep)",
            "role": "kills kappa_memF2 by chain rule",
            "current_signature": "UNSIGNED_CRITICAL",
            "failure_mode": "hidden F2 coefficient remains legal",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "clause_id": "SIG4706_1_fixed_readout_data",
            "clause": "D_v theta_rep = D_v mu_rep = 0 on the same memory vertical generator",
            "role": "prevents hidden representative dependence through standards/readout scales",
            "current_signature": "UNSIGNED_CRITICAL",
            "failure_mode": "readout tail survives even if bare Z_Q_eff descends",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "clause_id": "SIG4706_2_no_extra_F2_Hom",
            "clause": "Coeff(F_Q^2) has no independent hidden/material/readout target outside parent image",
            "role": "prevents Zbar(q)+epsilon*m_mem counterterm",
            "current_signature": "UNSIGNED_CRITICAL",
            "failure_mode": "kappa_memF2 finite branch survives",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "clause_id": "SIG4706_3_radiative_readout_naturality",
            "clause": "RG/matching/spectroscopy/material maps are natural on quotient objects",
            "role": "kills delta_lambda_rad and delta_lambda_readout",
            "current_signature": "UNSIGNED_CRITICAL",
            "failure_mode": "local clocks/WEP/R10 can see regenerated alpha/source drift",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "clause_id": "SIG4706_4_same_current_owner",
            "clause": "J_Q and T_EM are varied from the same q_obs-descended source action before readout",
            "role": "prevents clock-only/source-only branch mixing",
            "current_signature": "UNSIGNED_CRITICAL",
            "failure_mode": "arena products remain nonclaim even if alpha drift closes in one readout",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_status_next(timestamp: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    decision = [
        {
            "checkpoint": CHECKPOINT,
            "branch": "MTS_R2FR_Y5_ZQEFF_DESCENT_KAPPA_ZERO_4706",
            "decision": DECISION,
            "reason": "The best current route is derivation-first: kappa_memF2 is zero if the effective Maxwell normalization descends through q_obs and fixed readout data. If that contract is unsigned, finite score inputs remain required.",
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
            "derived": "exact conditional chain-rule theorem kappa_memF2=0 from Z_Q_eff quotient descent; beta_F consequence; readout/radiative/same-current extensions",
            "not_derived": "parent-owned Z_Q_eff factorization, fixed readout data, no-extra-F2/Hom object language, natural radiative/readout functors, same-current owner",
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
            "next_id": "NT4706_0",
            "target": NEXT_TARGET,
            "reason": "The theorem is exact; the next live work is signing or rejecting the parent-owned factorization/readout clauses.",
            "derive_first": "prove Z_Q_eff and observed alpha/material readout factor through q_obs with no extra F2 Hom target",
            "fallback": "bound finite kappa_memF2, delta_lambda_rad, delta_lambda_readout and same-current product coefficients",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]
    return decision, status, next_rows


def write_documents(timestamp: str, data: dict[str, list[dict[str, Any]]]) -> None:
    DOC_PATH.write_text(
        f"""# 4706 - ZQeff Descent Kappa Zero Or Source-Backed Score Input

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

Generated UTC: `{timestamp}`

## Result
4706 takes the derivation-first route.

The current first coefficient is `kappa_memF2`. The exact zero theorem is:

```text
v_m in ker(Dq_obs),
Z_Q_eff(Phi)=Zbar(q_obs(Phi),theta_rep,mu_rep),
D_v theta_rep = D_v mu_rep = 0
=> kappa_memF2 := D_v_m Z_Q_eff = 0.
```

Since 4623 ties `beta_F` to `kappa_memF2`, this also kills the EM scalar-invariant memory source on the same branch:

```text
beta_F = +/- kappa_memF2/4 = 0.
```

This is not a claim yet. If `Z_Q_eff` or readout/radiative maps can see `m_mem`, the countermodel remains:

```text
Z_Q_eff = Zbar(q_obs) + epsilon*m_mem.
```

Then the 4705 composed finite law remains active.

## Source Register
{table(data["sources"])}

## ZQeff Kappa Descent Theorem
{table(data["theorems"])}

## Finite Branch Countermodels
{table(data["countermodels"])}

## Source-Backed Input Hunt Verdict
{table(data["hunt"])}

## Parent Signature Contract
{table(data["contract"])}

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
        f"""# 722 - PPC4161 ZQeff Quotient Descent Kappa Zero Or Source-Backed Score

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

Generated UTC: `{timestamp}`

## Formal Insert
Let `v_m` be the memory vertical generator. If

```text
Dq_obs[v_m]=0,
Z_Q_eff(Phi)=Zbar(q_obs(Phi),theta_rep,mu_rep),
D_v theta_rep = D_v mu_rep = 0,
```

then

```text
kappa_memF2 := D_v_m Z_Q_eff
              = DZbar[Dq_obs(v_m),Dtheta_rep(v_m),Dmu_rep(v_m)]
              = 0.
```

Through the 4623 owner relation, `beta_F=+/-kappa_memF2/4`, so `beta_F=0` on the same branch. If radiative and readout maps are natural quotient functors, `delta_lambda_rad` and `delta_lambda_readout` also have zero vertical derivative. If any factorization clause fails, the finite branch `Z_Q_eff=Zbar(q_obs)+epsilon*m_mem` remains legal and must be scored with the 4705 composed residual law.
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
            "claim": "4706 derives the exact conditional kappa_memF2=0 theorem from Z_Q_eff quotient descent and keeps finite score inputs only if factorization fails.",
            "current_evidence": "Generated source register, ZQeff kappa theorem, finite countermodels, source-backed hunt verdict, parent signature contract, decision, status, next target and validation.",
            "status": "ZQeff_descent_kappa_zero_nonclaim",
            "next_test": NEXT_TARGET,
            "key_risk": "Treating bare action descent as observed readout descent, or mixing clock alpha closure with source/WEP/R10 products.",
            "sector": "local_gr",
            "evidence": str(DOC_PATH),
            "next_action": NEXT_TARGET,
            "title": "ZQeff quotient descent kappa zero",
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
- Movement: `kappa_memF2` now has an exact zero theorem: if `Z_Q_eff` descends through `q_obs` and fixed readout data, `D_v Z_Q_eff=0` by chain rule.
- Consequence: `beta_F=0` on the same branch because 4623 ties `beta_F` to `kappa_memF2`.
- Firewall: finite `Zbar(q)+epsilon*m_mem`, radiative and readout re-entry remain live until factorization and naturality are parent-signed.
- Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""### {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet role: derivation-first kappa_memF2 zero theorem from parent-owned Z_Q_eff quotient descent.
- Validation: `{VALIDATION_CSV}`.
""",
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

    add("VAL4706_0_sources_exist", all(row["path_exists"] for row in data["sources"]), "all source-register paths exist")
    add("VAL4706_1_needles_found", all(row["needle_found"] for row in data["sources"]), "all source-register needles found")
    add("VAL4706_2_kappa_theorem", any("kappa_memF2 := D_v_m Z_Q_eff" in row["formal_statement"] for row in data["theorems"]), "kappa descent theorem present")
    add("VAL4706_3_betaF_consequence", any("beta_F=0" in row["consequence"] for row in data["theorems"]), "beta_F consequence present")
    add("VAL4706_4_countermodel", any("epsilon*m_mem" in row["countermodel"] for row in data["countermodels"]), "finite countermodel retained")
    add("VAL4706_5_hunt_no_numeric_claim", all(row["claim_grade_input_found"] is False for row in data["hunt"]), "source hunt did not promote numeric claims")
    add("VAL4706_6_signature_contract", len(data["contract"]) >= 5 and all(row["current_signature"] == "UNSIGNED_CRITICAL" for row in data["contract"]), "signature contract rows present and unsigned")
    add("VAL4706_7_next_factorization", data["next"][0]["target"] == NEXT_TARGET, "next factorization/readout target selected")
    add("VAL4706_8_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), f"claims register contains {CLAIM_ID}")
    add("VAL4706_9_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker")
    add("VAL4706_10_post_doc", DOC_PATH.exists() and MARKER in text(DOC_PATH), "post checkpoint exists with marker")
    add("VAL4706_11_spine_marker", MARKER in text(SPINE_PATH), "spine marker written")
    add("VAL4706_12_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written")

    for csv_path in [
        SOURCE_REGISTER,
        THEOREM_CSV,
        COUNTERMODEL_CSV,
        HUNT_CSV,
        CONTRACT_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]:
        try:
            parsed = read_csv(csv_path)
            add(f"VAL4706_csv_{csv_path.stem}", len(parsed) > 0, f"{csv_path} parses with {len(parsed)} rows")
        except Exception as exc:
            add(f"VAL4706_csv_{csv_path.stem}", False, f"{csv_path} failed to parse: {exc}")

    claim_values: list[str] = []
    for rows_for_table in [
        data["theorems"],
        data["countermodels"],
        data["hunt"],
        data["contract"],
        data["decision"],
        data["status"],
        data["next"],
    ]:
        for row in rows_for_table:
            for key in ("valid_for_claim", "claim_allowed", "local_GR_public_claim"):
                if key in row:
                    claim_values.append(str(row[key]).lower())
    add("VAL4706_13_no_claim_rows_true", all(value in {"false", ""} for value in claim_values), "generated rows keep claim flags false")

    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    add("VAL4706_14_pycache_absent", not pycache.exists(), "scripts __pycache__ absent")

    overall = all(str(row["passed"]) == "True" or row["passed"] is True for row in rows)
    add("VAL4706_OVERALL", overall, "PASS" if overall else "FAIL")
    return rows


def main() -> None:
    timestamp = now()
    decision, status, next_rows = decision_status_next(timestamp)
    data: dict[str, list[dict[str, Any]]] = {
        "sources": source_rows(timestamp),
        "theorems": theorem_rows(timestamp),
        "countermodels": countermodel_rows(timestamp),
        "hunt": hunt_rows(timestamp),
        "contract": contract_rows(timestamp),
        "decision": decision,
        "status": status,
        "next": next_rows,
    }

    write_csv(SOURCE_REGISTER, data["sources"])
    write_csv(THEOREM_CSV, data["theorems"])
    write_csv(COUNTERMODEL_CSV, data["countermodels"])
    write_csv(HUNT_CSV, data["hunt"])
    write_csv(CONTRACT_CSV, data["contract"])
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
