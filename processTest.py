import sys, argparse, os, time, subprocess

parser = argparse.ArgumentParser(description = "Tests the different thread counts to find the optimum one for your machine")

parser.add_argument('-l', metavar="Lower", type=int, help="Lower bound for thread count",
                    default=0)
parser.add_argument('-u', metavar="Upper", type=int, help="Upper bound for thread count",
                    default=0)

arguments = parser.parse_args()

if arguments.u < arguments.l:
    sys.exit("error: Upper bound must be greater than or equal to lower bound")

nullPointer = open(os.devnull)
standardOutput = sys.stdout

for threadCount in range(arguments.l, arguments.u + 1):
    print("ThreadCount = {}".format(threadCount))
    print("Processing...", end="\r")
    #sys.stdout = nullPointer
    start = time.time()
    subprocess.run(["{}/productMatch.py".format(os.getcwd()), '-t', str(threadCount), "something"])
    end = time.time()
    #sys.stdout = standardOutput
    print("Total Time: {}\n".format(end - start))   
