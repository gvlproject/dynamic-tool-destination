"""
# =============================================================================

Copyright Government of Canada 2015

Written by: Eric Enns, Public Health Agency of Canada,
                       National Microbiology Laboratory
            Mark Iskander, Public Health Agency of Canada,
                       National Microbiology Laboratory
            Daniel Bouchard, Public Health Agency of Canada,
                       National Microbiology Laboratory

Funded by the National Micriobiology Laboratory

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this work except in compliance with the License. You may obtain a copy of the
License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.

# =============================================================================
"""
"""
Created on June 23rd, 2015
@currentauthor: Mark Iskander
@originalauthor: Daniel Bouchard
"""

import logging
import os
import re
import sys
sys.path.append("")
import unittest
import mockGalaxy as mg
import ymltests as yt
import dynamic_tool_destination.DynamicToolDestination as dt

from dynamic_tool_destination.DynamicToolDestination import map_tool_to_destination
from testfixtures import log_capture


theApp = mg.App( "waffles_default", "test_spec")

#======================Jobs====================================
zeroJob = mg.Job()

emptyJob = mg.Job()
emptyJob.add_input_dataset( mg.InputDataset("input1", mg.Dataset( (os.getcwd() + "/tests/data/test.empty"), "txt", 14)) )

failJob = mg.Job()
failJob.add_input_dataset( mg.InputDataset("input1", mg.Dataset( (os.getcwd() + "/tests/data/test1.full"), "txt", 15)) )

msfileJob = mg.Job()
msfileJob.add_input_dataset( mg.InputDataset("input1", mg.Dataset( (os.getcwd() + "/tests/data/not_here.full"), "txt", 15)) )

notfileinpJob = mg.Job()
msfileJob.add_input_dataset( mg.InputDataset("input1", mg.NotAFile() ) )

runJob = mg.Job()
runJob.add_input_dataset( mg.InputDataset("input1", mg.Dataset( (os.getcwd() + "/tests/data/test3.full"), "txt", 15)) )

vfJob = mg.Job()
vfJob.add_input_dataset( mg.InputDataset("input1", mg.Dataset( (os.getcwd() + "/tests/data/test3.full"), "txt", 15)) )
vfJob.set_arg_value( "mlst_or_genedb", {"vfdb_in": "-bact"} )

argJob = mg.Job()
argJob.add_input_dataset( mg.InputDataset("input1", mg.Dataset( (os.getcwd() + "/tests/data/test3.full"), "txt", 15)) )
argJob.set_arg_value( "careful", True )

argNotFoundJob = mg.Job()
argNotFoundJob.add_input_dataset( mg.InputDataset("input1", mg.Dataset( (os.getcwd() + "/tests/data/test3.full"), "txt", 15)) )
argNotFoundJob.set_arg_value( "careful", False )

notvfJob = mg.Job()
notvfJob.add_input_dataset( mg.InputDataset("input1", mg.Dataset( (os.getcwd() + "/tests/data/test3.full"), "txt", 15)) )
notvfJob.set_arg_value( "mlst_or_genedb", {"vfdb_in": "-not_here"} )

dbJob = mg.Job()
dbJob.add_input_dataset( mg.InputDataset("input1", mg.Dataset( (os.getcwd() + "/tests/data/test.fasta"), "fasta", 10)) )

dbcountJob = mg.Job()
dbcountJob.add_input_dataset( mg.InputDataset("input1", mg.Dataset( (os.getcwd() + "/tests/data/test.fasta"), "fasta", None)) )

vfdbJob = mg.Job()
vfdbJob.add_input_dataset( mg.InputDataset("input1", mg.Dataset( (os.getcwd() + "/tests/data/test.fasta"), "fasta", 6)) )
vfdbJob.set_arg_value( "mlst_or_genedb", {"vfdb_in": "-bact"} )

#======================Tools===================================
vanillaTool = mg.Tool( 'test' )

unTool = mg.Tool( 'unregistered' )

overlapTool = mg.Tool( 'test_overlap' )

defaultTool = mg.Tool( 'test_tooldefault' )

dbTool = mg.Tool( 'test_db' )
dbinfTool = mg.Tool( 'test_db_high' )

argTool = mg.Tool( 'test_arguments' )

vfdbTool = mg.Tool( 'test_db' )
vfdbTool.add_tool_dependency( mg.ToolDependency("vfdb", os.getcwd() + "/tests") )

noVBTool = mg.Tool( 'test_no_verbose' )

usersTool = mg.Tool( 'test_users' )

numinputsTool = mg.Tool( 'test_num_input_datasets' )

#=======================YML file================================
path = os.getcwd() + "/tests/data/tool_destination.yml"
priority_path = os.getcwd() + "/tests/data/priority_tool_destination.yml"
broken_default_dest_path = os.getcwd() + "/tests/data/dest_fail.yml"
no_verbose_path = os.getcwd() + "/tests/data/test_no_verbose.yml"
users_test_path = os.getcwd() + "/tests/data/test_users.yml"
num_input_datasets_test_path = os.getcwd() + "/tests/data/test_num_input_datasets.yml"

#======================Test Variables=========================
value = 1
valueK = value * 1024
valueM = valueK * 1024
valueG = valueM * 1024
valueT = valueG * 1024
valueP = valueT * 1024
valueE = valueP * 1024
valueZ = valueE * 1024
valueY = valueZ * 1024


class TestDynamicToolDestination(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        logger = logging.getLogger()

    #=======================map_tool_to_destination()================================

    @log_capture()
    def test_brokenDestYML(self, l):
        self.assertRaises(mg.JobMappingException, map_tool_to_destination, runJob, theApp, vanillaTool, "user@email.com", True, broken_default_dest_path)

        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'No global default destination specified in config!'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Loading file: input1' + os.getcwd() + '/tests/data/test3.full'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Total size: 3.23 KB')
        )

    @log_capture()
    def test_filesize_empty(self, l):
        self.assertRaises(mg.JobMappingException, map_tool_to_destination, emptyJob, theApp, vanillaTool, "user@email.com", True, path)
        self.assertRaises(mg.JobMappingException, map_tool_to_destination, emptyJob, theApp, vanillaTool, "user@email.com", True, priority_path)

        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Loading file: input1' + os.getcwd() + '/tests/data/test.empty'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Total size: 0.00 B'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Total number of files: 1'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Loading file: input1' + os.getcwd() + '/tests/data/test.empty'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Total size: 0.00 B'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Total number of files: 1')
        )

    @log_capture()
    def test_filesize_zero(self, l):
        self.assertRaises(mg.JobMappingException, map_tool_to_destination, zeroJob, theApp, vanillaTool, "user@email.com", True, path)
        self.assertRaises(mg.JobMappingException, map_tool_to_destination, zeroJob, theApp, vanillaTool, "user@email.com", True, priority_path)

        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Total size: 0.00 B'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Total number of files: 0'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Total size: 0.00 B'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Total number of files: 0')
        )

    @log_capture()
    def test_filesize_fail(self, l):
        self.assertRaises(mg.JobMappingException, map_tool_to_destination, failJob, theApp, vanillaTool, "user@email.com", True, path)
        self.assertRaises(mg.JobMappingException, map_tool_to_destination, failJob, theApp, vanillaTool, "user@email.com", True, priority_path)

        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Loading file: input1' + os.getcwd() + '/tests/data/test1.full'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Total size: 293.00 B'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Total number of files: 1'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Loading file: input1' + os.getcwd() + '/tests/data/test1.full'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Total size: 293.00 B'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Total number of files: 1')
        )

    @log_capture()
    def test_filesize_run(self, l):
        job = map_tool_to_destination( runJob, theApp, vanillaTool, "user@email.com", True, path )
        self.assertEquals( job, 'Destination1' )
        priority_job = map_tool_to_destination( runJob, theApp, vanillaTool, "user@email.com", True, priority_path )
        self.assertEquals( priority_job, 'Destination1_high' )

        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Loading file: input1' + os.getcwd() + '/tests/data/test3.full'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Total size: 3.23 KB'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Total number of files: 1'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Running 'test' with 'Destination1'."),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Loading file: input1' + os.getcwd() + '/tests/data/test3.full'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Total size: 3.23 KB'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Total number of files: 1'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Running 'test' with 'Destination1_high'.")
        )

    @log_capture()
    def test_default_tool(self, l):
        job = map_tool_to_destination( runJob, theApp, defaultTool, "user@email.com", True, path )
        self.assertEquals( job, 'waffles_default' )
        priority_job = map_tool_to_destination( runJob, theApp, defaultTool, "user@email.com", True, priority_path )
        self.assertEquals( priority_job, 'waffles_default_high' )

        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Tool 'test_tooldefault' not specified in config. Using default destination."),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Running 'test_tooldefault' with 'waffles_default'."),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Tool 'test_tooldefault' not specified in config. Using default destination."),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Running 'test_tooldefault' with 'waffles_default_high'.")
        )

    @log_capture()
    def test_arguments_tool(self, l):
        job = map_tool_to_destination( argJob, theApp, argTool, "user@email.com", True, path )
        self.assertEquals( job, 'Destination6' )
        priority_job = map_tool_to_destination( argJob, theApp, argTool, "user@email.com", True, priority_path )
        self.assertEquals( priority_job, 'Destination6_med' )

        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Running 'test_arguments' with 'Destination6'."),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Running 'test_arguments' with 'Destination6_med'.")
        )

    @log_capture()
    def test_arguments_arg_not_found(self, l):
        job = map_tool_to_destination( argNotFoundJob, theApp, argTool, "user@email.com", True, path )
        self.assertEquals( job, 'waffles_default' )
        priority_job = map_tool_to_destination( argNotFoundJob, theApp, argTool, "user@email.com", True, priority_path )
        self.assertEquals( priority_job, 'waffles_default_high' )

        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Running 'test_arguments' with 'waffles_default'."),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Running 'test_arguments' with 'waffles_default_high'.")
        )

    @log_capture()
    def test_tool_not_found(self, l):
        job = map_tool_to_destination( runJob, theApp, unTool, "user@email.com", True, path )
        self.assertEquals( job, 'waffles_default' )
        priority_job = map_tool_to_destination( runJob, theApp, unTool, "user@email.com", True, priority_path )
        self.assertEquals( priority_job, 'waffles_default_high' )

        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Tool 'unregistered' not specified in config. Using default destination."),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Running 'unregistered' with 'waffles_default'."),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Tool 'unregistered' not specified in config. Using default destination."),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Running 'unregistered' with 'waffles_default_high'.")
        )

    @log_capture()
    def test_fasta(self, l):
        job = map_tool_to_destination( dbJob, theApp, dbTool, "user@email.com", True, path )
        self.assertEquals( job, 'Destination4' )
        priority_job = map_tool_to_destination( dbJob, theApp, dbTool, "user@email.com", True, priority_path )
        self.assertEquals( priority_job, 'Destination4_high' )

        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Loading file: input1' + os.getcwd() + '/tests/data/test.fasta'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Total amount of records: 10'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Running 'test_db' with 'Destination4'."),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Loading file: input1' + os.getcwd() + '/tests/data/test.fasta'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Total amount of records: 10'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Running 'test_db' with 'Destination4_high'.")
        )

    @log_capture()
    def test_fasta_count(self, l):
        job = map_tool_to_destination( dbcountJob, theApp, dbTool, "user@email.com", True, path )
        self.assertEquals( job, 'Destination4' )
        priority_job = map_tool_to_destination( dbcountJob, theApp, dbTool, "user@email.com", True, priority_path )
        self.assertEquals( priority_job, 'Destination4_high' )

        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Loading file: input1' + os.getcwd() + '/tests/data/test.fasta'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Total amount of records: 6'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Running 'test_db' with 'Destination4'."),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Loading file: input1' + os.getcwd() + '/tests/data/test.fasta'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Total amount of records: 6'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Running 'test_db' with 'Destination4_high'.")
        )

    @log_capture()
    def test_vf(self, l):
        job = map_tool_to_destination( vfJob, theApp, vfdbTool, "user@email.com", True, path )
        self.assertEquals( job, 'Destination4' )
        priority_job = map_tool_to_destination( vfJob, theApp, vfdbTool, "user@email.com", True, priority_path )
        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Loading file: ' + os.getcwd() + '/tests/vfdb/?bact.test'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Loading file: input1' + os.getcwd() + '/tests/data/test3.full'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Total amount of records: 4'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Running 'test_db' with 'Destination4'."),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Loading file: ' + os.getcwd() + '/tests/vfdb/?bact.test'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Loading file: input1' + os.getcwd() + '/tests/data/test3.full'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Total amount of records: 4'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Running 'test_db' with 'Destination4_high'.")
        )
        self.assertEquals( priority_job, 'Destination4_high' )

        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Loading file: ' + os.getcwd() + '/tests/vfdb/?bact.test'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Loading file: input1' + os.getcwd() + '/tests/data/test3.full'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Total amount of records: 4'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Running 'test_db' with 'Destination4'."),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Loading file: ' + os.getcwd() + '/tests/vfdb/?bact.test'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Loading file: input1' + os.getcwd() + '/tests/data/test3.full'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Total amount of records: 4'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Running 'test_db' with 'Destination4_high'.")
        )

    @log_capture()
    def test_vf_not_found(self, l):
        job = map_tool_to_destination( notvfJob, theApp, vfdbTool, "user@email.com", True, path )
        self.assertEquals( job, 'Destination4' )
        priority_job = map_tool_to_destination( notvfJob, theApp, vfdbTool, "user@email.com", True, priority_path )
        self.assertEquals( priority_job, 'Destination4_high' )

        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.'),
            ('dynamic_tool_destination.DynamicToolDestination', 'INFO', 'No virulence factors database'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG',
             'Loading file: input1' + os.getcwd() + '/tests/data/test3.full'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Total amount of records: 0'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Running 'test_db' with 'Destination4'."),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.'),
            ('dynamic_tool_destination.DynamicToolDestination', 'INFO', 'No virulence factors database'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG',
             'Loading file: input1' + os.getcwd() + '/tests/data/test3.full'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Total amount of records: 0'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Running 'test_db' with 'Destination4_high'.")
        )

    @log_capture()
    def test_no_verbose(self, l):
        job = map_tool_to_destination( runJob, theApp, noVBTool, "user@email.com", True, no_verbose_path )
        self.assertEquals( job, 'Destination1' )

        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Running 'test_no_verbose' with 'Destination1'.")
        )

    @log_capture()
    def test_authorized_user(self, l):
        job = map_tool_to_destination( runJob, theApp, usersTool, "user@email.com", True, users_test_path )
        self.assertEquals( job, 'special_cluster' )

        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Running 'test_users' with 'special_cluster'."),
        )

    @log_capture()
    def test_unauthorized_user(self, l):
        job = map_tool_to_destination( runJob, theApp, usersTool, "userblah@email.com", True, users_test_path )
        self.assertEquals( job, 'lame_cluster' )

        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Running 'test_users' with 'lame_cluster'.")
        )


#================================Invalid yaml files==============================
    @log_capture()
    def test_no_file(self, l):
        self.assertRaises(IOError, dt.parse_yaml, path="")
        l.check()

    @log_capture()
    def test_bad_nice(self, l):
        dt.parse_yaml(path=yt.ivYMLTest11, test=True)
        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG',
             "Running config validation..."),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG',
             "nice_value goes from -20 to 20; rule 1 in 'spades' has a nice_value of '-21'. Setting nice_value to 0."),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.')
        )

    @log_capture()
    def test_empty_file(self, l):
        self.assertEquals(dt.parse_yaml(path=yt.ivYMLTest2, test=True), {})

    @log_capture()
    def test_no_tool_name(self, l):
        self.assertEquals(dt.parse_yaml(path=yt.ivYMLTest3, test=True), yt.iv3dict)
        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Malformed YML; expected job name, but found a list instead!'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.')
        )

    @log_capture()
    def test_no_rule_type(self, l):
        self.assertEquals(dt.parse_yaml(path=yt.ivYMLTest4, test=True), yt.ivDict)
        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "No rule_type found for rule 1 in 'spades'."),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.')
        )

    @log_capture()
    def test_no_rule_lower_bound(self, l):
        self.assertEquals(dt.parse_yaml(path=yt.ivYMLTest51, test=True), yt.ivDict)
        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Missing bounds for rule 1 in 'spades'. Ignoring rule."),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.')
        )

    @log_capture()
    def test_no_rule_upper_bound(self, l):
        self.assertEquals(dt.parse_yaml(path=yt.ivYMLTest52, test=True), yt.ivDict)
        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Missing bounds for rule 1 in 'spades'. Ignoring rule."),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.')
        )

    @log_capture()
    def test_no_rule_arg(self, l):
        self.assertEquals(dt.parse_yaml(path=yt.ivYMLTest53, test=True), yt.ivDict53)
        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Found a fail_message for rule 1 in 'spades', but destination is not 'fail'! Setting destination to 'fail'."),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.')
        )

    @log_capture()
    def test_bad_rule_type(self, l):
        self.assertEquals(dt.parse_yaml(path=yt.ivYMLTest6, test=True), yt.ivDict)
        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Unrecognized rule_type 'iencs' found in 'spades'. Ignoring..."),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.')
        )

    @log_capture()
    def test_no_err_msg(self, l):
        self.assertEquals(dt.parse_yaml(path=yt.ivYMLTest91, test=True), yt.iv91dict)
        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "No nice_value found for rule 1 in 'spades'. Setting nice_value to 0."),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Missing a fail_message for rule 1 in 'spades'. Adding generic fail_message."),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.')
        )

    @log_capture()
    def test_no_default_dest(self, l):
        dt.parse_yaml(path=yt.ivYMLTest7, test=True)
        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'No global default destination specified in config!'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.')
        )

    @log_capture()
    def test_invalid_category(self, l):
        dt.parse_yaml(path=yt.ivYMLTest8, test=True)
        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'No global default destination specified in config!'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Unrecognized category 'ice_cream' found in config file!"),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.')
        )

    @log_capture()
    def test_arguments_no_err_msg(self, l):
        self.assertEquals(dt.parse_yaml(path=yt.ivYMLTest12, test=True), yt.iv12dict)
        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG',
            "Missing a fail_message for rule 1 in 'spades'. Adding generic fail_message."),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.')
        )

    @log_capture()
    def test_arguments_no_args(self, l):
        self.assertEquals(dt.parse_yaml(path=yt.ivYMLTest131, test=True), yt.iv131dict)
        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG',
            "No arguments found for rule 1 in 'spades' despite being of type arguments. Ignoring rule."),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.')
        )

    @log_capture()
    def test_arguments_no_arg(self, l):
        self.assertEquals(dt.parse_yaml(path=yt.ivYMLTest132, test=True), yt.iv132dict)
        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Found a fail_message for rule 1 in 'spades', but destination is not 'fail'! Setting destination to 'fail'."),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.')
        )

    @log_capture()
    def test_return_bool_for_multiple_jobs(self, l):
        self.assertFalse(dt.parse_yaml(path=yt.ivYMLTest133, test=True, return_bool=True))
        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Missing a fail_message for rule 1 in 'smalt'.")
        )

    @log_capture()
    def test_return_rule_for_multiple_jobs(self, l):
        self.assertEquals(dt.parse_yaml(path=yt.ivYMLTest133, test=True), yt.iv133dict)
        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Missing a fail_message for rule 1 in 'smalt'. Adding generic fail_message."),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.')
        )

    @log_capture()
    def test_return_bool_for_no_destination(self, l):
        self.assertFalse(dt.parse_yaml(path=yt.ivYMLTest134, test=True, return_bool=True))
        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "No destination specified for rule 1 in 'spades'.")
        )


    @log_capture()
    def test_return_rule_for_no_destination(self, l):
        self.assertEquals(dt.parse_yaml(path=yt.ivYMLTest134, test=True), yt.iv134dict)
        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "No destination specified for rule 1 in 'spades'. Ignoring..."),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.')
        )

    @log_capture()
    def test_return_rule_for_reversed_bounds(self, l):
        self.assertEquals(dt.parse_yaml(path=yt.ivYMLTest135, test=True), yt.iv135dict)
        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "lower_bound exceeds upper_bound for rule 1 in 'spades'. Reversing bounds."),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.')
        )

    @log_capture()
    def test_return_bool_for_missing_tool_fields(self, l):
        self.assertFalse(dt.parse_yaml(path=yt.ivYMLTest136, test=True, return_bool=True))
        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Tool 'spades' does not have rules nor a default_destination!")
        )

    @log_capture()
    def test_return_rule_for_missing_tool_fields(self, l):
        self.assertEquals(dt.parse_yaml(path=yt.ivYMLTest136, test=True), yt.iv136dict)
        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Tool 'spades' does not have rules nor a default_destination!"),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.')
        )

    @log_capture()
    def test_return_bool_for_blank_tool(self, l):
        self.assertFalse(dt.parse_yaml(path=yt.ivYMLTest137, test=True, return_bool=True))
        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Config section for tool 'spades' is blank!")
        )

    @log_capture()
    def test_return_rule_for_blank_tool(self, l):
        self.assertEquals(dt.parse_yaml(path=yt.ivYMLTest137, test=True), yt.iv137dict)
        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Config section for tool 'spades' is blank!"),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.')
        )

    @log_capture()
    def test_return_bool_for_malformed_users(self, l):
        self.assertFalse(dt.parse_yaml(path=yt.ivYMLTest138, test=True, return_bool=True))
        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Entry '123' in users for rule 1 in tool 'spades' is in an invalid format!"),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Supplied email 'invaliduser.email@com' for rule 1 in tool 'spades' is in an invalid format!")
        )

    @log_capture()
    def test_return_rule_for_malformed_users(self, l):
        self.assertEquals(dt.parse_yaml(path=yt.ivYMLTest138, test=True), yt.iv138dict)
        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Entry '123' in users for rule 1 in tool 'spades' is in an invalid format! Ignoring entry."),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Supplied email 'invaliduser.email@com' for rule 1 in tool 'spades' is in an invalid format! Ignoring email."),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.')
        )

    @log_capture()
    def test_return_bool_for_no_users(self, l):
        self.assertFalse(dt.parse_yaml(path=yt.ivYMLTest139, test=True, return_bool=True))
        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Couldn't find a list under 'users:'!")
        )

    @log_capture()
    def test_return_rule_for_no_users(self, l):
        self.assertEquals(dt.parse_yaml(path=yt.ivYMLTest139, test=True), yt.iv139dict)
        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Couldn't find a list under 'users:'! Ignoring rule."),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.')
        )

    @log_capture()
    def test_return_bool_for_malformed_user_email(self, l):
        self.assertFalse(dt.parse_yaml(path=yt.ivYMLTest140, test=True, return_bool=True))
        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Supplied email 'invalid.user2@com' for rule 2 in tool 'spades' is in an invalid format!"),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Supplied email 'invalid.user1@com' for rule 2 in tool 'spades' is in an invalid format!"),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "No valid user emails were specified for rule 2 in tool 'spades'!")
        )

    @log_capture()
    def test_return_rule_for_malformed_user_email(self, l):
        self.assertEquals(dt.parse_yaml(path=yt.ivYMLTest140, test=True), yt.iv140dict)
        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Supplied email 'invalid.user2@com' for rule 2 in tool 'spades' is in an invalid format! Ignoring email."),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Supplied email 'invalid.user1@com' for rule 2 in tool 'spades' is in an invalid format! Ignoring email."),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "No valid user emails were specified for rule 2 in tool 'spades'! Ignoring rule."),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.')
        )

    @log_capture()
    def test_return_bool_for_empty_users(self, l):
        self.assertFalse(dt.parse_yaml(path=yt.ivYMLTest141, test=True, return_bool=True))
        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Entry 'None' in users for rule 2 in tool 'spades' is in an invalid format!"),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Entry 'None' in users for rule 2 in tool 'spades' is in an invalid format!"),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "No valid user emails were specified for rule 2 in tool 'spades'!")
        )

    @log_capture()
    def test_return_rule_for_empty_users(self, l):
        self.assertEquals(dt.parse_yaml(path=yt.ivYMLTest141, test=True), yt.iv141dict)
        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Entry 'None' in users for rule 2 in tool 'spades' is in an invalid format! Ignoring entry."),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Entry 'None' in users for rule 2 in tool 'spades' is in an invalid format! Ignoring entry."),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "No valid user emails were specified for rule 2 in tool 'spades'! Ignoring rule."),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.')
        )

    @log_capture()
    def test_return_bool_for_bad_num_input_datasets_bounds(self, l):
        self.assertFalse(dt.parse_yaml(path=yt.ivYMLTest142, test=True, return_bool=True))
        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Error: lower_bound is set to Infinity, but must be lower than upper_bound!"),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "lower_bound exceeds upper_bound for rule 1 in 'smalt'.")
        )

    @log_capture()
    def test_return_rule_for_bad_num_input_datasets_bound(self, l):
        self.assertEquals(dt.parse_yaml(path=yt.ivYMLTest142, test=True), yt.iv142dict)
        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Error: lower_bound is set to Infinity, but must be lower than upper_bound! Setting lower_bound to 0!"),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.')
        )

    @log_capture()
    def test_return_bool_for_worse_num_input_datasets_bounds(self, l):
        self.assertFalse(dt.parse_yaml(path=yt.ivYMLTest143, test=True, return_bool=True))
        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Error: lower_bound is set to Infinity, but must be lower than upper_bound!")
        )

    @log_capture()
    def test_return_rule_for_worse_num_input_datasets_bound(self, l):
        self.assertEquals(dt.parse_yaml(path=yt.ivYMLTest143, test=True), yt.iv143dict)
        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Error: lower_bound is set to Infinity, but must be lower than upper_bound! Setting lower_bound to 0!"),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.')
        )

    @log_capture()
    def test_priority_default_destination_without_med_priority_destination(self, l):
        dt.parse_yaml(path=yt.ivYMLTest144, test=True)
        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "No default 'med' priority destination!"),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.')
        )

    @log_capture()
    def test_priority_default_destination_with_invalid_priority_destination(self, l):
        dt.parse_yaml(path=yt.ivYMLTest145, test=True)
        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Invalid default priority destination 'mine' found in config!"),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.')
        )

    @log_capture()
    def test_tool_without_med_priority_destination(self, l):
        dt.parse_yaml(path=yt.ivYMLTest146, test=True)
        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "No 'med' priority destination for rule 1 in 'smalt'. Ignoring..."),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.')
        )

    @log_capture()
    def test_tool_with_invalid_priority_destination(self, l):
        dt.parse_yaml(path=yt.ivYMLTest147, test=True)
        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "Invalid priority destination 'mine' for rule 1 in 'smalt'. Ignoring..."),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.')
        )

    @log_capture()
    def test_users_with_invalid_priority(self, l):
        dt.parse_yaml(path=yt.ivYMLTest148, test=True)
        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', "User 'user@email.com', priority is not valid! Must be either low, med, or high."),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.')
        )

#================================Valid yaml files==============================
    @log_capture()
    def test_parse_valid_yml(self, l):
        self.assertEqual(dt.parse_yaml(yt.vYMLTest1, test=True), yt.vdictTest1_yml)
        self.assertEqual(dt.parse_yaml(yt.vYMLTest2, test=True), yt.vdictTest2_yml)
        self.assertEqual(dt.parse_yaml(yt.vYMLTest3, test=True), yt.vdictTest3_yml)
        self.assertTrue(dt.parse_yaml(yt.vYMLTest4, test=True, return_bool=True))
        self.assertEqual(dt.parse_yaml(yt.vYMLTest4, test=True), yt.vdictTest4_yml)
        self.assertTrue(dt.parse_yaml(yt.vYMLTest5, test=True, return_bool=True))
        self.assertEqual(dt.parse_yaml(yt.vYMLTest5, test=True), yt.vdictTest5_yml)
        self.assertTrue(dt.parse_yaml(yt.vYMLTest6, test=True, return_bool=True))
        self.assertEqual(dt.parse_yaml(yt.vYMLTest6, test=True), yt.vdictTest6_yml)
        self.assertTrue(dt.parse_yaml(yt.vYMLTest7, test=True, return_bool=True))
        self.assertEqual(dt.parse_yaml(yt.vYMLTest7, test=True), yt.vdictTest7_yml)
        l.check(
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Running config validation...'),
            ('dynamic_tool_destination.DynamicToolDestination', 'DEBUG', 'Finished config validation.'),
        )

#================================Testing str_to_bytes==========================
    def test_str_to_bytes_invalid(self):
        self.assertRaises(dt.MalformedYMLException, dt.str_to_bytes, "1d")
        self.assertRaises(dt.MalformedYMLException, dt.str_to_bytes, "1 d")

    def test_str_to_bytes_valid(self):
        self.assertEqual(dt.str_to_bytes("-1"), -1)
        self.assertEqual(dt.str_to_bytes( "1" ), value)
        self.assertEqual(dt.str_to_bytes( 156 ), 156)
        self.assertEqual(dt.str_to_bytes( "1 B" ), value)
        self.assertEqual(dt.str_to_bytes( "1 KB" ), valueK)
        self.assertEqual(dt.str_to_bytes( "1 MB" ), valueM)
        self.assertEqual(dt.str_to_bytes( "1 gB" ), valueG)
        self.assertEqual(dt.str_to_bytes( "1 Tb" ), valueT)
        self.assertEqual(dt.str_to_bytes( "1 pb" ), valueP)
        self.assertEqual(dt.str_to_bytes( "1 EB" ), valueE)
        self.assertEqual(dt.str_to_bytes( "1 ZB" ), valueZ)
        self.assertEqual(dt.str_to_bytes( "1 YB" ), valueY)

#==============================Testing bytes_to_str=============================
    @log_capture()
    def test_bytes_to_str_invalid(self, l):
        testValue = ""
        self.assertRaises( ValueError, dt.bytes_to_str, testValue )
        testValue = "5564fads"
        self.assertRaises( ValueError, dt.bytes_to_str, testValue )
        testValue = "45.0.1"
        self.assertRaises( ValueError, dt.bytes_to_str, testValue )
        self.assertRaises( ValueError, dt.bytes_to_str, "1 024" )

    def test_bytes_to_str_valid(self):
        self.assertEqual(dt.bytes_to_str(-1), "Infinity")
        self.assertEqual(dt.bytes_to_str( value), "1.00 B")
        self.assertEqual(dt.bytes_to_str( valueK), "1.00 KB")
        self.assertEqual(dt.bytes_to_str( valueM), "1.00 MB")
        self.assertEqual(dt.bytes_to_str( valueG), "1.00 GB")
        self.assertEqual(dt.bytes_to_str( valueT ), "1.00 TB")
        self.assertEqual(dt.bytes_to_str( valueP ), "1.00 PB")
        self.assertEqual(dt.bytes_to_str( valueE ), "1.00 EB")
        self.assertEqual(dt.bytes_to_str( valueZ ), "1.00 ZB")
        self.assertEqual(dt.bytes_to_str( valueY ), "1.00 YB")

        self.assertEqual(dt.bytes_to_str( 10, "B" ), "10.00 B")
        self.assertEqual(dt.bytes_to_str( 1000000, "KB" ), "976.56 KB")
        self.assertEqual(dt.bytes_to_str( 1000000000, "MB" ), "953.67 MB")
        self.assertEqual(dt.bytes_to_str( 1000000000000, "GB" ), "931.32 GB")
        self.assertEqual(dt.bytes_to_str( 1000000000000000, "TB" ), "909.49 TB")
        self.assertEqual(dt.bytes_to_str( 1000000000000000000, "PB" ), "888.18 PB")
        self.assertEqual(dt.bytes_to_str( 1000000000000000000000, "EB" ), "867.36 EB")
        self.assertEqual(dt.bytes_to_str( 1000000000000000000000000, "ZB" ), "847.03 ZB")

        self.assertEqual(dt.bytes_to_str( value, "KB" ), "1.00 B")
        self.assertEqual(dt.bytes_to_str( valueK, "MB" ), "1.00 KB")
        self.assertEqual(dt.bytes_to_str( valueM, "GB" ), "1.00 MB")
        self.assertEqual(dt.bytes_to_str( valueG, "TB" ), "1.00 GB")
        self.assertEqual(dt.bytes_to_str( valueT, "PB" ), "1.00 TB")
        self.assertEqual(dt.bytes_to_str( valueP, "EB" ), "1.00 PB")
        self.assertEqual(dt.bytes_to_str( valueE, "ZB" ), "1.00 EB")
        self.assertEqual(dt.bytes_to_str( valueZ, "YB" ), "1.00 ZB")

        self.assertEqual(dt.bytes_to_str( "1" ), "1.00 B")
        self.assertEqual(dt.bytes_to_str( "\t\t1000000" ), "976.56 KB")
        self.assertEqual(dt.bytes_to_str( "1000000000\n" ), "953.67 MB")
        self.assertEqual(dt.bytes_to_str( 1024, "fda" ), "1.00 KB")

if __name__ == '__main__':
    unittest.main()
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestDynamicToolDestination)
    #ret = not unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()
    #print(ret)
    #sys.exit(ret)
