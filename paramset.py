import os
import inspect

MY_PATH = os.path.abspath(__file__)
mydir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
TAINTANALYSISINFO = dict()
INITIALCMPOFFSET = dict()
BYTESTOCHANGE = dict()
INITDIR = './'
BB = list()
TEMPTRACE = list()
POPULATIONNUM = 1
BBPERC = 80
BBWITHOUTERR = set()
BBWITHERR = set()
LEAOFFSETS = set()
PATHTOLIB = './'
PATHTOINITINPUT = './'
# this is a directorty for internal use. Don't change this.
KEEPD="keep/"
# directory containing seed inputs
INITIALD=mydir
#a list to keep inputs that have triggered a new BB in generation. Such inputs will get a chance in the next generation as it is (no mutaiton/crossover).
SPECIALENTRY=[]
SPECIAL="special/"
# populated once during dry run on valid inputs
GOODBB=set()
#set the path where new input files are created
INPUTD="data/"
# set number of libraries that were statically analyzed for BB weights. This is related to LIBTOMONITOR. There is one default entry for the main executable. NOTE: in the current implementation, we assume to have only ONE library to be used, i.e. max value for this is 2.
LIBNUM=1
#set load offsets of the libraries of interest by observing pintool output for image load. You get this value by fisrt launching the application as trial and then reading the file imageOffset.txt.
LIBOFFSETS=[]

ERRORBBAPP=set()
ERRORBBLIB=set()
ERRORBBALL=set()

 # directory to combine initial inputs + special inputs to choose new inputs during population generation.
INTER="inter/"

# this flags decides if we wnat to run error BB detection step.
ERRORBBON=True

PTMODE=False

#set to keep name of the file resulted ina crash.
CRASHIN=set()

# this dictinary keeps offsets and their immediate values that are found in all the initial inputs. key=offset, value=list(immediate values in CMP). we also use negative offsets to mark bootom offsets in a file.
MOSTCOMMON=dict()
# population size in each generation. Choose even number.
POPSIZE=200

#set error log in this file
ERRORS="error.log"

# for elitist approach, set number of best inputs to go in the next generation. Make sure that POPSIZE-BESTP is multiple of 2.
BESTP=20

# a set to record seen BBs across previous iterations
SEENBB=set()
TMPBBINFO=dict()
PREVBBINFO=dict() #this keeps special entries for the previous generation. It is used to delete inputs which are superceded by newer inputs in dicovering new BBs.TAINTMAP

# data for calculating code-coverage
cPERGENBB=set()

# number of iterations (generations) to run
GENNUM=1000

#set path of software under test (SUT)
SUT=''

#set this flag if we want to consider BB weights, otherwise each BB have weight 1.
BBWEIGHT=True
# list of BBs seen in a single generation
BBSEENVECTOR=[]

# stoping condition "if run for GENNUM, stop"
STOPOVERGENNUM=True

# Set file path for crash hash info (this cannot be changed as pintool writes to this file)
CRASHFILE='crash.bin'

# this is a dictionary to keep per input taintinfo. key=file_name, value=tuple(set(all offsets used in some CMP),dict(key=offset; value=list(concrete values of immediates in CMP)))
TAINTMAP=dict()
LEAMAP=dict() # dictionary to keep offsets for a input that were used in LEA instructions.

FLASK=False

ALLSTRINGS=list()
NAMESPICKLE=list()
cAPPBB=set()
NOFFBYTES=True
ALLBB=list()

# set path of each library's saved pickle files (two files for each lib) that will be read by the fuzzer. This is set in a list, whose length should be equal to LIBNUM. We have created two separate variables to mention these files. 1st one if for BB weights and 2nd one is for strings found in binaries.
LIBPICKLE=[]