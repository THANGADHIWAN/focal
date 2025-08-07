import axios from '../axiosConfig';
import { AxiosResponse } from 'axios';

export interface Material {
  id: number;
  name: string;
  material_type?: string;
  cas_number?: string;
  manufacturer?: string;
  grade?: string;
  unit_of_measure?: string;
  shelf_life_days?: number;
  is_controlled: boolean;
  created_at: string;
  updated_at?: string;
}

export interface MaterialLot {
  id: number;
  material_id: number;
  lot_number: string;
  received_date?: string;
  expiry_date?: string;
  received_quantity: number;
  current_quantity: number;
  storage_location_id?: number;
  status: string;
  remarks?: string;
  material: Material;
}

export interface MaterialUsageLog {
  id: number;
  material_lot_id: number;
  used_by: string;
  used_quantity: number;
  purpose?: string;
  associated_sample_id?: number;
  remarks?: string;
  used_on: string;
  material_lot: MaterialLot;
}

export interface MaterialInventoryAdjustment {
  id: number;
  material_lot_id: number;
  adjusted_by: string;
  adjustment_type: string;
  quantity: number;
  reason: string;
  remarks?: string;
  adjusted_on: string;
  material_lot: MaterialLot;
}

export interface MaterialCreateInput {
  name: string;
  material_type?: string;
  cas_number?: string;
  manufacturer?: string;
  grade?: string;
  unit_of_measure?: string;
  shelf_life_days?: number;
  is_controlled: boolean;
}

export interface MaterialLotCreateInput {
  material_id: number;
  lot_number: string;
  received_date?: string;
  expiry_date?: string;
  received_quantity: number;
  current_quantity: number;
  storage_location_id?: number;
  status: string;
  remarks?: string;
}

export interface MaterialUsageLogCreateInput {
  material_lot_id: number;
  used_by: string;
  used_quantity: number;
  purpose?: string;
  associated_sample_id?: number;
  remarks?: string;
}

export interface MaterialInventoryAdjustmentCreateInput {
  material_lot_id: number;
  adjusted_by: string;
  adjustment_type: string;
  quantity: number;
  reason: string;
  remarks?: string;
}

export interface QueryParams {
  skip?: number;
  limit?: number;
  search?: string;
  material_type?: string;
  material_id?: number;
  status?: string;
  start_date?: string;
  end_date?: string;
  adjustment_type?: string;
}

class InventoryService {
  // Materials API
  async getMaterials(params: QueryParams = {}): Promise<Material[]> {
    const response: AxiosResponse<Material[]> = await axios.get('/api/inventory/materials', { params });
    return response.data;
  }

  async createMaterial(material: MaterialCreateInput): Promise<Material> {
    const response: AxiosResponse<Material> = await axios.post('/api/inventory/materials', material);
    return response.data;
  }

  async getMaterialById(id: number): Promise<Material> {
    const response: AxiosResponse<Material> = await axios.get(`/api/inventory/materials/${id}`);
    return response.data;
  }

  async updateMaterial(id: number, material: Partial<MaterialCreateInput>): Promise<Material> {
    const response: AxiosResponse<Material> = await axios.put(`/api/inventory/materials/${id}`, material);
    return response.data;
  }

  // Material Lots API
  async getMaterialLots(params: QueryParams = {}): Promise<MaterialLot[]> {
    const response: AxiosResponse<MaterialLot[]> = await axios.get('/api/inventory/material-lots', { params });
    return response.data;
  }

  async createMaterialLot(lot: MaterialLotCreateInput): Promise<MaterialLot> {
    const response: AxiosResponse<MaterialLot> = await axios.post('/api/inventory/material-lots', lot);
    return response.data;
  }

  async getMaterialLotById(id: number): Promise<MaterialLot> {
    const response: AxiosResponse<MaterialLot> = await axios.get(`/api/inventory/material-lots/${id}`);
    return response.data;
  }

  async updateMaterialLot(id: number, lot: Partial<MaterialLotCreateInput>): Promise<MaterialLot> {
    const response: AxiosResponse<MaterialLot> = await axios.put(`/api/inventory/material-lots/${id}`, lot);
    return response.data;
  }

  // Usage Logs API
  async getUsageLogs(params: QueryParams = {}): Promise<MaterialUsageLog[]> {
    const response: AxiosResponse<MaterialUsageLog[]> = await axios.get('/api/inventory/usage-logs', { params });
    return response.data;
  }

  async createUsageLog(log: MaterialUsageLogCreateInput): Promise<MaterialUsageLog> {
    const response: AxiosResponse<MaterialUsageLog> = await axios.post('/api/inventory/usage-logs', log);
    return response.data;
  }

  // Inventory Adjustments API
  async getInventoryAdjustments(params: QueryParams = {}): Promise<MaterialInventoryAdjustment[]> {
    const response: AxiosResponse<MaterialInventoryAdjustment[]> = 
      await axios.get('/api/inventory/inventory-adjustments', { params });
    return response.data;
  }

  async createInventoryAdjustment(
    adjustment: MaterialInventoryAdjustmentCreateInput
  ): Promise<MaterialInventoryAdjustment> {
    const response: AxiosResponse<MaterialInventoryAdjustment> = 
      await axios.post('/api/inventory/inventory-adjustments', adjustment);
    return response.data;
  }
}

export const inventoryService = new InventoryService();
