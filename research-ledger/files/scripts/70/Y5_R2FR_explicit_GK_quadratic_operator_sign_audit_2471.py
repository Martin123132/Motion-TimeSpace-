from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_EXPLICIT_GK_QUADRATIC_OPERATOR_SIGN_AUDIT_2471"
CHECKPOINT_ID = "2471"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"

DOC = ROOT / "2471-Y5-R2FR-explicit-GK-quadratic-operator-sign-audit.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_GK_OPERATOR_2471_SOURCE_REGISTER.csv",
    "operator_ansatz": OUT / "P8_Y5_GK_OPERATOR_2471_OPERATOR_ANSATZ.csv",
    "dimension_sign_table": OUT / "P8_Y5_GK_OPERATOR_2471_DIMENSION_SIGN_TABLE.csv",
    "coercivity_audit": OUT / "P8_Y5_GK_OPERATOR_2471_COERCIVITY_AUDIT.csv",
    "ghost_tachyon_checks": OUT / "P8_Y5_GK_OPERATOR_2471_GHOST_TACHYON_CHECKS.csv",
    "nohair_eligibility": OUT / "P8_Y5_GK_OPERATOR_2471_NOHAIR_ELIGIBILITY.csv",
    "stress_bound_branch": OUT / "P8_Y5_GK_OPERATOR_2471_STRESS_BOUND_BRANCH.csv",
    "promotion_verdict": OUT / "P8_Y5_GK_OPERATOR_2471_PROMOTION_VERDICT.csv",
    "claim_gates": OUT / "P8_Y5_GK_OPERATOR_2471_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_GK_OPERATOR_2471_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_GK_OPERATOR_2471_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_GK_OPERATOR_2471_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2471_VALIDATION.csv",
}

COPY_TARGETS = {
    "operator_ansatz_contract": QUEUE / "JR2471_GK_QUADRATIC_OPERATOR_ANSATZ_NONCLAIM.csv",
    "coercivity_contract": LOCAL_BOUNDS / "GK_quadratic_coercivity_contract_2471_NONCLAIM.csv",
    "stress_bound_branch": LOCAL_BOUNDS / "GK_operator_stress_bound_branch_2471_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2471_00_2470_doc",
        "source_path": ROOT / "2470-Y5-R2FR-GK-vacuum-no-hair-positivity-or-stress-bound.md",
        "needles": ["POS2470_1_quadratic_form", "NH2470_6_current_status", "NEXT2470_0_selected", "VAL2470_OVERALL"],
        "role": "handoff selecting explicit operator/sign audit",
    },
    {
        "source_id": "SRC2471_01_2470_positivity",
        "source_path": OUT / "P8_Y5_GK_NOHAIR_2470_POSITIVITY_CLAUSES.csv",
        "needles": ["POS2470_1_quadratic_form", "POS2470_2_cross_term_bound", "POS2470_6_parent_sign"],
        "role": "positivity clauses to instantiate",
    },
    {
        "source_id": "SRC2471_02_2470_nohair",
        "source_path": OUT / "P8_Y5_GK_NOHAIR_2470_NOHAIR_PROOF_ATTEMPT.csv",
        "needles": ["NH2470_2_energy_identity", "NH2470_5_stress_zero", "NOT_PROMOTED"],
        "role": "no-hair proof method and nonpromotion",
    },
    {
        "source_id": "SRC2471_03_2465_dimension",
        "source_path": OUT / "P8_Y5_PARENT_ACTION_2465_DIMENSION_AUDIT.csv",
        "needles": ["DIM2465_3_viable_branch", "DIM2465_4_Khat_dimension", "MISSING_PARENT_SCALE"],
        "role": "dimension branch for operator coefficients",
    },
    {
        "source_id": "SRC2471_04_2464_candidate_action",
        "source_path": OUT / "P8_Y5_PARENT_ACTION_2464_CANDIDATE_ACTIONS.csv",
        "needles": ["ACT2464_A_vertical_generator_current_law", "A_nu nabla^nu Gamma_eff", "L_Gamma"],
        "role": "action containing A-Gamma cross coupling",
    },
    {
        "source_id": "SRC2471_05_2469_ppn",
        "source_path": OUT / "P8_Y5_GK_STRESS_2469_PPN_RESIDUAL_LEDGER.csv",
        "needles": ["PPN2469_2_hair_bound", "DEFER_NUMERIC_TEST"],
        "role": "stress-bound fallback and future local tests",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row() -> dict[str, Any]:
    return {"timestamp_utc": stamp(), "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID, "valid_for_claim": False, "claim_allowed": False}


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    columns: list[str] = []
    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def source_register() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCES:
        path = Path(source["source_path"])
        exists = path.exists()
        missing: list[str] = []
        if exists:
            text = read_text(path)
            missing = [needle for needle in source["needles"] if needle not in text]
        else:
            missing = list(source["needles"])
        rows.append({**base_row(), "source_id": source["source_id"], "source_path": str(path), "exists": exists, "missing_needles": ";".join(missing), "source_pass": exists and not missing, "role": source["role"]})
    return rows


def operator_ansatz_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "OP2471_0_stationary_energy",
            "E_GK=int_Omega sqrt(h)[0.5 Z_A D_i A_j D^i A^j + 0.5 m_A2 A_i A^i + 0.5 Z_G D_i gamma D^i gamma + 0.5 m_G2 gamma^2 + c_AG A^i D_i gamma]",
            "gamma:=Gamma_eff-Gamma_0; stationary exterior energy functional, not full Lorentzian quantum action",
            "minimal explicit operator for no-hair audit",
            "CANDIDATE_ONLY",
        ),
        (
            "OP2471_1_displacement",
            "K_hat^{ij}=Z_A D^i A^j plus possible symmetric/projected refinements",
            "matches K_hat as derivative of L_K with respect to D_i A_j",
            "keeps q_loc Euler route compatible",
            "CANDIDATE_ONLY",
        ),
        (
            "OP2471_2_cross_origin",
            "c_AG A^i D_i gamma is the stationary energy version of A_nu nabla^nu Gamma_eff",
            "cross term is required by the q_loc current-law action",
            "must be small enough or completed by parent terms to avoid hair",
            "RISK_TERM",
        ),
        (
            "OP2471_3_vacuum_normalization",
            "L_Gamma has gamma=0 as stationary point and zero local vacuum energy after fixed parent subtraction",
            "avoids local cosmological stress",
            "required for T_GK silence",
            "REQUIRED_NOT_SOURCED",
        ),
        (
            "OP2471_4_scope",
            "operator is a minimal audit ansatz, not a source-backed MTS action",
            "coefficients are not yet parent-signed",
            "cannot promote local GR",
            "NONCLAIM",
        ),
    ]
    return [{**base_row(), "operator_id": i, "operator_clause": c, "basis": b, "effect": e, "status": st} for i, c, b, e, st in rows]


def dimension_sign_rows() -> list[dict[str, Any]]:
    rows = [
        ("DS2471_0_A", "A_i", "M", "from 2465 ordinary-current branch", "compatible"),
        ("DS2471_1_gamma", "gamma=Gamma_eff-Gamma_0", "M^2", "from 2465 curvature/compression branch", "compatible"),
        ("DS2471_2_ZA", "Z_A", "dimensionless", "D A has M^2 so (D A)^2 has M^4", "requires Z_A positive"),
        ("DS2471_3_mA", "m_A2", "M^2", "m_A2 A^2 has M^4", "requires m_A2 nonnegative for no tachyon"),
        ("DS2471_4_ZG", "Z_G", "M^-2", "D gamma has M^3 so Z_G(D gamma)^2 has M^4", "requires Z_G positive and parent scale"),
        ("DS2471_5_mG", "m_G2", "dimensionless", "m_G2 gamma^2 has M^4", "requires m_G2 positive in exterior"),
        ("DS2471_6_cAG", "c_AG", "M", "A D gamma has M^4 when c_AG is dimensionless? audit flags convention dependence", "needs parent normalization convention"),
        ("DS2471_7_parent_scale", "operator scale", "varies by convention", "Z_G or c_AG carries scale depending on Gamma normalization", "MISSING_PARENT_SCALE"),
    ]
    return [{**base_row(), "dimension_id": i, "symbol": s, "dimension_branch": dim, "basis": b, "sign_requirement": req} for i, s, dim, b, req in rows]


def coercivity_rows() -> list[dict[str, Any]]:
    rows = [
        ("COER2471_0_positive_blocks", "Z_A>0, Z_G>0, m_A2>0, m_G2>=0", "base positive quadratic energy", "REQUIRED_NOT_DERIVED"),
        ("COER2471_1_cross_bound", "c_AG^2 < m_A2 Z_G in a normalized stationary energy convention", "Schur/Young bound for A dot D gamma cross term", "PLAUSIBLE_IF_PARENT_SIGNED"),
        ("COER2471_2_eta_form", "abs(cross) <= eta E_positive with eta<1", "coordinate-free way to state the same condition", "PLAUSIBLE_IF_PARENT_SIGNED"),
        ("COER2471_3_massless_gamma_warning", "if m_G2=0 then constant gamma zero-mode must be removed by boundary/vacuum normalization", "otherwise vacuum hair can survive", "BOUNDARY_REQUIRED"),
        ("COER2471_4_massless_A_warning", "if m_A2=0 then transverse/harmonic A hair can survive unless gauge/topology removes it", "Maxwell-like no-hair requires gauge and boundary theorem", "TOPOLOGY_REQUIRED"),
        ("COER2471_5_current_status", "current corpus has no parent-signed values or inequalities for Z_A,Z_G,m_A2,m_G2,c_AG", "no-hair eligibility remains unproved", "NOT_PROMOTED"),
    ]
    return [{**base_row(), "coercivity_id": i, "condition": c, "basis": b, "status": st} for i, c, b, st in rows]


def ghost_tachyon_rows() -> list[dict[str, Any]]:
    rows = [
        ("GT2471_0_A_gradient", "Z_A>0", "negative Z_A is a ghost/negative energy gradient", "REQUIRED"),
        ("GT2471_1_gamma_gradient", "Z_G>0", "negative Z_G is a ghost/negative energy scalar-gradient branch", "REQUIRED"),
        ("GT2471_2_A_mass", "m_A2>=0", "negative m_A2 gives tachyonic vector hair", "REQUIRED"),
        ("GT2471_3_gamma_mass", "m_G2>=0 with boundary removal if zero", "negative m_G2 gives scalar/compression tachyon", "REQUIRED"),
        ("GT2471_4_cross", "c_AG does not violate coercivity bound", "too-large cross term destabilizes exterior", "REQUIRED"),
        ("GT2471_5_higher_derivative", "no second-time-derivative Ostrogradsky terms introduced in Lorentzian parent action", "stationary energy audit is not full dynamical proof", "MISSING_FULL_LORENTZIAN_CHECK"),
        ("GT2471_6_current_verdict", "ghost/tachyon safety is plausible only under chosen signs", "parent origin missing", "NONCLAIM"),
    ]
    return [{**base_row(), "check_id": i, "check": c, "reason": r, "status": st} for i, c, r, st in rows]


def nohair_eligibility_rows() -> list[dict[str, Any]]:
    rows = [
        ("NHG2471_0_operator", "minimal stationary quadratic operator exists", "OP2471_0", "PASS_AS_ANSATZ"),
        ("NHG2471_1_coercive", "coercivity condition can be stated", "COER2471_0-2", "PASS_AS_INEQUALITY"),
        ("NHG2471_2_parent_signed", "coefficients are parent-derived and fixed", "no current source", "FAIL_CURRENT_CLAIM"),
        ("NHG2471_3_boundary_topology", "boundary and topology remove zero modes/harmonic hair", "not handled by sign audit", "PENDING"),
        ("NHG2471_4_lorentzian_stability", "full dynamical stability/ghost audit in parent action", "stationary audit insufficient", "PENDING"),
        ("NHG2471_5_eligibility", "no-hair is mathematically plausible but not promotable", "sign inequalities written, parent proof absent", "PLAUSIBLE_NOT_PROVED"),
    ]
    return [{**base_row(), "eligibility_id": i, "criterion": c, "evidence": e, "status": st} for i, c, e, st in rows]


def stress_bound_branch_rows() -> list[dict[str, Any]]:
    rows = [
        ("SBB2471_0_defect", "negative_mode_defect=max(0,c_AG^2-m_A2 Z_G) plus unsigned boundary/topology defects", "quantifies failure of coercivity", "BOUND_INPUT"),
        ("SBB2471_1_energy_bound", "E_GK <= C_B boundary_flux + C_S source_tail + C_X negative_mode_defect", "fallback if exact no-hair fails", "BOUND_FORM_ONLY"),
        ("SBB2471_2_metric_bound", "delta_PPN <= C_metric C_T E_GK plus vacuum and retained-sector terms", "links stress energy to local tests", "BOUND_FORM_ONLY"),
        ("SBB2471_3_data_gate", "R10/PPN/clock/orbital tests need numeric C_B,C_S,C_X,C_metric and arena projections", "future empirical pass", "MISSING_NUMERIC_INPUTS"),
        ("SBB2471_4_claim", "stress-bound branch is not local GR unless all bounds sit below local arenas", "claim discipline", "NONCLAIM"),
    ]
    return [{**base_row(), "bound_branch_id": i, "bound_clause": c, "basis": b, "status": st} for i, c, b, st in rows]


def promotion_verdict_rows() -> list[dict[str, Any]]:
    rows = [
        ("PV2471_0_operator", "Is an explicit GK quadratic operator written?", "YES_AS_ANSATZ", "minimal stationary operator recorded", "progress"),
        ("PV2471_1_signs", "Are sign/coercivity conditions known?", "YES_AS_CONDITIONS", "Z and mass signs plus cross bound stated", "contract only"),
        ("PV2471_2_parent_origin", "Are the signs parent-derived?", "NO", "current corpus lacks source for coefficients", "blocks promotion"),
        ("PV2471_3_nohair", "Is no-hair plausible?", "PLAUSIBLE_NOT_PROVED", "coercive branch exists if parent signs and boundary/topology close", "next target"),
        ("PV2471_4_overall", "Overall 2471 verdict", "OPERATOR_SIGN_CONTRACT_WRITTEN_PARENT_SIGN_AND_BOUNDARY_PENDING", "no local GR claim; next gate is parent sign plus boundary topology", "continue"),
    ]
    return [{**base_row(), "verdict_id": i, "question": q, "result": r, "evidence": e, "effect": eff} for i, q, r, e, eff in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2471_0_operator_ansatz", "Explicit stationary GK quadratic operator is written.", "PASS_AS_ANSATZ", "operator/sign table exists", True, False),
        ("GATE2471_1_coercivity_contract", "Coercivity/no-hair sign conditions are stated.", "PASS_AS_CONTRACT", "cross-term bound and sign requirements written", True, False),
        ("GATE2471_2_parent_sign", "Parent action fixes the required signs.", "BLOCKED", "coefficients are not sourced", False, False),
        ("GATE2471_3_nohair_proved", "No-hair theorem is proved for current MTS.", "BLOCKED", "boundary/topology and parent signs remain pending", False, False),
        ("GATE2471_4_local_GR_PPN", "local GR/PPN branch passes.", "BLOCKED", "operator is nonclaim and residual coefficients missing", False, False),
        ("GATE2471_5_no_GitHub", "No public/GitHub update.", "PASS_GUARDRAIL", "private derivation checkpoint only", True, False),
    ]
    return [{**base_row(), "gate_id": i, "claim": c, "gate_status": st, "reason": r, "gate_pass": gp, "claim_allowed": ca} for i, c, st, r, gp, ca in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2471_0_keep_operator", "Keep the explicit quadratic operator as the active no-hair ansatz.", "it gives concrete sign/coercivity gates instead of vague positivity", "use as next derivation scaffold"),
        ("DEC2471_1_no_promotion", "Do not promote no-hair or local GR.", "signs and boundary/topology are not parent-derived", "claim gates stay blocked"),
        ("DEC2471_2_next_gate", "Attack parent sign origin plus boundary/topology no-hair next.", "coercivity alone is not enough if signs are designer-chosen or hair survives", "2472 selected"),
    ]
    return [{**base_row(), "decision_id": i, "decision": d, "reason": r, "effect": e} for i, d, r, e in rows]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            **base_row(),
            "route_id": "NEXT2471_0_selected",
            "selection_status": "selected",
            "target_file": "2472-Y5-R2FR-parent-sign-origin-and-boundary-topology-nohair-gate.md",
            "target_script": "scripts/Y5_R2FR_parent_sign_origin_and_boundary_topology_nohair_gate_2472.py",
            "task": "try to parent-sign the GK quadratic coefficients and close boundary/topology no-hair; if not possible, demote the local metric branch to stress-bound only",
            "acceptance_target": "parent sign source audit, boundary condition ledger, topology/harmonic hair audit, no-hair eligibility verdict, and claim gates",
            "guardrails": "no local-GR claim; no fitted GM; no M_H_ref reuse; no plateau axiom; no GitHub",
        }
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    for target in COPY_TARGETS.values():
        target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(OUTPUTS["operator_ansatz"], COPY_TARGETS["operator_ansatz_contract"])
    shutil.copyfile(OUTPUTS["coercivity_audit"], COPY_TARGETS["coercivity_contract"])
    shutil.copyfile(OUTPUTS["stress_bound_branch"], COPY_TARGETS["stress_bound_branch"])
    source_map = {
        "operator_ansatz_contract": OUTPUTS["operator_ansatz"],
        "coercivity_contract": OUTPUTS["coercivity_audit"],
        "stress_bound_branch": OUTPUTS["stress_bound_branch"],
    }
    return [{**base_row(), "copy_id": cid, "source_path": str(source_map[cid]), "target_path": str(target), "source_exists": source_map[cid].exists(), "target_exists": target.exists()} for cid, target in COPY_TARGETS.items()]


def csv_row_count(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as handle:
        return len(list(csv.DictReader(handle)))


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, status: bool, notes: str, detail: str = "") -> None:
        rows.append({**base_row(), "check_id": check_id, "status": "PASS" if status else "FAIL", "notes": notes, "detail": detail})

    add("VAL2471_00_sources_exist", all(row["source_pass"] is True or str(row["source_pass"]) == "True" for row in data["sources"]), "all cited source paths exist and needles are present")
    add("VAL2471_01_operator_written", any(row["operator_id"] == "OP2471_0_stationary_energy" for row in data["operator"]), "explicit stationary operator ansatz written")
    add("VAL2471_02_sign_table", len(data["dimensions"]) >= 8, "dimension/sign table written")
    add("VAL2471_03_cross_bound", any(row["coercivity_id"] == "COER2471_1_cross_bound" and row["status"] == "PLAUSIBLE_IF_PARENT_SIGNED" for row in data["coercivity"]), "cross-term coercivity bound written")
    add("VAL2471_04_ghost_checks", len(data["ghosts"]) >= 7 and any(row["check_id"] == "GT2471_5_higher_derivative" for row in data["ghosts"]), "ghost/tachyon checks written")
    add("VAL2471_05_nohair_not_proved", any(row["eligibility_id"] == "NHG2471_5_eligibility" and row["status"] == "PLAUSIBLE_NOT_PROVED" for row in data["eligibility"]), "no-hair plausibility not promoted")
    add("VAL2471_06_bound_branch", any(row["bound_branch_id"] == "SBB2471_2_metric_bound" for row in data["bounds"]), "stress-bound branch retained")
    add("VAL2471_07_overall_nonclaim", any(row["verdict_id"] == "PV2471_4_overall" and row["result"] == "OPERATOR_SIGN_CONTRACT_WRITTEN_PARENT_SIGN_AND_BOUNDARY_PENDING" for row in data["verdicts"]), "overall verdict is nonclaim")
    add("VAL2471_08_claim_gates_safe", all(row["claim_allowed"] is False for row in data["gates"]), "no claim gate allows local-GR/PPN claim")
    add("VAL2471_09_next_target_written", bool(data["next"]) and data["next"][0]["route_id"] == "NEXT2471_0_selected", "2472 parent sign/boundary topology target selected")
    add("VAL2471_10_branch_copies", all(row["source_exists"] and row["target_exists"] for row in data["copies"]), "nonclaim branch copies exist")
    markers = ("2471-Y5", "P8_Y5_GK_OPERATOR_2471", "P8_Y5_BRR545_2471", "JR2471")
    formal_hits = [path for path in FORMALIZATION.rglob("*") if path.is_file() and any(marker in path.name for marker in markers)] if FORMALIZATION.exists() else []
    add("VAL2471_11_no_formalization_artifacts", not formal_hits, "no 2471 artifacts were written to formalization-workbench", ";".join(str(path) for path in formal_hits))
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        try:
            count = csv_row_count(path)
            add(f"VAL2471_CSV_{path.stem}", count > 0, f"CSV parses with {count} rows", str(path))
        except Exception as exc:
            add(f"VAL2471_CSV_{path.stem}", False, f"CSV parse failed: {exc}", str(path))
    for copy_id, path in COPY_TARGETS.items():
        try:
            count = csv_row_count(path)
            add(f"VAL2471_COPY_CSV_{copy_id}", count > 0, f"copy CSV parses with {count} rows", str(path))
        except Exception as exc:
            add(f"VAL2471_COPY_CSV_{copy_id}", False, f"copy CSV parse failed: {exc}", str(path))
    add("VAL2471_OVERALL", all(row["status"] == "PASS" for row in rows), "2471 writes explicit GK quadratic operator signs, keeps no-hair nonclaim, and selects parent-sign/boundary gate")
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2471 Y5 R2FR Explicit GK Quadratic Operator Sign Audit",
        "",
        "**Status:** explicit operator/sign contract written, not promoted. A minimal stationary GK energy can be made coercive if `Z_A>0`, `Z_G>0`, mass/gap terms are nonnegative, and the `A dot grad Gamma` cross-coupling obeys a Schur/Young bound. That makes no-hair plausible, but only as a parent-signed contract.",
        "",
        "**Important caution:** the sign choices are not yet derived from MTS. If they are designer-chosen, the local-GR branch becomes post-hoc. The next gate must either parent-sign these coefficients and close boundary/topology hair, or demote the branch to stress-bound only.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Operator Ansatz",
        markdown_table(data["operator"], ["operator_id", "operator_clause", "basis", "effect", "status"]),
        "",
        "## Dimension And Sign Table",
        markdown_table(data["dimensions"], ["dimension_id", "symbol", "dimension_branch", "basis", "sign_requirement"]),
        "",
        "## Coercivity Audit",
        markdown_table(data["coercivity"], ["coercivity_id", "condition", "basis", "status"]),
        "",
        "## Ghost And Tachyon Checks",
        markdown_table(data["ghosts"], ["check_id", "check", "reason", "status"]),
        "",
        "## No-hair Eligibility",
        markdown_table(data["eligibility"], ["eligibility_id", "criterion", "evidence", "status"]),
        "",
        "## Stress Bound Branch",
        markdown_table(data["bounds"], ["bound_branch_id", "bound_clause", "basis", "status"]),
        "",
        "## Promotion Verdict",
        markdown_table(data["verdicts"], ["verdict_id", "question", "result", "evidence", "effect"]),
        "",
        "## Claim Gates",
        markdown_table(data["gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    data = {
        "sources": source_register(),
        "operator": operator_ansatz_rows(),
        "dimensions": dimension_sign_rows(),
        "coercivity": coercivity_rows(),
        "ghosts": ghost_tachyon_rows(),
        "eligibility": nohair_eligibility_rows(),
        "bounds": stress_bound_branch_rows(),
        "verdicts": promotion_verdict_rows(),
        "gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }
    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["operator_ansatz"], data["operator"])
    write_csv(OUTPUTS["dimension_sign_table"], data["dimensions"])
    write_csv(OUTPUTS["coercivity_audit"], data["coercivity"])
    write_csv(OUTPUTS["ghost_tachyon_checks"], data["ghosts"])
    write_csv(OUTPUTS["nohair_eligibility"], data["eligibility"])
    write_csv(OUTPUTS["stress_bound_branch"], data["bounds"])
    write_csv(OUTPUTS["promotion_verdict"], data["verdicts"])
    write_csv(OUTPUTS["claim_gates"], data["gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])
    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])
    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)
    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
