from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2726-Y5-R2FR-parent-no-extension-minimality-and-LC-descent-or-Eoperator-bound-under-AX1090-closure.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2726_SOURCE_REGISTER.csv",
    "proof_audit": RESIDUALS / "P8_Y5_R2FR_2726_NO_EXTENSION_LC_PROOF_AUDIT.csv",
    "kill_switches": RESIDUALS / "P8_Y5_R2FR_2726_PARENT_KILL_SWITCH_LEDGER.csv",
    "countermodels": RESIDUALS / "P8_Y5_R2FR_2726_SURVIVING_COUNTERMODEL_LEDGER.csv",
    "residual_rows": RESIDUALS / "P8_Y5_R2FR_2726_NO_EXTENSION_LC_RESIDUAL_ROWS_NONCLAIM.csv",
    "lc_routes": RESIDUALS / "P8_Y5_R2FR_2726_LC_DESCENT_ROUTE_AUDIT.csv",
    "ejeff_update": RESIDUALS / "P8_Y5_R2FR_2726_EJEFF_UPDATE_VECTOR_NONCLAIM.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2726_CLAIM_GATES.csv",
    "blocker_stack": RESIDUALS / "P8_Y5_R2FR_2726_CURRENT_BLOCKER_STACK.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2726_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2726_NEXT_TARGET.csv",
    "project_snapshot": RESIDUALS / "P8_Y5_R2FR_2726_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2726_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2726_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_bounds": LOCAL_BOUNDS / "parent_no_extension_LC_operator_rows_2726_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "parent_no_extension_LC_EJeff_update_2726_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2726_READOUT_AFTER_VARIATION_GENERATOR_NEXT.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return ""
    return str(value)


def md_escape(value: Any) -> str:
    return normalize(value).replace("|", "\\|").replace("\n", "<br>")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="raise")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: normalize(row.get(key, "")) for key in fieldnames})


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


SOURCE_SPECS = [
    {
        "source_id": "SRC2726_0_2725",
        "label": "2725 direct handoff",
        "path": ROOT / "2725-Y5-R2FR-metric-only-second-order-Levi-Civita-operator-gate-or-Eoperator-bound-under-AX1090-closure.md",
        "needles": [
            "MSC2725_4_verdict",
            "PC2725_1_no_extension_minimality",
            "EOP2725_6_E_connection_metric_affine",
            "NEXT2725_0_selected",
            "VAL2725_OVERALL",
        ],
        "use": "selects parent no-extension/minimality and LC descent as the next gate",
    },
    {
        "source_id": "SRC2726_1_414",
        "label": "414 local invariant algebra gate",
        "path": ROOT / "414-local-quotient-invariant-algebra-triviality-gate.md",
        "needles": [
            "I_loc(Q) = I_geom",
            "local_invariant_algebra_triviality_derived",
            "extra_generators_eliminated",
            "local_GR_promoted",
        ],
        "use": "states the exact local no-marker algebra burden and records surviving generators",
    },
    {
        "source_id": "SRC2726_2_965",
        "label": "965 primitive quotient/no-marker",
        "path": ROOT / "965-Y5-R10-primitive-quotient-no-natural-marker-theorem-or-R2FR-full-curve-intake.md",
        "needles": [
            "PQ965_5_verdict",
            "ALG965_9_verdict",
            "MC965_2_quotient_invariant_scalar",
            "DEC965_3_next_hinge",
        ],
        "use": "primitive quotient/no-natural-marker theorem remains unproved; quotient-invariant scalar countermodels remain",
    },
    {
        "source_id": "SRC2726_3_966",
        "label": "966 generator elimination ranking",
        "path": ROOT / "966-Y5-R10-local-invariant-generator-elimination-or-R2FR-curve-digitizer.md",
        "needles": [
            "GE966_0_readout_projector",
            "GE966_4_memory_class_scalar",
            "GE966_7_verdict",
            "DG966_6",
        ],
        "use": "ranks local invariant generators and selects readout projector as the promising first kill route",
    },
    {
        "source_id": "SRC2726_4_573_csv",
        "label": "573 invariant generator debt",
        "path": RESIDUALS / "P8_Y5_R10_573_INVARIANT_GENERATOR_DEBT.csv",
        "needles": [
            "IG573_0_finite_fibre_spectrum",
            "IG573_1_relative_domain_class",
            "IG573_2_domain_selector",
            "IG573_3_memory_scalar",
            "IG573_4_species_constants",
            "IG573_5_readout_projector",
        ],
        "use": "machine-readable generator debt list",
    },
    {
        "source_id": "SRC2726_5_574_csv",
        "label": "574 generator elimination attempts",
        "path": RESIDUALS / "P8_Y5_R10_574_GENERATOR_ELIMINATION_ATTEMPTS.csv",
        "needles": [
            "GE574_0_readout_projector",
            "GE574_1_species_constants",
            "GE574_2_relative_class",
            "GE574_3_domain_selector",
            "GE574_4_memory_scalar",
            "GE574_5_finite_fibre",
        ],
        "use": "attempted elimination forms, all nonclaim",
    },
    {
        "source_id": "SRC2726_6_964",
        "label": "964 no-higher-derivative minimality",
        "path": ROOT / "964-Y5-R10-parent-no-higher-derivative-minimality-theorem-or-R2FR-nonclaim-runner.md",
        "needles": [
            "MIN964_5_verdict",
            "CM964_0_EH_plus_R2",
            "CM964_2_marker_prefactor",
            "DEC964_0_theorem_result",
        ],
        "use": "best no-higher-derivative/minimality shot failed and countermodels remain legal",
    },
    {
        "source_id": "SRC2726_7_443",
        "label": "443 Levi-Civita connection fork",
        "path": ROOT / "443-metric-compatibility-Levi-Civita-or-R11-connection-row.md",
        "needles": [
            "P4_target",
            "legal_success",
            "independent_connection_absence_gate",
            "Levi_Civita_parent_derived",
            "hypermomentum_absence_derived",
        ],
        "use": "Levi-Civita compatibility remains conditional; torsion/nonmetricity rows are retained",
    },
    {
        "source_id": "SRC2726_8_785",
        "label": "785 coframe/connection contract",
        "path": ROOT / "785-Y5-R10-psi-metric-coframe-connection-contract-or-bg-residual-lock.md",
        "needles": [
            "PMC785_4_connection_from_coframe",
            "CDS785_5_stack_verdict",
            "BGL785_2_connection_trigger",
            "V785_8_lc_connection_conditional",
        ],
        "use": "metric-to-coframe stack is available only conditionally and locks connection leakage residuals",
    },
    {
        "source_id": "SRC2726_9_784_csv",
        "label": "784 coframe connection requirements",
        "path": RESIDUALS / "P8_Y5_R10_784_COFRAME_CONNECTION_REQUIREMENTS.csv",
        "needles": [
            "CCR784_2_connection",
            "CCR784_4_matter_blindness",
            "CCR784_5_action_derivation",
        ],
        "use": "machine-readable requirements for coframe, connection, matter blindness and action ownership",
    },
]


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = Path(spec["path"])
        text = read_text(path)
        missing = [needle for needle in spec["needles"] if needle not in text]
        rows.append(
            {
                "source_id": spec["source_id"],
                "label": spec["label"],
                "path": str(path),
                "exists": path.exists(),
                "required_needles_found": not missing,
                "missing_needles": ";".join(missing),
                "use": spec["use"],
                "claim_credit": False,
                "timestamp_utc": ts(),
            }
        )
    return rows


def proof_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "NELC2726_0_fixed_spurion_exclusion",
            "target": "exclude fixed noncovariant labels from the parent operator",
            "attempt": "quotient/object-language logic rejects fixed active labels that are not fields, constants, gauge, or readout maps",
            "result": "PARTIAL_HELPFUL_NOT_ENOUGH",
            "why_not_claim": "covariant material markers and quotient-invariant local scalars survive the fixed-spurion exclusion",
            "residual_if_failed": "E_visible_coefficient_morphism",
            "claim_allowed": False,
        },
        {
            "audit_id": "NELC2726_1_local_invariant_triviality",
            "target": "prove I_loc(Q_MTS)=I_geom[J^k(e_obs)] plus universal constants",
            "attempt": "use 414/965/966 local invariant algebra route to eliminate all hidden generators",
            "result": "NOT_DERIVED",
            "why_not_claim": "finite fibre spectra, domain/class data, memory scalar, species constants and readout projector remain live",
            "residual_if_failed": "E_local_invariant_algebra",
            "claim_allowed": False,
        },
        {
            "audit_id": "NELC2726_2_no_extension_minimality",
            "target": "forbid curvature-coupled marker/scalar/nonlocal extensions",
            "attempt": "activate parent no-extension theorem strong enough to kill EH+R2, F(sigma)R and R Box^-1 R countermodels",
            "result": "NO_EXTENSION_NOT_PROVED",
            "why_not_claim": "964/965 leave marker-prefactor, integrated-out scalar and nonlocal memory countermodels legal",
            "residual_if_failed": "E_no_extension_minimality",
            "claim_allowed": False,
        },
        {
            "audit_id": "NELC2726_3_LC_descent",
            "target": "derive Gamma_obs=LC(g_obs) and universal matter/light/spin use of omega[e_obs]",
            "attempt": "use no-independent-connection or Palatini/zero-hypermomentum route",
            "result": "LC_DESCENT_NOT_PROVED",
            "why_not_claim": "443/785 keep independent connection, torsion, nonmetricity, spin and hypermomentum routes open",
            "residual_if_failed": "E_LC_descent",
            "claim_allowed": False,
        },
        {
            "audit_id": "NELC2726_4_verdict",
            "target": "kill all 2725 countermodels and promote EH operator",
            "attempt": "combine no-extension/minimality with LC descent",
            "result": "PARENT_KILL_SWITCHES_UNSIGNED_EH_ROUTE_RESIDUALIZED",
            "why_not_claim": "no-extension and LC descent are both conditional; EH remains a relative theorem, not a parent-owned MTS limit",
            "residual_if_failed": "explicit E_operator_core residual vector",
            "claim_allowed": False,
        },
    ]


def kill_switch_rows() -> list[dict[str, Any]]:
    return [
        {
            "switch_id": "KS2726_0_readout_after_variation",
            "kill_switch": "readout projector is a post-variation map only",
            "would_kill": "post-readout projector as reduced-action source or marker",
            "current_status": "SCHEMA_LOCK_CANDIDATE_NOT_PARENT_SIGNED",
            "source": str(ROOT / "966-Y5-R10-local-invariant-generator-elimination-or-R2FR-curve-digitizer.md"),
            "next_action": "prove R_read: Sol(S_parent)->Obs is not an argument of S_parent",
            "claim_allowed": False,
        },
        {
            "switch_id": "KS2726_1_species_universality",
            "kill_switch": "no source-only species prefactors or hidden coefficient slots",
            "would_kill": "species constants as WEP/source-charge/clock markers",
            "current_status": "CONDITIONAL_SUPERSELECTION_NOT_PARENT_SIGNED",
            "source": str(RESIDUALS / "P8_Y5_R10_574_GENERATOR_ELIMINATION_ATTEMPTS.csv"),
            "next_action": "derive universal Hilbert source functor with no kappa_A slots",
            "claim_allowed": False,
        },
        {
            "switch_id": "KS2726_2_domain_class_triviality",
            "kill_switch": "local relative boundary/domain class is trivial and exchange-free",
            "would_kill": "domain/class source marker and boundary/domain charge",
            "current_status": "CONDITIONAL_ZERO_CLASS_NOT_DERIVED",
            "source": str(ROOT / "966-Y5-R10-local-invariant-generator-elimination-or-R2FR-curve-digitizer.md"),
            "next_action": "derive topology/no-defect and zero boundary exchange in local branch",
            "claim_allowed": False,
        },
        {
            "switch_id": "KS2726_3_memory_positive_operator",
            "kill_switch": "memory/class scalar obeys positive source-free operator with zero local value and gradient",
            "would_kill": "memory scalar as clock/source/fifth-force/non-EH prefactor",
            "current_status": "LEMMA_SHAPE_WRITTEN_INPUTS_UNSIGNED",
            "source": str(ROOT / "966-Y5-R10-local-invariant-generator-elimination-or-R2FR-curve-digitizer.md"),
            "next_action": "prove parent L_X, source silence, boundary flux silence and local energy identity",
            "claim_allowed": False,
        },
        {
            "switch_id": "KS2726_4_fibre_gap_universality",
            "kill_switch": "finite-cell fibre spectrum integrates out to universal constants",
            "would_kill": "finite fibre spectrum as material/source marker",
            "current_status": "NOT_DERIVED",
            "source": str(RESIDUALS / "P8_Y5_R10_573_INVARIANT_GENERATOR_DEBT.csv"),
            "next_action": "derive source-independent unique/gapped fibre stationary point",
            "claim_allowed": False,
        },
        {
            "switch_id": "KS2726_5_LC_connection_descent",
            "kill_switch": "no independent connection or Palatini/zero-hypermomentum makes Gamma=LC(g_obs)",
            "would_kill": "torsion/nonmetricity/hypermomentum connection residuals",
            "current_status": "CONDITIONAL_ROUTE_KNOWN_PARENT_PROOF_MISSING",
            "source": str(ROOT / "443-metric-compatibility-Levi-Civita-or-R11-connection-row.md"),
            "next_action": "write explicit parent connection variation or no-independent-connection clause",
            "claim_allowed": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "countermodel_id": "CM2726_0_marker_prefactor",
            "form": "S = integral sqrt(-g) F(sigma(Q)) R",
            "survives_because": "quotient-invariant scalar sigma(Q) remains live without local invariant algebra triviality",
            "blocked_claim": "metric-only EH operator and constant coupling",
            "required_kill_switch": "KS2726_1 or KS2726_3 or full I_loc triviality",
            "currently_killed": False,
        },
        {
            "countermodel_id": "CM2726_1_integrated_out_scalar",
            "form": "S = S_EH + beta phi R - M^2 phi^2/2, then phi is eliminated",
            "survives_because": "variation-first no-reentry theorem is not signed",
            "blocked_claim": "second-order minimality and R2/fR zero",
            "required_kill_switch": "KS2726_3 or KS2726_4 plus no-reentry proof",
            "currently_killed": False,
        },
        {
            "countermodel_id": "CM2726_2_readout_reduced_action",
            "form": "post-readout projector is inserted into a reduced action and varied",
            "survives_because": "readout-after-variation is a no-cheat rule but not a full parent-domain theorem",
            "blocked_claim": "no-extension/minimality and source/operator purity",
            "required_kill_switch": "KS2726_0",
            "currently_killed": False,
        },
        {
            "countermodel_id": "CM2726_3_domain_selector_stress",
            "form": "chi_D/domain selector contributes stress, preferred-frame source or local class marker",
            "survives_because": "domain selector, topology/no-defect and boundary exchange are not parent-derived",
            "blocked_claim": "metric-only and boundary-harmless EH operator",
            "required_kill_switch": "KS2726_2",
            "currently_killed": False,
        },
        {
            "countermodel_id": "CM2726_4_metric_affine_connection",
            "form": "independent Gamma with torsion T, nonmetricity Q, projective mode or hypermomentum",
            "survives_because": "connection variation and no-Gamma matter theorem are not supplied",
            "blocked_claim": "Levi-Civita descent and universal matter connection",
            "required_kill_switch": "KS2726_5",
            "currently_killed": False,
        },
    ]


def residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NER2726_0_E_visible_coefficient_morphism",
            "quantity": "E_visible_coefficient_morphism",
            "definition": "residual from hidden/local invariant scalars feeding visible coefficients such as F(sigma)R or kappa_A(I_hid)",
            "feeds": "E_no_extension_minimality;E_operator_core;source universality",
            "source_path": str(ROOT / "1114-Y5-R10-no-hidden-visible-coefficient-morphism-theorem-or-finite-coupling-inputs.md"),
            "units_need": "dimensionless coefficient drift or declared coupling units",
            "missing": "typed parent object-language theorem or local invariant algebra triviality",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "NER2726_1_E_local_invariant_algebra",
            "quantity": "E_local_invariant_algebra",
            "definition": "binary/norm residual for I_loc(Q_MTS) not reducing to observed geometry jets plus universal constants",
            "feeds": "E_no_extension_minimality;E_nonmetric_extra_field",
            "source_path": str(ROOT / "414-local-quotient-invariant-algebra-triviality-gate.md"),
            "units_need": "zero theorem or count/weight of surviving generators",
            "missing": "elimination of finite fibre, domain/class, chi_D, memory, species and readout generators",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "NER2726_2_E_readout_reentry",
            "quantity": "E_readout_reentry",
            "definition": "residual if post-readout projectors are inserted into a reduced action and varied as parent sources",
            "feeds": "E_auxiliary_reentry;E_no_extension_minimality;source/readout gates",
            "source_path": str(RESIDUALS / "P8_Y5_R10_574_GENERATOR_ELIMINATION_ATTEMPTS.csv"),
            "units_need": "dimensionless reduced-action source leakage",
            "missing": "readout-after-variation theorem as parent-domain statement",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "NER2726_3_E_species_slot",
            "quantity": "E_species_slot",
            "definition": "residual from species/source constants acting as independent active gravitational coefficient slots",
            "feeds": "source universality;WEP;E_no_extension_minimality",
            "source_path": str(RESIDUALS / "P8_Y5_R10_573_INVARIANT_GENERATOR_DEBT.csv"),
            "units_need": "relative source coupling or WEP-normalized coefficient",
            "missing": "parent-signed species universality and no kappa_A source slot",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "NER2726_4_E_domain_marker",
            "quantity": "E_domain_marker",
            "definition": "residual from chi_D/domain selector or relative boundary class appearing as local source/operator marker",
            "feeds": "E_nonmetric_extra_field;E_boundary_topological;PPN preferred-frame rows",
            "source_path": str(ROOT / "966-Y5-R10-local-invariant-generator-elimination-or-R2FR-curve-digitizer.md"),
            "units_need": "domain stress/source-normalization coefficient or zero theorem",
            "missing": "parent-selected domain, topology/no-defect and boundary exchange no-hair",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "NER2726_5_E_memory_scalar_generator",
            "quantity": "E_memory_scalar_generator",
            "definition": "residual from memory/class scalar with nonzero local value, gradient, source or boundary flux",
            "feeds": "E_no_extension_minimality;E_nonlocal_memory;R9/R10/clock",
            "source_path": str(ROOT / "966-Y5-R10-local-invariant-generator-elimination-or-R2FR-curve-digitizer.md"),
            "units_need": "scalar value/gradient/source norm and coupling normalization",
            "missing": "positive source-free operator identity plus boundary flux silence",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "NER2726_6_E_fibre_spectrum_marker",
            "quantity": "E_fibre_spectrum_marker",
            "definition": "residual from finite-cell fibre spectrum or trace acting as a local material/source marker",
            "feeds": "E_no_extension_minimality;source/WEP/fifth-force rows",
            "source_path": str(RESIDUALS / "P8_Y5_R10_573_INVARIANT_GENERATOR_DEBT.csv"),
            "units_need": "dimensionless spectrum variation or gap-normalized coefficient",
            "missing": "unique source-independent gapped fibre stationary theorem",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "NER2726_7_E_LC_parent_descent",
            "quantity": "E_LC_parent_descent",
            "definition": "residual from missing proof that Gamma/omega is not independent or that connection variation forces Gamma=LC(g_obs)",
            "feeds": "E_connection_LC;E_connection_metric_affine",
            "source_path": str(ROOT / "443-metric-compatibility-Levi-Civita-or-R11-connection-row.md"),
            "units_need": "zero theorem or connection residual norm",
            "missing": "no-independent-connection or Palatini/metric-affine zero equation",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "NER2726_8_E_projective_trace",
            "quantity": "E_projective_trace",
            "definition": "residual from projective torsion trace or connection trace mode if not gauge-only for all sectors",
            "feeds": "E_connection_metric_affine;source/WEP rows",
            "source_path": str(ROOT / "443-metric-compatibility-Levi-Civita-or-R11-connection-row.md"),
            "units_need": "projective mode coefficient or invariance proof",
            "missing": "all-sector projective invariance or trace-fixing theorem",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "NER2726_9_E_torsion_spin",
            "quantity": "E_torsion_spin",
            "definition": "residual from axial/tensor torsion sourced by spin or first-order coframe connection couplings",
            "feeds": "E_connection_metric_affine;spin/clocks/WEP",
            "source_path": str(ROOT / "443-metric-compatibility-Levi-Civita-or-R11-connection-row.md"),
            "units_need": "torsion coefficient and spin-source normalization",
            "missing": "spinor matter torsion exclusion or algebraic torsion bound",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "NER2726_10_E_nonmetricity_clock",
            "quantity": "E_nonmetricity_clock",
            "definition": "residual from Weyl/shear nonmetricity changing rods, clocks or light cones",
            "feeds": "E_connection_metric_affine;clock/light/WEP/PPN",
            "source_path": str(ROOT / "443-metric-compatibility-Levi-Civita-or-R11-connection-row.md"),
            "units_need": "nonmetricity trace/shear norm and clock/light projection",
            "missing": "metric-affine zero-Q theorem or finite nonmetricity bounds",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "NER2726_11_E_hypermomentum_source",
            "quantity": "E_hypermomentum_source",
            "definition": "residual from matter, light, spin, source or readout sectors coupling directly to independent connection",
            "feeds": "E_hypermomentum_connection;source normalization;WEP",
            "source_path": str(ROOT / "785-Y5-R10-psi-metric-coframe-connection-contract-or-bg-residual-lock.md"),
            "units_need": "hypermomentum/source-connection coupling norm",
            "missing": "matter-blindness theorem: S_matter uses only e_obs and omega[e_obs]",
            "status": "SOURCE_READY_SCHEMA_NONCLAIM",
            "valid_for_claim": False,
        },
    ]


def lc_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "LC2726_0_metric_formalism",
            "route": "Gamma is not an independent parent variable; omega=omega[e_obs] by construction",
            "would_close": "LC descent kinematically",
            "current_status": "CONDITIONAL_NOT_PARENT_DERIVED",
            "missing": "parent action signature excluding independent connection variables and direct matter connection slots",
            "claim_allowed": False,
        },
        {
            "route_id": "LC2726_1_Palatini_EH",
            "route": "Palatini EH connection variation plus matter independent of Gamma gives LC up to projective gauge",
            "would_close": "LC after EH operator and no hypermomentum",
            "current_status": "BLOCKED_BY_OPEN_EH_AND_MATTER_PREMISES",
            "missing": "EH operator ownership and no-hypermomentum matter/source theorem",
            "claim_allowed": False,
        },
        {
            "route_id": "LC2726_2_first_order_coframe",
            "route": "first-order coframe/spin-connection equation enforces zero torsion",
            "would_close": "torsion part if spin/source terms vanish or are mapped",
            "current_status": "CONDITIONAL_WITH_SPIN_ESCAPE",
            "missing": "ordinary spinor matter/source torsion handling",
            "claim_allowed": False,
        },
        {
            "route_id": "LC2726_3_metric_affine_zero",
            "route": "metric-affine equations algebraically force T=0 and Q=0",
            "would_close": "full torsion/nonmetricity descent",
            "current_status": "NOT_SUPPLIED",
            "missing": "explicit parent connection Euler equation and zero-source algebra",
            "claim_allowed": False,
        },
        {
            "route_id": "LC2726_4_projective_only",
            "route": "only projective trace remains and all sectors are projectively invariant",
            "would_close": "projective residue only",
            "current_status": "INSUFFICIENT_FOR_FULL_LC",
            "missing": "proof no axial/tensor torsion, shear/Weyl nonmetricity or hypermomentum remains",
            "claim_allowed": False,
        },
    ]


def ejeff_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "update_id": "EJ2726_0_no_extension_minimality",
            "formula": "E_no_extension_minimality := E_visible_coefficient_morphism + E_local_invariant_algebra + E_readout_reentry + E_species_slot + E_domain_marker + E_memory_scalar_generator + E_fibre_spectrum_marker",
            "status": "FORMAL_VECTOR_NONCLAIM",
            "claim_allowed": False,
        },
        {
            "update_id": "EJ2726_1_LC_descent",
            "formula": "E_LC_descent := E_LC_parent_descent + E_projective_trace + E_torsion_spin + E_nonmetricity_clock + E_hypermomentum_source",
            "status": "FORMAL_VECTOR_NONCLAIM",
            "claim_allowed": False,
        },
        {
            "update_id": "EJ2726_2_operator_core",
            "formula": "E_operator_core keeps 2725 form with E_no_extension_minimality and E_LC_descent as active sub-vectors until theorem-zero or bounds are sourced",
            "status": "DEPENDENCY_LEDGER_NONCLAIM",
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE2726_0_no_extension",
            "claim": "parent forbids curvature-coupled marker/scalar/nonlocal extensions",
            "status": "BLOCKED",
            "required_before_claim": "local invariant algebra triviality or typed parent object-language theorem",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2726_1_LC_descent",
            "claim": "Gamma_obs=LC(g_obs) and matter/light/spin universally use omega[e_obs]",
            "status": "BLOCKED",
            "required_before_claim": "no-independent-connection or Palatini/zero-hypermomentum proof",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2726_2_EH_operator",
            "claim": "EH left-hand operator is parent-owned",
            "status": "BLOCKED",
            "required_before_claim": "no-extension plus metric-only second-order LC and boundary-harmless gates",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2726_3_local_GR_Newton",
            "claim": "local GR/Newton reduction follows",
            "status": "BLOCKED",
            "required_before_claim": "EH/R11 operator gate plus source/coupling/readout/PPN gates",
            "claim_allowed": False,
        },
    ]


def blocker_stack_rows() -> list[dict[str, Any]]:
    return [
        {
            "blocker_id": "BLK2726_0_readout_projector",
            "missing_item": "readout-after-variation theorem as parent-domain statement",
            "effect": "readout projector remains a possible reduced-action generator",
            "best_next_attack": "prove R_read is external to S_parent and cannot source Euler equations",
            "claim_blocked": True,
        },
        {
            "blocker_id": "BLK2726_1_local_invariant_algebra",
            "missing_item": "I_loc(Q_MTS)=I_geom plus constants",
            "effect": "hidden scalar/marker countermodels can feed curvature or visible coefficients",
            "best_next_attack": "kill generators in the 966 priority order",
            "claim_blocked": True,
        },
        {
            "blocker_id": "BLK2726_2_connection",
            "missing_item": "parent connection variation or no-independent-connection clause",
            "effect": "torsion/nonmetricity/hypermomentum can alter local tests",
            "best_next_attack": "after readout generator, write exact connection variation contract",
            "claim_blocked": True,
        },
        {
            "blocker_id": "BLK2726_3_residual_coefficients",
            "missing_item": "numeric/source-backed R11 operator coefficients if theorem route fails",
            "effect": "local/R10/PPN branches cannot be scored",
            "best_next_attack": "only source coefficients after derivation route is exhausted for each generator",
            "claim_blocked": True,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2726_0_result",
            "decision": "No-extension/minimality and LC descent are not proved.",
            "rationale": "local invariant generator and connection countermodels remain legal in current corpus",
            "allowed": True,
            "claim_credit": False,
        },
        {
            "decision_id": "DEC2726_1_EH_status",
            "decision": "EH operator route is demoted to conditional/residualized status until kill switches close.",
            "rationale": "Lovelock cannot be activated while no-extension and LC premises remain unsigned",
            "allowed": True,
            "claim_credit": False,
        },
        {
            "decision_id": "DEC2726_2_next",
            "decision": "Attack readout-after-variation first.",
            "rationale": "966 ranks readout projector as the most promising generator to genuinely remove from I_loc(Q_MTS)",
            "allowed": True,
            "claim_credit": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2726_0_selected",
            "status": "selected_primary",
            "target_doc": "2727-Y5-R2FR-readout-after-variation-no-reduced-action-backreaction-or-generator-row-under-AX1090-closure.md",
            "target_script": "scripts/Y5_R2FR_readout_after_variation_no_reduced_action_backreaction_or_generator_row_under_AX1090_closure_2727.py",
            "mission": "prove readout/projector is a map on solution space only and cannot re-enter the parent action as a variational source; if not, keep E_readout_reentry explicit",
            "acceptance": "R_read notin Args(S_parent), no delta S/delta P_read equation, no reduced-action backreaction, no source/coupling absorption; or a retained nonclaim generator row",
            "forbidden": "hide readout in a closure axiom; infer from empirical success; edit formalization-workbench; GitHub action",
            "selected": True,
            "claim_allowed": False,
        }
    ]


def project_snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "snapshot_id": "SNAP2726_0_GR_route",
            "sector": "GR/Newton derivability",
            "state": "EH relative theorem is intact but kill switches unsigned",
            "confidence": "high that current nonclaim status is correct",
            "next_need": "generator elimination beginning with readout-after-variation",
        },
        {
            "snapshot_id": "SNAP2726_1_no_extension",
            "sector": "parent minimality",
            "state": "local invariant algebra triviality not derived",
            "confidence": "medium route viability, high blocker clarity",
            "next_need": "remove one generator at a time",
        },
        {
            "snapshot_id": "SNAP2726_2_LC",
            "sector": "Levi-Civita connection",
            "state": "conditional routes known, no parent proof",
            "confidence": "high blocker clarity",
            "next_need": "connection variation contract after readout generator",
        },
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": "COPY2726_0_local_bounds",
            "source_table": str(OUTPUTS["residual_rows"]),
            "copy_path": str(BRANCH_OUTPUTS["local_bounds"]),
            "purpose": "local/R10/PPN branches can ingest no-extension and LC residual rows without claim credit",
            "exists": BRANCH_OUTPUTS["local_bounds"].exists(),
            "valid_for_claim": False,
        },
        {
            "copy_id": "COPY2726_1_source_weight",
            "source_table": str(OUTPUTS["ejeff_update"]),
            "copy_path": str(BRANCH_OUTPUTS["source_weight"]),
            "purpose": "source-weight branch receives no-extension and LC sub-vector expansion",
            "exists": BRANCH_OUTPUTS["source_weight"].exists(),
            "valid_for_claim": False,
        },
        {
            "copy_id": "COPY2726_2_next_queue",
            "source_table": str(OUTPUTS["next_target"]),
            "copy_path": str(BRANCH_OUTPUTS["next_queue"]),
            "purpose": "queues readout-after-variation generator kill target",
            "exists": BRANCH_OUTPUTS["next_queue"].exists(),
            "valid_for_claim": False,
        },
    ]


def parse_csv(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        if not rows:
            return False, 0, "empty"
        return True, len(rows), "ok"
    except Exception as exc:
        return False, 0, repr(exc)


def recent_formalization_changes() -> int:
    if not FORMALIZATION.exists():
        return 0
    start = SCRIPT_START_UTC.timestamp()
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and path.stat().st_mtime >= start:
            count += 1
    return count


def validation_rows(
    source_rows: list[dict[str, Any]],
    proof_rows: list[dict[str, Any]],
    kill_rows: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    lc_routes: list[dict[str, Any]],
    ejeff: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    required_quantities = {
        "E_visible_coefficient_morphism",
        "E_local_invariant_algebra",
        "E_readout_reentry",
        "E_species_slot",
        "E_domain_marker",
        "E_memory_scalar_generator",
        "E_fibre_spectrum_marker",
        "E_LC_parent_descent",
        "E_projective_trace",
        "E_torsion_spin",
        "E_nonmetricity_clock",
        "E_hypermomentum_source",
    }
    csv_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    parse_results = [(*parse_csv(path), path) for path in csv_paths]
    parse_detail = "; ".join(
        f"{path.name}:{row_count}:{detail}" if passed else f"{path.name}:{detail}"
        for passed, row_count, detail, path in parse_results
    )
    branch_paths_ok = all(path.exists() for path in BRANCH_OUTPUTS.values())
    formalization_recent_changed_count = recent_formalization_changes()
    source_ok = all(row["exists"] is True and row["required_needles_found"] is True for row in source_rows)
    proof_nonclaim = all(row["claim_allowed"] is False for row in proof_rows)
    kill_nonclaim = all(row["claim_allowed"] is False for row in kill_rows)
    countermodels_live = all(row["currently_killed"] is False for row in countermodels)
    residual_nonclaim = (
        {row["quantity"] for row in residuals} == required_quantities
        and all(row["valid_for_claim"] is False for row in residuals)
    )
    lc_nonclaim = all(row["claim_allowed"] is False for row in lc_routes)
    ejeff_nonclaim = all(row["claim_allowed"] is False for row in ejeff)
    gates_false = all(row["claim_allowed"] is False for row in gates)
    no_github_outputs = all("github" not in str(path).lower() for path in csv_paths + [DOC])
    rows = [
        {
            "validation_id": "VAL2726_0_sources",
            "passed": source_ok,
            "detail": "all source paths exist and required needles found",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2726_1_doc_written",
            "passed": DOC.exists(),
            "detail": str(DOC),
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2726_2_csv_parse",
            "passed": all(result[0] for result in parse_results),
            "detail": parse_detail,
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2726_3_proof_audit_nonclaim",
            "passed": proof_nonclaim,
            "detail": "no-extension and LC proof audit stays nonclaim",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2726_4_kill_switches_nonclaim",
            "passed": kill_nonclaim,
            "detail": "all kill switches are targets, not claims",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2726_5_countermodels_live",
            "passed": countermodels_live,
            "detail": "surviving countermodels remain live until explicit parent kill switches close",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2726_6_residual_rows_complete_nonclaim",
            "passed": residual_nonclaim,
            "detail": "no-extension and LC residual rows are complete and valid_for_claim=false",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2726_7_lc_routes_nonclaim",
            "passed": lc_nonclaim,
            "detail": "LC descent routes are conditional only",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2726_8_ejeff_update_nonclaim",
            "passed": ejeff_nonclaim,
            "detail": "E_no_extension_minimality and E_LC_descent vectors remain formal/nonclaim",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2726_9_claim_gates_all_false",
            "passed": gates_false,
            "detail": "no no-extension, LC, EH, Newton, PPN or local-GR gate opened",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2726_10_branch_copies",
            "passed": branch_paths_ok,
            "detail": "branch copies exist and remain nonclaim",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2726_11_no_formalization_recent_changes",
            "passed": formalization_recent_changed_count == 0,
            "detail": f"formalization_recent_changed_count={formalization_recent_changed_count}",
            "timestamp_utc": ts(),
        },
        {
            "validation_id": "VAL2726_12_no_github_outputs",
            "passed": no_github_outputs,
            "detail": "no GitHub/public-output path was written",
            "timestamp_utc": ts(),
        },
    ]
    overall = all(row["passed"] is True for row in rows)
    rows.append(
        {
            "validation_id": "VAL2726_OVERALL",
            "passed": overall,
            "detail": "2726 refuses no-extension/LC promotion, residualizes EH operator route, and selects readout-after-variation generator kill next",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2726 - Y5/R2FR Parent No-Extension Minimality And LC Descent Or Eoperator Bound Under AX1090 Closure

## Private Verdict

2726 attacks the two kill-switches that would let the EH operator become a parent-owned MTS result:

1. **No-extension/minimality:** the parent admits no natural curvature-coupled marker, scalar, nonlocal memory, hidden coefficient morphism, readout re-entry, species slot, or fibre/domain generator.
2. **Levi-Civita descent:** the observed connection is forced to be `LC(g_obs)`, and matter/light/spin/source sectors use only `e_obs` and `omega[e_obs]`.

Both routes are mathematically clear. Neither closes in the current corpus.

This does not kill the GR route. It does stop any premature EH claim. The EH branch is now explicitly **conditional/residualized**: it can be promoted only if these kill-switches close, or it must carry the listed residual vectors into local/R10/PPN testing.

The next best move is not another broad EH pass. It is the highest-probability generator kill: **readout-after-variation**. If readout is proved to be a map on solution space only, one live generator genuinely drops out of `I_loc(Q_MTS)`.

## Claim Ceiling

- No no-extension, local invariant algebra triviality, Levi-Civita, EH, Newton, local-GR, PPN, R10, clock, WEP, orbital, or public claim is opened.
- The EH route is retained as a relative theorem, but demoted to explicit residual/closure-only until kill-switches close.
- All new residual rows are `valid_for_claim=false`.
- No `formalization-workbench` edits, GitHub action, or public-output path is allowed from this checkpoint.

## Source Register

{markdown_table(rows["source_register"], ["source_id", "label", "path", "exists", "required_needles_found", "missing_needles", "use", "claim_credit"])}

## No-Extension / LC Proof Audit

{markdown_table(rows["proof_audit"], ["audit_id", "target", "attempt", "result", "why_not_claim", "residual_if_failed", "claim_allowed"])}

## Parent Kill-Switch Ledger

{markdown_table(rows["kill_switches"], ["switch_id", "kill_switch", "would_kill", "current_status", "source", "next_action", "claim_allowed"])}

## Surviving Countermodels

{markdown_table(rows["countermodels"], ["countermodel_id", "form", "survives_because", "blocked_claim", "required_kill_switch", "currently_killed"])}

## Residual Rows

{markdown_table(rows["residual_rows"], ["row_id", "quantity", "definition", "feeds", "source_path", "units_need", "missing", "status", "valid_for_claim"])}

## Levi-Civita Descent Route Audit

{markdown_table(rows["lc_routes"], ["route_id", "route", "would_close", "current_status", "missing", "claim_allowed"])}

## E_Jeff Update

{markdown_table(rows["ejeff_update"], ["update_id", "formula", "status", "claim_allowed"])}

## Claim Gates

{markdown_table(rows["claim_gates"], ["gate_id", "claim", "status", "required_before_claim", "claim_allowed"])}

## Current Blocker Stack

{markdown_table(rows["blocker_stack"], ["blocker_id", "missing_item", "effect", "best_next_attack", "claim_blocked"])}

## Decision Ledger

{markdown_table(rows["decision_ledger"], ["decision_id", "decision", "rationale", "allowed", "claim_credit"])}

## Next Target

{markdown_table(rows["next_target"], ["next_id", "status", "target_doc", "target_script", "mission", "acceptance", "forbidden", "selected", "claim_allowed"])}

## Project Status Snapshot

{markdown_table(rows["project_snapshot"], ["snapshot_id", "sector", "state", "confidence", "next_need"])}

## Branch Copies

{markdown_table(rows["branch_copies"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(rows["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}

## Plain-English Read

This checkpoint is annoying in the good way. The door to GR is still there, but the lock is no-extension plus Levi-Civita. Right now the parent does not yet forbid hidden local generators strongly enough, and it does not yet own the connection strongly enough. So the right next punch is surgical: remove the readout projector from the parent action entirely, if possible. That would be one generator down, not just another lap around the same boss arena.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    proof = proof_audit_rows()
    kill = kill_switch_rows()
    countermodels = countermodel_rows()
    residuals = residual_rows()
    lc_routes = lc_route_rows()
    ejeff = ejeff_update_rows()
    gates = claim_gate_rows()
    blockers = blocker_stack_rows()
    decisions = decision_ledger_rows()
    next_rows = next_target_rows()
    snapshot = project_snapshot_rows()

    data: dict[str, list[dict[str, Any]]] = {
        "source_register": source_rows,
        "proof_audit": proof,
        "kill_switches": kill,
        "countermodels": countermodels,
        "residual_rows": residuals,
        "lc_routes": lc_routes,
        "ejeff_update": ejeff,
        "claim_gates": gates,
        "blocker_stack": blockers,
        "decision_ledger": decisions,
        "next_target": next_rows,
        "project_snapshot": snapshot,
    }

    for key, table_rows in data.items():
        write_csv(OUTPUTS[key], table_rows)

    write_csv(BRANCH_OUTPUTS["local_bounds"], residuals)
    write_csv(BRANCH_OUTPUTS["source_weight"], ejeff)
    write_csv(BRANCH_OUTPUTS["next_queue"], next_rows)

    copies = branch_copy_rows()
    data["branch_copies"] = copies
    write_csv(OUTPUTS["branch_copies"], copies)

    data["validation"] = [
        {
            "validation_id": "VAL2726_PRE_DOC",
            "passed": False,
            "detail": "pre-document placeholder",
            "timestamp_utc": ts(),
        }
    ]
    write_doc(data)

    validation = validation_rows(source_rows, proof, kill, countermodels, residuals, lc_routes, ejeff, gates)
    data["validation"] = validation
    write_csv(OUTPUTS["validation"], validation)
    write_doc(data)

    if not all(row["passed"] is True for row in validation):
        failed = [row for row in validation if row["passed"] is not True]
        raise SystemExit(f"2726 validation failed: {failed}")

    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
