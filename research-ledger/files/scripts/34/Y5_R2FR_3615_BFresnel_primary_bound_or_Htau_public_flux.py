from __future__ import annotations

import csv
import gzip
import shutil
import tarfile
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
EXTERNAL = ROOT / "source-intake" / "external" / "arxiv_1905_03413"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3615"
BRANCH_ID = "MTS_R2FR_Y5_BFRESNEL_PRIMARY_BOUND_OR_HTAU_PUBLIC_FLUX_3615"
DOC = ROOT / "3615-Y5-R2FR-BFresnel-primary-bound-or-Htau-public-flux.md"
ARXIV_URL = "https://arxiv.org/abs/1905.03413"
ARXIV_EPRINT_URL = "https://arxiv.org/e-print/1905.03413"
ARXIV_ID = "1905.03413"


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
        "source_register": RESIDUALS / "P8_Y5_R2FR_3615_SOURCE_REGISTER.csv",
        "bfresnel_bound_acquisition": RESIDUALS / "P8_Y5_R2FR_3615_BFRESNEL_PRIMARY_BOUND_ACQUISITION.csv",
        "bfresnel_mapping_gate": RESIDUALS / "P8_Y5_R2FR_3615_BFRESNEL_MTS_MAPPING_GATE.csv",
        "htau_public_flux_fallback": RESIDUALS / "P8_Y5_R2FR_3615_HTAU_PUBLIC_FLUX_FALLBACK.csv",
        "decision_gates": RESIDUALS / "P8_Y5_R2FR_3615_DECISION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3615_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3615_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_BFresnel_primary_bound_or_Htau_public_flux_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3615_VALIDATION.csv",
    }


def local_source_map() -> dict[str, tuple[Path, str]]:
    return {
        "handoff_3614": (
            RESIDUALS / "P8_Y5_R2FR_3614_NEXT_TARGET.csv",
            "3615-Y5-R2FR-BFresnel-primary-bound-or-Htau-public-flux.md",
        ),
        "principal_bound_3614": (
            RESIDUALS / "P8_Y5_R2FR_3614_PRINCIPAL_HODGE_BOUND.csv",
            "B_Fresnel",
        ),
        "empirical_acquisition_3614": (
            RESIDUALS / "P8_Y5_R2FR_3614_PRINCIPAL_HODGE_EMPIRICAL_ACQUISITION.csv",
            "vacuum birefringence",
        ),
        "htau_fallback_3614": (
            RESIDUALS / "P8_Y5_R2FR_3614_HTAU_CURL_FALLBACK.csv",
            "C_curl",
        ),
        "htau_vector_3578": (
            RESIDUALS / "P8_Y5_R2FR_3578_HTAU_CURL_COMPONENT_VECTOR.csv",
            "I_matter_EM_flux",
        ),
        "htau_identities_3578": (
            RESIDUALS / "P8_Y5_R2FR_3578_HTAU_CURL_IDENTITIES.csv",
            "d_F alpha_tau",
        ),
        "pim_htau_3602": (
            RESIDUALS / "P8_Y5_R2FR_3602_PIM_HTAU_COMPONENT_BOUND_ROWS.csv",
            "PHTB3602_3_C_curl",
        ),
        "denominator_fallback_3532": (
            RESIDUALS / "P8_Y5_R2FR_3532_DENOMINATOR_BOUND_FALLBACKS.csv",
            "C_Htau",
        ),
    }


def external_source_needles() -> dict[str, str]:
    return {
        "wei_2019_title": "New Constraints on Lorentz Invariance Violation with Polarized Gamma-Ray Bursts",
        "wei_2019_dispersion": r"E_{\pm}^2=p^2\pm \frac{2\xi}{M_{\rm pl}} p^3",
        "wei_2019_rotation": r"\Delta\theta(k)=\xi\frac{k^2}",
        "wei_2019_grb061122": "061122",
        "wei_2019_grb140206a": "140206A",
        "wei_2019_range": r"10^{-14}-10^{-17}",
    }


def ensure_external_source() -> dict[str, object]:
    EXTERNAL.mkdir(parents=True, exist_ok=True)
    source_tex = EXTERNAL / "ms.tex"
    temp_tex = Path("D:/Temp/mts_arxiv_1905_03413/ms.tex")
    blocker = EXTERNAL / "acquisition_blocker.txt"

    if source_tex.exists():
        return {
            "acquired": True,
            "source_path": source_tex,
            "method": "existing_local_source_intake",
            "detail": "source-intake TeX already present",
        }

    if temp_tex.exists():
        shutil.copy2(temp_tex, source_tex)
        return {
            "acquired": True,
            "source_path": source_tex,
            "method": "copied_from_prior_arxiv_eprint_extract",
            "detail": str(temp_tex),
        }

    eprint_path = EXTERNAL / "1905.03413.eprint"
    try:
        urllib.request.urlretrieve(ARXIV_EPRINT_URL, eprint_path)
        extracted = extract_first_tex(eprint_path, source_tex)
        if extracted:
            return {
                "acquired": True,
                "source_path": source_tex,
                "method": "downloaded_arxiv_eprint_and_extracted_tex",
                "detail": ARXIV_EPRINT_URL,
            }
        blocker.write_text(
            "Downloaded arXiv e-print but no TeX source could be extracted.\n",
            encoding="utf-8",
        )
    except Exception as exception:
        blocker.write_text(
            f"Failed to acquire {ARXIV_EPRINT_URL}: {exception}\n",
            encoding="utf-8",
        )

    return {
        "acquired": False,
        "source_path": blocker,
        "method": "acquisition_failed_blocker_written",
        "detail": ARXIV_EPRINT_URL,
    }


def extract_first_tex(eprint_path: Path, destination_tex: Path) -> bool:
    if tarfile.is_tarfile(eprint_path):
        with tarfile.open(eprint_path, "r:*") as archive:
            for member in archive.getmembers():
                if member.name.lower().endswith(".tex"):
                    extracted = archive.extractfile(member)
                    if extracted is None:
                        continue
                    destination_tex.write_bytes(extracted.read())
                    return True
        return False

    raw_bytes = eprint_path.read_bytes()
    try:
        raw_bytes = gzip.decompress(raw_bytes)
    except OSError:
        pass
    if b"\\title" in raw_bytes and b"\\begin{document}" in raw_bytes:
        destination_tex.write_bytes(raw_bytes)
        return True
    return False


def source_register_rows(acquisition: dict[str, object]) -> list[dict[str, object]]:
    timestamp = utc_now()
    rows: list[dict[str, object]] = []
    for source_id, source_data in local_source_map().items():
        source_path, needle = source_data
        exists = source_path.exists()
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source_id,
                "source_type": "local_checkpoint_input",
                "source_path": str(source_path),
                "source_url": "",
                "exists": exists,
                "needle": needle,
                "needle_found": exists and contains(source_path, needle),
                "extraction_method": "local_csv_anchor",
                "valid_for_claim": False,
            }
        )

    source_path = Path(acquisition["source_path"])
    for source_id, needle in external_source_needles().items():
        exists = source_path.exists()
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source_id,
                "source_type": "external_primary_source",
                "source_path": str(source_path),
                "source_url": ARXIV_URL,
                "exists": exists,
                "needle": needle,
                "needle_found": exists and contains(source_path, needle),
                "extraction_method": acquisition["method"],
                "valid_for_claim": False,
            }
        )
    return rows


def bfresnel_bound_rows(acquisition: dict[str, object]) -> list[dict[str, object]]:
    timestamp = utc_now()
    source_path = str(acquisition["source_path"])
    common = {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "target_quantity": "B_Fresnel / Delta_chi_principal observational analogue",
        "source_parameter": "xi_LIV",
        "bound_units": "dimensionless",
        "confidence_level": "68% C.L.",
        "arena": "prompt GRB gamma-ray polarization / vacuum birefringence",
        "source_title": "New Constraints on Lorentz Invariance Violation with Polarized Gamma-Ray Bursts",
        "source_author": "Jun-Jie Wei",
        "source_year": 2019,
        "source_url": ARXIV_URL,
        "arxiv_id": ARXIV_ID,
        "source_local_path": source_path,
        "extraction_method": acquisition["method"],
        "mts_mapping_status": "ANALOGUE_BOUND_NOT_DIRECT_MTS_COEFFICIENT",
        "score_ready": False,
        "claim_allowed": False,
        "valid_for_claim": False,
    }
    return [
        {
            **common,
            "bound_id": "BFB3615_0_GRB061122",
            "bound_relation": "xi < 5.2e-17",
            "bound_value": "5.2e-17",
            "object": "GRB 061122",
            "instrument": "INTEGRAL/IBIS",
            "energy_range_keV": "250-800",
            "redshift": "1.33",
            "source_anchor": "Table row GRB 061122: xi < 5.2e-17",
        },
        {
            **common,
            "bound_id": "BFB3615_1_GRB140206A",
            "bound_relation": "xi < 1.0e-16",
            "bound_value": "1.0e-16",
            "object": "GRB 140206A",
            "instrument": "INTEGRAL/IBIS",
            "energy_range_keV": "200-400",
            "redshift": "2.739",
            "source_anchor": "Table row GRB 140206A: xi < 1.0e-16",
        },
    ]


def bfresnel_mapping_gate_rows(acquisition: dict[str, object]) -> list[dict[str, object]]:
    timestamp = utc_now()
    source_path = str(acquisition["source_path"])
    principal_path = str(local_source_map()["principal_bound_3614"][0])
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "BFG3615_0_MTS_quantity",
            "quantity": "B_Fresnel",
            "formula": "B_Fresnel := ||G_chi(k)-rho(g_EM^{ab}k_a k_b)^2||_arena",
            "required_input": "Delta_chi_principal_MTS and arena norm",
            "status": "IMPORTED_FROM_3614",
            "source_path": principal_path,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "BFG3615_1_observable_bound",
            "quantity": "xi_LIV",
            "formula": "Delta theta(k)=xi k^2/(M_pl H0) int_0^z (1+z') dz'/sqrt(Omega_m(1+z')^3+Omega_Lambda)",
            "required_input": "primary GRB polarization source and model assumptions",
            "status": "PRIMARY_ANALOGUE_BOUND_ACQUIRED",
            "source_path": source_path,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "BFG3615_2_projection_law",
            "quantity": "MTS-to-observable projection",
            "formula": "B_Fresnel_MTS <= K_Fresnel |Delta_chi_principal_MTS|",
            "required_input": "K_Fresnel, projection_norm, energy/redshift mapping, and parent coefficient source path",
            "status": "MISSING_PARENT_PROJECTION",
            "source_path": principal_path,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "BFG3615_3_no_claim_guard",
            "quantity": "claim status",
            "formula": "score_ready=false until B_Fresnel_MTS is numerically projected into xi_LIV-compatible arena",
            "required_input": "no MTS claim from analogue bound alone",
            "status": "BOUND_SOURCE_ACQUIRED_PARENT_PROJECTION_MISSING",
            "source_path": str(output_paths()["bfresnel_bound_acquisition"]),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def htau_public_flux_fallback_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    sources = local_source_map()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "fallback_id": "HPF3615_0_not_activated",
            "quantity": "fallback branch",
            "formula": "fallback not activated because a primary B_Fresnel analogue bound was acquired",
            "status": "READY_BUT_NOT_ACTIVATED",
            "source_path": str(output_paths()["bfresnel_bound_acquisition"]),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "fallback_id": "HPF3615_1_EH_boundary",
            "quantity": "I_EH_stationary_boundary",
            "formula": "abs(int_S i_tau omega_EH) plus EH boundary flux",
            "status": "CONDITIONAL_ZERO_IF_STATIONARY_EH_BOUNDARY_ELSE_BOUND_REQUIRED",
            "source_path": str(sources["htau_vector_3578"][0]),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "fallback_id": "HPF3615_2_matter_EM_flux",
            "quantity": "I_matter_EM_flux",
            "formula": "int_BF | -int_S i_tau(omega_matter+omega_EM) + C_tau^matter + C_tau^EM |",
            "status": "PUBLIC_FLUX_BOUND_REQUIRED",
            "source_path": str(sources["htau_vector_3578"][0]),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "fallback_id": "HPF3615_3_Ccurl_route",
            "quantity": "C_curl",
            "formula": "Delta_H_curl_bound <= A_F sup_BF (I_pub+I_EM+I_extra+I_boundary+I_tau_surface+I_qdescent)",
            "status": "FALLBACK_BOUND_VECTOR_READY_VALUES_MISSING",
            "source_path": str(sources["pim_htau_3602"][0]),
            "score_ready": False,
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
            "decision_id": "DEC3615_0_primary_bound_acquired",
            "decision": "A primary source analogue bound for B_Fresnel/vacuum birefringence is now in source-intake.",
            "status": "PASS_NONCLAIM",
            "next_action": "use only as external constraint after MTS projection exists",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3615_1_direct_score_blocked",
            "decision": "The acquired xi_LIV bound is not yet an MTS Delta_chi_principal score.",
            "status": "BLOCKED_BY_PARENT_PROJECTION",
            "next_action": "derive or source K_Fresnel and the arena norm",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3615_2_fallback_staged",
            "decision": "H_tau public EH and matter/EM flux fallback is carried forward but not activated.",
            "status": "READY_IF_BFRESNEL_MAPPING_STALLS",
            "next_action": "attack I_EH_stationary_boundary or I_matter_EM_flux if projection cannot be parent-owned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3615_3_next_target_selected",
            "decision": "3616 should build the projection runner or reduce the public flux fallback.",
            "status": "NEXT_TARGET_SELECTED",
            "next_action": "3616-Y5-R2FR-BFresnel-projection-runner-or-Htau-flux-reduction.md",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def status_rows(acquisition: dict[str, object]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status_id": "STATUS3615_0",
            "result": "BOUND_SOURCE_ACQUIRED_PARENT_PROJECTION_MISSING",
            "summary": "Primary GRB polarization birefringence bounds now exist as nonclaim B_Fresnel analogue evidence; direct MTS score is blocked until the parent projection/norm is derived.",
            "external_source_acquired": bool(acquisition["acquired"]),
            "bound_source_acquired": bool(acquisition["acquired"]),
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
            "next_id": "NEXT3615_0",
            "target_doc": "3616-Y5-R2FR-BFresnel-projection-runner-or-Htau-flux-reduction.md",
            "target_script": "scripts/Y5_R2FR_3616_BFresnel_projection_runner_or_Htau_flux_reduction.py",
            "objective": "derive or source the MTS-to-GRB birefringence projection coefficient K_Fresnel and arena norm; if that stalls, reduce I_EH_stationary_boundary or I_matter_EM_flux in the H_tau curl fallback",
            "success_gate": "either produce a parent-owned projection law mapping Delta_chi_principal_MTS to the acquired xi_LIV bound, or theorem-zero/source-bound one public H_tau flux component",
            "reason": "3615 acquired real bound data; the next leap is translating MTS geometry into that arena rather than recording more missing rows.",
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
            "B_Fresnel_bound_source": "ACQUIRED_ANALOGUE_PRIMARY_SOURCE",
            "MTS_projection": "MISSING_PARENT_PROJECTION",
            "Htau_public_flux_fallback": "READY_NOT_ACTIVATED",
            "claim_status": "NO_CLAIM",
            "next_target": "3616 projection runner or H_tau flux reduction",
            "valid_for_claim": False,
        }
    ]


def write_markdown(acquisition: dict[str, object]) -> None:
    source_path = acquisition["source_path"]
    DOC.write_text(
        "\n".join(
            [
                "# 3615 Y5 R2FR: B_Fresnel primary bound or H_tau public flux",
                "",
                "## Verdict",
                "- Primary-source observational analogue data were acquired for the `B_Fresnel` / principal-Hodge birefringence arena.",
                "- The acquired rows are **not** an MTS pass: they constrain a published dimensionless LIV birefringence parameter `xi`, not a parent-owned MTS coefficient.",
                "- The live next target is now a real derivation step: map `Delta_chi_principal_MTS` into the GRB polarization/Fresnel arena via a sourced `K_Fresnel` and norm, or move to the `H_tau` public-flux fallback.",
                "",
                "## Source acquired",
                f"- Source: Jun-Jie Wei, *New Constraints on Lorentz Invariance Violation with Polarized Gamma-Ray Bursts*, arXiv:{ARXIV_ID}.",
                f"- URL: {ARXIV_URL}",
                f"- Local extracted source: `{source_path}`",
                "- Model anchor: circular-polarization dispersion uses a dimensionless `xi` and predicts energy-dependent polarization rotation.",
                "- Bound anchors: GRB 061122 gives `xi < 5.2e-17`; GRB 140206A gives `xi < 1.0e-16`, both at 68% C.L. in the source table.",
                "",
                "## Bound rows",
                "- `P8_Y5_R2FR_3615_BFRESNEL_PRIMARY_BOUND_ACQUISITION.csv` records two positive numeric dimensionless bound rows.",
                "- Every bound row is marked `valid_for_claim=false`, `claim_allowed=false`, and `score_ready=false`.",
                "- This is source plumbing, not a local-GR/R10/EM claim.",
                "",
                "## MTS translation gate",
                "- Current MTS target from 3614: `B_Fresnel := ||G_chi(k)-rho(g_EM^{ab}k_a k_b)^2||_arena`.",
                "- Required bridge: `B_Fresnel_MTS <= K_Fresnel |Delta_chi_principal_MTS|`.",
                "- Missing parent-owned inputs: `K_Fresnel`, the projection norm, energy/redshift arena matching, and a sourced MTS parent coefficient.",
                "- Until those exist, the bound is a useful external boxing ring, not a scorecard win.",
                "",
                "## H_tau fallback staged",
                "- Fallback is not activated because a real `B_Fresnel` source was acquired.",
                "- If projection stalls, the staged fallback is `I_EH_stationary_boundary` or `I_matter_EM_flux` inside the `C_curl`/`H_tau` denominator route.",
                "",
                "## Next target",
                "- `3616-Y5-R2FR-BFresnel-projection-runner-or-Htau-flux-reduction.md`.",
                "- First attempt: derive/source the `K_Fresnel` projection law.",
                "- Backup attempt: theorem-zero or source-bound the public EH/matter-EM Hamiltonian flux term.",
                "",
                "## Claim status",
                "- `NO_CLAIM`: the new rows are private robustness scaffolding.",
                "- A claim only becomes possible after a parent-owned projection maps MTS variables into the acquired observational bound arena.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def validate(acquisition: dict[str, object]) -> list[dict[str, object]]:
    timestamp = utc_now()
    paths = output_paths()
    results: list[tuple[str, bool, str]] = []

    local_sources = local_source_map()
    local_sources_exist = all(source_path.exists() for source_path, _needle in local_sources.values())
    local_needles_found = all(
        source_path.exists() and contains(source_path, needle)
        for source_path, needle in local_sources.values()
    )
    results.append(("VAL3615_0_local_sources_exist", local_sources_exist, "all required 3615 local source paths exist"))
    results.append(("VAL3615_1_local_needles_found", local_needles_found, "all selected 3615 local source anchors found"))

    source_path = Path(acquisition["source_path"])
    external_source_ready = bool(acquisition["acquired"]) and source_path.exists()
    external_needles_found = external_source_ready and all(
        contains(source_path, needle) for needle in external_source_needles().values()
    )
    results.append(("VAL3615_2_external_source_acquired", external_source_ready, f"external source path: {source_path}"))
    results.append(("VAL3615_3_external_needles_found", external_needles_found, "Wei 2019 title/equations/bound anchors found"))

    pre_validation_paths = [path for name, path in paths.items() if name != "validation"]
    outputs_exist = DOC.exists() and all(path.exists() for path in pre_validation_paths)
    results.append(("VAL3615_4_outputs_exist", outputs_exist, "all pre-validation 3615 outputs written"))

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
    results.append(("VAL3615_5_csv_parse", csv_parse_pass, "; ".join(parse_details)))

    bound_rows = read_csv(paths["bfresnel_bound_acquisition"]) if paths["bfresnel_bound_acquisition"].exists() else []
    positive_numeric_bounds = bool(bound_rows) and all(
        float(row["bound_value"]) > 0.0 and row["bound_units"] == "dimensionless"
        for row in bound_rows
    )
    all_bound_rows_nonclaim = bool(bound_rows) and all(
        row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" and row["score_ready"] == "False"
        for row in bound_rows
    )
    results.append(("VAL3615_6_positive_dimensionless_bounds", positive_numeric_bounds, "all B_Fresnel analogue bound rows are positive dimensionless numbers"))
    results.append(("VAL3615_7_bound_rows_nonclaim", all_bound_rows_nonclaim, "all acquired bound rows remain no-claim"))

    mapping_rows = read_csv(paths["bfresnel_mapping_gate"]) if paths["bfresnel_mapping_gate"].exists() else []
    projection_missing = any(row["status"] == "MISSING_PARENT_PROJECTION" for row in mapping_rows)
    no_score_ready = bool(mapping_rows) and all(row["score_ready"] == "False" for row in mapping_rows)
    results.append(("VAL3615_8_projection_missing_recorded", projection_missing, "MTS projection gate explicitly blocks direct scoring"))
    results.append(("VAL3615_9_no_score_without_projection", no_score_ready, "no mapping row is score-ready without parent projection"))

    fallback_rows = read_csv(paths["htau_public_flux_fallback"]) if paths["htau_public_flux_fallback"].exists() else []
    fallback_staged = any(row["quantity"] == "I_EH_stationary_boundary" for row in fallback_rows) and any(
        row["quantity"] == "I_matter_EM_flux" for row in fallback_rows
    )
    results.append(("VAL3615_10_htau_fallback_staged", fallback_staged, "public EH and matter/EM flux fallback rows staged"))

    all_outputs_nonclaim = True
    for name, path in paths.items():
        if name == "validation" or not path.exists():
            continue
        for row in read_csv(path):
            if row.get("valid_for_claim") == "True" or row.get("claim_allowed") == "True":
                all_outputs_nonclaim = False
    results.append(("VAL3615_11_all_outputs_nonclaim", all_outputs_nonclaim, "all generated rows remain nonclaim"))

    formalization_clean = True
    formalization_detail = "formalization-workbench not found"
    if FORMALIZATION.exists():
        leaked_paths = list(FORMALIZATION.rglob("*3615*"))
        formalization_clean = len(leaked_paths) == 0
        formalization_detail = "no 3615 files in formalization-workbench" if formalization_clean else "; ".join(str(path) for path in leaked_paths[:5])
    results.append(("VAL3615_12_no_formalization_leak", formalization_clean, formalization_detail))

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
    acquisition = ensure_external_source()
    paths = output_paths()

    write_csv(paths["source_register"], source_register_rows(acquisition))
    write_csv(paths["bfresnel_bound_acquisition"], bfresnel_bound_rows(acquisition))
    write_csv(paths["bfresnel_mapping_gate"], bfresnel_mapping_gate_rows(acquisition))
    write_csv(paths["htau_public_flux_fallback"], htau_public_flux_fallback_rows())
    write_csv(paths["decision_gates"], decision_gate_rows())
    write_csv(paths["status"], status_rows(acquisition))
    write_csv(paths["next_target"], next_target_rows())
    write_csv(paths["canonical_status"], canonical_status_rows())
    write_markdown(acquisition)
    write_csv(paths["validation"], validate(acquisition))

    failed = [row for row in read_csv(paths["validation"]) if row["result"] != "PASS"]
    if failed:
        raise SystemExit(f"3615 validation failed: {failed}")
    print(f"wrote 3615 checkpoint with {len(read_csv(paths['validation']))} validation checks")


if __name__ == "__main__":
    main()
