# sort wordlist in alphabetical order for binary search
with open('arabic-wordlist-1.6/arabic-wordlist-1.6.txt', 'r') as f:
    lines = [line.rstrip() for line in f]

lines.sort()

# write sorted wordlist to a new file
with open('arabic-wordlist-sorted.txt', 'w') as f:
    for line in lines:
        f.write(f"{line}\n")