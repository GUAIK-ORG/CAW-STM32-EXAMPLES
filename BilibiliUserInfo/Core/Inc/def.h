
#ifndef __DEF_H__
#define __DEF_H__
#include <stdint.h>

// 按照1字节内存对齐
#pragma pack(1)
typedef struct {
  int32_t following;
  int32_t follower;
} USER_INFO_T;
#pragma pack()

extern USER_INFO_T G_USER_INFO;

#endif