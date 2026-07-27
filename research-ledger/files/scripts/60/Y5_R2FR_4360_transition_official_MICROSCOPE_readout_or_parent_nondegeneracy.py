from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4360"
CLAIM_ID = "L-201"
BRANCH = "MTS_R2FR_Y5_TRANSITION_OFFICIAL_MICROSCOPE_READOUT_OR_PARENT_NONDEGENERACY_4360"
MARKER = "PPC4161_TRANSITION_OFFICIAL_MICROSCOPE_READOUT_OR_PARENT_NONDEGENERACY_4360"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_OFFICIAL_MICROSCOPE_READOUT_OR_PARENT_NONDEGENERACY_4360"
DECISION = "OFFICIAL_MICROSCOPE_PORTAL_REPROBED_PUBLIC_SOURCES_PARTIAL_CMIN_NOT_COMPUTABLE_PARENT_NONNULL_PROOF_FAILS_OWNER_ZERO_ROUTE_SELECTED_NONCLAIM"
NEXT_TARGET = "4361-Y5-R2FR-transition-owner-no-wA-theorem-or-explicit-source-coupling-closure.md"

FORMAL_PATH = FORMAL / "376-PPC4161-transition-official-MICROSCOPE-readout-or-parent-nondegeneracy.md"
DOC_PATH = POST / "4360-Y5-R2FR-transition-official-MICROSCOPE-readout-or-parent-nondegeneracy.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4360_VALIDATION.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4360_00_4359_next": (
        FORMAL / "375-PPC4161-transition-tau-min-lower-bound-or-action-measure-zero-proof.md",
        "Can we import/source the official MICROSCOPE readout/source/material objects or prove parent nondegeneracy so c_min>0?",
        "4359 selected official MICROSCOPE import or parent nondegeneracy.",
    ),
    "SRC4360_01_4359_validation": (
        SOURCE_DIR / "P8_Y5_BRR545_4359_VALIDATION.csv",
        "next_target_present",
        "4359 validation passed and handed off to 4360.",
    ),
    "SRC4360_02_1070_eta": (
        POST / "1070-Y5-R10-MICROSCOPE-eta-readout-formula-or-orbit-kernel-acquisition.md",
        "eta formula and delta_x identification are now source-backed",
        "MICROSCOPE eta/readout convention acquired previously.",
    ),
    "SRC4360_03_1072_portal": (
        POST / "1072-Y5-R10-MICROSCOPE-data-portal-schema-or-reconstructed-gxS-kernel.md",
        "does not yet obtain the official CMSM schema or arrays",
        "Prior portal/API attempt did not acquire official arrays.",
    ),
    "SRC4360_04_3366_live_audit": (
        POST / "3366-Y5-R2FR-WEP-live-projection-file-acquisition-or-refusal-under-AX1090.md",
        "Best next route is not another CMSM loop",
        "Prior live projection audit selected derivation-first after portal probing.",
    ),
    "SRC4360_05_3366_live_objects": (
        POST / "3366-Y5-R2FR-WEP-live-projection-file-acquisition-or-refusal-under-AX1090.md",
        "missing_or_partial=C_parent_WEP_slot_import;K_CMSM_readout;R_source_Earth_worldtube;R_material_TA6V_minus_PtRh10_full_tensor;tau_WEP_product_convention",
        "Exact live WEP projection objects still missing or partial.",
    ),
    "SRC4360_06_1697_axiom": (
        POST / "1697-Y5-R2FR-owner-axiom-candidate-and-WEP-readout-source-pack.md",
        "AX1697_1_no_source_prefactor",
        "Owner/no-w_A axiom candidate is the clean zero target.",
    ),
    "SRC4360_07_1084_readout_gate": (
        SOURCE_DIR / "P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv",
        "OFFICIAL_ARRAYS_NOT_IMPORTED",
        "Official MICROSCOPE readout arrays remain missing in current source intake.",
    ),
}


EXTERNAL_SOURCES = [
    {
        "external_id": "EXT4360_0_ONERA_public_data_page",
        "url": "https://microscope.onera.fr/fr/publication/microscope-data-are-available",
        "source_type": "official_mission_page",
        "extracted_item": "ONERA says MICROSCOPE mission data are available and points users to the CMSM data portal.",
        "use_in_4360": "portal provenance and current source-route check",
        "source_backed": "True",
        "valid_for_claim": "False",
    },
    {
        "external_id": "EXT4360_1_CMSM_portal_target",
        "url": "https://cmsm-ds.onera.fr/user/microscope",
        "source_type": "official_data_portal_target",
        "extracted_item": "CMSM/REGARDS portal target for MICROSCOPE public data products.",
        "use_in_4360": "attempt live acquisition/probe; not a local array by itself",
        "source_backed": "True",
        "valid_for_claim": "False",
    },
    {
        "external_id": "EXT4360_2_CQG_final_result",
        "url": "https://doi.org/10.1088/1361-6382/ac84be",
        "source_type": "peer_reviewed_final_result",
        "extracted_item": "MICROSCOPE final-result paper defines the observable/readout context and states data availability.",
        "use_in_4360": "readout formula/design-matrix provenance, not live tau_WEP arrays",
        "source_backed": "True",
        "valid_for_claim": "False",
    },
    {
        "external_id": "EXT4360_3_arXiv_final_result",
        "url": "https://arxiv.org/abs/2209.15487",
        "source_type": "open_preprint",
        "extracted_item": "Open final-result source candidate for eta bound and readout equations.",
        "use_in_4360": "public result provenance if DOI/PDF route is unavailable",
        "source_backed": "True",
        "valid_for_claim": "False",
    },
    {
        "external_id": "EXT4360_4_DLR_CQG_PDF_mirror",
        "url": "https://elib.dlr.de/193667/2/Touboul_2022_Class._Quantum_Grav._39_204009.pdf",
        "source_type": "open_pdf_mirror",
        "extracted_item": "Prior checkpoints cite lines for 4 Hz accelerometer data, gx/gz/Sxx/Sxz design columns and data availability.",
        "use_in_4360": "source-backed public design basis; still not a machine-readable CMSM export",
        "source_backed": "True",
        "valid_for_claim": "False",
    },
    {
        "external_id": "EXT4360_5_REGARDS_access_project",
        "url": "https://regardsoss.github.io/docs/development/services/access-project/overview",
        "source_type": "software_platform_docs",
        "extracted_item": "REGARDS access-project service can proxy search/product access, motivating candidate CMSM API endpoints.",
        "use_in_4360": "candidate API basis only; no MICROSCOPE payload acquired",
        "source_backed": "True",
        "valid_for_claim": "False",
    },
]

PROBE_URLS = [
    ("WEB4360_0_ONERA_page", "https://microscope.onera.fr/fr/publication/microscope-data-are-available", "official public data page"),
    ("WEB4360_1_CMSM_base", "https://cmsm-ds.onera.fr", "CMSM portal base"),
    ("WEB4360_2_CMSM_user", "https://cmsm-ds.onera.fr/user/microscope", "CMSM MICROSCOPE user route"),
    ("WEB4360_3_CMSM_module", "https://cmsm-ds.onera.fr/user/microscope/modules/7", "candidate REGARDS module route"),
    ("WEB4360_4_CMSM_dataset_api", "https://cmsm-ds.onera.fr/api/v1/rs-access-project/datasets/search", "candidate REGARDS dataset-search endpoint"),
]


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def find_line(path: Path, needle: str) -> str:
    text = read_text(path)
    index = text.find(needle)
    if index < 0:
        return ""
    return str(text[:index].count("\n") + 1)


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: str(row.get(field, "")) for field in fields})


def md_cell(value: object) -> str:
    return str(value).replace("|", r"\|").replace("\n", "<br>")


def md_table(rows: List[Dict[str, str]], fields: List[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + block.strip() + "\n", encoding="utf-8")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        line_number = find_line(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(bool(line_number)),
                "line_number": line_number,
                "role": role,
                "valid_for_claim": "False",
            }
        )
    return rows


def probe_url(probe_id: str, url: str, role: str) -> Dict[str, str]:
    row = {
        "probe_id": probe_id,
        "url": url,
        "role": role,
        "probe_status": "NOT_RUN",
        "http_status": "",
        "content_type": "",
        "bytes_sampled": "0",
        "schema_or_data_inventory_acquired": "False",
        "error": "",
        "valid_for_claim": "False",
    }
    try:
        request = Request(url, headers={"User-Agent": "MTS-4360-private-source-probe/1.0"})
        with urlopen(request, timeout=6) as response:
            sample = response.read(2048)
            row.update(
                {
                    "probe_status": "HTTP_OK",
                    "http_status": str(response.status),
                    "content_type": response.headers.get("Content-Type", ""),
                    "bytes_sampled": str(len(sample)),
                    "schema_or_data_inventory_acquired": str(
                        b"dataset" in sample.lower()
                        and (b"microscope" in sample.lower() or b"cmsm" in sample.lower())
                    ),
                }
            )
    except HTTPError as exc:
        row.update({"probe_status": "HTTP_ERROR", "http_status": str(exc.code), "error": str(exc)})
    except URLError as exc:
        row.update({"probe_status": "BLOCKED_OR_UNREACHABLE_FROM_THIS_RUN", "error": str(exc)})
    except Exception as exc:  # pragma: no cover - defensive source logging
        row.update({"probe_status": "BLOCKED_OR_UNREACHABLE_FROM_THIS_RUN", "error": type(exc).__name__ + ": " + str(exc)})
    return row


def portal_probe_rows() -> List[Dict[str, str]]:
    return [probe_url(probe_id, url, role) for probe_id, url, role in PROBE_URLS]


def official_route_rows(probes: List[Dict[str, str]]) -> List[Dict[str, str]]:
    cmsm_ok = any(
        row["probe_status"] == "HTTP_OK"
        and row["schema_or_data_inventory_acquired"] == "True"
        and "cmsm-ds.onera.fr" in row["url"]
        for row in probes
    )
    return [
        {
            "route_id": "OR4360_0_public_result",
            "object": "eta_TiPt_bound_and_delta_x_readout",
            "acquired_level": "SOURCE_BACKED_PUBLIC_OBSERVABLE",
            "what_it_gives": "eta formula, final Ti/Pt bound context, X-axis differential readout context",
            "what_it_does_not_give": "K_CMSM arrays, exact masks, orbit/attitude kernel, Earth source worldtube, parent material tensor, c_min",
            "claim_effect": "external comparator only",
            "valid_for_claim": "False",
        },
        {
            "route_id": "OR4360_1_CMSM_live_export",
            "object": "official CMSM machine-readable products",
            "acquired_level": "ACQUIRED" if cmsm_ok else "NOT_ACQUIRED_FROM_THIS_RUNTIME",
            "what_it_gives": "would give exact product inventory and possibly readout/orbit/attitude/accelerometer files if accessible",
            "what_it_does_not_give": "parent C_parent or MTS material/source basis by itself",
            "claim_effect": "needed but not sufficient for tau_min",
            "valid_for_claim": "False",
        },
        {
            "route_id": "OR4360_2_reconstructed_kernel",
            "object": "reconstructed gx/gz/Sxx/Sxz kernel",
            "acquired_level": "DRY_RUN_ONLY_FROM_1072",
            "what_it_gives": "code path and schema shape for future replacement by official arrays",
            "what_it_does_not_give": "phase/masks/timestamps/official gravity model/source/material contraction",
            "claim_effect": "cannot compute tau_WEP or c_min",
            "valid_for_claim": "False",
        },
        {
            "route_id": "OR4360_3_user_assisted_export",
            "object": "manual/browser CMSM export",
            "acquired_level": "OPTIONAL_FUTURE_INTAKE",
            "what_it_gives": "could fill K_CMSM/time-grid/masks if user obtains official files",
            "what_it_does_not_give": "no replacement for parent nondegeneracy or owner theorem",
            "claim_effect": "validate only, never auto-promote",
            "valid_for_claim": "False",
        },
    ]


def cmin_rows() -> List[Dict[str, str]]:
    return [
        {
            "cmin_id": "CMIN4360_0_definition",
            "object": "c_min",
            "definition": "positive lower bound on |cos(theta)| between K_CMSM and V_ST=S_Earth x M_TiPt in the branch-locked WEP projection",
            "status": "FORMALLY_DEFINED",
            "numeric_value": "",
            "why_not_numeric": "K_CMSM, V_ST and normalization are not live in one common parent/source/readout basis",
            "valid_for_claim": "False",
        },
        {
            "cmin_id": "CMIN4360_1_public_MICROSCOPE_limit",
            "object": "public eta/result sources",
            "definition": "public final-result sources define eta and the analysis context",
            "status": "INSUFFICIENT_FOR_CMIN",
            "numeric_value": "",
            "why_not_numeric": "public observable bound does not expose the vector pairing needed to prove or compute non-null alignment",
            "valid_for_claim": "False",
        },
        {
            "cmin_id": "CMIN4360_2_CMSM_portal_limit",
            "object": "CMSM portal route",
            "definition": "official array source route",
            "status": "NOT_ACQUIRED_FROM_THIS_RUNTIME",
            "numeric_value": "",
            "why_not_numeric": "portal/API routes are not inventory-readable from this run; even successful export still needs parent C_parent/R_source/R_material",
            "valid_for_claim": "False",
        },
        {
            "cmin_id": "CMIN4360_3_parent_nondegeneracy_limit",
            "object": "generic parent proof",
            "definition": "prove V_ST not in ker(K_CMSM) without official arrays",
            "status": "GENERIC_PROOF_REJECTED",
            "numeric_value": "",
            "why_not_numeric": "a nonzero linear readout functional has a kernel unless the parent forces V_ST into a one-dimensional non-null channel or supplies a positivity cone",
            "valid_for_claim": "False",
        },
        {
            "cmin_id": "CMIN4360_4_verdict",
            "object": "tau_min route",
            "definition": "tau_min=k_min*s_min*m_min*c_min/N_max",
            "status": "C_MIN_NOT_DERIVED",
            "numeric_value": "",
            "why_not_numeric": "the missing object is specifically a non-null/alignment theorem or sourced contraction, not another eta-bound citation",
            "valid_for_claim": "False",
        },
    ]


def parent_nondegeneracy_rows() -> List[Dict[str, str]]:
    return [
        {
            "attempt_id": "PND4360_0_linear_algebra_obstruction",
            "target": "prove c_min>0 from nonzero K_CMSM and nonzero V_ST",
            "attempt": "Use nonzero readout/source/material factors alone.",
            "result": "FAIL",
            "reason": "Any nonzero linear functional on a dimension>1 readout space has a kernel; V_ST can sit in that kernel.",
            "what_would_close": "official contraction showing |<K,V>|>0, or parent theorem forcing V_ST into a one-dimensional positive channel",
            "valid_for_claim": "False",
        },
        {
            "attempt_id": "PND4360_1_positivity_cone_obstruction",
            "target": "prove c_min>0 by positivity",
            "attempt": "Treat Earth/source and material responses as positive bulk objects.",
            "result": "FAIL",
            "reason": "MICROSCOPE readout is a signed differential/linear analysis channel; positivity before projection does not survive masks, Fourier bands, attitude/orbit weights and material differences.",
            "what_would_close": "same-basis positive cone theorem with K_CMSM in the dual cone and V_ST in the cone interior",
            "valid_for_claim": "False",
        },
        {
            "attempt_id": "PND4360_2_public_result_obstruction",
            "target": "derive c_min from the published eta bound",
            "attempt": "Use eta(Ti,Pt) bound and result value as a proxy for alignment.",
            "result": "FAIL",
            "reason": "the measured eta bound constrains the product channel after analysis; it does not decompose into MTS source-weight, material and readout vectors.",
            "what_would_close": "source-backed K_CMSM/R_source/R_material/C_parent packet or exact zero theorem",
            "valid_for_claim": "False",
        },
        {
            "attempt_id": "PND4360_3_parent_single_channel_possible",
            "target": "identify a viable parent theorem that could prove c_min>0",
            "attempt": "Require the parent source-weight residual to map into a single branch-locked EP channel with fixed sign and nonzero material contrast.",
            "result": "POSSIBLE_BUT_NOT_DERIVED",
            "reason": "this would exclude ker(K_CMSM), but it is stronger than current MTS parent clauses and risks becoming closure-only.",
            "what_would_close": "derive one-channel source-weight theorem from q-descended matter action, not from MICROSCOPE fitting after the fact",
            "valid_for_claim": "False",
        },
        {
            "attempt_id": "PND4360_4_verdict",
            "target": "4360 parent nondegeneracy",
            "attempt": "Try to prove c_min>0 from currently owned theory/source material.",
            "result": "NOT_CLOSED",
            "reason": "finite tau route remains legal but currently source-data-dependent; generic parent nondegeneracy is not derivable without adding a strong channel axiom.",
            "what_would_close": "either source official arrays and compute alignment, or switch to deriving the owner/no-w_A theorem so Delta_w_TiPt=0",
            "valid_for_claim": "False",
        },
    ]


def owner_route_rows() -> List[Dict[str, str]]:
    return [
        {
            "owner_id": "OWN4360_0_best_route",
            "route": "owner/no-w_A theorem",
            "statement": "If ordinary matter enters through one q-descended action-measure/current owner before readout, independent source-only weights w_A are not objects of the parent language.",
            "effect_if_proved": "Delta_w_TiPt=0, so the WEP finite tau_min route becomes optional for this source-label branch.",
            "current_status": "TARGET_SELECTED_NOT_PROVED",
            "risk": "must be derived from parent grammar, not adopted as a closure axiom",
            "valid_for_claim": "False",
        },
        {
            "owner_id": "OWN4360_1_minimal_clauses",
            "route": "minimal theorem contract",
            "statement": "domain exclusion + single action density line + variation before readout + connected ordinary matter naturality + no hidden readout reentry",
            "effect_if_proved": "source labels are quotient-forgotten up to one common calibration mode",
            "current_status": "CLAUSES_IMPORTED_FROM_1697",
            "risk": "disconnected matter graph, hidden scalar invariant, field normalization or EFT/readout loop can reopen w_A",
            "valid_for_claim": "False",
        },
        {
            "owner_id": "OWN4360_2_next_attack",
            "route": NEXT_TARGET,
            "statement": "prove the owner/no-w_A theorem directly or demote it to explicit closure with finite source-coupling rows",
            "effect_if_proved": "clean source-coupling branch for local GR/Newton/PPN WEP leg",
            "current_status": "NEXT_TARGET_SELECTED",
            "risk": "if it fails, do not keep circling MICROSCOPE; write the explicit source-coupling closure parameter",
            "valid_for_claim": "False",
        },
    ]


def runner_rows(cmin: List[Dict[str, str]], parent: List[Dict[str, str]]) -> List[Dict[str, str]]:
    cmin_closed = any(row["status"] == "C_MIN_DERIVED" for row in cmin)
    parent_closed = any(row["result"] == "PROVED" for row in parent)
    return [
        {
            "runner_id": "RUN4360_0_official_source_probe",
            "input": "ONERA/CMSM/REGARDS source routes",
            "action": "probe and ledger",
            "result": "public route recorded; live CMSM arrays not acquired from this runtime",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4360_1_cmin_compute",
            "input": "K_CMSM,V_ST,N_eta",
            "action": "attempt c_min computation",
            "result": "REFUSE_COMPUTE" if not cmin_closed else "COMPUTE",
            "claim_allowed": str(cmin_closed),
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4360_2_parent_nondegeneracy",
            "input": "current parent/source clauses",
            "action": "try generic non-null proof",
            "result": "GENERIC_PROOF_FAILS_KEEP_NONNULL_AS_INPUT" if not parent_closed else "PROVED",
            "claim_allowed": str(parent_closed),
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4360_3_owner_zero_route",
            "input": "AX1697/AX4359 owner package",
            "action": "select next derivation target",
            "result": "SELECT_OWNER_NO_WA_THEOREM",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> List[Dict[str, str]]:
    return [
        {
            "gate_id": "CG4360_0_public_MICROSCOPE_sources",
            "claim_component": "public WEP readout/result source",
            "gate_pass": "True",
            "claim_allowed": "False",
            "reason": "source-backed public observable, not an MTS tau/coupling prediction",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG4360_1_official_arrays",
            "claim_component": "K_CMSM official arrays",
            "gate_pass": "False",
            "claim_allowed": "False",
            "reason": "CMSM export/schema not acquired here",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG4360_2_cmin",
            "claim_component": "c_min>0 alignment",
            "gate_pass": "False",
            "claim_allowed": "False",
            "reason": "generic nondegeneracy proof fails and no official contraction was computed",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG4360_3_owner_zero",
            "claim_component": "Delta_w_TiPt=0",
            "gate_pass": "False",
            "claim_allowed": "False",
            "reason": "owner/no-w_A theorem selected but not derived",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG4360_4_local_GR_Newton_WEP",
            "claim_component": "local GR/Newton/source coupling pass",
            "gate_pass": "False",
            "claim_allowed": "False",
            "reason": "finite tau and zero theorem routes both remain open but unsigned",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4360_0",
            "decision": DECISION,
            "reason": (
                "4360 actually re-attacks the 4359 fork. Public MICROSCOPE sources and the ONERA data page are source-backed, "
                "but this runtime still cannot inventory or download official CMSM arrays. Even with arrays, c_min also needs "
                "a common MTS parent basis C_parent/R_source/R_material. The generic parent nondegeneracy proof fails because "
                "a signed linear readout has a kernel unless a stronger one-channel/positive-cone theorem is derived. Therefore "
                "the best next move is the owner/no-w_A theorem; if that fails it must be demoted to an explicit source-coupling closure."
            ),
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {"status_id": "STAT4360_0", "item": "official public MICROSCOPE sources", "status": "SOURCE_BACKED_PUBLIC_ONLY", "note": "eta/result/data-portal sources exist; no MTS prediction follows."},
        {"status_id": "STAT4360_1", "item": "CMSM live arrays", "status": "NOT_ACQUIRED_FROM_THIS_RUNTIME", "note": "portal/API routes probed; live schema/data inventory not obtained."},
        {"status_id": "STAT4360_2", "item": "c_min", "status": "NOT_DERIVED", "note": "needs official contraction or parent non-null theorem."},
        {"status_id": "STAT4360_3", "item": "parent nondegeneracy", "status": "GENERIC_PROOF_REJECTED", "note": "kernel and signed readout countermodels remain."},
        {"status_id": "STAT4360_4", "item": "best next route", "status": "OWNER_NO_WA_THEOREM_SELECTED", "note": NEXT_TARGET},
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_target_id": "NT4360_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can the source-only weight w_A be forbidden from the parent action/measure/current language rather than bounded by MICROSCOPE tau_min?",
            "preferred_route": "derive owner/no-w_A theorem from q-descended matter action, single measure/current owner, connected naturality, variation-before-readout and no-reentry",
            "fallback_route": "if theorem fails, write explicit source-coupling closure coefficient with finite WEP/PPN/R10/clock/orbital rows",
            "valid_for_claim": "False",
        }
    ]


def append_claim_register() -> None:
    path = FORMAL / "02-claims-register.csv"
    rows = []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames or ["claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk"]
        rows = list(reader)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    rows.append(
        {
            "claim_id": CLAIM_ID,
            "domain": "local_gr",
            "claim": (
                "4360 re-attacks the 4359 c_min fork using official MICROSCOPE source routes and a parent nondegeneracy proof attempt. "
                "Public ONERA/CQG/arXiv sources support the eta/readout/result/data-availability context, but this runtime does not acquire "
                "official CMSM arrays or a common MTS C_parent/R_source/R_material basis. The generic c_min>0 proof is rejected: a signed "
                "linear readout admits kernel and cancellation countermodels unless a stronger one-channel/positive-cone theorem or official "
                "contraction is supplied. The owner/no-w_A zero route is selected as the next derivation target."
            ),
            "current_evidence": (
                "4360 source register, external source ledger, portal probe, official route rows, c_min rows, parent nondegeneracy attempt rows, "
                "owner route rows, runner, claim gates, decision, status, next target and validation CSV."
            ),
            "status": "official_sources_public_only_cmin_not_computed_generic_nondegeneracy_rejected_owner_zero_route_selected_nonclaim",
            "next_test": "Derive the owner/no-w_A theorem from parent matter-action grammar or demote source coupling to explicit closure.",
            "key_risk": "Looping portal probes; treating public eta bound as tau_WEP; deriving positivity after signed readout; adopting owner axiom without proof.",
        }
    )
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_formal_doc(tables: Dict[str, List[Dict[str, str]]]) -> None:
    formal = f"""# 376 PPC4161 transition official MICROSCOPE readout or parent nondegeneracy

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. 4360 does not prove public local GR, Newton, WEP, PPN, R10, clock, orbital, EM, or source-coupling safety.

## Result

4360 attacks the exact 4359 lock instead of just restating it:

```text
tau_min = k_min*s_min*m_min*c_min/N_max.
```

The live question is whether `c_min>0` can be sourced from official MICROSCOPE readout/source/material data or proved by parent nondegeneracy.

The source hunt improves the map but does not close the finite route. Public MICROSCOPE sources give the `eta` observable/readout context and the official data-portal route. This runtime still does not acquire the live CMSM arrays/schema, and public result rows do not expose the MTS pairing:

```text
<K_CMSM, V_ST>,   V_ST := S_Earth x M_TiPt.
```

The parent nondegeneracy proof also fails in its generic form. A nonzero signed linear readout functional has a kernel, and the MICROSCOPE analysis channel is not a simple positive bulk map. Thus:

```text
K_CMSM != 0 and V_ST != 0  does not imply  c_min > 0.
```

The best next route is now the clean zero route:

```text
derive owner/no-w_A theorem
=> Delta_w_TiPt = 0
```

If that theorem cannot be derived from the parent matter-action grammar, the source-coupling branch must be demoted to explicit closure with finite WEP/PPN/R10/clock/orbital rows.

## Source Register

{md_table(tables["source"], ["source_id", "path", "path_exists", "needle_found", "line_number", "role", "valid_for_claim"])}

## External Source Ledger

{md_table(tables["external"], ["external_id", "url", "source_type", "extracted_item", "use_in_4360", "source_backed", "valid_for_claim"])}

## Portal Probe

{md_table(tables["probe"], ["probe_id", "url", "probe_status", "http_status", "content_type", "bytes_sampled", "schema_or_data_inventory_acquired", "error", "valid_for_claim"])}

## Official Route Rows

{md_table(tables["official"], ["route_id", "object", "acquired_level", "what_it_gives", "what_it_does_not_give", "claim_effect", "valid_for_claim"])}

## Cmin Rows

{md_table(tables["cmin"], ["cmin_id", "object", "definition", "status", "numeric_value", "why_not_numeric", "valid_for_claim"])}

## Parent Nondegeneracy Attempt Rows

{md_table(tables["parent"], ["attempt_id", "target", "attempt", "result", "reason", "what_would_close", "valid_for_claim"])}

## Owner Route Rows

{md_table(tables["owner"], ["owner_id", "route", "statement", "effect_if_proved", "current_status", "risk", "valid_for_claim"])}

## Runner

{md_table(tables["runner"], ["runner_id", "input", "action", "result", "claim_allowed", "valid_for_claim"])}

## Claim Gates

{md_table(tables["gates"], ["gate_id", "claim_component", "gate_pass", "claim_allowed", "reason", "valid_for_claim"])}

## Decision

{md_table(tables["decision"], ["decision_id", "decision", "reason", "next_action", "claim_allowed", "valid_for_claim"])}

## Status

{md_table(tables["status"], ["status_id", "item", "status", "note"])}

## Next Target

{md_table(tables["next"], ["next_target_id", "next_target", "target_question", "preferred_route", "fallback_route", "valid_for_claim"])}
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")
    DOC_PATH.write_text(formal.replace("# 376 PPC4161", "# 4360 - Y5/R2FR"), encoding="utf-8")


def append_spine_and_packet() -> None:
    spine_block = f"""
## PPC4161 4360 official MICROSCOPE readout or parent nondegeneracy

Marker: `{MARKER}`

4360 re-attacks the finite WEP route directly. Public MICROSCOPE sources support the observable/result/data-portal context, but no live CMSM array/schema is acquired in this runtime and public eta rows do not expose the MTS contraction:

```text
<K_CMSM, S_Earth x M_TiPt>.
```

The generic parent `c_min>0` proof is rejected: signed linear readout channels have kernels and cancellation modes unless the parent supplies a one-channel/positive-cone theorem or official arrays compute a nonzero alignment. The next target is therefore the owner/no-`w_A` zero theorem; if that fails, source coupling must be an explicit closure parameter rather than hidden in tau.
"""
    append_once(FORMAL / "07-unification-spine.md", MARKER, spine_block)

    packet_block = f"""
## PPC4161 packet update 4360 official readout/nondegeneracy fork

Marker: `{PACKET_MARKER}`

Packet update: official MICROSCOPE public sources are enough for the eta/readout/result context but not enough for `c_min>0`. The generic nondegeneracy proof fails because `V_ST` can remain in `ker(K_CMSM)` under a signed readout. The packet now routes forward to the parent owner/no-`w_A` theorem or explicit source-coupling closure.
"""
    append_once(FORMAL / "180-PPC4161-private-local-packet-integration.md", PACKET_MARKER, packet_block)


def validate(tables: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    csv_paths = [
        SOURCE_DIR / f"P8_Y5_R2FR_4360_{name}.csv"
        for name in [
            "SOURCE_REGISTER",
            "EXTERNAL_SOURCE_LEDGER",
            "PORTAL_PROBE",
            "OFFICIAL_ROUTE_ROWS",
            "CMIN_ROWS",
            "PARENT_NONDEGENERACY_ATTEMPT_ROWS",
            "OWNER_ROUTE_ROWS",
            "RUNNER",
            "CLAIM_GATES",
            "DECISION",
            "STATUS",
            "NEXT_TARGET",
        ]
    ]

    def all_csv_parse(paths: Iterable[Path]) -> bool:
        for path in paths:
            try:
                with path.open(newline="", encoding="utf-8") as handle:
                    list(csv.DictReader(handle))
            except Exception:
                return False
        return True

    checks = [
        ("formal_doc_written", FORMAL_PATH.exists(), str(FORMAL_PATH)),
        ("post_doc_written", DOC_PATH.exists(), str(DOC_PATH)),
        ("marker_in_formal", MARKER in read_text(FORMAL_PATH), MARKER),
        ("decision_in_formal", DECISION in read_text(FORMAL_PATH), DECISION),
        ("all_local_sources_exist", all(row["path_exists"] == "True" for row in tables["source"]), ""),
        ("all_local_needles_found", all(row["needle_found"] == "True" for row in tables["source"]), ""),
        ("external_sources_recorded", len(tables["external"]) >= 5, str(len(tables["external"]))),
        ("onera_source_recorded", any("microscope.onera.fr" in row["url"] for row in tables["external"]), ""),
        ("cmsm_probe_recorded", any("cmsm-ds.onera.fr" in row["url"] for row in tables["probe"]), ""),
        ("portal_does_not_promote_claim", all(row["valid_for_claim"] == "False" for row in tables["probe"]), ""),
        ("official_arrays_not_acquired", any(row["object"] == "official CMSM machine-readable products" and row["acquired_level"] != "ACQUIRED" for row in tables["official"]), ""),
        ("cmin_not_derived", any(row["object"] == "tau_min route" and row["status"] == "C_MIN_NOT_DERIVED" for row in tables["cmin"]), ""),
        ("generic_nondegeneracy_rejected", any(row["attempt_id"] == "PND4360_4_verdict" and row["result"] == "NOT_CLOSED" for row in tables["parent"]), ""),
        ("owner_route_selected", any(row["owner_id"] == "OWN4360_2_next_attack" and row["current_status"] == "NEXT_TARGET_SELECTED" for row in tables["owner"]), ""),
        ("claim_gates_block_local_gr", any(row["gate_id"] == "CG4360_4_local_GR_Newton_WEP" and row["claim_allowed"] == "False" for row in tables["gates"]), ""),
        ("next_target_present", NEXT_TARGET in read_text(FORMAL_PATH), NEXT_TARGET),
        ("claim_register_updated", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), CLAIM_ID),
        ("spine_marker_present", MARKER in read_text(FORMAL / "07-unification-spine.md"), MARKER),
        ("packet_marker_present", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), PACKET_MARKER),
        ("csv_parse", all_csv_parse(csv_paths), str(len(csv_paths))),
        ("no_valid_claim_rows", all(row.get("valid_for_claim", "False") == "False" for table in tables.values() for row in table), ""),
        ("generated_under_project", str(FORMAL_PATH).startswith(str(ROOT)) and str(DOC_PATH).startswith(str(ROOT)), str(ROOT)),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "passed": str(bool(passed)),
            "detail": detail,
            "valid_for_claim": "False",
        }
        for check_id, passed, detail in checks
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    probes = portal_probe_rows()
    tables = {
        "source": source_rows(),
        "external": EXTERNAL_SOURCES,
        "probe": probes,
        "official": official_route_rows(probes),
        "cmin": cmin_rows(),
        "parent": parent_nondegeneracy_rows(),
        "owner": owner_route_rows(),
    }
    tables["runner"] = runner_rows(tables["cmin"], tables["parent"])
    tables["gates"] = claim_gate_rows()
    tables["decision"] = decision_rows()
    tables["status"] = status_rows()
    tables["next"] = next_target_rows()

    outputs = {
        "SOURCE_REGISTER": tables["source"],
        "EXTERNAL_SOURCE_LEDGER": tables["external"],
        "PORTAL_PROBE": tables["probe"],
        "OFFICIAL_ROUTE_ROWS": tables["official"],
        "CMIN_ROWS": tables["cmin"],
        "PARENT_NONDEGENERACY_ATTEMPT_ROWS": tables["parent"],
        "OWNER_ROUTE_ROWS": tables["owner"],
        "RUNNER": tables["runner"],
        "CLAIM_GATES": tables["gates"],
        "DECISION": tables["decision"],
        "STATUS": tables["status"],
        "NEXT_TARGET": tables["next"],
    }
    for name, rows in outputs.items():
        write_csv(SOURCE_DIR / f"P8_Y5_R2FR_4360_{name}.csv", rows)

    write_formal_doc(tables)
    append_claim_register()
    append_spine_and_packet()

    validation_rows = validate(tables)
    write_csv(VALIDATION_PATH, validation_rows)
    failed = [row for row in validation_rows if row["passed"] != "True"]
    print(f"4360: wrote {len(outputs)} csv artifacts plus validation")
    print(f"4360: validation rows={len(validation_rows)} failed={len(failed)}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
