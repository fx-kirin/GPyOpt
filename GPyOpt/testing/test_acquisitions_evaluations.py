# Copyright (c) 2016, the GPyOpt Authors
# Licensed under the BSD 3-clause license (see LICENSE.txt)

import numpy as np
import os
import GPyOpt
from GPyOpt.util.general import samples_multidimensional_uniform
from GPyOpt.testing.driver import run_eval
import unittest

class TestAcquisitions(unittest.TestCase):
    '''
    Unittest for the available acquisition functions
    '''

    def setUp(self):

        # -- This file was used to generate the test files
        self.outpath = os.path.join(os.path.dirname(__file__),'test_files')
        self.is_unittest = True  # Test files were generated with this line = False

        ##
        # -- methods configuration
        ##

        model_type                  = 'GP'
        initial_design_numdata      = None
        initial_design_type         = 'random'
        acquisition_type            = 'EI'
        normalize_Y                 = True
        exact_feval                 = False
        acquisition_optimizer_type  = 'lbfgs'
        model_update_interval       = 1
        evaluator_type              = 'sequential'
        batch_size                  = 1
        num_cores                   = 1
        verbosity                   = False

        # stop conditions
        max_iter                    = 5
        max_time                    = 999
        eps                         = 1e-8


        self.methods_configs = [
                    {   'name': 'EI',
                        'model_type'                 : model_type,
                        'initial_design_numdata'     : initial_design_numdata,
                        'initial_design_type'        : initial_design_type,
                        'acquisition_type'           : 'EI',
                        'normalize_Y'                : normalize_Y,
                        'exact_feval'                : exact_feval,
                        'acquisition_optimizer_type' : acquisition_optimizer_type,
                        'model_update_interval'      : model_update_interval,
                        'verbosity'                  : verbosity,
                        'evaluator_type'             : evaluator_type,
                        'batch_size'                 : batch_size,
                        'num_cores'                  : num_cores,
                        'max_iter'                   : max_iter,
                        'max_time'                   : max_time,
                        'eps'                        : eps
                        },
                    {   'name': 'MPI',
                        'model_type'                 : model_type,
                        'initial_design_numdata'     : initial_design_numdata,
                        'initial_design_type'        : initial_design_type,
                        'acquisition_type'           : 'MPI',
                        'normalize_Y'                : normalize_Y,
                        'exact_feval'                : exact_feval,
                        'acquisition_optimizer_type' : acquisition_optimizer_type,
                        'model_update_interval'      : model_update_interval,
                        'verbosity'                  : verbosity,
                        'evaluator_type'             : evaluator_type,
                        'batch_size'                 : batch_size,
                        'num_cores'                  : num_cores,
                        'max_iter'                   : max_iter,
                        'max_time'                   : max_time,
                        'eps'                        : eps
                        },
                    {   'name': 'LCB',
                        'model_type'                 : model_type,
                        'initial_design_numdata'     : initial_design_numdata,
                        'initial_design_type'        : initial_design_type,
                        'acquisition_type'           : 'LCB',
                        'normalize_Y'                : normalize_Y,
                        'exact_feval'                : exact_feval,
                        'acquisition_optimizer_type' : acquisition_optimizer_type,
                        'model_update_interval'      : model_update_interval,
                        'verbosity'                  : verbosity,
                        'evaluator_type'             : evaluator_type,
                        'batch_size'                 : batch_size,
                        'num_cores'                  : num_cores,
                        'max_iter'                   : max_iter,
                        'max_time'                   : max_time,
                        'eps'                        : eps
                        }
                    ]

        # -- Problem setup
        np.random.seed(1)
        n_inital_design = 5
        input_dim = 5
        f_bounds = (-5,5)
        self.f_inits = samples_multidimensional_uniform([f_bounds]*input_dim,n_inital_design)
        self.f_inits = self.f_inits.reshape(1, input_dim, self.f_inits.shape[-1])

        self.problem_config = {
            'objective': GPyOpt.objective_examples.experimentsNd.gSobol(np.ones(input_dim)).f,
            'domain': [{'name': 'var_1', 'type': 'continuous', 'domain': f_bounds, 'dimensionality': input_dim}],
            'constrains': None,
            'cost_withGradients': None}


    def test_run(self):
        np.random.seed(1)
        for m_c in self.methods_configs:
            print('Testing acquisition ' + m_c['name'])
            name = m_c['name']+'_'+'acquisition_gradient_testfile'
            unittest_result = run_eval(problem_config= self.problem_config, f_inits= self.f_inits, method_config=m_c, name=name, outpath=self.outpath, time_limit=None, unittest = self.is_unittest)
            original_result = np.loadtxt(self.outpath +'/'+ name+'.txt')
            self.assertTrue((abs(original_result - unittest_result)<1e-1).all())

if __name__=='main':
    unittest.main()
