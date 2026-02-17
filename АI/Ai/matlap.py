import pandas as pd
import matplotlib.pyplot as plt

# Исходные данные
data = {
    'name': ['Alice', 'Bob', 'Charlie', 'David'],
    'age': [25, 30, 35, 40],
    'city': ['Moscow', 'London', 'Moscow', 'London']
}

df = pd.DataFrame(data)

# Группировка по городам и расчёт среднего возраста
average_age_by_city = df.groupby('city')['age'].mean()

# Визуализация: столбчатая диаграмма
average_age_by_city.plot(kind='bar', color=['skyblue', 'lightgreen'])
plt.title('Средний возраст по городам')
plt.xlabel('Город')
plt.ylabel('Средний возраст')
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()