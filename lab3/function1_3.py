def solve(numheads, numlegs):
    y = (numlegs - 2 * numheads) // 2
    x = numheads - y
    return x,y


numheads = 35
numlegs = 94
chicken, rabits = solve(numheads, numlegs)
print(chicken, rabits)