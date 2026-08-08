from __future__ import annotations

import csv
import re
import subprocess
from pathlib import Path
from typing import Dict, Iterable, List, Sequence


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


def text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for line_number, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return line_number
    return 0


def text_files(root: Path) -> List[Path]:
    allowed = {".md", ".csv", ".txt", ".py"}
    blocked_parts = {".git", "__pycache__", ".ipynb_checkpoints", "runs"}
    files: List[Path] = []
    for folder in ["formalization-workbench", "post-checkpoint-work", "core-mts-framework"]:
        base = root / folder
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in allowed:
                continue
            relative_parts = path.relative_to(root).parts
            if any(part in blocked_parts for part in relative_parts):
                continue
            if "source-intake" in relative_parts and "mts_residuals" not in relative_parts:
                continue
            try:
                if path.stat().st_size > 2_000_000:
                    continue
            except OSError:
                continue
            files.append(path)
    return files


def scan_patterns(root: Path, max_examples: int = 8) -> List[Dict[str, object]]:
    patterns: Sequence[Dict[str, object]] = [
        {
            "carrier_id": "SWEEP4481_wave_flux_poynting",
            "carrier_class": "wave_flux_poynting",
            "regex": r"\b(Poynting|flux|wave vector|wave-vector|polarization|radiation stress|EM wave|electromagnetic wave)\b",
            "orientation_content": "vector/flux/polarization can form l=2 STF products",
        },
        {
            "carrier_id": "SWEEP4481_tidal_hessian_stf",
            "carrier_class": "tidal_hessian_STF",
            "regex": r"\b(STF|tracefree|trace-free|Hessian|tidal|l=2|quadrupole|P2)\b",
            "orientation_content": "rank-2 tracefree/tidal carrier channel",
        },
        {
            "carrier_id": "SWEEP4481_boundary_normal",
            "carrier_class": "boundary_normal",
            "regex": r"\b(boundary normal|normal vector|boundary orientation|boundary flux|boundary data|symplectic flux)\b",
            "orientation_content": "boundary normal can source b^{<i}b^{j>}",
        },
        {
            "carrier_id": "SWEEP4481_source_worldtube_l2",
            "carrier_class": "source_worldtube_l2",
            "regex": r"\b(source[- ]worldtube|worldtube|same-source|same source|Delta J_2|J2_eff|J_2|source-domain|source domain)\b",
            "orientation_content": "ordinary source multipoles or extra source-map residuals",
        },
        {
            "carrier_id": "SWEEP4481_spin_nematic_director",
            "carrier_class": "spin_nematic_director",
            "regex": r"\b(spin axis|spin-axis|nematic|director|orientation distribution|anisotropic support metric)\b",
            "orientation_content": "director/spin/nematic axis can form l=2 STF products",
        },
        {
            "carrier_id": "SWEEP4481_phase_carrier_weights",
            "carrier_class": "phase_carrier_weights",
            "regex": r"\b(carrier weights|carrier inventory|phase/carrier|W_I|k_I=dS_I|multicarrier|phase ensemble)\b",
            "orientation_content": "carrier ensemble can become orientation-carrying if directions survive",
        },
        {
            "carrier_id": "SWEEP4481_scalar_only_parent",
            "carrier_class": "scalar_only_parent",
            "regex": r"\b(scalar psi|scalar `psi`|ψ|psi field|SO\(3\)-scalar|scalar marker)\b",
            "orientation_content": "scalar-only branch supports zero theorem only if exhaustive",
        },
    ]
    rows: List[Dict[str, object]] = []
    for spec in patterns:
        rg_roots = [
            root / "formalization-workbench",
            root / "post-checkpoint-work",
            root / "core-mts-framework",
        ]
        command = [
            "rg",
            "-n",
            "-i",
            "--max-count",
            "1",
            "--max-filesize",
            "2M",
            "-g",
            "*.md",
            "-g",
            "*.csv",
            "-g",
            "*.txt",
            "-g",
            "*.py",
            "-g",
            "!**/runs/**",
            "-g",
            "!**/source-intake/**",
            str(spec["regex"]),
            *[str(path) for path in rg_roots if path.exists()],
        ]
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            timeout=30,
        )
        output = completed.stdout.splitlines() if completed.returncode in {0, 1} else []
        hit_count = len(output)
        hit_files = set()
        examples: List[str] = []
        for line in output:
            match = re.match(r"^(.*):(\d+):(.*)$", line)
            if not match:
                continue
            path_text, line_number, content = match.groups()
            try:
                relative_path = str(Path(path_text).relative_to(root))
            except ValueError:
                relative_path = path_text
            hit_files.add(relative_path)
            if len(examples) < max_examples:
                examples.append(f"{relative_path}:{line_number}:{content.strip()[:180]}")
        rows.append(
            {
                "carrier_id": spec["carrier_id"],
                "carrier_class": spec["carrier_class"],
                "orientation_content": spec["orientation_content"],
                "hit_count": hit_count,
                "file_count": len(hit_files),
                "examples": " || ".join(examples),
                "sweep_status": "HITS_FOUND" if hit_count else "NO_DIRECT_HITS_FOUND",
                "zero_proof_impact": "blocks_alphabet_absence_claim" if hit_count and spec["carrier_class"] != "scalar_only_parent" else "supports_scalar_branch_only_if_exhaustive",
                "valid_for_claim": False,
            }
        )
    return rows


def carrier_inventory_rows(sweep_rows: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    hit_map = {str(row["carrier_class"]): int(row["hit_count"]) for row in sweep_rows}
    return [
        {
            "inventory_id": "CI4481_0_scalar_parent_branch",
            "carrier_class": "scalar_only_parent",
            "source_basis": "core action and 4480 SO(3)-scalar theorem",
            "sweep_hits": hit_map.get("scalar_only_parent", 0),
            "derivation_consequence": "If scalar marker/support is the exhaustive parent alphabet, Q_M_TF=0 follows.",
            "current_assessment": "SCALAR_BRANCH_EXISTS_BUT_NOT_EXHAUSTIVE",
            "Z_orientation_support": "partial",
            "finite_scorer_required": True,
            "valid_for_claim": False,
        },
        {
            "inventory_id": "CI4481_1_wave_flux_poynting",
            "carrier_class": "wave_flux_poynting",
            "source_basis": "heuristics plus core EM/wave language and 4480 counterroute",
            "sweep_hits": hit_map.get("wave_flux_poynting", 0),
            "derivation_consequence": "A finite flux/wave/polarization carrier can source S^{<i}S^{j>}, k^{<i}k^{j>} or e_TF^{ij}.",
            "current_assessment": "LIVE_COUNTERROUTE_NOT_PARENT_COEFFICIENT",
            "Z_orientation_support": "blocks_zero_until_routed_or_excluded",
            "finite_scorer_required": True,
            "valid_for_claim": False,
        },
        {
            "inventory_id": "CI4481_2_tidal_hessian_STF",
            "carrier_class": "tidal_hessian_STF",
            "source_basis": "1950/1951/3182 STF response and metric-slip rows",
            "sweep_hits": hit_map.get("tidal_hessian_STF", 0),
            "derivation_consequence": "Tracefree Hessian/tidal channels are exactly l=2 and need zero theorem or bound.",
            "current_assessment": "LIVE_STF_RESPONSE_ROUTE",
            "Z_orientation_support": "blocks_zero_until_B_eff_or_Sigma_H_zero",
            "finite_scorer_required": True,
            "valid_for_claim": False,
        },
        {
            "inventory_id": "CI4481_3_boundary_normal",
            "carrier_class": "boundary_normal",
            "source_basis": "867 boundary orientation warning and 1955 no-extra-boundary contract",
            "sweep_hits": hit_map.get("boundary_normal", 0),
            "derivation_consequence": "Boundary normals can source b^{<i}b^{j>} unless boundary orientation/flux is fixed or routed.",
            "current_assessment": "LIVE_BOUNDARY_FIREWALL_ROUTE",
            "Z_orientation_support": "blocks_zero_until_boundary_flux_zero",
            "finite_scorer_required": True,
            "valid_for_claim": False,
        },
        {
            "inventory_id": "CI4481_4_source_worldtube_l2",
            "carrier_class": "source_worldtube_l2",
            "source_basis": "1954/1955 GR-baseline subtraction and same-source map contract",
            "sweep_hits": hit_map.get("source_worldtube_l2", 0),
            "derivation_consequence": "Real source l=2 belongs to GR baseline only if same-source EH map signs; extra source-map residual must be bounded.",
            "current_assessment": "LIVE_SAME_SOURCE_MAP_GATE",
            "Z_orientation_support": "blocks_zero_until_same_source_map_signs",
            "finite_scorer_required": True,
            "valid_for_claim": False,
        },
        {
            "inventory_id": "CI4481_5_spin_nematic_director",
            "carrier_class": "spin_nematic_director",
            "source_basis": "4480 representation inventory plus corpus sweep",
            "sweep_hits": hit_map.get("spin_nematic_director", 0),
            "derivation_consequence": "Spin/nematic/director terms would source l=2 if present; absence needs an explicit parent alphabet certificate, not a failed text search.",
            "current_assessment": "NO_STRONG_DIRECT_HIT_BUT_ALPHABET_NOT_CERTIFIED",
            "Z_orientation_support": "unknown",
            "finite_scorer_required": True,
            "valid_for_claim": False,
        },
        {
            "inventory_id": "CI4481_6_phase_carrier_weights",
            "carrier_class": "phase_carrier_weights",
            "source_basis": "2275 minimal carrier inventory",
            "sweep_hits": hit_map.get("phase_carrier_weights", 0),
            "derivation_consequence": "Phase/carrier ensembles can represent local channels, but directional carrier distributions require isotropic averaging or l=2 scoring.",
            "current_assessment": "PROMISING_COUPLING_STRUCTURE_PARENT_UNSIGNED",
            "Z_orientation_support": "requires_isotropic_measure_or_bound",
            "finite_scorer_required": True,
            "valid_for_claim": False,
        },
    ]


def l2_bound_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "input_id": "L2BI4481_0_epsilon_Q_compact_bound",
            "symbol": "epsilon_Q",
            "value_or_bound": "0 <= epsilon_Q <= 1",
            "units": "dimensionless",
            "source_ref": "4480 compact-support parameterization",
            "status": "STRUCTURAL_BOUND_AVAILABLE_NONCLAIM",
            "claim_use": "can cap worst-case finite quadrupole amplitude, not evidence of pass",
            "valid_for_claim": False,
        },
        {
            "input_id": "L2BI4481_1_A_STF_orientation",
            "symbol": "A_STF^{ij}",
            "value_or_bound": "MISSING_UNIT_STF_ORIENTATION",
            "units": "dimensionless_tensor",
            "source_ref": "4480 finite branch",
            "status": "MISSING_CARRIER_GEOMETRY",
            "claim_use": "needed for non-worst-case PPN/clock/orbital/Shapiro projection",
            "valid_for_claim": False,
        },
        {
            "input_id": "L2BI4481_2_tau_Shapiro_Q_J2_scale",
            "symbol": "tau_Shapiro_Q / J2_eff",
            "value_or_bound": "J2_eff <= 2.0e-7 scale; rough pressure proxy 3.3e-8; transfer required",
            "units": "dimensionless J2-equivalent",
            "source_ref": "P8_Y5_R2FR_3169_EQUIVALENT_J2_K2_BOUNDS.csv",
            "status": "NUMERIC_SOURCE_HOOK_AVAILABLE_TRANSFER_BLOCKED",
            "claim_use": "usable only if J2_eff=K2*C_K2_unit/source-domain transfer is derived",
            "valid_for_claim": False,
        },
        {
            "input_id": "L2BI4481_3_tau_PPN_Q_private_gamma_policy",
            "symbol": "tau_PPN_Q",
            "value_or_bound": "6.7e-5 private STF/gamma screening scale only",
            "units": "dimensionless",
            "source_ref": "P8_Y5_PARENT_QLOC_1950_DIMENSIONLESS_STF_SOURCE_LEDGER.csv",
            "status": "PRIVATE_POLICY_NOT_FORMAL_L2_BOUND",
            "claim_use": "smoke threshold only; not a sourced anisotropic PPN covariance",
            "valid_for_claim": False,
        },
        {
            "input_id": "L2BI4481_4_W_STF_norm",
            "symbol": "||W_STF||_1",
            "value_or_bound": "MISSING",
            "units": "inverse profile units",
            "source_ref": "P8_Y5_PARENT_QLOC_1955_RESIDUAL_L2_BOUND_LEDGER.csv",
            "status": "MISSING_READOUT_NORM",
            "claim_use": "needed for residual l=2 bound after GR-baseline subtraction",
            "valid_for_claim": False,
        },
        {
            "input_id": "L2BI4481_5_same_source_residuals",
            "symbol": "DeltaJ2, P2R_extra, Deltah2",
            "value_or_bound": "MISSING",
            "units": "source/residual/boundary units",
            "source_ref": "P8_Y5_PARENT_QLOC_1955_RESIDUAL_L2_BOUND_LEDGER.csv",
            "status": "MISSING_RESIDUAL_ENVELOPES_OR_ZERO_THEOREMS",
            "claim_use": "needed to score extra MTS l=2 beyond GR baseline",
            "valid_for_claim": False,
        },
        {
            "input_id": "L2BI4481_6_tau_clock_Q",
            "symbol": "tau_clock_Q",
            "value_or_bound": "MISSING",
            "units": "dimensionless or declared clock convention",
            "source_ref": "4480 scorer contract",
            "status": "MISSING_CLOCK_QUADRUPOLE_BOUND",
            "claim_use": "needed if finite l=2 branch survives in clock/redshift arena",
            "valid_for_claim": False,
        },
        {
            "input_id": "L2BI4481_7_tau_orbital_Q",
            "symbol": "tau_orbital_Q",
            "value_or_bound": "MISSING",
            "units": "declared orbital convention",
            "source_ref": "4480 scorer contract and 1955 residual l2 bound formula",
            "status": "MISSING_ORBITAL_QUADRUPOLE_BOUND",
            "claim_use": "needed if finite l=2 branch survives in orbital/precession arena",
            "valid_for_claim": False,
        },
    ]


def zero_or_bound_decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "ZBD4481_0_zero_certificate",
            "question": "Can Z_orientation be signed from the current corpus?",
            "answer": "NO_NOT_YET",
            "reason": "scalar branch exists, but wave/flux, tidal/STF, boundary, source-worldtube and phase-carrier routes are live or unsigned",
            "consequence": "do not claim Q_M_TF=0 or local-GR/R10 pass",
            "next_action": "prove parent carrier alphabet closure or use finite l=2 scorer",
            "valid_for_claim": False,
        },
        {
            "decision_id": "ZBD4481_1_best_zero_route",
            "question": "What would close the zero branch?",
            "answer": "parent_action_alphabet_closure",
            "reason": "show all wave/EM/Poynting/readout/boundary/source carriers are after-variation data, quotient-vertical, common-mode, or isotropically averaged",
            "consequence": "then 4480 SO(3) theorem can promote to a real local branch theorem",
            "next_action": "4482 parent STF carrier alphabet closure",
            "valid_for_claim": False,
        },
        {
            "decision_id": "ZBD4481_2_best_bound_route",
            "question": "What is the most source-backed finite scorer route?",
            "answer": "GR_baseline_residual_l2_plus_J2_Shapiro_hook",
            "reason": "1954/1955 prevent unfairly penalizing GR source multipoles; 3169 supplies conditional J2/Shapiro scales if transfer is derived",
            "consequence": "bound route needs residual envelopes and source-domain transfer, not total solar J2",
            "next_action": "4482 J2eff transfer or residual l2 scorer inputs",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(
    source_rows: Sequence[Dict[str, object]],
    sweep_rows: Sequence[Dict[str, object]],
    inventory_rows: Sequence[Dict[str, object]],
    input_rows: Sequence[Dict[str, object]],
) -> List[Dict[str, object]]:
    sources_ok = all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in source_rows)
    sweep_ok = any(int(row.get("hit_count", 0)) > 0 for row in sweep_rows)
    non_scalar_live = any(
        int(row.get("sweep_hits", 0)) > 0 and row.get("carrier_class") != "scalar_only_parent"
        for row in inventory_rows
    )
    j2_hook = any(row.get("input_id") == "L2BI4481_2_tau_Shapiro_Q_J2_scale" for row in input_rows)
    numeric_ready = all(
        "MISSING" not in str(row.get("value_or_bound", "")) and row.get("valid_for_claim") is True
        for row in input_rows
    )
    return [
        {
            "gate_id": "CG4481_0_sources",
            "claim": "all cited local sources exist and needles are found",
            "gate_pass": sources_ok,
            "claim_allowed": False,
            "detail": "source register validates 4480, prior STF/coupling and J2 rows",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4481_1_corpus_sweep_executed",
            "claim": "carrier sweep was actually run over corpus files",
            "gate_pass": sweep_ok,
            "claim_allowed": False,
            "detail": "sweep rows include hit counts and example file:line anchors",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4481_2_Z_orientation_signed",
            "claim": "parent signs absence of all l=2 orientation carriers",
            "gate_pass": False,
            "claim_allowed": False,
            "detail": "non-scalar live or unsigned carrier routes remain; non_scalar_live=" + str(non_scalar_live),
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4481_3_l2_bound_pack_written",
            "claim": "l=2 finite scorer input pack exists",
            "gate_pass": j2_hook and len(input_rows) >= 8,
            "claim_allowed": False,
            "detail": "epsilon_Q structural bound, J2/Shapiro hook, PPN policy row, W_STF/residual/clock/orbital missing rows written",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4481_4_numeric_claim_ready",
            "claim": "finite l=2 scorer has claim-grade numeric/source inputs",
            "gate_pass": numeric_ready,
            "claim_allowed": False,
            "detail": "transfer, readout norm, residual envelopes, clock and orbital l=2 bounds remain missing or policy-only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4481_5_no_generated_claim_rows",
            "claim": "no generated row is promoted to local-GR evidence",
            "gate_pass": all(
                str(row.get("valid_for_claim")).lower() == "false"
                for group in [source_rows, sweep_rows, inventory_rows, input_rows]
                for row in group
            ),
            "claim_allowed": False,
            "detail": "4481 is an inventory and input-pack checkpoint, not a pass",
            "valid_for_claim": False,
        },
    ]
