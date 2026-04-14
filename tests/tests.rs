#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tokenize_rust() {
        let text = "Hello, World!";
        let tokens = fast_tokenize(text);
        assert_eq!(tokens, vec!["hello", "world"]);
    }

    #[test]
    fn test_extract_emails_rust() {
        let text = "Email me at test@example.com please";
        let emails = extract_emails(text);
        assert_eq!(emails, vec!["test@example.com"]);
    }
}