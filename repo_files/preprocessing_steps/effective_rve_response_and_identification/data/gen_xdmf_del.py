"""
Given an h5 file with voxelized RVE microstructures,
 write an xdmf file that points to datasets in the h5 file
 and allows for their visualization in Paraview

For correct visualization open .xdmf file in Paraview and choose "XDMF Reader"

Grid discretization in all datasets is assumed to be the same

Improvement: this writer may be extended to allow from FEM mesh visualization, check
https://www.xdmf.org/index.php/XDMF_Model_and_Format
"""
import xml.etree.ElementTree as et
import h5py
from pathlib import Path as path

input_file = path('random_3d_rve_1e4.h5')
# input_file = path('random_3d_rve_1e4.h5')
output_file = input_file.with_suffix('.xdmf')

def get_node_info(name, node):
    """
    Append to a "global" list all dataset names and their shapes
    datasets that include specific strings in their names may be excluded
    this fuction will be called by h5py.visititems so no need to pass any parameter
    e.g. obj.visititems(get_node_info)
    """
    if isinstance(node, h5py.Dataset):
        if '_L' not in node.name and '256x256x256' not in node.name and 'dset999' in node.name:
            datasets.append([node.name,node.shape])

datasets=[]
with h5py.File(input_file, 'r') as obj:
    obj.visititems(get_node_info)
# print(datasets)

#%% Write xml/xdmf file
dim = '{} {} {}'.format(*datasets[0][1])

xdmf = et.Element('Xdmf')
xdmf.set('Version', '2.2')

domain = et.SubElement(xdmf, 'Domain')

grid = et.SubElement(domain, 'Grid')
grid.set('Name', dim)
grid.set('Collection', '0')
grid.set('GridType', 'Uniform')

topology = et.SubElement(grid, 'Topology')
topology.set('Name', 'Topology')
topology.set('Dimensions', dim)
topology.set('TopologyType', '3DCORECTMesh')

geometry = et.SubElement(grid, 'Geometry')
geometry.set('Name', 'Geometry')
geometry.set('GeometryType', 'ORIGIN_DXDYDZ')

for name, txt in zip(['Origin','Spacing'],['0 0 0','1 1 1']):
    data_item = et.SubElement(geometry, 'DataItem')
    data_item.set('Dimensions', '3')
    data_item.set('Format', 'XML')
    data_item.set('Name', name)
    data_item.set('NumberType', 'Float')
    data_item.set('Precision', '4')
    data_item.text = txt

for dataset in datasets:
    voxel_img = dataset[0]

    attribute = et.SubElement(grid, 'Attribute')
    attribute.set('AttributeType','Scalar')
    attribute.set('Center','Cell')
    attribute.set('Name',f'material {voxel_img}')
    data_item = et.SubElement(attribute,'DataItem')
    data_item.set('Dimensions',dim)
    data_item.set('Format','HDF')
    data_item.set('NumberType','Int')
    data_item.text=f'{input_file}:{voxel_img}'

# convert xml to byte object, to allow flushing to file stream
b_xml = et.tostring(xdmf)

# Opening a file with operation mode `wb` (write + binary)
with open(output_file, 'wb') as f:
    f.write(b_xml)
# with open(output_file.with_suffix('.xml'), 'wb') as f:
#     f.write(b_xml)


