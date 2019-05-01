################################################################################
# Name:		README.performance_testing
# Author:	Rodney Marable <rodney.marable@gmail.com>
# Created On:	January 13, 2018
# Last Changed: April 28, 2019
# Purpose:	Describe the basic HPC performance tests
################################################################################

This document outlines the HPC performance tests and offers some guidelines
on others things to try.

Please refer to README.Axb_random for additional information.

################################
# Standalone Performance Tests #
################################

The standalone tests measure the following:

(a) Compute time required to solve Ax=b when A and b are matrices populated
with random floats from the standard distribution with an origin=0 and a
randomly generated standard deviation (mu) also computed from the standard
distribution and to dump A, b, and x to a logfile.

(b) Time required to dump the log files to disk.

(c) Time required to compress the logfile and move it to a new logs
subdirectory.

(a) and (b) are captured by Axb_random.py's first timer.
(c) is captured by Axb_random.py's second timer.

The resulting data is contained in the summary_final CSV file for each test in
separate columns for each timer.

The standalone plots graph N (matrix dimensions) versus total compute time
in hours.  Additional plotting capability to show the amount of time required
to compress and move the log files will be added to the same axes in a future
update.

#############################
# Cluster Performance Tests #
#############################

The cluster performance tests measure the amount of time that a given task
array executing an array of MATRIX_SIZES takes to fully complete.

Start_Time = the date/time that the first job began running
Finish_Time = the date/time that the last job completed
Queue_Time = the amount of time that the job spent waiting to execute

The cluster job scheduler captures the same data as the standalone test
(item (a) + (b) + (c) as outlined above), along with the time required to
schedule the job, spool it to the execute nodes, and cleanup after the job
has completed.

The cluster plots graph the task array size (in total jobs) versus total
compute time in hours.

Because it accounts for scheduler and spooling overhead, this is a far more
accurate measurement of the total time required for Axb_random.py to solve
Ax=b for MATRIX_SIZES, compress the log, and move it to another directory
than the standalone version.

########################
# Setting MATRIX_SIZES #
########################

Using MATRIX_SIZES=1000-10000 with steps of 1000 is a reasonable "full" test.
Originally this test was run with MATRIX_SIZES from 1000 to 15000 in steps
of 1000.  However, as matrices get bigger, they take longer to populate and
solve, with their log files also growing progressively larger.  

- If a shorter overall test time is desired, change MATRIX_SIZES as needed
but be careful about going beyond 10000 as the upper limit, especially when
using instances with less than 8GB of memory.

Examples:

MATRIX_SIZES = "500 1000 2500 5000 7500 10000"
MATRIX_SIZES = "512 1024 2048 4096 8192"

- Using much smaller matrices to test how schedulers and master nodes of 
different instance types perform when required to spool many small jobs.

Examples:

MATRIX_SIZES = "100 250 500 750 1000 1250 1500 1750 2000 2250 2500"
MATRIX_SIZES = "32 64 128 256 384 512 640 768 896 1024"

- If you are willing to wait and are willing to pay the cost, using larger
larger matrices on bigger instances is a good way to differentiate between the
suitability of compute platforms for jobs that will run for a long time.

Examples (only use on matrices with more than 16GB of memory):

MATRIX_SIZES = "1000 2500 5000 7500 10000 12500 15000 17500 20000"
MATRIX_SIZES = "1000 5000 10000 15000 20000 25000 30000"

- Disabling the LOG_FILE feature removes memory limitations imposed by the 
need to dump the log file to disk and compress it.  This permits solving of
much larger matrices with the test bounded only by the amount of memory
present in the instance.

The current default uses:

MATRIX_SIZES = "500 1000 1500 2000 2500 3000 3500 4000 4500 5000"

This test takes about 7 minutes to complete on a single m5.2xlarge instance
and generates approximately 280MB of log files.

##################
# AWS EC2 Limits #
##################

Please keep these constraints in mind when sizing cluster stacks.

* The default stack configuration limits the autoscaler to five (5) compute
nodes.  Modifying this value will incur additional charges.

* The default AWS EC2 limits prevent more than 20 on-demand or spot instances
at one time in any given availability zone.

* Be mindful that long-running jobs may exhaust the CPU credits available to
an instance and will therefore limit performance.