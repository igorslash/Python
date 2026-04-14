use pyo3::prelude::*;
use pyo3::types::PyList;

mod core;
mod parallel;

/// Python module "fast_text_proc"
#[pymodule]
fn fast_text_proc(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    
    // --- Single text functions ---
    #[pyfn(m)]
    #[pyo3(name = "fast_tokenize")]
    fn py_fast_tokenize(py: Python, text: &str) -> Vec<String> {
        core::fast_tokenize(text)
    }

    #[pyfn(m)]
    #[pyo3(name = "count_words")]
    fn py_count_words(text: &str) -> usize {
        core::count_words(text)
    }

    #[pyfn(m)]
    #[pyo3(name = "extract_emails")]
    fn py_extract_emails(text: &str) -> Vec<String> {
        core::extract_emails(text)
    }

     // --- Batch / Parallel functions ---

     #[pyfn(m)]
     #[pyo3(name = "batch_tokenize")]
     fn py_batch_tokenize(texts: Vec<String>) -> Vec<Vec<String>> {
         parallel::batch_tokenize(texts)
     }
 
     #[pyfn(m)]
     #[pyo3(name = "batch_clean")]
     fn py_batch_clean(texts: Vec<String>) -> Vec<String> {
         parallel::batch_clean(texts)
     }
 
     Ok(())

}
