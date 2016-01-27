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
Export script for Omega3P workflows
"""
import os
import sys
import smtk


ExportScope = type('ExportScope', (object,), dict())
# ---------------------------------------------------------------------
def ExportCMB(spec):
    '''Entry function, called by CMB to write export files

    Returns boolean indicating success
    Parameters
    ----------
    spec: Top-level object passed in from CMB
    '''
    #print 'Enter ExportCMB()'

    # Initialize scope instance to store spec values and other info
    scope = ExportScope()
    scope.logger = spec.getLogger()
    scope.sim_atts = spec.getSimulationAttributes()
    if scope.sim_atts is not None:
        scope.model_manager = scope.sim_atts.refModelManager()
        model_ents = scope.model_manager.entitiesMatchingFlags(smtk.model.MODEL_ENTITY, True)
        #print 'model_ents', model_ents
        if not model_ents:
            msg = 'No model - cannot export'
            print 'WARNING:', msg
            scope.logger.addWarning(msg)
            print 'Abort export - check logger'
            return False
        elif len(model_ents) > 1:
            msg = 'Multiple models - using first one'
            print 'WARNING:', msg
            scope.logger.addWarning(msg)
        scope.model_ent = model_ents.pop()

    scope.export_atts = spec.getExportAttributes()
    if scope.export_atts is not None:
        att_list = scope.export_atts.findAttributes('ExportSpec')
    if len(att_list) > 1:
        msg = 'More than one ExportSpec instance -- ignoring all'
        print 'WARNING:', msg
        scope.logger.addWarning(msg)
        print 'Abort export - check logger'
        return False

    # (else)
    att = att_list[0]

    # Initialize output file
    output_path = None
    item = att.find('OutputFile')
    if item is not None:
        file_item = smtk.to_concrete(item)
        output_path = file_item.value(0)
        #print 'output_path', output_path

    if not output_path:
        msg = 'No output file specified'
        print 'WARNING:', msg
        scope.logger.addWarning(msg)
        print 'Abort export - check logger'
        return False

    completed = False
    with open(output_path, 'w') as scope.output:
        write_modelinfo(scope)
        write_finiteelement(scope)
        completed = True

    print 'Export complete'
    return completed

# ---------------------------------------------------------------------
def write_modelinfo(scope):
    '''Writes ModelInfo section to output stream

    '''
    scope.output.write('ModelInfo:\n')
    scope.output.write('{\n')
    urls = scope.model_manager.stringProperty(scope.model_ent, 'url')
    if urls:
        scope.output.write('  File: %s\n\n' % urls[0])

    write_boundarycondition(scope)
    write_materials(scope)

    scope.output.write('}\n')

# ---------------------------------------------------------------------
def write_boundarycondition(scope):
    '''Writes SurfaceProperty attributes to output stream

    '''
    atts = scope.sim_atts.findAttributes('SurfaceProperty')
    if not atts:
        return

    name_list = [
        'Electric', 'Magnetic', 'Exterior', 'Impedance', 'Absorbing',
        'Waveguide', 'Periodic']

    scope.output.write('  BoundaryCondition: {\n')

    # Traverse attributes and write BoundaryCondition contents
    impedance_list = list()  # need to save these for SurfaceMaterial
    for att in atts:
        ent_string = format_entity_string(scope, att)
        if not ent_string:
            continue  # warning?

        type_item = att.findString('Type')
        index = type_item.discreteIndex(0)
        name = 'Unknown'
        if index < len(name_list):
            name = name_list[index]
        scope.output.write('    %s: %s\n' % (name, ent_string))

        # For Impedance BC, also save text to write as SurfaceMaterial
        if name == 'Impedance':
            sigma_item = att.findDouble('Sigma')
            sigma = sigma_item.value(0)
            line1 = '    ReferenceNumber: %s\n' % ent_string
            line2 = '    Sigma: %g\n' % sigma
            text = line1 + line2
            impedance_list.append(text)
    scope.output.write('  }\n')

    # Traverse impedance_list and write SurfaceMaterial entries
    for impedance_string in impedance_list:
        scope.output.write('\n')
        scope.output.write('  SurfaceMaterial: {\n')
        scope.output.write(impedance_string)
        scope.output.write('  }\n')

# ---------------------------------------------------------------------
def write_materials(scope):
    '''Writes Material attributes to output stream

    '''
    atts = scope.sim_atts.findAttributes('Material')
    if not atts:
        return

    # Traverse attributes
    for att in atts:
        ent_string = format_entity_string(scope, att)
        if not ent_string:
            continue  # warning?

        scope.output.write('\n')
        scope.output.write('  Material: {\n')
        scope.output.write('    Attribute: %s\n' % ent_string)

        # Make list of (item name, output label) to write
        items_todo = [
            ('Epsilon', 'Epsilon'),
            ('Mu', 'Mu'),
            ('ImgEpsilon', 'EpsilonImag'),
            ('ImgMu', 'MuImag')
        ]
        for item_info in items_todo:
            name, label = item_info
            item = att.findDouble(name)
            if item and item.isEnabled():
                value = item.value(0)
                scope.output.write('    %s: %g\n' % (label, value))

        scope.output.write('  }\n')


# ---------------------------------------------------------------------
def write_finiteelement(scope):
    '''Writes FiniteElement section to output stream

    '''
    scope.output.write('\n')
    scope.output.write('FiniteElement:\n')
    scope.output.write('{\n')

    att = scope.sim_atts.findAttributes('FEInfo')[0]
    order_item = att.findInt('Order')
    scope.output.write('  Order: %d\n' % order_item.value(0))

    curved_surfaces = 'off'
    curved_item = att.find('EnableCurvedSurfaces')
    if curved_item and curved_item.isEnabled():
        curved_surfaces = 'on'
    scope.output.write('  CurvedSurfaces: %s\n' % curved_surfaces)

    scope.output.write('}\n')

# ---------------------------------------------------------------------
def format_entity_string(scope, att):
    '''Generates comma-separated list of "pedigree id"s for model associations

    Returns None if no associations found
    '''
    model_ent_item = att.associations()
    if model_ent_item is None:
        return None

    # Traverse model entities
    ent_idlist = list()
    for i in range(model_ent_item.numberOfValues()):
        ent_ref = model_ent_item.value(i)
        ent = ent_ref.entity()
        prop_idlist = scope.model_manager.integerProperty(ent, 'pedigree id')
        #print 'idlist', idlist
        if prop_idlist:
            #scope.output.write(' %d' % idlist[0])
            ent_idlist.append(prop_idlist[0])

    ent_string = ','.join(str(id) for id in ent_idlist)
    return ent_string
