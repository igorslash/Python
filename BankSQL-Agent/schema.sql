{
  "instruction": "Найди общую сумму всех транзакций за вчерашний день.",
  "context": "Таблицы: transactions (transaction_id, amount, created_at)",
  "response": "SELECT SUM(amount) as total_amount FROM transactions WHERE created_at::date = CURRENT_DATE - INTERVAL '1 day';"
}
{
  "instruction": "Покажи список клиентов, у которых нет ни одного открытого счета.",
  "context": "Таблицы: clients (client_id, full_name), accounts (account_id, client_id, status)",
  "response": "SELECT c.full_name, c.client_id FROM clients c LEFT JOIN accounts a ON c.client_id = a.client_id AND a.status = 'Open' WHERE a.account_id IS NULL;"
}
{
  "instruction": "Выведи топ-5 отделений по количеству открытых в них счетов.",
  "context": "Таблицы: branches (branch_id, branch_name), accounts (account_id, branch_id, status)",
  "response": "SELECT b.branch_name, COUNT(a.account_id) as accounts_count FROM branches b JOIN accounts a ON b.branch_id = a.branch_id WHERE a.status = 'Open' GROUP BY b.branch_id, b.branch_name ORDER BY accounts_count DESC LIMIT 5;"
}
{
  "instruction": "Найди клиентов, у которых суммарный баланс по всем счетам превышает 1 миллион рублей.",
  "context": "Таблицы: clients (client_id, full_name), accounts (account_id, client_id, balance)",
  "response": "SELECT c.full_name, SUM(a.balance) as total_balance FROM clients c JOIN accounts a ON c.client_id = a.client_id GROUP BY c.client_id, c.full_name HAVING SUM(a.balance) > 1000000;"
}
{
  "instruction": "Посчитай среднюю сумму транзакции для каждого типа операции (пополнение, списание, перевод).",
  "context": "Таблицы: transactions (transaction_id, amount, transaction_type)",
  "response": "SELECT transaction_type, AVG(amount) as avg_amount FROM transactions GROUP BY transaction_type;"
}
{
  "instruction": "Выведи список кредитов, по которым была просрочка платежа более 30 дней в текущем году.",
  "context": "Таблицы: loans (loan_id, client_id, principal_amount), overdue_payments (overdue_id, loan_id, days_overdue, overdue_date)",
  "response": "SELECT DISTINCT l.loan_id, l.principal_amount FROM loans l JOIN overdue_payments op ON l.loan_id = op.loan_id WHERE op.days_overdue > 30 AND EXTRACT(YEAR FROM op.overdue_date) = EXTRACT(YEAR FROM CURRENT_DATE);"
}
{
  "instruction": "Найди 10 самых крупных транзакций за последнюю неделю.",
  "context": "Таблицы: transactions (transaction_id, from_account_id, to_account_id, amount, created_at)",
  "response": "SELECT transaction_id, amount, created_at FROM transactions WHERE created_at >= CURRENT_DATE - INTERVAL '7 days' ORDER BY amount DESC LIMIT 10;"
}
{
  "instruction": "Покажи количество счетов, открытых в каждом месяце 2024 года.",
  "context": "Таблицы: accounts (account_id, opened_at)",
  "response": "SELECT EXTRACT(MONTH FROM opened_at) as month, COUNT(*) as accounts_opened FROM accounts WHERE EXTRACT(YEAR FROM opened_at) = 2024 GROUP BY EXTRACT(MONTH FROM opened_at) ORDER BY month;"
}
{
  "instruction": "Выведи клиентов, которые совершали транзакции на сумму более 500 тысяч рублей за один раз.",
  "context": "Таблицы: clients (client_id, full_name), accounts (account_id, client_id), transactions (from_account_id, amount)",
  "response": "SELECT DISTINCT c.full_name FROM clients c JOIN accounts a ON c.client_id = a.client_id JOIN transactions t ON a.account_id = t.from_account_id WHERE t.amount > 500000;"
}
{
  "instruction": "Посчитай общую комиссию, заработанную банком за прошлый месяц.",
  "context": "Таблицы: transactions (transaction_id, fee_amount, created_at)",
  "response": "SELECT SUM(fee_amount) as total_fee FROM transactions WHERE EXTRACT(MONTH FROM created_at) = EXTRACT(MONTH FROM CURRENT_DATE - INTERVAL '1 month') AND EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM CURRENT_DATE - INTERVAL '1 month');"
}
{
  "instruction": "Найди счета, которые не использовались для транзакций более 6 месяцев.",
  "context": "Таблицы: accounts (account_id, client_id), transactions (from_account_id, created_at)",
  "response": "SELECT a.account_id FROM accounts a LEFT JOIN transactions t ON a.account_id = t.from_account_id AND t.created_at > CURRENT_DATE - INTERVAL '6 months' WHERE t.from_account_id IS NULL;"
}
{
  "instruction": "Выведи клиентов, у которых есть и кредитные, и дебетовые счета.",
  "context": "Таблицы: clients (client_id, full_name), accounts (account_id, client_id, account_type)",
  "response": "SELECT c.full_name FROM clients c JOIN accounts a ON c.client_id = a.client_id GROUP BY c.client_id, c.full_name HAVING COUNT(DISTINCT CASE WHEN a.account_type = 'Credit' THEN 1 END) > 0 AND COUNT(DISTINCT CASE WHEN a.account_type IN ('Debit', 'Checking', 'Savings') THEN 1 END) > 0;"
}
{
  "instruction": "Посчитай соотношение мужчин и женщин среди клиентов банка.",
  "context": "Таблицы: clients (client_id, gender)",
  "response": "SELECT gender, COUNT(*) as count, ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage FROM clients WHERE gender IN ('M', 'F') GROUP BY gender;"
}
{
  "instruction": "Найди средний возраст клиентов, у которых есть депозитный счет.",
  "context": "Таблицы: clients (client_id, birth_date), accounts (account_id, client_id, account_type)",
  "response": "SELECT AVG(EXTRACT(YEAR FROM AGE(CURRENT_DATE, c.birth_date))) as avg_age FROM clients c JOIN accounts a ON c.client_id = a.client_id WHERE a.account_type = 'Deposit';"
}
{
  "instruction": "Выведи топ-5 счетов по количеству входящих переводов.",
  "context": "Таблицы: accounts (account_id), transactions (to_account_id, transaction_id)",
  "response": "SELECT a.account_id, COUNT(t.transaction_id) as incoming_count FROM accounts a JOIN transactions t ON a.account_id = t.to_account_id GROUP BY a.account_id ORDER BY incoming_count DESC LIMIT 5;"
}
{
  "instruction": "Покажи общую сумму выданных кредитов по каждому отделению за 2024 год.",
  "context": "Таблицы: branches (branch_id, branch_name), loans (loan_id, branch_id, principal_amount, issued_at)",
  "response": "SELECT b.branch_name, SUM(l.principal_amount) as total_loans FROM branches b JOIN loans l ON b.branch_id = l.branch_id WHERE EXTRACT(YEAR FROM l.issued_at) = 2024 GROUP BY b.branch_id, b.branch_name;"
}
{
  "instruction": "Найди клиентов, у которых изменился номер телефона (есть запись в истории изменений).",
  "context": "Таблицы: clients (client_id, full_name), client_history (client_id, field_name, changed_at)",
  "response": "SELECT DISTINCT c.full_name FROM clients c JOIN client_history ch ON c.client_id = ch.client_id WHERE ch.field_name = 'phone_number';"
}
{
  "instruction": "Выведи список карт, которые будут заблокированы автоматически в ближайшие 30 дней (срок истекает).",
  "context": "Таблицы: cards (card_id, card_number, expiry_date)",
  "response": "SELECT card_number, expiry_date FROM cards WHERE expiry_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '30 days';"
}
{
  "instruction": "Посчитай количество активных кредитных карт у клиентов премиум-сегмента.",
  "context": "Таблицы: clients (client_id, segment), cards (card_id, client_id, card_type, status)",
  "response": "SELECT COUNT(c.card_id) FROM cards c JOIN clients cl ON c.client_id = cl.client_id WHERE cl.segment = 'Premium' AND c.card_type = 'Credit' AND c.status = 'Active';"
}
{
  "instruction": "Найди среднюю сумму транзакции в зависимости от дня недели.",
  "context": "Таблицы: transactions (amount, created_at)",
  "response": "SELECT EXTRACT(DOW FROM created_at) as day_of_week, AVG(amount) as avg_amount FROM transactions GROUP BY EXTRACT(DOW FROM created_at) ORDER BY day_of_week;"
}
{
  "instruction": "Выведи клиентов, у которых суммарный баланс по счетам уменьшился за последний месяц.",
  "context": "Таблицы: account_balance_history (account_id, balance, recorded_at), accounts (account_id, client_id)",
  "response": "WITH current_balance AS (SELECT account_id, balance FROM account_balance_history WHERE recorded_at::date = CURRENT_DATE), previous_balance AS (SELECT account_id, balance FROM account_balance_history WHERE recorded_at::date = CURRENT_DATE - INTERVAL '1 month') SELECT a.client_id, cb.balance - pb.balance as balance_change FROM accounts a JOIN current_balance cb ON a.account_id = cb.account_id JOIN previous_balance pb ON a.account_id = pb.account_id WHERE cb.balance < pb.balance;"
}
{
  "instruction": "Посчитай долю заблокированных счетов от общего количества счетов.",
  "context": "Таблицы: accounts (status)",
  "response": "SELECT ROUND(COUNT(CASE WHEN status = 'Blocked' THEN 1 END) * 100.0 / COUNT(*), 2) as blocked_percentage FROM accounts;"
}
{
  "instruction": "Найди транзакции, которые были отменены (имеют запись в таблице отмен).",
  "context": "Таблицы: transactions (transaction_id, amount), cancelled_transactions (transaction_id, cancelled_at, reason)",
  "response": "SELECT t.transaction_id, t.amount, ct.reason FROM transactions t JOIN cancelled_transactions ct ON t.transaction_id = ct.transaction_id;"
}
{
  "instruction": "Выведи список отделений, в которых не было открыто ни одного счета в прошлом месяце.",
  "context": "Таблицы: branches (branch_id, branch_name), accounts (account_id, branch_id, opened_at)",
  "response": "SELECT b.branch_name FROM branches b LEFT JOIN accounts a ON b.branch_id = a.branch_id AND EXTRACT(MONTH FROM a.opened_at) = EXTRACT(MONTH FROM CURRENT_DATE - INTERVAL '1 month') AND EXTRACT(YEAR FROM a.opened_at) = EXTRACT(YEAR FROM CURRENT_DATE - INTERVAL '1 month') WHERE a.account_id IS NULL;"
}
{
  "instruction": "Посчитай общую сумму кредитов, выданных клиентам в возрасте от 30 до 40 лет.",
  "context": "Таблицы: clients (client_id, birth_date), loans (loan_id, client_id, principal_amount)",
  "response": "SELECT SUM(l.principal_amount) as total_loans FROM clients c JOIN loans l ON c.client_id = l.client_id WHERE EXTRACT(YEAR FROM AGE(CURRENT_DATE, c.birth_date)) BETWEEN 30 AND 40;"
}
{
  "instruction": "Найди клиентов, которые совершали транзакции в выходные дни более 10 раз.",
  "context": "Таблицы: clients (client_id, full_name), accounts (account_id, client_id), transactions (from_account_id, created_at)",
  "response": "SELECT c.full_name, COUNT(t.transaction_id) as weekend_transactions FROM clients c JOIN accounts a ON c.client_id = a.client_id JOIN transactions t ON a.account_id = t.from_account_id WHERE EXTRACT(DOW FROM t.created_at) IN (0, 6) GROUP BY c.client_id, c.full_name HAVING COUNT(t.transaction_id) > 10;"
}
{
  "instruction": "Выведи топ-3 самых популярных типа счетов среди клиентов до 25 лет.",
  "context": "Таблицы: clients (client_id, birth_date), accounts (account_id, client_id, account_type)",
  "response": "SELECT a.account_type, COUNT(*) as count FROM clients c JOIN accounts a ON c.client_id = a.client_id WHERE EXTRACT(YEAR FROM AGE(CURRENT_DATE, c.birth_date)) < 25 GROUP BY a.account_type ORDER BY count DESC LIMIT 3;"
}
{
  "instruction": "Посчитай среднюю сумму транзакции для каждого часа суток.",
  "context": "Таблицы: transactions (amount, created_at)",
  "response": "SELECT EXTRACT(HOUR FROM created_at) as hour_of_day, AVG(amount) as avg_amount FROM transactions GROUP BY EXTRACT(HOUR FROM created_at) ORDER BY hour_of_day;"
}
{
  "instruction": "Найди клиентов, у которых есть счет в валюте, отличной от валюты их страны проживания.",
  "context": "Таблицы: clients (client_id, country_code), accounts (account_id, client_id, currency), countries (country_code, currency_code)",
  "response": "SELECT c.client_id FROM clients c JOIN accounts a ON c.client_id = a.client_id JOIN countries cnt ON c.country_code = cnt.country_code WHERE a.currency != cnt.currency_code;"
}
{
  "instruction": "Выведи список кредитов с просрочкой, отсортировав по количеству дней просрочки.",
  "context": "Таблицы: loans (loan_id, client_id), overdue_payments (loan_id, days_overdue)",
  "response": "SELECT l.loan_id, MAX(op.days_overdue) as max_overdue FROM loans l JOIN overdue_payments op ON l.loan_id = op.loan_id GROUP BY l.loan_id ORDER BY max_overdue DESC;"
}
{
  "instruction": "Посчитай количество новых клиентов, зарегистрировавшихся в каждом квартале 2024 года.",
  "context": "Таблицы: clients (client_id, registration_date)",
  "response": "SELECT EXTRACT(QUARTER FROM registration_date) as quarter, COUNT(*) as new_clients FROM clients WHERE EXTRACT(YEAR FROM registration_date) = 2024 GROUP BY EXTRACT(QUARTER FROM registration_date) ORDER BY quarter;"
}
{
  "instruction": "Найди счета, баланс на которых ниже минимального порога (например, 1000 рублей).",
  "context": "Таблицы: accounts (account_id, balance, min_balance_threshold)",
  "response": "SELECT account_id, balance FROM accounts WHERE balance < COALESCE(min_balance_threshold, 1000);"
}
{
  "instruction": "Выведи клиентов, которые закрыли счет в течение месяца после открытия.",
  "context": "Таблицы: accounts (account_id, client_id, opened_at, closed_at)",
  "response": "SELECT a.client_id FROM accounts a WHERE a.closed_at IS NOT NULL AND a.closed_at - a.opened_at <= INTERVAL '30 days';"
}
{
  "instruction": "Посчитай общую комиссию по транзакциям для каждого отделения.",
  "context": "Таблицы: branches (branch_id, branch_name), accounts (account_id, branch_id), transactions (from_account_id, fee_amount)",
  "response": "SELECT b.branch_name, SUM(t.fee_amount) as total_fee FROM branches b JOIN accounts a ON b.branch_id = a.branch_id JOIN transactions t ON a.account_id = t.from_account_id GROUP BY b.branch_id, b.branch_name;"
}
{
  "instruction": "Найди клиентов, у которых фамилия начинается на 'Иванов' и есть дебетовая карта.",
  "context": "Таблицы: clients (client_id, full_name), cards (card_id, client_id, card_type)",
  "response": "SELECT DISTINCT c.full_name FROM clients c JOIN cards ca ON c.client_id = ca.client_id WHERE c.full_name LIKE 'Иванов%' AND ca.card_type = 'Debit';"
}
{
  "instruction": "Выведи статистику по использованию разных типов карт (количество, средний оборот).",
  "context": "Таблицы: cards (card_id, client_id, card_type), transactions (card_id, amount)",
  "response": "SELECT c.card_type, COUNT(DISTINCT c.card_id) as cards_count, AVG(t.amount) as avg_transaction_amount FROM cards c LEFT JOIN transactions t ON c.card_id = t.card_id GROUP BY c.card_type;"
}
{
  "instruction": "Посчитай количество транзакций, совершенных через мобильное приложение за последнюю неделю.",
  "context": "Таблицы: transactions (transaction_id, channel, created_at)",
  "response": "SELECT COUNT(*) as mobile_transactions FROM transactions WHERE channel = 'Mobile App' AND created_at >= CURRENT_DATE - INTERVAL '7 days';"
}
{
  "instruction": "Найди клиентов, которые были обслужены в отделении более 5 раз за последний месяц.",
  "context": "Таблицы: clients (client_id, full_name), branch_visits (visit_id, client_id, visit_date)",
  "response": "SELECT c.full_name, COUNT(bv.visit_id) as visits_count FROM clients c JOIN branch_visits bv ON c.client_id = bv.client_id WHERE bv.visit_date >= CURRENT_DATE - INTERVAL '1 month' GROUP BY c.client_id, c.full_name HAVING COUNT(bv.visit_id) > 5;"
}
{
  "instruction": "Выведи список всех кредитных договоров с суммой больше среднего кредита по банку.",
  "context": "Таблицы: loans (loan_id, principal_amount)",
  "response": "SELECT loan_id, principal_amount FROM loans WHERE principal_amount > (SELECT AVG(principal_amount) FROM loans);"
}
{
  "instruction": "Посчитай, сколько клиентов пользуются интернет-банком (есть запись входа за последние 30 дней).",
  "context": "Таблицы: clients (client_id), online_banking_logins (login_id, client_id, login_time)",
  "response": "SELECT COUNT(DISTINCT client_id) as active_online_users FROM online_banking_logins WHERE login_time >= CURRENT_DATE - INTERVAL '30 days';"
}
{
  "instruction": "Найди счета, с которых были попытки снятия средств, превышающие доступный баланс (овердрафт).",
  "context": "Таблицы: accounts (account_id, balance), transaction_attempts (attempt_id, account_id, requested_amount)",
  "response": "SELECT a.account_id, a.balance, ta.requested_amount FROM accounts a JOIN transaction_attempts ta ON a.account_id = ta.account_id WHERE ta.requested_amount > a.balance;"
}
{
  "instruction": "Выведи клиентов, у которых день рождения сегодня.",
  "context": "Таблицы: clients (client_id, full_name, birth_date)",
  "response": "SELECT full_name, birth_date FROM clients WHERE EXTRACT(MONTH FROM birth_date) = EXTRACT(MONTH FROM CURRENT_DATE) AND EXTRACT(DAY FROM birth_date) = EXTRACT(DAY FROM CURRENT_DATE);"
}
{
  "instruction": "Посчитай общую сумму депозитов, привлеченных каждым менеджером.",
  "context": "Таблицы: managers (manager_id, manager_name), deposits (deposit_id, manager_id, amount)",
  "response": "SELECT m.manager_name, SUM(d.amount) as total_deposits FROM managers m JOIN deposits d ON m.manager_id = d.manager_id GROUP BY m.manager_id, m.manager_name;"
}
{
  "instruction": "Найди клиентов, которые меняли паспортные данные более одного раза.",
  "context": "Таблицы: clients (client_id, full_name), passport_changes (change_id, client_id, change_date)",
  "response": "SELECT c.full_name, COUNT(pc.change_id) as changes_count FROM clients c JOIN passport_changes pc ON c.client_id = pc.client_id GROUP BY c.client_id, c.full_name HAVING COUNT(pc.change_id) > 1;"
}
{
  "instruction": "Выведи список самых старых активных счетов (топ-10 по дате открытия).",
  "context": "Таблицы: accounts (account_id, opened_at, status)",
  "response": "SELECT account_id, opened_at FROM accounts WHERE status = 'Active' ORDER BY opened_at ASC LIMIT 10;"
}
{
  "instruction": "Посчитай средний чек (сумму транзакции) для POS-терминалов по категориям магазинов.",
  "context": "Таблицы: pos_terminals (terminal_id, merchant_category), transactions (terminal_id, amount)",
  "response": "SELECT pt.merchant_category, AVG(t.amount) as avg_check FROM pos_terminals pt JOIN transactions t ON pt.terminal_id = t.terminal_id GROUP BY pt.merchant_category;"
}
{
  "instruction": "Найди клиентов, у которых сумма кредитов превышает сумму депозитов в 2 раза.",
  "context": "Таблицы: clients (client_id), loans (client_id, principal_amount), deposits (client_id, amount)",
  "response": "SELECT c.client_id, COALESCE(SUM(l.principal_amount), 0) as total_loans, COALESCE(SUM(d.amount), 0) as total_deposits FROM clients c LEFT JOIN loans l ON c.client_id = l.client_id LEFT JOIN deposits d ON c.client_id = d.client_id GROUP BY c.client_id HAVING COALESCE(SUM(l.principal_amount), 0) > 2 * COALESCE(SUM(d.amount), 0);"
}
{
  "instruction": "Выведи информацию о последней транзакции по каждому счету.",
  "context": "Таблицы: accounts (account_id), transactions (from_account_id, amount, created_at)",
  "response": "SELECT DISTINCT ON (a.account_id) a.account_id, t.amount, t.created_at FROM accounts a LEFT JOIN transactions t ON a.account_id = t.from_account_id ORDER BY a.account_id, t.created_at DESC;"
}
{
  "instruction": "Посчитай количество счетов, открытых до 2020 года, которые до сих пор активны.",
  "context": "Таблицы: accounts (account_id, opened_at, status)",
  "response": "SELECT COUNT(*) as old_active_accounts FROM accounts WHERE opened_at < '2020-01-01' AND status = 'Active';"
}
{
  "instruction": "Найди клиентов, которые совершали транзакции в других странах (по IP или геолокации).",
  "context": "Таблицы: clients (client_id), transactions (transaction_id, client_id, ip_address), ip_geo(ip_range_start, ip_range_end, country)",
  "response": "SELECT DISTINCT c.client_id FROM clients c JOIN transactions t ON c.client_id = t.client_id JOIN ip_geo ig ON t.ip_address::inet BETWEEN ig.ip_range_start::inet AND ig.ip_range_end::inet WHERE ig.country != 'Russia';"
}
{
  "instruction": "Выведи статистику по выданным кредитам с разбивкой по целям кредитования.",
  "context": "Таблицы: loans (loan_id, purpose, principal_amount)",
  "response": "SELECT purpose, COUNT(*) as loans_count, SUM(principal_amount) as total_amount FROM loans GROUP BY purpose ORDER BY total_amount DESC;"
}