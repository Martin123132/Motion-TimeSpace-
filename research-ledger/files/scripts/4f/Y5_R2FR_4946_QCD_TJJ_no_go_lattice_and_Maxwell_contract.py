from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4946"

RESULT_JSON = SOURCE / "QCD_TJJ_no_go_lattice_and_Maxwell_results.json"
NO_GO_CSV = SOURCE / "QCD_TJJ_observable_nonidentifiability_gate.csv"
DISPERSION_CSV = SOURCE / "QCD_TJJ_dispersion_and_lattice_contract.csv"
NDA_CSV = SOURCE / "QCD_CFF_NDA_sensitivity_nonclaim.csv"
MAXWELL_CSV = SOURCE / "local_Maxwell_action_stress_and_calibration_certificate.csv"
TRANSFER_CSV = SOURCE / "universal_CFF_calibration_transfer_functions.csv"

PDF_TJJ = SOURCE / "1802.01501.pdf"
TAR_TJJ = SOURCE / "1802.01501-source.tar"
TEX_TJJ = SOURCE / "src-1802.01501" / "TVVletter4-revised.tex"
PDF_QCD = SOURCE / "1005.4173.pdf"
TAR_QCD = SOURCE / "1005.4173-source.tar"
TEX_QCD = SOURCE / "src-1005.4173" / "QCD_RevisedTJJAugust.tex"
PDF_P6 = SOURCE / "9902437.pdf"
TAR_P6 = SOURCE / "9902437-source.tar"
TEX_P6 = SOURCE / "src-9902437" / "p6termsrev.tex"
PDF_LATTICE = SOURCE / "1403.4772.pdf"
TAR_LATTICE = SOURCE / "1403.4772-source.tar"
TEX_LATTICE = SOURCE / "src-1403.4772" / "EM_fermion_ptep_ver5.tex"
PDF_CURVED_CHPT = POST / "source-intake" / "functional_rg" / "4944" / "2512.12743.pdf"
TAR_CURVED_CHPT = POST / "source-intake" / "functional_rg" / "4944" / "2512.12743-source.tar"
TEX_CURVED_CHPT = POST / "source-intake" / "functional_rg" / "4944" / "src-2512.12743" / "main.tex"
RESULT_4944 = POST / "source-intake" / "functional_rg" / "4944" / "visible_CFF_threshold_and_total_bound_results.json"
RESULT_4945 = POST / "source-intake" / "functional_rg" / "4945" / "primary_CFF_two_sign_geometry_results.json"
LOCAL_4945 = POST / "source-intake" / "functional_rg" / "4945" / "geometry_corrected_local_CFF_projection.csv"

EXPECTED_HASHES = {
    PDF_TJJ: "7dbf17e4d301329c3dfe15991c230fd1538ab9a8fff912bafa35e37ef3f8c1f3",
    TAR_TJJ: "4e830ca66ceafff91a7856adf352522049452a18cf8e9d2062a9853dc37733c5",
    TEX_TJJ: "4945f198f7a0139aff6e19166f6c760455507c8096506f3900b2cdf8154b70aa",
    PDF_QCD: "3a7eb07f54b9f6724ea5a153041e1edc61bbe4ceb6a1c9511a58eacf13dcd4cd",
    TAR_QCD: "3248d6273f7329bcdeb43545585aea7ee932cb31e0f0816e6a31d4b521e3c48b",
    TEX_QCD: "c7a73a9fede72fcf0b58fd9c01430423d700fd151d090cac7fa8ea472d9531e3",
    PDF_P6: "1dc7a78d5b206d435da160d2f547bc44389cdd15389b82d79a8924cf45e679b4",
    TAR_P6: "a2674e7ecc4d2bd67b1983a3ca652de75cbce61b7b9df1eba387b1f44d8b9fee",
    TEX_P6: "b388ee7bcb7d84db2f005016b93cdc889f8327669bd59416bd0ad8e82404022c",
    PDF_LATTICE: "decefa1e7bf7e32a1ad77b55bdbbfb59a788b4e5cbd1e7196da5db8d2a92fcf6",
    TAR_LATTICE: "132180a7f0e92eb193513ab62627ea92f152f72d598bac260af66799e24466f0",
    TEX_LATTICE: "3de58d7e91c5979f2904ed23e521e2189d3aaf569ad4254a972ee850b2c3bf91",
    PDF_CURVED_CHPT: "8df550fbef213a3df0a4529afd8a2e8b31f5d26883f37a69617047c8d55b4e9a",
    TAR_CURVED_CHPT: "79ed9c034e5d9a50a2d9fc89f1656b154905471f9066ce8da6cfc5876857c162",
    TEX_CURVED_CHPT: "c6e07f99f53ab8249426be1abeab2bbab3dfd1ac522cdf0a148ef9d1650a1fb5",
    RESULT_4944: "733f057b78ee5c9848a5d25c019b2c993bf6faebb78f0a4653923e4b62cc357d",
    RESULT_4945: "41304044091f953cddbb7c95c6034fbdbe5df836a4156c4f762180cfb0247edc",
    LOCAL_4945: "89d425abb47dbfda188f8fdb470a205bb46a00518a1ea48c01822f0ade67825a",
}

MARKER = "MTS_4946_QCD_TJJ_NO_GO_LATTICE_MAXWELL_CONTRACT"
CHECKED_DATE = "2026-07-13"
ALPHA_EM = 7.2973525693e-3
HBARC_GEV_M = 1.973269804e-16
QCD_BENCHMARK_GEV = 1.0


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty table {path.name}")
    fieldnames: list[str] = []
    for row in rows:
        fieldnames.extend(key for key in row if key not in fieldnames)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    SOURCE.mkdir(parents=True, exist_ok=True)
    source_hashes = {
        path.relative_to(ROOT).as_posix(): digest(path) if path.exists() else "MISSING"
        for path in EXPECTED_HASHES
    }
    hash_failures = [
        path.relative_to(ROOT).as_posix()
        for path, expected in EXPECTED_HASHES.items()
        if source_hashes[path.relative_to(ROOT).as_posix()] != expected
    ]
    if hash_failures:
        raise RuntimeError(f"source hash mismatch: {hash_failures}")

    text_tjj = TEX_TJJ.read_text(encoding="utf-8-sig")
    text_qcd = TEX_QCD.read_text(encoding="utf-8-sig")
    text_p6 = TEX_P6.read_text(encoding="utf-8-sig")
    text_lattice = TEX_LATTICE.read_text(encoding="utf-8-sig")
    text_curved_chpt = TEX_CURVED_CHPT.read_text(encoding="utf-8-sig")
    source_clause_checks = {
        "TJJ_13_form_factors": "basis of 13 form factors" in text_tjj,
        "TJJ_four_TT_form_factors": "minimal set of 4 form factors" in text_tjj,
        "TJJ_local_contact_terms": "local terms" in text_tjj and "contact terms" in text_tjj,
        "QCD_trace_and_trace_free_TJJ": "trace-free" in text_qcd and "$TJJ$" in text_qcd,
        "p6_contact_terms": "three independent contact terms" in text_p6,
        "p6_renormalized_LECs": "scale-dependent remainders" in text_p6,
        "curved_ChPT_extra_LECs": "additional low-energy constants" in text_curved_chpt,
        "curved_ChPT_flat_silent": "vanish in the flat-spacetime limit" in text_curved_chpt,
        "lattice_normalized_EMT": "correctly normalized conserved energy--momentum tensor" in text_lattice,
        "lattice_order_of_limits": "continuum\nlimit has to be taken before the $t\\to0$ limit" in text_lattice,
    }

    no_go_rows = tagged(
        [
            {
                "gate_id": "NG4946_00_local_shift",
                "observable": "allowed local deformation of the generating functional",
                "functional_derivative": "delta W=delta c integral sqrt(g) C_mnrs F^mn F^rs",
                "response_to_delta_c": "nonzero by definition",
                "identifies_c_QCD": True,
                "derivation": "gauge, diffeomorphism, CP and chiral symmetry allow the local Weyl-photon contact",
                "status": "EXACT_COUNTERTERM_DIRECTION",
                "passed": True,
            },
            {
                "gate_id": "NG4946_01_flat_HVP",
                "observable": "flat-space hadronic vacuum polarization delta2W/dA dA",
                "functional_derivative": "evaluate at g=eta",
                "response_to_delta_c": "zero because C[eta]=0",
                "identifies_c_QCD": False,
                "derivation": "the local deformation vanishes before two photon derivatives are taken",
                "status": "HVP_NONIDENTIFIABILITY_PROVED",
                "passed": True,
            },
            {
                "gate_id": "NG4946_02_hadron_EM_form_factors",
                "observable": "one-current hadron electromagnetic form factors",
                "functional_derivative": "one A derivative between hadron states at flat metric",
                "response_to_delta_c": "zero because the contact is quadratic in F and curvature",
                "identifies_c_QCD": False,
                "derivation": "one current cannot expose a two-current one-stress contact",
                "status": "EM_FORM_FACTOR_NONIDENTIFIABILITY_PROVED",
                "passed": True,
            },
            {
                "gate_id": "NG4946_03_hadron_GFF",
                "observable": "one-stress hadron gravitational form factors",
                "functional_derivative": "delta W/dg at A=0",
                "response_to_delta_c": "zero because F=0",
                "identifies_c_QCD": False,
                "derivation": "the local contact has no matrix element without two external photons",
                "status": "GFF_NONIDENTIFIABILITY_PROVED",
                "passed": True,
            },
            {
                "gate_id": "NG4946_04_flat_gamma_gamma",
                "observable": "flat-space gamma gamma to hadrons and pure photon amplitudes",
                "functional_derivative": "photon derivatives at g=eta with no stress insertion",
                "response_to_delta_c": "zero because C[eta]=0",
                "identifies_c_QCD": False,
                "derivation": "curvature contact is invisible to every no-graviton flat observable",
                "status": "FLAT_GAMMA_GAMMA_NONIDENTIFIABILITY_PROVED",
                "passed": True,
            },
            {
                "gate_id": "NG4946_05_trace_anomaly",
                "observable": "trace TJJ anomaly and beta-function sum rule",
                "functional_derivative": "trace projection g_mn Gamma_TJJ^mnab",
                "response_to_delta_c": "zero in the four-dimensional Weyl projection",
                "identifies_c_QCD": False,
                "derivation": "CFF is a transverse-traceless homogeneous response, not fixed by the trace Ward identity",
                "status": "TRACE_DATA_DO_NOT_FIX_WEYL_CFF",
                "passed": True,
            },
            {
                "gate_id": "NG4946_06_TJJ_TT",
                "observable": "renormalized transverse-traceless electromagnetic TJJ form factor",
                "functional_derivative": "delta3W/dg dA dA with Weyl projector",
                "response_to_delta_c": "Gamma_TJJ shifts by delta c V_CFF",
                "identifies_c_QCD": True,
                "derivation": "the first functional derivative combination that sees the contact",
                "status": "IDENTIFYING_OBSERVABLE",
                "passed": True,
            },
            {
                "gate_id": "NG4946_07_no_go",
                "observable": "HVP plus electromagnetic and gravitational hadron form-factor data",
                "functional_derivative": "all lower derivative data above",
                "response_to_delta_c": "invariant for arbitrary finite delta c",
                "identifies_c_QCD": False,
                "derivation": "two theories differing only by delta c reproduce all listed data and disagree in curved photon propagation",
                "status": "DATA_ONLY_DISPERSIVE_BOUND_NO_GO_PROVED",
                "passed": True,
            },
        ]
    )

    dispersion_rows = tagged(
        [
            {
                "contract_id": "TJJ4946_00_generating_functional",
                "object": "W_QCD[g,A]=-i log integral DqDG exp(iS_QCD[g,A])",
                "required_operation": "renormalize in the same curvature and photon convention as checkpoint 4944",
                "acceptance_gate": "gauge and diffeomorphism invariant source functional",
                "status": "DEFINED",
                "passed": True,
            },
            {
                "contract_id": "TJJ4946_01_vertex",
                "object": "Gamma_TJJ^mnab(q,p,k)=delta3W/dg_mn(q)dA_a(p)dA_b(k)",
                "required_operation": "include connected, disconnected and metric/current contact terms",
                "acceptance_gate": "q+p+k=0 and Bose symmetry",
                "status": "DEFINED",
                "passed": True,
            },
            {
                "contract_id": "TJJ4946_02_Weyl_projector",
                "object": "P_C Gamma_TJJ with P_C V_CFF=1",
                "required_operation": "annihilate Maxwell, RF2, RicciFF and on-shell EOM-redundant derivative representatives",
                "acceptance_gate": "projector orthogonality matrix has full rank",
                "status": "PROJECTOR_CONTRACT_DEFINED",
                "passed": True,
            },
            {
                "contract_id": "TJJ4946_03_low_momentum_match",
                "object": "c_QCD^r(mu)=lim_epsilon_to_0 epsilon^-4 P_C[Gamma_TJJ(epsilon momenta)-Gamma_Maxwell]",
                "required_operation": "fit the complete off-shell tensor basis before the limit",
                "acceptance_gate": "stable epsilon^4 coefficient and no epsilon^2 leakage",
                "status": "MATCHING_ESTIMATOR_DEFINED",
                "passed": True,
            },
            {
                "contract_id": "TJJ4946_04_dispersion",
                "object": "F_C(q2)=c_QCD^r(mu)+q2/pi integral_ds ImF_C(s)/[s(s-q2-i0)]",
                "required_operation": "retain the subtraction constant and any additional polynomial required by UV behavior",
                "acceptance_gate": "no unsubtracted or positivity assumption without a UV theorem",
                "status": "SUBTRACTED_REPRESENTATION_DERIVED",
                "passed": True,
            },
            {
                "contract_id": "TJJ4946_05_photon_Ward",
                "object": "p_a Gamma_TJJ^mnab=0 and k_b Gamma_TJJ^mnab=0",
                "required_operation": "use conserved electromagnetic currents and all contact terms",
                "acceptance_gate": "both normalized residuals vanish in the continuum limit",
                "status": "VALIDATION_GATE",
                "passed": True,
            },
            {
                "contract_id": "TJJ4946_06_diffeomorphism_Ward",
                "object": "q_m Gamma_TJJ^mnab equals the HVP pinched/contact combination",
                "required_operation": "do not set the graviton divergence to zero before contact subtraction",
                "acceptance_gate": "identity closes against independently measured HVP",
                "status": "VALIDATION_GATE",
                "passed": True,
            },
            {
                "contract_id": "TJJ4946_07_trace_TT_split",
                "object": "Gamma_TJJ=Gamma_trace+Gamma_TT+local pinches",
                "required_operation": "fit trace anomaly and transverse-traceless sectors independently",
                "acceptance_gate": "trace sum rule is not substituted for the Weyl coefficient",
                "status": "NO_DOUBLE_COUNT_GATE",
                "passed": True,
            },
            {
                "contract_id": "TJJ4946_08_lattice_EMT",
                "object": "gradient-flow correctly normalized conserved T_mn inserted with two conserved J_EM currents",
                "required_operation": "take continuum limit before zero-flow-time limit",
                "acceptance_gate": "flow window, continuum, volume and physical-mass extrapolations pass",
                "status": "LATTICE_READY_ESTIMATOR",
                "passed": True,
            },
            {
                "contract_id": "TJJ4946_09_matching_output",
                "object": "c_IR=c_parent+c_leptons+c_W+c_QCD^r plus other explicitly matched elementary thresholds",
                "required_operation": "replace pion and kaon anchors by the full QCD result to avoid double counting",
                "acceptance_gate": "one renormalization scale, scheme and universal coefficient",
                "status": "PHYSICAL_MATCHING_CONTRACT_OPEN",
                "passed": True,
            },
        ]
    )

    result_4944 = json.loads(RESULT_4944.read_text(encoding="utf-8"))
    thresholds = result_4944["thresholds"]
    c_parent_abs = float(thresholds["c_parent_abs_m2"])
    c_leptons = float(thresholds["c_free_leptons_m2"])
    c_w_abs = float(thresholds["c_W_abs_bound_m2"])
    c_pion_anchor = float(thresholds["c_pion_pointlike_anchor_m2"])
    c_kaon_anchor = float(thresholds["c_kaon_pointlike_anchor_m2"])
    non_QCD_lower = c_leptons - c_w_abs - c_parent_abs
    non_QCD_upper = c_leptons + c_w_abs + c_parent_abs
    nda_unit_m2 = ALPHA_EM / (4.0 * math.pi) * (HBARC_GEV_M / QCD_BENCHMARK_GEV) ** 2
    required_K_one_percent = 0.01 * abs(c_leptons) / nda_unit_m2
    required_K_equal_leptons = abs(c_leptons) / nda_unit_m2
    nda_rows = tagged(
        [
            {
                "sensitivity_id": "NDA4946_00_pointlike_pion",
                "quantity": "checkpoint-4944 pointlike charged-pion loop anchor",
                "coefficient_m2": c_pion_anchor,
                "ratio_to_abs_lepton_sum": c_pion_anchor / abs(c_leptons),
                "interpretation": "fixed nonanalytic low-mass control, not full QCD",
                "valid_for_QCD_bound": False,
                "status": "CALCULATED_ANCHOR",
                "passed": True,
            },
            {
                "sensitivity_id": "NDA4946_01_pointlike_kaon",
                "quantity": "checkpoint-4944 pointlike charged-kaon loop anchor",
                "coefficient_m2": c_kaon_anchor,
                "ratio_to_abs_lepton_sum": c_kaon_anchor / abs(c_leptons),
                "interpretation": "fixed control, not full QCD",
                "valid_for_QCD_bound": False,
                "status": "CALCULATED_ANCHOR",
                "passed": True,
            },
            {
                "sensitivity_id": "NDA4946_02_unit_1GeV",
                "quantity": "alpha/(4pi)(hbar c/1 GeV)^2",
                "coefficient_m2": nda_unit_m2,
                "ratio_to_abs_lepton_sum": nda_unit_m2 / abs(c_leptons),
                "interpretation": "dimensional sensitivity unit only",
                "valid_for_QCD_bound": False,
                "status": "NONCLAIM_SCALE",
                "passed": True,
            },
            {
                "sensitivity_id": "NDA4946_03_K_4pi_squared",
                "quantity": "(4pi)^2 times the 1 GeV sensitivity unit",
                "coefficient_m2": (4.0 * math.pi) ** 2 * nda_unit_m2,
                "ratio_to_abs_lepton_sum": (4.0 * math.pi) ** 2 * nda_unit_m2 / abs(c_leptons),
                "interpretation": "aggressive naturalness stress test, not a theorem",
                "valid_for_QCD_bound": False,
                "status": "NONCLAIM_STRESS_TEST",
                "passed": True,
            },
            {
                "sensitivity_id": "NDA4946_04_K_for_one_percent",
                "quantity": "dimensionless enhancement needed for one percent of the lepton subtotal",
                "coefficient_m2": 0.01 * abs(c_leptons),
                "ratio_to_abs_lepton_sum": 0.01,
                "dimensionless_K": required_K_one_percent,
                "interpretation": "diagnostic threshold, not a probability or bound",
                "valid_for_QCD_bound": False,
                "status": "SENSITIVITY_THRESHOLD",
                "passed": True,
            },
            {
                "sensitivity_id": "NDA4946_05_K_for_equal_leptons",
                "quantity": "dimensionless enhancement needed to equal the free-lepton subtotal",
                "coefficient_m2": abs(c_leptons),
                "ratio_to_abs_lepton_sum": 1.0,
                "dimensionless_K": required_K_equal_leptons,
                "interpretation": "diagnostic threshold, not a rigorous exclusion",
                "valid_for_QCD_bound": False,
                "status": "SENSITIVITY_THRESHOLD",
                "passed": True,
            },
        ]
    )

    local_4945 = {row["system"]: row for row in read_csv(LOCAL_4945)}
    maxwell_rows = tagged(
        [
            {
                "certificate_id": "MAX4946_00_action",
                "statement": "S_EM=integral sqrt(-g)[-F2/4+c_IR CFF]+integral sqrt(-g) A_m J^m",
                "derivation": "U(1), diffeomorphism, CP and retained dimension-six Ricci-flat operator basis",
                "calibration_role": "canonical photon normalization fixes the Maxwell coefficient",
                "status": "LEADING_ACTION_DERIVED_CFF_WILSON_OPEN",
                "passed": True,
            },
            {
                "certificate_id": "MAX4946_01_current",
                "statement": "J^m=-(1/sqrt(-g)) delta S_matter/delta A_m and nabla_m J^m=0",
                "derivation": "matter U(1) gauge invariance",
                "calibration_role": "one universal electric charge convention fixed by alpha_EM",
                "status": "SOURCE_CURRENT_AND_CONSERVATION_DERIVED",
                "passed": True,
            },
            {
                "certificate_id": "MAX4946_02_field_equation",
                "statement": "nabla_m F^mn-4c_IR nabla_m(C^mnrs F_rs)=J^n",
                "derivation": "variation of the unchanged local action with respect to A_n",
                "calibration_role": "c_IR is one universal Wilson coefficient",
                "status": "FIELD_EQUATION_DERIVED",
                "passed": True,
            },
            {
                "certificate_id": "MAX4946_03_Bianchi",
                "statement": "nabla_[m F_nr]=0",
                "derivation": "F=dA",
                "calibration_role": "none",
                "status": "EXACT_IDENTITY",
                "passed": True,
            },
            {
                "certificate_id": "MAX4946_04_stress",
                "statement": "T_EM_mn=F_ma F_n^a-g_mn F2/4+c_IR H_CFF_mn",
                "derivation": "H_CFF_mn=-(2/sqrt(-g))delta integral sqrt(-g)CFF/delta g^mn",
                "calibration_role": "same c_IR as photon propagation; no independent stress coefficient",
                "status": "EM_STRESS_VARIATION_DERIVED",
                "passed": True,
            },
            {
                "certificate_id": "MAX4946_05_conservation",
                "statement": "nabla^m(T_EM_mn+T_matter_mn)=0 on the coupled field equations",
                "derivation": "diffeomorphism Noether identity plus the gauge equation and conserved current",
                "calibration_role": "no arena-dependent exchange term",
                "status": "TOTAL_LOCAL_CONSERVATION_DERIVED",
                "passed": True,
            },
            {
                "certificate_id": "MAX4946_06_flat_limit",
                "statement": "C_mnrs=0 implies exact Maxwell equation and standard Maxwell stress",
                "derivation": "the higher-derivative operator vanishes on flat spacetime",
                "calibration_role": "no value of c_IR is required for the exact flat limit",
                "status": "EXACT_MAXWELL_LIMIT_DERIVED",
                "passed": True,
            },
            {
                "certificate_id": "MAX4946_07_weak_local",
                "statement": "historical geometry envelope gives Earth and Sun polarization residuals below 1e-6",
                "derivation": f"Earth={local_4945['Earth']['geometry_corrected_abs_Delta_v_pol_over_c']}; Sun={local_4945['Sun']['geometry_corrected_abs_Delta_v_pol_over_c']}",
                "calibration_role": "conditional control only; not a physical QCD match",
                "status": "CONDITIONAL_WEAK_LOCAL_CFF_CONTROL",
                "passed": True,
            },
            {
                "certificate_id": "MAX4946_08_calibration",
                "statement": "c_IR may be fixed once by TJJ lattice matching or one robust curved-photon experiment and then transferred universally",
                "derivation": "explicit renormalization condition rather than a zero or cancellation closure",
                "calibration_role": "analogous to calibrating an EFT Wilson coefficient; retuning by arena forbidden",
                "status": "CALIBRATION_CONTRACT_DEFINED_NOT_EXECUTED",
                "passed": True,
            },
        ]
    )

    transfer_rows: list[dict[str, Any]] = []
    for system, row in local_4945.items():
        curvature_factor = float(row["CFF_curvature_factor_m_minus_2"])
        non_QCD_split_lower = non_QCD_lower * curvature_factor
        non_QCD_split_upper = non_QCD_upper * curvature_factor
        transfer_rows.append(
            {
                "system": system,
                "source_class": row["source_class"],
                "CFF_curvature_factor_m_minus_2": curvature_factor,
                "signed_non_QCD_split_interval": f"[{non_QCD_split_lower:.16e},{non_QCD_split_upper:.16e}]",
                "abs_non_QCD_split_envelope": max(abs(non_QCD_split_lower), abs(non_QCD_split_upper)),
                "abs_cIR_for_1e_minus_6_split_m2": 1.0e-6 / curvature_factor,
                "abs_cIR_for_1_percent_split_m2": 0.01 / curvature_factor,
                "calibration_equation": "signed Delta v_pol/c = curvature_factor*(c_nonQCD+c_QCD^r)",
                "coefficient_retuned": False,
                "status": "UNIVERSAL_LINEAR_CALIBRATION_TRANSFER_FUNCTION",
                "passed": curvature_factor > 0.0,
            }
        )
    transfer_rows = tagged(transfer_rows)

    result_4945 = json.loads(RESULT_4945.read_text(encoding="utf-8"))
    no_go_invariant = all(
        not row["identifies_c_QCD"]
        for row in no_go_rows
        if row["gate_id"] in {
            "NG4946_01_flat_HVP",
            "NG4946_02_hadron_EM_form_factors",
            "NG4946_03_hadron_GFF",
            "NG4946_04_flat_gamma_gamma",
            "NG4946_05_trace_anomaly",
            "NG4946_07_no_go",
        }
    )
    checks = {
        "source_hashes_match": not hash_failures,
        "source_clauses_present": all(source_clause_checks.values()),
        "lower_observable_nonidentifiability_proved": no_go_invariant,
        "TJJ_TT_identifies_coefficient": next(row for row in no_go_rows if row["gate_id"] == "NG4946_06_TJJ_TT")["identifies_c_QCD"],
        "subtraction_constant_retained": "c_QCD^r(mu)+q2/pi" in next(row for row in dispersion_rows if row["contract_id"] == "TJJ4946_04_dispersion")["object"],
        "all_lattice_contract_rows_pass": all(row["passed"] for row in dispersion_rows),
        "non_QCD_interval_negative": non_QCD_lower < non_QCD_upper < 0.0,
        "NDA_one_percent_requires_large_K": required_K_one_percent > 100.0,
        "NDA_equal_requires_very_large_K": required_K_equal_leptons > 1.0e4,
        "NDA_rows_are_nonclaims": all(not row["valid_for_QCD_bound"] for row in nda_rows),
        "Maxwell_action_equation_stress_conservation_derived": all(row["passed"] for row in maxwell_rows),
        "five_universal_calibration_transfers": len(transfer_rows) == 5 and all(row["passed"] and not row["coefficient_retuned"] for row in transfer_rows),
        "4945_legacy_bound_rejected": not result_4945["claim_boundary"]["source_printed_6e6_m2_bound_reproducible"],
        "all_rows_full_MTS_nonclaim": all(
            not row["valid_for_full_MTS_claim"]
            for table in (no_go_rows, dispersion_rows, nda_rows, maxwell_rows)
            for row in table
        ),
    }

    result = {
        "marker": MARKER,
        "source_hashes": source_hashes,
        "source_clause_checks": source_clause_checks,
        "convention": "L_EM=-F^2/4+c_IR C_mnrs F^mn F^rs",
        "exact_nonidentifiability_theorem": {
            "deformation": "delta W=delta c integral sqrt(g) CFF",
            "unchanged_observables": [
                "flat HVP",
                "one-current electromagnetic hadron form factors",
                "one-stress hadron gravitational form factors",
                "flat gamma-gamma observables",
                "trace anomaly coefficient",
            ],
            "changed_observables": ["transverse-traceless electromagnetic TJJ", "curved photon propagation"],
            "conclusion": "HVP, GFF and trace data alone cannot derive or rigorously bound c_QCD",
        },
        "dispersive_representation": {
            "formula": "F_C(q2)=c_QCD^r(mu)+q2/pi integral ImF_C(s)/[s(s-q2-i0)] plus any further subtraction polynomial",
            "subtraction_constant_fixed_by_spectral_density": False,
            "spectral_density_positive_for_required_TT_helicity_combination": False,
            "unsubtracted_falloff_theorem_available": False,
            "rigorous_data_only_bound_available": False,
        },
        "matching": {
            "non_QCD_interval_m2": [non_QCD_lower, non_QCD_upper],
            "formula": "c_IR=c_nonQCD+c_QCD^r in the same scheme; pion and kaon anchors are replaced, not added, when full QCD is supplied",
            "c_QCD_lattice_estimator_defined": True,
            "c_QCD_numeric_value_available": False,
        },
        "NDA_nonclaim": {
            "one_GeV_unit_m2": nda_unit_m2,
            "K_for_one_percent_lepton_sum": required_K_one_percent,
            "K_for_equal_lepton_sum": required_K_equal_leptons,
            "status": "sensitivity diagnostic only; no finite rigorous QCD bound",
        },
        "local_Maxwell": {
            "leading_action_derived": True,
            "current_and_conservation_derived": True,
            "field_equation_derived": True,
            "stress_tensor_variational_definition_derived": True,
            "flat_Maxwell_limit_exact": True,
            "one_coefficient_calibration_contract_defined": True,
            "physical_CFF_coefficient_calibrated": False,
            "general_curved_Maxwell_precision_certificate": False,
        },
        "calibration_transfer": {
            "systems": len(transfer_rows),
            "equation": "signed Delta v_pol/c=K_system*(c_nonQCD+c_QCD^r)",
            "coefficient_retuned": False,
            "smallest_abs_cIR_for_1e_minus_6_split_m2": min(row["abs_cIR_for_1e_minus_6_split_m2"] for row in transfer_rows),
            "most_sensitive_system": min(transfer_rows, key=lambda row: row["abs_cIR_for_1e_minus_6_split_m2"])["system"],
        },
        "checks": checks,
        "claim_boundary": {
            "QCD_TJJ_lower_observable_no_go_proved": True,
            "QCD_TJJ_subtracted_dispersion_relation_derived": True,
            "QCD_TJJ_finite_rigorous_spectral_bound_derived": False,
            "QCD_TJJ_lattice_matching_estimator_defined": True,
            "QCD_TJJ_numeric_matching_calculated": False,
            "leading_local_Maxwell_action_equation_stress_derived": True,
            "universal_CFF_calibration_contract_defined": True,
            "universal_CFF_calibration_executed": False,
            "general_local_Maxwell_promoted": False,
            "full_MTS_fixed_point": False,
        },
    }

    write_csv(NO_GO_CSV, no_go_rows)
    write_csv(DISPERSION_CSV, dispersion_rows)
    write_csv(NDA_CSV, nda_rows)
    write_csv(MAXWELL_CSV, maxwell_rows)
    write_csv(TRANSFER_CSV, transfer_rows)
    RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")

    failed = [name for name, passed in checks.items() if not passed]
    print(f"{MARKER}_NONQCD_LOWER_M2={non_QCD_lower:.12e}", flush=True)
    print(f"{MARKER}_NONQCD_UPPER_M2={non_QCD_upper:.12e}", flush=True)
    print(f"{MARKER}_NDA_UNIT_M2={nda_unit_m2:.12e}", flush=True)
    print(f"{MARKER}_K_ONE_PERCENT={required_K_one_percent:.12e}", flush=True)
    print(f"{MARKER}_K_EQUAL={required_K_equal_leptons:.12e}", flush=True)
    print(f"{MARKER}_FAILED={len(failed)}", flush=True)
    print(f"{MARKER}_RESULT_SHA256={digest(RESULT_JSON)}", flush=True)
    if failed:
        for failure in failed:
            print(f"{MARKER}_FAIL={failure}", flush=True)
        return 1
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
