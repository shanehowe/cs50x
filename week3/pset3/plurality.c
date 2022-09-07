#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    string name;
    int votes;
}
candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
bool vote(string name);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        // Check for invalid vote
        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }
    }

    // Display winner of election
    print_winner();
}

// Update vote totals given a new vote
bool vote(string name)
{
    // loop through candidates array
    for (int i = 0; i < candidate_count; i++)
    {
        // If name matches a name in candidates
        // Update vote count and return true
        if (strcmp(candidates[i].name, name) == 0)
        {
            candidates[i].votes += 1;
            return true;
        }
    }

    return false;
}

// Print the winner (or winners) of the election
void print_winner(void)
{
    // Loop through candidates finding the max amount of votes
    int max_votes = 0;
    for (int i = 0; i < candidate_count; i++)
    {
        // Update max_votes if current candidates votes are greater than previous
        if (candidates[i].votes > max_votes)
        {
            max_votes = candidates[i].votes;
        }
    }

    // Loop through candidates again checking ito see if
    // More candidates got the same amount of votes
    for (int j = 0; j < candidate_count; j++)
    {
        // If so print names accordingly
        if (candidates[j].votes == max_votes)
        {
            printf("%s\n", candidates[j].name);
        }
    }
    return;
}