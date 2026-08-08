from __future__ import annotations

import csv
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
DOC = ROOT / "2023-Y5-R2FR-parent-X-normal-form-or-ZX-MX2-first-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row() -> dict[str, object]:
    return {
        "timestamp_utc": stamp(),
        "branch_id": BRANCH_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


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
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_rows_parse(path: Path) -> bool:
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def md_cell(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines) + "\n"


def count_formalization_modified_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    try:
        result = subprocess.run(
            ["git", "-C", str(FORMALIZATION), "status", "--porcelain"],
            check=False,
            capture_output=True,
            text=True,
        )
    except Exception:
        return 0
    if result.returncode != 0:
        return 0
    return len([line for line in result.stdout.splitlines() if line.strip()])


def formalization_has_2023_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        return any(FORMALIZATION.rglob("*2023*X*")) or any(FORMALIZATION.rglob("*2023*ZX*"))
    except Exception:
        return False


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2023_00_2022_handoff",
            ROOT / "2022-Y5-R2FR-Qtau-X-sector-zero-or-first-Ix-source-row.md",
            ["NEXT2022_0_2023", "XZT2022_1_positive_action", "XZT2022_7_verdict"],
            "2022 handoff selects parent X normal form or Z_X/M_X^2 first row.",
        ),
        (
            "SRC2023_01_562_prefactor",
            ROOT / "562-Y5-R10-ZX-lambda-mass-gap-and-bound-curve-fill-or-theorem-zero.md",
            ["PR562_2_canonical_mass_and_range", "PR562_5_positive_operator_identity", "NH562_5_verdict"],
            "Z_X/M_X^2 range law, nohair identity, and current failure verdict.",
        ),
        (
            "SRC2023_02_970_quadratic",
            ROOT / "970-Y5-R10-minimal-quadratic-memory-action-construction-or-strict-residual-runner.md",
            ["QMA970_0_action", "QMA970_5_double_zero_tension", "QMA970_7_verdict"],
            "minimal quadratic X action and double-zero tension.",
        ),
        (
            "SRC2023_03_967_lemma",
            ROOT / "967-Y5-R10-readout-after-variation-parent-schema-theorem-or-memory-positive-operator-lemma.md",
            ["MPO967_1_operator", "MPO967_4_energy_identity", "MPO967_6_verdict"],
            "positive-operator lemma and parent-input caveat.",
        ),
        (
            "SRC2023_04_968_inputs",
            ROOT / "968-Y5-R10-parent-domain-signature-and-memory-operator-input-audit.md",
            ["MOI968_0_X_variable", "MOI968_4_mass_gap", "MOI968_8_verdict"],
            "memory/operator input audit.",
        ),
        (
            "SRC2023_05_1799_ix",
            ROOT / "1799-Y5-R2FR-minimal-parent-current-action-skeleton-or-first-Ix-row.md",
            ["MXA1799_7_verdict", "IXR1799_1_operator_sign", "VAL1799_OVERALL"],
            "R2FR minimal X action skeleton and operator-sign row.",
        ),
        (
            "SRC2023_06_1800_x",
            ROOT / "1800-Y5-R2FR-X-positive-operator-activation-or-Yukawa-fallback-row.md",
            ["XPA1800_1_operator_sign_gap", "YFR1800_0_formula", "VAL1800_OVERALL"],
            "X activation and lambda/alpha fallback.",
        ),
        (
            "SRC2023_07_1785_parent",
            ROOT / "1785-Y5-R2FR-parent-Lagrangian-theta-vX-minimal-fill-or-DqZ-geometry-source-row.md",
            ["PLT1785_0_L_parent", "PLT1785_8_verdict", "VAL1785_OVERALL"],
            "parent Lagrangian/theta/vX route gate.",
        ),
        (
            "SRC2023_08_593_candidates",
            OUT / "P8_Y5_R10_593_MINIMAL_PARENT_FILL_CANDIDATES.csv",
            ["MPF593_B_strict_quotient_zero", "MPF593_D_EH_plus_quotient_extra", "MPF593_C_affine_topological_block"],
            "minimal parent-fill route candidates.",
        ),
        (
            "SRC2023_09_593_extraction",
            OUT / "P8_Y5_R10_593_PJ_EXTRACTION_TEST.csv",
            ["PJE593_1_quotient_zero_extracts_zero", "PJE593_2_affine_block_not_origin", "PJE593_3_hybrid_needs_split"],
            "P/J extraction route test.",
        ),
        (
            "SRC2023_10_562_formula_csv",
            OUT / "P8_Y5_R10_ZX_LAMBDA_PREFACtOR_FORMULA_REGISTER.csv",
            ["PR562_2_canonical_mass_and_range", "PR562_4_prefactor", "PR562_5_positive_operator_identity"],
            "machine-readable Z_X/lambda/prefactor formula register.",
        ),
        (
            "SRC2023_11_970_csv",
            OUT / "P8_Y5_R10_970_QUADRATIC_MEMORY_ACTION_CONSTRUCTION.csv",
            ["QMA970_0_action", "QMA970_5_double_zero_tension", "QMA970_7_verdict"],
            "machine-readable quadratic action construction.",
        ),
        (
            "SRC2023_12_2022_ix_csv",
            OUT / "P8_Y5_PARENT_QLOC_2022_IX_FIRST_SOURCE_ROW_SCHEMA.csv",
            ["IXS2022_0_ZX", "IXS2022_1_MX2", "IXS2022_11_Ix_abs"],
            "machine-readable 2022 I_X source-row schema.",
        ),
    ]
    rows = []
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


def normal_form_route_rows() -> list[dict[str, object]]:
    data = [
        {
            "route_id": "XNF2023_0_route_selector",
            "route": "parent X normal form selector",
            "mathematical_form": "L_parent must choose exactly one local status for X before Q_tau_X/I_X scoring",
            "status": "ROUTE_NOT_SELECTED",
            "best_use": "prevents moving between gauge, active-field, and residual interpretations mid-proof",
            "missing_for_claim": "parent action normal form and field list",
            "route_rank": "gate",
        },
        {
            "route_id": "XNF2023_1_absent_gauge_topological",
            "route": "absent/gauge/topological X",
            "mathematical_form": "X has no physical pole, or Q_tau_X=dB_X fixed/exact, or X is pure gauge/topological with no boundary charge",
            "status": "LEGAL_LOW_SCRUTINY_ROUTE_NOT_SIGNED",
            "best_use": "fastest clean route to I_X=0 if degree count, constraint class, boundary exactness, and matter/readout descent close",
            "missing_for_claim": "no-pole/first-class constraint certificate; boundary exactness; matter/readout blindness",
            "route_rank": "preferred_if_parent_signed",
        },
        {
            "route_id": "XNF2023_2_strict_quotient_zero",
            "route": "strict quotient-zero",
            "mathematical_form": "L_parent=L_red[pi(Y)], Dpi(v_X)=0, matter/readout also factor through pi, so theta_Y(v_X)=0 up to exact terms",
            "status": "PROMISING_DERIVATION_ROUTE_NOT_SIGNED",
            "best_use": "turns X into representative redundancy rather than a fifth-force field",
            "missing_for_claim": "explicit quotient map pi/q; kernel vertical generator; matter/source/readout functor descent",
            "route_rank": "preferred_derivation_route",
        },
        {
            "route_id": "XNF2023_3_EH_plus_quotient_extra",
            "route": "EH plus quotient-extra hybrid",
            "mathematical_form": "L_parent=L_EH[g_obs]+L_extra[g_obs,Phi_red]+L_matter[psi,g_obs], with v_X[g_obs]=0 and representative-sector theta exact",
            "status": "PROMISING_GR_BRIDGE_NOT_SIGNED",
            "best_use": "keeps the local observed metric GR-like while MTS representative variables are vertical/exact",
            "missing_for_claim": "observed/representative split; exact representative theta; fixed boundary; no hidden matter/source marker",
            "route_rank": "preferred_GR_reduction_route",
        },
        {
            "route_id": "XNF2023_4_active_positive_operator",
            "route": "active positive X field",
            "mathematical_form": "L_X=-1/2 Z_X |grad X|^2 -1/2 M_X^2 X^2 + X J_X + dB_X with Z_X>0 and M_X^2>=0 after zero-mode removal",
            "status": "VIABLE_BUT_INPUTS_MISSING",
            "best_use": "activates the energy nohair theorem if J_X=0, boundary_X=0, and Pi_M^H projection vanish",
            "missing_for_claim": "Z_X;M_X^2;zero-mode rule;J_X zero;boundary zero;Pi_M projection",
            "route_rank": "viable_if_coefficients_signed",
        },
        {
            "route_id": "XNF2023_5_double_zero_gate",
            "route": "double-zero observed coupling gate",
            "mathematical_form": "S_mem=int sqrt(-g) f(chi_D)L_X[X] with f(0)=f'(0)=0",
            "status": "TENSION_ACTIVE_NOT_ZERO_PROOF",
            "best_use": "can decouple observed stress/source exchange, but cannot by itself prove X=0",
            "missing_for_claim": "parent origin for f and proof that the kinetic/operator remains active when local coupling is double-zero",
            "route_rank": "auxiliary_only",
        },
        {
            "route_id": "XNF2023_6_sourced_residual",
            "route": "active sourced residual",
            "mathematical_form": "(-Z_X Delta+M_X^2)X=J_X with nonzero source/test/boundary projection and alpha_X(lambda)=K_X Qbar_XH qbar_XT",
            "status": "FINITE_TEST_ROUTE_SCHEMA_ONLY",
            "best_use": "turns failure of nohair into an empirical coefficient row instead of a hidden assumption",
            "missing_for_claim": "Z_X;M_X^2;Qbar_XH;qbar_XT;absolute tails;real bound curve",
            "route_rank": "fallback_empirical_route",
        },
        {
            "route_id": "XNF2023_7_affine_inserted_PJ",
            "route": "affine block with inserted P/J",
            "mathematical_form": "L0+P^{mu nu}(nabla_mu X_nu-A_mu_nu)+X_nu J_eff^nu",
            "status": "REJECT_AS_PARENT_ORIGIN",
            "best_use": "can be a bookkeeping device only after P/J are derived elsewhere",
            "missing_for_claim": "P/J must come from L0, theta0, v_X before the affine block is introduced",
            "route_rank": "rejected_shortcut",
        },
        {
            "route_id": "XNF2023_8_verdict",
            "route": "current parent X normal-form decision",
            "mathematical_form": "choose XNF2023_1/2/3/4/6 by parent action evidence, not by desired local-GR outcome",
            "status": "NORMAL_FORM_NOT_SELECTED",
            "best_use": "keeps the route honest: quotient/hybrid if derivable, active field if coefficients are signed, residual if sourced",
            "missing_for_claim": "one parent branch selecting the status of X with boundary/matter/source signatures",
            "route_rank": "current_verdict",
        },
    ]
    rows = []
    for item in data:
        row = base_row()
        row.update({**item, "parent_signed": False, "selected_for_claim": False})
        rows.append(row)
    return rows


def zx_mx2_rows() -> list[dict[str, object]]:
    data = [
        ("ZMR2023_0_branch", "x_normal_form_branch", "selected X branch: absent/gauge/topological, quotient-zero, EH+quotient-extra, active positive, or sourced residual", "MISSING_PARENT_BRANCH_SELECTION", "category"),
        ("ZMR2023_1_field", "X_field_definition", "field/representative/scalar/tensor variable whose second variation gives the operator", "MISSING_PARENT_X_VARIABLE", "field_definition"),
        ("ZMR2023_2_LX", "L_X", "parent X-sector Lagrangian density before readout", "MISSING_LX_SOURCE", "action_density"),
        ("ZMR2023_3_ZX", "Z_X", "kinetic/gradient residue of the X quadratic operator", "MISSING_ZX_VALUE_OR_SIGN_THEOREM", "action_or_operator_units"),
        ("ZMR2023_4_MX2", "M_X^2", "mass-gap/Hessian residue of the local X operator", "MISSING_MX2_VALUE_OR_SIGN_THEOREM", "operator_mass_units"),
        ("ZMR2023_5_Aij", "A^ij", "spatial/elliptic operator principal symbol or metric-weighted kinetic matrix", "MISSING_AIJ_POSITIVITY_CERTIFICATE", "operator_matrix"),
        ("ZMR2023_6_zero_mode", "zero_mode_rule", "removal or universalization of constant/topological kernel", "MISSING_ZERO_MODE_RULE", "certificate"),
        ("ZMR2023_7_lambda", "lambda_X=sqrt(Z_X/M_X^2)", "finite range after canonicalizing the operator", "MISSING_ZX_OR_MX2", "metres"),
        ("ZMR2023_8_KX", "K_X=s_X/(4*pi*Z_X*G_obs)", "source-normalized Yukawa prefactor if active/sourced", "MISSING_ZX_OR_SOURCE_NORMALIZATION", "dimensionless_prefactor"),
        ("ZMR2023_9_nohair_switch", "X=0 switch", "positive operator plus J_X=0 plus boundary/projection zero", "MISSING_SOURCE_BOUNDARY_PROJECTION_ZERO", "boolean_certificate"),
        ("ZMR2023_10_acceptance", "Z_X/M_X^2 acceptance", "claim-ready only when branch, signs, units, source paths, and zero-mode rule are all real", "REJECT_CURRENT_ROW", "gate"),
    ]
    rows = []
    for row_id, symbol, definition, current_status, units in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "symbol": symbol,
                "definition": definition,
                "required_payload": "value_or_theorem_zero;units;source_path;branch_assumptions;valid_for_claim",
                "current_status": current_status,
                "numeric_value": "MISSING",
                "units": units,
                "score_ready": False,
                "valid_for_claim": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("CG2023_0_route_menu_written", "legal X normal-form route menu is explicit", True, "route options are separated and shortcut insertion is rejected"),
        ("CG2023_1_zx_mx2_schema", "Z_X/M_X^2 first-row schema exists", True, "active route coefficients are named with units/source path requirements"),
        ("CG2023_2_affine_shortcut_rejected", "affine inserted P/J route is rejected as parent origin", True, "prevents deriving P/J by declaration"),
        ("CG2023_3_parent_branch_selected", "one parent X normal form is selected", False, "current corpus has no signed branch selection"),
        ("CG2023_4_quotient_hybrid_signed", "quotient-zero or EH-plus-quotient-extra route is signed", False, "q/pi map and observed/representative split remain missing"),
        ("CG2023_5_active_operator_signed", "active positive operator has Z_X/M_X^2 signs and zero-mode rule", False, "operator coefficients are missing"),
        ("CG2023_6_x_nohair_activated", "X=0/I_X=0 follows", False, "source, boundary, and Pi_M projection gates remain open"),
        ("CG2023_7_alpha_score_ready", "active/sourced alpha_X(lambda) is score-ready", False, "source/test charges, tails, and real bound curve missing"),
        ("CG2023_8_local_GR_Newton", "local GR/Newton reduction follows from X-sector closure", False, "normal form and downstream Q_tau/M_H_ref gates remain open"),
    ]
    rows = []
    for gate_id, gate, passed_for_nonclaim, reason in data:
        row = base_row()
        row.update(
            {
                "gate_id": gate_id,
                "gate": gate,
                "passed_for_nonclaim": passed_for_nonclaim,
                "passed_for_claim": False,
                "reason": reason,
            }
        )
        rows.append(row)
    return rows


def refusal_rows() -> list[dict[str, object]]:
    data = [
        ("REF2023_0_select_by_preference", "choose X route because it helps local GR", "REFUSE", "normal form must be selected by parent action evidence, not by desired conclusion."),
        ("REF2023_1_absent_axiom", "declare X absent/gauge/topological without certificate", "REFUSE", "requires degree count, constraint class, boundary exactness, and matter/readout descent."),
        ("REF2023_2_active_no_coefficients", "use active positive operator without Z_X/M_X^2", "REFUSE", "operator sign/gap and lambda are undefined without parent coefficients."),
        ("REF2023_3_double_zero_as_nohair", "use double-zero observed coupling as X=0 proof", "REFUSE", "double-zero can hide observed coupling but can also degenerate the operator; it is not nohair by itself."),
        ("REF2023_4_affine_PJ_origin", "derive P/J by adding an affine block containing P/J", "REFUSE", "that inserts the target coefficients instead of deriving them from theta and v_X."),
        ("REF2023_5_score_Ix_or_alpha", "score I_X/M_H_ref or alpha_X(lambda)", "REFUSE", "normal form, coefficients, source/test charges, tails, M_H_ref, and bounds are missing."),
        ("REF2023_6_local_GR", "claim local GR/Newton after 2023", "REFUSE", "X normal form is not selected and Q_tau/M_H_ref/Pi_GRH remain nonclaim."),
    ]
    rows = []
    for refusal_id, attempted_claim, verdict, reason in data:
        row = base_row()
        row.update(
            {
                "refusal_id": refusal_id,
                "attempted_claim": attempted_claim,
                "verdict": verdict,
                "reason": reason,
                "accepted_for_claim": False,
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    data = [
        (
            "DEC2023_0_result",
            "X_NORMAL_FORM_NOT_SELECTED",
            "The corpus contains legal contracts for quotient-zero, EH-plus-quotient-extra, active positive, and residual X, but no parent branch signs one of them.",
            "do not activate X=0 or alpha_X; continue at branch-selection level",
        ),
        (
            "DEC2023_1_best_route",
            "EH_PLUS_QUOTIENT_EXTRA_IS_BEST_GR_BRIDGE_IF_SIGNED",
            "It preserves local EH/GR source structure while treating MTS representative motion/time variables as quotient-vertical/exact, which is the lowest-scrutiny path to GR reduction.",
            "try to derive observed/representative split and q/pi map before active-field coefficient hunting",
        ),
        (
            "DEC2023_2_active_route",
            "ACTIVE_OPERATOR_REMAINS_VIABLE_BUT_DEMANDS_ZX_MX2",
            "If X is a real active field, the next facts are Z_X, M_X^2, zero-mode rule, J_X, boundary and Pi_M projection; no nohair without them.",
            "keep Z_X/M_X^2 first-row queue as fallback",
        ),
        (
            "DEC2023_3_next",
            "OBSERVED_REPRESENTATIVE_SPLIT_OR_ACTIVE_COEFFICIENT_ROW_NEXT",
            "The decisive fork is whether X is quotient-vertical/exact relative to observed GR variables, or active with parent coefficients.",
            "build 2024 to prove the observed/representative split, otherwise stage active Z_X/M_X^2 rows",
        ),
    ]
    rows = []
    for decision_id, verdict, rationale, next_action in data:
        row = base_row()
        row.update({"decision_id": decision_id, "verdict": verdict, "rationale": rationale, "next_action": next_action})
        rows.append(row)
    return rows


def next_target_rows() -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "target_id": "NEXT2023_0_2024",
            "next_doc": "2024-Y5-R2FR-observed-representative-split-or-active-ZX-MX2-row.md",
            "objective": "derive an observed/representative split where local g_obs follows EH/GR while X is quotient-vertical/exact; if not, stage the active-field Z_X/M_X^2 coefficient row",
            "required_inputs": "q/pi map; Dq(v_X)=0; g_obs independence; representative theta exactness; boundary class; matter/readout descent; or active L_X,Z_X,M_X^2,zero-mode units/source paths",
            "excluded": "choosing route by preference; declaring X absent by axiom; affine P/J insertion; double-zero as nohair; scoring I_X/alpha_X; local-GR/R10/PPN claim; GitHub; formalization-workbench edits",
        }
    )
    return [row]


def branch_copy_rows(paths: list[Path], notes: list[str]) -> list[dict[str, object]]:
    rows = []
    for idx, (path, note) in enumerate(zip(paths, notes, strict=True)):
        row = base_row()
        row.update({"copy_id": f"COPY2023_{idx}", "path": str(path), "exists": path.exists(), "note": note})
        rows.append(row)
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    routes: list[dict[str, object]],
    zx_rows: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    refusals: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    output_paths: list[Path],
    branch_paths: list[Path],
) -> list[dict[str, object]]:
    root_resolved = ROOT.resolve()
    scoped_paths = output_paths + branch_paths + [DOC]
    route_ids = {row["route_id"] for row in routes}
    required_routes = {
        "XNF2023_1_absent_gauge_topological",
        "XNF2023_2_strict_quotient_zero",
        "XNF2023_3_EH_plus_quotient_extra",
        "XNF2023_4_active_positive_operator",
        "XNF2023_6_sourced_residual",
        "XNF2023_7_affine_inserted_PJ",
        "XNF2023_8_verdict",
    }
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2023_00_sources", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources), "all cited source paths exist and needles are found"))
    checks.append(("VAL2023_01_route_coverage", required_routes.issubset(route_ids), "all relevant X normal-form routes are covered"))
    checks.append(("VAL2023_02_hybrid_preferred", any(row["route_id"] == "XNF2023_3_EH_plus_quotient_extra" and row["route_rank"] == "preferred_GR_reduction_route" for row in routes), "EH-plus-quotient-extra route is ranked as GR bridge"))
    checks.append(("VAL2023_03_affine_rejected", any(row["route_id"] == "XNF2023_7_affine_inserted_PJ" and row["status"] == "REJECT_AS_PARENT_ORIGIN" for row in routes), "affine P/J insertion is rejected"))
    checks.append(("VAL2023_04_normal_form_not_selected", any(row["route_id"] == "XNF2023_8_verdict" and row["status"] == "NORMAL_FORM_NOT_SELECTED" for row in routes), "normal form is not falsely selected"))
    checks.append(("VAL2023_05_zx_rows_nonclaim", all(row["score_ready"] is False and row["valid_for_claim"] is False and row["numeric_value"] == "MISSING" for row in zx_rows), "all Z_X/M_X^2 rows remain missing/nonclaim"))
    checks.append(("VAL2023_06_claim_gates_blocked", all(row["passed_for_claim"] is False for row in claim_gates), "all claim gates remain blocked"))
    checks.append(("VAL2023_07_refusals_active", all(row["verdict"] == "REFUSE" and row["accepted_for_claim"] is False for row in refusals), "refusals remain active"))
    checks.append(("VAL2023_08_double_zero_refused", any(row["refusal_id"] == "REF2023_3_double_zero_as_nohair" for row in refusals), "double-zero-as-nohair shortcut is refused"))
    checks.append(("VAL2023_09_decision_best_route", any(row["decision_id"] == "DEC2023_1_best_route" and "EH_PLUS_QUOTIENT_EXTRA" in row["verdict"] for row in decisions), "decision selects quotient/hybrid as best derivation route"))
    checks.append(("VAL2023_10_next_target", any(row["target_id"] == "NEXT2023_0_2024" and "observed/representative split" in row["objective"] for row in next_target), "2024 observed/representative split target is selected"))
    checks.append(("VAL2023_11_csv_parse", all(path.exists() and csv_rows_parse(path) for path in output_paths), "all generated CSV outputs parse cleanly"))
    checks.append(("VAL2023_12_branch_copies", all(path.exists() and csv_rows_parse(path) for path in branch_paths), "branch-copy CSVs exist and parse"))
    checks.append(("VAL2023_13_no_formalization_edits", count_formalization_modified_since_start() == 0 and not formalization_has_2023_artifacts(), "formalization-workbench modified-file count remains 0 and no 2023 X artifacts appear there"))
    checks.append(("VAL2023_14_output_scope", all(root_resolved == path.resolve() or root_resolved in path.resolve().parents for path in scoped_paths), "all outputs are under post-checkpoint-work"))
    overall = all(passed for _, passed, _ in checks)
    rows = []
    for check_id, passed, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail})
        rows.append(row)
    row = base_row()
    row.update({"check_id": "VAL2023_OVERALL", "status": "PASS" if overall else "FAIL", "detail": "2023 parent X normal form or Z_X M_X^2 first row"})
    rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    routes: list[dict[str, object]],
    zx_rows: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    refusals: list[dict[str, object]],
    decisions: list[dict[str, object]],
    branch_copies: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    parts = [
        "# 2023 Y5 R2FR: Parent X Normal Form Or Z_X M_X^2 First Row\n",
        "Private checkpoint. This pass decides what kind of object `X` is allowed to be before we try to kill it, source it, or use it in `Q_tau` and `M_H_ref`.\n",
        "## Current Verdict\n",
        "The parent normal form is not selected yet. The cleanest GR-reduction route is the EH-plus-quotient-extra/hybrid branch: keep the observed local metric and source charge on the EH/GR side while making the MTS representative `X` direction quotient-vertical or exact. That route is promising because it removes `I_X` without adding a physical pole, but it still needs an explicit `q/pi` map, observed/representative split, boundary exactness, and matter/readout descent.\n",
        "The active positive-operator branch remains viable, but it demands real `Z_X`, `M_X^2`, a zero-mode rule, source silence, boundary zero, and `Pi_M^H` projection before `X=0` can be claimed. The affine block route is rejected as a derivation because it inserts `P/J` instead of deriving them. Double-zero coupling is useful as a decoupling clue, not a nohair proof.\n",
        "So this is not a retreat. It is the fork written cleanly: either prove `X` is quotient/exact relative to observed GR variables, or accept it as active and source `Z_X/M_X^2` before testing.\n",
        "## Source Register\n",
        md_table(sources, ["source_id", "source_path", "status", "needles", "note"]),
        "## X Normal-Form Route Matrix\n",
        md_table(routes, ["route_id", "route", "mathematical_form", "status", "best_use", "missing_for_claim", "route_rank", "parent_signed", "selected_for_claim"]),
        "## Z_X / M_X^2 First Row Schema\n",
        md_table(zx_rows, ["row_id", "symbol", "definition", "required_payload", "current_status", "numeric_value", "units", "score_ready", "valid_for_claim"]),
        "## Claim Gates\n",
        md_table(claim_gates, ["gate_id", "gate", "passed_for_nonclaim", "passed_for_claim", "reason"]),
        "## Refusal Runner\n",
        md_table(refusals, ["refusal_id", "attempted_claim", "verdict", "reason", "accepted_for_claim"]),
        "## Decision Ledger\n",
        md_table(decisions, ["decision_id", "verdict", "rationale", "next_action"]),
        "## Branch Copies\n",
        md_table(branch_copies, ["copy_id", "path", "exists", "note"]),
        "## Next Target\n",
        md_table(next_target, ["target_id", "next_doc", "objective", "required_inputs", "excluded"]),
        "## Validation\n",
        md_table(validation, ["check_id", "status", "detail"]),
    ]
    DOC.write_text("\n".join(parts), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    routes = normal_form_route_rows()
    zx_rows = zx_mx2_rows()
    claim_gates = claim_gate_rows()
    refusals = refusal_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    output_map = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2023_SOURCE_REGISTER.csv",
        "routes": OUT / "P8_Y5_PARENT_QLOC_2023_X_NORMAL_FORM_ROUTE_MATRIX.csv",
        "zx_rows": OUT / "P8_Y5_PARENT_QLOC_2023_ZX_MX2_FIRST_ROW_SCHEMA.csv",
        "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2023_CLAIM_GATE.csv",
        "refusals": OUT / "P8_Y5_PARENT_QLOC_2023_REFUSAL_RUNNER.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2023_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_PARENT_QLOC_2023_NEXT_TARGET.csv",
    }
    write_csv(output_map["sources"], sources)
    write_csv(output_map["routes"], routes)
    write_csv(output_map["zx_rows"], zx_rows)
    write_csv(output_map["claim_gates"], claim_gates)
    write_csv(output_map["refusals"], refusals)
    write_csv(output_map["decisions"], decisions)
    write_csv(output_map["next_target"], next_target)

    branch_paths = [
        SOURCE_WEIGHT_DOCS / "AFRAME_PARENT_X_NORMAL_FORM_2023_NONCLAIM.csv",
        BRANCH_WEP / "P8_Y5_PARENT_QLOC_2023_X_NORMAL_FORM_STATUS_NONCLAIM.csv",
        QUEUE / "JR2023_ZX_MX2_FIRST_ROW_QUEUE.csv",
    ]
    for path in branch_paths:
        path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(output_map["routes"], branch_paths[0])
    shutil.copyfile(output_map["claim_gates"], branch_paths[1])
    shutil.copyfile(output_map["zx_rows"], branch_paths[2])

    branch_copies = branch_copy_rows(
        branch_paths,
        [
            "parent X normal-form route matrix nonclaim copy",
            "X normal-form claim-gate status nonclaim copy",
            "Z_X/M_X^2 first-row acquisition queue",
        ],
    )
    branch_copy_path = OUT / "P8_Y5_PARENT_QLOC_2023_BRANCH_COPIES.csv"
    write_csv(branch_copy_path, branch_copies)

    output_paths = [*output_map.values(), branch_copy_path]
    validation = validation_rows(sources, routes, zx_rows, claim_gates, refusals, decisions, next_target, output_paths, branch_paths)
    validation_path = OUT / "P8_Y5_BRR545_2023_VALIDATION.csv"
    write_csv(validation_path, validation)
    output_paths.append(validation_path)

    write_doc(sources, routes, zx_rows, claim_gates, refusals, decisions, branch_copies, next_target, validation)
    remove_pycache()

    overall = [row for row in validation if row["check_id"] == "VAL2023_OVERALL"][0]["status"]
    print(f"VAL2023_OVERALL={overall}")
    print(str(DOC))
    for path in output_paths:
        print(str(path))
    for path in branch_paths:
        print(str(path))


if __name__ == "__main__":
    main()
