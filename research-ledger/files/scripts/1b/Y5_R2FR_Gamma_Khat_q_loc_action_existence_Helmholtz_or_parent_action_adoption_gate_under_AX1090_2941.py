from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2941"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2941-Y5-R2FR-Gamma-Khat-q_loc-action-existence-Helmholtz-or-parent-action-adoption-gate-under-AX1090.md"

SRC_2940_DOC = ROOT / "2940-Y5-R2FR-minimal-parent-current-chain-action-synthesis-or-sector-certificate-matrix-under-AX1090.md"
SRC_2940_NEXT = RESIDUALS / "P8_Y5_R2FR_2940_NEXT_TARGET.csv"
SRC_2940_SYNTHESIS = RESIDUALS / "P8_Y5_R2FR_2940_MINIMAL_PARENT_ACTION_SYNTHESIS_ATTEMPT.csv"
SRC_2940_SECTORS = RESIDUALS / "P8_Y5_R2FR_2940_SECTOR_CERTIFICATE_MATRIX.csv"
SRC_1010_DOC = ROOT / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md"
SRC_GK_CONTRACT = RESIDUALS / "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv"
SRC_2464_CANDIDATES = RESIDUALS / "P8_Y5_PARENT_ACTION_2464_CANDIDATE_ACTIONS.csv"
SRC_2464_DERIVATION = RESIDUALS / "P8_Y5_PARENT_ACTION_2464_QLOC_DERIVATION_ATTEMPT.csv"
SRC_2464_VARIATION = RESIDUALS / "P8_Y5_PARENT_ACTION_2464_VARIATION_OWNERSHIP.csv"
SRC_2464_SOURCE = RESIDUALS / "P8_Y5_PARENT_ACTION_2464_SOURCE_BRIDGE_CONTRACT.csv"
SRC_2908 = RESIDUALS / "P8_Y5_R2FR_2908_PARENT_ACTION_SKELETON.csv"
SRC_2925 = RESIDUALS / "P8_Y5_R2FR_2925_EXTRA_SECTOR_SILENCE_AUDIT.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2941_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_2941_GK_ACTION_EXISTENCE_THEOREM_GATE.csv",
    "variation": RESIDUALS / "P8_Y5_R2FR_2941_ACT2464A_VARIATION_DERIVATION.csv",
    "helmholtz": RESIDUALS / "P8_Y5_R2FR_2941_HELMHOLTZ_STRONG_ADOPTION_GATE.csv",
    "vacuum": RESIDUALS / "P8_Y5_R2FR_2941_LOCAL_VACUUM_QLOC_CONDITIONS.csv",
    "adoption": RESIDUALS / "P8_Y5_R2FR_2941_PARENT_ACTION_ADOPTION_GATE.csv",
    "residuals": RESIDUALS / "P8_Y5_R2FR_2941_QLOC_RESIDUAL_RETENTION_LEDGER.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2941_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2941_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2941_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2941_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2941_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "gk_gate_copy": PARENT_ACTION / "Gamma_Khat_q_loc_action_existence_gate_2941_NONCLAIM.csv",
    "variation_copy": PARENT_ACTION / "ACT2464A_variation_derivation_2941_NONCLAIM.csv",
    "qloc_residual_copy": LOCAL_BOUNDS / "Qloc_residual_retention_2941_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2941_VERTICAL_GENERATOR_ORIGIN_NEXT_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv_rows(path)
        return True
    except Exception:
        return False


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": RUN_UTC,
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    selected = columns or list(rows[0].keys())
    header = "| " + " | ".join(selected) + " |"
    separator = "| " + " | ".join("---" for _ in selected) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in selected) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2941_00_2940_doc", SRC_2940_DOC, "NEXT2940_0_2941;Validation overall: `True`", "2940 selected GK/q_loc action-existence target"),
        ("SRC2941_01_2940_next", SRC_2940_NEXT, "NEXT2940_0_2941", "machine-readable handoff"),
        ("SRC2941_02_2940_synthesis", SRC_2940_SYNTHESIS, "SYN2940_4_GK_current_law;PRIMARY_HARDEST_BLOCKER", "minimal parent spine GK row"),
        ("SRC2941_03_2940_sectors", SRC_2940_SECTORS, "SEC2940_3_GK_q_loc;action existence and first variation not proved", "sector certificate status"),
        ("SRC2941_04_1010_doc", SRC_1010_DOC, "GKT1010_0_variational_route;CG1010_0_S_GK_action", "earlier Gamma/Khat Helmholtz route"),
        ("SRC2941_05_GK_contract", SRC_GK_CONTRACT, "GK513_0_action_existence;GK513_5_boundary_no_flux", "first variation contract"),
        ("SRC2941_06_2464_candidates", SRC_2464_CANDIDATES, "ACT2464_A_vertical_generator_current_law;ACT2464_C_quadratic_penalty", "candidate action rows"),
        ("SRC2941_07_2464_derivation", SRC_2464_DERIVATION, "QDER2464_1_vary_A;QDER2464_4_not_promoted", "formal q_loc derivation attempt"),
        ("SRC2941_08_2464_variation", SRC_2464_VARIATION, "VAR2464_0_delta_A;VAR2464_5_boundary", "variation ownership audit"),
        ("SRC2941_09_2464_source_bridge", SRC_2464_SOURCE, "SRCBR2464_0_current_origin;SRCBR2464_4_universality", "source-current bridge blockers"),
        ("SRC2941_10_2908_skeleton", SRC_2908, "ACT2908_2_vertical_generator_current_law;ACT2908_7_total_verdict", "latest parent action skeleton"),
        ("SRC2941_11_2925_silence", SRC_2925, "XSI2925_3_GK_double_zero;XSI2925_8_total", "extra-sector silence audit"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_path, anchors, role in specs:
        found, missing = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_type": "local_file",
                    "source_path": str(source_path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": source_path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def theorem_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "theorem_id": "GKT2941_0_weak_action_existence",
            "claim_piece": "weak Euler-action existence for unprojected q current",
            "statement": "If A_nu is admitted as a parent field and Khat^{mu nu}:=partial L_K/partial(nabla_mu A_nu), then S_GK=int sqrt(-g)[L_K + A_nu nabla^nu Gamma_eff - A_nu J_M^nu + L_Gamma]+B_GK has an A_nu Euler equation nabla^nu Gamma_eff - nabla_mu Khat^{mu nu} - J_M^nu = 0.",
            "status": "PASS_AS_CONSTRUCTIVE_ACTION_TEMPLATE",
            "proof_value": "This is not a plateau axiom; q is an Euler equation of A_nu.",
            "current_mts_adoption": False,
            "blocking_gap": "A_nu, L_K, L_Gamma, J_M, P_loc and B_GK are not parent-derived from the current MTS corpus.",
        },
        {
            "theorem_id": "GKT2941_1_projected_residual",
            "claim_piece": "projected q_loc law",
            "statement": "If P_loc is fixed or parent-owned and commutes with the local readout limit, q_loc^nu=P_loc^nu_rho(nabla^rho Gamma_eff - nabla_mu Khat^{mu rho})=P_loc^nu_rho J_M^rho on shell.",
            "status": "CONDITIONAL_ON_PROJECTOR_OWNER",
            "proof_value": "Gives the exact local-vacuum route: source-free exterior plus silent boundary implies q_loc=0.",
            "current_mts_adoption": False,
            "blocking_gap": "P_loc ownership and projector stress/boundary clauses remain unsigned.",
        },
        {
            "theorem_id": "GKT2941_2_Helmholtz_A_sector",
            "claim_piece": "A-sector Helmholtz integrability",
            "statement": "The A_nu equation is Helmholtz-compatible by construction for the synthetic action because it is an Euler-Lagrange derivative of S_GK.",
            "status": "PASS_WEAK_HELMHOLTZ_FOR_SYNTHETIC_TEMPLATE",
            "proof_value": "Removes one algebraic worry: the q equation can be action-generated.",
            "current_mts_adoption": False,
            "blocking_gap": "This does not prove the metric stress, source current, or the existing MTS Gamma/Khat definitions are the same objects.",
        },
        {
            "theorem_id": "GKT2941_3_strong_parent_action",
            "claim_piece": "accepted MTS parent GK sector",
            "statement": "To promote the template, the corpus must derive A_nu as the vertical generator, specify L_K/L_Gamma with units/signs/gap, derive J_M from S_matter, own P_loc, and prove boundary/source silence.",
            "status": "FAIL_CURRENT_STRONG_ADOPTION",
            "proof_value": "Finite adoption contract is now explicit.",
            "current_mts_adoption": False,
            "blocking_gap": "strong parent-origin and source/boundary certificates fail.",
        },
        {
            "theorem_id": "GKT2941_4_local_GR_impact",
            "claim_piece": "q_loc zero for local GR",
            "statement": "Local q_loc zero follows only under the full condition set: adopted S_GK, parent-owned fixed P_loc, J_M=0 on exterior collar, no boundary flux, and no metric stress hair from the new sector.",
            "status": "CONDITIONAL_ONLY_NOT_LOCAL_GR_PROOF",
            "proof_value": "Sharpens exactly what must be proved to connect MTS to GR/Newton.",
            "current_mts_adoption": False,
            "blocking_gap": "source bridge and GK stress/silence remain open.",
        },
    ]
    return [add_common(row) for row in rows]


def variation_rows() -> list[dict[str, Any]]:
    rows = [
        ("VAR2941_0_define_action", "S_GK", "int sqrt(-g)[L_K(g,tau,nabla A)+A_nu nabla^nu Gamma_eff-A_nu J_M^nu+L_Gamma]+B_GK", "candidate scalar density", "PASS_TEMPLATE"),
        ("VAR2941_1_define_Khat", "Khat^{mu nu}", "Khat^{mu nu}:=partial L_K/partial(nabla_mu A_nu)", "momentum conjugate to nabla_mu A_nu", "PASS_TEMPLATE_DEFINITION"),
        ("VAR2941_2_vary_A_bulk", "delta_A S_GK bulk", "delta_A S=int sqrt(-g)[-nabla_mu Khat^{mu nu}+nabla^nu Gamma_eff-J_M^nu]delta A_nu", "integration by parts", "PASS_FORMAL_EULER"),
        ("VAR2941_3_boundary_term", "delta_A S_GK boundary", "int_boundary sqrt(|h|) n_mu Khat^{mu nu} delta A_nu plus possible B_GK variation", "fixed delta A or cancelling B_GK/no-flux condition", "OPEN_BOUNDARY_GATE"),
        ("VAR2941_4_projected_law", "q_loc^nu", "P_loc^nu_rho(nabla^rho Gamma_eff-nabla_mu Khat^{mu rho})=P_loc^nu_rho J_M^rho", "P_loc fixed/parent-owned", "CONDITIONAL_PROJECTED_EULER"),
        ("VAR2941_5_not_promoted", "current MTS theorem", "formal action template is not the same as corpus-derived parent sector", "A_nu/L_K/L_Gamma/J_M/P_loc/B_GK still new or unsigned", "NONCLAIM"),
    ]
    return [
        add_common(
            {
                "variation_id": variation_id,
                "object": obj,
                "formula": formula,
                "condition": condition,
                "status": status,
            }
        )
        for variation_id, obj, formula, condition, status in rows
    ]


def helmholtz_rows() -> list[dict[str, Any]]:
    rows = [
        ("HG2941_0_A_equation", "Euler equation for A_nu", "passes for synthetic action because it is directly varied from S_GK", True, "weak action-existence only"),
        ("HG2941_1_metric_stress", "Hilbert stress of GK sector", "cannot be certified until L_K, L_Gamma and all metric/coframe dependence are explicit", False, "blocks local GR stress silence"),
        ("HG2941_2_existing_symbol_match", "current MTS Gamma_eff/Khat equal action variables", "not proven; Khat could be a newly defined conjugate momentum rather than the old Khat object", False, "blocks adoption as current MTS"),
        ("HG2941_3_source_current", "J_M from same matter action", "missing; cannot use fitted/orbital source current", False, "blocks Newton and WEP"),
        ("HG2941_4_projector", "P_loc parent-owned and variation-safe", "missing; projection may hide/tune force components", False, "blocks physical q_loc statement"),
        ("HG2941_5_boundary", "B_GK/no-flux boundary certificate", "missing; q may vanish in bulk while boundary leaks force/mass", False, "blocks local vacuum law"),
        ("HG2941_6_double_zero", "T_GK and first variation vanish at local fixed point", "not proved; F1 and PPN hair may survive", False, "blocks GR/PPN limit"),
        ("HG2941_7_strong_verdict", "strong Helmholtz/adoption gate", "fails current corpus despite weak template pass", False, "keep q_loc residual explicit"),
    ]
    return [
        add_common(
            {
                "helmholtz_id": gate_id,
                "gate": gate,
                "finding": finding,
                "gate_passed": passed,
                "impact": impact,
            }
        )
        for gate_id, gate, finding, passed, impact in rows
    ]


def vacuum_rows() -> list[dict[str, Any]]:
    rows = [
        ("VAC2941_0_exact_source_law", "q_loc^nu", "q_loc^nu=P_loc^nu_rho J_M^rho", "adopted S_GK template plus fixed/owned P_loc", "bulk local residual source is matter current projection", "CONDITIONAL"),
        ("VAC2941_1_exterior_zero", "q_loc^nu", "q_loc^nu -> 0", "J_M^rho=0 on compact exterior collar and no distributional boundary layer", "local vacuum zero follows without plateau axiom", "CONDITIONAL_NOT_CURRENT_CLAIM"),
        ("VAC2941_2_F1_zero", "F1", "F1=0", "q_loc zero plus smooth weak-field expansion plus no metric stress hair", "linear local fifth-force coefficient vanishes", "CONDITIONAL_BLOCKED_BY_STRESS"),
        ("VAC2941_3_Delta_m_bound", "Delta m/m", "|Delta m|/m <= C[||P_loc J_M||+||B_GK||+||delta P_loc||]/M_source", "source denominator and norm convention derived from parent source measure", "retains bounded fallback if exact zero fails", "BOUND_FORM_ONLY"),
        ("VAC2941_4_transition_scale", "ell_tr/L_cg", "ell_tr/L_cg = 1/(m_GK L_cg)", "positive GK operator gap m_GK from L_K/L_Gamma and independent cosmological scale L_cg", "transition can be coefficient-derived rather than fitted", "PARAMETRIC_ONLY"),
        ("VAC2941_5_current_policy", "local GR/Newton/PPN", "not claimed", "all above conditions plus PiM/worldtube/H_ref gates", "do not claim yet", "NONCLAIM"),
    ]
    return [
        add_common(
            {
                "condition_id": condition_id,
                "quantity": quantity,
                "law": law,
                "required_conditions": required,
                "consequence": consequence,
                "status": status,
            }
        )
        for condition_id, quantity, law, required, consequence, status in rows
    ]


def adoption_rows() -> list[dict[str, Any]]:
    rows = [
        ("AD2941_0_action_template", "write explicit S_GK template", True, False, "candidate template exists"),
        ("AD2941_1_variation", "delta_A variation owns q current", True, False, "formal Euler equation closes"),
        ("AD2941_2_no_plateau", "q zero is not imposed as plateau", True, False, "zero would follow from source-free Euler law"),
        ("AD2941_3_A_origin", "A_nu derived as actual MTS vertical generator", False, True, "new parent material unless quotient/gauge origin is proved"),
        ("AD2941_4_symbol_identity", "existing Gamma_eff/Khat match template variables", False, True, "Khat may be redefined by L_K"),
        ("AD2941_5_source_descent", "J_M is same-action Noether/Hilbert current", False, True, "source bridge missing"),
        ("AD2941_6_projector_owner", "P_loc is parent-owned and stress-safe", False, True, "selector variation not closed"),
        ("AD2941_7_boundary_no_flux", "B_GK/no-flux condition signed", False, True, "boundary leakage open"),
        ("AD2941_8_metric_stress_silence", "GK stress and first variation are silent/bounded", False, True, "double-zero not proved"),
        ("AD2941_9_total_adoption", "promote S_GK as accepted current MTS sector", False, True, "strong adoption fails despite weak template pass"),
    ]
    return [
        add_common(
            {
                "adoption_id": adoption_id,
                "clause": clause,
                "clause_passed": passed,
                "blocks_adoption": blocks,
                "reason": reason,
            }
        )
        for adoption_id, clause, passed, blocks, reason in rows
    ]


def residual_rows() -> list[dict[str, Any]]:
    rows = [
        ("QRES2941_0_q_loc", "q_loc^nu", "retained explicit residual until strong S_GK adoption", "P_loc J_M + boundary/projector/stress leakage", "local_GR;PPN;R10;clock;orbital"),
        ("QRES2941_1_A_origin", "A_nu", "vertical generator origin missing", "new field/closure risk", "parent_action"),
        ("QRES2941_2_Khat_identity", "Delta_Khat", "Khat_old - partial L_K/partial(nabla A)", "symbol mismatch residual", "local_GR;PPN"),
        ("QRES2941_3_source", "J_M^nu", "matter/source current not derived from S_matter", "source smuggling risk", "Newton;WEP"),
        ("QRES2941_4_boundary", "B_GK", "boundary/no-flux term not signed", "bulk-zero can leak at linking surfaces", "source_mass;local_GR"),
        ("QRES2941_5_stress", "T_GK and dT_GK", "metric stress/double-zero not proved", "PPN/source-normalization hair", "PPN;local_GR"),
    ]
    return [
        add_common(
            {
                "residual_id": residual_id,
                "residual_symbol": symbol,
                "status": status,
                "definition": definition,
                "observable_targets": targets,
            }
        )
        for residual_id, symbol, status, definition, targets in rows
    ]


def claim_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2941_0_weak_template", "weak S_GK action template can generate q Euler equation", True, "PASS_CONDITIONAL_NONCLAIM", False),
        ("CG2941_1_current_adoption", "current MTS adopts S_GK as parent sector", False, "BLOCKED_PARENT_ORIGIN_SOURCE_PROJECTOR_BOUNDARY", False),
        ("CG2941_2_q_loc_zero", "q_loc=0 in local vacuum is derived for current MTS", False, "CONDITIONAL_ONLY", False),
        ("CG2941_3_F1_zero", "F1=0 local residual coefficient is proved", False, "BLOCKED_BY_STRESS_AND_SOURCE_GATES", False),
        ("CG2941_4_Newton_GR", "Newton/local-GR/PPN branch reopens", False, "BLOCKED_BY_STRONG_ADOPTION_AND_SOURCE_MASS", False),
        ("CG2941_5_public_claim", "public empirical/local claim allowed from 2941", False, "NO_PUBLIC_CLAIM", False),
    ]
    return [
        add_common(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "condition_passed": passed,
                "status": status,
                "claim_allowed": allowed,
            }
        )
        for gate_id, claim, passed, status, allowed in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2941_0_result", "weak action-existence passes, strong MTS adoption fails", "ACT2464_A can generate the q equation, but it is not yet parent-derived MTS material", "keep template as best constructive candidate"),
        ("DEC2941_1_not_a_plateau", "the route is better than a plateau axiom", "q_loc zero would follow from an Euler equation plus source-free exterior", "continue derivation-first"),
        ("DEC2941_2_main_bottleneck", "A_nu vertical-generator origin is now the cleanest next proof", "without A_mu origin the action still looks like an added multiplier/current-law sector", "derive A_mu from quotient/gauge geometry or demote to closure"),
        ("DEC2941_3_parallel_bottleneck", "J_M/PiM/worldtube source bridge remains parallel", "even an adopted q equation will not give Newton without source mass descent", "return after A_mu origin or if A_mu fails"),
        ("DEC2941_4_residual_policy", "retain q_loc residual explicitly", "local-GR claims must not hide boundary/projector/stress leakage", "use residual rows for later bounds if derivation fails"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "reason": reason,
                "next_action": next_action,
            }
        )
        for decision_id, decision, reason, next_action in rows
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2941_0_2942",
                "priority": "selected_primary",
                "next_doc": "2942-Y5-R2FR-vertical-generator-origin-gauge-symmetry-or-A-mu-closure-demotion-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_vertical_generator_origin_gauge_symmetry_or_A_mu_closure_demotion_under_AX1090_2942.py",
                "objective": "Try to derive A_mu as the actual MTS vertical/local generator from quotient/gauge geometry so ACT2464_A is not a multiplier smuggled in by hand; if this fails, demote S_GK to closure-only and move to q_loc finite residual bounds.",
                "include": "quotient map q; vertical kernel; Dq(A)=0; gauge redundancy; transformation law; units; coupling to Gamma_eff; stress/source neutrality; impact on ACT2464_A adoption",
                "exclude": "local-GR/Newton/R10 claim; empirical scoring; plateau axiom; direct multiplier closure; GitHub action; formalization-workbench edits",
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    copies = [
        ("gk_gate_copy", OUTPUTS["theorem"], BRANCH_OUTPUTS["gk_gate_copy"]),
        ("variation_copy", OUTPUTS["variation"], BRANCH_OUTPUTS["variation_copy"]),
        ("qloc_residual_copy", OUTPUTS["residuals"], BRANCH_OUTPUTS["qloc_residual_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows = []
    for copy_id, source_path, copy_path in copies:
        if source_path.exists():
            shutil.copyfile(source_path, copy_path)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source_path),
                    "copy_path": str(copy_path),
                    "source_exists": source_path.exists(),
                    "copy_exists": copy_path.exists(),
                }
            )
        )
    return rows


def validation_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    formalization_has_2941 = False
    if FORMALIZATION.exists():
        formalization_has_2941 = any(FORMALIZATION.rglob("*2941*"))
    checks = [
        ("VAL2941_0_sources_exist", all(row["path_exists"] for row in source_rows), "all cited local source paths exist", True),
        ("VAL2941_1_anchors_found", all(row["anchors_found"] for row in source_rows), "all source anchors found", True),
        ("VAL2941_2_weak_template_pass", any(row.get("theorem_id") == "GKT2941_0_weak_action_existence" and row.get("status") == "PASS_AS_CONSTRUCTIVE_ACTION_TEMPLATE" for row in read_csv_rows(OUTPUTS["theorem"])), "weak action template pass is recorded", True),
        ("VAL2941_3_strong_adoption_fails", any(row.get("adoption_id") == "AD2941_9_total_adoption" and row.get("clause_passed") == "False" for row in read_csv_rows(OUTPUTS["adoption"])), "strong S_GK adoption remains refused", True),
        ("VAL2941_4_q_loc_retained", any(row.get("residual_id") == "QRES2941_0_q_loc" for row in read_csv_rows(OUTPUTS["residuals"])), "q_loc residual retention row exists", True),
        ("VAL2941_5_claims_blocked", all(row.get("claim_allowed") == "False" for row in read_csv_rows(OUTPUTS["claims"])), "no local-GR/Newton/R10 claim allowed", True),
        ("VAL2941_6_next_target_selected", any(row.get("next_id") == "NEXT2941_0_2942" for row in read_csv_rows(OUTPUTS["next"])), "2942 vertical-generator target selected", True),
        ("VAL2941_7_branches_exist", all(path.exists() for path in BRANCH_OUTPUTS.values()), "branch copy files exist", True),
        ("VAL2941_8_csvs_parse", all(csv_parses(path) for path in generated_csvs), "all generated CSV files parse", True),
        ("VAL2941_9_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in [DOC, *OUTPUTS.values(), *BRANCH_OUTPUTS.values()]), "all generated outputs are under post-checkpoint-work", True),
        ("VAL2941_10_formalization_clean", not formalization_has_2941, "no 2941 outputs were written to formalization-workbench", True),
    ]
    overall = all(passed == required for _, passed, _, required in checks)
    rows = [{"validation_id": validation_id, "passed": passed, "check": check, "required": required} for validation_id, passed, check, required in checks]
    rows.append({"validation_id": "VAL2941_OVERALL", "passed": overall, "check": "2941 validation overall", "required": True})
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    variation: list[dict[str, Any]],
    helmholtz: list[dict[str, Any]],
    vacuum: list[dict[str, Any]],
    adoption: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    branches: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    overall = next(row for row in validation if row["validation_id"] == "VAL2941_OVERALL")["passed"]
    text = f"""# 2941 - Y5 R2FR: Gamma/Khat/q_loc action-existence Helmholtz or parent-action adoption gate under AX1090

Status: `Y5_R2FR_2941_weak_GK_action_template_passes_strong_MTS_parent_adoption_fails_A_mu_origin_selected_next`

Claim ceiling: `weak_S_GK_template_yes_current_parent_GK_sector_no_q_loc_zero_no_F1_zero_no_Newton_no_local_GR_no_R10_no_GitHub_claim`

2941 separates the useful leap from the dangerous shortcut. The useful leap is that the ACT2464_A current-law template really can generate the `q_loc` equation as an Euler equation:

`S_GK = int sqrt(-g)[L_K(g,tau,nabla A)+A_nu nabla^nu Gamma_eff-A_nu J_M^nu+L_Gamma(Gamma_eff,g,tau)] + B_GK`,

with `Khat^{{mu nu}} := partial L_K / partial(nabla_mu A_nu)`, so

`delta_A S_GK = int sqrt(-g)[-nabla_mu Khat^{{mu nu}}+nabla^nu Gamma_eff-J_M^nu] delta A_nu + boundary`.

That is not a plateau axiom. But it is also not yet a current MTS derivation, because `A_nu`, `L_K`, `L_Gamma`, `J_M`, `P_loc`, and the boundary/no-flux/stress certificates are not parent-derived from the corpus. So the weak action-existence gate passes as a constructive template; the strong parent-action adoption gate fails.

## Source Register

{md_table(source_rows, ["source_id", "source_path", "path_exists", "anchors_found", "role"])}

## GK Action-Existence Theorem Gate

{md_table(theorem, ["theorem_id", "claim_piece", "statement", "status", "current_mts_adoption", "blocking_gap"])}

## ACT2464_A Variation Derivation

{md_table(variation, ["variation_id", "object", "formula", "condition", "status"])}

## Helmholtz Strong Adoption Gate

{md_table(helmholtz, ["helmholtz_id", "gate", "finding", "gate_passed", "impact"])}

## Local Vacuum q_loc Conditions

{md_table(vacuum, ["condition_id", "quantity", "law", "required_conditions", "consequence", "status"])}

## Parent Action Adoption Gate

{md_table(adoption, ["adoption_id", "clause", "clause_passed", "blocks_adoption", "reason"])}

## q_loc Residual Retention Ledger

{md_table(residuals, ["residual_id", "residual_symbol", "status", "definition", "observable_targets"])}

## Claim Gates

{md_table(claims, ["claim_gate_id", "claim", "condition_passed", "status", "claim_allowed"])}

## Decision Ledger

{md_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Next Target

{md_table(next_target, ["next_id", "priority", "next_doc", "next_script", "objective", "exclude"])}

## Branch Copies

{md_table(branches, ["copy_id", "source_path", "copy_path", "source_exists", "copy_exists", "valid_for_claim"])}

## Validation

{md_table(validation, ["validation_id", "passed", "check", "required"])}

Validation overall: `{overall}`.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    write_csv(OUTPUTS["sources"], source_rows)

    theorem = theorem_rows()
    variation = variation_rows()
    helmholtz = helmholtz_rows()
    vacuum = vacuum_rows()
    adoption = adoption_rows()
    residuals = residual_rows()
    claims = claim_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["variation"], variation)
    write_csv(OUTPUTS["helmholtz"], helmholtz)
    write_csv(OUTPUTS["vacuum"], vacuum)
    write_csv(OUTPUTS["adoption"], adoption)
    write_csv(OUTPUTS["residuals"], residuals)
    write_csv(OUTPUTS["claims"], claims)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    validation = validation_rows(source_rows)
    write_csv(OUTPUTS["validation"], validation)

    write_doc(source_rows, theorem, variation, helmholtz, vacuum, adoption, residuals, claims, decisions, next_target, branches, validation)

    overall = next(row for row in validation if row["validation_id"] == "VAL2941_OVERALL")["passed"]
    print(f"2941 validation overall: {overall}")
    print(DOC)


if __name__ == "__main__":
    main()
