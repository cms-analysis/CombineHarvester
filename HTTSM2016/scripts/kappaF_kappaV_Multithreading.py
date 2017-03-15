# Simple script to multithread the process of the KappaF, KappaV 2d grid
# Adjust the values below:
#  - nToysPerJob = number of toys per multithreaded process
#  - points = number of total points
#
# points / nToysPerJob = number of cores you will need to run on
# You do not need to set the number of cores



from multiprocessing import Process
import subprocess
import math




nToysPerJob = 15
points = 200




def runFit(points, toys, j) :

    bottom = int(j)*toys
    top = ((int(j)+1)*toys)-1

    toRun = []
    toRun.append('combineTool.py')
    toRun.append('-n')
    toRun.append('CvCf.%i' % j)
    toRun.append('-M')
    toRun.append('MultiDimFit')
    toRun.append('-m')
    toRun.append('125')
    toRun.append('--setPhysicsModelParameterRanges')
    toRun.append('CV=0.0,3.0:CF=0.0,1.5')
    toRun.append('kappaWorkspace.root')
    toRun.append('--algo=grid')
    toRun.append('--points=%i' % points)
    toRun.append('-t')
    toRun.append('-1')
    toRun.append('--expectSignal=1')
    toRun.append('--minimizerAlgoForMinos=Minuit2,Migrad')
    toRun.append('--firstPoint')
    toRun.append('%i' % bottom)
    toRun.append('--lastPoint')
    toRun.append('%i' % top)
    #toRun.append('--fastScan') # This does not re-profile the nuisances, it is really fast, but produces low quality results
    #toRun.append('')

    subprocess.call( toRun )

# CH takes your nPointsIn and chooses the next largest integer
# value that is a perfect square as its input nPoints
# So we want to match that if we are multithreading
def findNPointss( nPointsIn ) :
    toSquare = math.sqrt( nPointsIn )
    print "Sqrt( %i ) = %.2f" % (nPointsIn, toSquare)
    return math.ceil( toSquare ) * math.ceil( toSquare )


nPoints = findNPointss( points )
print "nPoints ",nPoints
jobs = int(nPoints/nToysPerJob)+1
processes = []

for i in range( jobs ) :
    processes.append( Process(target=runFit, args=(nPoints, nToysPerJob, i,) ) )
    processes[-1].start()

# Make sure all jobs finish
for process in processes :
    if process.is_alive() :
        print "Waiting for process pid: ",process.pid
        process.join()



print "\n\n"
print "Now Run:"
print "hadd higgsCombineCvCf.MultiDimFit.mH125.root higgsCombineCvCf.*.MultiDimFit.mH125.root"
print "root -l higgsCombineCvCf.MultiDimFit.mH125.root ../../../../scripts/contours2D.cxx"
print 'contour2D("CV",%i,0.0,3.0,"CF",%i,0.0,1.5,1.,1.)' % (math.sqrt(nPoints), math.sqrt(nPoints))
print "\n\n"



