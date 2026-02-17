import sqlglot

def validate_sql(sql_query):
    try:
        # Проверяем синтаксис под PostgreSQL
        sqlglot.transpile(sql_query, read="postgres")
        return True, "Valid SQL"
    except sqlglot.errors.ParseError as e:
        return False, str(e)

# Пример использования
generated_sql = ask_sql("Покажи баланс счета 123")
is_valid, message = validate_sql(generated_sql)

if is_valid:
    print(f"✅ Успех: {generated_sql}")
else:
    print(f"❌ Ошибка в синтаксисе: {message}")
