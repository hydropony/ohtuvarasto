from varasto import Warehouse

def main():
    juice = Warehouse(100.0)
    beer = Warehouse(100.0, 20.2)

    print("After creation:")
    print(f"Juice warehouse: {juice}")
    print(f"Beer warehouse: {beer}")


if __name__ == "__main__":
    main()
