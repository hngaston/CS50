#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

int main(void)
{
    //prompt for text
    string text = get_string("Text: ");


    //get letters
    //set variable for total letters to 0
    int letters = 0;

    //find total length of string
    int len = strlen(text);

    //count each letter and store in varaible 'letters'
    for (int i = 0; i < len; i++)
    {
        if (text[i] > 64 && text[i] < 91)
        {
            letters++;
        }
        if (text[i] > 96 && text[i] < 123)
        {
            letters++;
        }
    }


    //find number of words
    int words = 1;

    for (int w = 1; w < len; w++)
    {
        if (text[w] == 32)
        {
            words++;
        }
    }


    //find numer of sentences
    int sentences = 0;

    for (int s = 0; s < len; s++)
    {
        if ((text[s] == 33 || text[s] == 46 || text[s] == 63))
        {
            sentences++;
        }
    }


    //putting it all together
    //find value of L
    float L = 0;
    L = (((float) letters) / ((float) words) * 100);

    //find value of S
    float S = 0;
    S = (((float) sentences) / ((float) words) * 100);

    //equation and round
    float index = 0;
    index = 0.0588 * L - 0.296 * S - 15.8;

    int grade = round(index);

    if (grade > 16)
    {
        printf("Grade 16+\n");
    }

    else if (grade < 1)
    {
        printf("Before Grade 1\n");
    }

    else
    {
        printf("Grade %i\n", grade);
    }
}
