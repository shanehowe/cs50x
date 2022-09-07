#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    string text = get_string("Text: ");

    // letter_count, word_count, sentence_count treated as floats
    // to avoid integer division and accurately calculate the grade level

    float letter_count = count_letters(text);

    float word_count = count_words(text);

    float sentence_count = count_sentences(text);

    float L = (letter_count / word_count) * 100;

    float S = (sentence_count / word_count) * 100;

    // Formula for calculating grade level
    float index = (0.0588 * L) - (0.296 * S) - 15.8;

    // Round to nearest whole number and format grade as an integer
    int grade_index = round(index);

    if (grade_index >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (grade_index < 1)
    {

        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", grade_index);
    }

}

int count_letters(string text)
{
    int count = 0;

    for (int i = 0; i < strlen(text); i++)
    {
        if (isalpha(text[i]))
        {
            count++;
        }
    }

    return count;
}


int count_words(string text)
{
    int count = 0;

    for (int i = 0; i < strlen(text); i++)
    {
        // ASCII value for a space
        if (text[i] == 32)
        {
            count++;
        }
    }

    // word count will always be one greater than the amount of spaces
    count++;

    return count;
}

int count_sentences(string text)
{
    int count = 0;

    for (int i = 0; i < strlen(text); i++)
    {
        // ASCII values for '.', '?', '!'
        if (text[i] == 33 || text[i] == 63 || text[i] == 46)
        {
            count++;
        }
    }

    return count;
}#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    string text = get_string("Text: ");

    // letter_count, word_count, sentence_count treated as floats
    // to avoid integer division and accurately calculate the grade level

    float letter_count = count_letters(text);

    float word_count = count_words(text);

    float sentence_count = count_sentences(text);

    float L = (letter_count / word_count) * 100;

    float S = (sentence_count / word_count) * 100;

    // Formula for calculating grade level
    float index = (0.0588 * L) - (0.296 * S) - 15.8;

    // Round to nearest whole number and format grade as an integer
    int grade_index = round(index);

    if (grade_index >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (grade_index < 1)
    {

        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", grade_index);
    }

}

int count_letters(string text)
{
    int count = 0;

    for (int i = 0; i < strlen(text); i++)
    {
        if (isalpha(text[i]))
        {
            count++;
        }
    }

    return count;
}


int count_words(string text)
{
    int count = 0;

    for (int i = 0; i < strlen(text); i++)
    {
        // ASCII value for a space
        if (text[i] == 32)
        {
            count++;
        }
    }

    // word count will always be one greater than the amount of spaces
    count++;

    return count;
}

int count_sentences(string text)
{
    int count = 0;

    for (int i = 0; i < strlen(text); i++)
    {
        // ASCII values for '.', '?', '!'
        if (text[i] == 33 || text[i] == 63 || text[i] == 46)
        {
            count++;
        }
    }

    return count;
}