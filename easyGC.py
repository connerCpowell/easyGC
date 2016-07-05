import sys, os, argparse, glob
from GCMSalign import *

parser = argparse.ArgumentParser(prog='easyGC', description="easyGC calls peaks, deconvolutes them, quantitates them and then aligns them across all your GC-MS samples...magically!", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
subparsers = parser.add_subparsers(title='use one of these subcommands')

peak_parser = subparsers.add_parser('peakcall', help='peakcall help', description="run the peak caller on a directory of GC-MS files", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
peak_parser.set_defaults(which='peakcall')
peak_parser.add_argument('-i', '--indir', required=True, help='directory containing your GC-MS files to be processed', type=str)
peak_parser.add_argument('-f', '--ftype', required=True, help='CDF or JDX. This is the type of input GC-MS files you have. CDF is not supported on Windows', type=str)
peak_parser.add_argument('-TS','--trimstart', required=False, default="0.0", help='trim X.XX minutes from the start of the chromatogram', type=str)
peak_parser.add_argument('-TE','--trimend', required=False, default="0.0", help='trim X.XX minutes from the end of the chromatogram', type=str)
peak_parser.add_argument('-W', '--window', required=False, default=9, help='peak calling: width (in scans) of window over which local ion maxima are detected. Should be similar to the width off your peaks.', type=int)
peak_parser.add_argument('-S', '--scans', required=False, default=3, help='peak calling: distance (in scans) at which locally apexing ions can be combined into one peak', type=int)
peak_parser.add_argument('-N', '--minions', required=False, default=4, help='peak calling: min number of apexing ions with intensity above a threshold required for a peak to be called. Higher = less peaks called', type=int)
peak_parser.add_argument('-R', '--minintensity', required=False, default=5, help='peak calling: min intensity (percent) of an ion relative to max peak intensity for that ion to be included in the peak', type=int)
peak_parser.add_argument('-M', '--noisemult', required=False, default=4, help='peak calling: total peak intensity must be at least this multiple of the base noise level to be called. Higher multiple means fewer peaks called', type=int)
peak_parser.add_argument('-I', '--topions', required=False, default=10, help='from the list of most important ions in a peak, how many should be outputted as a mini mass-spec?', type=int)
peak_parser.add_argument('-T', '--threads', required=False, default=1, help='number of threads to use. Currently only multithreaded on linux!', type=int)

align_parser = subparsers.add_parser('align', help='align help', description="run the peak aligner on a directory of .expr files", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
align_parser.set_defaults(which='align')
align_parser.add_argument('-e', '--exprdir', required=True, help='the path to the .expr files from a previous peak calling run. These will be aligned.', type=str)
align_parser.add_argument('-D', '--distance', required=False, default=2.5, help='local alignment: distance in retention time (seconds) over which the local peak aligner should search for similar peaks to this one', type=float)
align_parser.add_argument('-G', '--gap', required=False, default=0.40, help='local alignment: gap penalty. Lower G results in more peaks in the output. Higher G result in fewer output peaks but possibly some peaks contain multiple merged peaks', type=float)
align_parser.add_argument('-C', '--mincommon', required=False, default=1, help='local alignment: minimum number of samples that an aligned peak must be called in for it to be outputted', type=int)
align_parser.add_argument('-T', '--threads', required=False, default=1, help='number of threads to use. Currently only multithreaded on linux!', type=int)

pipe_parser = subparsers.add_parser('pipeline', help='pipeline help', description="run the whole pipeline, including peak calling and peak aligner", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
pipe_parser.set_defaults(which='pipeline')
pipe_parser.add_argument('-i', '--indir', required=True, help='directory containing your GC-MS files to be processed', type=str)
pipe_parser.add_argument('-f', '--ftype', required=True, help='CDF or JDX. This is the type of input GC-MS files you have. CDF is not supported on Windows', type=str)
pipe_parser.add_argument('-TS','--trimstart', required=False, default=0.0, help='trim X.XX minutes from the start of the chromatogram', type=float)
pipe_parser.add_argument('-TE','--trimend', required=False, default=0.0, help='trim X.XX minutes from the end of the chromatogram', type=float)
pipe_parser.add_argument('-W', '--window', required=False, default=9, help='peak calling: width (in scans) of window over which local ion maxima are detected. Should be similar to the width off your peaks.', type=int)
pipe_parser.add_argument('-S', '--scans', required=False, default=3, help='peak calling: distance (in scans) at which locally apexing ions can be combined into one peak', type=int)
pipe_parser.add_argument('-N', '--minions', required=False, default=4, help='peak calling: min number of apexing ions with intensity above a threshold required for a peak to be called. Higher = less peaks called', type=int)
pipe_parser.add_argument('-R', '--minintensity', required=False, default=5, help='peak calling: min intensity (percent) of an ion relative to max peak intensity for that ion to be included in the peak', type=int)
pipe_parser.add_argument('-M', '--noisemult', required=False, default=4, help='peak calling: total peak intensity must be at least this multiple of the base noise level to be called. Higher multiple means fewer peaks called', type=int)
pipe_parser.add_argument('-I', '--topions', required=False, default=10, help='from the list of most important ions in a peak, how many should be outputted as a mini mass-spec?', type=int)
pipe_parser.add_argument('-D', '--distance', required=False, default=2.5, help='local alignment: distance in retention time (seconds) over which the local peak aligner should search for similar peaks to this one', type=float)
pipe_parser.add_argument('-G', '--gap', required=False, default=0.40, help='local alignment: gap penalty. Lower G results in more peaks in the output. Higher G result in fewer output peaks but possibly some peaks contain multiple merged peaks', type=float)
pipe_parser.add_argument('-C', '--mincommon', required=False, default=1, help='local alignment: minimum number of samples that an aligned peak must be called in for it to be outputted', type=int)
pipe_parser.add_argument('-T', '--threads', required=False, default=1, help='number of threads to use. Currently only multithreaded on linux!', type=int)

args = parser.parse_args()
print args

if args.which == 'pipeline':
    print "running full pipeline"
    detect_and_align(args)

elif args.which == 'align':
    print "running peak aligner"
    align(args)

elif args.which == 'peakcall':
    print "running peak detector and quantification"
    detect(args)
