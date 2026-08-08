import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3765"
BRANCH = "MTS_R2FR_Y5_CONSTRUCT_QOBS_PARENT_QUOTIENT_OR_FRAME_RESIDUAL_MAP_3765"
PCW = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work"
)
RESIDUALS = PCW / "source-intake" / "mts_residuals"
FORMALIZATION = PCW.parent / "formalization-workbench"
DOC_PATH = PCW / "3765-Y5-R2FR-construct-qobs-parent-quotient-or-frame-residual-map.md"


OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3765_SOURCE_REGISTER.csv",
    "qobs_candidate": RESIDUALS / "P8_Y5_R2FR_3765_QOBS_CANDIDATE_MAP.csv",
    "certificate_tests": RESIDUALS / "P8_Y5_R2FR_3765_QOBS_CERTIFICATE_TESTS.csv",
    "sector_residual_map": RESIDUALS / "P8_Y5_R2FR_3765_SECTOR_READOUT_RESIDUAL_MAP.csv",
    "parent_verdict": RESIDUALS / "P8_Y5_R2FR_3765_PARENT_QOBS_VERDICT.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_3765_CLAIM_GATES.csv",
    "decision_rows": RESIDUALS / "P8_Y5_R2FR_3765_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3765_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3765_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3765_VALIDATION.csv",
}


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(timestamp: str, valid_for_claim: bool = False) -> dict[str, object]:
    return {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH,
        "checkpoint_id": CHECKPOINT,
        "valid_for_claim": valid_for_claim,
    }


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_paths() -> dict[str, Path]:
    return {
        "SRC3765_0_3764_doc": PCW / "3764-Y5-R2FR-derive-single-observed-frame-and-same-total-source-from-parent-quotient.md",
        "SRC3765_1_3764_quotient_theorem": RESIDUALS / "P8_Y5_R2FR_3764_PARENT_QUOTIENT_DESCENT_THEOREM.csv",
        "SRC3765_2_3764_source_theorem": RESIDUALS / "P8_Y5_R2FR_3764_SAME_TOTAL_SOURCE_VARIATION_THEOREM.csv",
        "SRC3765_3_3764_fallbacks": RESIDUALS / "P8_Y5_R2FR_3764_FRAME_SOURCE_FALLBACK_RESIDUALS.csv",
        "SRC3765_4_3138_qobs_construction": RESIDUALS / "P8_Y5_R2FR_3138_TYPED_QOBS_CONSTRUCTION.csv",
        "SRC3765_5_3138_qobs_certificates": RESIDUALS / "P8_Y5_R2FR_3138_REP_QOBS_CERTIFICATE_MATRIX.csv",
        "SRC3765_6_3633_strict_quotient": RESIDUALS / "P8_Y5_R2FR_3633_STRICT_QUOTIENT_THEOREM.csv",
        "SRC3765_7_3635_source_readout": RESIDUALS / "P8_Y5_R2FR_3635_SOURCE_READOUT_DESCENT_THEOREM.csv",
        "SRC3765_8_3636_source_mass": RESIDUALS / "P8_Y5_R2FR_3636_SOURCE_MASS_QUOTIENT_SIGNATURE.csv",
        "SRC3765_9_3646_matter_descent": RESIDUALS / "P8_Y5_R2FR_3646_MATTER_DESCENT_THEOREM_ATTEMPT.csv",
        "SRC3765_10_3699_projection_rows": RESIDUALS / "P8_Y5_R2FR_3699_QUOTIENT_PROJECTION_ROWS.csv",
        "SRC3765_11_944_descent_doc": PCW / "944-Y5-R10-quotient-observed-coframe-descent-proof-or-frame-leak-source-bounds.md",
        "SRC3765_12_945_qmap_doc": PCW / "945-Y5-R10-parent-q-map-Obs-e-functor-construction-or-first-frame-leak-bound-pack.md",
        "SRC3765_13_1362_qobs_gap_doc": PCW / "1362-Y5-R10-RAB-quotient-observed-coframe-parent-qObs-or-MHref-denominator-source-pack.md",
        "SRC3765_14_1363_current_chain_doc": PCW / "1363-Y5-R10-RAB-parent-qObs-current-chain-bridge-or-Htau-Href-first-source-row.md",
    }


def source_register(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "source_id": source_id,
            "source_path": str(path),
            "source_exists": path.exists(),
            "role": "3765 q_obs construction/residual-map input",
        }
        for source_id, path in source_paths().items()
    ]


def qobs_candidate_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "QOC3765_0_parent_configuration",
            "Phi_parent",
            "local MTS parent configuration before observed quotient",
            "Phi_parent=(M, motion/time/space variables, candidate coframe geometry, relation data C, 27-cell/orbit data h, local current/readout data J, source fields psi_A,A_mu, constants theta, boundary/support data, representative labels xi)",
            "inventory_only",
            "not enough: parent action and vertical kernel still unsigned",
        ),
        (
            "QOC3765_1_vertical_equivalence",
            "R_vert and V=ker(Dq_obs)",
            "candidate gauge/representative equivalence",
            "Phi ~ Phi' when observed coframe/time/calibration/source readouts and quotient-owned relation/orbit/current data agree up to diffeomorphism, local Lorentz, and declared MTS representative moves",
            "definition_candidate",
            "must prove representative moves are presymplectic-null and matter-invisible",
        ),
        (
            "QOC3765_2_observed_object",
            "Q_obs",
            "typed observed quotient object",
            "Q_obs=(M, e_obs mod SO(1,3), g_eff=e_obs^T eta e_obs, tau_obs, orientation, calibration class, [C]_PD, Orbit_27(h), [J_rel]_local, theta_univ, boundary_class_if_owned, source_domain_id_if_owned)",
            "candidate_object_written",
            "e_obs cannot be a magic coordinate unless omitted directions are proved null/gauge",
        ),
        (
            "QOC3765_3_candidate_map",
            "q_obs_candidate: Phi_parent -> Q_obs",
            "explicit candidate map",
            "q_obs_candidate(Phi)=the tuple of observed coframe/time/calibration plus quotient classes [C]_PD, Orbit_27(h), [J_rel]_local, theta_univ, boundary/source-domain classes",
            "constructed_as_candidate",
            "map is not parent-signed until Dq_obs, kernel, action pullback, and source descent are proved",
        ),
        (
            "QOC3765_4_observed_frame_functor",
            "Obs_e(q_obs)",
            "frame extraction",
            "Obs_e(q_obs_candidate(Phi))=e_obs and Obs_g(q_obs_candidate(Phi))=g_eff",
            "conditional_identity",
            "projection trap remains unless e_obs is parent-owned and all sector frames factor through same q_obs",
        ),
        (
            "QOC3765_5_sector_factorization_template",
            "r_s=F_s o q_obs",
            "sector readout descent template",
            "s in {matter, EM, light, clock, orbital/source, boundary/current}; each q_s must be q_obs followed by a sector readout functor F_s",
            "template_emitted",
            "each sector still needs its own descent proof or residual row",
        ),
        (
            "QOC3765_6_source_action_template",
            "S_src=Sbar_src[q_obs(Phi),psi_A,A_mu,theta]",
            "same-source descent target",
            "material, EM, binding, apparatus, and interaction stresses vary against one g_eff/coframe from q_obs",
            "template_emitted",
            "current corpus has theorem interface but not parent-owned action factorization",
        ),
        (
            "QOC3765_7_current_chain_template",
            "theta_MTS,Q_tau,H_tau,H_ref",
            "local current/denominator descent target",
            "theta_MTS, Q_tau^MTS, H_tau, H_ref must be q_obs-basic or else they create a boundary/current residual",
            "template_emitted",
            "1363 says this bridge is still unsigned",
        ),
        (
            "QOC3765_8_boundary_support_template",
            "boundary_class and source_domain_id",
            "worldtube/support ownership",
            "compact source support and local boundary conditions must be quotient-owned, not hand-cut after variation",
            "template_emitted",
            "without this, side flux, radial hair, and source-current terms stay live",
        ),
        (
            "QOC3765_9_failure_identity",
            "Delta q_s := q_s - q_obs",
            "residual fallback identity",
            "if any sector readout does not factor through q_obs, retain an explicit Delta q_s residual feeding WEP, clocks, EM, PPN, orbit, R10, or Gdot rows",
            "residual_interface_constructed",
            "this keeps the branch honest if q_obs cannot be signed",
        ),
    ]
    return [
        {
            **base(timestamp),
            "construction_id": construction_id,
            "object": obj,
            "role": role,
            "mathematical_form": mathematical_form,
            "current_status": current_status,
            "failure_if_used_as_proof": failure,
            "claim_allowed": False,
        }
        for construction_id, obj, role, mathematical_form, current_status, failure in rows
    ]


def certificate_test_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "QCT3765_0_source_inventory",
            "all required source files for q_obs construction exist",
            "all SRC3765 rows source_exists=True",
            True,
            "path hygiene passes",
        ),
        (
            "QCT3765_1_parent_action_pullback",
            "S_parent[Phi]=S_red[q_obs(Phi)]+S_top[q_obs(Phi)] plus local-null topological variation",
            "no explicit parent action pullback signature found in current corpus",
            False,
            "blocks treating q_obs as a derived quotient",
        ),
        (
            "QCT3765_2_vertical_kernel_owned",
            "for every representative direction v, Dq_obs[v]=0 and v spans only gauge/representative freedom",
            "candidate vertical relation is written but not generated from the parent variational system",
            False,
            "blocks quotient uniqueness",
        ),
        (
            "QCT3765_3_presymplectic_null",
            "i_v Omega_parent=0 and i_v Theta_parent=dB_v with zero compact local flux",
            "3138 and 945 retain this as the hard missing certificate",
            False,
            "blocks saying omitted directions are unphysical",
        ),
        (
            "QCT3765_4_matter_invisibility",
            "Lie_v S_src=0 for matter, EM, binding, apparatus, and interaction terms",
            "3646 supplies exact chain-rule theorem but says premises are unsigned",
            False,
            "blocks WEP/source zero claim",
        ),
        (
            "QCT3765_5_no_shadow_frame",
            "no Weyl/disformal/species/material marker channel survives outside q_obs",
            "944/945/1362 keep shadow frame and material marker counterexamples live",
            False,
            "blocks single physical metric/coframe claim",
        ),
        (
            "QCT3765_6_tau_clock_orbit_descent",
            "tau_obs, clock readouts, orbital calibration, and source monopole all descend through q_obs",
            "3635/3636 derive normalized residual signatures but not zero",
            False,
            "blocks local-GR/Newton calibration closure",
        ),
        (
            "QCT3765_7_current_chain_basic",
            "theta_MTS, Q_tau^MTS, H_tau, and H_ref are q_obs-basic",
            "1363 explicitly marks the bridge unsigned",
            False,
            "blocks denominator/current closure",
        ),
        (
            "QCT3765_8_boundary_support_silence",
            "source support and boundary terms are quotient-owned with no compact leakage",
            "3756-3758 leave exchange/boundary channels as residual rows",
            False,
            "blocks no-flux/no-radial-hair closure",
        ),
        (
            "QCT3765_9_sector_factorization",
            "matter, EM, light, clock, orbital/source, and boundary readouts factor as F_s o q_obs",
            "3764 proves what follows if true, but this checkpoint cannot sign all factors",
            False,
            "forces explicit sector residual map",
        ),
    ]
    return [
        {
            **base(timestamp),
            "certificate_id": certificate_id,
            "required_clause": required_clause,
            "test_or_evidence": evidence,
            "passes_certificate": passes,
            "blocking_consequence": consequence,
            "claim_allowed": False,
        }
        for certificate_id, required_clause, evidence, passes, consequence in rows
    ]


def sector_residual_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "SRM3765_0_matter",
            "Delta q_matter",
            "|q_matter-q_obs|",
            "matter species or material constants see representative/bath variables outside q_obs",
            "eta_source_AB, beta_X^matter, qbar_XT, WEP",
            "derive matter action descent or bound composition residual",
        ),
        (
            "SRM3765_1_EM",
            "Delta q_EM",
            "|q_EM-q_obs|",
            "EM frame/stress or fine-structure channel uses non-q_obs variables",
            "eta_EM_AB, delta_gamma_EM, delta_beta_EM, alpha_fs drift, Maxwell same-source gate",
            "prove EM Hilbert-stress descent through q_obs or source EM residual rows",
        ),
        (
            "SRM3765_2_light",
            "Delta q_light",
            "|q_light-q_obs|",
            "null cone/readout metric differs from matter/source metric",
            "PPN gamma, Shapiro/lensing, preferred-frame tests",
            "prove light-cone factorization or bound gamma/light residual",
        ),
        (
            "SRM3765_3_clock",
            "Delta q_clock",
            "|q_clock-q_obs| + |delta tau_obs|",
            "clock time generator or transition frequencies see variables outside q_obs",
            "clock redshift, local Lorentz, time-dilation branch, alpha_fs drift",
            "prove tau/clock quotient ownership or produce clock residual profile",
        ),
        (
            "SRM3765_4_orbital_source",
            "Delta q_orbit_source",
            "|q_orbit-q_obs| + |partial_r ln mu_obs|",
            "orbital GM/source monopole not equal to q_obs Hilbert source readout",
            "Newtonian limit, Gdot, radial hair, orbital tests",
            "prove source monopole descent or source radial/profile rows",
        ),
        (
            "SRM3765_5_boundary_current",
            "Delta q_boundary",
            "|Pi_M q_exchange| + |delta H_tau| + |delta H_ref| + |boundary_owner_flux|",
            "boundary/current denominator not q_obs-basic",
            "Gdot, source conservation, radial hair, local action denominator",
            "prove current-chain q-basicness or fill H_tau/H_ref residuals",
        ),
        (
            "SRM3765_6_range_extra",
            "Delta q_range",
            "|alpha(lambda)| + |extra-field hair amplitude|",
            "finite-range mediator or exterior hair survives outside local EH/q_obs branch",
            "R10 fifth-force, PPN, radial profile",
            "prove no-range/no-hair from q_obs kernel or acquire bound curve inputs",
        ),
        (
            "SRM3765_7_frame_summary",
            "delta_frame_source",
            "|Delta q_matter|+|Delta q_EM|+|Delta q_light|+|Delta q_clock|+|Delta q_orbit_source|",
            "one or more sector readouts fail to descend through q_obs",
            "single-frame local GR gate",
            "drive all Delta q_s to zero by parent proof or keep a bounded residual vector",
        ),
    ]
    return [
        {
            **base(timestamp),
            "residual_id": residual_id,
            "symbol": symbol,
            "residual_formula": formula,
            "failure_mode": failure_mode,
            "feeds_observables": feeds_observables,
            "next_action": next_action,
            "numeric_value": "MISSING_PARENT_INPUT",
            "units": "dimensionless_or_sector_specific",
            "claim_allowed": False,
        }
        for residual_id, symbol, formula, failure_mode, feeds_observables, next_action in rows
    ]


def parent_verdict_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    certificates = grouped["certificate_tests"]
    all_core_pass = all(row["passes_certificate"] is True for row in certificates if row["certificate_id"] != "QCT3765_0_source_inventory")
    return [
        {
            **base(timestamp),
            "verdict_id": "PV3765_0_qobs_candidate",
            "verdict": "QOBS_CANDIDATE_CONSTRUCTED_BUT_NOT_PARENT_SIGNED",
            "qobs_candidate_exists": True,
            "all_core_certificates_pass": all_core_pass,
            "parent_qobs_signed": False,
            "local_gr_claim_allowed": False,
            "reason": "the candidate quotient object and sector residual map are explicit, but parent action pullback, kernel nullness, matter invisibility, no-shadow frame, current-chain descent, and boundary silence are unsigned",
        },
        {
            **base(timestamp),
            "verdict_id": "PV3765_1_residual_route",
            "verdict": "KEEP_DELTA_QS_RESIDUAL_VECTOR_LIVE",
            "qobs_candidate_exists": True,
            "all_core_certificates_pass": False,
            "parent_qobs_signed": False,
            "local_gr_claim_allowed": False,
            "reason": "until q_obs is signed, each sector mismatch Delta q_s is a named residual rather than a hidden closure assumption",
        },
    ]


def claim_gate_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    sources_exist = all(Path(str(row["source_path"])).exists() for row in grouped["sources"])
    candidate_emitted = len(grouped["qobs_candidate"]) >= 10
    certificates_emitted = len(grouped["certificate_tests"]) >= 10
    residuals_emitted = len(grouped["sector_residual_map"]) >= 8
    parent_signed = all(row["passes_certificate"] is True for row in grouped["certificate_tests"])
    rows = [
        ("CG3765_0_sources", "all 3765 source paths exist", sources_exist, "path hygiene"),
        ("CG3765_1_candidate_map", "q_obs candidate map emitted", candidate_emitted, "candidate object and map are written explicitly"),
        ("CG3765_2_certificate_matrix", "q_obs certificate tests emitted", certificates_emitted, "hard proof clauses are visible"),
        ("CG3765_3_sector_residual_map", "sector readout residual map emitted", residuals_emitted, "failure becomes Delta q_s vector"),
        ("CG3765_4_parent_qobs_signed", "parent q_obs construction signed", parent_signed, "blocked by unsigned parent action/kernel/source/current clauses"),
        ("CG3765_5_single_frame_claim", "single observed frame claim allowed", False, "blocked until CG3765_4 passes"),
        ("CG3765_6_same_total_source_claim", "same total Hilbert source claim allowed", False, "blocked until source action descent through q_obs is signed"),
        ("CG3765_7_local_gr_claim", "local GR/Newton branch claim allowed", False, "blocked until q_obs plus local EH/no-range/global-kappa clauses pass"),
    ]
    return [
        {
            **base(timestamp),
            "gate_id": gate_id,
            "gate": gate,
            "passed": passed,
            "details": details,
            "claim_allowed": False,
        }
        for gate_id, gate, passed, details in rows
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "DEC3765_0",
            "The best possible q_obs candidate is now explicit enough to attack; it is no longer just 'missing coupling'.",
            "try to prove the kernel of q_obs is presymplectic-null and matter-invisible",
        ),
        (
            "DEC3765_1",
            "The construction still cannot be claimed as MTS local GR because e_obs/q_obs could still be projection-by-declaration.",
            "do not update public claims; keep local-GR gate closed",
        ),
        (
            "DEC3765_2",
            "If the kernel proof fails, the sector residual vector Delta q_s is already the clean path to empirical bounds.",
            "fill the first frame/source residual bound rather than invent a closure axiom",
        ),
        (
            "DEC3765_3",
            "The next mathematical leap is not another list of missing inputs; it is a focused proof attempt on ker(Dq_obs).",
            "target the parent symplectic/boundary certificate directly",
        ),
    ]
    return [
        {
            **base(timestamp),
            "decision_id": decision_id,
            "decision": decision,
            "action": action,
            "claim_allowed": False,
        }
        for decision_id, decision, action in rows
    ]


def next_target_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "next_id": "NEXT3765_0",
            "target_doc": "3766-Y5-R2FR-prove-qobs-kernel-presymplectic-null-or-first-frame-residual-bound.md",
            "target_script": "scripts/Y5_R2FR_3766_prove_qobs_kernel_presymplectic_null_or_first_frame_residual_bound.py",
            "objective": "prove ker(Dq_obs) is presymplectic-null and matter-invisible for the constructed q_obs candidate, or emit the first numeric/source-ready frame residual bound row",
            "reason": "3765 constructs the candidate map and residual vector; the next pass must attack the kernel certificate directly rather than relisting the gap",
            "claim_allowed": False,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "status": "QOBS_CANDIDATE_AND_SECTOR_RESIDUAL_MAP_CONSTRUCTED_NOT_PARENT_SIGNED",
            "summary": "3765 constructs the explicit parent observed quotient candidate q_obs_candidate and the fallback Delta q_s sector residual vector. It does not claim local GR: the parent action pullback, vertical-kernel null proof, matter invisibility, no-shadow frame, current-chain descent, and boundary/support silence remain unsigned.",
            "claim_allowed": False,
        }
    ]


def validation_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks = [
        ("sources_exist", "all 3765 source paths exist", all(Path(str(row["source_path"])).exists() for row in grouped["sources"])),
        ("generated_csvs_parse", "all generated 3765 csvs parse", all(read_csv(path) for path in generated_csvs)),
        ("candidate_map", "q_obs candidate has at least ten construction rows", len(grouped["qobs_candidate"]) >= 10),
        ("certificate_tests", "q_obs certificate matrix has at least ten tests", len(grouped["certificate_tests"]) >= 10),
        ("unsigned_parent_visible", "parent q_obs remains explicitly unsigned", any(row["certificate_id"] == "QCT3765_1_parent_action_pullback" and row["passes_certificate"] is False for row in grouped["certificate_tests"])),
        ("sector_residuals", "sector residual map covers at least eight residual rows", len(grouped["sector_residual_map"]) >= 8),
        ("fallback_values_block_claim", "all residual numeric values remain missing parent input", all(row["numeric_value"] == "MISSING_PARENT_INPUT" for row in grouped["sector_residual_map"])),
        ("claim_gates_closed", "single-frame/same-source/local-GR claims remain closed", all(row["passed"] is False for row in grouped["claim_gates"] if row["gate_id"] in {"CG3765_4_parent_qobs_signed", "CG3765_5_single_frame_claim", "CG3765_6_same_total_source_claim", "CG3765_7_local_gr_claim"})),
        ("next_target", "3766 kernel certificate target emitted", grouped["next_target"][0]["target_doc"] == "3766-Y5-R2FR-prove-qobs-kernel-presymplectic-null-or-first-frame-residual-bound.md"),
        ("no_formalization_leak", "no 3765 files written to formalization-workbench", not FORMALIZATION.exists() or not list(FORMALIZATION.rglob("*3765*"))),
    ]
    return [
        {
            **base(timestamp),
            "validation_id": validation_id,
            "description": description,
            "result": "PASS" if result else "FAIL",
            "details": "" if result else "check failed",
        }
        for validation_id, description, result in checks
    ]


def render_doc(grouped: dict[str, list[dict[str, object]]]) -> str:
    lines = [
        "# 3765 - Construct q_obs Parent Quotient Or Frame Residual Map",
        "",
        "## Status",
        "",
        f"`{grouped['status'][0]['status']}`.",
        "",
        grouped["status"][0]["summary"],
        "",
        "## What Changed",
        "",
        "This checkpoint takes the hard object named by 3764 and writes the best current `q_obs` candidate explicitly. It also refuses to treat the candidate as a proof. The branch now has a concrete quotient target plus a concrete sector-residual vector if the quotient cannot be signed.",
        "",
        "The move is useful because the next derivation no longer has to hunt through the whole corpus for 'the coupling'. It can attack one sharp statement: `ker(Dq_obs)` must be gauge/null/matter-invisible, or the sector residuals must be bounded.",
        "",
        "## q_obs Candidate Map",
    ]
    for row in grouped["qobs_candidate"]:
        lines.append(f"- `{row['construction_id']}` `{row['object']}`: {row['mathematical_form']} Status: `{row['current_status']}`.")
    lines.extend(["", "## Certificate Tests"])
    for row in grouped["certificate_tests"]:
        lines.append(f"- `{row['certificate_id']}` pass=`{row['passes_certificate']}`: {row['required_clause']} Evidence: {row['test_or_evidence']}.")
    lines.extend(["", "## Sector Readout Residual Map"])
    for row in grouped["sector_residual_map"]:
        lines.append(f"- `{row['residual_id']}` `{row['symbol']}`: {row['residual_formula']} feeds `{row['feeds_observables']}`. Next: {row['next_action']}.")
    lines.extend(["", "## Parent Verdict"])
    for row in grouped["parent_verdict"]:
        lines.append(f"- `{row['verdict_id']}` `{row['verdict']}`: {row['reason']}")
    lines.extend(["", "## Claim Gates"])
    for row in grouped["claim_gates"]:
        lines.append(f"- `{row['gate_id']}` pass=`{row['passed']}`: {row['gate']} - {row['details']}")
    lines.extend(["", "## Decisions"])
    for row in grouped["decision_rows"]:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} Action: {row['action']}.")
    lines.extend(["", "## Next Target"])
    for row in grouped["next_target"]:
        lines.append(f"- `{row['target_doc']}`: {row['objective']}")
    lines.extend(["", "## Validation"])
    for row in grouped["validation"]:
        lines.append(f"- `{row['validation_id']}` `{row['result']}`: {row['description']}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    timestamp = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)

    grouped: dict[str, list[dict[str, object]]] = {
        "sources": source_register(timestamp),
        "qobs_candidate": qobs_candidate_rows(timestamp),
        "certificate_tests": certificate_test_rows(timestamp),
        "sector_residual_map": sector_residual_rows(timestamp),
        "decision_rows": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
    }
    grouped["parent_verdict"] = parent_verdict_rows(timestamp, grouped)
    grouped["claim_gates"] = claim_gate_rows(timestamp, grouped)

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["qobs_candidate"], grouped["qobs_candidate"])
    write_csv(OUTPUTS["certificate_tests"], grouped["certificate_tests"])
    write_csv(OUTPUTS["sector_residual_map"], grouped["sector_residual_map"])
    write_csv(OUTPUTS["parent_verdict"], grouped["parent_verdict"])
    write_csv(OUTPUTS["claim_gates"], grouped["claim_gates"])
    write_csv(OUTPUTS["decision_rows"], grouped["decision_rows"])
    write_csv(OUTPUTS["next_target"], grouped["next_target"])
    write_csv(OUTPUTS["status"], grouped["status"])

    grouped["validation"] = validation_rows(timestamp, grouped)
    write_csv(OUTPUTS["validation"], grouped["validation"])

    DOC_PATH.write_text(render_doc(grouped), encoding="utf-8")

    cache = Path(__file__).resolve().parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    failures = [row for row in grouped["validation"] if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3765 validation failed: {failures}")
    print("wrote 3765 checkpoint: q_obs candidate and sector residual map constructed, not parent-signed")


if __name__ == "__main__":
    main()
