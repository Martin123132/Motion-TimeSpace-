from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"
MICROSCOPE_TEX = ROOT / "source-intake" / "external-sources" / "microscope_2209.15488_source" / "chap9.tex"

DOC = ROOT / "3263-Y5-R2FR-source-profile-channel-projection-or-parent-domain-lock-under-AX1090.md"

TAU_READOUT_MIN = 0.98
TAU_READOUT_MAX = 1.02

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3263_SOURCE_REGISTER.csv",
    "microscope_channel": OUT / "P8_Y5_R2FR_3263_MICROSCOPE_EP_CHANNEL_EVIDENCE.csv",
    "conventions": OUT / "P8_Y5_R2FR_3263_ETA_LEVEL_VS_PARENT_SOURCE_CONVENTION_SPLIT.csv",
    "projection": OUT / "P8_Y5_R2FR_3263_CHANNEL_PROJECTION_RESULT.csv",
    "bounds": OUT / "P8_Y5_R2FR_3263_CONVENTION_BOUND_OUTPUT_NONCLAIM.csv",
    "remaining": OUT / "P8_Y5_R2FR_3263_REMAINING_PARENT_SOURCE_INPUTS.csv",
    "domain": OUT / "P8_Y5_R2FR_3263_PARENT_DOMAIN_LOCK_AUDIT.csv",
    "gates": OUT / "P8_Y5_R2FR_3263_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3263_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3263_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3263_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_ok(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        read_csv(path)
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_ok(path) if path.suffix.lower() == ".csv" else True


def evidence(path: Path, needles: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lowered_needles = [needle.lower() for needle in needles]
    hits: list[str] = []
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for line_number, line in enumerate(handle, start=1):
            lowered_line = line.lower()
            if any(needle in lowered_line for needle in lowered_needles):
                clean = " ".join(line.strip().split())
                if clean:
                    hits.append(f"L{line_number}:{clean[:280]}")
            if len(hits) >= limit:
                break
    return " | ".join(hits) if hits else "NO_MATCH"


def line_hit(path: Path, needle: str) -> tuple[int | None, str]:
    if not path.exists():
        return None, "MISSING_SOURCE"
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for line_number, line in enumerate(handle, start=1):
            if needle in line:
                return line_number, " ".join(line.strip().split())
    return None, "NO_MATCH"


def float_or_none(value: Any) -> float | None:
    try:
        return float(str(value).strip())
    except Exception:
        return None


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


def product_bound() -> float:
    path = OUT / "P8_Y5_R2FR_3260_DD_WEP_BOUND_OUTPUT_NONCLAIM.csv"
    for row in read_csv(path):
        if row.get("bound_id") == "BOUT3260_4_reported_level_product_bound":
            value = float_or_none(row.get("value"))
            if value is None:
                raise ValueError("missing product bound")
            return value
    raise ValueError("missing BOUT3260_4_reported_level_product_bound")


def source_register() -> list[dict[str, Any]]:
    specs = [
        (
            "SRC3263_3262_handoff",
            ROOT / "3262-Y5-R2FR-parent-action-domain-signature-or-source-tau-factor-intake-under-AX1090.md",
            "3262 selected source-profile/channel projection or parent domain lock",
            ["NEXT3262_0_3263", "tau_channel_projection", "tau_source_profile"],
        ),
        (
            "SRC3263_3262_tau",
            OUT / "P8_Y5_R2FR_3262_TAU_WEP_FACTORIZATION.csv",
            "tau_WEP factorization with sourced readout subfactor",
            ["TAU3262_1_readout_X", "TAU3262_3_channel_projection"],
        ),
        (
            "SRC3263_3262_bound",
            OUT / "P8_Y5_R2FR_3262_READOUT_REDUCED_PRODUCT_BOUND_NONCLAIM.csv",
            "readout-reduced product bound",
            ["RB3262_2_remaining_product_worst"],
        ),
        (
            "SRC3263_MICROSCOPE_tex",
            MICROSCOPE_TEX,
            "MICROSCOPE fitted EP channel equations",
            ["delta_x g_x", "parameters", "delta_x", "eta"],
        ),
        (
            "SRC3263_1899_pack",
            OUT / "P8_Y5_PARENT_QLOC_1899_WEP_INPUT_PACK_NONCLAIM.csv",
            "remaining parent-source profile inputs",
            ["WIP1899_1_source_worldtube_profile", "WIP1899_5_force_map"],
        ),
        (
            "SRC3263_1397_unique_F2",
            OUT / "P8_Y5_R10_1397_UNIQUE_MAXWELL_F2_PROOF_AUDIT.csv",
            "parent domain no-counterterm status",
            ["UMF1397_2_operator_basis_uniqueness", "UMF1397_7_current_verdict"],
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, role, needles in specs:
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def microscope_channel_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "MCH3263_0_force_model",
            "\\vv\\gamma^{(d)} = \\delta(2,1) \\vv{g}(O_{\\rm sat})",
            "raw differential acceleration contains the Eotvos/mass-ratio parameter multiplying satellite gravity.",
        ),
        (
            "MCH3263_1_g_source",
            "\\item $\\vv{g}(O_{\\rm sat}) $ is the gravity acceleration computed at the centre of the satellite",
            "experimental source signal is computed Earth gravity at satellite centre.",
        ),
        (
            "MCH3263_2_corrected_channel",
            "\\Gamma^{(d)}_{x, {\\rm corr}}=\\tilde{b}_x^{'(d)}+\\delta_x g_x",
            "corrected fitted X channel carries delta_x times g_x.",
        ),
        (
            "MCH3263_3_uncorrelated_signals",
            "these signals are almost uncorrelated",
            "the EP channel is separated by frequency/signature from nuisance terms in the model.",
        ),
        (
            "MCH3263_4_parameters_estimated",
            "The parameters $\\delta_x$, $\\delta_z$, $\\Delta'_{x}$ and $\\Delta'_{z}$ are estimated.",
            "delta_x is a fitted parameter, not a hidden hand-assigned projection.",
        ),
        (
            "MCH3263_5_eta_identification",
            "the conventional E\\\"otv\\\"os parameter $\\eta$ {can be practically identified} to the parameter  $\\delta_{x}$",
            "paper identifies final eta with delta_x in practice.",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for evidence_id, needle, role in specs:
        line_number, text = line_hit(MICROSCOPE_TEX, needle)
        rows.append(
            {
                "evidence_id": evidence_id,
                "source_path": str(MICROSCOPE_TEX),
                "line_number": line_number if line_number is not None else "NO_MATCH",
                "text_excerpt": text,
                "role": role,
                "valid_for_claim": "false",
            }
        )
    return rows


def convention_rows() -> list[dict[str, Any]]:
    return [
        {
            "convention_id": "CONV3263_ETA_LEVEL",
            "definition": "Define B_alpha^eta by eta_AB^EM = DeltaQe_AB * B_alpha^eta + residual.",
            "tau_status": "experimental EP-channel projection is already absorbed into the published eta fit; only readout calibration uncertainty remains",
            "bound_use": "use 3260 bound directly, or 3262 conservative readout-corrected version",
            "what_remains": "no-cancellation/full-channel control and parent interpretation of B_alpha^eta",
            "valid_for_claim": "false",
        },
        {
            "convention_id": "CONV3263_PARENT_SOURCE",
            "definition": "Define upstream B_alpha^parent before source/readout projection.",
            "tau_status": "requires tau_source_profile and tau_channel_projection from parent source profile or official/equivalent arrays",
            "bound_use": "only product B_alpha^parent*tau_source_profile*tau_channel_projection is bounded",
            "what_remains": "source worldtube/profile, force map, and parent source-charge normalization",
            "valid_for_claim": "false",
        },
    ]


def projection_rows() -> list[dict[str, Any]]:
    return [
        {
            "projection_id": "PROJ3263_0_observed_eta_channel",
            "projection": "eta_AB -> MICROSCOPE fitted delta_x",
            "result": "SOURCE_BACKED",
            "formula": "delta_x = tilde(a)_c11 eta_AB with |tilde(a)_c11-1|<2e-2 and final eta practically identified with delta_x",
            "claim_effect": "the experimental channel projection is not a remaining blocker for eta-level bounds",
            "valid_for_claim": "false",
        },
        {
            "projection_id": "PROJ3263_1_parent_source_channel",
            "projection": "MTS parent source residual -> eta_AB",
            "result": "NOT_CLOSED",
            "formula": "eta_AB^MTS = source/force/readout contraction of parent residual",
            "claim_effect": "still requires parent source-charge theorem or source_profile/force_map inputs",
            "valid_for_claim": "false",
        },
        {
            "projection_id": "PROJ3263_2_no_double_tau",
            "projection": "avoid multiplying by tau twice",
            "result": "GUARD_ACTIVE",
            "formula": "if B_alpha is eta-level, do not also include tau_channel_projection; if B_alpha is parent-source-level, include tau factors explicitly",
            "claim_effect": "prevents over-suppressing the residual by convention confusion",
            "valid_for_claim": "false",
        },
    ]


def bound_rows() -> list[dict[str, Any]]:
    direct = product_bound()
    conservative = direct / TAU_READOUT_MIN
    return [
        {
            "bound_id": "CB3263_0_eta_level_reported",
            "convention": "CONV3263_ETA_LEVEL",
            "quantity": "|B_alpha^eta|",
            "formula": "2.7e-15/|DeltaQe_DD|",
            "value": f"{direct:.12e}",
            "status": "OBSERVED_ETA_LEVEL_BOUND",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "CB3263_1_eta_level_readout_conservative",
            "convention": "CONV3263_ETA_LEVEL",
            "quantity": "|B_alpha^eta| with tau_readout_X>=0.98",
            "formula": "(2.7e-15/|DeltaQe_DD|)/0.98",
            "value": f"{conservative:.12e}",
            "status": "CONSERVATIVE_READOUT_CORRECTED_BOUND",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "CB3263_2_parent_source_product",
            "convention": "CONV3263_PARENT_SOURCE",
            "quantity": "|B_alpha^parent*tau_source_profile*tau_channel_projection|",
            "formula": "(2.7e-15/|DeltaQe_DD|)/0.98",
            "value": f"{conservative:.12e}",
            "status": "UPSTREAM_PRODUCT_ONLY",
            "valid_for_claim": "false",
        },
    ]


def remaining_rows() -> list[dict[str, Any]]:
    return [
        {
            "remaining_id": "REM3263_0_beta_source_interpretation",
            "missing_piece": "parent meaning of beta_source_alpha",
            "current_best": "eta-level product bound is usable empirically, but parent source-charge interpretation remains open",
            "needed_next": "same-owner Hamiltonian/source theorem or force-map input",
            "valid_for_claim": "false",
        },
        {
            "remaining_id": "REM3263_1_source_profile_only_for_upstream",
            "missing_piece": "tau_source_profile",
            "current_best": "not needed for eta-level bound; needed only if B_alpha is defined upstream of the observed Eotvos parameter",
            "needed_next": "Earth/source worldtube profile or theorem reducing parent residual to eta",
            "valid_for_claim": "false",
        },
        {
            "remaining_id": "REM3263_2_multi_channel_control",
            "missing_piece": "no-cancellation/full-channel fit",
            "current_best": "isolated EM/DD branch bound is hard but not full MTS WEP pass",
            "needed_next": "include light-quark/surface/readout channels or parent no-cancellation theorem",
            "valid_for_claim": "false",
        },
    ]


def domain_rows() -> list[dict[str, Any]]:
    return [
        {
            "domain_id": "DOM3263_0_eta_route_vs_zero_route",
            "question": "Should we prioritize parent-domain lock or eta-level empirical bound?",
            "answer": "both are now cleanly separated: eta-level bound constrains fallback; parent-domain lock would remove the branch by b_alpha_EM=0",
            "current_status": "BOUND_ROUTE_EXECUTABLE_ZERO_ROUTE_CONDITIONAL",
            "valid_for_claim": "false",
        },
        {
            "domain_id": "DOM3263_1_counterterm_block",
            "question": "What blocks fixed EM zero?",
            "answer": "UMF1397 still retains lambda_A while quotient-only/independent F_Q^2 counterterm is not forbidden by a signed parent domain",
            "current_status": "NO_COUNTERTERM_NOT_SIGNED",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG3263_0_eta_channel_projection",
            "gate": "MICROSCOPE eta-level channel projection sourced",
            "passed": "true",
            "reason": "measurement model fits delta_x g_x and identifies eta with delta_x in practice",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3263_1_parent_source_projection",
            "gate": "MTS parent source residual projected to eta",
            "passed": "false",
            "reason": "same-owner source theorem or source_profile/force-map still missing",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3263_2_parent_domain_lock",
            "gate": "parent domain forbids lambda_A counterterm",
            "passed": "false",
            "reason": "no-counterterm theorem remains conditional",
            "claim_allowed": "false",
        },
        {
            "gate_id": "CG3263_3_local_GR",
            "gate": "local GR/Newton/Maxwell promotion",
            "passed": "false",
            "reason": "eta-level bound is not a full parent-source/local-GR derivation",
            "claim_allowed": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3263_0",
            "verdict": "ETA_CHANNEL_PROJECTION_SOURCED_PARENT_SOURCE_STILL_OPEN",
            "what_moved": "the experimental channel projection is closed for eta-level bounds, avoiding a false tau blocker",
            "best_next": "attack parent source-charge meaning of beta_source_alpha or the parent no-counterterm domain",
            "fallback_next": "add other composition channels to prevent EM-only cancellation mistakes",
            "valid_for_claim": "false",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3263_0_3264",
            "selected": "primary",
            "target_doc": "3264-Y5-R2FR-parent-source-charge-meaning-or-multichannel-WEP-vector-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3264_parent_source_charge_meaning_or_multichannel_WEP_vector.py",
            "objective": "Either derive the parent source-charge meaning of beta_source_alpha in the eta-level branch, or add the non-EM DD/material channels so the WEP comparison is not EM-only.",
            "guardrail": "Do not reintroduce tau_channel_projection for eta-level B_alpha; use it only for upstream parent-source convention.",
            "valid_for_claim": "false",
        }
    ]


def formalization_changed_count() -> int:
    if not FW.exists():
        return 0
    script_mtime = Path(__file__).stat().st_mtime
    return sum(1 for path in FW.rglob("*") if path.is_file() and path.stat().st_mtime > script_mtime)


def validation_rows() -> list[dict[str, Any]]:
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    source_rows = source_register()
    channel = microscope_channel_rows()
    direct = product_bound()
    conservative = direct / TAU_READOUT_MIN
    bound_values = {row["bound_id"]: row["value"] for row in bound_rows()}
    validations = [
        {
            "check_id": "VAL3263_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": bool_str(all(row["exists"] == "true" for row in source_rows)),
            "detail": ";".join(row["source_id"] for row in source_rows if row["exists"] != "true"),
        },
        {
            "check_id": "VAL3263_1_sources_parse",
            "check": "all cited source CSV/MD/TEX paths parse",
            "passed": bool_str(all(row["parse_ok"] == "true" for row in source_rows)),
            "detail": ";".join(row["source_id"] for row in source_rows if row["parse_ok"] != "true"),
        },
        {
            "check_id": "VAL3263_2_channel_lines_found",
            "check": "MICROSCOPE channel evidence lines are found",
            "passed": bool_str(all(row["line_number"] != "NO_MATCH" for row in channel)),
            "detail": ";".join(f"{row['evidence_id']}:{row['line_number']}" for row in channel),
        },
        {
            "check_id": "VAL3263_3_outputs_parse",
            "check": "all 3263 output CSVs parse",
            "passed": bool_str(all(csv_ok(path) for path in output_paths)),
            "detail": ";".join(str(path) for path in output_paths if not csv_ok(path)),
        },
        {
            "check_id": "VAL3263_4_conservative_bound_matches",
            "check": "conservative eta-level bound equals direct/0.98",
            "passed": bool_str(abs(float(bound_values["CB3263_1_eta_level_readout_conservative"]) - conservative) <= conservative * 1e-12),
            "detail": bound_values["CB3263_1_eta_level_readout_conservative"],
        },
        {
            "check_id": "VAL3263_5_claim_gates_false",
            "check": "no 3263 claim gate allows local-GR/WEP/Maxwell promotion",
            "passed": bool_str(all(row["claim_allowed"] == "false" for row in claim_gate_rows())),
            "detail": "all claim_allowed=false",
        },
        {
            "check_id": "VAL3263_6_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": bool_str(formalization_changed_count() == 0),
            "detail": f"formalization_changed_count={formalization_changed_count()}",
        },
        {
            "check_id": "VAL3263_7_overall",
            "check": "3263 validation overall",
            "passed": "PENDING",
            "detail": "computed after rows are assembled",
        },
    ]
    overall = all(row["passed"] == "true" for row in validations if row["check_id"] != "VAL3263_7_overall")
    validations[-1]["passed"] = bool_str(overall)
    validations[-1]["detail"] = "all required checks passed" if overall else "one or more checks failed"
    return validations


def write_doc() -> None:
    sources = source_register()
    channel = microscope_channel_rows()
    conventions = convention_rows()
    projections = projection_rows()
    bounds = bound_rows()
    remaining = remaining_rows()
    domain = domain_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_rows()
    validations = validation_rows()
    conservative = product_bound() / TAU_READOUT_MIN
    content = f"""# 3263 - Source-profile channel projection or parent-domain lock under AX1090

Private derivation/checkpoint. This does not claim local GR, Newton, Maxwell, WEP, R10, PPN, clock, orbital, material-response, or public source-coupling success.

## Verdict
- `3263` closes the experimental EP-channel projection for the **eta-level** convention: MICROSCOPE fits `delta_x g_x` and identifies final `eta` with `delta_x` in practice.
- Therefore, if `B_alpha` is defined by `eta_AB^EM = DeltaQe_AB B_alpha^eta`, do **not** multiply by an extra `tau_channel_projection`.
- The conservative eta-level bound remains `|B_alpha^eta| <= {conservative:.12e}` after the 0.98 readout factor.
- The parent-source convention is still open: projecting an upstream MTS source residual into eta still needs the source-charge/force-map theorem.

## Source Register
{md_table(sources, ["source_id", "exists", "parse_ok", "role", "evidence_hits", "valid_for_claim"])}

## MICROSCOPE EP Channel Evidence
{md_table(channel, ["evidence_id", "line_number", "text_excerpt", "role", "valid_for_claim"])}

## Eta-Level vs Parent-Source Convention Split
{md_table(conventions, ["convention_id", "definition", "tau_status", "bound_use", "what_remains", "valid_for_claim"])}

## Channel Projection Result
{md_table(projections, ["projection_id", "projection", "result", "formula", "claim_effect", "valid_for_claim"])}

## Convention Bound Output
{md_table(bounds, ["bound_id", "convention", "quantity", "formula", "value", "status", "valid_for_claim"])}

## Remaining Parent-Source Inputs
{md_table(remaining, ["remaining_id", "missing_piece", "current_best", "needed_next", "valid_for_claim"])}

## Parent Domain Lock Audit
{md_table(domain, ["domain_id", "question", "answer", "current_status", "valid_for_claim"])}

## Claim Gates
{md_table(gates, ["gate_id", "gate", "passed", "reason", "claim_allowed"])}

## Decision
{md_table(decisions, ["decision_id", "verdict", "what_moved", "best_next", "fallback_next", "valid_for_claim"])}

## Next Target
{md_table(next_targets, ["next_id", "selected", "target_doc", "target_script", "objective", "guardrail", "valid_for_claim"])}

## Validation
{md_table(validations, ["check_id", "check", "passed", "detail"])}

Generated UTC: {RUN_UTC}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows_by_key = {
        "sources": source_register(),
        "microscope_channel": microscope_channel_rows(),
        "conventions": convention_rows(),
        "projection": projection_rows(),
        "bounds": bound_rows(),
        "remaining": remaining_rows(),
        "domain": domain_rows(),
        "gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
    }
    for key, rows in rows_by_key.items():
        write_csv(OUTPUTS[key], rows)
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc()
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
