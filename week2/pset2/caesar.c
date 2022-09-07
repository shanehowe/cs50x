#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

bool only_digits(string text);
char rotate(char c, int key);

int main(int argc, string argv[])
{
    // User did not provide correct number of
    // command line arguments
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // Users key was not a digit
    if (only_digits(argv[1]) == false)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // Conver key to integer
    int key = atoi(argv[1]);

    string plaintext = get_string("plaintext: ");

    printf("ciphertext: ");

    for (int i = 0; i < strlen(plaintext); i++)
    {
        // only encrypt char if is A-Z
        if (isalpha(plaintext[i]))
        {
            printf("%c", rotate(plaintext[i], key));
        }
        else
        {
            printf("%c", plaintext[i]);
        }
    }

    printf("\n");
    return 0;

}

// Check to see if key given is a digit
bool only_digits(string text)
{
    for (int i = 0; i < strlen(text); i++)
    {
        if (!isdigit(text[i]))
        {
            return false;
        }
    }

    return true;
}

// Turn plain text into cipher text
char rotate(char c, int key)
{
    char rotated;

    if (isupper(c))
    {
        rotated = (c + key - 65) % 26 + 65;
    }
    else
    {
        rotated = (c + key - 97) % 26 + 97;
    }

    return rotated;
}