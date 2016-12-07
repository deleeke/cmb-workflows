import os
import sys

import smtk

# Add path to IBAMR-2d.py script
abs_path = os.path.abspath(__file__)
abs_dir = os.path.dirname(abs_path)
module_dir = os.path.join(abs_dir, os.pardir, os.pardir)
sys.path.append(module_dir)
import IBAMR2d as ibamr

#----------------------------------------------------------------------
def load_resources(resource_file):
  '''Reads and returns smtk.common.ResourceSet
  '''
  print 'loading resource file'
  resources = smtk.common.ResourceSet()
  reader = smtk.io.ResourceSetReader()
  logger = smtk.io.Logger()

  hasErrors = reader.readFile(resource_file, resources, logger)
  if hasErrors:
      print "Reader has errors:"
      print logger.convertToString()

  return resources

#----------------------------------------------------------------------
def load_attributes(model_manager, att_file):
  '''Reads and returns attribute system
  '''
  print 'loading attribute file'
  att_system = smtk.attribute.System()
  if model_manager:
    att_system.setRefModelManager(model_manager)
  reader = smtk.io.AttributeReader()
  logger = smtk.io.Logger()
  read_err = reader.read(att_system, att_file, logger)
  print 'read ok?', not read_err
  return att_system

#----------------------------------------------------------------------
class MockExportSpec:
  '''
  '''
  def __init__(self, sim_atts, export_atts=None):
    self.sim_atts = sim_atts
    self.export_atts = export_atts
    self.logger = smtk.io.Logger()

  def getSimulationAttributes(self):
    return self.sim_atts

  def getExportAttributes(self):
    return self.export_atts

  def getLogger(self):
    return self.logger


#----------------------------------------------------------------------
if __name__ == '__main__':
  if len(sys.argv) < 2:
    print
    print 'Standalone writer test'
    print 'Usage: python testwriter.py input_crf_file  [output_file]'
    print
    sys.exit(-1)

  # Load resource file
  input_crf_file = sys.argv[1]
  resource_set = load_resources(input_crf_file)

  # Initialize simuation attributes
  simbuilder_resource = resource_set.get('simbuilder')
  sim_atts = smtk.attribute.System.CastTo(simbuilder_resource)
  print 'sim_atts', sim_atts

  export_resource = resource_set.get('export')
  export_atts = smtk.attribute.System.CastTo(export_resource)
  print 'export_atts', export_atts

  # Initialize export attributes
  export_spec_att = None
  att_list = export_atts.findAttributes('ExportSpec')
  if att_list:
    export_spec_att = att_list[0]
  else:
    export_spec_defn = export_atts.findDefinition('ExportSpec')
    export_spec_att = export_atts.createAttribute(
      'ExportSpec', export_spec_defn)

  file_item = export_spec_att.findFile('OutputFile')
  output_path = None
  if len(sys.argv) > 2:
    output_path = sys.argv[2]
  else:
    input_path = os.path.abspath(input_crf_file)
    root,ext = os.path.splitext(input_path)
    output_path = '%s.ibamr' % root
  file_item.setValue(0, output_path)

  # Initialize MockExportSpec and run export script
  export_spec = MockExportSpec(sim_atts, export_atts)
  completed = ibamr.ExportCMB(export_spec)

  print 'finish, completed:', completed
