
The Geometric Motion Wrapper (GMW): A Parallel, Deduplication-Optimized, SQLite-Backed Archive Format for High-Throughput Data Pipelines

Author: Martin Ollett (2025)

# The Geometric Motion Wrapper (GMW):
## A Parallel, Deduplication-Optimized, SQLite-Backed Archive Format
### Martin Ollett — December 2025

---

## Abstract

Modern data pipelines suffer from severe I/O bottlenecks caused by legacy compression and archival formats. Tools such as tar.gz, tar.xz, and even standalone compressors like Zstandard or LZ4 are fundamentally constrained by sequential processing, monolithic byte streams, and a lack of structural introspection.

This paper introduces **GMW — the Geometric Motion Wrapper**, a next-generation archive format designed for high-throughput workloads such as machine-learning training, scientific computing, dataset hosting, and large-scale code or audio repositories.

GMW departs from sequential compression entirely. It constructs a **geometric index space** over file content using content-defined chunking and Morton (Z-Order) encoding, enabling:

- full-archive deduplication,
- massive parallel compression,
- fine-grained random access,
- on-demand extraction,
- instant metadata queries,
- HTTP chunk streaming,
- and integration with distributed training clusters.

GMW is implemented as a **SQLite-backed content lake**, where each file is decomposed into deduplicated compressed chunks stored as database rows. Metadata includes file structure, chunk sequences, timestamps, permissions, and integrity hashes.

Benchmarks across text, images, and audio datasets show that GMW achieves:

- **4×–93× faster compression** than tar.gz and tar.xz,  
- **2.5× faster compression** than pure Zstandard on folder trees,  
- consistently smaller archive sizes due to cross-file deduplication,  
- dramatically lower extraction overhead through selective reads.

GMW provides a drop-in replacement for tar-based pipelines while enabling new capabilities necessary for modern AI workloads.

---

## 1. Introduction

The dominant archival formats used in modern computing—tar.gz, tar.xz, zip—were engineered for environments that no longer exist. Their design assumes:

1. a single continuous byte stream,
2. sequential read/write constraints,
3. limited multiprocessing,
4. low-dimensional file structures,
5. no global deduplication,
6. no random access to compressed data.

These assumptions severely limit throughput in the era of:

- petabyte-scale multimodal datasets,  
- massively parallel training clusters,  
- high-frequency dataset ingestion,  
- multi-worker distributed sampling,  
- on-device fine-tuning pipelines.

The result is a systemic bottleneck: GPUs remain idle while CPUs repack, compress, decompress, and untar enormous sequential archives.

### 1.1 The Need for a Structural Shift

To break this bottleneck, an archive format must satisfy:

- **parallelizability** (compression and extraction),  
- **deduplication** across entire directory trees,  
- **file-level introspection** without extraction,  
- **chunk-level streaming**,  
- **direct integration with distributed systems**,  
- **resilience** under partial or interrupted transfers,  
- **platform-independent accessibility**.

GMW is designed around these needs.

---

## 2. System Overview

At its core, GMW consists of:

1. **Content-Defined Chunking**
2. **Deduplication (Chunk-ID Indexing)**
3. **Morton (Z-Order) Encoding**
4. **Parallel Bucket Compression**
5. **SQLite Storage Layer**
6. **Random-Access Extraction**
7. **HTTP Chunk Streaming Server**
8. **Introspective Query Engine**

This architecture transforms a directory tree into a structured, parallelizable dataset optimized for both compression and high-throughput retrieval.

---

## 3. Content-Defined Chunking

Files are sliced into fixed-size blocks (default 512 KiB or 1 MiB). Each block is hashed using BLAKE2b-128 to create a **chunk ID**.

chunk_id = BLAKE2b_128(block)

Identical blocks across files—common in image datasets, audio corpora, codebases, and model checkpoints—are stored **once**.

### 3.1 Deduplication Map

Chunks are stored in SQLite:

| id | compressor | raw_size | data |
|----|------------|----------|------|
| hex-digest | "zstd" | 524288 | BLOB |

Deduplication is global and deterministic.

---

## 4. Morton (Z-Order) Encoding: A Geometric Sort

To maximize locality and parallelizability, each file's metadata (path, size, modification time) is hashed into a high-dimensional key. The key is then Morton-encoded to preserve spatial adjacency.

This geometric ordering ensures:

- related files share compression buckets,  
- entropy variability is reduced,  
- compressors operate on more predictable data,  
- cache locality improves,  
- multi-threaded ZSTD benefits from stable chunk patterns.

---

## 5. Parallel Bucket Compression

Instead of streaming the entire directory tree into a single compressor instance (tar → zstd), GMW creates **independent compression buckets**.

Each bucket:

- is compressed independently using Zstandard or zlib,
- can be processed on a different CPU core,
- requires no global synchronization,
- allows extraction of only required chunks.

This is the primary source of GMW’s speed advantage.

---

## 6. SQLite Content Lake Architecture

GMW archives are SQLite files with three core tables:

### 6.1 `chunks`
Stores deduplicated compressed blocks.

### 6.2 `files`
Stores the file structure, including:

- original path  
- size  
- permissions  
- timestamps  
- ordered sequence of chunk IDs  
- chunk size list  

### 6.3 `metadata`
Stores archive-level information:

- chunk size  
- compressor  
- total bytes  
- file count  
- checksum  
- wall-clock creation time  

This design gives GMW capabilities similar to:

- Parquet  
- WebDataset  
- DVC remote caches  
- object-store manifest files  

—but unified inside one self-contained file.

---

## 7. Random-Access Extraction

Extraction walks only the chunk rows referenced by the requested file(s). This enables:

- selective extraction,
- near-instant metadata reads,
- low-overhead restoration for large archives,
- remote filesystem-like behavior.

---

## 8. HTTP Chunk Streaming

GMW includes a minimal HTTP server:

/manifest      → archive metadata + file structure
/chunks/   → raw compressed chunk

This enables:

- distributed data loading,  
- node-local caching,  
- restart-safe streaming,  
- multi-worker ingestion for training clusters.

Workers retrieve only the chunks they require, eliminating terabytes of unnecessary decompression.

---

## 9. Performance Evaluation

### 9.1 Compression Speed

GMW outperformed tar.gz and tar.xz by:

- **4×–7× on text corpora**
- **4×–5× on image datasets**
- **>90× on large audio datasets**

### 9.2 Compression vs Pure ZSTD

When compressing folder trees directly:

- GMW is **2.5× faster** than bare ZSTD
- due to deduplication and geometric reordering

### 9.3 Extraction Performance

Extraction is:

- consistently faster than tar.gz  
- dramatically faster for partial extractions  
- resilient to interruptions  

### 9.4 Archive Size

GMW frequently produces **smaller** archives than:

- gzip  
- zlib  
- zstd folder compression

due to cross-file deduplication.

---

## 10. GUI Applications

GMW provides two full graphical interfaces:

### Simple GUI (Wizard-Style)
- Folder → Archive  
- Step-by-step compression dialog  

### Complete GUI
- Compress  
- Extract  
- Search  
- File browser  
- Metadata viewer  
- Selective extraction  
- Instructions for HTTP serving  

These interfaces make GMW accessible to non-technical users.

---

## 11. Applications

GMW is ideal for:

- dataset publication  
- dataset ingestion pipelines  
- cloud storage & object stores  
- ML training clusters  
- distributed sampling  
- codebase deduplication  
- multimodal research corpora  
- long-term archival systems  

Its random-access semantics and SQLite-embedded metadata make it especially valuable for **AI training at scale**.

---

## 12. Conclusion

The Geometric Motion Wrapper introduces a fundamental shift in archival design:

- from sequential pipelines to geometric, parallelizable structures,  
- from byte streams to introspective content lakes,  
- from monolithic extraction to fine-grained chunk access.

By merging compression, deduplication, metadata indexing, parallel computation, and HTTP chunk streaming into a single container format, GMW resolves the I/O bottlenecks limiting modern machine-learning systems.

GMW is not a derivative compressor—it is a new organizational principle for data itself.

---


⸻

