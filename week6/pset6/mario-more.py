# A program to print 2 half pyramids of height according to user input
while True:
    try:
        height = int(input("Height: "))
        if height > 0 and height < 9:
            break
    except ValueError:
        pass

# Prints the half pyramids
for i in range(height):
    print(" " * (height - (i+1)), end="")
    print("#" * ((height - height) + (i + 1)), end="")
    print("  ", end="")
    print("#" * ((height - height) + (i + 1)), end="")
    print()