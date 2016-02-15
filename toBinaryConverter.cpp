#include <stdlib.h>
#include <iostream>
#include <fstream>
#include <string>

using namespace std;

int main()
{
  ifstream myfile ("start_sequence");
  if (!myfile.is_open())
  {
    return 1;
  }

  ofstream outfile;
  outfile.open("start_sequence.dat", ios::binary | ios::out);
  if (!outfile.is_open())
  {
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
  return 0;
}
