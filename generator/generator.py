#/usr/bin/env python2

import random
import json
import math

numJobs = 100

numMapper = 32
numReducer = 2

rackSize = 20

numPhysComp = 80

durationMapTaskMs = 1000
fileSizeBytes = 1 * int(1e6)

time = 0

for i in range(0, numJobs):
	
	job = dict()
	job["am.type"]			= "mapreduce";
	job["job.start.ms"]		= str(time);
	job["job.end.ms"]		= str(time + 10000);
	job["job.queue.name"]	= "sls_queue_1";
	job["job.id"]			= "job_%i" % i;
	job["job.user"]			= "root";
	job["job.tasks"]		= list();

	job_bytes = random.randint(1,2) * fileSizeBytes

	for j in range(0, numMapper):
		task = dict();
		
		#where is the input data?
		inputLocation = int(random.random() * numPhysComp)
		if inputLocation <= 0:
			inputLocation = 1;
		if inputLocation > numPhysComp:
			inputLocation = numPhysComp;
	
		rackID = int( math.ceil(inputLocation / rackSize) )
	
		task["container.host"]				= "/rack-%i/node%i" % (rackID, inputLocation)  #location der daten (so tun wir momentan)
		task["container.start.ms"]			= "0"
		task["container.end.ms"]			= str(durationMapTaskMs)
		task["container.priority"]			= "20"
		task["container.type"]				= "map"
		task["container.inputBytes"]		= str(job_bytes)
		task["container.outputBytes"]		= str(job_bytes)
		task["container.splitLocations"]	= list()
		task["container.splitLocations"].append(task["container.host"])


		job["job.tasks"].append(task)


	for j in range(0, numReducer):
		task = dict();
		
		#where is the input data?
		inputLocation = int(random.random() * numPhysComp)
		if inputLocation <= 0:
			inputLocation = 1;
		if inputLocation > numPhysComp:
			inputLocation = numPhysComp;

		rackID = int( math.ceil(inputLocation / rackSize) )
		
		
		task["container.host"]				= "/rack-%i/node%i" % (rackID, inputLocation)  #location der daten (so tun wir momentan)
		task["container.start.ms"]			= "0"
		task["container.end.ms"]			= str(durationMapTaskMs)
		task["container.priority"]			= "20"
		task["container.type"]				= "reduce"
		task["container.inputBytes"]		= str(numMapper * job_bytes/4)
		task["container.outputBytes"]		= str(job_bytes)


		job["job.tasks"].append(task)

	time += random.randint(10000, 20000)

	#write in json file
	print json.dumps(job, indent=1)
