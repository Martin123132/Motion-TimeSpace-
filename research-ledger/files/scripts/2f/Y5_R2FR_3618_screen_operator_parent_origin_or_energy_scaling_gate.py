from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3618"
BRANCH_ID = "MTS_R2FR_Y5_SCREEN_OPERATOR_PARENT_ORIGIN_OR_ENERGY_SCALING_GATE_3618"
DOC = ROOT / "3618-Y5-R2FR-screen-operator-parent-origin-or-energy-scaling-gate.md"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for fieldname in row:
            if fieldname not in fieldnames:
                fieldnames.append(fieldname)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    return needle in path.read_text(encoding="utf-8-sig", errors="replace")


def output_paths() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3618_SOURCE_REGISTER.csv",
        "screen_zero_theorem": RESIDUALS / "P8_Y5_R2FR_3618_SCREEN_SPLIT_ZERO_THEOREM.csv",
        "operator_dimension_gate": RESIDUALS / "P8_Y5_R2FR_3618_OPERATOR_DIMENSION_ENERGY_SCALING_GATE.csv",
        "branch_packet": RESIDUALS / "P8_Y5_R2FR_3618_SCREEN_BRANCH_PACKET.csv",
        "projection_update": RESIDUALS / "P8_Y5_R2FR_3618_KTHETA_PROJECTION_UPDATE.csv",
        "decision_gates": RESIDUALS / "P8_Y5_R2FR_3618_DECISION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3618_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3618_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_screen_operator_parent_origin_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3618_VALIDATION.csv",
    }


def source_map() -> dict[str, tuple[Path, str]]:
    return {
        "handoff_3617": (
            RESIDUALS / "P8_Y5_R2FR_3617_NEXT_TARGET.csv",
            "3618-Y5-R2FR-screen-operator-parent-origin-or-energy-scaling-gate.md",
        ),
        "ktheta_3617": (
            RESIDUALS / "P8_Y5_R2FR_3617_KTHETA_SCREEN_ROOT_SPLIT_DERIVATION.csv",
            "h_AB",
        ),
        "energy_3617": (
            RESIDUALS / "P8_Y5_R2FR_3617_ENERGY_SCALING_LEDGER.csv",
            "PROMISING_ROUTE_NOT_PARENT_SIGNED",
        ),
        "runner_3617": (
            RESIDUALS / "P8_Y5_R2FR_3617_KTHETA_PROJECTION_RUNNER.csv",
            "BLOCKED_SYMBOLIC_KTHETA_DERIVED",
        ),
        "observed_hodge_3503": (
            RESIDUALS / "P8_Y5_R2FR_3503_OBSERVED_HODGE_MAXWELL_OWNER_THEOREM.csv",
            "*_EM=*_obs",
        ),
        "hodge_uniqueness_3504": (
            RESIDUALS / "P8_Y5_R2FR_3504_HODGE_UNIQUENESS_THEOREM.csv",
            "unique Hodge star",
        ),
        "chi_reconstruct_3287": (
            RESIDUALS / "P8_Y5_R2FR_3287_CHI_TO_HODGE_RECONSTRUCTION_THEOREM.csv",
            "theta_ax",
        ),
        "em_owner_3465": (
            RESIDUALS / "P8_Y5_R2FR_3465_EM_OWNER_PACKAGE_AUDIT.csv",
            "unique Maxwell curvature norm",
        ),
        "action_domain_3505": (
            RESIDUALS / "P8_EM_visible_action_domain_exhaustion_no_chiEM_bound_vector.csv",
            "Delta_chi_principal",
        ),
    }


def source_register_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    rows = []
    for source_id, source_data in source_map().items():
        source_path, needle = source_data
        exists = source_path.exists()
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source_id,
                "source_path": str(source_path),
                "exists": exists,
                "needle": needle,
                "needle_found": exists and contains(source_path, needle),
                "valid_for_claim": False,
            }
        )
    return rows


def screen_zero_theorem_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    sources = source_map()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "SZT3618_0_screen_split_definition",
            "claim_piece": "trace-free screen split",
            "statement": "Only the trace-free spectral diameter of the two-polarization screen operator contributes to Fresnel birefringence.",
            "formula": "h_split := h_AB - (1/2)tr(h) delta_AB; diam_spec(h)=diam_spec(h_split)",
            "result": "scalar impedance/normalization does not create a polarization split",
            "status": "DEFINITION_DERIVED",
            "source_path": str(sources["ktheta_3617"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "SZT3618_1_hodge_branch_identity",
            "claim_piece": "observed Hodge Maxwell branch",
            "statement": "If the EM principal action is the observed Hodge Maxwell action, the physical screen principal symbol is proportional to the identity on transverse polarizations.",
            "formula": "S_EM=-1/4 int Z_Q F wedge *_obs F => h_AB = sigma(k) delta_AB",
            "result": "h_split=0 and diam_spec(h)=0 for the local Hodge branch",
            "status": "EXACT_CONDITIONAL_ZERO",
            "source_path": str(sources["observed_hodge_3503"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "SZT3618_2_conformal_scale_guard",
            "claim_piece": "conformal/impedance scale",
            "statement": "A common conformal or impedance factor can change normalization/source coupling, but it cannot split the two transverse polarizations.",
            "formula": "chi=Z_Q *_g => h_AB proportional delta_AB; diam_spec(h)=0",
            "result": "GRB Fresnel split is silent while source/charge normalization gates remain live",
            "status": "ZERO_FOR_BIREFRINGENCE_NOT_FOR_COUPLING",
            "source_path": str(sources["hodge_uniqueness_3504"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "SZT3618_3_constant_axion_guard",
            "claim_piece": "constant axion",
            "statement": "A constant axion/topological F wedge F term does not alter the local principal Fresnel cone or the screen split.",
            "formula": "theta0 F wedge F contributes boundary/topological term; principal h_split=0",
            "result": "axion gradients remain separate polarization-rotation rows, not B_Fresnel screen splitting",
            "status": "ZERO_FOR_CONSTANT_AXION_SEPARATE_GRADIENT_GATE",
            "source_path": str(sources["chi_reconstruct_3287"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "SZT3618_4_parent_zero_contract",
            "claim_piece": "h_AB zero branch",
            "statement": "The local-GR/Maxwell branch gives h_split=0 if same-metric observed Hodge descent is parent-signed and independent constitutive/higher-derivative/readout terms are excluded.",
            "formula": "same_metric && observed_Hodge && unique_F2 && no_chi_EM && no_HD_screen && constant_or_absent_axion_gradient => h_split=0",
            "result": "B_Fresnel_MTS=0 and xi_MTS_eff=0 in that conditional branch",
            "status": "CONDITIONAL_THEOREM_ZERO_ROUTE_NOT_PARENT_SIGNED",
            "source_path": str(sources["action_domain_3505"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "SZT3618_5_surviving_sources",
            "claim_piece": "nonzero h_AB sources",
            "statement": "A nonzero screen split can only come from explicit surviving operators, not from ordinary Hodge Maxwell theory.",
            "formula": "h_split != 0 requires chi_aniso, skewon/non-Lagrangian, hidden Hodge, readout-after-variation, higher-derivative operator, or axion-gradient rotation gate",
            "result": "nonzero branch must carry a typed coefficient row with source path and energy scaling",
            "status": "SURVIVING_OPERATOR_LIST_DERIVED",
            "source_path": str(sources["action_domain_3505"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def operator_dimension_gate_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    sources = source_map()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "operator_id": "ODG3618_0_two_derivative_nonHodge",
            "operator_class": "two-derivative independent principal constitutive tensor",
            "schematic_action": "Delta S=-1/4 int F chi_aniso F",
            "energy_power_s": 0,
            "screen_effect": "energy-independent h_split",
            "gate": "forbid by action-domain exhaustion or bound as s=0",
            "status": "DANGEROUS_NONZERO_BRANCH_REQUIRES_PARENT_ROW",
            "source_path": str(sources["action_domain_3505"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "operator_id": "ODG3618_1_dimension_five",
            "operator_class": "dimension-five one-extra-derivative birefringent operator",
            "schematic_action": "Delta S~M_*^-1 int n dot F nabla F or parent-flow equivalent",
            "energy_power_s": 1,
            "screen_effect": "linear-in-energy h_split; same GRB kernel as xi model",
            "gate": "must be generated by parent motion/time/space structure with M_* and no local Lorentz overclaim",
            "status": "PROMISING_NONZERO_ROUTE_NOT_PARENT_SIGNED",
            "source_path": str(sources["energy_3617"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "operator_id": "ODG3618_2_dimension_six",
            "operator_class": "dimension-six two-extra-derivative operator",
            "schematic_action": "Delta S~M_*^-2 int F nabla^2 F or curvature/memory equivalent",
            "energy_power_s": 2,
            "screen_effect": "quadratic-in-energy h_split",
            "gate": "must declare tensor structure; nonbirefringent pieces belong to dispersion/readout not h_split",
            "status": "ALTERNATE_NONZERO_ROUTE_NOT_PARENT_SIGNED",
            "source_path": str(sources["energy_3617"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "operator_id": "ODG3618_3_axion_gradient",
            "operator_class": "pseudoscalar gradient rotation",
            "schematic_action": "theta(Phi) F wedge F with d theta != 0",
            "energy_power_s": "separate",
            "screen_effect": "polarization rotation without ordinary principal Fresnel cone split",
            "gate": "track in axion-gradient rotation ledger, not as B_Fresnel h_split",
            "status": "SEPARATE_GATE_RETAINED",
            "source_path": str(sources["action_domain_3505"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def branch_packet_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "packet_id": "SBP3618_0_local_Hodge_zero_branch",
            "branch": "local observed-Hodge Maxwell branch",
            "required_parent_clauses": "same_metric; observed_Hodge; unique_F2; no_independent_chi_EM; no_HD_screen; constant_or_absent_axion_gradient",
            "derived_h_split": "0",
            "derived_B_Fresnel_MTS": "0",
            "derived_xi_MTS_eff": "0",
            "status": "CONDITIONAL_ZERO_BRANCH_READY_NOT_PARENT_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "packet_id": "SBP3618_1_nonzero_s1_branch",
            "branch": "dimension-five parent-flow/high-frequency branch",
            "required_parent_clauses": "operator tensor; M_*; C_screen; gamma0; B_Fresnel_MTS; local-frame compatibility",
            "derived_h_split": "C_screen B_Fresnel_MTS (k/M_*)",
            "derived_B_Fresnel_MTS": "MISSING_PARENT_AMPLITUDE",
            "derived_xi_MTS_eff": "B_Fresnel_MTS C_screen M_pl/(4 gamma0 M_*)",
            "status": "NONZERO_ROUTE_TYPED_BUT_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "packet_id": "SBP3618_2_s0_bound_branch",
            "branch": "independent two-derivative constitutive anisotropy",
            "required_parent_clauses": "explicit chi_aniso coefficient or theorem ban",
            "derived_h_split": "B_Fresnel_MTS",
            "derived_B_Fresnel_MTS": "MISSING_OR_FORBID",
            "derived_xi_MTS_eff": "B_Fresnel_MTS C_screen M_pl I0/(4 gamma0 k0 I1)",
            "status": "DANGEROUS_BRANCH_SHOULD_BE_FORBIDDEN_OR_BOUND",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def projection_update_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    runner_rows = read_csv(source_map()["runner_3617"][0])
    rows: list[dict[str, object]] = []
    for runner_row in runner_rows:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "update_id": f"KPU3618_{len(rows)}_{runner_row['object'].replace(' ', '')}",
                "object": runner_row["object"],
                "xi_bound": runner_row["xi_bound"],
                "zero_branch_result": "xi_MTS_eff=0 if SBP3618_0 clauses are parent-signed",
                "nonzero_s1_result": "xi_MTS_eff <= B_Fresnel_MTS C_screen M_pl/(4 gamma0 M_*)",
                "nonzero_s0_warning": "xi_MTS_eff <= B_Fresnel_MTS C_screen M_pl I0/(4 gamma0 k0 I1)",
                "result": "TWO_BRANCH_GATE_READY_NOT_SCORED",
                "can_score": False,
                "claim_allowed": False,
                "valid_for_claim": False,
            }
        )
    return rows


def decision_gate_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3618_0_zero_route",
            "decision": "The clean local-GR route is to parent-sign observed Hodge/same-metric/unique-F2 and thereby force h_split=0.",
            "status": "BEST_ROUTE_IDENTIFIED_NOT_CLOSED",
            "next_action": "prove action-domain exhaustion forbids independent chi_EM and higher-derivative screen terms",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3618_1_nonzero_route",
            "decision": "If a nonzero branch survives, it must be typed by operator dimension; s=1 is allowed only if derived from a dimension-five parent-flow/high-frequency term.",
            "status": "NONZERO_ROUTE_TYPED_NOT_VALUES",
            "next_action": "source or derive M_*, C_screen, gamma0 and B_Fresnel_MTS",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3618_2_s0_warning",
            "decision": "A two-derivative non-Hodge constitutive anisotropy is the dangerous branch and should be theorem-banned if the local GR reduction is to be competitive.",
            "status": "DANGEROUS_BRANCH_EXPLICIT",
            "next_action": "attack no-independent-chi_EM theorem before trying to fit coefficients",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3618_3_next_target",
            "decision": "3619 should attempt visible EM action-domain exhaustion: no independent chi_EM, no hidden Hodge, no higher-derivative screen term in the local branch.",
            "status": "NEXT_TARGET_SELECTED",
            "next_action": "3619-Y5-R2FR-visible-EM-action-domain-exhaustion-or-screen-coefficient-row.md",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status_id": "STATUS3618_0",
            "result": "SCREEN_ZERO_ROUTE_DERIVED_NONZERO_BRANCH_TYPED",
            "summary": "3618 proves the conditional local Hodge/same-metric branch has h_split=0 and turns every nonzero alternative into an explicit operator-dimension branch; no GRB/local claim is made until parent action-domain exhaustion or coefficient rows exist.",
            "zero_route_derived": True,
            "nonzero_operator_dimension_gate": True,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3618_0",
            "target_doc": "3619-Y5-R2FR-visible-EM-action-domain-exhaustion-or-screen-coefficient-row.md",
            "target_script": "scripts/Y5_R2FR_3619_visible_EM_action_domain_exhaustion_or_screen_coefficient_row.py",
            "objective": "prove that the local visible EM action admits only the observed-Hodge Maxwell principal term, with no independent chi_EM, hidden Hodge map, readout-after-variation or higher-derivative screen operator; if not, produce the first nonzero screen coefficient row",
            "success_gate": "either the h_split=0 branch becomes parent-signed for local EM/GR, or a nonzero h_AB coefficient row declares operator class, s, M_*, gamma0, C_screen and B_Fresnel_MTS source path",
            "reason": "3618 reduced the problem to action-domain exhaustion versus an explicit typed coefficient.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def canonical_status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "screen_zero_route": "DERIVED_CONDITIONAL",
            "nonzero_route": "OPERATOR_DIMENSION_TYPED",
            "dangerous_branch": "two_derivative_nonHodge_s0",
            "preferred_next": "visible EM action-domain exhaustion",
            "claim_status": "NO_CLAIM",
            "valid_for_claim": False,
        }
    ]


def write_markdown() -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 3618 Y5 R2FR: screen operator parent origin or energy-scaling gate",
                "",
                "## Verdict",
                "- The local Maxwell/GR route now has a clean conditional zero: observed-Hodge Maxwell descent gives `h_split=0`.",
                "- That means the GRB birefringence pressure does **not** hit the local branch if the parent action really forbids independent `chi_EM` and higher-derivative screen terms.",
                "- If a nonzero branch survives, it must appear as an explicit operator-dimension row, not as vague coupling fog.",
                "",
                "## Conditional zero theorem",
                "- Define `h_split = h_AB - (1/2) tr(h) delta_AB`.",
                "- Scalar impedance, conformal scale, and common Maxwell normalization are proportional to identity on the two-polarization screen.",
                "- Therefore `diam_spec(h)=0` for the ordinary observed-Hodge Maxwell branch.",
                "- Contract:",
                "- `same_metric && observed_Hodge && unique_F2 && no_chi_EM && no_HD_screen && constant_or_absent_axion_gradient => h_split=0`.",
                "",
                "## Nonzero branches",
                "- Two-derivative independent `chi_EM` gives `s=0`; this is the dangerous branch and should be theorem-banned if possible.",
                "- Dimension-five parent-flow/high-frequency terms give `s=1`; this is the GRB-compatible nonzero route but needs `M_*`, `C_screen`, `gamma0`, and amplitude.",
                "- Dimension-six terms give `s=2`; less constrained at keV but still needs parent operator structure.",
                "- Axion-gradient rotation is kept separate from `B_Fresnel h_split`.",
                "",
                "## Practical meaning",
                "- Best next route is not fitting a coefficient.",
                "- Best next route is proving the local visible EM action domain only allows the observed-Hodge Maxwell principal term.",
                "- If that fails, the first nonzero screen coefficient row must be typed and sourced.",
                "",
                "## Next target",
                "- `3619-Y5-R2FR-visible-EM-action-domain-exhaustion-or-screen-coefficient-row.md`.",
                "- Aim: prove no independent `chi_EM`, hidden Hodge, readout-after-variation, or higher-derivative screen operator in the local branch.",
                "",
                "## Claim status",
                "- `NO_CLAIM`: zero route is conditional, nonzero route is typed but unvalued.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def validate() -> list[dict[str, object]]:
    timestamp = utc_now()
    paths = output_paths()
    results: list[tuple[str, bool, str]] = []

    sources = source_map()
    sources_exist = all(source_path.exists() for source_path, _needle in sources.values())
    needles_found = all(source_path.exists() and contains(source_path, needle) for source_path, needle in sources.values())
    results.append(("VAL3618_0_sources_exist", sources_exist, "all required 3618 source paths exist"))
    results.append(("VAL3618_1_needles_found", needles_found, "all selected 3618 source anchors found"))

    pre_validation_paths = [path for name, path in paths.items() if name != "validation"]
    outputs_exist = DOC.exists() and all(path.exists() for path in pre_validation_paths)
    results.append(("VAL3618_2_outputs_exist", outputs_exist, "all pre-validation 3618 outputs written"))

    parse_details: list[str] = []
    csv_parse_pass = True
    for name, path in paths.items():
        if name == "validation":
            continue
        try:
            parse_details.append(f"{name}:{len(read_csv(path))}")
        except Exception as exception:
            csv_parse_pass = False
            parse_details.append(f"{name}:ERROR:{exception}")
    results.append(("VAL3618_3_csv_parse", csv_parse_pass, "; ".join(parse_details)))

    zero_rows = read_csv(paths["screen_zero_theorem"]) if paths["screen_zero_theorem"].exists() else []
    hsplit_zero_written = any("h_split=0" in row["result"] for row in zero_rows)
    parent_contract_written = any("same_metric" in row["formula"] and "no_chi_EM" in row["formula"] for row in zero_rows)
    surviving_sources_written = any("SURVIVING_OPERATOR_LIST_DERIVED" == row["status"] for row in zero_rows)
    results.append(("VAL3618_4_hsplit_zero_written", hsplit_zero_written, "h_split zero theorem written"))
    results.append(("VAL3618_5_parent_contract_written", parent_contract_written, "parent zero contract written"))
    results.append(("VAL3618_6_surviving_sources_written", surviving_sources_written, "surviving nonzero sources listed"))

    operator_rows = read_csv(paths["operator_dimension_gate"]) if paths["operator_dimension_gate"].exists() else []
    has_s0 = any(str(row["energy_power_s"]) == "0" for row in operator_rows)
    has_s1 = any(str(row["energy_power_s"]) == "1" for row in operator_rows)
    has_s2 = any(str(row["energy_power_s"]) == "2" for row in operator_rows)
    results.append(("VAL3618_7_operator_dimensions_typed", has_s0 and has_s1 and has_s2, "s=0, s=1 and s=2 branches typed"))

    branch_rows = read_csv(paths["branch_packet"]) if paths["branch_packet"].exists() else []
    zero_packet = any(row["derived_xi_MTS_eff"] == "0" for row in branch_rows)
    nonzero_packet = any("MISSING_PARENT_AMPLITUDE" in row["derived_B_Fresnel_MTS"] for row in branch_rows)
    results.append(("VAL3618_8_branch_packets_ready", zero_packet and nonzero_packet, "zero and nonzero branch packets written"))

    all_outputs_nonclaim = True
    for name, path in paths.items():
        if name == "validation" or not path.exists():
            continue
        for row in read_csv(path):
            if row.get("valid_for_claim") == "True" or row.get("claim_allowed") == "True":
                all_outputs_nonclaim = False
    results.append(("VAL3618_9_all_outputs_nonclaim", all_outputs_nonclaim, "all generated rows remain nonclaim"))

    formalization_clean = True
    formalization_detail = "formalization-workbench not found"
    if FORMALIZATION.exists():
        leaked_paths = list(FORMALIZATION.rglob("*3618*"))
        formalization_clean = len(leaked_paths) == 0
        formalization_detail = "no 3618 files in formalization-workbench" if formalization_clean else "; ".join(str(path) for path in leaked_paths[:5])
    results.append(("VAL3618_10_no_formalization_leak", formalization_clean, formalization_detail))

    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "validation_id": validation_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for validation_id, passed, detail in results
    ]


def main() -> None:
    paths = output_paths()
    write_csv(paths["source_register"], source_register_rows())
    write_csv(paths["screen_zero_theorem"], screen_zero_theorem_rows())
    write_csv(paths["operator_dimension_gate"], operator_dimension_gate_rows())
    write_csv(paths["branch_packet"], branch_packet_rows())
    write_csv(paths["projection_update"], projection_update_rows())
    write_csv(paths["decision_gates"], decision_gate_rows())
    write_csv(paths["status"], status_rows())
    write_csv(paths["next_target"], next_target_rows())
    write_csv(paths["canonical_status"], canonical_status_rows())
    write_markdown()
    write_csv(paths["validation"], validate())

    failed = [row for row in read_csv(paths["validation"]) if row["result"] != "PASS"]
    if failed:
        raise SystemExit(f"3618 validation failed: {failed}")
    print(f"wrote 3618 checkpoint with {len(read_csv(paths['validation']))} validation checks")


if __name__ == "__main__":
    main()
