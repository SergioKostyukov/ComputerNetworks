import matplotlib.pyplot as plt

# Дані з таблиці
data_size_virtual = [500, 1500, 3000, 5000]
actual_traffic_virtual = [1000, 1000, 1000, 1000]

data_size_datagram = [500, 1500, 3000, 5000]
actual_traffic_datagram = [1000, 2000, 3000, 5000]

# Побудова графіку для VirtualLink (червоний колір)
plt.figure(figsize=(10, 6))
plt.plot(data_size_virtual, actual_traffic_virtual, marker='o', linestyle='-', color='red', label='VirtualLink')

# Побудова графіку для DatagramLink (синій колір)
plt.plot(data_size_datagram, actual_traffic_datagram, marker='o', linestyle='--', color='blue', label='DatagramLink')

plt.title('Залежність кількості службової інформації від розміру повідомлення в Full-Duplex каналі')
plt.xlabel('Розмір даних (байт)')
plt.ylabel('Фактичний обсяг інформації (байт)')
plt.grid(True)
plt.legend()

# Відображення графіку
plt.show()
