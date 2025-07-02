import catalogData from '$lib/catalog';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = () => {
	return {
		catalogs: Object.keys(catalogData)
	};
};
