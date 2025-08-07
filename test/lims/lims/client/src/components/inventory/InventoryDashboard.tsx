import React, { useEffect, useState } from 'react';
import { useInventory } from '../../context/InventoryContext';
import MaterialList from './MaterialList';
import MaterialLotList from './MaterialLotList';
import UsageLogList from './UsageLogList';
import InventoryAdjustmentList from './InventoryAdjustmentList';
import { TabView, TabPanel } from '../ui/TabView';
import { QueryParams } from '../../api/services/inventoryService';

const InventoryDashboard: React.FC = () => {
  const {
    fetchMaterials,
    fetchMaterialLots,
    fetchUsageLogs,
    fetchInventoryAdjustments,
    loading
  } = useInventory();

  const [activeTab, setActiveTab] = useState(0);
  const [filters, setFilters] = useState<QueryParams>({
    skip: 0,
    limit: 10
  });

  useEffect(() => {
    // Initial data load
    const loadData = async () => {
      switch (activeTab) {
        case 0:
          await fetchMaterials(filters);
          break;
        case 1:
          await fetchMaterialLots(filters);
          break;
        case 2:
          await fetchUsageLogs(filters);
          break;
        case 3:
          await fetchInventoryAdjustments(filters);
          break;
      }
    };

    loadData();
  }, [activeTab, filters, fetchMaterials, fetchMaterialLots, fetchUsageLogs, fetchInventoryAdjustments]);

  const handlePageChange = (page: number) => {
    setFilters(prev => ({
      ...prev,
      skip: (page - 1) * prev.limit!
    }));
  };

  const handleFilterChange = (newFilters: QueryParams) => {
    setFilters(prev => ({
      ...prev,
      ...newFilters,
      skip: 0 // Reset to first page when filters change
    }));
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Inventory Management</h1>
      
      <TabView
        activeIndex={activeTab}
        onTabChange={(e) => setActiveTab(e.index)}
        className="mb-4"
      >
        <TabPanel header="Materials">
          <MaterialList
            onFilterChange={handleFilterChange}
            onPageChange={handlePageChange}
            loading={loading}
          />
        </TabPanel>
        
        <TabPanel header="Material Lots">
          <MaterialLotList
            onFilterChange={handleFilterChange}
            onPageChange={handlePageChange}
            loading={loading}
          />
        </TabPanel>
        
        <TabPanel header="Usage Logs">
          <UsageLogList
            onFilterChange={handleFilterChange}
            onPageChange={handlePageChange}
            loading={loading}
          />
        </TabPanel>
        
        <TabPanel header="Inventory Adjustments">
          <InventoryAdjustmentList
            onFilterChange={handleFilterChange}
            onPageChange={handlePageChange}
            loading={loading}
          />
        </TabPanel>
      </TabView>
    </div>
  );
};

export default InventoryDashboard;
