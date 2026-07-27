from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4310"
CLAIM_ID = "L-151"
BRANCH = "MTS_R2FR_Y5_COLLAR_NO_CONCENTRATION_SIGNATURE_OR_TRACE_BOUND_INPUTS_4310"
DECISION = "COLLAR_NO_CONCENTRATION_REDUCED_TO_LAMBDA_FLOOR_AND_RESIDUAL_SILENCE_TRACE_INPUTS_RETAINED_NONCLAIM"
MARKER = "PPC4161_COLLAR_NO_CONCENTRATION_SIGNATURE_OR_TRACE_BOUND_INPUTS_4310"
PACKET_MARKER = "PPC4161_PACKET_COLLAR_NO_CONCENTRATION_SIGNATURE_OR_TRACE_BOUND_INPUTS_4310"
NEXT_TARGET = "4311-Y5-R2FR-lambda-floor-source-row-or-collar-residual-first-bound.md"

FORMAL_PATH = FORMAL / "326-PPC4161-collar-no-concentration-signature-or-trace-bound-inputs.md"
DOC_PATH = POST / "4310-Y5-R2FR-collar-no-concentration-signature-or-trace-bound-inputs.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4310_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4310_00_4309_doc": (
        POST / "4309-Y5-R2FR-source-domain-limit-defect-zero-or-first-numeric-flux-bound.md",
        "COLLAR_NO_CONCENTRATION_OR_TRACE_INPUTS_NEXT",
        "4309 handoff: sign collar no-concentration or source trace-bound inputs.",
    ),
    "SRC4310_01_4309_formal": (
        FORMAL / "325-PPC4161-source-domain-limit-defect-zero-or-first-numeric-flux-bound.md",
        "N_inner <= C_N[(Zbar+Mbar+EtaH_U)A_U + R_U] + ||B_src^A||.",
        "4309 first trace-bound formula.",
    ),
    "SRC4310_02_4302_lambda": (
        FORMAL / "318-PPC4161-m-lock-coercivity-gap-and-DvGamma-quadratic-input-pack.md",
        "lambda_m = Z_min lambda_1(D_loc)+M2_min-Eta_H",
        "coercivity gap formula.",
    ),
    "SRC4310_03_4302_nohair": (
        FORMAL / "318-PPC4161-m-lock-coercivity-gap-and-DvGamma-quadratic-input-pack.md",
        "lambda_m>0 and J_eff=0 and B_m=0",
        "exact m-lock no-hair gate.",
    ),
    "SRC4310_04_4301_positive": (
        FORMAL / "317-PPC4161-parent-double-zero-lock-or-second-order-DvGamma-bound-row.md",
        "lambda_m > 0",
        "parent double-zero lock requires positive operator/source-boundary silence.",
    ),
    "SRC4310_05_4268_fixed_collar": (
        FORMAL / "284-PPC4161-Dq-boundary-projector-fixed-collar-or-boundary-residual-bound.md",
        "fixed compact no-flux local collar/worldtube branch",
        "fixed collar and q-basic boundary projector precedent.",
    ),
    "SRC4310_06_4176_noflux": (
        FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md",
        "supp(T_local) subset int(W_loc)",
        "compact local no-flux/support-separation selector.",
    ),
    "SRC4310_07_319_visible": (
        FORMAL / "319-PPC4161-source-boundary-silence-or-component-norms-for-m-lock.md",
        "with no direct m slot in S_vis",
        "visible Hilbert no-direct-m source clause.",
    ),
    "SRC4310_08_321_npair": (
        FORMAL / "321-PPC4161-source-amplitude-inner-charge-EM-residual-reduction.md",
        "N_pair <= N_inner + N_EM + N_rest",
        "source-pair residual entering collar forcing.",
    ),
    "SRC4310_09_223_poynting": (
        FORMAL / "223-PPC4161-EM-Poynting-Hodge-source-owner-lock.md",
        "Poynting vector is real physical flow",
        "Poynting is Hilbert EM stress or boundary residual, not hidden source.",
    ),
    "SRC4310_10_309_precision": (
        FORMAL / "309-PPC4161-epsilon-mu-tr-shared-local-bound-runner-WEP-R10-PPN-clocks-orbital.md",
        "order-one projection of epsilon_AJ_seed into local observables fails",
        "local precision demands zero/suppression, not order-one coupling leakage.",
    ),
    "SRC4310_11_1714_guard": (
        POST / "1714-Y5-R2FR-Y5-worldtube-Hilbert-source-equality-or-Req-Icommutator-fill.md",
        "R_eq",
        "source-to-Newton equality remains a separate gate.",
    ),
}


def base_row() -> Dict[str, str]:
    return {
        "checkpoint": CHECKPOINT,
        "branch": BRANCH,
        "generated_utc": STAMP,
        "decision": DECISION,
        "claim_allowed": "False",
        "valid_for_claim": "False",
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


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
        writer.writerows(rows)


def md_table(rows: List[Dict[str, str]], columns: List[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(col, "")).replace("\n", "<br>").replace("|", "\\|") for col in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = read_text(path) if path.exists() else ""
    if marker in existing:
        return
    with path.open("a", encoding="utf-8", newline="") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + content.strip() + "\n")


def append_claim_once() -> None:
    path = FORMAL / "02-claims-register.csv"
    existing = read_text(path) if path.exists() else ""
    if CLAIM_ID in existing:
        return
    row = [
        CLAIM_ID,
        "local_gr",
        (
            "4310 reduces the collar no-concentration condition to a lambda-floor and residual-silence criterion. "
            "Starting from the 4309 conormal trace formula, the collar amplitude is no longer treated as an independent "
            "free slot: if the fixed collar is inside the m-lock domain and lambda_m >= lambda_* > 0, then "
            "A_U <= C_col(R_U+N_N+N_boundary)/lambda_*. Substitution gives "
            "N_inner <= C_N[(Zbar+Mbar+EtaH_U)C_col(R_U+N_N+N_boundary)/lambda_* + R_U] + ||B_src^A||. "
            "Thus mu_tr=0 follows if the residual numerator and boundary injection vanish. The current corpus supports "
            "fixed-collar/no-flux and no-direct-m clauses only conditionally, and it lacks a sourced lambda floor and "
            "collar residual values, so the route remains private nonclaim."
        ),
        (
            "4310 source register, collar signature audit, no-concentration criterion, reduced trace-bound inputs, "
            "branch runner, local precision map, decision, firewall, status, next-target and validation CSV."
        ),
        "private_collar_no_concentration_reduced_to_lambda_floor_and_residual_silence_nonclaim",
        (
            "Source lambda_*, C_col, C_N, coefficient ceilings, R_U, N_N/N_boundary and B_src^A, or parent-sign their "
            "zero/positive lower-bound theorems."
        ),
        (
            "Treating q-basic fixed collar as a sourced lambda floor, using conditional no-flux as a numeric zero, "
            "keeping A_U as a free fitted amplitude after deriving the coercive bound, or claiming local GR/Newton while "
            "R_eq, I_commutator and projection gates remain open."
        ),
    ]
    with path.open("a", encoding="utf-8", newline="") as handle:
        csv.writer(handle).writerow(row)


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, purpose) in SOURCES.items():
        text = read_text(path) if path.exists() else ""
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(needle in text),
                "purpose": purpose,
            }
        )
        rows.append(row)
    return rows


def signature_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "SIG4310_0_fixed_collar",
            "fixed q-basic collar/worldtube and boundary projector",
            "4268 fixed compact no-flux collar branch",
            "CONDITIONAL_BRANCH_SUPPORT",
            "partial",
            "supports domain stability but only inside the compact selector branch",
        ),
        (
            "SIG4310_1_support_separation",
            "source/sector support does not cross the collar side interfaces",
            "4176 no-flux/support-separation clauses",
            "CONDITIONAL_NOFLUX_SUPPORT",
            "partial",
            "helps set open-sector collar forcing to zero if parent selector signs it",
        ),
        (
            "SIG4310_2_visible_no_m_slot",
            "visible Hilbert matter/EM have no direct m-source slot",
            "319 visible Hilbert theorem",
            "CONDITIONAL_ZERO_ROUTE",
            "partial",
            "removes direct visible forcing only under the signed branch",
        ),
        (
            "SIG4310_3_EM_Poynting_once",
            "Poynting is counted once as Maxwell-Hodge Hilbert stress or boundary flux",
            "223 EM/Poynting owner lock",
            "ROUTE_AVAILABLE_NOT_NUMERIC_ZERO",
            "partial",
            "prevents double-counting but does not source the radiative residual value",
        ),
        (
            "SIG4310_4_lambda_floor",
            "lambda_m >= lambda_* > 0 on the collar branch",
            "4302 lambda_m formula",
            "MISSING_LOWER_BOUND",
            "no",
            "core missing input for no-concentration theorem",
        ),
        (
            "SIG4310_5_collar_residual_silence",
            "R_U, N_N and boundary/source residuals vanish or are bounded",
            "4309 trace-bound numerator",
            "MISSING_RESIDUAL_VALUES_OR_ZERO_THEOREMS",
            "no",
            "without this, A_U remains bounded but not zero",
        ),
        (
            "SIG4310_6_BsrcA_silence",
            "B_src^A is zero or bounded separately from conormal trace",
            "4309 firewall",
            "MISSING_REPRESENTATIVE_ZERO_OR_BOUND",
            "no",
            "prevents hiding exterior source injection inside gamma_N",
        ),
        (
            "SIG4310_7_verdict",
            "collar no-concentration theorem for live exterior branch",
            "all clauses above",
            "CRITERION_DERIVED_NOT_PARENT_SIGNED",
            "no",
            "the theorem form is ready; claim inputs remain missing",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for sig_id, clause, evidence_basis, status, signed_now, implication in specs:
        row = base_row()
        row.update(
            {
                "signature_id": sig_id,
                "clause": clause,
                "evidence_basis": evidence_basis,
                "status": status,
                "signed_now": signed_now,
                "implication": implication,
                "claim_ready": "False",
            }
        )
        rows.append(row)
    return rows


def criterion_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "CRIT4310_0_energy_gap",
            "If lambda_m >= lambda_* > 0 on U_W, then lambda_* ||u||_H1(U_W)^2 <= <u,L_m u> + residual_boundary_terms.",
            "4302 coercive gap restricted to fixed collar",
            "collar amplitude is controlled by forcing, not a free parameter",
            "DERIVED_CONDITIONAL",
        ),
        (
            "CRIT4310_1_amplitude_bound",
            "A_U <= C_col(R_U + N_N + N_boundary)/lambda_*",
            "energy estimate plus duality",
            "replaces independent A_U with lambda/residual inputs",
            "DERIVED_BOUND_VALUES_MISSING",
        ),
        (
            "CRIT4310_2_trace_substitution",
            "N_inner <= C_N[(Zbar+Mbar+EtaH_U)C_col(R_U+N_N+N_boundary)/lambda_* + R_U] + ||B_src^A||",
            "4309 conormal trace bound plus amplitude bound",
            "first reduced trace-bound formula",
            "DERIVED_REDUCED_BOUND",
        ),
        (
            "CRIT4310_3_zero_condition",
            "If lambda_* stays positive and R_U,N_N,N_boundary,B_src^A -> 0, then A_U->0 and mu_tr=0.",
            "coercivity plus conormal trace zero lemma",
            "no-concentration follows from positive operator and residual silence",
            "EXACT_ZERO_IF_INPUTS_SIGNED",
        ),
        (
            "CRIT4310_4_failure_condition",
            "If lambda_* is missing/nonpositive or residual numerator survives, no-concentration cannot be claimed.",
            "4302 failure gate plus 4309 trace bound",
            "fallback remains a finite bound, not local GR",
            "BOUND_ROUTE_RETAINED",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for criterion_id, statement, basis, implication, status in specs:
        row = base_row()
        row.update(
            {
                "criterion_id": criterion_id,
                "statement": statement,
                "basis": basis,
                "implication": implication,
                "status": status,
                "claim_ready": "False",
            }
        )
        rows.append(row)
    return rows


def input_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "IN4310_0_lambda_floor",
            "lambda_*",
            "positive lower bound for lambda_m on the collar branch",
            "operator spectral gap",
            "MISSING_NUMERIC_OR_THEOREM_LOWER_BOUND",
            "",
            "derive/source Z_min, lambda_1(D_loc), M2_min and Eta_H with lambda_*>0",
        ),
        (
            "IN4310_1_Ccol",
            "C_col",
            "collar coercivity/embedding constant in A_U bound",
            "dimensionless/operator-domain constant",
            "MISSING_ARENA_PROJECTION",
            "",
            "source fixed collar geometry or normalize theoremically",
        ),
        (
            "IN4310_2_CN",
            "C_N",
            "weak conormal trace extension constant",
            "trace/operator constant",
            "MISSING_ARENA_PROJECTION",
            "",
            "source trace extension bound for partialW_H subset U_W",
        ),
        (
            "IN4310_3_coeff_ceiling",
            "K_U := Zbar+Mbar+EtaH_U",
            "upper bilinear-form coefficient ceiling on U_W",
            "operator norm",
            "MISSING_SOURCE_VALUE_OR_THEOREM",
            "",
            "source parent m-lock coefficient ceilings",
        ),
        (
            "IN4310_4_RU",
            "R_U",
            "collar residual ||L_m u||_Hminus1(U_W)",
            "Hminus1 norm",
            "MISSING_RESIDUAL_ZERO_OR_BOUND",
            "",
            "prove source support/no-direct-m silence in collar or source residual value",
        ),
        (
            "IN4310_5_NN",
            "N_N",
            "nonlinear/noise/remainder forcing in collar m-lock equation",
            "dual norm",
            "MISSING_REMAINDER_BOUND",
            "",
            "prove higher-order silence or source local smallness bound",
        ),
        (
            "IN4310_6_Nboundary",
            "N_boundary",
            "open/radiative/corner/domain boundary forcing not included in R_U",
            "boundary dual norm",
            "MISSING_BOUNDARY_RESIDUAL",
            "",
            "use no-flux theorem only if selector clauses are parent-signed; otherwise source bound",
        ),
        (
            "IN4310_7_BsrcA",
            "B_src^A",
            "exterior source-boundary representative injection",
            "Hminus1/2 dual norm",
            "MISSING_REPRESENTATIVE_ZERO_OR_BOUND",
            "",
            "prove representative silence or source bound separately",
        ),
        (
            "IN4310_8_reduced_bound",
            "N_inner_reduced",
            "C_N[K_U*C_col*(R_U+N_N+N_boundary)/lambda_* + R_U] + ||B_src^A||",
            "same norm as N_inner",
            "FORMULA_READY_VALUES_MISSING",
            "",
            "score only after every component is real or theorem-zero",
        ),
        (
            "IN4310_9_zero_case",
            "mu_tr",
            "0 if lambda_*>0 and R_U,N_N,N_boundary,B_src^A -> 0",
            "trace measure",
            "EXACT_ZERO_CONDITIONAL",
            "0 conditional",
            "not live until input rows are parent-signed",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for input_id, symbol, definition, units, status, value_or_theorem, next_action in specs:
        row = base_row()
        row.update(
            {
                "input_id": input_id,
                "symbol": symbol,
                "definition": definition,
                "units": units,
                "status": status,
                "value_or_theorem": value_or_theorem,
                "source_path": "",
                "next_action": next_action,
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def runner_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "RUN4310_0_claim_no_concentration_now",
            "claim collar no-concentration/mu_tr=0 now",
            "REJECT",
            "lambda floor, residual numerator and B_src^A zero are not parent-signed",
            "keep exact conditional theorem plus reduced bound",
        ),
        (
            "RUN4310_1_conditional_zero",
            "all collar signature/input rows theorem-zero or positive",
            "ALLOW_CONDITIONAL",
            "A_U->0, mu_tr=0, B_src^A=0, N_inner=0",
            "then N_pair reduces to N_EM+N_rest before lambda_m scoring",
        ),
        (
            "RUN4310_2_current_bound",
            "current evidence with fixed-collar support but missing lambda/residual inputs",
            "USE_REDUCED_BOUND",
            "N_inner <= C_N[K_U*C_col*(R_U+N_N+N_boundary)/lambda_* + R_U]+||B_src^A||",
            "next target should fill lambda floor or first residual row",
        ),
        (
            "RUN4310_3_precision_guard",
            "allow order-one coupling leakage into local tests",
            "REJECT",
            "4293 shows order-one projection fails local precision rows",
            "must prove zero or derive strong projection suppression",
        ),
        (
            "RUN4310_4_local_GR_guard",
            "claim Newton/local-GR from collar theorem",
            "REJECT",
            "R_eq, I_commutator, EM/rest and projection/calibration gates remain open",
            "continue local source-coupling derivation only",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for runner_id, case, result, reason, next_action in specs:
        row = base_row()
        row.update(
            {
                "runner_id": runner_id,
                "case": case,
                "result": result,
                "reason": reason,
                "next_action": next_action,
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def precision_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "PREC4310_0_WEP",
            "WEP/composition",
            "first-order projection of trace/source leakage must be suppressed or theorem-zero",
            "4293 Y_WEP <= 8.328848673647216e-14 for raw seed-scale leakage",
            "ZERO_OR_SUPPRESSION_REQUIRED",
        ),
        (
            "PREC4310_1_PPN",
            "PPN gamma/beta",
            "metric readout of trace leakage must not mimic PPN source nonlinearity",
            "4293 gamma/beta projection bounds",
            "ZERO_OR_SUPPRESSION_REQUIRED",
        ),
        (
            "PREC4310_2_clock_orbit",
            "clocks/orbital/Gdot",
            "time-varying trace leakage must be static-degenerate or below drift budgets",
            "4293 clock/orbit/Gdot rows",
            "ZERO_OR_SUPPRESSION_REQUIRED",
        ),
        (
            "PREC4310_3_R10",
            "R10/fifth-force",
            "finite-range trace hair must map to alpha(lambda) with source-backed bounds",
            "4293 R10 diagnostic only, no pass",
            "BOUND_INPUTS_REQUIRED",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for precision_id, arena, rule, source_basis, status in specs:
        row = base_row()
        row.update(
            {
                "precision_id": precision_id,
                "arena": arena,
                "rule": rule,
                "source_basis": source_basis,
                "status": status,
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "DEC4310_0_gain",
            "A_U_NOT_FREE_AFTER_COERCIVITY",
            "The collar amplitude can be replaced by residual/lambda inputs: A_U <= C_col(R_U+N_N+N_boundary)/lambda_*.",
            "Use the reduced trace bound going forward.",
        ),
        (
            "DEC4310_1_zero",
            "NO_CONCENTRATION_REDUCED_TO_LAMBDA_AND_RESIDUAL_SILENCE",
            "Positive lambda floor plus vanishing residual numerator and B_src^A gives mu_tr=0.",
            "Try to source lambda_* or the first residual row next.",
        ),
        (
            "DEC4310_2_signature",
            "FIXED_COLLAR_SUPPORT_IS_CONDITIONAL",
            "4268/4176 support the compact no-flux collar branch, but do not provide numeric lambda or all residual zeros.",
            "Keep branch-conditional status visible.",
        ),
        (
            "DEC4310_3_precision",
            "ORDER_ONE_LOCAL_LEAKAGE_FORBIDDEN",
            "4293 says raw order-one local projection fails; this route needs theorem-zero or strong suppression.",
            "Do not score local tests with placeholder leakage.",
        ),
        (
            "DEC4310_4_next",
            "LAMBDA_FLOOR_OR_FIRST_RESIDUAL_ROW_NEXT",
            "The best next move is to source lambda_* or R_U/B_src^A, not broaden the audit.",
            NEXT_TARGET,
        ),
    ]
    rows: List[Dict[str, str]] = []
    for decision_id, result, reason, next_action in specs:
        row = base_row()
        row.update({"decision_id": decision_id, "result": result, "reason": reason, "next_action": next_action})
        rows.append(row)
    return rows


def firewall_rows() -> List[Dict[str, str]]:
    rules = [
        "Do not keep A_U as a free fitted amplitude after deriving the coercive A_U bound.",
        "Do not claim no-concentration without lambda_* > 0 and residual numerator silence/bounds.",
        "Do not treat conditional fixed-collar/no-flux selectors as numeric residual values.",
        "Do not hide B_src^A, radiative Poynting or open-sector flux inside R_U.",
        "Do not use trace-bound rows as local-GR/Newton evidence while R_eq, I_commutator, EM/rest and projection gates remain open.",
    ]
    rows: List[Dict[str, str]] = []
    for index, rule in enumerate(rules):
        row = base_row()
        row.update({"firewall_id": f"FW4310_{index}", "rule": rule, "status": "ACTIVE"})
        rows.append(row)
    return rows


def status_rows() -> List[Dict[str, str]]:
    specs = [
        ("STAT4310_0_AU", "A_U", "REDUCED_NOT_FREE", "bounded by residual numerator over lambda_*"),
        ("STAT4310_1_lambda", "lambda_*", "PRIMARY_MISSING_INPUT", "next best source row or theorem"),
        ("STAT4310_2_residuals", "R_U/N_N/N_boundary/B_src^A", "MISSING_ZERO_OR_BOUND_ROWS", "needed for mu_tr zero or score"),
        ("STAT4310_3_mu_tr", "mu_tr", "EXACT_CONDITIONAL_OR_REDUCED_BOUND", "zero if lambda/residual conditions close"),
        ("STAT4310_4_precision", "local precision", "SUPPRESSION_REQUIRED", "4293 forbids order-one leakage"),
        ("STAT4310_5_local_GR", "local GR/Newton", "STILL_BLOCKED", "source coupling improved, but full GR route remains gated"),
    ]
    rows: List[Dict[str, str]] = []
    for status_id, item, status, note in specs:
        row = base_row()
        row.update({"status_id": status_id, "item": item, "status": status, "note": note})
        rows.append(row)
    return rows


def next_rows() -> List[Dict[str, str]]:
    row = base_row()
    row.update(
        {
            "next_target_id": "NT4310_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can lambda_* be sourced/derived as positive, or should the first collar residual/boundary row be filled?",
            "preferred_route": "derive/source lambda_* = Z_min lambda_1(D_loc)+M2_min-Eta_H > 0 on the fixed collar branch",
            "fallback_route": "source R_U, N_N, N_boundary, B_src^A, C_col, C_N and K_U as nonclaim trace-bound inputs",
        }
    )
    return [row]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    formal_text = f"""# 326 PPC4161 collar no-concentration signature or trace-bound inputs

Marker: `{MARKER}`

## Decision

`{DECISION}`

4310 removes `A_U` as a free mystery amplitude. On the signed collar branch:

```text
A_U <= C_col (R_U + N_N + N_boundary) / lambda_*.
```

Substitute into 4309:

```text
N_inner <= C_N [ K_U C_col (R_U + N_N + N_boundary) / lambda_* + R_U ] + ||B_src^A||,
K_U := Zbar + Mbar + EtaH_U.
```

So the zero route is:

```text
lambda_* > 0,
R_U, N_N, N_boundary, B_src^A -> 0
=> A_U -> 0
=> mu_tr = 0.
```

The corpus supports the compact fixed-collar/no-flux branch conditionally, but does not yet source `lambda_*` or the residual numerator.

## Collar Signature Audit

{md_table(tables["signature"], ["signature_id", "clause", "status", "signed_now", "implication"])}

## No-Concentration Criterion

{md_table(tables["criterion"], ["criterion_id", "statement", "status", "implication"])}

## Reduced Trace-Bound Inputs

{md_table(tables["inputs"], ["input_id", "symbol", "definition", "status", "next_action"])}

## Branch Runner

{md_table(tables["runner"], ["runner_id", "case", "result", "reason"])}

## Local Precision Map

{md_table(tables["precision"], ["precision_id", "arena", "rule", "status"])}

## Result

The local coupling route is sharper again: the next real input is not vague coupling, it is `lambda_*` and the residual numerator in a fixed collar.

Next target: `{NEXT_TARGET}`.
"""
    doc_text = f"""# 4310 - collar no-concentration signature or trace-bound inputs

## Verdict
- Derived the collar no-concentration criterion: `A_U` is bounded by residual numerator over `lambda_*`.
- Reduced the 4309 trace formula to named inputs: `lambda_*`, `C_col`, `C_N`, `K_U`, `R_U`, `N_N`, `N_boundary`, and `B_src^A`.
- Current corpus conditionally supports fixed-collar/no-flux and no-direct-`m` source clauses, but does not source a positive `lambda_*` or residual silence.
- No local-GR/Newton claim fires.

## Source Register
{md_table(tables["sources"], ["source_id", "source_path", "exists", "needle_found", "purpose"])}

## Collar Signature Audit
{md_table(tables["signature"], ["signature_id", "clause", "evidence_basis", "status", "signed_now", "implication"])}

## No-Concentration Criterion
{md_table(tables["criterion"], ["criterion_id", "statement", "basis", "implication", "status"])}

## Reduced Trace-Bound Inputs
{md_table(tables["inputs"], ["input_id", "symbol", "definition", "units", "status", "value_or_theorem", "next_action"])}

## Branch Runner
{md_table(tables["runner"], ["runner_id", "case", "result", "reason", "next_action"])}

## Local Precision Map
{md_table(tables["precision"], ["precision_id", "arena", "rule", "source_basis", "status"])}

## Decision
{md_table(tables["decision"], ["decision_id", "result", "reason", "next_action"])}

## Claim Firewall
{md_table(tables["firewall"], ["firewall_id", "rule", "status"])}

## Status
{md_table(tables["status"], ["status_id", "item", "status", "note"])}

## Next Target
{md_table(tables["next"], ["next_target_id", "next_target", "target_question", "preferred_route", "fallback_route"])}
"""
    FORMAL_PATH.write_text(formal_text, encoding="utf-8")
    DOC_PATH.write_text(doc_text, encoding="utf-8")


def validate_csv(path: Path) -> Tuple[bool, str]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), f"{path.name} parses with {len(rows)} rows"
    except Exception as exc:
        return False, f"{path.name} parse failure: {exc}"


def validation_rows(paths: Dict[str, Path], tables: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []

    def add(check_id: str, description: str, passed: bool, evidence: str) -> None:
        row = base_row()
        row.update({"check_id": check_id, "description": description, "passed": str(passed), "evidence": evidence})
        rows.append(row)

    add("VAL4310_0_sources_exist", "all cited local source paths exist", all(Path(row["source_path"]).exists() for row in tables["sources"]), "source_register")
    add("VAL4310_1_needles_found", "all cited source needles found", all(row["needle_found"] == "True" for row in tables["sources"]), "source_register")
    add("VAL4310_2_AU_reduced", "A_U is reduced by coercivity rather than left free", any(row["criterion_id"] == "CRIT4310_1_amplitude_bound" for row in tables["criterion"]), "criterion_rows")
    add("VAL4310_3_reduced_bound", "reduced trace-bound formula exists", any(row["criterion_id"] == "CRIT4310_2_trace_substitution" for row in tables["criterion"]), "criterion_rows")
    add("VAL4310_4_lambda_missing", "lambda floor remains explicit missing input", any(row["input_id"] == "IN4310_0_lambda_floor" and row["status"] == "MISSING_NUMERIC_OR_THEOREM_LOWER_BOUND" for row in tables["inputs"]), "input_rows")
    add("VAL4310_5_runner_rejects_claim", "runner rejects no-concentration claim now", any(row["runner_id"] == "RUN4310_0_claim_no_concentration_now" and row["result"] == "REJECT" for row in tables["runner"]), "runner_rows")
    add("VAL4310_6_precision_guard", "local precision guard retained", any(row["precision_id"] == "PREC4310_0_WEP" for row in tables["precision"]), "precision_rows")
    add("VAL4310_7_next_selected", f"next target is {NEXT_TARGET}", tables["next"][0]["next_target"] == NEXT_TARGET, "next_rows")
    add(
        "VAL4310_8_claim_flags_false",
        "all generated rows keep claim flags false",
        all(row.get("claim_allowed") == "False" and row.get("valid_for_claim") == "False" for table in tables.values() for row in table),
        "generated_tables",
    )
    add(
        "VAL4310_9_inputs_nonclaim",
        "all reduced input rows remain nonclaim/source-unscored",
        all(row.get("score_ready") == "False" and row.get("valid_for_claim") == "False" for row in tables["inputs"]),
        "input_rows",
    )
    for name, path in paths.items():
        if name == "validation":
            continue
        ok, detail = validate_csv(path)
        add(f"VAL4310_csv_{name}", detail, ok, "generated_artifacts")
    add("VAL4310_docs", "formal and post checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "generated_docs")
    add("VAL4310_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims_register")
    add("VAL4310_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "unification_spine")
    add("VAL4310_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "private_packet")
    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4310_SOURCE_REGISTER.csv",
        "signature": SOURCE_DIR / "P8_Y5_R2FR_4310_COLLAR_SIGNATURE_AUDIT.csv",
        "criterion": SOURCE_DIR / "P8_Y5_R2FR_4310_NO_CONCENTRATION_CRITERION.csv",
        "inputs": SOURCE_DIR / "P8_Y5_R2FR_4310_REDUCED_TRACE_BOUND_INPUTS.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4310_BRANCH_RUNNER.csv",
        "precision": SOURCE_DIR / "P8_Y5_R2FR_4310_LOCAL_PRECISION_MAP.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4310_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4310_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4310_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4310_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = {
        "sources": source_rows(),
        "signature": signature_rows(),
        "criterion": criterion_rows(),
        "inputs": input_rows(),
        "runner": runner_rows(),
        "precision": precision_rows(),
        "decision": decision_rows(),
        "firewall": firewall_rows(),
        "status": status_rows(),
        "next": next_rows(),
    }
    for key, rows in tables.items():
        write_csv(paths[key], rows)
    write_docs(tables)
    append_claim_once()
    append_once(
        FORMAL / "07-unification-spine.md",
        MARKER,
        f"""
## PPC4161 4310 collar no-concentration signature or trace-bound inputs

Marker: `{MARKER}`

4310 reduces collar no-concentration to a lambda-floor and residual-silence gate. The independent trace amplitude is replaced by `A_U <= C_col(R_U+N_N+N_boundary)/lambda_*`, giving `N_inner <= C_N[K_U*C_col(R_U+N_N+N_boundary)/lambda_* + R_U]+||B_src^A||`. Fixed-collar/no-flux support exists only conditionally, and the current corpus still lacks a sourced positive `lambda_*` plus residual numerator rows, so this is a private nonclaim bound/zero criterion.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4310 packet collar no-concentration criterion

Marker: `{PACKET_MARKER}`

Packet update: the local source-coupling trace defect now reduces to a positive collar gap plus residual silence. Next useful inputs are `lambda_*`, `C_col`, `C_N`, `K_U`, `R_U`, `N_N`, `N_boundary` and `B_src^A`; no free `A_U` fitting is allowed after this checkpoint.
""",
    )
    validation = validation_rows(paths, tables)
    write_csv(paths["validation"], validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(tables)} csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(validation)} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['description']} evidence={row['evidence']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
