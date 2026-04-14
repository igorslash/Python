use rayon::prelude::*;
use crate::core::{fast_tokenize, clean_text};

pub fn batch_tokenize(texts: Vec<String>) -> Vec<Vec<String>> {
    texts
        .par_iter()
        .map(|text| fast_tokenize(clean_text(text)))
        .collect()
}

pub fn batch_clean(texts: Vec<String>) -> Vec<String> {
    texts
        .par_iter()
        .map(|text| clean_text(text))
        .collect()
}