import kronos
import random

@kronos.register('0 1 * * *')
def get_latest_fuel_rate():
    print("in function ****")
    return