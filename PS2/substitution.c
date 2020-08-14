#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    if (argc < 2)
    {
        printf("Usage: ./substitution KEY.\n");
        return 1;
    }


    string key = argv[1];
    int len = strlen(key);


    for (int a = 0; a < len; a++)
    {
        key[a] = toupper(key[a]);
    }



    //validate key
    //check key length
    if (len != 26)
    {
        printf("Key must contain 26 letters.\n");
        return 1;
    }


    //check for alphabetical characters
    for (int i = 0; i < len; i++)
    {
        if (key[i] < 65 || key[i] > 90)
        {
            printf("Key must only contain alphabetical characters.\n");
            return 1;
        }
    }


    //check for repeated characters
    int dups[len];
    for (int i = 0; i < len; i++)
    {
        dups[i] = 0;
    }

    for (int i = 0; i < len; i++)
    {
        if (dups[key[i] - 65] == 0)
        {
            dups[key[i] - 65] = 1;
        }

        else if (dups[key[i] - 65] == 1)
        {
            printf("Key must not contain repeated characters.\n");
            return 1;
        }
    }


    //prompt for plaintext
    string ptxt = get_string("plaintext: ");
    string ctxt = ptxt;

    //decipher plaintext
    for (int i = 0; i < strlen(ptxt); i++)
    {
        if (ptxt[i] > 64 && ptxt[i] < 91)
        {
            // ptxt[i] is the letter you are trying to replace
            // key[ptxt[i] - 'A'] is the letter in the key to replace the plaintext letter
            // ctxt[i] is the place to put the replacement letter

            ctxt[i] = key[ptxt[i] - 'A'];
        }

        if (ptxt[i] > 96 && ptxt[i] < 123)
        {
            ctxt[i] = (char)(key[ptxt[i] - 'a'] + 32);
        }
    }


    //print ciphertext
    printf("ciphertext: %s\n", ctxt);
}
