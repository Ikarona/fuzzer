import additional
import mutation_struct as ms
import paramset
import static_analysis
import timing
import threading
import time
import random
import os
import pickle
import shutil
import subprocess
import argparse



def main():
    additional.CheckEnv()
    parser = argparse.ArgumentParser(description='Fuzzer command line arguments')
    parser.add_argument("--ptl", help='Path to library')
    parser.add_argument("--input", help='Path to initial input')
    parser.add_argument("--weight", help='Path of the pickle file for Basic Blocks weights)')
    parser.add_argument(("--cmp_path", help='Path to CMP instructions\' args'))
    parser.add_argument("--offsets", help='Base offset of application and library')
    parser.add_argument("--tested_app", help='Application that we test')

    args = parser.parse_args()
    paramset.PATHTOLIB = args.ptl
    paramset.PATHTOINITINPUT = args.input
    paramset.LIBPICKLE = args.weight
    paramset.LIBOFFSETS = args.offsets
    # paramset.SUT = args.tested_app
    # paramset.
    paramset.minLength=additional.GetMinFile(paramset.INITIALD)
    try:
        shutil.rmtree(paramset.KEEPD)
    except OSError:
        pass
    os.mkdir(paramset.KEEPD)

    try:
        os.mkdir("outd")
    except OSError:
        pass

    try:
        os.mkdir("outd/crashInputs")
    except OSError:
        additional.IsEmptyDir("outd/crashInputs")

    crashHash=[]
    try:
        os.mkdir(paramset.SPECIAL)
    except OSError:
        additional.IsEmptyDir(paramset.SPECIAL)

    try:
        os.mkdir(paramset.INTER)
    except OSError:
        additional.IsEmptyDir(paramset.INTER)

    ###### open names pickle files
    additional.GetBBOffsets()
    if paramset.PTMODE:
        pt = simplept.simplept()
    else:
        pt = None
    if paramset.ERRORBBON==True:
        gbb,bbb=FirstRun()
    else:
        gbb=0
   # ms.Die("dry run over..")

    noprogress=0
    currentfit=0
    lastfit=0

    paramset.CRASHIN.clear()
    stat=open("stats.log",'w')
    stat.write("**** Fuzzing started at: %s ****\n"%(datetime.now().isoformat('+'),))
    stat.write("**** Initial BB for seed inputs: %d ****\n"%(gbb,))
    stat.flush()
    os.fsync(stat.fileno())
    stat.write("Genaration\t MINfit\t MAXfit\t AVGfit MINlen\t Maxlen\t AVGlen\t #BB\t AppCov\t AllCov\n")
    stat.flush()
    os.fsync(stat.fileno())
    starttime=time.clock()
    allnodes = set()
    alledges = set()
    try:
        shutil.rmtree(paramset.INPUTD)
    except OSError:
        pass
    shutil.copytree(paramset.INITIALD,paramset.INPUTD)
    # fisrt we get taint of the intial inputs
    get_taint(paramset.INITIALD)
    print ( "MOst common offsets and values:", paramset.MOSTCOMMON)
    paramset.MOSTCOMFLAG=True
    crashhappend=False
    filest = os.listdir(paramset.INPUTD)
    filenum=len(filest)
    if filenum < paramset.POPSIZE:
        ms.create_files(paramset.POPSIZE - filenum)

    if len(os.listdir(paramset.INPUTD)) != paramset.POPSIZE:
        ms.Die("something went wrong. number of files is not right!")

    efd=open(paramset.ERRORS,"w")
    ms.prepareBBOffsets()
    writecache = True
    genran=0
    bbslide=10 # this is used to call run_error_BB() functions
    keepslide=3
    keepfilenum=paramset.BESTP
    while True:
        print( "[**] Generation %d\n***********"%(genran,) )
        del paramset.SPECIALENTRY[:]
        del paramset.TEMPTRACE[:]
        del paramset.BBSEENVECTOR[:]
        paramset.SEENBB.clear()
        paramset.TMPBBINFO.clear()
        paramset.TMPBBINFO.update(paramset.PREVBBINFO)

        fitnes=dict()
        execs=0
        paramset.cPERGENBB.clear()
        paramset.GOTSTUCK=False

        if paramset.ERRORBBON == True:
            if genran > paramset.GENNUM/5:
                bbslide = max(bbslide,paramset.GENNUM/20)
                keepslide=max(keepslide,paramset.GENNUM/100)
                keepfilenum=keepfilenum/2
            if 0< genran < paramset.GENNUM/5 and genran%keepslide == 0:
                copy_files(paramset.INPUTD,paramset.KEEPD,keepfilenum)

        #lets find out some of the error handling BBs
            if  genran >20 and genran%bbslide==0:
                stat.write("\n**** Error BB cal started ****\n")
                stat.flush()
                os.fsync(stat.fileno())
                run_error_bb(pt)
                copy_files(paramset.KEEPD,paramset.INPUTD,len(os.listdir(paramset.KEEPD))*1/10)
        files=os.listdir(paramset.INPUTD)
        for fl in files:
                tfl=os.path.join(paramset.INPUTD,fl)
                iln=os.path.getsize(tfl)
                args = (paramset.SUT % tfl).split(' ')
                progname = os.path.basename(args[0])
                (bbs,retc)=execute(tfl)
                if paramset.BBWEIGHT == True:
                    fitnes[fl]=ms.fitnesCal2(bbs,fl,iln)
                else:
                    fitnes[fl]=ms.fitnesNoWeight(bbs,fl,iln)

                execs+=1
                if retc < 0 and retc != -2:
                    print( "[*]Error code is %d"%(retc,) )
                    efd.write("%s: %d\n"%(tfl, retc))
                    efd.flush()
                    os.fsync(efd)
                    tmpHash=sha1OfFile(paramset.CRASHFILE)
                    if tmpHash not in crashHash:
                            crashHash.append(tmpHash)
                            tnow=datetime.now().isoformat().replace(":","-")
                            nf="%s-%s.%s"%(progname,tnow,ms.splitFilename(fl)[1])
                            npath=os.path.join("outd/crashInputs",nf)
                            shutil.copyfile(tfl,npath)
                            shutil.copy(tfl,paramset.SPECIAL)
                            paramset.CRASHIN.add(fl)
                    if paramset.STOPONCRASH == True:
                        crashhappend=True
                        break
        fitscore=[v for k,v in fitnes.items()]
        maxfit=max(fitscore)
        avefit=sum(fitscore)/len(fitscore)
        mnlen,mxlen,avlen=ms.getFileMinMax(paramset.INPUTD)
        print( "[*] Done with all input in Gen, starting SPECIAL. \n" )
        #### copy special inputs in SPECIAL directory and update coverage info ###
        spinputs=os.listdir(paramset.SPECIAL)
        for sfl in spinputs:
                if sfl in paramset.PREVBBINFO and sfl not in paramset.TMPBBINFO:
                        tpath=os.path.join(paramset.SPECIAL,sfl)
                        os.remove(tpath)
                        if sfl in paramset.TAINTMAP:
                            del paramset.TAINTMAP[sfl]
        paramset.PREVBBINFO=copy.deepcopy(paramset.TMPBBINFO)
        spinputs=os.listdir(paramset.SPECIAL)
        for inc in paramset.TMPBBINFO:
                paramset.SPECIALENTRY.append(inc)
                if inc not in spinputs:
                        incp=os.path.join(paramset.INPUTD,inc)
                        shutil.copy(incp,paramset.SPECIAL)
        appcov,allcov=ms.calculateCov()
        stat.write("\t%d\t %d\t %d\t %d\t %d\t %d\t %d\t %d\t %d\t %d\n"%(genran,min(fitscore),maxfit,avefit,mnlen,mxlen,avlen,len(paramset.cPERGENBB),appcov,allcov))
        stat.flush()
        os.fsync(stat.fileno())
        print( "[*] Wrote to stat.log\n" )
        if crashhappend == True:
            break
        genran += 1
        #this part is to get initial fitness that will be used to determine if fuzzer got stuck.
        lastfit=currentfit
        currentfit=maxfit
        if currentfit==lastfit:
            noprogress +=1
        else:
            noprogress =0
        if noprogress > 20:
            paramset.GOTSTUCK=True
            stat.write("Heavy mutate happens now..\n")
            noprogress =0
        if (genran >= paramset.GENNUM) and (paramset.STOPOVERGENNUM == True):
            break
        if len(os.listdir(paramset.SPECIAL))>0:
            if len(os.listdir(paramset.SPECIAL))<paramset.NEWTAINTFILES:
                get_taint(paramset.SPECIAL)
            else:
                try:
                    os.mkdir("outd/tainttemp")
                except OSError:
                    ms.emptyDir("outd/tainttemp")
                if conditional_copy_files(paramset.SPECIAL,"outd/tainttemp",paramset.NEWTAINTFILES) == 0:
                    get_taint("outd/tainttemp")
        print( "[*] Going for new generation creation.\n" )
        ms.createNextGeneration3(fitnes,genran)

    efd.close()
    stat.close()
    libfd_mm.close()
    libfd.close()
    endtime=time.clock()

    print( "[**] Totol time %f sec."%(endtime-starttime,) )
    print( "[**] Fuzzing done. Check %s to see if there were crashes.."%(paramset.ERRORS,))


if __name__ == '__main__':


    fuzzthread = threading.Thread(target = main)

    fuzzthread.start()

    if paramset.FLASK:

        socketio.run(app, host="0.0.0.0", port=5000)


if __name__ == '__main__':
    pass