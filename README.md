# Fast Text Processor (Rust + Python)

High-performance text tokenization and normalization library written in Rust, exposed to Python via PyO3.

## 🚀 Features

- **Fast Tokenization**: Optimized word splitting without heavy regex overhead.
- **Text Cleaning**: Efficient punctuation removal and lowercasing.
- **Email Extraction**: Regex-based email finding compiled once at startup.
- **Parallel Processing**: Batch processing using Rayon for multi-core utilization.
- **Pythonic API**: Seamless integration with standard Python types.

## 📦 Installation

Requires Rust toolchain and `maturin`.

```bash
pip install maturin
git clone https://github.com/yourusername/fast-text-proc.git
cd fast-text-proc
maturin develop --release