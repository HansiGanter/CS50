// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 1000;

// Hash table
node *table[N];

int word_count = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    int n = strlen(word);
    char word_lowercase[n + 1];
    for (int i = 0; i < n; i++)
    {
        word_lowercase[i] = tolower(word[i]);
    }
    word_lowercase[n] = '\0';
    int index = hash(word_lowercase);
    node *cursor = table[index];
    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    // My own solution
    int value = 0;
    for (int i = 0, n = strlen(word); i < n; i++)
    {
        value += word[i];
    }

    // bench mark from the internet
    // unsigned int hash = 0;
    // for (int i = 0, n = strlen(hash_this); i < n; i++)
    // {
    //     hash = (hash << 2) ^ hash_this[i];
    // }
    // return hash % HASHTABLE_SIZE;
    return value % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        printf("Could not open %s.\n", dictionary);
        return false;
    }

    char word[LENGTH + 1];
    while (fscanf(file, "%s", word) != EOF)
    {
        node *temp_node = malloc(sizeof(node));
        if (temp_node == NULL)
        {
            printf("Out of memory");
            unload();
            return false;
        }
        strcpy(temp_node->word, word);
        int index = hash(temp_node->word);
        node *head = table[index];
        if (head == NULL)
        {
            table[index] = temp_node;
            word_count++;
        }
        else
        {
            temp_node->next = table[index];
            table[index] = temp_node;
            word_count++;
        }
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        node *head = table[i];
        node *cursor = head;
        node *tmp = head;

        while (cursor != NULL)
        {
            cursor = cursor->next;
            free(tmp);
            tmp = cursor;
        }
    }
    return true;
}
