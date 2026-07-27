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


DOC = ROOT / "2119-Y5-R2FR-projective-invariance-certificate-or-MICROSCOPE-numeric-kernel-acquisition.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

CSV_2118_NEXT = OUT / "P8_Y5_PARENT_QLOC_2118_NEXT_TARGET.csv"
CSV_2118_KERNELS = OUT / "P8_Y5_PARENT_QLOC_2118_EXPLICIT_EXCEPTION_KERNELS.csv"
CSV_2118_ZERO = OUT / "P8_Y5_PARENT_QLOC_2118_SOURCE_READOUT_ZERO_THEOREM_ATTEMPT.csv"
CSV_2118_VAL = OUT / "P8_Y5_BRR545_2118_VALIDATION.csv"
CSV_2117_EXC = OUT / "P8_Y5_PARENT_QLOC_2117_SECTOR_EXCEPTION_LEDGER.csv"
CSV_2099_COMPONENTS = OUT / "P8_Y5_PARENT_QLOC_2099_DELTAGAMMA_COMPONENT_MAP.csv"
CSV_2043_GUARDS = OUT / "P8_Y5_PARENT_QLOC_2043_SPIN_PROJECTIVE_GUARD.csv"
CSV_1960_LC = OUT / "P8_Y5_PARENT_QLOC_1960_LC_NO_HYPERMOMENTUM_ATTEMPT.csv"
CSV_1963_ACTION = OUT / "P8_Y5_PARENT_QLOC_1963_MINIMAL_PARENT_ACTION_SIGNATURE.csv"
CSV_1963_NOGAMMA = OUT / "P8_Y5_PARENT_QLOC_1963_NO_GAMMA_THEOREM.csv"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid", "claim_allowed"}


def formalization_has_2119_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2119-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2119*",
        "*Y5_R2FR_projective_invariance_certificate_or_MICROSCOPE_numeric_kernel_acquisition_2119*",
        "*AFRAME_PROJECTIVE_2119*",
        "*JR2119_MICROSCOPE*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC2119_00_2118_next", CSV_2118_NEXT, ["NEXT2118_0_2119", "projective trace", "MICROSCOPE numeric"], "2118 selects projective certificate or MICROSCOPE numeric kernel."),
        ("SRC2119_01_2118_kernels", CSV_2118_KERNELS, ["KSR2118_6_projective_trace_kernel", "CERTIFICATE_OR_BOUND_MISSING"], "2118 projective fallback kernel."),
        ("SRC2119_02_2118_zero", CSV_2118_ZERO, ["SRZ2118_5_projective_zero", "CONDITIONAL_ZERO_NOT_SIGNED"], "2118 projective zero theorem attempt."),
        ("SRC2119_03_2118_validation", CSV_2118_VAL, ["VAL2118_OVERALL", "PASS"], "2118 validation passed."),
        ("SRC2119_04_2117_exception", CSV_2117_EXC, ["SEC2117_8_projective_trace", "all-sector projective invariance proof missing"], "2117 projective exception."),
        ("SRC2119_05_2099_projective", CSV_2099_COMPONENTS, ["DGM2099_6_projective", "projective_invariance_certificate", "MAP_REGISTERED_PROJECTION_MISSING"], "2099 projective component map."),
        ("SRC2119_06_2043_guards", CSV_2043_GUARDS, ["SPG2043_1_projective_guard", "SPG2043_5_verdict"], "2043 projective guard."),
        ("SRC2119_07_1960_lc", CSV_1960_LC, ["LC1960_5_projective_caveat", "Projective gauge cannot hide"], "1960 projective caveat."),
        ("SRC2119_08_1963_action", CSV_1963_ACTION, ["ACT1963_5_no_independent_Gamma_clause", "NO_GAMMA_BY_VARIABLE_SIGNATURE"], "1963 excludes independent observed Gamma in candidate branch."),
        ("SRC2119_09_1963_nogamma", CSV_1963_NOGAMMA, ["NGT1963_0_theorem", "CONDITIONAL_PROOF_VALID"], "1963 no-Gamma theorem."),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(row(source_id=source_id, source_path=str(path), path_exists=exists, expected_needles="; ".join(needles), needles_found=exists and all(needle in text for needle in needles), role=role))
    return rows


def projective_certificate_rows() -> list[dict[str, object]]:
    return [
        row(
            cert_id="PJC2119_0_projective_shift",
            clause="projective transform",
            statement="Gamma^lambda_{mu nu} -> Gamma^lambda_{mu nu} + delta^lambda_mu A_nu",
            candidate_branch_status="NOT_A_VARIABLE_DIRECTION",
            global_status="REQUIRES_ALL_SECTOR_INVARIANCE_OR_GAUGE_FIX",
            consequence="inside 1963 candidate, there is no independent Gamma to shift; in affine fallback, observable couplings must be checked",
            source_anchor="LC1960_5_projective_caveat; ACT1963_5_no_independent_Gamma_clause",
            branch_zero=True,
            global_zero=False,
        ),
        row(
            cert_id="PJC2119_1_candidate_absence",
            clause="owned-coframe candidate",
            statement="Vars_obs contains e_obs, Xi, Psi and A_owned; omega_obs=omega_LC[e_obs], not an independent projective connection.",
            candidate_branch_status="EXACT_BRANCH_ZERO_BY_VARIABLE_ABSENCE",
            global_status="CANDIDATE_NOT_CANONICAL",
            consequence="projective_trace_current=0 inside the candidate owned-coframe branch.",
            source_anchor="ACT1963_5_no_independent_Gamma_clause; NGT1963_0_theorem",
            branch_zero=True,
            global_zero=False,
        ),
        row(
            cert_id="PJC2119_2_matter_spin",
            clause="ordinary matter/spin",
            statement="Matter/spin dependence on omega_LC[e_obs] contributes through coframe variation, not independent projective trace.",
            candidate_branch_status="CLOSED_INSIDE_CANDIDATE",
            global_status="MATTER_FUNCTOR_STILL_CONDITIONAL",
            consequence="spin and ordinary matter do not revive projective trace inside the candidate branch.",
            source_anchor="NGT1963_0_theorem; NGT1963_1_spinor_guard",
            branch_zero=True,
            global_zero=False,
        ),
        row(
            cert_id="PJC2119_3_source_readout",
            clause="source/readout sectors",
            statement="Source, clock, light, orbit and boundary readouts must also avoid independent projective trace couplings.",
            candidate_branch_status="NOT_FULLY_AUDITED",
            global_status="BLOCKED_BY_SOURCE_READOUT_EXCEPTIONS",
            consequence="source/readout exceptions prevent a public all-sector projective certificate.",
            source_anchor="SEC2117_8_projective_trace; KSR2118_6_projective_trace_kernel",
            branch_zero=False,
            global_zero=False,
        ),
        row(
            cert_id="PJC2119_4_affine_fallback",
            clause="affine fallback",
            statement="If an independent affine/projective trace branch is retained, projective_trace_current must be bounded or proven unobservable in every arena.",
            candidate_branch_status="NOT_NEEDED_IF_BRANCH_PROMOTED",
            global_status="FALLBACK_RETAINED",
            consequence="keep P_projective[source,clock,WEP] kernel and no-cancellation ledger outside candidate branch.",
            source_anchor="DGM2099_6_projective; SPG2043_1_projective_guard",
            branch_zero=False,
            global_zero=False,
        ),
        row(
            cert_id="PJC2119_5_verdict",
            clause="projective certificate",
            statement="Projective trace is killed inside the 1963 owned-coframe candidate by variable absence, but no all-sector/global certificate is claimed.",
            candidate_branch_status="PROJECTIVE_ZERO_INSIDE_CANDIDATE",
            global_status="GLOBAL_CERTIFICATE_BLOCKED",
            consequence="lower the projective guard for the owned-coframe route; continue source/readout canonicalization or numeric kernel acquisition.",
            source_anchor="2118 projective kernel; 1963 no-Gamma theorem",
            branch_zero=True,
            global_zero=False,
        ),
    ]


def projective_residual_policy_rows() -> list[dict[str, object]]:
    return [
        row(policy_id="PRP2119_0_candidate_branch", branch="1963 owned-coframe candidate", projective_current="0", treatment="derived zero by variable absence", score_ready=False, residual_retained=False),
        row(policy_id="PRP2119_1_global_corpus", branch="full current corpus", projective_current="not globally zero", treatment="all-sector source/readout certificate missing", score_ready=False, residual_retained=True),
        row(policy_id="PRP2119_2_affine_fallback", branch="independent affine fallback", projective_current="P_projective[source,clock,WEP]", treatment="retain kernel or source bound; no cancellation", score_ready=False, residual_retained=True),
        row(policy_id="PRP2119_3_MICROSCOPE_data_side", branch="empirical fork", projective_current="not addressed by data alone", treatment="MICROSCOPE numeric kernel can score source/readout residuals but cannot prove projective gauge by itself", score_ready=False, residual_retained=True),
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        row(gate_id="GATE2119_0_candidate_projective_zero", gate="projective trace zero inside owned-coframe candidate", gate_pass=True, rationale="no independent Gamma/projective trace exists in 1963 candidate variables"),
        row(gate_id="GATE2119_1_global_projective_certificate", gate="all-sector projective certificate", gate_pass=False, rationale="source/readout sectors are not globally canonical and all-sector invariance is not proven"),
        row(gate_id="GATE2119_2_affine_projective_score", gate="affine projective fallback score-ready", gate_pass=False, rationale="trace-coupling normalization and source/readout projection/bound are missing"),
        row(gate_id="GATE2119_3_source_readout_silence", gate="source/readout Gamma silence follows", gate_pass=False, rationale="projective branch progress does not close source, clock, light, orbit or boundary kernels"),
        row(gate_id="GATE2119_4_local_GR_Newton", gate="derived local GR/Newton claim allowed", gate_pass=False, rationale="canonical promotion, EH/source/readout/PPN gates remain open"),
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(decision_id="DEC2119_0", decision="PROJECTIVE_GUARD_LOWERED_INSIDE_CANDIDATE", because="1963 has no independent observed Gamma, so projective trace is absent inside the branch.", next_action="carry projective as branch-zero when auditing owned-coframe canonicalization."),
        row(decision_id="DEC2119_1", decision="GLOBAL_PROJECTIVE_CLAIM_BLOCKED", because="source/readout exceptions are not globally closed.", next_action="retain projective kernel outside the candidate branch."),
        row(decision_id="DEC2119_2", decision="DATA_SIDE_NEXT", because="after spin and projective are lowered inside the candidate, the biggest non-theorem wall is numeric source/readout projection.", next_action="go after MICROSCOPE numeric kernel acquisition/reconstruction next."),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2119_0_2120",
            next_target="2120-Y5-R2FR-MICROSCOPE-numeric-source-readout-kernel-acquisition.md",
            script="scripts/Y5_R2FR_MICROSCOPE_numeric_source_readout_kernel_acquisition_2120.py",
            objective="Acquire or reconstruct the numeric MICROSCOPE source/readout kernel inputs: orbit/attitude sampling, gx/gz/Sxx/Sxz arrays or defensible proxies, eta convention, segment averaging and source-worldtube normalization. Keep all rows nonclaim until data are real.",
            forbidden_shortcuts="using the 1071 skeleton as numeric data; assuming projective/source/readout silence; fitted-G absorption; cancellation; local-GR/Newton/PPN claim; formalization-workbench edits; GitHub action",
        )
    ]


def write_branch_copies(certs: list[dict[str, object]], policies: list[dict[str, object]], next_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    copies = [
        ("COPY2119_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_PROJECTIVE_2119_NONCLAIM.csv", certs + policies),
        ("COPY2119_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2119_PROJECTIVE_STATUS_NONCLAIM.csv", certs + policies),
        ("COPY2119_2_acquisition_queue", QUEUE / "JR2119_MICROSCOPE_NUMERIC_KERNEL_QUEUE.csv", next_rows + policies),
    ]
    result: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        result.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return result


def validation_rows(
    sources: list[dict[str, object]],
    certs: list[dict[str, object]],
    policies: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    branch_zero_ok = any(item["cert_id"] == "PJC2119_5_verdict" and truthy(item["branch_zero"]) and not truthy(item["global_zero"]) for item in certs)
    fallback_ok = any(item["policy_id"] == "PRP2119_2_affine_fallback" and truthy(item["residual_retained"]) for item in policies)
    gates_ok = any(item["gate_id"] == "GATE2119_0_candidate_projective_zero" and truthy(item["gate_pass"]) for item in gates) and any(item["gate_id"] == "GATE2119_1_global_projective_certificate" and not truthy(item["gate_pass"]) for item in gates)
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, certs, policies, gates, decisions, next_rows, copies)
        for item in group
    )
    branch_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2119_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    next_ok = any(item["route_id"] == "NEXT2119_0_2120" for item in next_rows)
    all_ok = all([sources_ok, branch_zero_ok, fallback_ok, gates_ok, no_claim_flags, branch_ok, csv_ok, formalization_clean, pycache_clean, next_ok])
    checks = [
        ("VAL2119_00_sources", sources_ok, "all cited projective/source files exist and contain expected needles"),
        ("VAL2119_01_branch_zero", branch_zero_ok, "projective trace is zero only inside the 1963 candidate branch"),
        ("VAL2119_02_fallback", fallback_ok, "affine/global projective fallback remains retained"),
        ("VAL2119_03_claim_gates", gates_ok, "candidate projective gate passes but global gate fails"),
        ("VAL2119_04_no_claim_flags", no_claim_flags, "no generated row allows a claim or score"),
        ("VAL2119_05_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2119_06_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2119_07_formalization_clean", formalization_clean, "formalization-workbench untouched by 2119"),
        ("VAL2119_08_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2119_09_next", next_ok, "next target selects MICROSCOPE numeric kernel acquisition"),
        ("VAL2119_OVERALL", all_ok, "2119 lowers projective trace inside the owned-coframe candidate, keeps global claims blocked, and selects numeric source/readout kernel acquisition next."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    certs: list[dict[str, object]],
    policies: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    content = "\n\n".join(
        [
            "# 2119 - Y5/R2FR Projective Invariance Certificate Or MICROSCOPE Numeric Kernel Acquisition",
            "## Current Verdict",
            "2119 lowers another guard, but only inside the owned-coframe candidate branch. Since the 1963 branch has no independent observed `Gamma`, a projective trace direction is not a physical variable direction there. So `projective_trace_current=0` inside that branch by variable absence.",
            "This is not a global all-sector certificate. If the affine fallback survives, or if source/readout sectors reintroduce independent connection/readout trace couplings, the projective kernel remains live and must be bounded or proven unobservable.",
            "Net effect: spin and projective trace are now branch-zero candidates; source/readout numeric kernels are the next practical wall.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Projective Certificate",
            md_table(certs, ["cert_id", "clause", "candidate_branch_status", "global_status", "statement", "consequence", "branch_zero", "global_zero", "valid_for_claim"]),
            "## Residual Policy",
            md_table(policies, ["policy_id", "branch", "projective_current", "treatment", "score_ready", "residual_retained", "valid_for_claim"]),
            "## Claim Gates",
            md_table(gates, ["gate_id", "gate", "gate_pass", "rationale", "valid_for_claim", "claim_allowed"]),
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
    certs = projective_certificate_rows()
    policies = projective_residual_policy_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2119_SOURCE_REGISTER.csv",
        "certs": OUT / "P8_Y5_PARENT_QLOC_2119_PROJECTIVE_CERTIFICATE.csv",
        "policies": OUT / "P8_Y5_PARENT_QLOC_2119_PROJECTIVE_RESIDUAL_POLICY.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2119_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2119_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2119_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2119_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2119_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["certs"], certs)
    write_csv(paths["policies"], policies)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows)

    copies = write_branch_copies(certs, policies, next_rows)
    write_csv(paths["branch"], copies)

    remove_pycache()
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(copy["destination"])) for copy in copies]
    validation = validation_rows(sources, certs, policies, gates, decisions, next_rows, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, certs, policies, gates, decisions, next_rows, copies, validation)

    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
