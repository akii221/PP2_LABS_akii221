def uniq(nums):
    new = []
    for kalabaka in nums:
        if kalabaka not in new:
            new.append(kalabaka)
    return new
    
print(uniq([1, 2, 3, 3, 4, 4, 5, 5]))