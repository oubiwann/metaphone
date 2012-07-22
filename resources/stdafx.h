#ifndef STDAFX__H
#define STDAFX__H

#include <string>
#include <cstring>

#define TRUE  true
#define FALSE false

class CString {
 public:
  string data;
  CString() {}
  CString(const string & str) : data(str) {}
  const char * c_str() {return data.c_str();}
  int GetLength()   {return data.size();}
  char GetAt(int i) {return data[i];}
  void SetAt(int i, char c) {data[i] = c;}
  CString Mid(int start, int len) {return data.substr(start,len);}
  MakeUpper() {int i = 0, l = data.size(); for (;i != l; ++i) data[i] = toupper(data[i]);}
  int Find(char c) {return data.find(c);}
  int Find(const char * str) {return data.find(str);}
  void operator+=(const char *str) {data += str;}
  void Insert(int p, const char * str) {data.insert(p, str);}
};

bool operator == (CString & rhs, const char * lhs)
{
  return rhs.data == lhs;
}

#endif




