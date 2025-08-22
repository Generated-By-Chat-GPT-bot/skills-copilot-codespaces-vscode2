def calculator():
    print("Prosty kalkulator (dodawanie i odejmowanie)")
    while True:
        try:
            num1 = float(input("Podaj pierwszą liczbę: "))
            op = input("Podaj operator (+ lub -): ")
            num2 = float(input("Podaj drugą liczbę: "))
            if op == '+':
                result = num1 + num2
            elif op == '-':
                result = num1 - num2
            else:
                print("Nieprawidłowy operator.")
                continue
            print(f"Wynik: {result}")
        except ValueError:
            print("Podano nieprawidłową wartość.")
        again = input("Czy chcesz kontynuować? (t/n): ")
        if again.lower() != 't':
            break

if __name__ == "__main__":
    calculator()