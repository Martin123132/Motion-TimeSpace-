from __future__ import annotations

import csv
from pathlib import Path

from Y5_R2FR_Dq_vX_observed_metric_zero_or_finite_DObs_leak_row_2025 import (
    BRANCH_WEP,
    OUT,
    QUEUE,
    ROOT,
    SOURCE_WEIGHT_DOCS,
    base_row,
    count_formalization_modified,
    csv_rows_parse,
    md_table,
    read_text,
    remove_pycache,
    write_csv,
)


DOC = ROOT / "2042-Y5-R2FR-Levi-Civita-no-hypermomentum-parent-clause-or-P4-connection-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()


def formalization_has_2042_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        artifact_patterns = (
            "*2042-Y5-R2FR*",
            "*P8_Y5_PARENT_QLOC_2042*",
            "*Y5_R2FR_Levi_Civita_no_hypermomentum_parent_clause_or_P4_connection_row_2042*",
        )
        return any(path.is_file() for pattern in artifact_patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def scripts_pycache_exists() -> bool:
    return (SCRIPT_PATH.parent / "__pycache__").exists()


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    try:
        with path.open("r", newline="", encoding="utf-8", errors="replace") as handle:
            return list(csv.DictReader(handle))
    except Exception:
        return []


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2042_00_2041_doc",
            ROOT / "2041-Y5-R2FR-second-order-no-extra-field-parent-clause-or-R11-priority-fill.md",
            ["NEXT2041_0_2042", "LC2041_5_verdict", "VAL2041_OVERALL"],
            "2041 selected the Levi-Civita/no-hypermomentum gate as the next structural attack.",
        ),
        (
            "SRC2042_01_2041_next",
            OUT / "P8_Y5_PARENT_QLOC_2041_NEXT_TARGET.csv",
            ["NEXT2041_0_2042", "no-independent-connection/no-hypermomentum"],
            "machine-readable 2042 target.",
        ),
        (
            "SRC2042_02_2041_connection",
            OUT / "P8_Y5_PARENT_QLOC_2041_TORSION_CONNECTION_DECISION_LEDGER.csv",
            ["LC2041_5_verdict", "SELECTED_NEXT_BLOCKED_GATE"],
            "2041 connection decision ledger.",
        ),
        (
            "SRC2042_03_960_doc",
            ROOT / "960-Y5-R10-R2-fR-scalar-mode-zero-or-bound-and-torsion-Levi-Civita-gate.md",
            ["LC960_4_verdict", "P4REV960_0", "V960_11_validation_rows_ready"],
            "earlier torsion/nonmetricity LC gate and P4 placeholder rejection.",
        ),
        (
            "SRC2042_04_960_lc_csv",
            OUT / "P8_Y5_R10_960_TORSION_LEVI_CIVITA_GATE_ATTEMPT.csv",
            ["LC960_4_verdict", "not_closed_current_corpus"],
            "machine-readable LC/torsion theorem attempt.",
        ),
        (
            "SRC2042_05_960_p4_csv",
            OUT / "P8_Y5_R10_960_P4_CONNECTION_SUBROW_REVIEW.csv",
            ["P4REV960_0", "P4REV960_5", "REJECTED_P4_CONNECTION_PLACEHOLDER"],
            "machine-readable rejected P4 connection subrows.",
        ),
        (
            "SRC2042_06_1960_p4",
            OUT / "P8_Y5_PARENT_QLOC_1960_P4_CONNECTION_ENVELOPE_LEDGER.csv",
            ["P4C1960_0_combined", "P4C1960_5_hypermomentum"],
            "current P4 connection envelope rows.",
        ),
        (
            "SRC2042_07_1045_matter_functor",
            ROOT / "1045-Y5-R10-parent-matter-functor-descent-signature-or-qbar-component-fill.md",
            ["MFS1045_1_observed_coframe_functor", "QG1045_2_connection_stack", "V1045_SUMMARY"],
            "matter functor/coframe descent source with explicit connection caveat.",
        ),
        (
            "SRC2042_08_1065_parent_grammar",
            ROOT / "1065-Y5-R10-no-source-only-slot-parent-grammar-or-first-relative-weight-numeric-row.md",
            ["PGG1065_0_parent_language", "PGG1065_4_measure_coframe_descent", "AAG1065_6_nonHilbert_current"],
            "ordinary matter grammar and non-Hilbert current caveat.",
        ),
        (
            "SRC2042_09_1309_matter_descent",
            ROOT / "1309-Y5-R10-RAB-matter-descent-constant-marker-theorem-or-qc-residual.md",
            ["QZT1309_1_chain_rule", "MCG1309_0_observed_coframe", "VAL1309_6_csv_parse"],
            "matter descent chain-rule theorem and ordinary coframe premise.",
        ),
        (
            "SRC2042_10_1339_left_hand",
            ROOT / "1339-Y5-R10-RAB-source-closure-to-EH-left-hand-local-GR-reduction-gate.md",
            ["EHGate1339_3_Levi_Civita", "R11V1339_1_torsion_nonmetricity", "VAL1339_12_overall"],
            "left-hand local-GR gate map marking Levi-Civita as unresolved.",
        ),
        (
            "SRC2042_11_R11_vector",
            OUT / "R11_nonEH_operator_vector_executable.csv",
            ["torsion_nonmetricity", "MISSING_WEP_CLOCK_LIGHTCONE_SPIN_SOURCE_MAP"],
            "global nonEH vector row for torsion/nonmetricity.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, note in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        ok = exists and all(needle in text for needle in needles)
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "status": "EXISTS_NEEDLES_CONFIRMED" if ok else "MISSING_OR_NEEDLE_FAIL",
                "needles": ";".join(needles),
                "note": note,
            }
        )
        rows.append(row)
    return rows


def no_hypermomentum_theorem_rows() -> list[dict[str, object]]:
    data = [
        (
            "NH2042_0_definition",
            "define observed hypermomentum",
            "Delta_lambda^{mu nu} := -2/sqrt(-g_obs) * delta S_ord / delta Gamma^lambda_{mu nu} for any independent observed connection Gamma.",
            "DEFINITION",
            "turns the coupling problem into an exact variational object",
            "none",
            "conditional_math",
        ),
        (
            "NH2042_1_no_gamma_slot",
            "no independent Gamma slot implies zero hypermomentum",
            "If S_ord = Sbar[Psi_A, e_obs(q), omega_LC(e_obs(q)), A_Q, theta_A] and has no independent Gamma argument, then delta S_ord/delta Gamma = 0.",
            "EXACT_CONDITIONAL_THEOREM",
            "kills hypermomentum without tuning or cancellation",
            "MTS has not parent-signed this object language for all matter/source/readout sectors",
            "parent_signature_required",
        ),
        (
            "NH2042_2_chain_rule",
            "coframe-owned spin connection is not an independent connection",
            "If omega is omega_LC[e_obs], Gamma variation is replaced by metric/coframe variation already counted in Hilbert stress; it does not source independent torsion/nonmetricity.",
            "EXACT_CONDITIONAL_THEOREM",
            "separates ordinary GR spin connection from a new physical Gamma field",
            "spinor and transport sectors still require an explicit coframe-owned connection clause",
            "parent_signature_required",
        ),
        (
            "NH2042_3_spin_guard",
            "spin/torsion guard",
            "If fermions or spin media couple to an independent torsionful connection, Delta != 0 generically and the P4 axial-torsion row must be retained.",
            "COUNTERBRANCH_EXPLICIT",
            "prevents silently using GR spin connection language while allowing torsion matter coupling",
            "no parent proof that ordinary spin sectors only see omega_LC[e_obs]",
            "retain_or_bound",
        ),
        (
            "NH2042_4_source_readout_guard",
            "source, clock, orbital and lightcone readouts must also be Gamma-free",
            "delta S_source/delta Gamma = delta S_clock/delta Gamma = delta S_orbit/delta Gamma = 0, or each residual is mapped into P4 rows.",
            "REQUIRED_GUARD_UNSIGNED",
            "stops an independent connection from reappearing through measurement rather than matter dynamics",
            "source/worldtube/clock/readout Gamma-slot audit is not parent-signed",
            "audit_slots_next",
        ),
        (
            "NH2042_5_verdict",
            "no-hypermomentum parent clause",
            "NH2042_1 + NH2042_2 + NH2042_4 would make Delta_lambda^{mu nu}=0 for ordinary local tests.",
            "CONDITIONAL_THEOREM_PARENT_SIGNATURE_MISSING",
            "this is the clean coupling route, not a numerical patch",
            "current corpus supplies contracts and caveats, not the parent action signature",
            "no_claim",
        ),
    ]
    rows = []
    for row_id, claim_piece, mathematical_statement, derivation_status, would_close, blocker, next_action in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "claim_piece": claim_piece,
                "mathematical_statement": mathematical_statement,
                "derivation_status": derivation_status,
                "would_close": would_close,
                "blocker": blocker,
                "next_action": next_action,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def palatini_lc_rows() -> list[dict[str, object]]:
    data = [
        (
            "PAL2042_0_setup",
            "Palatini-EH independent connection branch",
            "S = (2 kappa)^-1 int sqrt(-g) g^{mu nu} R_mu nu(Gamma) + S_ord[g,Psi] with Delta_lambda^{mu nu}=0.",
            "CONDITIONAL_SETUP",
            "the exact route if an independent Gamma exists but matter/source/readout ignore it",
            "EH-only operator and Delta=0 are not parent-signed",
        ),
        (
            "PAL2042_1_variation",
            "connection equation",
            "Variation of Gamma gives metric compatibility modulo the usual projective ambiguity when hypermomentum is zero.",
            "STANDARD_CONDITIONAL_RESULT",
            "forces nonmetricity/torsion away rather than fitting them small",
            "cannot be applied if non-EH Gamma operators or hypermomentum survive",
        ),
        (
            "PAL2042_2_projective_mode",
            "projective trace silence",
            "Gamma^lambda_{mu nu} -> Gamma^lambda_{mu nu}+delta^lambda_mu xi_nu must be gauge-fixed or unobservable in source/clock/light/spin/readout channels.",
            "REQUIRED_GUARD_UNSIGNED",
            "prevents projective trace becoming a real residual",
            "1960 marks projective trace as missing invariance or bound",
        ),
        (
            "PAL2042_3_lc_result",
            "Levi-Civita result",
            "With EH-only Gamma action, zero hypermomentum, and projective silence, Gamma=LC(g_obs), T=0 and Q=0 in the observed local branch.",
            "EXACT_CONDITIONAL_THEOREM",
            "closes the torsion/nonmetricity operator family if parent-signed",
            "all three premises remain unsigned in MTS corpus",
        ),
        (
            "PAL2042_4_verdict",
            "LC branch status",
            "Palatini theorem is available as a sharp contract, but not yet an MTS derivation.",
            "CONDITIONAL_ONLY_NO_LOCAL_GR_CLAIM",
            "turns the coupling hunt into named signatures",
            "must source/sign EH-only Gamma action, no-hypermomentum and projective silence",
        ),
    ]
    rows = []
    for row_id, theorem_piece, mathematical_statement, status, if_signed, blocker in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "theorem_piece": theorem_piece,
                "mathematical_statement": mathematical_statement,
                "status": status,
                "if_signed": if_signed,
                "blocker": blocker,
                "parent_signed": False if row_id != "PAL2042_1_variation" else "conditional_math_only",
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def gamma_slot_audit_rows() -> list[dict[str, object]]:
    data = [
        (
            "GSA2042_0_gravity_EH",
            "gravitational connection action",
            "Gamma appears only in Palatini-EH or is absent because formalism is metric/coframe LC from the start",
            "UNSIGNED",
            "needed to prevent T^2, Q^2 or non-EH connection kinetic terms",
            "source EH/no-extra-field parent clause",
        ),
        (
            "GSA2042_1_ordinary_matter",
            "ordinary matter action",
            "S_matter depends on e_obs and omega_LC[e_obs], not an independent Gamma",
            "CONDITIONAL_FROM_1045_1309_NOT_PARENT_SIGNED",
            "needed for Delta_matter=0",
            "source parent matter object language",
        ),
        (
            "GSA2042_2_spinor_transport",
            "spinor/spin transport",
            "spin connection is coframe-owned; no independent torsion coupling survives",
            "UNSIGNED_SPIN_GUARD",
            "needed to kill axial torsion P4 row",
            "derive or bound spin/torsion coupling",
        ),
        (
            "GSA2042_3_EM_gauge",
            "EM/gauge sector",
            "visible gauge connection A_Q is independent of affine Gamma and its normalization is fixed by parent lattice/norm",
            "PARTIAL_FROM_PRIOR_ALPHA_OWNER_NOT_CONNECTION_SIGNED",
            "prevents affine connection leakage into EM/clock readouts",
            "link EM owner to no-Gamma affine slot",
        ),
        (
            "GSA2042_4_source_worldtube",
            "source mass/worldtube action",
            "source charge and measured GM do not contain independent Gamma current, boundary torsion, or non-Hilbert support shift",
            "UNSIGNED",
            "needed for Newton source normalization and WEP/source charge",
            "source/worldtube Gamma-slot audit",
        ),
        (
            "GSA2042_5_clock_orbital_readout",
            "clock, lightcone and orbital readout",
            "readout uses g_obs/LC null/timelike structure only, or independent connection terms are bounded",
            "UNSIGNED",
            "needed for clock, Shapiro, orbital and PPN safety",
            "derive readout Gamma silence or retain P4 clock/light rows",
        ),
        (
            "GSA2042_6_boundary_nonHilbert",
            "boundary/non-Hilbert current",
            "no boundary, torsion, nonmetricity or non-Hilbert current contributes to ordinary compact source/current balance",
            "UNSIGNED_PARALLEL_OPEN_GATE",
            "needed for conservation and source coupling",
            "map to zero theorem or P4 residual",
        ),
        (
            "GSA2042_7_verdict",
            "all Gamma slots closed",
            "GSA2042_0 through GSA2042_6 are parent-signed or explicitly bounded",
            "FAIL_CURRENT_CORPUS",
            "would allow Levi-Civita/no-hypermomentum promotion",
            "2043 must hunt the parent slot owner or build P4 bounds",
        ),
    ]
    rows = []
    for row_id, slot, required_signature, status, why_needed, next_action in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "slot": slot,
                "required_signature": required_signature,
                "status": status,
                "why_needed": why_needed,
                "next_action": next_action,
                "parent_signed": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def p4_connection_interface_rows() -> list[dict[str, object]]:
    p4_rows = read_csv_dicts(OUT / "P8_Y5_PARENT_QLOC_1960_P4_CONNECTION_ENVELOPE_LEDGER.csv")
    affected = {
        "P4C1960_0_combined": "WEP;clock;lightcone;source_charge;PPN;local_GR",
        "P4C1960_1_axial_torsion": "spin_transport;clock;WEP;matter_coupling",
        "P4C1960_2_projective_trace": "clock;source_charge;orbital_readout;PPN",
        "P4C1960_3_weyl_nonmetricity": "clock;rod;source_normalization;WEP",
        "P4C1960_4_shear_nonmetricity": "lightcone;clock;WEP;Shapiro",
        "P4C1960_5_hypermomentum": "matter_source_readout;WEP;clock;source_charge",
    }
    requirements = {
        "P4C1960_0_combined": "split into axial/projective/Weyl/shear/hypermomentum or provide combined norm bound",
        "P4C1960_1_axial_torsion": "derive spin connection is LC[e_obs] or provide spin-torsion coupling and bound source",
        "P4C1960_2_projective_trace": "derive projective gauge silence or provide trace-mode readout/bound",
        "P4C1960_3_weyl_nonmetricity": "derive metric compatibility for rods/clocks or provide Weyl-trace clock/source map",
        "P4C1960_4_shear_nonmetricity": "derive lightcone metricity or provide shear/nonmetricity optical map",
        "P4C1960_5_hypermomentum": "derive delta S_ord/delta Gamma=0 or provide hypermomentum coefficient units and weak-field map",
    }
    rows: list[dict[str, object]] = []
    for source in p4_rows:
        row_id = source.get("row_id", "MISSING_P4_ID")
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "channel": source.get("channel", ""),
                "coefficient": source.get("coefficient", ""),
                "definition": source.get("definition", ""),
                "current_status": source.get("status", ""),
                "units": source.get("units", ""),
                "affected_tests": affected.get(row_id, "P4_connection_tests"),
                "first_executable_requirement": requirements.get(row_id, "derive zero or source coefficient/map/bound"),
                "source_path": str(OUT / "P8_Y5_PARENT_QLOC_1960_P4_CONNECTION_ENVELOPE_LEDGER.csv"),
                "ready_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def runner_refusal_rows() -> list[dict[str, object]]:
    data = [
        ("RUN2042_0_no_hypermomentum", "claim Delta_lambda^{mu nu}=0", "REFUSED_PARENT_GAMMA_SLOT_UNSIGNED", "conditional theorem is exact but ordinary matter/source/readout object language is not parent-signed"),
        ("RUN2042_1_palatini_lc", "claim Gamma=LC(g_obs)", "REFUSED_PREMISES_UNSIGNED", "Palatini-EH only, zero hypermomentum and projective silence are not all signed"),
        ("RUN2042_2_axial_torsion", "drop spin/torsion row", "REFUSED_SPIN_GUARD_UNSIGNED", "spinor transport could source axial torsion unless coframe-owned spin connection is proven"),
        ("RUN2042_3_p4_score", "score P4 connection residuals", "NOT_RUN_INPUTS_MISSING", "coefficients, units, weak-field maps and source bounds are missing"),
        ("RUN2042_4_local_GR", "claim derived local GR/Newton", "BLOCKED_NO_CLAIM", "LC/no-hypermomentum is only one unresolved gate among EH, beta, conservation, common matter and GM transfer"),
        ("RUN2042_5_GitHub", "publish or push checkpoint", "NOT_RUN_USER_EXCLUDED", "private work only; no GitHub action requested"),
    ]
    rows = []
    for row_id, branch, runner_status, reason in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "branch": branch,
                "runner_status": runner_status,
                "reason": reason,
                "score_attempted": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("GATE2042_0_no_hypermomentum", "Delta_lambda^{mu nu}=0 for ordinary local branch", "FAIL_BLOCKED", "no independent Gamma slot is not parent-signed"),
        ("GATE2042_1_Levi_Civita", "Gamma=LC(g_obs), T=0, Q=0", "FAIL_BLOCKED", "Palatini-EH only, zero hypermomentum and projective silence are conditional"),
        ("GATE2042_2_P4_rows", "P4 connection residual rows score-ready", "FAIL_BLOCKED", "coefficient values, units, maps and bounds missing"),
        ("GATE2042_3_EH_operator", "EH+Lambda local operator", "FAIL_BLOCKED", "LC gate helps but no-extra-field/EH parent operator remains unsigned"),
        ("GATE2042_4_WEP_clock_light", "WEP/clock/lightcone safety from connection sector", "FAIL_BLOCKED", "connection silence theorem not promoted and P4 rows unfilled"),
        ("GATE2042_5_local_GR", "derived local GR/Newton branch", "FAIL_BLOCKED", "left-hand operator, coupling, beta, conservation and measured-GM gates remain unresolved"),
        ("GATE2042_6_public_claim", "public PPN/R10/WEP/local-GR claim", "FAIL_BLOCKED", "private nonclaim checkpoint only"),
    ]
    rows = []
    for row_id, gate, status, detail in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "gate": gate,
                "status": status,
                "detail": detail,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    data = [
        (
            "DEC2042_0_theorem_result",
            "The no-hypermomentum theorem is derived only as an exact conditional.",
            "If matter/source/readout has no independent Gamma argument, hypermomentum vanishes by variational definition; this is not yet parent-signed for MTS.",
        ),
        (
            "DEC2042_1_lc_result",
            "The Palatini/Levi-Civita route is sharp but conditional.",
            "EH-only independent connection plus zero hypermomentum plus projective silence gives Gamma=LC(g_obs); the current corpus has not signed those premises.",
        ),
        (
            "DEC2042_2_best_next",
            "Next target should hunt the Gamma-slot owner directly.",
            "This is the least-circling route: either find/construct the parent action language that excludes independent Gamma from matter/source/readout, or make the first P4 row executable.",
        ),
        (
            "DEC2042_3_project_status",
            "The coupling suspicion is right.",
            "The live missing piece is not a vague vibe now: it is delta S_ord/delta Gamma, projective silence, and P4 residual maps.",
        ),
    ]
    rows = []
    for row_id, decision, rationale in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "decision": decision,
                "rationale": rationale,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def next_target_rows() -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "target_id": "NEXT2042_0_2043",
            "target_doc": "2043-Y5-R2FR-parent-Gamma-slot-owner-or-first-P4-connection-bound-row.md",
            "objective": "source or construct the parent ordinary-action Gamma-slot owner: prove S_matter, S_source, clocks and orbital readout depend only on e_obs/g_obs and LC[e_obs], not independent Gamma; if this fails, build the first executable P4 connection bound row, prioritizing hypermomentum or axial torsion",
            "must_include": "matter/source/readout action argument audit; spinor/coframe-owned connection guard; projective trace guard; first P4 coefficient units/map/source interface; refusal of local-GR and WEP/clock claims",
            "excluded": "claiming Levi-Civita from Palatini without zero hypermomentum; inventing c_T/c_Q; using GR matter language as an MTS parent proof; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    nh_rows: list[dict[str, object]],
    p4_rows: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2042_0_source_weight_lc_contract",
            SOURCE_WEIGHT_DOCS / "AFRAME_LEVI_CIVITA_NO_HYPERMOMENTUM_2042_NONCLAIM.csv",
            nh_rows,
        ),
        (
            "COPY2042_1_wep_p4_interface",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2042_P4_CONNECTION_INTERFACE_NONCLAIM.csv",
            p4_rows,
        ),
        (
            "COPY2042_2_rab_gamma_slot_next",
            QUEUE / "JR2042_GAMMA_SLOT_OWNER_NEXT_NONCLAIM.csv",
            next_rows_,
        ),
    ]
    rows = []
    for copy_id, path, data in copies:
        write_csv(path, data)
        row = base_row()
        row.update(
            {
                "copy_id": copy_id,
                "path": str(path),
                "rows": len(data),
                "status": "WRITTEN_NONCLAIM_COPY",
            }
        )
        rows.append(row)
    return rows


def validation_rows(
    source_rows: list[dict[str, object]],
    nh_rows: list[dict[str, object]],
    palatini_rows: list[dict[str, object]],
    gamma_rows: list[dict[str, object]],
    p4_rows: list[dict[str, object]],
    runner_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    nh_verdict = next(row for row in nh_rows if row["row_id"] == "NH2042_5_verdict")
    palatini_verdict = next(row for row in palatini_rows if row["row_id"] == "PAL2042_4_verdict")
    gamma_verdict = next(row for row in gamma_rows if row["row_id"] == "GSA2042_7_verdict")
    local_gate = next(row for row in gate_rows if row["row_id"] == "GATE2042_5_local_GR")
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2042_00_sources_exist", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows), "all cited local source paths and needles exist"))
    checks.append(("VAL2042_01_csv_parse", all(csv_rows_parse(path) for path in csv_paths), "all generated CSV files parse cleanly"))
    checks.append(("VAL2042_02_no_hypermomentum_conditional", nh_verdict["derivation_status"] == "CONDITIONAL_THEOREM_PARENT_SIGNATURE_MISSING", "no-hypermomentum theorem is conditional and not promoted"))
    checks.append(("VAL2042_03_palatini_conditional", palatini_verdict["status"] == "CONDITIONAL_ONLY_NO_LOCAL_GR_CLAIM", "Palatini/LC theorem is conditional only"))
    checks.append(("VAL2042_04_gamma_slots_not_closed", gamma_verdict["status"] == "FAIL_CURRENT_CORPUS", "Gamma-slot audit remains unsigned"))
    checks.append(("VAL2042_05_p4_rows_nonclaim", all(not bool(row.get("ready_for_scoring")) for row in p4_rows), "P4 connection rows remain nonclaim and not score-ready"))
    checks.append(("VAL2042_06_runner_blocks", all(str(row["runner_status"]).startswith(("REFUSED", "NOT_RUN", "BLOCKED")) for row in runner_rows), "runner refuses no-hypermomentum, LC, P4-score, local-GR and GitHub shortcuts"))
    checks.append(("VAL2042_07_claim_gates_closed", local_gate["status"] == "FAIL_BLOCKED", "local-GR claim gate remains closed"))
    checks.append(("VAL2042_08_next_selected", next_rows_[0]["target_id"] == "NEXT2042_0_2043", "2043 Gamma-slot owner or first P4 bound row target selected"))
    checks.append(("VAL2042_09_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2042_10_no_formalization_2042_artifacts", not formalization_has_2042_artifacts(), "no 2042 artifacts were written under formalization-workbench"))
    checks.append(("VAL2042_11_no_pycache", not scripts_pycache_exists(), "scripts __pycache__ removed"))
    overall_ok = all(ok for _, ok, _ in checks)
    checks.append(("VAL2042_OVERALL", overall_ok, "2042 derives the LC/no-hypermomentum route as a conditional theorem and selects Gamma-slot owner next"))
    rows = []
    for check_id, ok, detail in checks:
        row = base_row()
        row.update(
            {
                "check_id": check_id,
                "status": "PASS" if ok else "FAIL",
                "detail": detail,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def write_doc(
    source_rows: list[dict[str, object]],
    nh_rows: list[dict[str, object]],
    palatini_rows: list[dict[str, object]],
    gamma_rows: list[dict[str, object]],
    p4_rows: list[dict[str, object]],
    runner_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2042 Y5 R2FR Levi-Civita No-Hypermomentum Parent Clause Or P4 Connection Row",
        "",
        "## Current Verdict",
        "",
        "2042 gets a real theorem on the table: if the ordinary matter/source/readout action has no independent affine `Gamma` argument, then the observed hypermomentum `Delta_lambda^{mu nu}` is zero by variational definition. If the independent-connection action is Palatini-EH only, zero hypermomentum plus projective silence forces `Gamma=LC(g_obs)` and kills torsion/nonmetricity in the local branch.",
        "",
        "That is the clean coupling route. It is not yet an MTS claim, because the parent corpus has not signed the Gamma-slot object language for matter, spin, source, clocks, lightcones, orbital readout and boundary/non-Hilbert currents. So the next target is very specific: source or construct the parent Gamma-slot owner, or make the first P4 connection residual row executable. No local-GR, EH, WEP, clock, orbital, PPN, R10, GitHub, or public claim is made.",
        "",
        "## Source Register",
        md_table(source_rows, ["source_id", "source_path", "status", "note", "valid_for_claim"]),
        "## No-Hypermomentum Theorem Attempt",
        md_table(nh_rows, ["row_id", "claim_piece", "mathematical_statement", "derivation_status", "would_close", "blocker", "next_action", "claim_allowed"]),
        "## Palatini / Levi-Civita Contract",
        md_table(palatini_rows, ["row_id", "theorem_piece", "mathematical_statement", "status", "if_signed", "blocker", "parent_signed", "claim_allowed"]),
        "## Gamma-Slot Audit",
        md_table(gamma_rows, ["row_id", "slot", "required_signature", "status", "why_needed", "next_action", "parent_signed", "claim_allowed"]),
        "## P4 Connection Interface",
        md_table(p4_rows, ["row_id", "channel", "coefficient", "definition", "current_status", "units", "affected_tests", "first_executable_requirement", "ready_for_scoring", "claim_allowed"]),
        "## Runner Refusals",
        md_table(runner_rows, ["row_id", "branch", "runner_status", "reason", "score_attempted", "claim_allowed"]),
        "## Claim Gate",
        md_table(gate_rows, ["row_id", "gate", "status", "detail", "claim_allowed"]),
        "## Decision Ledger",
        md_table(decisions, ["row_id", "decision", "rationale", "claim_allowed"]),
        "## Next Target",
        md_table(next_rows_, ["target_id", "target_doc", "objective", "must_include", "excluded", "claim_allowed"]),
        "## Branch Copies",
        md_table(copies, ["copy_id", "path", "rows", "status", "valid_for_claim"]),
        "## Validation",
        md_table(validation, ["check_id", "status", "detail", "claim_allowed"]),
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    nh_rows = no_hypermomentum_theorem_rows()
    palatini_rows = palatini_lc_rows()
    gamma_rows = gamma_slot_audit_rows()
    p4_rows = p4_connection_interface_rows()
    runner_rows = runner_refusal_rows()
    gate_rows = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2042_SOURCE_REGISTER.csv",
        "nh": OUT / "P8_Y5_PARENT_QLOC_2042_NO_HYPERMOMENTUM_THEOREM_ATTEMPT.csv",
        "palatini": OUT / "P8_Y5_PARENT_QLOC_2042_PALATINI_LEVI_CIVITA_CONTRACT.csv",
        "gamma": OUT / "P8_Y5_PARENT_QLOC_2042_GAMMA_SLOT_AUDIT.csv",
        "p4": OUT / "P8_Y5_PARENT_QLOC_2042_P4_CONNECTION_INTERFACE.csv",
        "runner": OUT / "P8_Y5_PARENT_QLOC_2042_RUNNER_REFUSALS.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2042_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2042_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2042_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2042_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2042_VALIDATION.csv",
    }
    write_csv(paths["sources"], source_rows)
    write_csv(paths["nh"], nh_rows)
    write_csv(paths["palatini"], palatini_rows)
    write_csv(paths["gamma"], gamma_rows)
    write_csv(paths["p4"], p4_rows)
    write_csv(paths["runner"], runner_rows)
    write_csv(paths["gates"], gate_rows)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(nh_rows, p4_rows, next_rows_)
    write_csv(paths["branch"], copies)
    remove_pycache()
    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [Path(row["path"]) for row in copies]
    validation = validation_rows(source_rows, nh_rows, palatini_rows, gamma_rows, p4_rows, runner_rows, gate_rows, next_rows_, csv_paths_without_validation)
    write_csv(paths["validation"], validation)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in copies]
    remove_pycache()
    validation = validation_rows(source_rows, nh_rows, palatini_rows, gamma_rows, p4_rows, runner_rows, gate_rows, next_rows_, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(source_rows, nh_rows, palatini_rows, gamma_rows, p4_rows, runner_rows, gate_rows, decisions, next_rows_, copies, validation)
    remove_pycache()


if __name__ == "__main__":
    main()
