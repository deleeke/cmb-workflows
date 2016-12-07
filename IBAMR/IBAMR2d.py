#=============================================================================
#
#  Copyright (c) Kitware, Inc.
#  All rights reserved.
#  See LICENSE.txt for details.
#
#  This software is distributed WITHOUT ANY WARRANTY; without even
#  the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#  PURPOSE.  See the above copyright notice for more information.
#
#=============================================================================
"""
Root writer script for IBAMR workflows
"""
import os
import sys
sys.dont_write_bytecode = True
print 'loading', os.path.basename(__file__)

import smtk

import internal
reload(internal)  # for development
from internal.writers import CardFormat, OutputComponent, Writer2D


# ---------------------------------------------------------------------
#
# Dictionary of formatters for individual output lines
# CardFormat init arguments are: (keyword, **kwargs)
# See cardformat.py for full kwargs list
#
# ---------------------------------------------------------------------

card = CardFormat
# Please order the components alphabetically in this table
format_table = {
  'toplevel' : [  
    card('MFAC', item_path='mfac'),
    card('ELEM_TYPE', item_path='element-type'),
    card('PK1_DEV_QUAD_ORDER', item_path='pk1-dev-quad-order'),
    card('PK1_DIL_QUAD_ORDER', item_path='pk1-dil-quad-order'),
      ],
  'Main': [
    card('solver', att_type='solver', item_path='solver/solver-type'),
    card(None, comment='log file parameters'),
    card('log_file_name', item_path='log/log-file'),
    card('log_all_nodes', item_path='log/log-all-nodes'),

    card(None, item_path='visualization', set_condition='viz-output'),
    card(None, comment='visualization dump parameters'),
    card('viz_writer', is_custom=True, item_path='visualization'),
    card('viz_dump_interval',
      item_path='visualization/interval', zero_condition='viz-output'),
    card('viz_dump_dirname', item_path='visualization/directory'),
    card('visit_number_procs_per_file',
      item_path='visualization/visit/number-procs-per-file'),

    card(None, item_path='restart', set_condition='restart-output'),
    card(None, comment='restart dump parameters'),
    card('restart_dump_interval',
      item_path='restart/interval', zero_condition='restart-output'),
    card('restart_dump_dirname', item_path='restart/directory'),

    card(None, item_path='hierarchy', set_condition='hierarchy-output'),
    card(None, comment='hierarchy data dump parameters'),
    card('data_dump_interval',
      item_path='hierarchy/interval', zero_condition='hierarchy-output'),
    card('data_dump_dirname', item_path='hierarchy/directory'),

    card(None, item_path='timer', set_condition='timer-output'),
    card(None, comment='timer dump parameters'),
    card('timer_dump_interval',
      item_path='timer/interval', zero_condition='timer-output'),
  ],
  'bc': [],  # empty list for velocity BCs (all custom code)
  'CartesianGeometry': [
    card('domain_boxes',
      is_custom=True, att_type='grid', item_path='base-grid-size'),
    card('x_lo', item_path='origin'),
    card('x_up', item_path='length'),
    card('periodic_dimension', item_path='periodic')
  ],
  'GriddingAlgorithm': [
    card('max_levels', item_path='max-levels'),
    card('ratio_to_coarser', is_custom=True, item_path='refinement-ratio'),
    card('largest_patch_size', is_custom=True, item_path='largest-patch-size'),
    card('smallest_patch_size', is_custom=True, item_path='smallest-patch-size'),
    card('efficiency_tolerance', item_path='efficiency-tolerance'),
    card('combine_efficiency', item_path='combine-efficiency'),
  ],
  'IBHierarchyIntegrator': [
    card('start_time', item_path='time/start-time'),
    card('end_time', item_path='time/end-time'),
    card('grow_dt', item_path='time/grow-dt'),
    card('num_cycles', item_path='hierarchy-integrator/num-cycles'),
    card('regrid_cfl_interval', item_path='hierarchy-integrator/regrid-cfl-interval'),
    card('dt_max', item_path='time/dt-max'),
    card('error_on_dt_change', item_path='time/error-on-dt-change'),
    card('enable_logging', att_type='output', item_path='enable-logging'),
  ],
  'IBFEMethod':[
    card('IB_delta_fcn', item_path='ib-delta-function'),
    card('split_forces', item_path='split-forces'),
    card('use_jump_conditions', item_path='use-jump-conditions'),
    card('use_consistent_mass_matrix', item_path='use-consistent-mass-matrix'),
    card('IB_point_density', item_path='ib-point-density'),
  ],
  'LoadBalancer': [
    card('bin_pack_method', item_path='load-balancer/bin-pack-method'),
    card('max_workload_factor', item_path='load-balancer/max-workload-factor'),
  ],
  # Common cards used by collocated and staggered solvers:
  'solver': [
    card('mu', att_type='parameters', item_path='viscosity'),
    card('rho', att_type='parameters', item_path='density'),
    card('start_time', item_path='time/start-time'),
    card('end_time', item_path='time/end-time'),
    card('grow_dt', item_path='time/grow-dt'),
    card('convective_time_stepping_type', item_path='solver/convective-ts-type'),
    card('convective_op_type', item_path='solver/convective-op-type'),
    card('convective_difference_form', item_path='solver/convective-diff-form'),
    card('normalize_pressure', item_path='solver/normalize-pressure'),
    card('cfl', item_path='solver/cfl-max'),
    card('dt_max', item_path='time/dt-max'),
    card('using_vorticity_tagging', item_path='solver/vorticity-tagging'),
    card('vorticity_rel_threshold',
      item_path='solver/vorticity-tagging/vorticity-rel-thresh'),
    card('tag_buffer', item_path='solver/vorticity-tagging/tag-buffer'),
    card('output_U', att_type='output', item_path='output-fields/velocity'),
    card('output_P', att_type='output', item_path='output-fields/pressure'),
    card('output_F', att_type='output', item_path='output-fields/body-force'),
    card('output_Omega', att_type='output', item_path='output-fields/vorticity'),
    card('output_Div_U', att_type='output', item_path='output-fields/divergence'),
    card('enable_logging', att_type='output', item_path='enable-logging'),
    card('projection_method_type',
      if_condition='collated-integrator',
      item_path='solver/solver-type/projection-method'),
    card('use_2nd_order_pressure_update',
      if_condition='collated-integrator',
      item_path='solver/solver-type/second-order-pressure-update'),
  ],
  'StandardTagAndInitialize': [
    card('tagging_method', item_path='tagging-method')
  ],
  'TimerManager': [
    card('print_exclusive', item_path='timer-manager/print-exclusive'),
    card('print_total', item_path='timer-manager/print-total'),
    card('print_threshold', item_path='timer-manager/print-threshold'),
    card('timer_list', item_path='timer-manager/timer-list'),
  ],
}
    #card('', item_path='')

# ---------------------------------------------------------------------
#
# Ordered list of components to write
# OutputComponent init arguments are: (name, **kwargs)
# See outputcomponent.py for full kwargs list
#
# ---------------------------------------------------------------------

comp = OutputComponent
# Order the components in the order to be written
component_list = [
  comp('VelocityBcCoefs_0',
    att_name='velocity0',
    custom_component_method='write_bc_coefs',
    format_list_name='bc',
    tab=16),
  comp('VelocityBcCoefs_1',
    att_name='velocity1',
    custom_component_method='write_bc_coefs',
    format_list_name='bc',
    tab=16),
  comp('VelocityBcCoefs_2',
    att_name='velocity2',
    custom_component_method='write_bc_coefs',
    format_list_name='bc',
    tab=16),
  comp('VelocityBcCoefs_3',
    att_name='velocity3',
    custom_component_method='write_bc_coefs',
    format_list_name='bc',
    tab=16),
  comp('Top Level', att_type='toplevel', custom_component_method='write_toplevel', format_list_name='toplevel'),
  comp('Main', att_type='output', custom_component_method='write_main'),
  comp('CartesianGeometry',
    att_type='geometry', custom_component_method='write_geometry'),
  comp('GriddingAlgorithm',
    custom_component_method='write_grid', att_type='grid'),
  comp('IBHierarchyIntegrator', att_type='solver'),
  comp('IBFEMethod', att_type='solver', base_item_path='fe-method', tab=26),
  comp('INSCollocatedHierarchyIntegrator',
    format_list_name='solver',
    att_type='solver',
    set_condition='collated-integrator',
    tab=29),
  comp('INSStaggeredHierarchyIntegrator',
    format_list_name='solver', att_type='solver', tab=29),
  comp('StandardTagAndInitialize', att_type='controls'),
  comp('LoadBalancer', att_type='controls'),
  comp('TimerManager', att_type='controls'),
]

# ---------------------------------------------------------------------
def ExportCMB(spec):
  '''
  Entry function, called by CMB to write export file
  '''
  writer = Writer2D(spec)
  return writer.write(component_list, format_table)
