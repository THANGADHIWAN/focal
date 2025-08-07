import React, { useState } from 'react';
import { useInventory } from '../../context/InventoryContext';
import { MaterialLot, MaterialLotCreateInput, QueryParams } from '../../api/services/inventoryService';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Button } from 'primereact/button';
import { Dialog } from 'primereact/dialog';
import { InputText } from 'primereact/inputtext';
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Dropdown } from 'primereact/dropdown';

interface MaterialLotListProps {
  onFilterChange: (filters: QueryParams) => void;
  onPageChange: (page: number) => void;
  loading: boolean;
}

const MaterialLotList: React.FC<MaterialLotListProps> = ({
  onFilterChange,
  onPageChange,
  loading
}) => {
  const { materialLots, materials, createMaterialLot, updateMaterialLot } = useInventory();
  const [showDialog, setShowDialog] = useState(false);
  const [editingLot, setEditingLot] = useState<MaterialLot | null>(null);
  const [formData, setFormData] = useState<MaterialLotCreateInput>({
    material_id: 0,
    lot_number: '',
    received_date: '',
    expiry_date: '',
    received_quantity: 0,
    current_quantity: 0,
    storage_location_id: undefined,
    status: 'Available',
    remarks: ''
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (editingLot) {
      await updateMaterialLot(editingLot.id, formData);
    } else {
      await createMaterialLot(formData);
    }
    setShowDialog(false);
    resetForm();
  };

  const resetForm = () => {
    setFormData({
      material_id: 0,
      lot_number: '',
      received_date: '',
      expiry_date: '',
      received_quantity: 0,
      current_quantity: 0,
      storage_location_id: undefined,
      status: 'Available',
      remarks: ''
    });
    setEditingLot(null);
  };

  const handleEdit = (lot: MaterialLot) => {
    setEditingLot(lot);
    setFormData({
      material_id: lot.material_id,
      lot_number: lot.lot_number,
      received_date: lot.received_date || '',
      expiry_date: lot.expiry_date || '',
      received_quantity: lot.received_quantity,
      current_quantity: lot.current_quantity,
      storage_location_id: lot.storage_location_id,
      status: lot.status,
      remarks: lot.remarks || ''
    });
    setShowDialog(true);
  };

  const statusOptions = [
    { label: 'Available', value: 'Available' },
    { label: 'In Use', value: 'In Use' },
    { label: 'Depleted', value: 'Depleted' },
    { label: 'Expired', value: 'Expired' },
    { label: 'Quarantined', value: 'Quarantined' }
  ];

  return (
    <div>
      <div className="mb-4 flex justify-between items-center">
        <div className="flex gap-4">
          <Dropdown
            placeholder="Filter by material"
            onChange={(e) => onFilterChange({ material_id: e.value })}
            options={materials.map(m => ({ label: m.name, value: m.id }))}
          />
          <Dropdown
            placeholder="Filter by status"
            onChange={(e) => onFilterChange({ status: e.value })}
            options={statusOptions}
          />
        </div>
        <Button label="Add Material Lot" onClick={() => setShowDialog(true)} />
      </div>

      <DataTable
        value={materialLots}
        loading={loading}
        paginator
        rows={10}
        onPage={(e) => onPageChange(e.page + 1)}
      >
        <Column field="lot_number" header="Lot Number" sortable />
        <Column field="material.name" header="Material" sortable />
        <Column field="received_date" header="Received Date" sortable 
          body={(rowData) => new Date(rowData.received_date).toLocaleDateString()} />
        <Column field="expiry_date" header="Expiry Date" sortable
          body={(rowData) => rowData.expiry_date ? new Date(rowData.expiry_date).toLocaleDateString() : '-'} />
        <Column field="received_quantity" header="Received Qty" sortable />
        <Column field="current_quantity" header="Current Qty" sortable />
        <Column field="status" header="Status" sortable />
        <Column header="Actions" body={(rowData) => (
          <Button icon="pi pi-pencil" onClick={() => handleEdit(rowData)} />
        )} />
      </DataTable>

      <Dialog
        visible={showDialog}
        onHide={() => {
          setShowDialog(false);
          resetForm();
        }}
        header={editingLot ? 'Edit Material Lot' : 'Add Material Lot'}
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label>Material</label>
            <Dropdown
              value={formData.material_id}
              onChange={(e) => setFormData({ ...formData, material_id: e.value })}
              options={materials.map(m => ({ label: m.name, value: m.id }))}
              placeholder="Select Material"
              required
            />
          </div>

          <div>
            <label>Lot Number</label>
            <InputText
              value={formData.lot_number}
              onChange={(e) => setFormData({ ...formData, lot_number: e.target.value })}
              required
            />
          </div>

          <div>
            <label>Received Date</label>
            <Calendar
              value={formData.received_date ? new Date(formData.received_date) : null}
              onChange={(e) => setFormData({ ...formData, received_date: e.value?.toISOString() || '' })}
              showTime
            />
          </div>

          <div>
            <label>Expiry Date</label>
            <Calendar
              value={formData.expiry_date ? new Date(formData.expiry_date) : null}
              onChange={(e) => setFormData({ ...formData, expiry_date: e.value?.toISOString() || '' })}
              showTime
            />
          </div>

          <div>
            <label>Received Quantity</label>
            <InputNumber
              value={formData.received_quantity}
              onChange={(e) => setFormData({ ...formData, received_quantity: e.value || 0 })}
              required
              min={0}
            />
          </div>

          <div>
            <label>Current Quantity</label>
            <InputNumber
              value={formData.current_quantity}
              onChange={(e) => setFormData({ ...formData, current_quantity: e.value || 0 })}
              required
              min={0}
            />
          </div>

          <div>
            <label>Status</label>
            <Dropdown
              value={formData.status}
              onChange={(e) => setFormData({ ...formData, status: e.value })}
              options={statusOptions}
              required
            />
          </div>

          <div>
            <label>Remarks</label>
            <InputText
              value={formData.remarks}
              onChange={(e) => setFormData({ ...formData, remarks: e.target.value })}
            />
          </div>

          <div className="flex justify-end gap-2">
            <Button
              type="button"
              label="Cancel"
              onClick={() => {
                setShowDialog(false);
                resetForm();
              }}
            />
            <Button
              type="submit"
              label={editingLot ? 'Update' : 'Create'}
              severity="success"
            />
          </div>
        </form>
      </Dialog>
    </div>
  );
};

export default MaterialLotList;
