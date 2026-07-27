from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_VERTICAL_KERNEL_AND_VISIBLE_TARGET_CATEGORY_OWNER_OR_FIRST_COEFFICIENT_BOUND_ROW_2433"
CHECKPOINT_ID = "2433"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2433-Y5-R2FR-vertical-kernel-and-visible-target-category-owner-or-first-coefficient-bound-row.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2433_SOURCE_REGISTER.csv",
    "combined_theorem": OUT / "P8_Y5_PARENT_QLOC_2433_KERNEL_TARGET_COMBINED_THEOREM.csv",
    "owner_gates": OUT / "P8_Y5_PARENT_QLOC_2433_KERNEL_TARGET_OWNER_GATES.csv",
    "countermodels": OUT / "P8_Y5_PARENT_QLOC_2433_SURVIVING_COUNTERMODELS.csv",
    "jq_effect": OUT / "P8_Y5_PARENT_QLOC_2433_JQ_EFFECT_LEDGER.csv",
    "first_bound_row": OUT / "P8_Y5_PARENT_QLOC_2433_FIRST_COEFFICIENT_BOUND_ROW_CONTRACT.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2433_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_PARENT_QLOC_2433_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2433_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2433_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2433_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_theorem": QUEUE / "JR2433_KERNEL_TARGET_COMBINED_THEOREM_NONCLAIM.csv",
    "queue_bound": QUEUE / "JR2433_FIRST_COEFFICIENT_BOUND_ROW_CONTRACT_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "kernel_target_countermodels_nonclaim_2433.csv",
    "beta_docs": BETA_DOCS / "KERNEL_TARGET_JQ_EFFECT_2433_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2433_00_2432_handoff",
        "source_path": ROOT / "2432-Y5-R2FR-parent-observed-coefficient-functor-or-first-Jq-bound-row.md",
        "needles": ["NEXT2432_0_selected", "OCF2432_5_verdict", "VAL2432_OVERALL"],
        "role": "fresh handoff selecting vertical-kernel plus visible target-category owner",
    },
    {
        "source_id": "SRC2433_01_2432_validation",
        "source_path": OUT / "P8_Y5_BRR545_2432_VALIDATION.csv",
        "needles": ["VAL2432_OVERALL", "PASS"],
        "role": "confirms 2432 passed before 2433",
    },
    {
        "source_id": "SRC2433_02_2432_functor",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2432_OBSERVED_COEFFICIENT_FUNCTOR_ATTEMPT.csv",
        "needles": ["OCF2432_1_chain_rule", "PARENT_OBSERVED_COEFFICIENT_FUNCTOR_NOT_CONSTRUCTED"],
        "role": "observed coefficient functor contract",
    },
    {
        "source_id": "SRC2433_03_2432_target",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2432_VISIBLE_COEFFICIENT_TARGET_CATEGORY.csv",
        "needles": ["TGT2432_6_verdict", "TARGET_CATEGORY_NOT_PARENT_OWNED"],
        "role": "visible coefficient target category status",
    },
    {
        "source_id": "SRC2433_04_2392_kernel",
        "source_path": ROOT / "2392-Y5-R2FR-vertical-kernel-presymplectic-null-and-matter-invisible-or-kernel-charge-row.md",
        "needles": ["VKN2392_5_verdict", "VKC2392_2_theta_Qv", "VKL2392_1_kernel_charge"],
        "role": "vertical kernel null/matter-invisible precedent",
    },
    {
        "source_id": "SRC2433_05_2391_obs",
        "source_path": ROOT / "2391-Y5-R2FR-parent-q-Obs-e-functor-construction-or-frame-leak-source-pack.md",
        "needles": ["QOF2391_6_verdict", "QOC2391_6_matter_readout_descent"],
        "role": "q/Obs_e descent and no projection-by-declaration guard",
    },
    {
        "source_id": "SRC2433_06_1219_counterexamples",
        "source_path": ROOT / "1219-Y5-R10-typed-visible-coefficient-functor-or-hidden-scalar-counterexample-lock.md",
        "needles": ["HSC1219_0_generic_scalar", "HSC1219_4_source_weight", "VAL1219_16_overall"],
        "role": "typed visible coefficient and hidden scalar/source-weight counterexample lock",
    },
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def stringify(value: Any) -> str:
    if isinstance(value, bool):
        return "True" if value else "False"
    return str(value)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


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
        for row in rows:
            writer.writerow({key: stringify(row.get(key, "")) for key in fields})


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def table(headers: list[str], rows: list[dict[str, Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        cells = [stringify(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        needles = source["needles"]
        found = [needle for needle in needles if needle in text]
        rows.append(
            base_row(
                source_id=source["source_id"],
                source_path=path,
                path_exists=path.exists(),
                required_needles="; ".join(needles),
                found_needles="; ".join(found),
                needles_found=path.exists() and len(found) == len(needles),
                role=source["role"],
            )
        )
    return rows


def combined_theorem_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            theorem_id="KTT2433_0_target",
            theorem_piece="combined kernel-target theorem",
            statement="If V=ker(Dq) is a regular parent vertical distribution, V is presymplectic-null and matter-invisible, and visible coefficients factor through Obs_coeff with DObs_coeff[V]=0, then Lie_v c_A=0 for all visible coefficients.",
            status="EXACT_CONDITIONAL_THEOREM",
            missing_for_claim="V basis, rank/involutivity, Theta/Q_v, matter invisibility, target category and readout closure",
            theorem_zero=False,
        ),
        base_row(
            theorem_id="KTT2433_1_no_projection_declaration",
            theorem_piece="anti-tautology guard",
            statement="Declaring q or Obs_coeff to include the desired observed data is not enough; the kernel must be independently null, matter-invisible and coefficient-basic.",
            status="GUARD_RETAINED",
            missing_for_claim="independent kernel-null certificate",
            theorem_zero=False,
        ),
        base_row(
            theorem_id="KTT2433_2_target_exclusion",
            theorem_piece="no hidden-visible target theorem",
            statement="Visible coefficient targets must exclude hidden scalars, q representative labels, source-only weights, post-variation readout markers and material labels unless fixed by representation/topology.",
            status="REQUIRED_TYPE_RULE_NOT_PARENT_SIGNED",
            missing_for_claim="parent typed object-language/action-domain signature",
            theorem_zero=False,
        ),
        base_row(
            theorem_id="KTT2433_3_Jq_consequence",
            theorem_piece="J_q source consequence",
            statement="If KTT2433_0 through KTT2433_2 close, J_q^frame, J_q^marker, much of J_q^source_norm and readout coefficient drift vanish by chain rule.",
            status="CONDITIONAL_CONSEQUENCE_READY",
            missing_for_claim="body/worldtube, boundary, memory and source-normalization still need separate closure",
            theorem_zero=False,
        ),
        base_row(
            theorem_id="KTT2433_4_verdict",
            theorem_piece="promotion verdict",
            statement="The theorem route is exact but not activated. Current MTS has not supplied the parent vertical basis, kernel charge silence, matter invisibility, visible target category or readout closure needed for claim-grade J_q=0.",
            status="THEOREM_NOT_PROMOTED",
            missing_for_claim="owner gates below remain open",
            theorem_zero=False,
        ),
    ]


def owner_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("KGO2433_0_vertical_basis", "parent vertical basis v_i", "list retained v_i as parent variations and prove v_i in ker(Dq) and ker(DObs_coeff)", "MISSING_PARENT_VERTICAL_BASIS", "epsilon_q_rank_or_integrability"),
        ("KGO2433_1_regular_integrable", "regular quotient distribution", "rank(Dq) constant and [v_i,v_j] in V with sourced bracket table", "MISSING_RANK_BRACKET_AUDIT", "epsilon_q_rank_or_integrability"),
        ("KGO2433_2_presymplectic_null", "kernel Hamiltonian silence", "derive Theta_parent and Q_v, then show compact local flux integral_S(delta Q_v-i_v Theta_parent+improvements)=0", "MISSING_THETA_QV_ZERO_FLUX", "epsilon_kernel_charge"),
        ("KGO2433_3_matter_invisible", "matter/readout invisibility", "delta_v S_matter=0 and no direct source/material/worldtube slot for every v_i", "MISSING_MATTER_DESCENT_NO_DIRECT_SLOT", "epsilon_matter_kernel"),
        ("KGO2433_4_visible_target_category", "visible coefficient target category", "exclude hidden scalar, q representative, source-only prefactor and readout-tail targets by parent syntax", "MISSING_TYPED_TARGET_CATEGORY", "B_marker_q;B_source_norm_q"),
        ("KGO2433_5_readout_effective_closure", "readout/effective-action closure", "renormalized coefficients, detector thresholds, clocks, rods and source maps preserve the same target category", "MISSING_READOUT_EFT_CLOSURE", "B_projector_q;B_memory_q"),
        ("KGO2433_6_same_branch_lock", "same branch lock", "V, Obs_coeff, source normalization, boundary class and q operator use one parent branch", "MISSING_SAME_BRANCH_OWNER", "B_total_q"),
        ("KGO2433_7_verdict", "claim-grade owner package", "KGO2433_0 through KGO2433_6 pass together", "FAIL_CURRENT_CLAIM_KERNEL_TARGET_OWNER_MISSING", "finite coefficient rows remain live"),
    ]
    return [
        base_row(gate_id=gate_id, needed=needed, test=test, current_status=status, fallback_symbol=fallback, gate_pass=False)
        for gate_id, needed, test, status, fallback in rows
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        base_row(countermodel_id="CM2433_0_hidden_scalar_coefficient", countermodel="c_alpha=c0+epsilon I_hid with dI_hid(v_q)!=0", blocked_by="typed target category plus hidden invariant triviality/quotient-constant theorem", current_status="ACTIVE_COUNTERMODEL"),
        base_row(countermodel_id="CM2433_1_source_prefactor", countermodel="active source weight w_A=w0(1+epsilon s_A q) changes source leg without equal test-leg descent", blocked_by="source-label forgetting/common calibration owner", current_status="ACTIVE_COUNTERMODEL"),
        base_row(countermodel_id="CM2433_2_shadow_frame", countermodel="e_obs=exp(b_g q)e_basic gives public frame but not quotient-basic if b_g or q survives", blocked_by="basic coframe Lie_v e_parent=0 or finite b_g bound", current_status="ACTIVE_COUNTERMODEL"),
        base_row(countermodel_id="CM2433_3_readout_reentry", countermodel="clock/detector/source-worldtube readout depends on q after variation", blocked_by="readout functor naturality and variation-before-readout theorem", current_status="ACTIVE_COUNTERMODEL"),
        base_row(countermodel_id="CM2433_4_kernel_charge", countermodel="v_q has nonzero compact Hamiltonian charge or boundary/history flux", blocked_by="Theta/Q_v extraction and zero-flux certificate", current_status="ACTIVE_COUNTERMODEL"),
        base_row(countermodel_id="CM2433_5_verdict", countermodel="at least one legal countermodel survives", blocked_by="full owner package or finite source-backed bound rows", current_status="COUNTERMODELS_RETAINED"),
    ]


def jq_effect_rows() -> list[dict[str, Any]]:
    rows = [
        ("JQE2433_0_frame", "J_q^frame", "closed if V is basic for Obs_e/Obs_coeff and shadow-frame targets are forbidden", "OPEN", "B_frame_q"),
        ("JQE2433_1_marker", "J_q^marker", "closed if EM/mass/material coefficients are typed q-blind and readout/EFT preserves the type rule", "OPEN", "B_marker_q"),
        ("JQE2433_2_source_norm", "J_q^source_norm", "closed if source weights use common calibration only and measured-GM projector is q-orthogonal", "OPEN", "B_source_norm_q"),
        ("JQE2433_3_projector_readout", "J_q^projector", "closed if readout/projector/domain maps are fixed before variation or are functorial in q-blind observables", "OPEN", "B_projector_q"),
        ("JQE2433_4_body_boundary", "J_q^body+J_q^boundary", "not closed by coefficient functor alone; needs source-worldtube and B_q/Q_q boundary theorem", "SEPARATE_ROUTE_REQUIRED", "B_body_q+B_boundary_q"),
        ("JQE2433_5_total", "J_q^abs", "zero only if every component closes in same branch; otherwise use absolute finite bound vector", "TOTAL_ZERO_NOT_PROVED", "B_total_q"),
    ]
    return [
        base_row(effect_id=effect_id, jq_component=component, closure_effect=effect, current_status=status, fallback_bound_symbol=fallback, theorem_zero=False, score_ready=False)
        for effect_id, component, effect, status, fallback in rows
    ]


def first_bound_row_contract() -> list[dict[str, Any]]:
    return [
        base_row(row_id="FCR2433_0_preferred_first", coefficient="b_alpha or b_g", reason="these directly test hidden-visible coefficient drift or shadow-frame leakage and touch clocks/WEP/R10/EM", required_fields="symbol;sector;definition;units;q normalization;bound type;numeric value or theorem-zero;uncertainty;source path;arena projection;no-cancellation group", source_backed=False, score_ready=False),
        base_row(row_id="FCR2433_1_validity_rule", coefficient="all first finite rows", reason="a row may score only if either theorem_zero=true from parent proof or numeric value/uncertainty/source/projection are real", required_fields="valid_for_claim=false until source-backed; no MISSING_* markers; no fitted cancellation", source_backed=False, score_ready=False),
        base_row(row_id="FCR2433_2_product_rule", coefficient="R10/fifth-force source-test legs", reason="finite exchange uses beta_s beta_t and common frame appears as c_g^2 unless source leg is explicitly in Qbar", required_fields="source leg; test leg; K(lambda); lambda support; tail_abs; bound curve", source_backed=False, score_ready=False),
        base_row(row_id="FCR2433_3_verdict", coefficient="first coefficient bound row", reason="not filled at 2433 because no source-backed coefficient value is available in this checkpoint", required_fields="next step must either prove target-category owner or source one real coefficient row", source_backed=False, score_ready=False),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(claim_id="CGATE2433_0_kernel_owner", claim="q-vertical kernel is parent-null/matter-invisible", gate_pass=False, reason="vertical basis, rank, Theta/Q_v, zero flux, matter descent and boundary/history silence are missing"),
        base_row(claim_id="CGATE2433_1_target_category", claim="visible target category excludes hidden-visible Hom", gate_pass=False, reason="typed object-language/action-domain signature and readout/EFT closure are not parent-owned"),
        base_row(claim_id="CGATE2433_2_DObs_zero", claim="DObs_coeff(v_q)=0 for all retained verticals", gate_pass=False, reason="kernel basicness for observed coefficients is conditional only"),
        base_row(claim_id="CGATE2433_3_Jq_zero", claim="J_q=0 follows", gate_pass=False, reason="several J_q channels remain open or separate-route"),
        base_row(claim_id="CGATE2433_4_first_bound_score", claim="first finite coefficient row can score", gate_pass=False, reason="contract exists but no source-backed value/theorem-zero row is filled"),
        base_row(claim_id="CGATE2433_5_local_GR", claim="local GR/Newton reduction follows", gate_pass=False, reason="q no-hair activation and J_q/boundary/source normalization gates remain blocked"),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(decision_id="DEC2433_0_theorem_route", decision="KEEP_KERNEL_TARGET_THEOREM_AS_PRIMARY_ROUTE", rationale="it is the cleanest path to killing multiple J_q channels by structure", consequence="attack parent typed object-language and vertical basis next"),
        base_row(decision_id="DEC2433_1_no_promotion", decision="DO_NOT_PROMOTE_KERNEL_OR_TARGET_OWNER", rationale="active countermodels remain and owner gates are missing", consequence="J_q component vector remains live"),
        base_row(decision_id="DEC2433_2_first_bound", decision="PREPARE_FIRST_COEFFICIENT_BOUND_FALLBACK", rationale="if theorem route fails, b_alpha/b_g style rows are the most useful empirical handles", consequence="bound contract written but nonclaim"),
        base_row(decision_id="DEC2433_3_no_github", decision="NO_GITHUB_ACTION", rationale="private derivation/fallback gate only", consequence="continue private goal work"),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2433_0_selected",
            selection_status="selected",
            target_file="2434-Y5-R2FR-parent-typed-object-language-and-vertical-basis-certificate-or-balpha-bg-bound-row.md",
            target_script="scripts/Y5_R2FR_parent_typed_object_language_and_vertical_basis_certificate_or_balpha_bg_bound_row_2434.py",
            task="try to prove the parent typed object-language/action-domain signature and retained q-vertical basis make DObs_coeff(v_q)=0 while excluding hidden scalar/source-prefactor/readout targets; if not, fill a first nonclaim b_alpha or b_g coefficient-bound row",
            acceptance_target="typed target-category plus vertical-basis certificate, or source-backed finite coefficient-row contract with valid_for_claim=false",
            guardrails="do not use projection-by-declaration, invent coefficient values, cancel J_q components, claim local GR/R10/PPN/WEP/clock/orbital pass, edit formalization-workbench, or push GitHub",
        )
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue_theorem", OUTPUTS["combined_theorem"], COPY_TARGETS["queue_theorem"], "kernel-target combined theorem nonclaim queue"),
        ("queue_bound", OUTPUTS["first_bound_row"], COPY_TARGETS["queue_bound"], "first coefficient bound-row contract nonclaim queue"),
        ("branch_wep", OUTPUTS["countermodels"], COPY_TARGETS["branch_wep"], "surviving countermodels for WEP/local residual branch"),
        ("beta_docs", OUTPUTS["jq_effect"], COPY_TARGETS["beta_docs"], "J_q effect map for beta-source docs"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target, note in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(base_row(copy_id=copy_id, source_path=source, target_path=target, source_exists=source.exists(), target_exists=target.exists(), notes=note))
    return rows


def validation_rows(all_outputs: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    source_rows = all_outputs["source_register"]
    output_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    formalization_hits: list[Path] = []
    for pattern in ["*2433-Y5-R2FR*", "*P8_Y5_PARENT_QLOC_2433*", "*P8_Y5_BRR545_2433*", "*JR2433*", "*KERNEL_TARGET_JQ_EFFECT_2433*"]:
        formalization_hits.extend(FORMALIZATION.rglob(pattern) if FORMALIZATION.exists() else [])

    checks = [
        ("VAL2433_00_sources_exist", all(row["path_exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL2433_01_source_needles", all(row["needles_found"] for row in source_rows), "all cited source needles are present"),
        ("VAL2433_02_combined_theorem", any(row["theorem_id"] == "KTT2433_0_target" and row["status"] == "EXACT_CONDITIONAL_THEOREM" for row in all_outputs["combined_theorem"]), "combined kernel-target theorem written"),
        ("VAL2433_03_antitautology_guard", any(row["theorem_id"] == "KTT2433_1_no_projection_declaration" for row in all_outputs["combined_theorem"]), "projection-by-declaration guard retained"),
        ("VAL2433_04_owner_blocked", any(row["gate_id"] == "KGO2433_7_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM_KERNEL_TARGET_OWNER_MISSING" for row in all_outputs["owner_gates"]), "owner package remains blocked"),
        ("VAL2433_05_countermodels_retained", any(row["countermodel_id"] == "CM2433_5_verdict" and row["current_status"] == "COUNTERMODELS_RETAINED" for row in all_outputs["countermodels"]), "countermodels retained"),
        ("VAL2433_06_Jq_total_open", any(row["effect_id"] == "JQE2433_5_total" and row["current_status"] == "TOTAL_ZERO_NOT_PROVED" for row in all_outputs["jq_effect"]), "J_q total remains open"),
        ("VAL2433_07_bound_contract_nonclaim", all(not row["source_backed"] and not row["score_ready"] for row in all_outputs["first_bound_row"]), "first coefficient row contract remains nonclaim"),
        ("VAL2433_08_claims_blocked", all(not row["gate_pass"] for row in all_outputs["claim_gates"]), "all claim gates remain false"),
        ("VAL2433_09_next_target_written", any(row["route_id"] == "NEXT2433_0_selected" for row in all_outputs["next_target"]), "next target selected"),
        ("VAL2433_10_branch_copies", all(row["target_exists"] for row in all_outputs["branch_copies"]), "branch copies were written"),
        ("VAL2433_11_no_formalization_artifacts", len(formalization_hits) == 0, "no 2433 artifacts were written to formalization-workbench"),
    ]
    for check_id, passed, notes in checks:
        rows.append(base_row(check_id=check_id, status="PASS" if passed else "FAIL", notes=notes, detail="" if passed else "required checkpoint condition failed"))
    for path in output_csvs:
        parses, row_count, message = csv_parses(path)
        rows.append(base_row(check_id=f"VAL2433_CSV_{path.stem}", status="PASS" if parses and row_count > 0 else "FAIL", notes=f"CSV parses with {row_count} rows", detail=message))
    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        base_row(
            check_id="VAL2433_OVERALL",
            status="PASS" if overall else "FAIL",
            notes="2433 writes the combined vertical-kernel plus visible-target-category theorem, retains anti-tautology and countermodel guards, blocks J_q/local-GR promotion, and selects typed object-language plus vertical-basis certificate or first b_alpha/b_g bound row next",
            detail="",
        )
    )
    return rows


def write_markdown(all_outputs: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2433 - Y5/R2FR Vertical Kernel And Visible Target Category Owner Or First Coefficient Bound Row",
        "",
        "## Result",
        "- 2433 combines the two exact routes now on the table: vertical-kernel nullness and visible coefficient target typing.",
        "- The conditional theorem is clean: if `V=ker(Dq)` is a real parent-null, matter-invisible kernel and visible coefficients are functorial in q-blind observed objects, then `DObs_coeff(v_q)=0` and visible coefficient slopes vanish.",
        "- The theorem is not activated. The vertical basis, rank/bracket audit, `Theta/Q_v`, zero compact flux, matter invisibility, target category, no-Hom rule and readout closure are still unsigned.",
        "- Surviving countermodels are retained explicitly; no `J_q=0`, local GR/Newton, R10, PPN, WEP, clock, orbital or public claim is created.",
        "",
        "## Practical Status",
        "This is the right kind of grim: no magic closure, but the exact lock is now small enough to attack. Either the parent grammar and vertical basis close, or we stop trying to theorem-zero the coupling and source the first real coefficient row.",
        "",
        "## Source Register",
        table(["source_id", "source_path", "path_exists", "needles_found", "role"], all_outputs["source_register"]),
        "",
        "## Kernel Target Combined Theorem",
        table(["theorem_id", "theorem_piece", "statement", "status", "missing_for_claim", "theorem_zero", "valid_for_claim"], all_outputs["combined_theorem"]),
        "",
        "## Kernel Target Owner Gates",
        table(["gate_id", "needed", "test", "current_status", "fallback_symbol", "gate_pass", "valid_for_claim"], all_outputs["owner_gates"]),
        "",
        "## Surviving Countermodels",
        table(["countermodel_id", "countermodel", "blocked_by", "current_status", "valid_for_claim"], all_outputs["countermodels"]),
        "",
        "## J_q Effect Ledger",
        table(["effect_id", "jq_component", "closure_effect", "current_status", "fallback_bound_symbol", "valid_for_claim"], all_outputs["jq_effect"]),
        "",
        "## First Coefficient Bound Row Contract",
        table(["row_id", "coefficient", "reason", "required_fields", "source_backed", "score_ready", "valid_for_claim"], all_outputs["first_bound_row"]),
        "",
        "## Claim Gates",
        table(["claim_id", "claim", "gate_pass", "reason", "valid_for_claim"], all_outputs["claim_gates"]),
        "",
        "## Decisions",
        table(["decision_id", "decision", "rationale", "consequence", "valid_for_claim"], all_outputs["decisions"]),
        "",
        "## Next Target",
        table(["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"], all_outputs["next_target"]),
        "",
        "## Branch Copies",
        table(["copy_id", "source_path", "target_path", "source_exists", "target_exists", "notes"], all_outputs["branch_copies"]),
        "",
        "## Validation",
        table(["check_id", "status", "notes", "detail"], all_outputs["validation"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    for path in (OUT, QUEUE, MICROSCOPE, BETA_DOCS):
        path.mkdir(parents=True, exist_ok=True)

    all_outputs: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "combined_theorem": combined_theorem_rows(),
        "owner_gates": owner_gate_rows(),
        "countermodels": countermodel_rows(),
        "jq_effect": jq_effect_rows(),
        "first_bound_row": first_bound_row_contract(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next_target": next_target_rows(),
    }

    for key, rows in all_outputs.items():
        write_csv(OUTPUTS[key], rows)

    all_outputs["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], all_outputs["branch_copies"])
    all_outputs["validation"] = validation_rows(all_outputs)
    write_csv(OUTPUTS["validation"], all_outputs["validation"])
    write_markdown(all_outputs)

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    print(DOC)
    print(OUTPUTS["validation"])
    print(f"VAL2433_OVERALL={all_outputs['validation'][-1]['status']}")


if __name__ == "__main__":
    main()
