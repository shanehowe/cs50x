// Modifies the volume of an audio file

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Number of bytes in .wav header
const int HEADER_SIZE = 44;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    float factor = atof(argv[3]);

    // TODO: Copy header from input file to output file
    // Allocating memory for header
    uint8_t *header = malloc(sizeof(uint8_t) * HEADER_SIZE);

    // Reading header into memory
    fread(header, sizeof(uint8_t), HEADER_SIZE, input);

    // Writing header into output file
    fwrite(header, sizeof(uint8_t), HEADER_SIZE, output);

    // TODO: Read samples from input file and write updated data to output file
    int16_t buffer;

    while (fread(&buffer, sizeof(buffer), 1, input))
    {
        // Change volume according to factor provided
        buffer *= factor;

        // Write new bytes to output file
        fwrite(&buffer, sizeof(buffer), 1, output);
    }

    // Close files
    fclose(input);
    fclose(output);

    // Free malloced memory
    free(header);
}