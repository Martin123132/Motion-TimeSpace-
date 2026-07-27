from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_STARTED_UTC = datetime.now(timezone.utc)
ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
WORK = ROOT / "post-checkpoint-work"
MTS = WORK / "source-intake" / "mts_residuals"
RAB_QUEUE = WORK / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = WORK / "source-intake" / "beta-source" / "docs"
MICROSCOPE_DIR = WORK / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SCRIPTS = WORK / "scripts"
FORMALIZATION = ROOT / "formalization-workbench"
DOC = WORK / "2766-Y5-R2FR-visible-operator-domain-exhaustion-or-alpha-counterterm-prior-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2766_SOURCE_REGISTER.csv",
    "exhaustion": MTS / "P8_Y5_R2FR_2766_VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_ATTEMPT.csv",
    "algebra": MTS / "P8_Y5_R2FR_2766_ALLOWED_OPERATOR_ALGEBRA.csv",
    "prior": MTS / "P8_Y5_R2FR_2766_ALPHA_COUNTERTERM_PRIOR_BRANCH.csv",
    "product_pack": MTS / "P8_Y5_R2FR_2766_ALPHA_PRODUCT_PRIOR_PACK.csv",
    "transfer": MTS / "P8_Y5_R2FR_2766_NO_TRANSFER_GATES.csv",
    "debts": MTS / "P8_Y5_R2FR_2766_PROJECTION_DEBT_LEDGER.csv",
    "gates": MTS / "P8_Y5_R2FR_2766_CLAIM_GATES.csv",
    "refusal": MTS / "P8_Y5_R2FR_2766_REFUSAL_RUNNER_NONCLAIM.csv",
    "next": MTS / "P8_Y5_R2FR_2766_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2766_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2766_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "exhaustion_queue": RAB_QUEUE / "JR2766_VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_ATTEMPT_NONCLAIM.csv",
    "prior_queue": RAB_QUEUE / "JR2766_ALPHA_COUNTERTERM_PRIOR_BRANCH_NONCLAIM.csv",
    "product_queue": RAB_QUEUE / "JR2766_ALPHA_PRODUCT_PRIOR_PACK_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_OR_ALPHA_PRIOR_2766_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "visible_operator_exhaustion_or_alpha_prior_2766_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2766_ALPHA_PRODUCT_PREDICTION_NEXT.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(WORK))
    except ValueError:
        return str(path)


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["valid_for_claim"] = False
    return row


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def find_row(rows: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    for row in rows:
        if row.get(key) == value:
            return row
    return {}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def csv_row_count(path: Path) -> int:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        cells = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def build_sources() -> list[dict[str, Any]]:
    specs = [
        ("SRC2766_00_2765_doc", "2765_doc", DOC.parent / "2765-Y5-R2FR-unique-Maxwell-subblock-no-independent-F2-ban-or-balpha-retention-under-AX1090.md", ["NEXT2765_0_2766", "CT2765_3_verdict"], "2765 handoff to visible-operator exhaustion"),
        ("SRC2766_01_2765_validation", "2765_validation", MTS / "P8_Y5_BRR545_2765_VALIDATION.csv", ["VAL2765_OVERALL"], "2765 validation"),
        ("SRC2766_02_2765_counterterm", "2765_counterterm_csv", MTS / "P8_Y5_R2FR_2765_F2_COUNTERTERM_LEDGER.csv", ["CT2765_3_verdict"], "retained alpha counterterm branch from current R2/f(R) path"),
        ("SRC2766_03_1058_doc", "1058_doc", WORK / "1058-Y5-R10-visible-operator-domain-exhaustion-or-alpha-counterterm-prior.md", ["VOE1058_5_verdict", "ACP1058_0_ZA_decomposition"], "R10 visible operator-domain precedent"),
        ("SRC2766_04_1058_exhaustion", "1058_exhaustion_csv", MTS / "P8_Y5_R10_1058_VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_ATTEMPT.csv", ["VOE1058_5_verdict"], "prior exhaustion theorem attempt"),
        ("SRC2766_05_1058_algebra", "1058_algebra_csv", MTS / "P8_Y5_R10_1058_ALLOWED_OPERATOR_ALGEBRA_AUDIT.csv", ["OA1058_1_constant_counterterm"], "prior allowed operator algebra"),
        ("SRC2766_06_1058_prior", "1058_prior_csv", MTS / "P8_Y5_R10_1058_ALPHA_COUNTERTERM_PRIOR_BRANCH.csv", ["ACP1058_0_ZA_decomposition"], "prior alpha counterterm decomposition"),
        ("SRC2766_07_1059_doc", "1059_doc", WORK / "1059-Y5-R10-alpha-counterterm-product-prior-source-pack-and-cross-arena-gate.md", ["APP1059_0_clock_YbE3E2", "NTG1059_1_clock_to_WEP"], "product-prior source pack precedent"),
        ("SRC2766_08_1059_pack", "1059_product_pack_csv", MTS / "P8_Y5_R10_1059_ALPHA_PRODUCT_PRIOR_PACK.csv", ["APP1059_2_WEP_alpha_Coulomb"], "clock/WEP/R10 product rows"),
        ("SRC2766_09_1059_transfer", "1059_transfer_csv", MTS / "P8_Y5_R10_1059_NO_TRANSFER_GATES.csv", ["NTG1059_3_WEP_to_R10"], "no-transfer policy"),
        ("SRC2766_10_1059_debts", "1059_debts_csv", MTS / "P8_Y5_R10_1059_PROJECTION_DEBT_LEDGER.csv", ["PD1059_2_tau_WEP"], "projection debts"),
    ]
    rows = []
    for row_id, source_key, path, needles, role in specs:
        text = read_text(path)
        exists = path.exists()
        rows.append(nonclaim({
            "row_id": row_id,
            "source_key": source_key,
            "source_path": str(path),
            "exists": exists,
            "needle_spec": ";".join(needles),
            "needles_found": exists and all(needle in text for needle in needles),
            "source_role": role,
        }))
    return rows


def load_inputs() -> dict[str, list[dict[str, str]]]:
    return {
        "voe1058": read_csv_rows(MTS / "P8_Y5_R10_1058_VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_ATTEMPT.csv"),
        "oa1058": read_csv_rows(MTS / "P8_Y5_R10_1058_ALLOWED_OPERATOR_ALGEBRA_AUDIT.csv"),
        "acp1058": read_csv_rows(MTS / "P8_Y5_R10_1058_ALPHA_COUNTERTERM_PRIOR_BRANCH.csv"),
        "app1059": read_csv_rows(MTS / "P8_Y5_R10_1059_ALPHA_PRODUCT_PRIOR_PACK.csv"),
        "ntg1059": read_csv_rows(MTS / "P8_Y5_R10_1059_NO_TRANSFER_GATES.csv"),
        "pd1059": read_csv_rows(MTS / "P8_Y5_R10_1059_PROJECTION_DEBT_LEDGER.csv"),
    }


def build_exhaustion_rows(inputs: dict[str, list[dict[str, str]]]) -> list[dict[str, Any]]:
    prior_verdict = find_row(inputs["voe1058"], "attempt_id", "VOE1058_5_verdict")
    return [
        nonclaim({"row_id": "VOE2766_0_target", "claim_piece": "visible operator-domain exhaustion", "mathematical_form": "Allowed[S_vis]=Image(ParentGenerate[Phi,q_loc,Dq,F_parent,theta_rep,topological levels,measure/coframe/connection descent])", "current_status": "TARGET_SHARP", "proof_or_blocker": "would ban non-parent F_Q^2, hidden coefficient maps, and readout/radiative visible counterterms", "if_signed": "visible constants become quotient/representation data; b_alpha route can close", "if_unsigned": "alpha counterterm/product-prior branch remains mandatory"}),
        nonclaim({"row_id": "VOE2766_1_parent_generator_domain", "claim_piece": "declared parent generator domain", "mathematical_form": "Op_allowed subset Alg[q(Phi),Dq(Phi),F_parent,theta_rep,topological classes,descent measure]", "current_status": "CONTRACT_EXACT_IF_ADOPTED_NOT_DERIVED", "proof_or_blocker": "current corpus states a discipline rule but does not derive it from MTS primitives", "if_signed": "post-hoc F_Q^2/mass/clock slots forbidden", "if_unsigned": "ordinary effective field grammar admits extra visible scalar densities"}),
        nonclaim({"row_id": "VOE2766_2_quotient_functor_exactness", "claim_piece": "visible quotient functor exact/full enough", "mathematical_form": "S_vis factors through C_vis=q_loc(C_parent) with no extra coefficient object Coeff(O_vis)", "current_status": "UNSIGNED", "proof_or_blocker": "quotient map and full visible category are not constructed with a universal property", "if_signed": "no free visible coefficient slots", "if_unsigned": "lambda_A F_Q^2 remains legal"}),
        nonclaim({"row_id": "VOE2766_3_no_hidden_visible_hom", "claim_piece": "no hidden-to-visible coefficient morphisms", "mathematical_form": "Hom(C_hid,Coeff(O_vis))=Const or absent", "current_status": "BLOCKED_BY_SCALAR_OBSTRUCTION", "proof_or_blocker": "any surviving invariant scalar I_hid permits f(I_hid)F_Q^2 unless the parent action forbids it", "if_signed": "hidden alpha/mass/readout drifts vanish", "if_unsigned": "finite b_alpha and WEP/R10 product priors remain live"}),
        nonclaim({"row_id": "VOE2766_4_radiative_readout_closure", "claim_piece": "effective/readout action remains in parent image", "mathematical_form": "S_eff and readout maps stay in Image(ParentGenerate) after reduction, loops, thresholds, and apparatus projection", "current_status": "UNSIGNED", "proof_or_blocker": "tree-level grammar does not automatically block delta lambda_A(mu,Xhat) or readout coefficients", "if_signed": "operator exhaustion is stable under lab/cosmology projection", "if_unsigned": "radiative/readout alpha counterterm prior remains mandatory"}),
        nonclaim({"row_id": "VOE2766_5_boundary_projection_silence", "claim_piece": "boundary/local projection silence", "mathematical_form": "boundary terms and local projection operators do not generate F_Q^2, mass, clock, or source coefficients outside the parent image", "current_status": "UNSIGNED", "proof_or_blocker": "local residual work still carries source/readout projection debts", "if_signed": "local GR/Newton reduction loses one major constant-sector blocker", "if_unsigned": "no local-GR claim from alpha/source constants"}),
        nonclaim({"row_id": "VOE2766_6_verdict", "claim_piece": "visible operator-domain exhaustion theorem", "mathematical_form": prior_verdict.get("mathematical_form", "all exhaustion clauses signed => no independent alpha counterterm"), "current_status": "REJECT_CURRENT_CLAIM_RETAIN_COUNTERTERM_PRIOR", "proof_or_blocker": "current corpus has a precise contract and counterexample ledger, not a derivation", "if_signed": "b_alpha=0 route reopens", "if_unsigned": "formal alpha counterterm product-prior branch is the honest route"}),
    ]


def build_algebra_rows(inputs: dict[str, list[dict[str, str]]]) -> list[dict[str, Any]]:
    prior_constant = find_row(inputs["oa1058"], "operator_id", "OA1058_1_constant_counterterm")
    prior_hidden = find_row(inputs["oa1058"], "operator_id", "OA1058_2_hidden_counterterm")
    prior_radiative = find_row(inputs["oa1058"], "operator_id", "OA1058_3_radiative_counterterm")
    return [
        nonclaim({"row_id": "OA2766_0_parent_generated", "operator_class": "parent-generated visible kinetic term", "example": "C_P <F_Q T_Q,F_Q T_Q>_P", "status": "ALLOWED_CONDITIONAL", "ordinary_symmetry_result": "allowed", "claim_effect": "can supply one Maxwell coefficient if parent projection/norm is derived", "retained_if_unsigned": "yes"}),
        nonclaim({"row_id": "OA2766_1_constant_counterterm", "operator_class": prior_constant.get("operator_class", "constant visible counterterm"), "example": prior_constant.get("example", "lambda_A F_Q^2"), "status": prior_constant.get("status", "ALLOWED_BY_ORDINARY_SYMMETRIES"), "ordinary_symmetry_result": "diffeomorphism plus U(1) allow it", "claim_effect": "blocks alpha ownership as a theorem", "retained_if_unsigned": "yes"}),
        nonclaim({"row_id": "OA2766_2_hidden_counterterm", "operator_class": prior_hidden.get("operator_class", "hidden scalar visible counterterm"), "example": prior_hidden.get("example", "f(I_hid)F_Q^2"), "status": prior_hidden.get("status", "ALLOWED_IF_HIDDEN_INVARIANT_SURVIVES"), "ordinary_symmetry_result": "allowed if invariant scalar survives", "claim_effect": "opens vertical alpha drift and WEP/R10 pressure", "retained_if_unsigned": "yes"}),
        nonclaim({"row_id": "OA2766_3_radiative_counterterm", "operator_class": prior_radiative.get("operator_class", "effective/radiative threshold"), "example": prior_radiative.get("example", "delta lambda_A(mu,Xhat)F_Q^2"), "status": prior_radiative.get("status", "RETAINED_UNTIL_RADIOUT_CLOSURE"), "ordinary_symmetry_result": "not ruled out by tree-level exhaustion", "claim_effect": "prevents claim-grade alpha silence", "retained_if_unsigned": "yes"}),
        nonclaim({"row_id": "OA2766_4_mass_clock_source_slots", "operator_class": "visible mass/clock/source coefficient slots", "example": "m_A(Xhat) psi_bar psi; c_clock(Xhat) O_clock; beta_source_alpha O_source", "status": "SAME_GRAMMAR_RISK", "ordinary_symmetry_result": "legal unless parent grammar forbids or owns them", "claim_effect": "ties alpha problem to local-GR/source constant-sector debt", "retained_if_unsigned": "yes"}),
        nonclaim({"row_id": "OA2766_5_verdict", "operator_class": "forbidden non-parent visible terms", "example": "O_vis with coefficient outside Image(ParentGenerate)", "status": "FORBIDDEN_ONLY_BY_EXHAUSTION_THEOREM_OR_AXIOM", "ordinary_symmetry_result": "not forbidden by ordinary covariance/gauge invariance alone", "claim_effect": "no theorem-zero from symmetry alone", "retained_if_unsigned": "yes"}),
    ]


def build_prior_rows(inputs: dict[str, list[dict[str, str]]]) -> list[dict[str, Any]]:
    rows = []
    mappings = [
        ("ACP2766_0_ZA_decomposition", "ACP1058_0_ZA_decomposition"),
        ("ACP2766_1_balpha_counterterm", "ACP1058_1_balpha_counterterm"),
        ("ACP2766_2_WEP_product", "ACP1058_2_WEP_product"),
        ("ACP2766_3_R10_product", "ACP1058_3_R10_product"),
        ("ACP2766_4_counterterm_policy", "ACP1058_4_counterterm_policy"),
    ]
    for new_id, old_id in mappings:
        old = find_row(inputs["acp1058"], "prior_id", old_id)
        rows.append(nonclaim({
            "row_id": new_id,
            "source_row": old_id,
            "quantity": old.get("quantity", "MISSING_QUANTITY"),
            "definition": old.get("definition", "MISSING_DEFINITION"),
            "current_status": old.get("current_status", "MISSING_STATUS"),
            "observable_link": old.get("observable_link", "MISSING_LINK"),
            "source_or_bound": old.get("source_or_bound", "MISSING_SOURCE_OR_BOUND"),
        }))
    rows.append(nonclaim({"row_id": "ACP2766_5_R2FR_policy", "source_row": "2765_CT2765_3_verdict", "quantity": "R2/f(R) alpha counterterm branch", "definition": "Z_A=C_P N_Q+lambda_A0+lambda_Ahid(I_hid)+delta_lambda_A_rad+retained readout terms until visible operator-domain exhaustion is derived", "current_status": "RETAINED_NONCLAIM_BRANCH", "observable_link": "clock; WEP; R10; EM/readout; local source constants", "source_or_bound": "2765 retained branch plus 1058/1059 product-prior pack"}))
    return rows


def build_product_pack(inputs: dict[str, list[dict[str, str]]]) -> list[dict[str, Any]]:
    id_map = {
        "APP1059_0_clock_YbE3E2": "APP2766_0_clock_YbE3E2",
        "APP1059_1_clock_AlHg": "APP2766_1_clock_AlHg",
        "APP1059_2_WEP_alpha_Coulomb": "APP2766_2_WEP_alpha_Coulomb",
        "APP1059_3_WEP_surface_binding": "APP2766_3_WEP_surface_binding",
        "APP1059_4_R10_finite_alpha": "APP2766_4_R10_finite_alpha",
    }
    rows = []
    for old_id, new_id in id_map.items():
        old = find_row(inputs["app1059"], "pack_id", old_id)
        rows.append(nonclaim({
            "row_id": new_id,
            "source_row": old_id,
            "arena": old.get("arena", "MISSING_ARENA"),
            "product_symbol": old.get("product_symbol", "MISSING_PRODUCT_SYMBOL"),
            "bound_or_target": old.get("bound_or_target", "MISSING_BOUND_OR_TARGET"),
            "units": old.get("units", "MISSING_UNITS"),
            "score_rule": old.get("score_rule", "MISSING_SCORE_RULE"),
            "missing_for_standalone": old.get("missing_for_standalone", "MISSING_STANDALONE_INPUTS"),
            "score_ready": old.get("score_ready", "false"),
        }))
    rows.append(nonclaim({"row_id": "APP2766_5_policy", "source_row": "2766", "arena": "cross_arena", "product_symbol": "alpha counterterm/product prior branch", "bound_or_target": "may be used only as exact product rows; no division by guessed tau/source factors", "units": "per source row", "score_rule": "numeric product predictions can be tested only when sourced in same convention", "missing_for_standalone": "visible operator-domain theorem or parent-owned tau/source maps", "score_ready": "false"}))
    return rows


def build_transfer_rows(inputs: dict[str, list[dict[str, str]]]) -> list[dict[str, Any]]:
    id_map = {
        "NTG1059_0_clock_to_balpha": "NTG2766_0_clock_to_balpha",
        "NTG1059_1_clock_to_WEP": "NTG2766_1_clock_to_WEP",
        "NTG1059_2_clock_to_R10": "NTG2766_2_clock_to_R10",
        "NTG1059_3_WEP_to_R10": "NTG2766_3_WEP_to_R10",
    }
    rows = []
    for old_id, new_id in id_map.items():
        old = find_row(inputs["ntg1059"], "gate_id", old_id)
        rows.append(nonclaim({
            "row_id": new_id,
            "source_row": old_id,
            "forbidden_transfer": old.get("forbidden_transfer", "MISSING_TRANSFER"),
            "reason": old.get("reason", "MISSING_REASON"),
            "allowed_use": old.get("allowed_use", "MISSING_ALLOWED_USE"),
            "missing_to_unlock": old.get("missing_to_unlock", "MISSING_UNLOCK"),
            "gate_pass": False,
        }))
    rows.append(nonclaim({"row_id": "NTG2766_4_policy", "source_row": "2766", "forbidden_transfer": "operator-exhaustion contract -> public local-GR/EM claim", "reason": "the contract is not derived and cannot be used as if signed", "allowed_use": "private branch discipline and exact next theorem target", "missing_to_unlock": "derive all VOE2766 clauses or demote to explicit closure axiom", "gate_pass": False}))
    return rows


def build_debt_rows(inputs: dict[str, list[dict[str, str]]]) -> list[dict[str, Any]]:
    id_map = {
        "PD1059_0_tau_clock": "PD2766_0_tau_clock",
        "PD1059_1_beta_source_alpha": "PD2766_1_beta_source_alpha",
        "PD1059_2_tau_WEP": "PD2766_2_tau_WEP",
        "PD1059_3_tau_R10": "PD2766_3_tau_R10",
        "PD1059_4_KX_ZX_lambda": "PD2766_4_KX_ZX_lambda",
    }
    rows = []
    for old_id, new_id in id_map.items():
        old = find_row(inputs["pd1059"], "debt_id", old_id)
        rows.append(nonclaim({
            "row_id": new_id,
            "source_row": old_id,
            "projection": old.get("projection", "MISSING_PROJECTION"),
            "status": old.get("status", "MISSING_STATUS"),
            "source": old.get("source", "MISSING_SOURCE"),
            "blocks": old.get("blocks", "MISSING_BLOCKS"),
            "next_required_input": old.get("next_required_input", "MISSING_NEXT_INPUT"),
        }))
    rows.append(nonclaim({"row_id": "PD2766_5_visible_operator_universal_property", "source_row": "2766", "projection": "Allowed[S_vis]=Image(ParentGenerate)", "status": "UNIVERSAL_PROPERTY_NOT_DERIVED", "source": "VOE2766_1..6", "blocks": "alpha theorem-zero and local constant-sector closure", "next_required_input": "construct parent category/quotient functor and prove no extra visible coefficient object"}))
    rows.append(nonclaim({"row_id": "PD2766_6_radiative_readout", "source_row": "2766", "projection": "S_eff/readout closure", "status": "UNSIGNED", "source": "VOE2766_4", "blocks": "claim-grade alpha silence after reduction", "next_required_input": "show loop/threshold/readout operations preserve parent image or add explicit finite priors"}))
    return rows


def build_gates() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "CG2766_0_sources", "gate": "source paths and needles valid", "passed": True, "claim_effect": "audit reproducible"}),
        nonclaim({"row_id": "CG2766_1_exhaustion_theorem", "gate": "visible operator-domain exhaustion derived", "passed": False, "claim_effect": "cannot ban independent F_Q^2 as theorem"}),
        nonclaim({"row_id": "CG2766_2_no_hidden_visible_hom", "gate": "hidden-to-visible coefficient morphisms absent", "passed": False, "claim_effect": "hidden alpha counterterms remain retained"}),
        nonclaim({"row_id": "CG2766_3_radiative_readout", "gate": "radiative/readout closure signed", "passed": False, "claim_effect": "tree-level alpha silence cannot be claimed"}),
        nonclaim({"row_id": "CG2766_4_product_priors_scoreable", "gate": "clock/WEP/R10 product predictions are sourced", "passed": False, "claim_effect": "product rows remain nonclaim except exact source-backed targets"}),
        nonclaim({"row_id": "CG2766_5_local_GR_Newton", "gate": "local GR/Newton constant-sector residual closed", "passed": False, "claim_effect": "no local-GR/Newton derivation claim from 2766"}),
    ]


def build_refusals() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "REF2766_0_exhaustion", "claim": "2766 proves visible operator-domain exhaustion", "allowed": False, "reason": "the exact contract is stated but not derived from parent MTS primitives", "blocking_rows": "VOE2766_1_parent_generator_domain;VOE2766_6_verdict"}),
        nonclaim({"row_id": "REF2766_1_alpha_zero", "claim": "b_alpha=0 or alpha is fully parent-owned", "allowed": False, "reason": "lambda_A, hidden f(I_hid), and radiative/readout counterterms remain legal", "blocking_rows": "OA2766_1_constant_counterterm;OA2766_3_radiative_counterterm;ACP2766_5_R2FR_policy"}),
        nonclaim({"row_id": "REF2766_2_transfer", "claim": "clock product bound transfers to WEP/R10/local-GR", "allowed": False, "reason": "tau/source/K_X maps are not parent-derived in one convention", "blocking_rows": "NTG2766_1_clock_to_WEP;NTG2766_2_clock_to_R10;PD2766_2_tau_WEP"}),
        nonclaim({"row_id": "REF2766_3_public_pass", "claim": "R10/WEP/clock/local-GR pass from 2766", "allowed": False, "reason": "2766 is a private branch discipline checkpoint, not a score or public claim", "blocking_rows": "CG2766_4_product_priors_scoreable;CG2766_5_local_GR_Newton"}),
    ]


def build_next() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "row_id": "NEXT2766_0_2767",
            "next_target": "2767-Y5-R2FR-alpha-product-prediction-stub-runner-and-required-inputs-under-AX1090.md",
            "script": "scripts/Y5_R2FR_alpha_product_prediction_stub_runner_and_required_inputs_under_AX1090_2767.py",
            "why": "the derivation route is now sharply localized: either prove visible operator-domain exhaustion, or test the retained alpha branch using exact product predictions. Since the theorem is not yet derived, the productive next step is a runner that refuses missing tau/source/K_X inputs instead of handwaving them.",
            "include": "product prediction schema, required tau_clock/tau_WEP/tau_R10/beta/K_X/Z_X inputs, no-transfer enforcement, exact refusal modes, no claim flags",
            "exclude": "standalone b_alpha claim, guessed tau=1, cancellation, public WEP/R10/local-GR pass, GitHub, formalization-workbench edits",
        })
    ]


def copy_branch_outputs(
    exhaustion: list[dict[str, Any]],
    prior: list[dict[str, Any]],
    product_pack: list[dict[str, Any]],
    transfer: list[dict[str, Any]],
    debts: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    beta_rows = prior + product_pack + transfer
    microscope_rows = [row for row in product_pack if "WEP" in str(row.get("arena", ""))] + transfer + debts
    specs = [
        ("BR2766_0_exhaustion_queue", "exhaustion", exhaustion, OUTPUTS["exhaustion"], BRANCH_OUTPUTS["exhaustion_queue"], "visible operator-domain theorem attempt"),
        ("BR2766_1_prior_queue", "prior", prior, OUTPUTS["prior"], BRANCH_OUTPUTS["prior_queue"], "alpha counterterm prior branch"),
        ("BR2766_2_product_queue", "product_pack", product_pack, OUTPUTS["product_pack"], BRANCH_OUTPUTS["product_queue"], "alpha product-prior source pack"),
        ("BR2766_3_beta_doc", "beta_doc", beta_rows, OUTPUTS["prior"], BRANCH_OUTPUTS["beta_doc"], "beta/source-facing alpha prior copy"),
        ("BR2766_4_microscope_copy", "microscope", microscope_rows, OUTPUTS["product_pack"], BRANCH_OUTPUTS["microscope_copy"], "MICROSCOPE WEP product/non-transfer copy"),
        ("BR2766_5_next_queue", "next", next_rows, OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next alpha product-prediction runner target"),
    ]
    rows = []
    for copy_id, table_key, source_rows, source_table, copy_path, purpose in specs:
        write_csv(copy_path, source_rows)
        rows.append(nonclaim({
            "copy_id": copy_id,
            "table_key": table_key,
            "source_table": rel(source_table),
            "copy_path": rel(copy_path),
            "purpose": purpose,
            "exists": copy_path.exists(),
            "row_count": csv_row_count(copy_path) if copy_path.exists() else 0,
        }))
    return rows


def generated_files_under_work() -> bool:
    generated = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
    return all(WORK in path.parents or path == WORK for path in generated)


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and path.stat().st_mtime > RUN_STARTED_UTC.timestamp():
            return False
    return True


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if str(row.get("valid_for_claim", "False")).lower() == "true":
                return False
            if str(row.get("claim_allowed", "False")).lower() == "true":
                return False
            if str(row.get("allowed", "False")).lower() == "true":
                return False
    return True


def remove_pycache() -> None:
    pycache = SCRIPTS / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def build_validation(rows_by_name: dict[str, list[dict[str, Any]]], csv_paths: list[Path]) -> list[dict[str, Any]]:
    sources = rows_by_name["sources"]
    exhaustion = rows_by_name["exhaustion"]
    algebra = rows_by_name["algebra"]
    prior = rows_by_name["prior"]
    product_pack = rows_by_name["product_pack"]
    transfer = rows_by_name["transfer"]
    debts = rows_by_name["debts"]
    gates = rows_by_name["gates"]
    refusal = rows_by_name["refusal"]
    next_rows = rows_by_name["next"]
    branches = rows_by_name["branches"]
    checks = [
        ("VAL2766_0_sources", all(row["exists"] and row["needles_found"] for row in sources), "every cited source path exists and needles are found"),
        ("VAL2766_1_exhaustion_not_derived", any(row["row_id"] == "VOE2766_6_verdict" and row["current_status"] == "REJECT_CURRENT_CLAIM_RETAIN_COUNTERTERM_PRIOR" for row in exhaustion), "visible operator-domain exhaustion remains a contract, not a derived theorem"),
        ("VAL2766_2_operator_algebra_retains_F2", any(row["row_id"] == "OA2766_1_constant_counterterm" and "ALLOWED" in row["status"] for row in algebra), "constant F_Q^2 counterterm remains allowed by ordinary symmetries"),
        ("VAL2766_3_counterterm_prior_retained", any(row["row_id"] == "ACP2766_5_R2FR_policy" and row["current_status"] == "RETAINED_NONCLAIM_BRANCH" for row in prior), "R2/f(R) alpha counterterm branch retained"),
        ("VAL2766_4_product_pack_contains_clock_WEP_R10", all(any(row["row_id"] == required for row in product_pack) for required in ["APP2766_0_clock_YbE3E2", "APP2766_2_WEP_alpha_Coulomb", "APP2766_4_R10_finite_alpha"]), "clock, WEP, and R10 product rows are present"),
        ("VAL2766_5_transfer_gates_block", all(row["gate_pass"] is False for row in transfer), "all transfer gates remain blocked"),
        ("VAL2766_6_projection_debts_present", all(any(row["row_id"] == required for row in debts) for required in ["PD2766_0_tau_clock", "PD2766_2_tau_WEP", "PD2766_3_tau_R10", "PD2766_5_visible_operator_universal_property"]), "tau/source/operator projection debts are explicit"),
        ("VAL2766_7_claim_gates_block", all(row["passed"] is False for row in gates if row["row_id"] != "CG2766_0_sources"), "all physics claim gates remain blocked"),
        ("VAL2766_8_refusals_block", all(row["allowed"] is False for row in refusal), "refusal runner blocks premature claims"),
        ("VAL2766_9_next", any(row["row_id"] == "NEXT2766_0_2767" and "alpha-product-prediction" in row["next_target"] for row in next_rows), "next target selected"),
        ("VAL2766_10_branch_outputs", all(row["exists"] and int(row["row_count"]) > 0 for row in branches), "branch copies exist and contain rows"),
        ("VAL2766_11_csv_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2766_12_no_claim_flags", no_claim_flags(rows_by_name), "no generated row is valid_for_claim=true/claim_allowed=true/allowed=true"),
        ("VAL2766_13_generated_under_post_checkpoint", generated_files_under_work(), "all generated outputs are under post-checkpoint-work"),
        ("VAL2766_14_formalization_untouched", formalization_untouched(), "formalization-workbench modified-file count remains zero during this run"),
        ("VAL2766_15_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    rows = [{"validation_id": check_id, "passed": passed, "detail": detail, "timestamp_utc": ts()} for check_id, passed, detail in checks]
    rows.append({
        "validation_id": "VAL2766_OVERALL",
        "passed": all(row["passed"] for row in rows),
        "detail": "2766 states the visible operator-domain exhaustion contract in the current R2/f(R) branch, rejects it as a derived claim because parent-generator exactness, no-hidden-visible Hom, and radiative/readout closure are unsigned, retains the alpha counterterm/product-prior branch, blocks cross-arena transfers, and selects an alpha product-prediction refusal runner as the next target.",
        "timestamp_utc": ts(),
    })
    return rows


def build_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> str:
    return "\n\n".join([
        "# 2766 - Y5 R2/f(R): Visible Operator-Domain Exhaustion Or Alpha Counterterm Prior Under AX1090",
        "## Private Verdict\n\nThis is the coupling choke point, cleanly exposed. The exact contract we would love to prove is `Allowed[S_vis]=Image(ParentGenerate[...])`: every visible kinetic/coupling coefficient must descend from the parent MTS action, with no extra local visible operator algebra.\n\nThat contract is precise, but it is not derived yet. Ordinary covariance and U(1) gauge symmetry still allow `lambda_A F_Q^2`; a surviving hidden invariant can allow `f(I_hid)F_Q^2`; and loops/readout maps can regenerate alpha-sensitive coefficients. So 2766 does **not** prove alpha silence or local GR. It keeps the theory honest by retaining the alpha counterterm/product-prior branch.",
        "## Source Register\n\n" + markdown_table(rows_by_name["sources"], ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"]),
        "## Visible Operator-Domain Exhaustion Attempt\n\n" + markdown_table(rows_by_name["exhaustion"], ["row_id", "claim_piece", "mathematical_form", "current_status", "proof_or_blocker", "if_signed", "if_unsigned", "valid_for_claim"]),
        "## Allowed Operator Algebra\n\n" + markdown_table(rows_by_name["algebra"], ["row_id", "operator_class", "example", "status", "ordinary_symmetry_result", "claim_effect", "retained_if_unsigned", "valid_for_claim"]),
        "## Alpha Counterterm Prior Branch\n\n" + markdown_table(rows_by_name["prior"], ["row_id", "source_row", "quantity", "definition", "current_status", "observable_link", "source_or_bound", "valid_for_claim"]),
        "## Alpha Product-Prior Source Pack\n\n" + markdown_table(rows_by_name["product_pack"], ["row_id", "source_row", "arena", "product_symbol", "bound_or_target", "units", "score_rule", "missing_for_standalone", "score_ready", "valid_for_claim"]),
        "## No-Transfer Gates\n\n" + markdown_table(rows_by_name["transfer"], ["row_id", "source_row", "forbidden_transfer", "reason", "allowed_use", "missing_to_unlock", "gate_pass", "valid_for_claim"]),
        "## Projection Debt Ledger\n\n" + markdown_table(rows_by_name["debts"], ["row_id", "source_row", "projection", "status", "source", "blocks", "next_required_input", "valid_for_claim"]),
        "## Claim Gates\n\n" + markdown_table(rows_by_name["gates"], ["row_id", "gate", "passed", "claim_effect", "valid_for_claim"]),
        "## Refusal Runner\n\n" + markdown_table(rows_by_name["refusal"], ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"]),
        "## Next Target\n\n" + markdown_table(rows_by_name["next"], ["row_id", "next_target", "script", "why", "include", "exclude", "valid_for_claim"]),
        "## Branch Copies\n\n" + markdown_table(rows_by_name["branches"], ["copy_id", "table_key", "source_table", "copy_path", "purpose", "exists", "row_count", "valid_for_claim"]),
        "## Validation\n\n" + markdown_table(rows_by_name["validation"], ["validation_id", "passed", "detail", "timestamp_utc"]),
        "## Plain-English Read\n\nThe win here is not that the coupling is solved; it is that the coupling problem is no longer fog. The theory now has a named gate: either prove the visible action has no extra coefficient slots, or stop pretending zero and build exact product predictions against clock/WEP/R10 data. That is a good place to be: painful, but sharp.",
        "",
    ])


def main() -> None:
    ensure_dirs()
    inputs = load_inputs()
    sources = build_sources()
    exhaustion = build_exhaustion_rows(inputs)
    algebra = build_algebra_rows(inputs)
    prior = build_prior_rows(inputs)
    product_pack = build_product_pack(inputs)
    transfer = build_transfer_rows(inputs)
    debts = build_debt_rows(inputs)
    gates = build_gates()
    refusal = build_refusals()
    next_rows = build_next()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["exhaustion"], exhaustion)
    write_csv(OUTPUTS["algebra"], algebra)
    write_csv(OUTPUTS["prior"], prior)
    write_csv(OUTPUTS["product_pack"], product_pack)
    write_csv(OUTPUTS["transfer"], transfer)
    write_csv(OUTPUTS["debts"], debts)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["refusal"], refusal)
    write_csv(OUTPUTS["next"], next_rows)

    branches = copy_branch_outputs(exhaustion, prior, product_pack, transfer, debts, next_rows)
    write_csv(OUTPUTS["branches"], branches)
    remove_pycache()

    rows_by_name = {
        "sources": sources,
        "exhaustion": exhaustion,
        "algebra": algebra,
        "prior": prior,
        "product_pack": product_pack,
        "transfer": transfer,
        "debts": debts,
        "gates": gates,
        "refusal": refusal,
        "next": next_rows,
        "branches": branches,
    }
    csv_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    validation = build_validation(rows_by_name, csv_paths)
    rows_by_name["validation"] = validation
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(build_doc(rows_by_name), encoding="utf-8")
    remove_pycache()

    overall = next(row for row in validation if row["validation_id"] == "VAL2766_OVERALL")
    print(f"2766 complete: overall={overall['passed']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
