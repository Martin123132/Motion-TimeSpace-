from __future__ import annotations

import csv
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "974-Y5-R10-zero-origin-evenness-theorem-or-boundary-flux-coefficient-fill.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _field in fields) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join([header, separator, *body])


def source_path(relative_path: str) -> Path:
    return ROOT / relative_path


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return -1
    since = SCRIPT_START_UTC.timestamp()
    count = 0
    try:
        for directory, _subdirs, filenames in os.walk(FORMALIZATION):
            for filename in filenames:
                path = Path(directory) / filename
                try:
                    if path.stat().st_mtime > since:
                        count += 1
                except OSError:
                    return -2
    except OSError:
        return -2
    return count


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "973_doc",
            "path": "973-Y5-R10-source-free-SXkin-and-boundary-zero-proof-or-first-memory-residual-source-row.md",
            "role": "handoff selecting zero-origin/evenness or boundary coefficient fill",
            "needle": "974-Y5-R10-zero-origin-evenness-theorem-or-boundary-flux-coefficient-fill.md",
        },
        {
            "source_id": "973_source_free",
            "path": "source-intake/mts_residuals/P8_Y5_R10_973_SOURCE_FREE_SXKIN_LEMMA.csv",
            "role": "relative source-free S_Xkin lemma and parent-unsigned status",
            "needle": "SFL973_6_verdict",
        },
        {
            "source_id": "973_first_residual",
            "path": "source-intake/mts_residuals/P8_Y5_R10_973_FIRST_RESIDUAL_SOURCE_ROWS.csv",
            "role": "first alpha3/Gdot residual anchors",
            "needle": "FRS973_0_boundary_alpha3_flux",
        },
        {
            "source_id": "608_doc",
            "path": "608-Y5-R10-double-zero-exponent-origin-or-source-neutrality-proof.md",
            "role": "norm-square p>=2 theorem attempt and marker counterexample",
            "needle": "NS608_5_normsquare_verdict",
        },
        {
            "source_id": "608_counterexamples",
            "path": "source-intake/mts_residuals/P8_Y5_R10_608_COUNTEREXAMPLE_GATE.csv",
            "role": "linear marker covector counterexample",
            "needle": "CE608_0_linear_marker_covector",
        },
        {
            "source_id": "609_doc",
            "path": "609-Y5-R10-parent-own-norm-square-activation-or-finite-p1-branch.md",
            "role": "parent ownership failure and finite p=1 branch retention",
            "needle": "NL609_4_no_linear_verdict",
        },
        {
            "source_id": "609_no_linear_gate",
            "path": "source-intake/mts_residuals/P8_Y5_R10_609_NO_LINEAR_MARKER_SYMMETRY_GATE.csv",
            "role": "no-linear-marker symmetry gate",
            "needle": "NL609_4_no_linear_verdict",
        },
        {
            "source_id": "802_doc",
            "path": "802-Y5-R10-parent-ZL-evenness-and-gradient-signature-gate.md",
            "role": "scalar evenness repair and parent-signature failure",
            "needle": "D802_0_ZL_parent_signature",
        },
        {
            "source_id": "802_evenness_gate",
            "path": "source-intake/mts_residuals/P8_Y5_R10_802_SCALAR_EVENNESS_GATE.csv",
            "role": "smooth quadratic scalar closure pass but not parent-signed",
            "needle": "EV802_1_smooth_quadratic_scalar",
        },
        {
            "source_id": "417_boundary",
            "path": "417-boundary-exchange-nohair-theorem-attempt.md",
            "role": "boundary exchange/no-hair blockers and pressure anchors",
            "needle": "alpha3_flux",
        },
        {
            "source_id": "507_acceptance",
            "path": "source-intake/mts_residuals/P8_FIELD_SPECIFIC_SILENCE_ACCEPTANCE_GATES.csv",
            "role": "theorem-zero versus numeric-bound acceptance policy",
            "needle": "G507_0_theorem_zero",
        },
        {
            "source_id": "495_even_scalar",
            "path": "source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_EVEN_SCALAR_GATE.csv",
            "role": "even observed scalar cannot be killed by parity alone",
            "needle": "ES518_2_physical_lock",
        },
    ]
    rows = []
    for spec in specs:
        absolute_path = source_path(spec["path"])
        exists = absolute_path.exists()
        needle_found = spec["needle"] in read_text(absolute_path) if exists else False
        rows.append(
            {
                **spec,
                "absolute_path": str(absolute_path),
                "exists": flag(exists),
                "needle_found": flag(needle_found),
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def zero_origin_evenness_attempt() -> list[dict[str, str]]:
    specs = [
        {
            "attempt_id": "ZOE974_0_parent_amplitude",
            "claim_piece": "X is a primitive parent amplitude",
            "mathematical_form": "X in E_X with local trivial branch X=0 and parent fibre metric h_X",
            "status": "NEEDED_NOT_PARENT_SIGNED",
            "gap": "current corpus does not yet own X as the primitive signed amplitude rather than a derived/proxy residual",
        },
        {
            "attempt_id": "ZOE974_1_smooth_taylor",
            "claim_piece": "smooth parent scalar expansion",
            "mathematical_form": "F(X)=F(0)+F_1(X)+1/2 H_X(X,X)+O(||X||^3)",
            "status": "MATHEMATICAL_SETUP_VALID",
            "gap": "smoothness alone does not kill F_1",
        },
        {
            "attempt_id": "ZOE974_2_evenness_kills_linear",
            "claim_piece": "evenness or O(E_X) invariance removes F_1",
            "mathematical_form": "F(RX)=F(X) for R in O(E_X), or F(-X)=F(X), implies F_1=0",
            "status": "RELATIVE_THEOREM_DERIVED",
            "gap": "the symmetry/no-marker clause is not signed by the parent action",
        },
        {
            "attempt_id": "ZOE974_3_zero_origin_stationary",
            "claim_piece": "X=0 is stationary",
            "mathematical_form": "dF|_0=0; if F(0)=0 and L_X is positive/elliptic, local source-free branch has X=0",
            "status": "RELATIVE_THEOREM_DERIVED",
            "gap": "requires no affine shifted origin X0(q), no boundary source, and no history tail",
        },
        {
            "attempt_id": "ZOE974_4_source_free_kinetic_current",
            "claim_piece": "kinetic current has no local source",
            "mathematical_form": "S_X^kin=1/2<X,L_X X> gives delta_X S=<delta X,L_X X>+boundary and J_X^kin(0)=0",
            "status": "RELATIVE_THEOREM_DERIVED",
            "gap": "only closes after ZOE974_0 through ZOE974_3 plus boundary silence",
        },
        {
            "attempt_id": "ZOE974_5_even_scalar_warning",
            "claim_piece": "parity is not enough for observed even scalars",
            "mathematical_form": "even measured quantities such as GM/source-normalization offsets can survive X->-X",
            "status": "WARNING_RETAINED",
            "gap": "do not use evenness to erase physical source-normalization residuals",
        },
        {
            "attempt_id": "ZOE974_6_verdict",
            "claim_piece": "zero-origin/evenness theorem for local memory",
            "mathematical_form": "if X is primitive, centered, smooth, marker-free, and even/O(E_X)-invariant, then F_1=0 and X=0 is a stationary local branch",
            "status": "RELATIVE_THEOREM_DERIVED_PARENT_UNSIGNED",
            "gap": "no local-GR claim; parent origin, symmetry, marker exclusion, and boundary silence remain unsigned",
        },
    ]
    return [
        {
            **spec,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for spec in specs
    ]


def marker_counterexample_audit() -> list[dict[str, str]]:
    specs = [
        {
            "counterexample_id": "MCE974_0_linear_marker_covector",
            "construction": "F_1(X)=ell(X) with ell in E_X*",
            "why_still_legal": "unless parent O(E_X)/Z2/no-marker symmetry is proved, a material/domain/readout covector is allowed",
            "damage": "J_X(0)=ell != 0; p=1 branch returns",
            "needed_repair": "derive no parent covector/marker theorem",
        },
        {
            "counterexample_id": "MCE974_1_shifted_origin",
            "construction": "S_X=1/2<X-X0(q),L_X(X-X0(q))>",
            "why_still_legal": "zero-origin has not been parent-signed as X0(q)=0",
            "damage": "X=0 is not the stationary point and hidden source terms appear",
            "needed_repair": "prove centered origin, not fitted calibration origin",
        },
        {
            "counterexample_id": "MCE974_2_material_domain_marker",
            "construction": "ell_m(X) built from material species, domain class, or local readout marker",
            "why_still_legal": "609 keeps material/domain marker exclusion failed in the current corpus",
            "damage": "source-free local memory branch becomes matter/environment dependent",
            "needed_repair": "derive quotient-invariant marker exclusion for matter/domain labels",
        },
        {
            "counterexample_id": "MCE974_3_boundary_flux_source",
            "construction": "boundary lift or memory exchange flux enters the local X equation",
            "why_still_legal": "417/973 do not parent-derive boundary primitive silence, Bianchi cancellation, or projected flux zero",
            "damage": "X may be sourced even if bulk F_1=0",
            "needed_repair": "prove boundary no-hair/no-flux or source coefficient rows",
        },
        {
            "counterexample_id": "MCE974_4_even_observed_scalar",
            "construction": "parity-even source-normalization or observed GM offset",
            "why_still_legal": "495 shows observed even scalars are not killed by exchange/doublet parity",
            "damage": "wrongly claiming parity zero would smuggle local Newton/GR reduction",
            "needed_repair": "separate auxiliary odd variables from physical even source residuals",
        },
        {
            "counterexample_id": "MCE974_5_verdict",
            "construction": "all marker/source alternatives",
            "why_still_legal": "the no-linear-marker theorem is not yet parent-derived",
            "damage": "zero-origin theorem remains relative and cannot promote local-GR compatibility",
            "needed_repair": "make 975 a no-linear-marker theorem or boundary-flux coefficient acquisition",
        },
    ]
    return [
        {
            **spec,
            "counterexample_retained": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for spec in specs
    ]


def parent_origin_acceptance_gate() -> list[dict[str, str]]:
    specs = [
        {
            "gate_id": "POA974_0_primitive_X",
            "required_clause": "X is the parent-owned primitive local memory amplitude",
            "current_evidence": "608/609 identify the clause but do not parent-own it",
            "gate_pass": "false",
            "missing_input": "MISSING_PARENT_PRIMITIVE_X",
        },
        {
            "gate_id": "POA974_1_fibre_metric",
            "required_clause": "parent supplies h_X and norm-square ||X||^2 as the only scalar activation",
            "current_evidence": "norm-square route is the clean theorem target",
            "gate_pass": "false",
            "missing_input": "MISSING_PARENT_FIBRE_METRIC_AND_NORMSQUARE_ONLY",
        },
        {
            "gate_id": "POA974_2_even_symmetry",
            "required_clause": "parent action is X->-X or O(E_X)-invariant",
            "current_evidence": "802 gives smooth quadratic closure; 608 gives conditional theorem",
            "gate_pass": "false",
            "missing_input": "MISSING_PARENT_Z2_OR_OEX_SYMMETRY",
        },
        {
            "gate_id": "POA974_3_no_linear_marker",
            "required_clause": "no parent covector/source/domain/readout marker ell(X)",
            "current_evidence": "609 NL609_4 keeps this as closure/new parent clause required",
            "gate_pass": "false",
            "missing_input": "MISSING_NO_LINEAR_MARKER_THEOREM",
        },
        {
            "gate_id": "POA974_4_no_shifted_origin",
            "required_clause": "no affine X0(q) or calibration origin hidden in the kinetic sector",
            "current_evidence": "973 lists shifted-origin counterexample",
            "gate_pass": "false",
            "missing_input": "MISSING_NO_AFFINE_X0_PROOF",
        },
        {
            "gate_id": "POA974_5_boundary_silence",
            "required_clause": "boundary/local projection contributes zero source",
            "current_evidence": "417/973 boundary zero not derived",
            "gate_pass": "false",
            "missing_input": "MISSING_BOUNDARY_FLUX_ZERO_OR_COEFFICIENT",
        },
        {
            "gate_id": "POA974_6_matter_blindness",
            "required_clause": "ordinary matter and clocks depend only on q(Phi)/observed coframe and not X",
            "current_evidence": "943/945 conditional descent remains unsigned in the 973 handoff",
            "gate_pass": "false",
            "missing_input": "MISSING_MATTER_MARKER_EXCLUSION",
        },
        {
            "gate_id": "POA974_7_verdict",
            "required_clause": "all parent-origin/evenness gates close",
            "current_evidence": "relative theorem exists, but parent acceptance fails",
            "gate_pass": "false",
            "missing_input": "MISSING_PARENT_ZERO_ORIGIN_CONTRACT",
        },
    ]
    return [
        {
            **spec,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for spec in specs
    ]


def boundary_flux_coefficient_rows() -> list[dict[str, str]]:
    specs = [
        {
            "coefficient_id": "BFC974_0_alpha3_boundary_flux",
            "arena": "PPN/preferred-frame",
            "residual_channel": "projected boundary/memory exchange flux",
            "coefficient_symbol": "K_boundary_alpha3",
            "bound_or_anchor_value": "4.000e-20",
            "units": "dimensionless alpha3-scale lock",
            "source_path": "417-boundary-exchange-nohair-theorem-attempt.md",
            "source_needle": "alpha3_flux",
            "extraction_method": "source-backed local pressure anchor inherited from 417/973; no MTS coefficient extracted",
            "missing_parent_input": "MISSING_BOUNDARY_FLUX_PROJECTION_COEFFICIENT;MISSING_JX_BOUNDARY_NORM;MISSING_UNITS_NORMALIZATION;MISSING_LOCAL_PROJECTION_MAP",
            "row_status": "SOURCE_BACKED_BOUND_ANCHOR_NOT_SCOREABLE",
        },
        {
            "coefficient_id": "BFC974_1_Gdot_boundary_drift",
            "arena": "Gdot/time drift",
            "residual_channel": "secular boundary/domain/memory exchange drift",
            "coefficient_symbol": "K_boundary_Gdot",
            "bound_or_anchor_value": "9.600e-15",
            "units": "yr^-1",
            "source_path": "417-boundary-exchange-nohair-theorem-attempt.md",
            "source_needle": "Gdot",
            "extraction_method": "source-backed drift pressure anchor inherited from 417/973; no MTS coefficient extracted",
            "missing_parent_input": "MISSING_SECULAR_DRIFT_PROJECTION;MISSING_HISTORY_TAIL_NORM;MISSING_TIME_UNITS_NORMALIZATION",
            "row_status": "SOURCE_BACKED_BOUND_ANCHOR_NOT_SCOREABLE",
        },
        {
            "coefficient_id": "BFC974_2_gamma_scalar_hair",
            "arena": "PPN/R10",
            "residual_channel": "scalar/radial boundary hair beyond source-normalized monopole",
            "coefficient_symbol": "K_boundary_gamma_hair",
            "bound_or_anchor_value": "2.300e-05",
            "units": "dimensionless gamma-scale lock",
            "source_path": "417-boundary-exchange-nohair-theorem-attempt.md",
            "source_needle": "gamma-scale lock",
            "extraction_method": "source-backed PPN pressure anchor inherited from 973 first residual rows; no alpha(lambda) curve or MTS coefficient extracted",
            "missing_parent_input": "MISSING_SCALAR_HAIR_ALPHA_LAMBDA;MISSING_K_R10_K_PPN;MISSING_WEAK_FIELD_MAP",
            "row_status": "SOURCE_BACKED_BOUND_ANCHOR_NOT_SCOREABLE",
        },
    ]
    return [
        {
            **spec,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for spec in specs
    ]


def claim_gates() -> list[dict[str, str]]:
    specs = [
        {
            "gate_id": "CGATE974_0_zero_origin_evenness",
            "claim": "X=0 is parent-derived as the even centered origin",
            "current_evidence": "relative theorem derived, parent origin/symmetry/no-marker clauses unsigned",
            "gate_pass": "false",
        },
        {
            "gate_id": "CGATE974_1_no_linear_marker",
            "claim": "all linear marker covectors are excluded",
            "current_evidence": "linear covector, shifted origin, material/domain/readout markers remain legal counterexamples",
            "gate_pass": "false",
        },
        {
            "gate_id": "CGATE974_2_boundary_flux_zero",
            "claim": "boundary flux/lift vanishes by theorem",
            "current_evidence": "417/973 boundary zero route remains parent-unsigned",
            "gate_pass": "false",
        },
        {
            "gate_id": "CGATE974_3_boundary_flux_bound_score",
            "claim": "boundary flux coefficients pass alpha3/Gdot/PPN locks",
            "current_evidence": "bound anchors are sourced but MTS projection coefficients are missing",
            "gate_pass": "false",
        },
        {
            "gate_id": "CGATE974_4_local_GR",
            "claim": "local GR/Newton reduction follows from this branch",
            "current_evidence": "zero theorem and numeric residual pass are both absent",
            "gate_pass": "false",
        },
    ]
    return [
        {
            **spec,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for spec in specs
    ]


def decisions() -> list[dict[str, str]]:
    specs = [
        {
            "decision_id": "DEC974_0_evenness_theorem",
            "topic": "zero-origin/evenness route",
            "result": "relative_theorem_derived_parent_unsigned",
            "reason": "smooth even/O(E_X)-invariant parent scalars kill F_1, but current corpus does not yet sign X as primitive centered marker-free amplitude",
            "next_action": "try to prove the no-linear-marker/origin contract directly",
        },
        {
            "decision_id": "DEC974_1_counterexamples",
            "topic": "p=1 and shifted-source branches",
            "result": "retained_as_legal_without_parent_marker_exclusion",
            "reason": "linear covector, material/domain marker, shifted X0(q), and boundary flux counterexamples still fit the unsigned parent skeleton",
            "next_action": "either kill them by theorem or keep finite residual rows",
        },
        {
            "decision_id": "DEC974_2_boundary_coefficients",
            "topic": "first boundary flux coefficient fill",
            "result": "source_backed_bound_anchors_written_nonclaim",
            "reason": "417/973 provide alpha3/Gdot/gamma pressure anchors, but MTS projection coefficients and norms are missing",
            "next_action": "source K_boundary_alpha3 or derive boundary no-flux",
        },
        {
            "decision_id": "DEC974_3_best_next",
            "topic": "next checkpoint",
            "result": "no_linear_marker_theorem_or_boundary_flux_source_acquisition",
            "reason": "the clean proof now hinges on excluding ell(X); if that fails, the first executable coefficient must be acquired",
            "next_action": "make 975 prove no parent marker covector or acquire the alpha3 boundary-flux coefficient row",
        },
    ]
    return [
        {
            **spec,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for spec in specs
    ]


def next_target() -> list[dict[str, str]]:
    return [
        {
            "next_target": "975-Y5-R10-no-linear-marker-covector-proof-or-boundary-flux-source-acquisition.md",
            "objective": "prove that no parent covector/material/domain/readout marker can create F_1=ell(X), or acquire a real boundary-flux projection coefficient for the alpha3 row",
            "include": "parent quotient/orbit argument, O(E_X) or Z2 ownership, shifted-origin exclusion, material/domain marker audit, K_boundary_alpha3 source path and units",
            "exclude": "local-GR claim, invented coefficients, parity-only erasure of even source normalization, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validation(
    sources: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    counterexample_rows: list[dict[str, str]],
    origin_gate_rows: list[dict[str, str]],
    boundary_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    formalization_count = formalization_changed_after_start()
    rows = [
        {
            "check_id": "V974_0_source_paths_exist",
            "result": "pass" if all(row["exists"] == "true" for row in sources) else "fail",
            "detail": "all cited local source paths exist",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V974_1_source_needles_found",
            "result": "pass" if all(row["needle_found"] == "true" for row in sources) else "fail",
            "detail": "all source needles found",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V974_2_relative_theorem_written",
            "result": "pass"
            if any(row["attempt_id"] == "ZOE974_6_verdict" and row["status"] == "RELATIVE_THEOREM_DERIVED_PARENT_UNSIGNED" for row in theorem_rows)
            else "fail",
            "detail": "zero-origin/evenness theorem is written only as a relative theorem",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V974_3_marker_counterexamples_retained",
            "result": "pass"
            if any(row["counterexample_id"] == "MCE974_5_verdict" and row["counterexample_retained"] == "true" for row in counterexample_rows)
            else "fail",
            "detail": "linear marker and shifted-origin counterexamples remain retained",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V974_4_parent_acceptance_fails",
            "result": "pass" if all(row["gate_pass"] == "false" and row["valid_for_claim"] == "false" for row in origin_gate_rows) else "fail",
            "detail": "parent origin/evenness acceptance gates stay false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V974_5_boundary_rows_nonclaim",
            "result": "pass"
            if all(row["valid_for_claim"] == "false" and "MISSING_" in row["missing_parent_input"] for row in boundary_rows)
            else "fail",
            "detail": "boundary coefficient rows are source-backed anchors but non-scoreable",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V974_6_claim_gates_false",
            "result": "pass" if all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claim_rows) else "fail",
            "detail": "all local-memory/local-GR claim gates remain false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V974_7_decisions_nonclaim",
            "result": "pass" if all(row["claim_allowed"] == "false" for row in decision_rows) else "fail",
            "detail": "decision ledger remains nonclaim",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V974_8_next_target_written",
            "result": "pass" if len(target_rows) == 1 and target_rows[0]["valid_for_claim"] == "false" else "fail",
            "detail": "975 no-linear-marker or boundary-flux acquisition target selected",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V974_9_formalization_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization-workbench modified-file count since script start is {formalization_count}",
            "generated_utc": stamp(),
        },
    ]
    rows.append(
        {
            "check_id": "V974_READY",
            "result": "pass" if all(row["result"] == "pass" for row in rows) else "fail",
            "detail": "974 checkpoint pack validation summary",
            "generated_utc": stamp(),
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    counterexample_rows: list[dict[str, str]],
    origin_gate_rows: list[dict[str, str]],
    boundary_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    doc = f"""# 974 Y5 R10: Zero-Origin Evenness Theorem Or Boundary Flux Coefficient Fill

Status: `Y5_R10_974_zero_origin_evenness_relative_theorem_parent_unsigned_boundary_flux_coefficients_nonclaim`

Claim ceiling: no parent zero-origin theorem, no no-linear-marker theorem, no boundary no-flux theorem, no scoreable boundary coefficient, no R10/R11/PPN pass, and no EH/Newton/local-GR claim is made.

## Readout

974 gets the clean theorem shape, but not the parent claim.

The relative theorem is:

If `X` is a primitive parent amplitude in a fibre `E_X`, the parent scalar sector is smooth at `X=0`, and the action/readout is invariant under `X -> -X` or `O(E_X)`, then the linear Taylor piece is forbidden:

`F(X)=F(0)+1/2 H_X(X,X)+O(||X||^4)`.

Therefore `F_1=0`, `dF|_0=0`, and a centered homogeneous kinetic sector gives `J_X^kin(0)=0` up to boundary terms.

That is the right route. It is not yet enough. The current parent skeleton still allows a linear marker covector `ell(X)`, a shifted origin `X0(q)`, a material/domain/readout marker, or a boundary flux source. Those are not cheap objections; they are exactly the routes that would stop local GR from dropping out cleanly.

So the honest status is: the math skeleton is good, but the parent signature is missing. Because the zero proof does not close, 974 also writes the first boundary-flux coefficient rows as source-backed, non-scoreable pressure anchors. The next fight is now very narrow: prove no parent marker covector can exist, or acquire the actual boundary-flux projection coefficient.

## Source Register

{md_table(sources, ["source_id", "role", "exists", "needle_found", "path"])}

## Zero-Origin Evenness Attempt

{md_table(theorem_rows, ["attempt_id", "claim_piece", "status", "gap"])}

## Marker Counterexample Audit

{md_table(counterexample_rows, ["counterexample_id", "construction", "why_still_legal", "damage", "needed_repair"])}

## Parent Origin Acceptance Gate

{md_table(origin_gate_rows, ["gate_id", "required_clause", "current_evidence", "gate_pass", "missing_input"])}

## Boundary Flux Coefficient Rows

{md_table(boundary_rows, ["coefficient_id", "arena", "coefficient_symbol", "bound_or_anchor_value", "units", "missing_parent_input", "row_status", "valid_for_claim"])}

## Claim Gate

{md_table(claim_rows, ["gate_id", "claim", "current_evidence", "gate_pass", "claim_allowed"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "topic", "result", "reason", "next_action"])}

## Validation

{md_table(validation_rows, ["check_id", "result", "detail", "generated_utc"])}

## Next Target

{md_table(target_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"])}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    sources = source_register()
    theorem_rows = zero_origin_evenness_attempt()
    counterexample_rows = marker_counterexample_audit()
    origin_gate_rows = parent_origin_acceptance_gate()
    boundary_rows = boundary_flux_coefficient_rows()
    claim_rows = claim_gates()
    decision_rows = decisions()
    target_rows = next_target()
    validation_rows = validation(
        sources,
        theorem_rows,
        counterexample_rows,
        origin_gate_rows,
        boundary_rows,
        claim_rows,
        decision_rows,
        target_rows,
    )

    write_csv(
        OUT / "P8_Y5_R10_974_SOURCE_REGISTER.csv",
        sources,
        ["source_id", "path", "role", "needle", "absolute_path", "exists", "needle_found", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_974_ZERO_ORIGIN_EVENNESS_ATTEMPT.csv",
        theorem_rows,
        ["attempt_id", "claim_piece", "mathematical_form", "status", "gap", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_974_MARKER_COUNTEREXAMPLE_AUDIT.csv",
        counterexample_rows,
        ["counterexample_id", "construction", "why_still_legal", "damage", "needed_repair", "counterexample_retained", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_974_PARENT_ORIGIN_ACCEPTANCE_GATE.csv",
        origin_gate_rows,
        ["gate_id", "required_clause", "current_evidence", "gate_pass", "missing_input", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_974_BOUNDARY_FLUX_COEFFICIENT_ROW.csv",
        boundary_rows,
        ["coefficient_id", "arena", "residual_channel", "coefficient_symbol", "bound_or_anchor_value", "units", "source_path", "source_needle", "extraction_method", "missing_parent_input", "row_status", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_974_CLAIM_GATE.csv",
        claim_rows,
        ["gate_id", "claim", "current_evidence", "gate_pass", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_974_DECISION_LEDGER.csv",
        decision_rows,
        ["decision_id", "topic", "result", "reason", "next_action", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_974_NEXT_TARGET.csv",
        target_rows,
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_BRR545_974_VALIDATION.csv",
        validation_rows,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_doc(
        sources,
        theorem_rows,
        counterexample_rows,
        origin_gate_rows,
        boundary_rows,
        claim_rows,
        decision_rows,
        target_rows,
        validation_rows,
    )


if __name__ == "__main__":
    main()
