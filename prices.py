#prices.py
#Robert Nunez
#CEIS 150
import os

count = 0
sum = 0
full_name = input("Please enter your full name: ")
min_price = float(input("Please enter a minimum price to query: "))
price_list = [69.0, 71.0, 84.5, 91.0, 67.4, 81.2, 84.6, 58.8, 79.3, 101.2]

#Check through list, calculate sum and count
for price in price_list:
    sum += price
    if price > min_price:
        count += 1

print("Hello {}, the minimum price is {}.".format(full_name, min_price))
print("There are {} prices greater than the minimum price".format(count))
print("The total price is {:.2f}".format(sum))

os.system('pause') #press any key to continue