#include "myfilesystem.h"
#include <stdio.h>
#include<string.h>
#include<pthread.h>
#include <stdlib.h>
#include <math.h>
#define TEST(x) test(x, #x)
struct file{//storing the new file info
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
    size_t MAX_FILE_DATA;

}data;


/* You are free to modify any part of this file. The only requirement is that when it is run, all your tests are automatically executed */

/* Some example unit test functions */
/*since these are a very basic functions and we can always assume that
the given file names exist, we just check if they works;
*/
int test_init_fs_and_close(){
    FILE* file_data = fopen("file_data.bin","w");
    FILE* directory_table = fopen("directory_table.bin","w");
    FILE* hash_data = fopen("hash_data.bin","w");

    int i = 256*pow(2,3);

    void* zeros = calloc(sizeof(char)*i,sizeof(char));
    fwrite(zeros,sizeof(char)*i,1,file_data);

    free(zeros);
    zeros = NULL;
    

    fclose(file_data);
    fclose(directory_table);
    fclose(hash_data);

    void* new = init_fs("file_data.bin","directory_table.bin","hash_data.bin",4);
    //check no operation


    close_fs(new);

    if(!new){
        printf("Unsuccessful close\n");
        return 1;
    }


    return 0;
}


int test_create_file(){

    FILE* file_data = fopen("file_data.bin","w");
    FILE* directory_table = fopen("directory_table.bin","w");
    FILE* hash_data = fopen("hash_data.bin","w");
    //create file and set file_data to size 256
    int i = 256*pow(2,0);

    void* zeros = calloc(sizeof(char)*i,sizeof(char));
    fwrite(zeros,sizeof(char)*i,1,file_data);

    free(zeros);
    zeros = NULL;
    

    fclose(file_data);
    fclose(directory_table);
    fclose(hash_data);

    //write into the file system.
    void* new = init_fs("file_data.bin","directory_table.bin","hash_data.bin",4);

    create_file("asd.txt",30,new);//create first file
    create_file("dfg.jpg",40,new);//create second file
    data* ptr = (data*) new;
    fseek(ptr->directory_table,0,SEEK_SET);
    char buff[64];//use buffer to check the content of directory table
    int length = 0;

    fread(buff,sizeof(buff),1,ptr->directory_table);
    fseek(ptr->directory_table,68,SEEK_SET);//read the length and the name
    fread(&length,sizeof(int),1,ptr->directory_table);

    //check the name and its length
    if(strcmp(buff,"asd.txt")!=0 || length != 30){
        
        printf("Wrong values in directory table\n");
        return 1;
    }

    //do the same with second file
    fseek(ptr->directory_table,72,SEEK_SET);
    fread(buff,sizeof(buff),1,ptr->directory_table);
    fseek(ptr->directory_table,140,SEEK_SET);
    fread(&length,sizeof(int),1,ptr->directory_table);
    if(strcmp(buff,"dfg.jpg")!=0 || length != 40){
        
        printf("Wrong values in directory table\n");
        return 1;
    }

    //check if we will create a file that exceed the limit
    create_file("no_file.pdf",256,new);
    fseek(ptr->directory_table,144,SEEK_SET);
    fread(buff,sizeof(buff),1,ptr->directory_table);
    fseek(ptr->directory_table,208,SEEK_SET);
    fread(&length,sizeof(int),1,ptr->directory_table);
    //check if it was created
    if(strcmp(buff,"no_file.pdf")==0){
        
        printf("Wrong values in directory table\n");
        return 1;
    }
    //create this file to reach the limited content
    create_file("34.txt",180,new);
    //check if this file is created
    create_file("not_working.txt",10,new);

    fseek(ptr->directory_table,216,SEEK_SET);
    fread(buff,sizeof(buff),1,ptr->directory_table);

    
    if(strcmp(buff,"not_working.txt")==0){
        printf("Wrong values in directory table\n");
        return 1;
    }

    close_fs(ptr);

   

    return 0;

}


int test_resize_file(){

    FILE* file_data = fopen("file_data.bin","w");
    FILE* directory_table = fopen("directory_table.bin","w");
    FILE* hash_data = fopen("hash_data.bin","w");

    int i = 256*pow(2,0);
    

    void* zeros = calloc(sizeof(char)*i,sizeof(char));
    fwrite(zeros,sizeof(char)*i,1,file_data);

    free(zeros);
    zeros = NULL;


    fclose(file_data);
    fclose(directory_table);
    fclose(hash_data);

    void* new = init_fs("file_data.bin","directory_table.bin","hash_data.bin",4);
    create_file("asd.txt",30,new);
    create_file("dfg.jpg",40,new);
    data* ptr = (data*) new;
    //chunk file
    resize_file("asd.txt",3,new);

    //resize none existing file
    if(resize_file("dfg.jpg",256,new)!= 2){
        printf("Incorrect return value in file resize\n");
        return 1;
    }

    char buff[64];
    int num;

    fseek(ptr->directory_table,0,SEEK_SET);

    fread(buff,sizeof(buff),1,ptr->directory_table);
    fread(&num, sizeof(num),1,ptr->directory_table);

    //check the file offset
    if(strcmp(buff,"asd.txt")!= 0 && num != 0){
        printf("Incorrect first file resize\n");
        return 1;
    }
    //check if we chunked it or not
    fread(&num,sizeof(num),1,ptr->directory_table);
    if(num != 3){
        printf("Incorrect new file size\n");
        return 1;
    }
    //resize none existing file
    if(resize_file("fas.txt",4,new)!= 1){
        printf("Incorrect value\n");
        return 1;
    }

    close_fs(ptr);
    



    return 0;
}

//test if we return the correct file size
int test_file_size(){

    //just create the files
    FILE* file_data = fopen("file_data.bin","w");
    FILE* directory_table = fopen("directory_table.bin","w");
    FILE* hash_data = fopen("hash_data.bin","w");

    int i = 256*pow(2,0);
    

    void* zeros = calloc(sizeof(char)*i,sizeof(char));
    fwrite(zeros,sizeof(char)*i,1,file_data);

    free(zeros);
    zeros = NULL;


    fclose(file_data);
    fclose(directory_table);
    fclose(hash_data);

    void* new = init_fs("file_data.bin","directory_table.bin","hash_data.bin",4);
    create_file("asd.txt",30,new);//create files
    create_file("dfg.jpg",40,new);//create files

    data* ptr = (data*) new;

    if(file_size("asd.txt",new)!=30){
        printf("Wrong size\n");
        return 1;
    }
    //if the file doesn't exist
    if(file_size("as.txt",new)!=-1){
        printf("Wrong size\n");
        return 1;
    }

    close_fs(ptr);

    return 0;

}





int test_rename_file(){
    //create files in advanced
    FILE* file_data = fopen("file_data.bin","w");
    FILE* directory_table = fopen("directory_table.bin","w");
    FILE* hash_data = fopen("hash_data.bin","w");

    int i = 256*pow(2,0);
    

    void* zeros = calloc(sizeof(char)*i,sizeof(char));
    fwrite(zeros,sizeof(char)*i,1,file_data);

    free(zeros);
    zeros = NULL;


    fclose(file_data);
    fclose(directory_table);
    fclose(hash_data);


    void* new = init_fs("file_data.bin","directory_table.bin","hash_data.bin",4);
    data* ptr = (data*) new;
    create_file("asd.txt",30,new);//create file in the filesystem
    
    rename_file("asd.txt","newasd.txt",new);//rename file

    char buf[64];

    fseek(ptr->directory_table,0,SEEK_SET);

    fread(buf,sizeof(buf),1,ptr->directory_table);
    //check if we were able to rename the file
    if(strcmp(buf,"newasd.txt")!= 0){
        printf("Incorrect name of file\n");
        return 1;
    }
    //if file doesn't exists
    if(rename_file("adsfav","vdsf",new)!= 1){
        printf("Should not be able to rename file\n");
        return 1;

    }
    //see if we chunk the name if it is too long
    char name[] ="vadilhfuwhfjadsliabefjsiadfkjlknvsdjbvakjadsfajksdfnsklnvskjdnvsknvdb";
    rename_file("newasd.txt",name,new);
    char buf2[64];

    strncpy(buf2,name,sizeof(buf2));
    fseek(ptr->directory_table,0,SEEK_SET);
    fread(buf,sizeof(buf),1,ptr->directory_table);
    //compare the name
    if(strncmp(buf2,buf,64)!= 0){
        printf("Incorrect new file name\n");
        return 1;
    }


    close_fs(ptr);


    return 0;
}


int test_delete_file(){
    //create the files in advanced
    FILE* file_data = fopen("file_data.bin","w");
    FILE* directory_table = fopen("directory_table.bin","w");
    FILE* hash_data = fopen("hash_data.bin","w");

    int i = 256*pow(2,0);
    

    void* zeros = calloc(sizeof(char)*i,sizeof(char));
    fwrite(zeros,sizeof(char)*i,1,file_data);

    free(zeros);
    zeros = NULL;


    fclose(file_data);
    fclose(directory_table);
    fclose(hash_data);


    void* new = init_fs("file_data.bin","directory_table.bin","hash_data.bin",4);
    data* ptr = (data*) new;
    create_file("asd.txt",30,new);
    //delete none existing file
    if(delete_file("fsdf.pdf",new)!= 1){
        printf("Deleted none existing file\n");
        return 1;
    }

    delete_file("asd.txt",new);//delete the file

    fseek(ptr->directory_table,0,SEEK_SET);
    char buff[64];
    int length;
    fread(buff,sizeof(buff),1,ptr->directory_table);
    fseek(ptr->directory_table,68,SEEK_SET);
    fread(&length,sizeof(length),1,ptr->directory_table);

    //check if it is deleted or not
    if(length == 30 && strcmp(buff,"asd.txt")==0){
        printf("Should have been deleted but no\n");
        return 1;
    }


    close_fs(ptr);

    return 0;
}


int test_write_file(){

    FILE* file_data = fopen("file_data.bin","w");
    FILE* directory_table = fopen("directory_table.bin","w");
    FILE* hash_data = fopen("hash_data.bin","w");

    int i = 256*pow(2,0);
    

    void* zeros = calloc(sizeof(char)*i,sizeof(char));
    fwrite(zeros,sizeof(char)*i,1,file_data);

    free(zeros);
    zeros = NULL;


    fclose(file_data);
    fclose(directory_table);
    fclose(hash_data);


    void* new = init_fs("file_data.bin","directory_table.bin","hash_data.bin",4);
    data* ptr = (data*) new;
    create_file("asd.txt",30,new);
    create_file("second.txt",50,new);
    //text we will write in
    char buf[] = "Hi my name is Bob. How are you?";
    write_file("asd.txt",10,15,&buf,new);
    char read[15];//read the content from file_data to this buffer
    fseek(ptr->file_data,10,SEEK_SET);
    fread(read,sizeof(read),1,ptr->file_data);

    if(strncmp(read,buf,15)!= 0){
        printf("Wrong content\n");
        return 1;
    }
    //if file doesn't exist
    if(write_file("asdf",10,15,&buf,new)!= 1){
        printf("Wrote into none existing file\n");
        return 1;
    }

    //if we want to write at an incorrect offset
    if(write_file("second.txt",51,14,&buf,new)!=2){
        printf("Wrote into wrong offset\n");
        return 1;   
    }
    //if the new length we write is too long
    if(write_file("second.txt",40,256,&buf,new)!= 3){
        printf("Wrote outside of bound\n");
        return 1;
    }
    
    close_fs(ptr);
    return 0;
}

int test_repack(){
    FILE* file_data = fopen("file_data.bin","w");
    FILE* directory_table = fopen("directory_table.bin","w");
    FILE* hash_data = fopen("hash_data.bin","w");

    int i = 256*pow(2,0);
    

    void* zeros = calloc(sizeof(char)*i,sizeof(char));
    fwrite(zeros,sizeof(char)*i,1,file_data);

    free(zeros);
    zeros = NULL;


    fclose(file_data);
    fclose(directory_table);
    fclose(hash_data);


    void* new = init_fs("file_data.bin","directory_table.bin","hash_data.bin",4);
    
    create_file("asd.txt",30,new);
    create_file("second.txt",50,new);
    create_file("third.png",43,new);
    create_file("fourth.pdf",67,new);

    delete_file("asd.txt",new);//delete the first and 3rd files then repack
    delete_file("third.png",new);
    repack(new);


    close_fs(new);

    directory_table = fopen("directory_table.bin","r");
    struct file temp;

    fseek(directory_table,72, SEEK_SET);
    fread(&temp,sizeof(struct file),1,directory_table);

    //check the first file
    if(temp.offset != 0 || temp.length != 50 || strncmp(temp.name,"second.txt",64)!= 0){
        printf("Incorrect repack\n");
        return 1;
    }

    fseek(directory_table,3*sizeof(struct file),SEEK_SET);
    fread(&temp,sizeof(struct file),sizeof(char),directory_table);
    //check the second file
    if(temp.offset != 50 || temp.length != 67 || strcmp(temp.name,"fourth.pdf")!= 0){
        printf("Incorrect repack\n");
        return 1;
    }

    return 0;
}


int test_read_file(){

    FILE* file_data = fopen("file_data.bin","w");
    FILE* directory_table = fopen("directory_table.bin","w");
    FILE* hash_data = fopen("hash_data.bin","w");

    int i = 256*pow(2,0);
    

    void* zeros = calloc(sizeof(char)*i,sizeof(char));
    fwrite(zeros,sizeof(char)*i,1,file_data);

    free(zeros);
    zeros = NULL;


    fclose(file_data);
    fclose(directory_table);
    fclose(hash_data);


    void* new = init_fs("file_data.bin","directory_table.bin","hash_data.bin",4);
    
    create_file("asd.txt",30,new);
    create_file("second.txt",50,new);
    create_file("third.png",43,new);
    create_file("fourth.pdf",67,new);

    //this is the content we want to receive
    char write[] = "Hello, my name is Josh";
    //since our write_file is tested we could use that
    write_file("asd.txt",5,sizeof(write),write,new);

    char buf[64];
    //read the content from that file
    read_file("asd.txt",5,sizeof(write),buf,new);

    //do we get the content?
    if(strcmp(buf,write)!= 0){
        printf("Incorrect content read\n");
        return 1;
    }

    //read none existing file
    if(read_file("asvdfg",5,sizeof(char)*3,buf,new)!= 1){
        printf("Read none existing file\n");
        return 1;
    }
    //read from incorrect offset
    if(read_file("second.txt",45,12,buf,new)!= 2){
        printf("Read incorrect offset\n");
        return 1;
    }


    close_fs(new);

    return 0;
}


int test_content(){

    FILE* file_data = fopen("file_data.bin","w");
    FILE* directory_table = fopen("directory_table.bin","w");
    FILE* hash_data = fopen("hash_data.bin","w");

    //this is the content we should get after doing our combo
    FILE* test_fd = fopen("test_fd.bin","w");
    FILE* test_dt = fopen("test_dt.bin","w");

    struct file temp;
    strncpy(temp.name,"asd.txt",64);
    temp.offset = 40;
    temp.length = 45;

    //this is just setting up the starting scenario of teh files

    int i = 256*pow(2,0);
    

    void* zeros = calloc(sizeof(char)*i,sizeof(char));
    fwrite(zeros,sizeof(char)*i,1,file_data);
    fwrite(zeros,sizeof(char)*i,1,test_fd);

    free(zeros);

    fseek(directory_table,72,SEEK_SET);    
    fwrite(&temp,sizeof(struct file),1,directory_table);
    fseek(test_dt,72,SEEK_SET);    
    fwrite(&temp,sizeof(struct file),1,test_dt);

    strncpy(temp.name,"second.pdf",64);
    temp.offset = 4;
    temp.length= 15;
    //this file will be already in both files
    fseek(directory_table,144,SEEK_SET);    
    fwrite(&temp,sizeof(struct file),1,directory_table);
    fseek(test_dt,144,SEEK_SET);    
    fwrite(&temp,sizeof(struct file),1,test_dt);

    //this is only in the after file
    strncpy(temp.name,"third.txt",64);
    temp.offset = 19;
    temp.length = 15;

    fseek(test_dt,0,SEEK_SET);    
    fwrite(&temp,sizeof(struct file),1,test_dt);

    //this is also just in the after file
    char hello[] ="Hello";
    fseek(test_fd,19,SEEK_SET);
    fwrite(&hello,sizeof(char),sizeof(hello),test_fd);


    fflush(file_data);
    fflush(directory_table);
    fclose(file_data);
    fclose(directory_table);
    fclose(hash_data);

    fflush(test_dt);
    fflush(test_fd);
    fclose(test_fd);
    fclose(test_dt);


    void* new = init_fs("file_data.bin","directory_table.bin","hash_data.bin",4);

    if(create_file("asd.txt",64,new)!= 1){
        printf("Created file that already exists\n");
        return 1;
    }

    create_file("third.txt",15,new);//Create the file

    //write into the file
    write_file("third.txt",0,sizeof(hello),hello,new);


    close_fs(new);

    file_data = fopen("file_data.bin","r");
    directory_table = fopen("directory_table.bin","r");
    test_fd = fopen("test_fd.bin","r");
    test_dt = fopen("test_dt.bin","r");

    void* fd = malloc(sizeof(char)*i);
    void* dt = malloc(sizeof(char)*72*3);

    void* t_fd = malloc(sizeof(char)*i);
    void* t_dt = malloc(sizeof(char)*72*3);

    fseek(test_dt,0,SEEK_SET);
    fseek(test_fd,0,SEEK_SET);
    fseek(file_data,0,SEEK_SET);
    fseek(directory_table,0,SEEK_SET);


    fread(fd,sizeof(char)*i,1,file_data);
    fread(t_fd,sizeof(char)*i,1,test_fd);
    fread(dt,sizeof(char)*72*3,1,directory_table);
    fread(t_dt,sizeof(char)*72*3,1,test_dt);
    //compare the content of the files



    if(memcmp(fd,t_fd,i) != 0){
        printf("Incorrect file data content\n");
        fclose(file_data);
	    fclose(directory_table);
	    fclose(test_fd);
	    fclose(test_dt);
        return 1;
    }
    if(memcmp(dt,t_dt,72*3) !=0){
        printf("Incorrect directory table content\n");
        fclose(file_data);
	    fclose(directory_table);
	    fclose(test_fd);
	    fclose(test_dt);
        return 1;
    }
    fclose(file_data);
    fclose(directory_table);
    fclose(test_fd);
    fclose(test_dt);

    free(fd);
    free(dt);
    free(t_dt);
    free(t_fd);

    return 0;
}



int test_repack_resize(){


    FILE* file_data = fopen("file_data.bin","w");
    FILE* directory_table = fopen("directory_table.bin","w");
    FILE* hash_data = fopen("hash_data.bin","w");

    //this is the file that has the correct content after doing certain combos.
    FILE* test_fd = fopen("test_fd.bin","w");
    FILE* test_dt = fopen("test_dt.bin","w");
    struct file temp;
    int i = 256*pow(2,0);
    void* zeros = calloc(sizeof(char)*i,sizeof(char));
    fwrite(zeros,sizeof(char)*i,1,file_data);
    fwrite(zeros,sizeof(char)*i,1,test_fd);
    free(zeros);
    //first file with content into the before file
    strncpy(temp.name,"first.txt",64);
    temp.offset= 0;
    temp.length = 20;
    fseek(directory_table,0,SEEK_SET);
    fwrite(&temp,sizeof(struct file),1,directory_table);
    fseek(file_data,0,SEEK_SET);
    fwrite("Im first",sizeof("Im first"),1,file_data);
    //second file into the before file with content
    strncpy(temp.name,"second.txt",64);
    temp.offset= 20;
    temp.length = 13;
    fseek(file_data,20,SEEK_SET);
    fwrite("Im second",sizeof("Im second"),1,file_data);
    fwrite(&temp,sizeof(struct file),1,directory_table);
    //third file into the before file
    strncpy(temp.name,"third.txt",64);
    temp.offset= 33;
    temp.length = 5;

    fwrite(&temp,sizeof(struct file),1,directory_table);
    //4th file into the before content but there is a gap between 3rd and 4th file
    strncpy(temp.name,"fourth.txt",64);
    temp.offset= 45;
    temp.length = 24;

    fwrite(&temp,sizeof(struct file),1,directory_table);

    
    //we will put the first file at the end of the file since we are going to resize it
    //give a larger size
    strncpy(temp.name,"first.txt",64);
    temp.offset= 47;
    temp.length = 35;

    fseek(test_dt,0,SEEK_SET);
    fwrite(&temp,sizeof(struct file),1,test_dt);
    //second file will be at the smallest offset
    strncpy(temp.name,"second.txt",64);
    temp.offset= 0;
    temp.length = 13;
    fwrite(&temp,sizeof(struct file),1,test_dt);
    //then third file
    strncpy(temp.name,"third.txt",64);
    temp.offset= 13;
    temp.length = 10;
    fwrite(&temp,sizeof(struct file),1,test_dt);
    //4th file should be right next to the 3rd file
    strncpy(temp.name,"fourth.txt",64);
    temp.offset= 23;
    temp.length = 24;
    fwrite(&temp,sizeof(struct file),1,test_dt);

    
    //write the content into the right places in the after file
    fseek(test_fd,0,SEEK_SET);
    fwrite("Im second",sizeof("Im second"),1,test_fd);
    fseek(test_fd,47,SEEK_SET);
    fwrite("Im first",sizeof("Im first"),1,test_fd);

    fflush(file_data);
    fflush(directory_table);
    fclose(file_data);
    fclose(directory_table);
    fclose(hash_data);

    fflush(test_dt);
    fflush(test_fd);
    fclose(test_fd);
    fclose(test_dt);

    void* new = init_fs("file_data.bin","directory_table.bin","hash_data.bin",4);
    data* ptr = (data*) new;
    resize_file("third.txt",10,new);//resize the file
    fseek(ptr->directory_table,72*2,SEEK_SET);
    fread(&temp,sizeof(struct file),1,ptr->directory_table);

    if(temp.length != 10 || temp.offset != 33){
        printf("Wrong length or offset\n");
        fclose(file_data);
	    fclose(directory_table);
	    fclose(test_fd);
	    fclose(test_dt);
        return 1;
    }

    resize_file("first.txt",35,new);//resize the file

    close_fs(new);

    file_data = fopen("file_data.bin","r");
    directory_table = fopen("directory_table.bin","r");
    test_fd = fopen("test_fd.bin","r");
    test_dt = fopen("test_dt.bin","r");

    void* fd = malloc(sizeof(char)*i);
    void* dt = malloc(sizeof(char)*72*3);

    void* t_fd = malloc(sizeof(char)*i);
    void* t_dt = malloc(sizeof(char)*72*3);

    //check the content
    fseek(test_dt,0,SEEK_SET);
    fseek(test_fd,0,SEEK_SET);
    fseek(file_data,0,SEEK_SET);
    fseek(directory_table,0,SEEK_SET);


    fread(fd,sizeof(char)*i,1,file_data);
    fread(t_fd,sizeof(char)*i,1,test_fd);
    fread(dt,sizeof(char)*72*3,1,directory_table);
    fread(t_dt,sizeof(char)*72*3,1,test_dt);


    fclose(file_data);
    fclose(directory_table);
    fclose(test_fd);
    fclose(test_dt);

    if(memcmp(fd,t_fd,i) != 0){
        printf("Incorrect file data content\n");
        fclose(file_data);
	    fclose(directory_table);
	    fclose(test_fd);
	    fclose(test_dt);
        return 1;
    }
    if(memcmp(dt,t_dt,72*3) !=0){
        printf("Incorrect directory table content\n");
        fclose(file_data);
	    fclose(directory_table);
	    fclose(test_fd);
	    fclose(test_dt);
        return 1;
    }

    free(fd);
    free(dt);
    free(t_dt);
    free(t_fd);

    

    return 0;
}



int test_nospace_resize_and_write(){

    //check what happens if we want to resize file but there is no space
    FILE* file_data = fopen("file_data.bin","w");
    FILE* directory_table = fopen("directory_table.bin","w");
    FILE* hash_data = fopen("hash_data.bin","w");

    int i = 256*pow(2,0);
    void* zeros = calloc(sizeof(char)*i,sizeof(char));
    fwrite(zeros,sizeof(char)*i,1,file_data);
    free(zeros);
    zeros =NULL;

    fclose(file_data);
    fclose(directory_table);
    fclose(hash_data);
    void* new = init_fs("file_data.bin","directory_table.bin","hash_data.bin",4);

    create_file("first.txt",50,new);
    create_file("second.txt",100,new);
    create_file("third.txt",100,new);
    //resize to a larger file
    if(resize_file("first.txt",100,new)!= 2){
        printf("Should not resize\n");
        return 1;
    }
    //try to write a lot into the file
    if(write_file("third.txt",99,15,"Hello my name is Bob. I would like two coffe and a muffin",new)!= 3){
        printf("Should not write into file\n");
        return 1;
    }

    close_fs(new);

    return 0;
}



int test_hash_block(){

    FILE* file_data = fopen("file_data.bin","w");
    FILE* directory_table = fopen("directory_table.bin","w");
    FILE* hash_data = fopen("hash_data.bin","w");

    //this is the file that has the correct content after doing certain combos.
    FILE* test_fd = fopen("test_fd.bin","w");
    FILE* test_dt = fopen("test_dt.bin","w");
    FILE* test_hash = fopen("test_hash.bin","w");
    struct file temp;
    int i = 256*pow(2,0);
    void* zeros = calloc(sizeof(char)*i,sizeof(char));
    fwrite(zeros,sizeof(char)*i,1,file_data);
    fwrite(zeros,sizeof(char)*i,1,test_fd);
    free(zeros);

    //creating file into the before content
    strncpy(temp.name,"first.txt",64);
    temp.offset= 0;
    temp.length = 20;
    fseek(directory_table,0,SEEK_SET);
    
    fwrite(&temp,sizeof(struct file),1,directory_table);
    fseek(file_data,0,SEEK_SET);
    
    fwrite("Im first",sizeof("Im first"),1,file_data);
    


    temp.offset= 38;
    temp.length = 25;//resized first file and then moved it
    fseek(test_dt,0,SEEK_SET);
    fwrite(&temp,sizeof(struct file),1,test_dt);
    fseek(test_fd,38,SEEK_SET);
    fwrite("Im first",sizeof("Im first"),1,test_fd);

    //second file will be at the right place for both before and after file already
    strncpy(temp.name,"second.txt",64);
    temp.offset= 20;
    temp.length = 13;
    fseek(file_data,20,SEEK_SET);
    fseek(test_fd,20,SEEK_SET);
    fwrite("Im second",sizeof("Im second"),1,file_data);
    fwrite("Im second",sizeof("Im second"),1,test_fd);
    fwrite(&temp,sizeof(struct file),1,directory_table);
    fwrite(&temp,sizeof(struct file),1,test_dt);

    //we have a 3rd file in both file
    strncpy(temp.name,"third.txt",64);
    temp.offset= 33;
    temp.length = 5;

    fwrite(&temp,sizeof(struct file),1,directory_table);
    fwrite(&temp,sizeof(struct file),1,test_dt);
    //we have a 4th file for before file only
    strncpy(temp.name,"fourth.txt",64);
    temp.offset= 45;
    temp.length = 24;

    fwrite(&temp,sizeof(struct file),1,directory_table);
    //fwrite(&temp,sizeof(struct file),1,test_dt);delete fourth.txt

    fclose(test_hash);
    fclose(test_dt);
    fclose(test_fd);
    fclose(file_data);
    fclose(directory_table);
    fclose(hash_data);


    void* new = init_fs("file_data.bin","directory_table.bin","hash_data.bin",4);
    void* result = init_fs("test_fd.bin", "test_dt.bin","test_hash.bin",4);
    data* ptr = (data*) new;
    data* ptr_result = (data*) result;


    delete_file("fourth.txt",new);//let's delete the file first
    resize_file("first.txt",25,new);//resize

    compute_hash_tree(result);
    fseek(ptr_result->hash_data,0,SEEK_END);
    size_t size = ftell(ptr_result->hash_data);
    //check the hash tree
    void* hash_new = malloc(sizeof(char)*size);
    void* hash_result = malloc(sizeof(char)*size);

    fseek(ptr->hash_data,0,SEEK_SET);
    fseek(ptr_result->hash_data,0,SEEK_SET);

    fread(hash_new,sizeof(char)*size,1,ptr->hash_data);
    fread(hash_result,sizeof(char)*size,1,ptr_result->hash_data);


    if(memcmp(hash_new,hash_result,size)!= 0){
        printf("Wrong hash content\n");
        return 1;
    }


    free(hash_new);
    free(hash_result);
    close_fs(result);
    close_fs(new);
    return 0;
}

int test_hash_tree(){
    //check the hash_tree after resizing the first file
    //other than that, every file is the same

    FILE* file_data = fopen("file_data.bin","w");
    FILE* directory_table = fopen("directory_table.bin","w");
    FILE* hash_data = fopen("hash_data.bin","w");

    //this is the file that has the correct content after doing certain combos.
    FILE* test_fd = fopen("test_fd.bin","w");
    FILE* test_dt = fopen("test_dt.bin","w");
    FILE* test_hash = fopen("test_hash.bin","w");
    struct file temp;
    int i = 256*pow(2,0);
    void* zeros = calloc(sizeof(char)*i,sizeof(char));
    fwrite(zeros,sizeof(char)*i,1,file_data);
    fwrite(zeros,sizeof(char)*i,1,test_fd);
    free(zeros);


    strncpy(temp.name,"first.txt",64);
    temp.offset= 0;
    temp.length = 20;
    fseek(directory_table,0,SEEK_SET);
    fwrite(&temp,sizeof(struct file),1,directory_table);
    fseek(file_data,0,SEEK_SET);
    fwrite("Im first",sizeof("Im first"),1,file_data);
    


    temp.offset= 42;
    temp.length = 210;//resize
    fseek(test_dt,0,SEEK_SET);
    fwrite(&temp,sizeof(struct file),1,test_dt);
    fseek(test_fd,42,SEEK_SET);
    fwrite("Im first",sizeof("Im first"),1,test_fd);
    fwrite(&temp,sizeof(struct file),1,test_dt);
    



    strncpy(temp.name,"second.txt",64);
    temp.offset= 20;
    temp.length = 13;
    fseek(file_data,20,SEEK_SET);
    fwrite("Im second",sizeof("Im second"),1,file_data);
    fwrite(&temp,sizeof(struct file),1,directory_table);
    


    temp.offset = 0;
    temp.length = 13;
    fseek(test_fd,0,SEEK_SET);
    fwrite("Im second",sizeof("Im second"),1,test_fd);    
    fwrite(&temp,sizeof(struct file),1,test_dt);

    strncpy(temp.name,"third.txt",64);
    temp.offset= 33;
    temp.length = 5;

    fwrite(&temp,sizeof(struct file),1,directory_table);
    


    temp.offset = 13;
    temp.length = 5;
    fwrite(&temp,sizeof(struct file),1,test_dt);

    strncpy(temp.name,"fourth.txt",64);
    temp.offset= 45;
    temp.length = 24;

    fwrite(&temp,sizeof(struct file),1,directory_table);
    

    temp.offset= 18;
    temp.length = 42;
    fwrite(&temp,sizeof(struct file),1,test_dt);

    fclose(test_hash);
    fclose(test_dt);
    fclose(test_fd);
    fclose(file_data);
    fclose(directory_table);
    fclose(hash_data);


    void* new = init_fs("file_data.bin","directory_table.bin","hash_data.bin",4);
    void* result = init_fs("test_fd.bin", "test_dt.bin","test_hash.bin",4);
    data* ptr = (data*) new;
    data* ptr_result = (data*) result;


    resize_file("first.txt",210,new);

    compute_hash_tree(result);
    fseek(ptr_result->hash_data,0,SEEK_END);
    size_t size = ftell(ptr_result->hash_data);

    void* hash_new = malloc(sizeof(char)*size);
    void* hash_result = malloc(sizeof(char)*size);

    fseek(ptr->hash_data,0,SEEK_SET);
    fseek(ptr_result->hash_data,0,SEEK_SET);

    fread(hash_new,sizeof(char)*size,1,ptr->hash_data);
    fread(hash_result,sizeof(char)*size,1,ptr_result->hash_data);


    if(memcmp(hash_new,hash_result,size)!= 0){
        printf("Wrong hash content\n");
        return 1;
    }


    free(hash_new);
    free(hash_result);
    close_fs(result);
    close_fs(new);
    return 0;
}




/****************************/

/* Helper function */
void test(int (*test_function) (), char * function_name) {
    int ret = test_function();
    if (ret == 0) {
        printf("Passed %s\n", function_name);
    } else {
        printf("Failed %s returned %d\n", function_name, ret);
    }
}
/************************/

int main(int argc, char * argv[]) {
    
    // You can use the TEST macro as TEST(x) to run a test function named "x"
    
    TEST(test_init_fs_and_close);
    TEST(test_create_file);
    TEST(test_file_size);
    TEST(test_resize_file);
    TEST(test_rename_file);
    TEST(test_delete_file);
    TEST(test_write_file);
    TEST(test_repack);
    TEST(test_read_file);
    TEST(test_content);
    TEST(test_repack_resize);
    TEST(test_nospace_resize_and_write);
    TEST(test_hash_block);
    TEST(test_hash_tree);
    // Add more tests here

    return 0;
}
