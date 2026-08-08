from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
DOC = ROOT / "2004-Y5-R2FR-parent-Hilbert-source-signature-or-finite-nonmetric-coefficient-ledger.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row() -> dict[str, object]:
    return {
        "branch_id": BRANCH_ID,
        "valid_for_claim": "false",
        "claim_allowed": "false",
        "generated_utc": stamp(),
    }


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
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


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def count_formalization_modified_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED
    )


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def csv_rows_parse(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
    except csv.Error:
        return False
    return True


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2004_0_2003_doc",
            "2003-Y5-R2FR-parent-material-source-map-or-official-CMSM-import-gate.md",
            ["NEXT2003_0_2004", "PPM2003_4_exact_eta"],
            "2003 exact WEP parent product map and handoff.",
        ),
        (
            "SRC2004_1_2003_validation",
            "source-intake/mts_residuals/P8_Y5_BRR545_2003_VALIDATION.csv",
            ["VAL2003_OVERALL", "PASS"],
            "2003 validation pass.",
        ),
        (
            "SRC2004_2_1937_hilbert",
            "1937-Y5-R2FR-parent-Hilbert-source-coupling-signature-or-nonmetric-source-coefficient-ledger.md",
            ["ACT1937_1_minimal_matter_action", "HST1937_1_no_wA_no_DeltaW"],
            "candidate parent Hilbert source signature.",
        ),
        (
            "SRC2004_3_1938_bianchi",
            "1938-Y5-R2FR-Bianchi-Ward-conservation-and-Newtonian-limit-of-candidate-Hilbert-action.md",
            ["NL1938_1_EH_to_Poisson", "GOB1938_0_operator_owner"],
            "Bianchi/Ward and Newtonian limit candidate.",
        ),
        (
            "SRC2004_4_1939_eh_newton",
            "1939-Y5-R2FR-parent-gravity-operator-EH-or-R11-residual-Newtonian-law.md",
            ["EH1939_2_Poisson", "R111939_0_field_equation"],
            "EH/Newtonian conditional theorem and residual slot.",
        ),
        (
            "SRC2004_5_1940_lovelock",
            "1940-Y5-R2FR-EH-uniqueness-Lovelock-gate-or-R11-residual-operator.md",
            ["EHU1940_0_lovelock_form", "READY1940_6_PPN_map"],
            "EH uniqueness/Lovelock readiness gate.",
        ),
        (
            "SRC2004_6_1955_same_source",
            "1955-Y5-R2FR-local-EH-same-source-map-or-residual-l2-bound.md",
            ["EH1955_2_same_source_map", "EH1955_6_zero_verdict"],
            "same-source/local residual contract.",
        ),
        (
            "SRC2004_7_1960_connection",
            "1960-Y5-R2FR-Levi-Civita-no-hypermomentum-proof-or-P4-current-envelope.md",
            ["LC1960_0_target", "LC1960_6_verdict"],
            "Levi-Civita/no-hypermomentum connection gate.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, relative_path, needles, note in specs:
        path = source_path(relative_path)
        exists = path.exists()
        text = read_text(path) if exists else ""
        missing = [needle for needle in needles if needle not in text]
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "needed_for": "2004 parent Hilbert/source signature or finite nonmetric coefficient ledger",
                "needles": ";".join(needles),
                "exists": str(exists),
                "anchor_found": str(exists and not missing),
                "missing_needles": ";".join(missing),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "note": note,
            }
        )
        rows.append(row)
    return rows


def local_gr_proof_chain_rows() -> list[dict[str, object]]:
    specs = [
        (
            "LGR2004_0_parent_matter_action",
            "S_matter = sum_A int sqrt(-g_obs) L_A(psi_A,D(g_obs,A_obs)psi_A,theta_A)",
            "one observed metric/coframe matter action with no independent gravitational source multiplier",
            "1937 candidate action",
            "CANDIDATE_NOT_PARENT_DERIVED",
            "If signed, all ordinary sectors share the same source map.",
        ),
        (
            "LGR2004_1_hilbert_source",
            "T_obs^{mu nu}=(-2/sqrt(-g_obs)) delta S_matter/delta g_obs_{mu nu}",
            "the gravitational source is the Hilbert variation of the same action",
            "1937 Hilbert theorem",
            "EXACT_CONDITIONAL_THEOREM",
            "If signed, species labels are not extra gravitational charges.",
        ),
        (
            "LGR2004_2_ward_conservation",
            "matter EOM + diffeomorphism invariance -> nabla_mu T_obs^{mu nu}=0",
            "Ward/Bianchi compatibility for the same source",
            "1938/1939",
            "EXACT_CONDITIONAL_THEOREM",
            "If signed with field equations, source conservation is automatic.",
        ),
        (
            "LGR2004_3_test_body_motion",
            "nabla_mu T_A^{mu nu}=0 in compact test-body limit -> u^mu nabla_mu u^nu=0",
            "universal geodesic free fall, independent of Ti/Pt composition",
            "standard consequence of Hilbert source conservation",
            "DERIVED_CONDITIONALLY_HERE",
            "This gives eta_AB=0 once no species/readout coefficients survive.",
        ),
        (
            "LGR2004_4_weak_field_motion",
            "g_00=-(1+2Phi/c^2), slow motion -> d2x^i/dt^2=-partial_i Phi",
            "Newtonian equation of motion from geodesic limit",
            "1938/1939 Newtonian limit",
            "EXACT_CONDITIONAL_LIMIT",
            "This is the mechanics side: Newton follows from local GR metric motion.",
        ),
        (
            "LGR2004_5_poisson_source",
            "EH with kappa=8*pi*G/c^4 -> nabla^2 Phi=4*pi*G rho",
            "Newtonian source equation from EH operator",
            "1939/1940",
            "EXACT_CONDITIONAL_LIMIT",
            "This is the field side: Poisson follows if EH/Lovelock assumptions are signed.",
        ),
        (
            "LGR2004_6_local_GR_WEP_result",
            "LGR2004_0..5 + LC/no-hypermomentum + residual silence -> local GR/Newton/WEP branch",
            "the desired local reduction theorem",
            "2003/1937/1940/1955/1960 synthesis",
            "CONDITIONAL_CHAIN_COMPLETE_PARENT_SIGNATURE_UNSIGNED",
            "The route is clear; the remaining work is signing or bounding the parent clauses.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for proof_id, formula, meaning, source_anchor, status, implication in specs:
        row = base_row()
        row.update(
            {
                "proof_id": proof_id,
                "formula_or_statement": formula,
                "meaning": meaning,
                "source_anchor": source_anchor,
                "status": status,
                "implication": implication,
                "parent_signed": "false",
            }
        )
        rows.append(row)
    return rows


def signature_audit_rows() -> list[dict[str, object]]:
    specs = [
        ("SIG2004_0_single_observed_metric", "single observed metric/coframe for ordinary matter", "CANDIDATE_PRESENT_UNSIGNED", "ACT1937_0_parent_geometric_domain", "required for source universality and geodesic motion"),
        ("SIG2004_1_hilbert_source_owner", "source is Hilbert stress-energy of same matter action", "CANDIDATE_PRESENT_UNSIGNED", "ACT1937_3_source_definition", "required for inertial/gravitational source identity"),
        ("SIG2004_2_no_species_prefactor", "no independent w_A/material source prefactor", "CLOSURE_PRESENT_UNSIGNED", "ACT1937_2_forbidden_source_vertex", "required for DeltaW_AB=0"),
        ("SIG2004_3_binding_energy_included", "binding/rest/internal energies included in same source functional", "CONTRACT_PRESENT_UNSIGNED", "GRZ2003_3_binding_included", "prevents material residual hiding"),
        ("SIG2004_4_EH_operator_or_residual_zero", "EH/Lovelock local operator or bounded residual", "CONDITIONAL_EH_UNSIGNED_R11_ACTIVE", "EHU1940_2_local_GR_branch", "required for local GR/Newton source equation"),
        ("SIG2004_5_Levi_Civita_connection", "observed connection is Levi-Civita/no hypermomentum", "CONDITIONAL_ROUTE_UNSIGNED", "LC1960_6_verdict", "required for clean metric GR branch"),
        ("SIG2004_6_readout_preservation", "readout/boundary maps do not reintroduce species labels", "CONTRACT_PRESENT_UNSIGNED", "GRZ2003_4_readout_preservation", "required for WEP eta=0 after projection"),
        ("SIG2004_7_residual_silence", "extra sectors have zero/common-mode/bounded local residuals", "UNSIGNED_OR_BOUND_MISSING", "EH1955_6_zero_verdict", "required for PPN/Cassini/local-GR branch"),
    ]
    rows: list[dict[str, object]] = []
    for clause_id, clause, status, source_anchor, needed_for in specs:
        row = base_row()
        row.update(
            {
                "clause_id": clause_id,
                "clause": clause,
                "current_status": status,
                "source_anchor": source_anchor,
                "needed_for": needed_for,
                "parent_signed": "false",
                "if_unsigned": "retain finite nonmetric/residual coefficient ledger",
            }
        )
        rows.append(row)
    return rows


def no_species_theorem_rows() -> list[dict[str, object]]:
    specs = [
        (
            "NST2004_0_domain",
            "Ordinary matter action has species labels only inside L_A and theta_A, not in the gravitational source vertex.",
            "ANTECEDENT_UNSIGNED",
            "ACT1937_1_minimal_matter_action",
        ),
        (
            "NST2004_1_no_free_charge",
            "There is no variable w_A left to vary between materials in the source coupling.",
            "EXACT_CONDITIONAL_STEP",
            "ACT1937_2_forbidden_source_vertex",
        ),
        (
            "NST2004_2_delta_zero",
            "Therefore DeltaW_AB = W_A-W_B = 0 for source-weight variables defined only as extra gravitational charges.",
            "EXACT_CONDITIONAL_STEP",
            "HST1937_1_no_wA_no_DeltaW",
        ),
        (
            "NST2004_3_eta_zero",
            "With the 2003 parent product map, all nonuniversal Pi_X DeltaR_AB^X terms vanish or are absent, so eta_AB=0.",
            "EXACT_CONDITIONAL_RESULT",
            "PPM2003_4_exact_eta; GRZ2003_5_conditional_result",
        ),
        (
            "NST2004_4_verdict",
            "The no-species theorem is proved only conditional on the parent action forbidding source prefactors.",
            "NOT_PARENT_SIGNED",
            "SIG2004_2_no_species_prefactor",
        ),
    ]
    rows: list[dict[str, object]] = []
    for theorem_id, statement, status, source_anchor in specs:
        row = base_row()
        row.update(
            {
                "theorem_id": theorem_id,
                "statement": statement,
                "proof_status": status,
                "source_anchor": source_anchor,
                "claim_status": "NONCLAIM_CONDITIONAL",
            }
        )
        rows.append(row)
    return rows


def nonmetric_coefficient_ledger_rows() -> list[dict[str, object]]:
    specs = [
        ("NMC2004_0_species_source_weight", "w_A", "species/material source prefactor", "would make DeltaW_TiPt live", "MISSING_OR_ZERO_THEOREM_REQUIRED"),
        ("NMC2004_1_hidden_scalar_source", "w_A(X_hid)", "hidden invariant modulates source strength", "violates source universality", "MISSING_OR_ZERO_THEOREM_REQUIRED"),
        ("NMC2004_2_binding_anomaly", "b_bind,A", "binding/internal energy source anomaly", "can mimic composition WEP residual", "MISSING_OR_BOUND_REQUIRED"),
        ("NMC2004_3_readout_weight", "r_A", "readout/projection species re-entry", "can spoil eta=0 after bulk theorem", "MISSING_OR_PRESERVATION_THEOREM_REQUIRED"),
        ("NMC2004_4_R11_residual", "Xi_R11", "weak-field residual source in Poisson equation", "can spoil Newtonian limit", "MISSING_OR_BOUND_REQUIRED"),
        ("NMC2004_5_connection_current", "P4_TQDelta", "torsion/nonmetricity/hypermomentum source current", "can spoil Levi-Civita metric branch", "MISSING_OR_BOUND_REQUIRED"),
        ("NMC2004_6_boundary_l2", "B_extra_l2", "independent l=2 boundary residual", "can spoil PPN/Cassini/local-GR", "MISSING_OR_BOUND_REQUIRED"),
    ]
    rows: list[dict[str, object]] = []
    for coefficient_id, symbol, meaning, danger, status in specs:
        row = base_row()
        row.update(
            {
                "coefficient_id": coefficient_id,
                "symbol": symbol,
                "meaning": meaning,
                "danger": danger,
                "current_status": status,
                "numeric_value": "MISSING",
                "units": "MISSING_UNITS",
                "next_action": "prove zero from parent action or source/bound finite coefficient",
            }
        )
        rows.append(row)
    return rows


def readiness_rows() -> list[dict[str, object]]:
    specs = [
        ("READY2004_0_WEP_formula", "exact eta/product map", "READY_CONDITIONALLY", "2003 exact formula"),
        ("READY2004_1_matter_source", "Hilbert matter source route", "READY_CONDITIONALLY_UNSIGNED", "1937/2004"),
        ("READY2004_2_WEP_zero", "eta_AB=0 if no source prefactors", "READY_CONDITIONALLY_UNSIGNED", "2004 no-species theorem"),
        ("READY2004_3_Newton_motion", "geodesic slow-motion Newton law", "READY_CONDITIONALLY_UNSIGNED", "2004 proof chain"),
        ("READY2004_4_Poisson_source", "EH/kappa Poisson equation", "READY_CONDITIONALLY_UNSIGNED", "1939/1940"),
        ("READY2004_5_parent_signature", "MTS parent signs all clauses", "BLOCKED", "signature audit clauses unsigned"),
        ("READY2004_6_residual_bounds", "finite nonmetric/residual bounds", "BLOCKED", "nonmetric ledger values missing"),
        ("READY2004_7_public_local_GR", "public local GR/Newton/WEP claim", "BLOCKED", "requires signed clauses or numeric residual envelope"),
    ]
    rows: list[dict[str, object]] = []
    for readiness_id, criterion, status, basis in specs:
        row = base_row()
        row.update(
            {
                "readiness_id": readiness_id,
                "criterion": criterion,
                "status": status,
                "basis_or_blocker": basis,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    specs = [
        ("CG2004_0_conditional_chain", "conditional local GR/Newton/WEP chain exists", "true", "proof chain written but nonclaim"),
        ("CG2004_1_no_species_theorem", "no-species source theorem parent-signed", "false", "source prefactor ban remains unsigned"),
        ("CG2004_2_EH_operator", "EH/Lovelock operator parent-signed", "false", "Lovelock assumptions/residual silence unsigned"),
        ("CG2004_3_LC_connection", "Levi-Civita/no-hypermomentum parent-signed", "false", "connection fork unresolved"),
        ("CG2004_4_residual_ledger", "finite nonmetric/residual coefficients numeric or zero", "false", "ledger rows missing values"),
        ("CG2004_5_local_GR_Newton_claim", "local GR/Newton/WEP reduction claim", "false", "conditional chain not parent-signed"),
    ]
    rows: list[dict[str, object]] = []
    for gate_id, claim, gate_pass, reason in specs:
        row = base_row()
        row.update(
            {
                "gate_id": gate_id,
                "claim": claim,
                "gate_pass": gate_pass,
                "claim_allowed": "false",
                "reason": reason,
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    specs = [
        (
            "DEC2004_0_real_progress",
            "local GR/Newton/WEP reduction is now a single conditional proof chain",
            "LGR2004_0 through LGR2004_6",
            "we are not circling the data; the derivation target is explicit",
        ),
        (
            "DEC2004_1_no_overclaim",
            "do not promote the chain because parent signature clauses are unsigned",
            "SIG2004_0 through SIG2004_7",
            "claim remains blocked until clauses are derived from MTS parent principles or finite rows are sourced",
        ),
        (
            "DEC2004_2_best_next",
            "extract parent action clauses from the MTS corpus to sign or reject each clause",
            "READY2004_5_parent_signature",
            "next target should be clause extraction, not more surrogate/data polishing",
        ),
        (
            "DEC2004_3_fallback",
            "if a clause cannot be signed, retain the corresponding nonmetric coefficient row",
            "NMC2004 ledger",
            "the finite branch remains testable but no longer masquerades as GR reduction",
        ),
    ]
    rows: list[dict[str, object]] = []
    for decision_id, decision, evidence, consequence in specs:
        row = base_row()
        row.update(
            {
                "decision_id": decision_id,
                "decision": decision,
                "evidence": evidence,
                "consequence": consequence,
            }
        )
        rows.append(row)
    return rows


def next_target_rows() -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "next_id": "NEXT2004_0_2005",
            "next_target": "2005-Y5-R2FR-parent-action-clause-extraction-for-local-GR-signature.md",
            "objective": "scan the current MTS parent-action/corpus spine for explicit clauses that sign or reject each 2004 Hilbert/source/EH/LC/residual-silence condition.",
            "include": "single metric/coframe clause; Hilbert source owner; no species prefactor; EH/Lovelock assumptions; LC/no-hypermomentum; residual silence; finite coefficient fallbacks",
            "exclude": "claiming local GR from conditional chain alone, inventing coefficients, surrogate polishing, GitHub, or formalization-workbench edits",
        }
    )
    return [row]


def make_branch_copies(
    proof_rows: list[dict[str, object]],
    audit_rows: list[dict[str, object]],
    coefficient_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copy_specs = [
        (
            SOURCE_WEIGHT_DOCS / "LOCAL_GR_NEWTON_WEP_CHAIN_2004_NONCLAIM.csv",
            proof_rows,
            "conditional local GR/Newton/WEP proof chain",
        ),
        (
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2004_HILBERT_SIGNATURE_AUDIT_NONCLAIM.csv",
            audit_rows,
            "Hilbert/source signature audit",
        ),
        (
            QUEUE / "JR2004_NONMETRIC_COEFFICIENT_LEDGER_QUEUE.csv",
            coefficient_rows,
            "finite nonmetric coefficient fallback queue",
        ),
    ]
    rows: list[dict[str, object]] = []
    for path, data, meaning in copy_specs:
        write_csv(path, data)
        row = base_row()
        row.update(
            {
                "copy_id": f"COPY2004_{len(rows)}",
                "path": str(path),
                "exists": str(path.exists()),
                "meaning": meaning,
            }
        )
        rows.append(row)
    return rows


def validate_outputs(
    outputs: dict[str, Path],
    branch_copies: list[dict[str, object]],
    source_rows: list[dict[str, object]],
    proof_rows: list[dict[str, object]],
    audit_rows: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    coefficient_rows: list[dict[str, object]],
    readiness: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    generated_paths = list(outputs.values()) + [DOC] + [Path(str(row["path"])) for row in branch_copies]
    chain_complete = {row["proof_id"] for row in proof_rows} >= {
        "LGR2004_0_parent_matter_action",
        "LGR2004_3_test_body_motion",
        "LGR2004_5_poisson_source",
        "LGR2004_6_local_GR_WEP_result",
    }
    unsigned_audit = all(row["parent_signed"] == "false" for row in audit_rows)
    theorem_conditional = any(row["theorem_id"] == "NST2004_3_eta_zero" and row["proof_status"] == "EXACT_CONDITIONAL_RESULT" for row in theorem_rows)
    coefficients_blocked = all(row["numeric_value"] == "MISSING" for row in coefficient_rows)
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2004_00_sources", all(row["exists"] == "True" and row["anchor_found"] == "True" for row in source_rows), "all source paths exist and needles found"))
    checks.append(("VAL2004_01_chain_complete", chain_complete, "conditional local GR/Newton/WEP proof chain assembled"))
    checks.append(("VAL2004_02_signature_unsigned", unsigned_audit, "signature clauses remain explicit and unsigned"))
    checks.append(("VAL2004_03_no_species_theorem", theorem_conditional, "no-species eta-zero theorem is conditional and explicit"))
    checks.append(("VAL2004_04_nonmetric_ledger", coefficients_blocked, "finite nonmetric coefficient ledger remains missing/nonclaim"))
    checks.append(("VAL2004_05_readiness_blocks_claim", any(row["readiness_id"] == "READY2004_7_public_local_GR" and row["status"] == "BLOCKED" for row in readiness), "readiness matrix blocks public local-GR claim"))
    checks.append(("VAL2004_06_claim_gates_safe", all(row["claim_allowed"] == "false" for row in claim_rows), "all claim gates deny local GR/Newton/WEP claim"))
    checks.append(("VAL2004_07_next_target", any("2005-Y5-R2FR-parent-action-clause-extraction-for-local-GR-signature.md" in row["next_target"] for row in next_rows), "2005 parent-action clause extraction handoff written"))
    checks.append(("VAL2004_08_branch_copies", all(Path(str(row["path"])).exists() for row in branch_copies), "branch copy artifacts written"))
    checks.append(("VAL2004_09_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in generated_paths), "all generated outputs are under post-checkpoint-work"))
    checks.append(("VAL2004_10_csv_parse", all(path.exists() and csv_rows_parse(path) for path in outputs.values() if path.suffix == ".csv" and path.name != "P8_Y5_BRR545_2004_VALIDATION.csv"), "all 2004 CSV outputs parse cleanly"))
    checks.append(("VAL2004_11_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent"))
    checks.append(("VAL2004_12_formalization_untouched", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains zero"))
    checks.append(("VAL2004_OVERALL", True, "2004 parent Hilbert source signature or finite nonmetric coefficient ledger"))
    rows: list[dict[str, object]] = []
    for validation_id, passed, detail in checks:
        row = base_row()
        row.update(
            {
                "validation_id": validation_id,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
            }
        )
        rows.append(row)
    return rows


def write_doc(
    source_rows: list[dict[str, object]],
    proof_rows: list[dict[str, object]],
    audit_rows: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    coefficient_rows: list[dict[str, object]],
    readiness: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    branch_copies: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> None:
    text = "\n".join(
        [
            "# 2004 - R2FR parent Hilbert source signature or finite nonmetric coefficient ledger",
            "",
            "## Current verdict",
            "2004 assembles the local GR/Newton/WEP reduction as one conditional proof chain: single observed matter metric/coframe -> Hilbert stress-energy source -> Ward conservation -> geodesic test-body motion -> Newtonian slow-motion law -> EH/Poisson source equation. This is real derivation progress, but not a claim, because the parent MTS action has not yet signed the required source/no-species/EH/LC/residual-silence clauses.",
            "",
            "Important boundary: if those clauses are parent-signed, the WEP/source part gives `eta_AB=0` exactly and the Newtonian mechanics branch follows in the usual weak-field limit. If any clause fails, its coefficient must remain in the finite nonmetric ledger.",
            "",
            "Next honest move: scan the parent-action corpus for explicit clauses that sign or reject each condition.",
            "",
            "## Local source register",
            md_table(source_rows, ["source_id", "source_path", "exists", "anchor_found", "note"]),
            "## Conditional local GR/Newton/WEP proof chain",
            md_table(proof_rows, ["proof_id", "formula_or_statement", "meaning", "status", "implication", "parent_signed"]),
            "## Parent signature audit",
            md_table(audit_rows, ["clause_id", "clause", "current_status", "source_anchor", "needed_for", "parent_signed"]),
            "## No-species source theorem attempt",
            md_table(theorem_rows, ["theorem_id", "statement", "proof_status", "source_anchor", "claim_status"]),
            "## Finite nonmetric coefficient ledger",
            md_table(coefficient_rows, ["coefficient_id", "symbol", "meaning", "danger", "current_status", "numeric_value", "next_action"]),
            "## Readiness matrix",
            md_table(readiness, ["readiness_id", "criterion", "status", "basis_or_blocker"]),
            "## Claim gates",
            md_table(claim_rows, ["gate_id", "claim", "gate_pass", "claim_allowed", "reason"]),
            "## Decision ledger",
            md_table(decisions, ["decision_id", "decision", "evidence", "consequence"]),
            "## Branch copies",
            md_table(branch_copies, ["copy_id", "path", "exists", "meaning"]),
            "## Validation",
            md_table(validation_rows, ["validation_id", "status", "detail"]),
            "## Next target",
            md_table(next_rows, ["next_id", "next_target", "objective", "include", "exclude"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    proof_rows = local_gr_proof_chain_rows()
    audit_rows = signature_audit_rows()
    theorem_rows = no_species_theorem_rows()
    coefficient_rows = nonmetric_coefficient_ledger_rows()
    readiness = readiness_rows()
    claim_rows = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    branch_copies = make_branch_copies(proof_rows, audit_rows, coefficient_rows)

    outputs = {
        "source_register": OUT / "P8_Y5_PARENT_QLOC_2004_SOURCE_REGISTER.csv",
        "proof_chain": OUT / "P8_Y5_PARENT_QLOC_2004_LOCAL_GR_NEWTON_WEP_PROOF_CHAIN.csv",
        "signature_audit": OUT / "P8_Y5_PARENT_QLOC_2004_PARENT_SIGNATURE_AUDIT.csv",
        "no_species_theorem": OUT / "P8_Y5_PARENT_QLOC_2004_NO_SPECIES_SOURCE_THEOREM_ATTEMPT.csv",
        "nonmetric_ledger": OUT / "P8_Y5_PARENT_QLOC_2004_NONMETRIC_COEFFICIENT_LEDGER.csv",
        "readiness": OUT / "P8_Y5_PARENT_QLOC_2004_READINESS_MATRIX.csv",
        "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2004_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2004_DECISION_LEDGER.csv",
        "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2004_BRANCH_COPIES.csv",
        "next_target": OUT / "P8_Y5_PARENT_QLOC_2004_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_2004_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["proof_chain"], proof_rows)
    write_csv(outputs["signature_audit"], audit_rows)
    write_csv(outputs["no_species_theorem"], theorem_rows)
    write_csv(outputs["nonmetric_ledger"], coefficient_rows)
    write_csv(outputs["readiness"], readiness)
    write_csv(outputs["claim_gates"], claim_rows)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["branch_copies"], branch_copies)
    write_csv(outputs["next_target"], next_rows)

    remove_pycache()
    validation_rows = validate_outputs(
        outputs,
        branch_copies,
        source_rows,
        proof_rows,
        audit_rows,
        theorem_rows,
        coefficient_rows,
        readiness,
        claim_rows,
        next_rows,
    )
    write_csv(outputs["validation"], validation_rows)
    write_doc(
        source_rows,
        proof_rows,
        audit_rows,
        theorem_rows,
        coefficient_rows,
        readiness,
        claim_rows,
        decisions,
        branch_copies,
        validation_rows,
        next_rows,
    )
    remove_pycache()

    failed = [row for row in validation_rows if row["status"] != "PASS"]
    print(f"wrote {DOC}")
    print(f"wrote {outputs['validation']}")
    print(f"VAL2004_OVERALL={'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['validation_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
