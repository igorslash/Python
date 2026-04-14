use once_cell::sync::Lazy;
use regex::Regex;

// Компилируем regex один раз при запуске программы
static EMAIL_REGEX: Lazy<Regex> = Lazy::new(|| {
    Regex::new(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}").unwrap()
});

/// Разбивает текст на слова, игнорируя пунктуацию и лишние пробелы.
/// Работает быстрее split_whitespace + trim, так как делает все за один проход.
pub fn fast_tokenize(text: &str) -> Vec<String> {
    text.split_whitespace()
        .map(|word| {
            // Удаляем небуквенные символы с краев слова (упрощенная нормализация)
            word.trim_matches(|c: char| !c.is_alphanumeric())
                .to_lowercase()
        })
        .filter(|w| !w.is_empty())
        .collect()
}

/// Очищает текст: lower case, удаление пунктуации, схлопывание пробелов.
pub fn clean_text(text: &str) -> String {
    let mut result = String::with_capacity(text.len());
    let mut last_was_space = false;

    for c in text.chars() {
        if c.is_alphabetic() || c.is_numeric() || c == ' ' {
            if c == ' ' {
                if !last_was_space {
                    result.push(' ');
                    last_was_space = true;
                }
            } else {
                result.push(c.to_ascii_lowercase());
                last_was_space = false;
            }
        }
        // Игнорируем пунктуацию и спецсимволы
    }
    
    result.trim().to_string()
}

/// Считает количество слов.
pub fn count_words(text: &str) -> usize {
    // Используем быстрый подсчет без аллокации вектора
    text.split_whitespace()
        .filter(|w| !w.trim_matches(|c: char| !c.is_alphanumeric()).is_empty())
        .count()
}

/// Извлекает email-адреса.
pub fn extract_emails(text: &str) -> Vec<String> {
    EMAIL_REGEX
        .find_iter(text)
        .map(|mat| mat.as_str().to_string())
        .collect()
}