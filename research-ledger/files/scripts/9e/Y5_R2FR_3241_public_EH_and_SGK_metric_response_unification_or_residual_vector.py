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

CHECKPOINT = "3241"
DOC = ROOT / "3241-Y5-R2FR-public-EH-and-SGK-metric-response-unification-or-residual-vector-under-AX1090.md"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3241_SOURCE_REGISTER.csv",
    "normal_form": OUT / "P8_Y5_R2FR_3241_PARENT_ACTION_NORMAL_FORM_ATTEMPT.csv",
    "identity": OUT / "P8_Y5_R2FR_3241_EH_SGK_IDENTITY_DERIVATION.csv",
    "residuals": OUT / "P8_Y5_R2FR_3241_UNIFIED_RESIDUAL_VECTOR_NONCLAIM.csv",
    "gates": OUT / "P8_Y5_R2FR_3241_LOCAL_GR_GATE_STATUS.csv",
    "decision": OUT / "P8_Y5_R2FR_3241_DECISION.csv",
    "next": OUT / "P8_Y5_R2FR_3241_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_R2FR_3241_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


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
    lowered = [needle.lower() for needle in needles]
    hits: list[str] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        haystack = line.lower()
        if any(needle in haystack for needle in lowered):
            hits.append(f"L{line_number}:{' '.join(line.strip().split())[:240]}")
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
        "source_id": "SRC3241_00_3240_doc",
        "path": ROOT / "3240-Y5-R2FR-PWEP-EH-chain-rollforward-and-current-derivation-frontier-under-AX1090.md",
        "role": "3240 selects EH/SGK residual unification as the live next target",
        "needles": ["UNIFY_EH_RESIDUAL_WITH_SGK_QLOC_RESIDUAL_NEXT", "NEXT3240_0_3241", "3104` is the constructive"],
    },
    {
        "source_id": "SRC3241_01_3102_doc",
        "path": ROOT / "3102-Y5-R2FR-verify-Xhat-verticality-and-matter-descent-under-AX1090.md",
        "role": "quotient-descended ordinary matter rule kills direct Xhat matter coupling conditionally",
        "needles": ["delta_X S_matter", "c_g", "Ordinary matter is a functor"],
    },
    {
        "source_id": "SRC3241_02_3103_doc",
        "path": ROOT / "3103-Y5-R2FR-Xhat-matter-domain-conflict-resolution-under-AX1090.md",
        "role": "parent matter domain rule gives one Hilbert source and no source-only species slot",
        "needles": ["Parent Matter Domain Rule", "T_total", "delta_X S_matter = 0"],
    },
    {
        "source_id": "SRC3241_03_3104_doc",
        "path": ROOT / "3104-Y5-R2FR-left-hand-EH-Newton-reduction-under-quotient-matter-domain.md",
        "role": "constructive public EH plus residual tensor and Newton/Poisson limit",
        "needles": ["E_res_munu", "G_munu[g_pub]", "nabla^2 Phi = 4 pi G_* rho"],
    },
    {
        "source_id": "SRC3241_04_3237_doc",
        "path": ROOT / "3237-Y5-R2FR-geometric-Euler-same-branch-source-zero-or-bound-for-Jperp-under-AX1090.md",
        "role": "Euler/Ward route for q_loc and J_geom residual envelope",
        "needles": ["q_loc^nu=0", "nabla_mu T_GK", "J_geom_bound"],
    },
    {
        "source_id": "SRC3241_05_3238_doc",
        "path": ROOT / "3238-Y5-R2FR-SGK-metric-response-Helmholtz-gap-or-qLoc-bound-for-local-GR-under-AX1090.md",
        "role": "SGK strong metric-response route and Delta_K/H_GK obstruction",
        "needles": ["S_GK = -int", "K_metric", "Delta_K", "H_GK"],
    },
    {
        "source_id": "SRC3241_06_3086_doc",
        "path": ROOT / "3086-Y5-R2FR-EH-dominance-and-residual-sector-silence-or-operator-coefficient-pack-under-AX1090.md",
        "role": "left-hand Einstein operator plus DeltaE residual pack",
        "needles": ["E_LHS = G_munu", "DeltaE_munu", "OPERATOR_COEFFICIENT_PACK"],
    },
    {
        "source_id": "SRC3241_07_3089_doc",
        "path": ROOT / "3089-Y5-R2FR-boundary-exactness-projector-orthogonality-or-FB5540-source-pack-under-AX1090.md",
        "role": "weighted-Stokes boundary residual fallback",
        "needles": ["WEIGHTED_STOKES_IS_THE_CORRECT_LOCAL_BOUND_LAW", "Q_edge", "Qbar_edge_XH"],
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


def normal_form_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NF3241_0_total_action",
            "object": "minimal local parent action normal form",
            "formula": "S_loc=S_EH[g_pub;kappa_*,Lambda_*]+S_matter[Psi,g_pub,theta(q)]+S_GK[g_pub,Phi]+S_other_res+B",
            "derivation_status": "NORMAL_FORM_WRITTEN_CONDITIONAL",
            "must_be_parent_signed": "q-map, public metric, matter descent, Gamma_eff density, boundary/reference convention and residual sector inventory",
            "if_not_signed": "retain separate residual vector; no local-GR/Newton claim",
            "valid_for_claim": "false",
        },
        {
            "row_id": "NF3241_1_EH_block",
            "object": "public Einstein-Hilbert principal operator",
            "formula": "S_EH=(1/(2*kappa_*))*int sqrt(-g_pub)(R[g_pub]-2 Lambda_*)",
            "derivation_status": "CONSTRUCTIVE_BRANCH_FROM_3104",
            "must_be_parent_signed": "public geometry is the only compact-local spin-2 carrier and connection_pub=LC(g_pub)",
            "if_not_signed": "higher-derivative/connection residuals stay in E_res",
            "valid_for_claim": "false",
        },
        {
            "row_id": "NF3241_2_matter_block",
            "object": "quotient ordinary Hilbert matter",
            "formula": "S_matter=sum_A S_A[Psi_A,g_pub,omega[g_pub],theta_A(q,representation_A)]",
            "derivation_status": "CONDITIONAL_EXTENSION_FROM_3102_3103",
            "must_be_parent_signed": "NoSourceOnlySpeciesSlot and no direct Xhat matter/constants/source weights",
            "if_not_signed": "c_g, Delta_w_A and marker/source residuals return",
            "valid_for_claim": "false",
        },
        {
            "row_id": "NF3241_3_SGK_block",
            "object": "Gamma/Khat residual sector as metric-response action",
            "formula": "S_GK=-sigma_GK*int sqrt(-g_pub) Gamma_eff(g_pub,Phi,nablaPhi,D)+B_GK",
            "derivation_status": "FORMAL_ADOPTION_ROUTE_WRITTEN",
            "must_be_parent_signed": "Gamma_eff scalar density, units, branch domain, sign sigma_GK, Khat_live=K_metric[Gamma_eff], Helmholtz symmetry",
            "if_not_signed": "Delta_K and H_GK remain explicit residual components",
            "valid_for_claim": "false",
        },
        {
            "row_id": "NF3241_4_other_residuals",
            "object": "all non-SGK residual sectors",
            "formula": "S_other_res includes higher-derivative, connection, projector, memory/coframe, nonminimal, boundary/source-normalization pieces",
            "derivation_status": "INVENTORY_FROM_3086_RETAINED",
            "must_be_parent_signed": "each sector theorem-zero, topological, source-free no-hair, or source-backed bound row",
            "if_not_signed": "component enters unified no-cancellation residual vector",
            "valid_for_claim": "false",
        },
    ]


def identity_rows() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "ID3241_0_field_equation",
            "identity_piece": "EH plus residual field equation",
            "formula": "G_munu+Lambda_* g_munu+E_res_munu=kappa_* T_total_munu",
            "derived_from": "variation of S_EH+S_matter+S_res in 3104",
            "result": "left-hand deviations are forced into E_res_munu",
            "status": "CONDITIONAL_DERIVED",
            "valid_for_claim": "false",
        },
        {
            "step_id": "ID3241_1_SGK_metric_stress",
            "identity_piece": "SGK Hilbert stress from scalar-density residual sector",
            "formula": "T_GK_munu := sigma_GK*(Gamma_eff g_munu - K_metric_munu[Gamma_eff]) + boundary/improvement convention",
            "derived_from": "S_GK=-sigma_GK int sqrt(-g) Gamma_eff + B_GK",
            "result": "if Khat_live=K_metric then the old Gamma/Khat stress is a Hilbert stress",
            "status": "FORMAL_IDENTITY_CURRENT_ADOPTION_UNSIGNED",
            "valid_for_claim": "false",
        },
        {
            "step_id": "ID3241_2_Eres_GK_map",
            "identity_piece": "move SGK stress to left-hand residual tensor",
            "formula": "E_res_GK_munu := -kappa_* T_GK_munu",
            "derived_from": "G+Lambda g=kappa_*(T_total+T_GK+...) rewritten as G+Lambda g+E_res=kappa_*T_total",
            "result": "the public EH residual and the SGK stress become the same tensor slot",
            "status": "DERIVED_AS_SIGN_CONVENTION_GATE",
            "valid_for_claim": "false",
        },
        {
            "step_id": "ID3241_3_divergence_bridge",
            "identity_piece": "q_loc is projected divergence of E_res_GK plus defects",
            "formula": "q_loc^nu = -(1/(kappa_* sigma_GK)) P_loc[nabla_mu E_res_GK^{mu nu}] - P_loc[nabla_mu Delta_K^{mu nu}] + E_GK/B_GK/P_loc defects",
            "derived_from": "q_loc=P_loc[(nabla Gamma_eff-div K_metric)-div Delta_K]+projector/domain/boundary and E_res_GK=-kappa_*sigma_GK(Gamma g-K_metric)",
            "result": "q_loc is not an independent force if the SGK residual is the EH residual sector",
            "status": "NEW_USEFUL_IDENTITY_DERIVED_CONDITIONAL",
            "valid_for_claim": "false",
        },
        {
            "step_id": "ID3241_4_zero_condition",
            "identity_piece": "local GR zero route",
            "formula": "E_res_GK=0, Delta_K=0, E_GK=0, B_GK=0, [P_loc,nabla]=0 imply q_loc=0",
            "derived_from": "ID3241_3 plus same-branch Euler/Ward conditions",
            "result": "the local-vacuum plateau is replaced by an action/residual identity",
            "status": "CONDITIONAL_ZERO_ROUTE_NOT_CURRENT_CLAIM",
            "valid_for_claim": "false",
        },
        {
            "step_id": "ID3241_5_bound_condition",
            "identity_piece": "fallback if zero theorem fails",
            "formula": "||q_loc|| <= C_Eres||div E_res_GK|| + C_DK||Delta_K||_H1 + C_H||H_GK|| + C_B||B_GK|| + C_P||[P_loc,nabla]||",
            "derived_from": "3238 qLoc bound interface plus E_res_GK identification",
            "result": "the empirical branch gets one no-cancellation residual vector instead of split EH and qLoc ledgers",
            "status": "BOUND_INTERFACE_DERIVED_VALUES_MISSING",
            "valid_for_claim": "false",
        },
    ]


def residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "URV3241_0_Eres_GK",
            "object": "E_res_GK_munu",
            "formula": "-kappa_* sigma_GK*(Gamma_eff g_munu-K_metric_munu)",
            "blocks": "local_GR;Newton;PPN;R10;clock;orbit",
            "close_or_bound_requirement": "Gamma_eff density owned; Khat=Kmetric; stress zero/suppressed or projected residual below bounds",
            "current_status": "FORMULA_DERIVED_PARENT_ADOPTION_UNSIGNED",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "URV3241_1_DeltaK",
            "object": "Delta_K_munu",
            "formula": "Khat_live_munu-K_metric_munu[Gamma_eff]",
            "blocks": "q_loc;J_geom;PPN force residual",
            "close_or_bound_requirement": "component birth certificates in 00,0i,trace,TF,derivative/boundary,units,projector/domain slots",
            "current_status": "RETAINED_FROM_3238",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "URV3241_2_Helmholtz",
            "object": "H_GK",
            "formula": "antisymmetrized second metric variation of sqrt(-g)(Gamma_eff g-Khat_live)",
            "blocks": "action-existence claim",
            "close_or_bound_requirement": "prove live stress is variational or replace Khat_live by Kmetric from the adopted density",
            "current_status": "OPERATOR_READY_COMPONENTS_MISSING",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "URV3241_3_Euler_boundary_projector",
            "object": "E_GK, B_GK, P_loc commutator",
            "formula": "same-branch Euler residual plus boundary/projector/domain terms",
            "blocks": "q_loc zero and local force silence",
            "close_or_bound_requirement": "same-branch on-shellness, no-flux boundary, parent-owned P_loc commuting with local limit",
            "current_status": "CONDITIONAL_FROM_3237_3238",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "URV3241_4_other_Eres",
            "object": "E_res_other_munu",
            "formula": "higher-derivative + connection + projector + memory/coframe + nonminimal + boundary/source-normalization residuals",
            "blocks": "EH dominance and PPN/Newton residual scoring",
            "close_or_bound_requirement": "sector-by-sector silence/suppression/source-backed coefficient rows",
            "current_status": "RETAINED_FROM_3086_3087",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "URV3241_5_weighted_boundary",
            "object": "Q_edge/weighted-Stokes terms",
            "formula": "C_corner + ||d_S(F epsilon)||_*||b_X||_* + |int F epsilon h_X| + |int F epsilon r_X|",
            "blocks": "boundary/projector zero and source-normalization",
            "close_or_bound_requirement": "B_X primitive/cohomology/kernel/corner rows theorem-zero or source-backed",
            "current_status": "BOUND_LAW_READY_VALUES_MISSING",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "URV3241_6_GM_transfer",
            "object": "G_* M_H to measured GM",
            "formula": "G_*:=kappa_* c^4/(8*pi); require G_* M_H_ref = GM_orbital + DeltaGM",
            "blocks": "measured Newtonian mechanics claim",
            "close_or_bound_requirement": "same-frame Hamiltonian/worldtube/Gauss source charge before orbital readout",
            "current_status": "SECONDARY_AFTER_UNIFIED_RESIDUAL",
            "valid_for_claim": "false",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "G3241_0_action_normal_form",
            "claim": "one parent local action normal form owns EH, quotient matter and SGK residual",
            "gate_pass": "false",
            "reason": "normal form is written, but Gamma_eff density/sign/boundary and Khat match remain parent-unsigned",
            "claim_allowed": "false",
        },
        {
            "gate_id": "G3241_1_identity_progress",
            "claim": "q_loc can be expressed as projected divergence of E_res_GK plus explicit defects",
            "gate_pass": "true",
            "reason": "identity follows algebraically once S_GK is treated as the residual action sector",
            "claim_allowed": "false",
        },
        {
            "gate_id": "G3241_2_EH_SGK_unified",
            "claim": "EH residual tensor and SGK/qLoc residual are the same live parent-owned object",
            "gate_pass": "false",
            "reason": "strong adoption still requires Gamma_eff owner, Khat=Kmetric, Helmholtz, boundary and projector clauses",
            "claim_allowed": "false",
        },
        {
            "gate_id": "G3241_3_Newton",
            "claim": "Newton/Poisson is recovered as measured Newtonian mechanics",
            "gate_pass": "false",
            "reason": "E_res/q_loc residuals and G_*M_H to measured GM transfer remain open",
            "claim_allowed": "false",
        },
        {
            "gate_id": "G3241_4_empirical",
            "claim": "PPN/R10/clock/orbit scoring can promote local branch",
            "gate_pass": "false",
            "reason": "unified residual vector has formulas but no theorem-zero or source-backed numeric rows",
            "claim_allowed": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3241_0_result",
            "decision": "EH_SGK_BRIDGE_IDENTITY_DERIVED_CONDITIONAL_NOT_CLAIMED",
            "because": "the residual action S_GK makes q_loc the projected divergence of the same tensor slot used as E_res_GK in the EH field equation",
            "next_action": "try to parent-sign Gamma_eff density and Khat=Kmetric, or lock Delta_K/H_GK into the unified residual vector",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3241_1_not_enough",
            "decision": "LOCAL_GR_NEWTON_STILL_NOT_PROMOTED",
            "because": "the identity is conditional and does not itself prove Gamma_eff, Khat_live, Helmholtz, boundary/projector silence, or GM calibration",
            "next_action": "do not score PPN/R10/orbits from this until residual rows are theorem-zero or sourced",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3241_2_best_next",
            "decision": "GAMMA_EFF_DENSITY_OWNER_AND_SIGN_CONVENTION_IS_NEXT",
            "because": "without a parent scalar-density formula for Gamma_eff, Kmetric cannot be evaluated and E_res_GK remains a formal slot",
            "next_action": "search/extract or write the minimal Gamma_eff density owner contract with units, sign sigma_GK, branch domain and boundary convention",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3241_0_3242",
            "next_checkpoint": "3242-Y5-R2FR-Gamma-eff-density-owner-sign-convention-or-unified-residual-row-under-AX1090.md",
            "mission": "derive or reject a parent scalar-density owner for Gamma_eff on the public quotient branch, including units, sign sigma_GK, background subtraction, branch domain, and boundary convention",
            "starting_equation": "S_GK=-sigma_GK int sqrt(-g_pub) Gamma_eff(g_pub,Phi,nablaPhi,D)+B_GK; E_res_GK=-kappa_*sigma_GK(Gamma_eff g-K_metric)",
            "success_if": "Gamma_eff is source-backed as a parent density and Kmetric can be computed component-by-component against Khat_live",
            "fallback_if_fail": "retain epsilon_Gamma_owner, Delta_K and H_GK as unified residual-vector rows with no-cancellation gates",
            "claim_policy": "no local-GR/Newton/PPN/R10/clock/orbit claim from a formal density slot alone",
            "valid_for_claim": "false",
        }
    ]


def validation_rows(source_rows: list[dict[str, Any]], generated_csvs: list[Path]) -> list[dict[str, Any]]:
    no_missing_sources = all(row["exists"] == "true" and row["parse_ok"] == "true" for row in source_rows)
    no_no_match = all("MISSING_SOURCE" not in row["evidence_hits"] and "NO_MATCH" not in row["evidence_hits"] for row in source_rows)
    outputs = [DOC, *generated_csvs]
    outputs_under_pcw = all(under(path, ROOT) for path in outputs)
    no_fw_outputs = all(not under(path, FW) for path in outputs)
    csvs_parse = all(csv_ok(path) for path in generated_csvs)
    claim_true = 0
    for path in generated_csvs:
        for row in read_csv(path):
            for key in ("valid_for_claim", "claim_allowed", "claim_active"):
                if str(row.get(key, "")).strip().lower() == "true":
                    claim_true += 1
    gate_progress_present = any(row["gate_id"] == "G3241_1_identity_progress" and row["gate_pass"] == "true" for row in read_csv(OUTPUTS["gates"]))
    unified_residual_present = any(row["residual_id"] == "URV3241_0_Eres_GK" for row in read_csv(OUTPUTS["residuals"]))
    next_density_owner = any("Gamma-eff-density-owner" in row["next_checkpoint"] for row in read_csv(OUTPUTS["next"]))
    return [
        {
            "validation_id": "VAL3241_00_sources_exist_parse",
            "passed": bool_str(no_missing_sources),
            "requirement": "all cited source paths exist and parse",
            "evidence": str(OUTPUTS["sources"]),
        },
        {
            "validation_id": "VAL3241_01_evidence_hits",
            "passed": bool_str(no_no_match),
            "requirement": "source register has direct evidence hits",
            "evidence": str(OUTPUTS["sources"]),
        },
        {
            "validation_id": "VAL3241_02_identity_progress_recorded",
            "passed": bool_str(gate_progress_present),
            "requirement": "the new EH/SGK divergence identity is recorded as progress but not a physics claim",
            "evidence": str(OUTPUTS["gates"]),
        },
        {
            "validation_id": "VAL3241_03_unified_residual_vector",
            "passed": bool_str(unified_residual_present),
            "requirement": "unified residual vector includes E_res_GK and Delta_K/H_GK components",
            "evidence": str(OUTPUTS["residuals"]),
        },
        {
            "validation_id": "VAL3241_04_next_density_owner",
            "passed": bool_str(next_density_owner),
            "requirement": "next target is Gamma_eff density owner/sign convention, not another broad audit",
            "evidence": str(OUTPUTS["next"]),
        },
        {
            "validation_id": "VAL3241_05_claims_blocked",
            "passed": bool_str(claim_true == 0),
            "requirement": "no local-GR/Newton/PPN/R10/clock/orbit claim is promoted",
            "evidence": f"claim_true={claim_true}",
        },
        {
            "validation_id": "VAL3241_06_csv_parse",
            "passed": bool_str(csvs_parse),
            "requirement": "all generated CSV files parse cleanly",
            "evidence": ";".join(str(path) for path in generated_csvs),
        },
        {
            "validation_id": "VAL3241_07_outputs_under_post_checkpoint",
            "passed": bool_str(outputs_under_pcw),
            "requirement": "all outputs stay inside post-checkpoint-work",
            "evidence": str(ROOT),
        },
        {
            "validation_id": "VAL3241_08_no_formalization_outputs",
            "passed": bool_str(no_fw_outputs),
            "requirement": "formalization-workbench is not modified",
            "evidence": str(FW),
        },
        {
            "validation_id": "VAL3241_09_pycache_absent",
            "passed": bool_str(not PYCACHE.exists()),
            "requirement": "scripts __pycache__ removed",
            "evidence": str(PYCACHE),
        },
        {
            "validation_id": "VAL3241_10_doc_written",
            "passed": bool_str(DOC.exists()),
            "requirement": "checkpoint markdown document written",
            "evidence": str(DOC),
        },
    ]


def build_doc(
    source_rows: list[dict[str, Any]],
    normal_form: list[dict[str, Any]],
    identity: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    derivation = """```text
S_GK = -sigma_GK int sqrt(-g_pub) Gamma_eff + B_GK

T_GK^{mu nu} = sigma_GK (Gamma_eff g^{mu nu} - K_metric^{mu nu}) + boundary/improvement

E_res_GK^{mu nu} := -kappa_* T_GK^{mu nu}

q_loc^nu
 = P_loc[(nabla^nu Gamma_eff - nabla_mu K_metric^{mu nu})
         - nabla_mu Delta_K^{mu nu}]
   + projector/domain/boundary/Euler terms

therefore

q_loc^nu
 = -(1/(kappa_* sigma_GK)) P_loc[nabla_mu E_res_GK^{mu nu}]
   - P_loc[nabla_mu Delta_K^{mu nu}]
   + projector/domain/boundary/Euler terms.
```"""
    return "\n\n".join(
        [
            "# 3241 - Public EH and SGK Metric-response Unification or Residual Vector under AX1090",
            "Private checkpoint. This is not a local-GR, Newton, PPN, R10, WEP, clock, orbital, Maxwell, or public-facing claim.",
            "## Result",
            (
                "3241 makes a real algebraic move. If the `Gamma_eff/Khat` sector is adopted as a genuine metric-response "
                "residual action on the public quotient metric, then the old `q_loc` force is not a separate mystery source. "
                "It is the projected divergence of the same left-hand residual tensor `E_res_GK` that appears in the EH field equation, "
                "plus the explicit defects `Delta_K`, boundary/projector terms, and same-branch Euler terms."
            ),
            derivation,
            (
                "This is progress because the local branch no longer has two unrelated ledgers: one EH residual ledger and one qLoc/SGK ledger. "
                "They can be made into one no-cancellation residual vector. But it is not yet a proof of local GR, because the live corpus still has "
                "to parent-sign the `Gamma_eff` density, the sign/units/boundary convention, the equality `Khat_live=K_metric[Gamma_eff]`, "
                "and the Helmholtz/action-existence condition."
            ),
            "## Parent Action Normal Form Attempt",
            md_table(
                normal_form,
                [
                    "row_id",
                    "object",
                    "formula",
                    "derivation_status",
                    "must_be_parent_signed",
                    "if_not_signed",
                    "valid_for_claim",
                ],
            ),
            "## EH/SGK Identity Derivation",
            md_table(
                identity,
                [
                    "step_id",
                    "identity_piece",
                    "formula",
                    "derived_from",
                    "result",
                    "status",
                    "valid_for_claim",
                ],
            ),
            "## Unified Residual Vector",
            md_table(
                residuals,
                [
                    "residual_id",
                    "object",
                    "formula",
                    "blocks",
                    "close_or_bound_requirement",
                    "current_status",
                    "valid_for_claim",
                ],
            ),
            "## Local-GR Gate Status",
            md_table(gates, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed"]),
            "## Decision",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "## Next Target",
            md_table(
                next_target,
                [
                    "next_id",
                    "next_checkpoint",
                    "mission",
                    "starting_equation",
                    "success_if",
                    "fallback_if_fail",
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
    normal_form = normal_form_rows()
    identity = identity_rows()
    residuals = residual_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["normal_form"], normal_form)
    write_csv(OUTPUTS["identity"], identity)
    write_csv(OUTPUTS["residuals"], residuals)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)

    generated_csvs = [
        OUTPUTS["sources"],
        OUTPUTS["normal_form"],
        OUTPUTS["identity"],
        OUTPUTS["residuals"],
        OUTPUTS["gates"],
        OUTPUTS["decision"],
        OUTPUTS["next"],
    ]
    validation = validation_rows(source_rows, generated_csvs)
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(
        build_doc(source_rows, normal_form, identity, residuals, gates, decisions, next_target, validation),
        encoding="utf-8",
    )
    validation = validation_rows(source_rows, generated_csvs)
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(
        build_doc(source_rows, normal_form, identity, residuals, gates, decisions, next_target, validation),
        encoding="utf-8",
    )

    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)

    failed = [row for row in validation if row["passed"] != "true"]
    if failed:
        raise SystemExit(f"3241 validation failed: {failed}")


if __name__ == "__main__":
    main()
