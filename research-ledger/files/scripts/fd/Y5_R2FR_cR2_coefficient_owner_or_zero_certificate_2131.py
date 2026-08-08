from __future__ import annotations

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


DOC = ROOT / "2131-Y5-R2FR-cR2-coefficient-owner-or-zero-certificate.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

CSV_2130_NEXT = OUT / "P8_Y5_PARENT_QLOC_2130_NEXT_TARGET.csv"
CSV_2130_VAL = OUT / "P8_Y5_BRR545_2130_VALIDATION.csv"
CSV_2130_ACQ = OUT / "P8_Y5_PARENT_QLOC_2130_R2FR_COEFFICIENT_ACQUISITION.csv"
CSV_2130_SELECTOR = OUT / "P8_Y5_PARENT_QLOC_2130_SELECTOR_CONTRACT.csv"
CSV_2130_GATES = OUT / "P8_Y5_PARENT_QLOC_2130_CLAIM_GATES.csv"
CSV_1822_OWNER = OUT / "P8_Y5_PARENT_QLOC_1822_R2FR_COEFFICIENT_OWNER_ROW.csv"
CSV_1965_ZERO = OUT / "P8_Y5_PARENT_QLOC_1965_R2FR_ZERO_PROOF_ATTEMPT.csv"
CSV_1965_MAP = OUT / "P8_Y5_PARENT_QLOC_1965_R2FR_SCALARON_MAP.csv"
CSV_1965_SCHEMA = OUT / "P8_Y5_PARENT_QLOC_1965_R2FR_EXECUTABLE_BOUND_SCHEMA.csv"
CSV_1588_MAP = OUT / "P8_Y5_PARENT_QLOC_1588_R2FR_SCALARON_MAP.csv"
CSV_1821_SCHEMA = OUT / "P8_Y5_PARENT_QLOC_1821_R2FR_BOUND_ROW_SCHEMA.csv"
CSV_R11_EXEC = OUT / "R11_nonEH_operator_vector_executable.csv"
DOC_963 = ROOT / "963-Y5-R10-parent-second-order-signature-or-R2FR-bound-runner.md"
DOC_964 = ROOT / "964-Y5-R10-parent-no-higher-derivative-minimality-theorem-or-R2FR-nonclaim-runner.md"
DOC_965 = ROOT / "965-Y5-R10-primitive-quotient-no-natural-marker-theorem-or-R2FR-full-curve-intake.md"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid"}


def formalization_has_2131_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2131-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2131*",
        "*Y5_R2FR_cR2_coefficient_owner_or_zero_certificate_2131*",
        "*AFRAME_CR2_OWNER_2131*",
        "*JR2131*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC2131_00_2130_next", CSV_2130_NEXT, ["NEXT2130_0_2131", "cR2-coefficient-owner"], "2130 handoff selects c_R2 coefficient owner or zero certificate."),
        ("SRC2131_01_2130_validation", CSV_2130_VAL, ["VAL2130_OVERALL", "PASS"], "2130 validation passed."),
        ("SRC2131_02_2130_acq", CSV_2130_ACQ, ["R2FR2130_1_parent_coefficient", "MISSING_PARENT_NUMERIC_OR_SYMBOLIC_COEFFICIENT"], "2130 coefficient acquisition row is blocked by missing parent coefficient."),
        ("SRC2131_03_2130_selector", CSV_2130_SELECTOR, ["SEL2130_2_no_integrated_out_tower", "UNSIGNED_CENTRAL_BLOCKER"], "no integrated curvature tower is the central selector blocker."),
        ("SRC2131_04_2130_gates", CSV_2130_GATES, ["GATE2130_4_R2FR_finite_row_executable", "False"], "finite R2/fR row is not executable."),
        ("SRC2131_05_1822_owner", CSV_1822_OWNER, ["CO1822_5_verdict", "NO_EXECUTABLE_OWNER_FOUND_CURRENT_1822"], "older owner row confirms no executable owner."),
        ("SRC2131_06_1965_zero", CSV_1965_ZERO, ["ZP1965_6_verdict", "ZERO_PROOF_FAILED_CLEANLY"], "zero proof failed cleanly."),
        ("SRC2131_07_1965_map", CSV_1965_MAP, ["SM1965_1_scalar_mass", "SM1965_2_yukawa_alpha"], "scalaron formulas are available conditionally."),
        ("SRC2131_08_1965_schema", CSV_1965_SCHEMA, ["EXR1965_1_mts_prediction", "MISSING_PARENT_NUMERIC_COEFFICIENT"], "executable schema demands parent coefficient."),
        ("SRC2131_09_1588_map", CSV_1588_MAP, ["SC1588_5_verdict", "FAIL_CURRENT_CLAIM_NO_SCALARON_PREDICTION"], "scalaron prediction absent."),
        ("SRC2131_10_1821_schema", CSV_1821_SCHEMA, ["R2B1821_5_total", "MISSING_PARENT_AND_ARENA_INPUTS_ROW_NONCLAIM"], "bound-row contract remains nonclaim."),
        ("SRC2131_11_R11_exec", CSV_R11_EXEC, ["R2_fR_scalar_mode", "MISSING_NUMERIC_OR_DERIVED_ZERO_COEFFICIENT"], "R11 executable vector still has missing R2/fR coefficient."),
        ("SRC2131_12_963_doc", DOC_963, ["NO_EXECUTABLE_OWNER_FOUND", "MISSING_PARENT_INPUT"], "963 says no executable owner and runner input missing."),
        ("SRC2131_13_964_doc", DOC_964, ["CM964_1_auxiliary_scalar_integrated_out", "THEOREM_NOT_PROVEN_CURRENT_CORPUS"], "964 keeps integrated-out scalar countermodel live."),
        ("SRC2131_14_965_doc", DOC_965, ["ALG965_9_verdict", "MC965_2_quotient_invariant_scalar"], "965 leaves invariant scalar/marker generators live."),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            row(
                source_id=source_id,
                source_path=str(path),
                path_exists=exists,
                expected_needles="; ".join(needles),
                needles_found=exists and all(needle in text for needle in needles),
                role=role,
            )
        )
    return rows


def zero_certificate_rows() -> list[dict[str, object]]:
    return [
        row(
            cert_id="ZC2131_0_bare_operator_absent",
            clause="no bare R2/f(R) term in the primitive compact local action",
            zero_condition="c_R2_bare=0 and f_RR_bare=0 by parent action basis, not by preference",
            current_status="UNSIGNED",
            blocker="primitive first-jet/coframe minimality is not parent-signed strongly enough to exclude curvature-square generators",
            consequence="bare contribution to c_R2_eff remains missing, not zero",
        ),
        row(
            cert_id="ZC2131_1_no_integrated_out_scalar",
            clause="no eliminated scalar/auxiliary sector generates R2 after solving its Euler equation",
            zero_condition="for every Xi_A: beta_A=0, M_A^-2=0, source coupling zero, or variation/readout stress harmless before substitution",
            current_status="UNSIGNED_CENTRAL_BLOCKER",
            blocker="964 countermodel S=EH-1/2 M^2 phi^2+beta phi R remains legal",
            consequence="hidden scalar contribution beta_A^2/(2 M_A^2) cannot be set to zero",
        ),
        row(
            cert_id="ZC2131_2_no_marker_prefactor",
            clause="no quotient-invariant marker or class scalar multiplies R",
            zero_condition="F'(sigma)=F''(sigma)=0 locally, or sigma is universal constant with zero stress/source/readout effect",
            current_status="UNSIGNED",
            blocker="965 leaves quotient-invariant scalar, material marker, domain selector and species constants live",
            consequence="F(sigma)R can mimic scalar-tensor/f(R) leakage",
        ),
        row(
            cert_id="ZC2131_3_no_nonlocal_memory_local_expansion",
            clause="memory/nonlocal kernels do not reduce to local R2/f(R) terms in compact tests",
            zero_condition="local expansion coefficient of R Box^-1 R or history kernel is zero/screened with source-backed proof",
            current_status="UNSIGNED",
            blocker="nonlocal memory kernel countermodel remains live in 964 and R11",
            consequence="nonlocal contribution to effective curvature-square response remains retained",
        ),
        row(
            cert_id="ZC2131_4_no_boundary_or_redefinition_escape",
            clause="R2/f(R) is not hidden as boundary/topological/redefinition content",
            zero_condition="only exact 4D Gauss-Bonnet/topological or readout-equivalent field redefinition is harmless",
            current_status="PARTIAL_REJECTION_ONLY",
            blocker="R2 alone is not Gauss-Bonnet; redefinition equivalence would need matter/source/readout proof",
            consequence="cannot declare the scalar mode harmless by boundary language",
        ),
        row(
            cert_id="ZC2131_5_zero_certificate_verdict",
            clause="set c_R2_eff=f_RR=0",
            zero_condition="ZC2131_0 through ZC2131_4 all signed with source paths",
            current_status="ZERO_CERTIFICATE_NOT_DERIVED",
            blocker="bare, integrated-out, marker, nonlocal and readout-equivalence routes are not all killed",
            consequence="R2/fR remains a retained nonclaim operator family",
        ),
    ]


def coefficient_owner_rows() -> list[dict[str, object]]:
    return [
        row(
            owner_id="OWN2131_0_total_definition",
            owner_route="effective coefficient decomposition",
            formula="c_R2_eff = c_bare + sum_A beta_A^2/(2 M_A^2) + c_marker + c_nonlocal + c_boundary/redef + c_counterterm",
            required_inputs="all component coefficients, signs, units, EH normalization, source paths and no-cancellation policy",
            owner_status="DECOMPOSITION_WRITTEN_NONEXECUTABLE",
            score_ready=False,
        ),
        row(
            owner_id="OWN2131_1_bare_curvature_square",
            owner_route="visible parent curvature-square coefficient",
            formula="c_bare in S=(1/2 kappa) int sqrt(-g)(R + c_bare R^2 + ...)",
            required_inputs="parent action basis; coefficient or zero theorem; length^2 units; normalization relative to EH term",
            owner_status="MISSING_PARENT_INPUT",
            score_ready=False,
        ),
        row(
            owner_id="OWN2131_2_integrated_out_aux_scalar",
            owner_route="hidden scalar/auxiliary field solved before observed reduction",
            formula="simple algebraic toy: L_phi=-1/2 M^2 phi^2 + beta phi R gives Delta L_eff=beta^2 R^2/(2 M^2)",
            required_inputs="beta_A, M_A, sign convention, source/readout coupling, proof the algebraic toy applies, or theorem beta_A=0/M_A=infinity",
            owner_status="COUNTERMODEL_LIVE_NOT_SOURCED",
            score_ready=False,
        ),
        row(
            owner_id="OWN2131_3_marker_prefactor",
            owner_route="quotient-invariant marker/class scalar prefactor",
            formula="F(sigma)R can generate scalar-tensor/f(R)-like response after sigma variation or local expansion",
            required_inputs="F derivatives, sigma dynamics, local value/gradient, source coupling, no-marker theorem or finite coefficient map",
            owner_status="NO_MARKER_THEOREM_MISSING",
            score_ready=False,
        ),
        row(
            owner_id="OWN2131_4_nonlocal_memory_expansion",
            owner_route="nonlocal/memory kernel local expansion",
            formula="R K R or R Box^-1 R may induce effective c_nonlocal at compact-test scales",
            required_inputs="kernel norm, support scale, locality/screening theorem, expansion coefficient and R10/PPN regime map",
            owner_status="KERNEL_OWNER_MISSING",
            score_ready=False,
        ),
        row(
            owner_id="OWN2131_5_boundary_redefinition",
            owner_route="boundary/topological/redefinition channel",
            formula="harmless only for exact topological combination or field redefinition preserving matter/source/readout observables",
            required_inputs="exact GB/topological proof or equivalence theorem for matter, clocks, sources, boundaries and PPN readout",
            owner_status="NOT_A_ZERO_CERTIFICATE_CURRENTLY",
            score_ready=False,
        ),
        row(
            owner_id="OWN2131_6_verdict",
            owner_route="current corpus",
            formula="no executable c_R2_eff/f_RR owner and no zero certificate",
            required_inputs="derive ZC2131 certificate or fill one owner route with units/sign/source",
            owner_status="NO_EXECUTABLE_OWNER_FOUND_2131",
            score_ready=False,
        ),
    ]


def strict_row_update_rows() -> list[dict[str, object]]:
    return [
        row(field_id="ROW2131_0_coefficient", field="c_R2_eff_or_f_RR", current_value="MISSING_PARENT_NUMERIC_OR_SYMBOLIC_COEFFICIENT", required_before_score="zero certificate or component decomposition with sourced coefficient", status="BLOCKS_SCORE"),
        row(field_id="ROW2131_1_units", field="coefficient_units", current_value="length_squared_after_EH_normalization_required", required_before_score="explicit c=1/SI conversion and normalization S=(1/2kappa)int sqrt(-g)(R+cR2 R^2)", status="DECLARED_REQUIREMENT"),
        row(field_id="ROW2131_2_sign", field="sign_and_stability", current_value="MISSING_SIGN", required_before_score="positive c_R2 for simple non-tachyonic scalaron or explicit alternative branch", status="BLOCKS_SCALARON_MAP"),
        row(field_id="ROW2131_3_scalaron", field="lambda_s_alpha_s", current_value="FORMULA_ONLY", required_before_score="lambda_s=sqrt(6 c_R2) and alpha_s=1/3 only with unscreened metric f(R) context", status="CONDITIONAL_NONCLAIM"),
        row(field_id="ROW2131_4_screening", field="screening_readout_regime", current_value="MISSING", required_before_score="lab/solar-system regime, source/test coupling and readout-frame certificate", status="BLOCKS_PPN_R10_SCORE"),
        row(field_id="ROW2131_5_bound_curve", field="alpha_bound_lambda", current_value="MISSING_VALID_FULL_CURVE", required_before_score="digitized or machine-readable full curve with provenance, units and convention", status="BLOCKS_R10_SCORE"),
        row(field_id="ROW2131_6_acceptance", field="valid_for_claim", current_value=False, required_before_score="all blocking rows resolved with source paths and no bound-to-prediction inversion", status="FORCED_FALSE"),
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        row(gate_id="GATE2131_0_sources", gate="source evidence loaded", gate_pass=True, rationale="2130, 1822, 1965, 963, 964 and 965 sources are present and needle-checked"),
        row(gate_id="GATE2131_1_zero_certificate", gate="c_R2_eff/f_RR zero certificate derived", gate_pass=False, rationale="bare, integrated-out scalar, marker, nonlocal and boundary/redefinition routes are not all killed"),
        row(gate_id="GATE2131_2_owner_decomposition", gate="owner decomposition written", gate_pass=True, rationale="all major legal c_R2 owner routes are separated"),
        row(gate_id="GATE2131_3_executable_owner", gate="executable finite coefficient owner found", gate_pass=False, rationale="no coefficient value/sign/units/source path exists"),
        row(gate_id="GATE2131_4_scalaron_score", gate="R2/fR scalaron score ready", gate_pass=False, rationale="coefficient, screening/readout map and full bound curve are missing"),
        row(gate_id="GATE2131_5_EH_second_order", gate="EH second-order selector activated", gate_pass=False, rationale="R2/fR zero is not proven and selector contract remains unsigned"),
        row(gate_id="GATE2131_6_local_GR_Newton_PPN_claim", gate="local GR/Newton/PPN claim allowed", gate_pass=False, rationale="operator, source normalization, PPN and empirical gates remain open"),
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(decision_id="DEC2131_0", decision="ZERO_CERTIFICATE_NOT_DERIVED", because="legal owner routes for c_R2_eff remain live", next_action="do not claim EH second-order selection"),
        row(decision_id="DEC2131_1", decision="OWNER_DECOMPOSITION_ADOPTED", because="the coefficient is now a finite sum of owner routes rather than a fog term", next_action="attack the strongest owner route first"),
        row(decision_id="DEC2131_2", decision="NEXT_ATTACK_NO_INTEGRATED_CURVATURE_TOWER", because="hidden auxiliary scalar beta^2/(2M^2) is the cleanest countermodel to a bare zero action", next_action="prove no integrated curvature tower or stage an auxiliary scalar coefficient row"),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2131_0_2132",
            next_target="2132-Y5-R2FR-no-integrated-curvature-tower-or-aux-scalar-coefficient-row.md",
            script="scripts/Y5_R2FR_no_integrated_curvature_tower_or_aux_scalar_coefficient_row_2132.py",
            objective="Try to prove that no eliminated MTS auxiliary/scalar/memory sector can generate beta^2 R^2/(2M^2), f(R), or a scalar pole after variation; if not, write the first auxiliary-scalar coefficient row with beta, M, sign, units, source/readout coupling and nonclaim scalaron interface.",
            forbidden_shortcuts="assuming clean primitive action means clean effective action; using stability as zero proof; inventing beta/M; scoring alpha(lambda) without parent coefficient and full curve; formalization-workbench edits; GitHub action",
        )
    ]


def write_branch_copies(
    certs: list[dict[str, object]],
    owners: list[dict[str, object]],
    strict_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        ("COPY2131_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_CR2_OWNER_2131_NONCLAIM.csv", certs + owners + gates),
        ("COPY2131_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2131_CR2_OWNER_NONCLAIM.csv", owners + strict_rows),
        ("COPY2131_2_acquisition_queue", QUEUE / "JR2131_NO_TOWER_OR_AUX_SCALAR_QUEUE.csv", next_rows + strict_rows),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    certs: list[dict[str, object]],
    owners: list[dict[str, object]],
    strict_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    cert_ok = any(item["cert_id"] == "ZC2131_5_zero_certificate_verdict" and item["current_status"] == "ZERO_CERTIFICATE_NOT_DERIVED" for item in certs)
    owners_ok = any(item["owner_id"] == "OWN2131_0_total_definition" and "c_R2_eff" in str(item["formula"]) for item in owners) and any(item["owner_id"] == "OWN2131_6_verdict" and item["owner_status"] == "NO_EXECUTABLE_OWNER_FOUND_2131" for item in owners)
    strict_ok = any(item["field_id"] == "ROW2131_0_coefficient" and item["status"] == "BLOCKS_SCORE" for item in strict_rows) and any(item["field_id"] == "ROW2131_6_acceptance" and item["current_value"] is False for item in strict_rows)
    gates_ok = any(item["gate_id"] == "GATE2131_2_owner_decomposition" and truthy(item["gate_pass"]) for item in gates) and any(item["gate_id"] == "GATE2131_6_local_GR_Newton_PPN_claim" and not truthy(item["gate_pass"]) for item in gates)
    decisions_ok = any(item["decision_id"] == "DEC2131_2" and "NO_INTEGRATED_CURVATURE_TOWER" in str(item["decision"]) for item in decisions)
    next_ok = any(item["route_id"] == "NEXT2131_0_2132" for item in next_rows)
    branch_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, certs, owners, strict_rows, gates, decisions, next_rows, copies)
        for item in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2131_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, cert_ok, owners_ok, strict_ok, gates_ok, decisions_ok, next_ok, branch_ok, csv_ok, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2131_00_sources", sources_ok, "all cited cR2 owner sources exist and contain expected needles"),
        ("VAL2131_01_zero_certificate", cert_ok, "zero certificate is explicitly not derived"),
        ("VAL2131_02_owner_decomposition", owners_ok, "owner decomposition is written and no executable owner is found"),
        ("VAL2131_03_strict_row", strict_ok, "strict coefficient row remains blocked and valid_for_claim false"),
        ("VAL2131_04_gates", gates_ok, "owner decomposition gate passes while local-GR claim gate fails"),
        ("VAL2131_05_decisions", decisions_ok, "decision ledger selects no integrated curvature tower next"),
        ("VAL2131_06_next", next_ok, "next target is 2132 no integrated curvature tower or auxiliary scalar row"),
        ("VAL2131_07_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2131_08_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2131_09_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2131_10_formalization_clean", formalization_clean, "formalization-workbench untouched by 2131"),
        ("VAL2131_11_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2131_OVERALL", all_ok, "2131 fails the cR2 zero certificate honestly, decomposes coefficient ownership, and selects the no-integrated-curvature-tower gate next."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    certs: list[dict[str, object]],
    owners: list[dict[str, object]],
    strict_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    content = "\n\n".join(
        [
            "# 2131 - Y5/R2FR cR2 Coefficient Owner Or Zero Certificate",
            "## Current Verdict",
            "2131 tries the sharp version of the R2/f(R) derivation: either prove `c_R2_eff=f_RR=0`, or identify who owns the coefficient. The zero certificate does not close. The parent evidence still leaves bare curvature-square terms, integrated-out auxiliary scalars, quotient-invariant marker prefactors, nonlocal memory expansions, and boundary/redefinition escapes alive.",
            "But this is useful progress. The coefficient is no longer a fog bank: `c_R2_eff = c_bare + sum beta_A^2/(2 M_A^2) + c_marker + c_nonlocal + c_boundary/redef + c_counterterm`. Every term now has an owner route and a kill/fill requirement. The strongest next route is the integrated-out curvature tower, because even a clean primitive action can regenerate `R^2` after solving a hidden scalar.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Zero Certificate Audit",
            md_table(certs, ["cert_id", "clause", "zero_condition", "current_status", "blocker", "consequence", "valid_for_claim"]),
            "## Coefficient Owner Decomposition",
            md_table(owners, ["owner_id", "owner_route", "formula", "required_inputs", "owner_status", "score_ready", "valid_for_claim"]),
            "## Strict Executable Row Update",
            md_table(strict_rows, ["field_id", "field", "current_value", "required_before_score", "status", "valid_for_claim"]),
            "## Claim Gates",
            md_table(gates, ["gate_id", "gate", "gate_pass", "rationale", "claim_allowed", "valid_for_claim"]),
            "## Decision Ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "## Next Target",
            md_table(next_rows, ["route_id", "next_target", "script", "objective", "forbidden_shortcuts", "valid_for_claim"]),
            "## Branch Copies",
            md_table(copies, ["copy_id", "destination", "path_exists", "row_count", "parse_ok", "valid_for_claim"]),
            "## Validation",
            md_table(validation, ["check_id", "status", "detail", "claim_allowed", "valid_for_claim"]),
        ]
    )
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    certs = zero_certificate_rows()
    owners = coefficient_owner_rows()
    strict_rows = strict_row_update_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2131_SOURCE_REGISTER.csv",
        "certs": OUT / "P8_Y5_PARENT_QLOC_2131_ZERO_CERTIFICATE_AUDIT.csv",
        "owners": OUT / "P8_Y5_PARENT_QLOC_2131_CR2_OWNER_DECOMPOSITION.csv",
        "strict": OUT / "P8_Y5_PARENT_QLOC_2131_STRICT_EXECUTABLE_ROW_UPDATE.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2131_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2131_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2131_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2131_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2131_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["certs"], certs)
    write_csv(paths["owners"], owners)
    write_csv(paths["strict"], strict_rows)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows)

    copies = write_branch_copies(certs, owners, strict_rows, gates, next_rows)
    write_csv(paths["branch"], copies)

    remove_pycache()
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(copy["destination"])) for copy in copies]
    validation = validation_rows(sources, certs, owners, strict_rows, gates, decisions, next_rows, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, certs, owners, strict_rows, gates, decisions, next_rows, copies, validation)

    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
