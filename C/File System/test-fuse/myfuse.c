/* Do not change! */
#define FUSE_USE_VERSION 29
#define _FILE_OFFSET_BITS 64
/******************/

#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <fuse.h>
#include<errno.h>

#include "myfilesystem.c"

char * file_data_file_name = NULL;
char * directory_table_file_name = NULL;
char * hash_data_file_name = NULL;


int myfuse_getattr(const char * name, struct stat * result) {
    // MODIFY THIS FUNCTION
    if(name == '\0'){
        return 1;
    }
    printf("asd\n");
   
    memset(result, 0, sizeof(struct stat));
    if (strcmp(name, "/") == 0) {
        result->st_mode = S_IFDIR;
    } else {
        result->st_mode = S_IFREG;
    }

    char filename[strlen(name)+1];
    strncpy(filename,name,strlen(name));
    filename[strlen(name)]='\0';



    result->st_size = file_size(filename,fuse_get_context()->private_data);
    return 0;
}

int myfuse_readdir(const char * name, void * buf, fuse_fill_dir_t filler, off_t offset, struct fuse_file_info * fi) {
    // MODIFY THIS FUNCTION
   
    if (strcmp(name, "/") == 0) {
        filler(buf, "test_file", NULL, 0);
    }

    char* files = get_files(fuse_get_context()->private_data);
    for(int i = 0; i < strlen(files)/64;i++){
        char buff[64];
        strncpy(buff,files+i*64,64);
        filler(buf,buff,NULL,0);
    }


    return 0;
}

int myfuse_unlink(const char * path){
    // FILL OUT
    struct fuse_context* context = fuse_get_context();
    char name[strlen(path)+1];
    strncpy(name,path,strlen(path));
    name[strlen(path)]='\0';

    if(!delete_file(name,context->private_data)){
        return 0;
    }
    else{
        
        return ENOENT;
    }

}


int myfuse_rename(const char * oldname, const char * newname){
    // FILL OUT

    if(oldname=='\0' || newname=='\0'){
        return 1;
    }
    struct fuse_context* context = fuse_get_context();

    char name_old[strlen(oldname)+1];
    char name_new[strlen(newname)+1];

    strncpy(name_old,oldname,strlen(oldname));
    name_old[strlen(oldname)]='\0';
    strncpy(name_new,newname,strlen(newname));
    name_new[strlen(newname)]='\0';

    if(!rename_file(name_old,name_new,context->private_data)){
        return 0;
    }

   

    return ENOENT;

}

int myfuse_truncate(const char * filename, off_t length){
    // FILL OUT
    
    struct fuse_context* context = fuse_get_context();
    char name[strlen(filename)+1];
    strncpy(name,filename,strlen(filename));
    name[strlen(filename)]='\0';
    if(!resize_file(name,length,context->private_data)){
        return 0;
    }
    else{
        if(resize_file(name,length,context->private_data)==1){
            return ENOENT;
        }
        
    }
    return EINVAL;

}

int myfuse_open(const char * path, struct fuse_file_info * fi){
    // FILL OUT
    


    return 0;
}

int myfuse_read(const char * path, char * buf, size_t length, off_t offset, struct fuse_file_info * fi){
    // FILL OUT
    struct fuse_context context = fuse_get_context();

    char name[strlen(path)+1];
    strncpy(name,path,strlen(path));
    name[strlen(path)]='\0';

    int result = read_file(name,offset,count,buf,fuse_get_context()->private_data);

    if(result == 0){
        return 0;
    }
    else{
        if(result == 1){
            return ENOENT;
        }
        return EINVAL;
    }
    


}

int myfuse_write(const char * path, const char * buff, size_t length, off_t offset, struct fuse_file_info * fi){
    // FILL OUT
    char filename[strlen(path)+1];
    strncpy(filename,path,strlen(path));
    filename[strlen(path)]='\0';

    if(!write_file(filename,offset,length,buff,fuse_get_context()->private_data)){
        return 0;
    }
    else{
        if(write_file(filename,offset,length,buff,fuse_get_context()->private_data)==1){
            return ENOENT;
        }

        return EINVAL;
    }


    return 0;
}

int myfuse_release(const char * path, struct fuse_file_info * fi){
    // FILL OUT

    return 0;
}

void * myfuse_init(struct fuse_conn_info * data){
    // FILL OUT

    
    return init_fs(file_data_file_name,directory_table_file_name,hash_data_file_name,1);
}

void myfuse_destroy(void * filesystem){
    // FILL OUT
    filesystem = fuse_get_context()->private_data;

    close_fs(filesystem);

    return ;
}

int myfuse_create(const char * path, mode_t mode, struct fuse_file_info * fi){
    // FILL OUT
    char filename[strlen(path)+1];
    strncpy(filename,path,strlen(path));
    filename[strlen(path)]='\0';

    


    return 0;
}



struct fuse_operations operations = {
    .getattr = myfuse_getattr,
    .readdir = myfuse_readdir,
    
    .unlink = myfuse_unlink,
    .rename = myfuse_rename,
    .truncate =myfuse_truncate,
    .open = myfuse_open,
    .read = myfuse_read,
    .write = myfuse_write,
    .release = myfuse_release,
    .init = myfuse_init,//done
    .destroy = myfuse_destroy,//done
    .create = myfuse_create,

};

int main(int argc, char * argv[]) {
    // MODIFY (OPTIONAL)
    if (argc >= 5) {
        if (strcmp(argv[argc-4], "--files") == 0) {
            file_data_file_name = argv[argc-3];
            directory_table_file_name = argv[argc-2];
            hash_data_file_name = argv[argc-1];
            argc -= 4;
        }
    }
    // After this point, you have access to file_data_file_name, directory_table_file_name and hash_data_file_name
    int ret = fuse_main(argc, argv, &operations, NULL);
    return ret;
}