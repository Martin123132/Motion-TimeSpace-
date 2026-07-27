from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1692"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "1692-Y5-R2FR-EH-source-owner-or-R11-beta-vector-current-branch.md"

SOURCE_FILES = {
    "1691_doc": ROOT / "1691-Y5-R2FR-PPN-residual-vector-or-qRhat-source-row.md",
    "1691_validation": OUT / "P8_Y5_BRR545_1691_VALIDATION.csv",
    "1691_next": OUT / "P8_Y5_PARENT_QLOC_1691_NEXT_TARGET.csv",
    "1585_owner": OUT / "P8_Y5_PARENT_QLOC_1585_EH_SOURCE_OWNER_CONTRACT.csv",
    "1585_beta_residual": OUT / "P8_Y5_PARENT_QLOC_1585_BETA_RESIDUAL_LEDGER.csv",
    "1586_doc": ROOT / "1586-Y5-parent-minimality-no-extra-sector-signature-or-R11-beta-vector-fill.md",
    "1586_validation": OUT / "P8_Y5_BRR545_1586_VALIDATION.csv",
    "1587_nohair": OUT / "P8_Y5_PARENT_QLOC_1587_R2FR_RICCIWEYL_NOHAIR_ATTEMPT.csv",
    "1587_fill": OUT / "P8_Y5_PARENT_QLOC_1587_FIRST_COMPONENT_FILL_ROWS.csv",
    "1589_law": OUT / "P8_Y5_PARENT_QLOC_1589_EFFECTIVE_COEFFICIENT_LAW.csv",
    "1589_owner": OUT / "P8_Y5_PARENT_QLOC_1589_MEMORY_FIBRE_OWNER_STATUS.csv",
    "1590_doc": ROOT / "1590-Y5-R2FR-Gamma-Khat-Ploc-owner-bundle-or-cR2-finite-coefficient-row.md",
    "1590_validation": OUT / "P8_Y5_BRR545_1590_VALIDATION.csv",
    "1590_owner": OUT / "P8_Y5_PARENT_QLOC_1590_OWNER_BUNDLE_SYNTHESIS.csv",
    "1590_fixed_l0": OUT / "P8_Y5_PARENT_QLOC_1590_FIXED_L0_DOUBLE_ZERO_CONTRACT_GATE.csv",
    "1590_cr2": OUT / "P8_Y5_PARENT_QLOC_1590_CR2_COEFFICIENT_IMPLICATIONS.csv",
    "1590_qgamma": OUT / "P8_Y5_PARENT_QLOC_1590_QGAMMA_QNORM_RUNNER_BRIDGE.csv",
    "1590_next": OUT / "P8_Y5_PARENT_QLOC_1590_NEXT_TARGET.csv",
}

NEEDLES = {
    "1691_doc": ["gamma is not GR", "EH/source-owner or R11 beta-vector current-branch gate"],
    "1691_validation": ["VAL1691_OVERALL", "PASS"],
    "1691_next": ["NEXT1691_0_primary", "EH-source-owner"],
    "1585_owner": ["OWN1585_5_verdict", "FAIL_CURRENT_CLAIM_PARENT_OWNER_NOT_DERIVED"],
    "1585_beta_residual": ["BRL1585_7_total_no_cancellation", "NOT_RUN_COMPONENTS_MISSING"],
    "1586_doc": ["parent minimality/no-extra-sector would be powerful", "every R11 beta component must be theorem-zero"],
    "1586_validation": ["VAL1586_OVERALL", "PASS"],
    "1587_nohair": ["NH1587_6_verdict", "FAIL_CURRENT_CLAIM_FIRST_COMPONENTS_NOT_DERIVED"],
    "1587_fill": ["FC1587_0_R2FR", "FC1587_1_RicciWeyl"],
    "1589_law": ["LAW1589_0_integrated_hidden_modes", "c_R2_eff"],
    "1589_owner": ["OWN1589_4_response_bundle", "MISSING_GAMMA_KHAT_PLOC_OWNER"],
    "1590_doc": ["FIXED_L0_DOUBLE_ZERO_IS_THE_BEST_CURRENT_LOCAL_BRANCH", "Q_norm"],
    "1590_validation": ["VAL1590_OVERALL", "PASS"],
    "1590_owner": ["OBS1590_5_owner_verdict", "OWNER_BUNDLE_NOT_CLOSED_CURRENT_CORPUS"],
    "1590_fixed_l0": ["FLG1590_5_verdict", "ZERO_THEOREM_NOT_DERIVED"],
    "1590_cr2": ["CR2I1590_4_finite_row_trigger", "FINITE_ROW_REQUIRED_IF_RESIDUALS_RETAINED"],
    "1590_qgamma": ["QGB1590_0_symbolic_feed", "SYMBOLIC_CASSINI_BOUND_READY"],
    "1590_next": ["1591-Y5-R2FR-fixed-L0-cdb-memory-Qnorm-first-fill-or-cR2-bound-row.md", "first-fill Q_norm"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1692_SOURCE_REGISTER.csv"
OWNER_GATE = OUT / "P8_Y5_PARENT_QLOC_1692_EH_SOURCE_OWNER_GATE.csv"
R11_GATE = OUT / "P8_Y5_PARENT_QLOC_1692_R11_BETA_LEAKAGE_GATE.csv"
COEFF_BRIDGE = OUT / "P8_Y5_PARENT_QLOC_1692_CR2_QNORM_COEFFICIENT_BRIDGE.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1692_LOCAL_GR_OWNER_RUNNER.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1692_NEXT_TARGET.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1692_CLAIM_GATE.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1692_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    OWNER_GATE,
    R11_GATE,
    COEFF_BRIDGE,
    RUNNER,
    NEXT_TARGET,
    CLAIM_GATE,
]

CLAIM_CHECKED = [
    OWNER_GATE,
    R11_GATE,
    COEFF_BRIDGE,
    RUNNER,
    NEXT_TARGET,
    CLAIM_GATE,
]

COPY_TARGETS = {
    OWNER_GATE: [
        QUARANTINE / "EH_SOURCE_OWNER_GATE.csv",
        BRANCH_RESIDUALS / "R2FR_EH_source_owner_gate_1692.csv",
        QUEUE / "JR1692_EH_SOURCE_OWNER_GATE.csv",
    ],
    R11_GATE: [
        QUARANTINE / "R11_BETA_LEAKAGE_GATE.csv",
        BRANCH_RESIDUALS / "R2FR_R11_beta_leakage_gate_1692.csv",
        QUEUE / "JR1692_R11_BETA_LEAKAGE_GATE.csv",
    ],
    COEFF_BRIDGE: [
        QUARANTINE / "CR2_QNORM_COEFFICIENT_BRIDGE.csv",
        BRANCH_RESIDUALS / "R2FR_cR2_Qnorm_coefficient_bridge_1692.csv",
        QUEUE / "JR1692_CR2_QNORM_COEFFICIENT_BRIDGE.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_1692.csv",
        QUEUE / "JR1692_NEXT_TARGET.csv",
    ],
}


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def bool_cell(value: object) -> bool:
    return str(value).strip().lower() == "true"


def list_cell(values: list[object] | tuple[object, ...]) -> str:
    return ";".join(str(value) for value in values)


def markdown_table(rows: list[dict[str, object]], headers: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for key, path in SOURCE_FILES.items():
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles = NEEDLES[key]
        needles_present = exists and all(needle in text for needle in needles)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_key": key,
                "source_path": str(path),
                "exists": exists,
                "needles_present": needles_present,
                "required_needles": list_cell(needles),
                "use_in_1692": "EH source owner and R11 beta leakage current-branch gate",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def owner_gate_rows() -> list[dict[str, object]]:
    rows = [
        (
            "OWNG1692_0_single_parent_action",
            "one varied parent action owns observed geometry, EH-like operator, matter coupling, source normalization, boundary policy and residual sectors",
            "would prevent mixing imported GR with MTS source bookkeeping",
            "CONTRACT_WRITTEN_NOT_PARENT_SIGNED",
            "no single parent action currently signs all clauses",
        ),
        (
            "OWNG1692_1_EH_operator",
            "metric-only second-order EH-like exterior operator plus theorem-zero or bounded retained sectors",
            "would activate the one-parameter EH exterior beta=1 route",
            "MISSING_EH_ONLY_PARENT_SIGNATURE",
            "R11/non-EH operator families remain live",
        ),
        (
            "OWNG1692_2_universal_matter",
            "one observed coframe, universal Hilbert matter source, fixed constants and no marker/source weights",
            "would lock rods clocks photons sources and readout to one geometry",
            "COMMON_MATTER_UNSIGNED",
            "coframe/tau/matter descent/no-marker clauses are open",
        ),
        (
            "OWNG1692_3_measured_GM",
            "mu_EH equals observed source-normalized GM in the same Hilbert/source frame",
            "would make Newtonian denominator and PPN expansion use the same mass",
            "SOURCE_DENOMINATOR_MISSING",
            "GM/source equality remains an unfilled scorecard",
        ),
        (
            "OWNG1692_4_no_U2_leakage",
            "delta_beta_R11, delta_beta_q_loc, boundary/domain and readout U2 leakage vanish or are bounded",
            "would stop beta=1 being spoiled after the EH route",
            "SECOND_ORDER_LEAKAGE_OPEN",
            "R11 beta vector and q_loc/Qnorm rows are missing",
        ),
        (
            "OWNG1692_5_verdict",
            "source-normalized EH owner branch",
            "would allow serious local-GR rerun only if all owner clauses close together",
            "FAIL_CURRENT_CLAIM_PARENT_OWNER_NOT_DERIVED",
            "keep as target theorem, not evidence",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "owner_id": owner_id,
            "required_statement": required,
            "effect_if_signed": effect,
            "current_status": status,
            "blocking_gap": gap,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for owner_id, required, effect, status, gap in rows
    ]


def r11_gate_rows() -> list[dict[str, object]]:
    rows = [
        (
            "R11G1692_0_minimality",
            "parent minimality/no-extra-sector theorem",
            "would kill non-EH beta vector by object-language exclusion",
            "NOT_DERIVED",
            "marker, higher-curvature, vector, connection, nonlocal and source-normalization countermodels remain legal",
        ),
        (
            "R11G1692_1_R2FR",
            "delta_beta_R2_fR",
            "R2/fR scalar mode theorem-zero or finite scalaron coefficient row",
            "FIRST_COMPONENT_OPEN",
            "relative zero theorem exists but parent activator and c_R2/fRR value are missing",
        ),
        (
            "R11G1692_2_RicciWeyl",
            "delta_beta_Ricci_Weyl",
            "zero coefficient, exact topological safe case, or weak-field response map",
            "FIRST_COMPONENT_OPEN",
            "generic Ricci/Weyl curvature-squared leakage is not killed by Gauss-Bonnet language",
        ),
        (
            "R11G1692_3_source_normalization",
            "delta_beta_source and measured-GM operator",
            "source-normalization theorem or finite epsilon_SN row",
            "OPEN",
            "source denominator can mimic beta/source leakage if not owned",
        ),
        (
            "R11G1692_4_q_loc_Qnorm",
            "delta_beta_q_loc and Q_norm",
            "Gamma/Khat/P_loc owner theorem or component norm bounds",
            "SYMBOLIC_BOUND_LANE_ACTIVE",
            "Q_norm decomposition exists but no components or operator norms are numeric",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "component": component,
            "required_resolution": required,
            "current_status": status,
            "blocking_gap": gap,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, component, required, status, gap in rows
    ]


def coefficient_bridge_rows() -> list[dict[str, object]]:
    rows = [
        (
            "CBR1692_0_effective_cR2",
            "c_R2_eff(k)=c_bare+0.5*B^T*L^-1(k)*B+c_measure+c_boundary",
            "R2/fR coefficient accounting spine",
            "DERIVED_SYMBOLIC_LAW",
            "not numeric and not theorem-zero",
        ),
        (
            "CBR1692_1_fixed_L0_double_zero",
            "fixed L0 plus Fhat(m*)=0 and Fhat_prime(m*)=0",
            "best algebraic local closure branch for volume/m/L contribution",
            "BEST_LOCAL_CLOSURE_BRANCH_NOT_LIVE_CLAIM",
            "does not close K_conn, K_domain, K_boundary, memory/source stress or transition/projector leakage",
        ),
        (
            "CBR1692_2_Qnorm",
            "Q_norm <= Q_alg+Q_cdb+Q_mem+Q_bdy+Q_trans+Q_proj",
            "no-cancellation local residual norm lane",
            "BOUND_LANE_READY_SYMBOLIC",
            "component values, units, source paths and operator norms missing",
        ),
        (
            "CBR1692_3_Qgamma",
            "B_gamma <= c^2/(2*U_min)*N_G*N_D*Q_norm",
            "future Cassini gamma pressure row",
            "SYMBOLIC_CASSINI_BOUND_READY",
            "U_min, N_G, N_D and Q_norm components missing",
        ),
        (
            "CBR1692_4_finite_row_trigger",
            "if residual theorem fails, fill c_R2_eff, B_mem, B_h, K_cdb and Q_i rows",
            "finite empirical fallback",
            "FINITE_ROW_REQUIRED_IF_RESIDUALS_RETAINED",
            "rows must stay nonclaim until values and maps are real",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "bridge_id": bridge_id,
            "formula_or_contract": formula,
            "role": role,
            "current_status": status,
            "blocking_gap": gap,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for bridge_id, formula, role, status, gap in rows
    ]


def runner_rows() -> list[dict[str, object]]:
    rows = [
        ("RUN1692_0_owner_promotion", "use EH/source-owner contract as current proof", "REFUSE_REFERENCE_PROMOTION", "owner clauses are target theorem only"),
        ("RUN1692_1_minimality_zero", "set R11 beta vector to zero by minimality", "REFUSE_UNSIGNED_MINIMALITY", "minimality/no-extra-sector theorem is not derived"),
        ("RUN1692_2_R2FR_zero", "set R2/fR beta component to zero", "REFUSE_UNSIGNED_ZERO", "relative theorem lacks parent activator"),
        ("RUN1692_3_Qgamma_score", "score Qgamma/Qnorm Cassini row", "NOT_RUN_COMPONENTS_MISSING", "Qnorm components and operator inputs are missing"),
        ("RUN1692_4_local_gr", "claim derived local GR/Newton branch", "BLOCKED_NO_CLAIM", "owner, R11, source, matter, conservation and Qnorm gates are open"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "case": case,
            "status": status,
            "reason": reason,
            "can_score": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for runner_id, case, status, reason in rows
    ]


def next_target_rows() -> list[dict[str, object]]:
    rows = [
        (
            "NEXT1692_0_primary",
            "1693-Y5-R2FR-fixed-L0-cdb-memory-Qnorm-first-fill-current-branch.md",
            "scripts/Y5_R2FR_fixed_L0_cdb_memory_Qnorm_first_fill_current_branch.py",
            "try to close K_conn/K_domain/K_boundary and memory/source stress under the fixed-L0 double-zero branch; if not, create first nonclaim Q_norm/c_R2_eff finite rows with units, source paths and arena maps",
            "1590 says this is the next live route after owner bundle synthesis",
            "selected",
        ),
        (
            "NEXT1692_1_parallel",
            "1693b-Y5-R2FR-R2FR-RicciWeyl-first-coefficient-source-row.md",
            "scripts/Y5_R2FR_R2FR_RicciWeyl_first_coefficient_source_row.py",
            "fill or theorem-zero the first R11 beta components R2/fR and Ricci/Weyl if the fixed-L0 residual theorem stalls",
            "finite R11 beta vector is the fallback if parent owner theorem remains unsigned",
            "held_fallback",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": route_id,
            "next_target": target,
            "script": script,
            "objective": objective,
            "reason": reason,
            "selection_status": status,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for route_id, target, script, objective, reason, status in rows
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    rows = [
        ("CG1692_0_EH_owner", "source-normalized EH parent owner", "BLOCKED_NO_CLAIM", "owner contract is written but not parent-signed"),
        ("CG1692_1_R11_zero", "R11 beta leakage theorem-zero", "BLOCKED_NO_CLAIM", "minimality/no-extra-sector and first components remain unsigned"),
        ("CG1692_2_Qgamma", "Qgamma/Qnorm Cassini pressure score", "BLOCKED_NO_CLAIM", "symbolic only; no Q_i or operator values"),
        ("CG1692_3_beta", "PPN beta pass", "BLOCKED_NO_CLAIM", "beta residual vector is unfilled"),
        ("CG1692_4_local_gr", "derived local GR/Newton reduction", "BLOCKED_NO_CLAIM", "all owner, residual and source gates must close together"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": claim_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for claim_id, claim, status, reason in rows
    ]


def all_claim_flags_false(paths: list[Path]) -> bool:
    for path in paths:
        for row in read_csv(path):
            for field in ("can_score", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if field in row and bool_cell(row[field]):
                    return False
    return True


def copy_outputs() -> None:
    for source_path, target_paths in COPY_TARGETS.items():
        for target_path in target_paths:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, target_path)


def cleanup_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validate(
    source_rows: list[dict[str, object]],
    owner_rows: list[dict[str, object]],
    r11_rows: list[dict[str, object]],
    coeff_rows: list[dict[str, object]],
    runner_rows_: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    sources_ok = all(bool_cell(row["exists"]) and bool_cell(row["needles_present"]) for row in source_rows)
    owner_blocked = any(row["owner_id"] == "OWNG1692_5_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM_PARENT_OWNER_NOT_DERIVED" for row in owner_rows)
    r11_components_present = {"delta_beta_R2_fR", "delta_beta_Ricci_Weyl", "delta_beta_q_loc and Q_norm"}.issubset({str(row["component"]) for row in r11_rows})
    coeff_law_present = any(row["bridge_id"] == "CBR1692_0_effective_cR2" and "c_R2_eff" in row["formula_or_contract"] for row in coeff_rows)
    fixed_l0_nonclaim = any(row["bridge_id"] == "CBR1692_1_fixed_L0_double_zero" and "NOT_LIVE_CLAIM" in row["current_status"] for row in coeff_rows)
    qnorm_symbolic = any(row["bridge_id"] == "CBR1692_2_Qnorm" and "SYMBOLIC" in row["current_status"] for row in coeff_rows)
    runner_blocks = all(not bool_cell(row["can_score"]) for row in runner_rows_)
    next_selected = any(row["route_id"] == "NEXT1692_0_primary" and row["selection_status"] == "selected" and "fixed-L0-cdb-memory-Qnorm" in row["next_target"] for row in next_rows)
    local_gr_blocked = any(row["claim"] == "derived local GR/Newton reduction" and row["status"] == "BLOCKED_NO_CLAIM" for row in claim_rows)
    no_claim_flags = all_claim_flags_false(CLAIM_CHECKED)
    csv_parse = True
    for path in GENERATED:
        try:
            read_csv(path)
        except Exception:
            csv_parse = False
    branch_copies = all(target.exists() for targets in COPY_TARGETS.values() for target in targets)
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_untouched = len(list(FORMALIZATION.rglob("*1692*"))) == 0 if FORMALIZATION.exists() else True

    checks = [
        ("VAL1692_0_sources_exist", sources_ok, "all cited source paths exist and required needles are present"),
        ("VAL1692_1_owner_blocked", owner_blocked, "EH source-owner remains target theorem not claim"),
        ("VAL1692_2_r11_components_present", r11_components_present, "R11 beta leakage rows include R2/fR Ricci/Weyl and q_loc/Qnorm"),
        ("VAL1692_3_coeff_law_present", coeff_law_present, "c_R2 effective coefficient law is carried forward"),
        ("VAL1692_4_fixed_l0_nonclaim", fixed_l0_nonclaim, "fixed-L0 double-zero branch remains nonclaim"),
        ("VAL1692_5_qnorm_symbolic", qnorm_symbolic, "Qnorm bound lane remains symbolic"),
        ("VAL1692_6_runner_blocks", runner_blocks, "runner blocks all scoring cases"),
        ("VAL1692_7_next_selected", next_selected, "next target selects fixed-L0 cdb/memory Qnorm first fill"),
        ("VAL1692_8_local_gr_blocked", local_gr_blocked, "local GR/Newton claim remains blocked"),
        ("VAL1692_9_no_claim_flags", no_claim_flags, "all generated scoring and claim flags remain false"),
        ("VAL1692_10_csv_parse", csv_parse, "all generated 1692 CSVs parse"),
        ("VAL1692_11_branch_copies", branch_copies, "branch/quarantine/queue copies exist"),
        ("VAL1692_12_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL1692_13_formalization_untouched", formalization_untouched, "no 1692 outputs found under formalization-workbench"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1692_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1692 EH source-owner and R11 beta vector current-branch validation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def write_doc(
    source_rows: list[dict[str, object]],
    owner_rows: list[dict[str, object]],
    r11_rows: list[dict[str, object]],
    coeff_rows: list[dict[str, object]],
    runner_rows_: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    body = f"""# 1692 - EH Source Owner Or R11 Beta Vector Current Branch

## Verdict

1692 keeps the local-GR route honest. A clean GR-like result is available only as a target theorem: one parent action must own the EH-like local operator, universal matter coupling, source-normalized measured mass, source-compatible conservation, boundary policy and all second-order residual silence.

The current corpus does not yet earn that owner theorem. The R11/non-EH beta vector remains live, especially `delta_beta_R2_fR`, `delta_beta_Ricci_Weyl`, source normalization, and `q_loc/Q_norm`. The useful progress is that these are no longer vague objections: `c_R2_eff(k)=c_bare+0.5*B^T*L^-1(k)*B+c_measure+c_boundary`, and the fixed-L0 double-zero branch gives a precise nonclaim closure lane.

The next best route is to attack the fixed-L0 residuals that remain after the algebraic double-zero: `K_conn`, `K_domain`, `K_boundary`, memory/source stress, transition support and projector leakage. If those do not theorem-zero, we fill first nonclaim `Q_norm` and `c_R2_eff` coefficient rows with units and source paths.

## Source Register

{markdown_table(source_rows, ["source_key", "source_path", "exists", "needles_present", "use_in_1692"])}

## EH Source Owner Gate

{markdown_table(owner_rows, ["owner_id", "required_statement", "current_status", "blocking_gap"])}

## R11 Beta Leakage Gate

{markdown_table(r11_rows, ["gate_id", "component", "required_resolution", "current_status", "blocking_gap"])}

## cR2 and Qnorm Bridge

{markdown_table(coeff_rows, ["bridge_id", "formula_or_contract", "current_status", "blocking_gap"])}

## Local GR Owner Runner

{markdown_table(runner_rows_, ["runner_id", "case", "status", "reason"])}

## Next Target

{markdown_table(next_rows, ["route_id", "next_target", "objective", "selection_status"])}

## Claim Gates

{markdown_table(claim_rows, ["claim_id", "claim", "status", "reason"])}

## Validation

{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Working Interpretation

This is the serious GR fork: either MTS earns a single source-normalized parent owner, or it must compete as a finite-residual theory with explicit R11/Qnorm coefficients. The work is not dead; it is sharply localized. The next fight is residual closure after fixed-L0 double-zero, not another broad philosophical pass.
"""
    DOC.write_text(body, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    source_rows = source_register_rows()
    owner_rows = owner_gate_rows()
    r11_rows = r11_gate_rows()
    coeff_rows = coefficient_bridge_rows()
    runner_rows_ = runner_rows()
    next_rows = next_target_rows()
    claim_rows = claim_gate_rows()

    write_csv(SOURCE_REGISTER, source_rows, ["branch_id", "source_key", "source_path", "exists", "needles_present", "required_needles", "use_in_1692", "valid_for_claim", "claim_allowed"])
    write_csv(OWNER_GATE, owner_rows, ["branch_id", "owner_id", "required_statement", "effect_if_signed", "current_status", "blocking_gap", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(R11_GATE, r11_rows, ["branch_id", "gate_id", "component", "required_resolution", "current_status", "blocking_gap", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(COEFF_BRIDGE, coeff_rows, ["branch_id", "bridge_id", "formula_or_contract", "role", "current_status", "blocking_gap", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(RUNNER, runner_rows_, ["branch_id", "runner_id", "case", "status", "reason", "can_score", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(NEXT_TARGET, next_rows, ["branch_id", "route_id", "next_target", "script", "objective", "reason", "selection_status", "valid_for_claim", "claim_allowed"])
    write_csv(CLAIM_GATE, claim_rows, ["branch_id", "claim_id", "claim", "status", "reason", "valid_for_claim", "claim_allowed"])

    copy_outputs()
    cleanup_pycache()
    validation_rows = validate(source_rows, owner_rows, r11_rows, coeff_rows, runner_rows_, next_rows, claim_rows)
    write_csv(VALIDATION, validation_rows, ["check_id", "result", "detail", "valid_for_claim", "claim_allowed"])
    write_doc(source_rows, owner_rows, r11_rows, coeff_rows, runner_rows_, next_rows, claim_rows, validation_rows)

    failed = [row for row in validation_rows if row["result"] != "PASS"]
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("1692 validation PASS")


if __name__ == "__main__":
    main()
