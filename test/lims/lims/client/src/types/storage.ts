export interface StorageLocation {
    id: number;
    name: string;
    description?: string;
    type: string;
    capacity: number;
    temperature?: number;
    humidity?: number;
}
