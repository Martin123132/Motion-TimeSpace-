from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

STATUS = "Y5_R10_898_trace_vertical_generator_and_matter_descent_signature_not_signed_residual_vector_staged_nonclaim"
CLAIM_CEILING = "trace_vertical_generator_matter_descent_gate_only_no_Jtr_zero_no_residual_bounds_no_R10_PPN_or_local_GR_claim"
NEXT_TARGET = "899-Y5-R10-trace-residual-vector-source-pack-and-local-bound-interface.md"

VERTICAL_GENERATOR_FORMULA = "ell_tr=DQ_trace, v_tr=K_parent^{-1}ell_tr/<ell_tr,K_parent^{-1}ell_tr>, P_tr=v_tr otimes ell_tr"
MATTER_DESCENT_FORMULA = "S_matter[Phi,Psi]=Sbar_matter[q_loc(Phi),Psi,theta] with Lie_vtr theta=0 and Dq_loc[v_tr]=0"

SOURCE_SPECS = [
    {
        "source_id": "897_doc",
        "path": ROOT / "897-Y5-R10-coupling-origin-source-cokernel-and-double-zero-hunt.md",
        "needle": "residual vector instead of hiding the coupling",
        "role": "immediate vertical-generator/residual-vector handoff",
    },
    {
        "source_id": "897_validation",
        "path": OUT / "P8_Y5_BRR545_897_VALIDATION.csv",
        "needle": "V897_13_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "897_residual_vector",
        "path": OUT / "P8_Y5_R10_897_RESIDUAL_VECTOR_FALLBACK.csv",
        "needle": "RV897_0_Qtr_over_m",
        "role": "trace residual vector fallback rows",
    },
    {
        "source_id": "879_covector_pairing",
        "path": ROOT / "879-Y5-R10-parent-trace-covector-and-pairing-source-or-closure.md",
        "needle": "`P_tr` is demoted to closure-only",
        "role": "ell_tr/K_parent/P_tr source audit",
    },
    {
        "source_id": "878_projector",
        "path": ROOT / "878-Y5-R10-Ptr-parent-projector-definition-and-constraint-rank-test.md",
        "needle": "A real trace projector requires a parent trace covector",
        "role": "formal P_tr/v_tr projector construction",
    },
    {
        "source_id": "874_verticality",
        "path": ROOT / "874-Y5-R10-parent-qloc-verticality-signature-or-cT-coefficient-fill.md",
        "needle": "Dq_loc[U][v_T]=0",
        "role": "q_loc verticality proof shape and failure mode",
    },
    {
        "source_id": "873_trace_charge",
        "path": ROOT / "873-Y5-R10-local-matter-trace-charge-zero-theorem-or-coefficient-fill.md",
        "needle": "chain-rule zero theorem",
        "role": "conditional local matter trace-charge zero theorem",
    },
    {
        "source_id": "886_zero_pole",
        "path": ROOT / "886-Y5-R10-Htr-zero-pole-rank-test-and-Jtr-source-cokernel-gate.md",
        "needle": "Zero-Pole Implication Theorem",
        "role": "rank-zero/no-pole/source-cokernel conditional theorem",
    },
    {
        "source_id": "410_functor",
        "path": ROOT / "410-quotient-matter-functor-theorem-attempt.md",
        "needle": "Conditional Functor Theorem",
        "role": "quotient matter functor conditional proof and counterexamples",
    },
    {
        "source_id": "626_matter_signature",
        "path": ROOT / "626-Y5-R10-quotient-invariant-matter-action-signature-or-cg-bound-input.md",
        "needle": "S_matter[Phi,Psi] = Sbar_matter[q(Phi),Psi,theta]",
        "role": "quotient-invariant matter action descent criterion",
    },
    {
        "source_id": "762_geometry_stack",
        "path": ROOT / "762-Y5-R10-geometry-stack-descent-or-coupling-source-fill.md",
        "needle": "Geometry-Stack Descent Contract",
        "role": "matter measure/coframe/connection/derivative descent gate",
    },
    {
        "source_id": "763_no_marker",
        "path": ROOT / "763-Y5-R10-no-marker-spurion-theorem-or-coupling-source-fill.md",
        "needle": "no-marker/no-spurion theorem",
        "role": "marker/spurion/constant classification gate",
    },
    {
        "source_id": "767_matter_functor",
        "path": ROOT / "767-Y5-R10-parent-matter-functor-no-alpha-vertex-or-WEP-closure.md",
        "needle": "WEP safety remains an explicit quarantined closure",
        "role": "matter functor/WEP closure quarantine",
    },
    {
        "source_id": "338_readout_gate",
        "path": ROOT / "338-action-level-exact-readout-gate.md",
        "needle": "source-at-zero != physical spurion",
        "role": "readout-after-variation no-spurion rule",
    },
]


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def stringify(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return "" if value is None else str(value)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: stringify(row.get(field, "")) for field in fields})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def has_needle(path: Path, needle: str) -> bool:
    return path.exists() and needle in read_text(path)


def md_table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return "_No rows._"
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        values = [stringify(row.get(field, "")).replace("\n", " ").replace("|", "/") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_register_rows(generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in SOURCE_SPECS:
        path = Path(spec["path"])
        rows.append(
            {
                "source_id": spec["source_id"],
                "path": path,
                "exists": path.exists(),
                "needle_check": "pass" if has_needle(path, str(spec["needle"])) else "fail",
                "role": spec["role"],
                "valid_for_claim": False,
                "generated_utc": generated_utc,
            }
        )
    return rows


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "audited the actual trace vertical generator and matter descent signatures required to turn coupling silence into a theorem",
            "best_partial_result": "the exact proof stack is now explicit: parent-owned ell_tr/K_parent/v_tr, Dq_loc[v_tr]=0 or rank-zero, full matter geometry-stack descent, no-marker constants, and no boundary tail",
            "hard_blockers": "Q_trace/Q_star and K_parent remain missing, P_tr is closure-only, q_loc verticality is conditional, matter stack descent is unsigned, no-marker/no-alpha clauses are not parent-signed",
            "what_is_not_claimed": "v_tr is a parent vertical generator, J_tr=0, Q_tr^A=0, C_tr double-zero, residual vector bounds, R10/PPN/clock/WEP/orbital pass, local GR/Newton derivation",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def vertical_generator_signature_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "signature_id": "VGS898_0_Qtrace_covector",
            "object": "ell_tr=DQ_trace",
            "required_signature": "Q_trace and Q_* are parent-owned readouts/coordinates with fixed normalization before local testing",
            "current_status": "MISSING_QTRACE_QSTAR_PARENT_OWNERSHIP",
            "evidence": "879 audits ell_tr as formal only; Q_* and endpoint coordinate covectors are missing",
            "if_signed": "trace covector exists as a real parent object",
            "if_failed": "P_tr remains closure-only and residual vector branch is mandatory",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "signature_id": "VGS898_1_Kparent_pairing",
            "object": "K_parent or constrained pseudo-inverse",
            "required_signature": "parent action supplies a charge/kinetic/Hessian/symplectic pairing that raises ell_tr into v_tr",
            "current_status": "MISSING_KPARENT_PAIRING",
            "evidence": "879 finds relative charge metric, endpoint potential, symplectic map, and Hessian routes non-computable for trace",
            "if_signed": "v_tr normalization can be tested rather than chosen",
            "if_failed": "no parent vertical generator exists",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "signature_id": "VGS898_2_vtr_definition",
            "object": "v_tr",
            "required_signature": VERTICAL_GENERATOR_FORMULA,
            "current_status": "BLOCKED_BY_ELLTR_AND_KPARENT",
            "evidence": "878/879 provide the formal formula but not parent inputs",
            "if_signed": "Dq_loc[v_tr] and source-cokernel pairing become evaluable",
            "if_failed": "trace coupling cannot be theorem-zeroed",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "signature_id": "VGS898_3_local_verticality",
            "object": "Dq_loc[U][v_tr]=0",
            "required_signature": "q_loc is a compact local restriction/jet quotient and v_tr has no local support or is gauge/exact-zero",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "evidence": "874 proves the restriction lemma only if q_loc and support/no-tail are parent-owned",
            "if_signed": "matter chain-rule zero can apply to ordinary local domains",
            "if_failed": "Q_tr/m rows must be filled or bounded",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "signature_id": "VGS898_4_rank_zero_no_pole",
            "object": "rank(P_loc P_tr P_loc^dagger)=0",
            "required_signature": "P_tr is parent-owned and has zero compact-local image, or H_tr has no source-coupled local pole",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "evidence": "886 gives a valid implication theorem but missing parent signatures",
            "if_signed": "lambda_tr is absent locally and J_tr source-cokernel can vanish",
            "if_failed": "Z_tr/mu_tr/lambda_tr source rows become mandatory",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "signature_id": "VGS898_5_readout_no_spurion",
            "object": "trace readout status",
            "required_signature": "P_tr enters only as post-variation/source-at-zero readout, not as a physical spurion in S_parent",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED_FOR_TRACE",
            "evidence": "338 gives the source-at-zero rule; 878/879 do not sign it for trace endpoint",
            "if_signed": "readout itself cannot generate local force",
            "if_failed": "physical trace spurion/coupling must be retained",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "signature_id": "VGS898_6_verdict",
            "object": "trace vertical generator",
            "required_signature": "VGS898_0 through VGS898_5 jointly signed",
            "current_status": "not_signed",
            "evidence": "current corpus has a formal generator contract but no parent-owned vertical generator",
            "if_signed": "move to source-cokernel theorem promotion attempt",
            "if_failed": "stage residual vector source pack",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def matter_descent_signature_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "descent_id": "MDS898_0_parent_matter_functor",
            "object": "S_matter factorization",
            "required_signature": MATTER_DESCENT_FORMULA,
            "current_status": "SUFFICIENT_AXIOM_NOT_PARENT_DERIVED",
            "evidence": "410/626 give the conditional descent criterion but not the parent matter action",
            "if_signed": "fixed-Phi vertical matter derivative can vanish by chain rule",
            "if_failed": "representative geometry coupling remains legal",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "descent_id": "MDS898_1_geometry_stack",
            "object": "mu_m,e_m,g_m,omega_m,D_m",
            "required_signature": "matter measure, coframe/metric, connection, and derivative operator all factor through q_loc or owned gauge/exact data",
            "current_status": "GEOMETRY_STACK_DESCENT_NOT_PARENT_SIGNED",
            "evidence": "762 keeps each stack layer unsigned with counterexamples",
            "if_signed": "c_g-like frame leakage and derivative re-entry are theorem-zero",
            "if_failed": "c_g/disformal/connection residuals stay active",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "descent_id": "MDS898_2_no_marker_constants",
            "object": "theta_A, alpha_EM, charges, mass ratios, clock/binding responses",
            "required_signature": "all ordinary constants are quotient-only/superselection data or retained as residuals",
            "current_status": "NO_MARKER_THEOREM_NOT_PARENT_SIGNED",
            "evidence": "763/767 keep alpha/mass/charge and species constants quarantined as closure/residuals",
            "if_signed": "WEP/clock/species trace charges can vanish structurally",
            "if_failed": "clock/species residual vector rows become mandatory",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "descent_id": "MDS898_3_universal_source_current",
            "object": "Hilbert/coframe source current",
            "required_signature": "all ordinary species source one universal stress/current with one kappa and Ward-safe selector stress",
            "current_status": "UNIVERSAL_SOURCE_NOT_PARENT_SIGNED",
            "evidence": "763/767 retain source weights and selector Ward identity as debts",
            "if_signed": "measured-GM/source-normalization split is less likely to hide a fifth force",
            "if_failed": "source-normalization residual rows must be sourced",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "descent_id": "MDS898_4_boundary_EFT_no_extension",
            "object": "boundary/readout EFT extensions",
            "required_signature": "vertical variation has no local boundary projection and no post-readout EFT term is counted as parent theorem",
            "current_status": "BOUNDARY_AND_EFT_SILENCE_NOT_SIGNED",
            "evidence": "338 permits source-at-zero readout but counterterms return if made physical; 763 keeps post-readout EFT residual",
            "if_signed": "zero theorem is stable under readout and local integration",
            "if_failed": "boundary/EFT residual vector rows remain active",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "descent_id": "MDS898_5_verdict",
            "object": "matter descent source-cokernel",
            "required_signature": "MDS898_0 through MDS898_4 jointly signed",
            "current_status": "not_signed",
            "evidence": "descent theorem is clean but current parent matter branch remains closure/quarantine",
            "if_signed": "Q_tr^A=0 and J_tr=0 become promotable theorem targets",
            "if_failed": "trace residual vector must be carried explicitly",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def source_cokernel_pairing_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "pairing_id": "SCP898_0_trace_charge_zero",
            "target": "Q_tr^A=partial_{v_tr}m_A or partial_{v_tr}S_A",
            "proof_shape": "chain rule gives zero if Dq_loc[v_tr]=0 and theta_A has no trace marker",
            "current_status": "conditional_valid_not_signed",
            "missing": "v_tr parent ownership, q_loc verticality, matter stack descent, no-marker constants",
            "fallback_quantity": "Q_tr^A/m_A",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "pairing_id": "SCP898_1_Jtr_cokernel",
            "target": "J_tr=P_tr^dagger J_parent",
            "proof_shape": "rank-zero/no local trace image or source-cokernel pairing makes <u_tr,J_parent>=0",
            "current_status": "conditional_valid_not_signed",
            "missing": "P_tr/H_tr physical mode domain and boundary no-tail",
            "fallback_quantity": "J_tr source projection",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "pairing_id": "SCP898_2_alpha_tr",
            "target": "alpha_tr(lambda_tr)",
            "proof_shape": "alpha_tr=0 if Q_tr^A=0 or no source-coupled pole; otherwise alpha depends on Q_tr, Z_tr, lambda_tr, and source normalization",
            "current_status": "not_executable",
            "missing": "zero theorem or numeric/sourced residual vector",
            "fallback_quantity": "alpha_tr(lambda_tr)",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "pairing_id": "SCP898_3_metric_leakage",
            "target": "C_tr metric/source response",
            "proof_shape": "double-zero C_tr kills first-order PPN/source-normalization leakage; otherwise response operator is required",
            "current_status": "conditional_valid_not_signed",
            "missing": "trace double-zero parent origin and weak-field response",
            "fallback_quantity": "C_tr_gamma,C_tr_beta,C_tr_source,C_tr_clock",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "pairing_id": "SCP898_4_verdict",
            "target": "trace coupling source-cokernel",
            "proof_shape": "vertical generator + matter descent + no-pole/no-tail + double-zero",
            "current_status": "not_promoted",
            "missing": "all parent signatures remain unsigned",
            "fallback_quantity": "full trace residual vector",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def residual_vector_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "residual_id": "TRV898_0_Ztr",
            "quantity": "Z_tr",
            "definition": "principal-symbol normalization of local trace Hessian H_tr",
            "needed_for": "R10/orbital/PPN amplitude if finite trace carrier survives",
            "current_value": "MISSING_PARENT_HESSIAN_OR_NOPOLE",
            "units": "model_dependent",
            "arena": "R10;PPN;orbital",
            "source_path": "MISSING_PARENT_SOURCE",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "residual_id": "TRV898_1_lambdatr",
            "quantity": "lambda_tr",
            "definition": "local trace range lambda_tr=1/sqrt(mu_tr^2/Z_tr) or absent by no-pole theorem",
            "needed_for": "finite-range local comparisons",
            "current_value": "MISSING_MASS_GAP_OR_NOPOLE",
            "units": "length",
            "arena": "R10;orbital;PPN",
            "source_path": "MISSING_PARENT_SOURCE",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "residual_id": "TRV898_2_Qtr_universal",
            "quantity": "Q_tr_over_m_universal",
            "definition": "universal trace charge per inertial mass if source-cokernel fails but species differences vanish",
            "needed_for": "R10 common force and orbital/source-normalization audit",
            "current_value": "MISSING_SOURCE_PROJECTION_OR_ZERO_THEOREM",
            "units": "dimensionless_or_parent_charge_per_mass",
            "arena": "R10;orbital;Newton_source",
            "source_path": "MISSING_MATTER_SOURCE",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "residual_id": "TRV898_3_Qtr_species_delta",
            "quantity": "Delta_AB_Q_tr_over_m",
            "definition": "composition/species difference in trace charge per inertial mass",
            "needed_for": "WEP/MICROSCOPE and clock-material tests",
            "current_value": "MISSING_NO_MARKER_OR_SPECIES_FUNCTIONAL",
            "units": "dimensionless",
            "arena": "WEP;clock",
            "source_path": "MISSING_MATTER_SOURCE",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "residual_id": "TRV898_4_Ctr_PPN",
            "quantity": "C_tr_gamma,C_tr_beta,C_tr_alpha_i",
            "definition": "weak-field metric/PPN response to trace leakage",
            "needed_for": "solar-system PPN residual vector",
            "current_value": "MISSING_WEAK_FIELD_RESPONSE_OPERATOR",
            "units": "dimensionless",
            "arena": "PPN",
            "source_path": "MISSING_WEAK_FIELD_SOURCE",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "residual_id": "TRV898_5_clock_EM",
            "quantity": "C_tr_clock_i,C_tr_alphaEM",
            "definition": "clock transition and EM/fine-structure response to trace direction",
            "needed_for": "clock/redshift/EM local tests",
            "current_value": "MISSING_CLOCK_EM_FUNCTIONAL_OR_NO_ALPHA_THEOREM",
            "units": "dimensionless_or_per_time_after_projection",
            "arena": "clock;EM",
            "source_path": "MISSING_MATTER_SOURCE",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "residual_id": "TRV898_6_source_normalization",
            "quantity": "C_tr_source,delta_GM_tr,Gdot_tr",
            "definition": "measured-GM/source-normalization response to trace leakage",
            "needed_for": "Newtonian limit and orbital source normalization",
            "current_value": "MISSING_SOURCE_NORMALIZATION_OPERATOR",
            "units": "dimensionless_or_per_time",
            "arena": "Newton;orbital;Gdot",
            "source_path": "MISSING_SOURCE_NORMALIZATION_SOURCE",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "residual_id": "TRV898_7_boundary_tail",
            "quantity": "B_tr_tail,K_perp_trace",
            "definition": "boundary/exact trace current tail and transverse tensor leakage tied to trace branch",
            "needed_for": "boundary no-tail failure mode",
            "current_value": "MISSING_BOUNDARY_SUPPORT_CERTIFICATE_OR_BOUND",
            "units": "model_dependent",
            "arena": "PPN;orbital;local_GR",
            "source_path": "MISSING_BOUNDARY_SOURCE",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def branch_decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "branch_id": "BD898_0_theorem_zero_route",
            "branch": "parent-signed vertical generator and matter descent",
            "required_to_enter": "VGS898_0..6 and MDS898_0..5 signed",
            "current_status": "not_entered",
            "decision": "not_promoted",
            "next_action": "do not claim J_tr=0 or local GR",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "branch_id": "BD898_1_no_pole_route",
            "branch": "rank-zero/no source-coupled pole",
            "required_to_enter": "parent-owned P_tr plus rank-zero/no-tail/reduced-inverse certificate",
            "current_status": "not_entered",
            "decision": "not_promoted",
            "next_action": "keep no-pole linked but unsigned",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "branch_id": "BD898_2_residual_vector_route",
            "branch": "explicit trace residual vector",
            "required_to_enter": "failure to sign vertical generator/matter descent/no-pole route",
            "current_status": "selected_nonclaim",
            "decision": "stage_source_pack_next",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def promotion_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "PG898_0_vertical_generator",
            "promotion_target": "parent-owned v_tr/P_tr",
            "required_to_pass": "ell_tr, Q_*, endpoint coordinates, K_parent, normalization, and readout/no-spurion status",
            "current_evidence": "formal only; closure-only",
            "gate_result": "fail_for_claim",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG898_1_matter_descent",
            "promotion_target": "S_matter descends through q_loc for trace vertical direction",
            "required_to_pass": "parent matter functor, geometry stack descent, no-marker constants, universal source current, no boundary/EFT tail",
            "current_evidence": "conditional descent criterion only",
            "gate_result": "fail_for_claim",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG898_2_Jtr_zero",
            "promotion_target": "J_tr source-cokernel zero",
            "required_to_pass": "vertical generator + matter descent + no-pole/source-cokernel pairing",
            "current_evidence": "not signed",
            "gate_result": "fail_for_claim",
            "next_action": "use residual vector source pack",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG898_3_residual_vector_executable",
            "promotion_target": "trace residual vector ready for bounds",
            "required_to_pass": "all residual rows have numeric/theorem-zero source-backed values and units",
            "current_evidence": "schema staged with MISSING markers",
            "gate_result": "fail_for_claim",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG898_4_local_GR",
            "promotion_target": "local GR/Newton reduction",
            "required_to_pass": "trace residual zero/bounded plus other local-GR spine gates",
            "current_evidence": "trace coupling unresolved",
            "gate_result": "fail_for_claim",
            "next_action": "keep local-GR gate blocked",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def route_choice_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC898_0_selected",
            "route": "trace_residual_vector_source_pack_and_local_bound_interface",
            "status": "selected",
            "reason": "the vertical-generator and matter-descent signatures remain unsigned; theorem-zero cannot be promoted, so the honest route is an explicit trace residual vector source pack",
            "include": "Z_tr, lambda_tr, Q_tr/m, species delta, PPN response, clock/EM response, source-normalization, boundary tail, source paths and units",
            "exclude": "claiming J_tr=0, claiming local GR, fitted tiny coupling, endpoint transfer, public prose, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG898_0_no_vtr_claim",
            "forbidden_claim": "v_tr/P_tr is parent-owned",
            "status": "forbidden",
            "reason": "ell_tr/Q_*/K_parent are missing and P_tr remains closure-only",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG898_1_no_matter_descent_claim",
            "forbidden_claim": "ordinary matter descends through q_loc for trace direction",
            "status": "forbidden",
            "reason": "matter functor, geometry stack, no-marker constants, and boundary/EFT clauses are unsigned",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG898_2_no_Jtr_zero_claim",
            "forbidden_claim": "J_tr=0 or Q_tr^A=0",
            "status": "forbidden",
            "reason": "source-cokernel proof stack is not parent-signed",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG898_3_no_residual_bound_claim",
            "forbidden_claim": "trace residual vector is bounded or passes local tests",
            "status": "forbidden",
            "reason": "residual vector rows are schema-only and contain MISSING markers",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG898_4_no_local_GR_claim",
            "forbidden_claim": "local GR/Newton follows",
            "status": "forbidden",
            "reason": "trace coupling and broader local-GR gates remain open",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG898_5_allowed_private_result",
            "forbidden_claim": "none",
            "status": "allowed_private_nonclaim",
            "reason": "898 forces the trace coupling branch into either theorem signatures or explicit residual rows",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D898_0",
            "finding": "vertical_generator_not_signed",
            "reason": "current corpus lacks parent-owned ell_tr/Q_*/K_parent and therefore cannot define v_tr/P_tr for claim",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D898_1",
            "finding": "matter_descent_not_signed",
            "reason": "conditional chain-rule theorem lacks parent matter functor, geometry stack, no-marker constants, and boundary/EFT closure",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D898_2",
            "finding": "trace_residual_vector_staged",
            "reason": "theorem-zero route cannot promote; explicit residual rows are required for future local bounds",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "turn the staged trace residual vector into a source-pack/local-bound interface: validate schemas, keep missing rows nonclaim, and identify which residuals can be theorem-zeroed versus sourced later",
            "include": "Z_tr, lambda_tr, Q_tr/m, PPN vector, clock/EM response, source-normalization, boundary tail, units/provenance, local-bound mapping",
            "exclude": "claim scoring with MISSING inputs, free fitted coupling, public local-GR claim, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def prior_897_clean() -> bool:
    path = OUT / "P8_Y5_BRR545_897_VALIDATION.csv"
    return path.exists() and all(row.get("result") == "pass" for row in read_csv(path))


def formalization_changed_count() -> int:
    if not FORMALIZATION.exists():
        return -1
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime)
            if modified > CUTOFF:
                count += 1
    return count


def all_nonclaim(row_groups: list[list[dict[str, object]]]) -> bool:
    for rows in row_groups:
        for row in rows:
            if stringify(row.get("valid_for_claim", False)).lower() != "false":
                return False
    return True


def validation_rows(
    generated_utc: str,
    source_rows_: list[dict[str, object]],
    summary_rows_: list[dict[str, object]],
    vertical_rows_: list[dict[str, object]],
    matter_rows_: list[dict[str, object]],
    pairing_rows_: list[dict[str, object]],
    residual_rows_: list[dict[str, object]],
    branch_rows_: list[dict[str, object]],
    promotion_rows_: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    formalization_count = formalization_changed_count()
    row_groups = [
        source_rows_,
        summary_rows_,
        vertical_rows_,
        matter_rows_,
        pairing_rows_,
        residual_rows_,
        branch_rows_,
        promotion_rows_,
        route_rows_,
        claim_rows_,
        decision_rows_,
        next_rows_,
    ]
    checks = [
        {
            "check_id": "V898_0_sources_exist_and_needles",
            "result": "pass" if all(row["exists"] and row["needle_check"] == "pass" for row in source_rows_) else "fail",
            "detail": "all source paths exist and needles are present",
        },
        {
            "check_id": "V898_1_prior_897_clean",
            "result": "pass" if prior_897_clean() else "fail",
            "detail": "P8_Y5_BRR545_897_VALIDATION.csv clean",
        },
        {
            "check_id": "V898_2_vertical_generator_not_signed",
            "result": "pass"
            if any(row["signature_id"] == "VGS898_6_verdict" and row["current_status"] == "not_signed" for row in vertical_rows_)
            else "fail",
            "detail": "trace vertical generator remains unsigned",
        },
        {
            "check_id": "V898_3_matter_descent_not_signed",
            "result": "pass"
            if any(row["descent_id"] == "MDS898_5_verdict" and row["current_status"] == "not_signed" for row in matter_rows_)
            else "fail",
            "detail": "matter descent remains unsigned",
        },
        {
            "check_id": "V898_4_source_cokernel_not_promoted",
            "result": "pass"
            if any(row["pairing_id"] == "SCP898_4_verdict" and row["current_status"] == "not_promoted" for row in pairing_rows_)
            else "fail",
            "detail": "source-cokernel not promoted",
        },
        {
            "check_id": "V898_5_residual_vector_staged_missing",
            "result": "pass"
            if len(residual_rows_) == 8 and all("MISSING" in str(row["current_value"]) and not bool(row["valid_for_claim"]) for row in residual_rows_)
            else "fail",
            "detail": "trace residual vector rows staged with missing markers",
        },
        {
            "check_id": "V898_6_residual_route_selected",
            "result": "pass"
            if any(row["branch_id"] == "BD898_2_residual_vector_route" and row["current_status"] == "selected_nonclaim" for row in branch_rows_)
            else "fail",
            "detail": "residual vector route selected as nonclaim",
        },
        {
            "check_id": "V898_7_promotion_gates_blocked",
            "result": "pass" if all(row["gate_result"] == "fail_for_claim" for row in promotion_rows_) else "fail",
            "detail": "all promotion gates fail for claim",
        },
        {
            "check_id": "V898_8_claim_allowed_false",
            "result": "pass" if all(not bool(row["claim_allowed"]) for row in decision_rows_) else "fail",
            "detail": "decision rows keep claim_allowed=false",
        },
        {
            "check_id": "V898_9_all_rows_nonclaim",
            "result": "pass" if all_nonclaim(row_groups) else "fail",
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "V898_10_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V898_11_route_selected",
            "result": "pass" if next_rows_ and next_rows_[0]["next_target"] == NEXT_TARGET else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V898_12_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        },
    ]
    for row in checks:
        row["generated_utc"] = generated_utc
    return checks


def write_markdown(
    path: Path,
    generated_utc: str,
    source_rows_: list[dict[str, object]],
    summary_rows_: list[dict[str, object]],
    vertical_rows_: list[dict[str, object]],
    matter_rows_: list[dict[str, object]],
    pairing_rows_: list[dict[str, object]],
    residual_rows_: list[dict[str, object]],
    branch_rows_: list[dict[str, object]],
    promotion_rows_: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    content = f"""# 898 - Y5/R10 Trace Vertical Generator, Matter Descent Signature, Or Residual Vector

Status: `{STATUS}`
Claim ceiling: `{CLAIM_CEILING}`
Generated UTC: `{generated_utc}`

Current result: **the trace theorem-zero route is still not parent-signed, so the residual vector is now staged explicitly**. The required proof stack is:

`{VERTICAL_GENERATOR_FORMULA}`

plus:

`{MATTER_DESCENT_FORMULA}`

The corpus has formal/conditional versions of these clauses, but not parent-owned versions. Therefore `J_tr=0`, `Q_tr^A=0`, and local trace silence are not claimed. The honest next move is to treat trace leakage as a residual vector with named quantities, units, arenas, and missing-source blockers.

## Exact 898 Finding
This is the coupling bottleneck in its sharpest current form. A GR-safe trace branch needs a real parent vertical generator and a real matter descent theorem. We have neither yet. That does not kill the programme; it prevents a fake GR reduction. The trace channel is now forced into one of two honest futures: parent-sign the vertical/descent stack later, or source/bound the residual vector against R10, PPN, WEP, clocks, EM, orbital systems, and Newtonian source normalization.

## Nonclaim Summary
{md_table(summary_rows_)}

## Source Register
{md_table(source_rows_)}

## Trace Vertical Generator Signature
{md_table(vertical_rows_)}

## Matter Descent Signature
{md_table(matter_rows_)}

## Source-Cokernel Pairing
{md_table(pairing_rows_)}

## Trace Residual Vector
{md_table(residual_rows_)}

## Branch Decision
{md_table(branch_rows_)}

## Promotion Gate
{md_table(promotion_rows_)}

## Route Choice
{md_table(route_rows_)}

## Claim Guard
{md_table(claim_rows_)}

## Decision
{md_table(decision_rows_)}

## Next Target
{md_table(next_rows_)}

## Validation
{md_table(validation_rows_)}
"""
    path.write_text(content, encoding="utf-8")


def main() -> None:
    generated_utc = now_utc()
    source_rows_ = source_register_rows(generated_utc)
    summary_rows_ = nonclaim_summary_rows(generated_utc)
    vertical_rows_ = vertical_generator_signature_rows(generated_utc)
    matter_rows_ = matter_descent_signature_rows(generated_utc)
    pairing_rows_ = source_cokernel_pairing_rows(generated_utc)
    residual_rows_ = residual_vector_rows(generated_utc)
    branch_rows_ = branch_decision_rows(generated_utc)
    promotion_rows_ = promotion_gate_rows(generated_utc)
    route_rows_ = route_choice_rows(generated_utc)
    claim_rows_ = claim_guard_rows(generated_utc)
    decision_rows_ = decision_rows(generated_utc)
    next_rows_ = next_target_rows(generated_utc)
    validation_rows_ = validation_rows(
        generated_utc,
        source_rows_,
        summary_rows_,
        vertical_rows_,
        matter_rows_,
        pairing_rows_,
        residual_rows_,
        branch_rows_,
        promotion_rows_,
        route_rows_,
        claim_rows_,
        decision_rows_,
        next_rows_,
    )

    outputs = {
        "P8_Y5_R10_898_SOURCE_REGISTER.csv": source_rows_,
        "P8_Y5_R10_898_TRACE_VERTICAL_GENERATOR_SIGNATURE.csv": vertical_rows_,
        "P8_Y5_R10_898_MATTER_DESCENT_SIGNATURE.csv": matter_rows_,
        "P8_Y5_R10_898_SOURCE_COKERNEL_PAIRING.csv": pairing_rows_,
        "P8_Y5_R10_898_TRACE_RESIDUAL_VECTOR.csv": residual_rows_,
        "P8_Y5_R10_898_BRANCH_DECISION.csv": branch_rows_,
        "P8_Y5_R10_898_PROMOTION_GATE.csv": promotion_rows_,
        "P8_Y5_R10_898_ROUTE_CHOICE.csv": route_rows_,
        "P8_Y5_R10_898_CLAIM_GUARD.csv": claim_rows_,
        "P8_Y5_R10_898_DECISION.csv": decision_rows_,
        "P8_Y5_R10_898_NEXT_TARGET.csv": next_rows_,
        "P8_Y5_R10_898_NONCLAIM_SUMMARY.csv": summary_rows_,
        "P8_Y5_BRR545_898_VALIDATION.csv": validation_rows_,
    }
    for filename, rows in outputs.items():
        write_csv(OUT / filename, rows)

    doc_path = ROOT / "898-Y5-R10-trace-vertical-generator-matter-descent-signature-or-residual-vector.md"
    write_markdown(
        doc_path,
        generated_utc,
        source_rows_,
        summary_rows_,
        vertical_rows_,
        matter_rows_,
        pairing_rows_,
        residual_rows_,
        branch_rows_,
        promotion_rows_,
        route_rows_,
        claim_rows_,
        decision_rows_,
        next_rows_,
        validation_rows_,
    )

    failed = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"wrote {doc_path}")
    print(f"wrote {OUT / 'P8_Y5_BRR545_898_VALIDATION.csv'}")
    print(f"status={STATUS}")
    if failed:
        print("failed_validation=" + ",".join(row["check_id"] for row in failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
