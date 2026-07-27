from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4312"
CLAIM_ID = "L-153"
BRANCH = "MTS_R2FR_Y5_ZMIN_M2MIN_ETAH_SOURCE_OR_POYNTING_RESIDUAL_CANCELLATION_4312"
DECISION = "POYNTING_EXTRA_SOURCE_CANCELS_ON_SINGLE_HILBERT_OWNER_BRANCH_OTHERWISE_EXPLICIT_COLLAR_RESIDUAL_BOUND_NONCLAIM"
MARKER = "PPC4161_ZMIN_M2MIN_ETAH_SOURCE_OR_POYNTING_RESIDUAL_CANCELLATION_4312"
PACKET_MARKER = "PPC4161_PACKET_ZMIN_M2MIN_ETAH_SOURCE_OR_POYNTING_RESIDUAL_CANCELLATION_4312"
NEXT_TARGET = "4313-Y5-R2FR-EM-Ward-current-normalization-or-collar-residual-bound-values.md"

FORMAL_PATH = FORMAL / "328-PPC4161-Zmin-M2min-EtaH-source-or-Poynting-residual-cancellation.md"
DOC_PATH = POST / "4312-Y5-R2FR-Zmin-M2min-EtaH-source-or-Poynting-residual-cancellation.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4312_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4312_00_4311_formal": (
        FORMAL / "327-PPC4161-lambda-floor-source-row-or-collar-residual-first-bound.md",
        "S_U <= R_visible + R_EM_Poynting + R_transition + R_boundary + R_nonHilbert + R_N",
        "4311 declared EM/Poynting as an explicit collar residual target.",
    ),
    "SRC4312_01_4311_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4311_NEXT_TARGET.csv",
        "4312-Y5-R2FR-Zmin-M2min-EtaH-source-or-Poynting-residual-cancellation.md",
        "4311 handoff selecting lambda components or Poynting residual cancellation.",
    ),
    "SRC4312_02_4207_doc": (
        FORMAL / "223-PPC4161-EM-Poynting-Hodge-source-owner-lock.md",
        "Poynting vector is real physical flow",
        "Poynting is Hilbert EM stress, not a second source, on the safe branch.",
    ),
    "SRC4312_03_4207_once": (
        FORMAL / "223-PPC4161-EM-Poynting-Hodge-source-owner-lock.md",
        "=> c_Poynt_extra = 0",
        "once-only source theorem for extra Poynting coefficient.",
    ),
    "SRC4312_04_4207_gates": (
        SOURCE_DIR / "P8_Y5_R2FR_4207_RETAINED_GATES.csv",
        "Delta_rad_Poynting",
        "retained EM/Poynting failure gates.",
    ),
    "SRC4312_05_4207_owner": (
        SOURCE_DIR / "P8_Y5_R2FR_4207_POYNTING_OWNER_CHAIN.csv",
        "nabla_mu T_EM",
        "Ward exchange identity and Hilbert owner chain.",
    ),
    "SRC4312_06_319_visible": (
        FORMAL / "319-PPC4161-source-boundary-silence-or-component-norms-for-m-lock.md",
        "with no direct m slot in S_vis",
        "visible-sector no-direct-m source clause.",
    ),
    "SRC4312_07_321_source_split": (
        FORMAL / "321-PPC4161-source-amplitude-inner-charge-EM-residual-reduction.md",
        "N_pair <= N_inner + N_EM + N_rest",
        "source-pair residual split with EM/rest terms retained.",
    ),
    "SRC4312_08_4176_noflux": (
        FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md",
        "supp(T_local) subset int(W_loc)",
        "local no-flux/support-separation collar selector.",
    ),
    "SRC4312_09_4302_lambda": (
        FORMAL / "318-PPC4161-m-lock-coercivity-gap-and-DvGamma-quadratic-input-pack.md",
        "IP4302_4_EtaH",
        "Eta_H remains the correction bucket containing EM/Hodge/boundary terms.",
    ),
    "SRC4312_10_precision": (
        FORMAL / "309-PPC4161-epsilon-mu-tr-shared-local-bound-runner-WEP-R10-PPN-clocks-orbital.md",
        "order-one projection of epsilon_AJ_seed into local observables fails",
        "local precision forbids unbounded EM side-channel leakage.",
    ),
    "SRC4312_11_newton_guard": (
        POST / "1714-Y5-R2FR-Y5-worldtube-Hilbert-source-equality-or-Req-Icommutator-fill.md",
        "R_eq",
        "source-to-Newton equality gate remains open.",
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
            "4312 derives the EM/Poynting collar residual split needed by the 4311 lambda-bound route. "
            "On the single Maxwell-Hodge Hilbert-owner branch, Poynting is real energy flow but it is already "
            "the momentum/energy-flux component of T_EM, so an extra standalone Poynting source coefficient "
            "must be zero. The only EM terms that can enter the collar forcing numerator are therefore explicit "
            "defects: Hodge/constitutive mismatch, EM source-weight drift, extra X F^2 coupling, current/charge "
            "normalization drift, net radiative boundary flux, and unmatched matter-EM Ward exchange. If all six "
            "defects vanish and the collar no-flux selector is signed, R_EM_Poynting=0; otherwise R_EM_Poynting "
            "is bounded by those named defects and contributes to S_U. This advances the local route without "
            "claiming local GR/Newton/R10/PPN."
        ),
        (
            "4312 source register, EM cancellation theorem, residual bound ledger, Eta_H update, local route runner, "
            "claim firewall, status, next-target and validation CSV."
        ),
        "private_poynting_extra_source_cancels_on_single_hilbert_owner_branch_otherwise_residual_bound_nonclaim",
        (
            "Parent-sign the Maxwell-Hodge owner, charge/current normalization, Ward exchange and no-flux collar, "
            "or source numeric bounds for the six EM defect rows and feed them into Eta_H/S_U."
        ),
        (
            "Adding Poynting as a second source after T_EM is already in T_total, deleting radiative flux instead of "
            "routing it to a boundary row, using EM cancellation without same-Hodge/current/Ward signatures, or claiming "
            "local GR/Newton while lambda and source-equality gates remain open."
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


def em_cancellation_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "EC4312_0_same_hodge",
            "same Maxwell-Hodge/Hilbert owner",
            "S_MH uses the same observed metric/coframe/Hodge star as the local gravitational source functional",
            "EM Hilbert stress is counted once inside T_total",
            "CONDITIONAL_BRANCH_SIGNATURE_FROM_4207",
            "needed before cancellation can fire",
        ),
        (
            "EC4312_1_poynting_identity",
            "Poynting identity",
            "S_i = -T_EM(n,e_i) = (E cross B)_i",
            "Poynting is real energy flow, not an extra source field",
            "EXACT_LOCAL_FRAME_IDENTITY_FROM_4207",
            "use this to forbid double counting, not to erase radiation",
        ),
        (
            "EC4312_2_once_only",
            "extra Poynting source coefficient",
            "M_trial = M_H[J_H_total] + c_Poynt_extra int_boundary S_Poynting dot n dA",
            "single-owner branch requires c_Poynt_extra=0",
            "CANCELS_IF_SINGLE_SOURCE_FUNCTIONAL_PARENT_SIGNED",
            "blocks hidden preferred-frame/background-force source",
        ),
        (
            "EC4312_3_ward_exchange",
            "matter-EM Ward exchange",
            "div T_EM = -FJ and div T_matter = +FJ",
            "Lorentz force is internal exchange when both actions share the same current",
            "CONDITIONAL_WARD_CANCELLATION",
            "unmatched exchange stays as Delta_internal_exchange",
        ),
        (
            "EC4312_4_boundary_route",
            "radiative flux route",
            "net Poynting flux through the collar is boundary/Hamiltonian flux",
            "static bulk m-source receives no extra term if no-flux selector is signed",
            "CONDITIONAL_NOFLUX_OR_BOUNDARY_ROW",
            "nonzero radiation enters N_boundary, not hidden R_U",
        ),
        (
            "EC4312_5_zero_theorem",
            "R_EM_Poynting zero branch",
            "same Hodge owner, c_Poynt_extra=0, no X F2, fixed charge/current, Ward exchange, and no net radiative collar flux",
            "R_EM_Poynting=0",
            "EXACT_ZERO_IF_ALL_CLAUSES_SIGNED",
            "not live until parent signatures or source rows exist",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for theorem_id, clause, statement, result, status, implication in specs:
        row = base_row()
        row.update(
            {
                "theorem_id": theorem_id,
                "clause": clause,
                "statement": statement,
                "result": result,
                "status": status,
                "implication": implication,
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def residual_defect_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "RD4312_0_delta_Hodge_EM",
            "Delta_Hodge_EM",
            "observed Hodge/coframe not parent-owned or differs from local metric readout",
            "C_Hodge ||Delta_Hodge_EM|| ||F||^2",
            "Eta_H and S_U",
            "derive same-Hodge owner or source constitutive bound",
        ),
        (
            "RD4312_1_delta_w_EM",
            "delta_w_EM",
            "species/readout EM source weight survives",
            "C_w |delta_w_EM| ||T_EM||",
            "Eta_H/source normalization",
            "prove no independent EM weight or source local bound",
        ),
        (
            "RD4312_2_C_XF2",
            "C_XF2",
            "extra MTS X F^2 coupling",
            "|C_XF2| ||F||^2",
            "R_EM_Poynting and fifth-force side-channel",
            "parent-forbid, screen, or empirically bound",
        ),
        (
            "RD4312_3_C_JQ",
            "C_JQ",
            "hidden EM-current multiplier or charge normalization drift",
            "|C_JQ| ||J dot A||",
            "source-current and clock/WEP residual",
            "derive charge normalization or bound drift",
        ),
        (
            "RD4312_4_Delta_rad_Poynting",
            "Delta_rad_Poynting",
            "net radiative Poynting flux crosses the collar",
            "|int_boundary S_Poynting dot n dA|",
            "N_boundary/Hamiltonian flux",
            "prove no-through-flux selector or route as boundary value",
        ),
        (
            "RD4312_5_Delta_internal_exchange",
            "Delta_internal_exchange",
            "matter-EM exchange not owned by one action/current",
            "||div T_EM + div T_matter||_dual",
            "source conservation and Eta_H",
            "derive Ward exchange cancellation",
        ),
        (
            "RD4312_6_c_Poynt_extra",
            "c_Poynt_extra",
            "standalone Poynting source coefficient",
            "|c_Poynt_extra| |int_boundary S_Poynting dot n dA|",
            "forbidden double-count channel",
            "set exactly zero on single-owner branch; otherwise claim blocked",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for defect_id, symbol, failure_condition, bound_contribution, feeds, next_action in specs:
        row = base_row()
        row.update(
            {
                "defect_id": defect_id,
                "symbol": symbol,
                "failure_condition": failure_condition,
                "bound_contribution": bound_contribution,
                "feeds": feeds,
                "status": "EXPLICIT_DEFECT_ROW_VALUE_MISSING",
                "source_path": "",
                "numeric_value": "",
                "units": "collar dual/source-normalized units",
                "next_action": next_action,
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def residual_bound_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "RB4312_0_R_EM_bound",
            "R_EM_Poynting",
            "R_EM_Poynting <= C_H dH ||F||^2 + C_w |dw| ||T_EM|| + |C_XF2| ||F||^2 + |C_JQ| ||J dot A|| + |Phi_rad| + |Delta_ex|",
            "explicit bound for EM/Poynting contribution to S_U",
            "BOUND_DERIVED_VALUES_MISSING",
        ),
        (
            "RB4312_1_safe_branch",
            "R_EM_Poynting_zero",
            "if dH=dw=C_XF2=C_JQ=Phi_rad=Delta_ex=0 and c_Poynt_extra=0 then R_EM_Poynting=0",
            "exact cancellation branch",
            "CONDITIONAL_ZERO_NOT_LIVE",
        ),
        (
            "RB4312_2_EtaH_update",
            "Eta_H_EM",
            "Eta_H >= Eta_H_nonEM + C_Eta_EM(dH,dw,C_XF2,C_JQ,Phi_rad,Delta_ex)",
            "moves EM/Hodge defects into the lambda-floor correction ledger",
            "ETA_UPDATE_FORMULA_READY_VALUES_MISSING",
        ),
        (
            "RB4312_3_SU_update",
            "S_U",
            "S_U <= R_visible + R_transition + R_boundary + R_nonHilbert + R_N + R_EM_Poynting",
            "4311 residual numerator with EM term made auditable",
            "RESIDUAL_NUMERATOR_UPDATED",
        ),
        (
            "RB4312_4_no_double_count",
            "c_Poynt_extra",
            "single Hilbert source owner implies c_Poynt_extra=0",
            "prevents adding Poynting as separate source after T_EM",
            "DERIVED_CANCELLATION_CLAUSE",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for bound_id, symbol, law, role, status in specs:
        row = base_row()
        row.update(
            {
                "bound_id": bound_id,
                "symbol": symbol,
                "law": law,
                "role": role,
                "status": status,
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def runner_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "RUN4312_0_current_corpus",
            "current corpus with 4207 owner chain but retained EM defect gates",
            "BOUND_ROUTE_ONLY",
            "Poynting double-count channel is forbidden conditionally, but same-Hodge/current/Ward/no-flux signatures are not all parent-closed",
            "use explicit R_EM_Poynting bound rows",
        ),
        (
            "RUN4312_1_safe_EM",
            "single Hodge owner, fixed charge/current, Ward exchange, no extra XF2, no radiative collar flux",
            "ALLOW_R_EM_ZERO_CONDITIONAL",
            "EM/Poynting does not contribute an extra collar bulk source",
            "then S_U can drop R_EM_Poynting before lambda scoring",
        ),
        (
            "RUN4312_2_radiative_flux",
            "net Poynting flux through collar survives",
            "ROUTE_TO_BOUNDARY",
            "radiation is a boundary/Hamiltonian flux, not a static hidden source",
            "feed Phi_rad into N_boundary or an explicit source row",
        ),
        (
            "RUN4312_3_side_channel",
            "Hodge/current/XF2/Ward defects survive",
            "KEEP_EM_RESIDUAL",
            "defects enter Eta_H and S_U, weakening lambda positivity and local precision",
            "source or derive each defect bound",
        ),
        (
            "RUN4312_4_local_claim",
            "claim local GR/Newton/R10/PPN after EM split",
            "REJECT",
            "lambda components, non-EM residuals, R_eq, I_commutator and projection gates remain open",
            "continue derivation chain",
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


def lambda_status_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "LS4312_0_Zmin",
            "Z_min",
            "unchanged",
            "still requires parent kinetic sign/normalization",
            "not affected by EM cancellation except through shared normalization",
        ),
        (
            "LS4312_1_M2min",
            "M2_min",
            "unchanged",
            "still requires parent potential/Hessian signature",
            "mass-only branch remains possible but unsourced",
        ),
        (
            "LS4312_2_lambda1",
            "lambda_1(D_loc)",
            "unchanged",
            "still requires collar domain/zero-mode selector",
            "no EM shortcut to domain spectrum",
        ),
        (
            "LS4312_3_EtaH",
            "Eta_H",
            "updated",
            "EM/Poynting defects now enter Eta_H as named terms instead of a black box",
            "this is the real gain of 4312",
        ),
        (
            "LS4312_4_lambda_star",
            "lambda_*",
            "guarded",
            "lambda_* = Z_min lambda_1(D_loc)+M2_min-Eta_H remains unscored",
            "positive margin improves if EM defects cancel or are small",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for status_id, symbol, status, requirement, implication in specs:
        row = base_row()
        row.update(
            {
                "status_id": status_id,
                "symbol": symbol,
                "status": status,
                "requirement": requirement,
                "implication": implication,
            }
        )
        return_rows = rows
        return_rows.append(row)
    return rows


def decision_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "DEC4312_0_poynting",
            "POYNTING_IS_REAL_BUT_NOT_SECOND_SOURCE",
            "In the same-Hodge Hilbert branch, Poynting is the EM energy-flux component of T_EM already counted in T_total.",
            "set c_Poynt_extra=0 if the single source functional is parent-signed",
        ),
        (
            "DEC4312_1_residual",
            "EM_DEFECTS_ARE_NOW_NAMED",
            "Hodge mismatch, source weight, XF2, current normalization, radiative flux and Ward mismatch are the only EM/Poynting residual channels retained here.",
            "source or cancel these rows instead of revisiting vague coupling",
        ),
        (
            "DEC4312_2_eta",
            "ETAH_BLACK_BOX_SHRINKS",
            "EM/Poynting no longer sits as an undefined correction; it enters Eta_H/S_U through explicit rows.",
            "positive lambda margin can improve if these rows vanish or are bounded small",
        ),
        (
            "DEC4312_3_claim",
            "NO_LOCAL_GR_CLAIM",
            "This is a source-coupling derivation step, not a completed local-GR/Newton reduction.",
            "keep all arena claims blocked",
        ),
        (
            "DEC4312_4_next",
            "WARD_CURRENT_NORMALIZATION_NEXT",
            "The least handwavy next target is to close the shared current/charge/Ward exchange row or assign a collar bound value.",
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
        "Do not add Poynting as a standalone source after T_EM is already included in T_total.",
        "Do not erase radiation; nonzero Poynting flux must route to N_boundary/Hamiltonian flux.",
        "Do not claim EM cancellation unless same Hodge owner, current normalization and Ward exchange are signed.",
        "Do not hide X F^2 or current/charge drift inside Eta_H without a named bound row.",
        "Do not score local GR/Newton/R10/PPN from the EM split alone.",
    ]
    rows: List[Dict[str, str]] = []
    for index, rule in enumerate(rules):
        row = base_row()
        row.update({"firewall_id": f"FW4312_{index}", "rule": rule, "status": "ACTIVE"})
        rows.append(row)
    return rows


def status_rows() -> List[Dict[str, str]]:
    specs = [
        ("STAT4312_0_poynting", "Poynting", "OWNER_LOCKED_CONDITIONAL", "real EM flow, not an extra bulk source on safe branch"),
        ("STAT4312_1_extra_source", "c_Poynt_extra", "ZERO_IF_SINGLE_OWNER_SIGNED", "forbidden double-count channel"),
        ("STAT4312_2_R_EM", "R_EM_Poynting", "ZERO_OR_BOUND", "zero only if all EM defect clauses vanish"),
        ("STAT4312_3_EtaH", "Eta_H", "MORE_EXPLICIT", "EM correction is decomposed into named defect rows"),
        ("STAT4312_4_lambda", "lambda_*", "STILL_UNSCORED", "Z_min/M2_min/lambda_1/Eta_H values still missing"),
        ("STAT4312_5_local", "local GR/Newton", "BLOCKED", "source coupling improved but not complete"),
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
            "next_target_id": "NT4312_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can the shared EM current/charge/Ward exchange be parent-signed, or must its collar residual be bounded numerically?",
            "preferred_route": "derive shared current normalization and Ward exchange cancellation from one matter+EM action",
            "fallback_route": "fill nonclaim bounds for C_JQ, Delta_internal_exchange and Delta_rad_Poynting",
        }
    )
    return [row]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    formal_text = f"""# 328 PPC4161 Zmin M2min EtaH source or Poynting residual cancellation

Marker: `{MARKER}`

## Decision

`{DECISION}`

4312 attacks the Poynting fork directly. The safe branch is not "Poynting does not matter"; it is:

```text
Poynting flow is real EM energy flow,
but on the single Maxwell-Hodge Hilbert-owner branch it is already inside T_EM.
```

Therefore:

```text
M_trial = M_H[J_H_total] + c_Poynt_extra int_boundary S_Poynting dot n dA
single Hilbert source owner => c_Poynt_extra = 0.
```

The EM/Poynting collar residual is not erased. It is:

```text
R_EM_Poynting <= C_H dH ||F||^2
              + C_w |dw| ||T_EM||
              + |C_XF2| ||F||^2
              + |C_JQ| ||J dot A||
              + |Phi_rad|
              + |Delta_ex|.
```

So:

```text
R_EM_Poynting = 0
```

only if same-Hodge ownership, no extra XF2/current drift, Ward exchange, no through-collar radiative flux, and the once-only Poynting coefficient are all signed.

## EM Cancellation Theorem

{md_table(tables["em_cancellation"], ["theorem_id", "clause", "statement", "result", "status"])}

## Residual Defect Ledger

{md_table(tables["defects"], ["defect_id", "symbol", "failure_condition", "bound_contribution", "feeds", "next_action"])}

## Bound Update

{md_table(tables["bounds"], ["bound_id", "symbol", "law", "role", "status"])}

## Lambda Status

{md_table(tables["lambda_status"], ["status_id", "symbol", "status", "requirement", "implication"])}

## Runner

{md_table(tables["runner"], ["runner_id", "case", "result", "reason"])}

## Result

This is progress on calibrated source coupling: EM/Poynting is either cancelled by a once-only Hilbert owner theorem, or retained as named contributions to `Eta_H` and `S_U`. No local test claim fires from this checkpoint.

Next target: `{NEXT_TARGET}`.
"""
    doc_text = f"""# 4312 - Zmin/M2min/EtaH source or Poynting residual cancellation

## Verdict
- Derived the Poynting once-only cancellation condition: same Maxwell-Hodge Hilbert owner implies `c_Poynt_extra=0`.
- Kept physical Poynting/radiation alive as boundary flux or named residual, not as hidden background force.
- Replaced the EM part of `Eta_H` with six named defect channels: `Delta_Hodge_EM`, `delta_w_EM`, `C_XF2`, `C_JQ`, `Delta_rad_Poynting`, and `Delta_internal_exchange`.
- Updated the collar numerator path: `S_U` now has an auditable `R_EM_Poynting` term.
- No local-GR/Newton/R10/PPN claim fires.

## Source Register
{md_table(tables["sources"], ["source_id", "source_path", "exists", "needle_found", "purpose"])}

## EM Cancellation Theorem
{md_table(tables["em_cancellation"], ["theorem_id", "clause", "statement", "result", "status", "implication"])}

## Residual Defect Ledger
{md_table(tables["defects"], ["defect_id", "symbol", "failure_condition", "bound_contribution", "feeds", "status", "next_action"])}

## Bound Update
{md_table(tables["bounds"], ["bound_id", "symbol", "law", "role", "status"])}

## Lambda Status
{md_table(tables["lambda_status"], ["status_id", "symbol", "status", "requirement", "implication"])}

## Runner
{md_table(tables["runner"], ["runner_id", "case", "result", "reason", "next_action"])}

## Claim Firewall
{md_table(tables["firewall"], ["firewall_id", "rule", "status"])}

## Decision
{md_table(tables["decision"], ["decision_id", "result", "reason", "next_action"])}

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

    add("VAL4312_0_sources_exist", "all cited local source paths exist", all(Path(row["source_path"]).exists() for row in tables["sources"]), "source_register")
    add("VAL4312_1_needles_found", "all cited source needles found", all(row["needle_found"] == "True" for row in tables["sources"]), "source_register")
    add("VAL4312_2_once_only", "once-only Poynting coefficient clause exists", any(row["theorem_id"] == "EC4312_2_once_only" for row in tables["em_cancellation"]), "em_cancellation")
    add("VAL4312_3_zero_theorem", "R_EM_Poynting zero theorem exists but is conditional", any(row["theorem_id"] == "EC4312_5_zero_theorem" and row["status"] == "EXACT_ZERO_IF_ALL_CLAUSES_SIGNED" for row in tables["em_cancellation"]), "em_cancellation")
    add("VAL4312_4_defect_rows", "six physical EM defects plus c_Poynt_extra are ledgered", len(tables["defects"]) == 7, "defects")
    add("VAL4312_5_bound_formula", "R_EM_Poynting bound formula exists", any(row["bound_id"] == "RB4312_0_R_EM_bound" for row in tables["bounds"]), "bounds")
    add("VAL4312_6_eta_updated", "Eta_H update row exists", any(row["bound_id"] == "RB4312_2_EtaH_update" for row in tables["bounds"]), "bounds")
    add("VAL4312_7_runner_rejects_claim", "runner rejects local claim from EM split alone", any(row["runner_id"] == "RUN4312_4_local_claim" and row["result"] == "REJECT" for row in tables["runner"]), "runner")
    add("VAL4312_8_next_selected", f"next target is {NEXT_TARGET}", tables["next"][0]["next_target"] == NEXT_TARGET, "next")
    add(
        "VAL4312_9_claim_flags_false",
        "all generated rows keep claim flags false",
        all(row.get("claim_allowed") == "False" and row.get("valid_for_claim") == "False" for table in tables.values() for row in table),
        "generated_tables",
    )
    for name, path in paths.items():
        if name == "validation":
            continue
        ok, detail = validate_csv(path)
        add(f"VAL4312_csv_{name}", detail, ok, "generated_artifacts")
    add("VAL4312_docs", "formal and post checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "generated_docs")
    add("VAL4312_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims_register")
    add("VAL4312_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "unification_spine")
    add("VAL4312_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "private_packet")
    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4312_SOURCE_REGISTER.csv",
        "em_cancellation": SOURCE_DIR / "P8_Y5_R2FR_4312_EM_POYNTING_CANCELLATION_THEOREM.csv",
        "defects": SOURCE_DIR / "P8_Y5_R2FR_4312_EM_DEFECT_LEDGER.csv",
        "bounds": SOURCE_DIR / "P8_Y5_R2FR_4312_COLLAR_EM_RESIDUAL_BOUND.csv",
        "lambda_status": SOURCE_DIR / "P8_Y5_R2FR_4312_LAMBDA_STATUS_UPDATE.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4312_LOCAL_ROUTE_RUNNER.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4312_CLAIM_FIREWALL.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4312_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4312_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4312_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = {
        "sources": source_rows(),
        "em_cancellation": em_cancellation_rows(),
        "defects": residual_defect_rows(),
        "bounds": residual_bound_rows(),
        "lambda_status": lambda_status_rows(),
        "runner": runner_rows(),
        "firewall": firewall_rows(),
        "decision": decision_rows(),
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
## PPC4161 4312 Zmin/M2min/EtaH source or Poynting residual cancellation

Marker: `{MARKER}`

4312 resolves the Poynting fork into a theorem/ledger pair. On the single Maxwell-Hodge Hilbert-owner branch, Poynting is real EM energy flow already inside `T_EM`, so `c_Poynt_extra=0`. If the same-Hodge/current/Ward/no-flux clauses are signed, `R_EM_Poynting=0`; otherwise the residual is bounded by named defects and feeds `Eta_H` and `S_U`. This advances source coupling without claiming local GR/Newton/R10/PPN.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4312 packet EM/Poynting collar residual

Marker: `{PACKET_MARKER}`

Packet update: EM/Poynting is no longer a vague correction bucket. Either the single Hilbert owner theorem cancels the extra source channel, or the residual is scored through `Delta_Hodge_EM`, `delta_w_EM`, `C_XF2`, `C_JQ`, `Delta_rad_Poynting` and `Delta_internal_exchange`.
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
