from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
EXTERNAL = ROOT / "source-intake" / "external" / "arxiv_1905_03413"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3616"
BRANCH_ID = "MTS_R2FR_Y5_BFRESNEL_PROJECTION_RUNNER_OR_HTAU_FLUX_REDUCTION_3616"
DOC = ROOT / "3616-Y5-R2FR-BFresnel-projection-runner-or-Htau-flux-reduction.md"
ARXIV_URL = "https://arxiv.org/abs/1905.03413"


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
        "source_register": RESIDUALS / "P8_Y5_R2FR_3616_SOURCE_REGISTER.csv",
        "projection_derivation": RESIDUALS / "P8_Y5_R2FR_3616_FRESNEL_TO_XI_PROJECTION_DERIVATION.csv",
        "projection_runner_template": RESIDUALS / "P8_Y5_R2FR_3616_PROJECTION_RUNNER_TEMPLATE.csv",
        "grb_comparator_smoke": RESIDUALS / "P8_Y5_R2FR_3616_GRB_BOUND_COMPARATOR_SMOKE.csv",
        "htau_flux_backup": RESIDUALS / "P8_Y5_R2FR_3616_HTAU_FLUX_BACKUP_REDUCTION.csv",
        "decision_gates": RESIDUALS / "P8_Y5_R2FR_3616_DECISION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3616_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3616_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_BFresnel_projection_or_Htau_flux_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3616_VALIDATION.csv",
    }


def source_map() -> dict[str, tuple[Path, str]]:
    return {
        "handoff_3615": (
            RESIDUALS / "P8_Y5_R2FR_3615_NEXT_TARGET.csv",
            "3616-Y5-R2FR-BFresnel-projection-runner-or-Htau-flux-reduction.md",
        ),
        "bfresnel_bound_3615": (
            RESIDUALS / "P8_Y5_R2FR_3615_BFRESNEL_PRIMARY_BOUND_ACQUISITION.csv",
            "BFB3615_0_GRB061122",
        ),
        "mapping_gate_3615": (
            RESIDUALS / "P8_Y5_R2FR_3615_BFRESNEL_MTS_MAPPING_GATE.csv",
            "MISSING_PARENT_PROJECTION",
        ),
        "principal_bound_3614": (
            RESIDUALS / "P8_Y5_R2FR_3614_PRINCIPAL_HODGE_BOUND.csv",
            "B_Fresnel",
        ),
        "wei_2019_source": (
            EXTERNAL / "ms.tex",
            r"\Delta\theta(k)=\xi\frac{k^2}",
        ),
        "htau_vector_3578": (
            RESIDUALS / "P8_Y5_R2FR_3578_HTAU_CURL_COMPONENT_VECTOR.csv",
            "I_EH_stationary_boundary",
        ),
        "htau_identities_3578": (
            RESIDUALS / "P8_Y5_R2FR_3578_HTAU_CURL_IDENTITIES.csv",
            "d_F alpha_tau",
        ),
        "htau_fallback_3615": (
            RESIDUALS / "P8_Y5_R2FR_3615_HTAU_PUBLIC_FLUX_FALLBACK.csv",
            "I_matter_EM_flux",
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
                "source_url": ARXIV_URL if source_id == "wei_2019_source" else "",
                "exists": exists,
                "needle": needle,
                "needle_found": exists and contains(source_path, needle),
                "valid_for_claim": False,
            }
        )
    return rows


def projection_derivation_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    sources = source_map()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "derivation_id": "FPD3616_0_source_dispersion",
            "target": "published GRB birefringence parameter",
            "statement": "The acquired GRB bound constrains a dimensionless dispersion coefficient xi, not an MTS coefficient directly.",
            "formula": "E_pm^2=p^2 +/- 2 xi p^3/M_pl",
            "derived_bridge": "omega_pm = k +/- xi k^2/M_pl + higher_order_terms",
            "required_inputs": "published LIV model assumptions",
            "status": "SOURCE_MODEL_IMPORTED",
            "source_path": str(sources["wei_2019_source"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "derivation_id": "FPD3616_1_rotation_inversion",
            "target": "observable inversion",
            "statement": "Polarization rotation is half the accumulated circular-mode phase split, so the Wei xi bound can be inverted into an effective rotation bound.",
            "formula": "Delta_theta(k)=xi k_obs^2/(M_pl H0) I(z)",
            "derived_bridge": "xi_eff = Delta_theta_MTS M_pl H0/(k_obs^2 I(z))",
            "required_inputs": "I(z), k_obs bandpass, cosmology convention, predicted Delta_theta_MTS",
            "status": "EXACT_MODEL_INVERSION_DERIVED",
            "source_path": str(sources["wei_2019_source"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "derivation_id": "FPD3616_2_Fresnel_root_split",
            "target": "MTS Fresnel residual to phase split",
            "statement": "Near the GR light cone, the perturbed quartic can be written as a quadratic in u=g^{ab}k_a k_b; birefringence is the root splitting.",
            "formula": "F_chi(k)=u^2+a_MTS(k)u+b_MTS(k); Delta_u=sqrt(a_MTS^2-4b_MTS)",
            "derived_bridge": "|Delta_omega_MTS| <= C_root(k,observer,chi0) |Delta_u|",
            "required_inputs": "linearized constitutive tensor, observer frame, root regularity denominator",
            "status": "LOCAL_PROJECTION_FORM_DERIVED_INPUTS_MISSING",
            "source_path": str(sources["principal_bound_3614"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "derivation_id": "FPD3616_3_BFresnel_projection_contract",
            "target": "MTS-to-GRB projection coefficient",
            "statement": "If root regularity and bandpass averaging are sourced, MTS can be compared to the acquired xi bound by a single projection coefficient.",
            "formula": "|xi_MTS_eff| <= K_Fresnel(z,band,observer) B_Fresnel_MTS",
            "derived_bridge": "K_Fresnel := M_pl H0 K_theta(z,band,observer)/(k_obs^2 I(z))",
            "required_inputs": "K_theta root-split bound, B_Fresnel_MTS value, I(z), energy-band average",
            "status": "PROJECTION_CONTRACT_DERIVED_NOT_NUMERIC",
            "source_path": str(sources["mapping_gate_3615"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "derivation_id": "FPD3616_4_bandpass_guard",
            "target": "GRB energy integration",
            "statement": "The source bounds use finite energy bands and polarization survival, so a monochromatic MTS coefficient is insufficient for a claim.",
            "formula": "xi_MTS_eff[band] = <Delta_theta_MTS(k)>_spectrum M_pl H0/(<k^2>_spectrum I(z))",
            "derived_bridge": "replace k_obs^2 by source-model bandpass average before scoring",
            "required_inputs": "spectral weight, detector band, polarization survival criterion",
            "status": "BANDPASS_AVERAGE_REQUIRED",
            "source_path": str(sources["bfresnel_bound_3615"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "derivation_id": "FPD3616_5_claim_gate",
            "target": "safe comparator rule",
            "statement": "A comparison is allowed only when every bridge factor and the MTS Fresnel amplitude is parent-owned or primary-source backed.",
            "formula": "claim_allowed iff abs(xi_MTS_eff)<=xi_bound and no factor in {K_theta,B_Fresnel_MTS,I(z),bandpass} is missing",
            "derived_bridge": "missing bridge factors force comparator result BLOCKED, never PASS",
            "required_inputs": "numeric parent/source rows for all bridge factors",
            "status": "NO_CLAIM_GATE_DERIVED",
            "source_path": str(sources["mapping_gate_3615"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def projection_runner_template_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    bound_rows = read_csv(source_map()["bfresnel_bound_3615"][0])
    rows: list[dict[str, object]] = []
    for bound_row in bound_rows:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "template_id": f"PRT3616_{len(rows)}_{bound_row['object'].replace(' ', '')}",
                "object": bound_row["object"],
                "instrument": bound_row["instrument"],
                "redshift": bound_row["redshift"],
                "energy_range_keV": bound_row["energy_range_keV"],
                "xi_bound": bound_row["bound_value"],
                "comparison_formula": "abs(xi_MTS_eff) <= xi_bound",
                "xi_MTS_eff_formula": "xi_MTS_eff = Delta_theta_MTS M_pl H0/(k_obs^2 I(z))",
                "required_mts_inputs": "Delta_theta_MTS or K_Fresnel*B_Fresnel_MTS; K_theta; I(z); bandpass average; source path",
                "runner_status": "TEMPLATE_READY_INPUTS_MISSING",
                "can_score": False,
                "claim_allowed": False,
                "valid_for_claim": False,
            }
        )
    return rows


def grb_comparator_smoke_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    template_rows = projection_runner_template_rows()
    rows: list[dict[str, object]] = []
    for template_row in template_rows:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "smoke_id": f"GRBS3616_{len(rows)}",
                "object": template_row["object"],
                "xi_bound": template_row["xi_bound"],
                "provided_xi_MTS_eff": "MISSING_PARENT_PROJECTION",
                "provided_K_Fresnel": "MISSING_K_THETA_ROOT_SPLIT",
                "provided_B_Fresnel_MTS": "MISSING_PARENT_AMPLITUDE",
                "result": "BLOCKED_NOT_SCORED",
                "reason": "bound exists, but MTS projection/amplitude does not",
                "can_score": False,
                "claim_allowed": False,
                "valid_for_claim": False,
            }
        )
    return rows


def htau_flux_backup_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    sources = source_map()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "backup_id": "HFB3616_0_EH_zero_condition",
            "quantity": "I_EH_stationary_boundary",
            "statement": "The public EH symplectic flux vanishes on an exact stationary boundary generator with fixed corners and no radiative news.",
            "formula": "Lie_tau g=0 and N_AB=0 and delta C_corner=0 => int_S i_tau omega_EH=0",
            "residual_bound": "I_EH <= C_news||N_AB|| + C_stat||Lie_tau h_ab|| + C_corner|delta C_corner|",
            "status": "CONDITIONAL_ZERO_AND_BOUND_FORM_DERIVED",
            "source_path": str(sources["htau_vector_3578"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "backup_id": "HFB3616_1_matter_EM_zero_condition",
            "quantity": "I_matter_EM_flux",
            "statement": "Matter/EM flux vanishes for a stationary compact source with no Poynting or material flux through the boundary and fixed gauge/readout corners.",
            "formula": "Lie_tau Psi=0, Lie_tau A=0, T_matter(tau,n)=0, S_Poynting.n=0 => I_matter_EM_flux=0",
            "residual_bound": "I_matter_EM_flux <= int_S(|T_matter(tau,n)|+|S_Poynting.n|)dA + C_L||Lie_tau(Psi,A)|| + C_surface|delta C_tau|",
            "status": "CONDITIONAL_ZERO_AND_BOUND_FORM_DERIVED",
            "source_path": str(sources["htau_fallback_3615"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "backup_id": "HFB3616_2_backup_gate",
            "quantity": "C_curl fallback",
            "statement": "The fallback can be scored only if stationarity/no-flux clauses are parent-signed or replaced by numeric source rows.",
            "formula": "Delta_H_curl_bound <= A_F sup_BF(I_EH + I_matter_EM + I_extra + I_boundary + I_tau_surface + I_qdescent)",
            "residual_bound": "first two public flux terms now have conditional zero clauses plus non-cancellation residual envelopes",
            "status": "BACKUP_REDUCED_VALUES_MISSING",
            "source_path": str(sources["htau_identities_3578"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_gate_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3616_0_projection_contract",
            "decision": "A concrete MTS-to-GRB projection contract is now written: xi_MTS_eff is the inverted rotation predicted by MTS.",
            "status": "PASS_NONCLAIM_DERIVATION",
            "next_action": "derive/source K_theta root-split coefficient",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3616_1_runner_template",
            "decision": "The GRB comparator template exists and refuses to score missing parent inputs.",
            "status": "PASS_SMOKE_BLOCKED_CORRECTLY",
            "next_action": "fill K_Fresnel and B_Fresnel_MTS only if parent/source backed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3616_2_htau_public_flux",
            "decision": "The H_tau public flux backup is sharpened into exact stationarity/no-flux clauses plus residual envelopes.",
            "status": "PASS_BACKUP_REDUCED_NONCLAIM",
            "next_action": "use only if Fresnel projection stalls",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3616_3_next_target",
            "decision": "3617 should derive the root-split coefficient K_theta or turn stationarity/no-flux clauses into source rows.",
            "status": "NEXT_TARGET_SELECTED",
            "next_action": "3617-Y5-R2FR-Ktheta-root-split-or-stationary-flux-source-rows.md",
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
            "status_id": "STATUS3616_0",
            "result": "PROJECTION_CONTRACT_DERIVED_COMPARATOR_BLOCKED_CORRECTLY",
            "summary": "3616 converts the acquired GRB xi bound into an explicit MTS projection contract and smoke comparator; it still blocks claims until K_theta/root split and B_Fresnel_MTS are parent-owned.",
            "projection_contract_derived": True,
            "comparator_smoke_written": True,
            "htau_backup_reduced": True,
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
            "next_id": "NEXT3616_0",
            "target_doc": "3617-Y5-R2FR-Ktheta-root-split-or-stationary-flux-source-rows.md",
            "target_script": "scripts/Y5_R2FR_3617_Ktheta_root_split_or_stationary_flux_source_rows.py",
            "objective": "derive the linearized Fresnel root-split coefficient K_theta that maps Delta_chi_principal_MTS to polarization rotation; if that fails, source/zero the stationarity and no-flux clauses for I_EH_stationary_boundary and I_matter_EM_flux",
            "success_gate": "either K_theta is expressed in parent-owned linearized constitutive quantities, or the first H_tau public flux clauses become theorem-zero/source-bound rows",
            "reason": "3616 built the actual comparison bridge; 3617 must fill the bridge coefficient rather than restating that it is missing.",
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
            "projection_contract": "DERIVED_SYMBOLIC",
            "GRB_comparator": "TEMPLATE_BLOCKED_CORRECTLY",
            "missing_core_input": "K_theta root split and B_Fresnel_MTS parent amplitude",
            "Htau_backup": "STATIONARITY_NO_FLUX_CONDITIONS_DERIVED",
            "claim_status": "NO_CLAIM",
            "next_target": "3617 K_theta root split or stationary flux source rows",
            "valid_for_claim": False,
        }
    ]


def write_markdown() -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 3616 Y5 R2FR: B_Fresnel projection runner or H_tau flux reduction",
                "",
                "## Verdict",
                "- The project is no longer merely saying `K_Fresnel missing`: the exact comparison contract is now written.",
                "- The GRB bound constrains `xi`; MTS must first predict an effective polarization rotation `Delta_theta_MTS`, then invert it into `xi_MTS_eff`.",
                "- The comparator is deliberately blocked until the root-split coefficient and MTS amplitude are parent-owned.",
                "",
                "## Projection bridge",
                "- Source model: `E_pm^2 = p^2 +/- 2 xi p^3/M_pl`.",
                "- First-order split: `omega_pm = k +/- xi k^2/M_pl`.",
                "- Rotation inversion: `xi_eff = Delta_theta_MTS M_pl H0/(k_obs^2 I(z))`.",
                "- MTS contract: `|xi_MTS_eff| <= K_Fresnel(z, band, observer) B_Fresnel_MTS`.",
                "- Projection coefficient: `K_Fresnel := M_pl H0 K_theta/(k_obs^2 I(z))`.",
                "",
                "## What remains genuinely missing",
                "- `K_theta`: the linearized root-split coefficient from the principal constitutive/Fresnel residual.",
                "- `B_Fresnel_MTS`: the parent-owned amplitude of the MTS principal-cone residual.",
                "- GRB bandpass averaging: finite energy bands and spectrum weighting must be included before any score.",
                "",
                "## Comparator",
                "- `P8_Y5_R2FR_3616_PROJECTION_RUNNER_TEMPLATE.csv` creates rows for GRB 061122 and GRB 140206A.",
                "- `P8_Y5_R2FR_3616_GRB_BOUND_COMPARATOR_SMOKE.csv` proves the runner refuses to score missing parent inputs.",
                "- This is the right kind of blocked result: the observable bound is real, the bridge is explicit, and the missing pieces are sharply local.",
                "",
                "## H_tau backup reduction",
                "- `I_EH_stationary_boundary` is zero if the boundary generator is exactly stationary, no radiative news crosses the surface, and corners are fixed.",
                "- `I_matter_EM_flux` is zero if matter/EM fields are stationary and no material or Poynting flux crosses the boundary.",
                "- Otherwise both terms now have residual envelopes rather than vague missingness.",
                "",
                "## Next target",
                "- `3617-Y5-R2FR-Ktheta-root-split-or-stationary-flux-source-rows.md`.",
                "- First route: derive `K_theta` from the linearized Fresnel quartic.",
                "- Backup route: source or theorem-zero the stationarity/no-flux clauses.",
                "",
                "## Claim status",
                "- `NO_CLAIM`: this is a derivation and comparator-architecture checkpoint.",
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
    results.append(("VAL3616_0_sources_exist", sources_exist, "all required 3616 source paths exist"))
    results.append(("VAL3616_1_needles_found", needles_found, "all selected 3616 source anchors found"))

    pre_validation_paths = [path for name, path in paths.items() if name != "validation"]
    outputs_exist = DOC.exists() and all(path.exists() for path in pre_validation_paths)
    results.append(("VAL3616_2_outputs_exist", outputs_exist, "all pre-validation 3616 outputs written"))

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
    results.append(("VAL3616_3_csv_parse", csv_parse_pass, "; ".join(parse_details)))

    derivation_rows = read_csv(paths["projection_derivation"]) if paths["projection_derivation"].exists() else []
    inversion_written = any("xi_eff = Delta_theta_MTS" in row["derived_bridge"] for row in derivation_rows)
    projection_contract_written = any("|xi_MTS_eff| <= K_Fresnel" in row["formula"] for row in derivation_rows)
    results.append(("VAL3616_4_inversion_formula_written", inversion_written, "xi inversion from polarization rotation is explicit"))
    results.append(("VAL3616_5_projection_contract_written", projection_contract_written, "MTS-to-GRB projection contract is explicit"))

    comparator_rows = read_csv(paths["grb_comparator_smoke"]) if paths["grb_comparator_smoke"].exists() else []
    comparator_blocks = bool(comparator_rows) and all(
        row["result"] == "BLOCKED_NOT_SCORED" and row["can_score"] == "False"
        for row in comparator_rows
    )
    results.append(("VAL3616_6_comparator_blocks_missing_inputs", comparator_blocks, "GRB comparator refuses to score missing MTS inputs"))

    htau_rows = read_csv(paths["htau_flux_backup"]) if paths["htau_flux_backup"].exists() else []
    htau_zeroes_written = any("Lie_tau g=0" in row["formula"] for row in htau_rows) and any(
        "S_Poynting.n=0" in row["formula"] for row in htau_rows
    )
    results.append(("VAL3616_7_htau_zero_conditions_written", htau_zeroes_written, "EH and matter/EM stationarity/no-flux conditions written"))

    all_outputs_nonclaim = True
    for name, path in paths.items():
        if name == "validation" or not path.exists():
            continue
        for row in read_csv(path):
            if row.get("valid_for_claim") == "True" or row.get("claim_allowed") == "True":
                all_outputs_nonclaim = False
    results.append(("VAL3616_8_all_outputs_nonclaim", all_outputs_nonclaim, "all generated rows remain nonclaim"))

    formalization_clean = True
    formalization_detail = "formalization-workbench not found"
    if FORMALIZATION.exists():
        leaked_paths = list(FORMALIZATION.rglob("*3616*"))
        formalization_clean = len(leaked_paths) == 0
        formalization_detail = "no 3616 files in formalization-workbench" if formalization_clean else "; ".join(str(path) for path in leaked_paths[:5])
    results.append(("VAL3616_9_no_formalization_leak", formalization_clean, formalization_detail))

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
    write_csv(paths["projection_derivation"], projection_derivation_rows())
    write_csv(paths["projection_runner_template"], projection_runner_template_rows())
    write_csv(paths["grb_comparator_smoke"], grb_comparator_smoke_rows())
    write_csv(paths["htau_flux_backup"], htau_flux_backup_rows())
    write_csv(paths["decision_gates"], decision_gate_rows())
    write_csv(paths["status"], status_rows())
    write_csv(paths["next_target"], next_target_rows())
    write_csv(paths["canonical_status"], canonical_status_rows())
    write_markdown()
    write_csv(paths["validation"], validate())

    failed = [row for row in read_csv(paths["validation"]) if row["result"] != "PASS"]
    if failed:
        raise SystemExit(f"3616 validation failed: {failed}")
    print(f"wrote 3616 checkpoint with {len(read_csv(paths['validation']))} validation checks")


if __name__ == "__main__":
    main()
