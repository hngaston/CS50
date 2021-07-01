#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

//Pseudocode
//Open memory card
//Repeat until end of card;
//Read 512 bytes into a buffer;
//If start of new JPEG
//If first JPEG
//...
//Else
//...
//Else
//It already found JPEG
//...
//Close any remaining files

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    //Check for correct usage
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    //Open memory card
    FILE *infile = fopen(argv[1], "r");
    char *infile_name = argv[1];
    if (infile == NULL)
    {
        printf("Could not open %s.\n", infile_name);
        return 1;
    }

    //Read 512 bytes into buffer
    //Repeat until end of card
    BYTE buffer[512];
    int counter = 0;
    FILE *outfile = NULL;
    char filename[8];

    while (fread(&buffer, 512, 1, infile) == 1)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            //If not first, close previous
            if (!(counter == 0))
            {
                fclose(outfile);
            }

            //Create file
            sprintf(infile_name, "%03i.jpg", counter);
            outfile = fopen(infile_name, "w");
            counter++;
        }

        //If found, write to file
        if (!(counter == 0))
        {
            fwrite(&buffer, 512, 1, outfile);
        }
    }

    fclose(infile);
    fclose(outfile);

    return 0;
}
