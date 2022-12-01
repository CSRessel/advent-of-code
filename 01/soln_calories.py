with open('input', mode='r') as infile:
    input = infile.read()

per_elf_strings = input.split(sep="\n\n")
per_elf_lists = [[int(s) for s in elf.split(sep="\n")] for elf in per_elf_strings]
per_elf_calories = [sum(elf_list) for elf_list in per_elf_lists]

# part 1
print(max(per_elf_calories))
# part 2
print(sum(list(reversed(sorted(per_elf_calories)))[:3]))