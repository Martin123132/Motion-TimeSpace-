from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4309"
CLAIM_ID = "L-150"
BRANCH = "MTS_R2FR_Y5_SOURCE_DOMAIN_LIMIT_DEFECT_ZERO_OR_FIRST_NUMERIC_FLUX_BOUND_4309"
DECISION = "CONORMAL_TRACE_ZERO_LEMMA_DERIVED_MU_TR_BOUND_ROW_READY_VALUES_MISSING_NONCLAIM"
MARKER = "PPC4161_SOURCE_DOMAIN_LIMIT_DEFECT_ZERO_OR_FIRST_NUMERIC_FLUX_BOUND_4309"
PACKET_MARKER = "PPC4161_PACKET_SOURCE_DOMAIN_LIMIT_DEFECT_ZERO_OR_FIRST_NUMERIC_FLUX_BOUND_4309"
NEXT_TARGET = "4310-Y5-R2FR-collar-no-concentration-signature-or-trace-bound-inputs.md"

FORMAL_PATH = FORMAL / "325-PPC4161-source-domain-limit-defect-zero-or-first-numeric-flux-bound.md"
DOC_PATH = POST / "4309-Y5-R2FR-source-domain-limit-defect-zero-or-first-numeric-flux-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4309_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4309_00_4308_doc": (
        POST / "4308-Y5-R2FR-smooth-Hilbert-volume-domain-parent-signature-or-worldtube-flux-profile-row.md",
        "DEFECT_ZERO_OR_FIRST_NUMERIC_FLUX_BOUND_NEXT",
        "4308 handoff: prove mu_tr zero or source/bound the first trace profile.",
    ),
    "SRC4309_01_4308_formal": (
        FORMAL / "324-PPC4161-smooth-Hilbert-volume-domain-parent-signature-or-worldtube-flux-profile-row.md",
        "mu_tr := weak-lim_epsilon_to_0 g_in,epsilon dSigma",
        "formal trace-defect object.",
    ),
    "SRC4309_02_4306_boundary": (
        FORMAL / "322-PPC4161-inner-domain-certificate-or-QmH-bound.md",
        "N_inner <= C_tr",
        "4306 boundary-dual trace bound.",
    ),
    "SRC4309_03_4307_domain": (
        FORMAL / "323-PPC4161-source-domain-owner-or-inner-flux-profile-fill.md",
        "partialD_in = empty set  =>  N_inner = 0",
        "smooth branch and exterior branch split.",
    ),
    "SRC4309_04_4302_operator": (
        FORMAL / "318-PPC4161-m-lock-coercivity-gap-and-DvGamma-quadratic-input-pack.md",
        "L_m u = -nabla_i(Z_m h^ij nabla_j u) + M_m^2 u + Delta_H[u],",
        "m-lock operator used for the conormal trace lemma.",
    ),
    "SRC4309_05_4302_nohair": (
        FORMAL / "318-PPC4161-m-lock-coercivity-gap-and-DvGamma-quadratic-input-pack.md",
        "lambda_m>0 and J_eff=0 and B_m=0",
        "exact no-hair branch from positive m-lock.",
    ),
    "SRC4309_06_4301_lock": (
        FORMAL / "317-PPC4161-parent-double-zero-lock-or-second-order-DvGamma-bound-row.md",
        "lambda_m > 0",
        "parent double-zero lock reduced to positive-operator/no-hair gate.",
    ),
    "SRC4309_07_319_no_m_slot": (
        FORMAL / "319-PPC4161-source-boundary-silence-or-component-norms-for-m-lock.md",
        "with no direct m slot in S_vis",
        "visible Hilbert no-direct-m source clause.",
    ),
    "SRC4309_08_321_npair": (
        FORMAL / "321-PPC4161-source-amplitude-inner-charge-EM-residual-reduction.md",
        "N_pair <= N_inner + N_EM + N_rest",
        "source-pair branch entering the collar forcing.",
    ),
    "SRC4309_09_185_source": (
        FORMAL / "185-PPC4161-Hilbert-source-measure-descent-and-delta-ZH-closure.md",
        "All ordinary local source sectors use the same observed metric/coframe and the same volume measure.",
        "smooth Hilbert source measure support.",
    ),
    "SRC4309_10_1714_guard": (
        POST / "1714-Y5-R2FR-Y5-worldtube-Hilbert-source-equality-or-Req-Icommutator-fill.md",
        "R_eq",
        "source-to-Newton equality remains a separate gate.",
    ),
    "SRC4309_11_1715_guard": (
        POST / "1715-Y5-R2FR-PiM-commutator-fixed-topology-or-Icommutator-source-profile.md",
        "I_commutator",
        "topological commutator remains a separate gate.",
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
            "4309 derives the weak conormal trace zero lemma for the 4308 trace-defect object. On a collar U_W "
            "around the worldtube surface, define gamma_N^epsilon by the Green identity "
            "<gamma_N^epsilon,psi>=a_U(u_epsilon,Epsi)-<L_m u_epsilon,Epsi>. Then "
            "||gamma_N^epsilon||_{H^{-1/2}} is bounded by a collar trace constant times the H1 collar amplitude "
            "and the local residual ||L_m u_epsilon||_{H^{-1}}, plus any exterior source-boundary injection. Therefore "
            "mu_tr=0 if the collar no-hair/no-concentration terms and B_src^A vanish. The theorem is derived, but "
            "the current corpus does not yet source the collar constants, lambda_m lower bound, or signed no-concentration "
            "hypotheses, so the first flux-bound row remains nonclaim."
        ),
        (
            "4309 source register, conormal trace zero lemma, zero-condition audit, first flux-bound row, "
            "branch runner, Npair/lambda update, decision, firewall, status, next-target and validation CSV."
        ),
        "private_conormal_trace_zero_lemma_mu_tr_bound_values_missing_nonclaim",
        (
            "Parent-sign collar no-concentration/no-source conditions and lambda_m lower bound, or source the trace "
            "constant, collar residual and boundary injection inputs for the mu_tr bound."
        ),
        (
            "Claiming mu_tr=0 without collar H1/residual convergence, using global no-hair without a collar trace theorem, "
            "hiding B_src^A inside the conormal trace, or claiming Newton/local-GR while lambda_m, R_eq and I_commutator remain open."
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


def conormal_lemma_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "CTL4309_0_collar_setup",
            "Choose a fixed collar U_W of partialW_H and a bounded trace extension E:H^{1/2}(partialW_H)->H^1(U_W).",
            "geometric setup",
            "needed before exterior trace statements are meaningful",
            "SETUP_DERIVED_NEEDS_PARENT_COLLAR",
        ),
        (
            "CTL4309_1_weak_conormal_definition",
            "<gamma_N^eps,psi> := a_U(u_eps,Epsi) - <L_m u_eps,Epsi>_{U_W}",
            "Green identity for L_m",
            "defines Z_m n.grad u on rough/weak fields without assuming classical derivatives",
            "DERIVED_DEFINITION",
        ),
        (
            "CTL4309_2_trace_bound",
            "||gamma_N^eps||_{H^{-1/2}} <= C_N[(Zbar+Mbar+EtaH_U)||u_eps||_{H1(U_W)} + ||L_m u_eps||_{H^{-1}(U_W)}]",
            "bounded bilinear form plus extension theorem",
            "turns mu_tr into a collar amplitude/residual problem",
            "DERIVED_BOUND",
        ),
        (
            "CTL4309_3_nohair_to_collar",
            "||u_eps||_{H1(U_W)} <= C_col (N_collar+N_N)/lambda_m when lambda_m>=lambda_* and the collar is inside the parent m-lock domain",
            "4302 coercivity/no-hair gate restricted to the collar",
            "connects positive operator route to trace-defect zero",
            "CONDITIONAL_BOUND_VALUES_MISSING",
        ),
        (
            "CTL4309_4_mu_zero",
            "If ||u_eps||_{H1(U_W)}->0, ||L_m u_eps||_{H^{-1}(U_W)}->0, and ||B_src^A_eps||->0, then mu_tr=0 and B_src^A=0.",
            "weak convergence plus the conormal trace bound",
            "this is the desired smooth-to-exterior no-defect theorem",
            "EXACT_ZERO_IF_HYPOTHESES_SIGNED",
        ),
        (
            "CTL4309_5_bound_if_open",
            "||mu_tr|| + ||B_src^A|| <= limsup C_N[(Zbar+Mbar+EtaH_U)||u_eps||_{H1(U_W)} + ||L_m u_eps||_{H^{-1}(U_W)}] + ||B_src^A||",
            "absolute no-cancellation envelope",
            "first source-ready flux bound if zero theorem does not close",
            "BOUND_ROW_READY_VALUES_MISSING",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for lemma_id, statement, basis, implication, status in specs:
        row = base_row()
        row.update(
            {
                "lemma_id": lemma_id,
                "statement": statement,
                "basis": basis,
                "implication": implication,
                "status": status,
                "claim_ready": "False",
            }
        )
        rows.append(row)
    return rows


def zero_condition_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "ZERO4309_0_parent_collar",
            "fixed collar U_W belongs to the same parent m-lock operator domain",
            "needed for applying 4302 coercivity to the trace surface",
            "MISSING_PARENT_COLLAR_SIGNATURE",
            "no",
        ),
        (
            "ZERO4309_1_lambda_lower",
            "lambda_m >= lambda_* > 0 on the collar branch",
            "needed for collar no-hair and H1 amplitude decay",
            "MISSING_NUMERIC_OR_THEOREM_LOWER_BOUND",
            "no",
        ),
        (
            "ZERO4309_2_collar_forcing",
            "N_collar := ||L_m u_eps||_{H^{-1}(U_W)} -> 0",
            "needed for weak conormal trace decay",
            "MISSING_COLLAR_RESIDUAL_ZERO_OR_BOUND",
            "no",
        ),
        (
            "ZERO4309_3_no_concentration",
            "u_eps -> 0 in H1(U_W) and no gradient concentration at partialW_H",
            "needed for mu_tr=0",
            "MISSING_LIMIT_THEOREM",
            "no",
        ),
        (
            "ZERO4309_4_boundary_injection",
            "B_src^A_eps -> 0 separately from gamma_N",
            "prevents hiding source-representative injection inside trace flux",
            "MISSING_REPRESENTATIVE_ZERO_OR_BOUND",
            "no",
        ),
        (
            "ZERO4309_5_visible_no_m_slot",
            "visible Hilbert matter/EM have no direct m slot in the signed branch",
            "helps zero the collar forcing but does not alone sign the domain/limit",
            "CONDITIONAL_SUPPORT_FROM_319",
            "yes_conditionally",
        ),
        (
            "ZERO4309_6_verdict",
            "mu_tr=0 for the live exterior/source-normalization branch",
            "all zero clauses above",
            "ZERO_THEOREM_DERIVED_BUT_NOT_PARENT_SIGNED",
            "no",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for condition_id, condition, role, status, signed_now in specs:
        row = base_row()
        row.update(
            {
                "condition_id": condition_id,
                "condition": condition,
                "role": role,
                "status": status,
                "signed_now": signed_now,
                "claim_ready": "False",
            }
        )
        rows.append(row)
    return rows


def first_bound_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "FB4309_0_trace_constant",
            "C_N",
            "weak conormal trace/extension constant for partialW_H subset U_W",
            "operator/collar constant",
            "MISSING_ARENA_PROJECTION",
            "",
            "source collar geometry or prove a universal normalized bound",
        ),
        (
            "FB4309_1_coefficient_ceiling",
            "Zbar+Mbar+EtaH_U",
            "upper norm of m-lock bilinear-form coefficients on U_W",
            "operator norm",
            "MISSING_SOURCE_VALUE_OR_THEOREM",
            "",
            "source coefficient ceilings from the parent m-lock action",
        ),
        (
            "FB4309_2_collar_amplitude",
            "A_U := ||u_eps||_{H1(U_W)}",
            "collar H1 amplitude of the m-lock perturbation",
            "H1 norm",
            "MISSING_ZERO_THEOREM_OR_BOUND",
            "",
            "prove no-concentration/no-hair or bound from lambda_m",
        ),
        (
            "FB4309_3_collar_residual",
            "R_U := ||L_m u_eps||_{H^{-1}(U_W)}",
            "local residual forcing seen in the collar",
            "H^{-1} norm",
            "MISSING_COLLAR_RESIDUAL",
            "",
            "show source support is away from collar or source the residual",
        ),
        (
            "FB4309_4_boundary_injection",
            "B_src^A",
            "exterior source-boundary representative/injection",
            "H^{-1/2} dual norm",
            "MISSING_ZERO_THEOREM_OR_BOUND",
            "",
            "prove representative silence or source its bound",
        ),
        (
            "FB4309_5_bound_formula",
            "N_inner_defect",
            "C_N[(Zbar+Mbar+EtaH_U)A_U + R_U] + ||B_src^A||",
            "same norm as N_inner",
            "FORMULA_READY_VALUES_MISSING",
            "",
            "score only when every component is real or theorem-zero",
        ),
        (
            "FB4309_6_zero_special_case",
            "mu_tr",
            "0 if A_U=0, R_U=0, and B_src^A=0 in the eps->0 limit",
            "H^{-1/2} trace measure",
            "EXACT_ZERO_CONDITIONAL",
            "0 conditional",
            "not a live claim until zero conditions are parent-signed",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for bound_id, symbol, definition, units, status, value_or_theorem, next_action in specs:
        row = base_row()
        row.update(
            {
                "bound_id": bound_id,
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
            "RUN4309_0_claim_mu_zero_now",
            "claim mu_tr=0 for the live exterior branch",
            "REJECT",
            "collar domain, lambda lower bound, no-concentration and B_src^A zero are not parent-signed",
            "keep exact conditional lemma plus bound row",
        ),
        (
            "RUN4309_1_conditional_zero",
            "apply conormal trace zero lemma under signed collar hypotheses",
            "ALLOW_CONDITIONAL",
            "mu_tr=0 and B_src^A=0, so the 4308 trace-defect contribution vanishes",
            "then N_pair reduces to N_EM+N_rest on the smooth branch",
        ),
        (
            "RUN4309_2_current_bound",
            "current honest branch with unsigned zero hypotheses",
            "USE_BOUND_ROW",
            "N_inner <= C_N[(Zbar+Mbar+EtaH_U)A_U+R_U]+||B_src^A||",
            "source C_N, coefficient ceilings, A_U, R_U and B_src^A",
        ),
        (
            "RUN4309_3_collar_nohair_path",
            "try to derive A_U and R_U zero from lambda_m>0 and source silence",
            "NEXT_DERIVATION",
            "A_U <= C_col(N_collar+N_N)/lambda_m, then conormal trace decays if numerator decays",
            NEXT_TARGET,
        ),
        (
            "RUN4309_4_local_GR_guard",
            "claim local GR/Newton from mu_tr lemma",
            "REJECT",
            "lambda_m values, EM/rest residuals, R_eq, I_commutator and calibration/projection gates remain open",
            "no public/local-GR claim",
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


def handoff_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "HAND4309_0_zero_if_signed",
            "mu_tr=0 and B_src^A=0",
            "N_inner=0",
            "N_pair <= N_EM + N_rest",
            "Delta_m <= (N_EM+N_rest+N_N)/lambda_m",
            "CONDITIONAL_HANDOFF",
        ),
        (
            "HAND4309_1_current_bound",
            "N_inner <= C_N[(Zbar+Mbar+EtaH_U)A_U+R_U]+||B_src^A||",
            "N_pair <= C_N[(Zbar+Mbar+EtaH_U)A_U+R_U]+||B_src^A||+N_EM+N_rest",
            "Delta_m <= (N_pair+N_N)/lambda_m",
            "values missing but formula is score-ready",
            "BOUND_HANDOFF_VALUES_MISSING",
        ),
        (
            "HAND4309_2_monopole_expansion",
            "||mu_tr|| <= C_0|Q_m^H| + C_perp||g_perp||",
            "N_pair <= C_0|Q_m^H|+C_perp||g_perp||+||B_src||+N_EM+N_rest",
            "Delta_m <= (N_pair+N_N)/lambda_m",
            "equivalent worldtube profile expansion",
            "PROFILE_HANDOFF_VALUES_MISSING",
        ),
        (
            "HAND4309_3_guard",
            "source-domain trace control only",
            "retain R_eq + I_commutator + calibration/projection residuals",
            "local arena scores remain blocked",
            "prevents closed-wrong-charge move",
            "GUARD_ACTIVE",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for handoff_id, inner_bound, npair_formula, delta_m_formula, needed_for_claim, status in specs:
        row = base_row()
        row.update(
            {
                "handoff_id": handoff_id,
                "inner_bound": inner_bound,
                "npair_formula": npair_formula,
                "delta_m_formula": delta_m_formula,
                "needed_for_claim": needed_for_claim,
                "status": status,
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "DEC4309_0_gain",
            "CONORMAL_TRACE_ZERO_LEMMA_DERIVED",
            "The trace defect is now controlled by a weak conormal trace theorem, not a handwaved boundary term.",
            "Use the collar H1/residual conditions as the next exact proof gate.",
        ),
        (
            "DEC4309_1_zero",
            "MU_TR_ZERO_REDUCED_TO_COLLAR_NO_CONCENTRATION",
            "If A_U, R_U and B_src^A vanish in the smooth-to-exterior limit, mu_tr=0 follows.",
            "Try to parent-sign collar no-concentration/no-source support next.",
        ),
        (
            "DEC4309_2_bound",
            "FIRST_FLUX_BOUND_FORMULA_READY",
            "If zero does not close, the first bound is C_N[(Zbar+Mbar+EtaH_U)A_U+R_U]+||B_src^A||.",
            "Source C_N, coefficient ceilings, A_U, R_U and B_src^A before any local test score.",
        ),
        (
            "DEC4309_3_no_claim",
            "LOCAL_GR_STILL_BLOCKED",
            "This advances source coupling but does not close lambda_m, EM/rest, R_eq, I_commutator or calibration.",
            "Keep claim gates shut.",
        ),
        (
            "DEC4309_4_next",
            "COLLAR_NO_CONCENTRATION_OR_TRACE_INPUTS_NEXT",
            "The best next move is to prove the collar no-concentration signature or fill trace-bound inputs.",
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
        "Do not claim mu_tr=0 without H1 collar decay, local residual decay and B_src^A silence.",
        "Do not use global no-hair as a substitute for a collar conormal trace theorem.",
        "Do not absorb B_src^A into gamma_N, Q_m^H or g_perp; boundary injection is a separate absolute row.",
        "Do not score the trace-bound formula with placeholder C_N, lambda_m, A_U or R_U values.",
        "Do not use the conormal trace lemma as a Newton/local-GR proof while R_eq, I_commutator and calibration gates remain open.",
    ]
    rows: List[Dict[str, str]] = []
    for index, rule in enumerate(rules):
        row = base_row()
        row.update({"firewall_id": f"FW4309_{index}", "rule": rule, "status": "ACTIVE"})
        rows.append(row)
    return rows


def status_rows() -> List[Dict[str, str]]:
    specs = [
        ("STAT4309_0_mu_tr", "mu_tr", "ZERO_LEMMA_DERIVED_NOT_SIGNED", "vanishes if collar H1/residual/injection terms vanish"),
        ("STAT4309_1_trace_bound", "trace-bound formula", "FORMULA_READY_VALUES_MISSING", "C_N, coefficient ceilings, A_U, R_U and B_src^A needed"),
        ("STAT4309_2_collar_nohair", "collar no-hair/no-concentration", "NEXT_CORE_GATE", "must be parent-signed or bounded"),
        ("STAT4309_3_Ninner", "N_inner", "CONDITIONAL_ZERO_OR_BOUND", "no longer vague; controlled by conormal trace envelope"),
        ("STAT4309_4_Npair", "N_pair", "BOUND_HANDOFF_READY_NOT_NUMERIC", "feeds lambda_m only after inputs are sourced"),
        ("STAT4309_5_local_GR", "local GR/Newton", "STILL_BLOCKED", "lambda_m, EM/rest, R_eq/I_commutator and projection remain open"),
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
            "next_target_id": "NT4309_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can the collar no-concentration/no-source-support conditions be parent-signed, or must trace-bound constants and residuals be sourced?",
            "preferred_route": "prove fixed collar, lambda_m lower bound, N_collar->0, H1 no-concentration and B_src^A->0 so mu_tr=0",
            "fallback_route": "source C_N, Zbar/Mbar/EtaH_U, A_U, R_U and B_src^A as nonclaim trace-bound inputs",
        }
    )
    return [row]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    formal_text = f"""# 325 PPC4161 source-domain limit defect zero or first numeric flux bound

Marker: `{MARKER}`

## Decision

`{DECISION}`

4309 derives the weak conormal trace bridge:

```text
<gamma_N^eps,psi> := a_U(u_eps,Epsi) - <L_m u_eps,Epsi>_U_W
```

and therefore:

```text
||gamma_N^eps||_Hminus1/2
 <= C_N[(Zbar+Mbar+EtaH_U)||u_eps||_H1(U_W)
        + ||L_m u_eps||_Hminus1(U_W)].
```

So:

```text
mu_tr=0 if ||u_eps||_H1(U_W) -> 0,
          ||L_m u_eps||_Hminus1(U_W) -> 0,
          and ||B_src^A_eps|| -> 0.
```

If those hypotheses are not signed, the first honest bound is:

```text
N_inner <= C_N[(Zbar+Mbar+EtaH_U)A_U + R_U] + ||B_src^A||.
```

## Conormal Trace Zero Lemma

{md_table(tables["lemma"], ["lemma_id", "statement", "status", "implication"])}

## Zero-Condition Audit

{md_table(tables["zero"], ["condition_id", "condition", "status", "signed_now"])}

## First Flux Bound Row

{md_table(tables["bound"], ["bound_id", "symbol", "definition", "status", "next_action"])}

## Branch Runner

{md_table(tables["runner"], ["runner_id", "case", "result", "reason"])}

## Npair/Lambda Handoff

{md_table(tables["handoff"], ["handoff_id", "inner_bound", "npair_formula", "status"])}

## Result

The coupling gap has been reduced again: the trace defect is now either a theorem-zero from collar no-concentration or a concrete bound requiring named constants and residuals. No local-GR/Newton claim follows yet.

Next target: `{NEXT_TARGET}`.
"""
    doc_text = f"""# 4309 - source-domain limit defect zero or first numeric flux bound

## Verdict
- Derived the weak conormal trace zero lemma for `mu_tr`.
- `mu_tr=0` follows if collar `H1` amplitude, local residual and exterior boundary injection vanish in the smooth-to-exterior limit.
- Current corpus does not parent-sign the fixed collar, `lambda_m` lower bound, no-concentration limit, or `B_src^A=0`.
- The fallback is now a first scoreable formula: `N_inner <= C_N[(Zbar+Mbar+EtaH_U)A_U + R_U] + ||B_src^A||`.
- No local-GR/Newton claim fires.

## Source Register
{md_table(tables["sources"], ["source_id", "source_path", "exists", "needle_found", "purpose"])}

## Conormal Trace Zero Lemma
{md_table(tables["lemma"], ["lemma_id", "statement", "basis", "implication", "status"])}

## Mu_tr Zero-Condition Audit
{md_table(tables["zero"], ["condition_id", "condition", "role", "status", "signed_now"])}

## First Flux Bound Row
{md_table(tables["bound"], ["bound_id", "symbol", "definition", "units", "status", "value_or_theorem", "next_action"])}

## Branch Runner
{md_table(tables["runner"], ["runner_id", "case", "result", "reason", "next_action"])}

## Npair/Lambda Handoff
{md_table(tables["handoff"], ["handoff_id", "inner_bound", "npair_formula", "delta_m_formula", "needed_for_claim", "status"])}

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

    add("VAL4309_0_sources_exist", "all cited local source paths exist", all(Path(row["source_path"]).exists() for row in tables["sources"]), "source_register")
    add("VAL4309_1_needles_found", "all cited source needles found", all(row["needle_found"] == "True" for row in tables["sources"]), "source_register")
    add("VAL4309_2_conormal_definition", "weak conormal trace definition exists", any(row["lemma_id"] == "CTL4309_1_weak_conormal_definition" for row in tables["lemma"]), "lemma_rows")
    add("VAL4309_3_trace_bound", "conormal trace bound exists", any(row["lemma_id"] == "CTL4309_2_trace_bound" for row in tables["lemma"]), "lemma_rows")
    add("VAL4309_4_mu_zero_conditional", "mu_tr zero is conditional on signed hypotheses", any(row["lemma_id"] == "CTL4309_4_mu_zero" and row["status"] == "EXACT_ZERO_IF_HYPOTHESES_SIGNED" for row in tables["lemma"]), "lemma_rows")
    add("VAL4309_5_zero_not_signed", "zero-condition audit keeps live claim unsigned", any(row["condition_id"] == "ZERO4309_6_verdict" and row["signed_now"] == "no" for row in tables["zero"]), "zero_rows")
    add("VAL4309_6_first_bound_formula", "first flux-bound formula row exists", any(row["bound_id"] == "FB4309_5_bound_formula" for row in tables["bound"]), "bound_rows")
    add("VAL4309_7_runner_rejects_claim", "runner rejects live mu_tr zero claim", any(row["runner_id"] == "RUN4309_0_claim_mu_zero_now" and row["result"] == "REJECT" for row in tables["runner"]), "runner_rows")
    add("VAL4309_8_next_selected", f"next target is {NEXT_TARGET}", tables["next"][0]["next_target"] == NEXT_TARGET, "next_rows")
    add(
        "VAL4309_9_claim_flags_false",
        "all generated rows keep claim flags false",
        all(row.get("claim_allowed") == "False" and row.get("valid_for_claim") == "False" for table in tables.values() for row in table),
        "generated_tables",
    )
    add(
        "VAL4309_10_bound_rows_nonclaim",
        "all bound rows remain nonclaim/source-unscored",
        all(row.get("score_ready") == "False" and row.get("valid_for_claim") == "False" for row in tables["bound"]),
        "bound_rows",
    )
    for name, path in paths.items():
        if name == "validation":
            continue
        ok, detail = validate_csv(path)
        add(f"VAL4309_csv_{name}", detail, ok, "generated_artifacts")
    add("VAL4309_docs", "formal and post checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "generated_docs")
    add("VAL4309_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims_register")
    add("VAL4309_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "unification_spine")
    add("VAL4309_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "private_packet")
    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4309_SOURCE_REGISTER.csv",
        "lemma": SOURCE_DIR / "P8_Y5_R2FR_4309_CONORMAL_TRACE_ZERO_LEMMA.csv",
        "zero": SOURCE_DIR / "P8_Y5_R2FR_4309_MU_TR_ZERO_CONDITION_AUDIT.csv",
        "bound": SOURCE_DIR / "P8_Y5_R2FR_4309_FIRST_FLUX_BOUND_ROW.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4309_BRANCH_RUNNER.csv",
        "handoff": SOURCE_DIR / "P8_Y5_R2FR_4309_NPAIR_LAMBDA_HANDOFF.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4309_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4309_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4309_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4309_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = {
        "sources": source_rows(),
        "lemma": conormal_lemma_rows(),
        "zero": zero_condition_rows(),
        "bound": first_bound_rows(),
        "runner": runner_rows(),
        "handoff": handoff_rows(),
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
## PPC4161 4309 source-domain limit defect zero or first numeric flux bound

Marker: `{MARKER}`

4309 derives the weak conormal trace zero lemma for the 4308 trace-defect object. With a fixed collar `U_W`, bounded trace extension and m-lock operator, `||gamma_N^eps||_H^-1/2 <= C_N[(Zbar+Mbar+EtaH_U)||u_eps||_H1(U_W)+||L_m u_eps||_H^-1(U_W)]`. Hence `mu_tr=0` follows if collar H1 amplitude, collar residual and `B_src^A` vanish in the smooth-to-exterior limit. Current evidence does not yet parent-sign those zero hypotheses, so the first honest bound row is retained: `N_inner <= C_N[(Zbar+Mbar+EtaH_U)A_U+R_U]+||B_src^A||`.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4309 packet conormal trace zero lemma

Marker: `{PACKET_MARKER}`

Packet update: the source-domain trace defect is now controlled by a weak conormal trace theorem. The next proof target is collar no-concentration/no-source support; the fallback is a named bound row requiring `C_N`, coefficient ceilings, `A_U`, `R_U` and `B_src^A`.
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
