#include <stdlib.h>
#include <stdio.h>

int main()
{
	const char* filename = "pdf.encrypted";
	FILE *fp = fopen(filename, "rb");
	if(!fp)
	{
		printf("Error opening file\n");
		return 0;
	}
	unsigned char cipher[8] = { 0 }, header[8] = "%PDF-1.";
	if(!fread(cipher, 1, 8, fp))
	{
		printf("Error reading file\n");
		return 0;
	}
	// for(int i = 0;i < 8; i ++)
	// {
	// 	printf("%c", cipher[i]);
	// }
	// printf("")

	for(int i = 0; i < 256; i++)
	{
		header[7] = i;
		srand(header[0]);
		unsigned char result[8] = { 0 };
		for(int j = 0; j < 8; j++)
		{
			int r = rand();printf("%d-%d ",r, cipher[j]);
			result[j] = cipher[j] ^ r; 
		}
		printf("\n");
		// for(int j = 0; j < 8; j ++)
		// {
		// 	printf("%c", result[j]);
		// }
		// printf("\n");
	}
	return 0;
}