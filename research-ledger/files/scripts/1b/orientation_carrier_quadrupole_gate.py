from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, Iterable, List


def write_csv(path: Path, rows: Iterable[Dict[str, object]]) -> None:
    row_list = list(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not row_list:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row_list[0].keys()))
        writer.writeheader()
        writer.writerows(row_list)


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def orientation_zero_proof_rows() -> List[Dict[str, object]]:
    return [
        {
            "proof_id": "OCZ4480_0_SO3_scalar_profile_theorem",
            "clause": "a true local scalar marker profile has no tracefree second moment",
            "formal_statement": "If F_M(y) is invariant under the local SO(3) little group of h_ij, then M^{ij}=int y^i y^j F_M d^3y commutes with every rotation and therefore M^{ij}=(mu2_M/3)h^{ij}.",
            "derivation": "The second moment tensor is a symmetric rank-2 representation. The only SO(3)-invariant symmetric rank-2 tensor is the spatial metric h^{ij}; equivalently the l=2 irreducible part is projected out. Hence Q_M_TF^{ij}=M^{ij}-(mu2_M/3)h^{ij}=0.",
            "zero_result": "Z_orientation=True implies Q_M_TF^{ij}=0 and R_quad=0 on the spatial branch",
            "current_status": "DERIVED_REPRESENTATION_THEOREM_CONDITIONAL_ON_SO3_SCALAR_PARENT",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "proof_id": "OCZ4480_1_STF_carrier_inventory",
            "clause": "a nonzero tracefree quadrupole needs a rank-2 STF carrier",
            "formal_statement": "Q_M_TF^{ij} can be sourced only by an available STF object: n^{<i}n^{j>}, s^{<i}s^{j>}, k^{<i}k^{j>}, E^{ij}_TF, B^{ij}_TF, N^{ij}, boundary-normal b^{<i}b^{j>}, anisotropic support metric, or an equivalent orientation distribution.",
            "derivation": "The l=2 part cannot be manufactured from scalars alone. Products of one vector/director, spin axis, wave vector, Poynting/flux direction, tidal tensor, nematic tensor, or boundary normal supply the needed SO(3) representation.",
            "zero_result": "if the parent support alphabet contains no such carrier and no anisotropic boundary routing, Q_M_TF^{ij}=0",
            "current_status": "CARRIER_ALPHABET_TEST_WRITTEN_PARENT_UNSIGNED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "proof_id": "OCZ4480_2_orientation_averaging_theorem",
            "clause": "random or gauge orientation kills the STF branch only with a signed average",
            "formal_statement": "If orientation variables A are integrated with an isotropic measure dmu(A) independent of local source response, then int A^{ij}_STF dmu(A)=0.",
            "derivation": "The isotropic group average annihilates every l=2 component. This is a real zero proof only if the parent measure is isotropic before variation and no boundary, material or readout term reselects an axis.",
            "zero_result": "orientation averaging can sign Z_orientation only when the measure and response are parent-owned",
            "current_status": "AVERAGING_ZERO_THEOREM_CONDITIONAL_PARENT_MEASURE_UNSIGNED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "proof_id": "OCZ4480_3_wave_and_Poynting_counterroute",
            "clause": "waves, flux and the Poynting vector are live orientation carriers unless excluded",
            "formal_statement": "A finite background flux S^i, wave vector k^i, polarization tensor e^{ij}, or EM/gravitational radiation stress can generate S^{<i}S^{j>}, k^{<i}k^{j>} or e^{ij}_TF in the marker profile.",
            "derivation": "This route directly addresses the possible 'background field / Poynting vector' intuition: it is not automatically wrong. It is exactly an orientation-carrier branch, and therefore either a parent mechanism or a residual scorer is required.",
            "zero_result": "do not set Q_M_TF=0 while wave/flux carriers remain in the parent alphabet",
            "current_status": "COUNTERROUTE_KEPT_LIVE_FOR_EM_WAVE_BACKGROUND",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "proof_id": "OCZ4480_4_boundary_normal_counterroute",
            "clause": "local boundary or worldtube normals can reintroduce anisotropy",
            "formal_statement": "Even if the bulk scalar profile is SO(3)-silent, boundary terms can source Q_M_TF^{ij} through b^{<i}b^{j>} unless the boundary support is fixed, topological, no-flux, or Hamiltonian-routed.",
            "derivation": "The support-zero branch already separated boundary support. 4480 carries that discipline into the l=2 channel: boundary orientation is a separate carrier, not a harmless surface detail.",
            "zero_result": "bulk isotropy is insufficient without boundary-orientation routing",
            "current_status": "BOUNDARY_ORIENTATION_FIREWALL_UNSIGNED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "proof_id": "OCZ4480_5_verdict",
            "clause": "orientation zero theorem exists but is not parent-signed",
            "formal_statement": "Z_orientation=True iff the parent marker/support alphabet has no STF carrier, no surviving anisotropic orientation distribution, and no boundary-normal or wave/flux counterroute.",
            "derivation": "4480 proves the representation-theory zero route and writes the carrier inventory test. Current MTS has not yet signed the full parent carrier alphabet, so the finite quadrupole scorer remains live.",
            "zero_result": "no local-GR/R10/PPN claim; use quadrupole residual scorer until Z_orientation signs",
            "current_status": "ORIENTATION_ZERO_PARENT_UNSIGNED_QUADRUPOLE_SCORER_REQUIRED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
    ]


def quadrupole_residual_scorer_rows() -> List[Dict[str, object]]:
    return [
        {
            "scorer_id": "QRS4480_0_canonical_STF_amplitude",
            "quantity": "Q_M_TF^{ij}",
            "formula": "Q_M_TF^{ij}=epsilon_Q * mu0_abs * ell_sup^2 * A_STF^{ij}, with ||A_STF||=1 and 0<=epsilon_Q<=1",
            "derivation": "Any finite tracefree second moment can be written as an amplitude times a unit STF tensor. Compact support gives epsilon_Q<=1 because ||Q_M_TF||<=mu2_abs<=ell_sup^2 mu0_abs.",
            "target_arenas": "all_l2_local_residuals",
            "status": "DERIVED_CANONICAL_QUADRUPOLE_PARAMETERIZATION",
            "valid_for_claim": False,
        },
        {
            "scorer_id": "QRS4480_1_local_projection_bound",
            "quantity": "R_quad_a",
            "formula": "R_quad_a = lambda_M*zeta_Q_a*Q_M_TF^{ij}*H_a,ij^TF/(2*N_a); |R_quad_a| <= |lambda_M| |zeta_Q_a| mu0_abs ell_sup^2 /(2 |N_a| L_loc^2)",
            "derivation": "Normalize the tracefree Hessian response by ||H_a^TF||<=1/L_loc^2 and apply the compact-support STF bound. No cancellation across arenas is allowed.",
            "target_arenas": "PPN;clock;orbital;R10_shape_guard",
            "status": "DERIVED_COMPONENTWISE_LOCAL_BOUND",
            "valid_for_claim": False,
        },
        {
            "scorer_id": "QRS4480_2_PPN_anisotropy_gate",
            "quantity": "R_PPN_Q",
            "formula": "R_PPN_Q = Pi_PPN_Q[R_quad_a] with |R_PPN_Q| <= tau_PPN_Q required",
            "derivation": "A pure l=2 residual can vanish in a spherical monopole average but still enter preferred-location, anisotropic metric, or non-spherical light/clock readouts. The PPN gate must therefore use an l=2 projector, not a scalar gamma average.",
            "target_arenas": "PPN_xi;preferred_location;anisotropic_metric",
            "status": "SCORER_CONTRACT_WRITTEN_NEEDS_BOUND_INPUT",
            "valid_for_claim": False,
        },
        {
            "scorer_id": "QRS4480_3_Shapiro_LOS_kernel",
            "quantity": "R_Shapiro_Q",
            "formula": "Delta_Q = A_Q*C_Q*Pi_quad_LOS[W], with |Pi_quad_LOS|<=1 for positive radial W",
            "derivation": "Imported from the prior anisotropic Shapiro kernel: spherical orthogonality does not imply line-of-sight invisibility. The safe envelope is the worst-case LOS kernel unless a source geometry is supplied.",
            "target_arenas": "Shapiro;light_bending;Cassini_style_anisotropic_smoke",
            "status": "KERNEL_IMPORTED_NONCLAIM_NEEDS_TAU_SHAPIRO_Q",
            "valid_for_claim": False,
        },
        {
            "scorer_id": "QRS4480_4_clock_quadrupole_gate",
            "quantity": "R_clock_Q",
            "formula": "R_clock_Q = Pi_clock_Q[R_quad_a] and must satisfy |R_clock_Q|<=tau_clock_Q",
            "derivation": "Clock comparisons read potential/redshift differences along actual baseline geometry, so an l=2 field survives whenever the two clock locations sample different STF projections.",
            "target_arenas": "clock_redshift;clock_anisotropy;Lorentz_locality",
            "status": "SCORER_CONTRACT_WRITTEN_NEEDS_CLOCK_GEOMETRY_BOUND",
            "valid_for_claim": False,
        },
        {
            "scorer_id": "QRS4480_5_orbital_quadrupole_gate",
            "quantity": "R_orbital_Q",
            "formula": "R_orbital_Q = Pi_orb_Q[R_quad_a] and must satisfy |R_orbital_Q|<=tau_orbital_Q",
            "derivation": "A tracefree local potential shifts precession/nodal/phase observables through the orbit's orientation relative to A_STF. It is scoreable only after a source-domain transfer or direct local source geometry is declared.",
            "target_arenas": "orbital_precession;ephemerides;binary_orbits",
            "status": "SCORER_CONTRACT_WRITTEN_NEEDS_ORBITAL_TRANSFER",
            "valid_for_claim": False,
        },
        {
            "scorer_id": "QRS4480_6_no_cancellation_envelope",
            "quantity": "R_Q_abs",
            "formula": "R_Q_abs=max(|R_PPN_Q|/tau_PPN_Q, |R_clock_Q|/tau_clock_Q, |R_orbital_Q|/tau_orbital_Q, |R_Shapiro_Q|/tau_Shapiro_Q) when numeric bounds exist",
            "derivation": "The branch passes only if every relevant l=2 observable is below its own bound. A scalar pass cannot hide an anisotropic failure.",
            "target_arenas": "claim_gate_guard",
            "status": "NO_CANCELLATION_QUADRUPOLE_ENVELOPE_WRITTEN",
            "valid_for_claim": False,
        },
    ]


def quadrupole_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "QRI4480_0_Z_orientation",
            "quantity": "Z_orientation",
            "definition": "certificate that the parent support alphabet has no l=2 orientation carrier",
            "formula_or_test": "True iff no vector/director/spin/wave/Poynting/tidal/nematic/boundary-normal carrier survives before variation",
            "needed_inputs": "parent carrier alphabet; support variables; boundary routing; wave/EM flux treatment",
            "current_value": "MISSING_PARENT_ORIENTATION_ZERO_CERTIFICATE",
            "units": "boolean_certificate",
            "target": "Q_M_TF=0;R_quad=0",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "QRI4480_1_carrier_inventory",
            "quantity": "I_STF",
            "definition": "explicit list of possible rank-2 STF carrier sources",
            "formula_or_test": "I_STF={n_i n_j, s_i s_j, k_i k_j, S_i S_j, E_ij^TF, B_ij^TF, N_ij, b_i b_j, anisotropic_support_metric}_TF intersect S_parent",
            "needed_inputs": "parent action/support alphabet and all integrated-out/background fields",
            "current_value": "MISSING_STF_CARRIER_INVENTORY",
            "units": "set",
            "target": "orientation_zero_or_finite_branch",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "QRI4480_2_epsilon_Q",
            "quantity": "epsilon_Q",
            "definition": "dimensionless tracefree quadrupole support fraction",
            "formula_or_test": "epsilon_Q=||Q_M_TF||/(mu0_abs ell_sup^2), bounded 0<=epsilon_Q<=1",
            "needed_inputs": "Q_M_TF norm or carrier amplitude; mu0_abs; ell_sup",
            "current_value": "MISSING_QUADRUPOLE_FRACTION",
            "units": "dimensionless",
            "target": "finite_quadrupole_scorer",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "QRI4480_3_A_STF",
            "quantity": "A_STF^{ij}",
            "definition": "unit orientation tensor for the finite quadrupole branch",
            "formula_or_test": "A_STF^{ij}=Q_M_TF^{ij}/||Q_M_TF|| when Q_M_TF is nonzero",
            "needed_inputs": "orientation axis/tensor; norm convention; source frame",
            "current_value": "MISSING_UNIT_STF_ORIENTATION",
            "units": "dimensionless_tensor",
            "target": "PPN;clock;orbital;Shapiro kernels",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "QRI4480_4_tau_PPN_Q",
            "quantity": "tau_PPN_Q",
            "definition": "empirical bound for anisotropic local metric/PPN l=2 residual",
            "formula_or_test": "require |R_PPN_Q|<=tau_PPN_Q in a declared convention",
            "needed_inputs": "PPN anisotropy bound source; convention map; projection Pi_PPN_Q",
            "current_value": "MISSING_PPN_QUADRUPOLE_BOUND",
            "units": "dimensionless",
            "target": "PPN_xi;preferred_location",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "QRI4480_5_tau_clock_Q",
            "quantity": "tau_clock_Q",
            "definition": "empirical bound for clock/redshift anisotropic quadrupole residual",
            "formula_or_test": "require |R_clock_Q|<=tau_clock_Q",
            "needed_inputs": "clock geometry; redshift convention; projection Pi_clock_Q",
            "current_value": "MISSING_CLOCK_QUADRUPOLE_BOUND",
            "units": "dimensionless",
            "target": "clock_redshift;clock_anisotropy",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "QRI4480_6_tau_orbital_Q",
            "quantity": "tau_orbital_Q",
            "definition": "empirical orbital/ephemeris bound for source quadrupole residual",
            "formula_or_test": "require |R_orbital_Q|<=tau_orbital_Q",
            "needed_inputs": "orbital data bound; source-domain transfer; projection Pi_orb_Q",
            "current_value": "MISSING_ORBITAL_QUADRUPOLE_BOUND",
            "units": "declared_by_arena",
            "target": "orbital_precession;ephemerides",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "QRI4480_7_tau_Shapiro_Q",
            "quantity": "tau_Shapiro_Q",
            "definition": "empirical line-of-sight Shapiro/light-bending anisotropic quadrupole bound",
            "formula_or_test": "require |A_Q*C_Q*Pi_quad_LOS|<=tau_Shapiro_Q",
            "needed_inputs": "anisotropic Shapiro or light-bending source; LOS geometry; source-domain transfer",
            "current_value": "MISSING_SHAPIRO_QUADRUPOLE_BOUND",
            "units": "declared_by_arena",
            "target": "Shapiro;light_bending",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
    ]


def decision_rows(next_target: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4480_0_zero_route",
            "finding": "a genuine SO(3)-scalar marker profile has Q_M_TF^{ij}=0 by representation theory",
            "consequence": "the clean local branch is mathematically real if the parent carrier alphabet is signed",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4480_1_counterroute",
            "finding": "wave vectors, Poynting/flux directions, spin axes, tidal tensors and boundary normals are exactly the objects that can revive Q_M_TF",
            "consequence": "MTS should not ignore EM/wave-background intuitions; they become explicit carrier rows",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4480_2_scorer_route",
            "finding": "if any l=2 carrier survives, the quadrupole branch is scoreable with a compact-support no-cancellation envelope",
            "consequence": "the next target should source or bound the carrier inventory and empirical l=2 arena tolerances",
            "next_action": next_target,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(
    source_rows: List[Dict[str, object]],
    proof_rows: List[Dict[str, object]],
    scorer_rows: List[Dict[str, object]],
    input_rows: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    sources_ok = all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in source_rows)
    zero_parent_signed = any(
        row.get("proof_id") == "OCZ4480_5_verdict" and row.get("parent_signed") is True
        for row in proof_rows
    )
    scorer_written = all(
        any(row.get("scorer_id") == scorer_id for row in scorer_rows)
        for scorer_id in [
            "QRS4480_0_canonical_STF_amplitude",
            "QRS4480_1_local_projection_bound",
            "QRS4480_6_no_cancellation_envelope",
        ]
    )
    inputs_ready = all(
        "MISSING" not in str(row.get("current_value", "")) and row.get("valid_for_claim") is True
        for row in input_rows
    )
    return [
        {
            "gate_id": "CG4480_0_sources",
            "claim": "all cited local sources exist and needles are found",
            "gate_pass": sources_ok,
            "claim_allowed": False,
            "detail": "source register validates 4479 handoff plus prior quadrupole/orientation clues",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4480_1_orientation_zero_theorem_written",
            "claim": "SO(3) scalar marker implies Q_M_TF=0",
            "gate_pass": any(row.get("proof_id") == "OCZ4480_0_SO3_scalar_profile_theorem" for row in proof_rows),
            "claim_allowed": False,
            "detail": "representation theorem is written as a conditional branch",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4480_2_orientation_zero_parent_signed",
            "claim": "MTS parent signs absence of all l=2 orientation carriers",
            "gate_pass": zero_parent_signed,
            "claim_allowed": False,
            "detail": "carrier alphabet, wave/Poynting route and boundary orientation remain unsigned",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4480_3_quadrupole_scorer_written",
            "claim": "finite quadrupole branch has scorer formulas",
            "gate_pass": scorer_written,
            "claim_allowed": False,
            "detail": "canonical amplitude, local bound, Shapiro/clock/orbital/PPN contracts and no-cancellation envelope are written",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4480_4_bound_inputs_ready",
            "claim": "quadrupole scorer has numeric/source-ready arena inputs",
            "gate_pass": inputs_ready,
            "claim_allowed": False,
            "detail": "epsilon_Q, A_STF, carrier inventory and empirical l=2 bounds remain missing",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4480_5_no_generated_claim_rows",
            "claim": "no generated row is promoted to local-GR evidence",
            "gate_pass": all(
                str(row.get("valid_for_claim")).lower() == "false"
                for group in [source_rows, proof_rows, scorer_rows, input_rows]
                for row in group
            ),
            "claim_allowed": False,
            "detail": "4480 is a conditional zero theorem plus finite quadrupole scoring contract",
            "valid_for_claim": False,
        },
    ]
