import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Исходные данные
data = pd.DataFrame({
    'temp': [15, 16, 18, 20, 22],
    'humidity': [60, 55, 65, 70, 50],
    'sales': [100, 110, 130, 140, 150]
})

# Входные данные (X) и целевая переменная (y)
X = data[['temp', 'humidity']]
y = data['sales']

# Нормализация данных
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Разделение на обучающие и тестовые данные
(X_train, X_test, y_train, y_test) = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Создание нейросети
model = Sequential([
    Dense(10, activation='relu', input_shape=(X_train.shape[1],)),
    Dense(1)
])

# Компиляция модели
model.compile(optimizer='adam', loss='mse')

# Обучение модели
model.fit(X_train, y_train, epochs=100, verbose=0)

# Предсказание
new_data = scaler.transform([[21]][[60]])  # температура 21°C,
# влажность 60%
predicted_sales = model.predict(new_data)
print("Прогноз продаж:", predicted_sales[0][0])

#-----------------------------------------------------

# 1. Загрузка данных из CSV
data = pd.read_csv('data.csv')  # файл должен быть в той же папке

# 2. Подготовка данных
X = data[['temp', 'humidity']].values
y = data['sales'].values

# 3. Нормализация входных данных
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# 4. Разделение данных
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# 5. Создание модели
model = Sequential([
    Dense(10, activation='relu', input_shape=(2,)),
    Dense(1)
])

# 6. Компиляция и обучение
model.compile(optimizer='adam', loss='mse')
model.fit(X_train, y_train, epochs=100, batch_size=2, verbose=1)

# 7. Оценка качества
loss = model.evaluate(X_test, y_test, verbose=0)
print(f"Test Loss: {loss:.4f}")

# 8. Прогнозирование новых данных
new_data = np.array([[22]][[75]])  # новая точка: температура 22°C, влажность 75%
new_data_scaled = scaler.transform(new_data)  # нормализуем её так же, как и обучающие данные
prediction = model.predict(new_data_scaled)

print(f"Прогноз продаж при температуре 22°C и влажности 75%: {prediction[0][0]:.2f}")