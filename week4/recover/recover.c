#include <cs50.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    uint8_t *buffer = malloc(sizeof(uint8_t) * 512);
    if (buffer == NULL)
    {
        printf("File empty.\n");
        return 1;
    }

    int file_count = 0;
    char filename[8];
    FILE *img;
    bool foundOne = false;
    while (fread(buffer, sizeof(uint8_t), 512, input) == sizeof(uint8_t) * 512)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (foundOne)
                fclose(img);
            sprintf(filename, "%03i.jpg", file_count);
            img = fopen(filename, "w");
            file_count++;
            foundOne = true;
        }
        if (foundOne)
            fwrite(buffer, sizeof(uint8_t), 512, img);
    }
    fclose(input);
    fclose(img);
    free(buffer);
    return 0;
}