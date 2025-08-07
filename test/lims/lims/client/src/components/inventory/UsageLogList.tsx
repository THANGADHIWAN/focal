import React, { useState } from 'react';
import { useInventory } from '../../context/InventoryContext';
import { MaterialUsageLog, MaterialUsageLogCreateInput, QueryParams } from '../../api/services/inventoryService';
import { DataTable } from '../ui/DataTable';
import { Button } from '../ui/Button';
import { Dialog } from '../ui/Dialog';
import { Input } from '../ui/Input';
import { Select } from '../ui/Select';

interface UsageLogListProps {
  onFilterChange: (filters: QueryParams) => void;
  onPageChange: (page: number) => void;
  loading: boolean;
}

const UsageLogList: React.FC<UsageLogListProps> = ({
  onFilterChange,
  onPageChange,
  loading
}) => {
  const { usageLogs, materialLots, createUsageLog } = useInventory();
  const [showDialog, setShowDialog] = useState(false);
  const [formData, setFormData] = useState<MaterialUsageLogCreateInput>({
    material_lot_id: 0,
    used_by: '',
    used_quantity: 0,
    purpose: '',
    associated_sample_id: undefined,
    remarks: ''
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await createUsageLog(formData);
    setShowDialog(false);
    resetForm();
  };

  const resetForm = () => {
    setFormData({
      material_lot_id: 0,
      used_by: '',
      used_quantity: 0,
      purpose: '',
      associated_sample_id: undefined,
      remarks: ''
    });
  };

  return (
    <div>
      <div className="mb-4 flex justify-between items-center">
        <div className="flex gap-4">
          <Select
            placeholder="Filter by material lot"
            onChange={(value) => onFilterChange({ material_lot_id: Number(value) })}
            options={materialLots.map(lot => ({
              label: `${lot.material.name} - ${lot.lot_number}`,
              value: lot.id.toString()
            }))}
          />
          <div className="flex gap-2">
            <Input
              type="datetime-local"
              onChange={(e) => onFilterChange({
                start_date: e.target.value
              })}
              placeholder="Start Date"
            />
            <Input
              type="datetime-local"
              onChange={(e) => onFilterChange({
                end_date: e.target.value
              })}
              placeholder="End Date"
            />
          </div>
        </div>
        <Button onClick={() => setShowDialog(true)}>Log Usage</Button>
      </div>

      <DataTable
        value={usageLogs}
        loading={loading}
        paginator
        rows={10}
        onPage={(e) => onPageChange(e.page)}
        columns={[
          { field: "material_lot.material.name", header: "Material", sortable: true },
          { field: "material_lot.lot_number", header: "Lot Number", sortable: true },
          { field: "used_by", header: "Used By", sortable: true },
          { field: "used_quantity", header: "Quantity Used", sortable: true },
          { 
            field: "used_on",
            header: "Used On",
            sortable: true,
            body: (rowData) => new Date(rowData.used_on).toLocaleString()
          },
          { field: "purpose", header: "Purpose" },
          { field: "remarks", header: "Remarks" }
        ]}
      />

      <Dialog
        open={showDialog}
        onClose={() => {
          setShowDialog(false);
          resetForm();
        }}
        title="Log Material Usage"
      >
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <div>
            <label>Material Lot</label>
            <Select
              value={formData.material_lot_id.toString()}
              onChange={(value) => setFormData({ ...formData, material_lot_id: Number(value) })}
              options={materialLots.map(lot => ({
                label: `${lot.material.name} - ${lot.lot_number} (Available: ${lot.current_quantity})`,
                value: lot.id.toString()
              }))}
              placeholder="Select Material Lot"
            />
          </div>

          <div>
            <label>Used By</label>
            <Input
              value={formData.used_by}
              onChange={(e) => setFormData({ ...formData, used_by: e.target.value })}
              required
            />
          </div>

          <div>
            <label>Quantity Used</label>
            <Input
              type="number"
              value={formData.used_quantity}
              onChange={(e) => setFormData({ ...formData, used_quantity: Number(e.target.value) })}
              required
              min={0}
              step="0.01"
            />
          </div>

          <div>
            <label>Purpose</label>
            <Input
              value={formData.purpose}
              onChange={(e) => setFormData({ ...formData, purpose: e.target.value })}
            />
          </div>

          <div>
            <label>Associated Sample ID</label>
            <Input
              type="number"
              value={formData.associated_sample_id || ""}
              onChange={(e) => setFormData({ 
                ...formData, 
                associated_sample_id: e.target.value ? Number(e.target.value) : undefined 
              })}
              min={1}
            />
          </div>

          <div>
            <label>Remarks</label>
            <Input
              value={formData.remarks}
              onChange={(e) => setFormData({ ...formData, remarks: e.target.value })}
              as="textarea"
              rows={3}
            />
          </div>

          <div className="flex justify-end gap-2">
            <Button
              type="button"
              onClick={() => {
                setShowDialog(false);
                resetForm();
              }}
            >
              Cancel
            </Button>
            <Button type="submit" primary>
              Log Usage
            </Button>
          </div>verity="success"
          </form>
      </Dialog>
    </div>
  );
};

export default UsageLogList;
