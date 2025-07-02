import __catalogData from './data/catalogs.json';

export interface Catalog {
	courses: Record<string, string>;
	sections: Record<string, Section[]>;
}

export interface Section {
	id: string;
	days: string[];
	start: number; // start time in minutes from midnight
	end: number; // end time in same format
	instructor: string | undefined;
}

//@ts-expect-error
const catalogData: Record<string, Catalog> = __catalogData;
export default catalogData;
