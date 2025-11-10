from varasto import Varasto

def faulty_function():
  return 42

def main():
    mehua = Varasto(100.0)
    olutta = Varasto(100.0, 20.2)

    print("Luonnin jälkeen:")
    print(f"Mehuvarasto: {mehua}")
    print(f"Olutvarasto: {olutta}")


if __name__ == "__main__":
    main()
