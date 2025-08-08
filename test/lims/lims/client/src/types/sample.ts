export interface BoxLocation {
    drawer: string;
    rack: string;
    shelf: string;
    freezer: string;
    lab: string;
}

export interface SampleType {
    id: number;
    name: string;
    description?: string;
}

export interface SampleStatus {
    id: number;
    value: string;
    description: string;
}