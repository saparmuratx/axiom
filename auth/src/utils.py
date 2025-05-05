def debug_print(**kwargs):
    print("\n")
    print("#" * 30)
    print("\n")

    for key, value in kwargs.items():
        print(f"{key.upper()}: {value}")

    print("\n")
    print("#" * 30)
