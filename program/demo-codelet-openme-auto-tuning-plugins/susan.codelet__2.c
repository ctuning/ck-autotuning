typedef unsigned char  uchar;

#pragma hmpp astex_codelet__2 codelet &
#pragma hmpp astex_codelet__2 , args[l].io=inout &
#pragma hmpp astex_codelet__2 , args[mid].io=inout &
#pragma hmpp astex_codelet__2 , args[r].io=in &
#pragma hmpp astex_codelet__2 , target=C &
#pragma hmpp astex_codelet__2 , version=1.4.0

void astex_codelet__2(int *r, uchar *mid, int x_size, int y_size, int l[9], int a, int b)
{
  uchar  *mp;
  int  j;
  int  i;
  int  y;
  int  x;
  int  n;
  int  m;
  int  b22;
  int  b20;
  int  b02;
  int  b00;
  int  p4;
  int  p3;
  int  p2;
  int  p1;
  int  b10;
  int  b21;
  int  b12;
  int  b01;
  int  centre;
astex_thread_begin:  {
    for (i = 4 ; i < y_size - 4 ; i++)
      for (j = 4 ; j < x_size - 4 ; j++)
        if (mid[i * x_size + j] < 8)
          {
            centre = r[i * x_size + j];
            mp = mid + (i - 1) * x_size + j - 1;
            n = (*mp < 8) + (*(mp + 1) < 8) + (*(mp + 2) < 8) + (*(mp + x_size) < 8) + (*(mp + x_size + 2) < 8) + (*(mp + x_size + x_size) < 8) + (*(mp + x_size + x_size + 1) < 8) + (*(mp + x_size + x_size + 2) < 8);
            if (n == 0)
              mid[i * x_size + j] = 100;
            if ((n == 1) && (mid[i * x_size + j] < 6))
              {
                l[0] = r[(i - 1) * x_size + j - 1];
                l[1] = r[(i - 1) * x_size + j];
                l[2] = r[(i - 1) * x_size + j + 1];
                l[3] = r[(i) * x_size + j - 1];
                l[4] = 0;
                l[5] = r[(i) * x_size + j + 1];
                l[6] = r[(i + 1) * x_size + j - 1];
                l[7] = r[(i + 1) * x_size + j];
                l[8] = r[(i + 1) * x_size + j + 1];
                if (mid[(i - 1) * x_size + j - 1] < 8)
                  {
                    l[0] = 0;
                    l[1] = 0;
                    l[3] = 0;
                    l[2] *= 2;
                    l[6] *= 2;
                    l[5] *= 3;
                    l[7] *= 3;
                    l[8] *= 4;
                  }
                else                 {
                  if (mid[(i - 1) * x_size + j] < 8)
                    {
                      l[1] = 0;
                      l[0] = 0;
                      l[2] = 0;
                      l[3] *= 2;
                      l[5] *= 2;
                      l[6] *= 3;
                      l[8] *= 3;
                      l[7] *= 4;
                    }
                  else                   {
                    if (mid[(i - 1) * x_size + j + 1] < 8)
                      {
                        l[2] = 0;
                        l[1] = 0;
                        l[5] = 0;
                        l[0] *= 2;
                        l[8] *= 2;
                        l[3] *= 3;
                        l[7] *= 3;
                        l[6] *= 4;
                      }
                    else                     {
                      if (mid[(i) * x_size + j - 1] < 8)
                        {
                          l[3] = 0;
                          l[0] = 0;
                          l[6] = 0;
                          l[1] *= 2;
                          l[7] *= 2;
                          l[2] *= 3;
                          l[8] *= 3;
                          l[5] *= 4;
                        }
                      else                       {
                        if (mid[(i) * x_size + j + 1] < 8)
                          {
                            l[5] = 0;
                            l[2] = 0;
                            l[8] = 0;
                            l[1] *= 2;
                            l[7] *= 2;
                            l[0] *= 3;
                            l[6] *= 3;
                            l[3] *= 4;
                          }
                        else                         {
                          if (mid[(i + 1) * x_size + j - 1] < 8)
                            {
                              l[6] = 0;
                              l[3] = 0;
                              l[7] = 0;
                              l[0] *= 2;
                              l[8] *= 2;
                              l[1] *= 3;
                              l[5] *= 3;
                              l[2] *= 4;
                            }
                          else                           {
                            if (mid[(i + 1) * x_size + j] < 8)
                              {
                                l[7] = 0;
                                l[6] = 0;
                                l[8] = 0;
                                l[3] *= 2;
                                l[5] *= 2;
                                l[0] *= 3;
                                l[2] *= 3;
                                l[1] *= 4;
                              }
                            else                             {
                              if (mid[(i + 1) * x_size + j + 1] < 8)
                                {
                                  l[8] = 0;
                                  l[5] = 0;
                                  l[7] = 0;
                                  l[6] *= 2;
                                  l[2] *= 2;
                                  l[1] *= 3;
                                  l[3] *= 3;
                                  l[0] *= 4;
                                }
                            }
                          }
                        }
                      }
                    }
                  }
                }
                m = 0;
                for (y = 0 ; y < 3 ; y++)
                  for (x = 0 ; x < 3 ; x++)
                    if (l[y + y + y + x] > m)
                      {
                        m = l[y + y + y + x];
                        a = y;
                        b = x;
                      }
                if (m > 0)
                  {
                    if (mid[i * x_size + j] < 4)
                      mid[(i + a - 1) * x_size + j + b - 1] = 4;
                    else                     mid[(i + a - 1) * x_size + j + b - 1] = mid[i * x_size + j] + 1;
                    if ((a + a + b) < 3)
                      {
                        i += a - 1;
                        j += b - 2;
                        if (i < 4)
                          i = 4;
                        if (j < 4)
                          j = 4;
                      }
                  }
              }
            if (n == 2)
              {
                b00 = mid[(i - 1) * x_size + j - 1] < 8;
                b02 = mid[(i - 1) * x_size + j + 1] < 8;
                b20 = mid[(i + 1) * x_size + j - 1] < 8;
                b22 = mid[(i + 1) * x_size + j + 1] < 8;
                if (((b00 + b02 + b20 + b22) == 2) && ((b00 | b22) & (b02 | b20)))
                  {
                    if (b00)
                      {
                        if (b02)
                          {
                            x = 0;
                            y = -1;
                          }
                        else                         {
                          x = -1;
                          y = 0;
                        }
                      }
                    else                     {
                      if (b02)
                        {
                          x = 1;
                          y = 0;
                        }
                      else                       {
                        x = 0;
                        y = 1;
                      }
                    }
                    if (((float ) r[(i + y) * x_size + j + x] / (float ) centre) > 0.7)
                      {
                        if (((x == 0) && (mid[(i + (2 * y)) * x_size + j] > 7) && (mid[(i + (2 * y)) * x_size + j - 1] > 7) && (mid[(i + (2 * y)) * x_size + j + 1] > 7)) || ((y == 0) && (mid[(i) * x_size + j + (2 * x)] > 7) && (mid[(i + 1) * x_size + j + (2 * x)] > 7) && (mid[(i - 1) * x_size + j + (2 * x)] > 7)))
                          {
                            mid[(i) * x_size + j] = 100;
                            mid[(i + y) * x_size + j + x] = 3;
                          }
                      }
                  }
                else                 {
                  b01 = mid[(i - 1) * x_size + j] < 8;
                  b12 = mid[(i) * x_size + j + 1] < 8;
                  b21 = mid[(i + 1) * x_size + j] < 8;
                  b10 = mid[(i) * x_size + j - 1] < 8;
                  if (((b01 + b12 + b21 + b10) == 2) && ((b10 | b12) & (b01 | b21)) && ((b01 & ((mid[(i - 2) * x_size + j - 1] < 8) | (mid[(i - 2) * x_size + j + 1] < 8))) | (b10 & ((mid[(i - 1) * x_size + j - 2] < 8) | (mid[(i + 1) * x_size + j - 2] < 8))) | (b12 & ((mid[(i - 1) * x_size + j + 2] < 8) | (mid[(i + 1) * x_size + j + 2] < 8))) | (b21 & ((mid[(i + 2) * x_size + j - 1] < 8) | (mid[(i + 2) * x_size + j + 1] < 8)))))
                    {
                      mid[(i) * x_size + j] = 100;
                      i--;
                      j -= 2;
                      if (i < 4)
                        i = 4;
                      if (j < 4)
                        j = 4;
                    }
                }
              }
            if (n > 2)
              {
                b01 = mid[(i - 1) * x_size + j] < 8;
                b12 = mid[(i) * x_size + j + 1] < 8;
                b21 = mid[(i + 1) * x_size + j] < 8;
                b10 = mid[(i) * x_size + j - 1] < 8;
                if ((b01 + b12 + b21 + b10) > 1)
                  {
                    b00 = mid[(i - 1) * x_size + j - 1] < 8;
                    b02 = mid[(i - 1) * x_size + j + 1] < 8;
                    b20 = mid[(i + 1) * x_size + j - 1] < 8;
                    b22 = mid[(i + 1) * x_size + j + 1] < 8;
                    p1 = b00 | b01;
                    p2 = b02 | b12;
                    p3 = b22 | b21;
                    p4 = b20 | b10;
                    if (((p1 + p2 + p3 + p4) - ((b01 & p2) + (b12 & p3) + (b21 & p4) + (b10 & p1))) < 2)
                      {
                        mid[(i) * x_size + j] = 100;
                        i--;
                        j -= 2;
                        if (i < 4)
                          i = 4;
                        if (j < 4)
                          j = 4;
                      }
                  }
              }
          }
  }
astex_thread_end:;
}

