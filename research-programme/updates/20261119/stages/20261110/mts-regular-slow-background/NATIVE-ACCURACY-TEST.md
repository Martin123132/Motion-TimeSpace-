# Frozen native accuracy discrimination

The native-slope Hermite test does not reduce the candidate discrepancy.
The reported metric derivatives satisfy their algebraic identities at nodes,
but this alone does not show that the sampled metric history follows those
derivatives. Preserve both unsuccessful candidate comparisons.

Before changing any background or perturbation equation, rerun the identical
candidate tables, four-species/background settings, k=1 and saved4253 scales
at IntTolBoost12 and24, compared with the saved6. All other parameter settings,
physical inputs, output precision and acceptance gates are frozen. Run both
cold and heavy, one worker at a time. Higher IntTolBoost tightens native
integration; it does not loosen the independent componentwise2e-5 test.

Use a narrowly checked AST copy of the saved runner, altering only the
output label and IntTolBoost value. Hash both scripts and this protocol.
Save every attempt separately. Repeat the identical independent canonical
replay and compare whether residuals shrink; do not presume success.
