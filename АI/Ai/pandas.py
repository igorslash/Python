import pandas as pd
# Средний возраст по городам
average_age_by_city = df.groupby('city')['age'].mean()
print("Средний возраст по городам:")
print(average_age_by_city)

# Общая сумма возрастов по городам
total_age_by_city = df.groupby('city')['age'].sum()
print("\nСуммарный возраст по городам:")
print(total_age_by_city)

# Медианный возраст по городам
median_age_by_city = df.groupby('city')['age'].median()
print("\nМедианный возраст по городам:")
print(median_age_by_city)