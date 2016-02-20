#include <stdlib.h>
#include <iostream>
#include <fstream>
#include <string>

using namespace std;

int main(int argc,char *args[])
{
  if(argc!=3)
  {
    std::cerr<<"arg1: input; arg2: output";
    return 1;
  }

  ifstream myfile (args[1]/*"start_sequence"*/);
  if (!myfile.is_open())
  {
    std::cerr<<"arg1: is not a file";
    return 1;
  }

  ofstream outfile;
  outfile.open(args[2]/*"start_sequence.dat"*/, ios::binary | ios::out);
  if (!outfile.is_open())
  {
    std::cerr<<"arg2: can't open";
    return 1;
  }

  string s;
  while ( getline (myfile,s) )
  {
    std::string delimiter = ",";

    size_t pos = 0;
    std::string token;
    while ((pos = s.find(delimiter)) != std::string::npos) {
      token = s.substr(0, pos);
      char number =  atoi(token.c_str());
      outfile.write(&number, 1);
      s.erase(0, pos + delimiter.length());
    }
  }
  outfile.close();
  myfile.close();
  std::cout<<"converted '"<<args[1]<<"' to '"<<args[2]<<"'"<<std::endl;
  return 0;
}
