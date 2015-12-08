"""
# =============================================================================

Copyright Government of Canada 2015

Written by: Eric Enns, Public Health Agency of Canada,
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
#=============================================Valid XML===================================================
# One job, one condition
vYMLTest1 = """
    tools:
      spades:
        rules:
          - rule_type: file_size
            nice_value: 0
            lower_bound: 0
            upper_bound: 100000000
            destination: things
    default_destination: waffles_default
    verbose: True
"""

vdictTest1_yml = {
    "tools": {
        "spades": {
            "rules": [
                {
                    "rule_type": "file_size",
                    "nice_value": 0,
                    "lower_bound": 0,
                    "upper_bound": 100000000,
                    "destination": "things"
                },
            ]
        }
    },
    'default_destination': "waffles_default"
}

# Multiple jobs, multiple conditions
vYMLTest2 ='''
    tools:
      spades:
        default_destination: waffles_default
      smalt:
        rules:
          - rule_type: file_size
            nice_value: 0
            lower_bound: 0
            upper_bound: 100000000
            fail_message: Too few reads for smalt to work
            destination: fail
          - rule_type: file_size
            nice_value: 0
            lower_bound: 100000000
            upper_bound: Infinity
            fail_message: Too few reads for smalt to work
            destination: fail
    default_destination: waffles_low
    verbose: True
'''

vdictTest2_yml = {
    "tools": {
        "spades": {
            "default_destination": "waffles_default"
        },
        "smalt": {
            "rules": [
                {
                  "rule_type": "file_size",
                  'nice_value': 0,
                  "lower_bound": 0,
                  "upper_bound": 100000000,
                  "fail_message": "Too few reads for smalt to work",
                  "destination": "fail"
                },{
                  "rule_type": "file_size",
                  'nice_value': 0,
                  "lower_bound": 100000000,
                  "upper_bound": "Infinity",
                  "fail_message": "Too few reads for smalt to work",
                  "destination": "fail"
                }
            ]
        }
    },
    'default_destination': "waffles_low"
}

# Condition with extra attribute
vYMLTest3 = '''
    tools:
      spades:
        rules:
          - rule_type: file_size
            nice_value: 0
            hax: 1337
            lower_bound: 0
            upper_bound: 100000000
            fail_message: Whats hax
            destination: fail
    default_destination: waffles_default
    verbose: True
'''

vdictTest3_yml = {
    "tools": {
        "spades": {
            "rules": [
                {
                    "rule_type": "file_size",
                    'nice_value': 0,
                    "hax": 1337,
                    "lower_bound": 0,
                    "upper_bound": 100000000,
                    "fail_message": "Whats hax",
                    "destination": "fail"
                }
            ]
        }
    },
    'default_destination': "waffles_default"
}

# Arguments type
vYMLTest4 = """
    tools:
      spades:
        rules:
          - rule_type: arguments
            nice_value: 0
            arguments:
              careful: true
            fail_message: Failure
            destination: fail
    default_destination: waffles_default
    verbose: True
"""

vdictTest4_yml = {
    "tools": {
        "spades": {
            "rules": [
                {
                    "rule_type": "arguments",
                    'nice_value': 0,
                    "arguments": {
                        "careful": True,
                    },
                    "fail_message": "Failure",
                    "destination": "fail"
                }
            ]
        }
    },
    'default_destination': "waffles_default"
}

# Records type
vYMLTest5 = '''
    tools:
      spades:
        rules:
          - rule_type: records
            nice_value: 0
            lower_bound: 0
            upper_bound: 100000000
            destination: waffles_low_4
    default_destination: waffles_default
    verbose: True
'''

vdictTest5_yml = {
    "tools": {
        "spades": {
            "rules": [
                {
                    "rule_type": "records",
                    'nice_value': 0,
                    "lower_bound": 0,
                    "upper_bound": 100000000,
                    "destination": "waffles_low_4"
                }
            ]
        }
    },
    'default_destination': "waffles_default"
}

#=====================================================Invalid XML tests==========================================================

# Empty file
ivYMLTest2 = ""

# Job without name
ivYMLTest3 = '''
    tools:
      rules:
        - rule_type: file_size
          nice_value: 0
          upper_bound: 100
          lower_bound: 0
          destination: fail
    default_destination: waffles_default
    verbose: True
'''

iv3dict = {
    'default_destination': "waffles_default"
}

# Condition missing type
ivYMLTest4 = '''
    tools:
      spades:
        rules:
          - nice_value: 0
            lower_bound: 0
            upper_bound: 0
            fail_message: No type...
            destination: fail
    default_destination: waffles_default
    verbose: True
'''

# Condition missing attribute
ivYMLTest51 = '''
    tools:
      spades:
        rules:
          - rule_type: file_size
            nice_value: 0
            upper_bound: 0
            fail_message: No type...
            destination: fail
    default_destination: waffles_default
    verbose: True
'''

# Condition missing attribute
ivYMLTest52 = '''
    tools:
      spades:
        rules:
          - rule_type: file_size
            nice_value: 0
            lower_bound: 0
            fail_message: No type...
            destination: fail
    default_destination: waffles_default
    verbose: True
'''

# Condition missing attribute
ivYMLTest53 = '''
    tools:
      spades:
        rules:
          - rule_type: file_size
            nice_value: 0
            lower_bound: 0
            upper_bound: 0
            fail_message: No type...
    default_destination: waffles_default
    verbose: True
'''

ivDict53 = {
    'default_destination': 'waffles_default',
    'tools': {
        'spades': {
            'rules': [
                {
                    'upper_bound': 0,
                    'rule_type':
                    'file_size',
                    'fail_message':
                    'No type...',
                    'nice_value': 0,
                    'lower_bound': 0,
                    'destination': 'fail'
                }
            ]
        }
    }
}

# Condition unknown type
ivYMLTest6 = '''
    tools:
      spades:
        rules:
          - rule_type: iencs
            nice_value: 0
            lower_bound: 0
            upper_bound: 0
            fail_message: No type...
            destination: fail
    default_destination: waffles_default
    verbose: True
'''

# No default destination
ivYMLTest7 = '''
    default_destination:
    verbose: True
'''

ivDict = {
    'default_destination': "waffles_default"
}

# Invalid category
ivYMLTest8= '''
    ice_cream:
    verbose: True
'''

# Tool condition fail no fail_message and apparently no nice_value
ivYMLTest91 = '''
    tools:
      spades:
        rules:
          - rule_type: file_size
            lower_bound: 0
            upper_bound: 0
            destination: fail
    default_destination: waffles_default
    verbose: True
'''

iv91dict = {
    'tools': {
        'spades': {
            'rules': [
                {
                    'lower_bound': 0,
                    'nice_value': 0,
                    'rule_type': 'file_size',
                    'upper_bound': 0,
                    'destination': 'fail',
                    'fail_message': "Invalid parameters for rule 1 in 'spades'."
                }
            ]
        }
    },
    'default_destination': "waffles_default"
}

# Tool default fail no destination
ivYMLTest11 = '''
    tools:
      spades:
        rules:
          - rule_type: file_size
            nice_value: -21
            lower_bound: 1 KB
            upper_bound: Infinity
            destination: waffles_low
        default_destination: waffles_low
    default_destination: waffles_default
    verbose: True
'''

# Arguments fail no fail_message
ivYMLTest12 = """
    tools:
      spades:
        rules:
          - rule_type: arguments
            nice_value: 0
            arguments:
              careful: true
            destination: fail
    default_destination: waffles_default
    verbose: True
"""

iv12dict = {
    "tools": {
        "spades": {
            "rules": [
                {
                    "rule_type": "arguments",
                    'nice_value': 0,
                    "arguments": {
                        "careful": True,
                    },
                    "destination": "fail",
                    "fail_message": "Invalid parameters for rule 1 in 'spades'."
                }
            ]
        }
    },
    'default_destination': "waffles_default"
}

# Arguments fail no arguments
ivYMLTest131 = """
    tools:
      spades:
        rules:
          - rule_type: arguments
            nice_value: 0
            fail_message: Something went wrong
            destination: fail
    default_destination: waffles_default
    verbose: True
"""

iv131dict = {
    'default_destination': "waffles_default"
}

# Arguments fail no destination
ivYMLTest132 = """
    tools:
      spades:
        rules:
          - rule_type: arguments
            nice_value: 0
            fail_message: Something went wrong
            arguments:
              careful: true
    default_destination: waffles_default
    verbose: True
"""

iv132dict = {
    'default_destination': 'waffles_default',
    'tools': {
        'spades': {
            'rules': [
                {
                    'arguments': {
                        'careful': True
                    },
                    'rule_type': 'arguments',
                    'destination': 'fail',
                    'fail_message': 'Something went wrong',
                    'nice_value': 0
                }
            ]
        }
    }
}

# Multiple rules in 1 job, first one failing
ivYMLTest133 ='''
    tools:
      smalt:
        rules:
          - rule_type: file_size
            nice_value: 0
            lower_bound: 0
            upper_bound: 100000000
            destination: fail
          - rule_type: file_size
            nice_value: 0
            lower_bound: 100000000
            upper_bound: Infinity
            destination: waffles_low_4
    default_destination: waffles_low
    verbose: True
'''

iv133dict = {
    "tools": {
        "smalt": {
            "rules": [
                {
                  "rule_type": "file_size",
                  'nice_value': 0,
                  "lower_bound": 0,
                  "upper_bound": 100000000,
                  "fail_message": "Invalid parameters for rule 1 in 'smalt'.",
                  "destination": "fail"
                },{
                  "rule_type": "file_size",
                  'nice_value': 0,
                  "lower_bound": 100000000,
                  "upper_bound": "Infinity",
                  "destination": "waffles_low_4"
                }
            ]
        }
    },
    'default_destination': "waffles_low"
}

# No destination and no fail_message
ivYMLTest134 = """
    tools:
      spades:
        rules:
          - rule_type: file_size
            upper_bound: 10000
            lower_bound: 0
            nice_value: 0
    default_destination: waffles_default
    verbose: True
"""

iv134dict = {
    'default_destination': 'waffles_default',
    'tools': {
        'spades': {
            'rules': [
                {
                    'rule_type': 'file_size',
                    'upper_bound': 10000,
                    'lower_bound': 0,
                    'nice_value': 0
                }
            ]
        }
    }
}

# Reversed upper and lower bounds
ivYMLTest135 = """
    tools:
      spades:
        rules:
          - rule_type: file_size
            upper_bound: 100
            lower_bound: 200
            nice_value: 0
            destination: waffles_low_4
    default_destination: waffles_default
    verbose: True
"""

iv135dict = {
    'default_destination': 'waffles_default',
    'tools': {
        'spades': {
            'rules': [
                {
                    'rule_type': 'file_size',
                    'upper_bound': 200,
                    'lower_bound': 100,
                    'nice_value': 0,
                    'destination': 'waffles_low_4'
                }
            ]
        }
    }
}

# Tool has rules category but no rules, and no tool-specific default destination
ivYMLTest136 = """
    tools:
      spades:
        rules:

    default_destination: waffles_default
    verbose: True
"""

iv136dict = {
    'default_destination': 'waffles_default'
}

# Tool is blank; no tool-specific default destination, no rules category
ivYMLTest137 = """
    tools:
      spades:

    default_destination: waffles_default
    verbose: True
"""

iv137dict = {
    'default_destination': 'waffles_default'
}
