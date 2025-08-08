import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import equipmentService from '../api/services/equipmentService';
import type { Equipment, MaintenanceRecord } from '../types/equipment';

interface EquipmentContextType {
  equipment: Equipment[];
  isLoading: boolean;
  error: string | null;
  addEquipment: (item: Omit<Equipment, 'id' | 'maintenanceHistory' | 'notes' | 'attachments'>) => Promise<Equipment>;
  updateEquipment: (id: string, updates: Partial<Equipment>) => Promise<Equipment>;
  deleteEquipment: (id: string) => Promise<void>;
  addMaintenanceRecord: (id: string, record: Omit<Equipment['maintenanceHistory'][0], 'id'>) => Promise<Equipment>;
  addNote: (id: string, content: string, user: string) => Promise<Equipment>;
  addAttachment: (id: string, file: FormData) => Promise<Equipment>;
  refreshEquipment: () => Promise<void>;
}

const EquipmentContext = createContext<EquipmentContextType | undefined>(undefined);

export function EquipmentProvider({ children }: { children: ReactNode }) {
  const [equipment, setEquipment] = useState<Equipment[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refreshEquipment = async () => {
    try {
      setIsLoading(true);
      const response = await equipmentService.getAllEquipment();
      setEquipment(response.data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load equipment');
      console.error('Error loading equipment:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    refreshEquipment();
  }, []);

  const addEquipment = async (newEquipment: Omit<Equipment, 'id' | 'maintenanceHistory' | 'notes' | 'attachments'>) => {
    try {
      const added = await equipmentService.createEquipment(newEquipment);
      setEquipment(prev => [...prev, added]);
      return added;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to add equipment';
      setError(errorMessage);
      throw new Error(errorMessage);
    }
  };

  const updateEquipment = async (id: string, updates: Partial<Equipment>) => {
    try {
      const updated = await equipmentService.updateEquipment(id, updates);
      setEquipment(prev => prev.map(item => item.id === id ? updated : item));
      return updated;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to update equipment';
      setError(errorMessage);
      throw new Error(errorMessage);
    }
  };

  const deleteEquipment = async (id: string) => {
    try {
      await equipmentService.deleteEquipment(id);
      setEquipment(prev => prev.filter(item => item.id !== id));
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to delete equipment';
      setError(errorMessage);
      throw new Error(errorMessage);
    }
  };

  const addMaintenanceRecord = async (id: string, record: Omit<MaintenanceRecord, 'id'>) => {
    try {
      const updated = await equipmentService.addMaintenanceRecord(id, record);
      setEquipment(prev => prev.map(item => item.id === id ? updated : item));
      return updated;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to add maintenance record';
      setError(errorMessage);
      throw new Error(errorMessage);
    }
  };

  const addNote = async (id: string, content: string, user: string) => {
    try {
      const updated = await equipmentService.addNote(id, { content, user });
      setEquipment(prev => prev.map(item => item.id === id ? updated : item));
      return updated;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to add note';
      setError(errorMessage);
      throw new Error(errorMessage);
    }
  };

  const addAttachment = async (id: string, file: FormData) => {
    try {
      const updated = await equipmentService.addAttachment(id, file);
      setEquipment(prev => prev.map(item => item.id === id ? updated : item));
      return updated;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to add attachment';
      setError(errorMessage);
      throw new Error(errorMessage);
    }
  };

  return (
    <EquipmentContext.Provider value={{
      equipment,
      isLoading,
      error,
      addEquipment,
      updateEquipment,
      deleteEquipment,
      addMaintenanceRecord,
      addNote,
      addAttachment,
      refreshEquipment
    }}>
      {children}
    </EquipmentContext.Provider>
  );
}

export function useEquipment() {
  const context = useContext(EquipmentContext);
  if (context === undefined) {
    throw new Error('useEquipment must be used within an EquipmentProvider');
  }
  return context;
}