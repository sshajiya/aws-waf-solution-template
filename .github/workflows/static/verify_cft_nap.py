import boto3
import os
import sys
import re
import requests

def vfy_cft_link(cft_name,exp_op):
  '''
  This method is to verify the cloud formation output link status.
  |  *cft_name*         | Name of the Stack                      |
  |  *exp_op*           | expected output for the output link    |
  |  *returns*          | True if outoput exists if not False    |
  '''
  cf_client = boto3.client('cloudformation')
  response = cf_client.describe_stacks(StackName=cft_name)
  if not response["Stacks"][0]["Outputs"]:
    print("no results in output section")
    return False
  outputs = response["Stacks"][0]["Outputs"]
  print("output infor for the stack: ", outputs)
  try:
    for output in outputs:
      if output["OutputKey"] == "AppProtectLBDNSName":
        url="http://"+output["OutputValue"]
        print(url)
        chk_data = requests.get(url)
        print(exp_op,chk_data,chk_data.text)
        if exp_op in chk_data.text:
          print(chk_data.text)
          return True
        else:
          print(chk_data.text)
          return False
  except Exception as e:
    print("Exception raised with error:",e)

if __name__ == '__main__':

  nginx_default_page="Welcome to nginx"
  nginx_static_page="Hello World"
  nginx_dynamic_page="Arcadia Finance"
  stack_name= "nap-cft-stack"
  page_type=sys.argv[1] 
  if page_type == "static":
    page_type = nginx_static_page
  elif page_type == "dynamic":
    page_type = nginx_dynamic_page
  else:
    page_type = nginx_default_page
  #Verifying functionality of NAP
  try:
    vfy_status=vfy_cft_link(stack_name,page_type)
    if vfy_status:
      print("NGINX APP PROTECT ", sys.argv[1].upper() , "PAGE VERIFICATION IS COMPLETED SUCESSFULLY...")
    else:
      print("Error: NGINX APP PROTECT ", sys.argv[1].upper() , " PAGE VERIFICATION IS Failed...")
  except Exception as e:
    print("Exception raised with error:",e)
