//helpers.c
#include "helpers.h"
#include <stdio.h>
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    int average;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            average = round((image[i][j].rgbtRed + image[i][j].rgbtGreen + image [i][j].rgbtBlue) / 3.0);

            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    float sepiaRed;
    float sepiaGreen;
    float sepiaBlue;

    int sepiaR;
    int sepiaG;
    int sepiaB;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //sepia filter equations
            sepiaRed = .393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue;
            sepiaGreen = .349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue;
            sepiaBlue = .272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue;

            sepiaR = round(sepiaRed);
            sepiaG = round(sepiaGreen);
            sepiaB = round(sepiaBlue);

            //cap at 255
            if (sepiaR > 255)
            {
                image[i][j].rgbtRed = 255;
            }
            else
            {
                image[i][j].rgbtRed = sepiaR;
            }

            if (sepiaG > 255)
            {
                image[i][j].rgbtGreen = 255;
            }
            else
            {
                image[i][j].rgbtGreen = sepiaG;
            }

            if (sepiaB > 255)
            {
                image[i][j].rgbtBlue = 255;
            }
            else
            {
                image[i][j].rgbtBlue = sepiaB;
            }
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    int halfwidth = round(width / 2);

    for (int i = 0; i < height; i++)
    {
        //iterate through half
        for (int j = 0; j < halfwidth; j++)
        {
            RGBTRIPLE temp = image[i][j];   //temporary copy of image to reflect
            image[i][j] = image[i][width - (j + 1)];    //width - one more than the pixel's place in the row
            image[i][width - (j + 1)] = temp;   //set value to temp variable
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];  //temporary image to be blurred
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //set temp equal to the image
            temp[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float totalred = 0;
            float totalblue = 0;
            float totalgreen = 0;
            int c = 0;

            //check for surrounding pixels
            for (int h = -1; h < 2; h++)
            {
                for (int w = -1; w < 2; w++)
                {
                    if (i + h < 0 || i + h >= height)
                    {
                        continue; //skip
                    }

                    if (j + w < 0 || j + w >= width)
                    {
                        continue; //skip
                    }

                    //average color values for all pixels
                    totalred += temp[i + h][j + w].rgbtRed;
                    totalblue += temp[i + h][j + w].rgbtBlue;
                    totalgreen += temp[i + h][j + w].rgbtGreen;
                    c++;
                }
            }

            //round each number divided by the number of pixels to nearest int
            image[i][j].rgbtRed = round(totalred / c);
            image[i][j].rgbtBlue = round(totalblue / c);
            image[i][j].rgbtGreen = round(totalgreen / c);
        }
    }
    return;
}
