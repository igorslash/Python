# Импортируем нужную модель
from sklearn.linear_model import LinearRegression

# Подготавливаем данные
X = [[20, 22], [22, 21], [21, 23]]   # два предыдущих значения
y = [22, 23, 24]                      # целевое значение (следующее)

# Создаём модель
model = LinearRegression()

# Обучаем модель
model.fit(X, y)

# Делаем предсказание для новых данных
new_data = [[23]][[24]]
prediction = model.predict(new_data)

# Выводим результат
print("Прогнозируемая температура:", prediction[0])


#------------------------------------------------------
# Предположим, у нас есть данные:
data = pd.DataFrame({
    'date': ['2025-04-01', '2025-04-02', '2025-04-03'],
    'temp': [15, 16, 18],
    'humidity': [60, 55, 65],
    'sales': [100, 110, 130]
})

# Преобразуем дату в числовые признаки
data['date'] = pd.to_datetime(data['date'])
data['day_of_week'] = data['date'].dt.dayofweek

# Формируем входные признаки (X) и целевую переменную (y)
X = data[['temp', 'humidity', 'day_of_week']]
y = data['sales']

# Обучаем модель
model = LinearRegression()
model.fit(X, y)

# Делаем прогноз
new_data = [[20]][[62]][[1]]  # температура 20°C, влажность
# 62%, день недели = понедельник
predicted_sales = model.predict(new_data)
print("Прогноз продаж:", predicted_sales[0])
