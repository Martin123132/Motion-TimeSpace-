from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3739"
BRANCH_ID = "MTS_R2FR_Y5_PARENT_2PN_BETA_MAP_AND_GN_NORMALIZATION_3739"
DOC = ROOT / "3739-Y5-R2FR-parent-2PN-beta-map-and-GN-normalization.md"

DOC_3736 = ROOT / "3736-Y5-R2FR-Newton-PPN-response-coefficients-from-weak-field-limit.md"
DOC_3738 = ROOT / "3738-Y5-R2FR-beta-assembly-interface-and-open-coefficient-ledger.md"
NEXT_3738 = RESIDUALS / "P8_Y5_R2FR_3738_NEXT_TARGET.csv"
VALIDATION_3738 = RESIDUALS / "P8_Y5_BRR545_3738_VALIDATION.csv"
OPEN_INPUTS_3738 = RESIDUALS / "P8_Y5_R2FR_3738_OPEN_INPUT_LEDGER.csv"
BETA_FORMULAS_3738 = RESIDUALS / "P8_Y5_R2FR_3738_BETA_FORMULA_ROWS.csv"
BNP_3736 = RESIDUALS / "P8_Y5_R2FR_3736_BNP_COEFFICIENT_ROWS.csv"


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


def source_register(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("doc_3736", DOC_3736, "C_beta_2PN", "3736 exposes the missing second-order beta row"),
        ("doc_3738", DOC_3738, "G_N", "3738 selects the 2PN beta/G_N target"),
        ("next_3738", NEXT_3738, "3739-Y5-R2FR-parent-2PN-beta-map-and-GN-normalization.md", "3738 handoff"),
        ("validation_3738", VALIDATION_3738, "next_target_3739", "3738 validation"),
        ("open_inputs_3738", OPEN_INPUTS_3738, "C_beta_2PN", "3738 open coefficient/input ledger"),
        ("beta_formulas_3738", BETA_FORMULAS_3738, "beta_NP_diag", "3738 beta_NP assembly formula"),
        ("bnp_3736", BNP_3736, "BNP3736_4_beta_phi", "3736 beta coefficient source row"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append({
            **base(timestamp),
            "source_id": source_id,
            "path": str(path),
            "exists": exists,
            "needle": needle,
            "needle_found": needle in text,
            "role": role,
            "claim_allowed": False,
        })
    return rows


def weak_field_expansion_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("EXP3739_0_metric_00", "effective_matter_metric", "g00_eff = -1 + 2*A1*X - 2*A2*X^2 + O(X^3)", "A1 is the Newtonian potential normalization; A2 is the second-order lapse coefficient.", "MISSING_PARENT_METRIC_EXPANSION"),
        ("EXP3739_1_spatial_metric", "effective_matter_metric", "gij_eff = (1 + 2*G1*X)*delta_ij + O(X^2)", "G1/A1 is the PPN gamma ratio after first-order normalization.", "MISSING_PARENT_SPATIAL_EXPANSION"),
        ("EXP3739_2_parent_field_equation", "parent_field_equation", "L_X X = kappa_X*rho_eff; quasi-static local limit nabla^2 X = kappa_X*rho_eff", "kappa_X is the source response fixed by the parent kinetic/coupling normalization.", "MISSING_PARENT_SOURCE_NORMALIZATION"),
        ("EXP3739_3_newton_potential_match", "newtonian_limit", "U = A1*X; nabla^2 U = A1*kappa_X*rho_eff", "The first-order metric coefficient maps the parent potential X to the Newtonian potential U.", "DERIVED_MATCH_IF_A1_NONZERO"),
    ]
    return [
        {
            **base(timestamp),
            "expansion_id": expansion_id,
            "sector": sector,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "source_status": "parent_coefficients_not_yet_extracted",
            "claim_allowed": False,
        }
        for expansion_id, sector, formula, meaning, status in specs
    ]


def beta_map_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("BETA3739_0_ppn_compare", "beta_MTS = A2/A1^2", "Compare g00_eff=-1+2*A1*X-2*A2*X^2 with PPN g00=-1+2*U-2*beta*U^2 using U=A1*X.", "DERIVED_ALGEBRAIC_MAP"),
        ("BETA3739_1_residual", "beta_MTS - 1 = (A2-A1^2)/A1^2", "The local-GR beta residual is exactly the failure of the parent second-order coefficient to equal the square of the first-order coefficient.", "DERIVED_RESIDUAL_CONDITION"),
        ("BETA3739_2_fill_C_beta_2PN", "C_beta_2PN = abs(A2/A1^2 - 1)", "This is the 3738 beta-row coefficient if A1 and A2 are finite and source-owned.", "SYMBOLIC_FILL_VALUES_MISSING"),
        ("BETA3739_3_zero_condition", "C_beta_2PN = 0 iff A2=A1^2", "The non-smuggled local-GR route is a parent theorem forcing A2=A1^2, not a fitted beta row.", "ZERO_THEOREM_TARGET"),
    ]
    return [
        {
            **base(timestamp),
            "beta_map_id": beta_map_id,
            "formula": formula,
            "derivation": derivation,
            "status": status,
            "required_parent_inputs": "A1;A2;gauge;matter_metric_identification",
            "fills_3738_symbol": "C_beta_2PN" if "C_beta_2PN" in formula else "",
            "claim_allowed": False,
        }
        for beta_map_id, formula, derivation, status in specs
    ]


def gn_normalization_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("GN3739_0_first_order_match", "4*pi*G_N_eff = A1*kappa_X", "From U=A1*X and nabla^2 X=kappa_X*rho_eff, the Newtonian Poisson equation gives nabla^2 U=A1*kappa_X*rho_eff.", "DERIVED_ALGEBRAIC_MAP"),
        ("GN3739_1_action_coupling_form", "G_N_eff = A1*K_m/(4*pi*Z_X) times unit_factor_CG", "If the parent local quadratic action gives Z_X*L_X X = K_m*rho_eff, then kappa_X=K_m/Z_X up to the unit/sign convention.", "CONDITIONAL_PARENT_ACTION_MAP"),
        ("GN3739_2_derivation_vs_calibration", "G_N is derived only if A1, K_m, Z_X, and unit_factor_CG are fixed by the parent; otherwise G_N is a calibrated closure constant.", "This mirrors GR's coupling constant discipline: calibration is allowed for a model fit, but it is not a derivation.", "ANTI_OVERCLAIM"),
        ("GN3739_3_positive_attraction_gate", "A1*kappa_X > 0", "Attractive Newtonian gravity requires the first-order metric/source product to have the observed sign.", "SIGN_GATE_VALUES_MISSING"),
    ]
    return [
        {
            **base(timestamp),
            "gn_map_id": gn_map_id,
            "formula": formula,
            "derivation": derivation,
            "status": status,
            "required_parent_inputs": "A1;kappa_X;rho_eff_normalization;unit_factor_CG",
            "fills_3738_symbol": "rho_eff_norm/G_N_normalization" if "G_N" in formula or "kappa" in formula else "",
            "claim_allowed": False,
        }
        for gn_map_id, formula, derivation, status in specs
    ]


def parent_input_ledger(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("PIN3739_A1", "A1", "first-order g00 parent coefficient", "finite nonzero; sign chosen so U=A1*X matches attraction", "P0", "extract from parent matter metric/lapse expansion"),
        ("PIN3739_A2", "A2", "second-order g00 parent coefficient", "finite and tested against A1^2", "P0", "derive from 2PN parent metric expansion"),
        ("PIN3739_G1", "G1", "first-order spatial metric coefficient", "G1=A1 for gamma=1 local-GR recovery", "P1", "extract alongside A1 from spatial metric expansion"),
        ("PIN3739_kappa_X", "kappa_X", "quasi-static source response of parent potential", "finite with A1*kappa_X>0", "P0", "derive from parent field equation or calibrated Poisson closure"),
        ("PIN3739_ZX", "Z_X", "parent kinetic normalization for X", "positive or signed with stability convention", "P1", "extract from quadratic parent action"),
        ("PIN3739_Km", "K_m", "matter/source coupling to X", "finite with source-normalization convention", "P1", "extract from matter coupling/current term"),
        ("PIN3739_unit_factor", "unit_factor_CG", "unit conversion between parent variables and SI/PPN Poisson form", "fixed dimensional convention", "P1", "state c/unit powers before numeric G_N comparison"),
        ("PIN3739_gauge", "weak_field_gauge", "coordinate/gauge convention for PPN comparison", "must match standard PPN gauge or include transform", "P0", "derive gauge map rather than comparing raw coordinates"),
    ]
    return [
        {
            **base(timestamp),
            "input_id": input_id,
            "symbol": symbol,
            "meaning": meaning,
            "required_property": required_property,
            "priority": priority,
            "next_action": next_action,
            "current_status": "MISSING_PARENT_EXTRACTION",
            "valid_for_numeric_run": False,
            "claim_allowed": False,
        }
        for input_id, symbol, meaning, required_property, priority, next_action in specs
    ]


def fill_3738_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("FILL3739_0_C_beta_2PN", "C_beta_2PN", "abs(A2/A1^2 - 1)", "P8_Y5_R2FR_3738_OPEN_INPUT_LEDGER.csv", "ready only after A1 and A2 are source-owned in a fixed weak-field gauge", False),
        ("FILL3739_1_GN_eff", "G_N_eff", "A1*kappa_X/(4*pi)", "P8_Y5_R2FR_3738_OPEN_INPUT_LEDGER.csv", "derivable only if parent fixes A1 and kappa_X; otherwise calibrated closure", False),
        ("FILL3739_2_rho_eff_norm", "rho_eff_norm", "rho_eff normalization entering kappa_X and measured-G calibration", "P8_Y5_R2FR_3738_OPEN_INPUT_LEDGER.csv", "requires matter/source normalization and lab-G convention", False),
        ("FILL3739_3_gamma_condition", "Phi0_inv/gamma row support", "gamma_MTS=G1/A1; gamma residual vanishes iff G1=A1", "P8_Y5_R2FR_3738_OPEN_INPUT_LEDGER.csv", "A1 and G1 must be extracted before gamma row can be closed", False),
    ]
    return [
        {
            **base(timestamp),
            "fill_id": fill_id,
            "target_symbol": target_symbol,
            "symbolic_fill": symbolic_fill,
            "target_file": target_file,
            "condition": condition,
            "ready_to_patch_3738": ready,
            "claim_allowed": False,
        }
        for fill_id, target_symbol, symbolic_fill, target_file, condition, ready in specs
    ]


def theorem_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("THM3739_0_beta_map", "DERIVED_ALGEBRAIC_MAP", "For g00_eff=-1+2*A1*X-2*A2*X^2 and U=A1*X, the PPN beta parameter is beta=A2/A1^2.", "This turns the vague 2PN beta blocker into a concrete parent-coefficient equality."),
        ("THM3739_1_beta_zero", "ZERO_THEOREM_TARGET", "Local GR beta recovery follows if the parent action or quotient geometry proves A2=A1^2 in the local weak-field gauge.", "This is the clean no-fit route for the beta row."),
        ("THM3739_2_gn_map", "DERIVED_ALGEBRAIC_MAP", "The effective Newton constant obeys 4*pi*G_N_eff=A1*kappa_X in the matched Poisson limit.", "MTS can only claim to derive G_N if the parent fixes both factors rather than calibrating them."),
        ("THM3739_3_gr_reduction_conditions", "LOCAL_GR_CONDITION_SET", "A minimal local-GR gate is A1 nonzero, G1=A1, A2=A1^2, positive A1*kappa_X, no preferred-frame leakage, and controlled boundary/tail terms.", "This is a compact target list for actual derivation, not an empirical handwave."),
        ("THM3739_4_claim_gate", "ANTI_OVERCLAIM", "This checkpoint derives the algebraic gates but does not source the parent coefficients.", "No local-GR, PPN, or Newton-constant pass is claimed."),
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
        ("CG3739_0_beta_formula", "beta=A2/A1^2 map derived", True, "algebraic PPN comparison is explicit"),
        ("CG3739_1_gn_formula", "G_N_eff=A1*kappa_X/(4*pi) map derived", True, "first-order Poisson normalization is explicit"),
        ("CG3739_2_A1_source", "A1 source-owned", False, "parent metric expansion not extracted"),
        ("CG3739_3_A2_source", "A2 source-owned", False, "2PN parent metric expansion not extracted"),
        ("CG3739_4_beta_zero", "A2=A1^2 proved", False, "zero theorem not proved"),
        ("CG3739_5_kappa_source", "kappa_X or K_m/Z_X source-owned", False, "parent source normalization not extracted"),
        ("CG3739_6_gn_derived", "G_N numerically derived rather than calibrated", False, "parent constants not fixed"),
        ("CG3739_7_local_gr_claim", "local GR/Newton claim allowed", False, "compact gate set is derived but not closed"),
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
        ("DEC3739_0_progress", "LOCAL_GR_GATE_REDUCED_TO_PARENT_COEFFICIENTS", "The beta and Newton-G problems are now concrete coefficient equalities: A2=A1^2 and 4*pi*G_N=A1*kappa_X."),
        ("DEC3739_1_GN_stance", "G_N_DERIVATION_REQUIRES_PARENT_FIXING", "If the parent does not fix A1 and kappa_X, MTS may still calibrate G_N like GR, but must not call that a derivation."),
        ("DEC3739_2_next", "NEXT_EXTRACT_PARENT_ACTION_COEFFICIENTS", "The best next move is to hunt the corpus/action notes for the actual A1, A2, G1, kappa_X, Z_X, and K_m coefficients."),
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
        "status_id": "STATUS3739_0",
        "status": "PARENT_2PN_AND_GN_MAP_DERIVED_PARENT_COEFFICIENTS_MISSING",
        "summary": "3739 derives the parent coefficient gates beta=A2/A1^2 and 4*pi*G_N_eff=A1*kappa_X; local-GR/Newton recovery now depends on extracting or proving A2=A1^2, G1=A1, and the source normalization.",
        "claim_allowed": False,
    }]


def next_target_rows(timestamp: str) -> list[dict[str, object]]:
    return [{
        **base(timestamp),
        "next_id": "NEXT3739_0",
        "target_doc": "3740-Y5-R2FR-parent-action-coefficient-extraction-A1-A2-G1-kappa.md",
        "target_script": "scripts/Y5_R2FR_3740_parent_action_coefficient_extraction_A1_A2_G1_kappa.py",
        "objective": "search and extract the parent action/effective metric coefficients A1, A2, G1, kappa_X, Z_X, and K_m from the corpus or mark them as calibrated closure inputs",
        "success_gate": "at least one of C_beta_2PN, gamma_MTS-1, or G_N_eff moves from symbolic gate to source-owned theorem/calibration row",
        "claim_allowed": False,
    }]


def write_doc(paths: dict[str, Path], grouped: dict[str, list[dict[str, object]]]) -> None:
    lines = [
        "# 3739 - Parent 2PN Beta Map and G_N Normalization",
        "",
        "## Status",
        "- `PARENT_2PN_AND_GN_MAP_DERIVED_PARENT_COEFFICIENTS_MISSING`",
        "- The local-GR problem is now reduced to parent coefficient gates rather than a vague missing-coupling complaint.",
        "- No local-GR, PPN, or Newton-constant claim is made until the parent coefficients are extracted or explicitly calibrated.",
        "",
        "## Weak-Field Parent Expansion",
    ]
    for row in grouped["expansion"]:
        lines.append(f"- `{row['expansion_id']}` `{row['sector']}`: {row['formula']} | {row['meaning']}")
    lines.extend(["", "## 2PN Beta Map"])
    for row in grouped["beta_map"]:
        lines.append(f"- `{row['beta_map_id']}` `{row['status']}`: {row['formula']} | {row['derivation']}")
    lines.extend(["", "## Newton Constant Normalization"])
    for row in grouped["gn_map"]:
        lines.append(f"- `{row['gn_map_id']}` `{row['status']}`: {row['formula']} | {row['derivation']}")
    lines.extend(["", "## Fill Rows for 3738"])
    for row in grouped["fill_3738"]:
        lines.append(f"- `{row['fill_id']}` `{row['target_symbol']}` -> `{row['symbolic_fill']}` | {row['condition']}")
    lines.extend(["", "## Parent Input Ledger"])
    for row in grouped["parent_inputs"]:
        lines.append(f"- `{row['symbol']}` `{row['priority']}`: {row['meaning']} | next: {row['next_action']}")
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
    expansion = parse_csv(paths["expansion"])
    beta_map = parse_csv(paths["beta_map"])
    gn_map = parse_csv(paths["gn_map"])
    parent_inputs = parse_csv(paths["parent_inputs"])
    fill_3738 = parse_csv(paths["fill_3738"])
    claim_gates = parse_csv(paths["claim_gates"])
    next_target = parse_csv(paths["next_target"])
    validation_paths = [path for key, path in paths.items() if key != "validation"]
    formalization_leaks = []
    if FORMALIZATION.exists():
        formalization_leaks = list(FORMALIZATION.rglob("*3739*"))
    checks = [
        ("sources_exist", "all source paths exist", all(row["exists"] == "True" for row in sources)),
        ("needles_found", "all source needles found", all(row["needle_found"] == "True" for row in sources)),
        ("outputs_exist", "all outputs exist", all(path.exists() for path in validation_paths)),
        ("csv_parse", "all generated CSVs parse", all(len(parse_csv(path)) > 0 for key, path in paths.items() if key not in {"doc", "validation"})),
        ("expansion_rows", "weak-field expansion rows present", len(expansion) == 4 and all(token in read_text(paths["expansion"]) for token in ["g00_eff", "kappa_X", "U = A1*X"])),
        ("beta_map", "2PN beta map derived", len(beta_map) == 4 and all(token in read_text(paths["beta_map"]) for token in ["A2/A1^2", "A2=A1^2", "C_beta_2PN"])),
        ("gn_map", "G_N normalization map derived", len(gn_map) == 4 and all(token in read_text(paths["gn_map"]) for token in ["G_N_eff", "A1*kappa_X", "K_m/(4*pi*Z_X)"])),
        ("parent_inputs", "parent input extraction ledger present", len(parent_inputs) == 8),
        ("fill_3738", "3738 fill rows present", len(fill_3738) == 4 and any(row["target_symbol"] == "C_beta_2PN" for row in fill_3738)),
        ("claim_gates_blocked", "claim gates block promotion", all(row["claim_allowed"] == "False" for row in claim_gates)),
        ("next_target_3740", "next target is parent action coefficient extraction", next_target[0]["target_doc"] == "3740-Y5-R2FR-parent-action-coefficient-extraction-A1-A2-G1-kappa.md"),
        ("doc_core_terms", "doc contains beta/G_N conditions", all(token in read_text(paths["doc"]) for token in ["beta=A2/A1^2", "4*pi*G_N_eff=A1*kappa_X", "A2=A1^2", "G1=A1"])),
        ("no_formalization_leak", "no 3739 files in formalization-workbench", len(formalization_leaks) == 0),
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
        "source_register": RESIDUALS / "P8_Y5_R2FR_3739_SOURCE_REGISTER.csv",
        "expansion": RESIDUALS / "P8_Y5_R2FR_3739_WEAK_FIELD_EXPANSION_ROWS.csv",
        "beta_map": RESIDUALS / "P8_Y5_R2FR_3739_2PN_BETA_MAP_ROWS.csv",
        "gn_map": RESIDUALS / "P8_Y5_R2FR_3739_GN_NORMALIZATION_ROWS.csv",
        "parent_inputs": RESIDUALS / "P8_Y5_R2FR_3739_PARENT_INPUT_LEDGER.csv",
        "fill_3738": RESIDUALS / "P8_Y5_R2FR_3739_FILL_3738_ROWS.csv",
        "theorems": RESIDUALS / "P8_Y5_R2FR_3739_THEOREM_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3739_CLAIM_GATES.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3739_DECISION_ROWS.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3739_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3739_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3739_VALIDATION.csv",
        "doc": DOC,
    }
    grouped = {
        "source_register": source_register(timestamp),
        "expansion": weak_field_expansion_rows(timestamp),
        "beta_map": beta_map_rows(timestamp),
        "gn_map": gn_normalization_rows(timestamp),
        "parent_inputs": parent_input_ledger(timestamp),
        "fill_3738": fill_3738_rows(timestamp),
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
        raise SystemExit(f"3739 validation failed: {failures}")
    print("wrote 3739 checkpoint: parent beta/G_N maps derived, parent coefficients still missing")


if __name__ == "__main__":
    main()
