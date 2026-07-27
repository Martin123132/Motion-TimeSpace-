from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2171"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2171-Y5-R2FR-compatibility-object-category-principle-or-finite-local-source-row.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2171_SOURCE_REGISTER.csv",
    "category_audit": OUT / "P8_Y5_PARENT_QLOC_2171_CATEGORY_PRINCIPLE_AUDIT.csv",
    "noether_ledger": OUT / "P8_Y5_PARENT_QLOC_2171_NOETHER_GAUGE_CONDITION_LEDGER.csv",
    "countermodels": OUT / "P8_Y5_PARENT_QLOC_2171_COUNTERMODEL_LEDGER.csv",
    "finite_rows": OUT / "P8_Y5_PARENT_QLOC_2171_FINITE_LOCAL_SOURCE_ROW_CONTRACT.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2171_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2171_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2171_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2171_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2171_FINITE_LOCAL_SOURCE_ROW_CONTRACT_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2171_NOETHER_GAUGE_LEDGER_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "CATEGORY_PRINCIPLE_2171_SOURCE_COUPLING_BLOCKER_NONCLAIM.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def csv_rows_parse(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def formalization_has_2171_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2171-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2171*",
        "*P8_Y5_BRR545_2171*",
        "*Y5_R2FR_compatibility_object_category_principle_or_finite_local_source_row_2171*",
        "*JR2171*",
        "*CATEGORY_PRINCIPLE_2171*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2170_handoff",
            ROOT / "2170-Y5-R2FR-QR-ZR-MR2-source-chain-first-fill-or-no-charge-return.md",
            ["NEXT2170_0_2171", "FR2170_5_theory_route"],
            "2170 selects the category-principle route instead of repeating finite first-fill.",
        ),
        (
            "2170_validation",
            OUT / "P8_Y5_BRR545_2170_VALIDATION.csv",
            ["VAL2170_OVERALL,PASS"],
            "2170 validation passed.",
        ),
        (
            "2168_typed_grammar",
            ROOT / "2168-Y5-R2FR-object-language-radial-cell-constraint-or-finite-ZRJR-intake.md",
            ["MISSING_PARENT_CATEGORY_PRINCIPLE", "TLM2168_0_ZR_kinetic"],
            "2168 names the exact typed-grammar blocker and coframe derivative countermodel.",
        ),
        (
            "1868_grammar_precedent",
            ROOT / "1868-Y5-R2FR-typed-parent-grammar-for-radial-cell-or-coefficient-bound-branch.md",
            ["TYPE_ALONE_TOO_WEAK", "CGT1868_0_hypotheses"],
            "1868 writes the conditional grammar theorem and rejects type-only proof.",
        ),
        (
            "1877_qshape_no_escape",
            ROOT / "1877-Y5-R2FR-qshape-or-lambdaR-parent-origin-source-hunt.md",
            ["QSHAPE_IS_NOT_INDEPENDENT_ESCAPE", "DObs_e"],
            "1877 shows shape-only quotient collapses to readout/category proof.",
        ),
        (
            "1878_dobs_kernel",
            ROOT / "1878-Y5-R2FR-qshape-readout-functor-kernel-or-parent-category-principle.md",
            ["DOBS_E_KERNEL_NOT_DERIVED_CURRENT_CORPUS", "FDOBS1878_0_radial_cell_coframe"],
            "1878 shows radial-cell variation has visible coframe projection unless parent-silenced.",
        ),
        (
            "1879_coframe_ownership",
            ROOT / "1879-Y5-R2FR-parent-coframe-ownership-or-common-frame-leak-bound.md",
            ["PARENT_COFRAME_OWNERSHIP_NOT_DERIVED_CURRENT_CORPUS", "CFL1879_0_bR"],
            "1879 stages common-frame leak rows after coframe ownership fails.",
        ),
        (
            "1885_source_coupling",
            ROOT / "1885-Y5-R2FR-beta-second-order-source-coupling-gate-or-parent-zero-row.md",
            ["NO_SOURCE_ONLY_SLOT_IS_NEXT_BEST_ATTACK", "BETA_NOT_DERIVED_FROM_GAMMA"],
            "1885 identifies source coupling as the live loophole after first-order sharpening.",
        ),
    ]
    rows = []
    for source_id, path, needles, role in specs:
        text = read_text(path)
        found = [needle for needle in needles if needle in text]
        rows.append(
            base_row(
                source_id=source_id,
                source_path=str(path),
                path_exists=path.exists(),
                required_needles=";".join(needles),
                found_needles=";".join(found),
                needles_found=path.exists() and len(found) == len(needles),
                role=role,
            )
        )
    return rows


def category_audit_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "CAT2171_0_identity",
            "target object",
            "C_R=R_AB=ln(T^2 S)=2 ln(J_q)",
            "EXACT_IDENTITY",
            "the reciprocal local object is well-defined, but an identity is not a zero theorem",
            "use as the variable to be removed or bounded",
        ),
        (
            "CAT2171_1_type_only",
            "pure object-language typing",
            "declare C_R compatibility data, not a scalar field",
            "INSUFFICIENT",
            "coframe derivative invariants can still project onto derivatives of ln(J_q)",
            "must add a parent symmetry, quotient invariance, auxiliary constraint, or finite rows",
        ),
        (
            "CAT2171_2_readout_basicity",
            "q-basic readout functor",
            "e_obs=E(Q_vis) with no independent C_R/J_q argument",
            "EXACT_CONDITIONAL",
            "would make D_C_R e_obs=0, but Q_vis/E ownership is not parent-signed",
            "derive the readout functor or keep b_R/d_R finite",
        ),
        (
            "CAT2171_3_vertical_gauge",
            "vertical gauge symmetry",
            "there is a local generator v_R with delta C_R=epsilon(x) and delta Q_vis=0",
            "BEST_PARENT_PRINCIPLE_CANDIDATE",
            "local shift-gauge invariance would forbid C_R potentials, kinetic terms, sources and boundary charge as physical operators",
            "construct generator and Noether identity",
        ),
        (
            "CAT2171_4_noether_identity",
            "Noether/constraint identity",
            "L_{v_R} S_parent is zero or pure admissible boundary and matter/readout descend",
            "MISSING_PARENT_INPUT",
            "without this, Z_R, M_R2, J_R and Q_R remain legal countermodel slots",
            "2172 should attack the actual generator/identity",
        ),
        (
            "CAT2171_5_EH_like_route",
            "unique EH-like local operator",
            "one source-normalized metric action plus Bianchi/common matter would recover the GR exterior structure",
            "CONDITIONAL_BUT_GR_IMPORT_GUARD",
            "this is a useful benchmark but not a derivation unless MTS parent action signs the operator",
            "do not import GR as proof",
        ),
        (
            "CAT2171_6_verdict",
            "compatibility-object category principle",
            "current corpus proves C_R/R_AB is non-dynamical before readout",
            "NOT_DERIVED_CURRENT_CORPUS",
            "the principle has been sharpened into a vertical-gauge/Noether contract, not closed",
            "open 2172 Noether-generator attempt or use finite rows",
        ),
    ]
    return [
        base_row(
            audit_id=audit_id,
            clause=clause,
            statement=statement,
            status=status,
            reason=reason,
            next_action=next_action,
        )
        for audit_id, clause, statement, status, reason, next_action in specs
    ]


def noether_ledger_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "VG2171_0_generator",
            "vertical generator",
            "v_R satisfies delta_v C_R=epsilon(x), delta_v Q_vis=0 and has a defined action on parent primitives T,S,coframe,connection",
            "MISSING_GENERATOR",
            "cannot yet declare C_R pure gauge",
        ),
        (
            "VG2171_1_action_invariance",
            "parent action invariance",
            "delta_v S_parent=0 modulo admitted boundary class",
            "MISSING_PARENT_ACTION_IDENTITY",
            "without invariance, derivative and potential terms are legal dynamics",
        ),
        (
            "VG2171_2_operator_codomain",
            "operator permission rule",
            "allowed local operators have no codomain for D C_R, C_R^2, J_R C_R or source-only C_R prefactors",
            "MISSING_OPERATOR_GRAMMAR_PROOF",
            "this is the formal way to make Z_R, M_R2 and J_R theorem-zero",
        ),
        (
            "VG2171_3_matter_descent",
            "ordinary matter/source descent",
            "S_matter and measured source mass factor through Q_vis and terminal public coframe only",
            "MISSING_NO_SOURCE_ONLY_SLOT",
            "source weights can otherwise be WEP-clean but active-gravity dirty",
        ),
        (
            "VG2171_4_boundary_silence",
            "boundary and symplectic charge",
            "Theta, Q_Noether and admissible corner terms carry no v_R/C_R charge",
            "MISSING_BOUNDARY_NO_CHARGE_THEOREM",
            "Q_R can otherwise reappear as exterior reciprocal hair",
        ),
        (
            "VG2171_5_readout_tau_silence",
            "readout, clocks, tau and endpoints",
            "coframe, clock, source support, tau and endpoint maps are Q_vis-basic",
            "MISSING_READOUT_TAU_DESCENT",
            "b_R, d_R and endpoint leaks remain live",
        ),
        (
            "VG2171_6_result",
            "local-GR reduction from vertical gauge",
            "if VG2171_0 through VG2171_5 close, C_R is gauge/constraint-only and all local reciprocal residual slots vanish before PPN readout",
            "EXACT_CONDITIONAL_NOT_CLOSED",
            "this is a real theorem target, but not a current claim",
        ),
    ]
    return [
        base_row(
            condition_id=condition_id,
            condition=condition,
            required_statement=required_statement,
            status=status,
            implication=implication,
        )
        for condition_id, condition, required_statement, status, implication in specs
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "CM2171_0_coframe_derivative",
            "coframe-local derivative invariant",
            "a legal-looking local invariant reduces to a term proportional to h^ij partial_i C_R partial_j C_R",
            "revives Z_R unless vertical-gauge/operator codomain proof exists",
            "blocks type-only category proof",
        ),
        (
            "CM2171_1_potential",
            "smooth compatibility potential",
            "a term proportional to M_R^2 C_R^2 makes C_R a finite residual rather than a hard constraint",
            "revives lambda_R/range branch",
            "blocks compatibility-label-only proof",
        ),
        (
            "CM2171_2_source_prefactor",
            "source-only matter/action weight",
            "ordinary matter can be universally WEP-clean while carrying active-source dependence w_R(C_R)",
            "revives source coupling and beta/source-normalization residuals",
            "blocks WEP/Ward shortcut",
        ),
        (
            "CM2171_3_common_shadow_frame",
            "common Weyl/disformal readout",
            "e_obs=exp(b_R C_R)e_0 or disformal analog preserves one public frame but shifts PPN/clocks",
            "revives b_R/d_R finite rows",
            "blocks q_shape-only proof",
        ),
        (
            "CM2171_4_boundary_charge",
            "corner/symplectic reciprocal charge",
            "bulk C_R silence can be spoiled by a boundary charge Q_R",
            "revives exterior C_R/r hair",
            "blocks bulk-only proof",
        ),
        (
            "CM2171_5_GR_import",
            "EH exterior imported as closure",
            "beta=gamma=1 and C_R=0 follow in the GR benchmark, but only if the MTS parent action owns the same operator/source package",
            "would be GR-smuggling if used directly",
            "blocks premature local-GR claim",
        ),
    ]
    return [
        base_row(
            countermodel_id=countermodel_id,
            countermodel=countermodel,
            construction=construction,
            live_effect=live_effect,
            blocked_claim=blocked_claim,
        )
        for countermodel_id, countermodel, construction, live_effect, blocked_claim in specs
    ]


def finite_source_rows() -> list[dict[str, Any]]:
    specs = [
        ("FLR2171_0_ZR", "Z_R", "coefficient of h^ij D_i C_R D_j C_R", "R10;PPN;clock;orbital;local_GR", "MISSING_ZERO_THEOREM_OR_PARENT_OPERATOR_COEFFICIENT", "MISSING_NUMERIC_VALUE", "MISSING_UNITS", "MISSING_SOURCE_PATH"),
        ("FLR2171_1_MR2", "M_R^2", "coefficient of C_R^2 or finite range owner", "R10;clock;orbital", "MISSING_ZERO_THEOREM_OR_PARENT_MASS_GAP", "MISSING_NUMERIC_VALUE", "MISSING_UNITS", "MISSING_SOURCE_PATH"),
        ("FLR2171_2_JR", "J_R", "direct source current coefficient multiplying C_R", "R10;PPN;WEP;local_GR", "MISSING_MATTER_DESCENT_ZERO_OR_SOURCE_CURRENT_ROW", "MISSING_NUMERIC_VALUE", "dimensionless_or_declared_source_unit", "MISSING_SOURCE_PATH"),
        ("FLR2171_3_QR", "Q_R/q_R_hat", "boundary/exterior reciprocal charge or normalized hair amplitude", "PPN;orbital;light_time;local_GR", "MISSING_BOUNDARY_NO_CHARGE_THEOREM_OR_QR_ROW", "MISSING_NUMERIC_VALUE", "dimensionless_or_length_by_convention", "MISSING_SOURCE_PATH"),
        ("FLR2171_4_bR", "b_R", "common Weyl/log-coframe derivative with respect to C_R", "PPN;clock;WEP;orbital;local_GR", "MISSING_NO_SHADOW_ZERO_OR_BOUND", "MISSING_NUMERIC_VALUE", "dimensionless", "MISSING_SOURCE_PATH"),
        ("FLR2171_5_dR", "d_R", "common disformal/preferred-frame derivative", "PPN_preferred_frame;clock;orbital;local_GR", "MISSING_DISFORMAL_ZERO_OR_BOUND", "MISSING_NUMERIC_VALUE", "dimensionless_or_declared_scale", "MISSING_SOURCE_PATH"),
        ("FLR2171_6_wR", "w_R", "source-only matter prefactor derivative", "WEP;R10_source_leg;PPN_source_normalization;clock", "MISSING_NO_SOURCE_ONLY_SLOT_OR_BOUND", "MISSING_NUMERIC_VALUE", "dimensionless", "MISSING_SOURCE_PATH"),
        ("FLR2171_7_endpoint_tau", "epsilon_endpoint_tau_R", "boundary endpoint, source support and tau projection leakage", "clock;orbital;PPN;local_GR", "MISSING_BOUNDARY_READOUT_TAU_DESCENT_OR_BOUND", "MISSING_NUMERIC_VALUE", "dimensionless_projection_norm", "MISSING_SOURCE_PATH"),
        ("FLR2171_8_beta_source", "delta_beta_source", "second-order source-normalized beta residual from active coupling", "PPN;local_GR", "MISSING_BETA_SOURCE_COUPLING_ZERO_OR_VECTOR_ROW", "MISSING_NUMERIC_VALUE", "dimensionless", "MISSING_SOURCE_PATH"),
        ("FLR2171_9_total_abs", "epsilon_local_abs", "no-cancellation envelope across active local residual rows", "all_local_arenas", "MISSING_ALL_COMPONENTS", "MISSING_NUMERIC_VALUE", "dimensionless_or_component_declared", "MISSING_SOURCE_PATH"),
    ]
    return [
        base_row(
            row_id=row_id,
            symbol=symbol,
            definition=definition,
            observable_link=observable_link,
            status=status,
            value=value,
            units=units,
            source_path=source_path,
            no_cancellation_policy=True,
            score_ready=False,
        )
        for row_id, symbol, definition, observable_link, status, value, units, source_path in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2171_0_type_not_enough", "TYPE_ONLY_REJECTED", "compatibility labels do not forbid coframe-local derivative countermodels", "selected"),
        ("DEC2171_1_exact_route", "VERTICAL_GAUGE_NOETHER_ROUTE_SELECTED", "a true parent category principle must be a quotient/Noether identity, not a naming convention", "selected"),
        ("DEC2171_2_source_coupling", "SOURCE_COUPLING_REMAINS_LIVE", "the same missing parent owner also controls w_R and beta/source normalization", "selected"),
        ("DEC2171_3_claim_ceiling", "NO_LOCAL_GR_OR_ARENA_CLAIM", "all local arena rows remain nonclaim until theorem-zero or source-backed finite values exist", "selected"),
        ("DEC2171_4_next", "CONSTRUCT_GENERATOR_NEXT", "the next non-circular derivation step is to construct v_R and the Noether identity or explicitly fail it", "selected"),
    ]
    return [
        base_row(
            decision_id=decision_id,
            decision=decision,
            rationale=rationale,
            selection_status=status,
        )
        for decision_id, decision, rationale, status in specs
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2171_0_2172",
            selection_status="selected",
            target_file="2172-Y5-R2FR-radial-cell-vertical-gauge-noether-identity-or-coefficient-basis.md",
            target_script="scripts/Y5_R2FR_radial_cell_vertical_gauge_noether_identity_or_coefficient_basis_2172.py",
            objective="construct the actual parent vertical generator v_R and Noether identity that make C_R/R_AB gauge-or-constraint-only; if it fails, freeze the exact finite coefficient basis for local tests",
            success_condition="v_R, action invariance, matter/readout descent and boundary silence close together, or every residual slot is emitted as finite source-ready nonclaim input",
            do_not_do="do not claim a category principle by type labels, do not import GR, do not use q_shape-only, gamma-only, WEP-only, or R10-bound-only shortcuts",
        ),
        base_row(
            route_id="NEXT2171_1_parallel_source_rows",
            selection_status="held_parallel",
            target_file="2172b-Y5-R2FR-first-source-backed-local-residual-row-acquisition.md",
            target_script="scripts/Y5_R2FR_first_source_backed_local_residual_row_acquisition_2172b.py",
            objective="if the Noether route fails, begin acquiring one real source-backed finite row for Z_R, Q_R, b_R, w_R, or beta_source",
            success_condition="one component row has units, source path, convention and arena projection while still nonclaim",
            do_not_do="do not score symbolic rows or bound anchors as predictions",
        ),
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["finite_rows"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["noether_ledger"], BRANCH_COPIES["branch_wep"]),
        ("source_weight", OUTPUTS["decision"], BRANCH_COPIES["source_weight"]),
    ]
    rows = []
    for copy_id, source, target in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(base_row(copy_id=copy_id, source_path=str(source), target_path=str(target), copied=target.exists()))
    return rows


def all_claim_flags_false(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if str(row.get("claim_allowed", "")).lower() == "true":
                return False
            if str(row.get("valid_for_claim", "")).lower() == "true":
                return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    validations: list[dict[str, Any]] = []
    source_rows = rows_by_name["source_register"]
    validations.append(base_row(validation_id="VAL2171_00_sources_exist", status="PASS" if all(row["path_exists"] for row in source_rows) else "FAIL", detail=f"{sum(bool(row['path_exists']) for row in source_rows)}/{len(source_rows)} sources exist"))
    validations.append(base_row(validation_id="VAL2171_01_needles_found", status="PASS" if all(row["needles_found"] for row in source_rows) else "FAIL", detail=f"{sum(bool(row['needles_found']) for row in source_rows)}/{len(source_rows)} source needle sets found"))

    category_statuses = {row["status"] for row in rows_by_name["category_audit"]}
    validations.append(base_row(validation_id="VAL2171_02_category_audit", status="PASS" if "NOT_DERIVED_CURRENT_CORPUS" in category_statuses and "BEST_PARENT_PRINCIPLE_CANDIDATE" in category_statuses else "FAIL", detail="category proof is sharpened to vertical-gauge/Noether route but not claimed"))

    noether_statuses = {row["status"] for row in rows_by_name["noether_ledger"]}
    validations.append(base_row(validation_id="VAL2171_03_noether_conditions", status="PASS" if "MISSING_GENERATOR" in noether_statuses and "EXACT_CONDITIONAL_NOT_CLOSED" in noether_statuses else "FAIL", detail="generator/action/matter/boundary/readout conditions are explicit"))

    validations.append(base_row(validation_id="VAL2171_04_countermodels", status="PASS" if len(rows_by_name["countermodels"]) >= 6 else "FAIL", detail=f"countermodels={len(rows_by_name['countermodels'])}"))

    finite_rows = rows_by_name["finite_rows"]
    finite_ok = all(str(row.get("status", "")).startswith("MISSING_") and not bool(row.get("score_ready")) for row in finite_rows)
    validations.append(base_row(validation_id="VAL2171_05_finite_rows_nonclaim", status="PASS" if finite_ok else "FAIL", detail=f"finite_rows={len(finite_rows)} remain score_ready=false"))

    decision_text = " ".join(str(row.get("decision", "")) + " " + str(row.get("rationale", "")) for row in rows_by_name["decision"])
    validations.append(base_row(validation_id="VAL2171_06_decision", status="PASS" if "CONSTRUCT_GENERATOR_NEXT" in decision_text else "FAIL", detail="decision selects generator/Noether construction next"))

    validations.append(base_row(validation_id="VAL2171_07_next_target", status="PASS" if any(row["selection_status"] == "selected" and "2172" in row["target_file"] for row in rows_by_name["next_target"]) else "FAIL", detail="2172 radial-cell vertical-gauge route selected"))

    validations.append(base_row(validation_id="VAL2171_08_claim_flags_false", status="PASS" if all_claim_flags_false(rows_by_name) else "FAIL", detail="all generated rows keep valid_for_claim=false and claim_allowed=false"))

    parse_details: list[str] = []
    parse_pass = True
    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        parse_pass = parse_pass and ok
        parse_details.append(f"{path.name}:{count if ok else detail}")
    validations.append(base_row(validation_id="VAL2171_09_csv_parse", status="PASS" if parse_pass else "FAIL", detail="; ".join(parse_details)))

    copy_rows = rows_by_name["branch_copies"]
    validations.append(base_row(validation_id="VAL2171_10_branch_copies", status="PASS" if all(row["copied"] for row in copy_rows) else "FAIL", detail=";".join(str(row["target_path"]) for row in copy_rows)))

    formalization_clean = not formalization_has_2171_artifacts()
    validations.append(base_row(validation_id="VAL2171_11_formalization_clean", status="PASS" if formalization_clean else "FAIL", detail="formalization-workbench has no 2171 artifacts"))

    remove_pycache()
    cache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    validations.append(base_row(validation_id="VAL2171_12_pycache_absent", status="PASS" if cache_absent else "FAIL", detail=str(ROOT / "scripts" / "__pycache__")))

    overall = all(row["status"] == "PASS" for row in validations)
    validations.append(base_row(validation_id="VAL2171_OVERALL", status="PASS" if overall else "FAIL", detail="2171 rejects type-only category proof and promotes vertical-gauge/Noether identity as the exact next derivation target"))
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2171 - Y5/R2FR Compatibility-Object Category Principle Or Finite Local Source Row

## Current Verdict

2171 does **not** prove local GR/Newton, does **not** set `Z_R`, `M_R^2`, `J_R`, `Q_R`, `b_R`, `w_R`, or `delta_beta_source` to zero, and does **not** score any local arena.

It does sharpen the derivation target. Calling `C_R/R_AB` a "compatibility object" is not enough. A compatibility object becomes non-dynamical only if the parent theory supplies a real quotient/vertical-gauge/Noether identity:

`delta_v C_R = epsilon(x)`, `delta_v Q_vis = 0`, and `delta_v S_parent = 0` modulo an admitted boundary class, with matter/readout/boundary maps descending through the same quotient.

That is the clean route. Without it, the countermodels remain legal and the branch must stay as finite residual rows.

## Source Register

{md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"])}

## Category Principle Audit

{md_table(rows_by_name["category_audit"], ["audit_id", "clause", "statement", "status", "reason", "next_action", "valid_for_claim"])}

## Noether Gauge Condition Ledger

{md_table(rows_by_name["noether_ledger"], ["condition_id", "condition", "required_statement", "status", "implication", "valid_for_claim"])}

## Countermodel Ledger

{md_table(rows_by_name["countermodels"], ["countermodel_id", "countermodel", "construction", "live_effect", "blocked_claim", "valid_for_claim"])}

## Finite Local Source Row Contract

{md_table(rows_by_name["finite_rows"], ["row_id", "symbol", "definition", "observable_link", "status", "value", "units", "source_path", "score_ready", "valid_for_claim"])}

## Decision Ledger

{md_table(rows_by_name["decision"], ["decision_id", "decision", "rationale", "selection_status", "valid_for_claim"])}

## Next Target

{md_table(rows_by_name["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do", "valid_for_claim"])}

## Branch Copies

{md_table(rows_by_name["branch_copies"], ["copy_id", "source_path", "target_path", "copied", "valid_for_claim"])}

## Validation

{md_table(rows_by_name["validation"], ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"])}

## Working Interpretation

This is a useful failure, not a dead end. The project has moved from "maybe `C_R` is just compatibility data" to the exact mathematical burden: build the vertical generator and Noether identity, or admit the local branch contains finite residual coefficients.

If the generator closes, the local GR route gets serious because `C_R` becomes gauge/constraint-only rather than tuned small. If it does not close, we still have a disciplined empirical programme: source the finite rows and compare them honestly without gamma-only, WEP-only, or R10-bound-only shortcuts.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)

    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "category_audit": category_audit_rows(),
        "noether_ledger": noether_ledger_rows(),
        "countermodels": countermodel_rows(),
        "finite_rows": finite_source_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name in ["source_register", "category_audit", "noether_ledger", "countermodels", "finite_rows", "decision", "next_target"]:
        write_csv(OUTPUTS[name], rows_by_name[name])

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    remove_pycache()


if __name__ == "__main__":
    main()
