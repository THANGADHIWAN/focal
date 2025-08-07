import React, { useState } from 'react';
import { useInventory } from '../../context/InventoryContext';
import {
  MaterialInventoryAdjustment,
  MaterialInventoryAdjustmentCreateInput,
  QueryParams,
  AdjustmentType
} from '../../api/services/inventoryService';
import { DataTable } from '../ui/DataTable';
import { Button } from '../ui/Button';
import { Dialog } from '../ui/Dialog';
import { Input } from '../ui/Input';
import { Select } from '../ui/Select';

interface InventoryAdjustmentListProps {
  onFilterChange: (filters: QueryParams) => void;
  onPageChange: (page: number) => void;
  loading: boolean;
}

const InventoryAdjustmentList: React.FC<InventoryAdjustmentListProps> = ({
  onFilterChange,
  onPageChange,
  loading
}) => {
  const { inventoryAdjustments, materialLots, createInventoryAdjustment } = useInventory();
  const [showDialog, setShowDialog] = useState(false);
  const [formData, setFormData] = useState<MaterialInventoryAdjustmentCreateInput>({
    material_lot_id: 0,
    adjusted_by: '',
    adjustment_type: 'addition',
    quantity: 0,
    reason: '',
    remarks: ''
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await createInventoryAdjustment(formData);
    setShowDialog(false);
    resetForm();
  };

  const resetForm = () => {
    setFormData({
      material_lot_id: 0,
      adjusted_by: '',
      adjustment_type: 'addition',
      quantity: 0,
      reason: '',
      remarks: ''
    });
  };

  const adjustmentTypes = [
    { label: 'Addition', value: 'addition' },
    { label: 'Subtraction', value: 'subtraction' }
  ];

  return (
    <div>
      <div className="mb-4 flex justify-between items-center">
        <div className="flex gap-4">
          <Select
            placeholder="Filter by material lot"
            onChange={(value) => onFilterChange({ material_id: Number(value) })}
            options={materialLots.map(lot => ({
              label: `${lot.material.name} - ${lot.lot_number}`,
              value: lot.id.toString()
            }))}
          />
          <Select
            placeholder="Filter by type"
            onChange={(value) => onFilterChange({ adjustment_type: value })}
            options={adjustmentTypes}
          />
          <div className="flex gap-2">
            <Input
              type="datetime-local"
              placeholder="Start Date"
              onChange={(e) => onFilterChange({
                start_date: e.target.value ? new Date(e.target.value).toISOString() : undefined
              })}
            />
            <Input
              type="datetime-local"
              placeholder="End Date"
              onChange={(e) => onFilterChange({
                end_date: e.target.value ? new Date(e.target.value).toISOString() : undefined
              })}
            />
          </div>
        </div>
        <Button onClick={() => setShowDialog(true)}>New Adjustment</Button>
      </div>

      <DataTable
        value={inventoryAdjustments}
        columns={[
          { field: 'material_lot.material.name', header: 'Material' },
          { field: 'material_lot.lot_number', header: 'Lot Number' },
          {
            field: 'adjustment_type',
            header: 'Type',
            body: (row: MaterialInventoryAdjustment) => 
              row.adjustment_type.charAt(0).toUpperCase() + row.adjustment_type.slice(1)
          },
          { field: 'quantity', header: 'Quantity' },
          { field: 'adjusted_by', header: 'Adjusted By' },
          {
            field: 'adjusted_on',
            header: 'Adjusted On',
            body: (row: MaterialInventoryAdjustment) => new Date(row.adjusted_on).toLocaleString()
          },
          { field: 'reason', header: 'Reason' },
          { field: 'remarks', header: 'Remarks' }
        ]}
        loading={loading}
        paginator
        rows={10}
        onPage={(e) => onPageChange(e.page)}
      />

      <Dialog
        title="Create Inventory Adjustment"
        isOpen={showDialog}
        onClose={() => {
          setShowDialog(false);
          resetForm();
        }}
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label>Material Lot</label>
            <Select
              value={formData.material_lot_id?.toString()}
              onChange={(value) => setFormData({ ...formData, material_lot_id: Number(value) })}
              options={materialLots.map(lot => ({
                label: `${lot.material.name} - ${lot.lot_number} (Current: ${lot.current_quantity})`,
                value: lot.id.toString()
              }))}
              placeholder="Select Material Lot"
              required
            />
          </div>

          <div>
            <label>Adjustment Type</label>
            <Select
              value={formData.adjustment_type}
              onChange={(value) => setFormData({ ...formData, adjustment_type: value as AdjustmentType })}
              options={adjustmentTypes}
              required
            />
          </div>

          <div>
            <label>Quantity</label>
            <Input
              type="number"
              value={formData.quantity?.toString()}
              onChange={(e) => setFormData({ ...formData, quantity: Number(e.target.value) || 0 })}
              required
              min={0}
              step="0.01"
            />
          </div>

          <div>
            <label>Adjusted By</label>
            <Input
              type="text"
              value={formData.adjusted_by}
              onChange={(e) => setFormData({ ...formData, adjusted_by: e.target.value })}
              required
            />
          </div>

          <div>
            <label>Reason</label>
            <Input
              type="textarea"
              value={formData.reason}
              onChange={(e) => setFormData({ ...formData, reason: e.target.value })}
              required
              rows={3}
            />
          </div>

          <div>
            <label>Remarks</label>
            <Input
              type="textarea"
              value={formData.remarks}
              onChange={(e) => setFormData({ ...formData, remarks: e.target.value })}
              rows={3}
            />
          </div>

          <div className="flex justify-end gap-2">
            <Button
              type="button"
              variant="secondary"
              onClick={() => {
                setShowDialog(false);
                resetForm();
              }}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              variant="primary"
            >
              Create Adjustment
            </Button>
          </div>
        </form>
      </Dialog>
    </div>
  );
};

export default InventoryAdjustmentList;
