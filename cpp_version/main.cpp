// txt2mid.cpp

#include <iostream>
#include <cstdio>
#include <vector>
#include <map>
#include <string>

#include "project.h"


int main(int argc, char** argv){
    std::cout << "Hello Famitracker world" << std::endl;
    
    for (int i=0; i < argc; i++){
        printf("argv[%d] = \'%s\'\n", i, argv[i]);
    }
    return 0;
}

