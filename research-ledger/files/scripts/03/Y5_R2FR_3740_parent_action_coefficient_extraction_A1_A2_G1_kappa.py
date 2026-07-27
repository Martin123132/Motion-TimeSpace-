from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3740"
BRANCH_ID = "MTS_R2FR_Y5_PARENT_ACTION_COEFFICIENT_EXTRACTION_A1_A2_G1_KAPPA_3740"
DOC = ROOT / "3740-Y5-R2FR-parent-action-coefficient-extraction-A1-A2-G1-kappa.md"

DOC_3739 = ROOT / "3739-Y5-R2FR-parent-2PN-beta-map-and-GN-normalization.md"
NEXT_3739 = RESIDUALS / "P8_Y5_R2FR_3739_NEXT_TARGET.csv"
VALIDATION_3739 = RESIDUALS / "P8_Y5_BRR545_3739_VALIDATION.csv"
PARENT_INPUTS_3739 = RESIDUALS / "P8_Y5_R2FR_3739_PARENT_INPUT_LEDGER.csv"

ACTION_PRINCIPLE = REPO / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md"
FUNDAMENTAL_ACTION = REPO / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md"
MTS_GRAVITY = REPO / "core-mts-framework" / "gravity" / "motion-timespace-mts-gravity.md"
MTS_GRAVITY_CORE = REPO / "core-mts-framework" / "gravity" / "motion-timespace-mts-gravity-core-unified-formulation.md"
TIME_RELATIVITY = REPO / "core-mts-framework" / "relativity" / "time-as-thermodynamic-exchange-in-motion-timespace-a-unified-framework-for-relativity-and-thermodynamics.md"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(timestamp: str) -> dict[str, object]:
    return {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def read_lines(path: Path) -> list[str]:
    return read_text(path).splitlines()


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def find_line(path: Path, needle: str) -> tuple[int, str]:
    for line_number, line in enumerate(read_lines(path), start=1):
        if needle in line:
            return line_number, line.strip()
    return 0, ""


def source_register(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("doc_3739", DOC_3739, "A2=A1^2", "handoff requiring coefficient extraction"),
        ("next_3739", NEXT_3739, "3740-Y5-R2FR-parent-action-coefficient-extraction-A1-A2-G1-kappa.md", "3739 next target"),
        ("validation_3739", VALIDATION_3739, "next_target_3740", "3739 validation"),
        ("parent_inputs_3739", PARENT_INPUTS_3739, "PIN3739_A1", "3739 parent input ledger"),
        ("action_principle", ACTION_PRINCIPLE, "κ = 8πG / c⁴", "MTS-Einstein action and calibrated GR coupling"),
        ("fundamental_action", FUNDAMENTAL_ACTION, "A_MTS[ψ]", "microscopic psi action and kinetic normalization"),
        ("mts_gravity", MTS_GRAVITY, "β = 1 + O(K^m)", "weak-curvature PPN closure claim"),
        ("mts_gravity_core", MTS_GRAVITY_CORE, "G / (1 + Γ_G(a) / (3H²(a)))", "effective Newton constant closure"),
        ("time_relativity", TIME_RELATIVITY, "\\Gamma_\\kappa \\equiv", "weak-field clock/potential identification"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        line_number, line_text = find_line(path, needle) if exists else (0, "")
        rows.append({
            **base(timestamp),
            "source_id": source_id,
            "path": str(path),
            "exists": exists,
            "needle": needle,
            "needle_found": needle in text,
            "line_number": line_number,
            "line_text": line_text,
            "role": role,
            "claim_allowed": False,
        })
    return rows


def evidence_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("E3740_0_metric_covariance", ACTION_PRINCIPLE, "g_{μν}(x)", "metric emergence", "supports emergent metric from ψ covariance but does not normalize local Newtonian potential"),
        ("E3740_1_action_kappa", ACTION_PRINCIPLE, "κ = 8πG / c⁴", "source coupling", "shows G is inserted/calibrated in the macroscopic action"),
        ("E3740_2_matter_lagrangian", ACTION_PRINCIPLE, "L_matter the standard matter Lagrangian", "matter coupling", "standard metric matter coupling is present; no independent K_m to X is extracted"),
        ("E3740_3_curvature_exchange", ACTION_PRINCIPLE, "L_{Λκ} = (2/κ) Γ_G(x)", "curvature exchange", "curvature exchange is tied to the same calibrated κ"),
        ("E3740_4_psi_action", FUNDAMENTAL_ACTION, "A_MTS[ψ]", "microscopic action", "ψ action is present but has no explicit matter source coefficient K_m"),
        ("E3740_5_psi_equation", FUNDAMENTAL_ACTION, "∂²_t ψ – c² ∇²ψ + γ ∂_t ψ + λ |ψ|^{n−1} = 0", "microscopic equation", "free ψ equation provides kinetic normalization but no sourced Poisson equation for X"),
        ("E3740_6_gr_limit", FUNDAMENTAL_ACTION, "Γ_G → 0  ⇒ pure GR", "local closure", "if correction vanishes, local equations inherit GR"),
        ("E3740_7_weak_metric", TIME_RELATIVITY, "ds^2 = - (1 + \\frac{2\\Phi}{c^2})", "weak-field gauge", "Schwarzschild/Newtonian gauge template supplies first-order g00/spatial metric comparison"),
        ("E3740_8_gamma_kappa", TIME_RELATIVITY, "\\Gamma_\\kappa \\equiv -", "clock potential map", "Γ_kappa is identified with -2Φ/c², fixing only a convention-dependent first-order map"),
        ("E3740_9_source_placeholder", TIME_RELATIVITY, "S[T_{\\mu\\nu}]", "source placeholder", "matter source functional is named but no coefficient is given"),
        ("E3740_10_ppn_gamma", MTS_GRAVITY, "γ = 1 + O(K^m)", "PPN closure", "corpus asserts weak-curvature gamma residual is order K^m"),
        ("E3740_11_ppn_beta", MTS_GRAVITY, "β = 1 + O(K^m)", "PPN closure", "corpus asserts weak-curvature beta residual is order K^m"),
        ("E3740_12_solar_K", MTS_GRAVITY, "K_solar ≈ 10⁻⁶¹", "local bound scale", "corpus supplies a solar-system curvature scale for the closure route"),
        ("E3740_13_S_small", MTS_GRAVITY, "𝓢 ≈ K^m ≪ 10⁻¹²²", "local bound scale", "corpus supplies the weak-curvature suppression size when m>=2"),
        ("E3740_14_G_eff", MTS_GRAVITY_CORE, "G / (1 + Γ_G(a) / (3H²(a)))", "effective Newton closure", "effective G is written as a modulation of calibrated G, not a derivation of G"),
    ]
    rows: list[dict[str, object]] = []
    for evidence_id, path, needle, category, extraction_meaning in specs:
        line_number, line_text = find_line(path, needle)
        rows.append({
            **base(timestamp),
            "evidence_id": evidence_id,
            "category": category,
            "path": str(path),
            "line_number": line_number,
            "needle": needle,
            "found": line_number > 0,
            "line_text": line_text,
            "extraction_meaning": extraction_meaning,
            "claim_allowed": False,
        })
    return rows


def parent_coefficient_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("PC3740_A1", "A1", "first-order g00 coefficient", "CONVENTION_DEPENDENT_FIRST_ORDER_MATCH_ONLY", "A1=1 if X=Phi/c^2; A1=1/2 if X=Gamma_kappa=-2Phi/c^2 with g00=-(1-X)", "E3740_7_weak_metric;E3740_8_gamma_kappa", "choose parent variable X and extract from the actual matter metric rather than GR template"),
        ("PC3740_A2", "A2", "second-order g00 coefficient", "MISSING_PARENT_2PN_EXPANSION", "no source-owned A2 found; if X=Gamma_kappa clock ansatz gives no X^2 metric term, which would not prove beta=1", "none", "derive 2PN parent matter metric or keep beta row closure-only"),
        ("PC3740_G1", "G1", "first-order spatial metric coefficient", "GR_TEMPLATE_FIRST_ORDER_MATCH_ONLY", "G1=A1 follows only if the Schwarzschild/Newtonian weak-field template is adopted", "E3740_7_weak_metric", "extract spatial metric from parent covariance map"),
        ("PC3740_kappa_X", "kappa_X", "parent source response", "CALIBRATED_GR_COUPLING_PRESENT_NOT_PARENT_DERIVED", "macroscopic action uses kappa=8*pi*G/c^4; no independent kappa_X sourced from ψ/X equation", "E3740_1_action_kappa;E3740_14_G_eff", "either derive K_m/Z_X from parent action or label G_N as calibrated closure"),
        ("PC3740_ZX", "Z_X", "parent kinetic normalization", "PSI_KINETIC_NORMALIZATION_PRESENT_NOT_X_SOURCE_NORM", "ψ kinetic terms exist with canonical-looking coefficients, but they are not a sourced quasi-static X kinetic norm", "E3740_4_psi_action;E3740_5_psi_equation", "derive the quasi-static X reduction of ψ and its elliptic operator norm"),
        ("PC3740_Km", "K_m", "matter/source coupling to X", "STANDARD_MATTER_COUPLING_PRESENT_NO_X_COEFFICIENT", "standard L_matter/T_munu coupling exists; no parent-owned K_m multiplying X or ψ source was found", "E3740_2_matter_lagrangian;E3740_9_source_placeholder", "extract explicit source functional coefficient from matter coupling"),
        ("PC3740_unit_factor", "unit_factor_CG", "unit conversion", "PARTIAL_C_AND_KAPPA_CONVENTIONS_PRESENT", "c factors and kappa=8*pi*G/c^4 are present, but the X-to-SI unit factor is not defined", "E3740_1_action_kappa;E3740_7_weak_metric", "state whether X is Phi/c^2, Gamma_kappa, psi covariance, or another normalized potential"),
        ("PC3740_gauge", "weak_field_gauge", "PPN comparison gauge", "GR_WEAK_FIELD_TEMPLATE_PRESENT", "Schwarzschild/Newtonian weak-field gauge is quoted and can be used for closure comparisons", "E3740_7_weak_metric", "derive or declare the map from parent coordinates to standard PPN gauge"),
    ]
    return [
        {
            **base(timestamp),
            "coefficient_id": coefficient_id,
            "symbol": symbol,
            "meaning": meaning,
            "extraction_status": extraction_status,
            "extracted_value_or_bound": extracted_value_or_bound,
            "supporting_evidence_ids": supporting_evidence_ids,
            "next_action": next_action,
            "parent_owned": extraction_status in {"PARENT_DERIVED", "SOURCE_OWNED"},
            "closure_owned": extraction_status in {"CALIBRATED_GR_COUPLING_PRESENT_NOT_PARENT_DERIVED", "GR_WEAK_FIELD_TEMPLATE_PRESENT", "GR_TEMPLATE_FIRST_ORDER_MATCH_ONLY"},
            "claim_allowed": False,
        }
        for coefficient_id, symbol, meaning, extraction_status, extracted_value_or_bound, supporting_evidence_ids, next_action in specs
    ]


def closure_route_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("CL3740_0_base_equation", "calibrated_GR_closure", "G_{mu nu} + S g_{mu nu} = kappa T_{mu nu}, kappa=8*pi*G/c^4", "When S->0 the macroscopic equations reduce to GR with calibrated G.", "E3740_1_action_kappa;E3740_6_gr_limit", "CLOSURE_ROUTE_SOURCE_BACKED"),
        ("CL3740_1_newton", "calibrated_Newton_limit", "G_N_eff_local = G_calibrated + O(S)", "Newton's constant is not derived here; it is inherited from the calibrated Einstein-Hilbert coupling.", "E3740_1_action_kappa;E3740_14_G_eff", "CALIBRATED_CLOSURE_NOT_DERIVATION"),
        ("CL3740_2_ppn_bound", "local_PPN_bound", "|gamma-1|, |beta-1| = O(K^m); with K_solar≈1e-61 and m>=2, residual scale <<1e-122 up to operator constants", "This gives a local suppression route if the S≈K^m statement is upheld and the base metric is GR.", "E3740_10_ppn_gamma;E3740_11_ppn_beta;E3740_12_solar_K;E3740_13_S_small", "BOUND_ROUTE_SOURCE_BACKED_OPERATOR_CONSTANTS_OPEN"),
        ("CL3740_3_parent_route", "parent_owned_derivation", "A2=A1^2 and 4*pi*G_N=A1*kappa_X remain unproved by corpus extraction", "The stricter parent route remains open; closure does not replace it.", "PC3740_A2;PC3740_kappa_X", "PARENT_ROUTE_BLOCKED"),
    ]
    return [
        {
            **base(timestamp),
            "closure_id": closure_id,
            "route": route,
            "formula_or_bound": formula_or_bound,
            "meaning": meaning,
            "supporting_evidence_ids": supporting_evidence_ids,
            "status": status,
            "claim_allowed": False,
        }
        for closure_id, route, formula_or_bound, meaning, supporting_evidence_ids, status in specs
    ]


def fill_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("FILL3740_0_GN_eff_calibrated", "G_N_eff", "G_calibrated plus local O(S) correction", "Moved from unknown to calibrated closure: source-backed by kappa=8*pi*G/c^4, not parent-derived.", "READY_AS_CALIBRATED_CLOSURE_NOT_DERIVATION"),
        ("FILL3740_1_C_beta_2PN_closure_bound", "C_beta_2PN", "C_beta_S*K^m under calibrated-GR closure; parent A2/A1^2 route still missing", "Provides a local bound route but not a parent coefficient proof of A2=A1^2.", "BOUND_SCHEMA_READY_CONSTANT_OPEN"),
        ("FILL3740_2_gamma_closure_bound", "gamma_MTS-1", "C_gamma_S*K^m under calibrated-GR closure", "First-order gamma is bounded by weak-curvature suppression if the GR base metric is adopted.", "BOUND_SCHEMA_READY_CONSTANT_OPEN"),
        ("FILL3740_3_parent_A2_block", "A2", "MISSING_PARENT_2PN_EXPANSION", "No extracted parent-owned A2; beta zero theorem remains future work.", "BLOCKED_PARENT_ROUTE"),
    ]
    return [
        {
            **base(timestamp),
            "fill_id": fill_id,
            "target_symbol": target_symbol,
            "fill_value_or_bound": fill_value_or_bound,
            "meaning": meaning,
            "status": status,
            "ready_to_patch_3738": False,
            "claim_allowed": False,
        }
        for fill_id, target_symbol, fill_value_or_bound, meaning, status in specs
    ]


def theorem_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("THM3740_0_kappa_audit", "CALIBRATION_RESULT", "The corpus supplies kappa=8*pi*G/c^4 in the macroscopic action, so G_N is currently calibrated/inserted, not derived from parent coefficients.", "This answers the Newton-constant question cleanly."),
        ("THM3740_1_ppn_closure", "CONDITIONAL_BOUND_ROUTE", "If the base equation is GR plus S g_mu_nu and S=O(K^m), then local PPN deviations are inherited as O(K^m) corrections around GR.", "This is a legitimate local closure route, but it depends on the S functional and operator constants."),
        ("THM3740_2_parent_gap", "PARENT_DERIVATION_GAP", "The corpus does not yet provide source-owned A2 or kappa_X=K_m/Z_X for the parent-owned beta/G_N derivation route.", "The strict derivation ladder remains unfinished."),
        ("THM3740_3_variable_choice", "NORMALIZATION_WARNING", "A1 is convention-dependent until X is fixed; X=Phi/c^2 and X=Gamma_kappa give different A1 values.", "This prevents a fake coefficient extraction from a naming choice."),
        ("THM3740_4_claim_gate", "ANTI_OVERCLAIM", "3740 promotes G_N only to calibrated closure and PPN only to a bound schema; no local-GR proof is claimed.", "Private discipline stays intact."),
    ]
    return [
        {
            **base(timestamp),
            "theorem_id": theorem_id,
            "status": status,
            "clause": clause,
            "meaning": meaning,
            "claim_allowed": False,
        }
        for theorem_id, status, clause, meaning in specs
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("CG3740_0_sources", "target corpus sources inspected", True, "action, gravity, and weak-field relativity files are source-registered"),
        ("CG3740_1_gn_closure", "G_N calibrated closure identified", True, "kappa=8*pi*G/c^4 is source-backed"),
        ("CG3740_2_ppn_bound_schema", "PPN O(K^m) closure bound identified", True, "gamma/beta O(K^m) and K_solar scale are source-backed"),
        ("CG3740_3_parent_A1", "A1 parent-owned", False, "only convention-dependent first-order match found"),
        ("CG3740_4_parent_A2", "A2 parent-owned", False, "no 2PN parent expansion found"),
        ("CG3740_5_parent_kappa", "kappa_X parent-owned", False, "no K_m/Z_X source response extracted"),
        ("CG3740_6_numeric_beta", "beta_NP numeric executable", False, "operator constants and parent coefficients remain open"),
        ("CG3740_7_local_GR_claim", "local GR/Newton claim allowed", False, "closure route is promising but not a full derivation"),
    ]
    return [
        {
            **base(timestamp),
            "gate_id": gate_id,
            "gate": gate,
            "passed": passed,
            "rationale": rationale,
            "claim_allowed": False,
        }
        for gate_id, gate, passed, rationale in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("DEC3740_0_result", "SPLIT_PARENT_DERIVATION_FROM_CALIBRATED_GR_CLOSURE", "This avoids throwing away useful local-GR reduction evidence while staying honest about what is not parent-derived."),
        ("DEC3740_1_gn", "G_N_CURRENTLY_CALIBRATED_NOT_DERIVED", "The corpus uses the standard Einstein-Hilbert coupling; deriving G_N requires a deeper A1*K_m/Z_X calculation not yet present."),
        ("DEC3740_2_ppn", "PPN_ROUTE_NOW_BOUND_SCHEMA", "Existing MTS gravity notes support a local O(K^m) residual route, which should be formalized as a theorem with constants."),
        ("DEC3740_3_next", "NEXT_PROVE_LOCAL_GR_CLOSURE_BOUND", "The best next step is proving the S g_mu_nu perturbation bound from the field equation, then linking it to beta_NP coefficients."),
    ]
    return [
        {
            **base(timestamp),
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "claim_allowed": False,
        }
        for decision_id, decision, rationale in specs
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [{
        **base(timestamp),
        "status_id": "STATUS3740_0",
        "status": "GN_CALIBRATED_CLOSURE_AND_PPN_OKM_BOUND_FOUND_PARENT_A2_KAPPA_MISSING",
        "summary": "3740 finds source-backed calibrated-GR closure evidence: kappa=8*pi*G/c^4, GR recovery when the correction vanishes, and PPN residuals O(K^m); strict parent-owned A2 and kappa_X remain missing.",
        "claim_allowed": False,
    }]


def next_target_rows(timestamp: str) -> list[dict[str, object]]:
    return [{
        **base(timestamp),
        "next_id": "NEXT3740_0",
        "target_doc": "3741-Y5-R2FR-local-GR-closure-bound-from-Sgmunu-perturbation.md",
        "target_script": "scripts/Y5_R2FR_3741_local_GR_closure_bound_from_Sgmunu_perturbation.py",
        "objective": "prove the calibrated-GR closure theorem: from G_mu_nu + S g_mu_nu = kappa T_mu_nu with S=O(K^m), derive Newton/PPN residual bounds and map them into the 3738 beta_NP ledger",
        "success_gate": "C_beta_2PN and gamma residual receive source-backed O(K^m) bound rows while parent-owned A2/kappa_X remain explicitly separate",
        "claim_allowed": False,
    }]


def write_doc(paths: dict[str, Path], grouped: dict[str, list[dict[str, object]]]) -> None:
    lines = [
        "# 3740 - Parent Action Coefficient Extraction: A1, A2, G1, kappa",
        "",
        "## Status",
        "- `GN_CALIBRATED_CLOSURE_AND_PPN_OKM_BOUND_FOUND_PARENT_A2_KAPPA_MISSING`",
        "- The corpus supports a calibrated-GR closure route, not yet a parent-owned derivation of `G_N` or `A2=A1^2`.",
        "- This checkpoint separates useful local-GR reduction evidence from still-missing parent coefficients.",
        "",
        "## Extracted Coefficient Ledger",
    ]
    for row in grouped["parent_coefficients"]:
        lines.append(f"- `{row['symbol']}` `{row['extraction_status']}`: {row['extracted_value_or_bound']} | next: {row['next_action']}")
    lines.extend(["", "## Calibrated-GR Closure Route"])
    for row in grouped["closure_routes"]:
        lines.append(f"- `{row['closure_id']}` `{row['status']}`: {row['formula_or_bound']} | {row['meaning']}")
    lines.extend(["", "## Fill Rows"])
    for row in grouped["fills"]:
        lines.append(f"- `{row['target_symbol']}` `{row['status']}`: {row['fill_value_or_bound']} | {row['meaning']}")
    lines.extend(["", "## Evidence Rows"])
    for row in grouped["evidence"]:
        if row["found"]:
            lines.append(f"- `{row['evidence_id']}` `{row['category']}`: {row['path']}:{row['line_number']} | {row['extraction_meaning']}")
    lines.extend(["", "## Theorem Rows"])
    for row in grouped["theorems"]:
        lines.append(f"- `{row['theorem_id']}` `{row['status']}`: {row['clause']} | {row['meaning']}")
    lines.extend(["", "## Decisions"])
    for row in grouped["decisions"]:
        lines.append(f"- `{row['decision_id']}` `{row['decision']}` | {row['rationale']}")
    lines.extend(["", "## Next Target"])
    next_row = grouped["next_target"][0]
    lines.append(f"- `{next_row['target_doc']}`")
    lines.append(f"- Objective: {next_row['objective']}")
    paths["doc"].write_text("\n".join(lines) + "\n", encoding="utf-8")


def validation_rows(timestamp: str, paths: dict[str, Path]) -> list[dict[str, object]]:
    sources = parse_csv(paths["source_register"])
    evidence = parse_csv(paths["evidence"])
    coefficients = parse_csv(paths["parent_coefficients"])
    closure_routes = parse_csv(paths["closure_routes"])
    fills = parse_csv(paths["fills"])
    claim_gates = parse_csv(paths["claim_gates"])
    next_target = parse_csv(paths["next_target"])
    validation_paths = [path for key, path in paths.items() if key != "validation"]
    formalization_leaks = []
    if FORMALIZATION.exists():
        formalization_leaks = list(FORMALIZATION.rglob("*3740*"))
    checks = [
        ("sources_exist", "all source paths exist", all(row["exists"] == "True" for row in sources)),
        ("needles_found", "all source needles found", all(row["needle_found"] == "True" for row in sources)),
        ("outputs_exist", "all outputs exist", all(path.exists() for path in validation_paths)),
        ("csv_parse", "all generated CSVs parse", all(len(parse_csv(path)) > 0 for key, path in paths.items() if key not in {"doc", "validation"})),
        ("evidence_found", "all targeted evidence rows found", len(evidence) == 15 and all(row["found"] == "True" for row in evidence)),
        ("coefficient_rows", "eight parent coefficient rows classified", len(coefficients) == 8),
        ("gn_calibrated", "G_N classified as calibrated closure", any(row["symbol"] == "kappa_X" and row["extraction_status"] == "CALIBRATED_GR_COUPLING_PRESENT_NOT_PARENT_DERIVED" for row in coefficients)),
        ("A2_blocked", "A2 remains parent-blocked", any(row["symbol"] == "A2" and row["extraction_status"] == "MISSING_PARENT_2PN_EXPANSION" for row in coefficients)),
        ("closure_routes", "closure and parent routes separated", len(closure_routes) == 4 and any(row["route"] == "calibrated_GR_closure" for row in closure_routes) and any(row["route"] == "parent_owned_derivation" for row in closure_routes)),
        ("fills", "G_N and PPN fill rows emitted", len(fills) == 4 and any(row["target_symbol"] == "G_N_eff" for row in fills) and any(row["target_symbol"] == "C_beta_2PN" for row in fills)),
        ("claim_gates_blocked", "claim gates block promotion", all(row["claim_allowed"] == "False" for row in claim_gates)),
        ("next_target_3741", "next target is local GR closure bound", next_target[0]["target_doc"] == "3741-Y5-R2FR-local-GR-closure-bound-from-Sgmunu-perturbation.md"),
        ("doc_core_terms", "doc contains calibrated closure and parent gap", all(token in read_text(paths["doc"]) for token in ["calibrated-GR closure", "A2=A1^2", "O(K^m)", "G_N"])),
        ("no_formalization_leak", "no 3740 files in formalization-workbench", len(formalization_leaks) == 0),
    ]
    return [
        {
            **base(timestamp),
            "validation_id": validation_id,
            "description": description,
            "result": "PASS" if result else "FAIL",
            "details": "",
        }
        for validation_id, description, result in checks
    ]


def main() -> None:
    timestamp = stamp()
    paths = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3740_SOURCE_REGISTER.csv",
        "evidence": RESIDUALS / "P8_Y5_R2FR_3740_CORPUS_EVIDENCE_ROWS.csv",
        "parent_coefficients": RESIDUALS / "P8_Y5_R2FR_3740_PARENT_COEFFICIENT_EXTRACTION_ROWS.csv",
        "closure_routes": RESIDUALS / "P8_Y5_R2FR_3740_CLOSURE_ROUTE_ROWS.csv",
        "fills": RESIDUALS / "P8_Y5_R2FR_3740_FILL_ROWS.csv",
        "theorems": RESIDUALS / "P8_Y5_R2FR_3740_THEOREM_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3740_CLAIM_GATES.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3740_DECISION_ROWS.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3740_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3740_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3740_VALIDATION.csv",
        "doc": DOC,
    }
    grouped = {
        "source_register": source_register(timestamp),
        "evidence": evidence_rows(timestamp),
        "parent_coefficients": parent_coefficient_rows(timestamp),
        "closure_routes": closure_route_rows(timestamp),
        "fills": fill_rows(timestamp),
        "theorems": theorem_rows(timestamp),
        "claim_gates": claim_gate_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "status": status_rows(timestamp),
        "next_target": next_target_rows(timestamp),
    }
    for key, rows in grouped.items():
        write_csv(paths[key], rows)
    write_doc(paths, grouped)
    write_csv(paths["validation"], validation_rows(timestamp, paths))
    failures = [row for row in parse_csv(paths["validation"]) if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3740 validation failed: {failures}")
    print("wrote 3740 checkpoint: calibrated-GR closure evidence extracted; parent A2/kappa still missing")


if __name__ == "__main__":
    main()
