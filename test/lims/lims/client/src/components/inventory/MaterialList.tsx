import React, { useState } from 'react';
import { useInventory } from '../../context/InventoryContext';
import { Material, MaterialCreateInput, QueryParams } from '../../api/services/inventoryService';
import { DataTable } from '../ui/DataTable';
import { Button } from '../ui/Button';
import { Dialog } from '../ui/Dialog';
import { Input } from '../ui/Input';
import { Select } from '../ui/Select';
import { Checkbox } from '../ui/Checkbox';

interface MaterialListProps {
  onFilterChange: (filters: QueryParams) => void;
  onPageChange: (page: number) => void;
  loading: boolean;
}

const MaterialList: React.FC<MaterialListProps> = ({
  onFilterChange,
  onPageChange,
  loading
}) => {
  const { materials, createMaterial, updateMaterial } = useInventory();
  const [showDialog, setShowDialog] = useState(false);
  const [editingMaterial, setEditingMaterial] = useState<Material | null>(null);
  const [formData, setFormData] = useState<MaterialCreateInput>({
    name: '',
    material_type: '',
    cas_number: '',
    manufacturer: '',
    grade: '',
    unit_of_measure: '',
    shelf_life_days: 0,
    is_controlled: false
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (editingMaterial) {
      await updateMaterial(editingMaterial.id, formData);
    } else {
      await createMaterial(formData);
    }
    setShowDialog(false);
    resetForm();
  };

  const resetForm = () => {
    setFormData({
      name: '',
      material_type: '',
      cas_number: '',
      manufacturer: '',
      grade: '',
      unit_of_measure: '',
      shelf_life_days: 0,
      is_controlled: false
    });
    setEditingMaterial(null);
  };

  const handleEdit = (material: Material) => {
    setEditingMaterial(material);
    setFormData({
      name: material.name,
      material_type: material.material_type || '',
      cas_number: material.cas_number || '',
      manufacturer: material.manufacturer || '',
      grade: material.grade || '',
      unit_of_measure: material.unit_of_measure || '',
      shelf_life_days: material.shelf_life_days || 0,
      is_controlled: material.is_controlled
    });
    setShowDialog(true);
  };

  const columns = [
    {
      field: 'name',
      header: 'Name',
      sortable: true
    },
    {
      field: 'material_type',
      header: 'Type',
      sortable: true
    },
    {
      field: 'cas_number',
      header: 'CAS Number'
    },
    {
      field: 'manufacturer',
      header: 'Manufacturer'
    },
    {
      field: 'grade',
      header: 'Grade'
    },
    {
      field: 'unit_of_measure',
      header: 'Unit'
    },
    {
      field: 'shelf_life_days',
      header: 'Shelf Life (Days)'
    },
    {
      field: 'is_controlled',
      header: 'Controlled',
      body: (rowData: Material) => (
        <Checkbox checked={rowData.is_controlled} disabled />
      )
    },
    {
      field: 'actions',
      header: 'Actions',
      body: (rowData: Material) => (
        <Button onClick={() => handleEdit(rowData)}>Edit</Button>
      )
    }
  ];

  return (
    <div>
      <div className="mb-4 flex justify-between items-center">
        <div className="flex gap-4">
          <Input
            placeholder="Search materials..."
            onChange={(e) => onFilterChange({ search: e.target.value })}
          />
          <Select
            placeholder="Filter by type"
            onChange={(value) => onFilterChange({ material_type: value })}
            options={[
              { label: 'All', value: '' },
              { label: 'Chemical', value: 'chemical' },
              { label: 'Biological', value: 'biological' },
              { label: 'Equipment', value: 'equipment' }
            ]}
          />
        </div>
        <Button onClick={() => setShowDialog(true)}>Add Material</Button>
      </div>

      <DataTable
        value={materials}
        columns={columns}
        loading={loading}
        paginator
        rows={10}
        onPage={(e) => onPageChange(e.page + 1)}
      />

      <Dialog
        visible={showDialog}
        onHide={() => {
          setShowDialog(false);
          resetForm();
        }}
        header={editingMaterial ? 'Edit Material' : 'Add Material'}
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label>Name</label>
            <Input
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              required
            />
          </div>

          <div>
            <label>Type</label>
            <Select
              value={formData.material_type}
              onChange={(value) => setFormData({ ...formData, material_type: value })}
              options={[
                { label: 'Chemical', value: 'chemical' },
                { label: 'Biological', value: 'biological' },
                { label: 'Equipment', value: 'equipment' }
              ]}
            />
          </div>

          <div>
            <label>CAS Number</label>
            <Input
              value={formData.cas_number}
              onChange={(e) => setFormData({ ...formData, cas_number: e.target.value })}
            />
          </div>

          <div>
            <label>Manufacturer</label>
            <Input
              value={formData.manufacturer}
              onChange={(e) => setFormData({ ...formData, manufacturer: e.target.value })}
            />
          </div>

          <div>
            <label>Grade</label>
            <Input
              value={formData.grade}
              onChange={(e) => setFormData({ ...formData, grade: e.target.value })}
            />
          </div>

          <div>
            <label>Unit of Measure</label>
            <Input
              value={formData.unit_of_measure}
              onChange={(e) => setFormData({ ...formData, unit_of_measure: e.target.value })}
            />
          </div>

          <div>
            <label>Shelf Life (Days)</label>
            <Input
              type="number"
              value={formData.shelf_life_days}
              onChange={(e) => setFormData({ ...formData, shelf_life_days: parseInt(e.target.value) })}
            />
          </div>

          <div>
            <label>Controlled Substance</label>
            <Checkbox
              checked={formData.is_controlled}
              onChange={(e) => setFormData({ ...formData, is_controlled: e.checked })}
            />
          </div>

          <div className="flex justify-end gap-2">
            <Button type="button" onClick={() => {
              setShowDialog(false);
              resetForm();
            }}>
              Cancel
            </Button>
            <Button type="submit" primary>
              {editingMaterial ? 'Update' : 'Create'}
            </Button>
          </div>
        </form>
      </Dialog>
    </div>
  );
};

export default MaterialList;
