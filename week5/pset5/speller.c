// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <strings.h>

#include "dictionary.h"


// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

void free_list(node *n);

// TODO: Choose number of buckets in hash table
const unsigned int N = 593;

// Counter variable for number of words
int COUNT = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Get hash value of word
    int index = hash(word);

    // If bucket is not null we can traverse the list
    if (table[index] != NULL)
    {
        node *trav = table[index];

        // Traverse the linked list until null pointer
        while (trav != NULL)
        {
            // If we find the word return true
            if (strcasecmp(trav->word, word) == 0)
            {
                return true;
            }

            // Move to next node in the list
            trav = trav->next;
        }
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // Calculate hash value
    int sum = 1;

    for (int i = 0; i < strlen(word); i++)
    {
        sum += (tolower(word[i]) * sum * 491) % 313;
    }

    return sum % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open file
    FILE *file = fopen(dictionary, "r");

    // Return if file is null
    if (file == NULL)
    {
        fclose(file);
        return false;
    }

    // Read words into memory
    char word[LENGTH + 1];

    while (fscanf(file, "%s", word) != EOF)
    {
        // Malloc for node
        node *n = malloc(sizeof(node));

        // Return from function if not enough memory
        if (n == NULL)
        {
            fclose(file);
            return false;
        }

        // Copy word into node & set pointer to NULL
        strcpy(n->word, word);
        n->next = NULL;

        // Hash word stored in node to retrieve index
        unsigned int index = hash(n->word);

        // Check to see if node exists at index
        if (table[index] == NULL)
        {
            table[index] = n;
        }
        else
        {
            n->next = table[index];
            table[index] = n;
        }

        COUNT++;

    }
    // Close file
    fclose(file);

    // Return true if all went well
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // Return global variable that counts words as they are added
    return COUNT;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        if (table[i] == NULL)
        {
            continue;
        }

        free_list(table[i]);
    }
    return true;
}

void free_list(node *n)
{
    if (n == NULL)
    {
        return;
    }

    free_list(n->next);
    free(n);
}