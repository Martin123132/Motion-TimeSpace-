from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3240"
DOC = ROOT / "3240-Y5-R2FR-PWEP-EH-chain-rollforward-and-current-derivation-frontier-under-AX1090.md"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3240_SOURCE_REGISTER.csv",
    "chain": OUT / "P8_Y5_R2FR_3240_CHAIN_ROLLFORWARD.csv",
    "theorem": OUT / "P8_Y5_R2FR_3240_CONDITIONAL_LOCAL_GR_THEOREM.csv",
    "decision": OUT / "P8_Y5_R2FR_3240_CURRENT_FRONTIER_DECISION.csv",
    "next": OUT / "P8_Y5_R2FR_3240_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_R2FR_3240_VALIDATION.csv",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


RUN_UTC = now()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_ok(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        read_csv(path)
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_ok(path) if path.suffix.lower() == ".csv" else True


def evidence(path: Path, needles: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    hay_needles = [needle.lower() for needle in needles]
    hits: list[str] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        haystack = line.lower()
        if any(needle in haystack for needle in hay_needles):
            snippet = " ".join(line.strip().split())[:240]
            hits.append(f"L{line_number}:{snippet}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_MATCH"


def under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def md_escape(value: Any) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


SOURCES = [
    {
        "source_id": "SRC3240_00_3239_doc",
        "path": ROOT / "3239-Y5-R2FR-DeltaK-component-birth-certificate-or-qLoc-arena-bound-under-AX1090.md",
        "role": "latest chain target says P_WEP response operator is the next frontier",
        "needles": ["CURRENT_FRONTIER_IS_PWEP_RESPONSE_OPERATOR", "P_WEP response operator", "3083-Y5-R2FR"],
    },
    {
        "source_id": "SRC3240_01_3083_doc",
        "path": ROOT / "3083-Y5-R2FR-PWEP-response-operator-from-matter-functor-or-component-bound-under-AX1090.md",
        "role": "existing P_WEP response-operator theorem attempt",
        "needles": ["P_WEP = 0", "PWEP_NOT_DERIVED_CURRENT_CORPUS", "3084-Y5-R2FR"],
    },
    {
        "source_id": "SRC3240_02_3084_doc",
        "path": ROOT / "3084-Y5-R2FR-ordinary-matter-action-signature-source-label-forgetting-or-WEP-bound-first-fill-under-AX1090.md",
        "role": "ordinary matter descent/source-label forgetting attempt",
        "needles": ["ORDINARY_MATTER_SIGNATURE_NOT_PARENT_SIGNED", "SOURCE_SHADOW_BAN_OR_TAUWEP", "3085-Y5-R2FR"],
    },
    {
        "source_id": "SRC3240_03_3085_doc",
        "path": ROOT / "3085-Y5-R2FR-source-shadow-ban-or-tauWEP-direct-product-first-source-row-under-AX1090.md",
        "role": "source-shadow branch narrows WEP and hands off to EH left-hand operator",
        "needles": ["left-hand operator", "EH_DOMINANCE_AND_OPERATOR_RESIDUAL_SILENCE_NEXT", "3086-Y5-R2FR"],
    },
    {
        "source_id": "SRC3240_04_3086_doc",
        "path": ROOT / "3086-Y5-R2FR-EH-dominance-and-residual-sector-silence-or-operator-coefficient-pack-under-AX1090.md",
        "role": "EH dominance attempt and residual operator pack",
        "needles": ["E_LHS = G_munu", "SECTOR_ACTION_VARIATION_AND_LOCAL_SCALING_SILENCE_IS_NEXT", "DeltaE_munu"],
    },
    {
        "source_id": "SRC3240_05_3087_doc",
        "path": ROOT / "3087-Y5-R2FR-sector-action-variation-and-local-scaling-silence-or-operator-bounds-under-AX1090.md",
        "role": "sector variation reduces left-hand problem to source-charge owner",
        "needles": ["source-charge owner", "M_H_ref", "3088-Y5-R2FR"],
    },
    {
        "source_id": "SRC3240_06_3088_doc",
        "path": ROOT / "3088-Y5-R2FR-sector-Lagrangian-boundary-owner-or-FB5540-source-row-under-AX1090.md",
        "role": "parent action/source-charge contract",
        "needles": ["PARENT_ACTION_CONTRACT_WRITTEN_NOT_CLOSED", "M_H_ref", "3089-Y5-R2FR"],
    },
    {
        "source_id": "SRC3240_07_3089_doc",
        "path": ROOT / "3089-Y5-R2FR-boundary-exactness-projector-orthogonality-or-FB5540-source-pack-under-AX1090.md",
        "role": "boundary/projector route gives weighted-Stokes bound law rather than zero",
        "needles": ["WEIGHTED_STOKES_IS_THE_CORRECT_LOCAL_BOUND_LAW", "Q_edge", "3090-Y5-R2FR"],
    },
    {
        "source_id": "SRC3240_08_3090_doc",
        "path": ROOT / "3090-Y5-R2FR-BX-primitive-from-parent-variation-or-edge-bound-term-under-AX1090.md",
        "role": "B_X primitive attempt splits vertical quotient, scalar no-hair and edge-bound routes",
        "needles": ["B_X is still not derivable", "VERTICAL_QUOTIENT_CONSTRUCTION", "EDGEBOUND"],
    },
    {
        "source_id": "SRC3240_09_3104_doc",
        "path": ROOT / "3104-Y5-R2FR-left-hand-EH-Newton-reduction-under-quotient-matter-domain.md",
        "role": "constructive public-geometry EH/Newton branch",
        "needles": ["G_munu[g_pub]", "nabla^2 Phi = 4 pi G", "Right-hand/source problem"],
    },
    {
        "source_id": "SRC3240_10_3237_doc",
        "path": ROOT / "3237-Y5-R2FR-geometric-Euler-same-branch-source-zero-or-bound-for-Jperp-under-AX1090.md",
        "role": "geometric Euler/Ward route and q_loc residual envelope",
        "needles": ["q_loc^nu=0", "GEOMETRIC_EULER_ZERO_ROUTE_DERIVED_AS_CONDITIONAL", "J_geom_bound"],
    },
    {
        "source_id": "SRC3240_11_3238_doc",
        "path": ROOT / "3238-Y5-R2FR-SGK-metric-response-Helmholtz-gap-or-qLoc-bound-for-local-GR-under-AX1090.md",
        "role": "SGK metric-response and Helmholtz gap",
        "needles": ["WEAK_SGK_TEMPLATE_EXISTS", "Delta_K", "H_GK"],
    },
]


def source_register() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["path"]
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source["source_id"],
                "source_path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": source["role"],
                "evidence_hits": evidence(path, source["needles"]),
                "valid_for_claim": "false",
                "generated_utc": RUN_UTC,
            }
        )
    return rows


def chain_rows() -> list[dict[str, Any]]:
    return [
        {
            "chain_id": "CH3240_0_latest_handoff",
            "checkpoint": "3239",
            "result": "latest artifact names P_WEP response operator as next frontier",
            "rollforward_status": "STALE_IF_TAKEN_LITERAL",
            "reason_not_to_repeat": "3083 already attempted P_WEP from matter functor and staged component-bound rows",
            "current_use": "treat as pointer into existing 3083-3085 source-side chain",
            "valid_for_claim": "false",
        },
        {
            "chain_id": "CH3240_1_PWEP",
            "checkpoint": "3083",
            "result": "conditional P_WEP=0 theorem shape is clean under universal observed-matter descent",
            "rollforward_status": "DONE_CONDITIONAL_NOT_PARENT_SIGNED",
            "reason_not_to_repeat": "premises are one ordinary matter functor, one observed geometry, no source-only selectors and no shadow frame",
            "current_use": "source-side WEP route is narrowed, not closed",
            "valid_for_claim": "false",
        },
        {
            "chain_id": "CH3240_2_matter_signature",
            "checkpoint": "3084",
            "result": "ordinary matter action signature and source-label forgetting are exact contracts but unsigned",
            "rollforward_status": "DONE_NONCLAIM",
            "reason_not_to_repeat": "failure mode moved to source-shadow/readout label re-entry and tau/direct product",
            "current_use": "keep WEP source rows nonclaim",
            "valid_for_claim": "false",
        },
        {
            "chain_id": "CH3240_3_source_shadow",
            "checkpoint": "3085",
            "result": "source-shadow is classified but not zeroed; WEP sidecar rows acquisition-ready",
            "rollforward_status": "HANDOFF_TO_EH_LEFT_HAND",
            "reason_not_to_repeat": "source-side narrowing alone cannot deliver GR/Newton recovery",
            "current_use": "left-hand EH operator and source normalization become primary",
            "valid_for_claim": "false",
        },
        {
            "chain_id": "CH3240_4_EH_dominance",
            "checkpoint": "3086",
            "result": "E_LHS = G + Lambda g + DeltaE is the correct local-GR bridge form",
            "rollforward_status": "RESIDUAL_OPERATOR_PACK_RETAINED",
            "reason_not_to_repeat": "DeltaE sectors were enumerated: higher derivative, projector, boundary, nonminimal, memory/coframe, source normalization",
            "current_use": "derive/silence/suppress residual sectors or keep coefficient pack",
            "valid_for_claim": "false",
        },
        {
            "chain_id": "CH3240_5_sector_variation",
            "checkpoint": "3087",
            "result": "no non-EH sector fully silenced; root blocker becomes L_X/Theta_X/Q_X and same-frame M_H_ref",
            "rollforward_status": "SOURCE_CHARGE_OWNER_FRONTIER",
            "reason_not_to_repeat": "broad DeltaE language has already been reduced to source-charge owner and coefficient rows",
            "current_use": "need parent-owned source charge or bound pack",
            "valid_for_claim": "false",
        },
        {
            "chain_id": "CH3240_6_parent_contract",
            "checkpoint": "3088",
            "result": "exact parent contract written for L_X, Theta_X, Q_X, boundary/reference, tau lock and M_H_ref",
            "rollforward_status": "CONTRACT_WRITTEN_NOT_CLOSED",
            "reason_not_to_repeat": "the clauses are explicit; repeating them is not progress",
            "current_use": "test zero routes or fill full no-cancellation source pack",
            "valid_for_claim": "false",
        },
        {
            "chain_id": "CH3240_7_boundary_projector",
            "checkpoint": "3089",
            "result": "boundary/projector zero not proven, but weighted-Stokes edge bound law is derived",
            "rollforward_status": "BOUND_LAW_READY_VALUES_MISSING",
            "reason_not_to_repeat": "exactness words alone cannot zero edge charge if kernel derivative, harmonic, residual or corner terms survive",
            "current_use": "edge/source leakage must be theorem-zero or bounded termwise",
            "valid_for_claim": "false",
        },
        {
            "chain_id": "CH3240_8_BX_primitive",
            "checkpoint": "3090",
            "result": "B_X primitive not derived; branch split installed: vertical quotient first, scalar no-hair second, edge-bound third",
            "rollforward_status": "ROUTE_SPLIT_READY",
            "reason_not_to_repeat": "do not mix scalar no-hair with Noether edge exactness",
            "current_use": "least-scrutiny path is vertical/public quotient before variation",
            "valid_for_claim": "false",
        },
        {
            "chain_id": "CH3240_9_constructive_EH_branch",
            "checkpoint": "3104",
            "result": "quotient-matter/public-geometry branch gives a constructive EH plus residual tensor reduction and Newton/Poisson limit condition",
            "rollforward_status": "MOST_CONSTRUCTIVE_LOCAL_GR_LADDER_RUNG",
            "reason_not_to_repeat": "this is the branch to unify with q_loc/SGK rather than restarting WEP",
            "current_use": "try to parent-adopt public EH principal operator and identify E_res with q_loc/J_geom residuals",
            "valid_for_claim": "false",
        },
        {
            "chain_id": "CH3240_10_geometric_Euler",
            "checkpoint": "3237",
            "result": "same-branch Euler/Ward zero route derived conditionally; J_geom no-cancellation residual envelope written",
            "rollforward_status": "CONDITIONAL_QLOC_GATE",
            "reason_not_to_repeat": "bulk Euler zero still needs SGK action, metric response, Helmholtz, double-zero, projector and boundary clauses together",
            "current_use": "connect constructive EH branch to SGK metric-response gate",
            "valid_for_claim": "false",
        },
        {
            "chain_id": "CH3240_11_SGK_metric_response",
            "checkpoint": "3238",
            "result": "weak A-template can generate q-current, but live Gamma_eff/Khat metric-response and Helmholtz adoption fail",
            "rollforward_status": "CURRENT_HARD_GATE",
            "reason_not_to_repeat": "another P_WEP pass will not close Delta_K/H_GK/q_loc",
            "current_use": "next attempt must unify EH public action, Gamma_eff density, Khat metric response, and residual tensor bookkeeping",
            "valid_for_claim": "false",
        },
    ]


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "TH3240_0_public_geometry",
            "claim_piece": "observed quotient geometry has one public metric and Levi-Civita local connection",
            "mathematical_form": "q: Phi_parent -> Q_obs; g_pub=g[q(Phi)]; connection_pub=LC(g_pub)",
            "why_it_matters": "prevents source-side coupling and hidden matter frame from carrying the local-GR failure",
            "current_status": "CONSTRUCTIVE_BRANCH_EXISTS_NOT_PARENT_FINAL",
            "proof_source": "3104 plus 3102/3103 branch",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "TH3240_1_EH_principal",
            "claim_piece": "left-hand principal operator is Einstein-Hilbert plus explicit residual tensor",
            "mathematical_form": "G_munu[g_pub]+Lambda_* g_munu+E_res_munu=kappa_* T_total_munu",
            "why_it_matters": "this is the direct GR bridge; all deviations are forced into E_res rather than hidden in coupling language",
            "current_status": "CONDITIONAL_CLEAN_REDUCTION",
            "proof_source": "3104",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "TH3240_2_Newton_limit",
            "claim_piece": "Newton/Poisson follows from EH principal operator plus source calibration",
            "mathematical_form": "nabla^2 Phi=4*pi*G_* rho + R_Eres + R_Lambda + R_boundary",
            "why_it_matters": "shows where Newton's constant enters: kappa_* sets G_*; measured orbital GM still needs Hamiltonian/worldtube calibration",
            "current_status": "ALGEBRAICALLY_REACHABLE_CONDITIONAL",
            "proof_source": "3104",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "TH3240_3_qLoc_Ward",
            "claim_piece": "q_loc zero follows only if Gamma_eff/Khat are the same variational metric-response object",
            "mathematical_form": "q_loc=P_loc[(nabla Gamma_eff-div K_metric)-div Delta_K]+boundary/projector",
            "why_it_matters": "ties the local force residual to Delta_K and Helmholtz, not to a plateau axiom",
            "current_status": "WARD_SPLIT_DERIVED_STRONG_ADOPTION_FAILS",
            "proof_source": "3237 and 3238",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "TH3240_4_unified_gate",
            "claim_piece": "local GR branch closes only if public EH residual and SGK/q_loc residual are the same controlled object",
            "mathematical_form": "E_res_munu == E_GK_munu + E_boundary/projector with Delta_K=0 or bounded and H_GK=0 or bounded",
            "why_it_matters": "prevents a split-brain proof where EH looks clean but q_loc still carries an independent force source",
            "current_status": "NEW_CURRENT_DERIVATION_TARGET",
            "proof_source": "3240 roll-forward synthesis",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3240_0_no_PWEP_restart",
            "decision": "DO_NOT_START_3240_AS_PWEP_FROM_SCRATCH",
            "because": "3239's P_WEP target is real, but 3083-3085 already pursued that branch and handed it off to EH dominance",
            "physics_impact": "saves tokens and keeps the derivation ladder intact",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3240_1_constructive_branch",
            "decision": "USE_3104_AS_THE_CONSTRUCTIVE_LOCAL_GR_SPINE",
            "because": "3104 already gives the cleanest local equation: EH principal operator plus E_res and Newton/Poisson with residual/source-calibration clauses",
            "physics_impact": "the project is not just blocked; it has a viable conditional local-GR spine to harden",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3240_2_hard_gate",
            "decision": "UNIFY_EH_RESIDUAL_WITH_SGK_QLOC_RESIDUAL_NEXT",
            "because": "3237-3238 show q_loc remains live unless Gamma_eff/Khat are parent metric-response objects with Helmholtz integrability",
            "physics_impact": "the next derivation target is a single parent-action normal form, not more source-side bookkeeping",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3240_3_bound_fallback",
            "decision": "IF_UNIFICATION_FAILS_KEEP_TERMWISE_RESIDUAL_BOUNDS",
            "because": "3089-3090 provide weighted-Stokes and route-split bound language that can make failures testable rather than vague",
            "physics_impact": "local GR is not claimed, but the empirical PPN/R10/clock/orbit branch stays disciplined",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3240_0_3241",
            "next_checkpoint": "3241-Y5-R2FR-public-EH-and-SGK-metric-response-unification-or-residual-vector-under-AX1090.md",
            "mission": "attempt one minimal parent local action normal form that makes the 3104 public EH branch and the 3238 Gamma_eff/Khat/q_loc metric-response branch the same object; otherwise produce a single no-cancellation residual vector",
            "starting_equation": "S_local=(1/(2*kappa_*))*int sqrt(-g_pub)(R-2Lambda_*) + S_matter[g_pub] + S_GK_or_silent + S_res; require E_res_munu and q_loc/Delta_K/H_GK to be identified, zeroed, or bounded termwise",
            "success_if": "Gamma_eff is a parent scalar density, Khat=K_metric[Gamma_eff], H_GK=0 up to signed boundary/gauge terms, and E_res_munu maps onto the same residual vector used for PPN/R10/clock/orbit bounds",
            "failure_if": "EH public branch and q_loc/SGK branch remain independent closure assumptions or require separate fitted residuals",
            "claim_policy": "no local-GR/Newton/PPN/R10/clock/orbit claim until the unified gate is theorem-signed or every residual term is source-backed and below arena bounds",
            "valid_for_claim": "false",
        },
        {
            "next_id": "NEXT3240_1_secondary",
            "next_checkpoint": "source-charge/M_H_ref denominator extraction after unified residual vector",
            "mission": "once residual objects are unified, derive or bound the Hamiltonian/worldtube source charge that calibrates G_* M to measured GM without borrowing orbital fits",
            "starting_equation": "G_*:=kappa_* c^4/(8*pi); require M_H_ref and DeltaGM residual rows",
            "success_if": "same-frame M_H_ref is parent-owned and positive before readout",
            "failure_if": "measured GM remains a calibration input rather than a derived or explicitly bounded transfer",
            "claim_policy": "Newton-looking Poisson equation is not a measured-Newton claim until this closes",
            "valid_for_claim": "false",
        },
    ]


def validation_rows(source_rows: list[dict[str, Any]], generated_csvs: list[Path]) -> list[dict[str, Any]]:
    no_missing_sources = all(row["exists"] == "true" and row["parse_ok"] == "true" for row in source_rows)
    no_no_match = all("MISSING_SOURCE" not in row["evidence_hits"] and "NO_MATCH" not in row["evidence_hits"] for row in source_rows)
    outputs_under_pcw = all(under(path, ROOT) for path in [DOC, *generated_csvs])
    no_fw_outputs = all(not under(path, FW) for path in [DOC, *generated_csvs])
    csvs_parse = all(csv_ok(path) for path in generated_csvs)
    claim_rows_true = 0
    for path in generated_csvs:
        for row in read_csv(path):
            for key in ("valid_for_claim", "claim_allowed", "bridge_claim", "claim_active"):
                if str(row.get(key, "")).strip().lower() == "true":
                    claim_rows_true += 1
    pycache_absent = not PYCACHE.exists()
    rows = [
        {
            "validation_id": "VAL3240_00_sources_exist_parse",
            "passed": bool_str(no_missing_sources),
            "requirement": "all cited source paths exist and parse",
            "evidence": str(OUTPUTS["sources"]),
        },
        {
            "validation_id": "VAL3240_01_evidence_hits",
            "passed": bool_str(no_no_match),
            "requirement": "source register has direct evidence hits, not vibes",
            "evidence": str(OUTPUTS["sources"]),
        },
        {
            "validation_id": "VAL3240_02_chain_rolls_forward",
            "passed": bool_str(any(row["checkpoint"] == "3083" for row in read_csv(OUTPUTS["chain"])) and any(row["checkpoint"] == "3238" for row in read_csv(OUTPUTS["chain"]))),
            "requirement": "chain covers P_WEP route and current SGK/qLoc frontier",
            "evidence": str(OUTPUTS["chain"]),
        },
        {
            "validation_id": "VAL3240_03_no_PWEP_restart",
            "passed": bool_str(any(row["decision"] == "DO_NOT_START_3240_AS_PWEP_FROM_SCRATCH" for row in read_csv(OUTPUTS["decision"]))),
            "requirement": "explicitly avoids restarting the already-audited P_WEP branch",
            "evidence": str(OUTPUTS["decision"]),
        },
        {
            "validation_id": "VAL3240_04_constructive_spine_selected",
            "passed": bool_str(any(row["checkpoint"] == "3104" and "CONSTRUCTIVE" in row["rollforward_status"] for row in read_csv(OUTPUTS["chain"]))),
            "requirement": "selects 3104 public EH/Newton branch as constructive local-GR spine",
            "evidence": str(OUTPUTS["chain"]),
        },
        {
            "validation_id": "VAL3240_05_unified_next_target",
            "passed": bool_str(any("public-EH-and-SGK" in row["next_checkpoint"] for row in read_csv(OUTPUTS["next"]))),
            "requirement": "next target is the EH/SGK unification gate, not another missing-ledger loop",
            "evidence": str(OUTPUTS["next"]),
        },
        {
            "validation_id": "VAL3240_06_claims_blocked",
            "passed": bool_str(claim_rows_true == 0),
            "requirement": "no local-GR/Newton/PPN/R10/clock/orbit claim is promoted",
            "evidence": f"claim_rows_true={claim_rows_true}",
        },
        {
            "validation_id": "VAL3240_07_csv_parse",
            "passed": bool_str(csvs_parse),
            "requirement": "all generated CSV files parse cleanly",
            "evidence": ";".join(str(path) for path in generated_csvs),
        },
        {
            "validation_id": "VAL3240_08_outputs_under_post_checkpoint",
            "passed": bool_str(outputs_under_pcw),
            "requirement": "all outputs stay inside post-checkpoint-work",
            "evidence": str(ROOT),
        },
        {
            "validation_id": "VAL3240_09_no_formalization_outputs",
            "passed": bool_str(no_fw_outputs),
            "requirement": "formalization-workbench is not modified by this checkpoint",
            "evidence": str(FW),
        },
        {
            "validation_id": "VAL3240_10_pycache_absent",
            "passed": bool_str(pycache_absent),
            "requirement": "scripts __pycache__ removed",
            "evidence": str(PYCACHE),
        },
        {
            "validation_id": "VAL3240_11_doc_written",
            "passed": bool_str(DOC.exists()),
            "requirement": "checkpoint markdown document written",
            "evidence": str(DOC),
        },
    ]
    return rows


def build_doc(
    source_rows: list[dict[str, Any]],
    chain: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 3240 - P_WEP/EH Chain Rollforward and Current Derivation Frontier under AX1090",
            "Private checkpoint. This is not a local-GR, Newton, PPN, R10, WEP, clock, orbital, Maxwell, or public claim.",
            "## Result",
            (
                "3240 answers the immediate risk in the current ladder: `3239` says the next target is `P_WEP`, "
                "but that branch already exists in `3083`-`3085`. Repeating it would be a loop, not progress."
            ),
            (
                "The useful roll-forward is: `P_WEP` was conditionally sharpened, ordinary matter/source-shadow was narrowed, "
                "then the chain correctly moved to the left-hand Einstein operator. `3104` is the constructive local-GR spine: "
                "a public quotient metric with an EH principal operator, ordinary Hilbert matter, explicit residual tensor `E_res`, "
                "and a conditional Newton/Poisson limit. The hard remaining gate is to unify that EH residual tensor with the "
                "`3237`/`3238` `Gamma_eff/Khat/q_loc` metric-response residuals."
            ),
            (
                "So the next move is not another source-side WEP pass. It is one parent-action normal-form attempt: make the "
                "public EH branch and the SGK/qLoc branch the same variational object, or write one no-cancellation residual vector "
                "that can feed PPN/R10/clock/orbit tests."
            ),
            "## Chain Rollforward",
            md_table(
                chain,
                [
                    "chain_id",
                    "checkpoint",
                    "result",
                    "rollforward_status",
                    "reason_not_to_repeat",
                    "current_use",
                    "valid_for_claim",
                ],
            ),
            "## Conditional Local-GR Theorem Pieces",
            md_table(
                theorem,
                [
                    "theorem_id",
                    "claim_piece",
                    "mathematical_form",
                    "why_it_matters",
                    "current_status",
                    "proof_source",
                    "valid_for_claim",
                ],
            ),
            "## Decision",
            md_table(
                decisions,
                ["decision_id", "decision", "because", "physics_impact", "valid_for_claim"],
            ),
            "## Next Target",
            md_table(
                next_target,
                [
                    "next_id",
                    "next_checkpoint",
                    "mission",
                    "starting_equation",
                    "success_if",
                    "failure_if",
                    "claim_policy",
                    "valid_for_claim",
                ],
            ),
            "## Source Register",
            md_table(
                source_rows,
                ["source_id", "source_path", "exists", "parse_ok", "role", "evidence_hits", "valid_for_claim"],
            ),
            "## Validation",
            md_table(validation, ["validation_id", "passed", "requirement", "evidence"]),
            "## Generated Evidence",
            "\n".join(f"- `{path}`" for path in OUTPUTS.values()),
        ]
    )


def main() -> None:
    for path in OUTPUTS.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    DOC.parent.mkdir(parents=True, exist_ok=True)

    source_rows = source_register()
    chain = chain_rows()
    theorem = theorem_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["chain"], chain)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)

    generated_csvs = [
        OUTPUTS["sources"],
        OUTPUTS["chain"],
        OUTPUTS["theorem"],
        OUTPUTS["decision"],
        OUTPUTS["next"],
    ]
    validation = validation_rows(source_rows, generated_csvs)
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(
        build_doc(source_rows, chain, theorem, decisions, next_target, validation),
        encoding="utf-8",
    )
    validation = validation_rows(source_rows, generated_csvs)
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(
        build_doc(source_rows, chain, theorem, decisions, next_target, validation),
        encoding="utf-8",
    )

    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)

    failed = [row for row in validation if row["passed"] != "true"]
    if failed:
        raise SystemExit(f"3240 validation failed: {failed}")


if __name__ == "__main__":
    main()
