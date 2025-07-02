import { goto } from '$app/navigation';
import { base } from '$app/paths';

const gotoBase = (path: string) => {
	goto(`${base}/${path}`);
};

export { gotoBase as goto };
