# Final-panel continuation, not a new physical model

FROZEN_STAGE remains the original mts-full-cell-flow-integration-20261109. INHERITED_BATCH_STAGES includes both that stage and mts-full-cell-flow-continuation-20261109, whose closeout hash is3768ecafded183a8f0917892b67cefb59470ed2efef53d3d50d4874a874bd9d7.

The same source evaluation is imported unchanged. continuation_audit.py and all_source_projection.py are content-equivalent to the sealed previous stage; no physics or quadrature formula changes. common.py adapts ownership, cutoff, additional parent seal/hold and probe96. The campaign starts12and ends at most19. Both catalogues remain mandatory.

The previous stage's import-only failure is not repeated: every entry point imports common before inherited helpers. All attempts in this fresh stage must exit0to seal. No automatic failed-run retry.

Prior98segments/1730nodes are reused. The last60segments/1020nodes use the original frozen quadrature; selected105and157are already available and must not be recalculated. Both controls and all1e-10/2e-5thresholds remain unchanged.

