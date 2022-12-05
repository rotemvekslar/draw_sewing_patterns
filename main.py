import click

from SewingPattern import PantsSewingPattern, TShirtSewingPattern

if __name__ == '__main__':
    pattern_name = input("Enter Pattern Name:\n")
    pattern_type = input("Enter Pattern Type (T-Shirt / Pants):\n")

    patterns = {"T-Shirt": TShirtSewingPattern, "Pants": PantsSewingPattern}
    try:
        pattern = patterns.get(pattern_type)(pattern_name)
    except:
        print("Pattern Type Not Available! yet....(;")

    known_size = input("Do You Know The Wanted Size? (Y/ N)\n")

    if click.confirm('Do You Know The Wanted Size?', default=True):
        size = input("Enter Size:\n")
        size_file = input("Enter Size File Name:\n")
        pattern.get_known_size(size, size_file)
    else:
        pattern.get_size_by_measurements()

    print(pattern)
    pattern.draw_pattern()
