import { goto } from '$app/navigation';
import { base } from '$app/paths';

const gotoBase = (path: string) => {
	const cleanPath = path.startsWith('/') ? path.slice(1) : path;
	goto(`${base}/${cleanPath}`);
};

export { gotoBase as goto };
