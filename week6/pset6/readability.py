# Function to execute the program
def main():
    text = input("Text: ")
    letter_count = count_letters(text)
    word_count = count_words(text)
    sentence_count = count_sentences(text)
    # Calculate average letter count per 100 words
    L = (float(letter_count) / float(word_count)) * 100
    # Calculate average sentence count per 100 words
    S = (float(sentence_count) / float(word_count)) * 100
    # Calculate grade index
    index = (0.0588 * float(L)) - (0.296 * float(S)) - 15.8
    index = round(index)
    if index > 16:
        print("Grade 16+")
        return
    if index < 1:
        print("Before Grade 1")
        return
    print(f"Grade {index}")
    return


# Count number of letters
def count_letters(text):
    count = 0
    for char in text:
        if char.isalpha():
            count += 1
    return count


# Count number of words
def count_words(text):
    count = 1
    for char in text:
        if char == " ":
            count += 1
    return count


# Count number of sentences
def count_sentences(text):
    count = 0
    for char in text:
        sentence_break = ["!", "?", "."]
        if char in sentence_break:
            count += 1
    return count


# Call to main to execute program
main()