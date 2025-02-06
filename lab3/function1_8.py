
def spygame(nums):
    right = [0, 0, 7]
    index = 0

    for num in nums:
        if num == right[index]:
            index += 1
            if index == len(right):
                return True
            
    return False

print(spygame([1,2,4,0,0,7,5]))