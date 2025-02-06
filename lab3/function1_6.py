def reverse_words(sentence):
    return ' '.join(sentence.split()[::-1])

input_string = "We are ready"
reversed_sentence = reverse_words(input_string)
print(reversed_sentence)
