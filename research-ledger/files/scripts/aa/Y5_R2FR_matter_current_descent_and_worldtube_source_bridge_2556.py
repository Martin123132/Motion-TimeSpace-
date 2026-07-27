from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT_ID = "2556"
BRANCH_ID = "MTS_R2FR_MATTER_CURRENT_DESCENT_AND_WORLDTUBE_SOURCE_BRIDGE_2556"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SCRIPTS = ROOT / "scripts"

DOC = ROOT / "2556-Y5-R2FR-matter-current-descent-and-worldtube-source-bridge.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_NO_SHADOW_2556_SOURCE_REGISTER.csv",
    "current_candidates": OUT / "P8_Y5_NO_SHADOW_2556_CURRENT_CANDIDATES.csv",
    "hilbert_descent": OUT / "P8_Y5_NO_SHADOW_2556_HILBERT_CURRENT_DESCENT.csv",
    "conservation_audit": OUT / "P8_Y5_NO_SHADOW_2556_CONSERVATION_AUDIT.csv",
    "worldtube_bridge": OUT / "P8_Y5_NO_SHADOW_2556_WORLDTUBE_BRIDGE.csv",
    "wep_guardrail": OUT / "P8_Y5_NO_SHADOW_2556_WEP_COMPOSITION_GUARDRAIL.csv",
    "external_vacuum": OUT / "P8_Y5_NO_SHADOW_2556_EXTERNAL_VACUUM_SUPPORT.csv",
    "promotion_verdict": OUT / "P8_Y5_NO_SHADOW_2556_PROMOTION_VERDICT.csv",
    "claim_gates": OUT / "P8_Y5_NO_SHADOW_2556_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_NO_SHADOW_2556_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_NO_SHADOW_2556_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_NO_SHADOW_2556_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2556_VALIDATION.csv",
}

COPY_TARGETS = {
    "hilbert_current_contract": QUEUE / "JR2556_HILBERT_CURRENT_SOURCE_BRIDGE_CONTRACT_NONCLAIM.csv",
    "worldtube_contract": LOCAL_BOUNDS / "Worldtube_source_bridge_2556_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2556_00_2555_doc",
        "source_path": ROOT / "2555-Y5-R2FR-vertical-generator-current-law-variation-and-source-audit.md",
        "needles": ["SRC2555_0_matter_origin", "PV2555_5_overall", "NEXT2555_0_selected", "VAL2555_OVERALL"],
        "role": "active handoff selecting source-current descent",
    },
    {
        "source_id": "SRC2556_01_2555_source_descent",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2555_SOURCE_CURRENT_DESCENT.csv",
        "needles": ["SRC2555_0_matter_origin", "SRC2555_3_worldtube_readout", "SRC2555_6_candidate_route"],
        "role": "machine-readable source-current missing clauses",
    },
    {
        "source_id": "SRC2556_02_2555_dimension",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2555_DIMENSION_AUDIT.csv",
        "needles": ["DIM2555_3_viable_branch", "MISSING_PARENT_SCALE"],
        "role": "dimension branch and parent-scale warning",
    },
    {
        "source_id": "SRC2556_03_2555_stress",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2555_STRESS_TENSOR_EXPOSURE.csv",
        "needles": ["STR2555_3_WEP_risk", "STR2555_4_GR_limit_gate"],
        "role": "stress/WEP local-GR blockers",
    },
    {
        "source_id": "SRC2556_04_2554_candidate",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2554_CANDIDATE_ACTIONS.csv",
        "needles": ["ACT2554_A_vertical_generator_current_law", "A_nu J_M^nu"],
        "role": "parent action needing J_M source bridge",
    },
    {
        "source_id": "SRC2556_05_symbol_map",
        "source_path": OUT / "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
        "needles": ["Pi_M", "q_loc^nu", "not_derived_zero; plateau_axiom_forbidden"],
        "role": "local-GR source/action placement warning",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def truth(value: bool) -> str:
    return "true" if value else "false"


def base_row(valid_for_claim: bool = False, claim_allowed: bool = False) -> dict[str, str]:
    return {
        "timestamp_utc": stamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": truth(valid_for_claim),
        "claim_allowed": truth(claim_allowed),
    }


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
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


def cell(value: Any) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(cell(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def inside_root(path: Path) -> bool:
    resolved = path.resolve()
    root = ROOT.resolve()
    return resolved == root or root in resolved.parents


def source_register() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        missing = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            {
                **base_row(),
                "source_id": source["source_id"],
                "source_path": str(path),
                "exists": truth(path.exists()),
                "missing_needles": ";".join(missing),
                "source_pass": truth(path.exists() and not missing),
                "role": source["role"],
            }
        )
    return rows


def current_candidate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CUR2556_A_Hilbert_energy_current", "Hilbert/energy current", "J_M^nu = ell_J T_matter^{nu rho} tau_rho", "T_matter from metric variation; tau is local clock/coframe direction; ell_J supplies one inverse mass scale", "best universality route because all matter couples through stress-energy", "SELECTED_PRIMARY_CONTRACT", "needs parent scale ell_J, clock compatibility, and conservation identity"),
        ("CUR2556_B_vertical_Noether_current", "vertical Noether current", "J_M^nu = c_A pi_Psi^nu R_M Psi", "matter has vertical generator R_M and A_mu enters D_mu^A Psi=D_mu Psi+A_mu R_M Psi", "directly matches vertical-generator language", "SECONDARY_CANDIDATE", "risks species-dependent charge and WEP failure unless R_M is universal/geometric"),
        ("CUR2556_C_rest_mass_current", "rest-mass/baryonic current", "J_M^nu proportional to rho_0 u^nu", "phenomenological matter current", "useful for smoke tests only", "DEMOTE_TO_PHENOMENOLOGY", "not fundamental enough for GR reduction and likely fails pressure/radiation regimes"),
        ("CUR2556_D_orbital_GM_current", "fitted orbital GM current", "J_M chosen so worldtube integral equals observed GM", "post-readout fitted source", "would make Newton limit circular", "REJECTED", "forbidden shortcut"),
    ]
    return [
        {
            **base_row(),
            "candidate_id": candidate_id,
            "candidate_name": name,
            "candidate_law": law,
            "definition": definition,
            "strength": strength,
            "status": status,
            "main_risk": risk,
        }
        for candidate_id, name, law, definition, strength, status, risk in rows
    ]


def hilbert_descent_rows() -> list[dict[str, Any]]:
    rows = [
        ("HIL2556_0_define_T", "T_matter^{mu nu}:=-(2/sqrt(-g)) delta S_matter/delta g_mu_nu", "standard Hilbert stress from matter action", "universal source object exists if matter action is metric-coupled", "PASS_AS_CONTRACT"),
        ("HIL2556_1_define_current", "J_M^nu:=ell_J T_matter^{nu rho} tau_rho", "clock/coframe tau selects local energy current; ell_J fixes dimension to M^3 branch", "matches 2555 viable branch with [A]=M and [Gamma_eff]=M^2", "PASS_AS_CANDIDATE_CONTRACT"),
        ("HIL2556_2_parent_scale", "ell_J must be parent-derived and fixed before tests", "otherwise J_M normalization becomes a hidden fitted mass scale", "source bridge remains nonclaim until ell_J source exists", "MISSING_PARENT_SCALE"),
        ("HIL2556_3_clock_compatibility", "tau_rho must be parent-owned and locally compatible with conservation", "nabla_nu(T^{nu rho} tau_rho)=T^{nu rho} nabla_nu tau_rho on matter shell", "exact conservation needs tau Killing/covariantly constant locally or a controlled exchange term", "MISSING_CLOCK_CONSERVATION_CLAUSE"),
        ("HIL2556_4_matter_A_coupling", "If A also couples directly to matter, its source must reduce to the Hilbert current branch or be demoted.", "prevents double-counting Hilbert and vertical charge currents", "A_nu J_M^nu should be universal source coupling, not species charge tuning", "MISSING_UNIFICATION_OF_COUPLINGS"),
    ]
    return [{**base_row(), "hilbert_id": a, "clause": b, "basis": c, "result": d, "status": e} for a, b, c, d, e in rows]


def conservation_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("CON2556_0_matter_shell", "If matter equations and diffeomorphism invariance give nabla_mu T^{mu nu}=0, then divergence of J_M is ell_J T^{mu nu} nabla_mu tau_nu plus scale-gradient terms.", "Hilbert current branch", "conserved only under clock compatibility or controlled exchange", "CONDITIONAL_NOT_CLOSED"),
        ("CON2556_1_local_inertial_limit", "In a local inertial vacuum collar with tau approximately covariantly constant and no matter support, J_M=0 and nabla.J_M=0.", "local lab/PPN collar approximation", "supports conditional q_loc zero exterior", "PASS_AS_LOCAL_LIMIT_CONTRACT"),
        ("CON2556_2_exact_identity_needed", "Exact local-GR theorem needs an identity: nabla_mu J_M^mu + I_GK = 0, with I_GK supplied by Gamma/Khat/tau equations if tau is not Killing.", "integrability of A equation", "exchange term must be parent-derived, not added by hand", "MISSING_EXACT_IDENTITY"),
        ("CON2556_3_Noether_alternative", "Vertical Noether current can be exactly conserved if R_M is a genuine symmetry and A/Gamma sector has compatible transformation.", "secondary branch", "possible but WEP/composition risk is higher than Hilbert branch", "CANDIDATE_ONLY"),
        ("CON2556_4_distributional_source", "Worldtube boundary requires distributional conservation including surface layer flux.", "compact source with boundary", "needed before deriving Newton source mass", "MISSING_JUMP_IDENTITY"),
    ]
    return [{**base_row(), "conservation_id": a, "statement": b, "basis": c, "result": d, "status": e} for a, b, c, d, e in rows]


def worldtube_bridge_rows() -> list[dict[str, Any]]:
    rows = [
        ("WT2556_0_charge_integral", "Q_M[W,Sigma]:=int_{Sigma cap W} J_M^mu dSigma_mu", "source charge from current flux through parent-defined hypersurface", "valid only if J_M is conserved including boundary layers", "CONDITIONAL_CONTRACT"),
        ("WT2556_1_mass_readout", "M_source[W]:=Q_M/ell_J for Hilbert branch, equivalently int T^{mu nu} tau_nu dSigma_mu", "mass/energy source readout before orbital fitting", "requires ell_J fixed by parent convention and tau normalized", "CONDITIONAL_CONTRACT"),
        ("WT2556_2_surface_independence", "Q_M[Sigma_1]=Q_M[Sigma_2] if nabla_mu J_M^mu=0 and no flux leaks through side boundary", "Gauss law", "not proved until conservation/jump conditions close", "MISSING_CONSERVATION_PROOF"),
        ("WT2556_3_external_vacuum", "Outside W, J_M=0 so q_loc=P_loc J_M=0 up to bounded boundary tails", "local vacuum law", "requires compact support/falloff theorem", "MISSING_SUPPORT_THEOREM"),
        ("WT2556_4_no_orbital_GM", "Do not define M_source by observed GM or fitted orbital acceleration.", "anti-circularity guardrail", "passes as explicit forbidden route", "PASS_GUARDRAIL"),
    ]
    return [{**base_row(), "worldtube_id": a, "clause": b, "role": c, "condition": d, "status": e} for a, b, c, d, e in rows]


def wep_guardrail_rows() -> list[dict[str, Any]]:
    rows = [
        ("WEP2556_0_hilbert_universal", "Hilbert current branch is naturally universal because all matter contributes through T_matter.", "SUPPORTS_WEP_ROUTE", "still needs proof that A coupling does not add species charge"),
        ("WEP2556_1_noether_species_risk", "Vertical Noether branch may couple differently to different matter fields.", "RISK_OPEN", "requires universal R_M or geometric descent"),
        ("WEP2556_2_pressure_radiation", "Newton source cannot be only baryonic rest mass; relativistic pressure/radiation regimes must be handled.", "HILBERT_BRANCH_PREFERRED", "T_matter route is safer than rho_0 u^mu route"),
        ("WEP2556_3_composition_bound", "Any residual species-dependent component must be zero or bounded before WEP/PPN claims.", "BLOCKS_CLAIM", "future local tests need eta/WEP projection if branch survives"),
        ("WEP2556_4_coupling_unification", "A_nu J_M^nu should be the same source object that appears in metric stress equations.", "REQUIRED", "prevents duplicate source definitions"),
    ]
    return [{**base_row(), "wep_id": a, "statement": b, "status": c, "required_fix": d} for a, b, c, d in rows]


def external_vacuum_rows() -> list[dict[str, Any]]:
    rows = [
        ("VAC2556_0_exact_vacuum", "If T_matter=0 outside W and tau is regular, then Hilbert J_M=0 outside W.", "q_loc=P_loc J_M gives local vacuum zero in source-free exterior", "CONDITIONAL"),
        ("VAC2556_1_tail_bound", "If matter has tails, require ||J_M||_collar <= epsilon_J and boundary flux <= epsilon_B.", "Delta m/m bound inherits epsilon_J+epsilon_B", "BOUND_FORM_ONLY"),
        ("VAC2556_2_clock_leak", "If tau varies across collar, conservation leaks through T^{mu nu} nabla_mu tau_nu.", "clock compatibility needed for exact source silence", "MISSING_CLOCK_BOUND"),
        ("VAC2556_3_surface_layer", "Distributional worldtube surface terms must be included in J_M or boundary flux ledger.", "prevents hiding source at boundary", "MISSING_JUMP_LEDGER"),
    ]
    return [{**base_row(), "vacuum_id": a, "condition": b, "effect": c, "status": d} for a, b, c, d in rows]


def promotion_verdict_rows() -> list[dict[str, Any]]:
    rows = [
        ("PV2556_0_best_current", "Which source current route is best?", "HILBERT_ENERGY_CURRENT", "universal stress-energy source is least circular and most GR-compatible", "select for next derivation"),
        ("PV2556_1_source_bridge", "Is J_M fully derived?", "NO", "ell_J, tau conservation, exact identity and worldtube jump conditions are missing", "source bridge remains nonclaim"),
        ("PV2556_2_Newton_source", "Is Newton source mass derived?", "NO_BUT_CONTRACT_WRITTEN", "M_source=int T tau dSigma is the right-looking target but not yet parent-closed", "no Newton claim"),
        ("PV2556_3_WEP", "Does source branch avoid WEP risk?", "PARTIALLY", "Hilbert route is universal, but A coupling and any Noether supplement must not add composition charge", "WEP gate remains blocked"),
        ("PV2556_4_overall", "Overall 2556 verdict", "SOURCE_BRIDGE_SHARPENED_NOT_CLOSED", "best source route identified; theorem blocked by scale, clock conservation and worldtube support", "next target is exact conservation/scale gate"),
    ]
    return [{**base_row(), "verdict_id": a, "question": b, "result": c, "evidence": d, "effect": e} for a, b, c, d, e in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2556_0_hilbert_route", "Hilbert current is selected as best source-current route.", "PASS_AS_CONTRACT", "least circular and most universal", "true", "false"),
        ("GATE2556_1_parent_scale", "ell_J is parent-derived.", "BLOCKED", "no source for parent scale yet", "false", "false"),
        ("GATE2556_2_conservation", "J_M conservation identity is exact.", "BLOCKED", "tau compatibility/exchange identity missing", "false", "false"),
        ("GATE2556_3_worldtube", "worldtube source mass is parent-derived and surface-independent.", "BLOCKED", "jump/support conditions missing", "false", "false"),
        ("GATE2556_4_WEP_PPN", "WEP/PPN safe source coupling is proven.", "BLOCKED", "composition guardrail not closed", "false", "false"),
        ("GATE2556_5_local_GR_Newton", "local GR/Newton branch passes.", "BLOCKED", "source bridge not closed and stress gate still open", "false", "false"),
        ("GATE2556_6_no_GitHub", "No public/GitHub update.", "PASS_GUARDRAIL", "private derivation checkpoint only", "true", "false"),
    ]
    return [{**base_row(), "gate_id": a, "claim": b, "gate_status": c, "reason": d, "gate_pass": e, "claim_allowed": f} for a, b, c, d, e, f in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2556_0_select_hilbert", "Select Hilbert/energy current as primary source bridge.", "it best matches GR source structure and avoids species tuning", "use J_M=ell_J T_matter tau as working contract"),
        ("DEC2556_1_demote_orbital_GM", "Reject fitted orbital GM source definition.", "would make Newton limit circular", "keeps derivation honest"),
        ("DEC2556_2_keep_noether_secondary", "Keep vertical Noether current only as secondary route.", "it may map to vertical-generator intuition but has WEP risk", "do not use as primary local-GR source"),
        ("DEC2556_3_next_conservation_scale", "Next derive clock-compatible conservation and parent scale.", "Hilbert branch cannot close without ell_J and nabla.J identity", "2557 target selected"),
        ("DEC2556_4_no_claim", "No local-GR/Newton claim.", "source bridge sharpened but not closed", "private nonclaim status retained"),
    ]
    return [{**base_row(), "decision_id": a, "decision": b, "reason": c, "effect": d} for a, b, c, d in rows]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            **base_row(),
            "route_id": "NEXT2556_0_selected",
            "selection_status": "selected",
            "target_file": "2557-Y5-R2FR-Hilbert-current-conservation-scale-and-clock-compatibility-gate.md",
            "target_script": "scripts/Y5_R2FR_Hilbert_current_conservation_scale_and_clock_compatibility_gate_2557.py",
            "task": "derive or reject the exact conservation identity for J_M=ell_J T_matter tau, identify the parent scale ell_J, and decide whether the Hilbert source bridge can close",
            "acceptance_target": "clock compatibility equation, parent scale options, exchange-current identity, worldtube surface-independence gate, and demotion if ell_J is only fitted",
            "guardrails": "no local-GR claim; no fitted GM; no M_H_ref reuse; no plateau axiom; no GitHub",
        }
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    for target in COPY_TARGETS.values():
        target.parent.mkdir(parents=True, exist_ok=True)
    source_map = {
        "hilbert_current_contract": OUTPUTS["hilbert_descent"],
        "worldtube_contract": OUTPUTS["worldtube_bridge"],
    }
    for copy_id, target in COPY_TARGETS.items():
        shutil.copyfile(source_map[copy_id], target)
    return [
        {
            **base_row(),
            "copy_id": copy_id,
            "source_path": str(source_map[copy_id]),
            "target_path": str(target),
            "source_exists": truth(source_map[copy_id].exists()),
            "target_exists": truth(target.exists()),
        }
        for copy_id, target in COPY_TARGETS.items()
    ]


def csv_parse_status(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), ""
    except Exception as exc:
        return False, 0, repr(exc)


def formalization_hits() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    artifact_markers = (
        "2556-Y5",
        "_2556_",
        "_2556.",
        "JR2556",
        "P8_Y5_NO_SHADOW_2556",
        "P8_Y5_BRR545_2556",
        "Y5_R2FR_matter_current_descent_and_worldtube_source_bridge_2556",
    )
    return [
        path
        for path in FORMALIZATION.rglob("*")
        if any(marker in path.name for marker in artifact_markers)
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    hilbert: list[dict[str, Any]],
    conservation: list[dict[str, Any]],
    worldtube: list[dict[str, Any]],
    wep: list[dict[str, Any]],
    vacuum: list[dict[str, Any]],
    verdicts: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, notes: str, detail: str = "") -> None:
        rows.append({"check_id": check_id, "status": "PASS" if passed else "FAIL", "notes": notes, "detail": detail})

    add("VAL2556_00_sources_exist", all(row["source_pass"] == "true" for row in sources), "all cited source paths exist and needles are present", ";".join(row["source_id"] for row in sources if row["source_pass"] != "true"))
    add("VAL2556_01_hilbert_selected", any(row["candidate_id"] == "CUR2556_A_Hilbert_energy_current" and row["status"] == "SELECTED_PRIMARY_CONTRACT" for row in candidates), "Hilbert current selected as primary contract")
    add("VAL2556_02_hilbert_contract", any(row["hilbert_id"] == "HIL2556_1_define_current" and row["status"] == "PASS_AS_CANDIDATE_CONTRACT" for row in hilbert), "Hilbert source current contract written")
    add("VAL2556_03_scale_missing", any(row["status"] == "MISSING_PARENT_SCALE" for row in hilbert), "parent scale blocker retained")
    add("VAL2556_04_conservation_not_closed", any(row["status"] == "MISSING_EXACT_IDENTITY" for row in conservation), "exact conservation blocker retained")
    add("VAL2556_05_worldtube_guardrail", any(row["worldtube_id"] == "WT2556_4_no_orbital_GM" and row["status"] == "PASS_GUARDRAIL" for row in worldtube), "orbital-GM source definition rejected")
    add("VAL2556_06_wep_guardrail", any(row["wep_id"] == "WEP2556_3_composition_bound" and row["status"] == "BLOCKS_CLAIM" for row in wep), "WEP/composition gate blocks claim")
    add("VAL2556_07_vacuum_conditional", any(row["vacuum_id"] == "VAC2556_0_exact_vacuum" and row["status"] == "CONDITIONAL" for row in vacuum), "external vacuum condition recorded as conditional")
    add("VAL2556_08_overall_nonclaim", any(row["verdict_id"] == "PV2556_4_overall" and row["result"] == "SOURCE_BRIDGE_SHARPENED_NOT_CLOSED" for row in verdicts), "overall source bridge verdict is nonclaim")
    add("VAL2556_09_claim_gates_safe", all(row["claim_allowed"] == "false" for row in gates), "no claim gate allows local-GR/Newton claim")
    add("VAL2556_10_next_target_written", bool(next_rows) and next_rows[0]["route_id"] == "NEXT2556_0_selected", "2557 conservation/scale gate selected")
    add("VAL2556_11_branch_copies", all(row["source_exists"] == "true" and row["target_exists"] == "true" for row in branch_rows), "nonclaim branch copies exist")
    add("VAL2556_12_no_formalization_artifacts", not formalization_hits(), "no 2556 artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_hits()))
    add("VAL2556_13_all_outputs_inside_post_checkpoint", all(inside_root(path) for path in list(OUTPUTS.values()) + list(COPY_TARGETS.values()) + [DOC]), "all 2556 outputs stay inside post-checkpoint-work")
    add("VAL2556_14_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ absent after cleanup")

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_parse_status(path)
        add(f"VAL2556_CSV_{path.stem}", ok and count > 0, f"CSV parses with {count} rows" if ok else "CSV parse failed", detail or str(path))

    for copy_id, path in COPY_TARGETS.items():
        ok, count, detail = csv_parse_status(path)
        add(f"VAL2556_COPY_CSV_{copy_id}", ok and count > 0, f"copy CSV parses with {count} rows" if ok else "copy CSV parse failed", detail or str(path))

    overall = all(row["status"] == "PASS" for row in rows)
    add("VAL2556_OVERALL", overall, "2556 selects a Hilbert-current source bridge but blocks theorem claims on parent scale, conservation and worldtube support")
    return [{**base_row(), **row} for row in rows]


def write_doc(
    sources: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    hilbert: list[dict[str, Any]],
    conservation: list[dict[str, Any]],
    worldtube: list[dict[str, Any]],
    wep: list[dict[str, Any]],
    vacuum: list[dict[str, Any]],
    verdicts: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    sections = [
        "# 2556 Y5 R2FR Matter-current Descent And Worldtube Source Bridge",
        "",
        "**Result:** source bridge sharpened, not closed. The best route is not an arbitrary vertical charge and definitely not fitted orbital GM. The least-circular current is a Hilbert/energy current, `J_M^nu = ell_J T_matter^{nu rho} tau_rho`, because it uses the same stress-energy object that GR already treats as source.",
        "",
        "**Important shift:** this makes the Newton-source problem more concrete. Instead of asking for a mysterious `J_M`, the contract is now: derive/fix `ell_J`, prove the clock-compatible conservation identity, and make the worldtube integral surface-independent. If those close, `q_loc=P_loc J_M` has a real shot at giving source-free local vacuum outside matter without a plateau axiom.",
        "",
        "## Source Register",
        markdown_table(sources, ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Current Candidates",
        markdown_table(candidates, ["candidate_id", "candidate_name", "candidate_law", "definition", "strength", "status", "main_risk"]),
        "",
        "## Hilbert Current Descent",
        markdown_table(hilbert, ["hilbert_id", "clause", "basis", "result", "status"]),
        "",
        "## Conservation Audit",
        markdown_table(conservation, ["conservation_id", "statement", "basis", "result", "status"]),
        "",
        "## Worldtube Bridge",
        markdown_table(worldtube, ["worldtube_id", "clause", "role", "condition", "status"]),
        "",
        "## WEP And Composition Guardrail",
        markdown_table(wep, ["wep_id", "statement", "status", "required_fix"]),
        "",
        "## External Vacuum Support",
        markdown_table(vacuum, ["vacuum_id", "condition", "effect", "status"]),
        "",
        "## Promotion Verdict",
        markdown_table(verdicts, ["verdict_id", "question", "result", "evidence", "effect"]),
        "",
        "## Claim Gates",
        markdown_table(gates, ["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(decisions, ["decision_id", "decision", "reason", "effect"]),
        "",
        "## Next Target",
        markdown_table(next_rows, ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"]),
        "",
        "## Branch Copies",
        markdown_table(branch_rows, ["copy_id", "source_path", "target_path", "source_exists", "target_exists"]),
        "",
        "## Validation",
        markdown_table(validations, ["check_id", "status", "notes", "detail"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)

    sources = source_register()
    candidates = current_candidate_rows()
    hilbert = hilbert_descent_rows()
    conservation = conservation_audit_rows()
    worldtube = worldtube_bridge_rows()
    wep = wep_guardrail_rows()
    vacuum = external_vacuum_rows()
    verdicts = promotion_verdict_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["current_candidates"], candidates)
    write_csv(OUTPUTS["hilbert_descent"], hilbert)
    write_csv(OUTPUTS["conservation_audit"], conservation)
    write_csv(OUTPUTS["worldtube_bridge"], worldtube)
    write_csv(OUTPUTS["wep_guardrail"], wep)
    write_csv(OUTPUTS["external_vacuum"], vacuum)
    write_csv(OUTPUTS["promotion_verdict"], verdicts)
    write_csv(OUTPUTS["claim_gates"], gates)
    write_csv(OUTPUTS["decision_ledger"], decisions)
    write_csv(OUTPUTS["next_target"], next_rows)

    branch_rows = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], branch_rows)

    validations = validation_rows(sources, candidates, hilbert, conservation, worldtube, wep, vacuum, verdicts, gates, decisions, next_rows, branch_rows)
    write_csv(OUTPUTS["validation"], validations)
    write_doc(sources, candidates, hilbert, conservation, worldtube, wep, vacuum, verdicts, gates, decisions, next_rows, branch_rows, validations)

    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
