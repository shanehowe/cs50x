#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // Ensure correct usage
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    // Open file provided by user
    FILE *file = fopen(argv[1], "r");

    // Handle case where file could not be opened
    if (file == NULL)
    {
        printf("Could not open file\n");
        return 2;
    }

    // Allocate memory
    BYTE buffer[512];
    char *new_img = malloc(sizeof(BYTE) * 8);

    // Counter for file name
    int count = 0;

    FILE *img = NULL;

    while (fread(buffer, sizeof(BYTE), 512, file) == 512)
    {
        // Add logic to see if bytes being read are jpeg
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xff) == 0xe0)
        {
            // Close file if we have a previously opened one
            if (img != NULL)
            {
                fclose(img);
            }

            // Create file name
            sprintf(new_img, "%03i.jpg", count);

            img = fopen(new_img, "w");

            if (img == NULL)
            {
                printf("Could not open %s\n", new_img);
                return 3;
            }

            count++;
        }

        if (img != NULL)
        {
            // Write data to new file
            fwrite(buffer, sizeof(BYTE), 512, img);
        }
    }

    // Close files
    fclose(file);
    fclose(img);

    // Free allocated memory
    free(new_img);

    return 0;
}