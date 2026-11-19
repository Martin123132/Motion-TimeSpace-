# Independent coordinate-difference step separated from the live RHS

The original heavy run stops at preflight: its smaller independent WD directional-difference check gives5.32965e-5 against the unchanged2e-5 gate. It does NOT run a failed heavy evolution or claim a pass. Native owner release and exact worker exit are recorded. The original files and false check remain unchanged.

The local physical metric derivative itself passes at both original steps and agrees between them to1.04e-8. The source-map inverse and exact product/tail identity pass. Before retrying any evolution, a separate diagnostic scans independent coordinate-difference steps span/256,512,1024,2048,4096,8192 over the same65 states. This diagnostic does not alter the physical RHS.

Heavy WD check discrepancies are2.2542e-4,1.1600e-5,2.0000e-6,7.6566e-6,8.1226e-6,5.3297e-5 respectively. The large step truncates; making the step very small is not monotone refinement and amplifies the numerical evaluation/subtraction noise. This scan is evidence for a usable numerical step interval, not a new physical parameter or proof of which individual native floating operation dominates the noise.

The adjustment freezes TWO intermediate independent check steps span/1024 and span/2048 and checks the baseline at those too. The physical metric stencils remain span/4096 and span/8192; physical evolution, initial values, integration steps, equations, background, bank and both gates are unchanged. The baseline's completed evolution is reused, not counted as another independent calculation. New heavy outputs have a distinct balanced-check label.

The first diagnostic adapter invocation failed before starting a scientific worker because it looked for a dictionary literal where the driver uses dict keyword arguments. That adapter selector was corrected; no native calculation or saved physics changed. The later cold diagnostic selects its actual CDM coordinate rather than nonexistent heavy coordinates.
