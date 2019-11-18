#include <stdlib.h>
#include <math.h>
#include "myfilesystem.h"
#include <stdio.h>
#include<string.h>
#include<pthread.h>

//#define MAX_FILE_DATA 256*pow(2,24)
#define MAX_DIRECTORY_TABLE  pow(2,16)

//lock for the parallel write_file
pthread_mutex_t write_lock;
pthread_mutex_t lock[9];


//struct for files
struct file{//storing the new file info (name, offset, length)
    char name[64];
    int offset;
    int length;

};

//struct for the whole system
typedef struct data{//this is the main object
    FILE* file_data;
    FILE* directory_table;
    FILE* hash_data;
    int n_processors;
    size_t MAX_FILE_DATA;//thisis the size of file_data

}data;
int count_files(data* ptr);


int find_smallestoffset(data* ptr){//find the smallest offset in the directory table to insert te new file
    int result;

    fseek(ptr->directory_table,0,SEEK_END);
    //get the size of directory table
    size_t size = ftell(ptr->directory_table);
    fseek(ptr->directory_table,0,SEEK_SET);
    struct file temp;//store the 72 bytes here

    for(int i = 0; i < (int)size/sizeof(struct file);i++){
        //fseek(ptr->directory_table,i*sizeof(struct file),SEEK_SET);
        fread(&temp, sizeof(struct file),1, ptr->directory_table);
        if(temp.name[0] == 0){//if there is nothing in the buffer, it means there is a place
            result = i*sizeof(struct file);
            return result;//return the position
        }


    }

    return -1;

}
//compare two ints, it is for sorting files based on offset

int compare_ints(const void *a, const void *b){//compare numbers

    struct file* a_x = (struct file*)a;
    struct file* b_x = (struct file*)b;
    int x = (int) a_x->offset;
    int y = (int) b_x->offset;
    int diff = x-y;
    if(diff<0){
        return -1;
    }
    else if(diff == 0){
        return 0;
    }
    else{
        return 1;
    }
}

//get the actuall size of the file_data
size_t get_ActualSize(data* ptr){


    //list of info for the files within the directory table
    fseek(ptr->directory_table,0,SEEK_END);
    size_t size = ftell(ptr->directory_table);
    fseek(ptr->directory_table,0,SEEK_SET);
    size_t size_file = 0;
    struct file temp;//check the size of directory table


    if(size == 0){// if the size is 0, the offset must be 0
        return 0;
    }
    for(int i = 0; i< (int)(size/sizeof(struct file));i++){//put the structs into the list
        //loop through the directory and sum up all the offsets
        fseek(ptr->directory_table,i*sizeof(struct file),SEEK_SET);
        fread(&temp, sizeof(struct file),1,ptr->directory_table);
        if(temp.name[0] != '\0'){
            
            size_file+= temp.length;
        }

    }


    return size_file;
}

//given a file name return the closest right neighbour of the file from file_data
int find_neighbour(char *filename, data* ptr){


    struct file list[count_files(ptr)];

    //get the size of directory table
    fseek(ptr->directory_table,0,SEEK_END);
    int size = (int)ftell(ptr->directory_table)/sizeof(struct file);
    fseek(ptr->directory_table,0,SEEK_SET);

    struct file temp;
    int j = 0;
    for(int i = 0; i < size;i++){

        //store the files (72 bytes) in an array
        fseek(ptr->directory_table,i*sizeof(struct file),SEEK_SET);
        fread(&temp, sizeof(struct file),1, ptr->directory_table);
        if(temp.name[0]!='\0'){
            list[j] = temp;
            j++;
        }
    }

    //sort the files based on offset
    qsort(list,sizeof(list)/sizeof(struct file),sizeof(struct file), compare_ints);
    

    for(int i = 0;i < count_files(ptr);i++){
       
        //find the neighbour of our file
        if(strncmp(list[i].name,filename,64)==0){
            
            if(i < count_files(ptr)-1){
                
                return list[i+1].offset;
            }
            if(i ==count_files(ptr)-1){
                

                return list[i].offset;
            }
        }
    }
    
    
    return 0;
}



//verify the hash content for read_file function 
int verification(int block_offset,data* ptr){


    fseek(ptr->file_data, 0,SEEK_END);
    int leaf = (int) (ftell(ptr->file_data)/256);
    int nodes = log(leaf)/log(2);
    //store the hash tree format we will compute from the file_data
    uint8_t result[(int) (pow(2,nodes+1)-1)][16];
    //store the value of hash_data file
    uint8_t hash[(int) (pow(2,nodes+1)-1)][16];

    int check_block = (int) (pow(2,nodes+1)-1) -(leaf-block_offset);

    fseek(ptr->hash_data,0,SEEK_SET);
    fread(hash,sizeof(hash),1,ptr->hash_data);

    int idx = (int) (pow(2,nodes+1)-1)-1;
    int temp_bocks = leaf;
    //we will compute the hash tree here from file_data
    while(idx >= 0){
        uint8_t buff[256];
        uint8_t block[16];

        if(idx+1 >= leaf){
            
            fseek(ptr->file_data,((idx+1)-leaf)*256,SEEK_SET);
            fread(buff,sizeof(buff),sizeof(char),ptr->file_data);
            fletcher(buff,256,block);
            memcpy(&result[idx],block,sizeof(block));
        }

        if(idx+1 < leaf){
            uint8_t buffer[32];
            if(idx == 0){
                
                memcpy(buffer,result[1],16);
                memcpy(buffer+16,result[2],16);
                fletcher(buffer,32,block);
                memcpy(&result[0],block,16);
            }

            else{
                memcpy(buffer,result[(int)(idx+temp_bocks-1)],16);
                memcpy(buffer+16,result[(int)(idx+temp_bocks)],16);
                fletcher(buffer,32,block);
                memcpy(&result[idx],block,16);
                temp_bocks --;

            }

        }


        idx--;
        
    }
    //check the blocks
    while(check_block >= 0){

        if(memcmp(result[check_block],hash[check_block],sizeof(char)*16)!=0){
            return 3;
        }
        if(check_block%2==1){
            check_block = (check_block+1-2)/2;
        }
        else{
            check_block = (check_block-2)/2;
        }

    }
    


    return 0;
}

//find the smallest offset to put the content of the data into the file_data file
int file_data_offset(data* ptr, int num_files, size_t length){

    int result =0;
    

    if(length ==0){
        return result;
    }
    if(get_ActualSize(ptr) == 0){// if the size is 0, the offset must be 0
        return 0;
    }
    if(get_ActualSize(ptr)+length > ptr->MAX_FILE_DATA){
        return -1;
    }

    //list of info for the files within the directory table
    struct file list[num_files];

    fseek(ptr->directory_table,0,SEEK_END);
    size_t size = ftell(ptr->directory_table);//get size of the file
    fseek(ptr->directory_table,0,SEEK_SET);
    struct file temp;

    
    int idx =0;
    for(int i = 0; i< size/sizeof(struct file);i++){//put the structs into the list

        fseek(ptr->directory_table,i*sizeof(struct file),SEEK_SET);
        fread(&temp, sizeof(struct file),1,ptr->directory_table);
        if(temp.name[0] != '\0'){
            list[idx] = temp;
            idx++;
        }

    }
    //sort them based on offset
    qsort(list,sizeof(list)/sizeof(struct file),sizeof(struct file), compare_ints);//sort them increasingly, compare_ints function is on the top



    //check if there is a slot between the files in the file_data file
    for(int i = 0; i < num_files-1;i++){
        
        if(i== 0){
            if(list[i].offset >= length){
                result = 0;
                return result;
            }
        }
        if(list[i+1].offset-(list[i].offset+list[i].length)>= length){
            result = list[i].offset+list[i].length;
            return result;
        }
    }
    //if there is no slot between files
    if(num_files >0){
        //check if there is place in the end
        if(list[num_files-1].offset+list[num_files-1].length+length <= ptr->MAX_FILE_DATA){
            result = list[num_files-1].offset+list[num_files-1].length;
            return result;
        }
        else{
            //if there is no place, we repack
            repack((void*)ptr);

            //find the smallest offset in file_data again. We just run the function from the beginning again and return the new value
             result = file_data_offset(ptr,num_files,length);
            return result;
        }
        
    }
    


    return result;
}


char* get_files(void* helper){

    data* ptr = (data*) helper;

    fseek(ptr->directory_table,0,SEEK_END);
    size_t size = ftell(ptr->directory_table);
    fseek(ptr->directory_table,0,SEEK_SET);
    char buffer[64];
    char* result = malloc(sizeof(char)*64*count_files(ptr));

    int j = 0;
    for(int i = 0; i < size/sizeof(struct file);i++){
        fseek(ptr->directory_table,i*sizeof(struct file), SEEK_SET);
        fread(&buffer,sizeof(buffer),1,ptr->directory_table);
        if(buffer[0] != '\0'){
            strncpy(result+j*64,buffer,64);
            j++;
        }
    }


    return result;
}

//count number of files
int count_files(data* ptr){

    int result = 0;

    fseek(ptr->directory_table,0,SEEK_END);
    size_t size = ftell(ptr->directory_table);
    fseek(ptr->directory_table,0,SEEK_SET);
    char buffer;

    for(int i = 0; i < size/sizeof(struct file);i++){
        fseek(ptr->directory_table,i*sizeof(struct file), SEEK_SET);
        fread(&buffer,sizeof(char),1,ptr->directory_table);
        if(buffer != '\0'){
            result++;
        }
    }


    return result;
}

//see if the file already exist or not
int duplicate(char* filename, data* ptr){

    int result = 1;

    if(filename == NULL){
        return 1;
    }

    fseek(ptr->directory_table,0,SEEK_END);
    size_t size = ftell(ptr->directory_table);
    fseek(ptr->directory_table,0,SEEK_SET);
    struct file temp;//get directory table size


    //loop through the file names
    for(int i = 0; i < size/sizeof(struct file);i++){
        fseek(ptr->directory_table,i*sizeof(struct file), SEEK_SET);
        fread(&temp,sizeof(struct file),1,ptr->directory_table);
        if(strncmp(temp.name, filename,64)==0){
            //if exists return its position
            result= i*sizeof(struct file);
            return result;
        }
    }

    return result;
}





void * init_fs(char * f1, char * f2, char * f3, int n_processors) {
    data* new = (data*) malloc(sizeof(data));
    
    
    new-> file_data = fopen(f1,"rb+");
    new-> directory_table = fopen(f2,"rb+");
    new-> hash_data = fopen(f3,"rb+");
    new-> n_processors = n_processors;


    if(new->file_data != NULL){
        fseek(new->file_data,0,SEEK_END);
        new-> MAX_FILE_DATA = ftell(new->file_data);
        fseek(new->file_data,0,SEEK_SET);
    }
    else{
        new->MAX_FILE_DATA = 0;
    }
    
    pthread_mutex_init(&write_lock,NULL);
    for(int i=0; i < 9;i++){
        pthread_mutex_init(&lock[i],NULL);
    }

    return (void*)new;
}

void close_fs(void * helper) {
    if(helper != NULL){
        data* ptr = (data*) helper;
        if(ptr->file_data != NULL){
            fclose(ptr->file_data);
        }
        if(ptr->directory_table != NULL){
            fclose(ptr->directory_table);
        }
        if(ptr->hash_data != NULL){
            fclose(ptr->hash_data);
        }
        
        
        ptr->file_data = NULL;
        ptr->directory_table = NULL;
        ptr-> hash_data = NULL;
        ptr->n_processors= 0;

        free(helper);
        helper = NULL;

   }




    return;
}

int create_file(char * filename, size_t length, void * helper) {
    pthread_mutex_lock(&lock[0]);

    data* ptr = (data*) helper;//change it to struct data
    int num_files = count_files(ptr);//number of files
    
    if(num_files > 0){
        //if file already exists
        if(duplicate(filename,ptr)!=1){
            pthread_mutex_unlock(&lock[0]);
            return 1;
        }
    }
    //if number of files exceed the limit
    if(num_files == MAX_DIRECTORY_TABLE){
        pthread_mutex_unlock(&lock[0]);
        return 2;
    }

    //smallest offset in directory table
    int smallest_offset = find_smallestoffset(ptr);
    
    //smallest offset in file_data
    int offset_filed = file_data_offset(ptr,num_files,length);
    //if there is no space in file_data
    if(offset_filed  == -1){
        pthread_mutex_unlock(&lock[0]);
        return 2;
    }

    struct file new_file;
    
    strncpy(new_file.name,filename,64);
    
    new_file.offset = offset_filed;
    new_file.length = length;

    //if the length is 0 we just put the file in the directory file
    if(length == 0){
        new_file.offset = 0;
        fseek(ptr->directory_table,smallest_offset,SEEK_SET);
        fwrite(&new_file,sizeof(struct file),1, ptr->directory_table);
    }
    else{
        //move the cursor of the directory table to the smallest offset
        fseek(ptr->directory_table,smallest_offset,SEEK_SET);
        fwrite(&new_file,sizeof(struct file),1, ptr->directory_table);
        //write zeros in the file data at the correct offset
        void* zeros = calloc(sizeof(char)*length,sizeof(char));
        fseek(ptr->file_data,new_file.offset,SEEK_SET);
        fwrite(zeros, sizeof(char),sizeof(char)*length,ptr->file_data);
        free(zeros);
        zeros = NULL;

    }

    //compute the hash block. We loop twice if the content covers at least two blocks
    //necessary for correct computation
    int hash_pos = new_file.offset/256;
    int hash_length = (new_file.offset+new_file.length)/256;

    for(int i = hash_pos; i <= hash_length;i++){
        compute_hash_block(i,helper);
    }
    if(hash_length > hash_pos){
        for(int i = hash_pos; i <= hash_length;i++){
            compute_hash_block(i,helper);
        }
    }
    

    fflush(ptr->file_data);   
    fflush(ptr->directory_table);
    fflush(ptr->hash_data);
    pthread_mutex_unlock(&lock[0]);

    return 0;
}

int resize_file(char * filename, size_t length, void * helper) {
    pthread_mutex_lock(&lock[1]);
    

    data* ptr = (data*) helper;
    //if the file does not exists
    if(filename ==0 || duplicate(filename,ptr)==1){
        pthread_mutex_unlock(&lock[1]);
        return 1;
    }

    struct file temp;

    fseek(ptr->directory_table,duplicate(filename,ptr),SEEK_SET);
    fread(&temp, sizeof(struct file),sizeof(char),ptr->directory_table);

    //if there is no space in either directory table or file data
    if(get_ActualSize(ptr)+length-temp.length > ptr->MAX_FILE_DATA || count_files(ptr)==MAX_DIRECTORY_TABLE){
        pthread_mutex_unlock(&lock[1]);
        return 2;
    }



    //if the new length is the same as the old
    if(temp.length == length){
        pthread_mutex_unlock(&lock[1]);
        return 0;
    }
    //if we need to chunk the file size
    if(temp.length > length){

        temp.length = length;
        //set the new size in the directory table
        fseek(ptr->directory_table,duplicate(filename,ptr),SEEK_SET);
        fwrite(&temp,sizeof(struct file),sizeof(char),ptr->directory_table);

        //compute hash block
        int hash_pos = temp.offset/256;
        int hash_length = (temp.offset+temp.length)/256;

        for(int i = hash_pos; i <= hash_length;i++){
            compute_hash_block(i,helper);
        }
        if(hash_length > hash_pos){
            for(int i = hash_pos; i <= hash_length;i++){
                compute_hash_block(i,helper);
            }
        }
        

        fflush(ptr->file_data);   
        fflush(ptr->directory_table);
        fflush(ptr->hash_data);
        pthread_mutex_unlock(&lock[1]);
        return 0;        

    }

    //check the offset of the right neighbour of the resized file
    int neighbour = find_neighbour(filename,ptr);
    //if there is enough space between the file and its neighbour
    if(neighbour-temp.offset >= length){

        temp.length= length;
        //write new length into the directory table
        fseek(ptr->directory_table,duplicate(filename,ptr),SEEK_SET);
        fwrite(&temp, sizeof(struct file),1,ptr->directory_table);

        //compute hash
        int hash_pos = temp.offset/256;
        int hash_length = (temp.offset+temp.length)/256;

        for(int i = hash_pos; i <= hash_length;i++){
            compute_hash_block(i,helper);
        }
        if(hash_pos < hash_length){
            for(int i = hash_pos; i <= hash_length;i++){
                compute_hash_block(i,helper);
            }
        }
        
        
        fflush(ptr->file_data);   
        fflush(ptr->directory_table);
        fflush(ptr->hash_data);
        pthread_mutex_unlock(&lock[1]);
        return 0;

    }
    //if there is no space and we have to repack

    // read the content of the file
    void* buffer = calloc(sizeof(char)*length,1);
    fseek(ptr->file_data,temp.offset,SEEK_SET);
    fread(buffer,sizeof(char)*temp.length,sizeof(char),ptr->file_data);

    //store the original position of the file from the directory table
    int dir_pos = duplicate(filename,ptr);
    //delete the file from the directory table temporarily
    delete_file(filename,ptr);
    //repack
    repack(helper);
    //write the content of the file to its new place
    temp.length = length;
    temp.offset = file_data_offset(ptr,count_files(ptr),length);

    fseek(ptr->file_data,temp.offset,SEEK_SET);
    fwrite(buffer,sizeof(char)*length,1,ptr->file_data);

    //write the filename into directory table. We put it to its original place
    fseek(ptr->directory_table,dir_pos,SEEK_SET);
    fwrite(&temp,sizeof(struct file),1,ptr->directory_table);
    free(buffer);
    
    //compute hash
    int hash_pos = temp.offset/256;
    int hash_length = (temp.offset+temp.length)/256;

    for(int i = hash_pos; i <= hash_length;i++){
        compute_hash_block(i,helper);
    }
    if(hash_pos < hash_length){
        for(int i = hash_pos; i <= hash_length;i++){
            compute_hash_block(i,helper);
        }
    }
    

    fflush(ptr->file_data);   
    fflush(ptr->directory_table);
    fflush(ptr->hash_data);
    pthread_mutex_unlock(&lock[1]);
    return 0;
}

void repack(void * helper) {
    
    pthread_mutex_lock(&lock[2]);
    data* ptr = (data*) helper;

    if(count_files(ptr)>=1){
        //store the files into an array
        struct file list[count_files(ptr)];

        fseek(ptr->directory_table,0,SEEK_END);
        int size = (int)ftell(ptr->directory_table)/sizeof(struct file);
        fseek(ptr->directory_table,0,SEEK_SET);

        struct file temp;
        int j = 0;
        for(int i = 0; i < size;i++){
            fseek(ptr->directory_table,i*sizeof(struct file),SEEK_SET);
            fread(&temp, sizeof(struct file),1, ptr->directory_table);
            if(temp.name[0]!='\0'){
                list[j] = temp;
                j++;
            }
        }

        //sort the array
        qsort(list,sizeof(list)/sizeof(struct file),sizeof(struct file), compare_ints);

        
        for(int i =0; i < count_files(ptr);i++){
            
            if(i == 0){
                //we set the first file to offset 0
                void* buff = calloc(sizeof(char)*list[i].length,1);
                fseek(ptr->file_data,list[i].offset,SEEK_SET);//go to the offset in file_data
                //read the content into buff
                fread(buff, sizeof(char)*list[i].length,sizeof(char),ptr->file_data);
                
                
                list[i].offset = 0;
                
                fseek(ptr->file_data,0,SEEK_SET);
                fwrite(buff,sizeof(char)*list[i].length,sizeof(char),ptr->file_data);
                free(buff);
                buff = NULL;
                fseek(ptr->directory_table,duplicate(list[i].name,ptr),SEEK_SET);
                fwrite(&list[i],sizeof(struct file),sizeof(char),ptr->directory_table);
                
            }
            else{

                //if the file is not the first file, we just refer to the length+offset of the previous file as the new offset 
                void* buff = calloc(sizeof(char)*list[i].length,sizeof(char));
                fseek(ptr->file_data,list[i].offset,SEEK_SET);
                fread(buff, sizeof(char)*list[i].length,sizeof(char),ptr->file_data);
                
                //replace the original place with zeros
                fseek(ptr->file_data,list[i].offset,SEEK_SET);
                void* zeros = calloc(sizeof(char),sizeof(char)*list[i].length);
                fwrite(zeros, sizeof(char)*list[i].length,sizeof(char),ptr->file_data);
                free(zeros);
                zeros = NULL;
                //new offset
                list[i].offset = list[i-1].offset+list[i-1].length;
                //write the cotnent into the new offset
                fseek(ptr->file_data,list[i].offset,SEEK_SET);
                fwrite(buff,sizeof(char)*list[i].length,sizeof(char),ptr->file_data);
                free(buff);
                buff=NULL;
                fseek(ptr->directory_table,duplicate(list[i].name,ptr),SEEK_SET);
                fwrite(&list[i],sizeof(struct file),sizeof(char),ptr->directory_table);


            }
            

        }
        //compute the hash tree
        compute_hash_tree(helper);
        

    }

    fflush(ptr->file_data);   
    fflush(ptr->directory_table);
    fflush(ptr->hash_data);
    pthread_mutex_unlock(&lock[2]);

    return;
}

int delete_file(char * filename, void * helper) {
    pthread_mutex_lock(&lock[3]);
    if(filename[0]=='\0'){
        pthread_mutex_unlock(&lock[3]);
        return 1;
    }

    if(helper != NULL){
        data* ptr = (data*) helper;
        if(duplicate(filename,ptr)!=1){//if the file exist
            //we replace the filename with zeros
            fseek(ptr->directory_table,duplicate(filename,ptr),SEEK_SET);
            void* zeros = calloc(sizeof(char)*sizeof(struct file),sizeof(char));
            fwrite(zeros, sizeof(char),sizeof(char)*sizeof(struct file),ptr->directory_table);
            free(zeros);
            zeros = NULL;
            fflush(ptr->file_data);   
            fflush(ptr->directory_table);
            fflush(ptr->hash_data);
            pthread_mutex_unlock(&lock[3]);
            return 0;     
            
        }

    }

    pthread_mutex_unlock(&lock[3]);

    return 1;
}

int rename_file(char * oldname, char * newname, void * helper) {
    pthread_mutex_lock(&lock[4]);
    if(oldname == NULL || oldname[0] =='\0'|| newname==NULL || newname[0]=='\0'){
        pthread_mutex_unlock(&lock[4]);
        return 1;

    }

    if(helper != NULL){
        data* ptr = (data*) helper;
        //if the file exists and the new name does not exist in the directory table
        if(duplicate(oldname,ptr)!=1 && duplicate(newname,ptr)==1){
            struct file temp;
            fseek(ptr->directory_table,duplicate(oldname,ptr), SEEK_SET);
            fread(&temp,sizeof(struct file),1,ptr->directory_table);
            strncpy(temp.name,newname,64);
            fseek(ptr->directory_table,duplicate(oldname,ptr), SEEK_SET);
            fwrite(&temp,sizeof(struct file),sizeof(char),ptr->directory_table);
            
            fflush(ptr->file_data);   
            fflush(ptr->directory_table);
            fflush(ptr->hash_data);
            pthread_mutex_unlock(&lock[4]);
            return 0;       
            
        }
    }

    pthread_mutex_unlock(&lock[4]);
    return 1;
}

int read_file(char * filename, size_t offset, size_t count, void * buf, void * helper) {
    pthread_mutex_lock(&lock[5]);
    if(filename == NULL || count <= 0 || helper ==NULL || buf == NULL){
        pthread_mutex_unlock(&lock[5]);
        return 1;
    }

    data* ptr = (data*) helper;
    struct file temp;

    //check if the file exists
    if(duplicate(filename, helper)==1){
        pthread_mutex_unlock(&lock[5]);
        return 1;
    }

    fseek(ptr->directory_table,duplicate(filename,ptr), SEEK_SET);
    fread(&temp, sizeof(struct file),sizeof(char),ptr->directory_table);
    //see if we can read the content, if it is within the boundaries
    if((count+ offset)> temp.length){
        pthread_mutex_unlock(&lock[5]);
        return 2;
    }
    //verify the hash content
    if(verification(temp.offset/256,ptr)==3){
        pthread_mutex_unlock(&lock[5]);
        return 3;
    }
    //verify the hash blocks if the readable file covers more than 1 blocks
    if((int)(temp.offset+temp.length)/256 >(int) temp.offset/256){
        for(int i = temp.offset/256+1; i <=(int)(temp.offset+temp.length)/256;i++){
            if(verification(temp.offset+i,ptr)==3){
                pthread_mutex_unlock(&lock[5]);
                return 3;
            }
        }
    }


    //otherwise we just read the content
    if(offset+count < temp.length){
        fseek(ptr->file_data,offset+temp.offset,SEEK_SET);
        fread(buf,count,1,ptr->file_data);

    }


    pthread_mutex_unlock(&lock[5]);


    return 0;
}

int write_file(char * filename, size_t offset, size_t count, void * buf, void * helper) {
    
    //protect the process from parallel writing
    pthread_mutex_lock(&write_lock);    

    data* ptr = (data*) helper;
    //check if the file exists or not
    if(duplicate(filename,ptr)==1){
        pthread_mutex_unlock(&write_lock); 
        return 1;
    }

    fseek(ptr->directory_table,duplicate(filename,ptr),SEEK_SET);
    struct file temp;//get the file from the directory table
    fread(&temp, sizeof(struct file),sizeof(char),ptr->directory_table);
    fseek(ptr->directory_table,0,SEEK_SET);
    //check if the offset is correct
    if(offset > temp.length){
        pthread_mutex_unlock(&write_lock);
        return 2;
    }
    //check if the writing content exceed the length of the file
    if(offset+count > temp.length){
        //if exceed the length of the file, check if there is space
        if(get_ActualSize(ptr)-temp.length+offset+count > ptr->MAX_FILE_DATA){
            //if no space return 3
            pthread_mutex_unlock(&write_lock);
            return 3;
        }

        else{//resize if there is space. Note that 
            resize_file(filename,(count+offset),ptr);

        }
    }

    //write the content into the file data and and directory table 
    fseek(ptr->directory_table,duplicate(filename,ptr),SEEK_SET);
    fread(&temp,sizeof(struct file),sizeof(char),ptr->directory_table);

    fseek(ptr->file_data,temp.offset+offset,SEEK_SET);
    fwrite(buf,sizeof(char),sizeof(char)*count,ptr->file_data);


    //compute hash block
    int hash_pos = temp.offset/256;
    int hash_length = (temp.offset+temp.length)/256;

    for(int i = hash_pos; i <= hash_length;i++){
        compute_hash_block(i,helper);
    }
    if(hash_pos < hash_length){
        for(int i = hash_pos; i <= hash_length;i++){
            compute_hash_block(i,helper);
        }
    }
    


    

    fflush(ptr->file_data);   
    fflush(ptr->directory_table);
    fflush(ptr->hash_data);    
    pthread_mutex_unlock(&write_lock);
    return 0;
}

ssize_t file_size(char * filename, void * helper) {
    pthread_mutex_lock(&lock[7]);
    if(filename == NULL || helper ==NULL){
        pthread_mutex_unlock(&lock[7]);
        return -1;
    }

    data* ptr = (data*) helper;
    //if the file does note exist
    if(duplicate(filename,ptr)== 1){
        pthread_mutex_unlock(&lock[7]);
        return -1;

    }

    //return the file size

    
    struct file temp;
    fseek(ptr->directory_table,duplicate(filename,ptr), SEEK_SET);
    fread(&temp, sizeof(struct file), 1,ptr->directory_table);
    pthread_mutex_unlock(&lock[7]);
    return temp.length;
}

void fletcher(uint8_t * buf, size_t length, uint8_t * output) {

    uint64_t values[] = {0,0,0,0};
    uint32_t* temp = calloc(sizeof(uint32_t),1);

    //if the length is not accurate we complete it with paddings
    if(length % 4 != 0){
        for(int i = 0;i <= (length % 4);i++){
            *(buf+i) = '\0';
        }
    }
    length = length+ (length % 4);
    //compute the numbers
    for(int i = 0; i < length/4;i++){
        memcpy(temp, buf+(i*4),4);
        values[0] = (values[0]+ *temp) % (uint64_t) (pow(2,32)-1);
        values[1] = (values[1]+ values[0]) % (uint64_t) (pow(2,32)-1);
        values[2] = (values[2]+ values[1]) % (uint64_t) (pow(2,32)-1);
        values[3] = (values[3]+ values[2]) % (uint64_t) (pow(2,32)-1);

    }
    free(temp);
    temp = NULL; 

    //convert them into uint32_t
    uint32_t a = (uint32_t) values[0];
    uint32_t b = (uint32_t) values[1];
    uint32_t c = (uint32_t) values[2];
    uint32_t d = (uint32_t) values[3];

    memcpy(output,&a,sizeof(a));
    memcpy(output+4,&b,sizeof(b));
    memcpy(output+8,&c,sizeof(c));
    memcpy(output+12,&d,sizeof(d));

    return;
}

void compute_hash_tree(void * helper) {

    pthread_mutex_lock(&lock[6]);
    data* ptr = helper;
    fseek(ptr->file_data, 0,SEEK_END);
    //number of leafs
    int leaf = (int) (ftell(ptr->file_data)/256);
    //number of nodes
    int nodes = log(leaf)/log(2);
    if(nodes==0){
        pthread_mutex_unlock(&lock[6]);
        return;
    }
    //the array we write into the hash_data file
    uint8_t result[(int) (pow(2,nodes+1)-1)][16];

    int idx = (int) (pow(2,nodes+1)-1)-1;//start from the end of the array
    int temp_bocks = leaf;

    while(idx >= 0){
        uint8_t buff[256];
        uint8_t block[16];

        if(idx+1 >= leaf){//if we compute leaf
            
            fseek(ptr->file_data,((idx+1)-leaf)*256,SEEK_SET);
            fread(buff,sizeof(buff),sizeof(char),ptr->file_data);
            fletcher(buff,256,block);
            memcpy(&result[idx],block,sizeof(block));
        }

        if(idx+1 < leaf){//if we compute internal nodes
            uint8_t buffer[32];
            if(idx == 0){
                
                memcpy(buffer,result[1],16);
                memcpy(buffer+16,result[2],16);
                fletcher(buffer,32,block);
                memcpy(&result[0],block,16);
            }

            else{
                memcpy(buffer,result[(int)(idx+temp_bocks-1)],16);
                memcpy(buffer+16,result[(int)(idx+temp_bocks)],16);
                fletcher(buffer,32,block);
                memcpy(&result[idx],block,16);
                temp_bocks --;

            }

        }


        idx--;
        
    }
    fseek(ptr->hash_data,0,SEEK_SET);
    fwrite(&result,sizeof(result),sizeof(char),ptr->hash_data);
    fflush(ptr->file_data);   
    fflush(ptr->hash_data);
    pthread_mutex_unlock(&lock[6]);

    return;
}

void compute_hash_block(size_t block_offset, void * helper) {
    pthread_mutex_lock(&lock[8]);
    if(helper == NULL){
        pthread_mutex_unlock(&lock[8]);
        return;
    }

    data* ptr = (data*) helper;
    //number of leaf
    int leaf = (ptr->MAX_FILE_DATA)/256;

    if(leaf <= block_offset || block_offset < 0){
        pthread_mutex_unlock(&lock[8]);
        return;
    }

    uint8_t buff[256];
    fseek(ptr->file_data,block_offset*256,SEEK_SET);//read the block from the file data
    fread(&buff,sizeof(buff),1,ptr->file_data);
    //level of tree without rooot
    int level = log(leaf)/log(2);

    int num_nodes = (int) (pow(2,level+1)-1);//number of nodes

    int position = num_nodes-(leaf-block_offset);//position of the block we modify in the hash tree


    uint8_t result[num_nodes][16];
    fseek(ptr->hash_data,0,SEEK_SET);//read the whole hash tree
    fread(result,sizeof(result),1,ptr->hash_data);
    uint8_t new_block[16];
    uint8_t temp_block[32];

    fletcher(buff,256,new_block);//set the new value of leaf into the array
    memcpy(&result[position],new_block,sizeof(result[position]));
   
    int position2 = 0;

    //we gonna be tricky here. Every right child of an internal node can be computed from its parent.
    //if child array position is 14, then its parent is (14-2)/2 = 6 idx in the array.
    //left child is always on the odd position in the array, while right child is always on the even position.

    if(position % 2==0){//ensure that position is even and position2 is odd
        position2 = position-1;
    }
    else{
        position2 = position;
        position = position+1;
    }

    int idx = (position-2)/2;
    
    

    while(idx >=0){

        memcpy(temp_block,result[position2],16);
        memcpy(temp_block+16,result[position],16);

        fletcher(temp_block,32,new_block);
        memcpy(&result[idx],new_block,16);
        
        
        position = (position-2)/2;
        if(position % 2==0){
            position2 = position-1;
        }
        else{
            position2 = position;
            position = position+1;
        }

        //printf("new position %d\n",position);
        //printf("new position2 %d\n",position2);


        idx = (position-2)/2;
    }
    

    fseek(ptr->hash_data,0,SEEK_SET);
    fwrite(&result,sizeof(result),1,ptr->hash_data);
   
    fflush(ptr->file_data);   
    fflush(ptr->directory_table);
    fflush(ptr->hash_data);
    pthread_mutex_unlock(&lock[8]);
    
    return;
}




