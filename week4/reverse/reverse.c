#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include "wav.h"

int check_format(WAVHEADER header);
int get_block_size(WAVHEADER header);
int HEADER_SIZE = 44;

int main(int argc, char *argv[])
{
    // Ensure proper usage
    // TODO #1
    if (argc != 3)
    {
        printf("Usage: ./recover INPUT OUTPUT");
        return 1;
    }

    // Open input file for reading
    // TODO #2
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    // Read header
    // TODO #3
    WAVHEADER header;
    fread(&header, sizeof(WAVHEADER), 1, input);

    // Use check_format to ensure WAV format
    // TODO #4
    if (!check_format(header))
    {
        printf("Not a .wav file.\n");
        return 1;
    }

    // Open output file for writing
    // TODO #5
    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not create output file.\n");
        return 1;
    }

    // Write header to file
    // TODO #6
    fwrite(&header, sizeof(WAVHEADER), 1, output);

    // Use get_block_size to calculate size of block
    // TODO #7
    int BLOCK_SIZE = get_block_size(header);

    // Write reversed audio to file
    // TODO #8
    BYTE buffer[BLOCK_SIZE];
    fseek(input, 0, SEEK_END);
    long audio_size = ftell(input) - sizeof(WAVHEADER);
    int audio_block = (int) audio_size / BLOCK_SIZE;
    for (int i = audio_block - 1; i >= 0; i--)
    {
        fseek(input, sizeof(WAVHEADER) + i * BLOCK_SIZE, SEEK_SET);
        fread(buffer, BLOCK_SIZE, 1, input);
        fwrite(buffer, BLOCK_SIZE, 1, output);
    }

    fclose(input);
    fclose(output);
}

int check_format(WAVHEADER header)
{
    // TODO #4
    return (header.format[0] == 'W' && header.format[1] == 'A' && header.format[2] == 'V' && header.format[3] == 'E');
}

int get_block_size(WAVHEADER header)
{
    // TODO #7
    return header.numChannels * (header.bitsPerSample / 8);
}