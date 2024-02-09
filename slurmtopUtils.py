
import sys
import subprocess

def run_command_with_output(cmd):
  p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  return(p.stdout.read().decode())

def get_joblist(user_id):
  joblist = run_command_with_output("squeue --user="+user_id+" --noheader")
  return joblist

def get_jobinfo(job_number):
  jobinfo = run_command_with_output("squeue -j " + job_number + " --noheader --format=\"%i %U %C %D\"")
  return jobinfo

def get_nodelist(job_number):
  nodelist = run_command_with_output("scontrol show hostnames $(squeue -j " + job_number + " --format=\"%N\" --noheader)")
  return nodelist 

def get_nodeusage(node_name, user_name):
  cpu_usage = run_command_with_output("ssh " + node_name + " ps -U " + user_name + " -o pid,pcpu,pmem,stat | awk '{s+=$2} END {print s}'")
  mem_usage = run_command_with_output("ssh " + node_name + " ps -U " + user_name + " -o pid,pcpu,pmem,stat | awk '{s+=$3} END {print s}'")
  return cpu_usage + mem_usage

if __name__ == '__main__':
  j = "943441"
  u = "ub01556"
  nodelist = get_nodelist(j)
  jobinfo = get_jobinfo(j)
  joblist = get_joblist(u)
  print(nodelist)
  print(jobinfo)
  print(joblist)

