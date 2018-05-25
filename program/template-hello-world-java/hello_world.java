/*
 CK program template

 See CK LICENSE.txt for licensing details
 See CK COPYRIGHT.txt for copyright details

 Developer: Grigori Fursin, 2018, Grigori.Fursin@cTuning.org, http://fursin.net
*/

//Import libraries...
import java.io.*;

public class hello_world
{
  static int N=16;
  static double[][] A=new double [N][N];
  static double[][] B=new double [N][N];
  static double[][] C=new double [N][N];

  // *******************************************************************
  public static void main(String args[]) 
  {
    System.out.println("Hello world!");
    System.out.println("");

    String env=System.getenv("CK_VAR1");
    System.out.println("CK_VAR1="+env);

    env=System.getenv("CK_VAR2");
    System.out.println("CK_VAR2="+env);
  }
}
