def print_header(name, ip, ct_ratio):

    print("\n" + "=" * 70)
    print(f"{name}")
    print(f"IP        : {ip}")
    print(f"CT Ratio  : {ct_ratio}")
    print("-" * 50)


def print_error(name, error):

    print(f"\n{name} ERROR")
    print(error)