import React, { createContext, useContext, useState, ReactNode, useCallback } from 'react';
import API from '../api';
import {
    SampleType,
    SampleStatus,
    LabLocation,
    User,
    StorageLocation,
    Equipment,
    EquipmentType,
    EquipmentStatus,
    StorageHierarchy,
    AvailableSlot,
    HealthStatus
} from '../api/services/metadataService';

interface MetadataContextType {
    sampleTypes: SampleType[];
    sampleStatuses: SampleStatus[];
    labLocations: LabLocation[];
    users: User[];
    storageLocations: StorageLocation[];
    equipment: Equipment[];
    equipmentTypes: EquipmentType[];
    equipmentStatuses: EquipmentStatus[];
    storageHierarchy: StorageHierarchy | null;
    availableSlots: AvailableSlot[];
    healthStatus: HealthStatus | null;
    loading: boolean;
    error: string | null;
    refreshMetadata: () => Promise<void>;
    refreshEquipment: () => Promise<void>;
    refreshStorageHierarchy: () => Promise<void>;
    refreshAvailableSlots: () => Promise<void>;
    checkHealth: () => Promise<void>;
}

const MetadataContext = createContext<MetadataContextType | undefined>(undefined);

export function MetadataProvider({ children }: { children: ReactNode }) {
    const [sampleTypes, setSampleTypes] = useState<SampleType[]>([]);
    const [sampleStatuses, setSampleStatuses] = useState<SampleStatus[]>([]);
    const [labLocations, setLabLocations] = useState<LabLocation[]>([]);
    const [users, setUsers] = useState<User[]>([]);
    const [storageLocations, setStorageLocations] = useState<StorageLocation[]>([]);
    const [equipment, setEquipment] = useState<Equipment[]>([]);
    const [equipmentTypes, setEquipmentTypes] = useState<EquipmentType[]>([]);
    const [equipmentStatuses, setEquipmentStatuses] = useState<EquipmentStatus[]>([]);
    const [storageHierarchy, setStorageHierarchy] = useState<StorageHierarchy | null>(null);
    const [availableSlots, setAvailableSlots] = useState<AvailableSlot[]>([]);
    const [healthStatus, setHealthStatus] = useState<HealthStatus | null>(null);
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    const refreshMetadata = useCallback(async () => {
        setLoading(true);
        setError(null);
        
        try {
            console.log('Fetching sample types...');
            const sampleTypesResponse = await API.metadata.getSampleTypes();
            setSampleTypes(sampleTypesResponse);
            console.log('Sample types loaded:', sampleTypesResponse);

            console.log('Fetching sample statuses...');
            const sampleStatusesResponse = await API.metadata.getSampleStatuses();
            setSampleStatuses(sampleStatusesResponse);
            console.log('Sample statuses loaded:', sampleStatusesResponse);

            console.log('Fetching lab locations...');
            const labLocationsResponse = await API.metadata.getLabLocations();
            setLabLocations(labLocationsResponse);
            console.log('Lab locations loaded:', labLocationsResponse);

            console.log('Fetching users...');
            const usersResponse = await API.metadata.getUsers();
            setUsers(usersResponse);
            console.log('Users loaded:', usersResponse);

            console.log('Fetching storage locations...');
            const storageLocationsResponse = await API.metadata.getStorageLocations();
            setStorageLocations(storageLocationsResponse);
            console.log('Storage locations loaded:', storageLocationsResponse);

            console.log('Fetching equipment types...');
            const equipmentTypesResponse = await API.metadata.getEquipmentTypes();
            setEquipmentTypes(equipmentTypesResponse);
            console.log('Equipment types loaded:', equipmentTypesResponse);

            console.log('Fetching equipment statuses...');
            const equipmentStatusesResponse = await API.metadata.getEquipmentStatuses();
            setEquipmentStatuses(equipmentStatusesResponse);
            console.log('Equipment statuses loaded:', equipmentStatusesResponse);

            console.log('Fetching equipment...');
            const equipmentResponse = await API.metadata.getEquipment();
            setEquipment(equipmentResponse);
            console.log('Equipment loaded:', equipmentResponse);

        } catch (error) {
            console.error('Error loading metadata:', error);
            setError('Failed to load metadata. Please try again later.');
        } finally {
            setLoading(false);
        }
    }, []);

    const refreshEquipment = useCallback(async () => {
        try {
            console.log('Fetching equipment...');
            const equipmentResponse = await API.metadata.getEquipment();
            setEquipment(equipmentResponse);
            console.log('Equipment loaded:', equipmentResponse);
        } catch (error) {
            console.error('Error loading equipment:', error);
            setError('Failed to load equipment. Please try again later.');
        }
    }, []);

    const refreshStorageHierarchy = useCallback(async () => {
        try {
            console.log('Fetching storage hierarchy...');
            const hierarchyResponse = await API.metadata.getStorageHierarchy();
            setStorageHierarchy(hierarchyResponse);
            console.log('Storage hierarchy loaded:', hierarchyResponse);
        } catch (error) {
            console.error('Error loading storage hierarchy:', error);
            setError('Failed to load storage hierarchy. Please try again later.');
        }
    }, []);

    const refreshAvailableSlots = useCallback(async () => {
        try {
            console.log('Fetching available slots...');
            const slotsResponse = await API.metadata.getAvailableSlots();
            setAvailableSlots(slotsResponse);
            console.log('Available slots loaded:', slotsResponse);
        } catch (error) {
            console.error('Error loading available slots:', error);
            setError('Failed to load available slots. Please try again later.');
        }
    }, []);

    const checkHealth = useCallback(async () => {
        try {
            console.log('Checking health...');
            const healthResponse = await API.metadata.checkHealth();
            setHealthStatus(healthResponse);
            console.log('Health check completed:', healthResponse);
        } catch (error) {
            console.error('Error checking health:', error);
            setError('Failed to check health. Please try again later.');
        }
    }, []);

    return (
        <MetadataContext.Provider value={{
            sampleTypes,
            sampleStatuses,
            labLocations,
            users,
            storageLocations,
            equipment,
            equipmentTypes,
            equipmentStatuses,
            storageHierarchy,
            availableSlots,
            healthStatus,
            loading,
            error,
            refreshMetadata,
            refreshEquipment,
            refreshStorageHierarchy,
            refreshAvailableSlots,
            checkHealth
        }}>
            {children}
        </MetadataContext.Provider>
    );
}

export function useMetadata() {
    const context = useContext(MetadataContext);
    if (context === undefined) {
        throw new Error('useMetadata must be used within a MetadataProvider');
    }
    return context;
}
