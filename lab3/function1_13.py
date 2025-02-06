import random

def numbergame(guess):
    random.seed(20)
    #seed eto po kakomu patterny budet vibirat number 
    number = random.randint(0, 20)
    text = input("Hello, What is your Name?")
    
    while True:
        try:
            guesss = int(input(f'well,{text}, im thinking of a number, take a guess'))
            if guesss > number:
                    print('your guess is too high')
            elif guesss < number:
                    print('your guess is too low')
            else:
                    print(f'Good job, {text}! you guessed the number right')
                    break
        except ValueError:  
            print('wrong value')
    # dlya try: vsegda dolzhno bit except 
                
    
numbergame(0)