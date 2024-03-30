#include <iostream>
#include <fstream>

struct data
{
    int* numbers = nullptr;
    char* symbols = nullptr;
    unsigned int size = 0;
};


extern "C"
{
    void my_dump(unsigned int* numbers, char* symbols, int size)
    {        
        FILE* out = fopen("comp.bin", "wb");
        unsigned int size_elem = sizeof(int) + sizeof(char);
        
        char* buffer = (char*)calloc(size, size_elem);

        for (int index = 0; index < size; ++index)
        {
            *(int*)(buffer + index * size_elem) = numbers[index];
            buffer[index * size_elem + sizeof(int)] = symbols[index];
        }
    
        fwrite(buffer, size_elem, size, out);
        fclose(out);
        free(buffer);
    }

    data my_load(const char* file_name)
    {
        data dict = {};

        FILE* file = fopen(file_name, "rb");

        unsigned int size_elem = sizeof(int) + sizeof(char);

        fseek(file, 0, SEEK_END);
        int size = ftell(file);
        rewind(file);

        char* buffer = (char*)calloc(size, sizeof(char));

        size = fread(buffer, sizeof(char), size, file);

        dict.size = size / size_elem;

        dict.numbers = (int*)calloc(dict.size, sizeof(int));
        dict.symbols = (char*)calloc(dict.size, sizeof(char));

        for (int index = 0; index < dict.size; ++index)
        {
            dict.numbers[index] = (int)*(int*)(buffer + index * size_elem);
            dict.symbols[index] = *(buffer + index * size_elem + sizeof(int));
        }
        return dict;
    }
}